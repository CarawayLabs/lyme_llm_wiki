# EPA-0006: population density

- Catalog: EPA EnviroAtlas Web Services (`epa_enviroatlas`)
- Query mode: `geospatial_layer_search`
- Priority/theme: `P2` / `equity_context`
- Endpoint: `GET https://www.epa.gov/enviroatlas/enviroatlas-web-services`
- Retrieval URL: `https://www.epa.gov/enviroatlas/enviroatlas-web-services?layer_search_term=population+density&preferred_formats=GeoJSON&preferred_formats=CSV&preferred_formats=WFS&preferred_formats=ArcGIS+REST`
- Auth alias: `none`; credential sent: no
- HTTP status: `202`
- Records normalized from this page: `0`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\epa_enviroatlas\EPA-0006_population-density\raw\page_0001.html`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\epa_enviroatlas\EPA-0006_population-density\json\page_0001.json`

## Search Intent

Area-level or population-level access, vulnerability, insurance, transportation, language, and digital-access context.

## Downstream Use

Test whether proposed tools could reduce or worsen disparities.

## Pagination And Rate Notes

- Pagination: Enumerate services/layers, then use the selected service's ArcGIS REST or OGC pagination.
- Rate limit note: Throttle conservatively and retry 429/5xx with exponential backoff.

## Interpretation Notes

Select only layers tied to a defensible hypothesis; do not ingest the entire catalog.
