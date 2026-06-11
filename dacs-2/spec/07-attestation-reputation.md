# DACS/2 §7 — DACS-5: Verify

## 1. Outcomes

`completed | cancelled | failed-perm | failed-counterparty | failed-substrate | aborted-by-self | aborted-by-other`

`cancelled` is new: a policy-compliant cancellation (spec/04 §3). It is reputation-neutral in fault metrics and
counted in a separate rate (§6).

## 2. Session state machine (ST-1..ST-8, revised)

States: `draft → vetting → negotiating → committed → settling ⇄ settle-asymmetric → finalising → finalised`, plus
terminals `vet-failed`, `negotiate-failed`, `commit-failed`, `settle-failed`, `cancelled`, `aborted-by-self`,
`aborted-by-other`, `failed-substrate`, and the pause state `substrate-paused`.

- **ST-1** Transitions are forward-only along the pipeline; each party evaluates the machine independently from
  anchored facts (commit anchor, evidence anchors, milestone envelope anchors).
- **ST-2** A phase `ok:false` moves to that stage's `*-failed`, classified by `errorClass`
  (`permanent → failed-perm`, `counterparty → failed-counterparty`, `substrate → failed-substrate` after pause
  exhaustion, `settlement-atomicity → settle-asymmetric`).
- **ST-3** `abort` envelope at any pre-terminal state → `aborted-by-self` (sender) / `aborted-by-other` (receiver).
  A party's right, not a violation.
- **ST-4** `cancel` envelope: if compliant with the agreement's `cancellation` policy (including fee payment when
  `feePct` applies) → `cancelled`; otherwise it is an `abort`.
- **ST-5** `substrate-paused`: max 3600 s cumulative, then `failed-substrate` (reputation-neutral).
- **ST-6** `settle-asymmetric` (HTLC-9 / XM `partial_success`) resolves forward to `settling` (completion) or, at the
  binding expiry, to `settle-failed` with `errorClass: settlement-atomicity`; never silently to `finalised`.
- **ST-7** `rate` is optional and non-fatal; no `rate-failed` exists.
- **ST-8** Terminal-state → outcome mapping is total and unique (table in schema `attestation-bundle.schema.json`).

## 3. Fault attribution (FA-1) — shortening the v0.1 fragility chain

`errorClass` is asserted by the phase executor, but it only **counts** when counter-signed: each bundle's
`phaseSummary` entry carries `counterAck: contentHash(notice envelope) | null`. Entries with `counterAck: null` where
the counterparty's bundle disagrees on `errorClass` are excluded from fault metrics (they remain visible as
divergence and feed DACS-6). Two honest implementations can therefore disagree on classification without silently
poisoning reputation.

## 4. AttestationBundle (two-sided)

Schema substantially carried over from v0.1 (`jobId`, `outcome`, `listingRef`, `agreementRef`, `parties`,
`phaseSummary[]` with `counterAck`, `vetRecords`, `settlementEvidence`, `amendments?`, `ratingRefs?`,
`registryVersion`, `finalisedAt`, `signatures`), re-based on L1:

- **BD-1** Each party deploys its own bundle program `(party, "dacs2:bundle:{jobId}")` (AD-2) and writes its signed
  copy. The two copies SHOULD be byte-identical except `anchoredByRole` (excluded from contentHash — the v0.1 R5-1
  lesson is preserved as a MUST: role markers are never hashed).
- **BD-2** Co-signing: `bundle-cosign-request` / `bundle-cosign` envelopes exchange signatures over the shared
  contentHash. One-sided bundles are valid for the abort/failure outcomes that don't require counterparty consent.
- **BD-3** Divergent copies (same `jobId`, different contentHash, both signed) are the canonical DACS-6 trigger.

## 5. Why the bundle set is enumerable (the completeness oracle, REP-C)

Because BD-1 bundles are Storage Program transactions **from the party's own account**, the chain enumerates them:

> **REP-C** A reputation deriver MUST construct the bundle set for party P by enumerating P's `storageProgram`
> transactions (`getTransactionHistory(P, "storageProgram")` or equivalent index) filtered to `programName` prefix
> `dacs2:bundle:`, over the window. A derivation whose `bundleRefs` omits an enumerable bundle, or includes a
> non-enumerable one, is invalid.

This closes v0.1's acknowledged gap ("reproducible but not complete"): omitting negative history is now detectable by
anyone replaying the enumeration. AD-5 salted sessions are the exception by construction: their bundles enumerate
(the tx is visible) but don't parse without the salt; derivers MUST count unparseable `dacs2:bundle:`-prefixed
programs in `privateBundleCount` so consumers see how much history is opaque.

## 6. Reputation derivation

Carried over from v0.1 (per-root keying, two-sided reconciliation with `perspective_flip`, divergence-as-exclusion,
rating de-dup per `(rater, jobId, targetRole)`, null ≠ zero, determinism receipt) with amendments:

- **REP-1** Windowing basis is solely the bundle-anchoring **block timestamp** (TS-1). The v0.1 dual basis is removed.
- **REP-2** Fault denominator = terminal outcomes − `failed-substrate` − `cancelled` − `aborted-by-other`.
  `abortRate` (self) and `cancelRate` are reported as separate metrics; `aborted-by-other` no longer dilutes the
  victim's completionRate (the v0.1 griefing surface).
- **REP-3** `verifiedVolume` replaces self-declared volume: per currency, the sum of `paymentAmount` across
  success-evidence whose SB binding the deriver re-verified on-chain (spec/06 §4). Unverifiable evidence contributes
  zero. Sybil sessions now cost real, burned fees (network fee + anchoring + 1 DEM per L2PS tx) per fake unit of
  volume; this raises the floor without claiming to eliminate collusion (out of scope, spec/00 §5).
- **REP-4** Metrics: `completionRate`, `disputeRate` (DACS-6 records against P), `abortRate`, `cancelRate`,
  `averageBuyerRating`, `averageSellerRating`, `verifiedVolume[]`, `bundleCount`, `privateBundleCount`.
- **REP-5** Derivations are signed by the deriver and reproducible: `(party, window, registryVersion, saltSet)` →
  byte-identical output. Catalog mirrors surfacing reputation MUST attach the derivation, not just numbers.

## 7. Ratings

`RatingRecord` unchanged from v0.1 (1–5 integer, ≤1000-char freeText, opaque dimensions; `dacs-rating:v2:`), anchored
at `(rater, "dacs2:rating:{jobId}")`. Ratings without a finalised bundle for the same `jobId` are ignored by derivers.
