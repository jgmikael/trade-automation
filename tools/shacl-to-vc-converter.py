#!/usr/bin/env python3
"""
SHACL to W3C Verifiable Credential Converter

Converts SHACL application profiles into W3C VC JSON-LD contexts and JSON Schemas.

Usage:
    python3 shacl-to-vc-converter.py <shacl-file.jsonld> [output-dir]
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from urllib.parse import urlparse

def load_shacl(filepath: str) -> Dict:
    """Load SHACL JSON-LD file"""
    with open(filepath, 'r') as f:
        return json.load(f)

def extract_prefix_from_id(id_str: str) -> tuple[str, str]:
    """Extract prefix and local name from @id like 'dsibol:BillOfLading'"""
    if ':' in id_str and not id_str.startswith('http'):
        parts = id_str.split(':', 1)
        return parts[0], parts[1]
    elif '/' in id_str:
        return '', id_str.split('/')[-1]
    return '', id_str

def get_label(item: Dict, lang: str = 'en') -> str:
    """Extract label from rdfs:label"""
    label = item.get('rdfs:label', {})
    if isinstance(label, dict):
        return label.get('@value', '')
    return str(label)

def get_value(item: Any, default: Any = None) -> Any:
    """Extract value from JSON-LD value object or return as-is"""
    if isinstance(item, dict) and '@value' in item:
        val = item['@value']
        # Convert string numbers to actual numbers
        if item.get('@type') in ['xsd:integer', 'http://www.w3.org/2001/XMLSchema#integer']:
            return int(val)
        elif item.get('@type') in ['xsd:decimal', 'http://www.w3.org/2001/XMLSchema#decimal']:
            return float(val)
        return val
    return item if item is not None else default

def get_datatype_json_type(xsd_type: str) -> tuple[str, Optional[str]]:
    """Map XSD datatype to JSON Schema type and format"""
    type_map = {
        'http://www.w3.org/2001/XMLSchema#string': ('string', None),
        'http://www.w3.org/2001/XMLSchema#integer': ('integer', None),
        'http://www.w3.org/2001/XMLSchema#decimal': ('number', None),
        'http://www.w3.org/2001/XMLSchema#double': ('number', None),
        'http://www.w3.org/2001/XMLSchema#float': ('number', None),
        'http://www.w3.org/2001/XMLSchema#boolean': ('boolean', None),
        'http://www.w3.org/2001/XMLSchema#date': ('string', 'date'),
        'http://www.w3.org/2001/XMLSchema#dateTime': ('string', 'date-time'),
        'http://www.w3.org/2001/XMLSchema#time': ('string', 'time'),
        'http://www.w3.org/2001/XMLSchema#anyURI': ('string', 'uri'),
    }
    return type_map.get(xsd_type, ('string', None))

class SHACLToVCConverter:
    def __init__(self, shacl_data: Dict):
        self.data = shacl_data
        self.graph = {item['@id']: item for item in shacl_data['@graph']}
        self.context = shacl_data.get('@context', {})
        
        # Find the ontology/profile metadata
        self.profile = self._find_profile()
        self.namespace = self.profile.get('dcap:preferredXMLNamespace', '')
        self.prefix = self.profile.get('dcap:preferredXMLNamespacePrefix', '')
        self.version = self.profile.get('owl:versionInfo', '0.0.1')
        
    def _find_profile(self) -> Dict:
        """Find the main ontology/application profile"""
        for item in self.graph.values():
            if 'suomi-meta:ApplicationProfile' in item.get('@type', []):
                return item
        return {}
    
    def find_node_shapes(self) -> List[Dict]:
        """Find all NodeShapes (document types)"""
        shapes = []
        for item in self.graph.values():
            if 'sh:NodeShape' in item.get('@type', []):
                if 'sh:targetClass' in item:  # Main document shapes
                    shapes.append(item)
        return shapes
    
    def get_property_details(self, prop_id: str) -> Optional[Dict]:
        """Get PropertyShape details"""
        return self.graph.get(prop_id)
    
    def generate_jsonld_context(self, node_shape: Dict) -> Dict:
        """Generate JSON-LD context for a NodeShape"""
        _, shape_name = extract_prefix_from_id(node_shape['@id'])
        target_class = node_shape.get('sh:targetClass', {}).get('@id', '')
        _, class_name = extract_prefix_from_id(target_class)
        
        context = {
            "@context": {
                "@version": 1.1,
                "@protected": True,
                "ktdde": "https://iri.suomi.fi/model/ktddecv/",
                "xsd": "http://www.w3.org/2001/XMLSchema#",
                class_name: {
                    "@id": target_class,
                    "@context": {}
                }
            }
        }
        
        # Process properties (handle both array and single object)
        properties = node_shape.get('sh:property', [])
        if isinstance(properties, dict):
            properties = [properties]
        
        for prop_ref in properties:
            # Handle both {"@id": "..."} and direct string references
            if isinstance(prop_ref, str):
                prop_id = prop_ref
            else:
                prop_id = prop_ref.get('@id')
            prop = self.get_property_details(prop_id)
            if not prop:
                continue
            
            _, prop_name = extract_prefix_from_id(prop_id)
            path = prop.get('sh:path', {}).get('@id', '')
            
            prop_context = {"@id": path}
            
            # Datatype property
            if 'sh:datatype' in prop:
                datatype = prop['sh:datatype']
                if datatype != 'http://www.w3.org/2001/XMLSchema#string':
                    prop_context["@type"] = datatype
            
            # Object property (reference to another class)
            elif 'sh:class' in prop:
                prop_context["@type"] = "@id"
                # If it's a collection/array
                max_count = get_value(prop.get('sh:maxCount'), 999)
                if max_count > 1 or 'sh:maxCount' not in prop:
                    prop_context["@container"] = "@set"
            
            context["@context"][class_name]["@context"][prop_name] = prop_context
        
        return context
    
    def generate_json_schema(self, node_shape: Dict) -> Dict:
        """Generate JSON Schema for credential subject"""
        _, shape_name = extract_prefix_from_id(node_shape['@id'])
        target_class = node_shape.get('sh:targetClass', {}).get('@id', '')
        _, class_name = extract_prefix_from_id(target_class)
        label = get_label(node_shape)
        
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": f"https://github.com/jgmikael/trade-automation/credentials/{shape_name.lower()}-schema.json",
            "title": f"{label} Verifiable Credential",
            "description": f"W3C Verifiable Credential schema for KTDDE {label}",
            "type": "object",
            "required": ["@context", "type", "issuer", "issuanceDate", "credentialSubject"],
            "properties": {
                "@context": {
                    "type": "array",
                    "items": [
                        {"const": "https://www.w3.org/2018/credentials/v1"},
                        {"type": "string", "format": "uri"}
                    ],
                    "minItems": 2
                },
                "id": {"type": "string", "format": "uri"},
                "type": {
                    "type": "array",
                    "contains": {"const": "VerifiableCredential"},
                    "items": {"type": "string"},
                    "minItems": 2
                },
                "issuer": {
                    "oneOf": [
                        {"type": "string", "format": "uri"},
                        {
                            "type": "object",
                            "required": ["id"],
                            "properties": {
                                "id": {"type": "string", "format": "uri"},
                                "name": {"type": "string"}
                            }
                        }
                    ]
                },
                "issuanceDate": {"type": "string", "format": "date-time"},
                "expirationDate": {"type": "string", "format": "date-time"},
                "credentialSubject": self._generate_subject_schema(node_shape),
                "proof": {
                    "type": "object",
                    "description": "Digital signature proof"
                }
            }
        }
        
        return schema
    
    def _generate_subject_schema(self, node_shape: Dict) -> Dict:
        """Generate credentialSubject schema"""
        _, class_name = extract_prefix_from_id(node_shape.get('sh:targetClass', {}).get('@id', ''))
        
        subject_schema = {
            "type": "object",
            "required": ["type"],
            "properties": {
                "id": {
                    "type": "string",
                    "format": "uri",
                    "description": f"DID or URI of the {class_name}"
                },
                "type": {"const": class_name}
            }
        }
        
        # Process properties (handle both array and single object)
        required_props = ["type"]
        properties = node_shape.get('sh:property', [])
        if isinstance(properties, dict):
            properties = [properties]
        
        for prop_ref in properties:
            # Handle both {"@id": "..."} and direct string references
            if isinstance(prop_ref, str):
                prop_id = prop_ref
            else:
                prop_id = prop_ref.get('@id')
            prop = self.get_property_details(prop_id)
            if not prop:
                continue
            
            _, prop_name = extract_prefix_from_id(prop_id)
            label = get_label(prop)
            
            prop_schema = {"description": label if label else prop_name}
            
            # Datatype property
            if 'sh:datatype' in prop:
                json_type, json_format = get_datatype_json_type(prop['sh:datatype'])
                prop_schema["type"] = json_type
                if json_format:
                    prop_schema["format"] = json_format
            
            # Object property
            elif 'sh:class' in prop:
                class_ref = prop['sh:class'].get('@id', '')
                _, ref_class_name = extract_prefix_from_id(class_ref)
                
                # Check if it's a collection
                max_count = get_value(prop.get('sh:maxCount'), 999)
                if max_count > 1 or 'sh:maxCount' not in prop:
                    prop_schema["type"] = "array"
                    prop_schema["items"] = {
                        "type": "object",
                        "properties": {
                            "type": {"const": ref_class_name}
                        }
                    }
                else:
                    prop_schema["type"] = "object"
                    prop_schema["properties"] = {
                        "type": {"const": ref_class_name}
                    }
            
            # Check if required
            min_count = get_value(prop.get('sh:minCount'), 0)
            if min_count >= 1:
                required_props.append(prop_name)
            
            subject_schema["properties"][prop_name] = prop_schema
        
        if len(required_props) > 1:
            subject_schema["required"] = required_props
        
        return subject_schema
    
    def convert_all(self, output_dir: Path):
        """Convert all NodeShapes and output files"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        contexts_dir = output_dir / 'contexts'
        schemas_dir = output_dir / 'credentials'
        contexts_dir.mkdir(exist_ok=True)
        schemas_dir.mkdir(exist_ok=True)
        
        shapes = self.find_node_shapes()
        print(f"Found {len(shapes)} NodeShapes")
        
        for shape in shapes:
            _, shape_name = extract_prefix_from_id(shape['@id'])
            label = get_label(shape)
            print(f"\nProcessing: {label} ({shape_name})")
            
            # Generate JSON-LD context
            context = self.generate_jsonld_context(shape)
            context_file = contexts_dir / f"{shape_name.lower()}-context.jsonld"
            with open(context_file, 'w') as f:
                json.dump(context, f, indent=2)
            print(f"  ✓ Context: {context_file}")
            
            # Generate JSON Schema
            schema = self.generate_json_schema(shape)
            schema_file = schemas_dir / f"{shape_name.lower()}-schema.json"
            with open(schema_file, 'w') as f:
                json.dump(schema, f, indent=2)
            print(f"  ✓ Schema: {schema_file}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    shacl_file = sys.argv[1]
    output_dir = Path(sys.argv[2] if len(sys.argv) > 2 else '.')
    
    print(f"Loading SHACL file: {shacl_file}")
    shacl_data = load_shacl(shacl_file)
    
    converter = SHACLToVCConverter(shacl_data)
    print(f"Profile: {get_label(converter.profile)}")
    print(f"Version: {converter.version}")
    print(f"Namespace: {converter.namespace}")
    
    converter.convert_all(output_dir)
    print("\n✅ Conversion complete!")

if __name__ == '__main__':
    main()
