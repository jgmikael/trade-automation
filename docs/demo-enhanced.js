// Demo configuration
const API_BASE = 'http://localhost:5000';
const SCENARIO_ID = 'FINLAND_TO_JAPAN_GLUELAM_TIMBER';

// SAP source data (original ERP format)
const sapSourceData = {
    purchaseOrder: {
        EKKO: {
            EBELN: '4500001000',
            BUKRS: '1000',
            BSTYP: 'F',
            BSART: 'NB',
            AEDAT: '2023-12-15',
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
    
    billOfLading: {
        LIKP: {
            VBELN: '8000002000',
            LFART: 'ZLFD',
            VSTEL: '1000',
            KUNNR: '220001',
            KUNAG: '220001',
            ERDAT: '2024-02-08',
            LFDAT: '2024-02-08',
            WADAT: '2024-02-08',
            INCO1: 'CFR',
            INCO2: 'Tokyo Port',
            ROUTE: 'SEA-FI-JP',
            BTGEW: '28800.0',
            GEWEI: 'KG',
            VOLUM: '156.0',
            VOLEH: 'M3',
            BOLNR: 'FESCO2024FI123456'
        },
        LIPS: [
            {
                VBELN: '8000002000',
                POSNR: '000010',
                MATNR: 'TBR-GL-001',
                ARKTX: 'Gluelam Beam 90x315x12000mm GL30c',
                MATKL: 'TIMBER',
                LFIMG: '120',
                VRKME: 'EA',
                BRGEW: '145.0',
                NTGEW: '140.0',
                GEWEI: 'KG',
                WERKS: '1000',
                HERKL: 'FI'
            },
            {
                VBELN: '8000002000',
                POSNR: '000020',
                MATNR: 'TBR-GL-002',
                ARKTX: 'Gluelam Beam 115x405x15000mm GL32h',
                MATKL: 'TIMBER',
                LFIMG: '40',
                VRKME: 'EA',
                BRGEW: '285.0',
                NTGEW: '278.0',
                GEWEI: 'KG',
                WERKS: '1000',
                HERKL: 'FI'
            }
        ]
    },
    
    commercialInvoice: {
        VBRK: {
            VBELN: '9000002000',
            FKART: 'F2',
            FKTYP: 'F',
            KUNAG: '220001',
            KUNRG: '220001',
            ERDAT: '2024-02-10',
            FKDAT: '2024-02-10',
            ZTERM: 'LC60',
            ZBD1T: '60',
            WAERK: 'EUR',
            NETWR: '339000.00',
            MWSBK: '0.00',
            VBELN_REF: '0100002000',
            VBELN_DEL: '8000002000',
            INCO1: 'CFR',
            INCO2: 'Tokyo Port',
            LCNUM: 'LC-MUFG-FI-2024-05678',
            BOLNR: 'FESCO2024FI123456'
        },
        VBRP: [
            {
                VBELN: '9000002000',
                POSNR: '000010',
                MATNR: 'TBR-GL-001',
                ARKTX: 'Gluelam Beam 90x315x12000mm GL30c',
                MATKL: 'TIMBER',
                FKIMG: '120',
                VRKME: 'EA',
                NETWR: '234000.00',
                WAERK: 'EUR',
                MWSBP: '0.00',
                HERKL: 'FI'
            },
            {
                VBELN: '9000002000',
                POSNR: '000020',
                MATNR: 'TBR-GL-002',
                ARKTX: 'Gluelam Beam 115x405x15000mm GL32h',
                MATKL: 'TIMBER',
                FKIMG: '40',
                VRKME: 'EA',
                NETWR: '105000.00',
                WAERK: 'EUR',
                MWSBP: '0.00',
                HERKL: 'FI'
            }
        ]
    },
    
    documentaryCredit: {
        ZBANKF: {
            LCNUM: 'LC-MUFG-FI-2024-05678',
            LCTYPE: 'IRREVOCABLE_CONFIRMED',
            APPLICANT: '220001',
            BENEFICIARY: '110001',
            ISSUING_BANK: 'MUFGJPJT',
            ADVISING_BANK: 'NDEAFIHH',
            CONFIRMING_BANK: 'NDEAFIHH',
            LCAMOUNT: '339000.00',
            LCCURRENCY: 'EUR',
            ISSUE_DATE: '2024-01-15',
            EXPIRY_DATE: '2024-05-15',
            LATEST_SHIP_DATE: '2024-02-18',
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

// Transformation mappings (SAP field → KTDDE property)
const transformationMappings = {
    purchaseOrder: [
        { sap: 'EKKO.EBELN', ktdde: 'orderIdentifier', desc: 'Purchase order number' },
        { sap: 'EKKO.AEDAT', ktdde: 'orderDate', desc: 'Order date' },
        { sap: 'EKKO.KTWRT + EKKO.WAERS', ktdde: 'orderAmount{value,currencyCode}', desc: 'Total amount' },
        { sap: 'EKKO.INCO1 + INCO2', ktdde: 'deliveryTerms{incotermsCode,namedPlace}', desc: 'Incoterms' },
        { sap: 'EKPO.TXZ01', ktdde: 'hasItem[].productDescription', desc: 'Line item descriptions' },
        { sap: 'EKPO.MENGE + MEINS', ktdde: 'hasItem[].quantity', desc: 'Quantities with units' }
    ],
    billOfLading: [
        { sap: 'LIKP.BOLNR', ktdde: 'documentIdentifier', desc: 'B/L number' },
        { sap: 'LIKP.WADAT', ktdde: 'issueDate', desc: 'Issue date' },
        { sap: 'LIKP.BTGEW + GEWEI', ktdde: 'totalGrossWeight', desc: 'Total weight' },
        { sap: 'LIPS.ARKTX', ktdde: 'hasGoodsItem[].descriptionOfGoodsText', desc: 'Goods descriptions' },
        { sap: 'LIPS.HERKL', ktdde: 'hasGoodsItem[].originCountry', desc: 'Country of origin' },
        { sap: 'LIKP.INCO1 + INCO2', ktdde: 'deliveryTermsText', desc: 'Shipping terms' }
    ],
    commercialInvoice: [
        { sap: 'VBRK.VBELN', ktdde: 'invoiceNumber', desc: 'Invoice number' },
        { sap: 'VBRK.FKDAT', ktdde: 'invoiceDate', desc: 'Invoice date' },
        { sap: 'VBRK.NETWR + WAERK', ktdde: 'totalAmount', desc: 'Total amount' },
        { sap: 'VBRP.ARKTX', ktdde: 'hasInvoiceLine[].productDescription', desc: 'Line descriptions' },
        { sap: 'VBRK.BOLNR', ktdde: 'relatesToTransportDocument.documentIdentifier', desc: 'B/L reference' },
        { sap: 'VBRK.ZTERM', ktdde: 'invoicePaymentTerms.paymentTermsCode', desc: 'Payment terms' }
    ],
    documentaryCredit: [
        { sap: 'ZBANKF.LCNUM', ktdde: 'creditNumber', desc: 'L/C number' },
        { sap: 'ZBANKF.ISSUE_DATE', ktdde: 'issueDate', desc: 'Issue date' },
        { sap: 'ZBANKF.LCAMOUNT + LCCURRENCY', ktdde: 'creditAmount', desc: 'Credit amount' },
        { sap: 'ZBANKF.ISSUING_BANK', ktdde: 'issuingBankParty.swiftCode', desc: 'Issuing bank' },
        { sap: 'ZBANKF.PRES_DAYS', ktdde: 'presentationPeriodDays', desc: 'Presentation period' },
        { sap: 'ZBANKF.PARTIAL_SHIP', ktdde: 'partialShipmentAllowed', desc: 'Partial shipment flag' }
    ]
};

// Add SAP source to documents object (keeping existing structure, just adding sapSource)
const documents = {
    purchaseOrder: {
        id: 'PO-4500001000',
        type: 'PurchaseOrder',
        title: 'Purchase Order',
        number: '4500001000',
        date: 'T-60 days',
        status: 'created',
        visibleTo: ['buyer', 'seller', 'bank', 'customs'],
        createdBy: 'buyer',
        sapSource: sapSourceData.purchaseOrder,
        sapTables: ['EKKO (Header)', 'EKPO (Items)'],
        data: {
            '@type': 'PurchaseOrder',
            orderIdentifier: '4500001000',
            orderDate: '2023-12-15',
            buyerParty: {
                '@type': 'Party',
                partyName: 'Tokyo Construction Materials Ltd',
                hasAddress: {
                    '@type': 'Address',
                    street: '3-8-1 Shinjuku',
                    city: 'Tokyo',
                    postalCode: '160-0022',
                    country: { '@type': 'Country', countryCode: 'JP' }
                }
            },
            sellerParty: {
                '@type': 'Party',
                partyName: 'Nordic Timber Oy',
                hasAddress: {
                    '@type': 'Address',
                    street: 'Teollisuustie 12',
                    city: 'Kuhmo',
                    postalCode: '88900',
                    country: { '@type': 'Country', countryCode: 'FI' }
                }
            },
            orderAmount: {
                '@type': 'Amount',
                value: 285000.00,
                currencyCode: 'EUR'
            },
            deliveryTerms: {
                '@type': 'TradeDeliveryTerms',
                incotermsCode: 'CFR',
                namedPlace: 'Tokyo Port'
            },
            hasItem: [
                {
                    '@type': 'GoodsItem',
                    lineNumber: 10,
                    productDescription: 'Gluelam Beam 90x315x12000mm GL30c',
                    quantity: {
                        '@type': 'Quantity',
                        quantityValue: '120',
                        unitCode: 'EA'
                    },
                    unitPrice: {
                        '@type': 'Amount',
                        value: 1950.00,
                        currencyCode: 'EUR'
                    }
                },
                {
                    '@type': 'GoodsItem',
                    lineNumber: 20,
                    productDescription: 'Gluelam Beam 115x405x15000mm GL32h',
                    quantity: {
                        '@type': 'Quantity',
                        quantityValue: '40',
                        unitCode: 'EA'
                    },
                    unitPrice: {
                        '@type': 'Amount',
                        value: 2625.00,
                        currencyCode: 'EUR'
                    }
                }
            ]
        }
    },
    
    documentaryCredit: {
        id: 'LC-MUFG-FI-2024-05678',
        type: 'DocumentaryCredit',
        title: 'Letter of Credit',
        number: 'LC-MUFG-FI-2024-05678',
        date: 'T-30 days',
        status: 'created',
        visibleTo: ['buyer', 'seller', 'bank'],
        createdBy: 'bank',
        sapSource: sapSourceData.documentaryCredit,
        sapTables: ['ZBANKF (L/C Header)'],
        data: {
            '@type': 'DocumentaryCredit',
            creditNumber: 'LC-MUFG-FI-2024-05678',
            issueDate: '2024-01-15',
            expiryDate: '2024-05-15',
            creditAmount: {
                '@type': 'MonetaryAmount',
                amountValue: 339000.00,
                currencyCode: 'EUR'
            },
            applicantParty: {
                '@type': 'Party',
                partyName: 'Tokyo Construction Materials Ltd'
            },
            beneficiaryParty: {
                '@type': 'Party',
                partyName: 'Nordic Timber Oy'
            },
            issuingBankParty: {
                '@type': 'Bank',
                bankName: 'MUFG Bank Tokyo',
                swiftCode: 'MUFGJPJT'
            },
            advisingBankParty: {
                '@type': 'Bank',
                bankName: 'Nordea Bank Finland',
                swiftCode: 'NDEAFIHH'
            },
            confirmingBankParty: {
                '@type': 'Bank',
                bankName: 'Nordea Bank Finland',
                swiftCode: 'NDEAFIHH'
            },
            partialShipmentAllowed: false,
            transshipmentAllowed: true,
            presentationPeriodDays: 21,
            deliveryTerms: {
                '@type': 'TradeDeliveryTerms',
                incotermsCode: 'CFR',
                namedPlace: 'Tokyo Port'
            },
            requiresDocument: [
                { '@type': 'DocumentRequirement', documentType: 'Commercial Invoice' },
                { '@type': 'DocumentRequirement', documentType: 'Bill of Lading' },
                { '@type': 'DocumentRequirement', documentType: 'Packing List' },
                { '@type': 'DocumentRequirement', documentType: 'Certificate of Origin' },
                { '@type': 'DocumentRequirement', documentType: 'Phytosanitary Certificate' },
                { '@type': 'DocumentRequirement', documentType: 'Fumigation Certificate' }
            ]
        }
    },
    
    billOfLading: {
        id: 'BOL-FESCO2024FI123456',
        type: 'BillOfLading',
        title: 'Bill of Lading',
        number: 'FESCO2024FI123456',
        date: 'T-5 days',
        status: 'created',
        visibleTo: ['seller', 'buyer', 'bank', 'carrier', 'customs'],
        createdBy: 'carrier',
        sapSource: sapSourceData.billOfLading,
        sapTables: ['LIKP (Delivery Header)', 'LIPS (Delivery Items)'],
        data: {
            '@type': 'BillOfLading',
            documentIdentifier: 'FESCO2024FI123456',
            issueDate: '2024-02-08',
            carrierParty: {
                '@type': 'Party',
                partyName: 'Far Eastern Shipping Company (FESCO)'
            },
            consignorParty: {
                '@type': 'Party',
                partyName: 'Nordic Timber Oy',
                hasAddress: {
                    '@type': 'Address',
                    city: 'Kuhmo',
                    country: { '@type': 'Country', countryCode: 'FI' }
                }
            },
            consigneeParty: {
                '@type': 'Party',
                partyName: 'Tokyo Construction Materials Ltd',
                hasAddress: {
                    '@type': 'Address',
                    city: 'Tokyo',
                    country: { '@type': 'Country', countryCode: 'JP' }
                }
            },
            portOfLoadingUNLocode: 'FIRAU',
            portOfDischargeUNLocode: 'JPTYO',
            placeOfLoading: {
                '@type': 'Location',
                locationName: 'Rauma Port, Finland'
            },
            placeOfDischarge: {
                '@type': 'Location',
                locationName: 'Tokyo Port, Japan'
            },
            hasGoodsItem: [
                {
                    '@type': 'GoodsItem',
                    descriptionOfGoodsText: 'Gluelam Beam 90x315x12000mm GL30c - 120 pieces',
                    grossWeight: {
                        '@type': 'Quantity',
                        quantityValue: '17400',
                        unitCode: 'KG'
                    },
                    originCountry: {
                        '@type': 'Country',
                        countryCode: 'FI'
                    }
                },
                {
                    '@type': 'GoodsItem',
                    descriptionOfGoodsText: 'Gluelam Beam 115x405x15000mm GL32h - 40 pieces',
                    grossWeight: {
                        '@type': 'Quantity',
                        quantityValue: '11400',
                        unitCode: 'KG'
                    },
                    originCountry: {
                        '@type': 'Country',
                        countryCode: 'FI'
                    }
                }
            ],
            totalGrossWeight: {
                '@type': 'Quantity',
                quantityValue: '28800',
                unitCode: 'KG'
            },
            deliveryTermsText: 'CFR Tokyo Port',
            actualDepartureDateTime: '2024-02-08T08:00:00Z'
        }
    },
    
    commercialInvoice: {
        id: 'INV-9000002000',
        type: 'CommercialInvoice',
        title: 'Commercial Invoice',
        number: '9000002000',
        date: 'T-3 days',
        status: 'created',
        visibleTo: ['seller', 'buyer', 'bank', 'customs'],
        createdBy: 'seller',
        sapSource: sapSourceData.commercialInvoice,
        sapTables: ['VBRK (Billing Header)', 'VBRP (Billing Items)'],
        data: {
            '@type': 'CommercialInvoice',
            invoiceNumber: '9000002000',
            invoiceDate: '2024-02-10',
            buyerParty: {
                '@type': 'Party',
                partyName: 'Tokyo Construction Materials Ltd',
                hasAddress: {
                    '@type': 'Address',
                    street: '3-8-1 Shinjuku',
                    city: 'Tokyo',
                    postalCode: '160-0022',
                    country: { '@type': 'Country', countryCode: 'JP' }
                }
            },
            sellerParty: {
                '@type': 'Party',
                partyName: 'Nordic Timber Oy',
                hasAddress: {
                    '@type': 'Address',
                    street: 'Teollisuustie 12',
                    city: 'Kuhmo',
                    postalCode: '88900',
                    country: { '@type': 'Country', countryCode: 'FI' }
                }
            },
            totalAmount: {
                '@type': 'MonetaryAmount',
                amountValue: 339000.00,
                currencyCode: 'EUR'
            },
            deliveryTerms: {
                '@type': 'TradeDeliveryTerms',
                incotermsCode: 'CFR',
                namedPlace: 'Tokyo Port'
            },
            hasInvoiceLine: [
                {
                    '@type': 'InvoiceLine',
                    lineNumber: 10,
                    productDescription: 'Gluelam Beam 90x315x12000mm GL30c',
                    quantity: {
                        '@type': 'Quantity',
                        quantityValue: '120',
                        unitCode: 'EA'
                    },
                    lineAmount: {
                        '@type': 'MonetaryAmount',
                        amountValue: 234000.00,
                        currencyCode: 'EUR'
                    }
                },
                {
                    '@type': 'InvoiceLine',
                    lineNumber: 20,
                    productDescription: 'Gluelam Beam 115x405x15000mm GL32h',
                    quantity: {
                        '@type': 'Quantity',
                        quantityValue: '40',
                        unitCode: 'EA'
                    },
                    lineAmount: {
                        '@type': 'MonetaryAmount',
                        amountValue: 105000.00,
                        currencyCode: 'EUR'
                    }
                }
            ],
            relatesToTransportDocument: {
                '@type': 'TransportDocument',
                documentIdentifier: 'FESCO2024FI123456'
            },
            invoicePaymentTerms: {
                '@type': 'PaymentTerms',
                paymentTermsCode: 'LC60'
            }
        }
    },
    
    certificateOfOrigin: {
        id: 'COO-FI-2024-0234',
        type: 'CertificateOfOrigin',
        title: 'Certificate of Origin',
        number: 'COO-FI-2024-0234',
        date: 'T-3 days',
        status: 'created',
        visibleTo: ['seller', 'buyer', 'customs', 'chamber'],
        createdBy: 'chamber',
        sapSource: null, // Derived from multiple sources
        sapTables: ['Derived from Delivery + Invoice data'],
        data: {
            '@type': 'CertificateOfOrigin',
            certificateNumber: 'COO-FI-2024-0234',
            issueDate: '2024-02-10',
            exporterParty: {
                '@type': 'Party',
                partyName: 'Nordic Timber Oy',
                hasAddress: {
                    '@type': 'Address',
                    city: 'Kuhmo',
                    country: { '@type': 'Country', countryCode: 'FI' }
                }
            },
            importerParty: {
                '@type': 'Party',
                partyName: 'Tokyo Construction Materials Ltd',
                hasAddress: {
                    '@type': 'Address',
                    city: 'Tokyo',
                    country: { '@type': 'Country', countryCode: 'JP' }
                }
            },
            issuingAuthorityParty: {
                '@type': 'Party',
                partyName: 'Finnish Chamber of Commerce'
            },
            issuerParty: {
                '@type': 'Party',
                partyName: 'Authorized Officer - FCC'
            },
            hasGoodsItem: [
                {
                    '@type': 'GoodsItem',
                    descriptionOfGoods: 'Engineered gluelam timber beams for construction',
                    grossWeight: {
                        '@type': 'Quantity',
                        quantityValue: '28800',
                        unitCode: 'KG'
                    },
                    originCountry: {
                        '@type': 'Country',
                        countryCode: 'FI'
                    },
                    commodityClassification: {
                        '@type': 'CommodityClassification',
                        classificationCode: '4418.91'
                    }
                }
            ],
            invoiceNumber: '9000002000',
            transportDocumentNumber: 'FESCO2024FI123456'
        }
    }
};

// Actor document assignments
const actorDocuments = {
    buyer: ['purchaseOrder', 'documentaryCredit', 'billOfLading', 'commercialInvoice', 'certificateOfOrigin'],
    seller: ['purchaseOrder', 'documentaryCredit', 'billOfLading', 'commercialInvoice', 'certificateOfOrigin'],
    bank: ['purchaseOrder', 'documentaryCredit', 'commercialInvoice'],
    carrier: ['billOfLading'],
    customs: ['purchaseOrder', 'billOfLading', 'commercialInvoice', 'certificateOfOrigin'],
    chamber: ['certificateOfOrigin']
};

// Show actor view
function showActor(actorId) {
    // Update tabs
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');
    
    // Update views
    document.querySelectorAll('.actor-view').forEach(view => view.classList.remove('active'));
    document.getElementById(actorId).classList.add('active');
    
    // Load documents if not timeline
    if (actorId !== 'timeline') {
        loadActorDocuments(actorId);
    }
}

// Load documents for specific actor
function loadActorDocuments(actorId) {
    const container = document.getElementById(`${actorId}-docs`);
    container.innerHTML = '';
    
    const actorDocs = actorDocuments[actorId] || [];
    actorDocs.forEach(docKey => {
        const doc = documents[docKey];
        if (!doc) return;
        
        const statusClass = doc.createdBy === actorId ? 'status-created' : 'status-received';
        const statusText = doc.createdBy === actorId ? 'Created' : 'Received';
        
        const card = document.createElement('div');
        card.className = 'document-card';
        
        card.innerHTML = `
            <div class="document-status ${statusClass}">${statusText}</div>
            <h3>${doc.title}</h3>
            <div class="document-meta">
                Document #${doc.number} • ${doc.date}
            </div>
            <div class="document-preview">
                Type: ${doc.type}<br>
                SAP Tables: ${doc.sapTables ? doc.sapTables.join(', ') : 'N/A'}<br>
                <button class="sap-button" onclick="showSAPSource('${docKey}'); event.stopPropagation();">📊 View SAP Source</button>
                <button class="transform-button" onclick="showTransformation('${docKey}'); event.stopPropagation();">🔄 Show Transformation</button>
            </div>
        `;
        
        card.onclick = () => showDocument(docKey);
        container.appendChild(card);
    });
}

// Show SAP source data
function showSAPSource(docKey) {
    const doc = documents[docKey];
    if (!doc || !doc.sapSource) {
        alert('No SAP source data available for this document.');
        return;
    }
    
    document.getElementById('modalTitle').textContent = `SAP Source Data - ${doc.title}`;
    document.getElementById('modalContent').innerHTML = `
        <div style="margin-bottom: 20px; padding: 15px; background: #f0f9ff; border-left: 4px solid #3b82f6; border-radius: 6px;">
            <strong>SAP Tables:</strong> ${doc.sapTables.join(', ')}<br>
            <strong>Document:</strong> ${doc.title} #${doc.number}
        </div>
        ${formatJSON(doc.sapSource)}
    `;
    document.getElementById('documentModal').classList.add('active');
}

// Show transformation process
function showTransformation(docKey) {
    const doc = documents[docKey];
    const mappings = transformationMappings[docKey];
    
    if (!mappings) {
        alert('Transformation mapping not available for this document.');
        return;
    }
    
    document.getElementById('modalTitle').textContent = `SAP → KTDDE Transformation - ${doc.title}`;
    
    let transformHTML = `
        <div style="margin-bottom: 20px; padding: 15px; background: #f0f9ff; border-left: 4px solid #3b82f6; border-radius: 6px;">
            <h3 style="margin-top: 0;">Transformation Process</h3>
            <p>Converting SAP ERP data to KTDDE standardized JSON</p>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr auto 1fr; gap: 15px; align-items: center; margin-bottom: 30px;">
            <div style="text-align: center; padding: 20px; background: #fef3c7; border-radius: 8px;">
                <div style="font-size: 2em; margin-bottom: 10px;">📊</div>
                <strong>SAP ERP</strong><br>
                <span style="font-size: 0.9em; color: #666;">${doc.sapTables.join(', ')}</span>
            </div>
            <div style="font-size: 2em; color: #3b82f6;">→</div>
            <div style="text-align: center; padding: 20px; background: #d1fae5; border-radius: 8px;">
                <div style="font-size: 2em; margin-bottom: 10px;">📄</div>
                <strong>KTDDE JSON</strong><br>
                <span style="font-size: 0.9em; color: #666;">${doc.type}</span>
            </div>
        </div>
        
        <h3 style="margin-bottom: 15px;">Field Mappings:</h3>
        <div style="background: #f9fafb; border-radius: 8px; padding: 20px;">
    `;
    
    mappings.forEach((mapping, i) => {
        transformHTML += `
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
    
    transformHTML += `
        </div>
        <div style="margin-top: 20px; text-align: center;">
            <button onclick="showSAPSource('${docKey}')" style="margin-right: 10px; padding: 10px 20px; background: #fef3c7; border: 2px solid #f59e0b; border-radius: 6px; cursor: pointer; font-weight: 600;">View SAP Source</button>
            <button onclick="showDocument('${docKey}')" style="padding: 10px 20px; background: #d1fae5; border: 2px solid #10b981; border-radius: 6px; cursor: pointer; font-weight: 600;">View KTDDE Result</button>
        </div>
    `;
    
    document.getElementById('modalContent').innerHTML = transformHTML;
    document.getElementById('documentModal').classList.add('active');
}

// Show document in modal
function showDocument(docKey) {
    const doc = documents[docKey];
    if (!doc) return;
    
    document.getElementById('modalTitle').textContent = `KTDDE Document - ${doc.title} - ${doc.number}`;
    document.getElementById('modalContent').innerHTML = formatJSON(doc.data);
    document.getElementById('documentModal').classList.add('active');
}

// Close modal
function closeModal() {
    document.getElementById('documentModal').classList.remove('active');
}

// Format JSON with syntax highlighting
function formatJSON(obj, indent = 0) {
    const spaces = '  '.repeat(indent);
    const nextSpaces = '  '.repeat(indent + 1);
    
    if (typeof obj !== 'object' || obj === null) {
        if (typeof obj === 'string') {
            return `<span class="json-string">"${escapeHtml(obj)}"</span>`;
        } else if (typeof obj === 'number') {
            return `<span class="json-number">${obj}</span>`;
        } else if (typeof obj === 'boolean') {
            return `<span class="json-boolean">${obj}</span>`;
        }
        return String(obj);
    }
    
    if (Array.isArray(obj)) {
        if (obj.length === 0) return '[]';
        let result = '[\n';
        obj.forEach((item, i) => {
            result += nextSpaces + formatJSON(item, indent + 1);
            if (i < obj.length - 1) result += ',';
            result += '\n';
        });
        result += spaces + ']';
        return result;
    }
    
    const keys = Object.keys(obj);
    if (keys.length === 0) return '{}';
    
    let result = '{\n';
    keys.forEach((key, i) => {
        result += nextSpaces;
        result += `<span class="json-key">"${escapeHtml(key)}"</span>: `;
        result += formatJSON(obj[key], indent + 1);
        if (i < keys.length - 1) result += ',';
        result += '\n';
    });
    result += spaces + '}';
    return result;
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Close modal on outside click
window.onclick = function(event) {
    const modal = document.getElementById('documentModal');
    if (event.target === modal) {
        closeModal();
    }
};

// Initialize on load
window.addEventListener('DOMContentLoaded', () => {
    console.log('KTDDE Trade Demo (Enhanced) loaded');
    console.log('Available documents:', Object.keys(documents));
    console.log('SAP source data available for:', Object.keys(sapSourceData));
});
