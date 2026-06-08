# FDAE-0005: azithromycin adverse events

- Catalog: openFDA Drug Adverse Event API (`openfda_drug_event`)
- Query mode: `record_search`
- Priority/theme: `P2` / `treatment`
- Endpoint: `GET https://api.fda.gov/drug/event.json`
- Retrieval URL: `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name%3A%22azithromycin%22&limit=100`
- Auth alias: `OPENFDA_API_KEY`; credential sent: no
- HTTP status: `200`
- Records normalized from this page: `100`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\openfda_drug_event\FDAE-0005_azithromycin-adverse-events\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\openfda_drug_event\FDAE-0005_azithromycin-adverse-events\json\page_0001.json`

## Search Intent

Interventions, medications, treatment duration, comparative effectiveness, outcomes, and safety evidence.

## Downstream Use

Map current interventions, evidence gaps, safety signals, and treatment-navigation needs.

## Pagination And Rate Notes

- Pagination: Use skip/limit; use count endpoints for aggregate exploration before pulling reports.
- Rate limit note: Public access works without a key, but a key provides higher quotas.

## Interpretation Notes

Spontaneous reports are signal-generating and cannot establish incidence or causation.
