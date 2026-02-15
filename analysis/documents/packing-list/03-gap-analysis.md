# Packing List: Gap Analysis

## Summary

**Total Data Elements:** 22  
**Existing in KTDDE OWL:** 15 (68%)  
**Need Verification:** 5 (23%)  
**Missing / Need Proposal:** 2 (9%)

---

## ✅ Covered by Existing KTDDE OWL (15 elements)

These data elements map directly to existing KTDDE vocabulary:

| Data Element | KTDDE Property | Class | Notes |
|--------------|----------------|-------|-------|
| Packing List Number | `packingListNumber` | Identifier | Core document identifier |
| Issue Date/Time | `issueDateTime` | xsd:dateTime | Standard temporal property |
| Shipper (Name & Address) | `consignorParty` | Party | Via Party object composition |
| Consignee (Name & Address) | `consigneeParty` | Party | Via Party object composition |
| Number of Packages | `totalPackageCount` | Quantity | Package count aggregate |
| Package ID (SSCC) | `sscc` | Identifier | Serial Shipping Container Code |
| Gross Weight | `totalGrossWeight` | Quantity | Weight including packaging |
| Container Number | `containerNumber` | String | ISO 6346 container ID |
| Seal Number | `sealIdentifier` | Identifier | Security seal reference |
| Goods Description | `goodsDescription` | String | Textual description |
| HS Code | `commodityCode` | CommodityClassification | Harmonized System |
| Country of Origin | `originCountry` | Country | ISO 3166 country code |

**Action:** Use as-is in SHACL shape

---

## ⚠️ Needs Verification (5 elements)

These might exist but need confirmation of exact property names:

### 1. Document References

**Data Elements:**
- Transport Document Reference (UNTDED 1188)
- Invoice Reference (UNTDED 1334)

**Current Mapping:** `referencedDocument` (generic)

**Issue:**
- KTDDE has generic `referencedDocument` property
- Need to specify document type (TransportDocument vs CommercialInvoice)
- May need typed sub-properties

**Verification Needed:**
```bash
grep -A 5 "referencedDocument" ontology/ktdde-v0.0.5.rdf
# Check if there are typed variants like:
# - referencedTransportDocument
# - referencedInvoice
```

**Recommendation:**
- If typed properties exist → use them
- If not → use `referencedDocument` with `@type` annotation
- OR propose: `referencedTransportDocument`, `referencedInvoice`

---

### 2. Package Marks & Numbers

**Data Element:** Shipping Marks (UNTDED 7102)

**Possible Property:** `shippingMarks`

**Verification Needed:**
```bash
grep -i "shippingMarks\|packageMark" ontology/ktdde-v0.0.5.rdf
```

**Options:**
- If `shippingMarks` exists on Package class → use it
- If it's called something else (e.g., `marksAndNumbers`) → document
- If missing → propose new property

---

### 3. Total Volume

**Data Element:** Volume (UNTDED 6411)

**Possible Properties:**
- `totalCubeVolume`
- `totalVolume`
- `cubeVolume`

**Verification Needed:**
```bash
grep -i "volume\|cube" ontology/ktdde-v0.0.5.rdf | grep -i "total"
```

**Recommendation:**
- Use whatever KTDDE defines for total volumetric measurement
- Likely `totalCubeVolume` or similar

---

### 4. Dangerous Goods Indicator

**Data Element:** Dangerous Goods Flag (UNTDED 7124)

**Possible Properties:**
- `dangerousGoodsIndicator`
- `hasDangerousGoods`
- (might be in DangerousGoods class)

**Verification Needed:**
```bash
grep -i "dangerous" ontology/ktdde-v0.0.5.rdf
```

**Recommendation:**
- Boolean flag on GoodsItem or Package
- If missing → propose `dangerousGoodsIndicator`

---

## ❌ Missing Properties (2 elements - Need Proposals)

### 1. Package Type Code

**Data Element:** Package Type Code (UNTDED 7065)  
**Cardinality:** Mandatory  
**Example Values:** PAL (Pallet), BOX (Box), BDL (Bundle), CRT (Crate)

**Current Status:** ❌ Not found in KTDDE OWL

**Proposed Property:**
```turtle
ktddecv:packageTypeCode
  a owl:DatatypeProperty ;
  rdfs:label "package type code"@en ;
  rdfs:comment "UNTDED 7065 - Code specifying the type of package" ;
  rdfs:domain ktddecv:Package ;
  rdfs:range xsd:string ;  # Or reference to code list
  # Used in: PackingList, BillOfLading, Manifest, CustomsDeclaration
  .
```

**Justification:**
- UNTDED 7065 is a standard code list (UN/ECE Recommendation 21)
- Mandatory for packing list
- Generic - reusable across all documents with package information
- Essential for logistics and customs

**Alternative Names Considered:**
- `packageType` - too generic (could be description)
- `packagingTypeCode` - less common terminology
- **`packageTypeCode`** ✅ - matches UNTDED terminology

**Reusability:**
- Packing List (M)
- Bill of Lading (M)
- Cargo Manifest (M)
- Customs Declaration (M)
- Delivery Note (O)

---

### 2. Temperature Requirements

**Data Element:** Temperature Range (UNTDED 6245)  
**Cardinality:** Conditional (for temperature-controlled goods)  
**Example Values:** "-20°C to +5°C", "Frozen", "Refrigerated 2-8°C"

**Current Status:** ❌ Not found in KTDDE OWL

**Proposed Property:**
```turtle
ktddecv:temperatureRequirement
  a owl:DatatypeProperty ;
  rdfs:label "temperature requirement"@en ;
  rdfs:comment "UNTDED 6245 - Temperature control requirements for goods" ;
  rdfs:domain ktddecv:GoodsItem ;
  rdfs:range xsd:string ;  # Could be structured class with min/max
  # Used in: PackingList, BillOfLading, Manifest (conditional)
  .
```

**Justification:**
- Critical for perishable goods, pharmaceuticals, chemicals
- UNTDED 6245 is standard reference
- Conditional requirement (only when temperature control needed)
- Generic - applies to any temperature-sensitive shipment

**Alternative Approaches:**

**Option A: Simple String** (Proposed above)
```turtle
temperatureRequirement rdfs:range xsd:string
# Example: "-20°C to +5°C"
```

**Option B: Structured Object** (More complex but precise)
```turtle
ktddecv:temperatureRequirement
  rdfs:range ktddecv:TemperatureRange ;

ktddecv:TemperatureRange a owl:Class ;
  # Properties:
  # - minimumTemperature (xsd:decimal)
  # - maximumTemperature (xsd:decimal)
  # - temperatureUnit (C, F, K)
```

**Recommendation:** Start with Option A (string), evolve to Option B if needed

**Reusability:**
- Packing List (C)
- Bill of Lading (C)
- Cargo Manifest (C)
- Customs Declaration (O)
- Insurance Certificate (O - for valuation)

---

## Proposed New Property: Total Net Weight

**Data Element:** Net Weight (UNTDED 6292)  
**Cardinality:** Optional  
**Current Status:** ⚠️ `totalGrossWeight` exists, but `totalNetWeight` might be missing

**Search Needed:**
```bash
grep -i "netWeight\|net.*weight" ontology/ktdde-v0.0.5.rdf | grep -i total
```

**If missing, propose:**
```turtle
ktddecv:totalNetWeight
  a owl:ObjectProperty ;
  rdfs:label "total net weight"@en ;
  rdfs:comment "UNTDED 6292 - Total weight of goods excluding packaging" ;
  rdfs:domain ktddecv:PackingList ;  # Also other documents
  rdfs:range ktddecv:Quantity ;
  # Parallel to totalGrossWeight
  .
```

**Justification:**
- Net weight is critical for customs valuation
- Separate from gross weight (which includes packaging)
- Follows pattern of `totalGrossWeight` (if that exists)
- Standard UNTDED element

---

## Gap Priority Assessment

### High Priority (Must Have)

1. **packageTypeCode** - Mandatory element, no workaround
2. **totalNetWeight** - If missing, critical for customs

### Medium Priority (Should Have)

3. **Document reference clarification** - Can use generic property with type annotation
4. **shippingMarks** - Can use description field as workaround

### Low Priority (Nice to Have)

5. **temperatureRequirement** - Only for specific goods, conditional

---

## Recommended Actions

### Immediate (Before Creating SHACL)

1. ✅ **Verify existence** of these 5 properties:
   - `referencedDocument` (and typed variants)
   - `shippingMarks`
   - `totalCubeVolume` (or variant)
   - `dangerousGoodsIndicator`
   - `totalNetWeight`

2. ❌ **Propose new properties** for confirmed gaps:
   - `packageTypeCode` (if missing)
   - `temperatureRequirement` (if missing)

### Next Steps

1. **Search KTDDE OWL** systematically for verification items
2. **Document findings** in `04-proposals.ttl`
3. **Create SHACL shape** using confirmed properties
4. **Submit proposals** to Finnish Interoperability Platform
5. **Get community feedback** before finalizing

---

## Reusability Analysis

Properties proposed here should be usable in:

| Property | Also Used In |
|----------|--------------|
| `packageTypeCode` | Bill of Lading, Manifest, Customs Declaration, Delivery Note |
| `temperatureRequirement` | Bill of Lading, Manifest, Insurance Certificate |
| `totalNetWeight` | Commercial Invoice, Bill of Lading, Customs Declaration |

**Design Principle:** All proposed properties are generic enough to be reused across multiple trade documents, not specific to Packing List only.

---

## Next: Property Proposals

See `04-proposals.ttl` for formal OWL definitions of new properties.
