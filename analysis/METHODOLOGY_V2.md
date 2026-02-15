# KTDDE Data Modeling Methodology (W3C Semantic Web Stack)

## 🎯 Foundation: Proper Layered Architecture

This methodology follows the **W3C Semantic Web technology stack** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 5: W3C Verifiable Credentials                        │
│ Purpose: Trust, provenance, digital signatures             │
│ Technology: W3C VC Data Model 1.1/2.0                      │
└────────────────────┬────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────────────────────────┐
│ Layer 4: JSON-LD Serialization                             │
│ Purpose: Data exchange format with semantics               │
│ Technology: JSON-LD 1.1, @context mappings                 │
└────────────────────┬────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────────────────────────┐
│ Layer 3: SHACL Constraints                                  │
│ Purpose: Data validation, cardinality, business rules      │
│ Technology: SHACL (Shapes Constraint Language)             │
└────────────────────┬────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: OWL Data Model                                     │
│ Purpose: Structural model, classes, properties             │
│ Technology: OWL 2, RDFS                                     │
│ Platform: tietomallit.suomi.fi                             │
└────────────────────┬────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: SKOS Vocabulary (FOUNDATION) ⭐                    │
│ Purpose: Concepts, terminology, semantic relationships      │
│ Technology: SKOS (Simple Knowledge Organization System)     │
│ Platform: sanastot.suomi.fi                                │
└─────────────────────────────────────────────────────────────┘
```

**Key Principle:** Each layer builds on the layer below. Changes flow upward, not downward.

---

## 📚 Layer 1: SKOS Vocabulary (Foundation)

### Purpose
Define **concepts** and **terminology** independent of any data model.

### Platform
**sanastot.suomi.fi** (Finnish Interoperability Platform - Vocabulary service)

### What Goes Here

#### Concepts
```turtle
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix ktdde: <https://iri.suomi.fi/terminology/ktdde/> .

ktdde:c001  # Concept for "Package Type"
  a skos:Concept ;
  skos:prefLabel "Package Type"@en ,
                 "Pakkaustyyppi"@fi ;
  skos:definition """Classification of packaging used for goods in 
                     international trade."""@en ;
  skos:altLabel "Type of Package"@en ,
                "Packaging Type"@en ;
  skos:scopeNote """Includes pallets, boxes, bundles, crates, drums, etc. 
                    Used across all trade documents involving physical goods."""@en ;
  skos:example "Pallet", "Box", "Bundle", "Crate" ;
  skos:inScheme ktdde:ConceptScheme ;
  # Relationships to other concepts
  skos:broader ktdde:c_packaging ;      # Broader concept
  skos:related ktdde:c_packageMarks ;   # Related concept
  # External mappings
  skos:closeMatch <http://example.org/uncefact/PackageType> ;  # Close but not exact
  skos:exactMatch <http://example.org/iso/PackageType> ;       # Exact equivalent
  .

ktdde:c002  # Concept for "Temperature Requirement"
  a skos:Concept ;
  skos:prefLabel "Temperature Requirement"@en ,
                 "Lämpötilavaatimus"@fi ;
  skos:definition """Temperature conditions that must be maintained for goods 
                     during transport and storage."""@en ;
  skos:scopeNote """Critical for perishables, pharmaceuticals, and chemicals. 
                    May specify range, maximum, minimum, or specific conditions."""@en ;
  skos:example "-20°C to +5°C", "Frozen", "Refrigerated 2-8°C" ;
  skos:broader ktdde:c_goodsConditions ;
  skos:related ktdde:c_dangerousGoods ;
  .

# Hierarchical structure
ktdde:c_packaging
  a skos:Concept ;
  skos:prefLabel "Packaging"@en ;
  skos:narrower ktdde:c001 ,           # Package Type
                ktdde:c_packageCount ,
                ktdde:c_packageMarks ;
  .
```

#### Concept Schemes
```turtle
ktdde:ConceptScheme
  a skos:ConceptScheme ;
  skos:prefLabel "KTDDE Trade Document Concepts"@en ;
  skos:hasTopConcept ktdde:c_document ,
                     ktdde:c_party ,
                     ktdde:c_goods ,
                     ktdde:c_transport ,
                     ktdde:c_payment ;
  dcterms:created "2026-02-15"^^xsd:date ;
  dcterms:creator "KTDDE Working Group" ;
  .
```

### Why SKOS First?

1. **Concept Independence:** Concepts exist independently of any technical implementation
2. **Semantic Relationships:** `broader`, `narrower`, `related` create semantic network
3. **Multilingual:** Multiple `prefLabel` and `altLabel` for different languages
4. **Mapping:** Link to external vocabularies (UNCEFACT, ISO, WCO) via `exactMatch`, `closeMatch`
5. **Human-Readable:** Business experts can review and validate concepts
6. **Stable Foundation:** Concepts change slowly; implementation details change frequently

### SKOS Properties Used

| Property | Purpose | Example |
|----------|---------|---------|
| `skos:prefLabel` | Preferred term | "Package Type"@en |
| `skos:altLabel` | Alternative terms | "Packaging Type"@en |
| `skos:definition` | Clear meaning | "Classification of packaging..." |
| `skos:scopeNote` | Usage guidance | "Used across all trade docs..." |
| `skos:example` | Sample values | "Pallet", "Box" |
| `skos:broader` | Parent concept | broader → Packaging |
| `skos:narrower` | Child concepts | narrower → Pallet Type |
| `skos:related` | Related concepts | related → Package Marks |
| `skos:exactMatch` | Same meaning | ISO 17025:PackageType |
| `skos:closeMatch` | Similar meaning | UNCEFACT:PackagingType |

---

## 🏗️ Layer 2: OWL Data Model

### Purpose
Define **structural elements** (classes and properties) for data modeling.

### Platform
**tietomallit.suomi.fi** (Finnish Interoperability Platform - Data model service)

### Link to SKOS
Every OWL class/property **MUST** reference its SKOS concept:

```turtle
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ktddecv: <https://iri.suomi.fi/model/ktddecv/> .
@prefix ktdde: <https://iri.suomi.fi/terminology/ktdde/> .

# OWL Property linked to SKOS Concept
ktddecv:packageTypeCode
  a owl:DatatypeProperty ;
  rdfs:label "package type code"@en ,
             "pakkaustyyppikoodi"@fi ;
  rdfs:comment "Code identifying the type of package used for goods."@en ;
  dcterms:subject ktdde:c001 ;          # ⭐ LINK TO SKOS CONCEPT
  skos:definition "See concept ktdde:c001"@en ;  # Reference for definition
  rdfs:domain ktddecv:Package ;
  rdfs:range xsd:string ;               # Could also be ktddecv:PackageTypeCode (class)
  rdfs:isDefinedBy <https://iri.suomi.fi/model/ktddecv/> ;
  .

# OWL Class for Package
ktddecv:Package
  a owl:Class ;
  rdfs:label "Package"@en ,
             "Pakkaus"@fi ;
  rdfs:comment "Container or wrapping for goods."@en ;
  dcterms:subject ktdde:c_package ;     # ⭐ LINK TO SKOS CONCEPT
  rdfs:isDefinedBy <https://iri.suomi.fi/model/ktddecv/> ;
  .

# OWL Class for structured codes (optional, if using code lists)
ktddecv:PackageTypeCode
  a owl:Class ;
  rdfs:label "Package Type Code"@en ;
  rdfs:comment "Code from controlled vocabulary of package types."@en ;
  dcterms:subject ktdde:c001 ;
  rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty rdfs:label ;
    owl:cardinality 1 ;
  ] ;
  # Could enumerate valid codes
  owl:oneOf ( ktddecv:PackageType_PAL   # Pallet
              ktddecv:PackageType_BOX   # Box
              ktddecv:PackageType_BDL   # Bundle
              ktddecv:PackageType_CRT   # Crate
            ) ;
  .
```

### OWL Design Patterns

#### Pattern 1: Simple Datatype Property
```turtle
ktddecv:issueDate
  a owl:DatatypeProperty ;
  dcterms:subject ktdde:c_issueDate ;   # SKOS concept
  rdfs:domain ktddecv:Document ;
  rdfs:range xsd:date ;
  .
```

#### Pattern 2: Object Property (Relationship)
```turtle
ktddecv:consignorParty
  a owl:ObjectProperty ;
  dcterms:subject ktdde:c_consignor ;   # SKOS concept
  rdfs:domain ktddecv:PackingList ;
  rdfs:range ktddecv:Party ;
  .
```

#### Pattern 3: Structured Value (Quantity with Unit)
```turtle
ktddecv:totalGrossWeight
  a owl:ObjectProperty ;
  dcterms:subject ktdde:c_grossWeight ;
  rdfs:domain ktddecv:PackingList ;
  rdfs:range ktddecv:Quantity ;         # Structured object
  .

ktddecv:Quantity
  a owl:Class ;
  rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty ktddecv:numericValue ;
    owl:cardinality 1 ;
  ] , [
    a owl:Restriction ;
    owl:onProperty ktddecv:unitCode ;
    owl:cardinality 1 ;
  ] ;
  .
```

### Reusability in OWL

Design properties to be **domain-agnostic** when possible:

```turtle
# ❌ BAD: Too specific
ktddecv:packingListNumber
  rdfs:domain ktddecv:PackingList ;  # Only for packing list

# ✅ BETTER: Generic
ktddecv:documentNumber
  rdfs:domain ktddecv:Document ;     # For all documents
  rdfs:range ktddecv:Identifier ;

# Then specialize in SHACL if needed
```

---

## 🔒 Layer 3: SHACL Constraints

### Purpose
Define **validation rules** and **business constraints** on top of OWL structure.

### What SHACL Adds

OWL says "what can exist" - SHACL says "what must/should exist for this use case"

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ktddecv: <https://iri.suomi.fi/model/ktddecv/> .
@prefix ktdde: <https://iri.suomi.fi/terminology/ktdde/> .
@prefix dsi: <https://iri.suomi.fi/model/dsi/> .

# SHACL Shape for Packing List
dsi:PackingListShape
  a sh:NodeShape ;
  sh:targetClass ktddecv:PackingList ;
  dcterms:subject ktdde:c_packingList ;  # ⭐ LINK TO SKOS CONCEPT
  sh:name "Packing List"@en ,
          "Pakkauslista"@fi ;
  sh:description "Validation constraints for packing list documents."@en ;
  
  # Mandatory properties
  sh:property [
    sh:path ktddecv:documentNumber ;
    sh:name "Document Number"@en ;
    sh:description "Unique identifier for the packing list"@en ;
    dcterms:subject ktdde:c001 ;        # Reference SKOS concept
    sh:class ktddecv:Identifier ;       # References OWL class
    sh:minCount 1 ;                     # Mandatory
    sh:maxCount 1 ;                     # Single value
  ] ;
  
  sh:property [
    sh:path ktddecv:issueDate ;
    sh:name "Issue Date"@en ;
    dcterms:subject ktdde:c_issueDate ;
    sh:datatype xsd:date ;              # OWL says range, SHACL validates
    sh:minCount 1 ;
    sh:maxCount 1 ;
  ] ;
  
  sh:property [
    sh:path ktddecv:packageTypeCode ;
    sh:name "Package Type"@en ;
    dcterms:subject ktdde:c001 ;        # Package Type concept
    sh:datatype xsd:string ;
    sh:minCount 1 ;                     # Mandatory for packing list
    sh:maxCount 1 ;
    sh:pattern "^[A-Z]{2,3}$" ;         # Must be 2-3 uppercase letters
    sh:in ( "PAL" "BOX" "BDL" "CRT" "DRM" ) ;  # Enumeration
  ] ;
  
  # Optional properties
  sh:property [
    sh:path ktddecv:temperatureRequirement ;
    sh:name "Temperature Requirement"@en ;
    dcterms:subject ktdde:c002 ;
    sh:datatype xsd:string ;
    sh:minCount 0 ;                     # Optional
    sh:maxCount 1 ;
    # Conditional: if goods are perishable
    sh:condition [
      sh:property [
        sh:path ( ktddecv:hasGoodsItem ktddecv:isPerishable ) ;
        sh:hasValue true ;
      ] ;
    ] ;
  ] ;
  
  # Complex validation: gross weight >= net weight
  sh:sparql [
    sh:message "Gross weight must be greater than or equal to net weight"@en ;
    sh:prefixes ktddecv: ;
    sh:select """
      SELECT $this
      WHERE {
        $this ktddecv:totalGrossWeight ?gross .
        $this ktddecv:totalNetWeight ?net .
        ?gross ktddecv:numericValue ?grossValue .
        ?net ktddecv:numericValue ?netValue .
        FILTER (?grossValue < ?netValue)
      }
    """ ;
  ] ;
  .
```

### SHACL Validation Levels

```turtle
# Level 1: Structural (required/optional, data types)
sh:minCount, sh:maxCount, sh:datatype, sh:class

# Level 2: Content (patterns, enumerations, ranges)
sh:pattern, sh:in, sh:minInclusive, sh:maxInclusive

# Level 3: Business Rules (conditional, cross-property)
sh:condition, sh:sparql, sh:equals, sh:lessThan

# Level 4: Contextual (different rules for different contexts)
sh:targetSubjectsOf, sh:targetObjectsOf
```

### SHACL Application Profiles

**Key Insight:** Different documents may have different constraints on the same property

```turtle
# OWL says: packageTypeCode CAN exist on Package
ktddecv:packageTypeCode rdfs:domain ktddecv:Package .

# SHACL for Packing List says: packageTypeCode MUST exist
dsi:PackingListShape sh:property [
  sh:path ktddecv:packageTypeCode ;
  sh:minCount 1 ;  # Mandatory
] .

# SHACL for Delivery Note says: packageTypeCode SHOULD exist
dsi:DeliveryNoteShape sh:property [
  sh:path ktddecv:packageTypeCode ;
  sh:minCount 0 ;  # Optional
] .
```

---

## 📄 Layer 4: JSON-LD Serialization

### Purpose
Provide **JSON syntax** with **RDF semantics** for data exchange.

### @context Creation

Map JSON keys to RDF properties (defined in OWL, constrained by SHACL):

```json
{
  "@context": {
    "@version": 1.1,
    "@vocab": "https://iri.suomi.fi/model/ktddecv/",
    "ktddecv": "https://iri.suomi.fi/model/ktddecv/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    
    "PackingList": {
      "@id": "ktddecv:PackingList",
      "@context": {
        "documentNumber": {
          "@id": "ktddecv:documentNumber",
          "@type": "@id"
        },
        "issueDate": {
          "@id": "ktddecv:issueDate",
          "@type": "xsd:date"
        },
        "consignor": {
          "@id": "ktddecv:consignorParty",
          "@type": "@id"
        },
        "packageType": {
          "@id": "ktddecv:packageTypeCode",
          "@type": "xsd:string"
        },
        "temperatureRequirement": {
          "@id": "ktddecv:temperatureRequirement",
          "@type": "xsd:string"
        },
        "totalGrossWeight": {
          "@id": "ktddecv:totalGrossWeight",
          "@type": "@id"
        }
      }
    },
    
    "Quantity": {
      "@id": "ktddecv:Quantity",
      "@context": {
        "value": {
          "@id": "ktddecv:numericValue",
          "@type": "xsd:decimal"
        },
        "unit": {
          "@id": "ktddecv:unitCode",
          "@type": "xsd:string"
        }
      }
    }
  }
}
```

### JSON-LD Instance

```json
{
  "@context": "https://iri.suomi.fi/context/ktdde/packing-list-v1.jsonld",
  "@type": "PackingList",
  "@id": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
  
  "documentNumber": {
    "@type": "Identifier",
    "value": "PL-2024-0567"
  },
  
  "issueDate": "2024-02-15",
  
  "consignor": {
    "@type": "Party",
    "name": "Nordic Timber Oy",
    "address": {
      "@type": "Address",
      "street": "Metsäkatu 15",
      "city": "Kuhmo",
      "postalCode": "88900",
      "country": "FI"
    }
  },
  
  "packageType": "BDL",
  
  "packages": [
    {
      "@type": "Package",
      "packageType": "BDL",
      "marksAndNumbers": "NT-FI-2024-001",
      "grossWeight": {
        "@type": "Quantity",
        "value": 3600,
        "unit": "KGM"
      }
    }
  ],
  
  "totalGrossWeight": {
    "@type": "Quantity",
    "value": 28800,
    "unit": "KGM"
  },
  
  "temperatureRequirement": "Dry storage, 15-25°C"
}
```

### Semantic Benefits of JSON-LD

1. **Looks like JSON** - Developers can use standard JSON tools
2. **Has RDF semantics** - Can be processed as RDF triples
3. **Interoperable** - Shared @context ensures same meaning
4. **Extensible** - Add properties without breaking consumers
5. **Queryable** - Can use SPARQL on JSON-LD data

---

## 🔐 Layer 5: W3C Verifiable Credentials

### Purpose
Add **trust layer** with digital signatures, issuer identity, and verification.

### W3C VC Structure

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://iri.suomi.fi/context/ktdde/packing-list-v1.jsonld"
  ],
  
  "type": ["VerifiableCredential", "PackingListCredential"],
  
  "id": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
  
  "issuer": {
    "id": "did:web:nordictimber.fi",
    "name": "Nordic Timber Oy",
    "type": "Organization"
  },
  
  "issuanceDate": "2024-02-15T10:30:00Z",
  "expirationDate": "2024-08-15T10:30:00Z",
  
  "credentialSubject": {
    "@type": "PackingList",
    "id": "urn:uuid:pl-2024-0567",
    
    "documentNumber": {
      "@type": "Identifier",
      "value": "PL-2024-0567"
    },
    
    "issueDate": "2024-02-15",
    
    "consignor": {
      "@type": "Party",
      "id": "did:web:nordictimber.fi",
      "name": "Nordic Timber Oy"
    },
    
    "packageType": "BDL",
    
    "totalGrossWeight": {
      "@type": "Quantity",
      "value": 28800,
      "unit": "KGM"
    }
  },
  
  "proof": {
    "type": "DataIntegrityProof",
    "cryptosuite": "eddsa-rdfc-2022",
    "created": "2024-02-15T10:30:00Z",
    "verificationMethod": "did:web:nordictimber.fi#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z3FXQjecWRH8e...Y8dBk4Dqm"
  }
}
```

### VC Properties

| Property | Purpose | Layer |
|----------|---------|-------|
| `@context` | JSON-LD context | Layer 4 (JSON-LD) |
| `type` | VC type | Layer 5 (VC) |
| `issuer` | Who issued it | Layer 5 (VC) |
| `credentialSubject` | The actual data | Layers 1-4 (SKOS→OWL→SHACL→JSON-LD) |
| `proof` | Digital signature | Layer 5 (VC) |

---

## 📋 Complete Workflow: Packing List Example

### Step 1: Define SKOS Concepts (sanastot.suomi.fi)

```turtle
ktdde:c_packingList
  a skos:Concept ;
  skos:prefLabel "Packing List"@en , "Pakkauslista"@fi ;
  skos:definition "Document detailing goods and packages in a shipment"@en ;
  .

ktdde:c_packageType
  a skos:Concept ;
  skos:prefLabel "Package Type"@en , "Pakkaustyyppi"@fi ;
  skos:definition "Classification of packaging used for goods"@en ;
  .

# ... continue for all data elements
```

### Step 2: Model OWL Classes/Properties (tietomallit.suomi.fi)

```turtle
ktddecv:PackingList
  a owl:Class ;
  dcterms:subject ktdde:c_packingList ;
  .

ktddecv:packageTypeCode
  a owl:DatatypeProperty ;
  dcterms:subject ktdde:c_packageType ;
  rdfs:domain ktddecv:Package ;
  rdfs:range xsd:string ;
  .
```

### Step 3: Create SHACL Shapes (application profile)

```turtle
dsi:PackingListShape
  a sh:NodeShape ;
  sh:targetClass ktddecv:PackingList ;
  dcterms:subject ktdde:c_packingList ;
  
  sh:property [
    sh:path ktddecv:packageTypeCode ;
    dcterms:subject ktdde:c_packageType ;
    sh:minCount 1 ;
  ] ;
  .
```

### Step 4: Generate JSON-LD Context

```json
{
  "@context": {
    "packageType": "ktddecv:packageTypeCode"
  }
}
```

### Step 5: Create VC Template

```json
{
  "@context": ["...vc...", "...ktdde..."],
  "type": ["VerifiableCredential", "PackingListCredential"],
  "credentialSubject": {
    "@type": "PackingList",
    "packageType": "BDL"
  }
}
```

---

## 🎯 Analysis Process (Revised)

### Phase 1: SKOS Concept Identification

**Input:** KTDDE Data Glossary (identify data elements)

**Output:** List of concepts needed

**File:** `01-concepts-needed.csv`

| Data Element | SKOS Concept ID | Concept Label | Exists in sanastot.suomi.fi? |
|--------------|-----------------|---------------|------------------------------|
| Package Type | ktdde:c_packageType | Package Type | ⚠️ Check |
| Temperature Req | ktdde:c_temperature | Temperature Requirement | ❌ Create |

### Phase 2: SKOS Vocabulary Check/Creation

**Platform:** https://sanastot.suomi.fi/

**Actions:**
1. Search for existing concepts
2. Create missing concepts
3. Define relationships (broader/narrower/related)
4. Add multilingual labels
5. Map to external vocabularies

**File:** `02-skos-proposals.ttl`

### Phase 3: OWL Property Mapping

**Input:** SKOS concepts (from Phase 2)

**Output:** OWL properties linked to SKOS

**File:** `03-owl-mapping.csv`

| SKOS Concept | OWL Property | Domain | Range | Status |
|--------------|--------------|--------|-------|--------|
| ktdde:c_packageType | ktddecv:packageTypeCode | Package | xsd:string | ✅ |
| ktdde:c_temperature | ktddecv:temperatureRequirement | GoodsItem | xsd:string | ❌ Propose |

### Phase 4: SHACL Constraints

**Input:** OWL properties + business rules

**Output:** SHACL shape

**File:** `04-shacl-shape.ttl`

### Phase 5: JSON-LD Context

**Input:** SHACL shape

**Output:** @context mapping

**File:** `05-jsonld-context.json`

### Phase 6: W3C VC Template

**Input:** JSON-LD context

**Output:** VC template

**File:** `06-vc-template.json`

---

## 📁 Revised File Structure

```
analysis/
├── METHODOLOGY_V2.md                 # This file
└── documents/
    └── packing-list/
        ├── 00-SUMMARY.md             # Executive summary
        ├── 01-concepts-needed.csv    # Data elements → SKOS concepts
        ├── 02-skos-proposals.ttl     # New SKOS concepts (if needed)
        ├── 03-owl-mapping.csv        # SKOS → OWL mapping
        ├── 04-owl-proposals.ttl      # New OWL properties (if needed)
        ├── 05-shacl-shape.ttl        # SHACL validation shape
        ├── 06-jsonld-context.json    # JSON-LD @context
        ├── 07-vc-template.json       # W3C VC template
        └── 08-example-data.json      # Sample instance
```

---

## ✅ Quality Criteria (Revised)

A mapping is production-ready when:

- ✅ All concepts exist in SKOS vocabulary (sanastot.suomi.fi)
- ✅ All OWL properties reference SKOS concepts via `dcterms:subject`
- ✅ All SHACL properties reference SKOS concepts
- ✅ JSON-LD @context maps to OWL properties (not made-up names)
- ✅ W3C VC structure follows Data Model 1.1/2.0
- ✅ Each layer is validated independently
- ✅ Semantic links are bidirectional and traceable

---

## 🎯 Key Differences from V1

| Aspect | Old Approach (V1) | New Approach (V2) |
|--------|------------------|-------------------|
| **Foundation** | UNTDED codes | SKOS concepts |
| **Starting Point** | Data elements | Conceptual vocabulary |
| **Vocabulary** | Implicit in OWL | Explicit in SKOS |
| **Terminology** | Buried in comments | First-class citizens |
| **Semantic Links** | Missing | dcterms:subject throughout |
| **Platform** | Generic | sanastot.suomi.fi + tietomallit.suomi.fi |
| **Layers** | Mixed | Clearly separated |
| **Validation** | Only SHACL | SKOS + OWL + SHACL |

---

## 🚀 Next Steps

1. **Access sanastot.suomi.fi**
   - Review existing KTDDE SKOS vocabulary
   - Identify which concepts already exist

2. **Map Data Elements to SKOS**
   - For each data element, find/create SKOS concept
   - Define concept relationships

3. **Link OWL to SKOS**
   - Ensure all OWL properties have `dcterms:subject` pointing to SKOS
   - Propose new OWL properties only after SKOS concepts exist

4. **Create SHACL with Semantic Links**
   - Reference SKOS concepts in SHACL shapes
   - Enable traceability from constraint back to concept

5. **Generate JSON-LD and VCs**
   - Build proper @context from OWL (not made-up names)
   - Wrap in W3C VC structure

---

**This methodology ensures proper semantic web architecture with SKOS as the stable conceptual foundation.** 🎯
