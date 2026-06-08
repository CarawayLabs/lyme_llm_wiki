# AHRQ-0002: tickborne disease utilization

- Catalog: AHRQ Data Tools / MEPS / Community-Level Health (`ahrq`)
- Query mode: `download_manifest`
- Priority/theme: `P1` / `care_access`
- Endpoint: `GET https://datatools.ahrq.gov/`
- Retrieval URL: `https://datatools.ahrq.gov/?asset_search_term=tickborne+disease+utilization&capture_codebook=True`
- Auth alias: `none`; credential sent: no
- HTTP status: `200`
- Records normalized from this page: `0`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\ahrq\AHRQ-0002_tickborne-disease-utilization\raw\page_0001.html`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\ahrq\AHRQ-0002_tickborne-disease-utilization\json\page_0001.json`

## Search Intent

Providers, facilities, travel burden, utilization, cost, referral, wait-time, and navigation signals.

## Downstream Use

Identify care deserts and product opportunities in navigation, referral, and access.

## Pagination And Rate Notes

- Pagination: No single API; enumerate candidate files, codebooks, data-use terms, and download URLs.
- Rate limit note: Throttle conservatively and retry 429/5xx with exponential backoff.

## Interpretation Notes

Do not assume HCUP products are fully open. Record licensing, purchase, and data-use restrictions separately.
