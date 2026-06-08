# NLCD-0008: county zonal statistics

- Catalog: USGS Annual National Land Cover Database (`usgs_annual_nlcd`)
- Query mode: `download_manifest`
- Priority/theme: `P2` / `ecology_climate`
- Endpoint: `GET https://www.usgs.gov/centers/eros/science/annual-nlcd-data-access`
- Retrieval URL: `https://www.usgs.gov/centers/eros/science/annual-nlcd-data-access?product_or_derived_feature=county+zonal+statistics&target_resolution=30m&derive_county_features=True`
- Auth alias: `none`; credential sent: no
- HTTP status: `200`
- Records normalized from this page: `0`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\usgs_annual_nlcd\NLCD-0008_county-zonal-statistics\raw\page_0001.html`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\usgs_annual_nlcd\NLCD-0008_county-zonal-statistics\json\page_0001.json`

## Search Intent

Tick ecology, weather, climate, habitat, land-cover, hosts, and geographic-risk features.

## Downstream Use

Construct environmental context and risk features without treating correlation as causation.

## Pagination And Rate Notes

- Pagination: Download selected annual products; process locally with a reproducible zonal-statistics pipeline.
- Rate limit note: Throttle conservatively and retry 429/5xx with exponential backoff.

## Interpretation Notes

Heavy geospatial work. Defer until a specific ecological hypothesis justifies the computation.
