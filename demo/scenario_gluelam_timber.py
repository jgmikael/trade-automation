"""
Demo Scenario: Finnish Gluelam Timber Export to Japan

Realistic trade scenario for browser-based demonstration.
"""

from datetime import date, timedelta
from decimal import Decimal
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sap-simulator'))

from models.sap_structures import (
    EKKO, EKPO, VBAK, VBAP, LIKP, LIPS, VBRK, VBRP,
    ZBANKF, Partner, Material
)


# ============================================================================
# Master Data - Gluelam Timber Scenario
# ============================================================================

PARTNERS_TIMBER = {
    # Finnish Exporter
    "110001": Partner(
        PARTNER_NUM="110001",
        PARTNER_TYPE="CUSTOMER",  # From SAP perspective
        NAME1="Nordic Timber Oy",
        NAME2="Suomalainen Puutavara",
        STREET="Teollisuustie 12",
        CITY="Kuhmo",
        POST_CODE="88900",
        COUNTRY="FI",
        TEL_NUMBER="+358 8 6551 2000",
        EMAIL="export@nordictimber.fi",
        STCEG="FI98765432",
        SWIFT="NORTFIHH",
        BANKN="FI21 1234 5600 0007 85",
    ),
    
    # Japanese Importer
    "220001": Partner(
        PARTNER_NUM="220001",
        PARTNER_TYPE="CUSTOMER",
        NAME1="Tokyo Construction Materials Ltd",
        NAME2="東京建材株式会社",
        STREET="3-8-1 Shinjuku",
        CITY="Tokyo",
        POST_CODE="160-0022",
        COUNTRY="JP",
        TEL_NUMBER="+81 3 5321 8888",
        EMAIL="import@tcm.co.jp",
        STCD1="1234567890123",
        SWIFT="TOKMJPJT",
    ),
}


MATERIALS_TIMBER = {
    "TBR-GL-001": Material(
        MATNR="TBR-GL-001",
        MAKTX="Gluelam Beam 90x315x12000mm GL30c",
        MATKL="TIMBER",
        MEINS="EA",  # Each (per beam)
        BRGEW=Decimal("145.0"),  # kg per beam
        NTGEW=Decimal("140.0"),
        GEWEI="KG",
        HSNCODE="4418.91",  # HS Code: Builders' joinery of wood
        HERKL="FI",
    ),
    
    "TBR-GL-002": Material(
        MATNR="TBR-GL-002",
        MAKTX="Gluelam Beam 115x405x15000mm GL32h",
        MATKL="TIMBER",
        MEINS="EA",
        BRGEW=Decimal("285.0"),
        NTGEW=Decimal("278.0"),
        GEWEI="KG",
        HSNCODE="4418.91",
        HERKL="FI",
    ),
    
    "TBR-ACC-001": Material(
        MATNR="TBR-ACC-001",
        MAKTX="Steel Connection Plates for Gluelam",
        MATKL="ACCESSORIES",
        MEINS="SET",
        BRGEW=Decimal("8.5"),
        NTGEW=Decimal("8.0"),
        GEWEI="KG",
        HSNCODE="7326.90",  # Other articles of iron or steel
        HERKL="FI",
    ),
}


def scenario_finland_japan_gluelam():
    """
    Finnish gluelam timber manufacturer exports construction beams to Japan.
    Uses CFR Incoterms (Cost and Freight), Letter of Credit payment.
    
    Timeline:
    - T-60: PO received from Japan
    - T-50: Sales Order created
    - T-30: L/C opened
    - T-10: Production complete, goods ready
    - T-5: Delivery/shipment
    - T-3: Invoice issued
    - T+0: Today (goods in transit)
    - T+45: Expected arrival Tokyo
    """
    today = date.today()
    
    # Purchase Order from Japanese customer
    po_header = EKKO(
        EBELN="4500001000",
        BUKRS="1000",
        BSTYP="F",
        BSART="NB",
        AEDAT=today - timedelta(days=60),
        LIFNR="110001",  # Nordic Timber
        EKORG="1000",
        EKGRP="002",
        WAERS="EUR",
        ZTERM="LC60",  # Letter of Credit, 60 days
        INCO1="CFR",  # Cost and Freight
        INCO2="Tokyo Port",
        KTWRT=Decimal("285000.00"),
        IHREZ="TCM-PO-2024-1089",
    )
    
    po_items = [
        EKPO(
            EBELN="4500001000",
            EBELP="00010",
            MATNR="TBR-GL-001",
            TXZ01="Gluelam Beam 90x315x12000mm GL30c",
            MATKL="TIMBER",
            MENGE=Decimal("120"),  # 120 beams
            MEINS="EA",
            NETPR=Decimal("1950.00"),  # EUR per beam
            PEINH=Decimal("1"),
            WAERS="EUR",
            EINDT=today + timedelta(days=45),
            WERKS="1000",
            LAND1="FI",
        ),
        EKPO(
            EBELN="4500001000",
            EBELP="00020",
            MATNR="TBR-GL-002",
            TXZ01="Gluelam Beam 115x405x15000mm GL32h",
            MATKL="TIMBER",
            MENGE=Decimal("40"),  # 40 beams
            MEINS="EA",
            NETPR=Decimal("2625.00"),
            PEINH=Decimal("1"),
            WAERS="EUR",
            EINDT=today + timedelta(days=45),
            WERKS="1000",
            LAND1="FI",
        ),
    ]
    
    # Sales Order
    so_header = VBAK(
        VBELN="0100002000",
        VKORG="1000",
        VTWEG="10",
        SPART="00",
        VBTYP="C",
        AUART="ZEXP",
        KUNNR="220001",  # Tokyo Construction
        ERDAT=today - timedelta(days=50),
        AUDAT=today - timedelta(days=50),
        VDATU=today + timedelta(days=45),
        WAERK="EUR",
        NETWR=Decimal("285000.00"),
        ZTERM="LC60",
        INCO1="CFR",
        INCO2="Tokyo Port",
        BSTNK="TCM-PO-2024-1089",
        BSTDK=today - timedelta(days=60),
        LCNUM="LC-MUFG-FI-2024-05678",
    )
    
    so_items = [
        VBAP(
            VBELN="0100002000",
            POSNR="000010",
            MATNR="TBR-GL-001",
            ARKTX="Gluelam Beam 90x315x12000mm GL30c",
            MATKL="TIMBER",
            KWMENG=Decimal("120"),
            VRKME="EA",
            NETWR=Decimal("234000.00"),
            WAERK="EUR",
            NETPR=Decimal("1950.00"),
            WERKS="1000",
        ),
        VBAP(
            VBELN="0100002000",
            POSNR="000020",
            MATNR="TBR-GL-002",
            ARKTX="Gluelam Beam 115x405x15000mm GL32h",
            MATKL="TIMBER",
            KWMENG=Decimal("40"),
            VRKME="EA",
            NETWR=Decimal("105000.00"),
            WAERK="EUR",
            NETPR=Decimal("2625.00"),
            WERKS="1000",
        ),
    ]
    
    # Delivery
    delivery_header = LIKP(
        VBELN="8000002000",
        LFART="ZLFD",
        VSTEL="1000",
        KUNNR="220001",
        KUNAG="220001",
        ERDAT=today - timedelta(days=5),
        LFDAT=today - timedelta(days=5),
        WADAT=today - timedelta(days=5),
        INCO1="CFR",
        INCO2="Tokyo Port",
        ROUTE="SEA-FI-JP",
        BTGEW=Decimal("28800.0"),  # 120×145kg + 40×285kg = 28,800kg
        GEWEI="KG",
        VOLUM=Decimal("156.0"),  # cubic meters
        VOLEH="M3",
        BOLNR="FESCO2024FI123456",  # Far Eastern Shipping Company
    )
    
    delivery_items = [
        LIPS(
            VBELN="8000002000",
            POSNR="000010",
            MATNR="TBR-GL-001",
            ARKTX="Gluelam Beam 90x315x12000mm GL30c",
            MATKL="TIMBER",
            LFIMG=Decimal("120"),
            VRKME="EA",
            BRGEW=Decimal("145.0"),
            NTGEW=Decimal("140.0"),
            GEWEI="KG",
            WERKS="1000",
            HERKL="FI",
        ),
        LIPS(
            VBELN="8000002000",
            POSNR="000020",
            MATNR="TBR-GL-002",
            ARKTX="Gluelam Beam 115x405x15000mm GL32h",
            MATKL="TIMBER",
            LFIMG=Decimal("40"),
            VRKME="EA",
            BRGEW=Decimal("285.0"),
            NTGEW=Decimal("278.0"),
            GEWEI="KG",
            WERKS="1000",
            HERKL="FI",
        ),
    ]
    
    # Commercial Invoice
    invoice_header = VBRK(
        VBELN="9000002000",
        FKART="F2",
        FKTYP="F",
        KUNAG="220001",
        KUNRG="220001",
        ERDAT=today - timedelta(days=3),
        FKDAT=today - timedelta(days=3),
        ZTERM="LC60",
        ZBD1T=60,
        WAERK="EUR",
        NETWR=Decimal("339000.00"),  # Includes freight
        MWSBK=Decimal("0.00"),  # Export, no VAT
        VBELN_REF="0100002000",
        VBELN_DEL="8000002000",
        INCO1="CFR",
        INCO2="Tokyo Port",
        LCNUM="LC-MUFG-FI-2024-05678",
        BOLNR="FESCO2024FI123456",
    )
    
    invoice_items = [
        VBRP(
            VBELN="9000002000",
            POSNR="000010",
            MATNR="TBR-GL-001",
            ARKTX="Gluelam Beam 90x315x12000mm GL30c",
            MATKL="TIMBER",
            FKIMG=Decimal("120"),
            VRKME="EA",
            NETWR=Decimal("234000.00"),
            WAERK="EUR",
            MWSBP=Decimal("0.00"),
            HERKL="FI",
        ),
        VBRP(
            VBELN="9000002000",
            POSNR="000020",
            MATNR="TBR-GL-002",
            ARKTX="Gluelam Beam 115x405x15000mm GL32h",
            MATKL="TIMBER",
            FKIMG=Decimal("40"),
            VRKME="EA",
            NETWR=Decimal("105000.00"),
            WAERK="EUR",
            MWSBP=Decimal("0.00"),
            HERKL="FI",
        ),
    ]
    
    # Documentary Credit
    lc = ZBANKF(
        LCNUM="LC-MUFG-FI-2024-05678",
        LCTYPE="IRREVOCABLE_CONFIRMED",
        APPLICANT="220001",  # Tokyo Construction
        BENEFICIARY="110001",  # Nordic Timber
        ISSUING_BANK="MUFGJPJT",  # MUFG Bank Tokyo
        ADVISING_BANK="NDEAFIHH",  # Nordea Finland
        CONFIRMING_BANK="NDEAFIHH",
        LCAMOUNT=Decimal("339000.00"),
        LCCURRENCY="EUR",
        ISSUE_DATE=today - timedelta(days=30),
        EXPIRY_DATE=today + timedelta(days=90),
        LATEST_SHIP_DATE=today + timedelta(days=10),
        PARTIAL_SHIP=False,
        TRANSHIP=True,
        INCO1="CFR",
        INCO2="Tokyo Port",
        PRES_DAYS=21,
        DOCS_REQUIRED=[
            "Commercial Invoice",
            "Bill of Lading",
            "Packing List",
            "Certificate of Origin",
            "Phytosanitary Certificate",  # Required for wood products
            "Fumigation Certificate",
        ],
        PURCHASE_ORDER="TCM-PO-2024-1089",
        SALES_ORDER="0100002000",
    )
    
    return {
        "scenario": "FINLAND_TO_JAPAN_GLUELAM_TIMBER",
        "description": "Finnish gluelam timber manufacturer exports construction beams to Japan for large-scale building project",
        "product_description": "Engineered wood beams (gluelam) for commercial construction",
        "trade_value": "EUR 339,000",
        "incoterms": "CFR Tokyo Port",
        "payment": "Confirmed Irrevocable Letter of Credit (60 days)",
        "transport": "Sea freight via FESCO (Far Eastern Shipping Company)",
        "transit_time": "~45 days",
        "special_requirements": [
            "Phytosanitary Certificate (wood products)",
            "Fumigation Certificate (ISPM-15 standard)",
            "Structural engineering certification (GL30c/GL32h grades)",
        ],
        "purchase_order": {"header": po_header, "items": po_items},
        "sales_order": {"header": so_header, "items": so_items},
        "delivery": {"header": delivery_header, "items": delivery_items},
        "invoice": {"header": invoice_header, "items": invoice_items},
        "documentary_credit": lc,
        "parties": PARTNERS_TIMBER,
        "materials": MATERIALS_TIMBER,
    }


if __name__ == "__main__":
    import json
    from dataclasses import asdict
    
    scenario = scenario_finland_japan_gluelam()
    print(json.dumps({
        "scenario": scenario["scenario"],
        "description": scenario["description"],
        "product": scenario["product_description"],
        "value": scenario["trade_value"],
        "documents": list(scenario.keys())
    }, indent=2))
