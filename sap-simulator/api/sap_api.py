"""
SAP OData-style REST API Simulator

Simulates SAP ERP OData services for:
- Purchase Orders (MM)
- Sales Orders (SD)
- Deliveries (SD)
- Billing Documents / Invoices (SD)
- Documentary Credits (Banking)

Supports both SAP format responses and W3C VC conversion.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from dataclasses import asdict
from typing import Dict, Any, List
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.sample_data import (
    get_all_scenarios, get_partner, get_material,
    PARTNERS, MATERIALS
)
from mappings.sap_to_vc import SAPToVCMapper, convert_sap_scenario_to_vcs


app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Global mapper instance
vc_mapper = SAPToVCMapper()

# Store scenarios in memory (simulated SAP database)
SCENARIOS_DB = {s["scenario"]: s for s in get_all_scenarios()}


# ============================================================================
# Helper Functions
# ============================================================================

def dataclass_to_dict(obj) -> Dict[str, Any]:
    """Convert dataclass to dict, handling special types"""
    if hasattr(obj, '__dataclass_fields__'):
        result = {}
        for field_name, field_value in asdict(obj).items():
            if field_value is not None:
                # Convert Decimal to float for JSON
                if hasattr(field_value, '__class__') and field_value.__class__.__name__ == 'Decimal':
                    result[field_name] = float(field_value)
                elif isinstance(field_value, (list, tuple)):
                    result[field_name] = [dataclass_to_dict(item) if hasattr(item, '__dataclass_fields__') else item 
                                         for item in field_value]
                else:
                    result[field_name] = field_value
        return result
    return obj


def success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    """Standard success response"""
    return {
        "d": {
            "results": data if isinstance(data, list) else [data]
        },
        "metadata": {
            "status": "success",
            "message": message,
        }
    }


def error_response(message: str, code: int = 400) -> tuple:
    """Standard error response"""
    return jsonify({
        "error": {
            "code": str(code),
            "message": message,
        }
    }), code


# ============================================================================
# API Endpoints - SAP Format
# ============================================================================

@app.route('/sap/opu/odata/sap/api/v1/scenarios', methods=['GET'])
def get_scenarios():
    """List all available trade scenarios"""
    scenarios_list = []
    for scenario_id, scenario in SCENARIOS_DB.items():
        scenarios_list.append({
            "scenario_id": scenario_id,
            "description": scenario.get("description", ""),
            "available_documents": [k for k in scenario.keys() 
                                   if k not in ['scenario', 'description']],
        })
    return jsonify(success_response(scenarios_list))


@app.route('/sap/opu/odata/sap/api/v1/purchase-orders', methods=['GET'])
def get_purchase_orders():
    """Get all purchase orders (EKKO)"""
    pos = []
    for scenario_id, scenario in SCENARIOS_DB.items():
        if "purchase_order" in scenario:
            po = scenario["purchase_order"]
            po_dict = dataclass_to_dict(po["header"])
            po_dict["_items_count"] = len(po["items"])
            po_dict["_scenario"] = scenario_id
            pos.append(po_dict)
    return jsonify(success_response(pos))


@app.route('/sap/opu/odata/sap/api/v1/purchase-orders/<ebeln>', methods=['GET'])
def get_purchase_order(ebeln: str):
    """Get specific purchase order with items"""
    for scenario in SCENARIOS_DB.values():
        if "purchase_order" in scenario:
            po = scenario["purchase_order"]
            if po["header"].EBELN == ebeln:
                result = {
                    "header": dataclass_to_dict(po["header"]),
                    "items": [dataclass_to_dict(item) for item in po["items"]],
                }
                return jsonify(success_response(result))
    return error_response(f"Purchase Order {ebeln} not found", 404)


@app.route('/sap/opu/odata/sap/api/v1/sales-orders', methods=['GET'])
def get_sales_orders():
    """Get all sales orders (VBAK)"""
    sos = []
    for scenario_id, scenario in SCENARIOS_DB.items():
        if "sales_order" in scenario:
            so = scenario["sales_order"]
            so_dict = dataclass_to_dict(so["header"])
            so_dict["_items_count"] = len(so["items"])
            so_dict["_scenario"] = scenario_id
            sos.append(so_dict)
    return jsonify(success_response(sos))


@app.route('/sap/opu/odata/sap/api/v1/sales-orders/<vbeln>', methods=['GET'])
def get_sales_order(vbeln: str):
    """Get specific sales order with items"""
    for scenario in SCENARIOS_DB.values():
        if "sales_order" in scenario:
            so = scenario["sales_order"]
            if so["header"].VBELN == vbeln:
                result = {
                    "header": dataclass_to_dict(so["header"]),
                    "items": [dataclass_to_dict(item) for item in so["items"]],
                }
                return jsonify(success_response(result))
    return error_response(f"Sales Order {vbeln} not found", 404)


@app.route('/sap/opu/odata/sap/api/v1/deliveries', methods=['GET'])
def get_deliveries():
    """Get all deliveries (LIKP)"""
    deliveries = []
    for scenario_id, scenario in SCENARIOS_DB.items():
        if "delivery" in scenario:
            delivery = scenario["delivery"]
            del_dict = dataclass_to_dict(delivery["header"])
            del_dict["_items_count"] = len(delivery["items"])
            del_dict["_scenario"] = scenario_id
            deliveries.append(del_dict)
    return jsonify(success_response(deliveries))


@app.route('/sap/opu/odata/sap/api/v1/deliveries/<vbeln>', methods=['GET'])
def get_delivery(vbeln: str):
    """Get specific delivery with items"""
    for scenario in SCENARIOS_DB.values():
        if "delivery" in scenario:
            delivery = scenario["delivery"]
            if delivery["header"].VBELN == vbeln:
                result = {
                    "header": dataclass_to_dict(delivery["header"]),
                    "items": [dataclass_to_dict(item) for item in delivery["items"]],
                }
                return jsonify(success_response(result))
    return error_response(f"Delivery {vbeln} not found", 404)


@app.route('/sap/opu/odata/sap/api/v1/invoices', methods=['GET'])
def get_invoices():
    """Get all billing documents (VBRK)"""
    invoices = []
    for scenario_id, scenario in SCENARIOS_DB.items():
        if "invoice" in scenario:
            invoice = scenario["invoice"]
            inv_dict = dataclass_to_dict(invoice["header"])
            inv_dict["_items_count"] = len(invoice["items"])
            inv_dict["_scenario"] = scenario_id
            invoices.append(inv_dict)
    return jsonify(success_response(invoices))


@app.route('/sap/opu/odata/sap/api/v1/invoices/<vbeln>', methods=['GET'])
def get_invoice(vbeln: str):
    """Get specific invoice with items"""
    for scenario in SCENARIOS_DB.values():
        if "invoice" in scenario:
            invoice = scenario["invoice"]
            if invoice["header"].VBELN == vbeln:
                result = {
                    "header": dataclass_to_dict(invoice["header"]),
                    "items": [dataclass_to_dict(item) for item in invoice["items"]],
                }
                return jsonify(success_response(result))
    return error_response(f"Invoice {vbeln} not found", 404)


@app.route('/sap/opu/odata/sap/api/v1/documentary-credits', methods=['GET'])
def get_documentary_credits():
    """Get all documentary credits"""
    lcs = []
    for scenario_id, scenario in SCENARIOS_DB.items():
        if "documentary_credit" in scenario:
            lc = scenario["documentary_credit"]
            lc_dict = dataclass_to_dict(lc)
            lc_dict["_scenario"] = scenario_id
            lcs.append(lc_dict)
    return jsonify(success_response(lcs))


@app.route('/sap/opu/odata/sap/api/v1/documentary-credits/<lcnum>', methods=['GET'])
def get_documentary_credit(lcnum: str):
    """Get specific documentary credit"""
    for scenario in SCENARIOS_DB.values():
        if "documentary_credit" in scenario:
            lc = scenario["documentary_credit"]
            if lc.LCNUM == lcnum:
                return jsonify(success_response(dataclass_to_dict(lc)))
    return error_response(f"Documentary Credit {lcnum} not found", 404)


# ============================================================================
# API Endpoints - W3C VC Format
# ============================================================================

@app.route('/vc/api/v1/scenarios/<scenario_id>/verifiable-credentials', methods=['GET'])
def get_scenario_vcs(scenario_id: str):
    """
    Get all W3C Verifiable Credentials for a scenario
    
    Query params:
    - format: 'vc' (default) or 'sap' (original SAP format)
    """
    if scenario_id not in SCENARIOS_DB:
        return error_response(f"Scenario {scenario_id} not found", 404)
    
    scenario = SCENARIOS_DB[scenario_id]
    vcs = convert_sap_scenario_to_vcs(scenario)
    
    return jsonify({
        "scenario": scenario_id,
        "description": scenario.get("description", ""),
        "credentials": vcs,
    })


@app.route('/vc/api/v1/purchase-orders/<ebeln>/vc', methods=['GET'])
def get_purchase_order_vc(ebeln: str):
    """Convert purchase order to W3C VC"""
    for scenario in SCENARIOS_DB.values():
        if "purchase_order" in scenario:
            po = scenario["purchase_order"]
            if po["header"].EBELN == ebeln:
                vc = vc_mapper.map_purchase_order(po["header"], po["items"])
                return jsonify(vc)
    return error_response(f"Purchase Order {ebeln} not found", 404)


@app.route('/vc/api/v1/invoices/<vbeln>/vc', methods=['GET'])
def get_invoice_vc(vbeln: str):
    """Convert invoice to W3C VC"""
    for scenario in SCENARIOS_DB.values():
        if "invoice" in scenario:
            invoice = scenario["invoice"]
            if invoice["header"].VBELN == vbeln:
                vc = vc_mapper.map_commercial_invoice(
                    invoice["header"], invoice["items"]
                )
                return jsonify(vc)
    return error_response(f"Invoice {vbeln} not found", 404)


@app.route('/vc/api/v1/deliveries/<vbeln>/vc', methods=['GET'])
def get_delivery_vc(vbeln: str):
    """Convert delivery to Bill of Lading VC"""
    for scenario in SCENARIOS_DB.values():
        if "delivery" in scenario:
            delivery = scenario["delivery"]
            if delivery["header"].VBELN == vbeln:
                vc = vc_mapper.map_bill_of_lading(
                    delivery["header"], delivery["items"]
                )
                return jsonify(vc)
    return error_response(f"Delivery {vbeln} not found", 404)


@app.route('/vc/api/v1/documentary-credits/<lcnum>/vc', methods=['GET'])
def get_lc_vc(lcnum: str):
    """Convert documentary credit to W3C VC"""
    for scenario in SCENARIOS_DB.values():
        if "documentary_credit" in scenario:
            lc = scenario["documentary_credit"]
            if lc.LCNUM == lcnum:
                vc = vc_mapper.map_documentary_credit(lc)
                return jsonify(vc)
    return error_response(f"Documentary Credit {lcnum} not found", 404)


# ============================================================================
# Master Data Endpoints
# ============================================================================

@app.route('/sap/opu/odata/sap/api/v1/partners', methods=['GET'])
def get_partners():
    """Get all business partners"""
    partners_list = [dataclass_to_dict(p) for p in PARTNERS.values()]
    return jsonify(success_response(partners_list))


@app.route('/sap/opu/odata/sap/api/v1/partners/<partner_num>', methods=['GET'])
def get_partner_by_num(partner_num: str):
    """Get specific business partner"""
    partner = get_partner(partner_num)
    if partner:
        return jsonify(success_response(dataclass_to_dict(partner)))
    return error_response(f"Partner {partner_num} not found", 404)


@app.route('/sap/opu/odata/sap/api/v1/materials', methods=['GET'])
def get_materials():
    """Get all materials"""
    materials_list = [dataclass_to_dict(m) for m in MATERIALS.values()]
    return jsonify(success_response(materials_list))


@app.route('/sap/opu/odata/sap/api/v1/materials/<matnr>', methods=['GET'])
def get_material_by_num(matnr: str):
    """Get specific material"""
    material = get_material(matnr)
    if material:
        return jsonify(success_response(dataclass_to_dict(material)))
    return error_response(f"Material {matnr} not found", 404)


# ============================================================================
# Root and Health Check
# ============================================================================

@app.route('/')
def root():
    """API documentation"""
    return jsonify({
        "service": "SAP API Simulator for International Trade",
        "version": "1.0.0",
        "description": "Simulates SAP ERP OData services and provides W3C VC conversion",
        "endpoints": {
            "sap_format": {
                "scenarios": "/sap/opu/odata/sap/api/v1/scenarios",
                "purchase_orders": "/sap/opu/odata/sap/api/v1/purchase-orders",
                "sales_orders": "/sap/opu/odata/sap/api/v1/sales-orders",
                "deliveries": "/sap/opu/odata/sap/api/v1/deliveries",
                "invoices": "/sap/opu/odata/sap/api/v1/invoices",
                "documentary_credits": "/sap/opu/odata/sap/api/v1/documentary-credits",
                "partners": "/sap/opu/odata/sap/api/v1/partners",
                "materials": "/sap/opu/odata/sap/api/v1/materials",
            },
            "vc_format": {
                "scenario_vcs": "/vc/api/v1/scenarios/{scenario_id}/verifiable-credentials",
                "purchase_order_vc": "/vc/api/v1/purchase-orders/{ebeln}/vc",
                "invoice_vc": "/vc/api/v1/invoices/{vbeln}/vc",
                "delivery_vc": "/vc/api/v1/deliveries/{vbeln}/vc",
                "documentary_credit_vc": "/vc/api/v1/documentary-credits/{lcnum}/vc",
            }
        },
        "demo_scenarios": list(SCENARIOS_DB.keys()),
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "SAP API Simulator"})


# ============================================================================
# Run Server
# ============================================================================

if __name__ == '__main__':
    print("="*70)
    print("SAP API Simulator for International Trade")
    print("="*70)
    print("\nStarting server on http://localhost:5000")
    print("\nAvailable scenarios:")
    for scenario_id in SCENARIOS_DB.keys():
        print(f"  - {scenario_id}")
    print("\nAPI Documentation: http://localhost:5000/")
    print("="*70)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
