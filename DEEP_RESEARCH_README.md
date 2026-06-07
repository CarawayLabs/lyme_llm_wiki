# Deep Research Agent Usage

This repo supports two research execution modes:

- A flat Gemini Deep Research runner for one or more independent research prompts.
- A dependency-aware Phase Zero workflow that runs Gemini Deep Research tasks, routes the synthesis step through OpenAI, injects upstream artifacts into downstream prompts with Jinja2, and preserves rendered prompts for review.

Deep Research prompt files and generated reports are local artifacts. They are intentionally ignored by git.

## 1. Independent Gemini Deep Research Jobs

Use this mode when one or more prompts can run independently.

Prompt files go in:

```text
input/deep_research/
```

Configure jobs in:

```text
research/deep_research_config.json
```

Example:

```json
{
  "output_dir": "outputs/deep_research",
  "max_parallel": 2,
  "jobs": [
    {
      "id": "dataset_landscape",
      "enabled": true,
      "input_file": "input/deep_research/open_data_inventory.md",
      "output_prefix": "dataset_landscape"
    }
  ]
}
```

List configured jobs:

```powershell
python scripts/run_deep_research.py list
```

Run enabled jobs:

```powershell
python scripts/run_deep_research.py run
```

The runner uses `max_parallel` to run multiple enabled jobs at the same time.

## 2. Phase Zero Workflow

Use this mode for the sequenced research workflow where later prompts depend on earlier artifacts.

Configure the workflow in:

```text
research/phase_zero_workflow.json
```

The default workflow follows this sequence:

1. Run these Gemini Deep Research agents in parallel:
   - `problem_space_map`
   - `patient_and_clinician_journeys`
   - `open_data_inventory`
   - `evidence_and_controversy_map`
2. Run `synthesis_agent_integrate_findings` with OpenAI.
3. Run these Gemini Deep Research agents in parallel:
   - `data_linkage_feasibility`
   - `previous_solution_analysis`
4. Run `stakeholder_and_incentive_map`.
5. Run `opportunity_generation`.
6. Run `red_team_analysis`.
7. Run `interview_preparation`.

List workflow nodes:

```powershell
python scripts/run_deep_research.py workflow-list
```

Run the workflow:

```powershell
python scripts/run_deep_research.py workflow-run
```

The workflow runner only starts a node when all of its `depends_on` artifacts have completed. Ready nodes can still run in parallel, controlled by `max_parallel`.

## Jinja2 Dependency Injection

Downstream prompt files can include Jinja2-style placeholders for upstream artifacts:

```markdown
## Prior synthesis

{{ synthesis_agent_integrate_findings }}

## Open-data inventory

{{ open_data_inventory }}
```

The workflow uses `StrictUndefined`, so a missing placeholder fails the run instead of silently producing an incomplete prompt.

Each completed artifact is available by its node ID. A structured `artifacts` object is also available:

```markdown
{{ artifacts.open_data_inventory.output_file }}

{{ artifacts.open_data_inventory.markdown }}
```

Rendered prompts are written to:

```text
outputs/deep_research/rendered_prompts/
```

Workflow artifacts are written to:

```text
outputs/deep_research/phase_zero/
```

## Environment Variables

Create `.env` from `.env.example`.

Required for Gemini nodes:

```dotenv
GEMINI_API_KEY=your_gemini_api_key_here
```

Required for OpenAI synthesis nodes:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_SYNTHESIS_MODEL=gpt-4.1
```

Optional settings include:

```dotenv
GEMINI_DEEP_RESEARCH_AGENT=deep-research-preview-04-2026
GEMINI_DEEP_RESEARCH_POLL_INTERVAL_SECONDS=10
GEMINI_DEEP_RESEARCH_TIMEOUT_MINUTES=60
GEMINI_DEEP_RESEARCH_THINKING_SUMMARIES=none
GEMINI_DEEP_RESEARCH_VISUALIZATION=auto
GEMINI_DEEP_RESEARCH_STORE=true
LOG_LEVEL=INFO
```

## Retrieval

Retrieve a completed Gemini interaction by ID:

```powershell
python scripts/run_deep_research.py retrieve --interaction-id v1_your_interaction_id_here --job-id lyme_followup
```

## Notes

- The synthesis agent is intentionally source-bound and uses OpenAI through a normal API call.
- Gemini Deep Research is used for the other workflow research agents.
- Generated reports should be reviewed before promoting conclusions into `wiki/` or `findings/`.
- Keep sourced facts distinct from analysis and inference.
