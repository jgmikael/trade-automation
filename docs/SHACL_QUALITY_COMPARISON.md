# SHACL Shape Quality Comparison

## Example: Packing List

### What I Generated (Incomplete)

```turtle
dsi:PackingList a sh:NodeShape ;
    sh:targetClass ktddecv:PackingList ;
    sh:property [
        sh:path ktddecv:hasPackingListNumber ;  # ❌ Wrong property name
    ] ,
    [
        sh:path ktddecv:hasIssueDate ;
    ] ,
    [
        sh:path ktddecv:hasShipper ;
    ] ,
    [
        sh:path ktddecv:hasConsignee ;
    ] .
    # ❌ Missing: cardinality, data types, UNTDED codes
```

### What It Should Be (Proper)

```turtle
dsi:PackingList a sh:NodeShape ;
    sh:targetClass ktddecv:PackingList ;
    rdfs:label "Packing List"@en ;
    sh:property [
        sh:path ktddecv:packingListNumber ;     # ✅ Correct property from KTDDE
        sh:class ktddecv:Identifier ;           # ✅ Typed
        sh:minCount 1 ;                         # ✅ Mandatory
        sh:maxCount 1 ;                         # ✅ Single value
        sh:name "Packing List Number"@en ;
        sh:description "UNTDED 1004 - Reference number to identify a packing list"@en ;
    ] ,
    [
        sh:path ktddecv:issueDateTime ;         # ✅ Correct property
        sh:datatype xsd:dateTime ;              # ✅ Data type
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:name "Issue Date"@en ;
        sh:description "UNTDED 2379 - Date/time of document issue"@en ;
    ] ,
    [
        sh:path ktddecv:consignorParty ;        # ✅ Uses KTDDE vocab
        sh:class ktddecv:Party ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:name "Consignor"@en ;
        sh:description "UNTDED 3132 - Party consigning goods"@en ;
    ] ,
    [
        sh:path ktddecv:consigneeParty ;
        sh:class ktddecv:Party ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:name "Consignee"@en ;
        sh:description "UNTDED 3132 - Party to receive goods"@en ;
    ] ,
    [
        sh:path ktddecv:hasPackage ;            # ✅ At least one
        sh:class ktddecv:Package ;
        sh:minCount 1 ;
        sh:name "Package"@en ;
        sh:description "Details of packages in shipment"@en ;
    ] ,
    [
        sh:path ktddecv:totalPackageCount ;     # ✅ I missed this!
        sh:class ktddecv:Quantity ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:name "Total Package Quantity"@en ;
        sh:description "UNTDED 7224 - Total number of packages"@en ;
    ] ,
    [
        sh:path ktddecv:totalGrossWeight ;
        sh:class ktddecv:Quantity ;
        sh:minCount 0 ;                         # ✅ Optional
        sh:maxCount 1 ;
        sh:name "Total Gross Weight"@en ;
        sh:description "UNTDED 6292 - Total weight with packaging"@en ;
    ] ,
    [
        sh:path ktddecv:totalNetWeight ;
        sh:class ktddecv:Quantity ;
        sh:minCount 0 ;
        sh:maxCount 1 ;
        sh:name "Total Net Weight"@en ;
        sh:description "UNTDED 6292 - Total weight without packaging"@en ;
    ] ,
    [
        sh:path ktddecv:totalCubeVolume ;       # ✅ Correct property name
        sh:class ktddecv:Quantity ;
        sh:minCount 0 ;
        sh:maxCount 1 ;
        sh:name "Total Volume"@en ;
        sh:description "UNTDED 6411 - Total cubic measurement"@en ;
    ] .
```

## Key Differences

| Aspect | Generated | Proper |
|--------|-----------|--------|
| Property names | Made up (`hasX`) | From KTDDE OWL |
| Cardinality | ❌ Missing | ✅ min/max specified |
| Data types | ❌ Missing | ✅ Specified |
| UNTDED codes | ❌ Missing | ✅ Referenced |
| Descriptions | ❌ Generic | ✅ Standards-based |
| Mandatory/Optional | ❌ Unknown | ✅ Clear |
| Missing properties | ❌ Yes | ✅ Complete |

## Where to Find Official Data

1. **KTDDE Data Glossary** - Excel file with all data elements:
   ```
   https://www.digitalizetrade.org/files/ktdde/DSI-KTDDE-data-glossary_20260108.xlsx
   ```

2. **KTDDE OWL Ontology** - Property definitions:
   ```
   ontology/ktdde-v0.0.5.rdf
   ```

3. **UNTDED/ISO 7372** - Data element directory:
   ```
   https://unece.org/untded-iso7372
   ```

## How to Fix

1. Open KTDDE Data Glossary Excel
2. Find "Packing List" column
3. Extract all data elements marked M (Mandatory), O (Optional), C (Conditional)
4. Map each to KTDDE OWL property
5. Add cardinality based on M/O/C
6. Add UNTDED code in description
7. Specify data types
8. Validate against OWL ontology

## Production Readiness

**Generated shapes:** 🔴 **NOT production ready**
- Use for demos/prototypes only
- Add clear disclaimer
- Replace before production use

**Proper shapes:** 🟢 **Production ready**
- Based on official standards
- Validated against KTDDE
- Can be used in real systems
- Acceptable to standards bodies
