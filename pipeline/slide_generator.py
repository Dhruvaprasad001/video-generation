"""
SlideGeneratorAgent — stage 5 of the pipeline.

For each scene in a storyboard, generates a self-contained HTML slide
(beautiful dark-theme design) and renders it to a 1920×1080 PNG via playwright.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from models import Scene, SlideAsset, Storyboard
from pipeline.base import call_llm, load_json_if_exists, load_prompt, save_json
from tools.mcp_tools import render_slide_to_png
from config import settings

logger = logging.getLogger(__name__)


class SlideGeneratorAgent:
    """Generate HTML slides and render them to PNGs."""

    async def run(
        self,
        storyboards: List[Storyboard],
        output_dir: Path,
    ) -> dict[str, List[SlideAsset]]:
        """
        Returns a dict mapping lesson_title → list of SlideAsset.
        """
        system_prompt = load_prompt("slide_generator")
        all_assets: dict[str, List[SlideAsset]] = {}

        for board in storyboards:
            assets = await self._generate_lesson_slides(board, system_prompt, output_dir)
            all_assets[board.lesson_title] = assets

        return all_assets

    async def _generate_lesson_slides(
        self,
        board: Storyboard,
        system_prompt: str,
        output_dir: Path,
    ) -> List[SlideAsset]:
        lesson_key = board.lesson_title.lower().replace(" ", "_").replace("/", "_")
        slides_dir = output_dir / lesson_key / "slides"
        slides_dir.mkdir(parents=True, exist_ok=True)

        assets: List[SlideAsset] = []

        for scene in board.scenes:
            asset = await self._generate_scene_slide(
                scene=scene,
                lesson_title=board.lesson_title,
                system_prompt=system_prompt,
                slides_dir=slides_dir,
            )
            assets.append(asset)
            logger.info(
                "  Slide %d/%d: %s → %s",
                scene.scene_number,
                len(board.scenes),
                asset.html_path,
                asset.png_path,
            )

        logger.info(
            "SlideGeneratorAgent: '%s' — %d slides generated",
            board.lesson_title,
            len(assets),
        )
        return assets

    async def _generate_scene_slide(
        self,
        scene: Scene,
        lesson_title: str,
        system_prompt: str,
        slides_dir: Path,
    ) -> SlideAsset:
        html_path = slides_dir / f"scene_{scene.scene_number:03d}.html"
        png_path = slides_dir / f"scene_{scene.scene_number:03d}.png"

        # Resume: skip LLM call if HTML already exists (PNG may still need rendering)
        if html_path.exists():
            logger.info("  Resuming: HTML for slide %d already exists, skipping LLM", scene.scene_number)
            html_content = None  # signal to skip generation
        else:
            html_content = await self._request_slide_html(
                scene=scene,
                lesson_title=lesson_title,
                system_prompt=system_prompt,
            )
            html_path.write_text(html_content, encoding="utf-8")

        # Skip PNG render if it already exists
        if png_path.exists():
            return SlideAsset(
                scene_number=scene.scene_number,
                html_path=str(html_path),
                png_path=str(png_path),
            )

        # Render HTML → PNG
        result = await render_slide_to_png(
            html_path=str(html_path),
            png_path=str(png_path),
            width=settings.slide_width,
            height=settings.slide_height,
        )

        if result.startswith("ERROR:"):
            logger.warning("PNG render failed for scene %d: %s", scene.scene_number, result)
            # We still return an asset pointing to the HTML — video composer will handle missing PNGs
            return SlideAsset(
                scene_number=scene.scene_number,
                html_path=str(html_path),
                png_path=str(png_path),  # may not exist
            )

        return SlideAsset(
            scene_number=scene.scene_number,
            html_path=str(html_path),
            png_path=str(png_path),
        )

    async def _request_slide_html(
        self,
        scene: Scene,
        lesson_title: str,
        system_prompt: str,
    ) -> str:
        import json

        user_prompt = (
            f"Generate a beautiful HTML slide for this scene.\n\n"
            f"LESSON: {lesson_title}\n"
            f"SCENE NUMBER: {scene.scene_number}\n"
            f"SLIDE TYPE: {scene.slide_type}\n"
            f"SECTION: {scene.section_type}\n"
            f"DURATION: {scene.duration_seconds}s\n\n"
            f"SLIDE CONTENT:\n{json.dumps(scene.slide_content, indent=2)}\n\n"
            f"NARRATION (for context — do NOT show on slide):\n{scene.narration_text}\n\n"
            "Return ONLY the complete HTML — no explanation, no markdown fences. "
            "Start directly with <!DOCTYPE html>."
        )

        raw = await call_llm(user_prompt, system_prompt, f"SlideGen[scene {scene.scene_number}]")

        # Extract HTML — strip any accidental markdown fences
        raw = raw.strip()
        if raw.startswith("```"):
            lines = raw.split("\n")
            # drop first and last fence lines
            lines = [l for l in lines if not l.strip().startswith("```")]
            raw = "\n".join(lines)

        if not raw.startswith("<!DOCTYPE") and "<!DOCTYPE" in raw:
            raw = raw[raw.index("<!DOCTYPE"):]

        return raw.strip()
