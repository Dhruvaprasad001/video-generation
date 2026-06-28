"""
SlideGeneratorAgent — stage 5 of the pipeline.

For each scene in a storyboard, picks the right OneCap template,
calls the LLM once to format/enrich content as JSON,
fills the template, and renders it to a 1920x1080 PNG via playwright.
"""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import List

from models import Scene, SlideAsset, Storyboard
from pipeline.base import call_llm, extract_json_from_response, load_json_if_exists, load_prompt, save_json
from pipeline.template_mapper import map_scene_to_template
from pipeline.slide_templates import render_template
from tools.mcp_tools import render_slide_to_png
from config import settings


def _safe_lesson_key(title: str) -> str:
    key = title.lower()
    key = re.sub(r'[?#&=:*<>|\\\"\']+', '', key)
    key = re.sub(r'[\s/]+', '_', key)
    key = re.sub(r'_+', '_', key)
    return key.strip('_')

logger = logging.getLogger(__name__)


class SlideGeneratorAgent:
    """Generate HTML slides via OneCap templates and render them to PNGs."""

    async def run(
        self,
        storyboards: List[Storyboard],
        output_dir: Path,
    ) -> dict[str, List[SlideAsset]]:
        """Returns a dict mapping lesson_title → list of SlideAsset."""
        system_prompt = load_prompt("slide_content")
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
        lesson_key = _safe_lesson_key(board.lesson_title)
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

        if html_path.exists():
            logger.info("  Resuming: HTML for slide %d already exists, skipping", scene.scene_number)
        else:
            html_content = await self._build_slide_html(
                scene=scene,
                lesson_title=lesson_title,
                system_prompt=system_prompt,
            )
            html_path.write_text(html_content, encoding="utf-8")

        if png_path.exists():
            return SlideAsset(
                scene_number=scene.scene_number,
                html_path=str(html_path),
                png_path=str(png_path),
            )

        result = await render_slide_to_png(
            html_path=str(html_path),
            png_path=str(png_path),
            width=settings.slide_width,
            height=settings.slide_height,
        )

        if result.startswith("ERROR:"):
            logger.warning("PNG render failed for scene %d: %s", scene.scene_number, result)

        return SlideAsset(
            scene_number=scene.scene_number,
            html_path=str(html_path),
            png_path=str(png_path),
        )

    async def _build_slide_html(
        self,
        scene: Scene,
        lesson_title: str,
        system_prompt: str,
    ) -> str:
        """
        1. Use template_mapper to normalise raw storyboard content (no LLM needed for simple types).
        2. Call LLM once to enrich/reformat content as clean JSON for the template.
        3. Fill the template and return HTML.
        """
        # Step 1: Get template type + raw normalised content
        slide_type, raw_content = map_scene_to_template(
            slide_type=scene.slide_type,
            slide_content=scene.slide_content,
            scene_number=scene.scene_number,
            lesson_title=lesson_title,
            section_type=scene.section_type,
        )

        # Step 2: LLM enrichment — ask LLM to return clean, concise JSON for this template
        enriched_content = await self._enrich_content_via_llm(
            slide_type=slide_type,
            raw_content=raw_content,
            scene=scene,
            lesson_title=lesson_title,
            system_prompt=system_prompt,
        )

        # Step 3: Render template
        return render_template(slide_type, enriched_content)

    async def _enrich_content_via_llm(
        self,
        slide_type: str,
        raw_content: dict,
        scene: Scene,
        lesson_title: str,
        system_prompt: str,
    ) -> dict:
        """
        Call LLM to reformat the storyboard content into clean, concise content
        for the chosen template. Returns the parsed JSON dict, falling back to
        raw_content if the LLM call fails.
        """
        user_prompt = (
            f"Create rich, specific slide content as JSON for a '{slide_type}' slide.\n\n"
            f"LESSON: {lesson_title}\n"
            f"SCENE: {scene.scene_number}\n"
            f"SLIDE TYPE: {slide_type}\n"
            f"SECTION TYPE: {scene.section_type}\n"
            f"DURATION: {scene.duration_seconds}s\n\n"
            f"NARRATION SCRIPT (your PRIMARY source — mine this for specific facts, names, numbers, mechanisms):\n{scene.narration_text}\n\n"
            f"RAW STORYBOARD DATA (secondary reference):\n{json.dumps(scene.slide_content, indent=2)}\n\n"
            f"INSTRUCTIONS:\n"
            f"- Extract the most specific, interesting facts from the narration\n"
            f"- For diagrams: build accurate Mermaid code reflecting the real process described\n"
            f"- For charts: use realistic domain values from the narration (not placeholder numbers)\n"
            f"- For definitions: write precise, specific definitions naming real mechanisms\n"
            f"- Never write vague filler — every word must carry real information\n"
            f"Return ONLY valid JSON with the required keys for slide_type '{slide_type}'. No explanation."
        )

        try:
            raw = await call_llm(user_prompt, system_prompt, f"SlideContent[scene {scene.scene_number}]")
            json_str = extract_json_from_response(raw)
            enriched = json.loads(json_str)
            if isinstance(enriched, dict) and enriched:
                logger.debug("  LLM enrichment OK for scene %d (%s)", scene.scene_number, slide_type)
                return enriched
        except Exception as exc:
            logger.warning(
                "LLM enrichment failed for scene %d (%s): %s — using raw content",
                scene.scene_number, slide_type, exc,
            )

        # Fall back to the normalised raw content from template_mapper
        return raw_content
