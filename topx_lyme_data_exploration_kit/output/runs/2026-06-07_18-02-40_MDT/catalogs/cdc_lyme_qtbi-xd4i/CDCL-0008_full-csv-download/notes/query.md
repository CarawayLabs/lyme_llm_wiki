# CDCL-0008: full CSV download

- Catalog: CDC Lyme surveillance 2008-2021 (`cdc_lyme_qtbi-xd4i`)
- Query mode: `full_download`
- Priority/theme: `P0` / `surveillance_public_health`
- Endpoint: `GET https://data.cdc.gov/api/views/qtbi-xd4i/rows.csv?accessType=DOWNLOAD`
- Retrieval URL: `https://data.cdc.gov/api/views/qtbi-xd4i/rows.csv?accessType=DOWNLOAD`
- Auth alias: `CDC_SOCRATA_APP_TOKEN`; credential sent: yes
- HTTP status: `200`
- Records normalized from this page: `0`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cdc_lyme_qtbi-xd4i\CDCL-0008_full-csv-download\raw\page_0001.csv`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cdc_lyme_qtbi-xd4i\CDCL-0008_full-csv-download\json\page_0001.json`

## Search Intent

Human case counts, surveillance definitions, geographic trends, reporting limitations, and prevention assets.

## Downstream Use

Build geographic and temporal outcome layers and document surveillance caveats.

## Pagination And Rate Notes

- Pagination: For row APIs, use $limit/$offset or download the full CSV once.
- Rate limit note: Use an X-App-Token for repeatable automated access.

## Interpretation Notes

Download the complete public-use aggregate file for local profiling. Surveillance location is not necessarily exposure location; preserve case-definition vintage.
