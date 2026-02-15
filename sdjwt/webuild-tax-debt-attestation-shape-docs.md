# SD-JWT Schema: Tax Debt Status Attestation

## Overview

Electronic attestation issued by tax authorities certifying 
                    the tax debt status of a legal entity for procurement purposes.

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

### `valid`

- **Status:** Optional
- **Original:** `valid`
- **SKOS:** `webuild-vocab:c_expiryDate`

### `is_legal_entity`

- **Status:** **Required**
- **Original:** `isLegalEntity`
- **SKOS:** `webuild-vocab:c_legalEntity`

### `issuing_institution`

- **Status:** **Required**
- **Original:** `issuingInstitution`
- **SKOS:** `webuild-vocab:c_issuingInstitution`

### `has_tax_debt_status`

- **Status:** **Required**
- **Original:** `hasTaxDebtStatus`
- **SKOS:** `webuild-vocab:c_taxDebtStatus`

### `has_tax_debt_amount`

- **Status:** Optional
- **Original:** `hasTaxDebtAmount`
- **SKOS:** `webuild-vocab:c_taxDebtAmount`

### `has_applicable_jurisdiction`

- **Status:** **Required**
- **Original:** `hasApplicableJurisdiction`
- **SKOS:** `webuild-vocab:c_jurisdiction`

### `has_debt_arrangement_status`

- **Status:** Optional
- **Original:** `hasDebtArrangementStatus`
- **SKOS:** `webuild-vocab:c_debtArrangement`

### `applicable_period`

- **Status:** Optional
- **Original:** `applicablePeriod`
- **SKOS:** `webuild-vocab:c_period`

