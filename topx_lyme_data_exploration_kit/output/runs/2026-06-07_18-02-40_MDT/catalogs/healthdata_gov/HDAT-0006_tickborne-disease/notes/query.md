# HDAT-0006: tickborne disease

- Catalog: HealthData.gov / Socrata Catalog (`healthdata_gov`)
- Query mode: `catalog_search`
- Priority/theme: `P0` / `disease_core`
- Endpoint: `GET https://api.us.socrata.com/api/catalog/v1`
- Retrieval URL: `https://api.us.socrata.com/api/catalog/v1?search_context=healthdata.gov&q=tickborne+disease&limit=100`
- Auth alias: `HEALTHDATA_SOCRATA_APP_TOKEN`; credential sent: no
- HTTP status: `200`
- Records normalized from this page: `12`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\healthdata_gov\HDAT-0006_tickborne-disease\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\healthdata_gov\HDAT-0006_tickborne-disease\json\page_0001.json`

## Search Intent

Core disease, pathogen, vector, and syndrome records that define the Lyme problem space.

## Downstream Use

Build the disease/pathogen terminology graph and identify authoritative baseline datasets.

## Pagination And Rate Notes

- Pagination: Increment offset by limit until resultSetSize is exhausted.
- Rate limit note: Anonymous queries work, but an X-App-Token gives a separate, higher-throttle request pool.

## Interpretation Notes

Use X-App-Token when available. Some results are links to other HHS systems rather than row-level datasets.
