# initialize_wiki.ps1
#
# Creates the initial directory and file structure for the Lyme LLM Wiki.
# Run this script from inside the existing "lyme_llm_wiki" directory.

[CmdletBinding()]
param(
    [switch]$SkipFolderNameValidation
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ExpectedFolderName = "lyme_llm_wiki"
$RootPath = (Get-Location).Path
$CurrentFolderName = Split-Path -Path $RootPath -Leaf

if (
    -not $SkipFolderNameValidation -and
    $CurrentFolderName -ne $ExpectedFolderName
) {
    throw @"
This script must be run from inside the '$ExpectedFolderName' folder.

Current directory:
$RootPath

Change directories and run the script again:

    cd path\to\$ExpectedFolderName
    .\initialize_wiki.ps1

To intentionally run it somewhere else, use:

    .\initialize_wiki.ps1 -SkipFolderNameValidation
"@
}

$Directories = @(
    "raw_sources"
    "raw_sources\data_gov"
    "raw_sources\hhs"
    "raw_sources\nih"
    "raw_sources\papers"
    "raw_sources\challenge_docs"

    "wiki"
    "wiki\entities"
    "wiki\concepts"
    "wiki\datasets"
    "wiki\questions"
    "wiki\analyses"

    "scripts"

    "outputs"
    "outputs\json"
    "outputs\markdown"
)

$Files = @{
    "AGENTS.md" = @'
# Codex Instructions

This repository contains a research wiki for the TopX Lyme disease challenge.

## Repository structure

- `raw_sources/` contains original source material.
- `wiki/` contains structured research notes and synthesis.
- `scripts/` contains data collection and ingestion utilities.
- `outputs/` contains generated artifacts.

## General instructions

- Read relevant repository files before answering questions.
- Ground conclusions in repository content.
- Distinguish sourced facts from analysis and inference.
- Cite relevant file paths and headings.
- Do not modify files unless explicitly asked.
- Do not overwrite raw source material.
- Prefer small, reviewable changes.
'@

    "CLAUDE.md" = @'
# Claude Code Instructions

This repository contains a research wiki for the TopX Lyme disease challenge.

## Repository structure

- `raw_sources/` contains original source material.
- `wiki/` contains structured research notes and synthesis.
- `scripts/` contains data collection and ingestion utilities.
- `outputs/` contains generated artifacts.

## General instructions

- Read relevant repository files before answering questions.
- Ground conclusions in repository content.
- Distinguish sourced facts from analysis and inference.
- Cite relevant file paths and headings.
- Do not modify files unless explicitly asked.
- Do not overwrite raw source material.
- Prefer small, reviewable changes.
'@

    "README.md" = @'
# Lyme LLM Wiki

A repository for researching the TopX Lyme disease challenge, exploring relevant public datasets, and maintaining a structured LLM-assisted knowledge base.

## Repository structure

- `raw_sources/` — original documents, API results, papers, and challenge materials
- `wiki/` — structured summaries, concepts, datasets, questions, and analyses
- `scripts/` — data discovery and ingestion utilities
- `outputs/` — generated JSON and Markdown artifacts

## Getting started

1. Add original materials to `raw_sources/`.
2. Create structured summaries in `wiki/`.
3. Record research activity in `wiki/log.md`.
4. Track unanswered questions in `wiki/questions/`.
'@

    "wiki\index.md" = @'
# Wiki Index

## Core pages

- [Overview](overview.md)
- [Research Log](log.md)

## Sections

- [Entities](entities/)
- [Concepts](concepts/)
- [Datasets](datasets/)
- [Questions](questions/)
- [Analyses](analyses/)
'@

    "wiki\log.md" = @'
# Research Log

Record meaningful research, ingestion, and analysis activity here.

## Entries

'@

    "wiki\overview.md" = @'
# TopX Lyme Challenge Overview

## Challenge summary

To be completed.

## Current problem understanding

To be completed.

## Research priorities

To be completed.

## Key findings

To be completed.
'@

    "scripts\data_gov_search.py" = @'
"""Search Data.gov for datasets relevant to the Lyme LLM Wiki."""

from __future__ import annotations


def main() -> None:
    """Run the Data.gov discovery workflow."""
    raise NotImplementedError("Implement the Data.gov search workflow.")


if __name__ == "__main__":
    main()
'@

    "scripts\ingest_source.py" = @'
"""Ingest a source document into the Lyme LLM Wiki workflow."""

from __future__ import annotations


def main() -> None:
    """Run the source ingestion workflow."""
    raise NotImplementedError("Implement the source ingestion workflow.")


if __name__ == "__main__":
    main()
'@
}

Write-Host ""
Write-Host "Initializing Lyme LLM Wiki at:" -ForegroundColor Cyan
Write-Host "  $RootPath"
Write-Host ""

foreach ($RelativePath in $Directories) {
    $FullPath = Join-Path -Path $RootPath -ChildPath $RelativePath

    if (Test-Path -LiteralPath $FullPath) {
        Write-Host "[EXISTS]  $RelativePath" -ForegroundColor DarkGray
        continue
    }

    New-Item `
        -ItemType Directory `
        -Path $FullPath `
        -Force | Out-Null

    Write-Host "[CREATED] $RelativePath" -ForegroundColor Green
}

foreach ($Entry in $Files.GetEnumerator()) {
    $RelativePath = $Entry.Key
    $Content = $Entry.Value
    $FullPath = Join-Path -Path $RootPath -ChildPath $RelativePath

    if (Test-Path -LiteralPath $FullPath) {
        Write-Host "[EXISTS]  $RelativePath" -ForegroundColor DarkGray
        continue
    }

    $ParentDirectory = Split-Path -Path $FullPath -Parent

    if (-not (Test-Path -LiteralPath $ParentDirectory)) {
        New-Item `
            -ItemType Directory `
            -Path $ParentDirectory `
            -Force | Out-Null
    }

    Set-Content `
        -LiteralPath $FullPath `
        -Value $Content `
        -Encoding utf8

    Write-Host "[CREATED] $RelativePath" -ForegroundColor Green
}

Write-Host ""
Write-Host "Wiki structure created successfully." -ForegroundColor Cyan
Write-Host ""
Write-Host "Open the project in VS Code with:" -ForegroundColor Cyan
Write-Host "  code ."
Write-Host ""