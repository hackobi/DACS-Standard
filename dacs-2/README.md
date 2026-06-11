# DACS/2 — Demos Agent Commerce Standards, Second Edition (draft)

**Version:** `dacs/2.0-draft.1` · **Status:** working draft · **License:** MIT · **Steward:** KyneSys Labs (transitioning to steward group, see §Governance)

DACS/2 is a ground-up revision of [DACS v0.1](https://github.com/DACS-Agent-commerce/DACS-Standard). It specifies a complete,
verifiable lifecycle for agent-to-agent commerce — **Identify → Vet → Negotiate → Settle → Verify → Resolve** — built
natively on the [Demos Network node](https://github.com/kynesyslabs/node) instead of on abstract substrate requirements.

## Why a second edition

v0.1 was specified at the "substrate-capability level" (SR-1..SR-5), yet Demos was the only substrate shipping all five,
and two of the five (proxy attestation, private channels) had no wire format at all. The result was a standard that was
neither portable in practice nor interoperable on its home substrate: two independent conformant implementations could
not exchange a single message. DACS/2 resolves this honestly, with two layers:

- **L0 — Artifact layer (portable).** Signed, RFC 8785-canonicalised, content-addressed artifacts with a closed
  domain-separator registry. Any system can verify a DACS/2 artifact offline. This is the part of v0.1 that was
  genuinely substrate-neutral, and it is preserved and tightened.
- **L1 — Demos binding (normative wire format).** Every lifecycle operation is bound to an exact Demos node surface:
  transaction types, RPC methods, Storage Program addresses, SDK calls. Two conformant DACS/2 implementations
  interoperate because the wire is the Demos node itself.

## What changed (highlights)

| v0.1 gap | DACS/2 resolution |
|---|---|
| No agent-to-agent transport; RFQ bodies "implementation-defined" | Normative `DacsEnvelope` over Demos Instant Messaging / L2PS / HTTPS, with normative offer/counter/accept bodies ([spec/05](spec/05-negotiation.md)) |
| No escrow, no delivery-gated payment | `pay-demos-escrow` rail (GCR escrow edits) and `pay-demoswork-conditional` (DAHR-verified delivery → release) ([spec/06](spec/06-settlement.md)) |
| Settlement evidence not session-bound (replay gap) | Session-binding rules SB-1..SB-4: `d402_payment.memo` binding, unique deposit addresses, HTLC preimage, DemosWork jobId ([spec/06](spec/06-settlement.md)) |
| Omnipotent, unspecified orchestrator | Removed as a protocol role. Sessions are peer-driven; phase responsibility is assigned per phase ([spec/00](spec/00-architecture.md)) |
| No dispute resolution | DACS-6 Resolve: divergence detection, DisputeRecord, credentialed arbitrators ([spec/08](spec/08-disputes.md)) |
| Reputation has no completeness oracle | Bundles anchor as Storage Program txs from the party's own account; `getTransactionHistory` enumerates them — the chain is the oracle ([spec/07](spec/07-attestation-reputation.md)) |
| Weak SR-3 floor under institutional claims | Tier floor: institutional claims require `tlsnotary` / `verifiable-credential` / `zktls`; DAHR alone is insufficient ([spec/03](spec/03-vetting.md)) |
| No selective disclosure; full counterparty-graph exposure | ZK claim proofs via node nullifier registry; pairwise-salted anchor addresses ([spec/02](spec/02-identity.md)) |
| Single-steward registry chokepoint | Registries live in an ACL-group Storage Program; M-of-N steward co-signatures ([spec/03](spec/03-vetting.md) §Governance) |
| Anchor address rule didn't resolve on the node (DACS-VERIFY-0003) | All anchors use the node's real `StorageProgram.deriveStorageAddress` ([spec/01](spec/01-canonical-form-and-signatures.md)) |
| No machine-readable schemas | JSON Schema 2020-12 for core artifacts ([schemas/](schemas/)) |
| No cancellation semantics | `cancel` envelope + `cancelled` terminal outcome, reputation-neutral when policy-compliant ([spec/07](spec/07-attestation-reputation.md)) |
| Ed25519/secp256k1 only | Adds post-quantum `falcon` and `ml-dsa`, matching node `SigningAlgorithm` ([spec/01](spec/01-canonical-form-and-signatures.md)) |

What was kept from v0.1 because it was right: RFC 8785 + NFC canonicalisation, canonical decimals, the preserve-unknown
signature rule, four-valued verification decisions (`pass/fail/indeterminate/error`), the 7-value `availability` enum,
two-sided attestation bundles with perspective-flipped reconciliation, and the HTLC treatment (HKDF preimage, HTLC-9).

## The six stages

```
DACS-1 Identify   on-chain agent passport (CCI claims) + authority claims
DACS-2 Vet        recipe-driven verification, 4-valued decisions, tiered trust floors
DACS-3 Negotiate  signed envelopes over IM/L2PS; fixed-price, RFQ, sealed-envelope
DACS-4 Settle     session-bound payment + delivery rails, escrow, conditional release
DACS-5 Verify     co-signed AttestationBundle, enumerable reputation
DACS-6 Resolve    structured disputes with credentialed arbitrators
```

## Repository map

| Path | Contents |
|---|---|
| [spec/00-architecture.md](spec/00-architecture.md) | Layers, actors, peer-driven session model, conformance classes |
| [spec/01-canonical-form-and-signatures.md](spec/01-canonical-form-and-signatures.md) | Canonicalisation, separator registry, signatures, anchor addressing |
| [spec/02-identity.md](spec/02-identity.md) | DACS-1: chain-native + authority claims, presentation, revocation, ZK disclosure |
| [spec/03-vetting.md](spec/03-vetting.md) | DACS-2: methods, recipes, tier floors, registry governance |
| [spec/04-discovery.md](spec/04-discovery.md) | Listings as Storage Programs, search, agent card |
| [spec/05-negotiation.md](spec/05-negotiation.md) | DACS-3: transport envelope, negotiation patterns, agreement, commitment |
| [spec/06-settlement.md](spec/06-settlement.md) | DACS-4: rails, session binding, evidence, amendments |
| [spec/07-attestation-reputation.md](spec/07-attestation-reputation.md) | DACS-5: state machine, bundles, reputation |
| [spec/08-disputes.md](spec/08-disputes.md) | DACS-6: disputes, arbitrators, outcomes |
| [bindings/demos-node.md](bindings/demos-node.md) | The normative wire binding: tx types, RPC methods, SDK calls, feature gates |
| [bindings/mcp-tools.md](bindings/mcp-tools.md) | Commerce tool surface for the node's embedded MCP server |
| [schemas/](schemas/) | JSON Schema 2020-12 for core artifacts |
| [MIGRATION.md](MIGRATION.md) | v0.1 → DACS/2 mapping and resolved defects |

## Conformance classes

- **`dacs2-core`** — implements L0: produces/verifies canonical artifacts and signatures. Portable; no Demos dependency.
- **`dacs2-demos`** — implements L0 + L1: full lifecycle on a Demos network. This is the interoperability target.
- **Per-stage profiles** — `dacs2-demos/identify`, `/vet`, `/negotiate`, `/settle`, `/verify`, `/resolve`. A settlement-only
  integration (e.g. a d402-payable API) MAY conform to `/settle` alone.

## Normative language

"MUST", "SHOULD", "MAY" per RFC 2119 / RFC 8174. Non-normative text is marked *Note:* or appears in rationale blocks.

## Status and maturity

Draft. The L1 binding references the node's **`stabilisation` branch** (the most advanced; pins
`@kynesyslabs/demosdk 4.0.5`). Feature availability still differs per network — escrow and contract GCR handlers
remain stubs even on stabilisation — so the binding declares per-feature gates keyed to the node's fork registry
rather than assuming uniform availability ([bindings/demos-node.md](bindings/demos-node.md) §6). Nothing here is
ready for unsupervised production use.
