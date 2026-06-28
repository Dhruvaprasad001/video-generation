"""
CurriculumAgent — stage 2 of the pipeline.

Turns extracted content into a Module → Lesson structure
with learning objectives aligned to Bloom's taxonomy.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

from models import ContentExtraction, Course
from pipeline.base import load_prompt, run_agent

logger = logging.getLogger(__name__)


class CurriculumAgent:
    """Design a course curriculum from extracted content."""

    async def run(self, extraction: ContentExtraction, cache_dir: Path) -> Course:
        system_prompt = load_prompt("curriculum")

        user_prompt = (
            "Design a complete course curriculum based on the following extracted content. "
            "Return valid JSON only — 1 module with 2–3 lessons.\n\n"
            f"EXTRACTED CONTENT:\n{extraction.model_dump_json(indent=2)}"
        )

        result = await run_agent(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            output_model=Course,
            cache_path=cache_dir / "02_curriculum.json",
            label="CurriculumAgent",
        )

        lesson_count = sum(len(m.lessons) for m in result.modules)
        logger.info(
            "CurriculumAgent: %d module(s), %d lesson(s)",
            len(result.modules),
            lesson_count,
        )
        return result
