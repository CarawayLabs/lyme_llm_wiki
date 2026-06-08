# CDCL-0015: JSON page sample

- Catalog: CDC Lyme surveillance 2022-2023 (`cdc_lyme_x5j9-wybp`)
- Query mode: `dataset_query`
- Priority/theme: `P0` / `surveillance_public_health`
- Endpoint: `GET https://data.cdc.gov/resource/x5j9-wybp.json`
- Retrieval URL: `https://data.cdc.gov/resource/x5j9-wybp.json?%24limit=1000&%24offset=0`
- Auth alias: `CDC_SOCRATA_APP_TOKEN`; credential sent: yes
- HTTP status: `200`
- Records normalized from this page: `100`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cdc_lyme_x5j9-wybp\CDCL-0015_json-page-sample\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cdc_lyme_x5j9-wybp\CDCL-0015_json-page-sample\json\page_0001.json`

## Search Intent

Human case counts, surveillance definitions, geographic trends, reporting limitations, and prevention assets.

## Downstream Use

Build geographic and temporal outcome layers and document surveillance caveats.

## Pagination And Rate Notes

- Pagination: For row APIs, use $limit/$offset or download the full CSV once.
- Rate limit note: Use an X-App-Token for repeatable automated access.

## Interpretation Notes

Fetch an initial JSON sample to test normalization. Surveillance location is not necessarily exposure location; preserve case-definition vintage.
