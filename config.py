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

    # AWS Bedrock
    claude_code_use_bedrock: str = "0"
    aws_region: str = "us-east-1"
    aws_bearer_token_bedrock: str = ""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    claude_code_subagent_model: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()

# Derived paths
PROMPTS_DIR = Path(__file__).parent / "prompts"
OUTPUT_DIR = settings.workspace_root
