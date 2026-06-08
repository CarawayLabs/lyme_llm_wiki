# HDAT-0012: Lyme disease provider shortage

- Catalog: HealthData.gov / Socrata Catalog (`healthdata_gov`)
- Query mode: `catalog_search`
- Priority/theme: `P1` / `care_access`
- Endpoint: `GET https://api.us.socrata.com/api/catalog/v1`
- Retrieval URL: `https://api.us.socrata.com/api/catalog/v1?search_context=healthdata.gov&q=Lyme+disease+provider+shortage&limit=100`
- Auth alias: `HEALTHDATA_SOCRATA_APP_TOKEN`; credential sent: no
- HTTP status: `200`
- Records normalized from this page: `100`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\healthdata_gov\HDAT-0012_lyme-disease-provider-shortage\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\healthdata_gov\HDAT-0012_lyme-disease-provider-shortage\json\page_0001.json`

## Search Intent

Providers, facilities, travel burden, utilization, cost, referral, wait-time, and navigation signals.

## Downstream Use

Identify care deserts and product opportunities in navigation, referral, and access.

## Pagination And Rate Notes

- Pagination: Increment offset by limit until resultSetSize is exhausted.
- Rate limit note: Anonymous queries work, but an X-App-Token gives a separate, higher-throttle request pool.

## Interpretation Notes

Use X-App-Token when available. Some results are links to other HHS systems rather than row-level datasets.
