# KTDDE Vocabulary Overview

**Version:** 0.0.5  
**Source:** https://tietomallit.suomi.fi/  
**Namespace:** `https://iri.suomi.fi/model/ktddecv/`

## Purpose

KTDDE (Kansainvälisen Kaupan Digitaaliset Dokumentit Elektronisesti / International Trade Digital Documents Electronically) is a Finnish-developed OWL vocabulary for representing international trade documents semantically.

## Document Classes

The vocabulary defines **98 classes** covering all major trade documents:

### Core Trade Documents
- **CommercialInvoice** - Commercial invoice for goods
- **BillOfLading** - Maritime transport document
- **AirWaybill** - Air cargo transport document
- **SeaWaybill** - Sea transport waybill
- **CertificateOfOrigin** - Origin certification
- **PackingList** - Goods packing details
- **DeliveryNote** - Delivery confirmation

### Transport Documents
- **AirCargoManifest** - Air cargo manifest
- **SeaCargoManifest** - Sea cargo manifest
- **RailConsignmentNoteCIM** - Rail transport (CIM)
- **RoadConsignmentNoteCMR** - Road transport (CMR)
- **TransportDocument** - Generic transport doc

### Financial Documents
- **DocumentaryCredit** - Letter of credit
- **BillOfExchange** - Payment instrument
- **PromissoryNote** - Payment promise
- **PaymentConfirmation** - Payment proof
- **PaymentTerms** - Payment conditions

### Regulatory Documents
- **CustomsDeclaration** - Customs import/export declaration
- **ExportImportLicense** - Trade license
- **PhytosanitaryCertificate** - Plant health certificate
- **VeterinaryCertificate** - Animal health certificate
- **CITESPermit** - Endangered species permit
- **CODEXOfficialCertificate** - Food standards certificate
- **OrganicInspectionCertificate** - Organic certification

### Specialized Documents
- **ATACarnet** - Temporary admission document
- **TIRCarnet** - International road transport
- **CustomsBond** - Customs guarantee
- **InsuranceCertificate** - Cargo insurance
- **WarehouseReceipt** - Warehouse storage proof

### Supporting Entities
- **Party** - Organizations and persons
- **Location** - Physical addresses and places
- **Consignment** - Shipment grouping
- **TradeItem** - Product/goods
- **TransportMeans** - Vehicles, vessels, aircraft
- **MonetaryAmount** - Financial values
- **Quantity** - Measurements
- **Package** - Packaging units

## Standards Integration

The vocabulary imports and integrates:
- **GS1** - Global standards for supply chain
- **UN/CEFACT** - UN trade facilitation
- **SKOS** - W3C taxonomies
- **Dublin Core** - Metadata terms
- **SHACL** - Data validation

## Use Cases

1. **Digital Trade Documentation** - Replace paper documents with verifiable digital versions
2. **Cross-border Trade** - Standardized data for customs, logistics, banking
3. **Supply Chain Visibility** - Track goods through entire trade lifecycle
4. **Regulatory Compliance** - Automated validation against trade rules
5. **EU Business Wallet Integration** - Verifiable credentials for trade actors

## Next Steps

1. Map KTDDE classes to W3C Verifiable Credential schemas
2. Create JSON-LD contexts for each document type
3. Define credential subject structures
4. Implement validation logic
5. Build example credentials for common trade scenarios
