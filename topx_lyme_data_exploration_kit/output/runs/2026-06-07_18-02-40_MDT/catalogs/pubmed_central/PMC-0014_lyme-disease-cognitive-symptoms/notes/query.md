# PMC-0014: Lyme disease cognitive symptoms

- Catalog: NCBI PubMed Central E-utilities (`pubmed_central`)
- Query mode: `record_search`
- Priority/theme: `P1` / `symptoms_outcomes`
- Endpoint: `GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
- Retrieval URL: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=%28%22Lyme+disease+cognitive+symptoms%22%5BTitle%2FAbstract%5D%29+AND+open+access%5Bfilter%5D&retmode=json&retmax=100&usehistory=y&tool=topx_lyme_explorer`
- Auth alias: `NCBI_API_KEY`; credential sent: no
- HTTP status: `200`
- Records normalized from this page: `0`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\pubmed_central\PMC-0014_lyme-disease-cognitive-symptoms\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\pubmed_central\PMC-0014_lyme-disease-cognitive-symptoms\json\page_0001.json`

## Search Intent

Symptoms, complications, disability, utilization, and patient-reported outcome information.

## Downstream Use

Characterize patient burden and prioritize outcomes a Phase 1 concept should improve.

## Pagination And Rate Notes

- Pagination: Use history server plus batched ESummary/EFetch retrieval.
- Rate limit note: Same NCBI E-utilities limits as PubMed.

## Interpretation Notes

Confirm article-specific reuse rights before storing or redistributing full text.
