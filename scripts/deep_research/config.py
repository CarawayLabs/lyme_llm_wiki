"""Configuration loading for Gemini Deep Research wiki runs."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv() -> bool:
        """Fallback when python-dotenv is not installed."""

        return False


DEFAULT_AGENT = "deep-research-preview-04-2026"
DEFAULT_CONFIG_PATH = Path("research/deep_research_config.json")
DEFAULT_WORKFLOW_CONFIG_PATH = Path("research/phase_zero_workflow.json")


def _bool_from_env(name: str, default: bool) -> bool:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    normalized = raw_value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False

    raise ValueError(f"{name} must be a boolean value, got {raw_value!r}.")


def _int_from_env(name: str, default: int, minimum: int | None = None) -> int:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer, got {raw_value!r}.") from exc

    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be at least {minimum}, got {value}.")

    return value


@dataclass(frozen=True)
class GeminiSettings:
    """Runtime Gemini settings shared by all configured research jobs."""

    api_key: str
    default_agent: str = DEFAULT_AGENT
    poll_interval_seconds: int = 10
    timeout_minutes: int = 60
    thinking_summaries: str = "none"
    visualization: str = "auto"
    collaborative_planning: bool = False
    store: bool = True
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "GeminiSettings":
        """Load Gemini settings from `.env` and environment variables."""

        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required. Add it to your .env file.")

        return cls(
            api_key=api_key,
            default_agent=os.getenv("GEMINI_DEEP_RESEARCH_AGENT", DEFAULT_AGENT).strip(),
            poll_interval_seconds=_int_from_env(
                "GEMINI_DEEP_RESEARCH_POLL_INTERVAL_SECONDS", 10, minimum=1
            ),
            timeout_minutes=_int_from_env("GEMINI_DEEP_RESEARCH_TIMEOUT_MINUTES", 60, minimum=1),
            thinking_summaries=os.getenv("GEMINI_DEEP_RESEARCH_THINKING_SUMMARIES", "none").strip(),
            visualization=os.getenv("GEMINI_DEEP_RESEARCH_VISUALIZATION", "auto").strip(),
            collaborative_planning=_bool_from_env(
                "GEMINI_DEEP_RESEARCH_COLLABORATIVE_PLANNING", False
            ),
            store=_bool_from_env("GEMINI_DEEP_RESEARCH_STORE", True),
            log_level=os.getenv("LOG_LEVEL", "INFO").strip().upper(),
        )

    def agent_config(self, job: "ResearchJob") -> dict[str, object]:
        """Build Gemini agent config for a job, including job-level overrides."""

        collaborative_planning = job.collaborative_planning
        if collaborative_planning is None:
            collaborative_planning = self.collaborative_planning
        if collaborative_planning:
            raise ValueError(
                "Collaborative planning is not supported by this unattended runner because "
                "it requires an interactive plan approval step."
            )

        return {
            "type": "deep-research",
            "thinking_summaries": job.thinking_summaries or self.thinking_summaries,
            "visualization": job.visualization or self.visualization,
            "collaborative_planning": collaborative_planning,
        }


@dataclass(frozen=True)
class OpenAISettings:
    """Runtime OpenAI settings for source-bound synthesis nodes."""

    api_key: str
    model: str = "gpt-4.1"
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "OpenAISettings":
        """Load OpenAI settings from `.env` and environment variables."""

        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAI synthesis workflow nodes.")

        return cls(
            api_key=api_key,
            model=os.getenv("OPENAI_SYNTHESIS_MODEL", "gpt-4.1").strip(),
            log_level=os.getenv("LOG_LEVEL", "INFO").strip().upper(),
        )


@dataclass(frozen=True)
class ResearchJob:
    """A single markdown prompt scheduled for Gemini Deep Research."""

    job_id: str
    input_file: Path
    enabled: bool = True
    description: str = ""
    agent: str | None = None
    output_prefix: str | None = None
    thinking_summaries: str | None = None
    visualization: str | None = None
    collaborative_planning: bool | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def safe_output_name(self) -> str:
        """Return a filesystem-friendly output name derived from the job ID."""

        allowed = [character if character.isalnum() or character in {"-", "_"} else "_" for character in self.job_id]
        return "".join(allowed).strip("_") or "deep_research"


@dataclass(frozen=True)
class RunConfig:
    """Deep Research run configuration loaded from JSON."""

    config_path: Path
    output_dir: Path
    max_parallel: int
    jobs: tuple[ResearchJob, ...]

    @classmethod
    def from_json(cls, config_path: Path) -> "RunConfig":
        """Load and validate a Deep Research JSON config file."""

        if not config_path.exists():
            raise FileNotFoundError(f"Deep Research config not found: {config_path}")

        raw_config = json.loads(config_path.read_text(encoding="utf-8"))
        base_dir = config_path.parent

        output_dir = _resolve_path(raw_config.get("output_dir", "outputs/deep_research"), base_dir)
        max_parallel = int(raw_config.get("max_parallel", 2))
        if max_parallel < 1:
            raise ValueError("max_parallel must be at least 1.")

        raw_jobs = raw_config.get("jobs", [])
        if not isinstance(raw_jobs, list):
            raise ValueError("Deep Research config field 'jobs' must be a list.")

        jobs = tuple(_parse_job(job, base_dir) for job in raw_jobs)
        return cls(
            config_path=config_path,
            output_dir=output_dir,
            max_parallel=max_parallel,
            jobs=jobs,
        )

    @property
    def enabled_jobs(self) -> tuple[ResearchJob, ...]:
        """Return jobs that are enabled for execution."""

        return tuple(job for job in self.jobs if job.enabled)


def resolve_config_path(value: str | None) -> Path:
    """Resolve the config path supplied by CLI or environment."""

    raw_path = value or os.getenv("GEMINI_DEEP_RESEARCH_CONFIG") or str(DEFAULT_CONFIG_PATH)
    return Path(raw_path).resolve()


def resolve_workflow_config_path(value: str | None) -> Path:
    """Resolve the workflow config path supplied by CLI or environment."""

    raw_path = (
        value
        or os.getenv("DEEP_RESEARCH_WORKFLOW_CONFIG")
        or str(DEFAULT_WORKFLOW_CONFIG_PATH)
    )
    return Path(raw_path).resolve()


def _parse_job(raw_job: dict[str, Any], base_dir: Path) -> ResearchJob:
    if not isinstance(raw_job, dict):
        raise ValueError("Each Deep Research job must be an object.")

    job_id = str(raw_job.get("id", "")).strip()
    if not job_id:
        raise ValueError("Each Deep Research job must include a non-empty 'id'.")

    input_value = raw_job.get("input_file")
    if not input_value:
        raise ValueError(f"Deep Research job {job_id!r} must include 'input_file'.")

    reserved_keys = {
        "id",
        "input_file",
        "enabled",
        "description",
        "agent",
        "output_prefix",
        "thinking_summaries",
        "visualization",
        "collaborative_planning",
    }
    metadata = {key: value for key, value in raw_job.items() if key not in reserved_keys}

    return ResearchJob(
        job_id=job_id,
        input_file=_resolve_path(input_value, base_dir),
        enabled=bool(raw_job.get("enabled", True)),
        description=str(raw_job.get("description", "")).strip(),
        agent=_optional_str(raw_job.get("agent")),
        output_prefix=_optional_str(raw_job.get("output_prefix")),
        thinking_summaries=_optional_str(raw_job.get("thinking_summaries")),
        visualization=_optional_str(raw_job.get("visualization")),
        collaborative_planning=_optional_bool(raw_job.get("collaborative_planning")),
        metadata=metadata,
    )


def _resolve_path(value: object, base_dir: Path) -> Path:
    path = Path(str(value))
    if path.is_absolute():
        return path

    repo_relative = Path.cwd() / path
    if repo_relative.exists() or str(value).startswith(("input", "outputs", "research", "wiki", "raw_sources")):
        return repo_relative.resolve()

    return (base_dir / path).resolve()


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _optional_bool(value: object) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    raise ValueError("Job field 'collaborative_planning' must be a JSON boolean when set.")
