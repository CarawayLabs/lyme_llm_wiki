# TopX Lyme Disease Research Prompt Pack

This folder contains the remaining pipeline-ready prompts for the phase-zero research workflow.

## Template convention

The files use Jinja2-style placeholders:

```text
{{ artifact_name }}
```

Your Python pipeline should load the upstream Markdown artifact and render it into the dependent prompt.

Example:

```python
from pathlib import Path
from jinja2 import Template

template_text = Path("input/data_linkage_feasibility.md").read_text(encoding="utf-8")

rendered = Template(template_text).render(
    synthesis_agent_integrate_findings=Path(
        "output/synthesis_agent_integrate_findings_output.md"
    ).read_text(encoding="utf-8"),
    open_data_inventory=Path(
        "output/open_data_inventory_output.md"
    ).read_text(encoding="utf-8"),
    evidence_and_controversy_map=Path(
        "output/evidence_and_controversy_map_output.md"
    ).read_text(encoding="utf-8"),
)
```

Use `jinja2.StrictUndefined` in production so missing dependencies fail immediately.

## Execution types

| Agent | Recommended mode |
|---|---|
| Open-data inventory | Deep research |
| Evidence and controversy map | Deep research |
| Synthesis agent | Regular long-context reasoning LLM |
| Data-linkage feasibility | Deep research |
| Previous solution analysis | Deep research |
| Stakeholder and incentive map | Deep research |
| Opportunity generation | Strong reasoning LLM; optional targeted research |
| Red-team analysis | Strong reasoning plus targeted deep research |
| Interview preparation | Strong reasoning LLM; optional targeted research |

## Why synthesis should usually not be deep research

The synthesis agent should be source-bound. Its job is to integrate the four supplied artifacts, preserve citations and IDs, expose contradictions, and prepare handoffs. Giving it unrestricted browsing can introduce new facts that are not traceable to the original research package and can cause scope drift.

A normal long-context model is the better default. Enable targeted browsing only when a contradiction cannot be resolved from the supplied artifacts, and record any newly introduced source separately.

## Suggested execution sequence

1. Run in parallel:
   - `problem_space_map.md`
   - `patient_and_clinician_journeys.md`
   - `open_data_inventory.md`
   - `evidence_and_controversy_map.md`
2. Run `synthesis_agent_integrate_findings.md`.
3. Run:
   - `data_linkage_feasibility.md`
   - `previous_solution_analysis.md`
4. Run `stakeholder_and_incentive_map.md` after previous-solution analysis.
5. Run `opportunity_generation.md`.
6. Run `red_team_analysis.md`.
7. Run `interview_preparation.md`.

The stakeholder map can begin after synthesis, but its final run should include previous-solution analysis because prior adoption failures often reveal incentive and operating-model problems.
