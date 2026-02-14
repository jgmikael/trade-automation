# International Trade Automation with W3C Verifiable Credentials

A comprehensive demonstration of digitized international trade using **W3C Verifiable Credentials** based on the **KTDDE (Key Trade Documents and Data Elements)** vocabulary from Finland's national data models.

🌐 **Demonstration**: Finnish Gluelam Timber Export to Japan  
📊 **Documents**: 15 core trade documents (36 total available)  
🏛️ **Standards**: KTDDE OWL, W3C VC 1.1, SHACL, JSON-LD  
🎯 **Target Audiences**: EU, Japan, Singapore (ICC DSI), Global Trade Organizations

---

## 🎯 Project Goals

- **Demonstrate** end-to-end digital trade document exchange
- **Showcase** W3C Semantic Web stack (RDF, OWL, SHACL, JSON-LD)
- **Prove** production-readiness for EU Business Wallet
- **Enable** interoperability across jurisdictions
- **Standardize** on KTDDE vocabulary from Finnish authorities

---

## 📦 What's Included

### 1. **SHACL Profiles** (36 documents)

Document shapes defining structure and validation rules:

- `shacl/*.jsonld` - 36 SHACL application profiles

**Core Trade Documents (5):**
- Purchase Order
- Commercial Invoice
- Bill of Lading
- Certificate of Origin
- Documentary Credit (Letter of Credit)

**Additional Documents (31):**
- Packing List, Insurance Certificate, Phytosanitary Certificate
- Customs Declarations (Export/Import), Delivery Note
- Sea Waybill, Cargo Manifest, Payment Confirmation
- Regulatory Certificates, Warehouse Receipt
- And 21 more specialized documents...

### 2. **JSON-LD Contexts** (82 files)

Semantic mappings from SHACL to JSON-LD:

- `contexts/*.jsonld` - 82 JSON-LD context files
- Maps document classes and properties to IRIs
- Enables semantic interoperability

### 3. **JSON Schemas** (82 files)

Validation schemas for JSON documents:

- `credentials/*.json` - 82 JSON Schema files
- Ensures data structure compliance
- Ready for automated validation

### 4. **W3C VC Templates** (44 per document)

Credential templates for issuers:

- `templates/empty/*.json` - Empty templates with placeholders
- `templates/examples/*.json` - Example credentials with sample data

### 5. **SAP Simulator**

Mock SAP ERP API for trade data:

- `sap-simulator/` - Complete SAP MM/SD simulation
- Realistic data structures (EKKO, VBAK, LIKP, VBRK)
- Dual API mode: SAP format + W3C VCs
- Flask REST API on port 5000

### 6. **Browser Demo**

Interactive visualization of document flow:

- `demo/index.html` - Modern responsive UI
- `demo/demo.js` - Document data and logic
- **15 documents** for gluelam timber trade
- **7 actor views**: Buyer, Seller, Bank, Carrier, Customs, Chamber, Certifier
- **16 timeline events** from order to delivery
- Zero dependencies, runs in any browser

---

## 🚀 Quick Start

### View the Demo

```bash
cd demo
python3 -m http.server 8080
# Open: http://localhost:8080
```

**Or just open `demo/index.html` directly in your browser!**

### Run SAP Simulator

```bash
cd sap-simulator
pip3 install flask
python3 api/sap_api.py
# API available at: http://localhost:5000
```

### Generate New Documents

```bash
# Create SHACL profiles
python3 tools/generate_missing_shacl.py

# Convert to W3C VC contexts and schemas
for f in shacl/*.jsonld; do
    python3 tools/shacl-to-vc-converter.py "$f" .
done

# Generate templates
python3 tools/generate_vc_templates.py credentials/commercialinvoice-schema.json

# Update demo
python3 tools/generate_demo.py
```

---

## 📋 Trade Scenario: Finnish Gluelam Timber to Japan

**Real-world construction materials export**

| **Aspect** | **Details** |
|------------|-------------|
| **Exporter** | Nordic Timber Oy, Kuhmo, Finland 🇫🇮 |
| **Importer** | Tokyo Construction Materials Ltd, Japan 🇯🇵 |
| **Product** | Engineered Gluelam Timber Beams (GL30c, GL32h) |
| **Quantity** | 160 pieces (120× GL30c + 40× GL32h) |
| **Value** | EUR 339,000 (including freight) |
| **Weight** | 28,800 kg (8 timber bundles) |
| **Volume** | 156 cubic meters |
| **Incoterms** | CFR (Cost and Freight) Tokyo Port |
| **Payment** | Confirmed Irrevocable Letter of Credit (60 days) |
| **Route** | Rauma Port, Finland → Tokyo Port, Japan (~45 days) |
| **Carrier** | FESCO (Far Eastern Shipping Company) |
| **Special** | ISPM-15 fumigation, CE marking (EN 14080:2013) |

### Why This Scenario?

- ✅ **Real-world complexity** - Timber requires phytosanitary certificates
- ✅ **EU-Japan EPA** - Zero duty under trade agreement
- ✅ **Structural certification** - CE marking for engineered timber
- ✅ **Multi-party** - 7 actors involved in document exchange
- ✅ **Regulatory** - Customs, phytosanitary, quality certificates
- ✅ **Financial** - Letter of Credit with document collection

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│           KTDDE OWL Vocabulary (98 classes)             │
│         Finnish Digital Authority Core Model            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              SHACL Application Profiles                  │
│         36 Document Shapes (trade-specific)             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         W3C Verifiable Credentials Format               │
│   JSON-LD Contexts (82) + JSON Schemas (82)            │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴──────────┬────────────────┐
         ▼                      ▼                ▼
┌─────────────────┐   ┌──────────────────┐   ┌─────────────────┐
│  SAP Simulator  │   │  Browser Demo    │   │   Templates     │
│  (Backend API)  │   │ (Visualization)  │   │ (Issuers)      │
└─────────────────┘   └──────────────────┘   └─────────────────┘
```

---

## 🎨 Demo Features

### 7 Actor Views

1. **🏢 Buyer** (Tokyo Construction Materials)  
   Views: PO, L/C, B/L, Invoice, CoO, Packing List, Insurance, Import Customs, Delivery, Payment

2. **🏭 Seller** (Nordic Timber Oy)  
   Creates: Invoice, Ships cargo  
   Views: All 15 documents

3. **🏦 Bank** (MUFG Tokyo / Nordea Finland)  
   Issues: Letter of Credit  
   Views: Trade documents for L/C compliance

4. **🚢 Carrier** (FESCO)  
   Issues: Bill of Lading, Manifest  
   Views: Shipping documents

5. **🛃 Customs** (Finnish & Japanese)  
   Reviews: Import/Export declarations, certificates

6. **📜 Chamber of Commerce** (Finland)  
   Issues: Certificate of Origin

7. **✅ Certifier** (TÜV SÜD & Food Authority)  
   Issues: CE Marking, Phytosanitary Certificate

### Timeline View

16 chronological events from T-45 days to delivery:
- Purchase Order → L/C Opening → Certifications → Shipping → Customs → Payment → Delivery

### Document Cards

Click any document to view full SHACL-based JSON structure with syntax highlighting.

---

## 📚 Standards & Compliance

### W3C Standards

- **Verifiable Credentials 1.1** - Credential data model
- **JSON-LD 1.1** - Semantic linking
- **RDF/OWL** - Ontology representation
- **SHACL** - Shape validation

### Trade Standards

- **KTDDE** - Finnish national trade vocabulary
- **UN/CEFACT** - Business semantic library (BSP)
- **ISO standards** - Country codes, currency codes
- **Incoterms 2020** - Trade terms
- **SWIFT** - Banking identifiers

### Regulatory

- **ISPM-15** - Wood packaging treatment
- **EN 14080:2013** - Structural timber (Eurocode 5)
- **EU-Japan EPA** - Preferential trade treatment
- **Phytosanitary** - Plant health certificates

---

## 🛠️ Tools

All tools are **zero-dependency Python scripts** (stdlib only):

### `tools/shacl-to-vc-converter.py`

Converts SHACL profiles to W3C VC contexts and JSON schemas.

```bash
python3 tools/shacl-to-vc-converter.py shacl/commercial-invoice-v0.0.2.jsonld .
```

Output:
- `contexts/commercialinvoice-context.jsonld`
- `credentials/commercialinvoice-schema.json`

### `tools/generate_vc_templates.py`

Generates empty and example credential templates.

```bash
python3 tools/generate_vc_templates.py credentials/commercialinvoice-schema.json
```

Output:
- `templates/empty/commercialinvoice-empty.json`
- `templates/examples/commercialinvoice-example.json`

### `tools/generate_missing_shacl.py`

Generates 31 additional SHACL profiles from KTDDE classes.

```bash
python3 tools/generate_missing_shacl.py
```

Output: 31 new SHACL files in `shacl/`

### `tools/generate_demo.py`

Generates `demo/demo.js` from Python scenario data.

```bash
python3 tools/generate_demo.py
```

---

## 🔍 Validation Pipeline

```
Document JSON
     ↓
JSON Schema Validation (structure)
     ↓
SHACL Validation (semantics)
     ↓
Business Rules (custom logic)
     ↓
✅ Valid Credential
```

---

## 🌍 Use Cases

### For EU

- EU Business Wallet readiness demo
- Finnish KTDDE standardization showcase
- Cross-border digital trade within EU
- Export to Japan under EPA

### For Japan

- Tokyo-based importer example
- Japanese customs workflow
- MUFG Bank involvement
- Import under EU-Japan EPA

### For Singapore (ICC DSI)

- Digital Standards Initiative alignment
- Bill of Lading digitalization
- Letter of Credit automation
- Multi-jurisdiction compliance

### For Global

- Interoperable semantic standards
- Cross-border paperless trade
- Multi-party document exchange
- Real-world implementation example

---

## 📂 Repository Structure

```
trade-automation/
├── shacl/                      # 36 SHACL application profiles
├── contexts/                   # 82 JSON-LD context files
├── credentials/                # 82 JSON Schema files
├── templates/
│   ├── empty/                  # Empty VC templates
│   └── examples/               # Example VCs with data
├── sap-simulator/              # Mock SAP ERP API
│   ├── models/                 # SAP data structures
│   ├── data/                   # Sample SAP data
│   ├── mappings/               # SAP→KTDDE mappings
│   └── api/                    # Flask REST API
├── demo/                       # Browser-based demo
│   ├── index.html              # UI
│   └── demo.js                 # Document data & logic
├── tools/                      # Conversion & generation scripts
├── ontology/                   # KTDDE OWL vocabulary
├── scenario_gluelam_timber.py  # Original 5-doc scenario
└── scenario_gluelam_timber_full.py  # Complete 15-doc scenario
```

---

## 🔮 Future Enhancements

- [ ] **Digital Signatures** - JWS/JAdES signing of VCs
- [ ] **Issuer/Verifier Services** - API endpoints for issuance and verification
- [ ] **DID Integration** - Decentralized identifiers for parties
- [ ] **Selective Disclosure** - Zero-knowledge proof support
- [ ] **Status Registry** - Revocation and suspension
- [ ] **Multi-language** - Finnish, Japanese, Chinese translations
- [ ] **Mobile App** - Native iOS/Android viewer
- [ ] **Blockchain Anchoring** - Immutable audit trail
- [ ] **Real SAP Integration** - Live ERP connection
- [ ] **eFTI Compliance** - European electronic freight transport information

---

## 🤝 Contributing

This is a demonstration project for standards bodies and government agencies. For questions or collaboration:

- **Repository**: https://github.com/jgmikael/trade-automation
- **Standards**: KTDDE - https://tietomallit.suomi.fi/
- **Contact**: Mikael (jgmikael@github)

---

## 📄 License

[To be determined - likely MIT or Apache 2.0 for maximum reusability]

---

## 🙏 Acknowledgments

- **Finnish Digital and Population Data Services Agency** - KTDDE OWL vocabulary
- **W3C** - Verifiable Credentials, JSON-LD, SHACL standards
- **UN/CEFACT** - Business semantic library
- **ICC DSI** - Digital Standards Initiative
- **EU Commission** - EU Business Wallet initiative

---

## 📊 Project Statistics

- **36** SHACL document profiles
- **82** JSON-LD contexts
- **82** JSON Schemas
- **15** documents in demo scenario
- **7** actor perspectives
- **16** timeline events
- **2** API modes (SAP + W3C VC)
- **0** external dependencies (pure stdlib)
- **100%** semantic interoperability

---

**Built with ❤️ for global trade digitalization**

🌐 EU 🤝 Japan 🤝 Singapore 🤝 World
