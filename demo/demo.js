// demo.js - Finnish Gluelam Timber to Japan Trade Demo
// All 15 relevant KTDDE documents for the trade
// Generated from scenario_gluelam_timber_full.py

// Document metadata
const docInfo = {
  purchase_order: {
    title: "Purchase Order",
    icon: "📝",
    description: "Buyer's order for gluelam timber beams"
  },
  documentary_credit: {
    title: "Documentary Credit (L/C)",
    icon: "🏦",
    description: "Confirmed irrevocable letter of credit from MUFG Bank"
  },
  bill_of_lading: {
    title: "Bill of Lading",
    icon: "🚢",
    description: "Ocean transport document from FESCO"
  },
  commercial_invoice: {
    title: "Commercial Invoice",
    icon: "📄",
    description: "Seller's invoice for EUR 339,000"
  },
  certificate_of_origin: {
    title: "Certificate of Origin",
    icon: "📜",
    description: "Finnish Chamber of Commerce certificate"
  },
  packing_list: {
    title: "Packing List",
    icon: "📦",
    description: "Detailed packing information for 8 bundles"
  },
  insurance_certificate: {
    title: "Insurance Certificate",
    icon: "🛡️",
    description: "All Risks marine cargo insurance"
  },
  phytosanitary_certificate: {
    title: "Phytosanitary Certificate",
    icon: "🌲",
    description: "ISPM-15 compliant wood treatment certificate"
  },
  customs_declaration_export: {
    title: "Customs Declaration (Export)",
    icon: "🛃",
    description: "Finnish export customs clearance"
  },
  customs_declaration_import: {
    title: "Customs Declaration (Import)",
    icon: "🛃",
    description: "Japanese import customs clearance"
  },
  delivery_note: {
    title: "Delivery Note",
    icon: "🚚",
    description: "Final delivery to construction site"
  },
  regulatory_certificate: {
    title: "Regulatory Certificate",
    icon: "✅",
    description: "CE marking for structural timber (EN 14080)"
  },
  sea_cargo_manifest: {
    title: "Sea Cargo Manifest",
    icon: "📋",
    description: "Vessel manifest for MV Baltic Express"
  },
  warehouse_receipt: {
    title: "Warehouse Receipt",
    icon: "🏭",
    description: "Rauma Port warehouse receipt"
  },
  payment_confirmation: {
    title: "Payment Confirmation",
    icon: "💰",
    description: "Bank payment confirmation via L/C"
  }
};

// All documents (SHACL-based JSON)
const documents = {
  "purchase_order": {
    "@type": "PurchaseOrder",
    "purchaseOrderNumber": "4500001000",
    "issueDate": "2025-12-31",
    "buyerParty": {
      "@type": "Party",
      "partyName": "Tokyo Construction Materials Ltd",
      "postalAddress": "3-7-1 Koto, Koto-ku, Tokyo 135-0016, Japan",
      "country": {
        "@type": "Country",
        "countryCode": "JP"
      }
    },
    "sellerParty": {
      "@type": "Party",
      "partyName": "Nordic Timber Oy",
      "postalAddress": "Metsäkatu 15, 88900 Kuhmo, Finland",
      "country": {
        "@type": "Country",
        "countryCode": "FI"
      }
    },
    "deliveryTerms": {
      "@type": "TradeDeliveryTerms",
      "incoterms": "CFR",
      "namedPlace": "Tokyo Port, Japan"
    },
    "paymentTerms": {
      "@type": "PaymentTerms",
      "paymentMeans": "Letter of Credit",
      "paymentDueDate": "2026-04-05"
    },
    "goodsItems": [
      {
        "@type": "GoodsItem",
        "itemNumber": "1",
        "description": "Gluelam Beam 90x315x12000mm GL30c",
        "quantity": {
          "@type": "Quantity",
          "value": 120,
          "unitCode": "PCS"
        },
        "unitPrice": {
          "@type": "MonetaryAmount",
          "value": 1950.0,
          "currency": "EUR"
        },
        "totalAmount": {
          "@type": "MonetaryAmount",
          "value": 234000.0,
          "currency": "EUR"
        }
      },
      {
        "@type": "GoodsItem",
        "itemNumber": "2",
        "description": "Gluelam Beam 115x405x15000mm GL32h",
        "quantity": {
          "@type": "Quantity",
          "value": 40,
          "unitCode": "PCS"
        },
        "unitPrice": {
          "@type": "MonetaryAmount",
          "value": 2625.0,
          "currency": "EUR"
        },
        "totalAmount": {
          "@type": "MonetaryAmount",
          "value": 105000.0,
          "currency": "EUR"
        }
      }
    ],
    "totalAmount": {
      "@type": "MonetaryAmount",
      "value": 339000.0,
      "currency": "EUR"
    }
  },
  "documentary_credit": {
    "@type": "DocumentaryCredit",
    "creditNumber": "LC-MUFG-FI-2024-05678",
    "issueDate": "2026-01-15",
    "expiryDate": "2026-04-15",
    "applicant": {
      "@type": "Party",
      "partyName": "Tokyo Construction Materials Ltd",
      "postalAddress": "3-7-1 Koto, Koto-ku, Tokyo 135-0016, Japan"
    },
    "beneficiary": {
      "@type": "Party",
      "partyName": "Nordic Timber Oy",
      "postalAddress": "Metsäkatu 15, 88900 Kuhmo, Finland"
    },
    "issuingBank": {
      "@type": "Bank",
      "bankName": "MUFG Bank Tokyo",
      "swiftCode": "BOTKJPJT"
    },
    "advisingBank": {
      "@type": "Bank",
      "bankName": "Nordea Bank Finland",
      "swiftCode": "NDEAFIHH"
    },
    "creditAmount": {
      "@type": "MonetaryAmount",
      "value": 353000.0,
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
    "blNumber": "FESCO2024FI123456",
    "issueDate": "2026-02-04",
    "carrierParty": {
      "@type": "Party",
      "partyName": "FESCO (Far Eastern Shipping Company)"
    },
    "shipperParty": {
      "@type": "Party",
      "partyName": "Nordic Timber Oy",
      "postalAddress": "Metsäkatu 15, 88900 Kuhmo, Finland"
    },
    "consigneeParty": {
      "@type": "Party",
      "partyName": "Tokyo Construction Materials Ltd",
      "postalAddress": "3-7-1 Koto, Koto-ku, Tokyo 135-0016, Japan"
    },
    "notifyParty": {
      "@type": "Party",
      "partyName": "Tokyo Construction Materials Ltd",
      "contactInfo": "procurement@tokyoconstruction.jp"
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
    "numberOfPackages": 8,
    "grossWeight": {
      "@type": "Quantity",
      "value": 30400,
      "unitCode": "KGM"
    },
    "volume": {
      "@type": "Quantity",
      "value": 68.80000000000001,
      "unitCode": "MTQ"
    },
    "freightPayable": "Prepaid",
    "deliveryTerms": "CFR Tokyo Port"
  },
  "commercial_invoice": {
    "@type": "CommercialInvoice",
    "invoiceNumber": "9000002000",
    "issueDate": "2026-02-04",
    "sellerParty": {
      "@type": "Party",
      "partyName": "Nordic Timber Oy",
      "postalAddress": "Metsäkatu 15, 88900 Kuhmo, Finland",
      "vatNumber": "FI12345678"
    },
    "buyerParty": {
      "@type": "Party",
      "partyName": "Tokyo Construction Materials Ltd",
      "postalAddress": "3-7-1 Koto, Koto-ku, Tokyo 135-0016, Japan",
      "taxId": "JP9876543210"
    },
    "invoiceLines": [
      {
        "@type": "InvoiceLine",
        "lineNumber": "1",
        "productDescription": "Gluelam Beam 90x315x12000mm GL30c",
        "hsCode": "4418.91",
        "quantity": {
          "@type": "Quantity",
          "value": 120,
          "unitCode": "PCS"
        },
        "unitPrice": {
          "@type": "MonetaryAmount",
          "value": 1950.0,
          "currency": "EUR"
        },
        "lineTotal": {
          "@type": "MonetaryAmount",
          "value": 234000.0,
          "currency": "EUR"
        }
      },
      {
        "@type": "InvoiceLine",
        "lineNumber": "2",
        "productDescription": "Gluelam Beam 115x405x15000mm GL32h",
        "hsCode": "4418.91",
        "quantity": {
          "@type": "Quantity",
          "value": 40,
          "unitCode": "PCS"
        },
        "unitPrice": {
          "@type": "MonetaryAmount",
          "value": 2625.0,
          "currency": "EUR"
        },
        "lineTotal": {
          "@type": "MonetaryAmount",
          "value": 105000.0,
          "currency": "EUR"
        }
      }
    ],
    "subtotal": {
      "@type": "MonetaryAmount",
      "value": 339000.0,
      "currency": "EUR"
    },
    "freightCharges": {
      "@type": "MonetaryAmount",
      "value": 12000.0,
      "currency": "EUR"
    },
    "totalAmount": {
      "@type": "MonetaryAmount",
      "value": 351000.0,
      "currency": "EUR"
    },
    "paymentTerms": "Letter of Credit No. LC-MUFG-FI-2024-05678",
    "deliveryTerms": "CFR Tokyo Port",
    "referenceBL": "FESCO2024FI123456",
    "referenceLC": "LC-MUFG-FI-2024-05678"
  },
  "certificate_of_origin": {
    "@type": "CertificateOfOrigin",
    "certificateNumber": "COO-FI-2024-0234",
    "issueDate": "2026-02-04",
    "issuingAuthority": {
      "@type": "Party",
      "partyName": "Finnish Chamber of Commerce",
      "postalAddress": "Helsinki, Finland"
    },
    "exporter": {
      "@type": "Party",
      "partyName": "Nordic Timber Oy",
      "postalAddress": "Metsäkatu 15, 88900 Kuhmo, Finland"
    },
    "consignee": {
      "@type": "Party",
      "partyName": "Tokyo Construction Materials Ltd",
      "postalAddress": "3-7-1 Koto, Koto-ku, Tokyo 135-0016, Japan"
    },
    "countryOfOrigin": {
      "@type": "Country",
      "countryCode": "FI",
      "countryName": "Finland"
    },
    "goodsDescription": "Engineered Gluelam Timber Beams (GL30c, GL32h)",
    "hsCode": "4418.91",
    "referenceBL": "FESCO2024FI123456",
    "referenceInvoice": "9000002000"
  },
  "packing_list": {
    "@type": "PackingList",
    "packingListNumber": "PL-2024-0567",
    "issueDate": "2026-02-04",
    "shipper": {
      "@type": "Party",
      "partyName": "Nordic Timber Oy",
      "postalAddress": "Metsäkatu 15, 88900 Kuhmo, Finland"
    },
    "consignee": {
      "@type": "Party",
      "partyName": "Tokyo Construction Materials Ltd",
      "postalAddress": "3-7-1 Koto, Koto-ku, Tokyo 135-0016, Japan"
    },
    "packages": [
      {
        "@type": "Package",
        "packageNumber": "BUNDLE-001",
        "packageType": "Timber Bundle",
        "contents": "Gluelam Beam 90x315x12000mm GL30c (x30)",
        "grossWeight": {
          "@type": "Quantity",
          "value": 3800.0,
          "unitCode": "KGM"
        },
        "dimensions": "Strapped timber bundle"
      },
      {
        "@type": "Package",
        "packageNumber": "BUNDLE-002",
        "packageType": "Timber Bundle",
        "contents": "Gluelam Beam 115x405x15000mm GL32h (x10)",
        "grossWeight": {
          "@type": "Quantity",
          "value": 3800.0,
          "unitCode": "KGM"
        },
        "dimensions": "Strapped timber bundle"
      },
      {
        "@type": "Package",
        "packageNumber": "BUNDLE-003",
        "packageType": "Timber Bundle",
        "contents": "Gluelam Beam 90x315x12000mm GL30c (x30)",
        "grossWeight": {
          "@type": "Quantity",
          "value": 3800.0,
          "unitCode": "KGM"
        },
        "dimensions": "Strapped timber bundle"
      },
      {
        "@type": "Package",
        "packageNumber": "BUNDLE-004",
        "packageType": "Timber Bundle",
        "contents": "Gluelam Beam 115x405x15000mm GL32h (x10)",
        "grossWeight": {
          "@type": "Quantity",
          "value": 3800.0,
          "unitCode": "KGM"
        },
        "dimensions": "Strapped timber bundle"
      },
      {
        "@type": "Package",
        "packageNumber": "BUNDLE-005",
        "packageType": "Timber Bundle",
        "contents": "Gluelam Beam 90x315x12000mm GL30c (x30)",
        "grossWeight": {
          "@type": "Quantity",
          "value": 3800.0,
          "unitCode": "KGM"
        },
        "dimensions": "Strapped timber bundle"
      },
      {
        "@type": "Package",
        "packageNumber": "BUNDLE-006",
        "packageType": "Timber Bundle",
        "contents": "Gluelam Beam 115x405x15000mm GL32h (x10)",
        "grossWeight": {
          "@type": "Quantity",
          "value": 3800.0,
          "unitCode": "KGM"
        },
        "dimensions": "Strapped timber bundle"
      },
      {
        "@type": "Package",
        "packageNumber": "BUNDLE-007",
        "packageType": "Timber Bundle",
        "contents": "Gluelam Beam 90x315x12000mm GL30c (x30)",
        "grossWeight": {
          "@type": "Quantity",
          "value": 3800.0,
          "unitCode": "KGM"
        },
        "dimensions": "Strapped timber bundle"
      },
      {
        "@type": "Package",
        "packageNumber": "BUNDLE-008",
        "packageType": "Timber Bundle",
        "contents": "Gluelam Beam 115x405x15000mm GL32h (x10)",
        "grossWeight": {
          "@type": "Quantity",
          "value": 3800.0,
          "unitCode": "KGM"
        },
        "dimensions": "Strapped timber bundle"
      }
    ],
    "totalGrossWeight": {
      "@type": "Quantity",
      "value": 30400,
      "unitCode": "KGM"
    },
    "totalNetWeight": {
      "@type": "Quantity",
      "value": 29792.0,
      "unitCode": "KGM"
    },
    "totalVolume": {
      "@type": "Quantity",
      "value": 68.80000000000001,
      "unitCode": "MTQ"
    },
    "referenceBL": "FESCO2024FI123456",
    "referenceInvoice": "9000002000"
  },
  "insurance_certificate": {
    "@type": "InsuranceCertificate",
    "certificateNumber": "INS-FESCO-2024-1234",
    "issueDate": "2026-02-02",
    "insurer": {
      "@type": "Party",
      "partyName": "Nordic Marine Insurance AS",
      "postalAddress": "Oslo, Norway"
    },
    "insured": {
      "@type": "Party",
      "partyName": "Nordic Timber Oy",
      "postalAddress": "Metsäkatu 15, 88900 Kuhmo, Finland"
    },
    "policyNumber": "NMI-2024-TIMBER-5678",
    "insuredAmount": {
      "@type": "MonetaryAmount",
      "value": 388300.00000000006,
      "currency": "EUR"
    },
    "coverage": "All Risks (Institute Cargo Clauses A)",
    "goodsDescription": "Gluelam Timber Beams - 160 PCS total",
    "voyage": "Rauma Port, Finland to Tokyo Port, Japan",
    "vessel": "MV Baltic Express",
    "referenceBL": "FESCO2024FI123456"
  },
  "phytosanitary_certificate": {
    "@type": "PhytosanitaryCertificate",
    "certificateNumber": "PHY-FI-2024-00891",
    "issueDate": "2026-02-03",
    "issuingAuthority": {
      "@type": "Party",
      "partyName": "Finnish Food Authority - Plant Health Unit",
      "postalAddress": "Helsinki, Finland"
    },
    "exporter": {
      "@type": "Party",
      "partyName": "Nordic Timber Oy",
      "postalAddress": "Metsäkatu 15, 88900 Kuhmo, Finland"
    },
    "consignee": {
      "@type": "Party",
      "partyName": "Tokyo Construction Materials Ltd",
      "postalAddress": "3-7-1 Koto, Koto-ku, Tokyo 135-0016, Japan"
    },
    "placeOfOrigin": "Finland - Kainuu Region",
    "declaredMeansOfConveyance": "Sea Freight - Container",
    "pointOfEntry": "Tokyo Port, Japan",
    "botanicalName": "Picea abies (Norway Spruce), Pinus sylvestris (Scots Pine)",
    "treatment": "Heat treatment ISPM-15 compliant, Kiln dried to 12% moisture content",
    "disinfestationMethod": "HT (Heat Treatment) 56°C for 30 minutes",
    "additionalDeclaration": "Wood products free from bark, treated according to ISPM-15 standard",
    "inspectionDate": "2026-02-02",
    "inspectorName": "Dr. Matti Virtanen"
  },
  "customs_declaration_export": {
    "@type": "CustomsDeclaration",
    "declarationNumber": "FI-EXP-2024-123456",
    "declarationType": "Export Declaration",
    "declarationDate": "2026-02-04",
    "declarant": {
      "@type": "Party",
      "partyName": "Baltic Logistics Oy",
      "postalAddress": "Satamakatu 8, 26100 Rauma, Finland"
    },
    "exporter": {
      "@type": "Party",
      "partyName": "Nordic Timber Oy",
      "postalAddress": "Metsäkatu 15, 88900 Kuhmo, Finland",
      "eoriNumber": "FIFI12345678"
    },
    "importer": {
      "@type": "Party",
      "partyName": "Tokyo Construction Materials Ltd",
      "postalAddress": "3-7-1 Koto, Koto-ku, Tokyo 135-0016, Japan"
    },
    "customsOffice": {
      "@type": "CustomsOffice",
      "officeName": "Finnish Customs - Rauma",
      "officeCode": "FI-RAU-001"
    },
    "goodsItems": [
      {
        "@type": "GoodsItem",
        "itemNumber": "1",
        "description": "Gluelam Beam 90x315x12000mm GL30c",
        "hsCode": "4418.91",
        "origin": "FI",
        "quantity": {
          "@type": "Quantity",
          "value": 120,
          "unitCode": "PCS"
        },
        "value": {
          "@type": "MonetaryAmount",
          "value": 234000.0,
          "currency": "EUR"
        }
      },
      {
        "@type": "GoodsItem",
        "itemNumber": "2",
        "description": "Gluelam Beam 115x405x15000mm GL32h",
        "hsCode": "4418.91",
        "origin": "FI",
        "quantity": {
          "@type": "Quantity",
          "value": 40,
          "unitCode": "PCS"
        },
        "value": {
          "@type": "MonetaryAmount",
          "value": 105000.0,
          "currency": "EUR"
        }
      }
    ],
    "totalInvoiceAmount": {
      "@type": "MonetaryAmount",
      "value": 339000.0,
      "currency": "EUR"
    },
    "destinationCountry": "JP",
    "exportProcedure": "10 - Permanent export",
    "referenceBL": "FESCO2024FI123456",
    "referenceInvoice": "9000002000"
  },
  "customs_declaration_import": {
    "@type": "CustomsDeclaration",
    "declarationNumber": "JP-IMP-2024-987654",
    "declarationType": "Import Declaration",
    "declarationDate": "2026-03-21",
    "declarant": {
      "@type": "Party",
      "partyName": "Tokyo Customs Broker KK",
      "postalAddress": "Tokyo, Japan"
    },
    "exporter": {
      "@type": "Party",
      "partyName": "Nordic Timber Oy",
      "postalAddress": "Metsäkatu 15, 88900 Kuhmo, Finland"
    },
    "importer": {
      "@type": "Party",
      "partyName": "Tokyo Construction Materials Ltd",
      "postalAddress": "3-7-1 Koto, Koto-ku, Tokyo 135-0016, Japan",
      "customsId": "JP9876543210"
    },
    "customsOffice": {
      "@type": "CustomsOffice",
      "officeName": "Japan Customs - Tokyo Port",
      "officeCode": "JP-TYO-PORT"
    },
    "goodsItems": [
      {
        "@type": "GoodsItem",
        "itemNumber": "1",
        "description": "Gluelam Beam 90x315x12000mm GL30c",
        "hsCode": "4418.91",
        "origin": "FI",
        "quantity": {
          "@type": "Quantity",
          "value": 120,
          "unitCode": "PCS"
        },
        "value": {
          "@type": "MonetaryAmount",
          "value": 234000.0,
          "currency": "EUR"
        }
      },
      {
        "@type": "GoodsItem",
        "itemNumber": "2",
        "description": "Gluelam Beam 115x405x15000mm GL32h",
        "hsCode": "4418.91",
        "origin": "FI",
        "quantity": {
          "@type": "Quantity",
          "value": 40,
          "unitCode": "PCS"
        },
        "value": {
          "@type": "MonetaryAmount",
          "value": 105000.0,
          "currency": "EUR"
        }
      }
    ],
    "totalInvoiceAmount": {
      "@type": "MonetaryAmount",
      "value": 351000.0,
      "currency": "EUR"
    },
    "assessedDuties": {
      "@type": "MonetaryAmount",
      "value": 0.0,
      "currency": "JPY",
      "note": "Zero duty under EU-Japan EPA"
    },
    "importProcedure": "40 - Release for free circulation",
    "preferentialTreatment": "EU-Japan Economic Partnership Agreement (EPA)",
    "referenceBL": "FESCO2024FI123456",
    "referenceInvoice": "9000002000"
  },
  "delivery_note": {
    "@type": "DeliveryNote",
    "deliveryNoteNumber": "DN-2024-0234",
    "deliveryDate": "2026-03-24",
    "supplier": {
      "@type": "Party",
      "partyName": "Nordic Timber Oy",
      "postalAddress": "Metsäkatu 15, 88900 Kuhmo, Finland"
    },
    "recipient": {
      "@type": "Party",
      "partyName": "Tokyo Construction Materials Ltd",
      "postalAddress": "3-7-1 Koto, Koto-ku, Tokyo 135-0016, Japan"
    },
    "deliveryAddress": "3-7-1 Koto, Koto-ku, Tokyo 135-0016, Japan - Construction Site Warehouse",
    "carrierParty": {
      "@type": "Party",
      "partyName": "Tokyo Logistics KK",
      "vehicleRegistration": "Tokyo 500 た 1234"
    },
    "deliveryNoteLines": [
      {
        "@type": "DeliveryNoteLine",
        "lineNumber": "1",
        "productDescription": "Gluelam Beam 90x315x12000mm GL30c",
        "deliveredQuantity": {
          "@type": "Quantity",
          "value": 120,
          "unitCode": "PCS"
        },
        "condition": "Good"
      },
      {
        "@type": "DeliveryNoteLine",
        "lineNumber": "2",
        "productDescription": "Gluelam Beam 115x405x15000mm GL32h",
        "deliveredQuantity": {
          "@type": "Quantity",
          "value": 40,
          "unitCode": "PCS"
        },
        "condition": "Good"
      }
    ],
    "receivedBy": "Tanaka-san (Site Manager)",
    "receivedDate": "2026-03-24",
    "referencePO": "4500001000",
    "referenceBL": "FESCO2024FI123456"
  },
  "regulatory_certificate": {
    "@type": "RegulatoryCertificate",
    "certificateNumber": "CE-GL-2024-0156",
    "issueDate": "2026-01-30",
    "issuingAuthority": {
      "@type": "Party",
      "partyName": "TÜV SÜD Finland Oy",
      "postalAddress": "Helsinki, Finland"
    },
    "applicant": {
      "@type": "Party",
      "partyName": "Nordic Timber Oy",
      "postalAddress": "Metsäkatu 15, 88900 Kuhmo, Finland"
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
    "manifestNumber": "FESCO-MAN-2024-FI123",
    "issueDate": "2026-02-04",
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
      "partyName": "FESCO (Far Eastern Shipping Company)"
    },
    "consignments": [
      {
        "@type": "Consignment",
        "blNumber": "FESCO2024FI123456",
        "shipper": "Nordic Timber Oy",
        "consignee": "Tokyo Construction Materials Ltd",
        "description": "Gluelam Timber Beams",
        "packages": 8,
        "weight": {
          "@type": "Quantity",
          "value": 30400,
          "unitCode": "KGM"
        },
        "volume": {
          "@type": "Quantity",
          "value": 68.80000000000001,
          "unitCode": "MTQ"
        }
      }
    ],
    "totalPackages": 8,
    "totalWeight": {
      "@type": "Quantity",
      "value": 30400,
      "unitCode": "KGM"
    }
  },
  "warehouse_receipt": {
    "@type": "WarehouseReceipt",
    "receiptNumber": "WH-RAU-2024-0567",
    "issueDate": "2026-02-01",
    "warehouse": {
      "@type": "Party",
      "partyName": "Rauma Port Warehouse Services Oy",
      "postalAddress": "Rauma Port Terminal, 26100 Rauma, Finland"
    },
    "depositor": {
      "@type": "Party",
      "partyName": "Nordic Timber Oy",
      "postalAddress": "Metsäkatu 15, 88900 Kuhmo, Finland"
    },
    "goodsDescription": "Gluelam timber beams (160 pieces) ready for export",
    "quantity": {
      "@type": "Quantity",
      "value": 160,
      "unitCode": "PCS"
    },
    "weight": {
      "@type": "Quantity",
      "value": 30400,
      "unitCode": "KGM"
    },
    "storageLocation": "Export Warehouse Section B-12",
    "storageStartDate": "2026-02-01",
    "storageEndDate": "2026-02-04",
    "releaseCondition": "Released for shipment on B/L FESCO2024FI123456"
  },
  "payment_confirmation": {
    "@type": "PaymentConfirmation",
    "confirmationNumber": "PAY-MUFG-2024-05678",
    "paymentDate": "2026-03-01",
    "payer": {
      "@type": "Party",
      "partyName": "MUFG Bank Tokyo",
      "swiftCode": "BOTKJPJT"
    },
    "payee": {
      "@type": "Party",
      "partyName": "Nordic Timber Oy",
      "bankAccount": "FI7910001234567890",
      "swiftCode": "NDEAFIHH"
    },
    "paymentAmount": {
      "@type": "MonetaryAmount",
      "value": 351000.0,
      "currency": "EUR"
    },
    "paymentMethod": "Documentary Credit Settlement",
    "referenceDocument": "L/C No. LC-MUFG-FI-2024-05678",
    "paymentStatus": "Completed",
    "transactionId": "SWIFT-MT700-2024-05678",
    "valueDate": "2026-03-01"
  }
};

// Document IDs for reference
const docIds = {
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
};

// Actor views (which documents each actor sees)
const actorViews = {
  "buyer": [
    "purchase_order",
    "documentary_credit",
    "bill_of_lading",
    "commercial_invoice",
    "certificate_of_origin",
    "packing_list",
    "insurance_certificate",
    "customs_declaration_import",
    "delivery_note",
    "payment_confirmation"
  ],
  "seller": [
    "purchase_order",
    "documentary_credit",
    "bill_of_lading",
    "commercial_invoice",
    "certificate_of_origin",
    "packing_list",
    "insurance_certificate",
    "phytosanitary_certificate",
    "customs_declaration_export",
    "delivery_note",
    "regulatory_certificate",
    "warehouse_receipt",
    "payment_confirmation"
  ],
  "bank": [
    "purchase_order",
    "documentary_credit",
    "commercial_invoice",
    "bill_of_lading",
    "certificate_of_origin",
    "packing_list",
    "insurance_certificate",
    "phytosanitary_certificate",
    "payment_confirmation"
  ],
  "carrier": [
    "bill_of_lading",
    "packing_list",
    "sea_cargo_manifest",
    "phytosanitary_certificate",
    "dangerous_goods_declaration",
    "warehouse_receipt"
  ],
  "customs": [
    "commercial_invoice",
    "bill_of_lading",
    "certificate_of_origin",
    "packing_list",
    "phytosanitary_certificate",
    "customs_declaration_export",
    "customs_declaration_import"
  ],
  "chamber": [
    "certificate_of_origin",
    "commercial_invoice"
  ],
  "certifier": [
    "phytosanitary_certificate",
    "regulatory_certificate"
  ]
};

// Timeline events
const timeline = [
  {
    "date": "2025-12-31",
    "event": "Purchase Order Issued",
    "actor": "Buyer",
    "doc": "purchase_order"
  },
  {
    "date": "2026-01-15",
    "event": "Letter of Credit Opened",
    "actor": "Bank",
    "doc": "documentary_credit"
  },
  {
    "date": "2026-01-30",
    "event": "CE Certification Completed",
    "actor": "Certifier",
    "doc": "regulatory_certificate"
  },
  {
    "date": "2026-02-01",
    "event": "Goods Stored at Port Warehouse",
    "actor": "Warehouse",
    "doc": "warehouse_receipt"
  },
  {
    "date": "2026-02-02",
    "event": "Phytosanitary Inspection",
    "actor": "Authority",
    "doc": "phytosanitary_certificate"
  },
  {
    "date": "2026-02-02",
    "event": "Insurance Certificate Issued",
    "actor": "Insurer",
    "doc": "insurance_certificate"
  },
  {
    "date": "2026-02-03",
    "event": "Certificate of Origin Issued",
    "actor": "Chamber",
    "doc": "certificate_of_origin"
  },
  {
    "date": "2026-02-04",
    "event": "Goods Loaded & Shipped",
    "actor": "Carrier",
    "doc": "bill_of_lading"
  },
  {
    "date": "2026-02-04",
    "event": "Commercial Invoice Issued",
    "actor": "Seller",
    "doc": "commercial_invoice"
  },
  {
    "date": "2026-02-04",
    "event": "Packing List Created",
    "actor": "Seller",
    "doc": "packing_list"
  },
  {
    "date": "2026-02-04",
    "event": "Export Customs Clearance",
    "actor": "Customs",
    "doc": "customs_declaration_export"
  },
  {
    "date": "2026-02-04",
    "event": "Sea Cargo Manifest Filed",
    "actor": "Carrier",
    "doc": "sea_cargo_manifest"
  },
  {
    "date": "2026-03-01",
    "event": "Payment Processed",
    "actor": "Bank",
    "doc": "payment_confirmation"
  },
  {
    "date": "2026-03-21",
    "event": "Vessel Arrives Tokyo Port",
    "actor": "Carrier",
    "doc": null
  },
  {
    "date": "2026-03-21",
    "event": "Import Customs Clearance",
    "actor": "Customs",
    "doc": "customs_declaration_import"
  },
  {
    "date": "2026-03-24",
    "event": "Final Delivery to Buyer",
    "actor": "Logistics",
    "doc": "delivery_note"
  }
];

// Actor information
const actors = [
  { id: 'buyer', name: 'Buyer', icon: '🏢', description: 'Tokyo Construction Materials Ltd' },
  { id: 'seller', name: 'Seller', icon: '🏭', description: 'Nordic Timber Oy' },
  { id: 'bank', name: 'Bank', icon: '🏦', description: 'MUFG Tokyo / Nordea Finland' },
  { id: 'carrier', name: 'Carrier', icon: '🚢', description: 'FESCO Shipping' },
  { id: 'customs', name: 'Customs', icon: '🛃', description: 'Finnish & Japanese Customs' },
  { id: 'chamber', name: 'Chamber', icon: '📜', description: 'Finnish Chamber of Commerce' },
  { id: 'certifier', name: 'Certifier', icon: '✅', description: 'TÜV SÜD & Food Authority' }
];

// Current state
let currentActor = 'buyer';
let currentDoc = null;

// Initialize demo
function initDemo() {
  renderActorTabs();
  renderDocuments(currentActor);
  renderTimeline();
}

// Render actor tabs
function renderActorTabs() {
  const container = document.getElementById('actor-tabs');
  if (!container) return;
  
  container.innerHTML = actors.map(actor => `
    <button class="actor-tab ${actor.id === currentActor ? 'active' : ''}"
            onclick="switchActor('${actor.id}')">
      <span class="actor-icon">${actor.icon}</span>
      <span class="actor-name">${actor.name}</span>
      <small>${actor.description}</small>
    </button>
  `).join('');
}

// Switch actor view
function switchActor(actorId) {
  currentActor = actorId;
  renderActorTabs();
  renderDocuments(actorId);
}

// Render documents for actor
function renderDocuments(actorId) {
  const container = document.getElementById('documents-grid');
  if (!container) return;
  
  const actorDocs = actorViews[actorId] || [];
  
  if (actorDocs.length === 0) {
    container.innerHTML = '<p class="no-docs">No documents for this actor</p>';
    return;
  }
  
  container.innerHTML = actorDocs.map(docKey => {
    const info = docInfo[docKey];
    const doc = documents[docKey];
    
    if (!info || !doc) return '';
    
    return `
      <div class="document-card" onclick="showDocument('${docKey}')">
        <div class="doc-icon">${info.icon}</div>
        <div class="doc-title">${info.title}</div>
        <div class="doc-description">${info.description}</div>
      </div>
    `;
  }).join('');
}

// Show document modal
function showDocument(docKey) {
  currentDoc = docKey;
  const info = docInfo[docKey];
  const doc = documents[docKey];
  
  if (!info || !doc) return;
  
  const modal = document.getElementById('doc-modal');
  const title = document.getElementById('doc-modal-title');
  const content = document.getElementById('doc-modal-content');
  
  title.innerHTML = `${info.icon} ${info.title}`;
  content.innerHTML = `<pre class="json-display">${syntaxHighlight(JSON.stringify(doc, null, 2))}</pre>`;
  
  modal.style.display = 'flex';
}

// Close modal
function closeModal() {
  document.getElementById('doc-modal').style.display = 'none';
  currentDoc = null;
}

// Syntax highlighting for JSON
function syntaxHighlight(json) {
  json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\\.\d*)?(?:[eE][+\\-]?\d+)?)/g, function (match) {
    let cls = 'json-number';
    if (/^"/.test(match)) {
      if (/:$/.test(match)) {
        cls = 'json-key';
      } else {
        cls = 'json-string';
      }
    } else if (/true|false/.test(match)) {
      cls = 'json-boolean';
    } else if (/null/.test(match)) {
      cls = 'json-null';
    }
    return '<span class="' + cls + '">' + match + '</span>';
  });
}

// Render timeline
function renderTimeline() {
  const container = document.getElementById('timeline-view');
  if (!container) return;
  
  container.innerHTML = timeline.map(event => `
    <div class="timeline-event ${event.doc ? 'clickable' : ''}" 
         ${event.doc ? `onclick="showDocument('${event.doc}')"` : ''}>
      <div class="timeline-date">${event.date}</div>
      <div class="timeline-marker"></div>
      <div class="timeline-content">
        <strong>${event.event}</strong>
        <small>${event.actor}</small>
      </div>
    </div>
  `).join('');
}

// Close modal on escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && currentDoc) {
    closeModal();
  }
});

// Close modal on click outside
document.getElementById('doc-modal')?.addEventListener('click', (e) => {
  if (e.target.id === 'doc-modal') {
    closeModal();
  }
});

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initDemo);
} else {
  initDemo();
}
