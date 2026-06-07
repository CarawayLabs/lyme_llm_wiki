"""Orchestration for running configured Gemini Deep Research jobs."""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.deep_research.client import DeepResearchClient
from scripts.deep_research.config import GeminiSettings, ResearchJob, RunConfig
from scripts.deep_research.file_io import WrittenReport, read_prompt, write_report, write_run_summary

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RunOutcome:
    """Summary of a completed multi-job Deep Research run."""

    reports: list[WrittenReport]
    failures: list[dict[str, Any]]
    summary_path: Path


def run_configured_research(settings: GeminiSettings, run_config: RunConfig) -> RunOutcome:
    """Run all enabled jobs from a config, parallelizing when possible."""

    jobs = run_config.enabled_jobs
    if not jobs:
        raise ValueError(f"No enabled Deep Research jobs found in {run_config.config_path}.")

    logger.info("Running %s enabled Deep Research job(s)", len(jobs))
    reports: list[WrittenReport] = []
    failures: list[dict[str, Any]] = []

    worker_count = min(run_config.max_parallel, len(jobs))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        future_to_job = {
            executor.submit(_run_one_job, settings, run_config.output_dir, job): job for job in jobs
        }
        for future in as_completed(future_to_job):
            job = future_to_job[future]
            try:
                reports.append(future.result())
            except Exception as exc:
                logger.exception("Deep Research job %s failed", job.job_id)
                failures.append(
                    {
                        "job_id": job.job_id,
                        "input_file": str(job.input_file),
                        "error": str(exc),
                    }
                )

    reports.sort(key=lambda report: report.job_id)
    failures.sort(key=lambda failure: failure["job_id"])
    summary_path = write_run_summary(run_config.output_dir, reports, failures)
    logger.info("Wrote Deep Research run summary to %s", summary_path)

    if failures:
        logger.warning("%s Deep Research job(s) failed", len(failures))

    return RunOutcome(reports=reports, failures=failures, summary_path=summary_path)


def _run_one_job(settings: GeminiSettings, output_dir: Path, job: ResearchJob) -> WrittenReport:
    logger.info("Reading Deep Research prompt for job %s from %s", job.job_id, job.input_file)
    prompt = read_prompt(job.input_file)
    client = DeepResearchClient(settings)
    result = client.run(job, prompt)
    written_report = write_report(output_dir, job, result)
    logger.info("Saved Deep Research job %s report to %s", job.job_id, written_report.output_file)
    return written_report
