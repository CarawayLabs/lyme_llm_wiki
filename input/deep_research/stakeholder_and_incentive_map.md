---
agent_name: stakeholder_and_incentive_map
agent_type: deep_research
output_artifact: stakeholder_and_incentive_map_output.md
dependencies:
  - synthesis_agent_integrate_findings
  - problem_space_map
  - patient_and_clinician_journeys
  - previous_solution_analysis
template_engine: jinja2
---

# Deep Research Agent Prompt: Stakeholder and Incentive Map

## Role

Act as a health-system strategist, stakeholder researcher, implementation scientist, and product-market analyst.

## Mission

Map the stakeholder ecosystem surrounding Lyme disease and related tick-borne disease decisions.

Determine:

1. Who experiences each problem.
2. Who makes decisions.
3. Who controls data.
4. Who can act.
5. Who benefits.
6. Who pays.
7. Who operates a solution.
8. Who bears risk.
9. Which incentives align or conflict.
10. Why useful ideas may fail to be adopted.

## Supplied artifacts

### Integrated synthesis

<artifact name="synthesis_agent_integrate_findings">
{{ synthesis_agent_integrate_findings }}
</artifact>

### Problem-space map

<artifact name="problem_space_map">
{{ problem_space_map }}
</artifact>

### Patient and clinician journeys

<artifact name="patient_and_clinician_journeys">
{{ patient_and_clinician_journeys }}
</artifact>

### Previous solution analysis

<artifact name="previous_solution_analysis">
{{ previous_solution_analysis }}
</artifact>

## Stakeholders to analyze

At minimum:

- People seeking prevention information
- People with tick encounters
- Patients with early disease
- Patients with delayed or uncertain diagnosis
- Patients with persistent symptoms
- Caregivers
- Parents and guardians
- Primary-care clinicians
- Urgent-care clinicians
- Emergency clinicians
- Pediatric clinicians
- Infectious-disease specialists
- Neurologists
- Rheumatologists
- Dermatologists
- Laboratory professionals
- Health systems
- State and local health departments
- Federal agencies
- Researchers
- Vector-control programs
- Insurers
- Employers
- Schools and camps
- Outdoor organizations
- Outdoor workers
- Patient advocacy organizations
- Vendors and digital-health developers
- Funders
- Regulators

Add stakeholders discovered in upstream artifacts.

## Required analysis dimensions

For each stakeholder:

- Goals
- Decisions
- Success measures
- Pain points
- Information needs
- Data owned
- Data accessible
- Ability to act
- Budget authority
- Purchasing authority
- Implementation burden
- Clinical or legal risk
- Reputational risk
- Incentives
- Disincentives
- Trust relationships
- Power
- Dependency on others
- Likely resistance
- Adoption requirements

## Required deliverables

### 1. Executive ecosystem synthesis

Summarize:

- Central actors
- High-power actors
- High-need but low-power actors
- Misaligned incentives
- Data-control bottlenecks
- Adoption bottlenecks
- Likely operators and payers
- Stakeholders requiring direct validation

### 2. Stakeholder master matrix

| Stakeholder ID | Stakeholder | Role | Goals | Decisions | Problems | Data owned | Data needed | Ability to act | Power | Interest | Budget authority | Risk exposure | Incentives | Disincentives | Trust level | Adoption conditions | Upstream IDs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

### 3. User-beneficiary-buyer-operator map

For each important problem, identify:

| Problem ID | User | Beneficiary | Decision-maker | Buyer or funder | Operator | Data owner | Risk owner | Misalignment |
|---|---|---|---|---|---|---|---|---|

### 4. Incentive alignment map

Create:

| Relationship | Shared incentive | Conflicting incentive | Current behavior | Consequence | Evidence | Validation need |
|---|---|---|---|---|---|---|

### 5. Power-interest matrix

Classify stakeholders as:

- High power / high interest
- High power / low interest
- Low power / high interest
- Low power / low interest

Explain engagement implications.

### 6. Data-governance map

| Data | Owner | Controller | User | Legal basis | Sharing incentive | Sharing barrier | Access path | Sustainability |
|---|---|---|---|---|---|---|---|---|

### 7. Adoption workflow analysis

For major settings such as:

- Patient self-service
- Primary care
- Urgent care
- Laboratory
- Public health
- Employer or school
- Research

Identify:

- Decision to adopt
- Required approvers
- Procurement
- Integration
- Training
- Maintenance
- Liability
- Measurement
- Renewal or continued funding

### 8. Business and operating-model hypotheses

Do not design products. Identify plausible models such as:

- Government-operated
- Health-system-operated
- Employer-funded
- Insurer-funded
- Grant-funded
- Nonprofit-operated
- Research infrastructure
- Consumer-paid
- Public-private partnership

For each, evaluate incentive fit and sustainability.

### 9. Stakeholder conflict register

| Conflict ID | Stakeholders | Issue | Root cause | Power imbalance | Consequence | Evidence | Mitigation hypothesis |
|---|---|---|---|---|---|---|---|

### 10. Interview priority matrix

Score stakeholders on:

- Importance
- Knowledge
- Power
- Uncertainty
- Access difficulty
- Risk of untested assumptions

Provide recommended interview order.

## Required final sections

End with exactly:

## Stakeholders with the greatest unmet need

## Stakeholders with the greatest ability to act

## Major incentive misalignments

## Data and power bottlenecks

## Most plausible operators and funders

## Highest-priority stakeholder interviews

## Rules

- Cite claims about incentives and workflows.
- Separate documented behavior from hypotheses.
- Do not assume the user is the buyer.
- Do not assume the beneficiary controls adoption.
- Do not recommend a final business model.
- Preserve upstream IDs and traceability.
