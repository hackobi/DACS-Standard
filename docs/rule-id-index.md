# Rule-ID index

This non-normative index helps implementers locate labelled conformance rules in the specification. The specification text remains authoritative.

| Rule family | Role / surface | Spec section | Test-plan hook |
|-------------|----------------|--------------|----------------|
| BP-* | Bundle producers for IdentityBundle | [§6.3.2](../spec/SPECIFICATION.md#632-identity-bundle) | [§14.1](../spec/SPECIFICATION.md#141-dacs-1-identify) |
| BR-* | Bundle readers for IdentityBundle | [§6.3.2](../spec/SPECIFICATION.md#632-identity-bundle) | [§14.1](../spec/SPECIFICATION.md#141-dacs-1-identify) |
| LP-* | Listing publishers | [§6.3](../spec/SPECIFICATION.md#63-specification) | [§14.1](../spec/SPECIFICATION.md#141-dacs-1-identify) |
| LR-* | Listing readers | [§6.3](../spec/SPECIFICATION.md#63-specification) | [§14.1](../spec/SPECIFICATION.md#141-dacs-1-identify) |
| SIG-* | Universal domain-separated signatures | [§7.7](../spec/SPECIFICATION.md#77-universal-signature-scheme-domain-separated-signing) | [§14.6](../spec/SPECIFICATION.md#146-universal-signature-scheme-canonical-form-sig-1sig-5-cf-1cf-4-cd-1) |
| RAV-* | Recipe availability values and consumers | [§7.4.5](../spec/SPECIFICATION.md#745-recipe-availability-normative) | [§14.2](../spec/SPECIFICATION.md#142-dacs-2-vet) |
| RAV-R* | Rail availability values and orchestrators | [§9.4.5](../spec/SPECIFICATION.md#945-rail-availability-normative) | [§14.4](../spec/SPECIFICATION.md#144-dacs-4-settle) |
| VPC-* | Vet phase contract | [§7.8](../spec/SPECIFICATION.md#78-the-vet-credentials-phase) | [§14.2](../spec/SPECIFICATION.md#142-dacs-2-vet) |
| PC-* | Payment phase common contract | [§9.5](../spec/SPECIFICATION.md#95-payment-phases) | [§14.4](../spec/SPECIFICATION.md#144-dacs-4-settle) |
| RT-* | Rating bounds and derivation handling | [§10.6.1](../spec/SPECIFICATION.md#1061-phase-contract) | [§14.5](../spec/SPECIFICATION.md#145-dacs-5-verify) |

## How to use this index

- Treat it as a navigation aid only; rule wording lives in the linked spec sections.
- Prefer rule-family tests that point at the §14 conformance plan before adding one-off checks.
- Substrate-capability checks are indexed separately in [§14.8](../spec/SPECIFICATION.md#148-substrate-capability-tests).
- Update this index when a new labelled rule family is added to the specification.
