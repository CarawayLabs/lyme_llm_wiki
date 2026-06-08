# CDCC-0010: erythema migrans

- Catalog: Data.CDC.gov / Socrata Catalog (`data_cdc_gov`)
- Query mode: `catalog_search`
- Priority/theme: `P0` / `disease_core`
- Endpoint: `GET https://api.us.socrata.com/api/catalog/v1`
- Retrieval URL: `https://api.us.socrata.com/api/catalog/v1?search_context=data.cdc.gov&q=erythema+migrans&limit=100`
- Auth alias: `CDC_SOCRATA_APP_TOKEN`; credential sent: yes
- HTTP status: `200`
- Records normalized from this page: `3`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\data_cdc_gov\CDCC-0010_erythema-migrans\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\data_cdc_gov\CDCC-0010_erythema-migrans\json\page_0001.json`

## Search Intent

Core disease, pathogen, vector, and syndrome records that define the Lyme problem space.

## Downstream Use

Build the disease/pathogen terminology graph and identify authoritative baseline datasets.

## Pagination And Rate Notes

- Pagination: Increment offset by limit until resultSetSize is exhausted.
- Rate limit note: Anonymous queries work, but an X-App-Token is recommended for automated exploration.

## Interpretation Notes

After discovery, fetch /api/views/{dataset_id} for schema and /resource/{dataset_id}.json for rows.
