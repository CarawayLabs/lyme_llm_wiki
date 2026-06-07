"""Client wrapper for Gemini Deep Research interactions."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass

from google import genai

from scripts.deep_research.config import GeminiSettings, ResearchJob
from scripts.deep_research.report_extractor import extract_markdown_report

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ResearchResult:
    """Completed Gemini Deep Research interaction output."""

    job_id: str
    interaction_id: str
    markdown: str


class DeepResearchClient:
    """Run and retrieve Gemini Deep Research background interactions."""

    def __init__(self, settings: GeminiSettings) -> None:
        self._settings = settings
        self._client = genai.Client(api_key=settings.api_key)

    def run(self, job: ResearchJob, prompt: str) -> ResearchResult:
        """Start a Deep Research job and wait for its completed report."""

        agent = job.agent or self._settings.default_agent
        logger.info("Starting Gemini Deep Research job %s with agent %s", job.job_id, agent)
        interaction = self._client.interactions.create(
            input=prompt,
            agent=agent,
            agent_config=self._settings.agent_config(job),
            background=True,
            store=self._settings.store,
        )

        interaction_id = getattr(interaction, "id", None)
        if not interaction_id:
            raise RuntimeError(f"Gemini did not return an interaction ID for job {job.job_id}.")

        interaction = self._wait_for_completion(interaction_id, job.job_id, interaction)
        return self._build_result(job.job_id, interaction)

    def retrieve(self, interaction_id: str, job_id: str = "retrieved") -> ResearchResult:
        """Retrieve a completed interaction by ID and extract its report."""

        logger.info("Retrieving Gemini Deep Research interaction %s", interaction_id)
        interaction = self._client.interactions.get(interaction_id)
        status = getattr(interaction, "status", "unknown")
        if status != "completed":
            raise RuntimeError(
                f"Interaction {interaction_id} is not completed. Current status: {status}"
            )

        return self._build_result(job_id, interaction)

    def _wait_for_completion(
        self, interaction_id: str, job_id: str, initial_interaction: object
    ) -> object:
        deadline = time.monotonic() + (self._settings.timeout_minutes * 60)
        last_status = getattr(initial_interaction, "status", "unknown")
        logger.info("Gemini job %s started as interaction %s", job_id, interaction_id)

        while time.monotonic() < deadline:
            interaction = self._client.interactions.get(interaction_id)
            status = getattr(interaction, "status", "unknown")

            if status != last_status:
                logger.info("Gemini job %s status changed: %s", job_id, status)
                last_status = status
            else:
                logger.debug("Gemini job %s status: %s", job_id, status)

            if status == "completed":
                logger.info("Gemini job %s completed: %s", job_id, interaction_id)
                return interaction

            if status == "failed":
                error = getattr(interaction, "error", "Unknown error")
                raise RuntimeError(f"Gemini job {job_id} failed: {error}")

            if status in {"cancelled", "incomplete", "budget_exceeded"}:
                raise RuntimeError(f"Gemini job {job_id} ended with status: {status}")

            time.sleep(self._settings.poll_interval_seconds)

        raise TimeoutError(
            f"Gemini job {job_id} timed out after "
            f"{self._settings.timeout_minutes} minutes: {interaction_id}"
        )

    def _build_result(self, job_id: str, interaction: object) -> ResearchResult:
        interaction_id = getattr(interaction, "id", "unknown")
        markdown = extract_markdown_report(interaction)
        logger.info(
            "Extracted %s markdown characters for job %s from %s",
            len(markdown),
            job_id,
            interaction_id,
        )
        return ResearchResult(job_id=job_id, interaction_id=interaction_id, markdown=markdown)
