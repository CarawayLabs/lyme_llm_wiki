# NNDSS-0002: Babesiosis

- Catalog: CDC NNDSS Weekly Data (`cdc_nndss_weekly`)
- Query mode: `dataset_query`
- Priority/theme: `P1` / `coinfections`
- Endpoint: `GET https://data.cdc.gov/resource/x9gk-5huc.json`
- Retrieval URL: `https://data.cdc.gov/resource/x9gk-5huc.json?%24limit=5000`
- Auth alias: `CDC_SOCRATA_APP_TOKEN`; credential sent: yes
- HTTP status: `200`
- Records normalized from this page: `100`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cdc_nndss_weekly\NNDSS-0002_babesiosis\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cdc_nndss_weekly\NNDSS-0002_babesiosis\json\page_0001.json`

## Search Intent

Other tickborne pathogens, coinfection patterns, and related surveillance or clinical evidence.

## Downstream Use

Identify where single-disease workflows miss clinically relevant tickborne conditions.

## Pagination And Rate Notes

- Pagination: Use $limit/$offset after schema discovery; consider full CSV download for reproducibility.
- Rate limit note: Throttle conservatively and retry 429/5xx with exponential backoff.

## Interpretation Notes

Provisional data can be revised. Preserve publication date, reporting period, footnotes, and suppression markers.
