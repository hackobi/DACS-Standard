# DACS — Demos Agent Commerce Standards

**Introduction and DACS-1 through DACS-5**

> Published as DACS **v0.1** — the first publicly released version. See [CHANGELOG](../CHANGELOG.md) for normative change history.

## About this document

This document specifies DACS — the Demos Agent Commerce Standards — across five per-stage standards: DACS-1 (Identify), DACS-2 (Vet), DACS-3 (Negotiate), DACS-4 (Settle), and DACS-5 (Verify). Shared material (terminology, substrate capabilities, the Demos production mapping, references) is presented once in the front and back matter rather than repeated per chapter. Each per-stage chapter contains the material specific to that stage. The companion DACS Dev Tasks working document is published separately and is **not** part of the standards.
**Normative language.** This document uses the RFC 2119 / RFC 8174 keywords **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL**, interpreted as in those RFCs. Keywords are normative only when in uppercase.
**Section numbering.** The front matter is numbered §1–§5 (prose introduction) followed by three lettered cross-cutting reference sections — **§A Demos production mapping**, **§B Global terminology** (claim references, anchoring/signing, shared phase-handler types, the closed registries, and the universal signature scheme §B.7), and **§C Composed open standards**. The five per-stage standards are then **Chapters 6–10** (DACS-1..5), with back matter in **Chapters 11–14**. The lettering of §A–§C deliberately keeps the foundational reference sections out of the chapters' §6/§7/§8 numbering namespace, so a citation such as §B.7 (the universal signature scheme) versus §7.7 (the DACS-2 composite verification record) is unambiguous.
**Versioning.** This document is **DACS v0.1**, the first publicly released version. Earlier drafts circulated internally under per-stage version numbers (DACS-1..5 v0.1, paper v0.7) and a brief v0.8 cut that consolidated review-pass revisions; those numbers are retired and reset to a common baseline. v0.1 is that baseline: all five per-stage standards plus the front-matter substrate-binding, the threat model, the glossary, and the conformance plan are published together at v0.1. From this baseline onward, each per-stage standard versions independently — a standard that gains capabilities bumps its own minor version (v0.2, v0.3, …) without forcing the others — through to v1.0, the version at which a standard is considered ready for unsupervised production use.

## Abstract

Autonomous agents are transacting with agents they have never met. Open standards exist for fragments of what a transaction requires — identity registries, payment authorisation, HTTP-layer micropayments, capability discovery — but each addresses one slice of the problem. Nothing in widespread use composes the fragments into a working commerce lifecycle, which is why agents that need the full lifecycle today fall back to closed operator marketplaces.
**DACS — Demos Agent Commerce Standards** — is the protocol Demos uses for agent commerce. It is organised around the five stages every agent-to-agent transaction passes through: **Identify, Vet, Negotiate, Settle, Verify.** For each stage, DACS composes with the existing standards that already work and adds new standards where the open ecosystem has gaps. Each new standard names the substrate capability it depends on. DACS is built for the Demos Network, but the capability-level specification is kept clean of Demos-specific dependencies so a substrate that provides the same capabilities can host a compatible implementation.

This document is the **normative reference** (Core + the five stage modules). A non-normative overview — the five-stage lifecycle, the nine-artifact spine, and a worked end-to-end example — is in the [Primer](../PRIMER.md); read it first if you are new to DACS.

## 1. The problem

An agent transacting with another agent today chooses between **pre-integrated bilateral trust** (works for small ecosystems, breaks at scale), a **closed operator marketplace** (scales, but the operator captures rents, controls access, and becomes a single point of trust), or **open standards** (the only path that scales without conceding a marketplace position — but only if a *complete lifecycle* exists). Today the open standards cover stages, not the lifecycle: a buyer can discover a seller, recognise its identity, and authorise a payment, but cannot, with open standards alone, (a) declare and verify a stakes-appropriate bundle of identity claims, (b) negotiate terms in private, or (c) produce an end-to-end session record the participants own. These gaps map to four of the five stages and are why institutional and regulated agents still fall back to operator marketplaces. DACS provides the lifecycle on a public, permissionless substrate — composing the standards that already work and filling the gaps that remain.

*The [Primer](../PRIMER.md) gives the full motivation (including why this matters now, and how DACS relates to AP2, x402, ERC-8004, ERC-8183, and A2A) plus a worked end-to-end example.*

## 2. The approach

DACS follows three principles.
**Composition.** Identity, payment, and several forms of credential attestation already have working standards with real adoption. There is no value in replacing them, and reinventing them slows everyone down. DACS uses composition, not replacement.
**Gap-filling.** Where there are real gaps, DACS specifies a new standard. New standards stay narrow in scope and are designed to compose cleanly with the rest of the stack.
**Stated substrate requirements.** Each new DACS standard names the substrate capability it depends on. The capability is the requirement, stated in the spec. Which substrate provides it is operational detail. This keeps DACS substrate-agnostic in specification while staying honest about what the new standards actually need underneath.
Three things follow:

- **Adopters keep what they already have.** A seller using existing identity, payment, and credential tooling does not abandon any of it to adopt DACS.
- **DACS is replaceable in parts.** If a better identity standard supersedes a pre-existing standard, the DACS standard referencing identity updates its pointers and the rest of the stack is unaffected.
- **DACS is substrate-portable in principle.** The substrate requirements are explicit. Any substrate that implements them can host a DACS implementation.

## 3. The five stages

Every agent-to-agent transaction, whether a $5 data lookup or a $5M institutional swap, passes through five stages:

- **Identify** — who is transacting, what is being offered, and how do they find each other.
- **Vet** — each party verifies the other’s claims against authoritative sources.
- **Negotiate** — parties arrive at agreed terms (price, scope, deadlines, deliverable spec) and commit to them.
- **Settle** — value is exchanged and the deliverable is provided.
- **Verify** — the complete transaction is anchored as an audit artifact; reputation is derived from it.

DACS is one standard per stage. Each standard either fully composes existing open standards for that stage, or specifies what is needed to close the gaps. Phase types specific to a stage (e.g. negotiate-rfq, pay-cross-chain-htlc) belong to that stage’s standard.

| Standard | Stage | Scope |
| --- | --- | --- |
| DACS-1 | Identify | Agent identity, signed and anchored service listings, discovery (.well-known/agent.json extension and off-chain catalog) |
| DACS-2 | Vet | Method-pluggable credential attestation against authoritative sources |
| DACS-3 | Negotiate | Private negotiation phases (RFQ, sealed envelope, fixed price), agreement commitment |
| DACS-4 | Settle | Payment rail registry, payment phases, delivery phases |
| DACS-5 | Verify | Session record, attestation bundle, reputation derivation |

The stages are sequential within a transaction. The standards are published together at the v0.1 baseline and version independently thereafter. Chapters 6–10 below specify them in detail.

## 4. Per-stage summary

A compact summary of what each stage composes, what it adds, and which substrate capabilities it depends on. Chapters 6–10 expand each row in full.

| Stage | Existing standards used | DACS additions | Substrate capabilities |
| --- | --- | --- | --- |
| Identify (DACS-1) | ERC-8004, W3C DIDs, A2A, authority and platform identifiers | Identity claim reference scheme; identity bundle schema; listing schema; .well-known extension; catalog API | SR-2; SR-1 optional |
| Vet (DACS-2) | W3C VC, TLSNotary, zkTLS | Method-pluggable recipe registry; proxy-attestation method for public-registry credentials; composite verification record | SR-2, SR-3 |
| Negotiate (DACS-3) | (none widely adopted) | Private negotiation phases; agreement commitment | SR-4 (private patterns), SR-2 |
| Settle (DACS-4) | AP2, x402, ERC-20, SPL, HTLC | Payment rail registry; payment and delivery phases (incl. Liquidity Tanks) | SR-2, SR-5 (cross-chain only) |
| Verify (DACS-5) | ERC-8004 reputation registry (publication surface) | Session record; attestation bundle; reputation derivation | SR-1, SR-2 |

Three stages compose substantially with existing standards (Identify, Vet, Settle). Two stages are gap-filled almost entirely (Negotiate, Verify). All five reference the same small set of substrate capabilities introduced in chapter 5.

## 5. Substrate capabilities

Every DACS standard names the substrate capability it depends on. The capabilities below are the complete set; each per-stage chapter cites a subset by ID.

| ID | Capability | Description | Used by |
| --- | --- | --- | --- |
| SR-1 | Cross-substrate identity aggregation | Optional. A composition primitive binding one root key to multiple sub-identities — per-substrate keys, verified Web2 identifiers, authority-issued identifiers, platform accounts — presented under a single signature. Cross-Context Identities (CCI) is the Demos implementation. | DACS-1, DACS-5 |
| SR-2 | Anchored, immutable storage | Content-addressed key-value storage with chain-anchored writes, suitable for signed documents up to a soft size limit. Storage Programs is the Demos implementation. | DACS-1, 2, 3, 4, 5 |
| SR-3 | Consensus-backed proxy attestation of HTTP responses | A substrate primitive that, given a fetch specification, returns a response signed by a consensus set of validators and anchors the attestation on chain at production throughput. DAHR (Data Agnostic HTTPS Relay) is the Demos implementation. | DACS-2 (one of several methods) |
| SR-4 | Identity-keyed private coordination channels | Private channels whose membership is bound to the substrate’s public-chain identity and whose contents stay between members. The public chain sees only commitments. L2PS (Layer-2 Privacy Subnets) is the Demos implementation. | DACS-3 (private negotiation patterns) |
| SR-5 | Multi-chain coordinated atomic settlement | Atomic settlement across substrates. May be provided by substrate-native cross-chain transactions, HTLC contracts on participating chains, or pre-funded liquidity primitives such as Liquidity Tanks on Demos. | DACS-4 (cross-chain settlement only) |

A substrate shipping all five can host a full DACS implementation. A substrate that ships some subset can host DACS partially: listings whose pipelines require unsupported capabilities are unfulfillable there, but the rest of the stack still works.
**Substrate-coupling status in v0.1.** SR-1, SR-2, and SR-5 are specified at the protocol level: another substrate that ships an equivalent primitive (cross-substrate identity aggregation; content-addressed anchored storage; atomic cross-chain settlement) can interoperate with DACS implementations on Demos at the artifact level (the bundles, listings, evidence records validate the same way). **SR-3 and SR-4 are specified at the trust-property level only in v0.1.** Two substrates each shipping their own SR-3 (consensus-backed proxy attestation) or SR-4 (identity-keyed private coordination) implementations will *not* be wire-protocol interoperable; the trust properties listed under CH-1..CH-6 for SR-4 and under §7.3.5 for SR-3 are the conformance bar v0.1 requires, but the underlying message formats and consensus signatures are substrate-specific. v2 of DACS-2 and DACS-3 is expected to specify wire formats for SR-3 attestation envelopes and SR-4 channel messages that enable cross-substrate interoperability; until then, a session begun on substrate A cannot be completed on substrate B if it uses any SR-3- or SR-4-dependent phase.
**Reference substrate.** The **Demos Network** is the substrate against which DACS was designed and, as of this draft, the only substrate that ships all five capabilities natively. The DACS specifications cite the substrate capabilities (SR-1 through SR-5), not the Demos primitives themselves; this separation keeps the artifact-level specification portable while staying honest about which primitives are concretely realised today and where v2 work is needed.

## A. Demos production mapping

A mapping of which substrate primitives are live today, what extensions are needed for v0.1, and which dependencies are third-party. The mapping applies to every per-stage standard — DACS-1 through DACS-5 — in this paper.
**Legend.** 🟢 in production today; 🟡 Demos team to add for v0.1; 🔵 third-party (composed, not built by Demos). This legend describes the substrate-primitive status — what the chain ships. Per-recipe and per-rail operational status uses the normative availability field defined in §7.4.5 (recipes) and §9.4.4 (rails). The legend here is informative about substrate features; availability there is normative about specific attestation paths and settlement rails. Earlier drafts conflated the two surfaces by extending this legend to recipes and rails; that conflation has been corrected in v0.1.

### A.1 SR-1 — Cross-Context Identities (CCI)

- 🟢 8 native contexts in production: xm, web2, pqc, ud, nomis, humanpassport, ethos, tlsn. Stored in GCRMain.identities. SDK methods getXmIdentities, getWeb2Identities, addXmIdentity, addTwitterIdentity, etc. SIWD (wallet_signIn, EIP-4361-style) for presentation.
- 🟡 6 new CCI contexts for regulatory identity: lei, finra-crd, sam-uei, fedramp, naics, cmmc. Each needs a GCR routine following the pattern of the existing 8 reference implementations.
- 🔵 ERC-8004 token references; W3C DIDs (carried via claim references; verified through DACS-2).

**Stor-backed credentials.** The stor-cred:<type>:<id> scheme convention is the extensibility surface for future credentials not yet promoted to native CCI contexts. **OFAC-clear is not a CCI context** — it is a per-session freshness check that lives only in DACS-2’s CompositeVerificationRecord (it is a check, not a stable identity claim).

### A.2 SR-2 — Storage Programs

- 🟢 StorageProgramData per SDK at kynesyslabs/sdks/src/storage/StorageProgram.ts. Content-addressed at stor-{sha256(…)}. 128 KB cap. JSONB-backed in GCR_Main.data. ACL modes (private/public/restricted). Provenance via createdByTx, lastModifiedByTx, interactionTxs.
- 🟡 Native multi-party Storage Program signature helper so buyer + seller co-signature of a closed AttestationBundle is a single transaction — current SDK supports owner-signed writes only.

**Logical vs native addresses (applies universally).** Throughout this document, addresses of the form dacs1:…, dacs2:…, dacs3:…, dacs4:…, dacs5:… are *logical* addresses: substrate-independent, human-readable, stable identifiers the protocol reasons about. Variable segments embedded in a logical address (e.g. the seller's primary claim, which itself contains colons) are delimiter-encoded per rule CF-4 (§6.3.4) so the logical string is unambiguously parseable back into its components on any substrate. Each substrate maps the logical address to its native addressing in one of two ways:

- **Pure mapping.** Where a substrate's native address is a pure function of the logical address, the mapping MUST be deterministic, one-to-one, and reversible, and consumers compute the native address directly from the logical pattern before reading.
- **Write-input mapping.** Where a substrate folds write-time inputs (deployer address, transaction nonce, salt) into its native address — as Demos's StorageProgram derivation does (§6.3.4) — the native address is **not** recomputable from the logical address alone. The implementation MUST then publish the logical→native binding: as descriptive metadata on the anchored record AND via the discovery surfaces (§6.3.5 well-known index, §6.3.6 catalog). Consumers resolve the native address through that published binding before reading.

In both cases implementations MUST anchor at the native address, the anchor transaction is the canonical pointer, and consumers MUST verify the content hash after dereferencing.

### A.3 SR-3 — DAHR (Data Agnostic HTTPS Relay)

- 🟢 Live via demos.web2.createDahr() → dahr.startProxy(…). Returns IWeb2Result with responseHash, responseHeadersHash, txHash. One on-chain web2Request tx per call. GCR routines per CCI context handle native-claim validation (including tlsn).
- 🟡 DAHR signing-model clarification — current docs show **hash commitments only**, with no validator signature over the response body. v0.1 treats this as a **consensus-anchored hash commitment** model. If Kynesys upgrades DAHR to validator-sign the response body itself, DACS-2 v0.2 may strengthen the claim.
- 🟡 CompositeVerificationRecord Storage Program schema.
- 🟡 oauth-attested method depends on a Demos-side OAuth attester. If not built, the method is 🔵 third-party.
- 🔵 W3C Verifiable Credentials, TLSNotary (external proof library — distinct from the 🟢 cci-tlsn:* native context), zkTLS (Reclaim, Pluto), ACME challenges for domain-tls-control.

### A.4 SR-4 — L2PS (Layer-2 Privacy Subnets)

- 🟢 new l2ps.L2PS() / new l2ps.L2PS(rsaPrivateKey). DemosWork orchestration with WorkStep (id, context, content, output, depends_on, critical), BaseOperation, ConditionalOperation (SDK module @kynesyslabs/demosdk/demoswork). Storage Programs for agreement-hash anchoring and sealed-envelope commitments.
- 🟡 CCI-keyed L2PS membership — bind subnet membership to CCI primary claim so channel signatures map to the same identity that holds value on-chain. Current API is RSA-key-based.
- 🟡 L2PS channel message envelope API — sequence numbering, signature export, transcript export.
- 🟡 Encrypted transcript anchoring helper (for terms.transcriptDisclosurePolicy: "encrypted-anchored-required").
- 🔵 ERC-8183 escrow primitive (Ethereum, draft); institutional RFQ desks’ off-chain systems composed as L2PS-equivalent transport.

**DACS-3 phase types are realised as DemosWork WorkSteps.** Each negotiation pattern compiles to a sequence of WorkSteps with context: "xm" | "web2" | "native" and DACS-defined content shapes.

### A.5 SR-5 — Native Bridges / Liquidity Tanks

- 🟢 LiquidityTank.sol (audited; 600+ lines; rotating 2/3 multisig + 15-day emergency recovery) deployed on **ETH Sepolia** (0x7AE3A8B899BE0D9E9de51b81a9912C0CEE128d88) and **Polygon Amoy** (0x57cA16EeE7fbeC69BFD46E4806B5d91e173dd600).
- 🟢 SDK type BridgeOperation at kynesyslabs/sdks/src/bridge/nativeBridgeTypes.ts. RPC handler at kynesyslabs/node/src/libs/network/manageNativeBridge.ts. Tank addresses config at kynesyslabs/node/config/tankAddresses.json. **bridge_id** (16-char hash) is the canonical end-to-end tracking handle.
- 🟢 Trust model: **operated by a rotating Demos validator shard under 2/3 BFT multisig with 15-day deployer emergency recovery.** Not "no operator" — the operator is the substrate itself.
- 🟢 MVP scope: USDC only; EVM-source; unidirectional. Gasless bridge operations (contract reimburses user gas from subsidy pool). BridgeOperation.status lifecycle: "empty" → "pending" → "completed" | "failed". XM SDK single-chain transfers (preparePay, prepareTransfer, prepareTransfers) for non-bridge rails. Storage Programs for deliver-storage-program and entitlement records.
- 🟡 Phase 2: Solana tank programs (treasury Phases 3.3–3.4, SolanaAddressManagement class, vault management).
- 🟡 Phase 3: Bidirectional + cross-chain shard rotation.
- 🟡 Phase 4: Production polish + executeBridgeOperations consensus logic + cross-chain bridge message verification + emergency recovery mechanisms. Additional EVM tank deployments (currently 4 placeholder entries in tankAddresses.json). Mainnet deployments. Non-USDC stablecoin support. Native EntitlementRecord registry (optional; Stor-backed is fine for v0.1).
- 🔵 AP2 (Google → FIDO Alliance, April 2026) — DACS-4 carries as a rail envelope. x402 (Coinbase + Cloudflare + Anthropic) — DACS-4 carries as a rail envelope. Rubic Bridge (third-party DEX aggregator, wrapped by SDK at @kynesyslabs/demosdk/bridge) — alternative cross-chain rail with explicit third-party trust disclosure.
- 🔵 **HTLC contracts (generic atomic-swap pattern)** — pay-cross-chain-htlc is a first-class supported rail in DACS-4 v0.1. **The reference implementation in agent-commerce-demo uses HTLCs today for the fx-rfq cross-chain settlement** (929 LOC: real Solana Anchor program + Base Sepolia EVM HTLC contract; lock/reveal/refund implemented end-to-end). This predates Native Bridges Phase 1 deployment. The reference implementation will migrate to pay-cross-chain-liquidity-tank as Phase 1 stabilises; until then both rails are documented honestly. ERC-20, SPL (standard token interfaces). ERC-8183 escrow (proposed; future rail).

**v0.1 cross-chain settlement scope.** pay-cross-chain-liquidity-tank is supported **only** for the rails currently live in tankAddresses.json (ETH Sepolia, Polygon Amoy; USDC; unidirectional EVM source). All other tank rails in the registry are 🟡 to-add and will unlock as Native Bridges Phase 2–4 ship. pay-cross-chain-htlc is the path the reference implementation runs today; v0.1 keeps both first-class.

## B. Global terminology

Terms used in more than one per-stage chapter are defined here once. Per-stage chapters define only terms unique to that stage.

### B.1 Claim references and identity

- **Claim.** A fact a party asserts about itself (e.g., "this agent’s FINRA CRD is 12345").
- **Claim reference.** A typed identifier referring to the external system that authoritatively holds a claim. The reference is of the form <scheme>:<identifier>[?<parameters>]. Grammar and v0.1 registry defined in chapter 6 (DACS-1).
- **ClaimReference (type).** The typed equivalent of a claim reference used in JSON schemas throughout the spec.
- **Primary identity claim.** The claim within a bundle that serves as the canonical identifier of the party for reputation, audit, and addressing purposes. Determined by the presentedBy field of the bundle and the primaryClaimSelector of the requirement.
- **Identity bundle.** An ordered set of claims a party presents about itself, each independently verifiable, plus a presentation signature. Full schema in chapter 6 (DACS-1).

### B.2 Anchoring and signing

- **Anchored.** Stored on the substrate such that an anchor reference (substrate-native pointer plus content hash) is sufficient for any party with substrate access to retrieve the canonical content and verify integrity. Realized by SR-2.
- **Signed.** Carrying an Ed25519 (or equivalent) signature over the RFC 8785 canonical-JSON serialisation of the document’s signed scope, where the signed scope is all fields except the signature field itself.
- **Canonical form.** RFC 8785 JSON Canonicalization Scheme (JCS) serialisation of the document with the signature(s) field omitted.
- **Content hash.** sha256 hex of the canonical form.
- **Numeric safe-integer constraint.** RFC 8785 JCS defines a canonical serialisation only for JSON numbers within the IEEE-754 double range; integers above 2^53−1 (9,007,199,254,740,991) have no reproducible canonical form. Therefore every JSON number in a signed or content-hashed DACS document MUST lie within the IEEE-754 double safe-integer range. Any quantity that may exceed it (token IDs, uint256 values, large on-chain counters or block numbers) MUST be carried as a decimal string (or, where ABI conventions apply, a `0x`-prefixed hex string) rather than a bare JSON number, so that its canonical form and content hash are reproducible across serializers. Producers MUST NOT emit, and readers SHOULD reject, a signed or content-hashed document containing a JSON number outside this range.
- **Unicode normalisation (rule CF-1).** RFC 8785 JCS performs no Unicode normalisation — it preserves whatever code points are present. Therefore, before computing the canonical form, every JSON string value in a signed or content-hashed DACS document MUST be Unicode-normalised to NFC. Both producers and verifiers MUST apply NFC at this stage, so the canonical form, content hash, and signatures are reproducible across implementations regardless of the input's precomposed/decomposed form. Most DACS string fields are ASCII, for which NFC is a no-op; this rule binds the non-ASCII surface (e.g. `cci-ud`, `cci-web2` usernames, `domain:` identifiers). This lifts the per-field NFC requirement on `Identifier` (§6.3.1) into a single normative pre-hash step covering the whole signed scope.
- **Canonical decimal (rule CD-1).** RFC 8785 JCS canonicalises JSON *numbers* but preserves *string* bytes verbatim — and monetary amounts are carried as strings — so two parties formatting the same economic value differently (e.g. `"1.50"` vs `"1.5"`) would otherwise produce different bytes, hashes, and signatures. Every `PriceTerm.amount` string MUST be in minimal-digit canonical decimal form: no leading zeros (except a single `0` before the decimal point); no trailing zeros after the decimal point; `.` as the only separator; no `+` sign; no exponent. Producers MUST canonicalise `amount` per CD-1 before computing any agreement hash, `SettlementEvidence` hash, or other JCS hash; verifiers MUST canonicalise `amount` per CD-1 before any price-band or price-equality comparison. Two parties formatting the same value differently MUST therefore reproduce identical canonical bytes, hashes, and signatures.

### B.3 Verification and evidence

- **Verification reference.** A reference to a DACS-2 VerifyResult that attests a claim against its authority.
- **AttestationRef.** A reference to an anchored attestation: anchor locator + content hash + (optional) signer. Defined in chapter 7 (DACS-2).
- **VerifyResult.** The uniform record produced by every DACS-2 verification method. Defined in chapter 7.
- **VerifyResultRef.** A reference to an anchored VerifyResult: anchor + contentHash + recipeVersion (recipeVersion is load-bearing for staleness checks).
- **Composite verification record.** The anchored document produced by the vet-credentials phase, aggregating freshness checks, supplementary signals, and deal-specific claims. Defined in chapter 7.

### B.4 Session, pipeline, and phases

- **Listing.** A signed, anchored JSON document conforming to chapter 6; the canonical contract for a transaction.
- **Pipeline.** The ordered sequence of PhaseStep entries declared in a listing.
- **Phase / PhaseStep.** A single unit of work in the pipeline; kind names a closed set defined across DACS-2..5.
- **Session.** A per-transaction lifecycle from Identify through Verify.
- **Session record.** The live state document for an active session. Held off-chain by the orchestrator; the bundle is the on-chain artifact. Defined in chapter 10 (DACS-5).
- **Attestation bundle.** The frozen end-of-session artifact, anchored via SR-2. The audit unit. Defined in chapter 10.
- **Agreement document.** The canonical signed JSON document produced by a negotiation pattern. Defined in chapter 8 (DACS-3).
- **SettlementEvidence.** The uniform record produced by every DACS-4 payment and delivery phase. Defined in chapter 9.

### B.5 Shared phase-handler types

Every phase handler in the stack consumes a SessionContext and returns a PhaseHandlerResult. The full TypeScript declarations:

```
type SessionContext = {
  jobId: string
  listingRef: { listingId: string; version: number; contentHash: string }
  recipeRegistryVersion: number             // DACS-2 registry pinned at session start
  railRegistryVersion: number               // DACS-4 registry pinned at session start
  parties: SessionParty[]
  priorPhaseOutputs: Record<string, unknown> // accumulated contextDelta from completed phases
  signer: SubstrateSigner                   // substrate-specific signing capability
  startedAt: number                         // unix ms
}
type PhaseHandlerResult = {
  ok: boolean
  reason?: string                           // when !ok
  txRefs?: ChainTxRef[]                     // chain references produced by this invocation
  explorerUrls?: string[]                   // human-readable handles, parallel to txRefs
  contextDelta?: Record<string, unknown>    // merged into SessionRecord.PhaseEntry.contextDelta
  attestationRef?: AttestationRef           // anchored evidence reference
  errorClass?: "permanent" | "transient" | "counterparty" | "substrate" | "settlement-atomicity"
}
```

Conformance: phase handlers MUST accept a SessionContext and return a PhaseHandlerResult. On ok: true the orchestrator merges contextDelta into the corresponding PhaseEntry and records txRefs in the session event log; on ok: false the orchestrator classifies the failure per errorClass and applies the retry policy in chapter 10.

### B.6 Closed registries — v0.1 scope

The v0.1 set of identity schemes (DACS-1), verification methods (DACS-2), negotiation patterns (DACS-3), payment phases (DACS-4), and delivery phases (DACS-4) are **closed**. New entries are added in subsequent minor versions of the relevant standard via the governance process in chapter 11. Implementations MAY support pre-standard "experimental" entries prefixed x-; these MUST be treated as unknown by conforming readers unless out-of-band agreement exists.

### B.7 Universal signature scheme — domain-separated signing

Every signature in DACS — across DACS-1 (listings, revocations), DACS-2 (VerifyResults, composite records, recipes), DACS-3 (channel messages, agreements, commitments), DACS-4 (settlement evidence, amendments, rails, entitlements), and DACS-5 (bundles, ratings) — MUST be computed over a domain-separated payload. The domain separator prevents cross-protocol signature replay: a signature produced under one artifact kind MUST NOT validate as a signature under any other artifact kind, even when the underlying hash bytes coincide.
The canonical payload to be signed is:

```
signed_bytes := domain_separator || artifact_hash

domain_separator := "dacs-" || artifact_kind || ":v" || version_tag || ":"

artifact_hash    := the sha256 hex of the RFC 8785 canonical form of the

                    signed document, with the signature field(s) omitted
```

**`version_tag` binding.** `version_tag` is the **major** version of the per-stage standard that defines the artifact kind. All minor versions within a major (v0.1, v0.2, …) share the same `version_tag`; only a major break (v1 → v2) bumps it. The v0.1 registry below therefore uses `:v1:` for every kind and stays frozen across the independent per-stage minor versioning of §11.1.2 — a DACS-2 v0.2 VerifyResult still signs under `dacs-verifyresult:v1:`. (Forward-readability of signed artifacts across a minor bump is what SIG-5 below guarantees.)

The v0.1 registry of domain separators is closed:

| Artifact | Domain separator | Defined in |
| --- | --- | --- |
| DACS-1 listing | "dacs-listing:v1:" | §6.3.4 |
| DACS-1 listing revocation marker | "dacs-revocation:v1:" | §6.3.4 |
| DACS-1 identity bundle presentation | "dacs-bundle-presentation:v1:" | §6.3.2 |
| DACS-2 VerifyResult | "dacs-verifyresult:v1:" | §7.5 |
| DACS-2 composite verification record | "dacs-composite:v1:" | §7.7 |
| DACS-2 recipe | "dacs-recipe:v1:" | §7.4 |
| DACS-3 channel message | "dacs-channelmsg:v1:" | §8.3.3 |
| DACS-3 agreement | "dacs-agreement:v1:" | §8.5 |
| DACS-3 commitment record | "dacs-commitment:v1:" | §8.6 |
| DACS-3 channel transcript | "dacs-transcript:v1:" | §8.7 |
| DACS-4 settlement evidence | "dacs-evidence:v1:" | §9.7 |
| DACS-4 settlement amendment | "dacs-amendment:v1:" | §9.7.1 |
| DACS-4 rail definition | "dacs-rail:v1:" | §9.4 |
| DACS-4 entitlement record | "dacs-entitlement:v1:" | §9.6.2 |
| DACS-5 attestation bundle | "dacs-bundle:v1:" | §10.4.1 |
| DACS-5 rating record | "dacs-rating:v1:" | §10.6 |
| DACS-1 bundle session-key root binding | "dacs-session-binding:v1:" | §6.3.2 |
| DACS-3 auto-accept commitment | "dacs-auto-accept-commitment:v1:" | §8.4.1 |
| DACS-3 auto-accept instance | "dacs-auto-accept-instance:v1:" | §8.4.1 |

**Payload shape — single-hash vs composite.** Most artifacts use the single-hash payload `domain_separator || artifact_hash`. Three entries are *composite-payload* separators that, by design, prepend the separator to more than one framed value rather than a single artifact hash: `dacs-session-binding:v1:` (`|| session_key || bundle_hash`, §6.3.2), `dacs-auto-accept-commitment:v1:` (`|| sha256(canonical(commitment))`, single-hash), and `dacs-auto-accept-instance:v1:` (`|| agreementHash || autoAcceptCommitmentHash`, §8.4.1). For composite-payload separators each appended value MUST be a fixed-length hex sha256 digest (or, for `session_key`, the fixed-length hex public key) so the concatenation is unambiguously parseable; this is the sanctioned exception to the single-`artifact_hash` shape and these separators are first-class registry entries, not `dacs-x-` extensions.

**Commitment-hash domain tags.** The table above registers *signature* domain separators (SIG-1 scopes to signatures). One further `dacs-*:v1:` tag is a **commitment-hash** domain, not a signature payload: `dacs-sealed-bid:v1:` (the sealed-envelope bidHash preimage `sha256("dacs-sealed-bid:v1:" || sha256(canonical_JCS(bid)) || salt)`, §8.4.3). It follows the same domain-separation discipline (preventing cross-use of the hash) but is NOT a signature `signed_bytes`, so SIG-1 and the "sign every artifact kind" conformance do not apply to it; it is the one sanctioned commitment-hash domain tag in v0.1.

**Conformance.** (SIG-1) Every signature in DACS v0.1 MUST be computed over the appropriate domain-separated payload from the table above (single-hash or composite per the note above). (SIG-2) Verifiers MUST reconstruct the domain separator and artifact hash(es) independently and MUST NOT trust either supplied as-is by a counterparty. (SIG-3) Signatures whose payload computation cannot be reproduced exactly MUST be rejected. (SIG-4) An artifact kind not in the v0.1 table MUST use a domain separator of the form "dacs-x-" || kind || ":v" || version || ":" until accepted into a future version of the registry. (SIG-5) **Preserve-unknown.** A verifier MUST reconstruct the signed payload (canonical form and artifact hash) over the document **as received**, including any fields it does not recognise. It MUST NOT strip, drop, or otherwise omit unrecognised fields before recomputing the canonical form — doing so changes the hash and would reject a validly-signed document produced under a later minor version. A verifier MAY ignore the *meaning* of unknown fields but MUST include their bytes in the hash. This is what makes the "forward-readable shapes" guarantee of §11.1.2 hold for signed artifacts: an older verifier can still verify a newer minor version's signature, interpreting only the fields it knows.
**Algorithm.** The signing algorithm itself (Ed25519, ECDSA-secp256k1, or sr1-aggregate) is independent of the domain-separation rule. The domain separator is prepended to the signed bytes regardless of algorithm. Implementations MUST NOT compute a signature over the artifact hash without the separator and MUST NOT compute a signature over the canonical form directly (always over the prepended-separator-then-hash payload). `artifact_hash` MUST be the lowercase hex string of the sha256 digest; the `domain_separator` (a UTF-8 string) and `artifact_hash` (an ASCII hex string) are concatenated as UTF-8 byte sequences with no separator byte.

## C. Composed open standards

DACS composes with the following open standards. Each per-stage chapter cites the relevant entries by name; backwards-compatibility implications are stated per-stage.

| Standard | Composed by | Touchpoint |
| --- | --- | --- |
| ERC-8004 Trustless Agents | DACS-1, DACS-5 | Identity scheme; optional reputation publication surface |
| ERC-8183 Job Escrow (proposed) | DACS-4 | Future rail (v0.2) |
| W3C DIDs v1.0 | DACS-1 | Identity scheme |
| W3C Verifiable Credentials Data Model 2.0 | DACS-2 | verifiable-credential method |
| AP2 Agent Payments Protocol | DACS-4 | pay-ap2 rail envelope (FIDO Alliance custodian from April 2026) |
| x402 HTTP 402 revival | DACS-4 | pay-x402 rail envelope |
| A2A .well-known/agent.json | DACS-1 | Discovery extension |
| TLSNotary (PSE rebuild, 2024) | DACS-2 | tlsnotary method (distinct from native cci-tlsn context) |
| Reclaim Protocol / Pluto zkTLS | DACS-2 | zktls method |
| HTLC contracts (generic) | DACS-4 | pay-cross-chain-htlc; used by the reference implementation today |
| ERC-20 / SPL | DACS-4 | pay-evm-erc20 / pay-solana-spl |
| ACME / RFC 8555 | DACS-2 | domain-tls-control method |

## Document map

DACS v0.1 is published as a Core document plus one module per stage. Chapter numbers are retained across the split.

| Document | Contains | Chapters |
| --- | --- | --- |
| [PRIMER](../PRIMER.md) | non-normative overview + worked example | — |
| **CORE** (this doc) | framing (§1–5), Demos mapping (§A), shared terminology & types & signatures (§B), composed standards (§C), governance (§11), threat model (§12), glossary (§13), conformance frame (§14) | 1–5, 11–14 |
| [DACS-1-IDENTIFY](DACS-1-IDENTIFY.md) | identity, listings, discovery | 6 |
| [DACS-2-VET](DACS-2-VET.md) | verification methods, recipes, vet phase | 7 |
| [DACS-3-NEGOTIATE](DACS-3-NEGOTIATE.md) | channels, negotiation patterns, agreement commit | 8 |
| [DACS-4-SETTLE](DACS-4-SETTLE.md) | rails, payment & delivery phases, settlement evidence | 9 |
| [DACS-5-VERIFY](DACS-5-VERIFY.md) | session record, attestation bundle, reputation | 10 |
| [PROFILE](PROFILE.md) | the v0.1 version set | — |

A cross-reference to §6.x lives in DACS-1, §7.x in DACS-2, §8.x in DACS-3, §9.x in DACS-4, §10.x in DACS-5; everything else is in this Core document.

## Chapter 11 — Stewardship, versioning, follow-on

### 11.1 Stewardship and versioning

#### 11.1.1 Current steward

DACS v0.1 is stewarded by **KyneSys Labs**. This means: the registry signing key currently used to sign recipes (DACS-2) and rail definitions (DACS-4) is held by KyneSys Labs; the canonical anchored addresses for those registries are written by KyneSys Labs; spec changes between minor versions are reviewed and merged by KyneSys Labs. This is a single-steward arrangement — phase PA-2 in the progressive-anchoring scheme defined in §7.4.4. It is **not** the long-term governance target; it is the honest description of where v0.1 sits at time of publication.
Multi-party governance — a constituted working group, formal multi-signature schemes for the registries, sub-authority delegation by domain (sanctions lists, financial regulation, settlement rails) — is open work. v0.1 ships under single-steward semantics so the standard can move forward; transitioning to a multi-party arrangement is anticipated as the ecosystem of implementers, reviewers, and operators grows. The PA-2 → PA-3 transition (§7.4.4) is the formal anchor point for that change.
**(GOV-1)** Implementations consuming the registries MUST disclose to their users which signing key they treat as authoritative and MUST NOT misrepresent the current steward as a constituted multi-party body. Third-party implementations (such as PATH-OS Labs’ reference) MAY operate against the same canonical registries; the steward arrangement governs who writes the registries, not who reads them.

#### 11.1.2 Versioning

DACS v0.1 is a common baseline: all five per-stage standards, the front-matter substrate-binding, the threat model, the glossary, and the conformance plan are published together at v0.1, the first publicly released version. From this baseline onward each per-stage standard versions independently — a standard that gains capabilities bumps its own version without forcing the others, and a pipeline composes a coherent set of per-stage versions. Within a standard, major versions (v1, v2, …) break compatibility; minor versions (v0.2, v0.3, …) add capabilities while preserving forward-readable shapes. v0.1 freezes the registries (claim schemes in DACS-1, methods/recipes in DACS-2, patterns in DACS-3, rails in DACS-4) as an immutable baseline; later additions happen via minor-version registry updates released by the current steward, **appended to the same registry-index document** (`dacs2:registry:v0.1` / `dacs4:registry:v0.1`). That index address is the registry's **major-version line**: the `:v0.1` suffix denotes the v0.x line, not a content snapshot — the index document grows additively across minor versions and is re-addressed only on a major (v1 → v2) bump. A consumer therefore always resolves the same address and sees every v0.x entry; "frozen at v0.1" means the original baseline entries are immutable (never mutated in place), not that the index stops growing. Each entry carries its own `recipeVersion` / `railVersion` for per-session pinning (§7.4.3 / §9.4.3). v1.0 is the version at which a standard is considered ready for unsupervised production use.

#### 11.1.3 Conformance philosophy

Each spec’s conformance section enumerates the requirements an implementation must satisfy to claim conformance to that spec. Cross-spec conformance (a full DACS-1…DACS-5 implementation) is the conjunction of per-spec conformance for every spec the implementation covers. Implementations MAY cover a strict subset (e.g., DACS-1 + DACS-4 only, for a payment-rail aggregator that does not negotiate or rate); conformance is then to the implemented subset.

#### 11.1.4 Substrate stance

DACS does not standardise the substrate. The substrate-capability statements (SR-1 through SR-5) are the abstract contract. Any substrate that provides them can host a compatible implementation. Demos is the substrate against which DACS was designed and ships all five capabilities natively; other substrates (Ethereum L1+L2 stack with bridges, Polkadot, Cosmos with privacy zones) MAY satisfy varying subsets and host correspondingly varying DACS subsets. SR-1, SR-2, and SR-5 are protocol-specified; SR-3 and SR-4 are trust-property specified in v0.1, with wire-protocol harmonisation expected in v2.

#### 11.1.5 Composition stance

DACS composes with the existing open ecosystem and does not seek to replace standards that already work. Where existing standards have gaps relevant to agent commerce (negotiation patterns, end-to-end audit), DACS specifies new standards as narrowly as possible, with explicit substrate dependencies. The composed-standards table in §C is the comprehensive list of touchpoints; when an underlying standard updates, the corresponding DACS standard’s registry entry updates in the next minor version.

### 11.2 Follow-on topics

Seven areas are deliberately out of scope for v0.1 and intended for subsequent standards.

#### 11.2.1 Dispute resolution (DACS-X, anticipated)

v0.1 produces signed, anchored bundles. v0.1 does not specify what happens when parties disagree about a bundle’s contents, contest a settlement amendment, or wish to invoke an arbitrator. A follow-on standard (working name DACS-X) is anticipated to: specify a dispute initiation phase referencing one or more bundles; specify selective transcript disclosure protocols (revealing channel transcripts to a named arbitrator under signed party agreement); specify arbitrator credentialing patterns (likely composing DACS-1 + DACS-2 — arbitrators are agents with verified credentials); specify dispute outcome bundles that supersede or annotate the original session bundles.

#### 11.2.2 Open phase set

v0.1’s phase types are closed across DACS-2/3/4/5. v2 may relax this to permit ecosystem-defined phases under the steward’s oversight. Until then, x- experimental phases provide an escape valve for out-of-band agreement.

#### 11.2.3 Multi-party transactions beyond bilateral

v0.1 negotiation is bilateral (except sealed-envelope, which is one seller / many bidders). True multi-party transactions — syndicated trades, multi-seller bundles, escrow-with-arbitrator three-party flows — are out of scope. DACS-3 v0.2 will likely add a negotiate-multi-quote pattern; truly multi-party flows are likely v2 territory.

#### 11.2.4 Streaming / continuous-flow rails

v0.1 rails are discrete-transaction. Streaming payment rails (Sablier-style, payment per second of usage) and continuous-delivery rails (per-second compute, per-byte data feed) are out of scope. A future DACS-4 v0.2 entry (rail type continuous) is anticipated.

#### 11.2.5 Cross-DACS-version compatibility

Each per-stage standard specifies forward-compatibility within itself (a later-minor reader handles earlier-minor bundles of the same standard). Cross-version compatibility (a DACS-1 v2 listing pipelined against a DACS-3 v0.1 negotiator) is deferred; pipelines MUST currently use a coherent set of per-stage versions.

**v0.1 version-signalling scope.** Every anchored artifact carries a `*Version` literal (`dacsVersion`, `bundleVersion`, `agreementVersion`, `evidenceVersion`, `ratingVersion`, `resultVersion`) that records the **major** version only; in v0.1 these are all `"1"`. The listing-validation "dacsVersion supported" gate (§6.3.4 step 2) is therefore a **major-version** check in v0.1 — meaningful against a future major (v2) break, but not minor-discriminating. Two things are consequently **not** signalled in v0.1 and are roadmapped: (a) a per-artifact **producing-minor-version** field, which a reader would need to select an era-specific decode path (the later-reads-earlier direction is already handled for signed artifacts by SIG-5 preserve-unknown + "forward-readable shapes"); and (b) the **older-reader-newer-minor** direction (an older reader encountering a higher-minor artifact) — undefined in v0.1. Since v0.1 is the single published baseline, neither bites today; both land with the cross-version compatibility work above.

#### 11.2.6 Multi-party governance and registry stewardship

The transition from single-steward (PA-2) to multi-party constituted governance (PA-3) for the recipe and rail registries is itself follow-on work. v0.1 does not specify the constitution mechanism, multi-signature thresholds, sub-authority delegation, or transition procedure. These are open questions for the working group that the ecosystem chooses to constitute. Until that body exists, the current steward operates under the disclosure rules in §11.1.1.

#### 11.2.7 Selective-disclosure / minimised-claim presentation

v0.1 discloses a presented bundle's full `claims[]` set and its `presentedBy` primary claim to every counterparty (§6.3.2 scope note). The DACS-2 zkTLS / TLSNotary methods hide the secret inside a claim's verification but not which claims a party holds. A follow-on standard is anticipated to add bundle-layer selective disclosure — per-claim blinding, commitments with selective open, proof-of-possession-without-disclosure, and an unlinkable or rotating primary-claim presentation that preserves reputation continuity without exposing the durable high-tier identity in low-stakes interactions. Until then, the only minimisation is presenter-side bundle pruning, with the linkability caveat in §6.3.2.

### 11.3 Closing

Agent commerce is moving from prototype to production. DACS is a contribution toward keeping the lifecycle on public infrastructure: a stack that composes with the existing open standards where they work, fills the gaps where they don’t, and makes substrate dependencies explicit. A reference implementation runs the lifecycle end-to-end on the Demos substrate; an independent third-party reference implementation (PATH-OS Labs’ pathos-dacs-ref) implements the DACS-1 + DACS-2-GLEIF + DACS-5 verifier subset against the same spec.
What this document is **not**: a finished standard ready for unsupervised production at every scale. The honest list of remaining work — beyond the per-stage follow-on topics in §11.2 — includes: protocol-level wire specifications for SR-3 and SR-4 (currently trust-property specified only); expansion of independent reference-implementation coverage beyond the current third-party verifier; engagement with the maintainers of every composed standard (ERC-8004, AP2 via FIDO Alliance, W3C VC, A2A) to convert "DACS composes with X" from a unilateral claim into a documented cross-maintainer conversation; a unified threat-model audit (§12) reviewed by parties outside the current stewardship; constitution of multi-party governance (§11.2.6); and conformance test suites (§14) ready for implementers to run against.
Some of these will reveal gaps that need new work, not just refinement. The intent of v0.1 is to ship a coherent baseline that the next 6–12 months of implementation experience and ecosystem engagement can sharpen. It is not the final word on agent commerce.

## Chapter 12 — Unified threat model

This chapter collects, partitions, and rationalises the per-chapter security considerations into a unified threat model. It is the artifact a security review would start from. Where this chapter restates per-chapter threats, the per-chapter mitigation is normative; this chapter’s framing is informative.

### 12.1 Scope and non-goals

DACS’s security goals are: (a) cryptographic non-repudiation of every per-session artifact (listings, bundles, agreements, evidence) by the parties that produced them; (b) tamper-evident audit trail — any modification of an anchored artifact is detectable by content-hash comparison; (c) limited-trust substrate dependency — the substrate is trusted for liveness and consensus per its own security model, not for application-layer semantics; (d) prevention of cross-protocol signature confusion via the universal domain-separation scheme in §B.7; (e) prevention of replay across sessions via per-session jobIds, nonces, and content hashes; (f) substrate-failure isolation in reputation derivation so substrate outages do not damage party reputations.
Non-goals: DACS does **not** prevent collusion between buyer and seller (two parties who jointly fabricate a session produce a valid session; the audit trail records what they say happened, not what objectively happened). DACS does **not** prevent denial-of-service by a counterparty or by the substrate (it produces evidence of the failure for reputation purposes, but does not guarantee progress). DACS does **not** prevent regulatory non-compliance — it produces artifacts useful for compliance audit but does not enforce any specific regulatory regime. DACS does **not** provide unconditional privacy — the SR-4 channel contents stay between members, but member identity and timing of commitments are visible on the public chain by design. **This visibility extends to the audit layer**: anchored DACS-5 bundles, commit-agreement records, and DACS-2 vet attestations carry party **primary claims — durable authority-issued identities (LEI, FINRA-CRD, …) — in cleartext at derivable addresses**, so a passive observer can reconstruct the **counterparty graph** (who transacted with whom, correlatable across every session an identity runs) with **no cryptography to break**, and can read each vet attestation's `scheme:identifier:decision` (e.g. "party X was screened against OFAC → clear"). DACS accepts this by design — it is an *accountability* standard, and a public, verifiable audit trail necessarily exposes the relationship. (Raw private *values* behind a verification are separately protected by the §7.5 public-anchor data-minimisation rule; only predicate outcomes are exposed.) A confidentiality layer that anchors these records **encrypted to the parties** while keeping the content hash public for tamper-evidence is roadmap work, not v0.1.

### 12.2 Adversary model

The threat model assumes adversaries with the following capabilities; per-threat mitigations specify which class is being defended against.

| Adversary class | Capabilities | Assumed not capable of |
| --- | --- | --- |
| Network observer | Reads all public-chain traffic; can perform timing analysis on commitments; **can reconstruct the counterparty graph from anchored bundles / commit-agreement records / vet attestations (cleartext primary claims at derivable addresses) and read each vet attestation's scheme:identifier:decision**; cannot read private-channel contents. | Breaking standard cryptographic primitives (sha256, Ed25519, ECDSA-secp256k1 under standard assumptions); recovering the raw private values behind a verification (predicate-outcome-only under §7.5 minimisation). |
| Network active attacker | Can drop, delay, reorder, or inject messages on transport links; can MITM TLS sessions if PKI is compromised. | Forging signatures by valid private keys; producing sha256 preimages. |
| Malicious counterparty | Operates a fully-conformant DACS implementation but maximises self-interest within the protocol; signs everything they’re willing to be held to and refuses to sign anything else. | Forging the other party’s signatures; controlling validator-set consensus on the substrate. |
| Compromised authority | A registry authority (GLEIF, FINRA, OFAC, etc.) returns false data, either by deliberate compromise or by API corruption. | Forging substrate-validator signatures over the false response (validators sign the fetch result, not the data’s factuality). |
| Substrate validator-set minority | A minority of substrate validators is compromised; the consensus protocol’s normal Byzantine bound holds. | Producing valid consensus signatures on falsehoods (assuming the BFT assumption holds). |
| Substrate validator-set majority | A majority of substrate validators is compromised. | (none — above the substrate’s security floor; DACS inherits the failure.) |
| Substrate operator (rotating shard) | For Liquidity Tank-style SR-5: the rotating validator shard operating tanks is partially compromised within its multisig threshold. | Bypassing the 2/3 BFT multisig or the deployer emergency-recovery path. |
| Channel operator (SR-4) | Operates the private negotiation channel; can drop messages, fork views, observe all member messages. | Forging member signatures inside the channel; observing messages encrypted to a member subset (with realisation-appropriate encryption). |
| Recipe-registry attacker | Compromises the recipe registry signing key, attempts to push poisoned recipes. | Backdating recipe-version pinning; affecting already-pinned sessions. |
| Sybil attacker | Generates unlimited low-tier (key:…) identities and farms self-deal reputation. | Generating authority-issued claims (lei, finra-crd, etc.) without owning the underlying registrations. |
| Malicious orchestrator | Drives the session pipeline, assigns `errorClass`, constructs the SessionRecord, and MAY be a distinct REQUIRED signer (§10.4.1); can misclassify failures, drop or reorder phase results, or selectively anchor. | Forging buyer/seller signatures, or producing a both-sided-signed bundle without honest-party consent (§10.11 two-sided independent bundles; party-disagreement → aborted-by-other). |
| Malicious infrastructure | Operates discovery/index/storage infrastructure a party depends on (catalog API, listings index, anchor host); can serve poisoned, stale, or withheld data on the read path. | Forging the signatures on the signed artifacts it serves (consumers dereference anchors and verify content hashes + signatures independently). |
| Malicious verifier | Runs the DACS-2 vet path; can mis-run a recipe, substitute a method, or assert a decision the authority did not return. | Forging the authority's signed/consensus-anchored response, or a recipe steward signature; producing a VerifyResult that re-derives correctly under method/recipe-version checks. |
| Spam / resource-exhaustion adversary | Floods a public surface (ERC-8004 registry writes, negotiation-channel griefing, mempool) to raise cost or degrade availability. | Forging identities or claims (each write/identity costs); breaking liveness of correctly-rate-limited or staked surfaces. |

**Reconciling the §12.4 "Primary adversary" column with this model.** Every §12.4 row's adversary resolves to a class above, with two conventions: (a) **variants of an existing class** — "competing bidder" and "two colluding counterparties" are *Malicious counterparty* (single and colluding); "public-mempool observer" is *Network observer*; "storage operator" is *Malicious infrastructure*. (b) **Non-adversary conditions** — "time" (TOCTOU / stale-window races) and "implementation bug" (e.g. decimal overflow) are **environmental / robustness** conditions, not adversaries: the threat is real and the cited mitigation stands, but there is no actor to model — these rows are defended by deterministic rules and bounds, not by an adversary assumption.

### 12.3 Trust boundaries

A reader following the audit trail from a DACS-5 bundle backwards through the lifecycle crosses these trust boundaries; each boundary has its own assumptions.

- **Party-to-party cryptographic boundary.** Every signed artifact (listing, bundle, agreement, evidence, rating) is verifiable against the signer’s primary-claim key. Trust assumption: the signing key has not been compromised at or before the artifact’s timestamp. Mitigation: key-rotation handling per §6.6 (DACS-1 security considerations).
- **Party-to-authority boundary.** A DACS-2 VerifyResult of method consensus-backed-proxy depends on the authority (GLEIF, FINRA, OFAC, etc.) being honest at fetch time and on the TLS PKI between the substrate validators and the authority. Mitigation: the recipe’s alternatives mechanism (§7.4) lets high-stakes schemes declare additional independent verification methods (§7.12); the v0.2 strengthening (§7.3.5) will tighten the consensus-backed-proxy method itself.
- **Party-to-substrate boundary.** Every anchor (listings, bundles, evidence, recipes, rails) depends on the substrate’s SR-2 implementation for availability and content integrity. Trust assumption: substrate validator-set is honest per the substrate’s consensus protocol. Mitigation: on-substrate anchoring (Storage Programs on Demos) provides indefinite availability; off-substrate anchoring (IPFS, HTTPS) is best-effort.
- **Substrate-to-substrate boundary (cross-chain).** SR-5 atomic settlement crosses chains and depends on the SR-5 mechanism’s trust model (HTLC: cryptographic only; Liquidity Tank: substrate operator; substrate-native: substrate consensus). Mitigation: explicit rail-trust-model disclosure in rail definitions; per-stake rail selection.
- **Party-to-recipe-registry boundary.** Verification routes through recipes whose signing authority is the registry steward (currently KyneSys Labs, per §7.4.4 and §11.1.1). Trust assumption: the steward’s signing key is honest and uncompromised. Mitigation: monotonic recipe-version pinning per session; emergency-revision discipline (§7.4.4). Residual risk under PA-2: steward-key compromise; PA-3 multi-signature governance is the v0.2+ mitigation pathway.

### 12.4 Threat catalogue

Every per-chapter security threat, indexed by adversary class and mitigation status. The threats are stated normatively in the per-chapter sections; this is the cross-reference.

| Threat | Primary adversary | Where mitigated | Status |
| --- | --- | --- | --- |
| Forged listing | malicious counterparty | §6.6 + §B.7 (signatures + domain separator) | mitigated |
| Identity-bundle replay | network observer | §6.3.2 (session nonce) + §6.6 | mitigated |
| Attestation-bundle replay across sessions | malicious counterparty | §10.11 (jobId bound into the bundle hash) | mitigated |
| Catalog poisoning | malicious infrastructure | §6.3.6 (clients dereference anchors) | mitigated |
| Identity-claim substitution | malicious counterparty | §6.6 (pinned bundle hash) | mitigated |
| Method substitution | malicious verifier | §7.12 (method field comparison) | mitigated |
| Recipe poisoning | recipe-registry attacker | §7.12 (signed recipes + pinned recipeVersion) | mitigated |
| Substrate validator capture (SR-3) | substrate validator-set majority | §7.12 (multi-method alternatives) | partial — v0.2 strengthening planned |
| Authority-endpoint TLS MITM (forged authority response) | network active attacker (PKI compromise) | §7.3.5 (v0.2 validator-body-signed) + §7.4 (multi-method alternatives) | partial — v0.2 strengthening planned, residual in v0.1 |
| Negative-match fail-open (truncated sanctions list clears a listed party) | malicious infrastructure / lossy fetch | §7.4.1 PSP-5 (completeness floor before a negative `pass`) | mitigated |
| Verifiable-presentation replay (verified VC re-presented by a non-holder) | malicious counterparty | §7.3.2 (VP holder-binding to session nonce) | mitigated |
| HTLC preimage-reveal front-running | network observer / MEV | §9.5.4 (claims are beneficiary-bound — a front-runner cannot redirect funds; ordering/MEV is a chain-level concern, not a DACS theft vector) | mitigated (theft) / residual (ordering) |
| Rail availability-field poisoning (read before pin) | malicious infrastructure | §9.4.4 (availability pinned from the authoritative rail definition at session start, not a cached/untrusted read) | mitigated |
| Cross-session offer replay (channelId reuse) | malicious counterparty | §8.12 CH-6 (channelId unique per session) | mitigated |
| Counterparty-graph reconstruction (cleartext primary claims at derivable anchor addresses) | network observer | §12.1 (accepted by design — public audit trail; requires no crypto; encrypted-to-parties anchoring is roadmap) | accepted by design |
| Vet-attestation disclosure (anchored VerifyResult reveals "party X screened against authority Y → outcome Z") | network observer | §7.5 (public-anchor data minimisation — predicate outcomes only, no raw PII) + §12.1 (scheme:identifier:decision accepted by design) | partial — raw PII minimised; relationship/decision accepted by design |
| VerifyResult replay | malicious verifier | §7.12 (identifier + bundle hash binding) | mitigated |
| TOCTOU authority change | time | §7.12 (maxAge tightening) | parameter-driven |
| Indeterminate exploitation | malicious counterparty | §7.5.1 + §7.7.1 (aggregation) | mitigated |
| Channel-operator censorship | channel operator | §8.12 (CH-4 liveness detection) | mitigated (substrate-dependent) |
| Channel-operator forking | channel operator | §8.12 (monotonic sequence + cross-check) | mitigated |
| Offer replay across sessions | network observer | §8.12 (channelId in envelope) | mitigated |
| Cross-artifact signature replay | malicious counterparty | §B.7 universal domain separators | mitigated |
| HTLC asymmetric-loss blame ambiguity (window-expired ST-8 reads failed-counterparty for both sides) | time / malicious counterparty | §10.11 (out-of-band review of settlement-atomicity-marked failed-counterparty) | partial — DACS-X dispute concern |
| HTLC free-option abandonment (payer declines reveal after market move; payee capital locked) | malicious counterparty | §9.5.4 HTLC-10 (prefer liquidity-tank or payer stake; DACS-5 records the pattern) | partial — known HTLC property, not standardised in v0.1 |
| Sealed-envelope front-running | competing bidder | §8.12 (hash commitment + private channel) | mitigated |
| Sealed-envelope post-deadline submission | malicious counterparty | §8.4.3 (chain-timestamp anchoring) | mitigated |
| Agreement-listing mismatch | malicious counterparty | §8.5.2 (validation in commit-agreement) | mitigated |
| Re-entrancy on EVM rails | malicious counterparty | §9.13 (phase-handler ordering) | implementation-dependent |
| MEV front-running on payments | public-mempool observer | §9.13 (private mempool option) | parameter-driven |
| Cross-chain atomicity failure | time / chain operator | §9.13 (HTLC timelocks) | mitigated for HTLC; SR-5 implementation-dependent for tanks |
| Liquidity-tank operator compromise | substrate operator | §9.13 (substrate consensus + 15-day recovery) | partial — substrate-trust-floor |
| AP2 mandate replay | network observer | §9.13 (AP2 nonce/expiry) | inherited from AP2 |
| x402 receipt forgery | malicious server | §9.13 (signature verification) | inherited from x402 |
| Refund laundering | malicious seller | §9.13 (anchored amendments) | mitigated |
| Decimal-overflow on cross-decimal pay | implementation bug | §9.13 (string-decimal arithmetic) | mitigated |
| Bundle forgery | malicious counterparty | §10.11 (co-signature requirement) | mitigated |
| Bundle suppression | malicious counterparty | §10.11 (one-sided bundle classification) | mitigated |
| Sybil reputation farming | sybil attacker | §10.11 (per-primary-claim keying) | mitigated for cross-tier; not for same-tier |
| Reputation collusion | two colluding counterparties | §10.11 (volume disclosure + external signals) | partial — protocol cannot prevent |
| Orchestrator error-class misclassification | malicious orchestrator | §10.11 (party-disagreement → aborted-by-other) | mitigated |
| Bundle anchor unavailability | storage operator | §10.11 (on-substrate anchoring) | mitigated (substrate-dependent) |
| Stale reputation windows | time | §10.11 (explicit window bounds) | consumer-driven |
| ERC-8004 write spamming | spam adversary | §10.11 (gas cost + per-session rate limit) | mitigated |
| RFQ session-initiation flooding | malicious counterparty | §8.12 (per-counterparty session-rate limit + optional DACS-2 admission floor) | partial — maxTurns/timeoutSec bound a session, not the initiation rate |
| Sealed-envelope commit-spam | malicious counterparty | §8.12 (optional bidder stake + commit-anchor rate limit) | partial — v0.1 does not standardise stake or bidder eligibility |

### 12.5 Composite trust property

A DACS-5 bundle that validates against all per-chapter conformance rules and whose contained references all dereference and validate provides the following composite trust property to a consumer: "Two or more parties identified by the named primary claims (with the trust profile each claim’s scheme implies) participated in a session against the named listing version, agreed to the named terms, exchanged the named settlements, and produced this audit record. The substrate operator did not collude with the parties to forge the record. The recipe registry was not compromised at the time of the verifications. The composed external standards (W3C VC, TLSNotary, ACME, etc.) behaved per their own security models." This is the composite security claim of DACS v0.1. Each clause has explicit mitigation in the per-chapter sections; each has explicit residual risk in this chapter’s adversary model.

## Chapter 13 — Glossary

A single alphabetical glossary across all five per-stage standards, the front matter, and the back matter. Terms defined in multiple chapters are cross-referenced. This glossary is informative; per-chapter definitions are normative.

- **AgreementDocument.** The canonical signed JSON document produced by a DACS-3 negotiation pattern, carrying the final agreed terms. Defined in §8.5.
- **Anchor / Anchored.** Stored on the substrate such that an anchor reference (substrate-native pointer plus content hash) is sufficient for any party with substrate access to retrieve canonical content and verify integrity. Realised by SR-2.
- **AttestationBundle.** The frozen end-of-session artifact, signed by all parties, anchored via SR-2. The DACS-5 audit unit. Defined in §10.4.
- **AttestationRef.** A reference to an anchored attestation: anchor locator + content hash + (optional) signer. Defined in §7.5.
- **anchoredByRole.** Per-copy AttestationBundle field naming the role (buyer/seller/orchestrator) that anchored that copy; the copy's `outcome` is recorded from that party's perspective. Excluded from the hashed canonical form (so the two-sided copies stay equal) and integrity-checked against the anchor address instead. Defined in §10.4.1/§10.4.2.
- **Auto-accept commitment.** A pre-issued seller-side commitment authorising auto-acceptance of buyer signatures under negotiate-fixed-price. Defined in §8.4.1.
- **Bundle (identity bundle).** An ordered set of claims a party presents about itself, each independently verifiable, plus a presentation signature. Defined in §6.3.2.
- **BundleParty.** A party reference within a DACS-5 AttestationBundle. Defined in §10.4.
- **Canonical form.** RFC 8785 JCS serialisation of a document with signature field(s) omitted.
- **Catalog.** An off-chain index aggregating DACS-1 listings across many sellers for discovery. Defined in §6.3.6.
- **CCI (Cross-Context Identities).** The Demos implementation of SR-1 — cross-substrate identity aggregation. Demos product feature; not a DACS specification term.
- **Claim.** A fact a party asserts about itself.
- **Claim reference / ClaimReference.** A typed identifier referring to the external system that holds a claim. Grammar in §6.3.1; type definition in §7.1.
- **ClaimRequirement.** A listing-side declaration of which claims a buyer or seller bundle must include. Defined in §6.3.3.
- **Commit-agreement.** The DACS-3 phase that anchors the agreement hash on the public chain. Defined in §8.6.
- **CommitmentRecord.** The on-chain record produced by commit-agreement. Defined in §8.6.
- **CompositeVerificationRecord.** The document the DACS-2 vet-credentials phase produces, aggregating freshness checks, supplementary signals, and deal-specific claims. Defined in §7.7.
- **Content hash.** sha256 hex of the canonical form of a document.
- **DACS-1..5.** The five per-stage standards: Identify, Vet, Negotiate, Settle, Verify.
- **DACS-X.** Anticipated future standard for dispute resolution; not part of v0.1.
- **DAHR (Data Agnostic HTTPS Relay).** The Demos implementation of SR-3 — consensus-backed proxy attestation of HTTP responses.
- **Deliverable / DeliverableSpec / DeliverableRef.** The thing being delivered to the buyer; spec defines its shape; ref points to a specific instance. Defined in §9.3.
- **Domain separator.** A protocol-specific string prepended to a hash before signing, preventing cross-protocol signature replay. Universal registry in §B.7.
- **EntitlementRecord.** A DACS-4 deliverable record granting time-bound access to a service. Defined in §9.6.2.
- **errorClass.** A classification of why a phase failed: permanent, transient, counterparty, substrate, settlement-atomicity. Used in PhaseHandlerResult and BundlePhaseEntry.
- **Evidence (SettlementEvidence).** The uniform record produced by every DACS-4 payment and delivery phase. Defined in §9.7.
- **Extended-pointer pattern.** A pattern for handling artifacts larger than the substrate’s anchored-storage cap: the canonical address contains a pointer with externalUrl + externalContentHash; payload is hosted externally. Used by deliverables (§9.6.1) and bundles (§10.4.2).
- **Fixed-price negotiation.** DACS-3 pattern in which the buyer accepts the listed terms. Defined in §8.4.1.
- **HKDF.** The key derivation function specified in RFC 5869; used in HTLC preimage derivation per §9.5.4.
- **HTLC.** Hash Time-Locked Contract; the generic atomic-swap pattern used by pay-cross-chain-htlc. §9.5.4.
- **IdentityBundle.** See "Bundle".
- **Indeterminate.** A DACS-2 VerifyResult.decision value indicating the authority returned a parseable response that conclusively neither confirmed nor denied the claim. Distinct from "error" (verifier could not reach a decision at all). §7.5.1.
- **Error (decision value).** A DACS-2 VerifyResult.decision value indicating verification could not complete due to transport failure, parser exception, or other verifier-side failure. Distinct from "indeterminate" (authority answered, but ambiguously). §7.5.1.
- **JCS.** JSON Canonicalization Scheme; RFC 8785; used for canonical-form serialisation throughout.
- **jobId.** Per-session unique identifier; ULID or substrate-equivalent. Defined in §10.3.
- **L2PS (Layer-2 Privacy Subnets).** The Demos implementation of SR-4 — identity-keyed private coordination channels.
- **Liquidity Tank.** The Demos implementation of SR-5 — pre-funded cross-chain settlement primitive.
- **Listing.** A signed, anchored JSON document declaring an agent’s offering. The canonical contract for a transaction. Defined in §6.3.4.
- **ListingIndex / ListingSummary.** Discovery data structures; not the source of truth. Defined in §6.3.5–6.3.6.
- **negotiate-fixed-price / negotiate-rfq / negotiate-sealed-envelope.** The three DACS-3 negotiation patterns. §8.4.
- **PaymentRailRef / RailDefinition.** Reference to and full definition of a DACS-4 payment rail. §9.3, §9.4.
- **Per-claim keying.** DACS-5 rule that reputation is keyed against the bundle’s primary identity claim, not a wallet or signing key. §10.5.2.
- **perspective_flip.** The DACS-5 reconciliation mapping that re-interprets a counterparty-anchored bundle's `outcome` relative to the scored party (aborted-by-self ↔ aborted-by-other; failed-perm ↔ failed-counterparty). Buyer↔seller only. §10.5.1.
- **Phase / PhaseStep / PhaseType.** A single unit of work in a session pipeline. PhaseType is the closed enumeration across DACS-2..5. §6.3.4.
- **PhaseHandlerResult.** The return shape of every phase handler. §B.5 (front matter).
- **Pipeline.** The ordered sequence of PhaseStep entries declared in a listing. §6.3.4.
- **Presentation signature.** The signature on an identity bundle. §6.3.2.
- **sr1-root presentation.** A bundle-presentation kind in which a single SR-1 root key co-signs every claim under one aggregate signature, producing a single cryptographic artifact for the whole bundle. The natural presentation for a party self-binding a single document. §6.3.2.
- **Primary identity claim.** The claim within a bundle that serves as the canonical identifier of the party for reputation, audit, and addressing.
- **Rate phase.** Optional DACS-5 phase producing structured ratings between parties. §10.6.
- **RatingRecord.** A signed rating from one party about another. §10.6.
- **Recipe.** A DACS-2 binding of claim scheme to verification method, parsing rules, and defaults. §7.4.
- **Recipe availability.** A normative field on every Recipe declaring operational status: live | operator_gated | closed_data | bilateral | mocked | disabled | failed. Verifiers MUST inspect before running. §7.4.5.
- **Rail availability.** A normative field on every RailDefinition declaring operational status, with the same value set and semantics as recipe availability. Orchestrators MUST inspect before selecting. §9.4.4.
- **RFQ (Request For Quote).** DACS-3 bilateral negotiation pattern; bounded multi-turn offer-and-counter. §8.4.2.
- **Sealed-envelope.** DACS-3 sealed-bid procurement pattern. §8.4.3.
- **Session.** A per-transaction lifecycle from Identify through Verify.
- **SessionContext.** The context object every phase handler receives. §B.5 (front matter).
- **SessionRecord.** The orchestrator’s mutable working-state document. §10.3.
- **settle-asymmetric.** Non-terminal DACS-5 session state for the HTLC-9 cross-chain open case (payer claimed the destination, payee's source claim not yet final); resolves forward to settle-completed on a final htlc-claim, or to settle-failed on window expiry. §10.3.1 (ST-8).
- **SettlementAmendment.** A post-settlement record for refunds and corrections. §9.7.1.
- **SIWD (Sign-In With Demos).** Demos-wallet authentication pattern; EIP-4361-style envelope. Used for bundle presentation signatures.
- **SR-1..5.** Substrate requirements: SR-1 cross-substrate identity aggregation; SR-2 anchored immutable storage; SR-3 consensus-backed proxy attestation; SR-4 identity-keyed private coordination; SR-5 multi-chain coordinated atomic settlement. Defined in §5 (front matter).
- **Stor-backed credential.** A DACS-1 claim scheme whose verification result is anchored as a Storage Program. §6.3.1.
- **Storage Program.** The Demos implementation of SR-2 — content-addressed anchored key-value storage. 128 KB soft cap.
- **Substrate.** The underlying blockchain or protocol stack that hosts a DACS implementation. Demos is the v0.1 reference substrate.
- **Substrate-validator-set claim.** A ClaimReference identifying a substrate validator-set epoch; used as the signer for consensus-backed-proxy attestations. §7.5.
- **supersedesEvidenceRef.** SettlementEvidence field on an ST-8 `:resolved` success record pointing to the interim failure record it supersedes; a same-phase supersession, not a refund amendment. §9.7 / ST-8.
- **TxRef / ChainTxRef.** Discriminated union of on-chain transaction references. §9.3.
- **Universal signature scheme.** The cross-stack domain-separation scheme requiring every DACS signature to bind to a per-artifact-kind separator. §B.7.
- **ULID.** Universally Unique Lexicographically Sortable Identifier; recommended jobId format.
- **validator-set claim.** See "Substrate-validator-set claim".
- **VerifyResult / VerifyResultRef.** The uniform record every DACS-2 method produces; reference to an anchored VerifyResult. §7.5.
- **Vet-credentials phase.** The DACS-2 phase that runs verification across the counterparty’s bundle. §7.8.
- **Well-known/agent.json.** The A2A capability-discovery surface that DACS extends with a dacs block. §6.3.5.

## Chapter 14 — Conformance test plan

This chapter sketches the test categories an implementer should cover to claim conformance to each DACS standard. It is a **plan, not a test suite**; the test suite itself (test vectors, expected outputs, golden files) is produced separately and tracked alongside reference implementations. Where a chapter’s conformance summary enumerates labelled rules (e.g., BP-1, LR-2, CM-3), the test plan groups them into runnable categories.

### 14.1 DACS-1 — Identify

Exercise each rule at its normative home; full text is not restated (define-once). Fixtures under `conformance/`.

| Rules | Home | Exercise (intent) | Vectors |
| --- | --- | --- | --- |
| Claim-reference parser | §6.3.1 | every scheme: valid canonical / valid non-canonical (canonicalise on read) / invalid grammar (reject) / unknown-scheme (not silently accepted) | `conformance/vectors/` |
| BP-1..BP-4 (bundle producer) | §6.3.2 | produce → canonical form → hash → domain-separated sign → anchor round-trip | `conformance/fixtures/identity/` |
| BR-1..BR-5 (bundle reader) | §6.3.2 | accept-conformant; reject unsigned / missing-required-`verifiedBy` / unverified-`presentedBy`-when-selector-set; unknown-scheme → unverified; SIWD `dacs:<hex>` Resource + session-`Nonce` match | `conformance/fixtures/identity/` |
| match() (BundleRequirement) | §6.3.3 | required missing / required failing / oneOf satisfied / oneOf unsatisfied / selector match / mismatch | `conformance/vectors/` |
| LP-1..LP-4, LR-1..LR-3 | §6.3 | publisher: sign / anchor / version-monotonicity / revocation; reader: halt-on-first-failure, revoked refusal, size-cap | `conformance/vectors/` |
| Discovery | §6.3.6 | well-known parser; catalog endpoint shape; anchor cross-check from `ListingSummary` | `conformance/vectors/` |
| IT-1..IT-3 (identity tier) | §6.3.2.1 | derive from verified-and-fresh claims only; ignore self-asserted; deterministic; institutional precedence; stale-`verifiedBy` does not elevate | `conformance/fixtures/identity/` |

### 14.2 DACS-2 — Vet

| Rules | Home | Exercise (intent) | Vectors |
| --- | --- | --- | --- |
| CM-1..CM-5 (method common) | §7.3 | per-method: input-shape; pass/fail/indeterminate; attestation anchoring; `VerifyResult` with correct method; canonical form + domain-sep signature | `conformance/fixtures/` |
| RA-1..RA-5 + resolution | §7.4 | steward-sig + domain separator; canonical anchoring; version monotonicity; supersede-on-replace; index lookup; content-hash; version pinning | `conformance/` |
| PSP-1..PSP-5 | §7.5.1 | match-predicate per format; parse-fail → error (not fail); negative-match inversion; `indeterminateOn` before match; dataMap extraction non-deciding; deterministic (no script/sub-fetch/redirect); PSP-5 completeness floor before a negative `pass` | `conformance/` |
| VP-R1..VP-R4, VP-C1..VP-C3 | §7.6.1 | transient retry / permanent no-retry / new-attestation / no-retry-on-indeterminate; reuse within effective window; maxAge tightens never widens | `conformance/` |
| Aggregation | §7.7.1 | classify_required branches; oneOf within-group precedence error>indeterminate>fail; cross-accumulator fail>error>indeterminate; VPC-4 counterparty-malformed attribution | `conformance/` |
| RAV-1..RAV-7, RAV-R1..RAV-R5 | §7.4.5, §9.4.4 | recipe availability consumer+steward behaviour; rail preflight; no disabled/failed selection; RAV-R5 authoritative signed read | `conformance/` |
| VPC-1..VPC-4, MA-1..MA-3 | §7.8, §6.3.3 | phase order / two-sided / anchor-before-return / fail-or-indeterminate; matching + `presentedBy` verification | `conformance/` |
| WN-1..WN-6 (warnings) | §7.7 | advisory-only; MUST NOT move `overallDecision`; preserved on `pass`; `suggestedRetryAfterMs` doesn't override recipe; unknown-code conservative | `conformance/fixtures/` |

### 14.3 DACS-3 — Negotiate

| Rules | Home | Exercise (intent) | Vectors |
| --- | --- | --- | --- |
| Channel envelope + failure | §8.3.3, §8.12 | channelmsg domain-sep sig; sequence monotonicity; signature scope; liveness-exceeded → channel-failed; abort round-trip | `conformance/` |
| negotiate-fixed-price | §8.4.1 | live signature path; auto-accept commitment + instance-signature path; reject pre-issued per-instance signatures | `conformance/` |
| RFQ-1..RFQ-4 | §8.4.2 | maxTurns; turn-timeout; out-of-band-terms rejection at commit-agreement | `conformance/` |
| SE-1..SE-7 | §8.4.3 | commitDeadline (chain-timestamped); reveal-window vs SR-2 anchor (SE-3); mismatch exclusion; anchored-reveal-set selection (relay-suppression); exclusion ordering (currency/non-positive before reserve); reserve floor/ceiling inclusive; tie-break (SE-5); empty-set → negotiate-failed; rule-ref content-hash binding (SE-6); bidHash domain-sep + salt floor (SE-7) | `conformance/` |
| PS-1..PS-3 | §8.8 | exactly-one negotiate phase; commit immediately follows; pattern ↔ pricing-model compatibility | `conformance/` |
| Agreement validation | §8.5.2 | price-band / rail-acceptance / deliverable / deadline / pattern checks; `priceAnchor` valid-when-present, optional | `conformance/` |
| CA-1..CA-4 | §8.6 | refuse-advance-until-ok; double-commit reject; immutability after anchor; domain-sep commitment signature | `conformance/` |

### 14.4 DACS-4 — Settle

Exercise each rule at its normative home; the full rule text is **not** restated here (define-once — same discipline as the §12.4 threat index). "Exercise" is one-line test intent; executable fixtures live under `conformance/`.

| Rules | Home | Exercise (intent) | Vectors |
| --- | --- | --- | --- |
| RD-1..RD-5 | §9.4.3 | steward-sig + domain separator; anchor; version monotonicity; railType↔asset/network consistency | `conformance/fixtures/settlement/` |
| PC-1..PC-7 | §9.5.1 | input-shape; anchored evidence; correct `attestationRef` (deferrable under PC-7); all `errorClass` values; PC-5 currency-resolution; PC-6 `settlementFinality` present-on-success/absent-on-delivery; PC-7 cross-chain anchor decoupling | `conformance/fixtures/settlement/` |
| HTLC-1..HTLC-10 | §9.5.4 | buyerSalt entropy/confidentiality/non-reuse; HKDF derivation + input-uniqueness; canonical claim order; per-chain hashlocks; timelock asymmetry on absolute expiry (pinned params, source-finality margin); HTLC-9/ST-8 asymmetric resolution; HTLC-10 free-option | `conformance/fixtures/settlement/htlc9-asymmetric.json` |
| CD-1 | §B.2 | economically-equal decimals (`"1.50"`=`"1.5"`) → identical hashes/signatures | `conformance/vectors/` (CD-1) |
| AMEND-1..AMEND-4 | §9.7.1 | `amendsEvidenceRef` resolves + jobId match; refund/partial-refund reference success-only; summed `refundAmount` ≤ `paymentAmount`; flagged-amendment not treated as valid unwind | `conformance/fixtures/settlement/` |
| PIPE-1..PIPE-5 | §9.9 | ≥1 deliver (pay-* optional, §6.3.4(8)); deterministic ordering; pay↔deliver gating; phase repetition | `conformance/vectors/` |
| Per-rail procedures | §9.5.2–§9.5.7 | erc20/spl decimal-conversion (no float) + finality wait; tank BridgeOperation lifecycle + route scope; ap2/x402 mandate-revocation + receipt-signature | `conformance/fixtures/settlement/` |
| Delivery phases | §9.6 | storage-program (normal + extended-pointer); entitlement sig/anchor/scope; attested-payload composing a DACS-2 attestation | `conformance/fixtures/` |

### 14.5 DACS-5 — Verify

| Rules | Home | Exercise (intent) | Vectors |
| --- | --- | --- | --- |
| ST-1..ST-8 (state machine) | §10.3.1 | every `(from→to)` legal-only; illegal-pair reject (ST-1); abort from any `*-pending` (ST-3); rate branch + non-fatal (ST-4/5); ST-7 pause→resume / →failed-substrate; ST-8 `settle-asymmetric` forward-resolution (→completed on final source-claim, →failed-counterparty on expiry, →paused on SR-2 outage), non-terminal; terminal→`outcome` map (ST-6) | `conformance/fixtures/settlement/` |
| Bundle production | §10.4 | two-sided anchoring at role addresses; `anchoredByRole` ↔ address (mismatch rejected); canonical-equality happy path (excludes anchoredByRole/signatures); `dacs-bundle:v1:` sig; extended-pointer | `conformance/fixtures/` |
| Bundle consumption | §10.4.3 | two-sided lookup; one-sided → aborted-by-self; divergence = `outcome`/`phaseSummary` contradiction (advisory skew is NOT divergence); per-party policy; "disputed" is a consumer verdict, not an outcome value | `conformance/fixtures/` |
| Reputation derivation | §10.5.1 | all outcome partitions; party-fault denominator excl. failed-substrate; null vs zero; empty-input totality; two-sided reconciliation + `perspective_flip`; reconciliation guards; rating de-duplication | `conformance/fixtures/reputation/` |
| Determinism receipt | §10.5.3 | `bundleRefs` = `reconciled` set, ascending-`contentHash` order; re-derive byte-identical `metrics`/`bundleCount` under recorded `windowingBasis`; omitting basis or mis-ordering is non-conforming | `conformance/` |
| Category-scoped derivation | §10.5.4 | prefix filter before §10.5.1; non-resolving `agreementRef` excluded; exact-or-`category+"."` prefix; hint accuracy | `conformance/` |
| RT-1, RT-2 (rate phase) | §10.6.1 | run-after-settle; one-record-per-direction; rating domain-sep sig; RT-1 producer-reject out-of-range/over-length; RT-2 deriver-exclude non-conforming; `dimensions` opaque | `conformance/` |
| ERC-8004 publication (optional) | §10.7 | token-owner-signed entry; bundle-anchor pointer; rate-limit | `conformance/` |

### 14.6 Universal signature scheme & canonical form (SIG-1..SIG-5, CF-1..CF-4, CD-1)

A cross-cutting test category that every conforming implementation runs once:

- Sign every artifact kind in §B.7 with a known key; verify with the same key against the domain-separated payload; reject if the verifier reconstructs without the separator.
- Cross-artifact replay test: take a valid signature on artifact kind A, attempt to verify it as a signature on artifact kind B with the same hash bytes; verification MUST fail.
- Unknown-artifact x-* prefix test: implementations encountering an unknown domain separator MUST reject; experimental x- separators MUST be accepted only with out-of-band agreement.
- **CF-1 (NFC).** A document carrying a non-ASCII identifier supplied in NFD form MUST hash and verify identically to the same document supplied in NFC form; a verifier MUST normalise before recomputing the canonical form.
- **CF-2/CF-3 (ClaimReference canonical form & identity).** `CCI-LEI:…` and `cci-lei:…` MUST produce identical content hashes when embedded in a signed document (scheme case-folded). Two references differing only in parameter order MUST produce identical canonical bytes; two references differing only in the presence/value of parameters MUST resolve to the same reputation key (parameters excluded from identity).
- **CF-4 (logical-address encoding).** A logical address built from a multi-colon primary claim MUST round-trip: assemble → derive native address → split the logical address back into `{sellerPrimaryClaim, listingId, listingVersion}` and percent-decode each to the exact originals. The DACS-4 payment-evidence address `dacs4:payment:{jobId}:{railId}:{phaseIndex}` MUST likewise round-trip a multi-colon `railId` (e.g. `evm-erc20:1:USDC`) — the encoded railId splits back to its exact original while `phaseIndex`/`resolved` remain unescaped fixed segments — and the DACS-2 addresses `dacs2:{jobId}:{scheme}:{identifier}:v{recipeVersion}` and `dacs2:composite:{jobId}:{evaluatedParty}` MUST round-trip a multi-colon `{identifier}` / `{evaluatedParty}` (e.g. `evm:mainnet:0x1234`) while `{scheme}`/`v{recipeVersion}` remain unescaped; and the DACS-5 rating address `dacs5:rating:{jobId}:{rater}` MUST round-trip a multi-colon `{rater}`. An address whose variable segments are left raw (unescaped) MUST be rejected as malformed.
- **CD-1 (canonical decimal).** `"1.50"` and `"1.5"` as `PriceTerm.amount` MUST produce identical agreement hashes and signatures.
- **SIG-5 (preserve-unknown).** A verifier built against schema vN MUST successfully verify the signature on a document produced under vN+1 that adds an unknown field, by hashing the document as received (unknown field included); a verifier that strips the unknown field before hashing (and thus rejects) FAILS this test.

### 14.7 Governance (GOV-1..GOV-3)

- **GOV-1 steward disclosure.** A registry consumer surfaces which signing key it treats as authoritative and does not present the single steward as a constituted multi-party body.
- **GOV-2 anchoring-phase disclosure.** An implementation discloses its operating phase (in-code / single-signer / multisig).
- **GOV-3 anchoring-phase verification.** A consumer reads the resolved recipe's `governance.anchoring` and evaluates each pinned recipeVersion against the phase recorded at pin time; a recipe marked `in-code` is not treated as canonically anchored.

### 14.8 Substrate-capability tests

For substrates other than Demos that claim conformance, additional capability tests apply:

- **SR-1.** Sub-identity binding test: a root key binds N sub-identities, presents under a single SR-1 signature, verifier resolves each to its claim scheme.
- **SR-2.** Anchor-write → retrieve → content-hash check round-trip; size-cap enforcement.
- **SR-3.** Fetch-specification → consensus-signed commitment → anchor; body-hash verification by independent consumer. (v0.1 conformance bar is trust-property; v2 will add wire-protocol tests.)
- **SR-4.** Channel-establish → member-only-message-delivery → non-member-cannot-read; CH-1..CH-6 each as a test (CH-6: channelId unique per session — cross-session offer-replay rejected). (v0.1 trust-property; v2 wire-protocol.)
- **SR-5.** Cross-chain lock → release with bounded-time atomicity; refund path on counterparty timeout.

### 14.9 Out of scope for v0.1 conformance

The following are not part of v0.1 conformance and SHOULD NOT be tested as such:

- Cross-substrate interoperability for SR-3- or SR-4-dependent phases (deferred to v2).
- Multi-party transactions beyond bilateral plus sealed-envelope (deferred).
- Streaming / continuous-flow rails (deferred).
- Cross-DACS-version pipelines (deferred).
- Dispute *resolution* flows (DACS-X, anticipated). Divergence *detection* — the two-sided lookup plus canonical-divergence classification and per-party policy of §10.4.3(d) — **is** in scope for v0.1 conformance; only the resolution layer is deferred.

## References

Cross-stage references for DACS-1 through DACS-5. Per-stage chapters may cite additional substrate-specific or standard-specific material inline.
**Normative — RFCs**

- RFC 2119 — *Key words for use in RFCs to Indicate Requirement Levels*. Bradner. 1997.
- RFC 7231 §6.5.2 — *Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content — 402 Payment Required*. Fielding & Reschke. 2014.
- RFC 8174 — *Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words*. Leiba. 2017.
- RFC 8555 — *Automatic Certificate Management Environment (ACME)*. Barnes et al. 2019.
- RFC 8785 — *JSON Canonicalization Scheme (JCS)*. Rundgren et al. 2020.

**Companion DACS specifications**

- **DACS-1 — Agent Identity, Discovery and Listing**, chapter 6 of this document.
- **DACS-2 — Credential Attestation**, chapter 7 of this document.
- **DACS-3 — Negotiation**, chapter 8 of this document.
- **DACS-4 — Settlement: Payment Rails and Delivery Phases**, chapter 9 of this document.
- **DACS-5 — Verification, Session Records and Reputation**, chapter 10 of this document.

**Ethereum ecosystem**

- **ERC-8004** — *Trustless Agents*. Davide Crapis et al. Ethereum Foundation, Ethereum Improvement Proposals draft.
- **ERC-8183** — *Standard for Job Escrow*. Proposed standard for EVM-native escrow primitive supporting job-style transactions.

**W3C and related**

- **W3C Decentralized Identifiers (DIDs) v1.0**. W3C Recommendation, 2022.
- **W3C Verifiable Credentials Data Model 2.0**. W3C Recommendation Track.
- **W3C Verifiable Credentials Status List 2021**.

**Payment standards**

- **AP2 — Agent Payments Protocol**. Google. Donated to FIDO Alliance, April 2026.
- **x402 — HTTP 402 revival**. Coinbase, Cloudflare, Anthropic.

**Agent communication**

- **A2A** — *Agent2Agent Protocol*. .well-known/agent.json discovery surface.

**Verification and attestation**

- **TLSNotary**. Privacy & Scaling Explorations (PSE) rebuild, 2024.
- **Reclaim Protocol**. zkTLS proof system for HTTP responses.
- **DECO** — *Liabilities-and-Verifiability Decentralized Oracle Layer*. Earlier zkTLS-style construction.

**Demos / Kynesys**

- **Demos Whitepaper**. Kynesys Labs.
- **Kynesys SDK**, package @kynesyslabs/demosdk. Modules: identities, storage, bridge (Native Bridges + Rubic), demoswork (L2PS workflow), web2 (DAHR).

**Identifiers and utility**

- **ULID** — *Universally Unique Lexicographically Sortable Identifier*.

**Procurement frameworks**

- **FAR Part 14** — *Sealed Bidding*. US Federal Acquisition Regulation.
- **FAR Part 15** — *Contracting by Negotiation*. US Federal Acquisition Regulation.
- **EU Directive 2014/24/EU** — *Public Procurement Directive*.
