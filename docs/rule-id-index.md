# Rule-ID index

This non-normative index helps implementers locate labelled conformance rules in the specification. The specification text remains authoritative.

## Rule families

| Rule family | Role / surface | Spec section | Test-plan hook |
|-------------|----------------|--------------|----------------|
| AMEND-* | Settlement amendment validation | §9.7.1 | §14.4 |
| BP-* | Bundle producers for IdentityBundle | §6.3.2 | §14.1 |
| BR-* | Bundle readers for IdentityBundle | §6.3.2 | §14.1 |
| CA-* | Commit-agreement phase validation | §8.6 | §14.3 |
| CD-* | Canonical decimal handling | §8.5.1 | §14.6 |
| CF-* | Canonical form and logical-address encoding | §7.2 / §6.3.4 | §14.6 |
| CH-* | Private-channel message handling | §8.3.3 | §14.3 |
| CM-* | Content-addressed anchoring | §7.3.1 | §14.8 |
| GOV-* | Progressive-anchoring governance | §11.2.6 | §14.7 |
| HTLC-* | Cross-chain HTLC payment rail | §9.5.3 | §14.4 |
| LP-* | Listing publishers | §6.3 | §14.1 |
| LR-* | Listing readers | §6.3 | §14.1 |
| MA-* | Multi-claim agreement validation | §8.5.2 | §14.3 |
| PA-* | Progressive-anchoring phases | §11.2.6 | §14.7 |
| PC-* | Payment phase common contract | §9.5 | §14.4 |
| PIPE-* | Pipeline shape and phase ordering | §8.8 | §14.3 |
| PS-* | Negotiation pattern selection | §8.8 | §14.3 |
| PSP-* | Price snapshot phase | §8.5.1 | §14.3 |
| RA-* | Recipe availability values and consumers | §7.4.5 | §14.2 |
| RAV-* | Recipe availability values and consumers | §7.4.5 | §14.2 |
| RAV-R* | Rail availability values and orchestrators | §9.4.4 | §14.4 |
| RD-* | Delivery phase required data | §9.6 | §14.4 |
| RFQ-* | RFQ negotiation turns | §8.4.2 | §14.3 |
| RT-* | Rating bounds and derivation handling | §10.6.1 | §14.5 |
| SE-* | Sealed-envelope negotiation | §8.4.3 | §14.3 |
| SIG-* | Universal domain-separated signatures | §7.7 | §14.6 |
| ST-* | Session transcript and attestation bundle | §10.4 | §14.5 |
| VP-C* | VerifyResult caching semantics | §7.6.1 | §14.2 |
| VP-R* | VerifyResult retry semantics | §7.6.1 | §14.2 |
| VPC-* | Vet phase contract | §7.8 | §14.2 |

## How to use this index

- Treat it as a navigation aid only; rule wording lives in the linked spec sections.
- Prefer rule-family tests that point at the §14 conformance plan before adding one-off checks.
- Substrate-capability checks are indexed separately in [§14.8](../spec/SPECIFICATION.md#148-substrate-capability-tests).
- Update this index when a new labelled rule family is added to the specification.
- Run `python3 scripts/validate_rule_ids.py` before opening a PR that edits labelled rules or this index.
