# DACS Roadmap

DACS **v0.1** deliberately specifies only what is **shipped and reference-backed**:
a rail, method, or capability earns normative status when a live settlement /
verification path exists *and* a reference implementation exercises it. Everything
below is **anticipated follow-on work** — named honestly, with **no committed
dates**. DACS operates under progressive-anchoring phase PA-2 (single steward,
KyneSys Labs); we do not commit timelines we cannot guarantee.

This document is **informative**; the normative source is the
[specification](./spec/SPECIFICATION.md). Where an item is already described in the
spec, the section is cited.

The roadmap has two parts:

- **Part 1 — Standard (normative).** Work that changes the *specification* itself —
  new rails, methods, rules, governance. These land in future minor versions
  (v0.2, v0.3, …) per the independent per-stage versioning in
  [CONTRIBUTING](./CONTRIBUTING.md), merge through the steward, and can affect
  conformance.
- **Part 2 — Ecosystem & tooling (non-normative).** Supporting artifacts *around*
  the standard — tooling, documentation, reference implementations, test vectors.
  These never change the spec or conformance, are welcomed as community
  contributions under a "contributor prototypes, steward owns the standard" model,
  and may be designated canonical by the steward if they prove solid.

---

# Part 1 — Standard (normative)

## Settlement rails (DACS-4)

| Item | Status | Notes |
|------|--------|-------|
| `pay-d402` | Anticipated | Native Demos D402 payment path as a first-class rail, once it meets the v0.1 shipped-path + reference-implementation bar. Not subsumed by `pay-evm-erc20` / `pay-solana-spl` — it is a distinct native settlement path. |
| `pay-evm-erc8183` — escrow with delivery-gate (#8) | Anticipated | EVM-native job-escrow rail composing ERC-8183 (already named in the spec, §9) — the natural home for **escrow-with-delivery-gate** (lock → deliver → release), which the v0.1 atomic-swap `pay-cross-chain-htlc` handler cannot express (no mid-lock suspension point; §9.5.4 / §9.9). |
| Liquidity Tank Phase 2–4 | Partially live | Phase 1 is live (ETH Sepolia ↔ Polygon Amoy testnet, USDC, unidirectional, EVM-source). Roadmap: Solana destination, bidirectional flow, validator-set co-signing of tank operations, mainnet deployments, additional stablecoins. |
| Liquidity-tank recovery-pending evidence (#25) | Candidate | A `recoveryDeadline` field / recovery-pending marker (and possibly a `settle-recovery-pending` state) so a locked-but-not-yet-released tank settlement inside the recovery window is machine-distinguishable from a terminal loss. v0.1 tank evidence is success-only (§9.5.5); recoverable locks surface only via the settlement-atomicity failure mode. |
| Streaming / continuous-flow rails + subscription model (#64) | Anticipated | Per-second / per-byte settlement; and multi-tranche subscriptions modelled as a **sequence of correlated sessions** (a cross-session `subscriptionId` or renewal-as-amendment) — one pipeline = one jobId in v0.1, so streamed entitlement is N sessions, not a loop. Out of scope for v0.1 (§11.2.4, §9.9). |
| Proactive rail-liveness probe (#23) | Candidate | An out-of-band check that lets an orchestrator detect a rail is non-operational *before* attempting settlement (mirroring the §8.12 CH-4 channel-liveness probe). v0.1 pins `availability` at session start and detects rail failure only at the settlement attempt (RAV-R4, §9.4.5). |
| `SettlementFinality` field on SettlementEvidence | Candidate | Surface the chain-specific confirmation / finality model into the evidence record so audit tools can read it without re-deriving. Foundation already exists (PC-4 ties `ok:true` to the chain's finality semantics; rails carry `finalityBlocks` / `commitmentLevel`); this is the surfacing field. |
| `FeeSchedule` disclosure in AgreementDocument | Candidate | Declared/negotiated fee disclosure for regulated contexts (EU MiCA, US MSB). Optional, non-breaking. Design-issue first. |
| Entitlement credential / token handover (#61) | Candidate | How an access **credential / token** is delivered to the grantee for a `deliver-entitlement` grant (vs. presenting the EntitlementRecord itself as the bearer proof). v0.1 adds the `serviceEndpoint` (*where* to access); the credential mechanism (*how to authenticate*) is an out-of-band auth concern left to a future version. |
| Fee-split / multi-payee settlement model (#85) | Candidate; design-issue first | Settlement-time split of one price across distinct payees (e.g. seller + platform fee): `fees[]` / `splits[]` on the payment contract plus reconciliation, rounding, per-phase amount override, and volume attribution. v0.1's `PaymentPhaseInput.amount` is the single agreement price (PIPE-5 repetition settles the same amount), so fee-split is unrepresentable today. Distinct from the `FeeSchedule` *disclosure* candidate above — this is execution, that is declaration. |
| HTLC anti-free-option mechanism (#24, HTLC-10) | Candidate; design-issue first | Bonded premium / timeout fee / stake to compensate the payee for the inherent free option the preimage-holding payer holds in a basic HTLC swap (HTLC-10 discloses but does not remedy it). v0.1 steers option-sensitive flows to pay-cross-chain-liquidity-tank or a stake instead. |

## Identity & vetting (DACS-1 / DACS-2)

| Item | Status | Notes |
|------|--------|-------|
| 6 new CCI contexts (lei, finra-crd, sam-uei, fedramp, naics, cmmc) | Staged | Institutional DACS-1 conformance is gated on these GCR routines being built. |
| DAHR validator-body-signed mode | Anticipated | Strengthens SR-3 beyond hash-commitment; high-stakes recipes (lei, finra-crd, ofac-clear, sam-uei) migrate when it ships (§7.3.5). |
| Selective / minimised-claim disclosure | Anticipated | v0.1 provides no per-claim selective disclosure at the bundle layer (§11.2.7; scope note §6.3.2). |
| `ReputationHint` at discovery | Candidate | Surface a DACS-5 summary (e.g. `{completedSessions, disputeRate}`) in the DACS-1 listing so buying agents can filter before vetting. Optional, additive (§6.3). |
| `ServiceCategory` taxonomy + category-scoped reputation | Candidate | Listing-level category tag (recommended vocabulary) so DACS-5 reputation can be queried per-domain ("20+ completed data-analysis sessions") rather than as one undifferentiated score (§6.3, §10.5). |
| Primary-claim revocation / compromise signalling | Candidate; design-issue first | A way to publish "this primary claim is compromised" so reputation does not silently transfer to an attacker after key theft. Hard part is revocation without the old key — needs an RFC before a PR. |
| `identityTier` on IdentityBundle (#103) | Candidate | Optional, **derived-not-self-declared** trust tier (`institutional` / `verified` / `self-declared`) computed from the verified claims present, giving downstream a pre-reputation trust signal (cold-start). Listings can gate on it (§6.3). |
| `warnings` array on CompositeVerificationRecord (#102) | Candidate | Optional signal distinguishing a *transient* authority failure (5xx, rate-limit, DNS timeout — retryable, with `suggestedRetryAfterMs`) from a permanent fail, so DACS-3 can decide retry-vs-proceed-vs-block. Additive; does not change required/oneOf/supplementary aggregation (§7.7/§7.8). |

## Negotiation (DACS-3)

| Item | Status | Notes |
|------|--------|-------|
| CCI-keyed L2PS membership + channel-envelope API + transcript export | Substrate-live; SDK backlog | Today the CH-1..CH-5 channel properties are orchestrator-enforced at the application layer; these move enforcement into the SR-4 substrate (DACS-3 Tier-1). |
| `negotiate-multi-quote` | Anticipated | First-class 1-to-N RFQ; today approximated via `negotiate-sealed-envelope` (§11.2.3). |
| L2PS channel key rotation / forward secrecy | Anticipated | Rekeying, session-key expiry, and forward-secrecy requirements for long-lived (hours/days) negotiation channels. Lands with the SR-4 ergonomics work. |
| `PriceAnchor` in AgreementDocument | Candidate | Optional DAHR-attested price snapshot both parties sign against, anchoring an agreement to a verifiable market reference (regulated/financial use). Optional, non-breaking (§8.5). |
| Dynamic channel membership (#21) | Candidate; design-issue first | Mid-negotiation add/remove of channel members with a normative `admissionPolicy` schema and a `membership-change` message body. v0.1 fixes membership for the channel's lifetime (CH-1) and reserves `membership-change`; reopening it needs an admission-policy + verifier-validation design (and a real use case beyond the three v0.1 negotiate patterns). |

## Verify & accountability (DACS-5)

| Item | Status | Notes |
|------|--------|-------|
| DACS-X (dispute / execution-verification) | Anticipated; prototype in progress | Dispute initiation, arbitrator credentialing via DACS-1/2, named-arbitrator transcript disclosure, superseding outcome bundles (§11.2.1). The accountability layer — makes the session record adjudicable; it does not hide session content. |
| DACS-5 → ERC-8004 cross-claim hint | Candidate | Optional bridge for the primary-claim (DACS-5) vs token (ERC-8004) reputation-keying divergence (§10.7). For v0.1 the divergence stands and the §10.7 fetch-the-bundle requirement is the mitigation. |
| `suspiciousPatternFlags` on ReputationRecord + min-bundleCount gating advice (#101) | Candidate; design-issue first | Optional behavioural-Sybil signal for low-tier selectors (e.g. single-counterparty clustering, zero-variance outcomes). Flags themselves are fine as an **open vocabulary**; the normative-threshold and min-`bundleCount` gating parts need an RFC so the standard doesn't hard-code heuristics that belong in the implementation layer (§10.5). Pairs with `identityTier` (#103) — identity quality + behavioural quality as two orthogonal signals. |
| First-class `cancelled` outcome (#92) | Candidate | A reputation-neutral `cancelled` / `cancelled-with-fee` SessionState + AttestationBundle outcome that honours a pre-agreed `cancellationPolicy` without it reading as an `aborted-by-self` fault. v0.1 makes `cancellationPolicy` informational-only; this would wire it through the §10.3.1 state machine and exclude it from the §10.5 fault denominator. Composes with the ST-3 "withdrawal is a right" framing. |
| Canonical rating-`dimensions` namespace (#96) | Candidate | A registered set of per-dimension rating keys (timeliness, communication, …) with a normative value range and a per-dimension `ReputationDerivation` metric, making dimension-level reputation a comparable cross-impl signal. v0.1 treats `dimensions` as opaque pass-through (RT rules, §10.6); this promotes it to load-bearing. |

## Cross-substrate & governance

| Item | Status | Notes |
|------|--------|-------|
| SR-3 / SR-4 wire-protocol harmonisation | Anticipated (v2) | v0.1 specifies SR-3 and SR-4 at the trust-property level only; cross-substrate sessions cannot complete for SR-3- or SR-4-dependent phases until wire formats are aligned (§5). |
| PA-2 → PA-3 multi-party governance | Anticipated | Constitution of a multi-party steward body to replace the single-signer recipe and rail registries (§11.2.6). |
| AML / Travel-Rule compliance-metadata hook | Candidate; design-issue first | An optional extension point carrying compliance metadata (e.g. a Travel-Rule flag) for flows that touch real money (fiat via AP2, stablecoins), so DACS is usable in regulated markets. Hook only — DACS does not itself perform AML. |

---

# Part 2 — Ecosystem & tooling (non-normative)

Builder-facing artifacts *around* the standard. None change the spec or conformance.
Welcomed as community contributions under the "contributor prototypes, steward owns
the standard" model; if an artifact proves solid the steward may designate it
canonical. Anything that **mirrors** the spec (a reference tool, a generated doc)
MUST generate from this repo — so it cannot drift from the source of truth — and
version-stamp which DACS version it reflects.

## Tooling

| Item | Status | Notes |
|------|--------|-------|
| DACS spec-reference MCP server | Anticipated (community) | Query the spec by rule/section, fetch artifact schemas (Listing, IdentityBundle, AgreementDocument, SettlementEvidence, AttestationBundle, …), list rule families (SE-*, HTLC-*, PC-*, RAV-*), pull the §14 conformance vectors. Read/search/fetch only. |
| DACS builder/validator MCP server | Anticipated (community) | Construct and verify bundles, run conformance vectors. Follow-on to the reference MCP; held until the reference implementation + §14 vectors stabilise so it doesn't harden against a moving API. |

## Documentation

| Item | Status | Notes |
|------|--------|-------|
| Operational builders guide | Anticipated | A practical integration guide distinct from the existing [why-DACS guide](./docs/builders-guide.md): capital / float requirements, escrow sizing, behaviour when undercapitalised mid-session, key custody / HSM practice, and settlement-finality integration. These are implementation/ops concerns — deliberately **not** normative spec material. |

## Reference implementations & test vectors

| Item | Status | Notes |
|------|--------|-------|
| `agent-commerce-demo` | Live | KyneSys Labs reference implementation; runs an end-to-end DACS-1 … DACS-5 session against Demos testnet. |
| `pathos-dacs-ref` | Live (third-party) | PATH-OS Labs' independent implementation (DACS-1 publisher, DACS-2 GLEIF verifier, DACS-5 envelope-receipt verifier CLI) — the empirical third-party-implementability evidence (§11.3). |
| §14 conformance test vectors | In progress | Machine-runnable vectors for the §14 conformance plan, so implementers can self-check. Grows as contributor work (e.g. DACS-X) produces cases. |
| Cross-substrate portability test | In progress | Demonstrate an unmodified `verifyBundle` end-to-end on a non-Demos substrate (a filesystem-backed SR-2 candidate has been exercised) — the artifact-level proof behind the §11.3 portability claim. |

---

## Out of scope (not roadmap)

- **DTR** — node-internal relay, below the DACS abstraction; no DACS-layer rail or parameter.
- **MCP (as a normative binding)** — agent-to-tool, not agent-to-agent commerce. It composes *adjacent* to DACS (tool discovery sits below DACS; an MCP server can expose a DACS catalog above it) without a normative binding in the standard. (A *spec-reference* MCP server is a separate, welcomed tooling item — see Part 2 → Tooling.)

---

*Have an item you think belongs here, or a substrate that ships the SR-1..SR-5
capabilities? See [CONTRIBUTING](./CONTRIBUTING.md).*
