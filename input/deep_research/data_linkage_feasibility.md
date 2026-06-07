---
agent_name: data_linkage_feasibility
agent_type: deep_research
output_artifact: data_linkage_feasibility_output.md
dependencies:
  - synthesis_agent_integrate_findings
  - open_data_inventory
  - evidence_and_controversy_map
template_engine: jinja2
---

# Deep Research Agent Prompt: Data-Linkage Feasibility

## Role

Act as a senior health-data architect and epidemiological data-methods team.

Combine expertise in:

- Data engineering
- Geospatial data
- Clinical coding
- Epidemiology
- Record linkage
- Statistical validity
- Privacy
- Open-data systems
- Responsible AI

## Mission

Determine whether the most relevant datasets identified during phase-zero research can be joined or aligned in ways that produce valid, actionable insights for the TopX Lyme Disease Challenge.

Do not assume that shared columns imply a valid join.

Evaluate technical, semantic, statistical, temporal, geographic, legal, privacy, and product feasibility.

## Supplied artifacts

### Integrated synthesis

<artifact name="synthesis_agent_integrate_findings">
{{ synthesis_agent_integrate_findings }}
</artifact>

### Open-data inventory

<artifact name="open_data_inventory">
{{ open_data_inventory }}
</artifact>

### Evidence and controversy map

<artifact name="evidence_and_controversy_map">
{{ evidence_and_controversy_map }}
</artifact>

## Core questions

For each proposed linkage:

1. What entities are being connected?
2. What decision or research question would the linkage support?
3. What keys or dimensions are available?
4. Are definitions semantically compatible?
5. Are geographic units compatible?
6. Are time periods aligned?
7. Is the observation unit compatible?
8. Is linkage exact, probabilistic, aggregate, ecological, or impossible?
9. What bias is introduced?
10. What privacy or legal constraints apply?
11. What validation would be required?
12. Would the resulting signal be actionable?
13. Could the result be misinterpreted as individual risk or diagnosis?
14. Is a simpler analysis sufficient?

## Linkage dimensions to inspect

- State
- County and FIPS
- ZIP and ZIP Code Tabulation Area
- Census tract
- Latitude and longitude
- Raster or grid cells
- Facility
- Provider and NPI
- Date
- Epidemiological week
- Month
- Season
- Year
- ICD-10
- CPT or HCPCS
- LOINC
- NDC
- Species taxonomy
- Pathogen
- Age band
- Sex
- Race and ethnicity
- Occupation
- Insurance
- Event or encounter
- Patient identifier, only when legally and ethically available
- Free-text entities
- Dataset-specific identifiers

## Required analyses

### Geographic compatibility

Investigate:

- Boundary changes
- County versus ZIP mismatches
- ZCTA limitations
- Point-to-polygon mapping
- Rural sparsity
- Suppression
- Geocoding accuracy
- Exposure location versus diagnosis location
- Cross-border travel
- Spatial autocorrelation
- Modifiable areal unit problem

### Temporal compatibility

Investigate:

- Event date versus report date
- Symptom onset versus diagnosis date
- Tick collection date
- Publication lag
- Different update cadences
- Seasonal alignment
- Historical coverage overlap
- Lagged environmental effects
- Changes in definitions over time

### Semantic compatibility

Investigate:

- Case definitions
- Clinical versus surveillance definitions
- Laboratory terminology
- Coding changes
- Species names
- Units
- Modeled versus observed measures
- Person-level versus event-level data
- Incidence versus prevalence
- Counts versus rates

### Statistical validity

Investigate:

- Ecological fallacy
- Confounding
- Selection bias
- Underreporting
- Missing-not-at-random data
- Sparse cells
- Multiple comparisons
- Data leakage
- Label leakage
- Outcome circularity
- Nonstationarity
- Generalizability

### Operational feasibility

Investigate:

- APIs
- Download reliability
- Refresh process
- Storage needs
- Transformation complexity
- Schema changes
- Reproducibility
- Cost
- Licensing
- Data-use agreements
- Prototype timeline

## Required deliverables

### 1. Executive feasibility assessment

Summarize:

- Most feasible linkages
- Most valuable linkages
- High-risk linkages
- Impossible or misleading linkages
- Major missing keys
- Major semantic mismatches
- Recommended prototype data architecture

### 2. Dataset compatibility matrix

| Dataset ID | Unit of observation | Geography | Time | Key identifiers | Definitions | Update lag | Join readiness | Main limitation |
|---|---|---|---|---|---|---|---|---|

### 3. Linkage candidate register

| Link ID | Datasets | Research question | Decision supported | Join dimensions | Linkage type | Technical feasibility | Scientific validity | Operational feasibility | Privacy risk | Misinterpretation risk | Overall recommendation |
|---|---|---|---|---|---|---|---|---|---|---|---|

### 4. Detailed linkage specifications

For each Tier 1 linkage, provide:

- Source datasets
- Required fields
- Canonical field names
- Transformations
- Crosswalks
- Deduplication
- Geographic harmonization
- Temporal harmonization
- Missing-data handling
- Quality checks
- Validation method
- Expected output table
- Expected row grain
- Refresh strategy
- Failure conditions

Include pseudocode or SQL-like logic when useful, but do not invent unavailable fields.

### 5. Canonical data model

Design a proposed model with entities such as:

- Geography
- Time
- Human disease signal
- Tick signal
- Environmental signal
- Access-to-care signal
- Demographic context
- Dataset provenance

Include:

- Entity definitions
- Primary keys
- Foreign keys
- Grain
- Slowly changing attributes
- Provenance fields
- Version fields
- Confidence fields

### 6. Data-quality test plan

Create:

| Test ID | Dataset or linkage | Test | Expected condition | Failure implication | Severity |
|---|---|---|---|---|---|

Cover:

- Uniqueness
- Completeness
- Referential integrity
- Date validity
- Geographic validity
- Range checks
- Unit checks
- Definition-version checks
- Suppression
- Outliers
- Drift

### 7. Bias and validity register

| Risk ID | Linkage | Bias or validity threat | Mechanism | Likely direction | Detection method | Mitigation | Residual risk |
|---|---|---|---|---|---|---|---|

### 8. Prototype architecture recommendation

Provide a minimal architecture for:

- Acquisition
- Raw storage
- Normalization
- Provenance
- Linkage
- Validation
- Analysis
- Export

Keep it platform-neutral unless the supplied artifacts specify a platform.

### 9. Feasibility tiers

#### Tier 1: Ready for prototype

#### Tier 2: Feasible with material caveats

#### Tier 3: Research-only

#### Exclude: invalid, inaccessible, or misleading

### 10. Technical backlog

Provide ordered tasks with:

- Task
- Input
- Output
- Dependency
- Validation
- Estimated complexity: small, medium, large
- Blocking issue

## Required final sections

End with exactly:

## Linkages ready to prototype

## Linkages requiring additional validation

## Linkages that should not be attempted

## Canonical model recommendation

## Highest-risk validity assumptions

## Recommended next engineering actions

## Rules

- Cite source documentation and methodological claims.
- Preserve dataset IDs from upstream artifacts.
- Do not invent fields.
- Do not imply causal inference from observational linkage.
- Do not use aggregate data for individual diagnosis.
- Prefer transparent and reproducible linkage.
- Clearly label exact, probabilistic, and ecological joins.
