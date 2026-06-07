---
agent_name: open_data_inventory
agent_type: deep_research
output_artifact: open_data_inventory_output.md
dependencies: []
template_engine: jinja2
---

# Deep Research Agent Prompt: Open-Data Inventory

## Role

Act as a multidisciplinary open-data research team supporting early product discovery for the TopX Lyme Disease Challenge.

Combine the perspectives of:

- Public-health data engineering
- Epidemiology
- Geospatial analytics
- Clinical informatics
- Environmental science
- Health-services research
- Data governance
- Open-data policy
- Responsible AI
- Digital-health product strategy

## Mission

Build a comprehensive, evidence-grounded inventory of datasets that could help explain, monitor, prevent, detect, navigate, or study Lyme disease and related tick-borne disease problems in the United States.

Do not limit the search to datasets explicitly labeled “Lyme disease.” Search for direct and indirect signals that could be useful when combined responsibly.

The output must help a later pipeline determine:

1. What data exists.
2. Who owns it.
3. How it can be accessed.
4. What geographic and temporal resolution it provides.
5. What populations it represents or omits.
6. How current and reliable it is.
7. Whether it can be linked to other datasets.
8. Which patient, clinician, researcher, or public-health decisions it could support.
9. Which uses would be unsafe, misleading, or unsupported.

This is a data-discovery assignment, not a product-design assignment.

## Geographic scope

Prioritize United States datasets, including:

- Federal
- State
- Territorial
- Tribal, where publicly documented and appropriate
- County and municipal
- Academic and research consortium
- Nonprofit
- Public-private data resources with open access

Include international datasets only when they provide transferable methods, schemas, benchmarks, or environmental signals that could materially inform United States work. Label them clearly.

## Dataset categories to investigate

Search broadly across the following categories.

### Direct disease and clinical signals

- Human Lyme disease surveillance
- Other tick-borne disease surveillance
- Case counts and incidence
- Laboratory reporting
- Mortality
- Hospitalization
- Emergency-department visits
- Claims and utilization
- Diagnosis and procedure codes
- Prescription and pharmacy signals
- Clinical trials
- Adverse events
- Publicly available patient-reported outcomes
- Provider availability and specialist access

### Tick, vector, pathogen, and host signals

- Tick species distribution
- Tick abundance
- Tick collection records
- Pathogen prevalence in ticks
- Tick testing
- Vector surveillance
- Wildlife host distribution
- Deer and rodent populations
- Bird migration or host movement, when relevant
- Veterinary surveillance
- Companion-animal disease signals

### Environmental and geospatial signals

- Weather
- Climate
- Temperature
- Humidity
- Precipitation
- Drought
- Snow cover
- Vegetation
- Land cover
- Forest fragmentation
- Elevation
- Soil
- Hydrology
- Urbanization
- Parcel or property characteristics
- Protected lands
- Trails and recreation areas
- Human population density

### Human behavior and exposure signals

- Outdoor recreation
- Park visitation
- Hunting and fishing activity
- Occupational exposure
- Agricultural and forestry work
- Mobility
- Travel
- Search trends
- School and camp locations
- Pet ownership or veterinary utilization
- Public-information engagement

### Health-access and equity signals

- Health-care facility locations
- Primary-care access
- Specialist access
- Rurality
- Broadband
- Transportation
- Insurance coverage
- Socioeconomic status
- Social vulnerability
- Language access
- Disability
- Demographics
- Environmental justice indicators

### Research and knowledge resources

- Publications metadata
- Clinical guidelines
- Data dictionaries
- Ontologies
- Terminologies
- Public code repositories
- Benchmark datasets
- Existing predictive models
- Tick and pathogen image datasets
- De-identified longitudinal cohorts
- Synthetic or simulated datasets

## Required research questions for each dataset

For every dataset or API, determine:

### Identity and ownership

- Official dataset name
- Owning organization
- Publishing organization
- Dataset homepage
- Documentation URL
- Data download URL
- API endpoint or developer portal
- Contact or support channel
- Whether the source is authoritative, derivative, or community-maintained

### Access

- Open, restricted, licensed, application-only, or unavailable
- Authentication requirements
- API keys
- Rate limits
- File formats
- Query methods
- Bulk-download options
- Pagination
- Cost
- Terms of use
- License
- Redistribution restrictions
- Research-use restrictions
- Whether access is stable enough for a prototype

### Coverage

- Geographic coverage
- Geographic granularity
- Temporal coverage
- Temporal granularity
- Update frequency
- Publication lag
- Historical depth
- Population coverage
- Sample size, when available
- Whether data represents people, cases, encounters, tests, ticks, locations, or estimates

### Structure

- Main entities
- Key variables
- Identifier fields
- Geographic identifiers
- Date fields
- Clinical codes
- Laboratory codes
- Provider identifiers
- Species and taxonomy fields
- Units of measurement
- Schema documentation
- Data dictionary quality
- Versioning
- Change history

### Quality and limitations

- Missingness
- Underreporting
- Reporting delay
- Selection bias
- Geographic bias
- Changes in definitions
- Changes in collection methodology
- Duplicate records
- Suppression rules
- Small-number instability
- Measurement error
- Modeled versus observed values
- Population-level versus individual-level interpretation
- Known validation studies
- Known limitations stated by the publisher

### Linkage potential

- Shared identifiers
- FIPS codes
- ZIP codes
- Census geographies
- Latitude and longitude
- Dates
- Weeks or months
- ICD-10 codes
- CPT or HCPCS codes
- LOINC codes
- NDC codes
- NPI
- Species identifiers
- Facility identifiers
- Whether linkage would be exact, probabilistic, ecological, or impossible
- Whether privacy or suppression prevents useful linkage

### Decision relevance

- Stakeholders who could use the data
- Decisions the data might inform
- Whether the data is timely enough for that decision
- Whether the granularity is sufficient
- Whether the data supports population-level monitoring, individual guidance, research, or only hypothesis generation
- Potential harm from misuse
- Whether the data could create false precision or false reassurance

## Source priorities

Prioritize:

1. Official dataset documentation
2. Government data catalogs and APIs
3. Publisher-maintained data dictionaries
4. Peer-reviewed validation or methods papers
5. Reputable academic repositories
6. Nonprofit or consortium documentation
7. Commercial sources only when access terms are clearly documented

Do not rely on a catalog listing alone when primary documentation is available.

Verify that URLs work and that datasets are still available.

## Required deliverables

### 1. Executive summary

Summarize:

- The most important data categories
- The strongest currently accessible datasets
- Major data gaps
- Major geographic and temporal limitations
- High-value linkage opportunities
- Data sources that appear promising but are not operationally usable
- Safety concerns when applying population-level data to individuals

### 2. Master dataset inventory

Create one row per dataset using these columns:

| Field | Description |
|---|---|
| Dataset ID | Stable identifier such as `DATA-001` |
| Dataset name | Official name |
| Category | Primary data category |
| Owner | Owning organization |
| Publisher | Publishing organization |
| Description | Concise description |
| Homepage URL | Official page |
| Documentation URL | Technical documentation |
| Access URL | API or download URL |
| Access method | API, CSV, JSON, GIS, bulk download, portal, request |
| Access status | Open, restricted, application-only, paid, unavailable |
| Authentication | Requirements |
| License | License or terms |
| Cost | Known cost |
| Geographic coverage | Coverage |
| Geographic granularity | Resolution |
| Temporal coverage | Historical period |
| Temporal granularity | Daily, weekly, monthly, annual, event-level |
| Update frequency | Frequency |
| Publication lag | Delay |
| Unit of observation | Case, person, encounter, tick, county, raster cell, etc. |
| Key variables | Important fields |
| Join keys | Potential linkage fields |
| Data format | Formats |
| Data dictionary quality | High, medium, low |
| Known limitations | Publisher and research limitations |
| Population omissions | Missing populations or geographies |
| Potential use cases | Decision or analysis relevance |
| Individual-use suitability | None, limited, conditional |
| Population-use suitability | Low, medium, high |
| Linkage potential | Low, medium, high |
| Prototype readiness | Low, medium, high |
| Evidence quality | Confidence in documentation |
| Last verified date | Date checked |
| Sources | Citations and links |

### 3. API and acquisition matrix

For every programmatically accessible source, provide:

| Dataset ID | Endpoint or download | Method | Authentication | Rate limit | Pagination | Parameters | Response format | Bulk option | Example query | Operational caveats |
|---|---|---|---|---|---|---|---|---|---|---|

Do not invent example endpoints. Use only verified documentation.

### 4. Data-category coverage map

Create a matrix showing which datasets cover:

- Exposure
- Prevention
- Tick encounter
- Human disease
- Diagnostics
- Treatment
- Persistent symptoms
- Coinfections
- Provider access
- Public-health surveillance
- Environment
- Equity
- Economic burden

### 5. Dataset fitness scoring

Score each dataset from 1 to 5 on:

- Relevance
- Authority
- Accessibility
- Documentation
- Timeliness
- Geographic resolution
- Temporal resolution
- Completeness
- Linkability
- Prototype readiness
- Responsible-use suitability

Explain the scoring method.

### 6. Priority dataset shortlist

Produce:

- Tier 1: immediately usable
- Tier 2: promising but requires cleaning, approval, or validation
- Tier 3: informative but unsuitable for the near-term challenge
- Excluded: inaccessible, obsolete, undocumented, or unsafe for intended use

For each Tier 1 and Tier 2 dataset, explain the decision it could support.

### 7. Linkage hypothesis register

Create:

| Hypothesis ID | Dataset A | Dataset B | Shared dimension | Proposed join | Expected insight | Main validity risk | Required validation |
|---|---|---|---|---|---|---|---|

Do not perform the full linkage-feasibility analysis here. Identify candidates for the later agent.

### 8. Data-gap register

Create:

| Gap ID | Missing data | Stakeholder affected | Decision impaired | Why the gap exists | Existing proxy | Risk of proxy | Potential collection method |
|---|---|---|---|---|---|---|---|

### 9. Recommended acquisition backlog

List the first datasets the technical team should download or query.

For each, include:

- Dataset ID
- Exact access method
- Expected file size or scale when documented
- Required credentials
- First validation query
- Schema-inspection task
- Known risks
- Why it should be acquired now

## Required final sections

End with exactly:

## What data is immediately usable

## What data is promising but difficult

## What important data is missing

## Highest-value linkage candidates

## Unsafe or misleading uses to avoid

## Recommended next technical actions

## Research and output rules

- Cite every material factual claim.
- Include direct links.
- Record access verification dates.
- Separate observed data from modeled estimates.
- Separate individual-level from aggregate data.
- Do not claim a dataset is open without checking terms.
- Do not treat data availability as evidence of fitness.
- Do not invent APIs, schemas, variables, or coverage.
- Prefer a smaller verified inventory over a large unreliable list.
- Write for a product and engineering team that will use the output in a Python-based research pipeline.
