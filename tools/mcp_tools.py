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


def render_slide_to_png(
    html_path: str,
    png_path: str,
    width: int = 1920,
    height: int = 1080,
) -> str:
    """
    Screenshot an HTML slide to PNG using playwright.

    Falls back to wkhtmltoimage if playwright is not installed.
    Returns the path to the written PNG on success, or an error string.
    """
    html_path_obj = Path(html_path).resolve()
    png_path_obj = Path(png_path)
    png_path_obj.parent.mkdir(parents=True, exist_ok=True)

    # Try playwright first
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(args=["--no-sandbox", "--disable-setuid-sandbox"])
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(f"file://{html_path_obj}", wait_until="networkidle")
            page.wait_for_timeout(500)  # let CSS animations settle
            page.screenshot(path=str(png_path_obj), full_page=False)
            browser.close()

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
