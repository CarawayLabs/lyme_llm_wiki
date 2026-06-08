# CMSD-0008: Medicare geographic variation

- Catalog: CMS Data Catalog (`cms_data`)
- Query mode: `catalog_search`
- Priority/theme: `P1` / `treatment`
- Endpoint: `GET https://data.cms.gov/`
- Retrieval URL: `https://data.cms.gov/?catalog_search_term=Medicare+geographic+variation&follow_access_api_link=True`
- Auth alias: `none`; credential sent: no
- HTTP status: `200`
- Records normalized from this page: `0`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cms_data\CMSD-0008_medicare-geographic-variation\raw\page_0001.html`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cms_data\CMSD-0008_medicare-geographic-variation\json\page_0001.json`

## Search Intent

Interventions, medications, treatment duration, comparative effectiveness, outcomes, and safety evidence.

## Downstream Use

Map current interventions, evidence gaps, safety signals, and treatment-navigation needs.

## Pagination And Rate Notes

- Pagination: Catalog-specific. Once a dataset is selected, use its published API endpoint or downloadable file.
- Rate limit note: Throttle conservatively and retry 429/5xx with exponential backoff.

## Interpretation Notes

CMS APIs are dataset-specific. First capture dataset UUID, version, schema, update cadence, and API/download links.
