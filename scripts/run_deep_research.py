"""CLI entry point for Gemini Deep Research runs in the Lyme LLM Wiki."""

from __future__ import annotations

import logging
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.deep_research.config import (
    GeminiSettings,
    OpenAISettings,
    RunConfig,
    resolve_config_path,
    resolve_workflow_config_path,
)
from scripts.deep_research.logging_config import configure_logging

logger = logging.getLogger(__name__)


def build_parser() -> ArgumentParser:
    """Build the Deep Research command line parser."""

    parser = ArgumentParser(description="Run configured Gemini Deep Research jobs.")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run enabled jobs from the JSON config.")
    run_parser.add_argument(
        "--config",
        help="Path to the Deep Research JSON config. Defaults to research/deep_research_config.json.",
    )

    list_parser = subparsers.add_parser("list", help="List jobs from the JSON config without running them.")
    list_parser.add_argument("--config", help="Path to the Deep Research JSON config.")

    retrieve_parser = subparsers.add_parser(
        "retrieve",
        help="Retrieve one completed Gemini interaction by ID and write it as a report.",
    )
    retrieve_parser.add_argument("--interaction-id", required=True, help="Gemini interaction ID.")
    retrieve_parser.add_argument("--job-id", default="retrieved", help="Label to use in output metadata.")
    retrieve_parser.add_argument("--config", help="Path to the Deep Research JSON config.")

    workflow_list_parser = subparsers.add_parser(
        "workflow-list",
        help="List nodes from a dependency-aware workflow config without running them.",
    )
    workflow_list_parser.add_argument(
        "--config",
        help="Path to the workflow JSON config. Defaults to research/phase_zero_workflow.json.",
    )

    workflow_run_parser = subparsers.add_parser(
        "workflow-run",
        help="Run a dependency-aware research workflow.",
    )
    workflow_run_parser.add_argument(
        "--config",
        help="Path to the workflow JSON config. Defaults to research/phase_zero_workflow.json.",
    )
    workflow_run_parser.add_argument(
        "--resume-from-summary",
        help=(
            "Path to a previous workflow summary JSON. Completed artifacts in that summary "
            "are loaded as dependency context and are not rerun."
        ),
    )

    return parser


def main() -> int:
    """Run the requested Deep Research command."""

    args = build_parser().parse_args()
    command = args.command or "run"

    try:
        if command == "list":
            return _list_jobs(args)
        if command == "workflow-list":
            return _list_workflow(args)

        settings = GeminiSettings.from_env()
        configure_logging(settings.log_level)

        if command == "retrieve":
            return _retrieve(args, settings)
        if command == "workflow-run":
            return _run_workflow(args, settings)

        return _run(args, settings)
    except Exception:
        logger.exception("Gemini Deep Research command failed")
        return 1


def _load_run_config(args: Namespace) -> RunConfig:
    return RunConfig.from_json(resolve_config_path(getattr(args, "config", None)))


def _load_workflow_config(args: Namespace):
    from scripts.deep_research.workflow_config import WorkflowConfig

    return WorkflowConfig.from_json(resolve_workflow_config_path(getattr(args, "config", None)))


def _list_jobs(args: Namespace) -> int:
    run_config = _load_run_config(args)
    print(f"Config: {run_config.config_path}")
    print(f"Output directory: {run_config.output_dir}")
    print(f"Max parallel: {run_config.max_parallel}")
    print("")
    for job in run_config.jobs:
        state = "enabled" if job.enabled else "disabled"
        print(f"- {job.job_id} [{state}] {job.input_file}")
    return 0


def _run(args: Namespace, settings: GeminiSettings) -> int:
    from scripts.deep_research.runner import run_configured_research

    outcome = run_configured_research(settings, _load_run_config(args))
    print(f"Completed reports: {len(outcome.reports)}")
    print(f"Failed jobs: {len(outcome.failures)}")
    print(f"Run summary: {outcome.summary_path}")
    return 1 if outcome.failures else 0


def _retrieve(args: Namespace, settings: GeminiSettings) -> int:
    from scripts.deep_research.client import DeepResearchClient
    from scripts.deep_research.file_io import write_report, write_run_summary

    run_config = _load_run_config(args)
    client = DeepResearchClient(settings)
    result = client.retrieve(args.interaction_id, args.job_id)
    from scripts.deep_research.config import ResearchJob

    job = ResearchJob(job_id=args.job_id, input_file=run_config.config_path, enabled=True)
    report = write_report(run_config.output_dir, job, result)
    summary_path = write_run_summary(run_config.output_dir, [report], [])
    print(f"Retrieved report: {report.output_file}")
    print(f"Run summary: {summary_path}")
    return 0


def _list_workflow(args: Namespace) -> int:
    workflow_config = _load_workflow_config(args)
    print(f"Workflow: {workflow_config.name}")
    print(f"Config: {workflow_config.config_path}")
    print(f"Output directory: {workflow_config.output_dir}")
    print(f"Rendered prompt directory: {workflow_config.rendered_prompt_dir}")
    print(f"Max parallel: {workflow_config.max_parallel}")
    print("")
    for node in workflow_config.nodes:
        state = "enabled" if node.enabled else "disabled"
        dependencies = ", ".join(node.depends_on) or "none"
        print(f"- {node.node_id} [{state}] mode={node.mode} depends_on={dependencies}")
        print(f"  input: {node.input_file}")
    return 0


def _run_workflow(args: Namespace, gemini_settings: GeminiSettings) -> int:
    from scripts.deep_research.workflow_runner import run_workflow

    openai_settings = OpenAISettings.from_env()
    resume_from_summary = getattr(args, "resume_from_summary", None)
    outcome = run_workflow(
        gemini_settings,
        openai_settings,
        _load_workflow_config(args),
        Path(resume_from_summary).resolve() if resume_from_summary else None,
    )
    print(f"Completed workflow artifacts: {len(outcome.reports)}")
    print(f"Failed workflow nodes: {len(outcome.failures)}")
    print(f"Skipped workflow nodes: {len(outcome.skipped)}")
    print(f"Workflow summary: {outcome.summary_path}")
    return 1 if outcome.failures or outcome.skipped else 0


if __name__ == "__main__":
    sys.exit(main())
