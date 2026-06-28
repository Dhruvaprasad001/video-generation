"""
LessonPlannerAgent — stage 3 of the pipeline.

For each lesson, produces a five-act plan:
Hook → Explanation → Example → Recap → Quiz
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from models import Course, Lesson, LessonPlan
from pipeline.base import load_prompt, run_agent

logger = logging.getLogger(__name__)


class LessonPlannerAgent:
    """Plan every lesson with a narrative five-act structure."""

    async def run(self, course: Course, cache_dir: Path) -> List[LessonPlan]:
        system_prompt = load_prompt("lesson_planner")
        plans: List[LessonPlan] = []

        for module in course.modules:
            for lesson in module.lessons:
                plan = await self._plan_lesson(lesson, system_prompt, cache_dir)
                plans.append(plan)

        logger.info("LessonPlannerAgent: planned %d lesson(s)", len(plans))
        return plans

    async def _plan_lesson(
        self,
        lesson: Lesson,
        system_prompt: str,
        cache_dir: Path,
    ) -> LessonPlan:
        cache_key = lesson.title.lower().replace(" ", "_").replace("/", "_")
        cache_path = cache_dir / f"03_lesson_plan_{cache_key}.json"

        objectives_text = "\n".join(
            f"  - [{obj.bloom_level}] {obj.objective}"
            for obj in lesson.learning_objectives
        )
        user_prompt = (
            f"Plan this lesson in detail:\n\n"
            f"TITLE: {lesson.title}\n"
            f"ESTIMATED DURATION: {lesson.estimated_minutes} minutes\n"
            f"LEARNING OBJECTIVES:\n{objectives_text}\n\n"
            "Return valid JSON only — the full five-act lesson plan."
        )

        result = await run_agent(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            output_model=LessonPlan,
            cache_path=cache_path,
            label=f"LessonPlannerAgent[{lesson.title}]",
        )

        logger.info(
            "  Planned lesson '%s': %d sections, %ds total",
            lesson.title,
            len(result.sections),
            result.total_duration_seconds,
        )
        return result
