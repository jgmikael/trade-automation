#!/usr/bin/env python3
"""
Simple SHACL to SD-JWT converter (no dependencies)
Parses Turtle SHACL shapes and generates SD-JWT schemas + semantic registry
"""

import json
import re
from typing import Dict, List, Any

def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.lower()

def extract_value(line: str) -> str:
    """Extract value from RDF triple line"""
    if '"' in line:
        match = re.search(r'"([^"]+)"', line)
        return match.group(1) if match else ""
    elif '<' in line and '>' in line:
        match = re.search(r'<([^>]+)>', line)
        return match.group(1) if match else ""
    return line.split()[-1].strip(' ;.')

def parse_shacl_shape(turtle_file: str) -> Dict[str, Any]:
    """Parse SHACL shape from Turtle file (simple parser)"""
    with open(turtle_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find shape definition
    shape_match = re.search(r'(\w+:\w+Shape)\s+a\s+sh:NodeShape', content)
    if not shape_match:
        raise ValueError("No SHACL NodeShape found")
    
    shape_uri = shape_match.group(1)
    
    # Extract basic info
    info = {
        'uri': shape_uri,
        'label': None,
        'description': None,
        'target_class': None,
        'skos_concept': None,
        'properties': []
    }
    
    # Find shape block
    shape_block_match = re.search(
        rf'{re.escape(shape_uri)}.*?sh:targetClass.*?;(.*?)^\s*\.',
        content,
        re.MULTILINE | re.DOTALL
    )
    
    if not shape_block_match:
        return info
    
    shape_block = shape_block_match.group(1)
    
    # Extract labels
    label_match = re.search(r'sh:name\s+"([^"]+)"@en', shape_block)
    if label_match:
        info['label'] = label_match.group(1)
    
    # Extract description
    desc_match = re.search(r'sh:description\s+"""([^"]+)"""@en', shape_block, re.DOTALL)
    if desc_match:
        info['description'] = desc_match.group(1).strip()
    
    # Extract target class
    target_match = re.search(r'sh:targetClass\s+(\S+)', content)
    if target_match:
        info['target_class'] = target_match.group(1)
    
    # Extract SKOS concept
    skos_match = re.search(r'dcterms:subject\s+(\S+)', shape_block)
    if skos_match:
        info['skos_concept'] = skos_match.group(1)
    
    # Extract properties
    prop_blocks = re.findall(
        r'sh:property\s+\[(.*?)\]',
        shape_block,
        re.DOTALL
    )
    
    for prop_block in prop_blocks:
        prop_info = parse_property(prop_block)
        if prop_info:
            info['properties'].append(prop_info)
    
    return info

def parse_property(prop_block: str) -> Dict[str, Any]:
    """Parse property constraint block"""
    info = {
        'path': None,
        'path_uri': None,
        'name': None,
        'description': None,
        'datatype': None,
        'class': None,
        'min_count': 0,
        'max_count': None,
        'in': [],
        'skos_concept': None
    }
    
    # Extract path
    path_match = re.search(r'sh:path\s+(\S+)', prop_block)
    if path_match:
        info['path_uri'] = path_match.group(1)
        info['path'] = path_match.group(1).split(':')[-1] if ':' in path_match.group(1) else path_match.group(1)
    
    # Extract name
    name_match = re.search(r'sh:name\s+"([^"]+)"@en', prop_block)
    if name_match:
        info['name'] = name_match.group(1)
    
    # Extract description
    desc_match = re.search(r'sh:description\s+"([^"]+)"@en', prop_block)
    if desc_match:
        info['description'] = desc_match.group(1)
    
    # Extract datatype
    dtype_match = re.search(r'sh:datatype\s+(\S+)', prop_block)
    if dtype_match:
        info['datatype'] = dtype_match.group(1)
    
    # Extract class
    class_match = re.search(r'sh:class\s+(\S+)', prop_block)
    if class_match:
        info['class'] = class_match.group(1)
    
    # Extract cardinality
    min_match = re.search(r'sh:minCount\s+(\d+)', prop_block)
    if min_match:
        info['min_count'] = int(min_match.group(1))
    
    max_match = re.search(r'sh:maxCount\s+(\d+)', prop_block)
    if max_match:
        info['max_count'] = int(max_match.group(1))
    
    # Extract enumeration
    in_match = re.search(r'sh:in\s+\(\s*([^)]+)\s*\)', prop_block)
    if in_match:
        values = re.findall(r'"([^"]+)"', in_match.group(1))
        info['in'] = values
    
    # Extract SKOS concept
    skos_match = re.search(r'dcterms:subject\s+(\S+)', prop_block)
    if skos_match:
        info['skos_concept'] = skos_match.group(1)
    
    return info

def get_json_type(xsd_type: str) -> str:
    """Map XSD type to JSON type"""
    type_map = {
        'xsd:string': 'string',
        'xsd:boolean': 'boolean',
        'xsd:integer': 'integer',
        'xsd:int': 'integer',
        'xsd:decimal': 'number',
        'xsd:float': 'number',
        'xsd:double': 'number',
        'xsd:date': 'string',
        'xsd:dateTime': 'string',
    }
    return type_map.get(xsd_type, 'string')

def generate_sdjwt_schema(shape_info: Dict[str, Any]) -> Dict[str, Any]:
    """Generate SD-JWT schema"""
    schema = {
        "$schema": "https://json-schema.org/draft-07/schema#",
        "type": "object",
        "title": shape_info.get('label', 'Credential'),
        "description": shape_info.get('description', ''),
        "properties": {},
        "required": [],
        "_semantic_mapping": {
            "shacl_shape": shape_info['uri'],
            "target_class": shape_info.get('target_class'),
            "skos_concept": shape_info.get('skos_concept'),
            "properties": {}
        }
    }
    
    semantic_registry = {}
    
    for prop in shape_info['properties']:
        claim_name = camel_to_snake(prop['path'])
        
        # Determine JSON type
        if prop['datatype']:
            json_type = get_json_type(prop['datatype'])
        elif prop['class']:
            json_type = "object"
        else:
            json_type = "string"
        
        # Build property schema
        prop_schema = {
            "type": json_type,
            "description": prop.get('description') or prop.get('name', '')
        }
        
        if prop['in']:
            prop_schema['enum'] = prop['in']
        
        schema['properties'][claim_name] = prop_schema
        
        if prop['min_count'] >= 1:
            schema['required'].append(claim_name)
        
        # Semantic mapping
        schema['_semantic_mapping']['properties'][claim_name] = {
            "owl_property": prop['path_uri'],
            "original_name": prop['path'],
            "skos_concept": prop.get('skos_concept'),
            "datatype": prop.get('datatype'),
            "class": prop.get('class'),
            "mandatory": prop['min_count'] >= 1
        }
        
        # Registry entry
        semantic_registry[claim_name] = {
            "sdjwt_claim": claim_name,
            "shacl_shape": shape_info['uri'],
            "owl_property": prop['path_uri'],
            "skos_concept": prop.get('skos_concept'),
            "label": prop.get('name'),
            "description": prop.get('description')
        }
    
    return schema, semantic_registry

def generate_documentation(shape_info: Dict[str, Any], schema: Dict[str, Any]) -> str:
    """Generate markdown documentation"""
    doc = "# SD-JWT Schema: " + shape_info.get("label", "Attestation") + "\n\n"
    doc += "## Overview\n\n"
    doc += shape_info.get("description", "No description.") + "\n\n"
    doc += "⚠️ **Critical:** SD-JWT uses plain JSON without @context\n\n"
    doc += "## Claims\n\n"
    for prop in shape_info["properties"]:
        claim_name = camel_to_snake(prop["path"])
        required = "**Required**" if prop["min_count"] >= 1 else "Optional"
        doc += f"### `{claim_name}`\n\n"
        doc += f"- **Status:** {required}\n"
        doc += f"- **Original:** `{prop['path']}`\n"
        doc += f"- **SKOS:** `{prop.get('skos_concept', 'N/A')}`\n\n"
    return doc

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python simple_shacl_to_sdjwt.py <shacl-file.ttl>")
        sys.exit(1)
    
    shacl_file = sys.argv[1]
    base_name = shacl_file.split('/')[-1].replace('.ttl', '')
    
    print(f"🔄 Converting SHACL to SD-JWT...")
    print(f"   Input: {shacl_file}")
    
    # Parse SHACL
    try:
        shape_info = parse_shacl_shape(shacl_file)
        print(f"✅ Found shape: {shape_info.get('label', 'N/A')}")
        print(f"   Properties: {len(shape_info['properties'])}")
    except Exception as e:
        print(f"❌ Error parsing SHACL: {e}")
        sys.exit(1)
    
    # Generate SD-JWT schema
    schema, registry = generate_sdjwt_schema(shape_info)
    
    # Write schema
    schema_file = f"sdjwt/{base_name}-schema.json"
    with open(schema_file, 'w') as f:
        json.dump(schema, f, indent=2)
    print(f"✅ SD-JWT schema: {schema_file}")
    
    # Write registry
    registry_doc = {
        "$schema": "https://openclaw.ai/schemas/semantic-registry-v1.json",
        "description": "Semantic registry mapping SD-JWT claims to SHACL/OWL/SKOS",
        "version": "1.0.0",
        "source_shacl": shape_info['uri'],
        "mappings": registry
    }
    
    registry_file = f"sdjwt/{base_name}-registry.json"
    with open(registry_file, 'w') as f:
        json.dump(registry_doc, f, indent=2)
    print(f"✅ Semantic registry: {registry_file}")
    
    # Write documentation
    doc = generate_documentation(shape_info, schema)
    doc_file = f"sdjwt/{base_name}-docs.md"
    with open(doc_file, 'w') as f:
        f.write(doc)
    print(f"✅ Documentation: {doc_file}")
    
    print("\n" + "="*60)
    print("✅ CONVERSION COMPLETE")
    print("="*60)
    print(f"\nGenerated {len(registry)} snake_case claims")
    print(f"Semantic links maintained via registry")

if __name__ == "__main__":
    main()
