#!/usr/bin/env python3
"""
Document flow definition: Who creates what, and what triggers next steps
"""

# Document flow with creators and dependencies
DOCUMENT_FLOW = {
    "purchase_order": {
        "order": 1,
        "creator": "buyer",
        "creator_name": "Buyer (Tokyo Construction)",
        "action": "Issues Purchase Order",
        "triggers": ["documentary_credit"],
        "dependencies": [],
        "description": "Buyer issues PO requesting 160 gluelam beams for EUR 285,000"
    },
    "documentary_credit": {
        "order": 2,
        "creator": "bank",
        "creator_name": "Buyer's Bank (MUFG Tokyo)",
        "action": "Opens Letter of Credit",
        "triggers": ["regulatory_certificate", "phytosanitary_certificate", "warehouse_receipt"],
        "dependencies": ["purchase_order"],
        "description": "Bank opens confirmed irrevocable L/C for EUR 339,000 valid 90 days"
    },
    "regulatory_certificate": {
        "order": 3,
        "creator": "certifier",
        "creator_name": "Certifier (TÜV SÜD)",
        "action": "Issues CE Marking Certificate",
        "triggers": ["warehouse_receipt"],
        "dependencies": ["documentary_credit"],
        "description": "CE certification for structural timber per EN 14080:2013"
    },
    "warehouse_receipt": {
        "order": 4,
        "creator": "seller",
        "creator_name": "Warehouse (Rauma Port)",
        "action": "Receives Goods at Port",
        "triggers": ["phytosanitary_certificate", "insurance_certificate"],
        "dependencies": ["regulatory_certificate", "documentary_credit"],
        "description": "Timber stored at export warehouse, ready for shipment"
    },
    "phytosanitary_certificate": {
        "order": 5,
        "creator": "certifier",
        "creator_name": "Authority (Finnish Food Authority)",
        "action": "Issues Phytosanitary Certificate",
        "triggers": ["insurance_certificate"],
        "dependencies": ["warehouse_receipt"],
        "description": "ISPM-15 heat treatment certification for wood products"
    },
    "insurance_certificate": {
        "order": 6,
        "creator": "seller",
        "creator_name": "Insurer (Nordic Marine Insurance)",
        "action": "Issues Insurance Certificate",
        "triggers": ["certificate_of_origin", "packing_list"],
        "dependencies": ["phytosanitary_certificate"],
        "description": "All Risks marine cargo insurance for EUR 373,000 (110% CIF)"
    },
    "certificate_of_origin": {
        "order": 7,
        "creator": "chamber",
        "creator_name": "Chamber (Finnish Chamber of Commerce)",
        "action": "Issues Certificate of Origin",
        "triggers": ["bill_of_lading", "commercial_invoice"],
        "dependencies": ["insurance_certificate"],
        "description": "Certifies goods originate from Finland"
    },
    "packing_list": {
        "order": 8,
        "creator": "seller",
        "creator_name": "Seller (Nordic Timber)",
        "action": "Creates Packing List",
        "triggers": ["bill_of_lading"],
        "dependencies": ["insurance_certificate"],
        "description": "Details of 8 timber bundles, 28.8 tons total"
    },
    "bill_of_lading": {
        "order": 9,
        "creator": "carrier",
        "creator_name": "Carrier (FESCO)",
        "action": "Issues Bill of Lading",
        "triggers": ["commercial_invoice", "customs_declaration_export", "sea_cargo_manifest"],
        "dependencies": ["certificate_of_origin", "packing_list"],
        "description": "Ocean B/L for MV Baltic Express, Rauma → Tokyo"
    },
    "commercial_invoice": {
        "order": 10,
        "creator": "seller",
        "creator_name": "Seller (Nordic Timber)",
        "action": "Issues Commercial Invoice",
        "triggers": ["customs_declaration_export"],
        "dependencies": ["bill_of_lading"],
        "description": "Invoice for EUR 339,000 (CFR terms)"
    },
    "customs_declaration_export": {
        "order": 11,
        "creator": "customs",
        "creator_name": "Customs (Finnish Customs)",
        "action": "Clears for Export",
        "triggers": ["sea_cargo_manifest"],
        "dependencies": ["bill_of_lading", "commercial_invoice"],
        "description": "Export declaration at Rauma Port customs"
    },
    "sea_cargo_manifest": {
        "order": 12,
        "creator": "carrier",
        "creator_name": "Carrier (FESCO)",
        "action": "Files Cargo Manifest",
        "triggers": ["payment_confirmation"],
        "dependencies": ["customs_declaration_export", "bill_of_lading"],
        "description": "Vessel manifest filed, cargo loaded and sailing"
    },
    "payment_confirmation": {
        "order": 13,
        "creator": "bank",
        "creator_name": "Bank (MUFG/Nordea)",
        "action": "Processes L/C Payment",
        "triggers": ["customs_declaration_import"],
        "dependencies": ["sea_cargo_manifest"],
        "description": "Documents presented, L/C payment released (EUR 339,000)"
    },
    "customs_declaration_import": {
        "order": 14,
        "creator": "customs",
        "creator_name": "Customs (Japanese Customs)",
        "action": "Clears for Import",
        "triggers": ["delivery_note"],
        "dependencies": ["payment_confirmation"],
        "description": "Import clearance at Tokyo Port (zero duty under EU-Japan EPA)"
    },
    "delivery_note": {
        "order": 15,
        "creator": "buyer",
        "creator_name": "Logistics (Tokyo Logistics)",
        "action": "Delivers to Construction Site",
        "triggers": [],
        "dependencies": ["customs_declaration_import"],
        "description": "Final delivery to buyer's construction site warehouse"
    }
}

# Actor colors for visualization
ACTOR_COLORS = {
    "buyer": "#3b82f6",      # Blue
    "seller": "#10b981",     # Green
    "bank": "#f59e0b",       # Orange
    "carrier": "#06b6d4",    # Cyan
    "customs": "#8b5cf6",    # Purple
    "chamber": "#ec4899",    # Pink
    "certifier": "#14b8a6"   # Teal
}

# Stages of the trade process
PROCESS_STAGES = [
    {
        "name": "Negotiation & Contract",
        "docs": ["purchase_order", "documentary_credit"],
        "description": "Buyer and seller agree on terms; bank provides payment guarantee"
    },
    {
        "name": "Preparation & Certification",
        "docs": ["regulatory_certificate", "warehouse_receipt", "phytosanitary_certificate", "insurance_certificate"],
        "description": "Seller prepares goods, obtains required certificates and insurance"
    },
    {
        "name": "Documentation & Export",
        "docs": ["certificate_of_origin", "packing_list", "bill_of_lading", "commercial_invoice", "customs_declaration_export"],
        "description": "Export documents prepared, customs clearance, goods loaded"
    },
    {
        "name": "Transit & Payment",
        "docs": ["sea_cargo_manifest", "payment_confirmation"],
        "description": "Goods in transit, documents presented to bank, payment released"
    },
    {
        "name": "Import & Delivery",
        "docs": ["customs_declaration_import", "delivery_note"],
        "description": "Import clearance at destination, final delivery to buyer"
    }
]

if __name__ == "__main__":
    print(f"✅ Document flow defined: {len(DOCUMENT_FLOW)} documents")
    print(f"✅ Process stages: {len(PROCESS_STAGES)} stages")
    
    # Validate flow
    all_docs = set(DOCUMENT_FLOW.keys())
    for doc_key, doc_info in DOCUMENT_FLOW.items():
        for dep in doc_info["dependencies"]:
            if dep not in all_docs:
                print(f"⚠️  Warning: {doc_key} depends on unknown doc: {dep}")
        for trigger in doc_info["triggers"]:
            if trigger not in all_docs:
                print(f"⚠️  Warning: {doc_key} triggers unknown doc: {trigger}")
    
    print("\n📊 Document creation order:")
    for doc_key in sorted(DOCUMENT_FLOW.keys(), key=lambda k: DOCUMENT_FLOW[k]["order"]):
        info = DOCUMENT_FLOW[doc_key]
        print(f"  {info['order']:2d}. {info['creator_name']:35s} → {doc_key}")
