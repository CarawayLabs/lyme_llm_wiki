# CMSP-0015: urgent care

- Catalog: CMS Provider Data Catalog (`cms_provider_data`)
- Query mode: `catalog_search`
- Priority/theme: `P1` / `care_access`
- Endpoint: `GET https://data.cms.gov/provider-data/`
- Retrieval URL: `https://data.cms.gov/provider-data/?provider_or_facility_focus=urgent+care&follow_access_api_link=True`
- Auth alias: `none`; credential sent: no
- HTTP status: `200`
- Records normalized from this page: `0`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cms_provider_data\CMSP-0015_urgent-care\raw\page_0001.html`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\cms_provider_data\CMSP-0015_urgent-care\json\page_0001.json`

## Search Intent

Providers, facilities, travel burden, utilization, cost, referral, wait-time, and navigation signals.

## Downstream Use

Identify care deserts and product opportunities in navigation, referral, and access.

## Pagination And Rate Notes

- Pagination: Dataset-specific after selecting the appropriate Provider Data dataset.
- Rate limit note: Throttle conservatively and retry 429/5xx with exponential backoff.

## Interpretation Notes

Open provider data may be incomplete or stale for certain navigation uses. Record data vintage and verify specialty/location fields.
