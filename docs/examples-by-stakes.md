# DACS examples by transaction stakes

*Non-normative. These examples illustrate how the same five-stage lifecycle scales across different commercial stakes. They do not add conformance requirements; the normative source remains the Core specification plus the five stage modules.*

The important design point is that DACS does not define one flow for "micropayments" and another unrelated flow for "institutional commerce." The same stages and artifact chain apply. What changes is the identity bundle, verification depth, negotiation pattern, settlement rail, and audit expectations.

## Low-stakes: $0.01 data lookup

**Scenario:** An agent buys a single API response from a data seller.

- **Identify:** The seller presents a signing key and a signed listing discovered through `.well-known/agent.json` or a catalog lookup.
- **Vet:** The buyer performs a light freshness check: the signing key is still active and the seller's reputation is above the buyer's local threshold.
- **Negotiate:** Fixed-price acceptance. The posted terms already name rate limit, time window, allowed endpoint, and price.
- **Settle:** x402 micropayment over HTTP. The response is also the deliverable.
- **Verify:** A compact session bundle is anchored. Reputation updates against the signing-key primary claim.

**Why DACS still helps:** even when the payment is tiny, the buyer can verify the seller's listing, bind the payment to an audit trail, and reuse the same reputation machinery as larger sessions.

## Medium-stakes: $500 B2B SaaS purchase

**Scenario:** A marketing agent buys a SaaS subscription or tool access from another agent.

- **Identify:** The seller presents a signing key plus platform/domain claims: verified domain, GitHub or Google account, X handle, Stripe Connect tier, and visible reputation.
- **Vet:** The buyer refreshes each platform identity and pulls supplementary reputation. A listing may also require a deal-specific entitlement or business-status check.
- **Negotiate:** The parties negotiate discount, contract term, SLA tier, renewal grace, and usage limits. Final terms become an AgreementDocument.
- **Settle:** AP2 mandate or on-chain stablecoin payment. The seller delivers an EntitlementRecord naming service endpoint, scope, and validity window.
- **Verify:** The final bundle anchors identity, vet records, agreement, payment evidence, entitlement evidence, and optional rating.

**Why DACS still helps:** the buyer does not need to trust a marketplace database for proof of purchase, entitlement, or reputation; the audit artifact is portable.

## High-stakes: $50k regulated data trade

**Scenario:** A trading desk agent buys private market data or analysis from a regulated counterparty.

- **Identify:** The seller's primary claim is an LEI or equivalent authority-issued identifier, with signing key, domain, FINRA/FCA registration where applicable, and sanctions-screening requirements.
- **Vet:** The buyer refreshes LEI status, regulatory registration, OFAC/sanctions status, and any deal-specific KYB or clearance. Supplementary signals inform local acceptance policy.
- **Negotiate:** RFQ or sealed-envelope negotiation runs inside an identity-keyed private channel. Only the final commitment hash is public.
- **Settle:** Cross-chain stablecoin settlement through the selected rail. Delivery is an attested payload or anchored storage write.
- **Verify:** The AttestationBundle anchors every material artifact. Reputation derives against the institutional primary claim, not a low-stakes key.

**Why DACS still helps:** regulated counterparties get current credential checks, private negotiation, settlement evidence, and a participant-owned audit record without moving the whole flow into a closed operator marketplace.

## Comparison matrix

| Stage | $0.01 data lookup | $500 B2B SaaS | $50k regulated trade |
| --- | --- | --- | --- |
| Identify | Signing key; signed listing | Key + domain/platform claims | LEI/regulatory identity + key/domain |
| Vet | Key active; reputation threshold | Platform/domain freshness + reputation | LEI, registration, sanctions, KYB |
| Negotiate | Fixed-price acceptance | Light terms negotiation | Private RFQ / sealed-envelope |
| Settle | x402 HTTP payment | AP2 or stablecoin + entitlement | Cross-chain rail + attested payload |
| Verify | Compact bundle; key reputation | Bundle + entitlement/rating | Full audit bundle; institutional reputation |

## Review note

Readers should treat these examples as a readability aid. If an example appears to conflict with a rule in the normative spec, the spec controls and the example should be corrected.
