"""
Shared base utilities for all pipeline agents.

Every agent:
  - loads its system prompt from prompts/
  - calls the LLM via claude_agent_sdk query()
  - saves intermediate JSON to disk for resumability
  - returns a Pydantic model
"""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, TypeVar

from pydantic import BaseModel

from config import PROMPTS_DIR, settings

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def load_prompt(name: str) -> str:
    """Load a prompt from the prompts/ directory."""
    path = PROMPTS_DIR / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def save_json(data: Any, path: Path) -> None:
    """Persist any JSON-serialisable object to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, BaseModel):
        text = data.model_dump_json(indent=2)
    else:
        text = json.dumps(data, indent=2, default=str)
    path.write_text(text, encoding="utf-8")
    logger.debug("Saved intermediate output: %s", path)


def load_json_if_exists(path: Path) -> Optional[Dict]:
    """Return parsed JSON if the file exists, else None (for resumability)."""
    if path.exists():
        logger.info("Resuming from cached file: %s", path)
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def extract_json_from_response(raw: str) -> str:
    """
    Strip markdown fences and leading/trailing noise from an LLM response
    so we get a clean JSON string.
    """
    # Remove ```json ... ``` or ``` ... ``` fences
    raw = re.sub(r"```(?:json)?\s*", "", raw)
    raw = re.sub(r"```", "", raw)
    raw = raw.strip()

    # Find the outermost { ... } or [ ... ]
    for start_char, end_char in [('{', '}'), ('[', ']')]:
        start = raw.find(start_char)
        end = raw.rfind(end_char)
        if start != -1 and end != -1 and end > start:
            return raw[start:end + 1]

    return raw


async def call_llm(
    user_prompt: str,
    system_prompt: str,
    label: str = "agent",
) -> str:
    """
    Call Claude and return the concatenated text response.

    Strategy (in order of preference):
    1. If ANTHROPIC_API_KEY is set, use the direct Anthropic SDK — it is fast,
       stateless, and does not require a running Claude Code CLI process.
    2. Otherwise, attempt claude_agent_sdk (requires an authenticated Claude
       Code CLI in PATH). If the CLI is not authenticated or any error occurs,
       raise so the caller knows the operation failed rather than silently
       returning empty content.
    """
    import os

    if os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1":
        return await _call_anthropic_directly(user_prompt, system_prompt, label)

    try:
        from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

        options = ClaudeAgentOptions(
            system_prompt=system_prompt,
            model=settings.anthropic_model,
        )

        responses: List[str] = []
        async for msg in query(prompt=user_prompt, options=options):
            if isinstance(msg, ResultMessage):
                if msg.is_error:
                    # The CLI ran but returned an error (e.g. auth failure).
                    # Re-raise so we don't silently return empty content.
                    error_detail = msg.result or "unknown CLI error"
                    raise RuntimeError(
                        f"Claude Code CLI returned is_error=True: {error_detail}. "
                        "Set ANTHROPIC_API_KEY to use the direct Anthropic SDK instead."
                    )
                if msg.result:
                    responses.append(msg.result)
            elif hasattr(msg, "content") and msg.content:
                for block in (msg.content if isinstance(msg.content, list) else [msg.content]):
                    if hasattr(block, "text"):
                        responses.append(block.text)
                    else:
                        responses.append(str(block))

        result = "\n".join(responses)
        logger.debug("[%s] LLM response length: %d chars", label, len(result))
        return result

    except ImportError:
        logger.warning("claude_agent_sdk not found — falling back to anthropic SDK directly")
        return await _call_anthropic_directly(user_prompt, system_prompt, label)


async def _call_anthropic_directly(user_prompt: str, system_prompt: str, label: str) -> str:
    """
    Direct Anthropic API call — fallback when claude_agent_sdk is unavailable.
    Routes through AWS Bedrock when CLAUDE_CODE_USE_BEDROCK=1, otherwise uses
    the direct Anthropic API (requires ANTHROPIC_API_KEY).
    """
    import os
    import anthropic

    use_bedrock = os.getenv("CLAUDE_CODE_USE_BEDROCK", "0") == "1"

    if use_bedrock:
        # Let the standard AWS credential chain resolve AWS_ACCESS_KEY_ID /
        # AWS_SECRET_ACCESS_KEY from the environment — passing them explicitly
        # conflicts when the Anthropic client also finds an api_key somewhere.
        client = anthropic.AsyncAnthropicBedrock(
            aws_region=os.getenv("AWS_REGION", "us-east-1"),
        )
    else:
        client = anthropic.AsyncAnthropic()

    message = await client.messages.create(
        model=settings.anthropic_model,
        max_tokens=8096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    text = ""
    for block in message.content:
        if hasattr(block, "text"):
            text += block.text
    logger.debug("[%s] Anthropic direct response: %d chars", label, len(text))
    return text


async def run_agent(
    user_prompt: str,
    system_prompt: str,
    output_model: Type[T],
    cache_path: Optional[Path] = None,
    label: str = "agent",
) -> T:
    """
    Generic agent runner:
    1. Check cache (resumability)
    2. Call LLM
    3. Parse response into output_model
    4. Save to cache
    5. Return model instance
    """
    # Resume from cache if available
    if cache_path:
        cached = load_json_if_exists(cache_path)
        if cached:
            try:
                return output_model.model_validate(cached)
            except Exception as exc:
                logger.warning("Cache validation failed (%s), re-running agent", exc)

    raw = await call_llm(user_prompt, system_prompt, label)
    json_str = extract_json_from_response(raw)

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as exc:
        logger.error("[%s] Failed to parse JSON: %s\nRaw response:\n%s", label, exc, raw[:500])
        raise ValueError(f"Agent {label} returned invalid JSON: {exc}") from exc

    result = output_model.model_validate(data)

    if cache_path:
        save_json(result, cache_path)

    return result
