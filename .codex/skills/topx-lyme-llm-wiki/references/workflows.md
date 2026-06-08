# Codex Workflow Reference

Use these workflows as Codex equivalents of project slash commands.

## wiki-status

Purpose: summarize the current state of the wiki and recommend next research moves.

Steps:
1. Read `wiki/index.md`, `wiki/overview.md`, `wiki/00_home.md`, and `wiki/log.md`.
2. Skim headings in `wiki/01_challenge_brief.md` through `wiki/06_submission_plan.md`.
3. Check latest files under `outputs/deep_research/phase_zero/` when generated artifacts matter.
4. Report current strengths, gaps, stale areas, and the next 3-5 useful actions.

## promote-artifact

Purpose: turn a generated artifact into reviewed wiki knowledge.

Inputs: one file under `outputs/deep_research/` or another generated output path.

Steps:
1. Read the artifact and identify its main claims, datasets, opportunities, risks, and open questions.
2. Check relevant wiki pages and raw/source files when available.
3. Classify each proposed addition as sourced fact, generated synthesis, analysis, inference, or open question.
4. Recommend or make small edits to `wiki/04_findings.md`, `wiki/02_dataset_inventory.md`, `wiki/05_opportunities.md`, or `findings/`.
5. Cite the artifact path plus any source or wiki headings used.

Guardrail: do not treat an LLM-generated report as a primary source.

## research-question

Purpose: answer a question from repository evidence before reaching outside the repo.

Steps:
1. Search `wiki/`, `findings/`, `research/`, `prompts/`, `outputs/`, and relevant source folders with `rg`.
2. Read the smallest set of relevant files.
3. Answer in three layers: repo-supported facts, analysis/inference, and remaining uncertainty.
4. Suggest follow-up source collection or Deep Research prompts only when they would reduce uncertainty.

## dataset-score

Purpose: evaluate a dataset for TopX Lyme usefulness.

Steps:
1. Read `prompts/dataset_scorer.md`.
2. Read the dataset note, catalog result, metadata JSON, CSV dictionary entry, or source file.
3. Score relevance, freshness, completeness, geographic coverage, granularity, accessibility, AI usefulness, and risks.
4. Add linkage potential, likely user value, and evidence gaps.
5. If editing is requested, update `wiki/02_dataset_inventory.md` or a focused finding.

## opportunity-score

Purpose: evaluate an AI/product opportunity for the TopX Lyme challenge.

Steps:
1. Read `prompts/opportunity_scorer.md`.
2. Read related findings, datasets, stakeholder notes, and submission plan sections.
3. Score user pain, public health impact, feasibility, data availability, differentiation, submission fit, and prototype potential.
4. Identify assumptions, evidence needs, and a simple prototype path.
5. If editing is requested, update `wiki/05_opportunities.md` or `wiki/06_submission_plan.md`.

## deep-research-status

Purpose: inspect configured Deep Research jobs and recent outputs.

Safe commands:
```powershell
python scripts/run_deep_research.py list
python scripts/run_deep_research.py workflow-list
```

Steps:
1. Read `DEEP_RESEARCH_README.md`.
2. Run a list command when the user asks for current status.
3. Inspect latest `outputs/deep_research/phase_zero/` summaries and `outputs/deep_research/workflow_run_log.txt` when present.
4. Summarize enabled jobs, dependencies, recent completed outputs, and likely next step.

Run `workflow-run` only when the user explicitly asks to launch the workflow.

## catalog-smoke-test

Purpose: safely test the data exploration kit without launching a broad crawl.

Safe command pattern:
```powershell
python topx_lyme_data_exploration_kit/scripts/topx_catalog_explorer.py --smoke-test --workers 1 --max-records-per-page 25
```

Steps:
1. Read `topx_lyme_data_exploration_kit/README.md`.
2. Check `.env.example` for required tokens; do not print secrets from `.env`.
3. Prefer `--smoke-test`, `--catalog`, `--priority`, and `--max-queries` filters.
4. Summarize run manifest, search summary, errors, and promising catalog results.

## submission-gap-check

Purpose: compare the wiki against Phase 1 submission needs.

Steps:
1. Read `wiki/06_submission_plan.md`, `wiki/05_opportunities.md`, `wiki/04_findings.md`, and `wiki/02_dataset_inventory.md`.
2. Check `wiki/01_challenge_brief.md` for requirements and open questions.
3. Identify narrative gaps, evidence gaps, dataset gaps, prototype gaps, and review risks.
4. Return a prioritized checklist with the next actions that improve submission credibility.
