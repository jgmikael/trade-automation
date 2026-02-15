#!/usr/bin/env python3
"""
Real-world PD A1 Certificate Example: Dual-Track Issuance

Scenario:
Finnish construction worker (Matti Virtanen) employed by Nordic Construction Oy
is temporarily posted to work on a construction site in Berlin, Germany for 6 months.

The Finnish Social Insurance Institution (Kela) issues an A1 certificate proving that
Finnish social security legislation continues to apply during the posting period.
"""

import json
import sys
sys.path.insert(0, '../tools')
from dual_track_issuer import DualTrackIssuer

def issue_pda1_certificate():
    """Issue PD A1 certificate in both JSON-LD and SD-JWT formats"""
    
    issuer = DualTrackIssuer(
        issuer_did="did:web:kela.fi",
        schema_base_uri="https://kela.fi/schemas"
    )
    
    # Realistic A1 certificate data
    a1_data = {
        # Certificate metadata
        "identifier": "FI-2024-A1-123456",
        "issued": "2024-02-15",
        "coveredPeriod": "2024-03-01",  # Start date
        "valid": "2024-08-31",          # End date (6 months posting)
        
        # Insured person (worker)
        "insuredPerson": {
            "type": "Person",
            "id": "urn:fi:hetu:010180-123A",  # Finnish personal ID
            "givenName": "Matti",
            "familyName": "Virtanen",
            "birthDate": "1980-01-01",
            "nationality": "FI",
            "address": {
                "streetAddress": "Mannerheimintie 15 A 10",
                "postalCode": "00100",
                "addressLocality": "Helsinki",
                "addressCountry": "FI"
            }
        },
        
        # Employer
        "hasEmployer": {
            "type": "LegalEntity",
            "id": "https://ytj.fi/1234567-8",
            "legalName": "Nordic Construction Oy",
            "taxIdentifier": "FI12345678",
            "address": {
                "streetAddress": "Teollisuuskatu 3",
                "postalCode": "00510",
                "addressLocality": "Helsinki",
                "addressCountry": "FI"
            }
        },
        
        # Issuing institution
        "issuingInstitution": {
            "type": "PublicOrganisation",
            "id": "https://kela.fi",
            "name": "Kansaneläkelaitos / Folkpensionsanstalten",
            "acronym": "Kela",
            "contactPoint": {
                "email": "a1-todistukset@kela.fi",
                "telephone": "+358 20 634 0200"
            }
        },
        
        # Applicable legislation (Finnish social security applies)
        "hasLegalApplicability": {
            "type": "LegalApplicability",
            "applicableCountry": "FI",
            "legalFramework": "EU Regulation 883/2004",
            "description": "Finnish social security legislation applies"
        },
        
        # Work location (Germany)
        "hasWorkLocation": {
            "type": "Location",
            "countryCode": "DE",
            "addressLocality": "Berlin",
            "description": "Construction site in Berlin, Germany"
        },
        
        # Activity
        "hasActivity": {
            "type": "Activity",
            "activityType": "CONSTRUCTION",
            "description": "Commercial building construction project",
            "naceCode": "F41.2"  # Construction of residential and non-residential buildings
        },
        
        # Employment details
        "employmentType": "EMPLOYED",  # Not self-employed
        
        # Legal basis (Article 12.1 = temporary posting)
        "hasApplicableJurisdiction": "ART_12_1",
        
        # Not subject to transitional rules
        "isSubjectToTransitionalRules": False,
        
        # Determination (original certificate, not replacement)
        "hasDetermination": {
            "type": "Determination",
            "isOriginal": True,
            "replacementOf": None
        }
    }
    
    # Issue in both formats
    dual_credential = issuer.issue_dual_track(
        subject_data=a1_data,
        credential_type="PDA1Certificate",
        context_uri="https://iri.suomi.fi/context/webuild/pda1-v1.jsonld",
        registry_uri="https://iri.suomi.fi/registry/webuild/pda1-v1.json",
        subject_id="urn:fi:hetu:010180-123A"
    )
    
    return dual_credential

def main():
    print("="*80)
    print("PD A1 CERTIFICATE: DUAL-TRACK ISSUANCE")
    print("="*80)
    print()
    print("Scenario: Finnish worker posted to Germany")
    print("Worker:   Matti Virtanen (construction worker)")
    print("Employer: Nordic Construction Oy (Finland)")
    print("Posted:   Berlin, Germany (6 months)")
    print("Period:   2024-03-01 to 2024-08-31")
    print("Issuer:   Kela (Finnish Social Insurance Institution)")
    print()
    print("Generating dual-track credentials...")
    print()
    
    # Generate credentials
    result = issue_pda1_certificate()
    
    # Write output
    output_file = "../sdjwt/pda1-dual-track-example.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"✅ Dual-track credentials: {output_file}")
    print()
    
    # Extract both formats
    jsonld_vc = result['formats']['json-ld']['credential']
    sdjwt = result['formats']['sd-jwt']['credential']
    
    print("="*80)
    print("FORMAT COMPARISON")
    print("="*80)
    print()
    
    print("JSON-LD W3C VC:")
    print("  Type:", jsonld_vc['type'])
    print("  @context:", jsonld_vc['@context'][1])
    print("  Issuer:", jsonld_vc['issuer']['id'])
    print("  Subject ID:", jsonld_vc['credentialSubject'].get('id', 'N/A'))
    print()
    print("  Sample properties (camelCase):")
    print(f"    - identifier: {jsonld_vc['credentialSubject']['identifier']}")
    print(f"    - employmentType: {jsonld_vc['credentialSubject']['employmentType']}")
    print(f"    - hasApplicableJurisdiction: {jsonld_vc['credentialSubject']['hasApplicableJurisdiction']}")
    print()
    
    print("SD-JWT:")
    print("  Type:", sdjwt['type'])
    print("  Issuer:", sdjwt['iss'])
    print("  Subject:", sdjwt['sub'])
    print("  Semantic Registry:", sdjwt['_semantic_registry'])
    print()
    print("  Sample properties (snake_case):")
    print(f"    - identifier: {sdjwt['identifier']}")
    print(f"    - employment_type: {sdjwt['employment_type']}")
    print(f"    - has_applicable_jurisdiction: {sdjwt['has_applicable_jurisdiction']}")
    print()
    
    print("="*80)
    print("SEMANTIC RESOLUTION EXAMPLE")
    print("="*80)
    print()
    print("SD-JWT claim: 'has_applicable_jurisdiction'")
    print("      ↓ (lookup in semantic registry)")
    print("SHACL: webuild:hasApplicableJurisdiction")
    print("      ↓ (dcterms:subject)")
    print("SKOS: webuild-vocab:c_legalBasis")
    print("      ↓ (sanastot.suomi.fi)")
    print("Definition: 'EU regulation article under which certificate is issued'")
    print()
    print("Value: 'ART_12_1' = Article 12(1) of Regulation 883/2004")
    print("Meaning: Temporary posting (up to 24 months)")
    print()
    
    print("="*80)
    print("LEGAL CONTEXT: ARTICLE 12(1)")
    print("="*80)
    print()
    print("EU Regulation 883/2004, Article 12(1):")
    print()
    print("  'A person who pursues an activity as an employed person in a")
    print("   Member State on behalf of an employer which normally carries")
    print("   out its activities there and who is posted by that employer")
    print("   to another Member State to perform work on that employer's")
    print("   behalf shall continue to be subject to the legislation of")
    print("   the first Member State...'")
    print()
    print("Key conditions:")
    print("  ✅ Worker normally employed in Finland")
    print("  ✅ Employer (Nordic Construction Oy) operates in Finland")
    print("  ✅ Posting is temporary (6 months < 24 month limit)")
    print("  ✅ Worker continues under Finnish social security")
    print("  ✅ No German social security contributions required")
    print()
    
    print("="*80)
    print("USE CASES")
    print("="*80)
    print()
    print("Worker presents A1 certificate to:")
    print("  • German construction site inspector")
    print("  • German social security authority (Deutsche Rentenversicherung)")
    print("  • German health insurance providers")
    print("  • Border control (EU mobility)")
    print()
    print("Verification process:")
    print("  1. Scan QR code / receive digital credential")
    print("  2. Verify issuer signature (Kela's DID)")
    print("  3. Check validity period (2024-03-01 to 2024-08-31)")
    print("  4. Confirm legal basis (Article 12.1)")
    print("  5. Verify no German social security contributions needed")
    print()
    print("Benefits of digital A1:")
    print("  ✅ Instant verification (vs. weeks for paper)")
    print("  ✅ Tamper-proof (cryptographic signature)")
    print("  ✅ Semantic clarity (linked to EU regulations)")
    print("  ✅ Selective disclosure (can hide sensitive fields)")
    print("  ✅ Real-time validity check")
    print()
    
    print("="*80)
    print("STATISTICS")
    print("="*80)
    print()
    print(f"Properties in schema:       14")
    print(f"Required properties:        11")
    print(f"Optional properties:        3")
    print(f"Enum types:                 2 (employment_type, legal_basis)")
    print(f"Nested objects:             7")
    print(f"Total claims (SD-JWT):      14 snake_case")
    print(f"Semantic registry entries:  14")
    print()
    
    print("="*80)
    print("FILES GENERATED")
    print("="*80)
    print()
    print("Schema & Registry:")
    print("  ✅ sdjwt/webuild-pda1-certificate-shape-schema.json")
    print("  ✅ sdjwt/webuild-pda1-certificate-shape-registry.json")
    print("  ✅ sdjwt/webuild-pda1-certificate-shape-docs.md")
    print()
    print("Example Credentials:")
    print("  ✅ sdjwt/pda1-dual-track-example.json (both formats)")
    print()
    print("Source:")
    print("  ✅ analysis/webuild-pda1-certificate-shape.ttl (SHACL)")
    print()

if __name__ == "__main__":
    main()
