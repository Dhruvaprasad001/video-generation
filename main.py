"""
main.py — CLI entrypoint for the okvevo course generation pipeline.

Usage:
  python main.py --text "Explain how neural networks work..."
  python main.py --file path/to/content.txt
  python main.py --text "..." --output-dir ./output/my_course
"""
from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.text import Text

from config import settings

console = Console()


def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else getattr(logging, settings.log_level, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%H:%M:%S",
    )
    # quieten noisy libraries
    for noisy in ("httpx", "httpcore", "anthropic", "openai"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


async def _run_pipeline(raw_text: str, output_dir: Path, verbose: bool) -> None:
    from pipeline.orchestrator import PipelineOrchestrator

    _configure_logging(verbose)
    logger = logging.getLogger("main")

    console.print(
        Panel(
            Text("okvevo · AI Course Generator", style="bold white"),
            subtitle="text → curriculum → slides → silent video + narration script",
            style="bold purple",
        )
    )
    console.print(f"[dim]Output directory:[/dim] {output_dir.resolve()}")
    console.print(f"[dim]Model:[/dim] {settings.anthropic_model}")
    console.print()

    orchestrator = PipelineOrchestrator(output_dir=output_dir)

    stages = [
        ("1/7", "Content Extraction",  "Analysing text, extracting topics & concepts"),
        ("2/7", "Curriculum Design",   "Designing module & lesson structure"),
        ("3/7", "Lesson Planning",     "Building five-act lesson plans"),
        ("4/7", "Storyboarding",       "Mapping lessons to visual scenes"),
        ("5/7", "Slide Generation",    "Rendering HTML slides → PNGs"),
        ("6/7", "Narration Scripts",   "Writing teacher narration guides"),
        ("7/7", "Video Composition",   "Assembling silent MP4 videos with ffmpeg"),
    ]

    console.print("[bold green]Starting pipeline…[/bold green]")
    console.print()

    # We run the full pipeline as a single async call — progress is shown
    # via logging to console.  Rich progress bar would need hooks into each
    # agent, which is out of scope for this POC.
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    ) as progress:
        task = progress.add_task("[cyan]Running pipeline…", total=None)

        lesson_videos = await orchestrator.run(raw_text)

        progress.update(task, description="[green]Pipeline complete!")

    # Print results table
    console.print()
    console.print("[bold green]Course generation complete![/bold green]")
    console.print()

    table = Table(title="Generated Lessons", show_lines=True)
    table.add_column("Lesson", style="cyan", no_wrap=False, max_width=40)
    table.add_column("Duration", justify="right", style="yellow")
    table.add_column("Scenes", justify="right")
    table.add_column("Video", style="dim", no_wrap=False, max_width=50)
    table.add_column("Narration Script", style="dim", no_wrap=False, max_width=50)

    for lv in lesson_videos:
        mins, secs = divmod(int(lv.total_duration_seconds), 60)
        table.add_row(
            lv.lesson_title,
            f"{mins}m {secs:02d}s",
            str(lv.scene_count),
            lv.video_path,
            lv.narration_script_path,
        )

    console.print(table)
    console.print()
    console.print(f"[bold]Output directory:[/bold] {output_dir.resolve()}")
    console.print("[dim]Narration scripts are in each lesson's narration/ subfolder.[/dim]")


@click.command()
@click.option(
    "--text", "-t",
    default=None,
    help="Raw input text to generate a course from.",
)
@click.option(
    "--file", "-f",
    default=None,
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="Path to a text file containing the input content.",
)
@click.option(
    "--output-dir", "-o",
    default=None,
    type=click.Path(file_okay=False, writable=True),
    help="Directory to write output to (default: ./output/<timestamp>).",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging.")
def main(text: str | None, file: str | None, output_dir: str | None, verbose: bool) -> None:
    """
    Generate a complete educational course from raw text.

    Outputs: structured curriculum JSON, HTML slides, PNG renders,
    narration scripts, and a silent MP4 per lesson.
    """
    # resolve input
    if text and file:
        console.print("[red]Error:[/red] provide either --text or --file, not both.")
        sys.exit(1)

    if file:
        raw_text = Path(file).read_text(encoding="utf-8")
    elif text:
        raw_text = text
    else:
        console.print("[red]Error:[/red] provide --text or --file.")
        sys.exit(1)

    if not raw_text.strip():
        console.print("[red]Error:[/red] input text is empty.")
        sys.exit(1)

    # resolve output directory
    if output_dir:
        out_path = Path(output_dir)
    else:
        import time
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        out_path = settings.workspace_root / timestamp

    asyncio.run(_run_pipeline(raw_text, out_path, verbose))


if __name__ == "__main__":
    main()
