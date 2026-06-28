"""
StoryboardAgent — stage 4 of the pipeline.

For each lesson plan, produces a scene-by-scene storyboard:
slide type, content dict, narration text, duration, and transitions.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from models import LessonPlan, Storyboard
from pipeline.base import load_prompt, run_agent

logger = logging.getLogger(__name__)


class StoryboardAgent:
    """Convert lesson plans into visual scene storyboards."""

    async def run(self, plans: List[LessonPlan], cache_dir: Path) -> List[Storyboard]:
        system_prompt = load_prompt("storyboard")
        storyboards: List[Storyboard] = []

        for plan in plans:
            board = await self._storyboard_lesson(plan, system_prompt, cache_dir)
            storyboards.append(board)

        total_scenes = sum(len(b.scenes) for b in storyboards)
        logger.info(
            "StoryboardAgent: %d storyboard(s), %d total scene(s)",
            len(storyboards),
            total_scenes,
        )
        return storyboards

    async def _storyboard_lesson(
        self,
        plan: LessonPlan,
        system_prompt: str,
        cache_dir: Path,
    ) -> Storyboard:
        cache_key = plan.lesson_title.lower().replace(" ", "_").replace("/", "_")
        cache_path = cache_dir / f"04_storyboard_{cache_key}.json"

        sections_text = "\n\n".join(
            f"[{s.section_type.upper()}] {s.title} ({s.duration_seconds}s)\n{s.content}"
            for s in plan.sections
        )
        user_prompt = (
            f"Create a detailed scene-by-scene storyboard for this lesson.\n\n"
            f"LESSON: {plan.lesson_title}\n"
            f"TOTAL DURATION: {plan.total_duration_seconds}s\n\n"
            f"LESSON SECTIONS:\n{sections_text}\n\n"
            "Return valid JSON only — the complete storyboard with all scenes."
        )

        result = await run_agent(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            output_model=Storyboard,
            cache_path=cache_path,
            label=f"StoryboardAgent[{plan.lesson_title}]",
        )

        logger.info(
            "  Storyboard '%s': %d scenes",
            plan.lesson_title,
            len(result.scenes),
        )
        return result
