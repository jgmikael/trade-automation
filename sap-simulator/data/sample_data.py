"""
Realistic Sample Data for International Trade

Generates realistic SAP data for demonstration to:
- European Union
- Singapore (ICC DSI participant)
- Japan
- Other global trade actors

Scenarios cover machinery, electronics, and chemicals trade.
"""

from datetime import date, timedelta
from decimal import Decimal
from typing import Dict, List
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.sap_structures import (
    EKKO, EKPO, VBAK, VBAP, LIKP, LIPS, VBRK, VBRP,
    ZBANKF, Partner, Material
)


# ============================================================================
# MASTER DATA - Partners (Companies)
# ============================================================================

PARTNERS: Dict[str, Partner] = {
    # European Companies
    "100001": Partner(
        PARTNER_NUM="100001",
        PARTNER_TYPE="CUSTOMER",
        NAME1="Nordic Machinery Oy",
        STREET="Teollisuuskatu 15",
        CITY="Helsinki",
        POST_CODE="00510",
        COUNTRY="FI",
        TEL_NUMBER="+358 9 1234 5678",
        EMAIL="orders@nordicmachinery.fi",
        STCEG="FI12345678",
        SWIFT="NDEAFIHH",
    ),
    
    "100002": Partner(
        PARTNER_NUM="100002",
        PARTNER_TYPE="CUSTOMER",
        NAME1="Deutsche Elektronik GmbH",
        STREET="Industriestraße 42",
        CITY="Munich",
        POST_CODE="80331",
        REGION="BY",
        COUNTRY="DE",
        TEL_NUMBER="+49 89 1234 5678",
        EMAIL="procurement@de-elektronik.de",
        STCEG="DE123456789",
        SWIFT="DEUTDEMM",
    ),
    
    # Asian Companies
    "200001": Partner(
        PARTNER_NUM="200001",
        PARTNER_TYPE="CUSTOMER",
        NAME1="Singapore Trading Company Pte Ltd",
        STREET="1 Marina Boulevard",
        CITY="Singapore",
        POST_CODE="018989",
        COUNTRY="SG",
        TEL_NUMBER="+65 6123 4567",
        EMAIL="imports@sgtrade.com.sg",
        STCD1="199012345A",
        SWIFT="SGTRSGSG",
    ),
    
    "200002": Partner(
        PARTNER_NUM="200002",
        PARTNER_TYPE="CUSTOMER",
        NAME1="Tokyo Industrial Equipment Co Ltd",
        NAME2="東京工業設備株式会社",
        STREET="2-1-1 Marunouchi",
        CITY="Tokyo",
        POST_CODE="100-0005",
        COUNTRY="JP",
        TEL_NUMBER="+81 3 1234 5678",
        EMAIL="purchasing@tokyo-ind.co.jp",
        STCD1="1234567890123",
        SWIFT="TKIDJPJT",
    ),
    
    # Vendors (Suppliers)
    "300001": Partner(
        PARTNER_NUM="300001",
        PARTNER_TYPE="VENDOR",
        NAME1="European Components AB",
        STREET="Exportgatan 10",
        CITY="Stockholm",
        POST_CODE="11122",
        COUNTRY="SE",
        TEL_NUMBER="+46 8 1234 5678",
        EMAIL="sales@eurocomp.se",
        STCEG="SE123456789001",
        SWIFT="ECUPSESS",
        BANKN="12345678",
    ),
    
    "300002": Partner(
        PARTNER_NUM="300002",
        PARTNER_TYPE="VENDOR",
        NAME1="Asia Pacific Supplies Ltd",
        STREET="100 Orchard Road",
        CITY="Singapore",
        POST_CODE="238840",
        COUNTRY="SG",
        TEL_NUMBER="+65 6789 0123",
        EMAIL="export@apsupplies.sg",
        STCD1="200112345B",
        SWIFT="APSUSGSG",
    ),
}


# ============================================================================
# MASTER DATA - Materials
# ============================================================================

MATERIALS: Dict[str, Material] = {
    # Industrial Machinery
    "MAT-100001": Material(
        MATNR="MAT-100001",
        MAKTX="Industrial Servo Motor 5kW",
        MATKL="MACHINERY",
        MEINS="EA",
        BRGEW=Decimal("85.5"),
        NTGEW=Decimal("78.0"),
        GEWEI="KG",
        HSNCODE="8501.32",  # Electric motors
        HERKL="FI",
    ),
    
    "MAT-100002": Material(
        MATNR="MAT-100002",
        MAKTX="Precision CNC Milling Machine",
        MATKL="MACHINERY",
        MEINS="EA",
        BRGEW=Decimal("2850.0"),
        NTGEW=Decimal("2650.0"),
        GEWEI="KG",
        HSNCODE="8459.61",  # Machine tools
        HERKL="DE",
    ),
    
    # Electronics
    "MAT-200001": Material(
        MATNR="MAT-200001",
        MAKTX="Industrial Control Unit ICU-500",
        MATKL="ELECTRONICS",
        MEINS="EA",
        BRGEW=Decimal("2.5"),
        NTGEW=Decimal("2.2"),
        GEWEI="KG",
        HSNCODE="8537.10",  # Control panels
        HERKL="SE",
    ),
    
    "MAT-200002": Material(
        MATNR="MAT-200002",
        MAKTX="Programmable Logic Controller PLC-1200",
        MATKL="ELECTRONICS",
        MEINS="EA",
        BRGEW=Decimal("1.8"),
        NTGEW=Decimal("1.5"),
        GEWEI="KG",
        HSNCODE="8537.10",
        HERKL="DE",
    ),
    
    # Components
    "MAT-300001": Material(
        MATNR="MAT-300001",
        MAKTX="High-Precision Bearing Assembly",
        MATKL="COMPONENTS",
        MEINS="EA",
        BRGEW=Decimal("0.85"),
        NTGEW=Decimal("0.75"),
        GEWEI="KG",
        HSNCODE="8482.10",  # Ball bearings
        HERKL="FI",
    ),
    
    "MAT-300002": Material(
        MATNR="MAT-300002",
        MAKTX="Industrial Cable Assembly 50m",
        MATKL="COMPONENTS",
        MEINS="EA",
        BRGEW=Decimal("12.5"),
        NTGEW=Decimal("11.8"),
        GEWEI="KG",
        HSNCODE="8544.49",  # Electric conductors
        HERKL="SE",
    ),
}


# ============================================================================
# SCENARIO 1: EU → Singapore Export (Machinery)
# ============================================================================

def scenario_eu_singapore_export():
    """
    Finnish company exports industrial machinery to Singapore.
    Uses CIF Incoterms, Letter of Credit payment.
    """
    today = date.today()
    
    # Purchase Order from Singapore customer
    po_header = EKKO(
        EBELN="4500000123",
        BUKRS="1000",  # Company Code
        BSTYP="F",
        BSART="NB",  # Standard PO
        AEDAT=today - timedelta(days=45),
        LIFNR="300001",  # European Components AB
        EKORG="1000",
        EKGRP="001",
        WAERS="EUR",
        ZTERM="LC30",  # Letter of Credit, 30 days
        INCO1="CIF",
        INCO2="Singapore Port",
        KTWRT=Decimal("125000.00"),
        IHREZ="SG-PO-2024-0156",
    )
    
    po_items = [
        EKPO(
            EBELN="4500000123",
            EBELP="00010",
            MATNR="MAT-100001",
            TXZ01="Industrial Servo Motor 5kW",
            MATKL="MACHINERY",
            MENGE=Decimal("50"),
            MEINS="EA",
            NETPR=Decimal("2500.00"),
            PEINH=Decimal("1"),
            WAERS="EUR",
            EINDT=today + timedelta(days=30),
            WERKS="1000",
            LAND1="FI",
        ),
    ]
    
    # Sales Order
    so_header = VBAK(
        VBELN="0100000234",
        VKORG="1000",
        VTWEG="10",
        SPART="00",
        VBTYP="C",
        AUART="ZEXP",  # Export Order
        KUNNR="200001",  # Singapore Trading Company
        ERDAT=today - timedelta(days=40),
        AUDAT=today - timedelta(days=40),
        VDATU=today + timedelta(days=30),
        WAERK="EUR",
        NETWR=Decimal("125000.00"),
        ZTERM="LC30",
        INCO1="CIF",
        INCO2="Singapore Port",
        BSTNK="SG-PO-2024-0156",
        BSTDK=today - timedelta(days=45),
        LCNUM="LC-HSBC-SG-2024-00789",
    )
    
    so_items = [
        VBAP(
            VBELN="0100000234",
            POSNR="000010",
            MATNR="MAT-100001",
            ARKTX="Industrial Servo Motor 5kW",
            MATKL="MACHINERY",
            KWMENG=Decimal("50"),
            VRKME="EA",
            NETWR=Decimal("125000.00"),
            WAERK="EUR",
            NETPR=Decimal("2500.00"),
            WERKS="1000",
        ),
    ]
    
    # Delivery
    delivery_header = LIKP(
        VBELN="8000000456",
        LFART="ZLFD",  # Export Delivery
        VSTEL="1000",
        KUNNR="200001",
        KUNAG="200001",
        ERDAT=today - timedelta(days=10),
        LFDAT=today - timedelta(days=5),
        WADAT=today - timedelta(days=5),
        INCO1="CIF",
        INCO2="Singapore Port",
        ROUTE="SEA-EU-SG",
        BTGEW=Decimal("4275.0"),  # 50 motors × 85.5kg
        GEWEI="KG",
        BOLNR="MAEU123456789",  # Maersk B/L
    )
    
    delivery_items = [
        LIPS(
            VBELN="8000000456",
            POSNR="000010",
            MATNR="MAT-100001",
            ARKTX="Industrial Servo Motor 5kW",
            MATKL="MACHINERY",
            LFIMG=Decimal("50"),
            VRKME="EA",
            BRGEW=Decimal("85.5"),
            NTGEW=Decimal("78.0"),
            GEWEI="KG",
            WERKS="1000",
            HERKL="FI",
        ),
    ]
    
    # Commercial Invoice
    invoice_header = VBRK(
        VBELN="9000000789",
        FKART="F2",
        FKTYP="F",
        KUNAG="200001",
        KUNRG="200001",
        ERDAT=today - timedelta(days=5),
        FKDAT=today - timedelta(days=5),
        ZTERM="LC30",
        ZBD1T=30,
        WAERK="EUR",
        NETWR=Decimal("125000.00"),
        MWSBK=Decimal("0.00"),  # Export, no VAT
        VBELN_REF="0100000234",
        VBELN_DEL="8000000456",
        INCO1="CIF",
        INCO2="Singapore Port",
        LCNUM="LC-HSBC-SG-2024-00789",
        BOLNR="MAEU123456789",
    )
    
    invoice_items = [
        VBRP(
            VBELN="9000000789",
            POSNR="000010",
            MATNR="MAT-100001",
            ARKTX="Industrial Servo Motor 5kW",
            MATKL="MACHINERY",
            FKIMG=Decimal("50"),
            VRKME="EA",
            NETWR=Decimal("125000.00"),
            WAERK="EUR",
            MWSBP=Decimal("0.00"),
            HERKL="FI",
        ),
    ]
    
    # Documentary Credit
    lc = ZBANKF(
        LCNUM="LC-HSBC-SG-2024-00789",
        LCTYPE="IRREVOCABLE",
        APPLICANT="200001",
        BENEFICIARY="100001",
        ISSUING_BANK="HSBCSGSG",
        ADVISING_BANK="NDEAFIHH",
        LCAMOUNT=Decimal("125000.00"),
        LCCURRENCY="EUR",
        ISSUE_DATE=today - timedelta(days=40),
        EXPIRY_DATE=today + timedelta(days=50),
        LATEST_SHIP_DATE=today + timedelta(days=30),
        PARTIAL_SHIP=False,
        TRANSHIP=True,
        INCO1="CIF",
        INCO2="Singapore Port",
        PRES_DAYS=21,
        DOCS_REQUIRED=[
            "Commercial Invoice",
            "Bill of Lading",
            "Packing List",
            "Certificate of Origin",
            "Insurance Certificate",
        ],
        PURCHASE_ORDER="SG-PO-2024-0156",
        SALES_ORDER="0100000234",
    )
    
    return {
        "scenario": "EU_TO_SINGAPORE_MACHINERY_EXPORT",
        "description": "Finnish machinery manufacturer exports servo motors to Singapore via sea freight with L/C payment",
        "purchase_order": {"header": po_header, "items": po_items},
        "sales_order": {"header": so_header, "items": so_items},
        "delivery": {"header": delivery_header, "items": delivery_items},
        "invoice": {"header": invoice_header, "items": invoice_items},
        "documentary_credit": lc,
    }


# ============================================================================
# SCENARIO 2: EU → Japan Export (Electronics)
# ============================================================================

def scenario_eu_japan_electronics():
    """
    German company exports industrial control systems to Japan.
    Uses FOB Incoterms, Documentary Credit.
    """
    today = date.today()
    
    so_header = VBAK(
        VBELN="0100000567",
        VKORG="1000",
        VTWEG="10",
        SPART="00",
        VBTYP="C",
        AUART="ZEXP",
        KUNNR="200002",  # Tokyo Industrial Equipment
        ERDAT=today - timedelta(days=35),
        AUDAT=today - timedelta(days=35),
        VDATU=today + timedelta(days=25),
        WAERK="EUR",
        NETWR=Decimal("87500.00"),
        ZTERM="LC45",
        INCO1="FOB",
        INCO2="Hamburg Port",
        BSTNK="JP-PO-2024-0893",
        BSTDK=today - timedelta(days=38),
        LCNUM="LC-MUFG-JP-2024-01234",
    )
    
    so_items = [
        VBAP(
            VBELN="0100000567",
            POSNR="000010",
            MATNR="MAT-200001",
            ARKTX="Industrial Control Unit ICU-500",
            MATKL="ELECTRONICS",
            KWMENG=Decimal("100"),
            VRKME="EA",
            NETWR=Decimal("50000.00"),
            WAERK="EUR",
            NETPR=Decimal("500.00"),
            WERKS="2000",
        ),
        VBAP(
            VBELN="0100000567",
            POSNR="000020",
            MATNR="MAT-200002",
            ARKTX="Programmable Logic Controller PLC-1200",
            MATKL="ELECTRONICS",
            KWMENG=Decimal("50"),
            VRKME="EA",
            NETWR=Decimal("37500.00"),
            WAERK="EUR",
            NETPR=Decimal("750.00"),
            WERKS="2000",
        ),
    ]
    
    delivery_header = LIKP(
        VBELN="8000000678",
        LFART="ZLFD",
        VSTEL="2000",
        KUNNR="200002",
        KUNAG="200002",
        ERDAT=today - timedelta(days=8),
        LFDAT=today - timedelta(days=3),
        WADAT=today - timedelta(days=3),
        INCO1="FOB",
        INCO2="Hamburg Port",
        ROUTE="SEA-EU-JP",
        BTGEW=Decimal("340.0"),
        GEWEI="KG",
        BOLNR="HLCUHAMB20240123",
    )
    
    delivery_items = [
        LIPS(
            VBELN="8000000678",
            POSNR="000010",
            MATNR="MAT-200001",
            ARKTX="Industrial Control Unit ICU-500",
            MATKL="ELECTRONICS",
            LFIMG=Decimal("100"),
            VRKME="EA",
            BRGEW=Decimal("2.5"),
            NTGEW=Decimal("2.2"),
            GEWEI="KG",
            WERKS="2000",
            HERKL="SE",
        ),
        LIPS(
            VBELN="8000000678",
            POSNR="000020",
            MATNR="MAT-200002",
            ARKTX="Programmable Logic Controller PLC-1200",
            MATKL="ELECTRONICS",
            LFIMG=Decimal("50"),
            VRKME="EA",
            BRGEW=Decimal("1.8"),
            NTGEW=Decimal("1.5"),
            GEWEI="KG",
            WERKS="2000",
            HERKL="DE",
        ),
    ]
    
    invoice_header = VBRK(
        VBELN="9000001012",
        FKART="F2",
        FKTYP="F",
        KUNAG="200002",
        KUNRG="200002",
        ERDAT=today - timedelta(days=3),
        FKDAT=today - timedelta(days=3),
        ZTERM="LC45",
        ZBD1T=45,
        WAERK="EUR",
        NETWR=Decimal("87500.00"),
        MWSBK=Decimal("0.00"),
        VBELN_REF="0100000567",
        VBELN_DEL="8000000678",
        INCO1="FOB",
        INCO2="Hamburg Port",
        LCNUM="LC-MUFG-JP-2024-01234",
        BOLNR="HLCUHAMB20240123",
    )
    
    invoice_items = [
        VBRP(
            VBELN="9000001012",
            POSNR="000010",
            MATNR="MAT-200001",
            ARKTX="Industrial Control Unit ICU-500",
            MATKL="ELECTRONICS",
            FKIMG=Decimal("100"),
            VRKME="EA",
            NETWR=Decimal("50000.00"),
            WAERK="EUR",
            MWSBP=Decimal("0.00"),
            HERKL="SE",
        ),
        VBRP(
            VBELN="9000001012",
            POSNR="000020",
            MATNR="MAT-200002",
            ARKTX="Programmable Logic Controller PLC-1200",
            MATKL="ELECTRONICS",
            FKIMG=Decimal("50"),
            VRKME="EA",
            NETWR=Decimal("37500.00"),
            WAERK="EUR",
            MWSBP=Decimal("0.00"),
            HERKL="DE",
        ),
    ]
    
    lc = ZBANKF(
        LCNUM="LC-MUFG-JP-2024-01234",
        LCTYPE="IRREVOCABLE_CONFIRMED",
        APPLICANT="200002",
        BENEFICIARY="100002",
        ISSUING_BANK="MUFGJPJT",  # MUFG Bank Tokyo
        ADVISING_BANK="DEUTDEMM",  # Deutsche Bank Munich
        CONFIRMING_BANK="DEUTDEMM",
        LCAMOUNT=Decimal("87500.00"),
        LCCURRENCY="EUR",
        ISSUE_DATE=today - timedelta(days=35),
        EXPIRY_DATE=today + timedelta(days=55),
        LATEST_SHIP_DATE=today + timedelta(days=25),
        PARTIAL_SHIP=True,
        TRANSHIP=True,
        INCO1="FOB",
        INCO2="Hamburg Port",
        PRES_DAYS=21,
        DOCS_REQUIRED=[
            "Commercial Invoice",
            "Bill of Lading",
            "Packing List",
            "Certificate of Origin",
        ],
        PURCHASE_ORDER="JP-PO-2024-0893",
        SALES_ORDER="0100000567",
    )
    
    return {
        "scenario": "EU_TO_JAPAN_ELECTRONICS_EXPORT",
        "description": "German electronics manufacturer exports control systems to Japan",
        "sales_order": {"header": so_header, "items": so_items},
        "delivery": {"header": delivery_header, "items": delivery_items},
        "invoice": {"header": invoice_header, "items": invoice_items},
        "documentary_credit": lc,
    }


# ============================================================================
# Data Access Functions
# ============================================================================

def get_all_scenarios():
    """Return all available trade scenarios"""
    return [
        scenario_eu_singapore_export(),
        scenario_eu_japan_electronics(),
    ]


def get_partner(partner_num: str) -> Partner:
    """Get partner data by number"""
    return PARTNERS.get(partner_num)


def get_material(matnr: str) -> Material:
    """Get material data by number"""
    return MATERIALS.get(matnr)


if __name__ == "__main__":
    # Demo: Print scenario summary
    for scenario in get_all_scenarios():
        print(f"\n{'='*70}")
        print(f"SCENARIO: {scenario['scenario']}")
        print(f"{'='*70}")
        print(f"Description: {scenario['description']}")
        print(f"\nDocuments available:")
        for doc_type in scenario.keys():
            if doc_type not in ['scenario', 'description']:
                print(f"  - {doc_type}")
