"""Filesystem helpers for Deep Research prompt and report files."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from scripts.deep_research.config import ResearchJob

if TYPE_CHECKING:
    from scripts.deep_research.client import ResearchResult


@dataclass(frozen=True)
class WrittenReport:
    """Metadata for a report written to disk."""

    job_id: str
    interaction_id: str
    input_file: str
    output_file: str
    provider: str = "gemini"


def read_prompt(path: Path) -> str:
    """Read and validate a markdown research prompt."""

    if not path.exists():
        raise FileNotFoundError(f"Deep Research prompt file not found: {path}")
    if path.suffix.lower() != ".md":
        raise ValueError(f"Deep Research prompt must be a markdown file: {path}")

    prompt = path.read_text(encoding="utf-8").strip()
    if not prompt:
        raise ValueError(f"Deep Research prompt file is empty: {path}")

    return prompt


def write_report(output_dir: Path, job: ResearchJob, result: "ResearchResult") -> WrittenReport:
    """Write one completed Deep Research report to a timestamped markdown file."""

    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = job.output_prefix or job.safe_output_name
    report_path = output_dir / f"{prefix}_{timestamp}.md"

    header = (
        f"# Gemini Deep Research Report: {job.job_id}\n\n"
        f"- Interaction ID: `{result.interaction_id}`\n"
        f"- Input file: `{job.input_file}`\n"
        f"- Generated at: `{datetime.now().isoformat(timespec='seconds')}`\n\n"
        "---\n\n"
    )
    report_path.write_text(header + result.markdown.strip() + "\n", encoding="utf-8")

    return WrittenReport(
        job_id=job.job_id,
        interaction_id=result.interaction_id,
        input_file=str(job.input_file),
        output_file=str(report_path),
        provider="gemini",
    )


def write_workflow_report(
    output_dir: Path,
    node_id: str,
    label: str,
    provider: str,
    input_file: Path,
    markdown: str,
    external_id: str,
    output_prefix: str | None = None,
) -> WrittenReport:
    """Write a workflow node artifact to a timestamped markdown file."""

    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = _safe_name(output_prefix or node_id)
    report_path = output_dir / f"{safe_name}_{timestamp}.md"

    header = (
        f"# Research Workflow Artifact: {label}\n\n"
        f"- Artifact ID: `{node_id}`\n"
        f"- Provider: `{provider}`\n"
        f"- External ID: `{external_id}`\n"
        f"- Input file: `{input_file}`\n"
        f"- Generated at: `{datetime.now().isoformat(timespec='seconds')}`\n\n"
        "---\n\n"
    )
    report_path.write_text(header + markdown.strip() + "\n", encoding="utf-8")

    return WrittenReport(
        job_id=node_id,
        interaction_id=external_id,
        input_file=str(input_file),
        output_file=str(report_path),
        provider=provider,
    )


def write_run_summary(output_dir: Path, reports: list[WrittenReport], failures: list[dict[str, Any]]) -> Path:
    """Write a JSON summary for the full Deep Research run."""

    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_path = output_dir / f"deep_research_run_summary_{timestamp}.json"
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "completed": [asdict(report) for report in reports],
        "failed": failures,
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary_path


def write_rendered_prompt(output_dir: Path, node_id: str, prompt: str) -> Path:
    """Write a rendered workflow prompt for traceability."""

    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prompt_path = output_dir / f"{_safe_name(node_id)}_{timestamp}.md"
    prompt_path.write_text(prompt.strip() + "\n", encoding="utf-8")
    return prompt_path


def _safe_name(value: str) -> str:
    allowed = [character if character.isalnum() or character in {"-", "_"} else "_" for character in value]
    return "".join(allowed).strip("_") or "artifact"
