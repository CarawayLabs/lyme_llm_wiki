# SVI-0004: household characteristics theme

- Catalog: CDC/ATSDR Social Vulnerability Index (`cdc_svi`)
- Query mode: `download_manifest`
- Priority/theme: `P0` / `equity_context`
- Endpoint: `GET https://www.atsdr.cdc.gov/place-health/php/svi/svi-data-documentation-download.html`
- Retrieval URL: `https://www.atsdr.cdc.gov/place-health/php/svi/svi-data-documentation-download.html?geography=tract&capture_csv_and_documentation=True`
- Auth alias: `none`; credential sent: no
- HTTP status: `200`
- Records normalized from this page: `0`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cdc_svi\SVI-0004_household-characteristics-theme\raw\page_0001.html`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cdc_svi\SVI-0004_household-characteristics-theme\json\page_0001.json`

## Search Intent

Area-level or population-level access, vulnerability, insurance, transportation, language, and digital-access context.

## Downstream Use

Test whether proposed tools could reduce or worsen disparities.

## Pagination And Rate Notes

- Pagination: Download the selected vintage and geography files once; preserve checksums and documentation.
- Rate limit note: Throttle conservatively and retry 429/5xx with exponential backoff.

## Interpretation Notes

SVI is an area-level index, not an individual characteristic. Align vintage and geographic boundaries with outcome data.
