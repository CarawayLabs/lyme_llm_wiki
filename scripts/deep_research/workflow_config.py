"""Configuration loading for dependency-aware research workflows."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from scripts.deep_research.config import _resolve_path


@dataclass(frozen=True)
class WorkflowNode:
    """A single research workflow node."""

    node_id: str
    label: str
    mode: str
    input_file: Path
    depends_on: tuple[str, ...] = ()
    enabled: bool = True
    output_prefix: str | None = None
    agent: str | None = None
    model: str | None = None
    thinking_summaries: str | None = None
    visualization: str | None = None
    collaborative_planning: bool | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def safe_output_name(self) -> str:
        """Return a filesystem-friendly output name derived from the node ID."""

        allowed = [character if character.isalnum() or character in {"-", "_"} else "_" for character in self.node_id]
        return "".join(allowed).strip("_") or "workflow_node"


@dataclass(frozen=True)
class WorkflowConfig:
    """A dependency-aware Deep Research workflow loaded from JSON."""

    config_path: Path
    name: str
    output_dir: Path
    rendered_prompt_dir: Path
    max_parallel: int
    nodes: tuple[WorkflowNode, ...]

    @classmethod
    def from_json(cls, config_path: Path) -> "WorkflowConfig":
        """Load and validate a workflow JSON file."""

        if not config_path.exists():
            raise FileNotFoundError(f"Workflow config not found: {config_path}")

        raw_config = json.loads(config_path.read_text(encoding="utf-8"))
        base_dir = config_path.parent
        output_dir = _resolve_path(raw_config.get("output_dir", "outputs/deep_research/workflows"), base_dir)
        rendered_prompt_dir = _resolve_path(
            raw_config.get("rendered_prompt_dir", "outputs/deep_research/rendered_prompts"),
            base_dir,
        )
        max_parallel = int(raw_config.get("max_parallel", 4))
        if max_parallel < 1:
            raise ValueError("max_parallel must be at least 1.")

        raw_nodes = raw_config.get("nodes", [])
        if not isinstance(raw_nodes, list):
            raise ValueError("Workflow config field 'nodes' must be a list.")

        nodes = tuple(_parse_node(node, base_dir) for node in raw_nodes)
        _validate_nodes(nodes)

        return cls(
            config_path=config_path,
            name=str(raw_config.get("name", config_path.stem)).strip(),
            output_dir=output_dir,
            rendered_prompt_dir=rendered_prompt_dir,
            max_parallel=max_parallel,
            nodes=nodes,
        )

    @property
    def enabled_nodes(self) -> tuple[WorkflowNode, ...]:
        """Return workflow nodes enabled for execution."""

        return tuple(node for node in self.nodes if node.enabled)


def _parse_node(raw_node: dict[str, Any], base_dir: Path) -> WorkflowNode:
    if not isinstance(raw_node, dict):
        raise ValueError("Each workflow node must be an object.")

    node_id = str(raw_node.get("id", "")).strip()
    if not node_id:
        raise ValueError("Each workflow node must include a non-empty 'id'.")

    input_value = raw_node.get("input_file")
    if not input_value:
        raise ValueError(f"Workflow node {node_id!r} must include 'input_file'.")

    depends_on = raw_node.get("depends_on", [])
    if not isinstance(depends_on, list):
        raise ValueError(f"Workflow node {node_id!r} field 'depends_on' must be a list.")

    reserved_keys = {
        "id",
        "label",
        "mode",
        "input_file",
        "depends_on",
        "enabled",
        "output_prefix",
        "agent",
        "model",
        "thinking_summaries",
        "visualization",
        "collaborative_planning",
    }

    return WorkflowNode(
        node_id=node_id,
        label=str(raw_node.get("label", node_id)).strip(),
        mode=str(raw_node.get("mode", "gemini_deep_research")).strip(),
        input_file=_resolve_path(input_value, base_dir),
        depends_on=tuple(str(dependency).strip() for dependency in depends_on),
        enabled=bool(raw_node.get("enabled", True)),
        output_prefix=_optional_str(raw_node.get("output_prefix")),
        agent=_optional_str(raw_node.get("agent")),
        model=_optional_str(raw_node.get("model")),
        thinking_summaries=_optional_str(raw_node.get("thinking_summaries")),
        visualization=_optional_str(raw_node.get("visualization")),
        collaborative_planning=_optional_bool(raw_node.get("collaborative_planning")),
        metadata={key: value for key, value in raw_node.items() if key not in reserved_keys},
    )


def _validate_nodes(nodes: tuple[WorkflowNode, ...]) -> None:
    ids = [node.node_id for node in nodes]
    duplicate_ids = sorted({node_id for node_id in ids if ids.count(node_id) > 1})
    if duplicate_ids:
        raise ValueError(f"Duplicate workflow node IDs: {', '.join(duplicate_ids)}")

    enabled_ids = {node.node_id for node in nodes if node.enabled}
    for node in nodes:
        if not node.enabled:
            continue
        missing = [dependency for dependency in node.depends_on if dependency not in enabled_ids]
        if missing:
            raise ValueError(
                f"Workflow node {node.node_id!r} depends on missing or disabled node(s): "
                f"{', '.join(missing)}"
            )

    _validate_acyclic(nodes)


def _validate_acyclic(nodes: tuple[WorkflowNode, ...]) -> None:
    node_map = {node.node_id: node for node in nodes if node.enabled}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in visited:
            return
        if node_id in visiting:
            raise ValueError(f"Workflow contains a dependency cycle at {node_id!r}.")
        visiting.add(node_id)
        for dependency in node_map[node_id].depends_on:
            visit(dependency)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in node_map:
        visit(node_id)


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
    raise ValueError("Workflow field 'collaborative_planning' must be a JSON boolean when set.")
