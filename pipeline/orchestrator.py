"""
Pipeline orchestrator — runs all stages end to end.

Stage flow:
  1. ContentExtractionAgent   → ContentExtraction
  2. CurriculumAgent          → Course
  3. LessonPlannerAgent       → List[LessonPlan]
  4. StoryboardAgent          → List[Storyboard]
  5. SlideGeneratorAgent      → Dict[lesson_title, List[SlideAsset]]
  6. NarrationAgent           → List[NarrationScript]
  7. VideoComposerAgent       → List[LessonVideo]

Each stage saves intermediate JSON so the pipeline can be resumed
if interrupted at any point.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from models import LessonVideo
from pipeline.content_extraction import ContentExtractionAgent
from pipeline.curriculum import CurriculumAgent
from pipeline.lesson_planner import LessonPlannerAgent
from pipeline.narration import NarrationAgent
from pipeline.slide_generator import SlideGeneratorAgent
from pipeline.storyboard import StoryboardAgent
from pipeline.video_composer import VideoComposerAgent

logger = logging.getLogger(__name__)


class PipelineOrchestrator:
    """
    Orchestrates the full text → silent slide video pipeline.

    All intermediate artefacts are saved to `output_dir` for resumability.
    """

    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # instantiate all agents
        self._content_agent = ContentExtractionAgent()
        self._curriculum_agent = CurriculumAgent()
        self._planner_agent = LessonPlannerAgent()
        self._storyboard_agent = StoryboardAgent()
        self._slide_agent = SlideGeneratorAgent()
        self._narration_agent = NarrationAgent()
        self._video_agent = VideoComposerAgent()

    async def run(self, raw_text: str) -> List[LessonVideo]:
        """
        Run the full pipeline from raw text to lesson videos.
        Returns a list of LessonVideo descriptors.
        """
        cache_dir = self.output_dir / "_cache"
        cache_dir.mkdir(exist_ok=True)

        # extract structured content from raw text
        extraction = await self._content_agent.run(raw_text, cache_dir)

        # design module + lesson structure
        course = await self._curriculum_agent.run(extraction, cache_dir)

        # plan each lesson with five-act structure
        lesson_plans = await self._planner_agent.run(course, cache_dir)

        # storyboard each lesson into scenes
        storyboards = await self._storyboard_agent.run(lesson_plans, cache_dir)

        # generate HTML slides and render to PNG
        slide_assets = await self._slide_agent.run(storyboards, self.output_dir)

        # write polished narration scripts (teacher guides, text only)
        narration_scripts = await self._narration_agent.run(storyboards, self.output_dir)

        # compose silent slide videos with ffmpeg
        lesson_videos = await self._video_agent.run(
            storyboards=storyboards,
            slide_assets=slide_assets,
            narration_scripts=narration_scripts,
            output_dir=self.output_dir,
        )

        return lesson_videos
