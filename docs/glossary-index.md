# Glossary index

This non-normative index maps commonly referenced DACS terms to their canonical specification sections. The normative glossary remains [Chapter 13](../spec/SPECIFICATION.md#chapter-13-glossary).

| Term | Primary spec section | Notes |
|------|----------------------|-------|
| Anchor / Anchored | [§5 / SR-2](../spec/SPECIFICATION.md#5-substrate-capabilities), [§12.5](../spec/SPECIFICATION.md#125-composite-trust-property) | Stored with content integrity via substrate anchoring. |
| AttestationBundle | [§10.4](../spec/SPECIFICATION.md#104-attestation-bundle) | End-of-session DACS-5 audit artifact. |
| AttestationRef | [§7.5](../spec/SPECIFICATION.md#75-shared-phase-handler-types) | Reference to anchored evidence plus content hash. |
| BundleParty | [§10.4](../spec/SPECIFICATION.md#104-attestation-bundle) | Party entry inside an AttestationBundle. |
| Canonical form | [§7.7](../spec/SPECIFICATION.md#77-universal-signature-scheme-domain-separated-signing) | RFC 8785 / JCS form used for hashes and signatures. |
| ClaimReference | [§7.1](../spec/SPECIFICATION.md#71-claim-references-and-identity) | Canonical identifier format for identity claims. |
| CompositeVerificationRecord | [§7.7](../spec/SPECIFICATION.md#77-composite-verification-record) | DACS-2 composite output for Vet. |
| IdentityBundle | [§6.3.2](../spec/SPECIFICATION.md#632-identity-bundle) | Ordered self-presented claim set with presentation signature. |
| Listing | [§6.3](../spec/SPECIFICATION.md#63-specification) | DACS-1 signed service advertisement. |
| Payment rail | [§9.4](../spec/SPECIFICATION.md#94-payment-rail-registry) | Registry entry describing a supported payment path. |
| RatingRecord | [§10.6](../spec/SPECIFICATION.md#106-the-rate-phase-optional) | Optional per-direction counterparty rating artifact. |
| SettlementEvidence | [§9.7](../spec/SPECIFICATION.md#97-settlement-evidence) | Anchored DACS-4 evidence produced by settle/deliver phases. |
| VerifyResult | [§7.5](../spec/SPECIFICATION.md#75-verifyresult) | DACS-2 single-method verification result. |

## Maintenance notes

- Keep this file additive and non-normative.
- If a term definition changes, update the linked spec section rather than paraphrasing new semantics here.
- Run `python3 scripts/validate-docs.py` after editing anchors.
