"""
ContentExtractionAgent — stage 1 of the pipeline.

Takes raw text and extracts structured educational content:
topics, subtopics, key concepts, examples, and prerequisites.
"""
from __future__ import annotations

import logging
from pathlib import Path

from models import ContentExtraction
from pipeline.base import load_prompt, run_agent

logger = logging.getLogger(__name__)


class ContentExtractionAgent:
    """Extract topics, concepts, and examples from raw input text."""

    async def run(self, raw_text: str, cache_dir: Path) -> ContentExtraction:
        # load the focused extraction system prompt
        system_prompt = load_prompt("content_extraction")

        user_prompt = (
            "Please analyse the following educational text and extract structured content "
            "according to your instructions. Return valid JSON only.\n\n"
            f"--- BEGIN TEXT ---\n{raw_text}\n--- END TEXT ---"
        )

        result = await run_agent(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            output_model=ContentExtraction,
            cache_path=cache_dir / "01_content_extraction.json",
            label="ContentExtractionAgent",
        )

        logger.info(
            "ContentExtractionAgent: extracted %d topics, %d key concepts",
            len(result.topics),
            len(result.key_concepts),
        )
        return result
