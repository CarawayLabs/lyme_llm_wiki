"""Dependency-aware orchestration for phase-zero research workflows."""

from __future__ import annotations

import logging
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.deep_research.client import DeepResearchClient
from scripts.deep_research.config import GeminiSettings, OpenAISettings, ResearchJob
from scripts.deep_research.file_io import (
    WrittenReport,
    write_rendered_prompt,
    write_run_summary,
    write_workflow_report,
)
from scripts.deep_research.openai_client import OpenAISynthesisClient
from scripts.deep_research.prompt_renderer import render_prompt_template
from scripts.deep_research.workflow_config import WorkflowConfig, WorkflowNode

logger = logging.getLogger(__name__)

GEMINI_MODE = "gemini_deep_research"
OPENAI_MODE = "openai_synthesis"


@dataclass(frozen=True)
class WorkflowOutcome:
    """Summary of a completed workflow run."""

    reports: list[WrittenReport]
    failures: list[dict[str, Any]]
    skipped: list[dict[str, Any]]
    summary_path: Path


@dataclass(frozen=True)
class Artifact:
    """A completed workflow artifact used as dependency context."""

    node_id: str
    label: str
    provider: str
    markdown: str
    output_file: str


def run_workflow(
    gemini_settings: GeminiSettings,
    openai_settings: OpenAISettings,
    workflow_config: WorkflowConfig,
) -> WorkflowOutcome:
    """Run a dependency-aware workflow with parallel ready-node execution."""

    nodes = list(workflow_config.enabled_nodes)
    if not nodes:
        raise ValueError(f"No enabled workflow nodes found in {workflow_config.config_path}.")

    node_map = {node.node_id: node for node in nodes}
    pending = set(node_map)
    running: dict[Future[WrittenReport], WorkflowNode] = {}
    completed: dict[str, Artifact] = {}
    failed: set[str] = set()
    reports: list[WrittenReport] = []
    failures: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []

    logger.info("Running workflow %s with %s enabled node(s)", workflow_config.name, len(nodes))
    with ThreadPoolExecutor(max_workers=min(workflow_config.max_parallel, len(nodes))) as executor:
        while pending or running:
            _skip_blocked_nodes(pending, node_map, failed, skipped)
            ready = [
                node_map[node_id]
                for node_id in sorted(pending)
                if all(dependency in completed for dependency in node_map[node_id].depends_on)
            ]

            while ready and len(running) < workflow_config.max_parallel:
                node = ready.pop(0)
                pending.remove(node.node_id)
                future = executor.submit(
                    _run_node,
                    gemini_settings,
                    openai_settings,
                    workflow_config.output_dir,
                    workflow_config.rendered_prompt_dir,
                    node,
                    completed,
                )
                running[future] = node

            if not running:
                if pending:
                    unresolved = ", ".join(sorted(pending))
                    raise RuntimeError(f"Workflow stalled with unresolved node(s): {unresolved}")
                break

            done, _ = wait(running, return_when=FIRST_COMPLETED)
            for future in done:
                node = running.pop(future)
                try:
                    report = future.result()
                    markdown = Path(report.output_file).read_text(encoding="utf-8")
                    completed[node.node_id] = Artifact(
                        node_id=node.node_id,
                        label=node.label,
                        provider=report.provider,
                        markdown=markdown,
                        output_file=report.output_file,
                    )
                    reports.append(report)
                except Exception as exc:
                    logger.exception("Workflow node %s failed", node.node_id)
                    failed.add(node.node_id)
                    failures.append(
                        {
                            "node_id": node.node_id,
                            "input_file": str(node.input_file),
                            "error": str(exc),
                        }
                    )

    reports.sort(key=lambda report: report.job_id)
    failures.sort(key=lambda failure: failure["node_id"])
    skipped.sort(key=lambda item: item["node_id"])
    summary_path = write_run_summary(workflow_config.output_dir, reports, failures + skipped)
    logger.info("Wrote workflow run summary to %s", summary_path)
    return WorkflowOutcome(
        reports=reports,
        failures=failures,
        skipped=skipped,
        summary_path=summary_path,
    )


def _run_node(
    gemini_settings: GeminiSettings,
    openai_settings: OpenAISettings,
    output_dir: Path,
    rendered_prompt_dir: Path,
    node: WorkflowNode,
    completed: dict[str, Artifact],
) -> WrittenReport:
    logger.info("Rendering workflow prompt for node %s", node.node_id)
    prompt = render_prompt_template(node.input_file, _build_template_context(completed))
    rendered_prompt_path = write_rendered_prompt(rendered_prompt_dir, node.node_id, prompt)
    logger.info("Rendered workflow prompt for node %s to %s", node.node_id, rendered_prompt_path)

    if node.mode == GEMINI_MODE:
        result = _run_gemini_node(gemini_settings, node, prompt)
        return write_workflow_report(
            output_dir=output_dir,
            node_id=node.node_id,
            label=node.label,
            provider="gemini",
            input_file=node.input_file,
            markdown=result.markdown,
            external_id=result.interaction_id,
            output_prefix=node.output_prefix,
        )

    if node.mode == OPENAI_MODE:
        result = OpenAISynthesisClient(openai_settings).run(node.node_id, prompt, node.model)
        return write_workflow_report(
            output_dir=output_dir,
            node_id=node.node_id,
            label=node.label,
            provider="openai",
            input_file=node.input_file,
            markdown=result.markdown,
            external_id=result.response_id,
            output_prefix=node.output_prefix,
        )

    raise ValueError(
        f"Unsupported workflow node mode {node.mode!r}. "
        f"Expected {GEMINI_MODE!r} or {OPENAI_MODE!r}."
    )


def _run_gemini_node(gemini_settings: GeminiSettings, node: WorkflowNode, prompt: str):
    job = ResearchJob(
        job_id=node.node_id,
        input_file=node.input_file,
        enabled=node.enabled,
        description=node.label,
        agent=node.agent,
        output_prefix=node.output_prefix,
        thinking_summaries=node.thinking_summaries,
        visualization=node.visualization,
        collaborative_planning=node.collaborative_planning,
        metadata=node.metadata,
    )
    return DeepResearchClient(gemini_settings).run(job, prompt)


def _build_template_context(completed: dict[str, Artifact]) -> dict[str, object]:
    artifacts = {
        node_id: {
            "id": artifact.node_id,
            "label": artifact.label,
            "provider": artifact.provider,
            "output_file": artifact.output_file,
            "markdown": artifact.markdown,
        }
        for node_id, artifact in completed.items()
    }
    context: dict[str, object] = {"artifacts": artifacts}
    for node_id, artifact in completed.items():
        context[node_id] = artifact.markdown
    return context


def _skip_blocked_nodes(
    pending: set[str],
    node_map: dict[str, WorkflowNode],
    failed: set[str],
    skipped: list[dict[str, Any]],
) -> None:
    changed = True
    blocked = set(failed)
    while changed:
        changed = False
        for node_id in sorted(list(pending)):
            blocking_dependencies = [
                dependency for dependency in node_map[node_id].depends_on if dependency in blocked
            ]
            if blocking_dependencies:
                pending.remove(node_id)
                blocked.add(node_id)
                skipped.append(
                    {
                        "node_id": node_id,
                        "input_file": str(node_map[node_id].input_file),
                        "error": (
                            "Skipped because dependency failed or was skipped: "
                            + ", ".join(blocking_dependencies)
                        ),
                    }
                )
                changed = True
