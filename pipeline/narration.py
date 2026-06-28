"""
NarrationAgent — stage 6 of the pipeline.

Refines each scene's raw narration text into a polished, teacher-quality
script suitable for a real instructor to read while presenting the slides.

No audio is generated here — this is text output only.
The scripts are saved as:
  - Per-scene .txt files
  - A combined JSON summary for the lesson
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from models import Scene, SceneNarration, NarrationScript, Storyboard
from pipeline.base import call_llm, load_json_if_exists, load_prompt, save_json

logger = logging.getLogger(__name__)


class NarrationAgent:
    """Write teacher-quality narration scripts for every scene."""

    async def run(
        self,
        storyboards: List[Storyboard],
        output_dir: Path,
    ) -> List[NarrationScript]:
        system_prompt = load_prompt("narration")
        all_scripts: List[NarrationScript] = []

        for board in storyboards:
            script = await self._narrate_lesson(board, system_prompt, output_dir)
            all_scripts.append(script)

        return all_scripts

    async def _narrate_lesson(
        self,
        board: Storyboard,
        system_prompt: str,
        output_dir: Path,
    ) -> NarrationScript:
        lesson_key = board.lesson_title.lower().replace(" ", "_").replace("/", "_")
        narration_dir = output_dir / lesson_key / "narration"
        narration_dir.mkdir(parents=True, exist_ok=True)

        # Check for cached combined script
        cache_path = narration_dir / "narration_script.json"
        cached = load_json_if_exists(cache_path)
        if cached:
            try:
                return NarrationScript.model_validate(cached)
            except Exception as exc:
                logger.warning("Narration cache invalid (%s), regenerating", exc)

        scene_narrations: List[SceneNarration] = []

        for scene in board.scenes:
            scene_script = await self._narrate_scene(scene, system_prompt, narration_dir)
            scene_narrations.append(scene_script)

        narration_script = NarrationScript(
            lesson_title=board.lesson_title,
            scenes=scene_narrations,
        )

        # save combined JSON
        save_json(narration_script, cache_path)

        # also save a human-readable full script .txt
        self._save_readable_script(narration_script, narration_dir)

        logger.info(
            "NarrationAgent: '%s' — %d scene scripts written to %s",
            board.lesson_title,
            len(scene_narrations),
            narration_dir,
        )
        return narration_script

    async def _narrate_scene(
        self,
        scene: Scene,
        system_prompt: str,
        narration_dir: Path,
    ) -> SceneNarration:
        txt_path = narration_dir / f"scene_{scene.scene_number:03d}_script.txt"

        # Resume if script already exists
        if txt_path.exists():
            logger.info("  Resuming narration for scene %d", scene.scene_number)
            return SceneNarration(
                scene_number=scene.scene_number,
                duration_seconds=scene.duration_seconds,
                script=txt_path.read_text(encoding="utf-8").strip(),
            )

        words_needed = int(scene.duration_seconds * 130 / 60)  # ~130 wpm
        user_prompt = (
            f"Refine this narration into a polished teacher script.\n\n"
            f"SCENE {scene.scene_number} | TYPE: {scene.slide_type} | SECTION: {scene.section_type}\n"
            f"DURATION: {scene.duration_seconds} seconds (~{words_needed} words at 130 wpm)\n\n"
            f"RAW NARRATION:\n{scene.narration_text}\n\n"
            "Return only the refined script text — no JSON, no markdown, no metadata."
        )

        refined = await call_llm(user_prompt, system_prompt, f"NarrationAgent[scene {scene.scene_number}]")
        refined = refined.strip()

        # persist individual scene script
        txt_path.write_text(refined, encoding="utf-8")

        return SceneNarration(
            scene_number=scene.scene_number,
            duration_seconds=scene.duration_seconds,
            script=refined,
        )

    def _save_readable_script(
        self,
        narration_script: NarrationScript,
        narration_dir: Path,
    ) -> None:
        """Write the full lesson narration as a single readable .txt file."""
        lines = [
            f"NARRATION SCRIPT: {narration_script.lesson_title}",
            "=" * 60,
            "",
        ]
        for sn in narration_script.scenes:
            lines += [
                f"[Scene {sn.scene_number} — {sn.duration_seconds}s]",
                "",
                sn.script,
                "",
                "-" * 40,
                "",
            ]
        full_txt = "\n".join(lines)
        script_path = narration_dir / "full_narration_script.txt"
        script_path.write_text(full_txt, encoding="utf-8")
        logger.info("  Full narration script saved: %s", script_path)
