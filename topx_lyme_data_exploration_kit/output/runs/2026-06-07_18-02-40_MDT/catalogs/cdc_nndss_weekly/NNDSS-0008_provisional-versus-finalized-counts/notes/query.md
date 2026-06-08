# NNDSS-0008: provisional versus finalized counts

- Catalog: CDC NNDSS Weekly Data (`cdc_nndss_weekly`)
- Query mode: `dataset_query`
- Priority/theme: `P1` / `surveillance_public_health`
- Endpoint: `GET https://data.cdc.gov/resource/x9gk-5huc.json`
- Retrieval URL: `https://data.cdc.gov/resource/x9gk-5huc.json?%24limit=5000`
- Auth alias: `CDC_SOCRATA_APP_TOKEN`; credential sent: yes
- HTTP status: `200`
- Records normalized from this page: `100`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cdc_nndss_weekly\NNDSS-0008_provisional-versus-finalized-counts\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cdc_nndss_weekly\NNDSS-0008_provisional-versus-finalized-counts\json\page_0001.json`

## Search Intent

Human case counts, surveillance definitions, geographic trends, reporting limitations, and prevention assets.

## Downstream Use

Build geographic and temporal outcome layers and document surveillance caveats.

## Pagination And Rate Notes

- Pagination: Use $limit/$offset after schema discovery; consider full CSV download for reproducibility.
- Rate limit note: Throttle conservatively and retry 429/5xx with exponential backoff.

## Interpretation Notes

Provisional data can be revised. Preserve publication date, reporting period, footnotes, and suppression markers.
