# KTDDE Trade Documents Browser Demo

Interactive browser-based demonstration of KTDDE standardized trade documents for international trade.

## Scenario

**Finnish Gluelam Timber Export to Japan**

- **Exporter:** Nordic Timber Oy, Kuhmo, Finland 🇫🇮
- **Importer:** Tokyo Construction Materials Ltd, Tokyo, Japan 🇯🇵
- **Product:** Engineered gluelam timber beams for construction
- **Quantity:** 160 beams (120× GL30c + 40× GL32h)
- **Value:** EUR 339,000
- **Incoterms:** CFR Tokyo Port
- **Payment:** Confirmed Irrevocable Letter of Credit (60 days)
- **Transport:** Sea freight via FESCO (~45 days transit)

## Documents Showcased

1. **Purchase Order** - Buyer's order to seller
2. **Documentary Credit (Letter of Credit)** - Bank guarantee
3. **Bill of Lading** - Carrier's receipt and transport document
4. **Commercial Invoice** - Seller's invoice
5. **Certificate of Origin** - Origin certification from Chamber of Commerce

## Actors

The demo shows the document flow from different actor perspectives:

- **🏢 Buyer (Tokyo Construction)** - Receives and reviews documents
- **🏭 Seller (Nordic Timber)** - Creates and sends documents
- **🏦 Bank (MUFG / Nordea)** - Manages L/C and payments
- **🚢 Carrier (FESCO)** - Issues Bill of Lading
- **🛃 Customs (FI & JP)** - Reviews all trade documents
- **📜 Chamber of Commerce** - Issues Certificate of Origin

## Features

✅ **SHACL-Based JSON** - Documents formatted according to KTDDE SHACL profiles  
✅ **Actor Views** - See what each party creates/receives  
✅ **Timeline** - Chronological flow of the trade process  
✅ **Interactive** - Click documents to view full KTDDE JSON  
✅ **Realistic Data** - Based on actual international trade requirements  
✅ **No Backend Required** - Pure frontend demo

## Quick Start

### Option 1: Direct Browser (Simplest)

```bash
cd demo
# Open index.html in your browser
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

### Option 2: Local HTTP Server (Recommended)

```bash
cd demo

# Python 3
python3 -m http.server 8080

# Node.js
npx http-server -p 8080

# Then open: http://localhost:8080
```

### Option 3: With SAP API (Advanced)

If you want to fetch live data from the SAP simulator:

```bash
# Terminal 1: Start SAP API
cd ../sap-simulator
python3 api/sap_api.py

# Terminal 2: Serve demo
cd ../demo
python3 -m http.server 8080

# Open: http://localhost:8080
```

## Usage

1. **View Timeline** - See the chronological flow of documents
2. **Click Actor Tabs** - Switch between different party perspectives
3. **Click Document Cards** - View full KTDDE JSON structure
4. **Explore** - See how different actors interact with same documents

## Document Format

Documents are displayed in **KTDDE SHACL-based JSON** format:

```json
{
  "@type": "CommercialInvoice",
  "invoiceNumber": "9000002000",
  "invoiceDate": "2024-02-10",
  "buyerParty": {
    "@type": "Party",
    "partyName": "Tokyo Construction Materials Ltd",
    "hasAddress": {
      "@type": "Address",
      "city": "Tokyo",
      "country": {
        "@type": "Country",
        "countryCode": "JP"
      }
    }
  },
  "totalAmount": {
    "@type": "MonetaryAmount",
    "amountValue": 339000.00,
    "currencyCode": "EUR"
  }
}
```

**Note:** These are SHACL-based JSON documents, NOT full W3C Verifiable Credentials (VC stage 1).

## Demonstration Points

### For EU Business Wallet

- Shows KTDDE standardization of trade documents
- Demonstrates semantic interoperability
- Highlights multi-party document exchange
- Real-world Finnish export scenario

### For Japan / Asia

- Tokyo-based importer receiving EU goods
- Japanese customs integration
- Asia-Pacific banking (MUFG)
- HS codes, phytosanitary requirements

### For ICC DSI (Singapore)

- Digital standards implementation
- Bill of Lading digitalization
- Letter of Credit workflow
- Multiple jurisdiction compliance

## Technical Details

### Technology Stack

- **Frontend:** Pure HTML5 + CSS3 + Vanilla JavaScript
- **Data Format:** KTDDE SHACL-based JSON
- **No Dependencies:** No frameworks, no build step
- **Responsive:** Works on desktop, tablet, mobile

### Document Sources

Documents based on:
- SAP ERP structures (EKKO, VBAK, LIKP, VBRK)
- KTDDE OWL vocabulary v0.0.5
- SHACL application profiles from tietomallit.suomi.fi
- Real international trade requirements

### Customization

To add more documents, edit `demo.js`:

1. Add document to `documents` object
2. Add document key to relevant actors in `actorDocuments`
3. Include in timeline if needed

```javascript
documents.newDocument = {
    id: 'DOC-ID',
    type: 'DocumentType',
    title: 'Document Title',
    number: 'DOC-123',
    date: 'T-X days',
    status: 'created',
    visibleTo: ['actor1', 'actor2'],
    createdBy: 'actor1',
    data: {
        '@type': 'DocumentType',
        // KTDDE SHACL structure here
    }
};
```

## Future Enhancements

- [ ] Add W3C Verifiable Credential format toggle
- [ ] Implement digital signatures visualization
- [ ] Add more document types (Packing List, etc.)
- [ ] Show validation status
- [ ] Export documents
- [ ] Multi-language support (Finnish, Japanese)

## Browser Compatibility

Tested on:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Demo URL

Once deployed, this demo will be accessible at:
`https://yourdomain.com/trade-demo/`

## Questions?

For demo questions or to discuss implementation for your organization, contact the KTDDE project team.

---

**Developed for demonstration to:**
- European Union (EU Business Wallet initiative)
- Japan (Cross-border trade digitalization)
- Singapore (ICC DSI)
- Global trade digitalization initiatives
