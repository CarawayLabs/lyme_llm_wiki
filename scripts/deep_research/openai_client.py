"""OpenAI client for source-bound long-context synthesis workflow nodes."""

from __future__ import annotations

import logging
from dataclasses import dataclass

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
