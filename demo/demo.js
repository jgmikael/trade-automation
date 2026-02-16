// demo.js - Finnish Gluelam Timber to Japan Trade Demo
// All 15 relevant KTDDE documents for the trade
// WITH INTERACTIVE DOCUMENT FLOW VISUALIZATION

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
    title: "Regulatory Certificate (CE)",
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
    "issueDate": "2026-01-01",
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
      "paymentDueDate": "2026-04-06"
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
    "issueDate": "2026-01-16",
    "expiryDate": "2026-04-16",
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
    "issueDate": "2026-02-05",
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
    "issueDate": "2026-02-05",
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
    "issueDate": "2026-02-05",
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
    "issueDate": "2026-02-05",
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
    "issueDate": "2026-02-03",
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
    "issueDate": "2026-02-04",
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
    "inspectionDate": "2026-02-03",
    "inspectorName": "Dr. Matti Virtanen"
  },
  "customs_declaration_export": {
    "@type": "CustomsDeclaration",
    "declarationNumber": "FI-EXP-2024-123456",
    "declarationType": "Export Declaration",
    "declarationDate": "2026-02-05",
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
    "declarationDate": "2026-03-22",
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
    "deliveryDate": "2026-03-25",
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
    "receivedDate": "2026-03-25",
    "referencePO": "4500001000",
    "referenceBL": "FESCO2024FI123456"
  },
  "regulatory_certificate": {
    "@type": "RegulatoryCertificate",
    "certificateNumber": "CE-GL-2024-0156",
    "issueDate": "2026-01-31",
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
    "issueDate": "2026-02-05",
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
    "issueDate": "2026-02-02",
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
    "storageStartDate": "2026-02-02",
    "storageEndDate": "2026-02-05",
    "releaseCondition": "Released for shipment on B/L FESCO2024FI123456"
  },
  "payment_confirmation": {
    "@type": "PaymentConfirmation",
    "confirmationNumber": "PAY-MUFG-2024-05678",
    "paymentDate": "2026-03-02",
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
    "valueDate": "2026-03-02"
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
    "date": "2026-01-01",
    "event": "Purchase Order Issued",
    "actor": "Buyer",
    "doc": "purchase_order"
  },
  {
    "date": "2026-01-16",
    "event": "Letter of Credit Opened",
    "actor": "Bank",
    "doc": "documentary_credit"
  },
  {
    "date": "2026-01-31",
    "event": "CE Certification Completed",
    "actor": "Certifier",
    "doc": "regulatory_certificate"
  },
  {
    "date": "2026-02-02",
    "event": "Goods Stored at Port Warehouse",
    "actor": "Warehouse",
    "doc": "warehouse_receipt"
  },
  {
    "date": "2026-02-03",
    "event": "Phytosanitary Inspection",
    "actor": "Authority",
    "doc": "phytosanitary_certificate"
  },
  {
    "date": "2026-02-03",
    "event": "Insurance Certificate Issued",
    "actor": "Insurer",
    "doc": "insurance_certificate"
  },
  {
    "date": "2026-02-04",
    "event": "Certificate of Origin Issued",
    "actor": "Chamber",
    "doc": "certificate_of_origin"
  },
  {
    "date": "2026-02-05",
    "event": "Goods Loaded & Shipped",
    "actor": "Carrier",
    "doc": "bill_of_lading"
  },
  {
    "date": "2026-02-05",
    "event": "Commercial Invoice Issued",
    "actor": "Seller",
    "doc": "commercial_invoice"
  },
  {
    "date": "2026-02-05",
    "event": "Packing List Created",
    "actor": "Seller",
    "doc": "packing_list"
  },
  {
    "date": "2026-02-05",
    "event": "Export Customs Clearance",
    "actor": "Customs",
    "doc": "customs_declaration_export"
  },
  {
    "date": "2026-02-05",
    "event": "Sea Cargo Manifest Filed",
    "actor": "Carrier",
    "doc": "sea_cargo_manifest"
  },
  {
    "date": "2026-03-02",
    "event": "Payment Processed",
    "actor": "Bank",
    "doc": "payment_confirmation"
  },
  {
    "date": "2026-03-22",
    "event": "Vessel Arrives Tokyo Port",
    "actor": "Carrier",
    "doc": null
  },
  {
    "date": "2026-03-22",
    "event": "Import Customs Clearance",
    "actor": "Customs",
    "doc": "customs_declaration_import"
  },
  {
    "date": "2026-03-25",
    "event": "Final Delivery to Buyer",
    "actor": "Logistics",
    "doc": "delivery_note"
  }
];

// Document flow (who creates what, dependencies, triggers)
const documentFlow = {
  "purchase_order": {
    "order": 1,
    "creator": "buyer",
    "creator_name": "Buyer (Tokyo Construction)",
    "action": "Issues Purchase Order",
    "triggers": [
      "documentary_credit"
    ],
    "dependencies": [],
    "description": "Buyer issues PO requesting 160 gluelam beams for EUR 285,000"
  },
  "documentary_credit": {
    "order": 2,
    "creator": "bank",
    "creator_name": "Buyer's Bank (MUFG Tokyo)",
    "action": "Opens Letter of Credit",
    "triggers": [
      "regulatory_certificate",
      "phytosanitary_certificate",
      "warehouse_receipt"
    ],
    "dependencies": [
      "purchase_order"
    ],
    "description": "Bank opens confirmed irrevocable L/C for EUR 339,000 valid 90 days"
  },
  "regulatory_certificate": {
    "order": 3,
    "creator": "certifier",
    "creator_name": "Certifier (TÜV SÜD)",
    "action": "Issues CE Marking Certificate",
    "triggers": [
      "warehouse_receipt"
    ],
    "dependencies": [
      "documentary_credit"
    ],
    "description": "CE certification for structural timber per EN 14080:2013"
  },
  "warehouse_receipt": {
    "order": 4,
    "creator": "seller",
    "creator_name": "Warehouse (Rauma Port)",
    "action": "Receives Goods at Port",
    "triggers": [
      "phytosanitary_certificate",
      "insurance_certificate"
    ],
    "dependencies": [
      "regulatory_certificate",
      "documentary_credit"
    ],
    "description": "Timber stored at export warehouse, ready for shipment"
  },
  "phytosanitary_certificate": {
    "order": 5,
    "creator": "certifier",
    "creator_name": "Authority (Finnish Food Authority)",
    "action": "Issues Phytosanitary Certificate",
    "triggers": [
      "insurance_certificate"
    ],
    "dependencies": [
      "warehouse_receipt"
    ],
    "description": "ISPM-15 heat treatment certification for wood products"
  },
  "insurance_certificate": {
    "order": 6,
    "creator": "seller",
    "creator_name": "Insurer (Nordic Marine Insurance)",
    "action": "Issues Insurance Certificate",
    "triggers": [
      "certificate_of_origin",
      "packing_list"
    ],
    "dependencies": [
      "phytosanitary_certificate"
    ],
    "description": "All Risks marine cargo insurance for EUR 373,000 (110% CIF)"
  },
  "certificate_of_origin": {
    "order": 7,
    "creator": "chamber",
    "creator_name": "Chamber (Finnish Chamber of Commerce)",
    "action": "Issues Certificate of Origin",
    "triggers": [
      "bill_of_lading",
      "commercial_invoice"
    ],
    "dependencies": [
      "insurance_certificate"
    ],
    "description": "Certifies goods originate from Finland"
  },
  "packing_list": {
    "order": 8,
    "creator": "seller",
    "creator_name": "Seller (Nordic Timber)",
    "action": "Creates Packing List",
    "triggers": [
      "bill_of_lading"
    ],
    "dependencies": [
      "insurance_certificate"
    ],
    "description": "Details of 8 timber bundles, 28.8 tons total"
  },
  "bill_of_lading": {
    "order": 9,
    "creator": "carrier",
    "creator_name": "Carrier (FESCO)",
    "action": "Issues Bill of Lading",
    "triggers": [
      "commercial_invoice",
      "customs_declaration_export",
      "sea_cargo_manifest"
    ],
    "dependencies": [
      "certificate_of_origin",
      "packing_list"
    ],
    "description": "Ocean B/L for MV Baltic Express, Rauma → Tokyo"
  },
  "commercial_invoice": {
    "order": 10,
    "creator": "seller",
    "creator_name": "Seller (Nordic Timber)",
    "action": "Issues Commercial Invoice",
    "triggers": [
      "customs_declaration_export"
    ],
    "dependencies": [
      "bill_of_lading"
    ],
    "description": "Invoice for EUR 339,000 (CFR terms)"
  },
  "customs_declaration_export": {
    "order": 11,
    "creator": "customs",
    "creator_name": "Customs (Finnish Customs)",
    "action": "Clears for Export",
    "triggers": [
      "sea_cargo_manifest"
    ],
    "dependencies": [
      "bill_of_lading",
      "commercial_invoice"
    ],
    "description": "Export declaration at Rauma Port customs"
  },
  "sea_cargo_manifest": {
    "order": 12,
    "creator": "carrier",
    "creator_name": "Carrier (FESCO)",
    "action": "Files Cargo Manifest",
    "triggers": [
      "payment_confirmation"
    ],
    "dependencies": [
      "customs_declaration_export",
      "bill_of_lading"
    ],
    "description": "Vessel manifest filed, cargo loaded and sailing"
  },
  "payment_confirmation": {
    "order": 13,
    "creator": "bank",
    "creator_name": "Bank (MUFG/Nordea)",
    "action": "Processes L/C Payment",
    "triggers": [
      "customs_declaration_import"
    ],
    "dependencies": [
      "sea_cargo_manifest"
    ],
    "description": "Documents presented, L/C payment released (EUR 339,000)"
  },
  "customs_declaration_import": {
    "order": 14,
    "creator": "customs",
    "creator_name": "Customs (Japanese Customs)",
    "action": "Clears for Import",
    "triggers": [
      "delivery_note"
    ],
    "dependencies": [
      "payment_confirmation"
    ],
    "description": "Import clearance at Tokyo Port (zero duty under EU-Japan EPA)"
  },
  "delivery_note": {
    "order": 15,
    "creator": "buyer",
    "creator_name": "Logistics (Tokyo Logistics)",
    "action": "Delivers to Construction Site",
    "triggers": [],
    "dependencies": [
      "customs_declaration_import"
    ],
    "description": "Final delivery to buyer's construction site warehouse"
  }
};

// Actor colors for visualization
const actorColors = {
  "buyer": "#3b82f6",
  "seller": "#10b981",
  "bank": "#f59e0b",
  "carrier": "#06b6d4",
  "customs": "#8b5cf6",
  "chamber": "#ec4899",
  "certifier": "#14b8a6"
};

// Process stages
const processStages = [
  {
    "name": "Negotiation & Contract",
    "docs": [
      "purchase_order",
      "documentary_credit"
    ],
    "description": "Buyer and seller agree on terms; bank provides payment guarantee"
  },
  {
    "name": "Preparation & Certification",
    "docs": [
      "regulatory_certificate",
      "warehouse_receipt",
      "phytosanitary_certificate",
      "insurance_certificate"
    ],
    "description": "Seller prepares goods, obtains required certificates and insurance"
  },
  {
    "name": "Documentation & Export",
    "docs": [
      "certificate_of_origin",
      "packing_list",
      "bill_of_lading",
      "commercial_invoice",
      "customs_declaration_export"
    ],
    "description": "Export documents prepared, customs clearance, goods loaded"
  },
  {
    "name": "Transit & Payment",
    "docs": [
      "sea_cargo_manifest",
      "payment_confirmation"
    ],
    "description": "Goods in transit, documents presented to bank, payment released"
  },
  {
    "name": "Import & Delivery",
    "docs": [
      "customs_declaration_import",
      "delivery_note"
    ],
    "description": "Import clearance at destination, final delivery to buyer"
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
let flowAnimationStep = 0;
let flowAnimationInterval = null;

// Initialize demo
function initDemo() {
  renderActorTabs();
  renderDocuments(currentActor);
  renderTimeline();
  renderDocumentFlow();
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
  const container = document.getElementById('timeline-events');
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

// Render document flow
function renderDocumentFlow() {
  const container = document.getElementById('flow-diagram');
  if (!container) return;
  
  // Get documents sorted by order
  const sortedDocs = Object.keys(documentFlow).sort((a, b) => 
    documentFlow[a].order - documentFlow[b].order
  );
  
  // Group by stage
  let html = '<div class="flow-stages">';
  
  processStages.forEach((stage, stageIdx) => {
    html += `
      <div class="flow-stage">
        <div class="stage-header">
          <div class="stage-number">${stageIdx + 1}</div>
          <div>
            <h3>${stage.name}</h3>
            <p>${stage.description}</p>
          </div>
        </div>
        <div class="stage-docs">
    `;
    
    stage.docs.forEach(docKey => {
      const flow = documentFlow[docKey];
      const info = docInfo[docKey];
      const color = actorColors[flow.creator];
      
      html += `
        <div class="flow-doc" 
             data-doc="${docKey}"
             data-order="${flow.order}"
             style="border-color: ${color};"
             onclick="showDocumentFlow('${docKey}')">
          <div class="flow-doc-header" style="background: ${color};">
            <div class="flow-doc-number">${flow.order}</div>
            <div class="flow-doc-icon">${info.icon}</div>
          </div>
          <div class="flow-doc-body">
            <div class="flow-doc-title">${info.title}</div>
            <div class="flow-doc-creator">${flow.creator_name}</div>
            <div class="flow-doc-action">${flow.action}</div>
          </div>
          ${flow.dependencies.length > 0 ? `
            <div class="flow-doc-deps">
              <small>Requires: ${flow.dependencies.length} doc(s)</small>
            </div>
          ` : ''}
          ${flow.triggers.length > 0 ? `
            <div class="flow-doc-triggers">
              <small>→ Triggers: ${flow.triggers.length} doc(s)</small>
            </div>
          ` : ''}
        </div>
      `;
    });
    
    html += `
        </div>
      </div>
    `;
    
    // Add stage connector
    if (stageIdx < processStages.length - 1) {
      html += '<div class="stage-connector">→</div>';
    }
  });
  
  html += '</div>';
  
  container.innerHTML = html;
}

// Show document in flow context
function showDocumentFlow(docKey) {
  const flow = documentFlow[docKey];
  const info = docInfo[docKey];
  const doc = documents[docKey];
  
  if (!flow || !info || !doc) return;
  
  const modal = document.getElementById('doc-modal');
  const title = document.getElementById('doc-modal-title');
  const content = document.getElementById('doc-modal-content');
  
  let flowInfo = `
    <div class="flow-info">
      <h3>📋 Document Flow Information</h3>
      <div class="flow-info-grid">
        <div class="flow-info-item">
          <strong>Order:</strong> #${flow.order} of 15
        </div>
        <div class="flow-info-item">
          <strong>Creator:</strong> ${flow.creator_name}
        </div>
        <div class="flow-info-item">
          <strong>Action:</strong> ${flow.action}
        </div>
        <div class="flow-info-item">
          <strong>Description:</strong> ${flow.description}
        </div>
      </div>
  `;
  
  if (flow.dependencies.length > 0) {
    flowInfo += `
      <div class="flow-dependencies">
        <h4>📥 Requires These Documents First:</h4>
        <ul>
          ${flow.dependencies.map(dep => `
            <li onclick="showDocumentFlow('${dep}')" style="cursor: pointer; color: #3b82f6;">
              ${docInfo[dep].icon} ${docInfo[dep].title}
            </li>
          `).join('')}
        </ul>
      </div>
    `;
  }
  
  if (flow.triggers.length > 0) {
    flowInfo += `
      <div class="flow-triggers">
        <h4>📤 Triggers Creation Of:</h4>
        <ul>
          ${flow.triggers.map(trig => `
            <li onclick="showDocumentFlow('${trig}')" style="cursor: pointer; color: #10b981;">
              ${docInfo[trig].icon} ${docInfo[trig].title}
            </li>
          `).join('')}
        </ul>
      </div>
    `;
  }
  
  flowInfo += '</div><hr>';
  
  title.innerHTML = `${info.icon} ${info.title} <span style="font-size: 0.6em; opacity: 0.8;">(#${flow.order})</span>`;
  content.innerHTML = flowInfo + `<pre class="json-display">${syntaxHighlight(JSON.stringify(doc, null, 2))}</pre>`;
  
  modal.style.display = 'flex';
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

// ============================================================================
// SAP SOURCE DATA AND TRANSFORMATION MAPPINGS
// ============================================================================

const sapSourceData = {
    purchase_order: {
        EKKO: {
            EBELN: '4500001000',
            BUKRS: '1000',
            BSTYP: 'F',
            BSART: 'NB',
            AEDAT: '2026-01-01',
            LIFNR: '110001',
            EKORG: '1000',
            EKGRP: '002',
            WAERS: 'EUR',
            ZTERM: 'LC60',
            INCO1: 'CFR',
            INCO2: 'Tokyo Port',
            KTWRT: '285000.00',
            IHREZ: 'TCM-PO-2024-1089'
        },
        EKPO: [
            {
                EBELN: '4500001000',
                EBELP: '00010',
                MATNR: 'TBR-GL-001',
                TXZ01: 'Gluelam Beam 90x315x12000mm GL30c',
                MATKL: 'TIMBER',
                MENGE: '120',
                MEINS: 'EA',
                NETPR: '1950.00',
                PEINH: '1',
                WAERS: 'EUR',
                LAND1: 'FI'
            },
            {
                EBELN: '4500001000',
                EBELP: '00020',
                MATNR: 'TBR-GL-002',
                TXZ01: 'Gluelam Beam 115x405x15000mm GL32h',
                MATKL: 'TIMBER',
                MENGE: '40',
                MEINS: 'EA',
                NETPR: '2625.00',
                PEINH: '1',
                WAERS: 'EUR',
                LAND1: 'FI'
            }
        ]
    },
    
    bill_of_lading: {
        LIKP: {
            VBELN: '8000002000',
            LFART: 'ZLFD',
            VSTEL: '1000',
            KUNNR: '220001',
            KUNAG: '220001',
            ERDAT: '2026-02-08',
            LFDAT: '2026-02-08',
            WADAT: '2026-02-08',
            INCO1: 'CFR',
            INCO2: 'Tokyo Port',
            ROUTE: 'SEA-FI-JP',
            BTGEW: '28800.0',
            GEWEI: 'KG',
            VOLUM: '156.0',
            VOLEH: 'M3',
            BOLNR: 'FESCO2026FI123456'
        }
    },
    
    commercial_invoice: {
        VBRK: {
            VBELN: '9000002000',
            FKART: 'F2',
            FKTYP: 'F',
            KUNAG: '220001',
            KUNRG: '220001',
            ERDAT: '2026-02-10',
            FKDAT: '2026-02-10',
            ZTERM: 'LC60',
            ZBD1T: '60',
            WAERK: 'EUR',
            NETWR: '339000.00',
            MWSBK: '0.00',
            VBELN_REF: '0100002000',
            VBELN_DEL: '8000002000',
            INCO1: 'CFR',
            INCO2: 'Tokyo Port',
            LCNUM: 'LC-MUFG-FI-2026-05678',
            BOLNR: 'FESCO2026FI123456'
        }
    },
    
    documentary_credit: {
        ZBANKF: {
            LCNUM: 'LC-MUFG-FI-2026-05678',
            LCTYPE: 'IRREVOCABLE_CONFIRMED',
            APPLICANT: '220001',
            BENEFICIARY: '110001',
            ISSUING_BANK: 'MUFGJPJT',
            ADVISING_BANK: 'NDEAFIHH',
            CONFIRMING_BANK: 'NDEAFIHH',
            LCAMOUNT: '339000.00',
            LCCURRENCY: 'EUR',
            ISSUE_DATE: '2026-01-15',
            EXPIRY_DATE: '2026-05-15',
            LATEST_SHIP_DATE: '2026-02-18',
            PARTIAL_SHIP: 'FALSE',
            TRANSHIP: 'TRUE',
            INCO1: 'CFR',
            INCO2: 'Tokyo Port',
            PRES_DAYS: '21',
            PURCHASE_ORDER: 'TCM-PO-2024-1089',
            SALES_ORDER: '0100002000'
        }
    }
};

const sapTableInfo = {
    purchase_order: ['EKKO (Header)', 'EKPO (Items)'],
    bill_of_lading: ['LIKP (Delivery Header)', 'LIPS (Delivery Items)'],
    commercial_invoice: ['VBRK (Billing Header)', 'VBRP (Billing Items)'],
    documentary_credit: ['ZBANKF (L/C Header)'],
    certificate_of_origin: ['Derived from Material Master'],
    packing_list: ['Derived from Delivery data']
};

const transformationMappings = {
    purchase_order: [
        { sap: 'EKKO.EBELN', ktdde: 'purchaseOrderNumber', desc: 'Purchase order number' },
        { sap: 'EKKO.AEDAT', ktdde: 'issueDate', desc: 'Order date' },
        { sap: 'EKKO.KTWRT + EKKO.WAERS', ktdde: 'totalAmount{value,currency}', desc: 'Total amount' },
        { sap: 'EKKO.INCO1 + INCO2', ktdde: 'deliveryTerms{incoterms,namedPlace}', desc: 'Incoterms' },
        { sap: 'EKPO.TXZ01', ktdde: 'goodsItems[].description', desc: 'Line item descriptions' },
        { sap: 'EKPO.MENGE + MEINS', ktdde: 'goodsItems[].quantity', desc: 'Quantities with units' }
    ],
    bill_of_lading: [
        { sap: 'LIKP.BOLNR', ktdde: 'billOfLadingNumber', desc: 'B/L number' },
        { sap: 'LIKP.WADAT', ktdde: 'issueDate', desc: 'Issue date' },
        { sap: 'LIKP.BTGEW + GEWEI', ktdde: 'totalGrossWeight', desc: 'Total weight' },
        { sap: 'LIKP.VOLUM + VOLEH', ktdde: 'totalVolume', desc: 'Total volume' },
        { sap: 'LIPS.ARKTX', ktdde: 'goodsItems[].description', desc: 'Goods descriptions' },
        { sap: 'LIKP.INCO1 + INCO2', ktdde: 'deliveryTerms', desc: 'Shipping terms' }
    ],
    commercial_invoice: [
        { sap: 'VBRK.VBELN', ktdde: 'invoiceNumber', desc: 'Invoice number' },
        { sap: 'VBRK.FKDAT', ktdde: 'issueDate', desc: 'Invoice date' },
        { sap: 'VBRK.NETWR + WAERK', ktdde: 'totalAmount', desc: 'Total amount' },
        { sap: 'VBRP.ARKTX', ktdde: 'invoiceLines[].description', desc: 'Line descriptions' },
        { sap: 'VBRK.BOLNR', ktdde: 'relatedDocuments.billOfLading', desc: 'B/L reference' },
        { sap: 'VBRK.ZTERM', ktdde: 'paymentTerms.code', desc: 'Payment terms' }
    ],
    documentary_credit: [
        { sap: 'ZBANKF.LCNUM', ktdde: 'creditNumber', desc: 'L/C number' },
        { sap: 'ZBANKF.ISSUE_DATE', ktdde: 'issueDate', desc: 'Issue date' },
        { sap: 'ZBANKF.LCAMOUNT + LCCURRENCY', ktdde: 'creditAmount', desc: 'Credit amount' },
        { sap: 'ZBANKF.ISSUING_BANK', ktdde: 'issuingBank.swiftCode', desc: 'Issuing bank' },
        { sap: 'ZBANKF.PRES_DAYS', ktdde: 'presentationPeriodDays', desc: 'Presentation period' },
        { sap: 'ZBANKF.PARTIAL_SHIP', ktdde: 'partialShipmentAllowed', desc: 'Partial shipment flag' }
    ]
};

// ============================================================================
// SAP DISPLAY FUNCTIONS
// ============================================================================

function showSAPSource(docKey) {
    const sapSource = sapSourceData[docKey];
    if (!sapSource) {
        alert('SAP source data not available for this document yet. Available for: Purchase Order, Bill of Lading, Commercial Invoice, Documentary Credit.');
        return;
    }
    
    const tables = sapTableInfo[docKey] || ['SAP Data'];
    
    const modal = document.getElementById('documentModal');
    const title = document.getElementById('modalTitle');
    const content = document.getElementById('modalContent');
    
    title.textContent = `SAP Source Data - ${docKey.replace(/_/g, ' ').toUpperCase()}`;
    
    content.innerHTML = `
        <div style="margin-bottom: 20px; padding: 15px; background: #fef3c7; border-left: 4px solid #f59e0b; border-radius: 6px;">
            <strong>SAP Tables:</strong> ${tables.join(', ')}<br>
            <strong>Document:</strong> ${docKey.replace(/_/g, ' ').toUpperCase()}
        </div>
        ${formatSAPData(sapSource)}
        <div style="margin-top: 20px; text-align: center;">
            <button onclick="showTransformation('${docKey}')" style="padding: 10px 20px; background: #3b82f6; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; margin-right: 10px;">View Transformation →</button>
            <button onclick="closeModal()" style="padding: 10px 20px; background: #6b7280; color: white; border: none; border-radius: 6px; cursor: pointer;">Close</button>
        </div>
    `;
    
    modal.classList.add('active');
}

function showTransformation(docKey) {
    const mappings = transformationMappings[docKey];
    
    if (!mappings) {
        alert('Transformation mapping not available for this document yet.');
        return;
    }
    
    const modal = document.getElementById('documentModal');
    const title = document.getElementById('modalTitle');
    const content = document.getElementById('modalContent');
    
    title.textContent = `SAP → KTDDE Transformation - ${docKey.replace(/_/g, ' ').toUpperCase()}`;
    
    const tables = sapTableInfo[docKey] || ['SAP Data'];
    
    let html = `
        <div style="margin-bottom: 20px; padding: 15px; background: #f0f9ff; border-left: 4px solid #3b82f6; border-radius: 6px;">
            <h3 style="margin-top: 0;">Transformation Process</h3>
            <p>Converting SAP ERP data to KTDDE standardized JSON</p>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr auto 1fr; gap: 15px; align-items: center; margin-bottom: 30px;">
            <div style="text-align: center; padding: 20px; background: #fef3c7; border-radius: 8px;">
                <div style="font-size: 2em; margin-bottom: 10px;">📊</div>
                <strong>SAP ERP</strong><br>
                <span style="font-size: 0.9em; color: #666;">${tables.join(', ')}</span>
            </div>
            <div style="font-size: 2em; color: #3b82f6;">→</div>
            <div style="text-align: center; padding: 20px; background: #d1fae5; border-radius: 8px;">
                <div style="font-size: 2em; margin-bottom: 10px;">📄</div>
                <strong>KTDDE JSON</strong><br>
                <span style="font-size: 0.9em; color: #666;">W3C VC</span>
            </div>
        </div>
        
        <h3 style="margin-bottom: 15px;">Field Mappings:</h3>
        <div style="background: #f9fafb; border-radius: 8px; padding: 20px;">
    `;
    
    mappings.forEach((mapping, i) => {
        html += `
            <div style="display: grid; grid-template-columns: 1fr auto 1fr; gap: 15px; align-items: center; padding: 15px; background: white; border-radius: 6px; margin-bottom: 10px; border: 2px solid #e5e7eb;">
                <div>
                    <code style="background: #fef3c7; padding: 4px 8px; border-radius: 4px; font-size: 0.9em;">${mapping.sap}</code>
                </div>
                <div style="color: #3b82f6; font-weight: bold;">➜</div>
                <div>
                    <code style="background: #d1fae5; padding: 4px 8px; border-radius: 4px; font-size: 0.9em;">${mapping.ktdde}</code>
                    <div style="font-size: 0.85em; color: #666; margin-top: 5px;">${mapping.desc}</div>
                </div>
            </div>
        `;
    });
    
    html += `
        </div>
        <div style="margin-top: 20px; text-align: center;">
            <button onclick="showSAPSource('${docKey}')" style="margin-right: 10px; padding: 10px 20px; background: #fef3c7; border: 2px solid #f59e0b; border-radius: 6px; cursor: pointer; font-weight: 600;">← View SAP Source</button>
            <button onclick="showDocument('${docKey}')" style="padding: 10px 20px; background: #d1fae5; border: 2px solid #10b981; border-radius: 6px; cursor: pointer; font-weight: 600;">View KTDDE Result →</button>
        </div>
    `;
    
    content.innerHTML = html;
    modal.classList.add('active');
}

function formatSAPData(data) {
    let html = '<div style="font-family: monospace; font-size: 0.9em; background: #f9fafb; padding: 20px; border-radius: 8px; overflow-x: auto;">';
    
    for (const [table, records] of Object.entries(data)) {
        html += `<div style="margin-bottom: 20px;">`;
        html += `<div style="background: #fef3c7; padding: 10px; border-radius: 4px; font-weight: bold; margin-bottom: 10px;">Table: ${table}</div>`;
        
        if (Array.isArray(records)) {
            records.forEach((record, idx) => {
                html += `<div style="margin-left: 20px; margin-bottom: 15px;">`;
                html += `<div style="color: #666; margin-bottom: 5px;">Record ${idx + 1}:</div>`;
                html += formatSAPRecord(record);
                html += `</div>`;
            });
        } else {
            html += formatSAPRecord(records);
        }
        
        html += `</div>`;
    }
    
    html += '</div>';
    return html;
}

function formatSAPRecord(record) {
    let html = '<div style="margin-left: 20px;">';
    for (const [field, value] of Object.entries(record)) {
        html += `<div style="padding: 4px 0;">`;
        html += `<span style="color: #f59e0b; font-weight: 600;">${field}:</span> `;
        html += `<span style="color: #374151;">${value}</span>`;
        html += `</div>`;
    }
    html += '</div>';
    return html;
}
