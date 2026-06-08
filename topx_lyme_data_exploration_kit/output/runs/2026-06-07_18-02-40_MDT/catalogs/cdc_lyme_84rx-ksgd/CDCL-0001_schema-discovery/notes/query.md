# CDCL-0001: schema discovery

- Catalog: CDC Lyme surveillance 1992-2007 (`cdc_lyme_84rx-ksgd`)
- Query mode: `schema_discovery`
- Priority/theme: `P0` / `surveillance_public_health`
- Endpoint: `GET https://data.cdc.gov/api/views/84rx-ksgd`
- Retrieval URL: `https://data.cdc.gov/api/views/84rx-ksgd`
- Auth alias: `CDC_SOCRATA_APP_TOKEN`; credential sent: yes
- HTTP status: `200`
- Records normalized from this page: `1`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cdc_lyme_84rx-ksgd\CDCL-0001_schema-discovery\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cdc_lyme_84rx-ksgd\CDCL-0001_schema-discovery\json\page_0001.json`

## Search Intent

Human case counts, surveillance definitions, geographic trends, reporting limitations, and prevention assets.

## Downstream Use

Build geographic and temporal outcome layers and document surveillance caveats.

## Pagination And Rate Notes

- Pagination: For row APIs, use $limit/$offset or download the full CSV once.
- Rate limit note: Use an X-App-Token for repeatable automated access.

## Interpretation Notes

Fetch field names, types, descriptions, and metadata before constructing SoQL. Surveillance location is not necessarily exposure location; preserve case-definition vintage.
