# TICK-0006: Babesia microti tick pathogen detections

- Catalog: CDC Tick Surveillance Data Sets (`cdc_tick_surveillance`)
- Query mode: `download_manifest`
- Priority/theme: `P0` / `ecology_climate`
- Endpoint: `GET https://www.cdc.gov/ticks/data-research/facts-stats/tick-surveillance-data-sets.html`
- Retrieval URL: `https://www.cdc.gov/ticks/data-research/facts-stats/tick-surveillance-data-sets.html?target_asset_description=County-level+pathogen+detection+records`
- Auth alias: `none`; credential sent: no
- HTTP status: `200`
- Records normalized from this page: `0`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cdc_tick_surveillance\TICK-0006_babesia-microti-tick-pathogen-detections\raw\page_0001.html`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cdc_tick_surveillance\TICK-0006_babesia-microti-tick-pathogen-detections\json\page_0001.json`

## Search Intent

Tick ecology, weather, climate, habitat, land-cover, hosts, and geographic-risk features.

## Downstream Use

Construct environmental context and risk features without treating correlation as causation.

## Pagination And Rate Notes

- Pagination: No API pagination; enumerate linked files, record checksums, and download each once.
- Rate limit note: Throttle conservatively and retry 429/5xx with exponential backoff.

## Interpretation Notes

A no-records value is not evidence of absence. Preserve sampling and status definitions.
