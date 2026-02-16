// Interactive SAP to KTDDE Transformation
// Handles the animated transformation demonstration

let currentDocument = null;
let transformationStep = 0;
let transformInterval = null;

// Select document to transform
function selectDocument(docKey) {
    if (!docKey) {
        document.getElementById('transform-area').classList.remove('active');
        document.querySelectorAll('.doc-button').forEach(btn => btn.classList.remove('active'));
        currentDocument = null;
        resetTransformation();
        return;
    }
    
    currentDocument = docKey;
    
    // Update button states
    document.querySelectorAll('.doc-button').forEach(btn => btn.classList.remove('active'));
    event.target.closest('.doc-button').classList.add('active');
    
    // Show transformation area
    document.getElementById('transform-area').classList.add('active');
    
    // Reset and load SAP data
    resetTransformation();
    loadSAPData(docKey);
    loadMappings(docKey);
    
    // Update step indicator
    document.getElementById('step-1').classList.add('active');
    
    // Scroll to transformation area
    document.getElementById('transform-area').scrollIntoView({ behavior: 'smooth' });
}

// Load SAP source data
function loadSAPData(docKey) {
    const sapData = sapSourceData[docKey];
    if (!sapData) {
        document.getElementById('sap-data').innerHTML = '<p>No SAP data available</p>';
        return;
    }
    
    let html = '';
    
    for (const [tableName, data] of Object.entries(sapData)) {
        html += `<div class="sap-table">`;
        html += `<div class="table-name">${tableName}</div>`;
        
        if (Array.isArray(data)) {
            data.forEach((record, idx) => {
                html += `<div style="margin-left: 15px; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #e5e7eb;">`;
                html += `<div style="color: #6b7280; font-size: 0.85em; margin-bottom: 8px;">Record ${idx + 1}</div>`;
                html += formatSAPRecord(record, tableName);
                html += `</div>`;
            });
        } else {
            html += formatSAPRecord(data, tableName);
        }
        
        html += `</div>`;
    }
    
    document.getElementById('sap-data').innerHTML = html;
}

// Format SAP record
function formatSAPRecord(record, tableName) {
    let html = '';
    for (const [field, value] of Object.entries(record)) {
        html += `<div class="field-row" data-table="${tableName}" data-field="${field}">`;
        html += `<span class="field-name">${field}:</span>`;
        html += `<span class="field-value">${value}</span>`;
        html += `</div>`;
    }
    return html;
}

// Load transformation mappings
function loadMappings(docKey) {
    const mappings = transformationMappings[docKey];
    if (!mappings) {
        document.getElementById('mapping-list').innerHTML = '';
        return;
    }
    
    let html = '<h3 style="margin-bottom: 20px; color: #1f2937;">Field Mappings</h3>';
    
    mappings.forEach((mapping, idx) => {
        html += `
            <div class="mapping-item" data-mapping-idx="${idx}">
                <div class="mapping-sap">${mapping.sap}</div>
                <div class="mapping-arrow">→</div>
                <div class="mapping-ktdde">${mapping.ktdde}</div>
                <div class="mapping-desc">${mapping.desc}</div>
            </div>
        `;
    });
    
    document.getElementById('mapping-list').innerHTML = html;
}

// Start transformation animation
function startTransformation() {
    if (!currentDocument) return;
    if (transformInterval) return; // Already running
    
    const btn = document.getElementById('transform-btn');
    btn.classList.add('animating');
    btn.disabled = true;
    
    // Update steps
    document.getElementById('step-1').classList.add('completed');
    document.getElementById('step-2').classList.add('active');
    
    const mappings = transformationMappings[currentDocument];
    const doc = documents[currentDocument];
    
    if (!mappings || !doc) {
        alert('Transformation data not available');
        return;
    }
    
    transformationStep = 0;
    
    // Animate through each mapping
    transformInterval = setInterval(() => {
        if (transformationStep < mappings.length) {
            const mapping = mappings[transformationStep];
            
            // Highlight SAP fields
            const sapField = mapping.sap.split(/[.+\[\]]/)[0];
            document.querySelectorAll(`.field-row[data-field*="${sapField}"]`).forEach(row => {
                row.classList.add('highlight');
                setTimeout(() => row.classList.remove('highlight'), 2000);
            });
            
            // Activate mapping item
            const mappingItem = document.querySelector(`[data-mapping-idx="${transformationStep}"]`);
            if (mappingItem) {
                mappingItem.classList.add('active');
            }
            
            // Build output incrementally
            buildIncrementalOutput(transformationStep);
            
            transformationStep++;
        } else {
            // Complete
            clearInterval(transformInterval);
            transformInterval = null;
            btn.classList.remove('animating');
            btn.disabled = false;
            btn.innerHTML = '✅';
            
            // Update steps
            document.getElementById('step-2').classList.add('completed');
            document.getElementById('step-3').classList.add('active');
            document.getElementById('step-3').classList.add('completed');
            
            // Show full output
            showFullOutput();
            
            // Show completed message
            document.getElementById('completed-msg').style.display = 'block';
        }
    }, 1000); // 1 second per field
}

// Build incremental output
function buildIncrementalOutput(step) {
    const doc = documents[currentDocument];
    const mappings = transformationMappings[currentDocument];
    
    let output = {
        "@context": ["https://www.w3.org/ns/credentials/v2"],
        "@type": doc["@type"],
        "status": `Transforming... (${step + 1}/${mappings.length} fields)`
    };
    
    // Add fields up to current step
    for (let i = 0; i <= step; i++) {
        const mapping = mappings[i];
        const ktddeField = mapping.ktdde.split(/[.\[\]{}]/)[0];
        
        // Get value from document (simplified)
        if (doc[ktddeField]) {
            output[ktddeField] = doc[ktddeField];
        }
    }
    
    document.getElementById('ktdde-data').innerHTML = 
        '<pre class="json-display">' + syntaxHighlightJSON(JSON.stringify(output, null, 2)) + '</pre>';
}

// Show full output
function showFullOutput() {
    const doc = documents[currentDocument];
    
    const vc = {
        "@context": [
            "https://www.w3.org/ns/credentials/v2",
            "https://iri.suomi.fi/context/ktdde/v1"
        ],
        "type": ["VerifiableCredential", doc["@type"]],
        "issuer": {
            "id": "did:web:nordic-timber.fi",
            "name": "Nordic Timber Oy"
        },
        "issuanceDate": new Date().toISOString(),
        "credentialSubject": doc
    };
    
    document.getElementById('ktdde-data').innerHTML = 
        '<pre class="json-display">' + syntaxHighlightJSON(JSON.stringify(vc, null, 2)) + '</pre>';
}

// Syntax highlight JSON
function syntaxHighlightJSON(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        let cls = 'json-number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'json-key';
            } else {
                cls = 'json-string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'json-boolean';
        } else if (/null/.test(match)) {
            cls = 'json-null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

// Reset transformation
function resetTransformation() {
    if (transformInterval) {
        clearInterval(transformInterval);
        transformInterval = null;
    }
    
    transformationStep = 0;
    
    // Reset button
    const btn = document.getElementById('transform-btn');
    btn.classList.remove('animating');
    btn.disabled = false;
    btn.innerHTML = '⚡';
    
    // Reset steps
    document.querySelectorAll('.step').forEach(step => {
        step.classList.remove('active', 'completed');
    });
    document.getElementById('step-1').classList.add('active');
    
    // Reset mappings
    document.querySelectorAll('.mapping-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Clear output
    document.getElementById('ktdde-data').innerHTML = `
        <div style="text-align: center; padding: 50px; color: #9ca3af;">
            Click the ⚡ button to start transformation
        </div>
    `;
    
    // Hide completed message
    document.getElementById('completed-msg').style.display = 'none';
}

// Download VC
function downloadVC() {
    if (!currentDocument) return;
    
    const doc = documents[currentDocument];
    const vc = {
        "@context": [
            "https://www.w3.org/ns/credentials/v2",
            "https://iri.suomi.fi/context/ktdde/v1"
        ],
        "type": ["VerifiableCredential", doc["@type"]],
        "issuer": {
            "id": "did:web:nordic-timber.fi",
            "name": "Nordic Timber Oy"
        },
        "issuanceDate": new Date().toISOString(),
        "credentialSubject": doc
    };
    
    const blob = new Blob([JSON.stringify(vc, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${currentDocument}_vc.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
