# NIHR-0011: Lyme disease misdiagnosis

- Catalog: NIH RePORTER API v2 (`nih_reporter`)
- Query mode: `record_search`
- Priority/theme: `P1` / `diagnosis_testing`
- Endpoint: `POST https://api.reporter.nih.gov/v2/projects/search`
- Retrieval URL: `https://api.reporter.nih.gov/v2/projects/search`
- Auth alias: `none`; credential sent: no
- HTTP status: `200`
- Records normalized from this page: `1`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\nih_reporter\NIHR-0011_lyme-disease-misdiagnosis\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\nih_reporter\NIHR-0011_lyme-disease-misdiagnosis\json\page_0001.json`

## Search Intent

Diagnostic tests, accuracy evidence, biomarkers, delays, false results, and differential-diagnosis resources.

## Downstream Use

Map diagnostic failure modes and candidate opportunities for faster, clearer testing and interpretation.

## Pagination And Rate Notes

- Pagination: Increase offset by limit; maximum project offset is constrained, so split broad searches by fiscal year if needed.
- Rate limit note: No API key is documented; avoid parallel scraping and prefer bulk export for very large retrievals.

## Interpretation Notes

Funding is not evidence that a hypothesis is validated. Preserve project dates, award amounts, investigators, organizations, and public-health relevance.
