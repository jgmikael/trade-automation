# International Trade Automation

Automating international trade document workflows using W3C Verifiable Credentials and semantic web technologies.

## Overview

This project aims to digitize and automate traditional paper-based international trade processes by:

- Modeling trade documents (KTDDE) using W3C Semantic Web standards
- Representing trade documents as W3C Verifiable Credentials
- Enabling interoperable, machine-readable trade data exchange
- Supporting EU Business Wallet integration

## Technology Stack

- **W3C Semantic Web Stack** - RDF, OWL, RDFS
- **JSON-LD** - JSON-based linked data representation
- **W3C Verifiable Credentials** - Standardized digital credential format
- **OWL Vocabulary** - Custom ontology for KTDDE trade documents

## Repository Structure

```
├── ontology/           # OWL vocabulary definitions
├── credentials/        # VC JSON-LD schemas (51 files)
├── contexts/           # JSON-LD context files (51 files)
├── shacl/             # Source SHACL profiles (5 files)
├── examples/           # Sample trade documents as VCs
├── tools/             # SHACL to VC converter tool
├── sap-simulator/     # SAP ERP API simulator with VC mapping
└── docs/              # Documentation
```

## KTDDE Trade Documents

KTDDE (to be documented) covers key international trade documents including:

- Commercial Invoice
- Bill of Lading
- Certificate of Origin
- Packing List
- (additional documents to be specified)

## Status

✅ **COMPLETE - All 5 Core Documents Implemented**

**Completed:**
- ✅ Bill of Lading (17 types, 40 properties)
- ✅ Certificate of Origin (14 types, 23 properties)
- ✅ Commercial Invoice (22 types, 28 properties)
- ✅ Documentary Credit / Letter of Credit (29 types, 51 properties)
- ✅ Purchase Order (12 types, 12 properties)

**Deliverables:**
- 5 SHACL application profiles processed (683KB total)
- 54+ unique semantic types defined
- 51 JSON-LD contexts generated
- 51 JSON Schemas for validation
- SHACL to W3C VC converter tool (Python 3)
- Full KTDDE v0.0.5 vocabulary (98 classes)

See [IMPLEMENTATION-SUMMARY.md](IMPLEMENTATION-SUMMARY.md) for complete details.

## SAP API Simulator

**NEW:** Complete SAP ERP simulation with W3C VC conversion!

**Location:** `/sap-simulator/`

**Features:**
- Simulates SAP MM & SD modules (Purchase Orders, Sales Orders, Deliveries, Invoices)
- Realistic international trade scenarios (EU ↔ Singapore, EU ↔ Japan)
- Dual API: Traditional SAP OData format + W3C VC format
- Real company data, products, HS codes, Incoterms
- Mapping engine: SAP → KTDDE W3C VCs
- Flask REST API with full documentation

**Quick Start:**
```bash
cd sap-simulator
pip install -r requirements.txt
python3 api/sap_api.py
# API runs on http://localhost:5000
```

**Demo:**
```bash
# Get all scenarios
curl http://localhost:5000/sap/opu/odata/sap/api/v1/scenarios

# Get W3C VCs for EU → Singapore scenario
curl http://localhost:5000/vc/api/v1/scenarios/EU_TO_SINGAPORE_MACHINERY_EXPORT/verifiable-credentials
```

See [sap-simulator/README.md](sap-simulator/README.md) for full documentation.

## 🎭 Browser Demo

**NEW:** Interactive trade document demo!

**Location:** `/demo/`

**Scenario:** Finnish gluelam timber export to Japan
- **Exporter:** Nordic Timber Oy (Finland) 🇫🇮
- **Importer:** Tokyo Construction Materials (Japan) 🇯🇵
- **Product:** Engineered gluelam timber beams (EUR 339,000)
- **Documents:** Purchase Order, L/C, Bill of Lading, Invoice, Certificate of Origin

**Features:**
- 📱 Interactive browser-based UI
- 👥 Multiple actor perspectives (Buyer, Seller, Bank, Carrier, Customs, Chamber)
- ⏱️ Timeline view of document flow
- 📄 KTDDE SHACL-based JSON documents
- ✨ Zero dependencies, no backend required

**Quick Start:**
```bash
cd demo
open index.html
# or serve with: python3 -m http.server 8080
```

Perfect for demonstrating to EU, Japan, Singapore, and global audiences!

See [demo/README.md](demo/README.md) for full details.

## EU Business Wallet

This project is designed to work with the upcoming EU Business Wallet (EU regulation proposal November 2025).

## License

(To be determined)

## Contact

Developed for production-ready trade automation solutions.
