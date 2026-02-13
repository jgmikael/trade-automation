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
├── credentials/        # VC JSON-LD schemas and examples
├── contexts/           # JSON-LD context files
├── examples/           # Sample trade documents as VCs
├── validation/         # Schema validation tools
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

## EU Business Wallet

This project is designed to work with the upcoming EU Business Wallet (EU regulation proposal November 2025).

## License

(To be determined)

## Contact

Developed for production-ready trade automation solutions.
