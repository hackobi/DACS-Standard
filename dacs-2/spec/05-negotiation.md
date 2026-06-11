# DACS/2 §5 — DACS-3: Negotiate

## 1. Transport: the DacsEnvelope

v0.1 defined channel *properties* but no wire format; DACS/2 defines both. All agent-to-agent application messages are
`DacsEnvelope`s:

```ts
type DacsEnvelope = {
  dacs: "2"
  channelId: string                 // sha256hex(jobId || ":" || buyer || ":" || seller), spec/00 §3
  jobId: string
  seq: number                       // per-sender monotonic from 1
  from: string, to: string          // "demos:<account>" roots (session keys sign, roots address)
  sentAt: string
  kind: "offer" | "counter" | "accept" | "reject" | "cancel" | "abort"
      | "bundle-present" | "vet-result" | "agreement-cosign" | "settle-notice"
      | "deliver-notice" | "bundle-cosign-request" | "bundle-cosign"
      | "dispute-open" | "dispute-evidence" | "ping"
  body: object                      // normative per kind, §3
  refs?: { repliesTo?: string /* envelope contentHash */ }
  sig: Sig                          // dacs-envelope:v2:
}
```

**Transport bindings (TB-1..TB-3), in preference order:**

- **TB-1 — Demos IM (default).** Envelopes travel E2E-encrypted over the node's IM SignalingServer
  (`register`/`message` WebSocket flow; SDK `@kynesyslabs/demosdk/instant_messaging`), addressed by root account.
  Offline delivery is provided by the signaling layer. **Milestone messages** (`accept`, `cancel`, `abort`,
  `dispute-open`) MUST additionally be hash-anchored with an `instantMessaging` transaction
  (`{targetId, senderId, messageHash = contentHash(envelope)}`) — cheap, non-repudiable ordering evidence.
- **TB-2 — L2PS lane.** For confidential B2B flows, parties with a shared L2PS subnet exchange envelopes as
  `l2psInstantMessaging` payloads; the periodic `l2ps_hash_update` provides the public integrity anchor. Channel
  confidentiality here is subnet-level (AES per-subnet keys), not merely pairwise.
- **TB-3 — HTTPS fallback.** POST the envelope JSON to the counterparty's `endpoints.https.url` (for counterparties
  not running an IM client, e.g. a plain d402-payable API). No anchoring; TB-3 alone cannot carry milestone messages —
  a TB-3-only session MUST anchor milestones via the buyer's `instantMessaging` transactions.

**Channel rules:** CH-1 fixed two-party membership (envelope `from/to` + signature check — enforced
cryptographically, not by transport trust); CH-2 per-sender `seq` strictly monotonic, receivers reject regressions;
CH-3 a channel is bound to one `jobId` forever.

## 2. Negotiation patterns

`negotiate-fixed-price` | `negotiate-rfq` | `negotiate-sealed-envelope` — same trio as v0.1, now with interoperable bodies.

## 3. Normative bodies (the v0.1 "implementation-defined" gap, closed)

```ts
type OfferBody    = { price: PriceTerm, deliverable: DeliverableRef, rail: RailRef, deadline: string,
                      expiresAt: string, bond?: { escrowTxHash: string }, notes?: string }
type CounterBody  = OfferBody                       // a counter is a complete replacement offer
type AcceptBody   = { acceptsEnvelope: string /* contentHash */, agreementHash: string }
type RejectBody   = { rejectsEnvelope: string, reason?: string, final: boolean }
type CancelBody   = { policyRef: "commit" | "pre-settlement" | "pre-delivery", feeAcknowledged?: PriceTerm }
type AbortBody    = { reason?: string }
```

- **NB-1** Every `offer`/`counter` is complete (no diffs): the latest envelope is the entire proposed terms.
- **NB-2** `accept` MUST reference the exact envelope it accepts and carry the hash of the AgreementDocument the
  acceptor derived from it; the counterparty re-derives and MUST get the same hash (deterministic derivation, §4).
- **NB-3** RFQ defaults: `maxTurns = 6` (≥2), `timeoutSec` per listing; turn limit counts `offer|counter` only.

## 4. AgreementDocument and the accept rule

```ts
type AgreementDocument = {
  dacs: "2", jobId: string
  listingRef: { listingId, listingVersion, contentHash, programAddress }
  parties: [ { role: "buyer", root, bundleHash, sessionNonce }, { role: "seller", root, bundleHash, sessionNonce } ]
  terms: { deliverable: DeliverableRef, price: PriceTerm, rail: RailRef, deadline: string,
           cancellation?: CancellationPolicy, optionFee?: PriceTerm /* spec/06 §5 */, pairSalt?: string /* AD-5 */ }
  derivedFrom: { pattern: "fixed-price" | "rfq" | "sealed-envelope", envelopeHash: string }
  generatedAt: string
  signatures: Sig[]                 // both parties, dacs-agreement:v2:
}
```

**Accept rule (AR-1, deterministic):** an agreement is listing-conformant iff currency matches; price within
`[bandCenter×(100−minPct)/100, bandCenter×(100+maxPct)/100]` (half-up rounding to bandCenter's CD-1 digits) for
`negotiable`, equal for `fixed`, ≥ reserve for `auction`; rail ∈ `acceptedRails`; deliverable hash equals the
listing's; deadline ≤ commit-block-time + `deadlineSecAfterCommit`; and commit-block-time within listing validity.
Both sides MUST evaluate AR-1 before signing. Because `maxPct` is finite (PRC-1), the ceiling check is symmetric.

**Auto-accept** (fixed-price): the seller MAY pre-publish an `AutoAcceptCommitment {listingRef, validUntil, sig}`
(`dacs-auto-accept:v2:`); a buyer presenting a conformant agreement + the commitment gets a binding agreement when the
seller's live countersignature over `agreementHash || commitmentHash` arrives — unchanged from v0.1 in substance.

## 5. Sealed-envelope auctions

Carried over from v0.1 with anchoring re-based on Storage Programs: bid commitment
`bidHash = sha256("dacs-sealed-bid:v2:" || contentHash(bid) || salt)` (salt ≥ 256-bit); bidders anchor commitments in
their **own** programs `(bidder, "dacs2:bid:{jobId}")` before `commitDeadline` (block time, TS-1); reveals append
`{bid, salt}` within `revealWindow`; selection is deterministic from the revealed set
(`lowest-price | highest-price | first-acceptable | rule-ref:<contentHash>`). Since there is no orchestrator, **any
party can recompute the winner**; the seller's `accept` envelope to the winner + AR-1 close the loop. Late or
malformed reveals are simply excluded. Bidder admission MAY require `listingBond` (spec/04 §6).

## 6. Commitment

Buyer deploys `(buyer, "dacs2:commit:{jobId}")` containing the `CommitmentRecord {dacs:"2", jobId, agreementHash, listingRef, parties, committedAt}`
co-signed by both (`dacs-commitment:v2:`). CA rules unchanged: no settlement before the commit anchors; the agreement
body itself is not anchored publicly (only its hash) unless the parties choose to; re-commit for a `jobId` is invalid.
The commit transaction's block time is the session's normative T0 (TS-1).

## 7. Transcript

`ChannelTranscript {dacs:"2", channelId, members, envelopes: DacsEnvelope[], generatedAt, signatures}` — assembled by
either party on demand; disclosure policy per listing (`none` default | `encrypted-anchored`). Milestone anchors
(TB-1) make selective transcript forgery detectable even under `none`.
