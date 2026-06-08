# Codex Instructions

This repository contains a research wiki and research automation workspace for the TopX Lyme Disease Prevention and Cure challenge. It follows an Andrej Karpathy-style LLM wiki pattern: source material, generated research artifacts, synthesis notes, dataset inventory, opportunity scoring, and submission planning live together in a navigable knowledge base.

## Project Mission

Help accelerate discovery for the TopX Lyme challenge by turning source material, public datasets, LLM research runs, and analysis into a source-grounded wiki that can support a credible Phase 1 submission.

## Repository Structure

- `raw_sources/` contains original source material. Do not overwrite these files.
- `wiki/` contains structured research notes and synthesis.
- `findings/` contains developed evidence notes and synthesized outputs that should become part of the project record.
- `research/` contains research configuration, including Deep Research workflow config.
- `prompts/` contains reusable prompt templates for research, dataset scoring, and opportunity scoring.
- `scripts/` contains data collection, ingestion, sync, and LLM workflow utilities.
- `outputs/` contains generated artifacts. Review outputs before promoting conclusions into `wiki/` or `findings/`.
- `topx_lyme_data_exploration_kit/` contains the open-data catalog exploration workflow and generated catalog outputs.
- `.codex/skills/topx-lyme-llm-wiki/` contains the project-local Codex skill for wiki workflows.

## Canonical Reading Order

Read the smallest relevant set before answering or editing:

1. `README.md`
2. `wiki/index.md`, `wiki/overview.md`, and `wiki/00_home.md`
3. Task-specific wiki pages:
   - `wiki/01_challenge_brief.md`
   - `wiki/02_dataset_inventory.md`
   - `wiki/03_research_questions.md`
   - `wiki/04_findings.md`
   - `wiki/05_opportunities.md`
   - `wiki/06_submission_plan.md`
   - `wiki/log.md`
4. Relevant generated artifacts under `outputs/`
5. Relevant source material under `raw_sources/`

For research workflow questions, also read `DEEP_RESEARCH_README.md`, `research/phase_zero_workflow.json`, and `research/deep_research_config.json`.

For data catalog questions, also read `topx_lyme_data_exploration_kit/README.md` and `topx_lyme_data_exploration_kit/CSV_DATA_DICTIONARY.md`.

## Codex Skill

Use the project-local skill at `.codex/skills/topx-lyme-llm-wiki/` when working on:

- Wiki status and research triage
- Artifact review or promotion from `outputs/`
- Repository-grounded research questions
- Dataset scoring
- Opportunity scoring
- Deep Research workflow status
- Catalog smoke tests
- Submission gap checks

The skill's workflow reference is `.codex/skills/topx-lyme-llm-wiki/references/workflows.md`.

## Research Modes

- **Answer from the wiki:** read relevant pages, cite paths and headings, and separate facts from analysis.
- **Promote generated artifacts:** treat `outputs/` reports as candidates, not primary sources. Extract useful claims, classify evidence quality, and propose small wiki edits.
- **Score datasets:** use `prompts/dataset_scorer.md` and update `wiki/02_dataset_inventory.md` only when asked.
- **Score opportunities:** use `prompts/opportunity_scorer.md` and update `wiki/05_opportunities.md` or `wiki/06_submission_plan.md` only when asked.
- **Run workflows:** list or inspect safely by default; launch expensive or broad API/LLM runs only when explicitly requested.

## Citation Rules

- Cite repository file paths and headings for conclusions.
- Distinguish sourced facts, generated synthesis, analysis, inference, and open questions.
- Do not present an LLM-generated report as a primary source.
- When evidence is weak, say so directly and identify what would reduce uncertainty.

## Do Not Do

- Do not modify files unless explicitly asked.
- Do not overwrite raw source material.
- Do not print secrets from `.env`.
- Do not run broad API crawls or Deep Research workflows unless the user explicitly asks.
- Do not promote generated outputs into the wiki without review.

## Definition of Done

For research answers, provide the supported conclusion, uncertainty, citations, and next useful steps. For edits, keep changes small and reviewable, preserve raw sources, and mention verification performed.
