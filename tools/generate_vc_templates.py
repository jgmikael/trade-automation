#!/usr/bin/env python3
"""
W3C VC Template Generator

Generates fillable W3C Verifiable Credential templates from SHACL profiles.
Creates both empty templates and pre-filled examples.

Usage:
    python3 generate_vc_templates.py <shacl-file.jsonld> [output-dir]
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, date


def load_shacl(filepath: str) -> Dict:
    """Load SHACL JSON-LD file"""
    with open(filepath, 'r') as f:
        return json.load(f)


def extract_prefix_from_id(id_str: str) -> tuple[str, str]:
    """Extract prefix and local name from @id"""
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
    """Extract value from JSON-LD value object"""
    if isinstance(item, dict) and '@value' in item:
        val = item['@value']
        if item.get('@type') in ['xsd:integer', 'http://www.w3.org/2001/XMLSchema#integer']:
            return int(val)
        elif item.get('@type') in ['xsd:decimal', 'http://www.w3.org/2001/XMLSchema#decimal']:
            return float(val)
        return val
    return item if item is not None else default


class VCTemplateGenerator:
    """Generates W3C VC templates from SHACL profiles"""
    
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
    
    def generate_empty_template(self, node_shape: Dict, context_base: str) -> Dict[str, Any]:
        """Generate empty VC template with placeholders"""
        _, shape_name = extract_prefix_from_id(node_shape['@id'])
        target_class = node_shape.get('sh:targetClass', {}).get('@id', '')
        _, class_name = extract_prefix_from_id(target_class)
        label = get_label(node_shape)
        
        # Build empty credential structure
        template = {
            "@context": [
                "https://www.w3.org/2018/credentials/v1",
                f"{context_base}/{shape_name.lower()}-context.jsonld"
            ],
            "id": "<<CREDENTIAL_ID>>",
            "type": ["VerifiableCredential", f"{class_name}Credential"],
            "issuer": {
                "id": "<<ISSUER_DID>>",
                "name": "<<ISSUER_NAME>>"
            },
            "issuanceDate": "<<ISO_8601_DATETIME>>",
            "credentialSubject": {
                "id": "<<SUBJECT_ID>>",
                "type": class_name
            }
        }
        
        # Add properties with placeholders
        properties = node_shape.get('sh:property', [])
        if isinstance(properties, dict):
            properties = [properties]
        
        for prop_ref in properties:
            if isinstance(prop_ref, str):
                prop_id = prop_ref
            else:
                prop_id = prop_ref.get('@id')
            
            prop = self.get_property_details(prop_id)
            if not prop:
                continue
            
            _, prop_name = extract_prefix_from_id(prop_id)
            prop_label = get_label(prop) or prop_name
            min_count = get_value(prop.get('sh:minCount'), 0)
            
            # Datatype property
            if 'sh:datatype' in prop:
                datatype = prop['sh:datatype']
                placeholder = self._get_placeholder_for_datatype(datatype, prop_label)
                template["credentialSubject"][prop_name] = placeholder
            
            # Object property
            elif 'sh:class' in prop:
                class_ref = prop['sh:class'].get('@id', '')
                _, ref_class_name = extract_prefix_from_id(class_ref)
                
                max_count = get_value(prop.get('sh:maxCount'), 999)
                if max_count > 1 or 'sh:maxCount' not in prop:
                    # Array
                    template["credentialSubject"][prop_name] = [
                        {
                            "type": ref_class_name,
                            "<<PROPERTY>>": f"<<VALUE for {ref_class_name}>>"
                        }
                    ]
                else:
                    # Single object
                    template["credentialSubject"][prop_name] = {
                        "type": ref_class_name,
                        "<<PROPERTY>>": f"<<VALUE for {ref_class_name}>>"
                    }
        
        # Add proof placeholder
        template["proof"] = {
            "type": "<<SIGNATURE_TYPE>>",
            "created": "<<ISO_8601_DATETIME>>",
            "verificationMethod": "<<ISSUER_DID#KEY_ID>>",
            "proofPurpose": "assertionMethod",
            "proofValue": "<<SIGNATURE_VALUE>>"
        }
        
        return template
    
    def generate_example_template(self, node_shape: Dict, context_base: str) -> Dict[str, Any]:
        """Generate VC template with example values"""
        _, shape_name = extract_prefix_from_id(node_shape['@id'])
        target_class = node_shape.get('sh:targetClass', {}).get('@id', '')
        _, class_name = extract_prefix_from_id(target_class)
        label = get_label(node_shape)
        
        now = datetime.now()
        
        # Build credential with examples
        template = {
            "@context": [
                "https://www.w3.org/2018/credentials/v1",
                f"{context_base}/{shape_name.lower()}-context.jsonld"
            ],
            "id": f"https://example.com/credentials/{shape_name.lower()}/EXAMPLE-001",
            "type": ["VerifiableCredential", f"{class_name}Credential"],
            "issuer": {
                "id": "did:example:issuer123",
                "name": f"Example {label} Issuer"
            },
            "issuanceDate": now.isoformat() + "Z",
            "credentialSubject": {
                "id": f"https://example.com/{shape_name.lower()}/EXAMPLE-001",
                "type": class_name
            }
        }
        
        # Add properties with example values
        properties = node_shape.get('sh:property', [])
        if isinstance(properties, dict):
            properties = [properties]
        
        for prop_ref in properties:
            if isinstance(prop_ref, str):
                prop_id = prop_ref
            else:
                prop_id = prop_ref.get('@id')
            
            prop = self.get_property_details(prop_id)
            if not prop:
                continue
            
            _, prop_name = extract_prefix_from_id(prop_id)
            prop_label = get_label(prop) or prop_name
            
            # Datatype property
            if 'sh:datatype' in prop:
                datatype = prop['sh:datatype']
                example_value = self._get_example_for_datatype(datatype, prop_label)
                template["credentialSubject"][prop_name] = example_value
            
            # Object property
            elif 'sh:class' in prop:
                class_ref = prop['sh:class'].get('@id', '')
                _, ref_class_name = extract_prefix_from_id(class_ref)
                
                max_count = get_value(prop.get('sh:maxCount'), 999)
                if max_count > 1 or 'sh:maxCount' not in prop:
                    # Array with one example
                    template["credentialSubject"][prop_name] = [
                        self._get_example_object(ref_class_name, prop_label)
                    ]
                else:
                    # Single object
                    template["credentialSubject"][prop_name] = self._get_example_object(
                        ref_class_name, prop_label
                    )
        
        # Add example proof
        template["proof"] = {
            "type": "Ed25519Signature2020",
            "created": now.isoformat() + "Z",
            "verificationMethod": "did:example:issuer123#key-1",
            "proofPurpose": "assertionMethod",
            "proofValue": "z58DAdFfa9SkqZMVPxAQpE1..." + ("." * 40)
        }
        
        return template
    
    def _get_placeholder_for_datatype(self, xsd_type: str, label: str) -> str:
        """Get placeholder value for XSD datatype"""
        type_map = {
            'http://www.w3.org/2001/XMLSchema#string': f"<<{label}>>",
            'http://www.w3.org/2001/XMLSchema#integer': "<<INTEGER>>",
            'http://www.w3.org/2001/XMLSchema#decimal': "<<DECIMAL>>",
            'http://www.w3.org/2001/XMLSchema#double': "<<DECIMAL>>",
            'http://www.w3.org/2001/XMLSchema#float': "<<DECIMAL>>",
            'http://www.w3.org/2001/XMLSchema#boolean': "<<TRUE_OR_FALSE>>",
            'http://www.w3.org/2001/XMLSchema#date': "<<YYYY-MM-DD>>",
            'http://www.w3.org/2001/XMLSchema#dateTime': "<<ISO_8601_DATETIME>>",
            'http://www.w3.org/2001/XMLSchema#time': "<<HH:MM:SS>>",
            'http://www.w3.org/2001/XMLSchema#anyURI': "<<URI>>",
        }
        return type_map.get(xsd_type, f"<<{label}>>")
    
    def _get_example_for_datatype(self, xsd_type: str, label: str) -> Any:
        """Get example value for XSD datatype"""
        now = datetime.now()
        type_map = {
            'http://www.w3.org/2001/XMLSchema#string': f"Example {label}",
            'http://www.w3.org/2001/XMLSchema#integer': 1,
            'http://www.w3.org/2001/XMLSchema#decimal': 123.45,
            'http://www.w3.org/2001/XMLSchema#double': 123.45,
            'http://www.w3.org/2001/XMLSchema#float': 123.45,
            'http://www.w3.org/2001/XMLSchema#boolean': True,
            'http://www.w3.org/2001/XMLSchema#date': now.date().isoformat(),
            'http://www.w3.org/2001/XMLSchema#dateTime': now.isoformat() + "Z",
            'http://www.w3.org/2001/XMLSchema#time': now.time().isoformat(),
            'http://www.w3.org/2001/XMLSchema#anyURI': "https://example.com/resource",
        }
        return type_map.get(xsd_type, f"Example {label}")
    
    def _get_example_object(self, class_name: str, label: str) -> Dict[str, Any]:
        """Get example object for a class reference"""
        # Common examples for known types
        examples = {
            "Party": {
                "type": "Party",
                "partyName": "Example Company Ltd",
                "hasAddress": {
                    "type": "Address",
                    "street": "123 Example Street",
                    "city": "Example City",
                    "postalCode": "12345",
                    "country": {
                        "type": "Country",
                        "countryCode": "FI"
                    }
                }
            },
            "MonetaryAmount": {
                "type": "MonetaryAmount",
                "amountValue": 1000.00,
                "currencyCode": "EUR"
            },
            "Amount": {
                "type": "Amount",
                "value": 1000.00,
                "currencyCode": "EUR"
            },
            "Quantity": {
                "type": "Quantity",
                "quantityValue": "10",
                "unitCode": "EA"
            },
            "Location": {
                "type": "Location",
                "locationName": "Example Location",
                "hasAddress": {
                    "type": "Address",
                    "city": "Example City",
                    "country": {
                        "type": "Country",
                        "countryCode": "FI"
                    }
                }
            },
            "GoodsItem": {
                "type": "GoodsItem",
                "productDescription": "Example Product",
                "quantity": {
                    "type": "Quantity",
                    "quantityValue": "10",
                    "unitCode": "EA"
                }
            },
            "Country": {
                "type": "Country",
                "countryCode": "FI"
            },
        }
        
        return examples.get(class_name, {
            "type": class_name,
            "exampleProperty": f"Example value for {class_name}"
        })
    
    def generate_all_templates(self, output_dir: Path, context_base: str):
        """Generate all templates for all NodeShapes"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        empty_dir = output_dir / 'empty'
        examples_dir = output_dir / 'examples'
        empty_dir.mkdir(exist_ok=True)
        examples_dir.mkdir(exist_ok=True)
        
        shapes = self.find_node_shapes()
        print(f"Found {len(shapes)} NodeShapes")
        
        for shape in shapes:
            _, shape_name = extract_prefix_from_id(shape['@id'])
            label = get_label(shape)
            print(f"\nProcessing: {label} ({shape_name})")
            
            # Generate empty template
            empty_template = self.generate_empty_template(shape, context_base)
            empty_file = empty_dir / f"{shape_name.lower()}-template.jsonld"
            with open(empty_file, 'w') as f:
                json.dump(empty_template, f, indent=2)
            print(f"  ✓ Empty template: {empty_file}")
            
            # Generate example template
            example_template = self.generate_example_template(shape, context_base)
            example_file = examples_dir / f"{shape_name.lower()}-example.jsonld"
            with open(example_file, 'w') as f:
                json.dump(example_template, f, indent=2)
            print(f"  ✓ Example: {example_file}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    shacl_file = sys.argv[1]
    output_dir = Path(sys.argv[2] if len(sys.argv) > 2 else 'templates')
    context_base = "https://github.com/jgmikael/trade-automation/contexts"
    
    print(f"Loading SHACL file: {shacl_file}")
    shacl_data = load_shacl(shacl_file)
    
    generator = VCTemplateGenerator(shacl_data)
    print(f"Profile: {get_label(generator.profile)}")
    print(f"Version: {generator.version}")
    
    generator.generate_all_templates(output_dir, context_base)
    print("\n✅ Template generation complete!")


if __name__ == '__main__':
    main()
