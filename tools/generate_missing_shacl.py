#!/usr/bin/env python3
"""
Generate 31 missing SHACL profiles for KTDDE documents
Based on the KTDDE OWL vocabulary classes
"""

import json
from datetime import datetime
from typing import List, Dict, Any

# Document types to generate (31 most relevant for gluelam timber trade)
DOCUMENTS_TO_GENERATE = [
    {
        "name": "PackingList",
        "label": "Packing List",
        "description": "Document specifying the details of packed goods",
        "properties": ["packingListNumber", "issueDate", "shipper", "consignee", "goodsItem", "package", "totalGrossWeight", "totalNetWeight", "totalVolume"]
    },
    {
        "name": "InsuranceCertificate",
        "label": "Insurance Certificate",
        "description": "Certificate of insurance coverage for goods in transit",
        "properties": ["certificateNumber", "issueDate", "insurer", "insured", "policyNumber", "insuredAmount", "goodsDescription", "transportDetails"]
    },
    {
        "name": "PhytosanitaryCertificate",
        "label": "Phytosanitary Certificate",
        "description": "Certificate that plants/wood products are free from pests and diseases",
        "properties": ["certificateNumber", "issueDate", "issuingAuthority", "exporter", "consignee", "placeOfOrigin", "meansOfConveyance", "pointOfEntry", "treatment"]
    },
    {
        "name": "DeliveryNote",
        "label": "Delivery Note",
        "description": "Document accompanying goods delivery",
        "properties": ["deliveryNoteNumber", "deliveryDate", "supplier", "recipient", "deliveryAddress", "deliveryNoteLine", "carrierParty"]
    },
    {
        "name": "WarehouseReceipt",
        "label": "Warehouse Receipt",
        "description": "Receipt for goods stored in a warehouse",
        "properties": ["receiptNumber", "issueDate", "warehouse", "depositor", "goodsDescription", "quantity", "storageLocation"]
    },
    {
        "name": "SeaWaybill",
        "label": "Sea Waybill",
        "description": "Non-negotiable transport document for sea cargo",
        "properties": ["waybillNumber", "issueDate", "carrier", "shipper", "consignee", "portOfLoading", "portOfDischarge", "goodsItem", "freightAmount"]
    },
    {
        "name": "CustomsDeclaration",
        "label": "Customs Declaration",
        "description": "Declaration of goods for customs clearance",
        "properties": ["declarationNumber", "declarationType", "declarationDate", "declarant", "exporter", "importer", "customsOffice", "goodsItem", "totalInvoiceAmount"]
    },
    {
        "name": "PaymentConfirmation",
        "label": "Payment Confirmation",
        "description": "Confirmation of payment transaction",
        "properties": ["confirmationNumber", "paymentDate", "payer", "payee", "paymentAmount", "paymentMethod", "referenceDocument"]
    },
    {
        "name": "SeaCargoManifest",
        "label": "Sea Cargo Manifest",
        "description": "List of cargo carried by sea vessel",
        "properties": ["manifestNumber", "issueDate", "vessel", "voyage", "portOfLoading", "portOfDischarge", "carrierParty", "consignment"]
    },
    {
        "name": "ExportImportLicense",
        "label": "Export Import License",
        "description": "License permitting export or import of goods",
        "properties": ["licenseNumber", "issueDate", "expiryDate", "issuingAuthority", "licensee", "goodsDescription", "quantity", "value", "destinationCountry"]
    },
    {
        "name": "ShipsDeliveryOrder",
        "label": "Ships Delivery Order",
        "description": "Order to release cargo from vessel",
        "properties": ["orderNumber", "issueDate", "carrier", "consignee", "vessel", "goodsDescription", "releaseLocation"]
    },
    {
        "name": "DangerousGoodsDeclaration",
        "label": "Dangerous Goods Declaration",
        "description": "Declaration for transport of dangerous goods",
        "properties": ["declarationNumber", "issueDate", "shipper", "carrier", "dangerousGoods", "unNumber", "properShippingName", "hazardClass", "packingGroup"]
    },
    {
        "name": "BillOfExchange",
        "label": "Bill of Exchange",
        "description": "Negotiable payment instrument",
        "properties": ["billNumber", "issueDate", "drawer", "drawee", "payee", "amount", "tenor", "placeOfPayment"]
    },
    {
        "name": "PromissoryNote",
        "label": "Promissory Note",
        "description": "Written promise to pay a specific amount",
        "properties": ["noteNumber", "issueDate", "maker", "payee", "amount", "maturityDate", "interestRate"]
    },
    {
        "name": "RegulatoryCertificate",
        "label": "Regulatory Certificate",
        "description": "Certificate of compliance with regulations",
        "properties": ["certificateNumber", "issueDate", "issuingAuthority", "applicant", "productDescription", "standard", "testResults"]
    },
    {
        "name": "TransitAccompanyingDocument",
        "label": "Transit Accompanying Document",
        "description": "Document for goods in customs transit",
        "properties": ["documentNumber", "issueDate", "declarant", "officeOfDeparture", "officeOfDestination", "goodsItem", "guarantee"]
    },
    {
        "name": "CustomsBond",
        "label": "Customs Bond",
        "description": "Financial guarantee for customs duties",
        "properties": ["bondNumber", "issueDate", "principal", "surety", "customsAuthority", "bondAmount", "validityPeriod"]
    },
    {
        "name": "ConsignmentSecurityDeclaration",
        "label": "Consignment Security Declaration",
        "description": "Security information for consignment",
        "properties": ["declarationNumber", "issueDate", "declarant", "consignment", "securityMeasures", "screeningMethod"]
    },
    {
        "name": "RoadConsignmentNoteCMR",
        "label": "Road Consignment Note CMR",
        "description": "CMR convention road transport document",
        "properties": ["cmrNumber", "issueDate", "sender", "carrier", "consignee", "placeOfLoading", "placeOfDelivery", "goodsDescription", "freightCharges"]
    },
    {
        "name": "RailConsignmentNoteCIM",
        "label": "Rail Consignment Note CIM",
        "description": "CIM convention rail transport document",
        "properties": ["cimNumber", "issueDate", "sender", "carrier", "consignee", "stationOfDeparture", "stationOfDestination", "goodsDescription", "freightCharges"]
    },
    {
        "name": "AirWaybill",
        "label": "Air Waybill",
        "description": "Transport document for air cargo",
        "properties": ["awbNumber", "issueDate", "carrier", "shipper", "consignee", "airportOfDeparture", "airportOfDestination", "goodsItem", "chargeableWeight", "freightAmount"]
    },
    {
        "name": "ATACarnet",
        "label": "ATA Carnet",
        "description": "Temporary admission document for goods",
        "properties": ["carnetNumber", "issueDate", "validityDate", "holderName", "issuingCountry", "goodsList", "intendedUse"]
    },
    {
        "name": "TIRCarnet",
        "label": "TIR Carnet",
        "description": "International road transport document",
        "properties": ["tirNumber", "issueDate", "expiryDate", "holder", "vehicleRegistration", "customsOfficeOfDeparture", "customsOfficeOfDestination", "goodsDescription"]
    },
    {
        "name": "AirCargoManifest",
        "label": "Air Cargo Manifest",
        "description": "List of cargo carried by aircraft",
        "properties": ["manifestNumber", "issueDate", "flight", "aircraft", "airportOfDeparture", "airportOfDestination", "carrier", "consignment"]
    },
    {
        "name": "EMCSDocument",
        "label": "EMCS Document",
        "description": "Excise Movement and Control System document",
        "properties": ["arcNumber", "issueDate", "consignor", "consignee", "placeOfDispatch", "placeOfDelivery", "exciseProduct", "quantity", "dutyAmount"]
    },
    {
        "name": "ExciseGuarantee",
        "label": "Excise Guarantee",
        "description": "Guarantee for excise duty payment",
        "properties": ["guaranteeNumber", "issueDate", "guarantor", "beneficiary", "guaranteeAmount", "validityPeriod", "coverageType"]
    },
    {
        "name": "AdvanceRulingApplication",
        "label": "Advance Ruling Application",
        "description": "Application for advance customs ruling",
        "properties": ["applicationNumber", "applicationDate", "applicant", "customsAuthority", "subject", "goodsDescription", "requestedRuling"]
    },
    {
        "name": "CODEXOfficialCertificate",
        "label": "CODEX Official Certificate",
        "description": "Official certificate for food products (Codex Alimentarius)",
        "properties": ["certificateNumber", "issueDate", "issuingAuthority", "exporter", "consignee", "productDescription", "certificationStatement"]
    },
    {
        "name": "VeterinaryCertificate",
        "label": "Veterinary Certificate",
        "description": "Certificate for animal products and health",
        "properties": ["certificateNumber", "issueDate", "issuingAuthority", "exporter", "consignee", "animalProducts", "healthDeclaration", "inspectionDetails"]
    },
    {
        "name": "OrganicInspectionCertificate",
        "label": "Organic Inspection Certificate",
        "description": "Certificate for organic products",
        "properties": ["certificateNumber", "issueDate", "certificationBody", "operator", "productDescription", "organicStandard", "inspectionDate"]
    },
    {
        "name": "CITESPermit",
        "label": "CITES Permit",
        "description": "Permit for trade in endangered species",
        "properties": ["permitNumber", "issueDate", "expiryDate", "issuingAuthority", "exporter", "importer", "species", "quantity", "purpose"]
    }
]

def create_shacl_document(doc_info: Dict[str, Any]) -> Dict[str, Any]:
    """Create a SHACL profile for a document type"""
    
    name = doc_info["name"]
    label = doc_info["label"]
    description = doc_info["description"]
    properties = doc_info["properties"]
    
    namespace = f"dsi{name.lower()}"
    version = "0.0.1"
    timestamp = datetime.utcnow().isoformat() + "Z"
    creator_uuid = "5dc030a4-740f-4dde-9548-4e6e797899d8"
    
    # Start building the SHACL graph
    graph = []
    
    # Add ontology metadata
    ontology = {
        "@id": f"https://iri.suomi.fi/model/{namespace}/",
        "@type": ["suomi-meta:ApplicationProfile", "owl:Ontology"],
        "rdfs:label": {"@language": "en", "@value": f"DSI KTDDE {label}"},
        "dcterms:identifier": f"{len(graph)}-{name.lower()}",
        "dcterms:language": "en",
        "dcterms:created": {"@value": timestamp, "@type": "xsd:dateTime"},
        "dcterms:modified": {"@value": timestamp, "@type": "xsd:dateTime"},
        "suomi-meta:contentModified": {"@value": timestamp, "@type": "xsd:dateTime"},
        "suomi-meta:creator": creator_uuid,
        "suomi-meta:modifier": creator_uuid,
        "suomi-meta:publicationStatus": {
            "@id": "http://uri.suomi.fi/codelist/interoperabilityplatform/interoperabilityplatform_status/code/SUGGESTED"
        },
        "suomi-meta:contact": "yhteentoimivuus@dvv.fi",
        "owl:versionInfo": version,
        "owl:versionIRI": {"@id": f"{namespace}:{version}/"},
        "dcap:preferredXMLNamespace": f"https://iri.suomi.fi/model/{namespace}/",
        "dcap:preferredXMLNamespacePrefix": namespace,
        "dcterms:requires": {"@id": "https://iri.suomi.fi/model/ktddecv/0.0.1/"},
        "dcterms:isPartOf": [
            {"@id": "http://urn.fi/URN:NBN:fi:au:ptvl:v1105"},
            {"@id": "http://urn.fi/URN:NBN:fi:au:ptvl:v1132"},
            {"@id": "http://urn.fi/URN:NBN:fi:au:ptvl:v1142"}
        ]
    }
    graph.append(ontology)
    
    # Add main document class shape
    document_shape = {
        "@id": f"{namespace}:{name}",
        "@type": ["owl:Class", "sh:NodeShape"],
        "rdfs:label": {"@language": "en", "@value": label},
        "dcterms:description": {"@language": "en", "@value": description},
        "dcterms:identifier": {"@value": name, "@type": "xsd:NCName"},
        "dcterms:created": {"@value": timestamp, "@type": "xsd:dateTime"},
        "dcterms:modified": {"@value": timestamp, "@type": "xsd:dateTime"},
        "suomi-meta:creator": creator_uuid,
        "suomi-meta:modifier": creator_uuid,
        "suomi-meta:publicationStatus": {
            "@id": "http://uri.suomi.fi/codelist/interoperabilityplatform/interoperabilityplatform_status/code/SUGGESTED"
        },
        "rdfs:isDefinedBy": {"@id": f"https://iri.suomi.fi/model/{namespace}/"},
        "rdfs:subClassOf": {"@id": "ktddecv:Document"},
        "sh:targetClass": {"@id": f"ktddecv:{name}"},
        "sh:property": []
    }
    
    # Add properties
    for prop_name in properties:
        property_def = {
            "@id": f"{namespace}:has{prop_name[0].upper()}{prop_name[1:]}",
            "@type": ["owl:ObjectProperty", "sh:PropertyShape"],
            "rdfs:label": {"@language": "en", "@value": f"has {prop_name.lower()}"},
            "dcterms:identifier": {"@value": f"has{prop_name[0].upper()}{prop_name[1:]}", "@type": "xsd:NCName"},
            "dcterms:created": {"@value": timestamp, "@type": "xsd:dateTime"},
            "dcterms:modified": {"@value": timestamp, "@type": "xsd:dateTime"},
            "suomi-meta:creator": creator_uuid,
            "suomi-meta:modifier": creator_uuid,
            "suomi-meta:publicationStatus": {
                "@id": "http://uri.suomi.fi/codelist/interoperabilityplatform/interoperabilityplatform_status/code/SUGGESTED"
            },
            "sh:path": {"@id": f"ktddecv:has{prop_name[0].upper()}{prop_name[1:]}"},
            "rdfs:isDefinedBy": {"@id": f"https://iri.suomi.fi/model/{namespace}/"}
        }
        
        # Add to document shape properties
        document_shape["sh:property"].append({"@id": f"{namespace}:has{prop_name[0].upper()}{prop_name[1:]}"})
        graph.append(property_def)
    
    graph.append(document_shape)
    
    # Create final SHACL document
    shacl_doc = {
        "@context": {
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "owl": "http://www.w3.org/2002/07/owl#",
            "sh": "http://www.w3.org/ns/shacl#",
            "dcterms": "http://purl.org/dc/terms/",
            "dcap": "http://purl.org/ws-mmi-dc/terms/",
            "suomi-meta": "http://iow.csc.fi/ns/suomi-meta/",
            "ktddecv": "https://iri.suomi.fi/model/ktddecv/",
            namespace: f"https://iri.suomi.fi/model/{namespace}/"
        },
        "@graph": graph
    }
    
    return shacl_doc

def main():
    """Generate all missing SHACL profiles"""
    
    print(f"Generating {len(DOCUMENTS_TO_GENERATE)} SHACL profiles...")
    
    for doc_info in DOCUMENTS_TO_GENERATE:
        name = doc_info["name"]
        filename = f"{name.lower()}-v0.0.1.jsonld"
        filepath = f"shacl/{filename}"
        
        print(f"  Creating {filename}...")
        
        shacl_doc = create_shacl_document(doc_info)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(shacl_doc, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Generated {len(DOCUMENTS_TO_GENERATE)} SHACL profiles in shacl/")
    print("\nNext steps:")
    print("  1. Run: python3 tools/shacl-to-vc-converter.py")
    print("  2. Run: python3 tools/generate_vc_templates.py")
    print("  3. Update demo to use all 36 documents")

if __name__ == "__main__":
    main()
