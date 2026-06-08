# CTG-0021: Lyme babesiosis coinfection

- Catalog: ClinicalTrials.gov API v2 (`clinicaltrials_gov`)
- Query mode: `record_search`
- Priority/theme: `P1` / `coinfections`
- Endpoint: `GET https://clinicaltrials.gov/api/v2/studies`
- Retrieval URL: `https://clinicaltrials.gov/api/v2/studies?query.cond=Lyme+babesiosis+coinfection&query.term=Lyme+babesiosis+coinfection&pageSize=100&format=json&countTotal=true`
- Auth alias: `none`; credential sent: no
- HTTP status: `200`
- Records normalized from this page: `0`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\clinicaltrials_gov\CTG-0021_lyme-babesiosis-coinfection\raw\page_0001.bin`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\clinicaltrials_gov\CTG-0021_lyme-babesiosis-coinfection\json\page_0001.json`

## Search Intent

Other tickborne pathogens, coinfection patterns, and related surveillance or clinical evidence.

## Downstream Use

Identify where single-disease workflows miss clinically relevant tickborne conditions.

## Pagination And Rate Notes

- Pagination: Pass nextPageToken from the previous response.
- Rate limit note: No API key is documented for public API v2; use a descriptive User-Agent and conservative concurrency.

## Interpretation Notes

Registry data are not patient-level data. Preserve study status, design, eligibility, outcomes, results-posting status, and update date.
