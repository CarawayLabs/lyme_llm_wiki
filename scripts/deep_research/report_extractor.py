"""Extract markdown reports from Gemini Interactions API responses."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def extract_markdown_report(interaction: Any) -> str:
    """Extract all text content from a completed Interaction response.

    Gemini Deep Research reports may appear in multiple model output steps. This
    walks those steps first, then falls back to the SDK convenience
    `output_text` property when steps are not populated.
    """

    step_text = _extract_text_from_steps(_get_value(interaction, "steps"))
    if step_text:
        return step_text

    output_text = _get_value(interaction, "output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    raise RuntimeError("Interaction completed without extractable markdown text.")


def _extract_text_from_steps(steps: Any) -> str:
    if not isinstance(steps, Iterable) or isinstance(steps, (str, bytes, dict)):
        return ""

    text_parts: list[str] = []
    for step in steps:
        step_type = _get_value(step, "type")
        if step_type and step_type not in {"model_output", "output"}:
            continue

        content = _get_value(step, "content")
        if isinstance(content, str):
            text_parts.append(content)
            continue

        if not isinstance(content, Iterable) or isinstance(content, (str, bytes, dict)):
            continue

        for part in content:
            part_type = _get_value(part, "type")
            text = _get_value(part, "text")
            if isinstance(text, str) and text.strip() and part_type in {None, "text"}:
                text_parts.append(text)

    return "\n\n".join(part.strip() for part in text_parts if part.strip()).strip()


def _get_value(source: Any, key: str) -> Any:
    if source is None:
        return None
    if isinstance(source, dict):
        return source.get(key)
    return getattr(source, key, None)
