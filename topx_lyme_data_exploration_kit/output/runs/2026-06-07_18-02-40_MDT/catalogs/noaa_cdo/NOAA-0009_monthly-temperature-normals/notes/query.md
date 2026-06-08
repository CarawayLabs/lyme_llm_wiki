# NOAA-0009: monthly temperature normals

- Catalog: NOAA Climate Data Online API v2 (`noaa_cdo`)
- Query mode: `record_search`
- Priority/theme: `P1` / `ecology_climate`
- Endpoint: `GET https://www.ncei.noaa.gov/cdo-web/api/v2/data`
- Retrieval URL: `https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=MLY-TAVG-NORMAL&startdate=2024-05-01&enddate=2024-05-07&locationid=FIPS%3A24&limit=1000&offset=1&units=standard`
- Auth alias: `NOAA_CDO_TOKEN`; credential sent: yes
- HTTP status: `200`
- Records normalized from this page: `1`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\noaa_cdo\NOAA-0009_monthly-temperature-normals\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\noaa_cdo\NOAA-0009_monthly-temperature-normals\json\page_0001.json`

## Search Intent

Tick ecology, weather, climate, habitat, land-cover, hosts, and geographic-risk features.

## Downstream Use

Construct environmental context and risk features without treating correlation as causation.

## Pagination And Rate Notes

- Pagination: Increase offset by limit; read metadata.resultset.count to stop.
- Rate limit note: Limit is 5 requests/second and 10,000 requests/day per token.

## Interpretation Notes

Use station-quality flags and coverage checks. Climate correlation alone does not establish causation.
