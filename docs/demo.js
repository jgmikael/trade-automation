// Demo configuration
const API_BASE = 'http://localhost:5000';
const SCENARIO_ID = 'FINLAND_TO_JAPAN_GLUELAM_TIMBER';

// Document data structure (SHACL-based JSON)
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
        card.onclick = () => showDocument(docKey);
        
        card.innerHTML = `
            <div class="document-status ${statusClass}">${statusText}</div>
            <h3>${doc.title}</h3>
            <div class="document-meta">
                Document #${doc.number} • ${doc.date}
            </div>
            <div class="document-preview">
                Type: ${doc.type}<br>
                Status: ${doc.status}<br>
                Click to view full KTDDE JSON document
            </div>
        `;
        
        container.appendChild(card);
    });
}

// Show document in modal
function showDocument(docKey) {
    const doc = documents[docKey];
    if (!doc) return;
    
    document.getElementById('modalTitle').textContent = `${doc.title} - ${doc.number}`;
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
    console.log('KTDDE Trade Demo loaded');
    console.log('Available documents:', Object.keys(documents));
});
