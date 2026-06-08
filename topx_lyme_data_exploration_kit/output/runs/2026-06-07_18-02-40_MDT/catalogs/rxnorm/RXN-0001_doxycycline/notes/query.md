# RXN-0001: doxycycline

- Catalog: NLM RxNorm API (`rxnorm`)
- Query mode: `terminology_lookup`
- Priority/theme: `P1` / `treatment`
- Endpoint: `GET https://rxnav.nlm.nih.gov/REST/approximateTerm.json`
- Retrieval URL: `https://rxnav.nlm.nih.gov/REST/approximateTerm.json?term=doxycycline&maxEntries=20&option=1`
- Auth alias: `none`; credential sent: no
- HTTP status: `200`
- Records normalized from this page: `1`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\rxnorm\RXN-0001_doxycycline\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\rxnorm\RXN-0001_doxycycline\json\page_0001.json`

## Search Intent

Interventions, medications, treatment duration, comparative effectiveness, outcomes, and safety evidence.

## Downstream Use

Map current interventions, evidence gaps, safety signals, and treatment-navigation needs.

## Pagination And Rate Notes

- Pagination: Not generally paginated for approximate-term lookup; follow returned RxCUIs with property/relationship calls.
- Rate limit note: Throttle conservatively and retry 429/5xx with exponential backoff.

## Interpretation Notes

Use RxNorm to normalize medication names returned by literature, trials, labels, and provider datasets.
