# DACS/2 §4 — Discovery and Listings

## 1. Listing

```ts
type Listing = {
  dacs: "2"
  listingId: string                       // ≤128 URL-safe ASCII, unique per seller
  listingVersion: number                  // monotonic
  seller: { root: string, bundle: IdentityBundle, displayName: string, endpoints: Endpoints }
  offering: {
    title: string, description: string
    category: string                      // dot-delimited taxonomy, e.g. "data.financial.feeds"
    tags: string[]                        // ≤16 × ≤32 chars
    deliverable: DeliverableSpec          // storage-program | ipfs | entitlement | attested-payload | external
    extendedDescription?: Anchor          // AD-3; hash-bound
  }
  buyerRequirement: BundleRequirement     // spec/02 §4
  pipeline: PhaseStep[]                   // declared order is normative (PIPE rules, spec/06 §1)
  pricing: PricingSpec                    // §4
  acceptedRails: RailRef[]                // REQUIRED iff pipeline contains any pay-* phase
  terms: {
    deadlineSecAfterCommit?: number
    acceptanceModel?: "auto-accept"       // spec/05 §4
    cancellationPolicy?: CancellationPolicy   // §3 — now normative, not informational
    listingBond?: PriceTerm               // §6
    jurisdictions?: string[], termsOfService?: Anchor
    arbitrators?: string[]                // pre-agreed arbitrator roots for DACS-6 (spec/08)
  }
  validity: { notBefore: string, notAfter?: string }
  status: "active" | "paused" | "revoked" // mutable program field, outside contentHash (§2)
  signature: Sig                          // dacs-listing:v2: over all fields except status & signature
}
type Endpoints = {
  im?: { signalingUrl: string }           // Demos IM SignalingServer (default transport)
  l2ps?: { uid: string }                  // private subnet lane
  https?: { url: string }                 // fallback envelope POST endpoint
}
```

Canonical-form cap: 16 KB (unchanged); larger content goes behind `extendedDescription`.

## 2. Listings are Storage Programs (LP-1..LP-4)

- **LP-1** A listing lives in the program `(sellerAccount, "dacs2:listing:{listingId}")` (AD-2), deployed and owned by
  the seller, ACL `{mode: "public"}` for reads, owner-only writes. Fields:
  `current` (the Listing JSON), `versions` (append-only list of `{listingVersion, contentHash, blockAnchor}`), `status`.
- **LP-2** Publishing version N: `SET_FIELD current`, `APPEND_ITEM versions`. The version history is tamper-evident:
  each append is a chain transaction from the seller's account.
- **LP-3** **Revocation** is `SET_FIELD status = "revoked"` (optionally per-version notes in `versions`). v0.1's
  separate revocation-marker anchor is removed. Clients MUST read `status` at session start; a session committed while
  `active` is unaffected by later revocation.
- **LP-4** Clients MUST verify `contentHash(current)` matches the latest `versions` entry and the signature verifies
  under the seller root (or bound PQC key) before relying on a listing. Reads are free REST:
  `GET /storage-program/:address/field/current`.

## 3. Cancellation policy (normative)

```ts
type CancellationPolicy = { allowedUntil: "commit" | "pre-settlement" | "pre-delivery", feePct?: string /* CD-1, of agreed price */ }
```

A `cancel` envelope (spec/05 §3) compliant with the policy leads to terminal state `cancelled` — reputation-neutral
(spec/07). Non-compliant cancellation is an `abort` with normal reputation consequences. v0.1 had no such path; every
legitimate cancellation read as a reputational abort.

## 4. Pricing

`PricingSpec = {model:"fixed", price: PriceTerm} | {model:"negotiable", bandCenter: PriceTerm, minPct: string, maxPct: string} | {model:"auction", reservePrice?: PriceTerm, selectionRule: SelectionRule}`

- `PriceTerm = {amount: string /* CD-1, base units: OS for DEM */, currency: "DEM" | "USDC" | <registry asset>, unit?: string}`
- **PRC-1** `minPct, maxPct` are CD-1 with `0 ≤ minPct < 100` and `maxPct` **finite** and declared. (v0.1 left the
  band unbounded upward; the accept-rule ceiling is now checkable by both sides — spec/05 §4.)

## 5. Agent card and search

- **Card:** sellers SHOULD publish `.well-known/agent.json` with an additive `dacs` block:
  `{dacs: "2", root, profiles: ["dacs2-demos/settle", …], listings: {deployer, programNames: string[]}, endpoints}` —
  pointers only; the chain is authoritative.
- **On-chain search (primary):** free REST `GET /storage-program/search/:name` with the `dacs2:listing:` prefix and
  `GET /storage-program/owner/:address` enumerate listings without any indexer.
- **Catalog mirrors (secondary):** operators MAY serve filtered/ranked views (category, rail, price, reputation
  hints). Mirrors are non-authoritative: clients MUST re-resolve the program and re-verify LP-4 before binding.
  Reputation hints follow spec/07 §6 and carry `computedAt` + the deriver's signature.

## 6. Listing spam and bidder admission

- **SP-1** Listing creation costs real chain fees (program creation + per-chunk storage fees) — the economic floor.
- **SP-2** A listing MAY set `terms.listingBond`: bidders/buyers must place a refundable escrow deposit
  (`pay-demos-escrow` deposit with `expiryDays`) before the seller is obliged to negotiate. Bond evidence travels in
  the first `offer` envelope. This is the standard's admission-control hook for RFQ-flood and commit-spam DoS;
  residual DoS below the bond threshold remains out of scope (spec/00 §5).
