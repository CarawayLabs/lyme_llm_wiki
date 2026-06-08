# FDAL-0005: azithromycin

- Catalog: openFDA Drug Label API (`openfda_drug_label`)
- Query mode: `record_search`
- Priority/theme: `P1` / `treatment`
- Endpoint: `GET https://api.fda.gov/drug/label.json`
- Retrieval URL: `https://api.fda.gov/drug/label.json?search=openfda.generic_name%3A%22azithromycin%22&limit=100`
- Auth alias: `OPENFDA_API_KEY`; credential sent: no
- HTTP status: `200`
- Records normalized from this page: `100`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\openfda_drug_label\FDAL-0005_azithromycin\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\openfda_drug_label\FDAL-0005_azithromycin\json\page_0001.json`

## Search Intent

Interventions, medications, treatment duration, comparative effectiveness, outcomes, and safety evidence.

## Downstream Use

Map current interventions, evidence gaps, safety signals, and treatment-navigation needs.

## Pagination And Rate Notes

- Pagination: Use skip/limit within openFDA limits; split broad queries by date or drug when necessary.
- Rate limit note: Public access works without a key, but a key provides higher quotas.

## Interpretation Notes

Use labels for official product information, not proof of comparative effectiveness.
