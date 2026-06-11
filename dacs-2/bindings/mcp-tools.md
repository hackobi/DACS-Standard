# DACS/2 Binding: MCP Commerce Tools

The Demos node embeds an MCP server (`createDemosMCPServer`, stdio + SSE at `/sse`, discovery at `GET /mcp`), today
exposing read-only chain tools. This binding defines the **DACS/2 commerce tool surface** so any MCP-capable agent can
transact without linking the SDK directly. Status: proposed extension to the node's `demosTools.ts`; tool names are
normative once shipped.

Conventions: all amounts CD-1 OS strings; all hashes lowercase sha256 hex; errors return
`{ok: false, errorClass, reason}` mirroring `PhaseResult`. Tools marked **[signing]** require the MCP host to hold a
session key (spec/02 §3) or wallet; nodes MUST NOT custody user keys for these tools — they accept pre-signed
transactions or operate in prepare/execute pairs.

## Discovery and identity (read-only)

| Tool | Input → Output |
|---|---|
| `dacs_search_listings` | `{category?, tags?, rail?, maxPriceOS?, sellerRoot?}` → `{listings: [{listingId, seller, title, price, programAddress, contentHash}]}` — wraps `/storage-program/search` + LP-4 verification |
| `dacs_get_listing` | `{programAddress \| (sellerRoot, listingId)}` → `{listing, status, versions, verified: boolean}` |
| `dacs_get_identity` | `{root}` → `{claims: BundleClaim[], identityTier, revocations}` — wraps `getAddressInfo` + revocation program read |
| `dacs_get_reputation` | `{root, windowStart, windowEnd}` → signed `ReputationDerivation` (REP-C enumerated) |
| `dacs_verify_artifact` | `{artifact, kind}` → `{valid, contentHash, errors[]}` — L0 verification (schema + separator + signature) |
| `dacs_verify_bundle_set` | `{jobId}` → `{copies: [{deployer, contentHash}], divergent: boolean}` |

## Session lifecycle

| Tool | Input → Output |
|---|---|
| `dacs_open_session` | `{listingRef, buyerBundle}` → `{jobId, channelId}` — validates requirement match (MA rules) before opening |
| `dacs_send_envelope` **[signing]** | `{envelope}` → `{delivered, anchored?, txHash?}` — TB-1 transport + milestone anchoring |
| `dacs_poll_envelopes` | `{channelId, sinceSeq}` → `{envelopes[]}` |
| `dacs_derive_agreement` | `{jobId, acceptedEnvelopeHash}` → `{agreement, agreementHash, ar1: {conformant, violations[]}}` — deterministic NB-2/AR-1 evaluation |
| `dacs_commit` **[signing]** | `{agreement, signatures}` → `{commitProgramAddress, txHash, t0BlockTime}` |
| `dacs_vet` | `{root, requirement}` → `{composite: CompositeVerificationRecord}` — chain-native via ID-1; authority claims via recipes (TF-1 enforced; uses node TLSNotary/DAHR) |

## Settlement

| Tool | Input → Output |
|---|---|
| `dacs_quote` | `{jobId, rail}` → `{validityDataPreview?, fees, gates: {railAvailable, reason?}}` — §6 feature-gate probe + node confirm-phase quote |
| `dacs_pay` **[signing]** | `{jobId, rail, signedTx \| paymentIntent}` → `{evidence: SettlementEvidence, txHash}` — enforces SB-1..SB-4 binding construction; refuses unbound payments |
| `dacs_escrow` **[signing]** | `{jobId, op: "deposit"\|"claim"\|"refund", params}` → `{evidence, txHash}` — gate-checked (`escrowEnabled`) |
| `dacs_deliver` **[signing]** | `{jobId, deliverable: {kind, content \| anchor}, attestation?: "dahr"\|"tlsnotary"}` → `{evidence, anchor}` |
| `dacs_verify_settlement` | `{evidenceHash \| (jobId, phaseIndex)}` → `{valid, bindingChecked, finality}` — re-resolves the tx and SB binding |

## Finalisation and disputes

| Tool | Input → Output |
|---|---|
| `dacs_finalise` **[signing]** | `{jobId}` → `{bundle, programAddress, cosignStatus}` — assembles the caller's bundle copy, runs the cosign envelope exchange |
| `dacs_rate` **[signing]** | `{jobId, value (1-5), freeText?}` → `{ratingAnchor}` |
| `dacs_open_dispute` **[signing]** | `{jobId, trigger, claims, requestedOutcome, arbitrator?}` → `{disputeAnchor}` |
| `dacs_dispute_status` | `{jobId}` → `{record, evidence[], outcome?}` |

## Security notes

- **MT-1** The MCP server is an interface to the caller's own agent logic, not a trusted third party: every output an
  agent relies on is independently re-verifiable via the L1 reads in [demos-node.md](demos-node.md).
- **MT-2** Hosts SHOULD scope session keys per `jobId` (PR-2) so a compromised MCP host bounds losses to one session.
- **MT-3** Nodes exposing the commerce tools over SSE MUST apply the standard RPC rate limits and SHOULD require a
  d402 payment for `dacs_vet` (it consumes TLSNotary tokens, which the node buys).
