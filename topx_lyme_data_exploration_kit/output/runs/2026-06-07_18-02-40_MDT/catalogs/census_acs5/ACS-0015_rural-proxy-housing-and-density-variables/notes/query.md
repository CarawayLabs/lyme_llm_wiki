# ACS-0015: rural proxy housing and density variables

- Catalog: U.S. Census ACS 5-Year API (`census_acs5`)
- Query mode: `variable_query`
- Priority/theme: `P1` / `equity_context`
- Endpoint: `GET https://api.census.gov/data/2024/acs/acs5`
- Retrieval URL: `https://api.census.gov/data/2024/acs/acs5?get=NAME%2Cgroup%28B25001%29&for=county%3A%2A&key=%3Credacted%3E`
- Auth alias: `CENSUS_API_KEY`; credential sent: yes
- HTTP status: `200`
- Records normalized from this page: `100`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\census_acs5\ACS-0015_rural-proxy-housing-and-density-variables\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\census_acs5\ACS-0015_rural-proxy-housing-and-density-variables\json\page_0001.json`

## Search Intent

Area-level or population-level access, vulnerability, insurance, transportation, language, and digital-access context.

## Downstream Use

Test whether proposed tools could reduce or worsen disparities.

## Pagination And Rate Notes

- Pagination: No page cursor for this county query; split by state or geography level when requesting tract/block-group data.
- Rate limit note: All Census Data API queries require a key as of 2026; avoid excessively wide group requests.

## Interpretation Notes

Expected use: Housing/density context. Preserve estimate and margin-of-error variables; do not treat ZCTA as postal ZIP.
