# DGOV-0038: neurology access Lyme

- Catalog: Data.gov Catalog API (`data_gov`)
- Query mode: `catalog_search`
- Priority/theme: `P1` / `care_access`
- Endpoint: `GET https://api.gsa.gov/technology/datagov/v4/search`
- Retrieval URL: `https://api.gsa.gov/technology/datagov/v4/search?q=neurology+access+Lyme&sort=relevance&per_page=100`
- Auth alias: `DATA_GOV_API_KEY`; credential sent: yes
- HTTP status: `200`
- Records normalized from this page: `0`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\data_gov\DGOV-0038_neurology-access-lyme\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\data_gov\DGOV-0038_neurology-access-lyme\json\page_0001.json`

## Search Intent

Providers, facilities, travel burden, utilization, cost, referral, wait-time, and navigation signals.

## Downstream Use

Identify care deserts and product opportunities in navigation, referral, and access.

## Pagination And Rate Notes

- Pagination: Use the returned after cursor with otherwise identical parameters.
- Rate limit note: Personal key: respect response rate-limit headers; DEMO_KEY is unsuitable for automated exploration.

## Interpretation Notes

Metadata discovery only; follow distribution or landing-page URLs to obtain actual data.
