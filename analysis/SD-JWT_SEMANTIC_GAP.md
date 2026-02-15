# SD-JWT Semantic Gap: Problem and Solution

## 🚨 The Problem

**IETF SD-JWT** (Selective Disclosure JWT) for verifiable credentials uses **plain JSON** without `@context`.

### W3C JSON-LD VC (Has Semantics) ✅

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://iri.suomi.fi/context/ktdde/v1"  // ⭐ Semantic linking!
  ],
  "type": ["VerifiableCredential"],
  "credentialSubject": {
    "packageType": "BDL"  // Maps to ktddecv:packageTypeCode via @context
  }
}
```

**Semantic resolution:**
```
"packageType" 
    ↓ (@context lookup)
ktddecv:packageTypeCode
    ↓ (dcterms:subject)
ktdde:c001 (SKOS concept)
    ↓
Full definition from sanastot.suomi.fi
```

### IETF SD-JWT (No Semantics) ❌

```json
{
  "iss": "https://issuer.example.com",
  "sub": "did:example:123",
  "package_type": "BDL"  // ❌ Just a string, no semantic meaning!
}
```

**Problems:**
- ❌ No `@context` field
- ❌ No automatic mapping to RDF
- ❌ `package_type` is just an arbitrary identifier
- ❌ No link to SHACL → OWL → SKOS layers
- ❌ Semantic meaning is lost

---

## 💡 The Solution: Semantic Registry

### Architecture

```
┌─────────────────────────────────────────────────┐
│ SD-JWT (Plain JSON)                             │
│ { "package_type": "BDL" }                       │
└──────────────┬──────────────────────────────────┘
               │
               │ (external lookup)
               ↓
┌─────────────────────────────────────────────────┐
│ Semantic Registry (JSON)                        │
│ {                                               │
│   "package_type": {                             │
│     "shacl_property": "...",                    │
│     "owl_property": "ktddecv:packageTypeCode",  │
│     "skos_concept": "ktdde:c001"               │
│   }                                             │
│ }                                               │
└──────────────┬──────────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────────┐
│ Layer 3: SHACL (Constraints)                    │
└──────────────┬──────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────┐
│ Layer 2: OWL (Data Model)                       │
└──────────────┬──────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────┐
│ Layer 1: SKOS (Concepts)                        │
└─────────────────────────────────────────────────┘
```

**Key Insight:** Since SD-JWT doesn't support `@context`, we maintain semantic links in a **separate registry** that maps SD-JWT claims back to SHACL/OWL/SKOS.

---

## 🛠️ Tool: SHACL to SD-JWT Converter

### What It Does

1. **Reads SHACL shapes** from tietomallit.suomi.fi
2. **Generates SD-JWT schema** (JSON Schema format)
3. **Creates snake_case claims** (e.g., `packageTypeCode` → `package_type`)
4. **Maintains semantic mapping** in separate registry
5. **Generates documentation** with semantic lineage

### Usage

```bash
python tools/shacl_to_sdjwt.py shacl/packinglist-shape.ttl
```

### Output Files

```
sdjwt/
├── packinglist-schema.json          # SD-JWT JSON Schema
├── packinglist-docs.md              # Human-readable docs
└── semantic-registry.json           # Claim → Semantic mapping
```

---

## 📄 Example Output

### Input: SHACL Shape

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ktddecv: <https://iri.suomi.fi/model/ktddecv/> .
@prefix ktdde: <https://iri.suomi.fi/terminology/ktdde/> .

dsi:PackingListShape
  a sh:NodeShape ;
  sh:targetClass ktddecv:PackingList ;
  dcterms:subject ktdde:c_packingList ;
  
  sh:property [
    sh:path ktddecv:packageTypeCode ;
    dcterms:subject ktdde:c_packageType ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:in ( "PAL" "BOX" "BDL" ) ;
  ] ;
  .
```

### Output 1: SD-JWT Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "Packing List",
  "properties": {
    "package_type_code": {
      "type": "string",
      "description": "Code identifying package type",
      "enum": ["PAL", "BOX", "BDL"]
    }
  },
  "required": ["package_type_code"],
  "_semantic_mapping": {
    "shacl_shape": "https://iri.suomi.fi/model/dsi/PackingListShape",
    "target_class": "https://iri.suomi.fi/model/ktddecv/PackingList",
    "skos_concept": "https://iri.suomi.fi/terminology/ktdde/c_packingList",
    "properties": {
      "package_type_code": {
        "owl_property": "https://iri.suomi.fi/model/ktddecv/packageTypeCode",
        "shacl_path": "https://iri.suomi.fi/model/ktddecv/packageTypeCode",
        "skos_concept": "https://iri.suomi.fi/terminology/ktdde/c_packageType",
        "mandatory": true
      }
    }
  }
}
```

### Output 2: Semantic Registry

```json
{
  "$schema": "https://openclaw.ai/schemas/semantic-registry-v1.json",
  "description": "Semantic registry mapping SD-JWT claims to SHACL/OWL/SKOS",
  "version": "1.0.0",
  "layers": {
    "layer_5": "SD-JWT (IETF RFC, plain JSON)",
    "layer_4": "JSON-LD (@context - MISSING in SD-JWT!)",
    "layer_3": "SHACL (validation constraints)",
    "layer_2": "OWL (data model)",
    "layer_1": "SKOS (conceptual vocabulary)"
  },
  "mappings": {
    "package_type_code": {
      "sdjwt_claim": "package_type_code",
      "shacl_shape": "https://iri.suomi.fi/model/dsi/PackingListShape",
      "shacl_property": "https://iri.suomi.fi/model/ktddecv/packageTypeCode",
      "owl_property": "https://iri.suomi.fi/model/ktddecv/packageTypeCode",
      "skos_concept": "https://iri.suomi.fi/terminology/ktdde/c_packageType",
      "label": "Package Type Code",
      "description": "Code identifying the type of package"
    }
  }
}
```

### Output 3: Documentation (Markdown)

```markdown
# SD-JWT Schema: Packing List

**Critical Note:** SD-JWT uses plain JSON without @context

## Semantic Lineage

| Layer | Resource |
|-------|----------|
| Layer 5 | SD-JWT Schema |
| Layer 4 | ⚠️ NOT SUPPORTED by SD-JWT |
| Layer 3 | SHACL Shape: dsi:PackingListShape |
| Layer 2 | OWL Class: ktddecv:PackingList |
| Layer 1 | SKOS Concept: ktdde:c_packingList |

## Claims

### `package_type_code`

- **Status:** Required
- **Type:** string
- **Allowed Values:** PAL, BOX, BDL

**Semantic Traceability:**
- SHACL Path: ktddecv:packageTypeCode
- OWL Property: ktddecv:packageTypeCode
- SKOS Concept: ktdde:c_packageType

## Semantic Resolution

```
SD-JWT claim: "package_type_code"
       ↓ (registry lookup)
SHACL property: ktddecv:packageTypeCode
       ↓ (sh:path)
OWL property: ktddecv:packageTypeCode
       ↓ (dcterms:subject)
SKOS concept: ktdde:c_packageType
       ↓ (sanastot.suomi.fi)
Definition: [Access vocabulary]
```
```

---

## 📊 Comparison: JSON-LD vs SD-JWT

| Feature | JSON-LD W3C VC | SD-JWT IETF |
|---------|----------------|-------------|
| **@context** | ✅ Built-in | ❌ Not supported |
| **Automatic semantic linking** | ✅ Yes | ❌ No, manual registry |
| **RDF compatibility** | ✅ Native | ❌ Requires conversion |
| **SHACL validation** | ✅ Direct | ⚠️ Via registry |
| **SKOS traceability** | ✅ Automatic | ❌ Manual lookup |
| **Selective disclosure** | ⚠️ Requires BBS+ | ✅ Native |
| **JWT ecosystem** | ⚠️ Via JWT-VC | ✅ Native |
| **Simplicity** | Complex | Simple |
| **Semantic integrity** | ✅ Guaranteed | ⚠️ Requires discipline |

---

## 🎯 Best Practices

### 1. Always Distribute Registry with Schema

```
credential-package/
├── schema.json              # SD-JWT schema
├── semantic-registry.json   # Semantic mappings
└── documentation.md         # Human-readable docs
```

### 2. Embed Registry Reference in SD-JWT

```json
{
  "iss": "https://issuer.example.com",
  "type": "PackingListCredential",
  "_semantic_registry": "https://issuer.example.com/registry/v1/packing-list",
  "package_type_code": "BDL"
}
```

### 3. Provide Resolution Endpoint

```
GET https://issuer.example.com/semantics/resolve?claim=package_type_code

Response:
{
  "claim": "package_type_code",
  "owl_property": "https://iri.suomi.fi/model/ktddecv/packageTypeCode",
  "skos_concept": "https://iri.suomi.fi/terminology/ktdde/c_packageType",
  "definition": "Classification of packaging used for goods..."
}
```

### 4. Version the Registry

```json
{
  "version": "1.0.0",
  "schema_version": "2024-02-15",
  "vocabulary_version": "ktdde:v0.0.5"
}
```

### 5. Include in Credential Metadata

```json
{
  "iss": "https://issuer.example.com",
  "credentialSchema": {
    "id": "https://example.com/schemas/packing-list-v1.json",
    "type": "JsonSchema2023"
  },
  "semanticRegistry": {
    "id": "https://example.com/registry/packing-list-v1.json",
    "type": "SemanticRegistry"
  }
}
```

---

## ⚠️ Limitations and Trade-offs

### Limitations

1. **No automatic resolution** - Requires manual registry lookup
2. **Registry dependency** - Verifiers need access to registry
3. **Version management** - Must sync schema + registry versions
4. **Claim name collisions** - snake_case may clash across domains
5. **No RDF graphs** - Cannot automatically build knowledge graphs

### Trade-offs

**Use SD-JWT when:**
- ✅ Selective disclosure is critical
- ✅ JWT ecosystem compatibility matters
- ✅ Simplicity is preferred
- ⚠️ Semantic interoperability is secondary

**Use JSON-LD W3C VC when:**
- ✅ Semantic interoperability is critical
- ✅ RDF/SPARQL processing needed
- ✅ Knowledge graph construction required
- ✅ W3C standards compliance mandatory
- ⚠️ Selective disclosure can use BBS+ signatures

---

## 💡 Recommended Approach: Dual-Track

Issue **both formats** from the same SHACL source:

```
SHACL Shape (Source of Truth)
    ↓
    ├─→ JSON-LD Context → W3C VC (semantic track)
    │
    └─→ SD-JWT Schema → IETF SD-JWT (simple track)
          + Semantic Registry (bridge to semantic track)
```

**Benefits:**
- ✅ Semantic integrity via JSON-LD
- ✅ Selective disclosure via SD-JWT
- ✅ Single source of truth (SHACL)
- ✅ Verifier can choose format
- ✅ Gradual migration path

**Implementation:**
```bash
# Generate both from SHACL
python tools/shacl_to_jsonld.py shacl/packing-list.ttl
python tools/shacl_to_sdjwt.py shacl/packing-list.ttl

# Issue in both formats
issue_credential(data, format='json-ld')  # W3C VC
issue_credential(data, format='sd-jwt')   # IETF SD-JWT
```

---

## 📚 References

- **SD-JWT Spec:** [IETF Draft](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-selective-disclosure-jwt)
- **W3C VC Data Model:** [W3C Recommendation](https://www.w3.org/TR/vc-data-model-2.0/)
- **SHACL:** [W3C Recommendation](https://www.w3.org/TR/shacl/)
- **SKOS:** [W3C Recommendation](https://www.w3.org/TR/skos-reference/)
- **OWL 2:** [W3C Recommendation](https://www.w3.org/TR/owl2-overview/)

---

## 🎯 Conclusion

**Problem:** SD-JWT loses semantic links by omitting `@context`

**Solution:** Maintain semantic traceability via external registry

**Best Practice:** Use dual-track approach (JSON-LD + SD-JWT) from single SHACL source

**Tool:** `shacl_to_sdjwt.py` automates registry generation

**Critical:** Always distribute semantic registry with SD-JWT schemas to maintain link to SKOS/OWL/SHACL layers.

---

**This approach preserves semantic integrity even when using SD-JWT's simplified JSON format.** 🎯
