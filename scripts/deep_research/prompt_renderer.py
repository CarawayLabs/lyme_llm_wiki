"""Jinja2 prompt rendering for dependency-aware research workflows."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from jinja2 import Environment, StrictUndefined


def render_prompt_template(path: Path, context: Mapping[str, object]) -> str:
    """Render a markdown prompt with StrictUndefined dependency placeholders."""

    if not path.exists():
        raise FileNotFoundError(f"Workflow prompt file not found: {path}")
    if path.suffix.lower() != ".md":
        raise ValueError(f"Workflow prompt must be a markdown file: {path}")

    template_text = path.read_text(encoding="utf-8").strip()
    if not template_text:
        raise ValueError(f"Workflow prompt file is empty: {path}")

    environment = Environment(undefined=StrictUndefined, autoescape=False)
    return environment.from_string(template_text).render(**context).strip()
