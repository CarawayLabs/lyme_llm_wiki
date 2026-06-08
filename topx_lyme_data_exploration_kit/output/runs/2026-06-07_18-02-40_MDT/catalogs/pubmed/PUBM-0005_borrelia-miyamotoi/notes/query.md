# PUBM-0005: Borrelia miyamotoi

- Catalog: NCBI PubMed E-utilities (`pubmed`)
- Query mode: `record_search`
- Priority/theme: `P0` / `disease_core`
- Endpoint: `GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
- Retrieval URL: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%28%22Borrelia+miyamotoi%22%5BTitle%2FAbstract%5D%29+AND+humans%5BMeSH+Terms%5D&retmode=json&retmax=100&usehistory=y&sort=pub+date&tool=topx_lyme_explorer`
- Auth alias: `NCBI_API_KEY`; credential sent: no
- HTTP status: `200`
- Records normalized from this page: `100`
- Raw response: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\pubmed\PUBM-0005_borrelia-miyamotoi\raw\page_0001.json`
- JSON envelope: `C:\codex_programming\lyme_llm_wiki\topx_lyme_data_exploration_kit\output\runs\2026-06-07_18-02-40_MDT\catalogs\pubmed\PUBM-0005_borrelia-miyamotoi\json\page_0001.json`

## Search Intent

Core disease, pathogen, vector, and syndrome records that define the Lyme problem space.

## Downstream Use

Build the disease/pathogen terminology graph and identify authoritative baseline datasets.

## Pagination And Rate Notes

- Pagination: Use WebEnv/query_key history plus retstart/retmax; retrieve details in batched ESummary/EFetch calls.
- Rate limit note: Without a key stay at or below 3 requests/second; with a key the default supported limit is 10 requests/second.

## Interpretation Notes

Do not assume all abstracts or full text are reusable. Capture publication type, retraction/correction status, and linked identifiers.
