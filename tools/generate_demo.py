#!/usr/bin/env python3
"""
Generate demo/demo.js from scenario_gluelam_timber_full.py
"""

import sys
import json

# Import the scenario
sys.path.insert(0, '.')
from scenario_gluelam_timber_full import DOCUMENTS, ACTOR_VIEWS, TIMELINE, DOC_IDS

def generate_demo_js():
    """Generate demo.js with all documents and actor views"""
    
    # Convert documents to JavaScript format
    documents_json = json.dumps(DOCUMENTS, indent=2, ensure_ascii=False)
    actor_views_json = json.dumps(ACTOR_VIEWS, indent=2, ensure_ascii=False)
    timeline_json = json.dumps(TIMELINE, indent=2, ensure_ascii=False)
    doc_ids_json = json.dumps(DOC_IDS, indent=2, ensure_ascii=False)
    
    js_content = f'''// demo.js - Finnish Gluelam Timber to Japan Trade Demo
// All 15 relevant KTDDE documents for the trade
// Generated from scenario_gluelam_timber_full.py

// Document metadata
const docInfo = {{
  purchase_order: {{
    title: "Purchase Order",
    icon: "📝",
    description: "Buyer's order for gluelam timber beams"
  }},
  documentary_credit: {{
    title: "Documentary Credit (L/C)",
    icon: "🏦",
    description: "Confirmed irrevocable letter of credit from MUFG Bank"
  }},
  bill_of_lading: {{
    title: "Bill of Lading",
    icon: "🚢",
    description: "Ocean transport document from FESCO"
  }},
  commercial_invoice: {{
    title: "Commercial Invoice",
    icon: "📄",
    description: "Seller's invoice for EUR 339,000"
  }},
  certificate_of_origin: {{
    title: "Certificate of Origin",
    icon: "📜",
    description: "Finnish Chamber of Commerce certificate"
  }},
  packing_list: {{
    title: "Packing List",
    icon: "📦",
    description: "Detailed packing information for 8 bundles"
  }},
  insurance_certificate: {{
    title: "Insurance Certificate",
    icon: "🛡️",
    description: "All Risks marine cargo insurance"
  }},
  phytosanitary_certificate: {{
    title: "Phytosanitary Certificate",
    icon: "🌲",
    description: "ISPM-15 compliant wood treatment certificate"
  }},
  customs_declaration_export: {{
    title: "Customs Declaration (Export)",
    icon: "🛃",
    description: "Finnish export customs clearance"
  }},
  customs_declaration_import: {{
    title: "Customs Declaration (Import)",
    icon: "🛃",
    description: "Japanese import customs clearance"
  }},
  delivery_note: {{
    title: "Delivery Note",
    icon: "🚚",
    description: "Final delivery to construction site"
  }},
  regulatory_certificate: {{
    title: "Regulatory Certificate",
    icon: "✅",
    description: "CE marking for structural timber (EN 14080)"
  }},
  sea_cargo_manifest: {{
    title: "Sea Cargo Manifest",
    icon: "📋",
    description: "Vessel manifest for MV Baltic Express"
  }},
  warehouse_receipt: {{
    title: "Warehouse Receipt",
    icon: "🏭",
    description: "Rauma Port warehouse receipt"
  }},
  payment_confirmation: {{
    title: "Payment Confirmation",
    icon: "💰",
    description: "Bank payment confirmation via L/C"
  }}
}};

// All documents (SHACL-based JSON)
const documents = {documents_json};

// Document IDs for reference
const docIds = {doc_ids_json};

// Actor views (which documents each actor sees)
const actorViews = {actor_views_json};

// Timeline events
const timeline = {timeline_json};

// Actor information
const actors = [
  {{ id: 'buyer', name: 'Buyer', icon: '🏢', description: 'Tokyo Construction Materials Ltd' }},
  {{ id: 'seller', name: 'Seller', icon: '🏭', description: 'Nordic Timber Oy' }},
  {{ id: 'bank', name: 'Bank', icon: '🏦', description: 'MUFG Tokyo / Nordea Finland' }},
  {{ id: 'carrier', name: 'Carrier', icon: '🚢', description: 'FESCO Shipping' }},
  {{ id: 'customs', name: 'Customs', icon: '🛃', description: 'Finnish & Japanese Customs' }},
  {{ id: 'chamber', name: 'Chamber', icon: '📜', description: 'Finnish Chamber of Commerce' }},
  {{ id: 'certifier', name: 'Certifier', icon: '✅', description: 'TÜV SÜD & Food Authority' }}
];

// Current state
let currentActor = 'buyer';
let currentDoc = null;

// Initialize demo
function initDemo() {{
  renderActorTabs();
  renderDocuments(currentActor);
  renderTimeline();
}}

// Render actor tabs
function renderActorTabs() {{
  const container = document.getElementById('actor-tabs');
  if (!container) return;
  
  container.innerHTML = actors.map(actor => `
    <button class="actor-tab ${{actor.id === currentActor ? 'active' : ''}}"
            onclick="switchActor('${{actor.id}}')">
      <span class="actor-icon">${{actor.icon}}</span>
      <span class="actor-name">${{actor.name}}</span>
      <small>${{actor.description}}</small>
    </button>
  `).join('');
}}

// Switch actor view
function switchActor(actorId) {{
  currentActor = actorId;
  renderActorTabs();
  renderDocuments(actorId);
}}

// Render documents for actor
function renderDocuments(actorId) {{
  const container = document.getElementById('documents-grid');
  if (!container) return;
  
  const actorDocs = actorViews[actorId] || [];
  
  if (actorDocs.length === 0) {{
    container.innerHTML = '<p class="no-docs">No documents for this actor</p>';
    return;
  }}
  
  container.innerHTML = actorDocs.map(docKey => {{
    const info = docInfo[docKey];
    const doc = documents[docKey];
    
    if (!info || !doc) return '';
    
    return `
      <div class="document-card" onclick="showDocument('${{docKey}}')">
        <div class="doc-icon">${{info.icon}}</div>
        <div class="doc-title">${{info.title}}</div>
        <div class="doc-description">${{info.description}}</div>
      </div>
    `;
  }}).join('');
}}

// Show document modal
function showDocument(docKey) {{
  currentDoc = docKey;
  const info = docInfo[docKey];
  const doc = documents[docKey];
  
  if (!info || !doc) return;
  
  const modal = document.getElementById('doc-modal');
  const title = document.getElementById('doc-modal-title');
  const content = document.getElementById('doc-modal-content');
  
  title.innerHTML = `${{info.icon}} ${{info.title}}`;
  content.innerHTML = `<pre class="json-display">${{syntaxHighlight(JSON.stringify(doc, null, 2))}}</pre>`;
  
  modal.style.display = 'flex';
}}

// Close modal
function closeModal() {{
  document.getElementById('doc-modal').style.display = 'none';
  currentDoc = null;
}}

// Syntax highlighting for JSON
function syntaxHighlight(json) {{
  json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return json.replace(/("(\\\\u[a-zA-Z0-9]{{4}}|\\\\[^u]|[^\\\\"])*"(\\s*:)?|\\b(true|false|null)\\b|-?\\d+(?:\\\\.\\d*)?(?:[eE][+\\\\-]?\\d+)?)/g, function (match) {{
    let cls = 'json-number';
    if (/^"/.test(match)) {{
      if (/:$/.test(match)) {{
        cls = 'json-key';
      }} else {{
        cls = 'json-string';
      }}
    }} else if (/true|false/.test(match)) {{
      cls = 'json-boolean';
    }} else if (/null/.test(match)) {{
      cls = 'json-null';
    }}
    return '<span class="' + cls + '">' + match + '</span>';
  }});
}}

// Render timeline
function renderTimeline() {{
  const container = document.getElementById('timeline-view');
  if (!container) return;
  
  container.innerHTML = timeline.map(event => `
    <div class="timeline-event ${{event.doc ? 'clickable' : ''}}" 
         ${{event.doc ? `onclick="showDocument('${{event.doc}}')"` : ''}}>
      <div class="timeline-date">${{event.date}}</div>
      <div class="timeline-marker"></div>
      <div class="timeline-content">
        <strong>${{event.event}}</strong>
        <small>${{event.actor}}</small>
      </div>
    </div>
  `).join('');
}}

// Close modal on escape
document.addEventListener('keydown', (e) => {{
  if (e.key === 'Escape' && currentDoc) {{
    closeModal();
  }}
}});

// Close modal on click outside
document.getElementById('doc-modal')?.addEventListener('click', (e) => {{
  if (e.target.id === 'doc-modal') {{
    closeModal();
  }}
}});

// Initialize when DOM is ready
if (document.readyState === 'loading') {{
  document.addEventListener('DOMContentLoaded', initDemo);
}} else {{
  initDemo();
}}
'''
    
    return js_content

def main():
    """Generate demo.js"""
    print("Generating demo/demo.js...")
    
    js_content = generate_demo_js()
    
    with open('demo/demo.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✅ Generated demo/demo.js ({len(js_content)} bytes)")
    print(f"   📦 {len(DOCUMENTS)} documents")
    print(f"   👥 {len(ACTOR_VIEWS)} actors")
    print(f"   ⏱️  {len(TIMELINE)} timeline events")

if __name__ == "__main__":
    main()
