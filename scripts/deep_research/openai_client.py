"""OpenAI client for source-bound long-context synthesis workflow nodes."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version

from openai import OpenAI

from scripts.deep_research.config import OpenAISettings

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class OpenAIResult:
    """Completed OpenAI synthesis output."""

    job_id: str
    response_id: str
    markdown: str


class OpenAISynthesisClient:
    """Run normal API synthesis calls over rendered markdown prompts."""

    def __init__(self, settings: OpenAISettings) -> None:
        self._settings = settings
        _validate_openai_httpx_compatibility()
        self._client = OpenAI(api_key=settings.api_key)

    def run(self, job_id: str, prompt: str, model: str | None = None) -> OpenAIResult:
        """Run one source-bound synthesis request and return markdown output."""

        selected_model = model or self._settings.model
        logger.info("Starting OpenAI synthesis job %s with model %s", job_id, selected_model)
        response = self._client.responses.create(
            model=selected_model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a source-bound research synthesis agent. Integrate only the "
                        "supplied artifacts unless the prompt explicitly asks otherwise. Preserve "
                        "citations, artifact IDs, contradictions, and missing-evidence notes."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )

        markdown = getattr(response, "output_text", "")
        if not isinstance(markdown, str) or not markdown.strip():
            raise RuntimeError(f"OpenAI synthesis job {job_id} returned no output_text.")

        response_id = getattr(response, "id", "unknown")
        logger.info("OpenAI synthesis job %s completed as response %s", job_id, response_id)
        return OpenAIResult(job_id=job_id, response_id=response_id, markdown=markdown.strip())


def _validate_openai_httpx_compatibility() -> None:
    """Fail early for the known OpenAI 1.36/httpx 0.28 constructor mismatch."""

    try:
        openai_version = _parse_version(version("openai"))
        httpx_version = _parse_version(version("httpx"))
    except PackageNotFoundError:
        return

    if openai_version < (1, 58, 1) and httpx_version >= (0, 28, 0):
        raise RuntimeError(
            "Installed package versions are incompatible: openai<1.58.1 with httpx>=0.28. "
            "Run `python -m pip install -r requirements.txt --upgrade` and retry."
        )


def _parse_version(value: str) -> tuple[int, int, int]:
    parts = value.split("+", 1)[0].split("-", 1)[0].split(".")
    numbers = []
    for part in parts[:3]:
        try:
            numbers.append(int(part))
        except ValueError:
            numbers.append(0)
    while len(numbers) < 3:
        numbers.append(0)
    return tuple(numbers)
