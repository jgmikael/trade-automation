#!/usr/bin/env python3
"""
Generate demo/demo.js with interactive document flow
"""

import sys
import json

# Import the scenarios
sys.path.insert(0, '.')
from scenario_gluelam_timber_full import DOCUMENTS, ACTOR_VIEWS, TIMELINE, DOC_IDS
from scenario_flow import DOCUMENT_FLOW, ACTOR_COLORS, PROCESS_STAGES

def generate_demo_js():
    """Generate demo.js with all documents, actors, and flow"""
    
    # Convert to JavaScript format
    documents_json = json.dumps(DOCUMENTS, indent=2, ensure_ascii=False)
    actor_views_json = json.dumps(ACTOR_VIEWS, indent=2, ensure_ascii=False)
    timeline_json = json.dumps(TIMELINE, indent=2, ensure_ascii=False)
    doc_ids_json = json.dumps(DOC_IDS, indent=2, ensure_ascii=False)
    document_flow_json = json.dumps(DOCUMENT_FLOW, indent=2, ensure_ascii=False)
    actor_colors_json = json.dumps(ACTOR_COLORS, indent=2, ensure_ascii=False)
    process_stages_json = json.dumps(PROCESS_STAGES, indent=2, ensure_ascii=False)
    
    js_content = f'''// demo.js - Finnish Gluelam Timber to Japan Trade Demo
// All 15 relevant KTDDE documents for the trade
// WITH INTERACTIVE DOCUMENT FLOW VISUALIZATION

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
    title: "Regulatory Certificate (CE)",
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

// Document flow (who creates what, dependencies, triggers)
const documentFlow = {document_flow_json};

// Actor colors for visualization
const actorColors = {actor_colors_json};

// Process stages
const processStages = {process_stages_json};

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
let flowAnimationStep = 0;
let flowAnimationInterval = null;

// Initialize demo
function initDemo() {{
  renderActorTabs();
  renderDocuments(currentActor);
  renderTimeline();
  renderDocumentFlow();
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
  const container = document.getElementById('timeline-events');
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

// Render document flow
function renderDocumentFlow() {{
  const container = document.getElementById('flow-diagram');
  if (!container) return;
  
  // Get documents sorted by order
  const sortedDocs = Object.keys(documentFlow).sort((a, b) => 
    documentFlow[a].order - documentFlow[b].order
  );
  
  // Group by stage
  let html = '<div class="flow-stages">';
  
  processStages.forEach((stage, stageIdx) => {{
    html += `
      <div class="flow-stage">
        <div class="stage-header">
          <div class="stage-number">${{stageIdx + 1}}</div>
          <div>
            <h3>${{stage.name}}</h3>
            <p>${{stage.description}}</p>
          </div>
        </div>
        <div class="stage-docs">
    `;
    
    stage.docs.forEach(docKey => {{
      const flow = documentFlow[docKey];
      const info = docInfo[docKey];
      const color = actorColors[flow.creator];
      
      html += `
        <div class="flow-doc" 
             data-doc="${{docKey}}"
             data-order="${{flow.order}}"
             style="border-color: ${{color}};"
             onclick="showDocumentFlow('${{docKey}}')">
          <div class="flow-doc-header" style="background: ${{color}};">
            <div class="flow-doc-number">${{flow.order}}</div>
            <div class="flow-doc-icon">${{info.icon}}</div>
          </div>
          <div class="flow-doc-body">
            <div class="flow-doc-title">${{info.title}}</div>
            <div class="flow-doc-creator">${{flow.creator_name}}</div>
            <div class="flow-doc-action">${{flow.action}}</div>
          </div>
          ${{flow.dependencies.length > 0 ? `
            <div class="flow-doc-deps">
              <small>Requires: ${{flow.dependencies.length}} doc(s)</small>
            </div>
          ` : ''}}
          ${{flow.triggers.length > 0 ? `
            <div class="flow-doc-triggers">
              <small>→ Triggers: ${{flow.triggers.length}} doc(s)</small>
            </div>
          ` : ''}}
        </div>
      `;
    }});
    
    html += `
        </div>
      </div>
    `;
    
    // Add stage connector
    if (stageIdx < processStages.length - 1) {{
      html += '<div class="stage-connector">→</div>';
    }}
  }});
  
  html += '</div>';
  
  container.innerHTML = html;
}}

// Show document in flow context
function showDocumentFlow(docKey) {{
  const flow = documentFlow[docKey];
  const info = docInfo[docKey];
  const doc = documents[docKey];
  
  if (!flow || !info || !doc) return;
  
  const modal = document.getElementById('doc-modal');
  const title = document.getElementById('doc-modal-title');
  const content = document.getElementById('doc-modal-content');
  
  let flowInfo = `
    <div class="flow-info">
      <h3>📋 Document Flow Information</h3>
      <div class="flow-info-grid">
        <div class="flow-info-item">
          <strong>Order:</strong> #${{flow.order}} of 15
        </div>
        <div class="flow-info-item">
          <strong>Creator:</strong> ${{flow.creator_name}}
        </div>
        <div class="flow-info-item">
          <strong>Action:</strong> ${{flow.action}}
        </div>
        <div class="flow-info-item">
          <strong>Description:</strong> ${{flow.description}}
        </div>
      </div>
  `;
  
  if (flow.dependencies.length > 0) {{
    flowInfo += `
      <div class="flow-dependencies">
        <h4>📥 Requires These Documents First:</h4>
        <ul>
          ${{flow.dependencies.map(dep => `
            <li onclick="showDocumentFlow('${{dep}}')" style="cursor: pointer; color: #3b82f6;">
              ${{docInfo[dep].icon}} ${{docInfo[dep].title}}
            </li>
          `).join('')}}
        </ul>
      </div>
    `;
  }}
  
  if (flow.triggers.length > 0) {{
    flowInfo += `
      <div class="flow-triggers">
        <h4>📤 Triggers Creation Of:</h4>
        <ul>
          ${{flow.triggers.map(trig => `
            <li onclick="showDocumentFlow('${{trig}}')" style="cursor: pointer; color: #10b981;">
              ${{docInfo[trig].icon}} ${{docInfo[trig].title}}
            </li>
          `).join('')}}
        </ul>
      </div>
    `;
  }}
  
  flowInfo += '</div><hr>';
  
  title.innerHTML = `${{info.icon}} ${{info.title}} <span style="font-size: 0.6em; opacity: 0.8;">(#${{flow.order}})</span>`;
  content.innerHTML = flowInfo + `<pre class="json-display">${{syntaxHighlight(JSON.stringify(doc, null, 2))}}</pre>`;
  
  modal.style.display = 'flex';
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
    """Generate demo.js with flow"""
    print("Generating demo/demo.js with interactive flow...")
    
    js_content = generate_demo_js()
    
    with open('demo/demo.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✅ Generated demo/demo.js ({len(js_content)} bytes)")
    print(f"   📦 {len(DOCUMENTS)} documents")
    print(f"   👥 {len(ACTOR_VIEWS)} actors")
    print(f"   ⏱️  {len(TIMELINE)} timeline events")
    print(f"   🔄 {len(DOCUMENT_FLOW)} flow definitions")
    print(f"   📊 {len(PROCESS_STAGES)} process stages")

if __name__ == "__main__":
    main()
