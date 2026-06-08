# PUBM-0022: Lyme disease cognitive symptoms

- Catalog: NCBI PubMed E-utilities (`pubmed`)
- Query mode: `record_search`
- Priority/theme: `P1` / `symptoms_outcomes`
- Endpoint: `GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
- Retrieval URL: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%28%22Lyme+disease+cognitive+symptoms%22%5BTitle%2FAbstract%5D%29+AND+humans%5BMeSH+Terms%5D&retmode=json&retmax=100&usehistory=y&sort=pub+date&tool=topx_lyme_explorer`
- Auth alias: `NCBI_API_KEY`; credential sent: no
- HTTP status: `200`
- Records normalized from this page: `0`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\pubmed\PUBM-0022_lyme-disease-cognitive-symptoms\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\pubmed\PUBM-0022_lyme-disease-cognitive-symptoms\json\page_0001.json`

## Search Intent

Symptoms, complications, disability, utilization, and patient-reported outcome information.

## Downstream Use

Characterize patient burden and prioritize outcomes a Phase 1 concept should improve.

## Pagination And Rate Notes

- Pagination: Use WebEnv/query_key history plus retstart/retmax; retrieve details in batched ESummary/EFetch calls.
- Rate limit note: Without a key stay at or below 3 requests/second; with a key the default supported limit is 10 requests/second.

## Interpretation Notes

Do not assume all abstracts or full text are reusable. Capture publication type, retraction/correction status, and linked identifiers.
