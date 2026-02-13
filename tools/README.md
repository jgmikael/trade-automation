# SHACL to W3C VC Converter

Automatically converts SHACL application profiles into W3C Verifiable Credential JSON-LD contexts and JSON Schemas.

## Purpose

SHACL (Shapes Constraint Language) defines the structure and validation rules for RDF data. This tool transforms SHACL shapes into production-ready W3C VC components:

1. **JSON-LD Contexts** - Map SHACL properties to W3C VC format
2. **JSON Schemas** - Provide validation for credential subjects
3. **Ready for EU Business Wallet** - Standards-compliant credentials

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

## Technical Notes

- **Zero dependencies** - Pure Python 3 stdlib
- **Fast** - Processes 17 shapes in <1 second
- **Extensible** - Easy to add custom mappings
- **Standards-compliant** - W3C VC 1.1, JSON-LD 1.1, JSON Schema Draft 7

## License

(To be determined)
