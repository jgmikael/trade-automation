"""
SAP Data Structure Models

Simulates key SAP SD (Sales & Distribution) and MM (Materials Management) tables
for international trade document generation.

Based on standard SAP ERP structures with fields relevant to cross-border trade.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal


# ============================================================================
# PURCHASE ORDER (MM Module - EKKO/EKPO)
# ============================================================================

@dataclass
class EKKO:
    """Purchase Order Header (EKKO table)"""
    # Key fields
    EBELN: str  # Purchase Order Number
    BUKRS: str  # Company Code
    BSTYP: str  # Purchase Document Category (F=Purchase Order)
    BSART: str  # Purchase Document Type
    
    # Dates
    AEDAT: date  # Purchase Order Date
    LIFNR: str  # Vendor Account Number
    
    # Organizational
    EKORG: str  # Purchasing Organization
    EKGRP: str  # Purchasing Group
    WAERS: str  # Currency Key
    
    # Terms and Conditions
    ZTERM: Optional[str] = None  # Terms of Payment Key
    INCO1: Optional[str] = None  # Incoterms Part 1 (e.g., "FOB", "CIF")
    INCO2: Optional[str] = None  # Incoterms Part 2 (Location)
    
    # Amounts
    KTWRT: Optional[Decimal] = None  # Target Value for Header
    
    # Reference
    KONNR: Optional[str] = None  # Contract Number
    KDATB: Optional[date] = None  # Contract Validity Start Date
    KDATE: Optional[date] = None  # Contract Validity End Date
    
    # Additional fields
    IHREZ: Optional[str] = None  # Your Reference
    UNSEZ: Optional[str] = None  # Our Reference


@dataclass
class EKPO:
    """Purchase Order Item (EKPO table)"""
    # Key fields
    EBELN: str  # Purchase Order Number
    EBELP: str  # Item Number (e.g., "00010", "00020")
    
    # Material
    MATNR: Optional[str] = None  # Material Number
    TXZ01: Optional[str] = None  # Short Text (Item Description)
    MATKL: Optional[str] = None  # Material Group
    
    # Quantity and Unit
    MENGE: Decimal = Decimal("0")  # Purchase Order Quantity
    MEINS: str = "EA"  # Order Unit (EA=Each, KG=Kilogram, etc.)
    
    # Pricing
    NETPR: Decimal = Decimal("0")  # Net Price
    PEINH: Decimal = Decimal("1")  # Price Unit
    WAERS: str = "EUR"  # Currency Key
    
    # Delivery
    EINDT: Optional[date] = None  # Delivery Date
    WERKS: Optional[str] = None  # Plant
    LGORT: Optional[str] = None  # Storage Location
    
    # Country of Origin
    LAND1: Optional[str] = None  # Country of Origin (ISO code)
    
    # Tax and Customs
    MWSKZ: Optional[str] = None  # Tax Code


# ============================================================================
# SALES ORDER (SD Module - VBAK/VBAP)
# ============================================================================

@dataclass
class VBAK:
    """Sales Document Header (VBAK table)"""
    # Key fields
    VBELN: str  # Sales Document Number
    VKORG: str  # Sales Organization
    VTWEG: str  # Distribution Channel
    SPART: str  # Division
    
    # Document Type
    VBTYP: str  # Sales Document Category (C=Order)
    AUART: str  # Sales Document Type
    
    # Customer
    KUNNR: str  # Sold-to Party
    
    # Dates
    ERDAT: date  # Date Created
    AUDAT: date  # Order Date
    VDATU: Optional[date] = None  # Requested Delivery Date
    
    # Pricing
    WAERK: str = "EUR"  # Currency
    NETWR: Decimal = Decimal("0")  # Net Value
    
    # Terms
    ZTERM: Optional[str] = None  # Terms of Payment
    INCO1: Optional[str] = None  # Incoterms Part 1
    INCO2: Optional[str] = None  # Incoterms Part 2
    
    # Reference
    BSTNK: Optional[str] = None  # Customer Purchase Order Number
    BSTDK: Optional[date] = None  # Customer Purchase Order Date
    
    # Documentary Credit
    LCNUM: Optional[str] = None  # Letter of Credit Number


@dataclass
class VBAP:
    """Sales Document Item (VBAP table)"""
    # Key fields
    VBELN: str  # Sales Document Number
    POSNR: str  # Item Number (e.g., "000010", "000020")
    
    # Material
    MATNR: Optional[str] = None  # Material Number
    ARKTX: Optional[str] = None  # Item Description
    MATKL: Optional[str] = None  # Material Group
    
    # Quantity
    KWMENG: Decimal = Decimal("0")  # Order Quantity
    VRKME: str = "EA"  # Sales Unit
    
    # Pricing
    NETWR: Decimal = Decimal("0")  # Net Value
    WAERK: str = "EUR"  # Currency
    NETPR: Decimal = Decimal("0")  # Net Price
    
    # Plant and Delivery
    WERKS: Optional[str] = None  # Plant
    LGORT: Optional[str] = None  # Storage Location


# ============================================================================
# DELIVERY (SD Module - LIKP/LIPS)
# ============================================================================

@dataclass
class LIKP:
    """Delivery Header (LIKP table)"""
    # Key fields
    VBELN: str  # Delivery Number
    LFART: str  # Delivery Type
    
    # References
    VBTYP: str = "J"  # Sales Document Category (J=Delivery)
    VSTEL: str  # Shipping Point
    
    # Customer
    KUNNR: str  # Ship-to Party
    KUNAG: Optional[str] = None  # Sold-to Party
    
    # Dates
    ERDAT: date  # Creation Date
    LFDAT: date  # Delivery Date
    WADAT: Optional[date] = None  # Goods Issue Date
    
    # Incoterms
    INCO1: Optional[str] = None  # Incoterms Part 1
    INCO2: Optional[str] = None  # Incoterms Part 2
    
    # Transport
    ROUTE: Optional[str] = None  # Route
    VSBED: Optional[str] = None  # Shipping Conditions
    
    # Weights and Volumes
    BTGEW: Optional[Decimal] = None  # Total Weight (kg)
    GEWEI: Optional[str] = "KG"  # Weight Unit
    VOLUM: Optional[Decimal] = None  # Volume
    VOLEH: Optional[str] = "M3"  # Volume Unit
    
    # Bills of Lading
    BOLNR: Optional[str] = None  # Bill of Lading Number


@dataclass
class LIPS:
    """Delivery Item (LIPS table)"""
    # Key fields
    VBELN: str  # Delivery Number
    POSNR: str  # Item Number
    
    # Material
    MATNR: Optional[str] = None  # Material Number
    ARKTX: Optional[str] = None  # Item Description
    MATKL: Optional[str] = None  # Material Group
    
    # Quantity
    LFIMG: Decimal = Decimal("0")  # Delivered Quantity
    VRKME: str = "EA"  # Sales Unit
    
    # Weight
    BRGEW: Optional[Decimal] = None  # Gross Weight
    NTGEW: Optional[Decimal] = None  # Net Weight
    GEWEI: Optional[str] = "KG"  # Weight Unit
    
    # Plant
    WERKS: Optional[str] = None  # Plant
    LGORT: Optional[str] = None  # Storage Location
    
    # Origin
    HERKL: Optional[str] = None  # Country of Origin


# ============================================================================
# BILLING/INVOICE (SD Module - VBRK/VBRP)
# ============================================================================

@dataclass
class VBRK:
    """Billing Document Header (VBRK table)"""
    # Key fields
    VBELN: str  # Billing Document Number
    FKART: str  # Billing Type (F2=Invoice)
    FKTYP: str  # Billing Category (F=Invoice)
    
    # Customer
    KUNAG: str  # Sold-to Party
    KUNRG: str  # Payer
    
    # Dates
    ERDAT: date  # Creation Date
    FKDAT: date  # Billing Date
    ZTERM: Optional[str] = None  # Terms of Payment
    ZBD1T: Optional[int] = None  # Payment Terms Days
    
    # Currency and Amounts
    WAERK: str = "EUR"  # Currency
    NETWR: Decimal = Decimal("0")  # Net Value
    MWSBK: Decimal = Decimal("0")  # Tax Amount
    
    # Reference Documents
    VBELN_REF: Optional[str] = None  # Reference Sales Order
    VBELN_DEL: Optional[str] = None  # Reference Delivery
    
    # Incoterms
    INCO1: Optional[str] = None  # Incoterms Part 1
    INCO2: Optional[str] = None  # Incoterms Part 2
    
    # Documentary Credit
    LCNUM: Optional[str] = None  # Letter of Credit Number
    
    # Transport
    BOLNR: Optional[str] = None  # Bill of Lading Number


@dataclass
class VBRP:
    """Billing Document Item (VBRP table)"""
    # Key fields
    VBELN: str  # Billing Document Number
    POSNR: str  # Item Number
    
    # Material
    MATNR: Optional[str] = None  # Material Number
    ARKTX: Optional[str] = None  # Item Description
    MATKL: Optional[str] = None  # Material Group
    
    # Quantity
    FKIMG: Decimal = Decimal("0")  # Billed Quantity
    VRKME: str = "EA"  # Sales Unit
    
    # Pricing
    NETWR: Decimal = Decimal("0")  # Net Value
    WAERK: str = "EUR"  # Currency
    
    # Tax
    MWSBP: Decimal = Decimal("0")  # Tax Amount
    MWSKZ: Optional[str] = None  # Tax Code
    
    # Origin
    HERKL: Optional[str] = None  # Country of Origin


# ============================================================================
# DOCUMENTARY CREDIT / LETTER OF CREDIT
# ============================================================================

@dataclass
class ZBANKF:
    """Documentary Credit Header (Custom Z-table)"""
    # Key fields
    LCNUM: str  # Letter of Credit Number
    LCTYPE: str  # LC Type (IRREVOCABLE, REVOCABLE, etc.)
    
    # Parties
    APPLICANT: str  # Applicant (Buyer) Customer Number
    BENEFICIARY: str  # Beneficiary (Seller) Vendor/Customer Number
    
    # Banks
    ISSUING_BANK: str  # Issuing Bank Code
    ADVISING_BANK: Optional[str] = None  # Advising Bank Code
    CONFIRMING_BANK: Optional[str] = None  # Confirming Bank Code
    
    # Amounts
    LCAMOUNT: Decimal = Decimal("0")  # LC Amount
    LCCURRENCY: str = "EUR"  # LC Currency
    
    # Dates
    ISSUE_DATE: date  # Issue Date
    EXPIRY_DATE: date  # Expiry Date
    LATEST_SHIP_DATE: Optional[date] = None  # Latest Shipment Date
    
    # Shipment Terms
    PARTIAL_SHIP: bool = False  # Partial Shipments Allowed
    TRANSHIP: bool = False  # Transshipment Allowed
    INCO1: Optional[str] = None  # Incoterms
    INCO2: Optional[str] = None  # Incoterms Location
    
    # Presentation
    PRES_DAYS: int = 21  # Presentation Period (days after shipment)
    
    # Documents Required
    DOCS_REQUIRED: List[str] = field(default_factory=list)  # List of required documents
    
    # References
    PURCHASE_ORDER: Optional[str] = None  # PO Number
    SALES_ORDER: Optional[str] = None  # SO Number


# ============================================================================
# PARTNER FUNCTIONS (Common across documents)
# ============================================================================

@dataclass
class Partner:
    """Partner/Party Data (Customer/Vendor Master)"""
    # Key
    PARTNER_NUM: str  # Partner Number (KUNNR or LIFNR)
    PARTNER_TYPE: str  # Type: "CUSTOMER" or "VENDOR"
    
    # Basic Data
    NAME1: str  # Name 1
    NAME2: Optional[str] = None  # Name 2
    NAME3: Optional[str] = None  # Name 3
    
    # Address
    STREET: str  # Street Address
    CITY: str  # City
    POST_CODE: str  # Postal Code
    REGION: Optional[str] = None  # Region/State
    COUNTRY: str  # Country Code (ISO)
    
    # Contact
    TEL_NUMBER: Optional[str] = None  # Telephone
    FAX_NUMBER: Optional[str] = None  # Fax
    EMAIL: Optional[str] = None  # Email
    
    # Tax
    STCEG: Optional[str] = None  # VAT Registration Number
    STCD1: Optional[str] = None  # Tax Number 1
    
    # Banking (for vendors/customers)
    BANKL: Optional[str] = None  # Bank Key
    BANKN: Optional[str] = None  # Bank Account Number
    SWIFT: Optional[str] = None  # SWIFT/BIC Code


# ============================================================================
# MATERIAL MASTER
# ============================================================================

@dataclass
class Material:
    """Material Master Data (MARA)"""
    # Key
    MATNR: str  # Material Number
    
    # Description
    MAKTX: str  # Material Description
    MATKL: Optional[str] = None  # Material Group
    
    # Basic Data
    MEINS: str = "EA"  # Base Unit of Measure
    BRGEW: Optional[Decimal] = None  # Gross Weight
    NTGEW: Optional[Decimal] = None  # Net Weight
    GEWEI: Optional[str] = "KG"  # Weight Unit
    
    # Classification
    HSNCODE: Optional[str] = None  # HS Commodity Code (for customs)
    HERKL: Optional[str] = None  # Country of Origin
    
    # Dangerous Goods
    DANGEROUS: bool = False  # Dangerous Goods Indicator
    UN_NUMBER: Optional[str] = None  # UN Number
