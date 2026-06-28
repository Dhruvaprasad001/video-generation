"""
Central configuration: reads from environment / .env file.
"""
from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    anthropic_model: str = "claude-sonnet-4-5"
    workspace_root: Path = Path("./output")
    log_level: str = "INFO"

    # Slide rendering
    slide_width: int = 1920
    slide_height: int = 1080

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Derived paths
PROMPTS_DIR = Path(__file__).parent / "prompts"
OUTPUT_DIR = settings.workspace_root
