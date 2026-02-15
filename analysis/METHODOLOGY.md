# KTDDE Data Element to OWL Mapping Methodology

## Purpose
Systematically map KTDDE data elements to OWL classes and properties, identifying gaps and proposing extensions while maintaining semantic consistency and maximum reusability.

## Process Overview

```
KTDDE Data Glossary (Excel)
        ↓
Extract Data Elements for Document
        ↓
Analyze Each Data Element
        ↓
Map to Existing KTDDE OWL
        ↓
Identify Gaps
        ↓
Propose New Properties (Generic & Reusable)
        ↓
Create SHACL Shape
        ↓
Validate & Document
```

---

## Step 1: Extract Data Elements

### Source: KTDDE Data Glossary
- URL: https://www.digitalizetrade.org/files/ktdde/DSI-KTDDE-data-glossary_20260108.xlsx
- Structure: Rows = data elements, Columns = documents
- Markers: M (Mandatory), O (Optional), C (Conditional)

### For Each Document, Extract:

| Column | Content |
|--------|---------|
| **Data Element Name** | Short name from glossary |
| **UID** | UNTDED/ISO 7372 code |
| **Description** | Definition from UNTDED |
| **Cardinality** | M (1), O (0..1), C (conditional) |
| **Data Type** | String, Date, Numeric, etc. |
| **Example Value** | Sample data |

---

## Step 2: Analyze KTDDE OWL Coverage

### Check Existing Vocabulary

For each data element:

1. **Search KTDDE OWL ontology:**
   ```bash
   grep -i "element_name" ontology/ktdde-v0.0.5.rdf
   ```

2. **Look for:**
   - Exact property match
   - Similar property (different name, same meaning)
   - Class that should have this property
   - Domain/range restrictions

3. **Document findings:**
   - ✅ **Exists:** Property name, IRI, definition
   - ⚠️ **Similar:** Close match, differences
   - ❌ **Missing:** No equivalent found

---

## Step 3: Gap Analysis

### Types of Gaps

#### 3.1 Property Exists ✅
- Use as-is
- Document mapping

#### 3.2 Close Match ⚠️
**Example:** 
- Data element: "Consignor Name"
- OWL has: `consignorParty` (returns Party object, not string)
- **Decision:** Use existing, access via `Party.name`

#### 3.3 Completely Missing ❌
- Propose new property
- Follow KTDDE naming conventions
- Ensure maximum reusability

---

## Step 4: Propose New Properties

### Design Principles

#### 4.1 **Generic Before Specific**

❌ **BAD (Too Specific):**
```turtle
ktddecv:packingListContainerNumber
ktddecv:billOfLadingContainerNumber
ktddecv:manifestContainerNumber
```

✅ **GOOD (Generic):**
```turtle
ktddecv:containerNumber
# Reusable across all transport documents
```

#### 4.2 **Separate Concerns**

❌ **BAD (Mixed Concepts):**
```turtle
ktddecv:exporterNameAndAddress
```

✅ **GOOD (Separated):**
```turtle
ktddecv:exporterParty  # Points to Party class
  Party.name
  Party.address
```

#### 4.3 **Use Existing Patterns**

Look at existing KTDDE properties:
```turtle
# Pattern: has + Object
ktddecv:hasPackage
ktddecv:hasShipment
ktddecv:hasGoodsItem

# Pattern: [verb] + Party
ktddecv:buyerParty
ktddecv:sellerParty
ktddecv:consignorParty

# Pattern: [adjective] + Property
ktddecv:totalGrossWeight
ktddecv:netQuantity
ktddecv:estimatedArrivalDate
```

#### 4.4 **Domain & Range**

Always specify:
```turtle
ktddecv:newProperty
  a owl:ObjectProperty ;
  rdfs:domain ktddecv:Document ;         # What has this property
  rdfs:range ktddecv:Identifier ;        # What type of value
  rdfs:label "new property"@en ;
  rdfs:comment "Description from UNTDED"@en .
```

---

## Step 5: Create Mapping Table

### Template Format

```markdown
| Data Element | UID | M/O/C | KTDDE OWL Property | Class | Data Type | Gap | Notes |
|--------------|-----|-------|-------------------|-------|-----------|-----|-------|
| Document ID | 1004 | M | packingListNumber | Identifier | string | ✅ | Exact match |
| Issue Date | 2379 | M | issueDateTime | xsd:dateTime | dateTime | ✅ | Exists |
| Shipper | 3132 | M | consignorParty | Party | Party | ✅ | Via Party object |
| Container# | 7140 | O | ❌ NEW | Identifier | string | ❌ | Propose: containerIdentifier |
```

### Gap Status Codes

- ✅ **Exists** - Direct match
- ⚠️ **Partial** - Close match, document path
- ❌ **Missing** - Propose new property
- 🔄 **Review** - Needs discussion

---

## Step 6: Propose OWL Extensions

### Format for New Properties

```turtle
@prefix ktddecv: <https://iri.suomi.fi/model/ktddecv/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

# New Property Proposal
ktddecv:containerIdentifier
  a owl:ObjectProperty ;
  rdfs:label "container identifier"@en ;
  rdfs:comment "UNTDED 7140 - Unique identification of a transport container" ;
  rdfs:domain ktddecv:TransportEquipment ;
  rdfs:range ktddecv:Identifier ;
  # Reusable in: PackingList, BillOfLading, Manifest, CustomsDeclaration
  .

# Usage in multiple documents
ktddecv:PackingList
  a owl:Class ;
  rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty ktddecv:containerIdentifier ;
    owl:minCardinality 0 ;  # Optional
  ] .

ktddecv:BillOfLading
  a owl:Class ;
  rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty ktddecv:containerIdentifier ;
    owl:minCardinality 1 ;  # Mandatory
  ] .
```

---

## Step 7: SHACL Shape Creation

### Convert Mapping to SHACL

```turtle
dsi:PackingListShape
  a sh:NodeShape ;
  sh:targetClass ktddecv:PackingList ;
  
  # Existing property (✅)
  sh:property [
    sh:path ktddecv:packingListNumber ;
    sh:class ktddecv:Identifier ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:name "Packing List Number"@en ;
    sh:description "UNTDED 1004 - Unique reference number"@en ;
  ] ;
  
  # New property (❌ → proposed)
  sh:property [
    sh:path ktddecv:containerIdentifier ;
    sh:class ktddecv:Identifier ;
    sh:minCount 0 ;  # Optional
    sh:name "Container Number"@en ;
    sh:description "UNTDED 7140 - Container identification"@en ;
  ] .
```

---

## Step 8: Validation & Documentation

### Validate Against:

1. **KTDDE OWL Ontology**
   - No conflicts with existing properties
   - Follows naming conventions
   - Proper domain/range

2. **UNTDED/ISO 7372**
   - Matches official definitions
   - Correct UID references

3. **Reusability Check**
   - Can be used in multiple documents?
   - Generic enough?
   - Not too specific to one use case?

4. **Completeness**
   - All mandatory data elements covered
   - Optional elements documented
   - Conditional logic specified

### Documentation Structure

```
analysis/
├── METHODOLOGY.md                    # This file
├── documents/
│   ├── packing-list/
│   │   ├── 01-data-elements.csv     # Extracted from KTDDE
│   │   ├── 02-owl-mapping.csv       # Mapping table
│   │   ├── 03-gap-analysis.md       # What's missing
│   │   ├── 04-proposals.ttl         # New properties in Turtle
│   │   └── 05-shacl-shape.ttl       # Final SHACL shape
│   ├── commercial-invoice/
│   └── ...
└── proposals/
    ├── new-properties.ttl           # All proposed properties
    └── rationale.md                 # Why each is needed
```

---

## Best Practices

### ✅ DO

1. **Start with one document** as a complete example
2. **Check existing properties first** - don't reinvent
3. **Propose generic properties** - max reusability
4. **Document everything** - why each decision was made
5. **Use UNTDED definitions** - don't make up descriptions
6. **Follow KTDDE patterns** - naming, structure
7. **Specify cardinality** - mandatory vs optional
8. **Add examples** - sample data for each property

### ❌ DON'T

1. **Don't guess** - verify against official sources
2. **Don't duplicate** - check for existing properties first
3. **Don't over-specify** - keep properties generic
4. **Don't ignore patterns** - follow KTDDE conventions
5. **Don't skip validation** - check against ontology
6. **Don't forget documentation** - explain all decisions

---

## Example: Full Analysis Workflow

### 1. Pick Document
**Packing List** (good example - medium complexity)

### 2. Extract Data Elements
From KTDDE Data Glossary Excel

### 3. Create Mapping Table
See `analysis/documents/packing-list/02-owl-mapping.csv`

### 4. Identify Gaps
List all ❌ missing properties

### 5. Propose Extensions
Write Turtle proposals in `proposals/new-properties.ttl`

### 6. Create SHACL Shape
Combine existing + proposed in proper SHACL

### 7. Document Rationale
Explain why each new property is needed

### 8. Validate
Check against KTDDE OWL, UNTDED, reusability

---

## Output Deliverables

### For Each Document:

1. **Data Elements List** (CSV)
   - All elements from KTDDE glossary
   - UID, description, cardinality

2. **Mapping Table** (CSV)
   - Element → OWL property mapping
   - Gap status (✅⚠️❌)

3. **Gap Analysis** (Markdown)
   - What's missing
   - Why it's needed
   - Reusability across documents

4. **Property Proposals** (Turtle)
   - New properties in OWL
   - Proper domain/range
   - Following KTDDE patterns

5. **SHACL Shape** (Turtle)
   - Complete shape with all properties
   - Cardinality constraints
   - UNTDED references

6. **Rationale Document** (Markdown)
   - Design decisions
   - Trade-offs
   - Alternatives considered

---

## Quality Criteria

A mapping is **production-ready** when:

- ✅ All mandatory data elements covered
- ✅ All properties map to KTDDE OWL or are proposed
- ✅ Proposed properties are generic & reusable
- ✅ SHACL validates against OWL ontology
- ✅ UNTDED codes referenced correctly
- ✅ Cardinality matches KTDDE glossary (M/O/C)
- ✅ Documentation explains all decisions
- ✅ Examples provided for each property

---

## Next Steps

1. **Create example for Packing List** (complete workflow)
2. **Review with KTDDE community** (get feedback)
3. **Apply to remaining documents** (systematic approach)
4. **Submit proposals** to Finnish Interoperability Platform
5. **Iterate based on feedback** (refine approach)

---

**This methodology ensures semantic correctness, standards compliance, and maximum reusability of OWL properties across all trade documents.**
