# 🌍 International Trade Document Flow Demo

Interactive browser-based demonstration of 15 KTDDE trade documents for Finnish gluelam timber export to Japan.

## 🚀 How to View the Demo

### ⚠️ Important: Cannot View on GitHub Directly

HTML files on GitHub **do not execute JavaScript** in preview mode. You must use one of these methods:

---

### ✅ Method 1: GitHub Pages (RECOMMENDED - Live URL)

**After setup, the demo will be available at:**
```
https://jgmikael.github.io/trade-automation/
```

**Setup steps (one-time):**

1. Go to repository settings: https://github.com/jgmikael/trade-automation/settings/pages
2. Under "Build and deployment":
   - **Source**: Select "GitHub Actions"
3. Push any commit to trigger deployment
4. Wait ~2 minutes for deployment
5. Visit the URL above

**Status check:**
- GitHub Actions: https://github.com/jgmikael/trade-automation/actions

---

### ✅ Method 2: Download and Open Locally

**Option A: Download ZIP**
```bash
# Download from GitHub
https://github.com/jgmikael/trade-automation/archive/refs/heads/master.zip

# Extract and open
cd trade-automation-master/demo
open index.html              # macOS
xdg-open index.html          # Linux  
start index.html             # Windows
```

**Option B: Git Clone**
```bash
git clone https://github.com/jgmikael/trade-automation.git
cd trade-automation/demo
open index.html
```

---

### ✅ Method 3: Local Web Server (Best for Development)

```bash
cd demo

# Python 3
python3 -m http.server 8080

# Python 2
python -m SimpleHTTPServer 8080

# Node.js
npx http-server -p 8080

# PHP
php -S localhost:8080

# Then open: http://localhost:8080
```

---

### ✅ Method 4: Standalone HTML (No External Files)

The `standalone.html` file has all JavaScript embedded inline:

```bash
# Just double-click or:
open standalone.html
```

This works even without a web server!

---

## 📋 What's in the Demo

### 15 Trade Documents

1. **Purchase Order** - Buyer's order (EUR 339k)
2. **Documentary Credit** - Confirmed L/C from MUFG Bank
3. **Bill of Lading** - FESCO ocean transport
4. **Commercial Invoice** - Seller's invoice
5. **Certificate of Origin** - Finnish Chamber of Commerce
6. **Packing List** - 8 timber bundles
7. **Insurance Certificate** - All Risks marine cargo
8. **Phytosanitary Certificate** - ISPM-15 wood treatment
9. **Customs Declaration (Export)** - Finnish customs
10. **Customs Declaration (Import)** - Japanese customs
11. **Delivery Note** - Final delivery to construction site
12. **Regulatory Certificate** - CE marking (EN 14080:2013)
13. **Sea Cargo Manifest** - Vessel manifest
14. **Warehouse Receipt** - Rauma Port storage
15. **Payment Confirmation** - Bank payment via L/C

### 7 Actor Perspectives

- **🏢 Buyer** (Tokyo Construction Materials) - 10 documents
- **🏭 Seller** (Nordic Timber Oy) - 13 documents
- **🏦 Bank** (MUFG / Nordea) - 9 documents
- **🚢 Carrier** (FESCO) - 6 documents
- **🛃 Customs** (Finnish & Japanese) - 7 documents
- **📜 Chamber of Commerce** (Finland) - 2 documents
- **✅ Certifier** (TÜV SÜD & Food Authority) - 2 documents

### Timeline View

16 chronological events from Purchase Order (T-45 days) to final delivery.

---

## 🎯 Demo Features

- ✅ **Zero dependencies** - Pure HTML, CSS, JavaScript
- ✅ **Responsive design** - Works on mobile, tablet, desktop
- ✅ **Interactive cards** - Click any document to view full JSON
- ✅ **Syntax highlighting** - Color-coded JSON display
- ✅ **Actor switching** - See documents from different perspectives
- ✅ **Timeline view** - Chronological event flow
- ✅ **Real data** - Based on actual KTDDE standards

---

## 🔧 Files in This Directory

| File | Description | Size |
|------|-------------|------|
| `index.html` | Main demo page (external JS) | 13 KB |
| `demo.js` | Document data and logic | 34 KB |
| `standalone.html` | All-in-one file (inline JS) | 48 KB |
| `index_simple.html` | Diagnostic test page | 4 KB |
| `minimal_test.html` | JavaScript test | 1 KB |

---

## 🐛 Troubleshooting

### Issue: Page is blank or shows "Loading..."

**Cause**: JavaScript is disabled or blocked

**Solutions**:
1. Enable JavaScript in browser settings
2. Use `standalone.html` instead
3. Try a different browser (Chrome, Firefox, Safari)

### Issue: "Cannot read property of undefined"

**Cause**: `demo.js` failed to load

**Solutions**:
1. Use a web server (Method 3) instead of opening file directly
2. Use `standalone.html` (all JS is inline)
3. Check browser console for errors (F12 → Console)

### Issue: Fonts look weird or layout broken

**Cause**: CSS failed to load

**Solutions**:
1. All CSS is inline in HTML - should always work
2. Try hard refresh: Ctrl+Shift+R (Cmd+Shift+R on Mac)

---

## 📊 Trade Scenario Details

| Aspect | Details |
|--------|---------|
| **Exporter** | Nordic Timber Oy, Kuhmo, Finland 🇫🇮 |
| **Importer** | Tokyo Construction Materials Ltd, Japan 🇯🇵 |
| **Product** | Engineered Gluelam Timber (GL30c, GL32h) |
| **Value** | EUR 339,000 CFR Tokyo Port |
| **Quantity** | 160 pieces (120× GL30c + 40× GL32h) |
| **Weight** | 28,800 kg (8 timber bundles) |
| **Volume** | 156 cubic meters |
| **Route** | Rauma Port, FI → Tokyo Port, JP (~45 days) |
| **Carrier** | FESCO (Far Eastern Shipping Company) |
| **Payment** | Confirmed Irrevocable Letter of Credit (60 days) |
| **Standards** | ISPM-15, EN 14080:2013, CE marking |

---

## 🌐 For Presentations

**Best viewing method**: GitHub Pages (Method 1)
- Clean URL to share
- No local setup required
- Works on any device with browser
- Can present directly from URL

**For offline demos**: Use `standalone.html`
- Works without internet
- No server required
- Single file to share

---

## 📞 Support

**Issue**: Demo not working?  
**Try**: `minimal_test.html` first to test if JavaScript works

**Issue**: Still broken?  
**Contact**: Open an issue at https://github.com/jgmikael/trade-automation/issues

---

## 🎓 Technical Details

- **Standards**: KTDDE OWL, W3C VC 1.1, SHACL
- **Format**: SHACL-based JSON (not W3C VCs yet - stage 1)
- **Framework**: None (vanilla JavaScript)
- **Browser**: Any modern browser (Chrome 90+, Firefox 88+, Safari 14+)
- **Mobile**: Fully responsive, works on phones/tablets

---

**Built with ❤️ for global trade digitalization**

🇫🇮 Finland 🤝 🇯🇵 Japan 🤝 🌍 World
