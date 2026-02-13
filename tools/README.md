# SHACL to W3C VC Tools

Two tools for converting SHACL application profiles into W3C Verifiable Credentials:

1. **shacl-to-vc-converter.py** - Generates JSON-LD contexts and JSON Schemas
2. **generate_vc_templates.py** - Generates fillable VC templates

## Purpose

SHACL (Shapes Constraint Language) defines the structure and validation rules for RDF data. These tools transform SHACL shapes into production-ready W3C VC components:

1. **JSON-LD Contexts** - Map SHACL properties to W3C VC format
2. **JSON Schemas** - Provide validation for credential subjects
3. **VC Templates** - Fillable and example credentials
4. **Ready for EU Business Wallet** - Standards-compliant credentials

## Installation

```bash
# No dependencies needed - uses Python 3 standard library only
chmod +x shacl-to-vc-converter.py
```

## Usage

### Basic Conversion

```bash
python3 shacl-to-vc-converter.py <shacl-file.jsonld> [output-dir]
```

### Example: Convert Bill of Lading SHACL

```bash
python3 tools/shacl-to-vc-converter.py \
  shacl/bill-of-lading-v0.0.1.jsonld \
  .
```

**Output:**
- `contexts/billoflading-context.jsonld` - JSON-LD context
- `credentials/billoflading-schema.json` - JSON Schema
- Plus contexts/schemas for all referenced types (Party, Location, GoodsItem, etc.)

## How It Works

### 1. SHACL Input Structure

The tool expects SHACL JSON-LD files from tietomallit.suomi.fi with:

- **NodeShapes** (`sh:NodeShape`) - Define document types
- **PropertyShapes** (`sh:PropertyShape`) - Define properties with:
  - `sh:path` - Links to KTDDE vocabulary
  - `sh:datatype` - XSD datatype (for literals)
  - `sh:class` - Target class (for object properties)
  - `sh:minCount` / `sh:maxCount` - Cardinality constraints

### 2. JSON-LD Context Generation

Maps SHACL properties to W3C VC JSON-LD:

- Extracts `sh:path` for `@id` mapping
- Converts `sh:datatype` to JSON-LD `@type`
- Identifies collections via `sh:maxCount`
- Adds `@container: @set` for arrays

### 3. JSON Schema Generation

Creates validation schemas:

- Maps XSD types to JSON Schema types
- Enforces cardinality constraints (`minCount` → required)
- Structures nested objects for `sh:class` references
- Includes W3C VC envelope structure

## Supported SHACL Features

✅ **Fully Supported:**
- `sh:NodeShape` with `sh:targetClass`
- `sh:PropertyShape` with `sh:path`
- `sh:datatype` (all XSD types)
- `sh:class` (object property references)
- `sh:minCount` / `sh:maxCount` (cardinality)
- Multi-language labels (`rdfs:label`)

⚠️ **Partial Support:**
- Complex SHACL constraints (not yet mapped to JSON Schema)
- `sh:or`, `sh:and`, `sh:not` logic (simplified)

🔄 **Future:**
- SHACL validation rule to JSON Schema constraint mapping
- Example credential generation
- Vocabulary documentation extraction

## Output Structure

For each SHACL NodeShape, generates:

### JSON-LD Context (`contexts/<name>-context.jsonld`)

```json
{
  "@context": {
    "@version": 1.1,
    "@protected": true,
    "ktdde": "https://iri.suomi.fi/model/ktddecv/",
    "BillOfLading": {
      "@id": "ktddecv:BillOfLading",
      "@context": {
        "documentIdentifier": {
          "@id": "ktddecv:documentIdentifier"
        },
        "issueDate": {
          "@id": "ktddecv:issueDate",
          "@type": "xsd:date"
        },
        "carrierParty": {
          "@id": "ktddecv:carrierParty",
          "@type": "@id"
        }
      }
    }
  }
}
```

### JSON Schema (`credentials/<name>-schema.json`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Bill of Lading Verifiable Credential",
  "type": "object",
  "required": ["@context", "type", "issuer", "issuanceDate", "credentialSubject"],
  "properties": {
    "@context": { ... },
    "credentialSubject": {
      "type": "object",
      "properties": {
        "type": {"const": "BillOfLading"},
        "documentIdentifier": {"type": "string"},
        "issueDate": {"type": "string", "format": "date"},
        "carrierParty": {"type": "object"}
      }
    }
  }
}
```

## Integration with W3C VCs

### Using Generated Context

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://github.com/jgmikael/trade-automation/contexts/billoflading-context.jsonld"
  ],
  "type": ["VerifiableCredential", "BillOfLadingCredential"],
  "issuer": "did:example:carrier",
  "issuanceDate": "2024-02-13T10:00:00Z",
  "credentialSubject": {
    "type": "BillOfLading",
    "documentIdentifier": "BOL-2024-0001",
    "issueDate": "2024-02-13",
    "carrierParty": {
      "type": "Party",
      "partyName": "Global Shipping Line"
    }
  },
  "proof": { ... }
}
```

### Validation

```bash
# Validate against JSON Schema
ajv validate -s credentials/billoflading-schema.json -d my-credential.json
```

## KTDDE Document Types

Ready to process from tietomallit.suomi.fi:

1. **Bill of Lading** (dsibol) ✅ Tested
2. **Commercial Invoice** (TBD)
3. **Certificate of Origin** (TBD)
4. **[Your 4th document]** (TBD)

## Next Steps

1. **Add remaining 3 SHACL files** to `shacl/` directory
2. **Run converter** on each file
3. **Create example credentials** using generated schemas
4. **Implement validation** pipeline
5. **Build issuer/verifier** services

---

## Tool 2: VC Template Generator

### Purpose

Generates fillable W3C Verifiable Credential templates from SHACL profiles. Creates both:
- **Empty templates** with placeholders (for filling in)
- **Example templates** with sample data (for reference)

### Usage

```bash
python3 generate_vc_templates.py <shacl-file.jsonld> [output-dir]
```

### Example

```bash
# Generate templates for Commercial Invoice
python3 generate_vc_templates.py ../shacl/commercial-invoice-v0.0.2.jsonld ../templates/

# Outputs:
# - templates/empty/commercialinvoice-template.jsonld    (fillable)
# - templates/examples/commercialinvoice-example.jsonld  (with examples)
# - Plus templates for all supporting types (Party, Location, etc.)
```

### Output Structure

#### Empty Templates (`templates/empty/`)

Fillable templates with placeholders:

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://github.com/jgmikael/trade-automation/contexts/commercialinvoice-context.jsonld"
  ],
  "id": "<<CREDENTIAL_ID>>",
  "type": ["VerifiableCredential", "CommercialInvoiceCredential"],
  "issuer": {
    "id": "<<ISSUER_DID>>",
    "name": "<<ISSUER_NAME>>"
  },
  "issuanceDate": "<<ISO_8601_DATETIME>>",
  "credentialSubject": {
    "id": "<<SUBJECT_ID>>",
    "type": "CommercialInvoice",
    "invoiceNumber": "<<Invoice Number>>",
    "invoiceDate": "<<YYYY-MM-DD>>",
    "totalAmount": [
      {
        "type": "MonetaryAmount",
        "<<PROPERTY>>": "<<VALUE for MonetaryAmount>>"
      }
    ]
  },
  "proof": {
    "type": "<<SIGNATURE_TYPE>>",
    "created": "<<ISO_8601_DATETIME>>",
    "verificationMethod": "<<ISSUER_DID#KEY_ID>>",
    "proofPurpose": "assertionMethod",
    "proofValue": "<<SIGNATURE_VALUE>>"
  }
}
```

**How to use:**
1. Copy template
2. Replace `<<PLACEHOLDERS>>` with actual values
3. Sign and issue the credential

#### Example Templates (`templates/examples/`)

Pre-filled with realistic sample data:

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://github.com/jgmikael/trade-automation/contexts/commercialinvoice-context.jsonld"
  ],
  "id": "https://example.com/credentials/commercialinvoice/EXAMPLE-001",
  "type": ["VerifiableCredential", "CommercialInvoiceCredential"],
  "issuer": {
    "id": "did:example:issuer123",
    "name": "Example Commercial Invoice Issuer"
  },
  "issuanceDate": "2026-02-13T17:40:49.107553Z",
  "credentialSubject": {
    "id": "https://example.com/commercialinvoice/EXAMPLE-001",
    "type": "CommercialInvoice",
    "invoiceNumber": "Example Invoice Number",
    "invoiceDate": "2026-02-13",
    "totalAmount": [
      {
        "type": "MonetaryAmount",
        "amountValue": 1000.0,
        "currencyCode": "EUR"
      }
    ],
    "buyerParty": [
      {
        "type": "Party",
        "partyName": "Example Company Ltd",
        "hasAddress": {
          "type": "Address",
          "street": "123 Example Street",
          "city": "Example City",
          "postalCode": "12345"
        }
      }
    ]
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-02-13T17:40:49.107553Z",
    "verificationMethod": "did:example:issuer123#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z58DAdFfa9SkqZMVPxAQp..."
  }
}
```

**How to use:**
1. Reference as examples
2. Copy structure for similar credentials
3. Use in documentation and demos

### Features

- **Automatic placeholder generation** based on field types
- **Smart example values** for common types (Party, Amount, Location, etc.)
- **Complete VC structure** including proof section
- **Proper JSON-LD contexts** linked
- **W3C VC 1.1 compliant** format

### Generate All Document Templates

```bash
# Bill of Lading
python3 generate_vc_templates.py ../shacl/bill-of-lading-v0.0.1.jsonld ../templates/

# Certificate of Origin
python3 generate_vc_templates.py ../shacl/certificate-of-origin-v0.0.1.jsonld ../templates/

# Commercial Invoice
python3 generate_vc_templates.py ../shacl/commercial-invoice-v0.0.2.jsonld ../templates/

# Documentary Credit
python3 generate_vc_templates.py ../shacl/letter-of-credit-v0.0.1.jsonld ../templates/

# Purchase Order
python3 generate_vc_templates.py ../shacl/purchase-order-v0.0.1.jsonld ../templates/
```

---

## Technical Notes

- **Zero dependencies** - Pure Python 3 stdlib
- **Fast** - Processes 17 shapes in <1 second
- **Extensible** - Easy to add custom mappings
- **Standards-compliant** - W3C VC 1.1, JSON-LD 1.1, JSON Schema Draft 7

## License

(To be determined)
