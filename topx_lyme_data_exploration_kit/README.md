# TOPx Lyme Data Exploration: API Access and Output Contract

Verified against official documentation on **2026-06-07**.

## API keys or tokens you should obtain

### Required

- **Data.gov Catalog API** — `DATA_GOV_API_KEY`
  - Get it: https://api.data.gov/signup/
  - Use the personal key for automated work. DEMO_KEY has very low limits.
- **U.S. Census Data API** — `CENSUS_API_KEY`
  - Get it: https://api.census.gov/data/key_signup.html
  - All Census Data API queries now require a key.
- **NOAA Climate Data Online API v2** — `NOAA_CDO_TOKEN`
  - Get it: https://www.ncei.noaa.gov/cdo-web/token
  - Send the token in the token request header.

### Optional but recommended

- **Data.CDC.gov Socrata APIs** — `CDC_SOCRATA_APP_TOKEN`
  - Get it: https://data.cdc.gov/profile/edit/developer_settings
  - Anonymous reads work; an app token provides a separate, higher-throttle request pool.
- **HealthData.gov Socrata APIs** — `HEALTHDATA_SOCRATA_APP_TOKEN`
  - Get it: https://healthdata.gov/profile/edit/developer_settings
  - Anonymous reads work; use an app token for repeatable automated exploration.
- **NCBI E-utilities: PubMed and PMC** — `NCBI_API_KEY`
  - Get it: https://www.ncbi.nlm.nih.gov/account/settings/
  - Without a key, remain at or below 3 requests/second; a key supports 10 requests/second by default.
- **openFDA** — `OPENFDA_API_KEY`
  - Get it: https://open.fda.gov/apis/authentication/
  - Public calls work without a key, but a key provides higher quotas.

### No API token required for normal public access

- ClinicalTrials.gov API v2
- NIH RePORTER API v2
- CMS public dataset APIs and Provider Data Catalog
- RxNorm API
- CDC WONDER public API
- CDC Tick Surveillance public downloads
- CDC/ATSDR SVI public downloads
- USGS Annual NLCD public data-access pages
- EPA EnviroAtlas public web services
- AHRQ public-use downloads (some separate products, especially HCUP, may have licensing or purchase requirements)

Do not store actual secrets in output JSON. Store only the environment-variable name or credential alias used.

## Recommended output folders

```text
output/
├── runs/
│   └── {YYYY-MM-DD_HH-MM-SS_MDT-or-MST}/
│       ├── run_manifest.json
│       ├── search_summary.csv
│       └── errors.jsonl
├── raw/
│   └── {catalog_slug}/{search_id}/page_0001.json
├── normalized/
│   └── {catalog_slug}/{search_id}.jsonl
├── records/
│   └── {catalog_slug}/{normalized_id}.json
├── downloads/
│   └── {catalog_slug}/{source_filename}
└── reports/
    ├── catalog_coverage.csv
    ├── duplicate_candidates.csv
    └── manual_review_queue.csv
```

### Why both raw and normalized data

- `raw/` preserves the source response exactly enough to reproduce and debug parsing.
- `normalized/` contains one normalized record per JSONL line for scalable downstream processing.
- `records/` is optional and useful when you want one durable file per important dataset, paper, trial, provider, grant, or layer.
- `run_manifest.json` records code version, configuration, timestamps, pagination, failures, and counts.

## How to use the CSV

1. Run `P0` rows first. They cover the minimum viable discovery stack.
2. Execute rows whose `requires_schema_discovery` value is `false` directly.
3. For schema-first rows, fetch metadata or documentation, map real field names, then build the final query.
4. For `download_manifest` rows, save the source file, checksum, documentation, license, and vintage before parsing.
5. Store raw response pages using the JSON schema in this kit, then write normalized records as JSONL.
6. Deduplicate within each source first, then across sources using canonical identifiers and URLs.

## Important interpretation safeguards

- CDC human surveillance uses aggregated public-health data; it is not individual diagnostic training data.
- County of residence may not equal exposure location.
- Surveillance definitions and reporting practices change over time.
- Tick/pathogen `no records` does not prove absence.
- Area-level ACS and SVI values do not describe every individual in that area.
- Spontaneous adverse-event reports do not establish incidence or causation.
- Funding, trial registration, and publication do not by themselves establish clinical validity.

## Official documentation used

- Data.gov Catalog API: https://resources.data.gov/catalog-api/
- Census Data API: https://www.census.gov/data/developers/guidance/api-user-guide.html
- NOAA CDO API v2: https://www.ncei.noaa.gov/cdo-web/webservices/v2
- Socrata application tokens: https://dev.socrata.com/docs/app-tokens.html
- NCBI E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25497/
- ClinicalTrials.gov API: https://clinicaltrials.gov/data-api/api
- NIH RePORTER API: https://api.reporter.nih.gov/
- CDC WONDER API: https://wonder.cdc.gov/wonder/help/wonder-api.html
- RxNorm API: https://lhncbc.nlm.nih.gov/RxNav/APIs/RxNormAPIs.html
- openFDA APIs: https://open.fda.gov/apis/
