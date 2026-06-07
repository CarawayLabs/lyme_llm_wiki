# update_repo_structure.ps1
# Safe to run from anywhere.
# Expected location: LYME_LLM_WIKI/project_scaffolding/update_repo_structure.ps1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Write-Host "Script directory: $ScriptDir" -ForegroundColor Cyan
Write-Host "Repo root:        $RepoRoot" -ForegroundColor Cyan

# Guardrail: make sure we are operating on the repo root, not project_scaffolding
if (-not (Test-Path (Join-Path $RepoRoot ".git"))) {
    throw "Repo root does not contain a .git folder. Expected script to live inside: <repo>/project_scaffolding/"
}

function Ensure-Directory {
    param (
        [Parameter(Mandatory = $true)]
        [string]$RelativePath,

        [bool]$AddGitkeep = $true
    )

    $FullPath = Join-Path $RepoRoot $RelativePath

    if (-not (Test-Path $FullPath)) {
        New-Item -ItemType Directory -Path $FullPath | Out-Null
        Write-Host "Created directory: $RelativePath"
    }
    else {
        Write-Host "Directory exists: $RelativePath"
    }

    if ($AddGitkeep) {
        $GitkeepPath = Join-Path $FullPath ".gitkeep"
        if (-not (Test-Path $GitkeepPath)) {
            New-Item -ItemType File -Path $GitkeepPath | Out-Null
            Write-Host "Created .gitkeep: $RelativePath/.gitkeep"
        }
    }
}

function Ensure-File {
    param (
        [Parameter(Mandatory = $true)]
        [string]$RelativePath,

        [Parameter(Mandatory = $true)]
        [AllowEmptyString()]
        [string]$Content
    )

    $FullPath = Join-Path $RepoRoot $RelativePath
    $Parent = Split-Path -Parent $FullPath

    if (-not (Test-Path $Parent)) {
        New-Item -ItemType Directory -Path $Parent | Out-Null
    }

    if (-not (Test-Path $FullPath)) {
        Set-Content -Path $FullPath -Value $Content -Encoding UTF8
        Write-Host "Created file: $RelativePath"
    }
    else {
        Write-Host "Skipped existing file: $RelativePath"
    }
}

# Directories
Ensure-Directory ".github/workflows" $true
Ensure-Directory ".vscode" $false

Ensure-Directory "outputs/json" $true
Ensure-Directory "outputs/markdown" $true

Ensure-Directory "raw_sources/challenge_docs" $true
Ensure-Directory "raw_sources/data_gov" $true
Ensure-Directory "raw_sources/hhs" $true
Ensure-Directory "raw_sources/nih" $true
Ensure-Directory "raw_sources/papers" $true

Ensure-Directory "scripts" $false

Ensure-Directory "wiki/templates" $true
Ensure-Directory "prompts" $false
Ensure-Directory "findings/daily" $true
Ensure-Directory "research/notes" $true
Ensure-Directory "research/hypotheses" $true
Ensure-Directory "project_scaffolding" $false

# Move existing root-level PowerShell scripts into project_scaffolding
$Ps1FilesToMove = @(
    "create_vscode_settings.ps1",
    "initialize_wiki.ps1"
)

foreach ($File in $Ps1FilesToMove) {
    $Source = Join-Path $RepoRoot $File
    $Destination = Join-Path $RepoRoot "project_scaffolding/$File"

    if ((Test-Path $Source) -and (-not (Test-Path $Destination))) {
        Move-Item -Path $Source -Destination $Destination
        Write-Host "Moved $File to project_scaffolding/"
    }
}

# Files
Ensure-File ".github/workflows/sync-notion.yml" @"
name: Sync Markdown to Notion

on:
  push:
    branches:
      - main
    paths:
      - 'wiki/**/*.md'
      - 'research/**/*.md'
      - 'findings/**/*.md'
      - 'prompts/**/*.md'
      - 'README.md'
      - 'scripts/sync_notion.py'

jobs:
  sync-notion:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Placeholder
        run: echo "Notion sync will be configured in a later step."
"@

Ensure-File "scripts/sync_notion.py" @"
"""
Sync selected markdown files from this repo to Notion.

Placeholder for now.
"""

def main() -> None:
    print("Notion sync placeholder. Implementation coming next.")


if __name__ == "__main__":
    main()
"@

Ensure-File "wiki/00_home.md" @"
# TopX Lyme Challenge Wiki

This is the working knowledge base for the TopX Lyme Challenge.

## Main Sections

- Challenge brief
- Dataset inventory
- Research questions
- Findings
- Opportunities
- Submission plan
"@

Ensure-File "wiki/01_challenge_brief.md" @"
# Challenge Brief

## Purpose

Summarize the challenge, goals, phases, submission requirements, scoring criteria, and important deadlines.

## Open Questions

- What exactly is required for Phase 1?
- What evidence will make the submission stronger?
- What constraints or assumptions matter?
"@

Ensure-File "wiki/02_dataset_inventory.md" @"
# Dataset Inventory

| Dataset | Source | URL | Relevance | Quality | Status | Notes |
|---|---|---|---|---|---|---|
"@

Ensure-File "wiki/03_research_questions.md" @"
# Research Questions

## Current Questions

- What public datasets are most relevant to Lyme disease?
- What user or agency pain points are visible from the data?
- Where could AI meaningfully improve discovery, triage, analysis, or communication?
"@

Ensure-File "wiki/04_findings.md" @"
# Findings

## Finding Template

### Finding

### Evidence

### Why It Matters

### Source Links

### Follow-Up
"@

Ensure-File "wiki/05_opportunities.md" @"
# Opportunities

| Opportunity | User | Problem | AI Angle | Feasibility | Impact | Priority |
|---|---|---|---|---|---|---|
"@

Ensure-File "wiki/06_submission_plan.md" @"
# Submission Plan

## Phase 1 Deliverables

- TBD

## Submission Narrative

- Problem
- Users
- Data sources
- Proposed AI solution
- Evidence
- Risks
- Implementation path

## Checklist

- [ ] Confirm submission requirements
- [ ] Identify strongest dataset sources
- [ ] Select core problem/opportunity
- [ ] Draft solution concept
- [ ] Review scoring rubric
"@

Ensure-File "prompts/research_assistant.md" @"
# Research Assistant Prompt

Use this prompt to analyze challenge documents, public datasets, papers, and source material.

## Instructions

- Identify key facts
- Extract useful source links
- Separate evidence from speculation
- Suggest follow-up research questions
"@

Ensure-File "prompts/dataset_scorer.md" @"
# Dataset Scorer Prompt

Evaluate a dataset for usefulness in the TopX Lyme Challenge.

## Scoring Dimensions

- Relevance
- Freshness
- Completeness
- Geographic coverage
- Granularity
- Accessibility
- AI usefulness
- Risks or limitations
"@

Ensure-File "prompts/opportunity_scorer.md" @"
# Opportunity Scorer Prompt

Evaluate a product or AI opportunity for the TopX Lyme Challenge.

## Scoring Dimensions

- User pain
- Public health impact
- Feasibility
- Data availability
- Differentiation
- Submission fit
- Prototype potential
"@

Write-Host ""
Write-Host "Repo structure update complete." -ForegroundColor Green
Write-Host ""
Write-Host "Next:"
Write-Host "  git status"
Write-Host "  git add ."
Write-Host "  git commit -m `"Update repo structure for Lyme LLM wiki`""
Write-Host "  git push"
