#!/usr/bin/env python3
"""
Dual-Track Credential Issuer

Issues BOTH formats from the same SHACL source:
1. JSON-LD W3C Verifiable Credentials (semantic track)
2. IETF SD-JWT (selective disclosure track)

Both maintain semantic integrity through different mechanisms:
- JSON-LD: @context provides automatic semantic linking
- SD-JWT: External semantic registry provides manual linking
"""

import json
import time
import hashlib
from typing import Dict, Any, Optional

def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case"""
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.lower()

class DualTrackIssuer:
    """Issue credentials in both JSON-LD and SD-JWT formats"""
    
    def __init__(self, issuer_did: str, schema_base_uri: str):
        self.issuer_did = issuer_did
        self.schema_base_uri = schema_base_uri
    
    def issue_jsonld_vc(self, 
                       subject_data: Dict[str, Any],
                       credential_type: str,
                       context_uri: str,
                       subject_id: Optional[str] = None) -> Dict[str, Any]:
        """Issue W3C Verifiable Credential in JSON-LD format"""
        
        now = int(time.time())
        credential_id = f"urn:uuid:{hashlib.sha256(str(now).encode()).hexdigest()[:32]}"
        
        vc = {
            "@context": [
                "https://www.w3.org/ns/credentials/v2",
                context_uri  # ⭐ Semantic linking via @context
            ],
            "type": ["VerifiableCredential", credential_type],
            "id": credential_id,
            "issuer": {
                "id": self.issuer_did,
                "type": "Organization"
            },
            "issuanceDate": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
            "expirationDate": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now + 86400)),
            "credentialSubject": subject_data
        }
        
        if subject_id:
            vc["credentialSubject"]["id"] = subject_id
        
        # Add proof placeholder (would be signed in production)
        vc["proof"] = {
            "type": "DataIntegrityProof",
            "cryptosuite": "eddsa-rdfc-2022",
            "created": vc["issuanceDate"],
            "verificationMethod": f"{self.issuer_did}#key-1",
            "proofPurpose": "assertionMethod",
            "proofValue": "z..." + "PLACEHOLDER" * 10  # Would be actual signature
        }
        
        return vc
    
    def issue_sdjwt(self,
                   subject_data: Dict[str, Any],
                   credential_type: str,
                   registry_uri: str,
                   subject_id: Optional[str] = None) -> Dict[str, Any]:
        """Issue IETF SD-JWT format"""
        
        now = int(time.time())
        
        # Convert camelCase data to snake_case for SD-JWT
        sdjwt_data = {}
        for key, value in subject_data.items():
            snake_key = camel_to_snake(key)
            sdjwt_data[snake_key] = value
        
        # SD-JWT structure (no @context!)
        sdjwt = {
            "iss": self.issuer_did,
            "sub": subject_id or f"urn:uuid:{hashlib.sha256(str(now).encode()).hexdigest()[:16]}",
            "iat": now,
            "exp": now + 86400,
            "type": credential_type,
            
            # ⭐ Reference to semantic registry (external linking)
            "_semantic_registry": registry_uri,
            "_semantic_context": f"{self.schema_base_uri}/context/{credential_type.lower()}-v1.jsonld",
            
            # Actual claims (snake_case)
            **sdjwt_data
        }
        
        # Note: In production, this would be:
        # 1. JWT-encoded (header.payload.signature)
        # 2. Include selective disclosure hashes
        # 3. Append disclosure claims
        # Format: <JWT>~<disclosure-1>~<disclosure-2>~...
        
        return sdjwt
    
    def issue_dual_track(self,
                        subject_data: Dict[str, Any],
                        credential_type: str,
                        context_uri: str,
                        registry_uri: str,
                        subject_id: Optional[str] = None) -> Dict[str, Any]:
        """Issue both formats from same data"""
        
        return {
            "format": "dual-track",
            "source": "SHACL shape",
            "credential_type": credential_type,
            "formats": {
                "json-ld": {
                    "format": "W3C Verifiable Credential",
                    "specification": "https://www.w3.org/TR/vc-data-model-2.0/",
                    "semantic_linking": "automatic via @context",
                    "credential": self.issue_jsonld_vc(
                        subject_data, 
                        credential_type, 
                        context_uri, 
                        subject_id
                    )
                },
                "sd-jwt": {
                    "format": "IETF SD-JWT",
                    "specification": "https://datatracker.ietf.org/doc/draft-ietf-oauth-selective-disclosure-jwt/",
                    "semantic_linking": "manual via registry",
                    "semantic_registry": registry_uri,
                    "credential": self.issue_sdjwt(
                        subject_data, 
                        credential_type, 
                        registry_uri, 
                        subject_id
                    )
                }
            },
            "semantic_equivalence": True,
            "note": "Both credentials carry the same information. JSON-LD has automatic semantic linking; SD-JWT requires registry lookup."
        }

def demo_weBuild_attestation():
    """Demo: Issue WE BUILD Tax Debt Status Attestation in both formats"""
    
    issuer = DualTrackIssuer(
        issuer_did="did:web:tax-authority.fi",
        schema_base_uri="https://tax-authority.fi/schemas"
    )
    
    # Subject data (camelCase for JSON-LD)
    attestation_data = {
        "identifier": "ATT-2024-TAX-00123",
        "issued": "2024-02-15T10:30:00Z",
        "valid": "2024-08-15T10:30:00Z",
        "isLegalEntity": {
            "type": "LegalEntity",
            "id": "https://ytj.fi/0123456-7",
            "legalName": "Example Construction Oy",
            "taxIdentifier": "FI12345678"
        },
        "issuingInstitution": {
            "type": "PublicOrganisation",
            "id": "https://vero.fi",
            "name": "Finnish Tax Administration"
        },
        "hasTaxDebtStatus": "NO_DEBT",
        "hasApplicableJurisdiction": {
            "type": "Location",
            "countryCode": "FI"
        },
        "applicablePeriod": "2023-Q4"
    }
    
    # Issue both formats
    dual_credential = issuer.issue_dual_track(
        subject_data=attestation_data,
        credential_type="TaxDebtStatusAttestation",
        context_uri="https://iri.suomi.fi/context/webuild/tax-debt-v1.jsonld",
        registry_uri="https://iri.suomi.fi/registry/webuild/tax-debt-v1.json",
        subject_id="https://ytj.fi/0123456-7"
    )
    
    return dual_credential

def main():
    print("="*70)
    print("DUAL-TRACK CREDENTIAL ISSUER")
    print("="*70)
    print()
    print("Issuing WE BUILD Tax Debt Status Attestation in BOTH formats...")
    print()
    
    # Generate dual-track credentials
    result = demo_weBuild_attestation()
    
    # Write output
    output_file = "sdjwt/dual-track-example.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"✅ Dual-track credentials generated: {output_file}")
    print()
    print("="*70)
    print("COMPARISON")
    print("="*70)
    print()
    
    jsonld_vc = result['formats']['json-ld']['credential']
    sdjwt = result['formats']['sd-jwt']['credential']
    
    print("JSON-LD W3C VC:")
    print(f"  - Has @context: ✅ (automatic semantic linking)")
    print(f"  - Property names: camelCase (as per context)")
    print(f"  - Example: 'hasTaxDebtStatus': '{jsonld_vc['credentialSubject']['hasTaxDebtStatus']}'")
    print()
    
    print("SD-JWT:")
    print(f"  - Has @context: ❌ (no semantic linking)")
    print(f"  - Property names: snake_case (convention)")
    print(f"  - Example: 'has_tax_debt_status': '{sdjwt['has_tax_debt_status']}'")
    print(f"  - Semantic registry: {sdjwt['_semantic_registry']}")
    print()
    
    print("Semantic Resolution for SD-JWT:")
    print("  SD-JWT claim: 'has_tax_debt_status'")
    print("       ↓ (registry lookup)")
    print("  SHACL: webuild:hasTaxDebtStatus")
    print("       ↓ (dcterms:subject)")
    print("  SKOS: webuild-vocab:c_taxDebtStatus")
    print("       ↓ (sanastot.suomi.fi)")
    print("  Definition: [Full semantic meaning]")
    print()
    
    print("="*70)
    print("VERIFICATION NOTES")
    print("="*70)
    print()
    print("JSON-LD W3C VC Verifier:")
    print("  1. Verify signature (proof)")
    print("  2. Resolve @context to get semantic meaning")
    print("  3. Validate against SHACL shape")
    print("  4. RDF triples available for reasoning")
    print()
    print("SD-JWT Verifier:")
    print("  1. Verify JWT signature")
    print("  2. Fetch semantic registry from _semantic_registry URI")
    print("  3. Resolve claim meanings via registry")
    print("  4. Manual validation (no automatic RDF)")
    print()
    
    print("Both formats carry the same information.")
    print("Choice depends on requirements:")
    print("  - Semantic interoperability → JSON-LD")
    print("  - Selective disclosure → SD-JWT")
    print("  - Best of both → Issue both! (dual-track)")

if __name__ == "__main__":
    main()
