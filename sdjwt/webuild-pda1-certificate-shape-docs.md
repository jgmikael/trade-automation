# SD-JWT Schema: Portable Document A1 Certificate

## Overview

Electronic attestation certifying which Member State's social 
                    security legislation applies to a posted or mobile worker in the EU.
                    Required for cross-border work to avoid double social security contributions.

⚠️ **Critical:** SD-JWT uses plain JSON without @context

## Claims

### `identifier`

- **Status:** **Required**
- **Original:** `identifier`
- **SKOS:** `webuild-vocab:c_identifier`

### `issued`

- **Status:** **Required**
- **Original:** `issued`
- **SKOS:** `webuild-vocab:c_issueDate`

### `covered_period`

- **Status:** **Required**
- **Original:** `coveredPeriod`
- **SKOS:** `webuild-vocab:c_periodStart`

### `valid`

- **Status:** Optional
- **Original:** `valid`
- **SKOS:** `webuild-vocab:c_periodEnd`

### `insured_person`

- **Status:** **Required**
- **Original:** `insuredPerson`
- **SKOS:** `webuild-vocab:c_insuredPerson`

### `has_employer`

- **Status:** **Required**
- **Original:** `hasEmployer`
- **SKOS:** `webuild-vocab:c_employer`

### `issuing_institution`

- **Status:** **Required**
- **Original:** `issuingInstitution`
- **SKOS:** `webuild-vocab:c_issuingInstitution`

### `has_legal_applicability`

- **Status:** **Required**
- **Original:** `hasLegalApplicability`
- **SKOS:** `webuild-vocab:c_applicableLegislation`

### `has_work_location`

- **Status:** **Required**
- **Original:** `hasWorkLocation`
- **SKOS:** `webuild-vocab:c_workLocation`

### `has_activity`

- **Status:** **Required**
- **Original:** `hasActivity`
- **SKOS:** `webuild-vocab:c_activity`

### `employment_type`

- **Status:** **Required**
- **Original:** `employmentType`
- **SKOS:** `webuild-vocab:c_employmentType`

### `has_applicable_jurisdiction`

- **Status:** **Required**
- **Original:** `hasApplicableJurisdiction`
- **SKOS:** `webuild-vocab:c_legalBasis`

### `is_subject_to_transitional_rules`

- **Status:** Optional
- **Original:** `isSubjectToTransitionalRules`
- **SKOS:** `webuild-vocab:c_transitionalRules`

### `has_determination`

- **Status:** Optional
- **Original:** `hasDetermination`
- **SKOS:** `webuild-vocab:c_determination`

