#!/usr/bin/env python3
"""
SHACL to SD-JWT Schema Generator

Problem: SD-JWT uses plain JSON without @context, losing semantic links.
Solution: Generate SD-JWT schema + semantic mapping from SHACL shapes.

This tool:
1. Reads SHACL shapes from tietomallit.suomi.fi
2. Generates SD-JWT schema (snake_case claims)
3. Creates semantic mapping (SD-JWT claim → SHACL → OWL → SKOS)
4. Maintains traceability even without @context

Input: SHACL shape (RDF/Turtle)
Output: 
  - SD-JWT schema (JSON)
  - Semantic mapping registry
  - Documentation
"""

import json
import re
from typing import Dict, List, Any, Optional
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, SH, DCTERMS, SKOS

# Namespaces
KTDDECV = Namespace("https://iri.suomi.fi/model/ktddecv/")
KTDDE = Namespace("https://iri.suomi.fi/terminology/ktdde/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")


def camel_to_snake(name: str) -> str:
    """Convert camelCase or PascalCase to snake_case for SD-JWT claims"""
    # Insert underscore before uppercase letters
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.lower()


def extract_local_name(uri: URIRef) -> str:
    """Extract local name from URI"""
    uri_str = str(uri)
    if '#' in uri_str:
        return uri_str.split('#')[-1]
    elif '/' in uri_str:
        return uri_str.split('/')[-1]
    return uri_str


def get_datatype_for_sdjwt(xsd_type: Optional[URIRef]) -> str:
    """Map XSD datatype to SD-JWT JSON type"""
    if not xsd_type:
        return "string"
    
    type_map = {
        str(XSD.string): "string",
        str(XSD.boolean): "boolean",
        str(XSD.integer): "integer",
        str(XSD.int): "integer",
        str(XSD.decimal): "number",
        str(XSD.float): "number",
        str(XSD.double): "number",
        str(XSD.date): "string",  # ISO 8601 date
        str(XSD.dateTime): "string",  # ISO 8601 datetime
        str(XSD.time): "string",
        str(XSD.anyURI): "string",
    }
    
    return type_map.get(str(xsd_type), "string")


class SHACLToSDJWT:
    """Convert SHACL shapes to SD-JWT schema with semantic mapping"""
    
    def __init__(self):
        self.graph = Graph()
        self.semantic_registry = {}
        
    def load_shacl(self, file_path: str):
        """Load SHACL shape from file"""
        self.graph.parse(file_path, format='turtle')
        
    def extract_shape_info(self, shape_uri: URIRef) -> Dict[str, Any]:
        """Extract information from SHACL shape"""
        info = {
            'uri': str(shape_uri),
            'label': None,
            'description': None,
            'target_class': None,
            'skos_concept': None,
            'properties': []
        }
        
        # Get basic info
        for label in self.graph.objects(shape_uri, SH.name):
            info['label'] = str(label)
            break
        
        for desc in self.graph.objects(shape_uri, SH.description):
            info['description'] = str(desc)
            break
            
        for target in self.graph.objects(shape_uri, SH.targetClass):
            info['target_class'] = str(target)
            break
            
        # Get SKOS concept link
        for concept in self.graph.objects(shape_uri, DCTERMS.subject):
            info['skos_concept'] = str(concept)
            break
        
        # Get properties
        for prop_shape in self.graph.objects(shape_uri, SH.property):
            prop_info = self._extract_property_info(prop_shape)
            if prop_info:
                info['properties'].append(prop_info)
        
        return info
    
    def _extract_property_info(self, prop_shape: URIRef) -> Dict[str, Any]:
        """Extract property constraint information"""
        info = {
            'path': None,
            'path_uri': None,
            'name': None,
            'description': None,
            'datatype': None,
            'class': None,
            'min_count': 0,
            'max_count': None,
            'pattern': None,
            'in': [],
            'skos_concept': None
        }
        
        # Get path (the OWL property)
        for path in self.graph.objects(prop_shape, SH.path):
            info['path_uri'] = str(path)
            info['path'] = extract_local_name(path)
            break
        
        # Get name
        for name in self.graph.objects(prop_shape, SH.name):
            info['name'] = str(name)
            break
        
        # Get description
        for desc in self.graph.objects(prop_shape, SH.description):
            info['description'] = str(desc)
            break
        
        # Get datatype
        for dtype in self.graph.objects(prop_shape, SH.datatype):
            info['datatype'] = str(dtype)
            break
        
        # Get class (for object properties)
        for cls in self.graph.objects(prop_shape, SH['class']):
            info['class'] = str(cls)
            break
        
        # Get cardinality
        for min_count in self.graph.objects(prop_shape, SH.minCount):
            info['min_count'] = int(min_count)
            break
        
        for max_count in self.graph.objects(prop_shape, SH.maxCount):
            info['max_count'] = int(max_count)
            break
        
        # Get pattern
        for pattern in self.graph.objects(prop_shape, SH.pattern):
            info['pattern'] = str(pattern)
            break
        
        # Get enumeration
        for in_list in self.graph.objects(prop_shape, SH['in']):
            # Parse RDF list
            for item in self.graph.items(in_list):
                info['in'].append(str(item))
        
        # Get SKOS concept link
        for concept in self.graph.objects(prop_shape, DCTERMS.subject):
            info['skos_concept'] = str(concept)
            break
        
        return info
    
    def generate_sdjwt_schema(self, shape_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate SD-JWT compatible schema"""
        
        # SD-JWT schema structure
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
        
        for prop in shape_info['properties']:
            # Generate snake_case claim name
            claim_name = camel_to_snake(prop['path'])
            
            # Determine JSON type
            json_type = "string"
            if prop['datatype']:
                json_type = get_datatype_for_sdjwt(URIRef(prop['datatype']))
            elif prop['class']:
                json_type = "object"
            
            # Build property schema
            prop_schema = {
                "type": json_type,
                "description": prop.get('description', prop.get('name', ''))
            }
            
            # Add constraints
            if prop['pattern']:
                prop_schema['pattern'] = prop['pattern']
            
            if prop['in']:
                prop_schema['enum'] = prop['in']
            
            # Add to schema
            schema['properties'][claim_name] = prop_schema
            
            # Add to required if minCount >= 1
            if prop['min_count'] >= 1:
                schema['required'].append(claim_name)
            
            # Add semantic mapping
            schema['_semantic_mapping']['properties'][claim_name] = {
                "owl_property": prop['path_uri'],
                "original_name": prop['path'],
                "shacl_path": prop['path_uri'],
                "skos_concept": prop.get('skos_concept'),
                "datatype": prop.get('datatype'),
                "class": prop.get('class'),
                "mandatory": prop['min_count'] >= 1
            }
            
            # Store in global registry
            self.semantic_registry[claim_name] = {
                "sdjwt_claim": claim_name,
                "shacl_shape": shape_info['uri'],
                "shacl_property": prop['path_uri'],
                "owl_property": prop['path_uri'],
                "skos_concept": prop.get('skos_concept'),
                "label": prop.get('name'),
                "description": prop.get('description')
            }
        
        return schema
    
    def generate_semantic_registry(self) -> Dict[str, Any]:
        """Generate complete semantic mapping registry"""
        return {
            "$schema": "https://openclaw.ai/schemas/semantic-registry-v1.json",
            "description": """Semantic registry mapping SD-JWT claims to SHACL/OWL/SKOS.
                            
                            Problem: SD-JWT has no @context, losing semantic links.
                            Solution: This registry maintains traceability from 
                                     SD-JWT claims back through all semantic layers.
                            
                            Usage: When processing SD-JWT, use this registry to
                                  resolve semantic meaning of claims.""",
            "version": "1.0.0",
            "layers": {
                "layer_5": "SD-JWT (IETF RFC, plain JSON)",
                "layer_4": "JSON-LD (@context - MISSING in SD-JWT!)",
                "layer_3": "SHACL (validation constraints)",
                "layer_2": "OWL (data model)",
                "layer_1": "SKOS (conceptual vocabulary)"
            },
            "mappings": self.semantic_registry
        }
    
    def generate_documentation(self, shape_info: Dict[str, Any], 
                             schema: Dict[str, Any]) -> str:
        """Generate human-readable documentation"""
        
        doc = f"""# SD-JWT Schema: {shape_info.get('label', 'Credential')}

## Overview

{shape_info.get('description', 'No description available.')}

**Critical Note:** SD-JWT uses plain JSON without @context, which means:
- ❌ No automatic semantic linking to RDF
- ❌ No connection to SKOS/OWL layers
- ✅ BUT: This schema includes semantic mapping to maintain traceability

## Semantic Lineage

| Layer | Resource | URI |
|-------|----------|-----|
| **Layer 5** | SD-JWT Schema | (this document) |
| **Layer 4** | JSON-LD @context | ⚠️ NOT SUPPORTED by SD-JWT |
| **Layer 3** | SHACL Shape | `{shape_info['uri']}` |
| **Layer 2** | OWL Class | `{shape_info.get('target_class', 'N/A')}` |
| **Layer 1** | SKOS Concept | `{shape_info.get('skos_concept', 'N/A')}` |

## Claims (Attributes)

"""
        
        for prop in shape_info['properties']:
            claim_name = camel_to_snake(prop['path'])
            required = "**Required**" if prop['min_count'] >= 1 else "Optional"
            
            doc += f"""
### `{claim_name}`

- **Status:** {required}
- **Original Property:** `{prop['path']}`
- **Type:** {prop.get('datatype') or prop.get('class') or 'string'}
- **Description:** {prop.get('description') or prop.get('name') or 'No description'}

**Semantic Traceability:**
- **SHACL Path:** `{prop['path_uri']}`
- **OWL Property:** `{prop['path_uri']}`
- **SKOS Concept:** `{prop.get('skos_concept') or 'Not linked'}`

"""
            
            if prop['pattern']:
                doc += f"- **Pattern:** `{prop['pattern']}`\n"
            
            if prop['in']:
                doc += f"- **Allowed Values:** {', '.join(f'`{v}`' for v in prop['in'])}\n"
            
            doc += "\n"
        
        doc += """
## SD-JWT Example

```json
{
  "iss": "https://issuer.example.com",
  "sub": "did:example:123",
  "iat": 1516239022,
  "exp": 1735689600,
"""
        
        # Add example claims
        for i, prop in enumerate(shape_info['properties'][:3]):  # First 3 as example
            claim_name = camel_to_snake(prop['path'])
            example_value = '"example_value"'
            
            if prop.get('datatype'):
                dtype = prop['datatype']
                if 'integer' in dtype.lower():
                    example_value = '42'
                elif 'boolean' in dtype.lower():
                    example_value = 'true'
                elif 'date' in dtype.lower():
                    example_value = '"2024-02-15"'
            
            comma = "," if i < min(2, len(shape_info['properties']) - 1) else ""
            doc += f'  "{claim_name}": {example_value}{comma}\n'
        
        doc += """}
```

## Semantic Resolution

To resolve semantic meaning of SD-JWT claims:

1. **Look up claim in semantic registry** (see `semantic-registry.json`)
2. **Get SHACL shape URI** from registry
3. **Resolve to OWL property** via SHACL path
4. **Find OWL property's SKOS concept** via `dcterms:subject`
5. **Access concept definition** from sanastot.suomi.fi

**Example for `{camel_to_snake(shape_info['properties'][0]['path'])}` claim:**

```
SD-JWT claim: "{camel_to_snake(shape_info['properties'][0]['path'])}"
       ↓ (registry lookup)
SHACL property: {shape_info['properties'][0]['path_uri']}
       ↓ (sh:path)
OWL property: {shape_info['properties'][0]['path_uri']}
       ↓ (dcterms:subject)
SKOS concept: {shape_info['properties'][0].get('skos_concept', 'N/A')}
       ↓ (sanastot.suomi.fi)
Definition: [Access SKOS vocabulary for full definition]
```

## Comparison: JSON-LD vs SD-JWT

| Aspect | JSON-LD (W3C VC) | SD-JWT (IETF) |
|--------|------------------|---------------|
| **@context** | ✅ Built-in | ❌ Not supported |
| **Semantic linking** | ✅ Automatic via @context | ❌ Manual via registry |
| **RDF compatibility** | ✅ Native | ❌ Requires conversion |
| **Selective disclosure** | ⚠️ Requires extensions | ✅ Native |
| **JWT compatibility** | ⚠️ Via JWT-VC | ✅ Native |
| **Simplicity** | More complex | Simpler |

## Maintaining Semantic Integrity

**Best Practices:**

1. **Always distribute semantic registry** with SD-JWT schema
2. **Document semantic lineage** in credential metadata
3. **Provide resolution endpoint** for claim semantics
4. **Reference SHACL shapes** in credential type
5. **Include vocabulary version** in credential metadata

**Registry Usage:**

```python
# Resolve semantic meaning
registry = load_semantic_registry()
claim_semantic = registry['mappings']['document_number']

print(f"OWL Property: {claim_semantic['owl_property']}")
print(f"SKOS Concept: {claim_semantic['skos_concept']}")
print(f"Definition: {fetch_skos_definition(claim_semantic['skos_concept'])}")
```

## Warning: Semantic Gap

⚠️ **Important:** SD-JWT intentionally does not include @context to keep it simple.
This means semantic linking is **not automatic** and must be maintained externally
via this registry.

**Implications:**
- Verifiers must have access to semantic registry
- Claim names (snake_case) are arbitrary identifiers
- Semantic meaning requires registry lookup
- No automatic RDF graph construction

**Recommendation:** If semantic interoperability is critical, consider:
1. Using JSON-LD W3C VCs instead of SD-JWT
2. Providing both formats (dual-track approach)
3. Embedding registry reference in SD-JWT metadata

---

**Generated by:** SHACL to SD-JWT Converter  
**Source SHACL:** {shape_info['uri']}  
**Generated:** 2026-02-15
"""
        
        return doc


def main():
    """Main conversion process"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python shacl_to_sdjwt.py <shacl-file.ttl>")
        print("\nExample:")
        print("  python shacl_to_sdjwt.py shacl/packinglist-shape.ttl")
        sys.exit(1)
    
    shacl_file = sys.argv[1]
    output_base = shacl_file.replace('.ttl', '').replace('shacl/', 'sdjwt/')
    
    print(f"Converting SHACL to SD-JWT schema...")
    print(f"Input: {shacl_file}")
    
    converter = SHACLToSDJWT()
    
    # Load SHACL
    try:
        converter.load_shacl(shacl_file)
        print("✅ SHACL loaded")
    except Exception as e:
        print(f"❌ Error loading SHACL: {e}")
        sys.exit(1)
    
    # Find NodeShapes
    shapes = list(converter.graph.subjects(RDF.type, SH.NodeShape))
    
    if not shapes:
        print("❌ No SHACL NodeShapes found in file")
        sys.exit(1)
    
    print(f"Found {len(shapes)} shape(s)")
    
    for shape_uri in shapes:
        print(f"\nProcessing: {shape_uri}")
        
        # Extract shape info
        shape_info = converter.extract_shape_info(shape_uri)
        print(f"  Label: {shape_info.get('label', 'N/A')}")
        print(f"  Properties: {len(shape_info['properties'])}")
        
        # Generate SD-JWT schema
        schema = converter.generate_sdjwt_schema(shape_info)
        
        # Write schema
        schema_file = f"{output_base}-schema.json"
        with open(schema_file, 'w') as f:
            json.dump(schema, f, indent=2)
        print(f"  ✅ SD-JWT schema: {schema_file}")
        
        # Generate documentation
        doc = converter.generate_documentation(shape_info, schema)
        doc_file = f"{output_base}-docs.md"
        with open(doc_file, 'w') as f:
            f.write(doc)
        print(f"  ✅ Documentation: {doc_file}")
    
    # Generate semantic registry
    registry = converter.generate_semantic_registry()
    registry_file = "sdjwt/semantic-registry.json"
    with open(registry_file, 'w') as f:
        json.dump(registry, f, indent=2)
    print(f"\n✅ Semantic registry: {registry_file}")
    
    print("\n" + "="*60)
    print("CONVERSION COMPLETE")
    print("="*60)
    print("\n⚠️  IMPORTANT: SD-JWT Schema Limitations")
    print("• No @context support (plain JSON only)")
    print("• Semantic links maintained via external registry")
    print("• Always distribute semantic-registry.json with schemas")
    print("• Verifiers need registry to resolve semantic meaning")
    print("\n💡 Recommendation:")
    print("• Consider dual-track: JSON-LD W3C VCs + SD-JWT")
    print("• Embed registry reference in credential metadata")
    print("• Provide resolution endpoint for semantics")


if __name__ == "__main__":
    main()
