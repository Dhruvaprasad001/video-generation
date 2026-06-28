"""
VideoComposerAgent — stage 7 of the pipeline (final stage).

Assembles PNGs + scene durations into a silent MP4 per lesson using ffmpeg.

Pipeline:
  1. For each scene: create a short clip — PNG held for duration_seconds
  2. Write a concat list file
  3. Concatenate all clips into a single lesson MP4 with fade transitions
  4. No audio track — the video is intentionally silent (a real teacher's
     voice will be overlaid later using the narration scripts as a guide)
"""
from __future__ import annotations

import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List

from models import LessonVideo, NarrationScript, SlideAsset, Storyboard

logger = logging.getLogger(__name__)

FFMPEG_LOGLEVEL = "warning"


def _find_ffmpeg() -> str:
    """Return the ffmpeg binary path, checking common install locations."""
    # Check PATH first
    found = shutil.which("ffmpeg")
    if found:
        return found
    # Homebrew on Apple Silicon and Intel
    for candidate in ["/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg"]:
        if os.path.isfile(candidate):
            return candidate
    raise RuntimeError(
        "ffmpeg is not installed or not on PATH. "
        "Install with: brew install ffmpeg  (macOS) or  apt install ffmpeg  (Linux)"
    )


FFMPEG_BIN = None  # resolved lazily on first use


class VideoComposerAgent:
    """Compose silent slide videos from PNGs using ffmpeg."""

    async def run(
        self,
        storyboards: List[Storyboard],
        slide_assets: dict[str, List[SlideAsset]],
        narration_scripts: List[NarrationScript],
        output_dir: Path,
    ) -> List[LessonVideo]:
        videos: List[LessonVideo] = []

        narration_map = {ns.lesson_title: ns for ns in narration_scripts}

        for board in storyboards:
            assets = slide_assets.get(board.lesson_title, [])
            narration = narration_map.get(board.lesson_title)
            video = self._compose_lesson_video(board, assets, narration, output_dir)
            videos.append(video)

        return videos

    # ------------------------------------------------------------------
    # Entry point — reads like English, no logic inline
    # ------------------------------------------------------------------

    def _compose_lesson_video(
        self,
        board: Storyboard,
        assets: List[SlideAsset],
        narration: "NarrationScript | None",
        output_dir: Path,
    ) -> LessonVideo:
        lesson_key = board.lesson_title.lower().replace(" ", "_").replace("/", "_")
        lesson_dir = output_dir / lesson_key
        lesson_dir.mkdir(parents=True, exist_ok=True)
        video_path = lesson_dir / "lesson.mp4"

        # skip if already composed
        if video_path.exists():
            logger.info("Resuming: video already exists for '%s'", board.lesson_title)
            return LessonVideo(
                lesson_title=board.lesson_title,
                video_path=str(video_path),
                narration_script_path=self._narration_script_path(lesson_dir),
                total_duration_seconds=float(board.total_duration_seconds),
                scene_count=len(board.scenes),
            )

        # build one clip per scene
        asset_map = {a.scene_number: a for a in assets}
        scene_clips = self._compose_scene_clips(board.scenes, asset_map, lesson_dir)

        # concatenate all scene clips into final MP4
        self._concatenate_clips(scene_clips, video_path)

        narration_script_path = self._narration_script_path(lesson_dir)

        logger.info(
            "VideoComposerAgent: '%s' → %s (%d scenes, %ds)",
            board.lesson_title,
            video_path,
            len(board.scenes),
            board.total_duration_seconds,
        )

        return LessonVideo(
            lesson_title=board.lesson_title,
            video_path=str(video_path),
            narration_script_path=narration_script_path,
            total_duration_seconds=float(board.total_duration_seconds),
            scene_count=len(board.scenes),
        )

    # ------------------------------------------------------------------
    # Scene clip creation
    # ------------------------------------------------------------------

    def _compose_scene_clips(
        self,
        scenes: list,
        asset_map: dict,
        lesson_dir: Path,
    ) -> List[Path]:
        clips_dir = lesson_dir / "clips"
        clips_dir.mkdir(exist_ok=True)
        clips: List[Path] = []

        for scene in scenes:
            clip_path = self._make_scene_clip(scene, asset_map, clips_dir)
            clips.append(clip_path)

        return clips

    def _make_scene_clip(self, scene, asset_map: dict, clips_dir: Path) -> Path:
        clip_path = clips_dir / f"scene_{scene.scene_number:03d}.mp4"
        if clip_path.exists():
            return clip_path

        asset = asset_map.get(scene.scene_number)
        png_path = asset.png_path if asset else None

        if png_path and Path(png_path).exists():
            self._ffmpeg_png_to_clip(png_path, clip_path, scene.duration_seconds)
        else:
            logger.warning(
                "Scene %d: PNG not found (%s) — generating colour card fallback",
                scene.scene_number,
                png_path,
            )
            self._ffmpeg_colour_card_clip(clip_path, scene.duration_seconds, scene.scene_number)

        return clip_path

    # ------------------------------------------------------------------
    # ffmpeg helpers
    # ------------------------------------------------------------------

    def _ffmpeg_png_to_clip(self, png_path: str, clip_path: Path, duration: int) -> None:
        """Convert a single PNG to a video clip of `duration` seconds (silent)."""
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(png_path),
            "-c:v", "libx264",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
            "-preset", "fast",
            "-an",  # no audio
            "-loglevel", FFMPEG_LOGLEVEL,
            str(clip_path),
        ]
        self._run_ffmpeg(cmd, f"PNG→clip scene {clip_path.stem}")

    def _ffmpeg_colour_card_clip(
        self,
        clip_path: Path,
        duration: int,
        scene_number: int,
    ) -> None:
        """Generate a plain dark-coloured fallback clip when PNG is missing."""
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"color=c=0x0f1117:size=1920x1080:rate=25:duration={duration}",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "fast",
            "-an",
            "-loglevel", FFMPEG_LOGLEVEL,
            str(clip_path),
        ]
        self._run_ffmpeg(cmd, f"colour card fallback scene {scene_number}")

    def _concatenate_clips(self, clips: List[Path], output_path: Path) -> None:
        """Concatenate scene clips using ffmpeg concat demuxer (lossless, no re-encode)."""
        if not clips:
            raise ValueError("No clips to concatenate")

        # write concat list file
        concat_file = output_path.parent / "concat_list.txt"
        lines = [f"file '{clip.resolve()}'\n" for clip in clips]
        concat_file.write_text("".join(lines), encoding="utf-8")

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "fast",
            "-an",
            "-loglevel", FFMPEG_LOGLEVEL,
            str(output_path),
        ]
        self._run_ffmpeg(cmd, "concatenate lesson video")

    def _run_ffmpeg(self, cmd: List[str], label: str) -> None:
        """Run an ffmpeg command, raising a clear error if it fails."""
        global FFMPEG_BIN
        if FFMPEG_BIN is None:
            FFMPEG_BIN = _find_ffmpeg()
        # Replace the 'ffmpeg' placeholder at index 0 with the resolved binary
        cmd[0] = FFMPEG_BIN
        logger.debug("ffmpeg [%s]: %s", label, " ".join(cmd))
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode != 0:
                logger.error("ffmpeg [%s] stderr:\n%s", label, result.stderr)
                raise RuntimeError(
                    f"ffmpeg failed for '{label}' (exit {result.returncode}):\n{result.stderr[-500:]}"
                )
        except FileNotFoundError as exc:
            raise RuntimeError(
                "ffmpeg is not installed or not on PATH. "
                "Install with: brew install ffmpeg  (macOS) or  apt install ffmpeg  (Linux)"
            ) from exc

    def _narration_script_path(self, lesson_dir: Path) -> str:
        """Return the expected path of the full narration script text file."""
        p = lesson_dir / "narration" / "full_narration_script.txt"
        return str(p) if p.exists() else str(lesson_dir / "narration")
