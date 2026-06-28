# okvevo — AI Educational Course Generator

> **Text → Curriculum → HTML Slides → Silent Video + Narration Script**

okvevo takes any raw explanatory text and runs it through a multi-stage AI pipeline to produce a complete, watchable educational course — structured curriculum, beautiful slide decks, and a silent MP4 per lesson. A narration script is generated alongside each video to guide a real teacher who will later overlay their voice.

---

## Architecture

```
Text Input
↓
ContentExtractionAgent    — topics, subtopics, key concepts, examples
↓
CurriculumAgent           — Module → Lesson structure with Bloom-level objectives
↓
LessonPlannerAgent        — Hook → Explanation → Example → Recap → Quiz (per lesson)
↓
StoryboardAgent           — per lesson: scenes with duration, slide type, transitions
↓
SlideGeneratorAgent       — beautiful dark-theme HTML/CSS slides → 1920×1080 PNGs
↓
NarrationAgent            — teacher-quality narration scripts (text, no audio)
↓
VideoComposerAgent        — silent MP4 per lesson (PNG slides × duration via ffmpeg)
```

**Each stage saves intermediate JSON** — if the pipeline is interrupted, it resumes from the last completed stage automatically.

---

## Output

For each lesson the pipeline produces:

```
output/<run>/
└── <lesson_title>/
    ├── slides/
    │   ├── scene_001.html          ← self-contained HTML slide
    │   ├── scene_001.png           ← 1920×1080 PNG render
    │   ├── scene_002.html
    │   ├── scene_002.png
    │   └── ...
    ├── narration/
    │   ├── full_narration_script.txt   ← full teacher guide (plain text)
    │   ├── narration_script.json       ← per-scene JSON
    │   └── scene_001_script.txt        ← individual scene scripts
    ├── clips/
    │   ├── scene_001.mp4           ← per-scene silent video clip
    │   └── ...
    ├── lesson.mp4                  ← final assembled silent lesson video
    └── concat_list.txt
```

---

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.10+ | [python.org](https://python.org) |
| ffmpeg | any recent | `brew install ffmpeg` / `apt install ffmpeg` |
| playwright | included via pip | see below |

---

## Setup

```bash
# 1. Clone / enter the repo
cd /path/to/okvevo

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Playwright's Chromium browser (for slide rendering)
playwright install chromium

# 5. Copy the environment template and fill in your values
cp .env.example .env
```

Edit `.env`:

```dotenv
ANTHROPIC_MODEL=claude-sonnet-4-5
WORKSPACE_ROOT=./output
LOG_LEVEL=INFO
```

> **Note:** No OpenAI API key is required. The pipeline generates silent videos only. TTS/audio is intentionally excluded — a real teacher's voice will be layered on top using the narration scripts as a guide.

---

## Running the pipeline

```bash
# From a string
python main.py --text "Explain how neural networks work, covering perceptrons, \
  activation functions, backpropagation, and gradient descent"

# From a file
python main.py --file my_content.txt

# Specify a custom output directory
python main.py --text "..." --output-dir ./output/neural_networks

# Verbose (debug) logging
python main.py --text "..." --verbose
```

On completion the CLI prints a table showing each lesson's video path and narration script path.

---

## Environment variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_MODEL` | Yes | `claude-sonnet-4-5` | Claude model to use for all LLM stages |
| `WORKSPACE_ROOT` | No | `./output` | Root directory for all generated output |
| `LOG_LEVEL` | No | `INFO` | Python logging level |

---

## Project structure

```
okvevo/
├── main.py                    # CLI entrypoint
├── config.py                  # env vars, paths
├── models.py                  # Pydantic data models
├── requirements.txt
├── .env.example
├── pipeline/
│   ├── base.py                # shared LLM call, caching, JSON parsing utilities
│   ├── orchestrator.py        # runs all stages in sequence
│   ├── content_extraction.py  # stage 1
│   ├── curriculum.py          # stage 2
│   ├── lesson_planner.py      # stage 3
│   ├── storyboard.py          # stage 4
│   ├── slide_generator.py     # stage 5 — HTML + PNG
│   ├── narration.py           # stage 6 — narration scripts (text)
│   └── video_composer.py      # stage 7 — silent MP4 via ffmpeg
├── tools/
│   └── mcp_tools.py           # slide rendering MCP tool (playwright)
├── prompts/
│   ├── content_extraction.md
│   ├── curriculum.md
│   ├── lesson_planner.md
│   ├── storyboard.md
│   ├── slide_generator.md
│   └── narration.md
└── output/                    # generated courses (git-ignored)
```

---

## Resuming an interrupted run

Every pipeline stage writes a JSON cache file to `output/<run>/_cache/`.
Re-running the exact same command with the same `--output-dir` will skip
already-completed stages and resume from where it stopped.

---

## Slide rendering fallback

The pipeline tries **playwright** first (recommended). If it is not installed,
it falls back to **wkhtmltoimage**. If neither is available, HTML files are
still saved but PNG rendering is skipped — the video composer will substitute
a plain dark colour card for any missing slide PNG.

To install playwright:
```bash
pip install playwright
playwright install chromium
```

To install wkhtmltoimage (alternative):
```bash
brew install wkhtmltopdf   # macOS
apt install wkhtmltopdf    # Ubuntu/Debian
```

---

## Adding audio later

The narration scripts in each lesson's `narration/full_narration_script.txt`
are designed to be read by a real teacher while presenting `lesson.mp4`.

To add audio in the future:

1. Record the teacher reading each scene script
2. Use ffmpeg to mux audio into the existing silent video:

```bash
ffmpeg -i lesson.mp4 -i teacher_audio.mp3 \
  -c:v copy -c:a aac -shortest \
  lesson_with_audio.mp4
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ffmpeg not found` | `brew install ffmpeg` / `apt install ffmpeg` |
| `playwright not found` | `pip install playwright && playwright install chromium` |
| `claude_agent_sdk not found` | Pipeline falls back to `anthropic` SDK directly — ensure `ANTHROPIC_MODEL` is set |
| LLM returns invalid JSON | Re-run — the model occasionally mis-formats; intermediate caching means only the failed stage re-runs |
| Slide PNG is blank/wrong size | Check `slide_width` / `slide_height` in `.env`; default is 1920×1080 |
