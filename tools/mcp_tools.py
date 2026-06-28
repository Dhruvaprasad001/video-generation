"""
MCP tool definitions used by pipeline agents.

Exposes slide_to_png (playwright screenshot) as an MCP tool so
Claude agents can call it during execution.  No TTS or audio tools —
the pipeline produces silent slide videos only.
"""
from __future__ import annotations

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Slide rendering (HTML → PNG via playwright)
# ---------------------------------------------------------------------------


async def render_slide_to_png(
    html_path: str,
    png_path: str,
    width: int = 1920,
    height: int = 1080,
) -> str:
    """
    Screenshot an HTML slide to PNG using playwright async API.
    Falls back to wkhtmltoimage if playwright is not installed.
    Returns the path to the written PNG on success, or an error string.
    """
    html_path_obj = Path(html_path).resolve()
    png_path_obj = Path(png_path)
    png_path_obj.parent.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )
            page = await browser.new_page(viewport={"width": width, "height": height})
            await page.goto(f"file://{html_path_obj}", wait_until="networkidle")
            await page.wait_for_timeout(500)
            await page.screenshot(path=str(png_path_obj), full_page=False)
            await browser.close()

        logger.info("Rendered slide (playwright): %s → %s", html_path, png_path)
        return str(png_path_obj)

    except ImportError:
        logger.warning("playwright not available, trying wkhtmltoimage fallback")
    except Exception as exc:
        logger.warning("playwright failed (%s), trying wkhtmltoimage fallback", exc)

    # Fallback: wkhtmltoimage
    try:
        result = subprocess.run(
            [
                "wkhtmltoimage",
                "--width", str(width),
                "--height", str(height),
                "--quality", "95",
                str(html_path_obj),
                str(png_path_obj),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            logger.info("Rendered slide (wkhtmltoimage): %s → %s", html_path, png_path)
            return str(png_path_obj)
        error_msg = f"wkhtmltoimage failed: {result.stderr}"
        logger.error(error_msg)
        return f"ERROR: {error_msg}"
    except FileNotFoundError:
        msg = (
            "Neither playwright nor wkhtmltoimage is available. "
            "Run: pip install playwright && playwright install chromium"
        )
        logger.error(msg)
        return f"ERROR: {msg}"
    except Exception as exc:
        logger.error("wkhtmltoimage error: %s", exc)
        return f"ERROR: {exc}"


# ---------------------------------------------------------------------------
# MCP server (optional — used when agents need tool access via MCP protocol)
# ---------------------------------------------------------------------------


def build_mcp_server():
    """
    Create an MCP server exposing the slide rendering tool.
    Returns None if claude_agent_sdk is not available.
    """
    try:
        from claude_agent_sdk import create_sdk_mcp_server, tool as mcp_tool

        @mcp_tool
        def slide_to_png(
            html_path: str,
            png_path: str,
            width: int = 1920,
            height: int = 1080,
        ) -> str:
            """Screenshot an HTML slide to a PNG file using playwright."""
            return render_slide_to_png(html_path, png_path, width, height)

        return create_sdk_mcp_server(
            name="okvevo_tools",
            version="1.0.0",
            tools=[slide_to_png],
        )

    except ImportError:
        logger.warning("claude_agent_sdk not available — MCP server not created")
        return None


# ---------------------------------------------------------------------------
# Slide animation recording (HTML → MP4 via playwright video API)
# ---------------------------------------------------------------------------


async def record_slide_to_video(
    html_path: str,
    mp4_path: str,
    duration_seconds: int,
    animation_seconds: int = 0,
    width: int = 1920,
    height: int = 1080,
) -> str:
    """
    Record a slide HTML file to an MP4 clip.

    Records the full scene duration so that all continuous looping animations
    (floating orbs, pulsing glows, drifting particles) play throughout.
    animation_seconds=0 means record the full duration_seconds.

    Returns the path to the written MP4 on success, or an error string prefixed
    with "ERROR:" so callers can detect failure and fall back to PNG-based clips.
    """
    import shutil
    import tempfile

    html_path_obj = Path(html_path).resolve()
    mp4_path_obj = Path(mp4_path)
    mp4_path_obj.parent.mkdir(parents=True, exist_ok=True)

    # Record full duration (animation_seconds=0 means no cap)
    record_duration = duration_seconds if animation_seconds == 0 else min(animation_seconds, duration_seconds)
    hold_seconds = duration_seconds - record_duration

    try:
        from playwright.async_api import async_playwright

        ffmpeg_bin = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"

        with tempfile.TemporaryDirectory() as clips_dir:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    args=["--no-sandbox", "--disable-setuid-sandbox"]
                )
                context = await browser.new_context(
                    viewport={"width": width, "height": height},
                    record_video_dir=clips_dir,
                    record_video_size={"width": width, "height": height},
                )
                page = await context.new_page()
                await page.goto(f"file://{html_path_obj}", wait_until="networkidle")
                await page.wait_for_timeout(300)                    # let animations begin
                await page.wait_for_timeout(record_duration * 1000) # full scene duration
                await context.close()
                await browser.close()

            recorded_files = list(Path(clips_dir).glob("*.webm")) + list(Path(clips_dir).glob("*.mp4"))
            if not recorded_files:
                return "ERROR: playwright recorded no video file"

            recorded = recorded_files[0]

            # Intermediate path for the raw animation clip before we extend it
            anim_mp4 = mp4_path_obj.with_suffix(".anim.mp4")

            if recorded.suffix == ".webm":
                result = subprocess.run(
                    [
                        ffmpeg_bin, "-y", "-i", str(recorded),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        "-preset", "fast", "-an",
                        str(anim_mp4),
                    ],
                    capture_output=True, text=True, timeout=duration_seconds + 180,
                )
                if result.returncode != 0:
                    return f"ERROR: ffmpeg webm→mp4 failed: {result.stderr[-300:]}"
            else:
                shutil.copy2(str(recorded), str(anim_mp4))

        # Extend by cloning the last frame for hold_seconds
        if hold_seconds > 0:
            result = subprocess.run(
                [
                    ffmpeg_bin, "-y", "-i", str(anim_mp4),
                    "-vf", f"tpad=stop_mode=clone:stop_duration={hold_seconds}",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-preset", "fast", "-an",
                    str(mp4_path_obj),
                ],
                capture_output=True, text=True, timeout=duration_seconds + 180,
            )
            if result.returncode != 0:
                logger.warning(
                    "tpad extension failed (%s) — using animation clip only",
                    result.stderr[-200:],
                )
                shutil.copy2(str(anim_mp4), str(mp4_path_obj))
        else:
            shutil.copy2(str(anim_mp4), str(mp4_path_obj))

        anim_mp4.unlink(missing_ok=True)

        logger.info(
            "Recorded slide video (playwright): %s → %s  [%ds anim + %ds hold]",
            html_path, mp4_path, record_duration, hold_seconds,
        )
        return str(mp4_path_obj)

    except ImportError:
        return "ERROR: playwright not available for video recording"
    except Exception as exc:
        logger.warning("playwright video recording failed: %s", exc)
        return f"ERROR: {exc}"
