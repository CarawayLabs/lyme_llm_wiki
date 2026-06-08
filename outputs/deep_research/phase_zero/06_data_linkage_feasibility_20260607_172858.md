# Research Workflow Artifact: 5. Data-linkage feasibility

- Artifact ID: `data_linkage_feasibility`
- Provider: `gemini`
- External ID: `v1_ChdXZnNsYXAzS0RLZlJqTWNQOFoyTHdRWRIXV2ZzbGFwM0tES2ZSak1jUDhaMkx3UVk`
- Input file: `C:\codex_programming\lyme_llm_wiki\input\deep_research\data_linkage_feasibility.md`
- Generated at: `2026-06-07T17:28:58`

---

# Data-Linkage Feasibility Assessment: Architecting an Epidemiological and Environmental Intelligence Pipeline for Lyme Disease

## 1. Executive feasibility assessment

The data ecosystem surrounding Lyme disease and tick-borne zoonoses presents a profound architectural challenge characterized by severe geographic fragmentation, asynchronous temporal reporting, and deep semantic misalignment. Adopting a One Health paradigm—which integrates human, animal, and environmental health data—is strictly necessary to generate predictive epidemiological models for vector-borne diseases [cite: 1, 2]. This assessment evaluates the technical, statistical, and operational feasibility of linking disjointed environmental hazard data, vector surveillance, and socioeconomic indicators to generate actionable intelligence for the TopX Lyme Disease Challenge.

The most feasible and operationally valuable linkage opportunity lies in constructing a population-level Ecological Hazard and Vulnerability Index. This architecture relies on deterministic spatial joins using Federal Information Processing Standard (FIPS) codes to unify the Centers for Disease Control and Prevention (CDC) Tickborne Pathogen Surveillance layers [cite: 3] with the CDC/ATSDR Social Vulnerability Index (SVI) [cite: 4] and Health Resources and Services Administration (HRSA) Area Health Resources Files. Furthermore, by deploying high-performance raster-extraction libraries, data engineering pipelines can seamlessly aggregate continuous 30-meter National Land Cover Database (NLCD) forest fragmentation metrics into administrative county polygons [cite: 5, 6]. This establishes a robust, highly predictive baseline of environmental risk and healthcare access disparities without violating patient privacy boundaries or entering the regulatory domain of individual clinical diagnostics.

Conversely, the most scientifically hazardous and methodologically flawed linkages involve attempting to correlate hyper-local environmental exposure data directly with National Notifiable Diseases Surveillance System (NNDSS) human case counts to predict localized, real-time outbreaks. The NNDSS legally mandates the attribution of infectious disease cases to the patient's county of residence, which routinely differs from the county of actual tick exposure due to recreational and occupational travel [cite: 7, 8]. Linking environmental hazard data directly to residence-based clinical data introduces severe spatial displacement bias. Furthermore, the CDC’s mandated suppression of NNDSS data for geographic and demographic strata containing fewer than five cases [cite: 8], combined with a fundamental structural break in the 2022 surveillance case definition [cite: 9, 10], renders granular, longitudinal predictive modeling of clinical incidence highly unstable and operationally misleading. 

Major missing keys across the ecosystem include the precise geographic location of human-tick encounters, requiring the use of behavioral proxies such as hunting and fishing license apportionments [cite: 11, 12], and the absence of national, open-access longitudinal patient-reported outcomes for post-treatment symptom trajectories [cite: 13]. Major semantic mismatches involve the misinterpretation of administrative surveillance data as absolute biological ground truth, particularly regarding regions designated as having "no records" of vector presence, which frequently indicates a lack of public health sampling rather than a true absence of the pathogen [cite: 3]. 

The recommended prototype data architecture is a cloud-native, Extract, Load, and Transform (ELT) pipeline centered on a canonical star schema. This design anchors the disparate temporal cadences and spatial grains of the source systems to standardized, slowly changing dimensions for geography and time, enforcing strict ecological fallacy guardrails before the data reaches the downstream application layer.

## Dimensions of Analytical Integration

To engineer scientifically valid linkages, the data must be rigorously evaluated across geographic, temporal, semantic, and statistical dimensions. Shared field nomenclature does not guarantee analytical compatibility.

### Geographic Compatibility

The tick-borne disease ecosystem spans continuous environmental raster grids, administrative vector polygons, and postal routing networks. Integrating these disparate geographic scales introduces severe methodological risks if not handled with precision tools. 

The National Land Cover Database (NLCD) provides 30-meter resolution pixel data detailing land cover, imperviousness, and forest fragmentation indices [cite: 6, 14]. Linking this continuous environmental data to administrative human health outcomes requires spatial aggregation into county or census tract polygons. Utilizing legacy geoprocessing libraries (such as Python's `rasterstats`) on national-scale 30-meter rasters is computationally prohibitive and inherently inaccurate at the borders. Legacy tools rely on an `all_touched` parameter; setting it to false drops polygons smaller than the pixel size, while setting it to true includes edge pixels that severely bias the mean of small geographic units [cite: 15, 16]. The required architectural standard is the implementation of `exactextract`, an optimized C++ library with Python bindings that operates directly on raster blocks. It calculates the exact fractional coverage of raster cells intersecting a polygon geometry, delivering results up to 100 times faster than vector-based intersections while maintaining absolute boundary precision [cite: 5, 17, 18, 19].

When linking clinical Electronic Health Record (EHR) data—which is frequently aggregated at the ZIP code level to preserve patient privacy—to demographic datasets like the CDC SVI (published at the Census Tract level), deterministic spatial joins fail entirely. ZIP codes are linear mail delivery routes, while Census Tracts are contiguous administrative polygons [cite: 4, 20]. Furthermore, ZIP Code Tabulation Areas (ZCTAs), the Census Bureau's areal approximation of ZIP codes, frequently straddle multiple county and tract boundaries [cite: 4, 21]. To resolve this, architects must execute a probabilistic allocation using the HUD-USPS ZIP Code Crosswalk Files [cite: 22, 23]. The crosswalk provides a `RES_RATIO` (Residential Ratio), indicating the exact proportion of residential delivery addresses from a given ZIP code that fall into intersecting census tracts. Raw clinical counts at the ZIP level must be multiplied by the `RES_RATIO` to apportion the epidemiological burden accurately into the standard FIPS hierarchy [cite: 22, 24, 25].

Furthermore, boundary changes must be accounted for within the spatial hierarchy. The Census Bureau periodically updates FIPS codes and definitions, such as the 2022 adoption of Connecticut's nine planning regions as county-equivalent units, which completely redefined the state's historical eight-county system [cite: 26, 27]. Systems utilizing crosswalks from earlier epochs will fail to map contemporary Connecticut data without localized Geocorr 2022 interpolation weights [cite: 21, 28].

### Temporal Compatibility

Temporal misalignment fundamentally restricts the utility of tick-borne disease data for real-time applications. NNDSS public-use files suffer from a publication lag of 12 to 24 months [cite: 7, 8]. More critically, the `event_date` in surveillance datasets rarely reflects the actual date of tick exposure or the onset of the erythema migrans rash; it predominantly represents the date of the laboratory report or notification to the health department.

Longitudinal analysis of Lyme disease incidence is severely constrained by administrative structural breaks. The Council of State and Territorial Epidemiologists (CSTE) modified the Lyme disease surveillance case definition in 1996, 2008, 2011, 2017, and most substantially in 2022 [cite: 7, 8, 9, 29]. Under the 2022 guidelines, high-incidence jurisdictions (e.g., Connecticut, Maine, New York, Pennsylvania, Wisconsin) are permitted to report cases based exclusively on confirmatory laboratory evidence, completely eliminating the previously mandated clinical investigation requirement [cite: 9, 10, 29]. This administrative shift significantly increased the volume of reported cases, effectively breaking the continuity of the time series [cite: 8, 10, 30]. Any temporal linkage attempting to forecast disease trends must treat pre-2022 and post-2022 data as distinct, non-comparable statistical tranches to avoid falsely predicting an exponential biological outbreak.

Additionally, environmental epochs require lagged integration. NLCD forest data is published in multi-year epochs (e.g., 2019, 2021) [cite: 6, 31]. Ecological linkages must employ a "closest preceding epoch" logic; clinical cases from 2020 should be joined against 2019 environmental metrics, as changes in forest fragmentation require chronological lag to influence reservoir host dynamics, tick proliferation, and subsequent human encounters.

### Semantic Compatibility

Semantic misalignment across datasets requires aggressive preprocessing to prevent predictive models from drawing false conclusions. In the CDC ArboNET Tickborne Pathogen dataset, counties are classified based on the presence of pathogens such as *Borrelia burgdorferi*, *Babesia microti*, and *Anaplasma phagocytophilum* [cite: 3, 32]. A classification of "no records" explicitly indicates a lack of active sampling effort, funding, or reporting capacity within that jurisdiction; it does not confirm the biological absence of the vector or pathogen [cite: 3]. Transcoding "no records" to a mathematical zero within a linkage pipeline will systematically train algorithms to associate under-funded, rural counties with environmental safety, creating a dangerous observation bias [cite: 33].

Similar semantic care must be applied to NNDSS suppression rules. To protect patient privacy and prevent re-identification, the CDC suppresses data cells where the combination of demographic and geographic variables results in fewer than five reported cases, replacing the value with text denoting suppression [cite: 8]. If a data ingestion pipeline improperly casts these suppressed string values to zero, it artificially deflates the disease incidence rates in sparsely populated, highly vulnerable counties, systematically skewing downstream health equity models.

For clinical phenotyping, integrating EHR data to bypass the delays of public health surveillance requires strict adherence to standardized ontologies. Research by the SubLyme Network and others demonstrates that the most accurate computable phenotypes for early Lyme disease rely on combining a Systematized Nomenclature of Medicine Clinical Terms (SNOMED CT) diagnosis code with a relevant antibiotic prescription within a 14-day window, or detecting specific Logical Observation Identifiers Names and Codes (LOINC) for positive Western Blot or dual-EIA serological tests [cite: 34, 35, 36]. Linkages relying on unstructured clinical notes without validated Natural Language Processing (NLP) are highly susceptible to false positives generated by rule-out differential diagnoses.

### Statistical Validity

The paramount threat to statistical validity in this domain is the ecological fallacy: the erroneous inference that population-level aggregates or macro-environmental hazard maps dictate absolute, individual-level clinical risk [cite: 37]. A county demonstrating a high density of infected nymphs (DIN) or severe forest fragmentation does not guarantee infection for an individual residing there, as transmission risk is profoundly mediated by anthropic factors, including time spent in edge habitats, use of permethrin, and prompt tick removal [cite: 38, 39]. 

To bridge the gap between environmental hazard and clinical outcomes, predictive models must incorporate proxies for human behavior. Studies validating the Human-Tick Encounter Probability index demonstrate that behavioral exposure proxies—such as USFWS TRACS hunting license apportionments or National Park Service trail usage data—offer strong statistical correlation with self-reported and verified tick-borne disease incidence [cite: 11, 39, 40, 41]. Standardized exposure formulas, conceptualized as $P_{encounter} = 1 - (1 - p)^n$ (where $p$ is the probability of exposure and $n$ represents the human behavioral factors), are required to modulate raw entomological density metrics into valid epidemiological risk models [cite: 37, 42].

### Operational Feasibility

Operational execution requires navigating varying API capabilities and legal data-use constraints. Datasets hosted on the Socrata platform (e.g., NNDSS, SVI) and ArcGIS REST endpoints (e.g., ArboNET) offer high operational feasibility for automated extraction [cite: 3, 8, 43]. The USGS NLCD raster files are accessible via Google Earth Engine or bulk download, though processing them requires robust cloud-compute provisioning [cite: 6, 44]. Conversely, attempting to integrate highly granular clinical outcome data for indigenous populations via Tribal Epidemiology Centers (TECs) requires negotiating bespoke Data Use Agreements (DUAs) to respect tribal data sovereignty, rendering it operationally infeasible for rapid prototyping despite its immense scientific value [cite: 45, 46].

## 2. Dataset compatibility matrix

The following matrix documents the baseline interoperability parameters of the prioritized open-data inventory, highlighting the essential constraints required for engineering automated ETL operations.

| Dataset ID | Unit of observation | Geography | Time | Key identifiers | Definitions | Update lag | Join readiness | Main limitation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DATA-001 (NNDSS)** | Aggregated case counts | State, County | Annual | FIPS (State, County), Year | CSTE Surveillance Rules | 1–2 years | High | Severe underreporting; measures residence, not exposure site; 2022 definition break [cite: 7, 8, 9]. |
| **DATA-002 (ArboNET)** | Cumulative tick/pathogen presence | County | Cumulative (Annual updates) | FIPS (County) | "Present", "Reported", "Established" | 1 year | High | "No records" reflects sampling bias, not biological absence; cumulative nature masks recent trends [cite: 3]. |
| **DATA-003 (NLCD)** | 30m Pixel | Raster grid | Epochs (2019, 2021) | Lat/Lon, Projection Coords | Anderson Land Cover Classes | 2–3 years | Low (Requires processing) | Massive computational overhead; requires `exactextract` aggregation to yield actionable polygons [cite: 5, 6, 14]. |
| **DATA-004 (SVI)** | Demographic composite | Tract, ZCTA, County | Biennial | FIPS, ZCTA | 16 ACS-derived variables | 2 years | High | Cannot be used for longitudinal comparisons across different census years; tracts shift decennially [cite: 4]. |
| **DATA-005 (TRACS)** | Hunting/Fishing License | State | Annual | State FIPS | Paid apportionments | 1 year | Medium | Hunters cross state boundaries; highly generalized exposure proxy lacking deep-woods specificity [cite: 11, 47]. |
| **DATA-006 (EHR/Claims)** | Clinical Encounter | ZIP / ZCTA | Daily / Encounter | ZIP Code, LOINC, SNOMED | Computable Phenotypes | Varies | Medium | Aggregated to ZIP code; requires probabilistic `RES_RATIO` allocation to join with Tract-level metrics [cite: 22, 25, 34]. |

## 3. Linkage candidate register

The candidate register isolates high-value engineering opportunities that merge disparate ecological, behavioral, and clinical domains into cohesive predictive models, while strictly rejecting linkages that violate statistical validity.

| Link ID | Datasets | Research question | Decision supported | Join dimensions | Linkage type | Technical feasibility | Scientific validity | Operational feasibility | Privacy risk | Misinterpretation risk | Overall recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **LNK-01** | DATA-002 (ArboNET) + DATA-004 (SVI) | Which highly vulnerable communities intersect with emerging tick pathogen hazards? | Targeted public health funding, telemedicine resource allocation. | County FIPS | Exact | High | High (Both are ecological/population metrics) | High | Low | Low (If restricted to population-level decision making) | **Tier 1** (Ready) |
| **LNK-02** | DATA-003 (NLCD) + DATA-002 (ArboNET) | Does high forest fragmentation correlate with increased *B. burgdorferi* presence? | Predictive environmental risk modeling for unsampled counties. | Spatial (Raster to Polygon) | Aggregation / Exact | Medium (Compute intensive) | Medium (Subject to tick sampling bias) | Medium | Low | Moderate (Predicts habitat suitability, not human bites) | **Tier 1** (Ready) |
| **LNK-03** | EHR/Claims (ZIP) + DATA-004 (SVI) | Are delayed Lyme diagnoses more prevalent in highly vulnerable census tracts? | Clinical workflow auditing, equity interventions. | ZIP to Tract | Probabilistic | High | High (With proper weighting via HUD crosswalk) | High | High (Requires HIPAA compliance for raw EHRs) | Low | **Tier 2** (Requires HUD USPS RES_RATIO crosswalk) |
| **LNK-04** | DATA-001 (NNDSS) + DATA-003 (NLCD) | Do highly fragmented counties produce more human Lyme disease cases? | Ecological exposure risk assessment. | County FIPS | Ecological | High | **Low** (Severe spatial mismatch) | High | Low | **Extreme** (Assumes residence = exposure) | **Tier 3** (Do not attempt without behavioral exposure proxies) |
| **LNK-05** | DATA-001 (NNDSS 2019) + NNDSS 2023 | What is the 5-year growth rate of Lyme disease incidence? | Trend forecasting. | County FIPS, Year | Exact | High | **Invalid** | High | Low | High (Due to 2022 case definition break) | **Do Not Attempt** |

## 4. Detailed linkage specifications

### Tier 1.1: Ecological Hazard and Vulnerability Index (LNK-01 & LNK-02)

This specification constructs the foundational environmental risk baseline. By linking fragmented land cover with confirmed tick pathogen presence and social vulnerability indices, it establishes a macro-level hazard score completely isolated from the spatial displacement bias inherent in human clinical surveillance.

*   **Source datasets:** DATA-002 (CDC ArboNET Tickborne Pathogens) [cite: 3], DATA-003 (USGS NLCD 2021) [cite: 6, 31], DATA-004 (CDC/ATSDR SVI 2022) [cite: 4], US Census Cartographic Boundary Files (County polygons).
*   **Required fields:**
    *   `NLCD`: Pixels classified as 41 (Deciduous Forest), 42 (Evergreen Forest), 43 (Mixed Forest), 90 (Woody Wetlands) [cite: 14].
    *   `ArboNET`: `county_fips`, `Pathogen_Borrelia_burgdorferi_ss_Status`, `Pathogen_Babesia_microti_Status`.
    *   `SVI`: `FIPS`, `RPL_THEMES` (Overall Vulnerability Percentile) [cite: 4].
*   **Canonical field names:** `geo_fips_county`, `env_forest_coverage_pct`, `vec_bb_status`, `vec_bm_status`, `soc_svi_percentile`.
*   **Transformations & Geographic Harmonization:**
    1.  Acquire Census County polygons (EPSG:4326) and reproject them to the NLCD native projection (Albers Equal Area Conic) to ensure mathematically accurate area calculations across the curvature of the Earth.
    2.  Instantiate the Python `exactextract` library to execute a raster-to-polygon zonal statistics operation [cite: 17, 48]. Unlike legacy tools, this computes the fractional intersection of every 30-meter pixel along the county boundary, preventing data loss.
    3.  Calculate `env_forest_coverage_pct` by taking the sum of the fractional cell coverages for classes 41, 42, 43, and 90, divided by the total fractional cell coverage of the respective county polygon.
    4.  Extract `RPL_THEMES` from the SVI dataset, explicitly casting the `FIPS` string to match the `geo_fips_county` format to prevent the truncation of leading zeros [cite: 4].
*   **Missing-data handling:** 
    *   If the SVI `RPL_THEMES` value equals `-999`, it must be recoded as `NULL` [cite: 4].
    *   If the ArboNET pathogen status equals "No records", it must be recoded as `NULL`, actively avoiding the assignment of an "Absent" or `0` flag [cite: 3].
*   **Expected output table & Grain:** A denormalized fact table structured at the `County / Year` grain.
*   **Validation method:** Perform an exploratory distribution analysis of `env_forest_coverage_pct` against states with verified high forest density (e.g., Maine, New Hampshire) to confirm the integrity of the projection parameters and the zonal extraction logic.

**Pseudocode Logic:**
```python
import geopandas as gpd
from exactextract import exact_extract
import rasterio
import pandas as pd

# 1. Load Geometries and Raster
counties = gpd.read_file('cb_2021_us_county_500k.shp').to_crs('EPSG:5070')
nlcd_raster = rasterio.open('nlcd_2021_land_cover.tif')

# 2. Extract fractional coverage for forest classes (41, 42, 43, 90)
# 'exact_extract' computes the exact proportion of each pixel inside the polygon
stats = exact_extract(nlcd_raster, counties, ['count'], include_classes=True)

# 3. Calculate forest percentage
counties['env_forest_coverage_pct'] = calculate_forest_ratio(stats, target_classes=[41, 42, 43, 90])

# 4. Join ArboNET and SVI using zero-padded FIPS strings
counties['geo_fips_county'] = counties['STATEFP'] + counties['COUNTYFP']
final_df = counties.merge(arbonet_df, left_on='geo_fips_county', right_on='county_fips', how='left')
final_df = final_df.merge(svi_df, left_on='geo_fips_county', right_on='FIPS', how='left')

# 5. Guardrails: Handle Semantic Nulls
final_df.loc[final_df['vec_bb_status'] == 'No records', 'vec_bb_status'] = None
final_df.loc[final_df['soc_svi_percentile'] == -999.0, 'soc_svi_percentile'] = None
```

### Tier 2: Clinical Data to Socioeconomic Linkage (LNK-03)

This specification addresses the integration of high-resolution, HIPAA-compliant clinical Electronic Health Record (EHR) data, typically aggregated at the ZIP code level, with highly granular SVI demographic data located at the Census Tract level.

*   **Source datasets:** Synthetic/Aggregated EHR outcomes (ZIP code grain), DATA-004 (SVI at Census Tract grain), HUD-USPS ZIP-Tract Crosswalk Files [cite: 4, 22, 25].
*   **Join dimensions:** Probabilistic linkage translating `ZIP` representations into `TRACT` geometries.
*   **Transformations:** 
    1. Join the raw EHR clinical dataset to the HUD-USPS ZIP-Tract crosswalk table on the common `ZIP` field.
    2. Multiply the raw clinical case count by the corresponding `RES_RATIO` (Residential Ratio) to probabilistically apportion cases based on the density of residential delivery addresses falling into each intersecting Census Tract [cite: 20, 22].
    3. Aggregate the apportioned, fractional case counts by `TRACT`.
    4. Join the newly aggregated tract data to the SVI dataset utilizing the standard 11-digit Tract FIPS code [cite: 4].
*   **Quality checks:** Execute an assertion confirming that the total sum of apportioned clinical cases across all tracts exactly equals the original total case count at the ZIP level, permitting minor variances exclusively for float rounding.
*   **Failure conditions:** This linkage logic fundamentally fails if the clinical data provided relies on institutional ZIP codes (e.g., the billing location of the hospital) rather than the residential ZIP code of the patient, as the `RES_RATIO` models residential settlement patterns [cite: 23].

## 5. Canonical data model

To facilitate scalable, reproducible epidemiological intelligence, the underlying data warehouse must be architected using a dimensional star schema. This structural abstraction serves to isolate the volatile, asynchronous reporting cadences of the source datasets from the final analytical queries.

*   **`dim_geography`**: The central geospatial spine for all relational joins.
    *   *Primary Key*: `geo_sk` (Surrogate Key).
    *   *Attributes*: `fips_state`, `fips_county`, `county_name`, `state_name`, `geom` (MultiPolygon geometry object).
    *   *SCD*: Type 2. Strictly tracks decennial census boundary adjustments and administrative reorganizations (e.g., Connecticut's 2022 transition to nine planning regions) to ensure longitudinal spatial accuracy [cite: 26, 27].
*   **`dim_time`**: 
    *   *Primary Key*: `date_sk`.
    *   *Attributes*: `year`, `month`, `epi_week`, `season`.
*   **`dim_case_definition`**:
    *   *Primary Key*: `def_sk`.
    *   *Attributes*: `cste_version` (e.g., 2017, 2022), `reporting_criteria` (e.g., "Clinical + Lab", "Lab Only" for high-incidence jurisdictions) [cite: 9].
*   **`fact_hazard_ecology`**:
    *   *Grain*: County / Year.
    *   *Foreign Keys*: `geo_sk`, `date_sk`.
    *   *Measures*: `pct_forest_cover`, `forest_fragmentation_index`, `bb_present_flag`, `bm_present_flag`.
    *   *Provenance*: Flags explicitly tracking if the surveillance status is "Established", "Reported", or "Null" (retained securely from "No records") [cite: 3].
*   **`fact_surveillance_clinical`**:
    *   *Grain*: County / Month / Demographic Cohort.
    *   *Foreign Keys*: `geo_sk`, `date_sk`, `def_sk`.
    *   *Measures*: `reported_cases`, `imputed_cases`.
    *   *Confidence*: `suppression_flag` (True if the original demographic/geographic cell count was `<5` and systematically recoded to Null by the CDC) [cite: 8].
*   **`fact_vulnerability`**:
    *   *Grain*: Tract or County / Decennial Epoch.
    *   *Foreign Keys*: `geo_sk`, `date_sk`.
    *   *Measures*: `svi_overall_pct`, `svi_socioeconomic_pct`.

## 6. Data-quality test plan

Rigorous, automated data-quality testing must be integrated intrinsically into the ELT pipeline to prevent data leakage and the silent compounding of semantic errors across the architecture.

| Test ID | Dataset or linkage | Test | Expected condition | Failure implication | Severity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DQ-01** | `dim_geography` | Uniqueness & Format | `fips_county` must be exactly 5 characters, zero-padded, and uniquely constrained per active record. | Spatial joins fail or generate Cartesian products, massively inflating epidemiological counts. | Critical |
| **DQ-02** | NNDSS to `fact_surveillance` | Suppression Handling | Fields flagged as "suppressed" must cast cleanly to `NULL`, never to `0` [cite: 8]. | Analytical models will falsely classify rural or highly vulnerable demographic cohorts as possessing "zero risk". | Critical |
| **DQ-03** | ArboNET Pathogens | Semantic Null Check | The text value "No records" must be parsed exclusively as `NULL` [cite: 3]. | Predictive algorithms will inadvertently learn to equate a lack of scientific funding or sampling effort with human biological safety. | High |
| **DQ-04** | HUD-USPS Crosswalk | Referential Integrity | The mathematical sum of `RES_RATIO` for a given `ZIP`, grouped across all corresponding tracts, must equal 1.0 (with a ±0.01 tolerance margin) [cite: 22, 25]. | Probabilistic allocation logic will silently drop or inappropriately duplicate clinical cases during transformation. | High |
| **DQ-05** | NNDSS Time Series | Definition Drift | A structural break routine must actively flag longitudinal queries spanning the 2021/2022 CSTE definition transition [cite: 9]. | Downstream machine learning models will falsely forecast a sudden, massive biological outbreak due to administrative changes. | High |
| **DQ-06** | NLCD ExactExtract | Range Check | `env_forest_coverage_pct` must remain bounded as a float between `0.0` and `1.0`. | Values outside this range indicate a catastrophic breakdown in coordinate reference system (CRS) alignment or raster clipping bounds. | High |

## 7. Bias and validity register

Observational data linkage within spatial epidemiology is inherently susceptible to bias. The following threats to scientific validity must be formally documented and actively mitigated prior to the deployment of any predictive models or public-facing applications.

| Risk ID | Linkage | Bias or validity threat | Mechanism | Likely direction | Detection method | Mitigation | Residual risk |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BVR-01** | NNDSS + NLCD | **Ecological Fallacy** (Spatial Displacement) | NNDSS records the patient's *residence*; NLCD quantifies the physical hazard *environment*. Individuals frequently travel to contract tick-borne diseases. | Urban counties falsely appear highly hazardous; rural/recreational counties falsely appear safe. | Conduct spatial autocorrelation tests; cross-reference residential incidence with NPS park visitation data. | **Do not execute direct correlation.** Integrate behavioral exposure proxies (e.g., TRACS hunting data, geolocated mobile data) as a necessary epidemiological intermediary [cite: 11, 39, 40]. | High |
| **BVR-02** | ArboNET + FIPS | **Observation/Selection Bias** | The designation "No records" frequently signifies that no entomological field teams sampled the county, not that ticks are biologically absent [cite: 3]. | Underestimates environmental hazard in underfunded, highly rural, or socioeconomically vulnerable jurisdictions. | Compare entomological sampling density against AHRF funding metrics or proximity to academic research institutions. | Employ environmental niche modeling (predicting habitat suitability via NLCD attributes) to statistically interpolate vector hazard in unsampled counties [cite: 12, 49]. | Medium |
| **BVR-03** | EHR (ZIP) + SVI | **Modifiable Areal Unit Problem (MAUP)** | Aggregating discrete clinical point data into arbitrary administrative boundaries (ZIPs/Tracts) artificially alters statistical correlations. | Highly variable, dependent entirely on the spatial scale and boundary configurations utilized. | Execute sensitivity analyses comparing outputs across multiple geographic scales (Tract vs. County resolutions). | Mandate the use of probabilistic HUD-USPS crosswalk allocations [cite: 22]; strictly avoid attributing aggregated tract-level social vulnerability to individual patient profiles. | Medium |
| **BVR-04** | NNDSS (Pre/Post '22) | **Instrumentation Bias** | The 2022 CSTE surveillance rules eliminated clinical investigation requirements for high-incidence states, relying purely on laboratory confirmation [cite: 9, 10]. | Artificial, exponential spike in reported cases beginning post-2021. | Time-series decomposition; implementing structural break testing on historical curves. | Architecturally segregate NNDSS data into distinct, non-comparable chronological tranches (e.g., 1992-2007, 2008-2021, and 2022-Present). | Low (If segregated) |

## 8. Prototype architecture recommendation

To systematically orchestrate the complex geoprocessing operations, probabilistic allocations, and null-handling logic detailed above, a scalable, cloud-agnostic ELT (Extract, Load, Transform) architecture must be deployed.

1.  **Acquisition & Raw Storage (Data Lake):**
    *   Programmatically ingest NNDSS CSVs via the CDC Socrata API, ArboNET GeoJSON files via ArcGIS REST endpoints, SVI demographic CSVs, and the HUD-USPS ZIP-Tract Excel crosswalks into a secure, raw object storage zone (e.g., AWS S3, Google Cloud Storage).
    *   Acquire the multi-gigabyte USGS NLCD 2021 raster datasets (GeoTIFF) [cite: 6, 31].
2.  **Geospatial Processing Compute (Harmonization Layer):**
    *   Provision an ephemeral, high-memory compute cluster or a containerized environment (e.g., Docker running Python 3.10).
    *   Execute `geopandas` alongside the `exactextract` library [cite: 5, 17, 18] to perform the computationally heavy raster-to-polygon zonal statistics, extracting highly precise NLCD forest fragmentation metrics into administrative County FIPS polygons. Relying on legacy `rasterstats` is strictly prohibited to ensure bounded memory management and absolute boundary precision [cite: 19].
3.  **Relational Transformation & Modeling (Data Warehouse):**
    *   Load the harmonized geospatial outputs and the raw CSV extracts into an analytical data warehouse designed for columnar processing (e.g., Snowflake, BigQuery, PostgreSQL/PostGIS).
    *   Deploy SQL-based dbt (data build tool) models to execute the probabilistic HUD-USPS ZCTA-to-Tract allocations [cite: 22, 25] and construct the dimensional star schema defined in Section 5.
4.  **Validation & Export (Access Layer):**
    *   Implement automated data-quality frameworks (e.g., dbt tests) directly against the Data-Quality Test Plan (Section 6), specifically auditing for correct null suppression logic and primary key uniqueness.
    *   Expose the canonical fact and dimension tables to data science and epidemiology teams via secure, read-only views or downstream BI dashboards. 
    *   **Crucial Guardrail:** The architecture must enforce application-level policies that strictly prevent the exposure of individual-level diagnostic predictions based on aggregated environmental hazard data.

## 9. Feasibility tiers

### Tier 1: Ready for prototype
The construction of the Ecological Hazard Baseline—achieved by linking USGS forest fragmentation rasters to CDC tick pathogen presence layers via `exactextract` zonal statistics and spatial joins—is highly feasible. It establishes a robust, population-level environmental risk layer. Concurrently, linking the CDC SVI with HRSA AHRF files using standard FIPS codes provides immediate, validated insights into the socioeconomic barriers and healthcare access disparities facing populations within emerging tick-endemic zones.

### Tier 2: Feasible with material caveats
Linking clinical Electronic Health Record (EHR) data to Census Tracts via ZIP codes (EHR + SVI via HUD-USPS) is methodologically sound utilizing the HUD-USPS crosswalk to probabilistically allocate patient data via the `RES_RATIO` [cite: 22, 25]. However, this linkage requires rigorous upstream validation of the underlying EHR data to definitively verify that the ZIP code analyzed represents the patient's true residence, rather than a default billing facility or hospital location.

### Tier 3: Research-only
Attempting to utilize hunting and fishing license sales as a primary behavioral proxy for human-tick encounters (USFWS TRACS + NNDSS) holds conceptual promise but requires deep academic validation. The data is complicated by hunters crossing state boundaries, the exclusion of exempt demographics such as youth and seniors, and the inability to distinguish deep-woods tracking from edge-habitat recreation [cite: 11, 12, 47].

### Exclude: invalid, inaccessible, or misleading
Any direct correlation mapping NNDSS case residence strictly to local NLCD environmental hazard must be excluded. Joining human case data directly to the environmental characteristics of their home county introduces a severe ecological fallacy; disease incidence is often driven by exposure location during recreational travel, rendering direct spatial correlation at the residence level scientifically invalid without a behavioral proxy [cite: 37]. Furthermore, longitudinal NNDSS trend modeling crossing the 2021/2022 threshold must not be attempted. Because the CSTE radically altered the Lyme disease reporting criteria in 2022 to allow laboratory-only reporting in high-incidence states [cite: 9, 10], treating pre-2022 and post-2022 data as a continuous series is statistically invalid and will fabricate artificial outbreak trends.

## 10. Technical backlog

The following operational sequence directs the initial engineering sprint required to instantiate the prototype pipeline.

| Order | Task | Input | Output | Dependency | Validation | Estimated complexity | Blocking Issue |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Ingest NNDSS & SVI** | CDC Socrata API | Raw CSVs in Data Lake | None | Total row counts match source; `<5` suppression values remain intact [cite: 8]. | Small | None |
| 2 | **Process NLCD Raster** | NLCD 2021 GeoTIFF, Census County Shapefiles | `nlcd_fips_metrics.csv` | Task 1 | Verify that `exactextract` fractional sums logically equal 1.0 per polygon [cite: 48]. | Large | Requires high-memory compute instance or an advanced chunking strategy. |
| 3 | **Harmonize ArboNET** | ArcGIS REST GeoJSON | `arbonet_fips_clean.csv` | None | "No records" string literals are successfully and universally cast to `NULL` [cite: 3]. | Small | None |
| 4 | **Deploy HUD Crosswalk** | HUD-USPS ZIP-Tract Excel | `brdg_zip_tract` table | None | The sum of `RES_RATIO` groups exactly to 1.0 by ZIP code [cite: 20, 22]. | Medium | File access requires manual HUD user account registration [cite: 22]. |
| 5 | **Build Canonical Model** | Outputs from Tasks 1-4 | Star Schema (`dim_geography`, `fact_hazard`) | Tasks 1, 2, 3 | All foreign keys (`geo_sk`) resolve successfully without generating orphaned records. | Medium | Resolving FIPS string padding (maintaining 0-prefixes) across disparate federal datasets. |

## Linkages ready to prototype

The Ecological Hazard Baseline (NLCD + ArboNET Pathogens mapped to County FIPS) and the Vulnerability and Healthcare Access Index (CDC SVI + HRSA AHRF mapped to Tract/County FIPS) are ready for immediate prototyping. These deterministic joins rely on robust APIs, well-documented crosswalks, and high-performance geospatial libraries to yield actionable, population-level insights into environmental risk and health equity.

## Linkages requiring additional validation

The probabilistic allocation of clinical EHR data to Census Tracts via ZIP codes utilizing the HUD-USPS crosswalk, alongside the use of behavioral proxies such as USFWS TRACS hunting data, requires extensive validation. While the mathematical logic (e.g., `RES_RATIO` allocation) is sound, the underlying clinical records and behavioral proxies must be audited to ensure they accurately represent human exposure geometries and residential locations.

## Linkages that should not be attempted

Architects must strictly prohibit the direct correlation of NNDSS case residence data to local NLCD environmental hazard metrics due to the severe spatial displacement bias (the ecological fallacy). Additionally, longitudinal NNDSS trend modeling spanning the 2021/2022 reporting threshold must not be attempted, as the 2022 CSTE case definition change severs the statistical continuity of the surveillance data.

## Canonical model recommendation

The data architecture must deploy a dimensional Star Schema. The relational core must be anchored by a slowly changing `dim_geography` (capable of handling decennial boundary shifts, such as Connecticut's 2022 FIPS reconfiguration) and a standard `dim_time` table. Transactional realities must be decoupled into distinct fact tables: `fact_hazard_ecology` for environmental and vector data, `fact_vulnerability` for SVI and healthcare access indicators, and `fact_surveillance_clinical` for epidemiological counts. This structural separation isolates the volatile update cadences of environmental rasters from the lagging, discrete reporting intervals of clinical surveillance.

## Highest-risk validity assumptions

The highest-risk assumption is treating the administrative designation "No Records" in ArboNET datasets as synonymous with absolute biological safety or zero risk; this frequently reflects a lack of entomological funding or sampling effort in rural counties, introducing massive observation bias. Additionally, assuming that NNDSS data captures true incidence ignores profound systemic underreporting, while mathematically imputing CDC-suppressed data (cells with `<5` counts) as zero actively obscures biological risk in highly vulnerable, low-population rural areas.

## Recommended next engineering actions

The engineering team should immediately provision cloud storage and ingest the Tier 1 datasets (SVI, NNDSS aggregated data, and ArboNET GeoJSON) to establish the foundational FIPS-based geographic hierarchy. Concurrently, data engineers must deploy a containerized Python environment utilizing the `geopandas`, `rasterio`, and `exactextract` libraries to execute the computationally intensive raster-to-polygon aggregation of the NLCD 2021 dataset. Finally, strict automated data-quality tests must be established to explicitly verify that text values such as "No records" (ArboNET) and "suppressed" (NNDSS) are reliably cast to `NULL` prior to their insertion into the analytical data warehouse.

**Sources:**
1. [who.int](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFbN-aBtRFhW-J8mTApMYfzKuXPsRqwr6P3b6szZ8775Qwr86RSXQI1UmnR7gJCBXoIES9pfShlal4ocpqDGAr8L8apGyzN6EP968APg3cuc8vbvlacZRAhRjkFOyLBR3KhaXGSX53rVHnKSs4ozxg5Dg==)
2. [nih.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFo04vbl8YMwS_0nS_AfPA5y46C73VQOzHJ9FzCVOsV-5DTuyXS91zcpRqIlZvrAKYX6YydKjR-xVwYqKUZF6vd-u3-TbYfgBWqXhmTV3GbaOLsa0bW2oVyx3-MDTF-0VJcrCHBlNipwg==)
3. [cdc.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFSjDZjoJGQCu7hh5-f6AUrwjshCQgNMKIefZlf6VXqjryq83enoj8QdzYHHWnXKhVDLqNZC56fuz7tPp0BLdkx_Kvvg1fZu9oNaVMEFAogjl1SgcNvvc8sCbNoRHL-DGuhXske9GpuUwAfFTYWRHUqTCMmtvc8XhkyiVZUpXR673gKR1di6b-7RmM=)
4. [cdc.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEtt71JW70n50Ucs0Rf9zobqa_1epvtAAy0JtLXmrrwBNyHkxOvAtOiGHqMBiqSJshDIdH6q5gnyLyBNCxFqn4eLm6hjgc-mewEvd_FTm9KENKYhXj6rb0ICH-nQaq_ggKZbh1YriYc62cEoFYK3t1zxfqY0695PA==)
5. [readthedocs.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGXswjAhDZD4je4hn63wJDE9IyUzZF8ZaL3CX82IwmEo7P99kCzXrdjP1ZPUrwybEjnjGLpd80y9tZ975ke7HMgv_Z027kHN7vGkNKRfmDljY19CnjGmq2ufwz7JkMGu0Fruu-vXf_ts5dTvkJ__Mt57bBHOQ8Hgh-bNl_FXOT3FQgj)
6. [usgs.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGMgG98ZD3x-8QKX2V5DtNHRSv2naon8yH276q_W9UByMuAByqibOW1xnBFZN0qptQ1H0uHmNpYpl1J_6gNOQsEh85rd83LAd3Cgo5KtmMNzToStwpLY_pnSRwR-FogWCYtcrK7fuZN1IgXLFRCHTQ3k0Rptu97Jqlm9Nvu)
7. [cdc.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHbvNJIxp0gMGsc_MVFzQMDp8NBxVrRmogMtBSG2TudC5kXlSM1UCPoMab6vTAGfODuQOY6PoSOJ85mMfVNzUQ0w0JDnOr0NLxsKgq4c5zRB8vyYIP0Wip4Oa2N8dIAMss2tzyj7Q8A3S7JvTyFp4f5Vdbq)
8. [cdc.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHcNYFqx4ZX2TKFASs8qUJkGAAmhVTarXUyF9M-0SGvmT6Ph8WQBoMgz8dmqAivt-7lO4lX5G8bbunoK7-dRY_La8bBOyiNl4C0tcWlB8xxr-QKVmscL-pix-lGFt9cnyjumvvdZMzy2gGQ29nf-rnlEcemPwQYC1Bc1khvuy1JLEydzR4kqYVYX9aZpyz4lclcwySz83fx_kmpaMjl4TZPklDOrcFnz3tNBeagPSOonxx618GvQ0rZFqMi)
9. [Link](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEWjKCPpnhq7eeYEM_eFxyY6Pf7C6qGPTZ7OmOglM0ghSin4DmtS0vJCFreFKfJ6RqemRANaGmYhEjdu74nnC7mJWO_SCocnI1Zn62fV_2N0x3Cn0lWWvF_ynT4FSZS95l_G6Qa-ARyz1cFg1gwYUV_t9woVYNz)
10. [datalumos.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEC3hLKwf0FeXDQv-rno-NCRDM0OSTCb0IW0o5RFnm0_M91E_29I176_WO4iYN3ObiT-tCMMMakwT1VBcaX1z7t89zaB6kcBV7Fw4IAr06SFUDT_pzE8jh6xwq_Q9sDka5Ci9SFhM5P1wC9jCgRi7gyljqEli9bO94=)
11. [fws.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEiMz4rfUEnrlXrM2sTpx_HIlpQIp0vEP8hT0LAFb13HLGDnPqEcB-_wkzsOyMlZfG3VEzRvp3-FVcRgvTy4jI_KuZIbGp8dpsq44kMF72xgtpzeoxno2Nf8osqP8Mw5_P8KETtj1J0yf8qtq9B4fjmVjgkHB91tZKi)
12. [plos.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFlj8TLHL6ZXij5y1RB1PP1jr9yA65an4qlhGserUBq-DdcyneAxZRIvrh4nd8SpgUSdu0y7h2Rr0iyBAiPQSqDTKJNfm2hbT4lBmYGuwfn9Wp1_SMf59lGb2QqmzCdExTcflLktyqgaQTmCqi1Jptx61_2GIm88XfPYMDFGGXZnA==)
13. [lymedisease.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHsUFoxLNxxKMFnsiGPAlwujR-dx029wb6iEdLPWUK8BoTpu-OysizDiep-eoao7voicXXA2zl6KECXCvCeMXht30Miyog5okpl5JdaeStV7sam6QKZZUopG9YPtQNeHcC7E3KGg2nnu2MRSgPG0mXVnpP9bXctqSoL)
14. [mrlc.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHkWch83WGZeZjUyZCDtIT0mLEJXPRJ3tEeyUs2ZnHsvMg0VU5ECJtl9Cn5m0ONCnnmBQVehWoM0htOcTWU7mUucUg21dmJxfBGdGxTMVxmPCruZMB0uOP6kNEShC8SrtfmNfMlC0DbnsnSuuMRFSIbOXci9RvqHHLICMsUDe4Vgg7gRLJ7HkGu9SVni6hAvbET)
15. [pypi.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEj7lk-TPLrNsW_BEYhNC_6Xk4z0oWvhsq_8SNfsENFvcwCzdLjH9DOyZTCukvIZ8R3t832vxaPORqdMgKDV3jlbTvRaQtB13h8NA_IU8peAj8QdwTFPLIJSUvAhGsw56t1)
16. [stackexchange.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGE173fHtcBDF0epzygZ-Q2xDRVPlvlIQ5mEA9_liOdTxm1a6Rb5Hc0r--GsoyxpTFKIiHOWc--izy3yjdTi44xfkawnBWANhFs1iNKc6Hq0nc2-VLohPkQHf7MvppRL9UTVPJwwscIFuzkJA9Y4njCvvnoArSjDb5i4ZPllIT9LdfWlp2UzXrwWppoHEBwMijwVUOJoikEm1FbslzVAExnDZB1wArJqP7o)
17. [osgeo.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF4bHiBKSwkreQr8sqMBCY8a7srhbkIeyODf1JBFbokbbAaCEEgaAtfoGo40C-69fP-NsfnPpjJQlTbhgMwNUoAQ9g6RJofxAYCxe8dKyPfrNQzulTIdjrb2qCY_Lq_a8eppX1nqo3drD8=)
18. [github.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGvoo_a8BcMYvYaWh20jNSbOBy4h893HB6GO_uCKszgbejcadlVmsNimWj2RRHtZr7kxnGcuoh020tivd1oLS8mL6miFC1uuEabWtXS0eYUmnNKEqn8CX1ty48C2y0Bwal9w-Z-GGJ1QXfrsN7MGib2YXIDBWDdrnwNOw==)
19. [stackoverflow.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHaE2NBpoAlf9ddSbbLfGESjJyvofRs_5pcj2ejg_HY1KlFbq4UCPn5Fd7iyIrC0W0KGSV5G6lumq8r4lNzRNpfBRE3SiLONpxTmKdHXwoUQq1s8uDspIRN0MbE0UHt3tqbyQ_Cr7gmGs_GItVRC2hD8cuWCnDLOg8Anqjdle21nQNxvGNHTkldECUtZKx7j3fpUY8hCRgTSqf1yoOh3LIfJYqcan_9_04gInijt_ufqaPv8Q==)
20. [missouri.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH2VTcyWFgDhGW7x6vgFBNE9S3RmiY0hXT72T5sDnuw_yu441rutXvzD_nNrX0VR-ZXOpEGhbc0jOL08OQ2HJpeI1Wzs4NQCo5vNwNJggo0laCNG4re42SZfki-bbdS-FI9JymNxpVVGnA=)
21. [atcoordinates.info](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH47WVCU2qZC2ahZMnKG90L8ji8KgO_zJEXZRDQi_BMpHd8ReOvQNglAuEwU0FOUSv07yiDjjNdL5Zg2_qnA-LmquClSmXQRhQQY1FqUffwei47ailRVJu9EA==)
22. [huduser.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH_GPEVTmdL8frhI2kthWrk9jE19SaJ6ZL6tYJ3lQAW4-BnQSJfZAwoYvFBx6hoS1QcTKtfL60lMZuAOG4t7Rv-bcx0bEI_TGvMR_XkIjA_ExoyM7la4QoiAmJkymeCyfX0v80moFoKFIQoHFmGgCXPtA==)
23. [datalumos.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHN8c5IEJhDuEu12-Xc_K_uXz6YysheJ-gCzGN66VobPto9dI7MyU9AeI17F15wEWSY0JC1TpYfkw1rw3awm6n8SywjoJts30hBINouUchEUGzLMWLmxE3yo1x4oqksQTJbi8-iKUK2xAeizLbQA80TUa4-LMYJeE0=)
24. [widcenter.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF5Hjs-m9r_g_t9teznoxV7jAc6-5P-IhDoYsHmqs0bmVVXXGbvtytDkX4_CkW2zUqi3x3VQqmDsytO4-Q3fnlw2BQlfHSWVMowv1Yi5CXLyD-60iC0SiWIvE66f_pZSu-8aOOaWpT59n7Hb_azmJZXrsLrJLZqLs_ROuI=)
25. [redivis.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE7JDgt_uVF632n-u1rgl2Z0L-wkT7JoA9yNwgWDaACOeql5qkiB6Kl-gx9Z8gWfycQWVgeS1t1ZXQbSZUfTY-VgFSJEHDiBjtZbYB5PbbAtabYuksAnFVVrYIlJoornHp_)
26. [nhgis.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEyPj2Nf34CPqk0HP1LMTSoadNj2ibrdqEBZANwxvDLzwTCeB-u9jiHbvlmNp16wCNhYrwnptX6GU31Rz_XMRgKKLVn3PhOp6p5kyoNksx0SE99QMoSa6wZglzRGLUMnirp)
27. [nber.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHUCNkVXoGMmKwVOGLnUgRzBPaStHoz2jh_I7Di6jGC_fAE703vgOVF5acUSptB34TBvwvNwSW2AR6Doud4q_4XxGNvBPn5VvUdcBj2TWIF850TUyb5p2PHh8KXHPG4PqwP-Rd-knwbmENJ_rdCVZA8WXJvMr7xh0WnhUIu8fTzQCzzBXVFOK8igC5QoGyR6jsS4IfKckAJYKwkwJsN_AgTrqw=)
28. [missouri.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGfhTJqcxsm7HK37EUxug5ICo4Rqck6SxgTOzuiAp5gWDEXh6hy-hnTDBoS6_eEmQXfdqCEIXqNKLNuaZtL2KcctYrGpTtIMK83JD4gTgabg0Dvh3IhwKBprkUzsD7YYHrLzw==)
29. [cdc.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHCbWnX4Vi7rk-NBSnvxMLDbbhIfuhm2jpOgcjP62MoGrN37HA-kon_Sy2CZ7dx9WnH8SVgpH-jNweeA-16YvjQGsWObuKkj9D9w-pHpLPhNns23AF3OMc4eETWhTb6R2KZ7twIJtNV1RQ3SPttnvaiv02JXwzMumUNu8rf)
30. [bayarealyme.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFrn4BroupVu8Ak135r8Q8msExPg3YnkZbc7csABhXT0NqsWGofgrZBflCieQWvMDutzpXKeEtwYFbGiEx6fUuy-AYuidHqC9kqmrmDrPx9NIFV4paqLZhzF0JQDniYQsoOeDn6BMSu2oxChoxiw66msGi-jZVeSiXYQOI=)
31. [mnatlas.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEYtVHO7Ri7xogmL_VSshFKZoJiDODovbxc_9Ku76_eo2-tTWMvrgS4k5ME37Er-SfAd48vFQD-DT4qW2tUSXsxIUTxJCj5dnM6hWwFbYe9FOWXKTmYFUtc753J9_zN594WSOWKPvoqRY2LqkINdYQ=)
32. [nih.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHleFZLN3Lr_ZhlqPvi-i0WAacFOu_hono5xA2ehdSXMB7WKiemKiqKXS6NxfAo1kybUIrwVcVHxZVMXOhhW18_AoUkZhHxNx56dFQVtgKPfDQ3obeOaLNRwXuttKW5dZhwwFWtu14FoA==)
33. [nih.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEZDhBI0kmCaW_SVsqN9UKq2xz5Xatv5rbcqR_jjcXMDpjjrahf1XZ3iLhOOIgOzRj3003KX2VopPc6p7ggOIq4IdsBOMbY0-XbzauNHMizdWNo-ZpNBG2XWT9v4QeEOaFVb3XhuLc_)
34. [nih.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGc8BySijvsg1piK47bcbL_5kjg2sFjipfLlfsLxS9M856rr4s3XCL7oTs_XjY1ouaXAgGlwGEGymzQqy_8wpa-QKRyh5DQ9SYNUICkfrozRAWSlRuSODSJeWX2yafBfQ==)
35. [researchgate.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG7-nJLBLdO3s80W_czqzwx-HmP7gxoyHBGL6ryzzcZDYNh50WZvXIgfU44_mUkHsDP8kIDP2pQOZnzalKmk8zCU3Gyo4Qyur3zZVvZ3UNBzgYOIqgfH1eLiAZSbmDnb4N63B_oxp9C3OJdZatwgObO5QV9Q5wZo9JEMgDu6FZ1JKnXNRoPw3DvdtQeA0DcQGFZtVaYXuglETXm3GS_biMiqE3ljbMOPXyP652LoXRK-TwwQy6VD3_GAZasuqyLAuGN-jQ5omXpkEiD9R-dP1Ea-hJHQmYF8TMubbh_2ptZYQb0Btc=)
36. [clinisys.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFZxATe8qT4nfU1ifjD9WsO0MBtnOT8vwf1ANjaMlgmMhRO8g3wHVyuppJIKQ7JSwFUITw66CmwmNd_UJ5prvBn4Zpp5Cr0_ClVtJbQq1Nocg0UIJxHsXIJEWqOf1OBAgSXOm7TNul7kQy4XS4iSgtINlFXW22Y8z3UmV81XJ4FHg0PBokTQN9zOtVhV-eO4xwFKnR3C7yUyZwZn8WW)
37. [columbia.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEBVkrn0TGF_Tik9jnu5dAZFRGv3JVuarVe6mjI89fuyMszc1HyQGMynmk8NdXUS1TBmC2uy9MRf9-KxlU6r9vAaomMyjIsrpUQFtb6Ovza5dhY91D8Gj0HM7uGMVawwkNpeevVM7iwMeWQAZZWTZIrGx8eAf-_hiRk6hNtJxRSB7PJm8QJKa4J_Co5Wej7THrbN9Xa-RYKxgTNST-YjirpTsQeTffiFL_wZAXLnQHPQAnQj3gpQFkUcSXaioNVAMZ_CVV8kMcx8z1R5XvyxdK47Q==)
38. [nih.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEvwOeMrMi20FcAia3oVAHSo5kuCja5om1S5kyDCyl6XcF59U1QWlzdsJEHr9ybEFLPRW2or3CkGXm36ZCb5G8gh8DZ3KK61cWVGGohhZa2De50QvzTy9ScrD9bPlqNn_-0H6VaX9_W0g==)
39. [nih.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFbgORamMVQK619Q_t6xbfWiggzCrV1tpl4CSip0XSfXRqc8TqdZ6Yy_6mp03sLHO5XBytt17WZmSTzz9PUFktL0RcPMDl_y1hHYC7uuEvJTvh44RBnnPfKQHcwVsX5sswghMqwAdFR3A==)
40. [nih.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH8Ud9DWhxtyOumepzfKhRQKsBVJMmGejulwYtQDWUdkKDekqFiivKE5fQN-7VWM5NILz8nOaSblcsodBnKViArZhPlAbpFpirXg-isx41t136D3BZuieokoFqpO76kTLh-0REXHk5u)
41. [nih.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEsSk65ZxuMXdRnqKd1U_KD_Qqresj2Xo3z9v8U5PWDv2X_xNDHBxMV5nUvXig2hAHtMTqlmur7uGxz4ok0-WqnlC4ZQbx7A-Cz0EXitiJAxiam6Zigi09BgoirHsOQag==)
42. [entsoc.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGUSaur3PXBBMqqEiqK-KLOGcGZu4hCh2SYAoTkEV54O6MdT4ARW04MUNX-1IXYhMIIpX_zbC83v_HhhYkZh4Rfk_ET6LNhWvbobMokF2PR7QtoJIMIqS0m0dFRP7-b3AK6WDynxrc4d6F9jOw7mDJkGZk2CFY9AatYSOztfxHEkM3-kys=)
43. [datalumos.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGY5nCm48Z40bGMePmHSueqz-89oen3T8u0Neh00RyWr3Jqo45gMQeKjQAyNAZ2VSKe2SmBk7c0RaU9Xd56MHD80jEECR8L4dHzLrnITCni19GLPDAUnsTDtZ356ByUCgC8gxXrms-SNYX1o7Q9BrPtDuS7SuWbyUw=)
44. [mdpi.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEp9VCludIuXWGalHlnPapSRg1Ig82g1lXLgBbzmhL3KqVH6_6IhJsLL6ztTcq62Iva3Nbe6-0lFXq27JPY0ZYa0RZ8-H82_Gr-H9s2hQ08bNkxKqYVwXR4rFjwJH1y)
45. [mdpi.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFtyym9RF-IW3xZoZQYAcqj62czTuwWYxNuhDlOYjok6KQxUVW5zglhEjiMWr5YvsDYvqxAAv73vsT3O4Iol0c5QPH0T2O9NslGhJu3Y1A05YOfoUHp0TjYGHJjmmk=)
46. [usgs.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGQBgNlfSUCC--86miZKz1TgaocIL8wATBkS-twnYRwQEca6TXwbSFqtV53e3-570-TyxrWzPn3Qjj2DjoAKDWQLocw74aQOOursQJMrGMrVDagNecGmkVFPDX010BYXYpAea36zx6FPYGn0UGCcr-dNJEOCpqnWf0cyMO8v2UfL7-3HP80wuoqKnP_lg==)
47. [asafishing.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFbKh90ZbyTcUVM7QLy-95kSwDnpzuWntaD6NrgE6Z48-R-orlANHjkEtEHJJnFMZxnwdZpBl1iW5JmEUpWc2eQCoYp-6OU_R5MatUa-T3VE0ryJx7TCOvYlZKMS5W_RRlvknlwbBZkOTjY2tDEclkbWanoB8ELvlvvaho8sFo37aV5vAHOlGyzkzSIyzfARqyBT40QfmE7MiWW9w==)
48. [gitlab.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHk60FFqVIGfU8aVIu-s9XCRg8T5g12Y-rnwDiZynrpFgRX4zx0Kqm8uHU6NPrnaV4WAUIqzaKJgZEZgl8BKzYYmdOfYeYN-p5ayfjKU_pSIYl5SeRM6ftF0QCTSQF3ajLf1yWRA-m8kNbBCS1dUgJULhPP482YjNO0PWpJ)
49. [semanticscholar.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHGm6JZZvY36mBHGYAoiq2RqKIaW0dw73vDedue-dhvYdYFPHEHRy-dSzq8BkNpc0b15XhONehjttJqO4LVxmEYxwoskHcc_Ur9GxqwOyV3GNBJonAgKthZh7ZkKzsLvbEaEiKIIU6R-LgZbL2OObTnrsutadgemUopfhXZDFRmnYJMar0=)
