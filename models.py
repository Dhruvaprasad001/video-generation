"""
Pydantic data models shared across all pipeline stages.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Core educational models
# ---------------------------------------------------------------------------


class KeyConcept(BaseModel):
    term: str
    definition: str
    example: Optional[str] = None


class ContentExtraction(BaseModel):
    title: str
    summary: str
    topics: List[str]
    subtopics: Dict[str, List[str]]  # topic -> list of subtopics
    key_concepts: List[KeyConcept]
    examples: List[str]
    prerequisites: List[str] = Field(default_factory=list)


class LearningObjective(BaseModel):
    objective: str
    bloom_level: str  # remember, understand, apply, analyze, evaluate, create


class Lesson(BaseModel):
    lesson_number: int
    title: str
    learning_objectives: List[LearningObjective]
    estimated_minutes: int = 10
    scenes: List["Scene"] = Field(default_factory=list)


class Module(BaseModel):
    module_number: int
    title: str
    description: str
    lessons: List[Lesson]


class Course(BaseModel):
    title: str
    description: str
    target_audience: str
    modules: List[Module]


# ---------------------------------------------------------------------------
# Lesson plan models
# ---------------------------------------------------------------------------


class LessonSection(BaseModel):
    section_type: str  # hook, explanation, example, recap, quiz
    title: str
    content: str
    duration_seconds: int


class LessonPlan(BaseModel):
    lesson_title: str
    sections: List[LessonSection]
    total_duration_seconds: int


# ---------------------------------------------------------------------------
# Storyboard models
# ---------------------------------------------------------------------------


class Scene(BaseModel):
    scene_number: int
    duration_seconds: int
    narration_text: str
    slide_type: str  # title, content, diagram, code, summary, quiz
    slide_content: Dict[str, Any]
    transition: str = "fade"  # fade, slide, dissolve
    section_type: str = "explanation"  # hook, explanation, example, recap, quiz


class Storyboard(BaseModel):
    lesson_title: str
    scenes: List[Scene]
    total_duration_seconds: int


# ---------------------------------------------------------------------------
# Asset models
# ---------------------------------------------------------------------------


class SlideAsset(BaseModel):
    scene_number: int
    html_path: str
    png_path: str
    width: int = 1920
    height: int = 1080


class SceneNarration(BaseModel):
    scene_number: int
    duration_seconds: int
    script: str  # polished teacher guide text for this scene


class NarrationScript(BaseModel):
    lesson_title: str
    scenes: List[SceneNarration]


class SceneClip(BaseModel):
    scene_number: int
    video_path: str
    duration_seconds: int


class LessonVideo(BaseModel):
    lesson_title: str
    video_path: str
    narration_script_path: str
    total_duration_seconds: float
    scene_count: int
