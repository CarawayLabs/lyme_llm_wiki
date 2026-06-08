# HDAT-0018: Lyme disease underserved communities

- Catalog: HealthData.gov / Socrata Catalog (`healthdata_gov`)
- Query mode: `catalog_search`
- Priority/theme: `P1` / `equity_context`
- Endpoint: `GET https://api.us.socrata.com/api/catalog/v1`
- Retrieval URL: `https://api.us.socrata.com/api/catalog/v1?search_context=healthdata.gov&q=Lyme+disease+underserved+communities&limit=100`
- Auth alias: `HEALTHDATA_SOCRATA_APP_TOKEN`; credential sent: no
- HTTP status: `200`
- Records normalized from this page: `100`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\healthdata_gov\HDAT-0018_lyme-disease-underserved-communities\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\healthdata_gov\HDAT-0018_lyme-disease-underserved-communities\json\page_0001.json`

## Search Intent

Area-level or population-level access, vulnerability, insurance, transportation, language, and digital-access context.

## Downstream Use

Test whether proposed tools could reduce or worsen disparities.

## Pagination And Rate Notes

- Pagination: Increment offset by limit until resultSetSize is exhausted.
- Rate limit note: Anonymous queries work, but an X-App-Token gives a separate, higher-throttle request pool.

## Interpretation Notes

Use X-App-Token when available. Some results are links to other HHS systems rather than row-level datasets.
