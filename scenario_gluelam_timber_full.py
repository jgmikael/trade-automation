#!/usr/bin/env python3
"""
Complete Finland → Japan Gluelam Timber Export Scenario
All 15 relevant documents for the trade
"""

from datetime import datetime, timedelta

# Trade participants
SELLER = {
    "name": "Nordic Timber Oy",
    "address": "Metsäkatu 15, 88900 Kuhmo, Finland",
    "country": "FI",
    "vat": "FI12345678",
    "contact": "exports@nordictimber.fi",
    "bank": "Nordea Bank Finland",
    "iban": "FI7910001234567890",
    "swift": "NDEAFIHH"
}

BUYER = {
    "name": "Tokyo Construction Materials Ltd",
    "address": "3-7-1 Koto, Koto-ku, Tokyo 135-0016, Japan",
    "country": "JP",
    "tax_id": "JP9876543210",
    "contact": "procurement@tokyoconstruction.jp",
    "bank": "MUFG Bank Tokyo",
    "account": "JP1234567890",
    "swift": "BOTKJPJT"
}

CARRIER = {
    "name": "FESCO (Far Eastern Shipping Company)",
    "scac": "FESO",
    "contact": "booking@fesco.com"
}

FREIGHT_FORWARDER = {
    "name": "Baltic Logistics Oy",
    "address": "Satamakatu 8, 26100 Rauma, Finland",
    "contact": "operations@balticlogistics.fi"
}

# Trade details
SHIPMENT_DATE = datetime.now() - timedelta(days=10)
ARRIVAL_DATE = datetime.now() + timedelta(days=35)
LC_ISSUE_DATE = datetime.now() - timedelta(days=30)
PO_DATE = datetime.now() - timedelta(days=45)

# Products
PRODUCTS = [
    {
        "code": "GLULAM-GL30C-90X315",
        "description": "Gluelam Beam 90x315x12000mm GL30c",
        "quantity": 120,
        "unit": "PCS",
        "unit_price": 1950.00,
        "total": 234000.00,
        "hs_code": "4418.91",
        "weight_per_unit": 160,  # kg
        "volume_per_unit": 0.34,  # m³
        "grade": "GL30c",
        "standard": "EN 14080:2013"
    },
    {
        "code": "GLULAM-GL32H-115X405",
        "description": "Gluelam Beam 115x405x15000mm GL32h",
        "quantity": 40,
        "unit": "PCS",
        "unit_price": 2625.00,
        "total": 105000.00,
        "hs_code": "4418.91",
        "weight_per_unit": 280,  # kg
        "volume_per_unit": 0.70,  # m³
        "grade": "GL32h",
        "standard": "EN 14080:2013"
    }
]

# Calculate totals
TOTAL_GOODS_VALUE = sum(p["total"] for p in PRODUCTS)
FREIGHT_COST = 12000.00
INSURANCE_COST = 2000.00
TOTAL_INVOICE = TOTAL_GOODS_VALUE + FREIGHT_COST
LC_AMOUNT = TOTAL_INVOICE + INSURANCE_COST

TOTAL_WEIGHT = sum(p["quantity"] * p["weight_per_unit"] for p in PRODUCTS)
TOTAL_VOLUME = sum(p["quantity"] * p["volume_per_unit"] for p in PRODUCTS)
TOTAL_PACKAGES = 8  # 8 bundles

# Document IDs
DOC_IDS = {
    "purchase_order": "4500001000",
    "documentary_credit": "LC-MUFG-FI-2024-05678",
    "bill_of_lading": "FESCO2024FI123456",
    "commercial_invoice": "9000002000",
    "certificate_of_origin": "COO-FI-2024-0234",
    "packing_list": "PL-2024-0567",
    "insurance_certificate": "INS-FESCO-2024-1234",
    "phytosanitary_certificate": "PHY-FI-2024-00891",
    "customs_declaration_export": "FI-EXP-2024-123456",
    "customs_declaration_import": "JP-IMP-2024-987654",
    "delivery_note": "DN-2024-0234",
    "regulatory_certificate": "CE-GL-2024-0156",
    "sea_cargo_manifest": "FESCO-MAN-2024-FI123",
    "warehouse_receipt": "WH-RAU-2024-0567",
    "payment_confirmation": "PAY-MUFG-2024-05678"
}

# All 15 documents for the gluelam timber trade
DOCUMENTS = {
    "purchase_order": {
        "@type": "PurchaseOrder",
        "purchaseOrderNumber": DOC_IDS["purchase_order"],
        "issueDate": PO_DATE.strftime("%Y-%m-%d"),
        "buyerParty": {
            "@type": "Party",
            "partyName": BUYER["name"],
            "postalAddress": BUYER["address"],
            "country": {"@type": "Country", "countryCode": BUYER["country"]}
        },
        "sellerParty": {
            "@type": "Party",
            "partyName": SELLER["name"],
            "postalAddress": SELLER["address"],
            "country": {"@type": "Country", "countryCode": SELLER["country"]}
        },
        "deliveryTerms": {
            "@type": "TradeDeliveryTerms",
            "incoterms": "CFR",
            "namedPlace": "Tokyo Port, Japan"
        },
        "paymentTerms": {
            "@type": "PaymentTerms",
            "paymentMeans": "Letter of Credit",
            "paymentDueDate": (SHIPMENT_DATE + timedelta(days=60)).strftime("%Y-%m-%d")
        },
        "goodsItems": [
            {
                "@type": "GoodsItem",
                "itemNumber": str(i+1),
                "description": prod["description"],
                "quantity": {"@type": "Quantity", "value": prod["quantity"], "unitCode": prod["unit"]},
                "unitPrice": {"@type": "MonetaryAmount", "value": prod["unit_price"], "currency": "EUR"},
                "totalAmount": {"@type": "MonetaryAmount", "value": prod["total"], "currency": "EUR"}
            } for i, prod in enumerate(PRODUCTS)
        ],
        "totalAmount": {
            "@type": "MonetaryAmount",
            "value": TOTAL_GOODS_VALUE,
            "currency": "EUR"
        }
    },
    
    "documentary_credit": {
        "@type": "DocumentaryCredit",
        "creditNumber": DOC_IDS["documentary_credit"],
        "issueDate": LC_ISSUE_DATE.strftime("%Y-%m-%d"),
        "expiryDate": (LC_ISSUE_DATE + timedelta(days=90)).strftime("%Y-%m-%d"),
        "applicant": {
            "@type": "Party",
            "partyName": BUYER["name"],
            "postalAddress": BUYER["address"]
        },
        "beneficiary": {
            "@type": "Party",
            "partyName": SELLER["name"],
            "postalAddress": SELLER["address"]
        },
        "issuingBank": {
            "@type": "Bank",
            "bankName": BUYER["bank"],
            "swiftCode": BUYER["swift"]
        },
        "advisingBank": {
            "@type": "Bank",
            "bankName": SELLER["bank"],
            "swiftCode": SELLER["swift"]
        },
        "creditAmount": {
            "@type": "MonetaryAmount",
            "value": LC_AMOUNT,
            "currency": "EUR"
        },
        "creditType": "Confirmed Irrevocable",
        "presentationPeriod": "21 days after shipment date",
        "documentsRequired": [
            "Commercial Invoice",
            "Bill of Lading",
            "Certificate of Origin",
            "Packing List",
            "Insurance Certificate",
            "Phytosanitary Certificate"
        ]
    },
    
    "bill_of_lading": {
        "@type": "BillOfLading",
        "blNumber": DOC_IDS["bill_of_lading"],
        "issueDate": SHIPMENT_DATE.strftime("%Y-%m-%d"),
        "carrierParty": {
            "@type": "Party",
            "partyName": CARRIER["name"]
        },
        "shipperParty": {
            "@type": "Party",
            "partyName": SELLER["name"],
            "postalAddress": SELLER["address"]
        },
        "consigneeParty": {
            "@type": "Party",
            "partyName": BUYER["name"],
            "postalAddress": BUYER["address"]
        },
        "notifyParty": {
            "@type": "Party",
            "partyName": BUYER["name"],
            "contactInfo": BUYER["contact"]
        },
        "portOfLoading": {
            "@type": "Location",
            "locationName": "Rauma Port",
            "countryCode": "FI"
        },
        "portOfDischarge": {
            "@type": "Location",
            "locationName": "Tokyo Port",
            "countryCode": "JP"
        },
        "vessel": "MV Baltic Express",
        "voyageNumber": "V2024-FI-123",
        "goodsDescription": "Engineered Gluelam Timber Beams",
        "numberOfPackages": TOTAL_PACKAGES,
        "grossWeight": {
            "@type": "Quantity",
            "value": TOTAL_WEIGHT,
            "unitCode": "KGM"
        },
        "volume": {
            "@type": "Quantity",
            "value": TOTAL_VOLUME,
            "unitCode": "MTQ"
        },
        "freightPayable": "Prepaid",
        "deliveryTerms": "CFR Tokyo Port"
    },
    
    "commercial_invoice": {
        "@type": "CommercialInvoice",
        "invoiceNumber": DOC_IDS["commercial_invoice"],
        "issueDate": SHIPMENT_DATE.strftime("%Y-%m-%d"),
        "sellerParty": {
            "@type": "Party",
            "partyName": SELLER["name"],
            "postalAddress": SELLER["address"],
            "vatNumber": SELLER["vat"]
        },
        "buyerParty": {
            "@type": "Party",
            "partyName": BUYER["name"],
            "postalAddress": BUYER["address"],
            "taxId": BUYER["tax_id"]
        },
        "invoiceLines": [
            {
                "@type": "InvoiceLine",
                "lineNumber": str(i+1),
                "productDescription": prod["description"],
                "hsCode": prod["hs_code"],
                "quantity": {"@type": "Quantity", "value": prod["quantity"], "unitCode": prod["unit"]},
                "unitPrice": {"@type": "MonetaryAmount", "value": prod["unit_price"], "currency": "EUR"},
                "lineTotal": {"@type": "MonetaryAmount", "value": prod["total"], "currency": "EUR"}
            } for i, prod in enumerate(PRODUCTS)
        ],
        "subtotal": {"@type": "MonetaryAmount", "value": TOTAL_GOODS_VALUE, "currency": "EUR"},
        "freightCharges": {"@type": "MonetaryAmount", "value": FREIGHT_COST, "currency": "EUR"},
        "totalAmount": {"@type": "MonetaryAmount", "value": TOTAL_INVOICE, "currency": "EUR"},
        "paymentTerms": "Letter of Credit No. " + DOC_IDS["documentary_credit"],
        "deliveryTerms": "CFR Tokyo Port",
        "referenceBL": DOC_IDS["bill_of_lading"],
        "referenceLC": DOC_IDS["documentary_credit"]
    },
    
    "certificate_of_origin": {
        "@type": "CertificateOfOrigin",
        "certificateNumber": DOC_IDS["certificate_of_origin"],
        "issueDate": SHIPMENT_DATE.strftime("%Y-%m-%d"),
        "issuingAuthority": {
            "@type": "Party",
            "partyName": "Finnish Chamber of Commerce",
            "postalAddress": "Helsinki, Finland"
        },
        "exporter": {
            "@type": "Party",
            "partyName": SELLER["name"],
            "postalAddress": SELLER["address"]
        },
        "consignee": {
            "@type": "Party",
            "partyName": BUYER["name"],
            "postalAddress": BUYER["address"]
        },
        "countryOfOrigin": {
            "@type": "Country",
            "countryCode": "FI",
            "countryName": "Finland"
        },
        "goodsDescription": "Engineered Gluelam Timber Beams (GL30c, GL32h)",
        "hsCode": "4418.91",
        "referenceBL": DOC_IDS["bill_of_lading"],
        "referenceInvoice": DOC_IDS["commercial_invoice"]
    },
    
    "packing_list": {
        "@type": "PackingList",
        "packingListNumber": DOC_IDS["packing_list"],
        "issueDate": SHIPMENT_DATE.strftime("%Y-%m-%d"),
        "shipper": {
            "@type": "Party",
            "partyName": SELLER["name"],
            "postalAddress": SELLER["address"]
        },
        "consignee": {
            "@type": "Party",
            "partyName": BUYER["name"],
            "postalAddress": BUYER["address"]
        },
        "packages": [
            {
                "@type": "Package",
                "packageNumber": f"BUNDLE-{i+1:03d}",
                "packageType": "Timber Bundle",
                "contents": f"{PRODUCTS[i % len(PRODUCTS)]['description']} (x{PRODUCTS[i % len(PRODUCTS)]['quantity'] // (TOTAL_PACKAGES // len(PRODUCTS))})",
                "grossWeight": {"@type": "Quantity", "value": TOTAL_WEIGHT / TOTAL_PACKAGES, "unitCode": "KGM"},
                "dimensions": "Strapped timber bundle"
            } for i in range(TOTAL_PACKAGES)
        ],
        "totalGrossWeight": {"@type": "Quantity", "value": TOTAL_WEIGHT, "unitCode": "KGM"},
        "totalNetWeight": {"@type": "Quantity", "value": TOTAL_WEIGHT * 0.98, "unitCode": "KGM"},
        "totalVolume": {"@type": "Quantity", "value": TOTAL_VOLUME, "unitCode": "MTQ"},
        "referenceBL": DOC_IDS["bill_of_lading"],
        "referenceInvoice": DOC_IDS["commercial_invoice"]
    },
    
    "insurance_certificate": {
        "@type": "InsuranceCertificate",
        "certificateNumber": DOC_IDS["insurance_certificate"],
        "issueDate": (SHIPMENT_DATE - timedelta(days=2)).strftime("%Y-%m-%d"),
        "insurer": {
            "@type": "Party",
            "partyName": "Nordic Marine Insurance AS",
            "postalAddress": "Oslo, Norway"
        },
        "insured": {
            "@type": "Party",
            "partyName": SELLER["name"],
            "postalAddress": SELLER["address"]
        },
        "policyNumber": "NMI-2024-TIMBER-5678",
        "insuredAmount": {"@type": "MonetaryAmount", "value": LC_AMOUNT * 1.1, "currency": "EUR"},
        "coverage": "All Risks (Institute Cargo Clauses A)",
        "goodsDescription": "Gluelam Timber Beams - 160 PCS total",
        "voyage": "Rauma Port, Finland to Tokyo Port, Japan",
        "vessel": "MV Baltic Express",
        "referenceBL": DOC_IDS["bill_of_lading"]
    },
    
    "phytosanitary_certificate": {
        "@type": "PhytosanitaryCertificate",
        "certificateNumber": DOC_IDS["phytosanitary_certificate"],
        "issueDate": (SHIPMENT_DATE - timedelta(days=1)).strftime("%Y-%m-%d"),
        "issuingAuthority": {
            "@type": "Party",
            "partyName": "Finnish Food Authority - Plant Health Unit",
            "postalAddress": "Helsinki, Finland"
        },
        "exporter": {
            "@type": "Party",
            "partyName": SELLER["name"],
            "postalAddress": SELLER["address"]
        },
        "consignee": {
            "@type": "Party",
            "partyName": BUYER["name"],
            "postalAddress": BUYER["address"]
        },
        "placeOfOrigin": "Finland - Kainuu Region",
        "declaredMeansOfConveyance": "Sea Freight - Container",
        "pointOfEntry": "Tokyo Port, Japan",
        "botanicalName": "Picea abies (Norway Spruce), Pinus sylvestris (Scots Pine)",
        "treatment": "Heat treatment ISPM-15 compliant, Kiln dried to 12% moisture content",
        "disinfestationMethod": "HT (Heat Treatment) 56°C for 30 minutes",
        "additionalDeclaration": "Wood products free from bark, treated according to ISPM-15 standard",
        "inspectionDate": (SHIPMENT_DATE - timedelta(days=2)).strftime("%Y-%m-%d"),
        "inspectorName": "Dr. Matti Virtanen"
    },
    
    "customs_declaration_export": {
        "@type": "CustomsDeclaration",
        "declarationNumber": DOC_IDS["customs_declaration_export"],
        "declarationType": "Export Declaration",
        "declarationDate": SHIPMENT_DATE.strftime("%Y-%m-%d"),
        "declarant": {
            "@type": "Party",
            "partyName": FREIGHT_FORWARDER["name"],
            "postalAddress": FREIGHT_FORWARDER["address"]
        },
        "exporter": {
            "@type": "Party",
            "partyName": SELLER["name"],
            "postalAddress": SELLER["address"],
            "eoriNumber": "FI" + SELLER["vat"]
        },
        "importer": {
            "@type": "Party",
            "partyName": BUYER["name"],
            "postalAddress": BUYER["address"]
        },
        "customsOffice": {
            "@type": "CustomsOffice",
            "officeName": "Finnish Customs - Rauma",
            "officeCode": "FI-RAU-001"
        },
        "goodsItems": [
            {
                "@type": "GoodsItem",
                "itemNumber": str(i+1),
                "description": prod["description"],
                "hsCode": prod["hs_code"],
                "origin": "FI",
                "quantity": {"@type": "Quantity", "value": prod["quantity"], "unitCode": prod["unit"]},
                "value": {"@type": "MonetaryAmount", "value": prod["total"], "currency": "EUR"}
            } for i, prod in enumerate(PRODUCTS)
        ],
        "totalInvoiceAmount": {"@type": "MonetaryAmount", "value": TOTAL_GOODS_VALUE, "currency": "EUR"},
        "destinationCountry": "JP",
        "exportProcedure": "10 - Permanent export",
        "referenceBL": DOC_IDS["bill_of_lading"],
        "referenceInvoice": DOC_IDS["commercial_invoice"]
    },
    
    "customs_declaration_import": {
        "@type": "CustomsDeclaration",
        "declarationNumber": DOC_IDS["customs_declaration_import"],
        "declarationType": "Import Declaration",
        "declarationDate": ARRIVAL_DATE.strftime("%Y-%m-%d"),
        "declarant": {
            "@type": "Party",
            "partyName": "Tokyo Customs Broker KK",
            "postalAddress": "Tokyo, Japan"
        },
        "exporter": {
            "@type": "Party",
            "partyName": SELLER["name"],
            "postalAddress": SELLER["address"]
        },
        "importer": {
            "@type": "Party",
            "partyName": BUYER["name"],
            "postalAddress": BUYER["address"],
            "customsId": BUYER["tax_id"]
        },
        "customsOffice": {
            "@type": "CustomsOffice",
            "officeName": "Japan Customs - Tokyo Port",
            "officeCode": "JP-TYO-PORT"
        },
        "goodsItems": [
            {
                "@type": "GoodsItem",
                "itemNumber": str(i+1),
                "description": prod["description"],
                "hsCode": prod["hs_code"],
                "origin": "FI",
                "quantity": {"@type": "Quantity", "value": prod["quantity"], "unitCode": prod["unit"]},
                "value": {"@type": "MonetaryAmount", "value": prod["total"], "currency": "EUR"}
            } for i, prod in enumerate(PRODUCTS)
        ],
        "totalInvoiceAmount": {"@type": "MonetaryAmount", "value": TOTAL_INVOICE, "currency": "EUR"},
        "assessedDuties": {"@type": "MonetaryAmount", "value": 0.00, "currency": "JPY", "note": "Zero duty under EU-Japan EPA"},
        "importProcedure": "40 - Release for free circulation",
        "preferentialTreatment": "EU-Japan Economic Partnership Agreement (EPA)",
        "referenceBL": DOC_IDS["bill_of_lading"],
        "referenceInvoice": DOC_IDS["commercial_invoice"]
    },
    
    "delivery_note": {
        "@type": "DeliveryNote",
        "deliveryNoteNumber": DOC_IDS["delivery_note"],
        "deliveryDate": (ARRIVAL_DATE + timedelta(days=3)).strftime("%Y-%m-%d"),
        "supplier": {
            "@type": "Party",
            "partyName": SELLER["name"],
            "postalAddress": SELLER["address"]
        },
        "recipient": {
            "@type": "Party",
            "partyName": BUYER["name"],
            "postalAddress": BUYER["address"]
        },
        "deliveryAddress": BUYER["address"] + " - Construction Site Warehouse",
        "carrierParty": {
            "@type": "Party",
            "partyName": "Tokyo Logistics KK",
            "vehicleRegistration": "Tokyo 500 た 1234"
        },
        "deliveryNoteLines": [
            {
                "@type": "DeliveryNoteLine",
                "lineNumber": str(i+1),
                "productDescription": prod["description"],
                "deliveredQuantity": {"@type": "Quantity", "value": prod["quantity"], "unitCode": prod["unit"]},
                "condition": "Good"
            } for i, prod in enumerate(PRODUCTS)
        ],
        "receivedBy": "Tanaka-san (Site Manager)",
        "receivedDate": (ARRIVAL_DATE + timedelta(days=3)).strftime("%Y-%m-%d"),
        "referencePO": DOC_IDS["purchase_order"],
        "referenceBL": DOC_IDS["bill_of_lading"]
    },
    
    "regulatory_certificate": {
        "@type": "RegulatoryCertificate",
        "certificateNumber": DOC_IDS["regulatory_certificate"],
        "issueDate": (SHIPMENT_DATE - timedelta(days=5)).strftime("%Y-%m-%d"),
        "issuingAuthority": {
            "@type": "Party",
            "partyName": "TÜV SÜD Finland Oy",
            "postalAddress": "Helsinki, Finland"
        },
        "applicant": {
            "@type": "Party",
            "partyName": SELLER["name"],
            "postalAddress": SELLER["address"]
        },
        "certificateType": "CE Marking - Structural Timber",
        "productDescription": "Glued laminated timber (Glulam) structural beams",
        "standard": "EN 14080:2013 - Timber structures - Glued laminated timber and glued solid timber",
        "grades": "GL30c, GL32h",
        "strengthClass": "GL30c (f_m,g,k = 30 N/mm²), GL32h (f_m,g,k = 32 N/mm²)",
        "testResults": "All mechanical properties compliant with EN 14080:2013",
        "factoryProductionControl": "ISO 9001:2015 certified",
        "validityPeriod": "5 years from issue date",
        "remarks": "Suitable for structural use in construction per Eurocode 5"
    },
    
    "sea_cargo_manifest": {
        "@type": "SeaCargoManifest",
        "manifestNumber": DOC_IDS["sea_cargo_manifest"],
        "issueDate": SHIPMENT_DATE.strftime("%Y-%m-%d"),
        "vessel": {
            "@type": "TransportMeans",
            "vesselName": "MV Baltic Express",
            "imoNumber": "IMO9876543",
            "flag": "Finland"
        },
        "voyage": "V2024-FI-123",
        "portOfLoading": {
            "@type": "Location",
            "locationName": "Rauma Port",
            "unlocode": "FIRAU"
        },
        "portOfDischarge": {
            "@type": "Location",
            "locationName": "Tokyo Port",
            "unlocode": "JPTYO"
        },
        "carrierParty": {
            "@type": "Party",
            "partyName": CARRIER["name"]
        },
        "consignments": [
            {
                "@type": "Consignment",
                "blNumber": DOC_IDS["bill_of_lading"],
                "shipper": SELLER["name"],
                "consignee": BUYER["name"],
                "description": "Gluelam Timber Beams",
                "packages": TOTAL_PACKAGES,
                "weight": {"@type": "Quantity", "value": TOTAL_WEIGHT, "unitCode": "KGM"},
                "volume": {"@type": "Quantity", "value": TOTAL_VOLUME, "unitCode": "MTQ"}
            }
        ],
        "totalPackages": TOTAL_PACKAGES,
        "totalWeight": {"@type": "Quantity", "value": TOTAL_WEIGHT, "unitCode": "KGM"}
    },
    
    "warehouse_receipt": {
        "@type": "WarehouseReceipt",
        "receiptNumber": DOC_IDS["warehouse_receipt"],
        "issueDate": (SHIPMENT_DATE - timedelta(days=3)).strftime("%Y-%m-%d"),
        "warehouse": {
            "@type": "Party",
            "partyName": "Rauma Port Warehouse Services Oy",
            "postalAddress": "Rauma Port Terminal, 26100 Rauma, Finland"
        },
        "depositor": {
            "@type": "Party",
            "partyName": SELLER["name"],
            "postalAddress": SELLER["address"]
        },
        "goodsDescription": "Gluelam timber beams (160 pieces) ready for export",
        "quantity": {
            "@type": "Quantity",
            "value": 160,
            "unitCode": "PCS"
        },
        "weight": {"@type": "Quantity", "value": TOTAL_WEIGHT, "unitCode": "KGM"},
        "storageLocation": "Export Warehouse Section B-12",
        "storageStartDate": (SHIPMENT_DATE - timedelta(days=3)).strftime("%Y-%m-%d"),
        "storageEndDate": SHIPMENT_DATE.strftime("%Y-%m-%d"),
        "releaseCondition": "Released for shipment on B/L " + DOC_IDS["bill_of_lading"]
    },
    
    "payment_confirmation": {
        "@type": "PaymentConfirmation",
        "confirmationNumber": DOC_IDS["payment_confirmation"],
        "paymentDate": (SHIPMENT_DATE + timedelta(days=25)).strftime("%Y-%m-%d"),
        "payer": {
            "@type": "Party",
            "partyName": BUYER["bank"],
            "swiftCode": BUYER["swift"]
        },
        "payee": {
            "@type": "Party",
            "partyName": SELLER["name"],
            "bankAccount": SELLER["iban"],
            "swiftCode": SELLER["swift"]
        },
        "paymentAmount": {
            "@type": "MonetaryAmount",
            "value": TOTAL_INVOICE,
            "currency": "EUR"
        },
        "paymentMethod": "Documentary Credit Settlement",
        "referenceDocument": "L/C No. " + DOC_IDS["documentary_credit"],
        "paymentStatus": "Completed",
        "transactionId": "SWIFT-MT700-2024-05678",
        "valueDate": (SHIPMENT_DATE + timedelta(days=25)).strftime("%Y-%m-%d")
    }
}

# Actor views - who sees which documents
ACTOR_VIEWS = {
    "buyer": [
        "purchase_order", "documentary_credit", "bill_of_lading", 
        "commercial_invoice", "certificate_of_origin", "packing_list",
        "insurance_certificate", "customs_declaration_import", 
        "delivery_note", "payment_confirmation"
    ],
    "seller": [
        "purchase_order", "documentary_credit", "bill_of_lading",
        "commercial_invoice", "certificate_of_origin", "packing_list",
        "insurance_certificate", "phytosanitary_certificate",
        "customs_declaration_export", "delivery_note", "regulatory_certificate",
        "warehouse_receipt", "payment_confirmation"
    ],
    "bank": [
        "purchase_order", "documentary_credit", "commercial_invoice",
        "bill_of_lading", "certificate_of_origin", "packing_list",
        "insurance_certificate", "phytosanitary_certificate",
        "payment_confirmation"
    ],
    "carrier": [
        "bill_of_lading", "packing_list", "sea_cargo_manifest",
        "phytosanitary_certificate", "dangerous_goods_declaration",
        "warehouse_receipt"
    ],
    "customs": [
        "commercial_invoice", "bill_of_lading", "certificate_of_origin",
        "packing_list", "phytosanitary_certificate",
        "customs_declaration_export", "customs_declaration_import"
    ],
    "chamber": [
        "certificate_of_origin", "commercial_invoice"
    ],
    "certifier": [
        "phytosanitary_certificate", "regulatory_certificate"
    ]
}

# Timeline events
TIMELINE = [
    {"date": (PO_DATE).strftime("%Y-%m-%d"), "event": "Purchase Order Issued", "actor": "Buyer", "doc": "purchase_order"},
    {"date": (LC_ISSUE_DATE).strftime("%Y-%m-%d"), "event": "Letter of Credit Opened", "actor": "Bank", "doc": "documentary_credit"},
    {"date": (SHIPMENT_DATE - timedelta(days=5)).strftime("%Y-%m-%d"), "event": "CE Certification Completed", "actor": "Certifier", "doc": "regulatory_certificate"},
    {"date": (SHIPMENT_DATE - timedelta(days=3)).strftime("%Y-%m-%d"), "event": "Goods Stored at Port Warehouse", "actor": "Warehouse", "doc": "warehouse_receipt"},
    {"date": (SHIPMENT_DATE - timedelta(days=2)).strftime("%Y-%m-%d"), "event": "Phytosanitary Inspection", "actor": "Authority", "doc": "phytosanitary_certificate"},
    {"date": (SHIPMENT_DATE - timedelta(days=2)).strftime("%Y-%m-%d"), "event": "Insurance Certificate Issued", "actor": "Insurer", "doc": "insurance_certificate"},
    {"date": (SHIPMENT_DATE - timedelta(days=1)).strftime("%Y-%m-%d"), "event": "Certificate of Origin Issued", "actor": "Chamber", "doc": "certificate_of_origin"},
    {"date": SHIPMENT_DATE.strftime("%Y-%m-%d"), "event": "Goods Loaded & Shipped", "actor": "Carrier", "doc": "bill_of_lading"},
    {"date": SHIPMENT_DATE.strftime("%Y-%m-%d"), "event": "Commercial Invoice Issued", "actor": "Seller", "doc": "commercial_invoice"},
    {"date": SHIPMENT_DATE.strftime("%Y-%m-%d"), "event": "Packing List Created", "actor": "Seller", "doc": "packing_list"},
    {"date": SHIPMENT_DATE.strftime("%Y-%m-%d"), "event": "Export Customs Clearance", "actor": "Customs", "doc": "customs_declaration_export"},
    {"date": SHIPMENT_DATE.strftime("%Y-%m-%d"), "event": "Sea Cargo Manifest Filed", "actor": "Carrier", "doc": "sea_cargo_manifest"},
    {"date": (SHIPMENT_DATE + timedelta(days=25)).strftime("%Y-%m-%d"), "event": "Payment Processed", "actor": "Bank", "doc": "payment_confirmation"},
    {"date": ARRIVAL_DATE.strftime("%Y-%m-%d"), "event": "Vessel Arrives Tokyo Port", "actor": "Carrier", "doc": None},
    {"date": ARRIVAL_DATE.strftime("%Y-%m-%d"), "event": "Import Customs Clearance", "actor": "Customs", "doc": "customs_declaration_import"},
    {"date": (ARRIVAL_DATE + timedelta(days=3)).strftime("%Y-%m-%d"), "event": "Final Delivery to Buyer", "actor": "Logistics", "doc": "delivery_note"}
]

print("✅ Complete Gluelam Timber Scenario Loaded")
print(f"   📦 {len(DOCUMENTS)} Documents")
print(f"   👥 {len(ACTOR_VIEWS)} Actor Views")
print(f"   ⏱️  {len(TIMELINE)} Timeline Events")
