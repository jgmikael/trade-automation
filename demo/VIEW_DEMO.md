# 🚀 How to View the Latest Demo

## ✅ **Demo Server is RUNNING**

**Local URL:** http://localhost:9000

Just open this URL in your browser!

---

## 📋 **What You'll See**

### 3 Navigation Tabs:

#### 1. 👥 **Document Actors**
- View documents from each party's perspective
- 7 actor views (Buyer, Seller, Bank, Carrier, Customs, Chamber, Certifier)
- Click any actor to see their documents
- Click any document card to view full SHACL JSON

#### 2. ⏱️ **Timeline**
- 16 chronological events from order to delivery
- See what happens when
- Click events to view associated documents

#### 3. 🔄 **Document Flow** ⭐ NEW!
- **5 process stages** showing the complete workflow
- **Color-coded cards** by who creates each document
- **Click any card** to see:
  - Who creates it
  - What documents it requires (dependencies)
  - What documents it triggers next
  - Full JSON data
- **Interactive navigation** - click dependencies/triggers to jump to those docs

---

## 🎯 **Testing the Flow Feature**

1. Open: **http://localhost:9000**
2. Click the **"🔄 Document Flow"** tab
3. You'll see 5 horizontal stages:
   - Stage 1: Negotiation & Contract
   - Stage 2: Preparation & Certification
   - Stage 3: Documentation & Export
   - Stage 4: Transit & Payment
   - Stage 5: Import & Delivery

4. **Click** the first card: **"📝 Purchase Order"**
5. Notice it shows:
   - "Created by: Buyer (Tokyo Construction)"
   - "Triggers Creation Of: Documentary Credit (L/C)"
   
6. **Click** "Documentary Credit" in the green triggers section
7. Now you'll see:
   - "Requires These Documents First: Purchase Order"
   - "Triggers Creation Of: Regulatory Certificate, Phytosanitary Certificate, Warehouse Receipt"

8. **Keep clicking** to follow the flow through all 15 documents!

---

## 🎨 **Color Coding**

Documents are color-coded by who creates them:

- 🔵 **Blue** - Buyer
- 🟢 **Green** - Seller  
- 🟠 **Orange** - Bank
- 🟦 **Cyan** - Carrier
- 🟣 **Purple** - Customs
- 🩷 **Pink** - Chamber of Commerce
- 🩵 **Teal** - Certifier

---

## 🛠️ **If Server Not Running**

```bash
cd ~/.openclaw/workspace/trade-automation/demo
python3 -m http.server 9000
# Then open: http://localhost:9000
```

---

## 🐛 **Troubleshooting**

### Issue: "Can't connect" or "Connection refused"

**Solution:** Restart the server:
```bash
# Kill any existing server
pkill -f "python3 -m http.server 9000"

# Start fresh
cd ~/.openclaw/workspace/trade-automation/demo
python3 -m http.server 9000
```

### Issue: "Old version showing"

**Solution:** Hard refresh your browser:
- **Chrome/Firefox:** Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
- **Safari:** Cmd+Option+R

### Issue: "Flow tab not showing"

**Solution:** Use the latest file:
```bash
cd ~/.openclaw/workspace/trade-automation
git pull origin master
cd demo
# Restart server
```

Or use **standalone.html** which has everything embedded:
```bash
open standalone.html
```

---

## 📊 **What's New in This Version**

✨ **Interactive Document Flow Visualization**
- Visual flowchart showing all 15 documents
- Grouped into 5 logical process stages
- Color-coded by document creator
- Click to see dependencies and triggers
- Navigate through the entire workflow

✅ **Makes It Clear:**
- Who creates what document
- What order documents are created
- What triggers the next document
- How parties coordinate

---

## 🌐 **Sharing the Demo**

### For Local Presentation:
Use the running server at http://localhost:9000

### For Remote Sharing:
Use **standalone.html** (65KB, all-in-one file):
```bash
# Copy this file to share:
~/.openclaw/workspace/trade-automation/demo/standalone.html
```

### For GitHub Pages:
Enable Pages in repository settings, then access at:
```
https://jgmikael.github.io/trade-automation/
```

---

## 📞 **Quick Help**

**Server URL:** http://localhost:9000
**Server Log:** `/tmp/demo_server.log`
**Server PID:** `/tmp/demo_server.pid`

**Stop Server:**
```bash
kill $(cat /tmp/demo_server.pid)
```

**Restart Server:**
```bash
cd ~/.openclaw/workspace/trade-automation/demo
python3 -m http.server 9000
```

---

**🎉 Enjoy the demo! The Document Flow visualization shows exactly how documents flow between parties in international trade.**
