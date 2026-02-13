# SAP API Simulator for International Trade

Production-quality SAP ERP API simulator with W3C Verifiable Credential conversion for international trade documents.

## Purpose

Demonstrates digital transformation of trade documents for:
- **European Union** (EU Business Wallet integration)
- **Singapore** (ICC DSI participant)
- **Japan** (Cross-border trade digitalization)
- **Global actors** (Standards-based interoperability)

## Features

### SAP Modules Simulated
- **MM (Materials Management)** - Purchase Orders
- **SD (Sales & Distribution)** - Sales Orders, Deliveries, Invoices
- **Banking Integration** - Documentary Credits / Letters of Credit

### Two API Modes

1. **SAP OData Format** - Traditional SAP ERP REST API
2. **W3C VC Format** - KTDDE-based Verifiable Credentials

### Realistic Sample Data

**Trade Scenarios:**
- EU → Singapore: Machinery export with CIF Incoterms, L/C payment
- EU → Japan: Electronics export with FOB Incoterms, confirmed L/C

**Master Data:**
- Business partners (EU and Asian companies)
- Materials (industrial machinery, electronics, components)
- HS codes, country of origin, weights

## Architecture

```
sap-simulator/
├── models/
│   └── sap_structures.py      # SAP table structures (EKKO, VBAK, etc.)
├── data/
│   └── sample_data.py          # Realistic trade scenarios
├── mappings/
│   └── sap_to_vc.py           # SAP → W3C VC transformation
├── api/
│   └── sap_api.py             # Flask REST API
├── tests/
│   └── (test files)
└── requirements.txt
```

## Installation

```bash
cd sap-simulator

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Start the API Server

```bash
python3 api/sap_api.py
```

Server starts on `http://localhost:5000`

### 2. Explore Available Scenarios

```bash
curl http://localhost:5000/sap/opu/odata/sap/api/v1/scenarios
```

**Returns:**
- `EU_TO_SINGAPORE_MACHINERY_EXPORT`
- `EU_TO_JAPAN_ELECTRONICS_EXPORT`

### 3. Get SAP Documents (Traditional Format)

**Purchase Order:**
```bash
curl http://localhost:5000/sap/opu/odata/sap/api/v1/purchase-orders/4500000123
```

**Commercial Invoice:**
```bash
curl http://localhost:5000/sap/opu/odata/sap/api/v1/invoices/9000000789
```

**Delivery (for Bill of Lading):**
```bash
curl http://localhost:5000/sap/opu/odata/sap/api/v1/deliveries/8000000456
```

**Documentary Credit:**
```bash
curl http://localhost:5000/sap/opu/odata/sap/api/v1/documentary-credits/LC-HSBC-SG-2024-00789
```

### 4. Get W3C Verifiable Credentials

**All credentials for a scenario:**
```bash
curl http://localhost:5000/vc/api/v1/scenarios/EU_TO_SINGAPORE_MACHINERY_EXPORT/verifiable-credentials
```

**Individual credentials:**
```bash
# Purchase Order VC
curl http://localhost:5000/vc/api/v1/purchase-orders/4500000123/vc

# Commercial Invoice VC
curl http://localhost:5000/vc/api/v1/invoices/9000000789/vc

# Bill of Lading VC
curl http://localhost:5000/vc/api/v1/deliveries/8000000456/vc

# Documentary Credit VC
curl http://localhost:5000/vc/api/v1/documentary-credits/LC-HSBC-SG-2024-00789/vc
```

## API Endpoints

### SAP Format Endpoints (`/sap/opu/odata/sap/api/v1/`)

| Endpoint | Description |
|----------|-------------|
| `GET /scenarios` | List all trade scenarios |
| `GET /purchase-orders` | List all purchase orders |
| `GET /purchase-orders/{ebeln}` | Get specific PO |
| `GET /sales-orders` | List all sales orders |
| `GET /sales-orders/{vbeln}` | Get specific sales order |
| `GET /deliveries` | List all deliveries |
| `GET /deliveries/{vbeln}` | Get specific delivery |
| `GET /invoices` | List all invoices |
| `GET /invoices/{vbeln}` | Get specific invoice |
| `GET /documentary-credits` | List all L/Cs |
| `GET /documentary-credits/{lcnum}` | Get specific L/C |
| `GET /partners` | List business partners |
| `GET /partners/{partner_num}` | Get specific partner |
| `GET /materials` | List materials |
| `GET /materials/{matnr}` | Get specific material |

### W3C VC Endpoints (`/vc/api/v1/`)

| Endpoint | Description |
|----------|-------------|
| `GET /scenarios/{id}/verifiable-credentials` | All VCs for scenario |
| `GET /purchase-orders/{ebeln}/vc` | PurchaseOrder VC |
| `GET /invoices/{vbeln}/vc` | CommercialInvoice VC |
| `GET /deliveries/{vbeln}/vc` | BillOfLading VC |
| `GET /documentary-credits/{lcnum}/vc` | DocumentaryCredit VC |

## SAP Data Structures

### Purchase Order (MM)
- **EKKO** - PO Header
- **EKPO** - PO Items

### Sales Order (SD)
- **VBAK** - Sales Document Header
- **VBAP** - Sales Document Items

### Delivery (SD)
- **LIKP** - Delivery Header
- **LIPS** - Delivery Items

### Billing/Invoice (SD)
- **VBRK** - Billing Document Header
- **VBRP** - Billing Document Items

### Documentary Credit (Banking)
- **ZBANKF** - L/C Header (Custom Z-table)

## Mapping Logic

### SAP → KTDDE W3C VC

The mapping engine (`mappings/sap_to_vc.py`) handles:

**Field Mappings:**
- SAP partner functions → KTDDE Party
- SAP material data → KTDDE GoodsItem / TradeProduct
- SAP amounts → KTDDE MonetaryAmount / Amount
- SAP Incoterms → KTDDE TradeDeliveryTerms
- SAP payment terms → KTDDE PaymentTerms

**Document Transformations:**
- EKKO/EKPO → PurchaseOrder VC
- VBRK/VBRP → CommercialInvoice VC
- LIKP/LIPS → BillOfLading VC
- Derived → CertificateOfOrigin VC
- ZBANKF → DocumentaryCredit VC

**Context Resolution:**
Uses generated JSON-LD contexts from `/contexts/`

## Sample Scenarios

### Scenario 1: EU → Singapore Machinery Export

**Companies:**
- **Seller:** Nordic Machinery Oy (Finland)
- **Buyer:** Singapore Trading Company Pte Ltd

**Products:**
- 50× Industrial Servo Motor 5kW
- Total: EUR 125,000

**Terms:**
- Incoterms: CIF Singapore Port
- Payment: Letter of Credit (30 days)
- Transport: Sea freight (Maersk)

**Documents:**
- Purchase Order: `4500000123`
- Sales Order: `0100000234`
- Delivery: `8000000456`
- Invoice: `9000000789`
- Bill of Lading: `MAEU123456789`
- Letter of Credit: `LC-HSBC-SG-2024-00789`

### Scenario 2: EU → Japan Electronics Export

**Companies:**
- **Seller:** Deutsche Elektronik GmbH (Germany)
- **Buyer:** Tokyo Industrial Equipment Co Ltd (Japan)

**Products:**
- 100× Industrial Control Unit ICU-500
- 50× Programmable Logic Controller PLC-1200
- Total: EUR 87,500

**Terms:**
- Incoterms: FOB Hamburg Port
- Payment: Confirmed Letter of Credit (45 days)
- Transport: Sea freight (Hapag-Lloyd)

**Documents:**
- Sales Order: `0100000567`
- Delivery: `8000000678`
- Invoice: `9000001012`
- Bill of Lading: `HLCUHAMB20240123`
- Letter of Credit: `LC-MUFG-JP-2024-01234`

## Extending with New Documents

To add new trade documents:

1. **Define SAP Structure** (`models/sap_structures.py`)
```python
@dataclass
class NewDocHeader:
    FIELD1: str
    FIELD2: date
    # ...
```

2. **Add Sample Data** (`data/sample_data.py`)
```python
def scenario_new_document():
    return {...}
```

3. **Create Mapping** (`mappings/sap_to_vc.py`)
```python
def map_new_document(self, header, items):
    return {
        "@context": [...],
        "credentialSubject": {...}
    }
```

4. **Add API Endpoint** (`api/sap_api.py`)
```python
@app.route('/vc/api/v1/new-documents/<id>/vc')
def get_new_document_vc(id):
    # ...
```

## Production Deployment

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "api/sap_api.py"]
```

```bash
docker build -t sap-simulator .
docker run -p 5000:5000 sap-simulator
```

### Environment Variables

```bash
# Flask configuration
export FLASK_ENV=production
export FLASK_SECRET_KEY=your-secret-key

# API base URLs
export VC_BASE_URL=https://example.com
export CONTEXT_BASE_URL=https://github.com/jgmikael/trade-automation/contexts
```

## Testing

```bash
# Run all tests
python -m pytest tests/

# Test specific mapping
python mappings/sap_to_vc.py

# Test API endpoints
curl http://localhost:5000/health
```

## Integration Examples

### JavaScript/TypeScript

```typescript
// Fetch SAP invoice and convert to VC
const response = await fetch(
  'http://localhost:5000/vc/api/v1/invoices/9000000789/vc'
);
const commercialInvoiceVC = await response.json();

// Validate against JSON Schema
import Ajv from 'ajv';
const ajv = new Ajv();
const schema = await fetch('credentials/commercialinvoice-schema.json').then(r => r.json());
const valid = ajv.validate(schema, commercialInvoiceVC);
```

### Python

```python
import requests

# Get all VCs for a scenario
response = requests.get(
    'http://localhost:5000/vc/api/v1/scenarios/EU_TO_SINGAPORE_MACHINERY_EXPORT/verifiable-credentials'
)
vcs = response.json()['credentials']

# Access specific credentials
purchase_order_vc = vcs['purchase_order_vc']
commercial_invoice_vc = vcs['commercial_invoice_vc']
bill_of_lading_vc = vcs['bill_of_lading_vc']
```

## Roadmap

### Phase 1 ✅ (Current)
- SAP MM & SD simulation
- 5 core documents (PO, Invoice, B/L, CoO, L/C)
- W3C VC conversion
- REST API

### Phase 2 (Next 31 Documents)
- Packing List
- Delivery Note
- Customs Declaration
- Export Declaration
- Insurance Certificate
- Quality Certificate
- Inspection Certificate
- ...and 24 more based on KTDDE OWL

### Phase 3 (Advanced Features)
- Digital signatures (proof generation)
- DID resolution
- Webhook notifications
- Event streaming
- Multi-tenant support

## Support

For questions or issues:
- GitHub Issues: https://github.com/jgmikael/trade-automation
- Documentation: See `/docs` directory

## License

(To be determined)

---

**Developed for demonstration to EU, Singapore (ICC DSI), Japan, and global trade digitalization initiatives.**
