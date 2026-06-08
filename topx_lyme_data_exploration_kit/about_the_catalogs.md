---------

# What matters most at step 0

The TOPx challenge is asking teams to turn U.S. Open Data into practical AI-enabled tools that help people obtain answers and access care more quickly. That framing matters: you are not looking for one perfect Lyme database. You are looking for several incomplete datasets that can be combined around a specific patient, clinician, researcher, or public-health problem. Phase 1 currently closes **June 30, 2026, at 11:59 PM ET**, so I would not spend the entire month cataloging data before selecting a problem. ([HHS.gov][1])

## Succinct list of organizations and catalogs

### Core discovery and Lyme data

* **HealthData.gov** — the main HHS open-data catalog.
* **Data.gov** — the government-wide dataset metadata catalog.
* **CDC Data.CDC.gov** — downloadable and API-accessible public-health datasets, including Lyme surveillance.
* **CDC Tick Surveillance** — county-level tick establishment and pathogen-detection data.
* **CDC WONDER and NNDSS** — finalized and provisional notifiable-disease surveillance data.

### Research, treatment, and care delivery

* **ClinicalTrials.gov** — clinical study registry and results database.
* **NCBI PubMed and PubMed Central** — biomedical citations and open-access articles.
* **NIH RePORTER** — federally funded research projects, investigators, organizations, and publications.
* **CMS Data and Provider Data Catalog** — providers, facilities, utilization, spending, and Medicare/Medicaid data.
* **AHRQ Data Tools** — healthcare use, spending, insurance, access, quality, and community-level health data.
* **openFDA and RxNorm** — drug labels, adverse-event reports, recalls, and standardized drug identities.

### Population, access, and environmental context

* **U.S. Census Bureau / American Community Survey** — population, demographic, insurance, income, disability, and geographic context.
* **CDC/ATSDR Social Vulnerability Index** — community vulnerability measures.
* **NOAA National Centers for Environmental Information** — weather and climate observations.
* **USGS Annual National Land Cover Database** — forests, developed land, impervious surfaces, and land-cover change.
* **EPA EnviroAtlas** — environmental and ecosystem GIS layers.

---

# Detailed catalog and dataset guide

## 1. HealthData.gov

**Name:** HHS Open Data — HealthData.gov

**Read more:** [HealthData.gov](https://healthdata.gov/)

**Developer/API portal:** [HealthData.gov datasets on the Socrata developer portal](https://dev.socrata.com/foundry/healthdata.gov/)

**Information about its API:**
HealthData.gov is largely a Socrata-backed catalog. Tabular datasets commonly expose JSON, CSV, GeoJSON, and other representations through URLs based on a four-character dataset identifier. Socrata’s query language, SoQL, supports server-side selection, filtering, grouping, ordering, and aggregation. Open the individual dataset page and look for its API or export options.

**Description of the organization/catalog:**
This is the umbrella open-data site for the Department of Health and Human Services. It contains HHS datasets, tools, data inventories, dashboards, and links into systems operated by agencies such as CDC, CMS, FDA, NIH, and AHRQ. It is a discovery portal rather than one clean, unified healthcare database. ([HealthData.gov][2])

**How I would use it:**
Use it to discover HHS assets that might not appear when searching only CDC or CMS. Search terms should include:

* Lyme disease
* tickborne disease
* invisible illness
* diagnostic delay
* access to care
* chronic symptoms
* infectious disease surveillance
* healthcare expenditures
* provider shortage
* rural healthcare

---

## 2. Data.gov

**Name:** Data.gov Catalog

**Read more:** [Data.gov](https://data.gov/)

**Developer/API portal:** [Data.gov Catalog API documentation](https://resources.data.gov/catalog-api/)

**Information about its API:**
The current Catalog API is a REST/JSON metadata API with this base URL:

```text
https://api.gsa.gov/technology/datagov/v4/
```

It supports keyword search, organization filters, geographic filters, dataset details, and cursor-based pagination. It requires an `api.data.gov` key in the `X-Api-Key` header, although a low-limit `DEMO_KEY` is available for exploration. A standard personal key currently allows 1,000 requests per hour. Importantly, the API searches **metadata**. It normally tells you where a dataset is located; it does not necessarily return the dataset’s rows. ([resources.data.gov][3])

**Description of the organization/catalog:**
Data.gov, operated through GSA, aggregates dataset metadata from federal, state, local, county, tribal, university, and nonprofit publishers. It is the broadest place to discover American government data, but results can be noisy and sometimes point to old or superseded resources. ([resources.data.gov][4])

**How I would use it:**
Use Data.gov as your automated dataset-search layer. Your script can query hundreds of terms, save the matching metadata, normalize the publisher and URL, and then rank results for deeper investigation.

---

## 3. CDC Lyme disease surveillance datasets

**Name:** CDC Lyme Disease Public-Use Aggregated Data

**Read more and access the datasets:**

* [1992–2007 aggregated data](https://data.cdc.gov/National-Center-for-Emerging-and-Zoonotic-Infectio/Lyme-disease-public-use-aggregated-data-with-geogr/84rx-ksgd)
* [2008–2021 aggregated data](https://data.cdc.gov/National-Center-for-Emerging-and-Zoonotic-Infectio/Lyme-disease-public-use-aggregated-data-with-geogr/qtbi-xd4i)
* [2022–2023 aggregated data](https://data.cdc.gov/National-Center-for-Emerging-and-Zoonotic-Infectio/Lyme-disease-public-use-aggregated-data-with-geogr/x5j9-wybp)
* [CDC Lyme Surveillance and Data overview](https://www.cdc.gov/lyme/data-research/facts-stats/index.html)

**Developer/API portals:**

* [1992–2007 API documentation](https://dev.socrata.com/foundry/data.cdc.gov/84rx-ksgd)
* [2008–2021 API documentation](https://dev.socrata.com/foundry/data.cdc.gov/qtbi-xd4i)
* [2022–2023 API documentation](https://dev.socrata.com/foundry/data.cdc.gov/x5j9-wybp)

**Information about its API:**
These are Socrata datasets. A basic JSON request looks like:

```text
https://data.cdc.gov/resource/qtbi-xd4i.json?$limit=100
```

You can use SoQL parameters such as:

```text
$select=
$where=
$group=
$order=
$limit=
$offset=
```

The same datasets can normally be exported as CSV, which may be easier for your initial local exploration.

**Description of the organization/catalog:**
Data.CDC.gov is CDC’s open-data platform. The Lyme datasets contain public-use, aggregated surveillance data rather than individual patient records. They are the most obvious human-disease outcome data for the challenge. ([Data.CDC.gov][5])

**Critical limitations:**
CDC explicitly warns that Lyme surveillance contains underreporting and possible misclassification. Location refers to the patient’s **county of residence**, not necessarily where exposure occurred. National case definitions changed in 1996, 2008, 2011, 2017, and 2022, so a chart that treats the entire time series as perfectly comparable would be misleading. ([CDC][6])

**Best use:**
Use this as an aggregated outcome layer for:

* Geographic and temporal patterns
* Incidence or reporting trends
* Identifying areas for further investigation
* Comparing human cases with tick, climate, land-cover, access, or vulnerability data

Do **not** treat this as training data for diagnosing an individual patient.

---

## 4. CDC Tick Surveillance Data Sets

**Name:** CDC Tick Surveillance Data Sets

**Read more:** [CDC Tick Surveillance Data Sets](https://www.cdc.gov/ticks/data-research/facts-stats/tick-surveillance-data-sets.html)

**Related interactive resources:**

* [Blacklegged Tick Surveillance](https://www.cdc.gov/ticks/data-research/facts-stats/blacklegged-tick-surveillance.html)
* [Tickborne Pathogen Surveillance](https://www.cdc.gov/ticks/data-research/facts-stats/tickborne-pathogen-surveillance-1.html)

**Developer/API portal:**
There is no clearly documented, general-purpose REST API for these specific downloadable datasets. CDC provides data files used to build its maps and dashboards.

**Information about its API:**
Plan to download the source files and load them into your own local database or dataframe. You will likely join them through county identifiers or county/state names. Normalize these to five-digit county FIPS codes immediately.

**Description of the organization/catalog:**
CDC publishes county-level information about established blacklegged and western blacklegged tick populations and whether selected pathogens have been detected in host-seeking ticks. Included pathogens cover *Borrelia burgdorferi*, *Borrelia mayonii*, *Borrelia miyamotoi*, *Babesia microti*, Powassan virus, and others. The data were updated in May 2026 and include records through December 2025. ([CDC][7])

**Critical limitations:**
A county marked “no records” does **not** mean that the pathogen or tick is absent. It may mean nobody sampled, tested, published, or reported observations there. The “present” and “established” statuses are also cumulative, so they are not measurements of current tick density. ([CDC][7])

**Best use:**
This is probably your second-most-important Lyme-specific dataset after human surveillance. It supports:

* Exposure-risk education
* Geographic risk models
* Identification of surveillance gaps
* Comparison of pathogen presence with reported human cases
* Identification of counties where ecological and human signals disagree

That last category may be especially interesting for product discovery.

---

## 5. CDC NNDSS and CDC WONDER

**Name:** National Notifiable Diseases Surveillance System and CDC WONDER

**Read more:**

* [NNDSS overview](https://www.cdc.gov/nndss/about/index.html)
* [NNDSS annual summary in CDC WONDER](https://wonder.cdc.gov/nndss-annual-summary.html)
* [NNDSS weekly data on Data.CDC.gov](https://data.cdc.gov/NNDSS/NNDSS-Weekly-Data/x9gk-5huc)

**Developer/API portal:** [CDC WONDER API documentation](https://wonder.cdc.gov/wonder/help/wonder-api.html)

**Information about its API:**
CDC WONDER has an older HTTP/XML query API rather than a modern JSON-first API. You submit a structured request describing dimensions, measures, and filters and receive XML results. The weekly NNDSS dataset on Data.CDC.gov uses the easier Socrata API.

**Description of the organization/catalog:**
NNDSS collects case-surveillance data from U.S. jurisdictions. It publishes provisional weekly data and finalized annual data. CDC WONDER allows analysis by dimensions such as disease, year, geography, demographics, and reporting period. It is broader than the dedicated Lyme files and lets you compare Lyme with other notifiable conditions. ([CDC][8])

**Best use:**
Use it for:

* Comparing Lyme with other tickborne diseases
* Exploring possible co-occurring public-health patterns
* Looking at differential-diagnosis categories at an aggregate level
* Understanding provisional versus finalized reporting

Remember that surveillance case definitions support consistent public-health counting; CDC explicitly says they are not clinical diagnostic criteria for individual patients. ([CDC Surveillance Case Definitions][9])

---

## 6. ClinicalTrials.gov

**Name:** ClinicalTrials.gov

**Read more:** [ClinicalTrials.gov](https://clinicaltrials.gov/)

**Developer/API portal:** [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api)

**Information about its API:**
The current API is defined using an OpenAPI 3.0 specification and returns structured JSON. It supports study searches, individual study retrieval, field selection, pagination, and access to registration and results information. Bulk downloads are also available in the current JSON format. ([ClinicalTrials.gov][10])

**Description of the organization/catalog:**
ClinicalTrials.gov is the federal registry and results database for clinical studies. Records may include study design, conditions, interventions, eligibility criteria, outcomes, status, locations, sponsors, and reported results.

**Best use:**
Search for:

* Lyme disease
* post-treatment Lyme disease syndrome
* persistent symptoms
* tickborne disease
* Borrelia
* diagnostic testing
* neuroborreliosis
* Lyme arthritis
* Lyme carditis

This is a registry of studies, not an open patient-level clinical dataset. Its biggest product value may be helping patients or clinicians navigate relevant evidence and recruiting studies.

---

## 7. PubMed and PubMed Central

**Name:** NCBI PubMed and PubMed Central

**Read more:**

* [PubMed](https://pubmed.ncbi.nlm.nih.gov/)
* [PubMed Central](https://pmc.ncbi.nlm.nih.gov/)
* [MeSH medical vocabulary](https://www.ncbi.nlm.nih.gov/mesh/)

**Developer/API portal:** [NCBI APIs](https://www.ncbi.nlm.nih.gov/home/develop/api/)

**Detailed API guide:** [NCBI E-utilities documentation](https://www.ncbi.nlm.nih.gov/books/NBK25501/)

**Information about its API:**
The Entrez E-utilities API supports searching, linking, summarizing, and retrieving records from PubMed, PMC, Gene, Nucleotide, Protein, and other NCBI databases. Common operations include `esearch`, `esummary`, `efetch`, and `elink`. Large-scale PubMed data are also available through bulk downloads. ([NCBI][11])

**Description of the organization/catalog:**
PubMed contains biomedical citations and abstracts, while PMC contains full-text articles available through its archive. MeSH provides a controlled biomedical vocabulary that can improve your search expansion and terminology normalization. PubMed currently contains more than 40 million citations. ([PubMed][12])

**Best use:**
This is likely the foundation of any evidence-oriented AI feature, including:

* Evidence retrieval
* Claim-to-source citations
* Research summarization
* Identification of conflicting findings
* Extraction of symptoms, interventions, outcomes, and populations
* Building a Lyme-specific terminology and synonym graph

Do not blindly embed every search result. Capture publication type, date, study design, sample size, population, and retraction/correction status where available.

---

## 8. NIH RePORTER

**Name:** NIH Research Portfolio Online Reporting Tools — RePORTER

**Read more:** [NIH RePORTER](https://reporter.nih.gov/)

**Developer/API portal:** [NIH RePORTER API](https://api.reporter.nih.gov/)

**Information about its API:**
The RePORTER v2 API accepts and returns JSON. It supports searches over projects, fiscal years, text terms, organizations, investigators, project numbers, and other attributes. Results can include project abstracts, awards, principal investigators, organizations, publications, and related project information. The documented project-search endpoint allows up to 500 results per request and recommends restrained request rates.

**Description of the organization/catalog:**
RePORTER describes NIH-funded and selected other federally funded research. It tells you what work is funded, who is performing it, at which institutions, and what publications or patents may be associated with the project.

**Best use:**
This can uncover:

* Active Lyme research not obvious from published papers alone
* Leading investigators and institutions
* Recently completed studies
* Research gaps
* Potential subject-matter experts or interview candidates
* Connections between grants, publications, and clinical trials

It should not be interpreted as evidence that a funded hypothesis has been validated.

---

## 9. CMS Data and Provider Data Catalog

**Name:** Centers for Medicare & Medicaid Services Data

**Read more:**

* [CMS Data](https://data.cms.gov/)
* [CMS Provider Data Catalog](https://data.cms.gov/provider-data/)

**Developer/API portals:**

* [CMS dataset API documentation](https://data.cms.gov/api-docs)
* [Provider Data Catalog API documentation](https://data.cms.gov/provider-data/docs)

**Information about its API:**
Many CMS datasets have their own endpoint and schema. The CMS workflow is to locate a dataset, open its overview page, and select **Access API**. The Provider Data Catalog separately exposes endpoints for schemas, datasets, and dataset items. ([data.cms.gov][13])

**Description of the organization/catalog:**
CMS publishes provider, facility, utilization, quality, payment, geographic, Medicare, and Medicaid-related datasets. Provider Data supports the information behind Medicare Care Compare and related provider-search experiences.

**Best use:**
Potential uses include:

* Finding provider and facility locations
* Measuring geographic access to care
* Identifying specialist deserts
* Estimating travel burden
* Studying selected utilization or expenditure patterns
* Adding provider-directory information to a navigation product

**Critical limitation:**
Most open CMS data are aggregated, provider-level, or facility-level. You will not get an open patient-level longitudinal claims history for individual Lyme patients. Medicare populations also differ from the overall U.S. Lyme population.

---

## 10. AHRQ Data Tools, MEPS, and Community-Level Health

**Name:** Agency for Healthcare Research and Quality Data Tools

**Read more:**

* [AHRQ Data Tools](https://datatools.ahrq.gov/)
* [MEPS public-use files](https://meps.ahrq.gov/mepsweb/data_stats/download_data_files.jsp)
* [Community-Level Health Database](https://www.ahrq.gov/data/innovations/clh-data.html)

**Developer/API portal:**
AHRQ does not provide one consistent API across all these products. Many assets are query tools, downloadable public-use files, codebooks, CSVs, or statistical files.

**Information about its API:**
Expect a file-oriented workflow. Download datasets and codebooks, then process them locally. HCUP tools provide aggregate query experiences, while many underlying HCUP datasets have licensing, purchasing, or data-use requirements and should not automatically be classified as fully open.

**Description of the organization/catalog:**
MEPS covers healthcare utilization, expenditures, insurance, access, quality, treated conditions, and prescribed drugs for the U.S. civilian noninstitutionalized population. The Community-Level Health Database provides linkable small-area variables covering demographics, economics, education, physical infrastructure, providers, and health conditions at county, ZIP, census-tract, and block-group levels. ([datatools.ahrq.gov][14])

**Best use:**
Use AHRQ for:

* Cost-of-illness framing
* Healthcare access and affordability
* Utilization and expenditure methodology
* Community-level contextual variables
* Understanding what can and cannot be inferred from national surveys

Lyme may have too few observations in a national sample such as MEPS for reliable disease-specific estimates. Check unweighted counts and statistical precision before making claims.

---

## 11. Census Bureau American Community Survey

**Name:** American Community Survey

**Read more:** [Explore Census data](https://data.census.gov/)

**Developer/API portals:**

* [Census developers portal](https://www.census.gov/data/developers.html)
* [ACS data via API](https://www.census.gov/programs-surveys/acs/data/data-via-api.html)
* [ACS five-year API datasets](https://www.census.gov/data/developers/data-sets/acs-5year.html)

**Information about its API:**
The Census Data API returns JSON and supports variables, geographic predicates, and dataset/year selection. As of 2026, all Census Data API queries require an API key. The five-year ACS is usually the best choice when you need consistent county, tract, or small-area coverage. ([Census.gov][15])

**Description of the organization/catalog:**
The ACS provides population and community estimates such as age, income, poverty, insurance status, disability, education, employment, household characteristics, internet access, vehicles, and migration.

**Best use:**
Use ACS data for:

* Population denominators
* Rural and urban context
* Insurance and socioeconomic context
* Age distributions
* Internet and transportation access
* Estimating whether a digital intervention may worsen access disparities

Normalize your joins carefully: county FIPS, census tract, ZIP Code Tabulation Area, and ordinary postal ZIP code are not interchangeable.

---

## 12. CDC/ATSDR Social Vulnerability Index

**Name:** CDC/ATSDR Social Vulnerability Index

**Read more:** [Social Vulnerability Index](https://www.atsdr.cdc.gov/place-health/php/svi/index.html)

**Developer/API portal:**
The primary distribution mechanism is downloadable tabular and GIS data rather than a dedicated developer API.

**Information about its API:**
Download the CSV or geospatial files and join them to county or census-tract geography. Confirm that the SVI year and geographic boundaries align with the period of your other data.

**Description of the organization/catalog:**
SVI is a place-based measure designed to help identify communities that may experience greater difficulty preparing for, responding to, or recovering from hazardous events and public-health stresses.

**Best use:**
Use it to test whether reported cases, provider access, diagnostic resources, or educational coverage differ systematically across community vulnerability levels. It is an area-level index, not a description of every person living in the area.

---

## 13. NOAA climate and weather data

**Name:** NOAA National Centers for Environmental Information

**Read more:** [NCEI Data Access](https://www.ncei.noaa.gov/access)

**Developer/API portal:** [Climate Data Online web services](https://www.ncei.noaa.gov/cdo-web/webservices/v2)

**Information about its API:**
Climate Data Online provides REST-style services for weather stations, datasets, locations, data categories, and observations. An access token is required. The documented limit is five requests per second and 10,000 requests per day. NCEI also provides newer data-access, search, management, ordering, and GIS APIs. ([NCEI][16])

**Description of the organization/catalog:**
NCEI maintains large collections of historical weather and climate observations, including temperature, precipitation, snow, humidity-related measurements, wind, and station metadata.

**Best use:**
Potential Lyme applications include:

* Seasonal exposure context
* Temperature and precipitation patterns
* Comparing climate conditions with tick-establishment changes
* Identifying geographic or temporal anomalies

Climate correlation should not be presented as proof that climate caused a particular disease trend.

---

## 14. USGS Annual National Land Cover Database

**Name:** Annual National Land Cover Database

**Read more:** [Annual NLCD](https://www.usgs.gov/centers/eros/science/annual-national-land-cover-database)

**Data access:** [Annual NLCD data access](https://www.usgs.gov/centers/eros/science/annual-nlcd-data-access)

**Developer/API portal:**
This is primarily a geospatial raster-data product rather than a simple JSON business API. Data are available through USGS download systems, cloud storage, ScienceBase, mapping tools, and geospatial services.

**Information about its API:**
Plan to work with GeoTIFF or other raster products using tools such as Rasterio, GDAL, GeoPandas, or a cloud geospatial platform. You can calculate county-level features from the raster and then join those results to CDC data.

**Description of the organization/catalog:**
Annual NLCD provides annual land-cover and surface-change products at 30-meter resolution. Products include land cover, land-cover change, confidence, fractional impervious surface, impervious descriptors, and spectral change. ([USGS][17])

**Best use:**
Useful derived features might include:

* Percentage of forested land
* Developed/forest boundary density
* Impervious-surface percentage
* Land-cover change over time
* Fragmentation or habitat-edge measurements

This is valuable for ecological risk research, but it is probably too heavy for your first data-ingestion experiment.

---

## 15. EPA EnviroAtlas

**Name:** EPA EnviroAtlas

**Read more:** [EnviroAtlas](https://www.epa.gov/enviroatlas)

**Developer/API portal:** [EnviroAtlas Web Services](https://www.epa.gov/enviroatlas/enviroatlas-web-services)

**Interactive exploration:** [EnviroAtlas Interactive Map](https://www.epa.gov/enviroatlas/enviroatlas-interactive-map)

**Information about its API:**
EnviroAtlas publishes layers through Esri ArcGIS Server and Open Geospatial Consortium services, including WMS and WFS. Some features can be queried or exported as GeoJSON, shapefiles, GeoTIFF, CSV, or geodatabase files. ([US EPA][18])

**Description of the organization/catalog:**
EnviroAtlas provides hundreds of environmental and ecosystem-service maps involving land use, vegetation, water, climate, human health, transportation, recreation, and community conditions. Its interactive map currently provides access to more than 500 maps and tools. ([US EPA][19])

**Best use:**
Use it when you need an environmental feature that Census, NOAA, and USGS do not already provide. Do not ingest hundreds of layers merely because they exist. Select them after you have a defensible hypothesis.

---

## 16. openFDA and RxNorm

**Name:** openFDA and NLM RxNorm

**Read more:**

* [openFDA](https://open.fda.gov/)
* [RxNav and RxNorm](https://lhncbc.nlm.nih.gov/RxNav/)

**Developer/API portals:**

* [openFDA APIs](https://open.fda.gov/apis/)
* [RxNorm API documentation](https://lhncbc.nlm.nih.gov/RxNav/APIs/RxNormAPIs.html)

**Information about the APIs:**
openFDA exposes JSON APIs for drug labels, adverse-event reports, recalls, NDC information, devices, and other FDA-regulated products. RxNorm provides JSON or XML web services for identifying normalized drug concepts, synonyms, ingredients, branded products, and relationships between drug concepts. Most RxNorm data returned by the API do not require a separate terminology license. ([Lister Hill Center][20])

**Description of the organizations/catalogs:**
FDA data describes regulated products and reports submitted to FDA. RxNorm, maintained by the National Library of Medicine, provides standardized identifiers for medications.

**Best use:**
These sources are useful for:

* Normalizing medication names across literature and trials
* Looking up official drug labels
* Exploring treatment terminology
* Studying reported safety signals

Adverse-event reports are signal-generating data. They should not be used to calculate incidence or to claim that a drug caused an event without substantially stronger evidence.

---

# The minimum viable dataset stack I recommend

Do not ingest everything above immediately. I would begin with this stack:

1. **Human disease outcome:** CDC Lyme surveillance, 1992–2023.
2. **Ecological signal:** CDC tick establishment and tickborne-pathogen data through 2025.
3. **Population denominator:** ACS five-year population estimates.
4. **Community context:** SVI or AHRQ Community-Level Health.
5. **Care access:** CMS provider and facility locations.
6. **Evidence layer:** PubMed, PMC, and ClinicalTrials.gov.

All six can be connected through a limited number of entities:

```text
Geography: state, county FIPS, tract, ZCTA
Time: year, month, surveillance period
Disease: normalized disease/condition terminology
Pathogen: Borrelia and other tickborne pathogens
Provider: NPI, specialty, facility, location
Evidence: PMID, PMCID, NCT number, grant/project number
Drug: RxCUI, ingredient, branded product
```

A useful architecture is therefore not one giant flat file. It is a small set of related tables or a lightweight knowledge graph.

---

[1]: https://www.hhs.gov/lyme/index.html?utm_source=chatgpt.com "Invisible Illness: Lyme Disease"
[2]: https://healthdata.gov/?utm_source=chatgpt.com "HealthData.gov"
[3]: https://resources.data.gov/catalog-api/ "
  Catalog API | resources.data.gov
"
[4]: https://resources.data.gov/catalog-api/?utm_source=chatgpt.com "Catalog API"
[5]: https://data.cdc.gov/National-Center-for-Emerging-and-Zoonotic-Infectio/Lyme-disease-public-use-aggregated-data-with-geogr/84rx-ksgd "Lyme disease public use aggregated data with geography, 1992-2007 | Data | Centers for Disease Control and Prevention"
[6]: https://www.cdc.gov/lyme/data-research/facts-stats/index.html "Lyme Disease Surveillance and Data | Lyme Disease | CDC"
[7]: https://www.cdc.gov/ticks/data-research/facts-stats/tick-surveillance-data-sets.html?utm_source=chatgpt.com "Tick Surveillance Data Sets"
[8]: https://www.cdc.gov/nndss/about/index.html?utm_source=chatgpt.com "About National Notifiable Diseases Surveillance System"
[9]: https://ndc.services.cdc.gov/?utm_source=chatgpt.com "NNDSS case definitions - CDC"
[10]: https://clinicaltrials.gov/data-api/api?utm_source=chatgpt.com "ClinicalTrials.gov API"
[11]: https://www.ncbi.nlm.nih.gov/home/develop/api/?utm_source=chatgpt.com "APIs - Develop - NCBI - NIH"
[12]: https://pubmed.ncbi.nlm.nih.gov/?author=+Bikramdeep+Singh&utm_source=chatgpt.com "Home Page - PubMed - NIH"
[13]: https://data.cms.gov/api-docs?utm_source=chatgpt.com "API Docs"
[14]: https://datatools.ahrq.gov/?utm_source=chatgpt.com "AHRQ Data Tools – Agency for Healthcare Research and ..."
[15]: https://www.census.gov/library/video/2026/adrm/requesting-a-census-data-api-key.html?utm_source=chatgpt.com "Requesting a Census Data API Key"
[16]: https://www.ncei.noaa.gov/access "Access | National Centers for Environmental Information (NCEI)"
[17]: https://www.usgs.gov/centers/eros/science/annual-national-land-cover-database?utm_source=chatgpt.com "Annual National Land Cover Database"
[18]: https://www.epa.gov/enviroatlas/enviroatlas-web-services?utm_source=chatgpt.com "EnviroAtlas Web Services"
[19]: https://www.epa.gov/enviroatlas/enviroatlas-interactive-map?utm_source=chatgpt.com "EnviroAtlas Interactive Map"
[20]: https://lhncbc.nlm.nih.gov/RxNav/APIs/RxNormAPIs.html?utm_source=chatgpt.com "RxNorm API - APIs"
[21]: https://opportunity.census.gov/product-development/toolkit/?utm_source=chatgpt.com "TOP Product Development Toolkit | The Opportunity Project"
[22]: https://www.designcouncil.org.uk/resources/the-double-diamond/?utm_source=chatgpt.com "The Double Diamond"
[23]: https://www.designkit.org/?utm_source=chatgpt.com "Design Kit"
[24]: https://www.christenseninstitute.org/theory/jobs-to-be-done/?utm_source=chatgpt.com "Jobs to Be Done Theory"
[25]: https://www.producttalk.org/opportunity-solution-trees/?srsltid=AfmBOop8EVcZh6sDwZ7gi8myQ4TjhveBGfpcGYEhk5nzfrHHsXkKElJs&utm_source=chatgpt.com "Opportunity Solution Trees: Visualize Your Discovery to ..."
[26]: https://www.strategyzer.com/library/how-assumptions-mapping-can-focus-your-teams-on-running-experiments-that-matter?utm_source=chatgpt.com "How Assumptions Mapping Can Focus Your Teams On ..."
[27]: https://www.nngroup.com/articles/service-blueprints-definition/?utm_source=chatgpt.com "Service Blueprints: Definition"
