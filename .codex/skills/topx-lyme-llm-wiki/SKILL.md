---
name: topx-lyme-llm-wiki
description: Operate the TopX Lyme Challenge LLM wiki workflow. Use when Codex is asked to answer research questions from this repository, review or promote generated Deep Research artifacts, synthesize wiki notes, score datasets or AI opportunities, inspect deep-research workflow status, run safe catalog exploration checks, or assess submission gaps for the TopX Lyme Disease Prevention and Cure challenge.
---

# TopX Lyme LLM Wiki

## Core Rule

Treat this repository as a source-grounded research system, not a scratchpad. Read the relevant wiki/source/output files first, distinguish sourced facts from analysis and inference, cite file paths and headings, and do not modify files unless the user explicitly asks.

## Reading Order

Start with the smallest set that fits the task:

1. `README.md` for repo structure and working principles.
2. `wiki/index.md`, `wiki/overview.md`, and `wiki/00_home.md` for navigation.
3. Task-specific pages:
   - Challenge context: `wiki/01_challenge_brief.md`
   - Datasets: `wiki/02_dataset_inventory.md`
   - Research questions: `wiki/03_research_questions.md`
   - Findings: `wiki/04_findings.md`
   - Opportunities: `wiki/05_opportunities.md`
   - Submission: `wiki/06_submission_plan.md`
   - Activity history: `wiki/log.md`
4. Generated artifacts only when needed: `outputs/deep_research/`.
5. Raw source material only when needed: `raw_sources/`.

For deep research or data collection tasks, also read:

- `DEEP_RESEARCH_README.md`
- `research/phase_zero_workflow.json`
- `research/deep_research_config.json`
- `topx_lyme_data_exploration_kit/README.md`
- `topx_lyme_data_exploration_kit/CSV_DATA_DICTIONARY.md`

## Workflow Selection

Use `references/workflows.md` for the detailed workflow when the user asks for one of these operations:

- Wiki status or research triage
- Promote a generated artifact into the wiki
- Answer a research question
- Score a dataset
- Score an opportunity
- Check deep-research status
- Run a catalog smoke test
- Check submission gaps

## Promotion Standard

Generated reports in `outputs/` are candidates, not established wiki knowledge. Before promoting anything:

1. Identify the artifact path and relevant headings.
2. Extract claims, datasets, opportunities, and open questions.
3. Label each item as sourced fact, generated synthesis, analysis, inference, or open question.
4. Cross-check against repository sources when possible.
5. Propose small edits to `wiki/` or `findings/`.
6. Preserve raw source material unchanged.

## Output Style

For research answers, include:

- What the repo currently supports.
- What is analysis or inference.
- What remains uncertain.
- Relevant file paths and headings.
- Concrete next steps when useful.

For file edits, keep changes small and reviewable. Update `wiki/log.md` only if the user asks for research activity logging or the edit represents a durable research event.
