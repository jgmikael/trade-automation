"""
SAP to W3C Verifiable Credential Mapping Engine

Transforms SAP document structures into KTDDE-based W3C Verifiable Credentials.
Uses the JSON-LD contexts and schemas generated from SHACL profiles.
"""

from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import Dict, Any, Optional, List
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.sap_structures import *
from data.sample_data import get_partner, get_material


class SAPToVCMapper:
    """Maps SAP documents to W3C Verifiable Credentials"""
    
    def __init__(self, base_url: str = "https://example.com"):
        self.base_url = base_url
        self.context_base = "https://github.com/jgmikael/trade-automation/contexts"
    
    # ========================================================================
    # PURCHASE ORDER → PurchaseOrder VC
    # ========================================================================
    
    def map_purchase_order(self, header: EKKO, items: List[EKPO], 
                          issuer_did: str = "did:example:buyer") -> Dict[str, Any]:
        """
        Map SAP Purchase Order (EKKO/EKPO) to PurchaseOrder W3C VC
        """
        vendor = get_partner(header.LIFNR)
        
        # Map items
        vc_items = []
        for item in items:
            material = get_material(item.MATNR) if item.MATNR else None
            
            vc_item = {
                "type": "GoodsItem",
                "lineNumber": int(item.EBELP),
                "productDescription": item.TXZ01 or (material.MAKTX if material else ""),
                "quantity": {
                    "type": "Quantity",
                    "quantityValue": str(item.MENGE),
                    "unitCode": item.MEINS,
                },
                "unitPrice": {
                    "type": "Amount",
                    "value": float(item.NETPR),
                    "currencyCode": item.WAERS,
                },
                "lineAmount": {
                    "type": "Amount",
                    "value": float(item.MENGE * item.NETPR),
                    "currencyCode": item.WAERS,
                },
            }
            
            if item.LAND1:
                vc_item["originCountry"] = {
                    "type": "Country",
                    "countryCode": item.LAND1,
                }
            
            vc_items.append(vc_item)
        
        # Build credential
        credential = {
            "@context": [
                "https://www.w3.org/2018/credentials/v1",
                f"{self.context_base}/purchaseorder-context.jsonld",
            ],
            "id": f"{self.base_url}/credentials/po/{header.EBELN}",
            "type": ["VerifiableCredential", "PurchaseOrderCredential"],
            "issuer": {
                "id": issuer_did,
                "name": "Buyer Company",  # Would come from BUKRS master data
            },
            "issuanceDate": self._format_datetime(header.AEDAT),
            "credentialSubject": {
                "id": f"{self.base_url}/purchase-orders/{header.EBELN}",
                "type": "PurchaseOrder",
                "orderIdentifier": header.EBELN,
                "orderDate": str(header.AEDAT),
                "orderAmount": {
                    "type": "Amount",
                    "value": float(header.KTWRT) if header.KTWRT else 0.0,
                    "currencyCode": header.WAERS,
                },
                "buyerParty": self._map_buyer_party(header.BUKRS),
                "sellerParty": self._map_party(vendor) if vendor else None,
                "hasItem": vc_items,
            }
        }
        
        # Add payment terms if present
        if header.ZTERM:
            credential["credentialSubject"]["definesPaymentTerms"] = {
                "type": "PaymentTerms",
                "paymentTermsCode": header.ZTERM,
            }
        
        # Add delivery terms if present
        if header.INCO1:
            credential["credentialSubject"]["deliveryTerms"] = {
                "type": "TradeDeliveryTerms",
                "incotermsCode": header.INCO1,
                "namedPlace": header.INCO2,
            }
        
        return credential
    
    # ========================================================================
    # COMMERCIAL INVOICE → CommercialInvoice VC
    # ========================================================================
    
    def map_commercial_invoice(self, header: VBRK, items: List[VBRP],
                               issuer_did: str = "did:example:seller") -> Dict[str, Any]:
        """
        Map SAP Billing Document (VBRK/VBRP) to CommercialInvoice W3C VC
        """
        customer = get_partner(header.KUNAG)
        payer = get_partner(header.KUNRG)
        
        # Map invoice lines
        vc_lines = []
        for item in items:
            material = get_material(item.MATNR) if item.MATNR else None
            
            vc_line = {
                "type": "InvoiceLine",
                "lineNumber": int(item.POSNR),
                "productDescription": item.ARKTX or (material.MAKTX if material else ""),
                "quantity": {
                    "type": "Quantity",
                    "quantityValue": str(item.FKIMG),
                    "unitCode": item.VRKME,
                },
                "lineAmount": {
                    "type": "MonetaryAmount",
                    "amountValue": float(item.NETWR),
                    "currencyCode": item.WAERK,
                },
            }
            
            if item.HERKL:
                vc_line["originCountry"] = {
                    "type": "Country",
                    "countryCode": item.HERKL,
                }
            
            if material and material.HSNCODE:
                vc_line["commodityClassification"] = {
                    "type": "CommodityClassification",
                    "classificationCode": material.HSNCODE,
                }
            
            vc_lines.append(vc_line)
        
        # Build credential
        credential = {
            "@context": [
                "https://www.w3.org/2018/credentials/v1",
                f"{self.context_base}/commercialinvoice-context.jsonld",
            ],
            "id": f"{self.base_url}/credentials/invoice/{header.VBELN}",
            "type": ["VerifiableCredential", "CommercialInvoiceCredential"],
            "issuer": {
                "id": issuer_did,
                "name": "Seller Company",
            },
            "issuanceDate": self._format_datetime(header.FKDAT),
            "credentialSubject": {
                "id": f"{self.base_url}/invoices/{header.VBELN}",
                "type": "CommercialInvoice",
                "invoiceNumber": header.VBELN,
                "invoiceDate": str(header.FKDAT),
                "totalAmount": {
                    "type": "MonetaryAmount",
                    "amountValue": float(header.NETWR),
                    "currencyCode": header.WAERK,
                },
                "buyerParty": self._map_party(customer) if customer else None,
                "sellerParty": self._map_seller_party("SELLER"),
                "hasInvoiceLine": vc_lines,
            }
        }
        
        # Add payment terms
        if header.ZTERM:
            credential["credentialSubject"]["invoicePaymentTerms"] = {
                "type": "PaymentTerms",
                "paymentTermsCode": header.ZTERM,
            }
            if header.ZBD1T:
                credential["credentialSubject"]["paymentDueDate"] = str(
                    header.FKDAT + timedelta(days=header.ZBD1T)
                )
        
        # Add Incoterms
        if header.INCO1:
            credential["credentialSubject"]["deliveryTerms"] = {
                "type": "TradeDeliveryTerms",
                "incotermsCode": header.INCO1,
                "namedPlace": header.INCO2,
            }
        
        # Add Bill of Lading reference
        if header.BOLNR:
            credential["credentialSubject"]["relatesToTransportDocument"] = {
                "type": "TransportDocument",
                "documentIdentifier": header.BOLNR,
            }
        
        # Add Letter of Credit reference
        if header.LCNUM:
            credential["credentialSubject"]["relatesToDocumentaryCredit"] = {
                "type": "DocumentaryCredit",
                "creditNumber": header.LCNUM,
            }
        
        # Add sales order reference
        if header.VBELN_REF:
            credential["credentialSubject"]["purchaseOrderNumber"] = header.VBELN_REF
        
        return credential
    
    # ========================================================================
    # DELIVERY → BillOfLading VC
    # ========================================================================
    
    def map_bill_of_lading(self, header: LIKP, items: List[LIPS],
                          issuer_did: str = "did:example:carrier") -> Dict[str, Any]:
        """
        Map SAP Delivery (LIKP/LIPS) to BillOfLading W3C VC
        """
        customer = get_partner(header.KUNNR)
        
        # Map goods items
        vc_goods = []
        for item in items:
            material = get_material(item.MATNR) if item.MATNR else None
            
            vc_good = {
                "type": "GoodsItem",
                "descriptionOfGoodsText": item.ARKTX or (material.MAKTX if material else ""),
                "grossWeight": {
                    "type": "Quantity",
                    "quantityValue": str(item.BRGEW) if item.BRGEW else "0",
                    "unitCode": item.GEWEI or "KG",
                },
                "netWeight": {
                    "type": "Quantity",
                    "quantityValue": str(item.NTGEW) if item.NTGEW else "0",
                    "unitCode": item.GEWEI or "KG",
                },
                "quantity": {
                    "type": "Quantity",
                    "quantityValue": str(item.LFIMG),
                    "unitCode": item.VRKME,
                },
            }
            
            if item.HERKL:
                vc_good["originCountry"] = {
                    "type": "Country",
                    "countryCode": item.HERKL,
                }
            
            vc_goods.append(vc_good)
        
        # Build credential
        credential = {
            "@context": [
                "https://www.w3.org/2018/credentials/v1",
                f"{self.context_base}/billoflading-context.jsonld",
            ],
            "id": f"{self.base_url}/credentials/bol/{header.BOLNR or header.VBELN}",
            "type": ["VerifiableCredential", "BillOfLadingCredential"],
            "issuer": {
                "id": issuer_did,
                "name": "Carrier Company",
            },
            "issuanceDate": self._format_datetime(header.WADAT or header.LFDAT),
            "credentialSubject": {
                "id": f"{self.base_url}/bills-of-lading/{header.BOLNR or header.VBELN}",
                "type": "BillOfLading",
                "documentIdentifier": header.BOLNR or header.VBELN,
                "issueDate": str(header.WADAT or header.LFDAT),
                "consigneeParty": self._map_party(customer) if customer else None,
                "carrierParty": {
                    "type": "Party",
                    "partyName": "Carrier Company",  # Would come from carrier master
                },
                "hasGoodsItem": vc_goods,
                "totalGrossWeight": {
                    "type": "Quantity",
                    "quantityValue": str(header.BTGEW) if header.BTGEW else "0",
                    "unitCode": header.GEWEI or "KG",
                },
            }
        }
        
        # Add Incoterms
        if header.INCO1:
            credential["credentialSubject"]["deliveryTermsText"] = f"{header.INCO1} {header.INCO2 or ''}"
        
        # Add delivery date
        if header.LFDAT:
            credential["credentialSubject"]["actualDepartureDateTime"] = self._format_datetime(header.LFDAT)
        
        return credential
    
    # ========================================================================
    # CERTIFICATE OF ORIGIN → CertificateOfOrigin VC
    # ========================================================================
    
    def map_certificate_of_origin(self, delivery_header: LIKP, delivery_items: List[LIPS],
                                   invoice_header: VBRK,
                                   issuer_did: str = "did:example:authority") -> Dict[str, Any]:
        """
        Map SAP data to CertificateOfOrigin W3C VC
        
        Certificate of Origin is typically issued by chambers of commerce or customs authorities.
        We derive it from delivery and invoice data.
        """
        exporter = get_partner(invoice_header.KUNAG)
        importer = get_partner(delivery_header.KUNNR)
        
        # Determine primary origin country from goods
        origin_countries = set()
        for item in delivery_items:
            if item.HERKL:
                origin_countries.add(item.HERKL)
        
        # Map goods
        vc_goods = []
        for item in delivery_items:
            material = get_material(item.MATNR) if item.MATNR else None
            
            vc_good = {
                "type": "GoodsItem",
                "descriptionOfGoods": item.ARKTX or (material.MAKTX if material else ""),
                "grossWeight": {
                    "type": "Quantity",
                    "quantityValue": str(item.BRGEW) if item.BRGEW else "0",
                    "unitCode": item.GEWEI or "KG",
                },
                "netWeight": {
                    "type": "Quantity",
                    "quantityValue": str(item.NTGEW) if item.NTGEW else "0",
                    "unitCode": item.GEWEI or "KG",
                },
            }
            
            if item.HERKL:
                vc_good["originCountry"] = {
                    "type": "Country",
                    "countryCode": item.HERKL,
                }
            
            if material and material.HSNCODE:
                vc_good["commodityClassification"] = {
                    "type": "CommodityClassification",
                    "classificationCode": material.HSNCODE,
                }
            
            vc_goods.append(vc_good)
        
        # Build credential
        cert_number = f"COO-{delivery_header.VBELN}-{datetime.now().strftime('%Y%m%d')}"
        
        credential = {
            "@context": [
                "https://www.w3.org/2018/credentials/v1",
                f"{self.context_base}/certificateoforigin-context.jsonld",
            ],
            "id": f"{self.base_url}/credentials/coo/{cert_number}",
            "type": ["VerifiableCredential", "CertificateOfOriginCredential"],
            "issuer": {
                "id": issuer_did,
                "name": "Chamber of Commerce",
            },
            "issuanceDate": self._format_datetime(datetime.now().date()),
            "credentialSubject": {
                "id": f"{self.base_url}/certificates-of-origin/{cert_number}",
                "type": "CertificateOfOrigin",
                "certificateNumber": cert_number,
                "issueDate": str(datetime.now().date()),
                "exporterParty": self._map_party(exporter) if exporter else None,
                "importerParty": self._map_party(importer) if importer else None,
                "issuingAuthorityParty": {
                    "type": "Party",
                    "partyName": "Chamber of Commerce",
                },
                "issuerParty": {
                    "type": "Party",
                    "partyName": "Authorized Official",
                },
                "hasGoodsItem": vc_goods,
            }
        }
        
        # Add invoice reference
        if invoice_header:
            credential["credentialSubject"]["invoiceNumber"] = invoice_header.VBELN
        
        # Add transport document reference
        if delivery_header.BOLNR:
            credential["credentialSubject"]["transportDocumentNumber"] = delivery_header.BOLNR
        
        return credential
    
    # ========================================================================
    # DOCUMENTARY CREDIT → DocumentaryCredit VC
    # ========================================================================
    
    def map_documentary_credit(self, lc: ZBANKF,
                               issuer_did: str = "did:example:bank") -> Dict[str, Any]:
        """
        Map SAP Documentary Credit to DocumentaryCredit W3C VC
        """
        applicant = get_partner(lc.APPLICANT)
        beneficiary = get_partner(lc.BENEFICIARY)
        
        # Build credential
        credential = {
            "@context": [
                "https://www.w3.org/2018/credentials/v1",
                f"{self.context_base}/documentarycredit-context.jsonld",
            ],
            "id": f"{self.base_url}/credentials/lc/{lc.LCNUM}",
            "type": ["VerifiableCredential", "DocumentaryCreditCredential"],
            "issuer": {
                "id": issuer_did,
                "name": "Issuing Bank",
            },
            "issuanceDate": self._format_datetime(lc.ISSUE_DATE),
            "expirationDate": self._format_datetime(lc.EXPIRY_DATE),
            "credentialSubject": {
                "id": f"{self.base_url}/documentary-credits/{lc.LCNUM}",
                "type": "DocumentaryCredit",
                "creditNumber": lc.LCNUM,
                "issueDate": str(lc.ISSUE_DATE),
                "expiryDate": str(lc.EXPIRY_DATE),
                "creditAmount": {
                    "type": "MonetaryAmount",
                    "amountValue": float(lc.LCAMOUNT),
                    "currencyCode": lc.LCCURRENCY,
                },
                "applicantParty": self._map_party(applicant) if applicant else None,
                "beneficiaryParty": self._map_party(beneficiary) if beneficiary else None,
                "issuingBankParty": {
                    "type": "Bank",
                    "bankName": "Issuing Bank",
                    "swiftCode": lc.ISSUING_BANK,
                },
                "partialShipmentAllowed": lc.PARTIAL_SHIP,
                "transshipmentAllowed": lc.TRANSHIP,
                "presentationPeriodDays": lc.PRES_DAYS,
            }
        }
        
        # Add advising bank
        if lc.ADVISING_BANK:
            credential["credentialSubject"]["advisingBankParty"] = {
                "type": "Bank",
                "bankName": "Advising Bank",
                "swiftCode": lc.ADVISING_BANK,
            }
        
        # Add confirming bank
        if lc.CONFIRMING_BANK:
            credential["credentialSubject"]["confirmingBankParty"] = {
                "type": "Bank",
                "bankName": "Confirming Bank",
                "swiftCode": lc.CONFIRMING_BANK,
            }
        
        # Add Incoterms
        if lc.INCO1:
            credential["credentialSubject"]["deliveryTerms"] = {
                "type": "TradeDeliveryTerms",
                "incotermsCode": lc.INCO1,
                "namedPlace": lc.INCO2,
            }
        
        # Add document requirements
        if lc.DOCS_REQUIRED:
            doc_reqs = []
            for doc_name in lc.DOCS_REQUIRED:
                doc_reqs.append({
                    "type": "DocumentRequirement",
                    "documentType": doc_name,
                })
            credential["credentialSubject"]["requiresDocument"] = doc_reqs
        
        # Add latest shipment date
        if lc.LATEST_SHIP_DATE:
            credential["credentialSubject"]["latestShipmentDate"] = str(lc.LATEST_SHIP_DATE)
        
        return credential
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def _map_party(self, partner: Optional[Partner]) -> Optional[Dict[str, Any]]:
        """Map SAP Partner to KTDDE Party"""
        if not partner:
            return None
        
        party = {
            "type": "Party",
            "partyName": partner.NAME1,
            "hasAddress": {
                "type": "Address",
                "street": partner.STREET,
                "city": partner.CITY,
                "postalCode": partner.POST_CODE,
                "country": {
                    "type": "Country",
                    "countryCode": partner.COUNTRY,
                }
            }
        }
        
        if partner.STCEG:
            party["taxNumber"] = partner.STCEG
        
        return party
    
    def _map_buyer_party(self, bukrs: str) -> Dict[str, Any]:
        """Map buyer party (would come from company code master)"""
        return {
            "type": "Party",
            "partyName": "Buyer Company",
            "companyCode": bukrs,
        }
    
    def _map_seller_party(self, seller_id: str) -> Dict[str, Any]:
        """Map seller party"""
        return {
            "type": "Party",
            "partyName": "Seller Company",
        }
    
    def _format_datetime(self, dt) -> str:
        """Format date/datetime to ISO 8601"""
        if isinstance(dt, datetime):
            return dt.isoformat() + "Z"
        elif isinstance(dt, date):
            return datetime.combine(dt, datetime.min.time()).isoformat() + "Z"
        return str(dt)


# ============================================================================
# Convenience Functions
# ============================================================================

def convert_sap_scenario_to_vcs(scenario: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert an entire SAP trade scenario to W3C VCs
    """
    mapper = SAPToVCMapper()
    vcs = {}
    
    # Purchase Order
    if "purchase_order" in scenario:
        po = scenario["purchase_order"]
        vcs["purchase_order_vc"] = mapper.map_purchase_order(
            po["header"], po["items"]
        )
    
    # Sales Order → not directly mapped (internal document)
    
    # Delivery → Bill of Lading
    if "delivery" in scenario:
        delivery = scenario["delivery"]
        vcs["bill_of_lading_vc"] = mapper.map_bill_of_lading(
            delivery["header"], delivery["items"]
        )
    
    # Invoice → Commercial Invoice
    if "invoice" in scenario:
        invoice = scenario["invoice"]
        vcs["commercial_invoice_vc"] = mapper.map_commercial_invoice(
            invoice["header"], invoice["items"]
        )
    
    # Certificate of Origin (derived from delivery + invoice)
    if "delivery" in scenario and "invoice" in scenario:
        vcs["certificate_of_origin_vc"] = mapper.map_certificate_of_origin(
            scenario["delivery"]["header"],
            scenario["delivery"]["items"],
            scenario["invoice"]["header"],
        )
    
    # Documentary Credit
    if "documentary_credit" in scenario:
        vcs["documentary_credit_vc"] = mapper.map_documentary_credit(
            scenario["documentary_credit"]
        )
    
    return vcs


if __name__ == "__main__":
    from data.sample_data import scenario_eu_singapore_export
    import json
    
    # Demo: Convert Singapore scenario to VCs
    scenario = scenario_eu_singapore_export()
    vcs = convert_sap_scenario_to_vcs(scenario)
    
    print("Generated W3C Verifiable Credentials:")
    for vc_type, vc in vcs.items():
        print(f"\n{vc_type}:")
        print(json.dumps(vc, indent=2))
