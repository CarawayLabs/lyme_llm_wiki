# CDCC-0024: notifiable disease Lyme

- Catalog: Data.CDC.gov / Socrata Catalog (`data_cdc_gov`)
- Query mode: `catalog_search`
- Priority/theme: `P0` / `surveillance_public_health`
- Endpoint: `GET https://api.us.socrata.com/api/catalog/v1`
- Retrieval URL: `https://api.us.socrata.com/api/catalog/v1?search_context=data.cdc.gov&q=notifiable+disease+Lyme&limit=100`
- Auth alias: `CDC_SOCRATA_APP_TOKEN`; credential sent: yes
- HTTP status: `200`
- Records normalized from this page: `9`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\data_cdc_gov\CDCC-0024_notifiable-disease-lyme\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\data_cdc_gov\CDCC-0024_notifiable-disease-lyme\json\page_0001.json`

## Search Intent

Human case counts, surveillance definitions, geographic trends, reporting limitations, and prevention assets.

## Downstream Use

Build geographic and temporal outcome layers and document surveillance caveats.

## Pagination And Rate Notes

- Pagination: Increment offset by limit until resultSetSize is exhausted.
- Rate limit note: Anonymous queries work, but an X-App-Token is recommended for automated exploration.

## Interpretation Notes

After discovery, fetch /api/views/{dataset_id} for schema and /resource/{dataset_id}.json for rows.
