"""
template_mapper.py — maps Scene → template type + normalised content dict.

The LLM storyboard generates varied key names (e.g. "main_title", "title", "headline").
This module normalises all of them to the keys each template actually expects.
"""
from __future__ import annotations

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def map_scene_to_template(
    slide_type: str,
    slide_content: Dict[str, Any],
    scene_number: int = 0,
    lesson_title: str = "",
    section_type: str = "explanation",
) -> tuple[str, Dict[str, Any]]:
    """
    Return (resolved_slide_type, normalised_content_dict).

    resolved_slide_type may differ from slide_type when a requested type
    has no matching template (falls back to 'content').
    """
    resolved_type = _resolve_type(slide_type, section_type)
    normaliser = _NORMALISERS.get(resolved_type, _normalise_content)
    normalised = normaliser(slide_content, lesson_title=lesson_title, scene_number=scene_number)
    logger.debug(
        "template_mapper: scene %d %s→%s, keys=%s",
        scene_number, slide_type, resolved_type, list(normalised.keys()),
    )
    return resolved_type, normalised


# ---------------------------------------------------------------------------
# Type resolution
# ---------------------------------------------------------------------------

_VALID_TYPES = {"title", "content", "two_column", "definition", "diagram", "code", "chart", "summary", "quiz"}

_SECTION_TYPE_HINTS = {
    "hook": "title",
    "recap": "summary",
    "quiz": "quiz",
}


def _resolve_type(slide_type: str, section_type: str) -> str:
    t = str(slide_type).lower().strip()
    if t in _VALID_TYPES:
        return t
    # Try section_type hint
    hint = _SECTION_TYPE_HINTS.get(section_type.lower(), "")
    if hint:
        return hint
    # Fuzzy matching
    if "diagram" in t or "flow" in t or "graph" in t:
        return "diagram"
    if "code" in t or "snippet" in t or "program" in t:
        return "code"
    if "chart" in t or "bar" in t or "line" in t or "graph" in t:
        return "chart"
    if "definition" in t or "term" in t or "glossary" in t:
        return "definition"
    if "summary" in t or "recap" in t or "takeaway" in t:
        return "summary"
    if "two" in t or "column" in t or "compare" in t:
        return "two_column"
    if "title" in t or "intro" in t or "cover" in t:
        return "title"
    if "quiz" in t or "question" in t or "check" in t:
        return "quiz"
    return "content"


# ---------------------------------------------------------------------------
# Per-template normalisers
# ---------------------------------------------------------------------------

def _first(*keys: str, src: dict, default: Any = "") -> Any:
    """Return the first truthy value found under any of the given keys."""
    for k in keys:
        v = src.get(k)
        if v:
            return v
    return default


def _to_list(value: Any) -> list:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        lines = [l.strip().lstrip("•-* ") for l in value.split("\n") if l.strip()]
        return lines if lines else [value]
    if isinstance(value, dict):
        return [f"{k}: {v}" for k, v in value.items()]
    return [str(value)] if value else []


def _normalise_title(src: dict, lesson_title: str = "", scene_number: int = 0) -> dict:
    return {
        "headline": _first("headline", "main_title", "title", "heading", src=src, default=lesson_title or "Untitled"),
        "subtitle": _first("subtitle", "description", "sub_title", "visual_hint", src=src, default=""),
        "lesson_number": _first("lesson_number", "scene_number", src=src, default=scene_number or ""),
        "module_name": _first("module_name", "module", "course", src=src, default=""),
    }


def _normalise_content(src: dict, lesson_title: str = "", scene_number: int = 0) -> dict:
    bullets_raw = _first("bullets", "points", "key_points", "items", "content", src=src, default=[])
    return {
        "heading": _first("heading", "title", "headline", src=src, default=""),
        "bullets": _to_list(bullets_raw),
        "section_label": _first("section_label", "section", "highlight", "label", "tag", src=src, default=""),
    }


def _normalise_two_column(src: dict, lesson_title: str = "", scene_number: int = 0) -> dict:
    left = _first("left_bullets", "left", "bullets", "points", src=src, default=[])
    right = _first("right_content", "right", "description", "details", "visual_hint", src=src, default="")
    return {
        "heading": _first("heading", "title", "headline", src=src, default=""),
        "left_bullets": _to_list(left),
        "right_content": right,
        "section_label": _first("section_label", "section", "label", src=src, default=""),
    }


def _normalise_definition(src: dict, lesson_title: str = "", scene_number: int = 0) -> dict:
    return {
        "term": _first("term", "title", "word", "concept", src=src, default=""),
        "definition": _first("definition", "body", "description", "meaning", "content", src=src, default=""),
        "example": _first("example", "illustration", "instance", src=src, default=""),
    }


def _normalise_diagram(src: dict, lesson_title: str = "", scene_number: int = 0) -> dict:
    mermaid = _first("mermaid_code", "mermaid", "diagram_code", "code", src=src, default="")
    if not mermaid:
        # Build a placeholder mermaid graph from elements if present
        elements = src.get("elements", [])
        if elements and isinstance(elements, list):
            lines = ["flowchart LR"]
            for i, el in enumerate(elements[:6]):
                label = str(el).replace('"', "'")[:40]
                if i == 0:
                    lines.append(f'  A["{label}"]')
                else:
                    prev = chr(ord("A") + i - 1)
                    curr = chr(ord("A") + i)
                    lines.append(f'  {prev} --> {curr}["{label}"]')
            mermaid = "\n".join(lines)
        else:
            desc = _first("description", "content", "title", src=src, default="Diagram")
            mermaid = f'graph LR\n  A["{desc}"]'
    return {
        "heading": _first("heading", "title", "headline", src=src, default=""),
        "mermaid_code": mermaid,
        "caption": _first("caption", "note", "annotation", src=src, default=""),
    }


def _normalise_code(src: dict, lesson_title: str = "", scene_number: int = 0) -> dict:
    return {
        "heading": _first("heading", "title", "headline", src=src, default=""),
        "language": _first("language", "lang", src=src, default="python"),
        "code": _first("code", "code_block", "snippet", "source", src=src, default="# No code provided"),
        "explanation": _first("explanation", "annotation", "description", "note", src=src, default=""),
    }


def _normalise_chart(src: dict, lesson_title: str = "", scene_number: int = 0) -> dict:
    labels = src.get("labels", src.get("categories", src.get("x_labels", [])))
    values = src.get("values", src.get("data", src.get("y_values", [])))
    return {
        "heading": _first("heading", "title", "headline", src=src, default=""),
        "chart_type": _first("chart_type", "type", src=src, default="bar"),
        "labels": _to_list(labels) if not isinstance(labels, list) else labels,
        "values": values if isinstance(values, list) else [],
        "caption": _first("caption", "note", src=src, default=""),
    }


def _normalise_summary(src: dict, lesson_title: str = "", scene_number: int = 0) -> dict:
    takeaways_raw = _first("takeaways", "bullets", "key_points", "points", "items", src=src, default=[])
    return {
        "heading": _first("heading", "title", "headline", src=src, default="Key Takeaways"),
        "takeaways": _to_list(takeaways_raw),
        "next_lesson": _first("next_lesson", "next", "next_topic", "upcoming", src=src, default=""),
    }


def _normalise_quiz(src: dict, lesson_title: str = "", scene_number: int = 0) -> dict:
    return {
        "question": _first("question", "prompt", "title", src=src, default=""),
        "options": _first("options", "choices", "answers", src=src, default=[]),
        "correct": _first("correct", "correct_answer", "answer", src=src, default=""),
        "explanation": _first("explanation", "reason", "rationale", src=src, default=""),
    }


_NORMALISERS = {
    "title":      _normalise_title,
    "content":    _normalise_content,
    "two_column": _normalise_two_column,
    "definition": _normalise_definition,
    "diagram":    _normalise_diagram,
    "code":       _normalise_code,
    "chart":      _normalise_chart,
    "summary":    _normalise_summary,
    "quiz":       _normalise_quiz,
}
