# DACS/2 §8 — DACS-6: Resolve

v0.1 deferred disputes entirely ("handled out-of-band"); DACS/2 specifies a minimal, evidence-first resolution stage.
Scope: structured dispute records, credentialed arbitration, and outcome artifacts that reputation derivers honor.
Non-goals: on-chain enforcement of arbitral awards (awards bind via escrow where used, and via reputation otherwise),
and legal effect (jurisdiction terms live in the listing).

## 1. Triggers

A dispute MAY be opened by either party when any of:

- **DT-1** Divergent bundles: both parties anchored signed bundles for the same `jobId` with different contentHashes (BD-3).
- **DT-2** Unresolved `settle-asymmetric`: the binding expiry passed with value stranded on one leg (HTLC-9, XM partial).
- **DT-3** Amendment violation: refunds exceeding `paymentAmount`, or a refund promise (cancellation `feePct`,
  escrow ES-3) not honored.
- **DT-4** Delivery contested: buyer disputes that anchored delivery evidence satisfies the agreed `DeliverableRef`.
- **DT-5** Classification contested: un-counter-acked `errorClass` divergence (FA-1).

## 2. DisputeRecord

```ts
type DisputeRecord = {
  dacs: "2", jobId: string
  opener: string, respondent: string            // roots
  trigger: "divergent-bundles" | "settle-asymmetric" | "amendment-violation" | "delivery-contested" | "classification-contested"
  claims: string                                 // ≤4000 chars, opener's statement
  evidence: EvidenceRef[]                        // §3
  requestedOutcome: "refund" | "partial-refund" | "complete-delivery" | "reclassify" | "release-escrow" | "declaratory"
  arbitrator?: string                            // root; from listing.terms.arbitrators or mutually agreed
  openedAt: string
  sig: Sig                                       // dacs-dispute:v2:
}
```

- **DR-1** Anchored at `(opener, "dacs2:dispute:{jobId}")` and sent as a `dispute-open` envelope (milestone — TB-1
  anchoring REQUIRED).
- **DR-2** One dispute program per `jobId` per opener; additional material is appended, not re-deployed.

## 3. Evidence

`EvidenceRef = {kind, contentHash, anchor}` where kind ∈ artifact kinds plus `envelope`, `transcript`, `validity-data`,
`chain-tx`. The evidentiary base is exactly what the protocol already produced — listings, agreements, commit anchors,
settlement evidence with SB bindings, milestone envelope anchors, ValidityData quotes, TLSNotary proofs. **EV-D1**:
arbitrators MUST disregard unanchorable evidence (unsigned envelopes, unverifiable transcripts) except as context.
Parties respond with `dispute-evidence` envelopes appended to their own dispute/bundle programs.

## 4. Arbitrators

- **AR-1** An arbitrator is a DACS seller whose listing category is `service.arbitration.*`, credentialed via
  DACS-1/2 like any seller (institutional claims expected; e.g. bar membership via `stor-cred:` or VC).
- **AR-2** Selection precedence: (1) `listing.terms.arbitrators` (pre-agreed at commit time — strongly RECOMMENDED for
  escrowed flows), (2) mutual agreement post-dispute, (3) none — the dispute record stands as a public, structured
  disagreement, which is still strictly better than v0.1's silence: derivers count it (REP-4 `disputeRate`) on both
  parties symmetrically until an outcome exists.
- **AR-3** Arbitration is a paid DACS session itself (typically `demos-d402`), giving arbitrators an enumerable track
  record of their own.

## 5. DisputeOutcome

```ts
type DisputeOutcome = {
  dacs: "2", jobId: string, disputeRef: string
  finding: "for-opener" | "for-respondent" | "split" | "no-fault" | "unresolvable"
  reclassification?: { phaseIndex: number, errorClass: ErrorClass }[]   // overrides FA-1 exclusions
  monetary?: { direction: "opener" | "respondent", amount: PriceTerm, satisfiedBy?: ChainTxRef }
  reasoning: string                              // ≤8000 chars
  decidedAt: string
  sig: Sig                                       // arbitrator; dacs-dispute-outcome:v2:
}
```

- **DO-1** Anchored by the arbitrator at `(arbitrator, "dacs2:dispute-outcome:{jobId}")`, referenced from both
  parties' dispute programs.
- **DO-2** Where the session used `demos-escrow` and funds are still locked, the outcome is enforceable in-protocol:
  the parties (or the escrow's expiry mechanics) execute the matching claim/refund, and `monetary.satisfiedBy` records
  it. Elsewhere, compliance is voluntary; non-compliance after a signed outcome is itself derivable
  (outcome present, `satisfiedBy` absent past deadline) and weighs as `disputeRate` against the non-compliant party only.
- **DO-3** Reputation effect: derivers MUST apply `reclassification` entries when present, count `finding` against the
  losing party's `disputeRate`, and stop counting the dispute against the prevailing party.

## 6. Lifecycle interaction

Disputes do not reopen terminal sessions; they annotate them. A session in `settle-asymmetric` MAY proceed to its
ST-6 resolution concurrently with a dispute. Bundles finalised before an outcome are not rewritten — the outcome is a
separate, later artifact that derivers join by `jobId` (append-only history, no retroactive mutation; this avoids the
v0.1 prototype's retired correction-amendment confusion).
