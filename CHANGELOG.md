# DACS Changelog

All notable changes to the Demos Agent Commerce Standards.

This document follows the spirit of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The format is adapted for a standards document rather than a software project: the focus is on normative changes that affect implementers, not on internal editorial revisions.

The format used per release:
- **Added** — new normative requirements, new fields, new sections.
- **Changed** — modified normative requirements; semantics changes; renames.
- **Removed** — retired normative requirements; deleted fields; obsolete framing.
- **Fixed** — spec defects (rules that referenced undefined values, internal inconsistencies, addressing patterns that did not work on the named substrate).
- **Governance** — changes to stewardship, working-group framing, or progressive-anchoring phase.

---

## [Unreleased]

Defect-triage and follow-on hardening on top of v0.1 (steward-merged via the issue triage of the cX3po review wave and the xm33 / DACS-X contributions).

### Added

- **Canonical-form rule family CF-1..CF-4** (§7.2, §6.3.1, §6.3.4) — CF-1 global NFC pre-canonicalisation of all signed/hashed string values; CF-2 ClaimReference canonical byte form (scheme lowercased before hash/sign/compare, identifier NFC, parameters sorted + uppercase-hex percent-encoded); CF-3 ClaimReference canonical identity = (scheme, identifier) only, parameters excluded from reputation keying; CF-4 logical-address delimiter encoding so the `dacsN:` logical address is reversibly parseable. Closes #7, #42, #54.
- **SIG-5 preserve-unknown** signature verification + **`version_tag` = major-version** binding (§7.7), making §11.1.2 forward-readable shapes hold for signed artifacts. Conformance vectors for CF-1..CF-4 / CD-1 / SIG-5 added to §14.6. Closes #74.
- **Normative session-state transition table** (§10.3.1) — rules ST-1..ST-7 (forward-only, abort entry from any `*-pending` framed as a party's right, rate branch, rate-non-fatal with no `rate-failed` state, terminal-state set + `endedAt`, substrate pause/resume) plus a state→bundle-`outcome` mapping resolving the `transient`/`settlement-atomicity` buckets. Closes #41, #80, #81, #91, #93, #97.
- **`rfqInitiator` negotiate-rfq phase parameter** (§6, §8.4.2) — `'buyer' | 'seller'`, default `'buyer'`, defining who sends the first RFQ offer; the prose that called it a listing field is corrected. Closes #20.
- **`ClaimRequirement.recipeVersion` pin** (§6.3.3, §7.4.1) — per-claim exact DACS-2 recipe-version pin (symmetric with the rail-side `railVersion`), making the §7.4.1 "pinned recipe" branch reachable and restoring the mid-session-revision protection. `docs/flow-trace.md` reconciled. Closes #82.
- **Rating bounds — rules RT-1 / RT-2** (§10.6.1, §10.5.1, §10.8, §14.5) — producer MUST reject a RatingRecord whose `value` is not an integer in [1,5] or whose `freeText` exceeds 1000 chars (RT-1); deriver MUST exclude non-conforming records before aggregation (RT-2), closing the metric-poisoning gap where a self-signed `value: 1e9` would inflate the average. Closes #84.

### Changed

- **`RatingRecord.dimensions` declared opaque pass-through** (§10.6.1) — not interpreted or aggregated by DACS-5 derivation, no protocol semantics, unconstrained keys/ranges; consumers MUST NOT rely on it for conformance decisions. A canonical dimension namespace is a roadmap candidate. Closes #96.
- **`cancellationPolicy` declared informational-only in v0.1** (§6.3.4 listing terms) — no enforced `cancelled` state/outcome; advertised policies are not binding, reputation-neutral exits, and the §10.3.1 abort semantics govern. A first-class `cancelled` outcome is a roadmap candidate. Closes #92.
- **Settlement over-promises reconciled to v0.1 scope** (§9.9, §9.5.5) — patterns the spec named but the v0.1 model cannot express are now scoped out and roadmapped, removing four internal contradictions: (i) **escrow-with-delivery-gate** — the v0.1 atomic-swap `pay-cross-chain-htlc` handler has no mid-lock suspension point, so "deliver between lock and reveal" is reserved for a future job-escrow rail (ERC-8183) (#8); (ii) **streamed entitlement** — reframed as a sequence of independent sessions (one pipeline = one jobId), with continuous-flow/subscription settlement out of scope per §11.2.4 (#64); (iii) **PIPE-5 fee-split** — narrowed so repeated pay-* phases settle the same agreement price; distinct-amount/multi-payee fee-split is unrepresentable in v0.1's single-amount contract and is roadmapped (#85); (iv) **liquidity-tank recovery-pending evidence** — v0.1 tank evidence is success-only; a recovery-pending marker distinguishing a recoverable lock from terminal loss is roadmapped (#25). Roadmap rows added/extended for all four. Closes #8, #25, #64, #85.

### Removed

- **`membership-change` reserved out of v0.1** (§8.3.1 CH-1, §8.3.3 `ChannelMessage.type`) — channel membership is fixed for the channel's lifetime in v0.1; the undefined `membership-change` type and `admissionPolicy` are removed from the closed enum and reserved for a future version (dynamic membership is a roadmap candidate). Closes #21.

### Fixed

- **Demos logical→native address mapping did not match the StorageProgram SDK** (§6.2, §6.3.4). v0.1 stated `native_address := "stor-" + sha256(logical_address)` and required consumers to recompute the native address from the logical pattern. The actual Demos SDK (`storage/StorageProgram.ts`) derives `"stor-" + first40hex(sha256(deployerAddress + ":" + storageProgramName + ":" + nonce + ":" + salt))` — folding in the deployer address and the per-write transaction nonce (truncated to 40 hex), so the native address is **not** recomputable from the logical address alone. The §6.2 universal rule now distinguishes **pure mappings** (consumer recomputes directly) from **write-input mappings** (implementation MUST publish the logical→native binding via record metadata + discovery; consumer resolves through it); the §6.3.4 Demos binding shows the real derivation and requires binding publication. The CF-4 delimiter-encoding (logical-address reversibility) and this correction coexist: CF-4 governs the *logical* address; the *native* derivation is the write-input case. Surfaced by the `agent-commerce-demo` reference implementation (#106).
- **HTLC cross-chain settlement actor topology was internally contradictory** (§9.5.4, HTLC-7, HTLC-9, §9.8). The procedure, the HTLC-7 safety proof, and the HTLC-9 asymmetric-state evidence named conflicting actors for who claims/receives on which chain, and the claim order depended on an undefined `flow` selector. Corrected to the canonical atomic-swap topology (verified against Tier Nolan / bip-atom, the Bitcoin Wiki, COMIT, and Lightning): the **payer** (preimage holder) locks the **longer-timelock source** (beneficiary = payee, refund → payer); the **payee** locks the **shorter-timelock destination** (beneficiary = payer, refund → payee); the **payer claims the destination first** (revealing the preimage), then the **payee claims the source**. `flow` deleted. HTLC-9 corrected (the **payer** — not the payee — receives on the destination in the asymmetric state; the marker `dest-revealed-source-unclaimed` and the never-refund/`correction` rule are unchanged, so the DACS-X correction flow is unaffected). Added **HTLC-10** (free-option disclosure) and a conservative finality-margin requirement (≥ 2× destination P99 latency), and tightened HTLC-5's input-uniqueness/salt-loss conditions. Two reference-impl conformance items tracked (reveal order; HKDF derivation) — app-layer only, no contract or SDK change. (#24)
- **Settlement/delivery inconsistencies fixed** (§8.5.2, §9.4.5, §9.5.5, §9.6.2/§9.6.3): (i) delivery handlers read entitlement/attested-payload parameters from the **DeliverableSpec** (the listing's `offering.deliverable`, hash-bound per §8.5.2), not from the `DeliverableRef` in `agreement.terms.deliverable` which carries none of them; `verificationMethod` added to the attested-payload variant (#77); (ii) EntitlementRecord renewal gets a `renewalSeq` address discriminator (`dacs4:entitlement:{jobId}:{renewalSeq}`) so a renewal no longer collides with the original on deterministic storage (#83); (iii) the §8.5.2 settle-by deadline is bounded against `committedAt` (the SR-2 commitment anchor timestamp, same clock as SE-2) not the self-reported `generatedAt` (#90); (iv) §8.5.2 now re-checks `validity.notAfter ≥ committedAt`, closing the read-to-commit expiry interval (#86); (v) §9.5.5 forbids silent rail-mechanism substitution (no tank→HTLC fallthrough; `txRef.kind` MUST match the pinned rail), with flow-trace.md reconciled (#60); (vi) RAV-R4 narrowed to detect rail failure at the settlement attempt (availability is pinned at session start, so a mid-session flip isn't observable) — a proactive liveness probe is roadmapped (#23). Closes #23, #60, #77, #83, #86, #90.
- **x402 evidence is now chain-verifiable + rail-protocol-version captured** (§9.5.6, §9.5.7, §9.3 txRefs, §12.5). x402 settles on-chain (a gasless USDC transfer on its settlement chain, e.g. Base) and the facilitator returns the on-chain tx hash in the `PAYMENT-RESPONSE` header — but the evidence carried only the receipt hash, so §9.13/§12.5's "verifiers MUST validate" was unsatisfiable from the anchored artifact. The x402 txRef now carries `settlementTxHash` + `chainId`, making the record **chain-verifiable directly against the settlement chain, like the `evm` rail** (the primary audit path; the receipt hash is supplementary, with a documented fallback for facilitators that don't return a tx hash) (#28). Both the x402 and AP2 txRefs now carry a required `protocolVersion`, so historical evidence is re-validatable against the wire rules of its era (#27). Closes #27, #28.

---

## [0.1] — 2026-05-31

First publicly released version.

Earlier drafts circulated internally under per-stage version numbers (DACS-1..5 v0.1) attached to a paper version (v0.7), with a brief v0.8 cut that consolidated review-pass revisions. Those numbers are retired and reset to a common baseline. v0.1 publishes all five per-stage standards together; from this baseline onward each per-stage standard versions independently.

External implementers who saw earlier drafts (most notably PATH-OS Labs' `pathos-dacs-ref`, which was built against the v0.7 paper / v0.1 per-stage state) should treat this entry as the migration list for what changed between their drafting target and v0.1.

### Added

- **`sr1-root` variant on `PresentationSignature`** (§6.3.2). New variant: `{ kind: "sr1-root"; rootClaim: ClaimReference; aggregateSignature: string }`. The natural presentation kind for a party self-binding a single document — a seller signing their own listing, an orchestrator binding multiple per-substrate addresses under one identity. Previously, the spec referenced `sr1-root` in §6.3.3's `preferredPresentation` enum and §6.3.4's listing-signature rule, but the union didn't define it; implementers fell back to `per-claim` with synthetic key claims. The domain-separated payload (`"dacs-bundle-presentation:v1:" || bundle_hash`) is shared with the other three presentation kinds.

- **`VerifyResult.decision` fourth value: `error`** (§7.5.1). Decision is now `pass | fail | indeterminate | error`. Distinction:
  - `indeterminate` — authority responded, response parseable but conclusively neither confirms nor contradicts the claim. The authority's indeterminate answer.
  - `error` — verification could not complete (transport failure, SR-3 fetch timeout, parser exception). The verifier never received an authority decision.
  - Retry rules now distinguish: `error` is the default-retryable value; `indeterminate` is not retried unless `recipe.retryOnIndeterminate: true`.
  - Aggregation precedence: failures > errors > indeterminates. The composite record's `overallDecision` is now also four-valued. New rules VP-R1 through VP-R4 cover the retry semantics.

- **`HTLC-6` normative rule on per-chain hashlock computation** (§9.5.4). Hashlock is the chain-native hash function applied to the preimage. Source and destination chains MAY use different hash functions (keccak256 on EVM, sha256 on Solana/Bitcoin family, blake2b on Cosmos family). The preimage is the only cross-chain-shared value; each side's hashlock binds against its own native hash of that preimage. The previous HTLC-5 rule conflated preimage derivation (one operation, sha256 globally appropriate) with hashlock computation (one per chain, must be chain-native).

- **Logical-vs-native address split, applied universally** (§6.2, §6.3.4). Throughout DACS, addresses of the form `dacs1:…` through `dacs5:…` are *logical* addresses: substrate-independent, human-readable, stable identifiers the protocol reasons about. Each substrate maps them to its native addressing under a deterministic rule. On Demos, the mapping is `native_address := "stor-" + sha256(logical_address)` because Demos's StorageProgram naming does not permit colons. Other substrates substitute their own mapping; the requirement is determinism, one-to-one, and reversibility by any party knowing the logical pattern.

- **`recipe.availability` normative field** (§7.4.5). Every `Recipe` now declares an operational status from a closed enum: `live | operator_gated | closed_data | bilateral | mocked | disabled | failed`. Verifiers MUST inspect availability before running a recipe (RAV-1 through RAV-7). Aggregation under §7.7.1 treats `disabled` and `failed` recipes as decision = `error` regardless of any output. The previous informative legend in §6.1 (🟢/🟡/🔵) flattened distinct operational states into one and pushed disambiguation onto every implementer's UI surface; promoting availability to a normative field moves the disambiguation into the protocol layer where verifiers can reason about it programmatically.

- **`rail.availability` normative field** (§9.4.5). Same value set and semantics as recipe availability, applied to `RailDefinition`. Orchestrator obligations (RAV-R1 through RAV-R4) parallel verifier obligations on recipes. A rail transitioning from `live` to `failed` mid-session maps to errorClass = `substrate`, not `counterparty`.

- **Progressive anchoring phases on registries** (§7.4.4 recipes, §9.4.3 rails). Three explicit phases: PA-1 (bootstrap; in-code constants), PA-2 (single-steward; signed by the steward), PA-3 (constituted; signed by a multi-party governance body). Implementations MUST disclose which phase they operate in; consumers MUST verify the phase against their own trust requirements. The current operating phase for v0.1 is PA-2 with KyneSys Labs as the steward.

- **§11.2.6 Multi-party governance** as named follow-on work. Acknowledges that the PA-2 → PA-3 transition is itself open work that v0.1 does not specify (constitution mechanism, multi-signature thresholds, sub-authority delegation by domain).

- **Glossary entries** for `sr1-root presentation`, `Error (decision value)`, `Indeterminate (decision value)`, `Recipe availability`, `Rail availability`.

- **Conformance test plan entries** for the four-value `VerifyResult.decision`, HTLC-1..HTLC-6 per-chain hashlock testing, RAV-1..RAV-7 recipe availability obligations, RAV-R1..RAV-R4 rail availability obligations.

- **Acknowledgement of `pathos-dacs-ref`** (§11.3 closing). The previous draft listed "second independent reference implementation against the spec" as remaining work. The PATH-OS Labs reference implementation, built independently against earlier drafts, closes this gap. The cross-substrate test of the artifact-level portability claim (an implementation against a non-Demos substrate) remains future work, but the third-party-implementability claim is now empirically tested.

### Changed

- **DACS-5 bundle separator renamed** from `dacs5-bundle:v1:` to `dacs-bundle:v1:` (§7.7, §10.4.1). The earlier name was the lone outlier in the universal separator scheme (`dacs-<kind>:v<ver>:`); a universal separator builder could not produce it. Bundles signed under the old separator will not verify under the new one (which is the point — domain separators exist to prevent cross-context reuse). The "preserved verbatim for backwards compatibility" justification in earlier drafts was never valid as no reference implementation had shipped under the old name.

- **`Listing.acceptedRails` is now optional** with a conditional rule (§6.3.4). Previously declared `acceptedRails: PaymentRailRef[] // non-empty`, which forced sentinel `railId: "none"` workarounds for intake-only listings. The schema is now:
  ```
  acceptedRails?: PaymentRailRef[]      // required iff pipeline contains any pay-* phase
  ```
  Intake-only patterns explicitly accommodated in validation step 8: RFP intake, reverse auctions where the bid is the commitment, free services gated by reputation, sealed-bid procurements settled out-of-band.

- **HTLC-5 narrowed** (§9.5.4). Previously a single rule covering both preimage derivation and hashlock computation. Now scoped to preimage derivation only: HKDF per RFC 5869, sha256 KDF, IKM = buyerSalt, salt = jobId, info = agreementHash. Hashlock computation moved to HTLC-6 (see Added).

- **`overallDecision` type on `CompositeVerificationRecord`** expanded to four values (§7.7). Matches the four-value `VerifyResult.decision`. Failure-reason text distinguishes "required errored" from "required indeterminate" from "required failing" so consumers can debug.

- **Aggregation algorithm** rewritten to handle four classifications with precedence `failures > errors > indeterminates` (§7.7.1). The `classify_required` helper now distinguishes all four cases; `oneOf` group resolution similarly distinguishes "at least one indeterminate" from "at least one errored" from "no claim satisfied at all".

- **§6.1 production-mapping legend** (🟢/🟡/🔵) clarified as informative-about-substrate-features only. Per-recipe and per-rail operational status uses the normative `availability` fields in §7.4.5 and §9.4.5 — the legend no longer carries the disambiguation it used to.

- **§11.1 Governance and versioning** renamed to **§11.1 Stewardship and versioning** and rewritten throughout. The previous §11.1.1 "The proposal" was sales-shaped (positioning Demos as the substrate, listing what needed to happen with composed standards); replaced by **§11.1.1 Current steward**, which names KyneSys Labs honestly and discloses the single-steward arrangement.

- **§11.3 closing** rewritten. The previous version led with "the closed-marketplace alternative is consolidating fast" and positioned DACS as Demos's contribution to keeping the lifecycle open. The v0.1 closing is descriptive rather than positional, acknowledges the PATH-OS reference implementation explicitly, and lists honest remaining work without sales register.

- **Versioning scheme.** Earlier drafts used dual versioning (paper v0.X + per-stage v0.Y) with diverging per-stage numbers. v0.1 retires those and resets all five per-stage standards to a common baseline, published together. From this baseline onward each per-stage standard versions independently; a pipeline composes a coherent set of per-stage versions.

### Removed

- **All "working-group multi-sig" language from normative requirements.** Affected: RA-1 (recipe signature), RD-1 (rail signature), recipe signature type, rail signature type, recipe-poisoning threat mitigation, validator-set claim text, closed-method rationale, closed-rail-registry rationale, trust-boundary threat-model text. No working group is constituted. References that previously asserted multi-sig governance now describe the steward's signing key, with multi-party governance named as follow-on work in §11.2.6.

- **§7.4.4 recipe sub-authority delegation.** Earlier drafts described sub-authority delegation by domain (sanctions-list sub-authority, financial-regulation sub-authority). No such sub-authorities exist; the structure that would constitute them does not exist. The section now describes the steward's lifecycle responsibilities and the progressive-anchoring path; sub-authority delegation is open work for v0.2+.

- **The §11.1.1 "Demos proposal" sales-pitch material.** What positioned Demos as the substrate and listed actions to be taken with composed-standards maintainers. Substrate and composition stances retained as factual statements in §11.1.4 and §11.1.5; the proposal framing removed.

- **`dacs-bundle:v2:` forward reference.** Premature v2 mention in the v1 spec. Removed.

- **The previous "preserved verbatim for backwards compatibility" note** on the bundle separator. The compatibility concern it cited never materialised (no reference implementation had shipped under the old name).

### Fixed

- **`sr1-root` was referenced but undefined.** Spec referenced the value in §6.3.3's `preferredPresentation` enum and §6.3.4's signature rule but did not define it as a variant of the `PresentationSignature` union. Now defined (see Added).

- **`dacs5-bundle:v1:` broke the universal separator pattern.** The §7.7 registry promised `dacs-<kind>:v<ver>:` for every separator but the DACS-5 bundle separator was an outlier. Renamed to fix (see Changed).

- **`acceptedRails: PaymentRailRef[] // non-empty` was incompatible with intake-only listings.** Sealed-bid government procurements, RFPs, reverse auctions, free services — none of these have a per-listing settlement rail, but the schema required one. Fixed by making the field conditionally optional (see Changed).

- **The `dacs1:…` logical anchor address was not realisable on Demos.** §6.3.4 said "the recommended scheme on Demos uses StorageProgram with address `dacs1:{primaryClaim}:{listingId}:v{n}`," but Demos rejects colons in StorageProgram names. The addressable handle is the sha256-derived `stor-<hex>`. Implementations were correctly using a colon-free native address and carrying the `dacs1:…` string as descriptive metadata; the spec now matches that behaviour. The same logical/native split now applies across all DACS address patterns universally (see Added).

### Governance

- **KyneSys Labs is named as the v0.1 steward** (§7.4.4, §9.4.3, §11.1.1, threat-model trust-boundary text). Single-signer arrangement; progressive-anchoring phase PA-2.
- **PA-2 residual risks acknowledged.** Steward-key compromise is the principal residual risk under PA-2 single-signer governance; multi-signature governance under PA-3 is the v0.2+ mitigation pathway, conditional on the constitution of a multi-party body.
- **PA-3 transition is open work.** §11.2.6 names this explicitly. v0.1 does not specify the constitution mechanism, multi-signature thresholds, sub-authority delegation, or transition procedure.

---

## Earlier drafts (retired)

The following internal numbering is retired and replaced by the v0.1 document-level versioning above:

- **Paper v0.7 + per-stage DACS-1..5 v0.1** — the longest-circulating internal draft. Reviewed by PATH-OS Labs (whose reference implementation `pathos-dacs-ref` was built against this state).
- **Paper v0.8 + per-stage DACS-1..5 v0.2** — a brief consolidation cut that incorporated review-pass revisions (the four-value decision, the universal separator rename, the conditional `acceptedRails`, the logical/native address split, the steward framing). Not externally circulated under this version number.

If you implemented against the v0.7 / v0.1 state and are migrating to v0.1, the **Added** and **Changed** sections above are your migration list.

---

## Format conventions

- Versions follow `v0.MINOR` style during draft phase (v0.1, v0.2, …) and `vMAJOR.MINOR` once a standard reaches v1.0. Each per-stage standard versions independently from the shared v0.1 baseline.
- Breaking changes get a major-version bump (v0.x → v1.0, v1.x → v2.0).
- Additive non-breaking changes get a minor-version bump (v0.1 → v0.2).
- Editorial-only changes (typo fixes, formatting, examples that don't change semantics) do not bump the version.
- Each release entry cites section numbers for every change so implementers can scan against their own code.
