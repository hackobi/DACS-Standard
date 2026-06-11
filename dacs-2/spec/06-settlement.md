# DACS/2 §6 — DACS-4: Settle

## 1. Pipeline rules

Carried over from v0.1 (PIPE-1..PIPE-5): ≥1 deliver-* phase; pay-* optional; declared order normative; pay↔deliver
gating per order; repeated pay-* phases settle the same agreed price. Added:

- **PIPE-6** A pipeline containing `pay-demos-escrow` or `pay-demoswork-conditional` is **delivery-gated**: funds lock
  before delivery and release on delivery evidence (or refund on expiry). Listings SHOULD prefer these rails wherever
  the deliverable is machine-verifiable; plain pay-then-deliver / deliver-then-pay pipelines MUST disclose which party
  bears counterparty risk in `offering.description`.

## 2. Rails (closed registry, steward-group governed)

| `railId` | Mechanism (L1 binding) | Finality model | Availability note |
|---|---|---|---|
| `demos-native` | `native` send (`{nativeOperation:"send", args:[to, amountOS]}`) via two-phase confirm/broadcast | `demos-block` | live |
| `demos-d402` | `d402_payment {to, amount, memo}`; SDK `D402Client.createPayment/settle`, `D402Server.require/verify` | `demos-block` | live |
| `demos-escrow` | `escrow` tx → `GCREditEscrow {deposit / claim / refund, expiryDays}`; SDK `EscrowTransaction.sendToIdentity / claimEscrow` | `demos-block` (per edit) | **gate: `escrowEnabled`** (GCR handler is a stub on all current branches incl. `stabilisation` — bindings/demos-node.md §6/§7; SDK-side support is complete) |
| `demoswork-conditional` | `demoswork` tx: `DemoScript` conditional — DAHR/TLSN delivery predicate → native pay step | `demos-block` | gate: `demosworkEnabled` |
| `bridge-usdc` | `nativeBridge` USDC (EVM ⇄ Solana ⇄ Demos), compiled via the `nativeBridge` RPC method | `bridge-release` | gate: `bridgeEnabled` |
| `xm-pay` | `crosschainOperation` XMScript `pay` task on evm/solana/aptos/btc/near/ton/xrp/multiversx/ibc | foreign-chain `block-depth` | live; **sequential best-effort, never atomic** (XM-1) |
| `cross-chain-htlc` | HTLC contracts on the two legs; preimage = HKDF-SHA256(IKM=buyerSalt, salt=jobId, info=agreementHash) | `htlc-reveal` | live where contracts deployed |
| `evm-erc20` / `solana-spl` | direct foreign-chain transfer | `block-depth` | live; SB-2 binding REQUIRED |
| `x402` | external x402 HTTP flow | `provider-receipt`(+`settlementTxHash`) | composition rail |
| `ap2` | external AP2 fiat mandate | `provider-receipt` | composition rail |

- **XM-1** XM outcomes are `all_ops_ok | partial_success | all_ops_failed`; `partial_success` maps to
  `errorClass: "settlement-atomicity"` and enters `settle-asymmetric` handling (spec/07 §2). Pipelines needing
  atomicity MUST use `cross-chain-htlc` or `demos-escrow`, not `xm-pay`.
- HTLC rules HTLC-1..HTLC-10 are carried over from v0.1 verbatim (canonical topology, absolute-expiry timelock
  inequality, HTLC-9 asymmetric state, HTLC-10 free-option disclosure). New: **HTLC-11** — the agreement MAY price the
  free option as `terms.optionFee`, a non-refundable `demos-d402` micro-payment from payer at lock time, evidenced
  like any payment.

## 3. Delivery phases

`deliver-storage-program` (deliverable written to an ACL'd program readable by buyer; evidence = program address +
contentHash) | `deliver-ipfs` (ipfs tx, CID + contentHash, cost-capped) | `deliver-entitlement` (EntitlementRecord,
schema unchanged from v0.1) | `deliver-attested-payload` (payload + DAHR or TLSNotary attestation of the delivering
fetch/response — TLSNotary REQUIRED when the listing marks delivery `attestation: "strong"`).

## 4. Session binding (SB-1..SB-4) — closes the v0.1 replay gap

Every settlement transaction MUST be cryptographically or structurally bound to the session. A `SettlementEvidence`
whose underlying transaction is unbound is invalid (not merely weak):

- **SB-1 (memo rails)** `demos-d402`: `memo` MUST equal `dacs2:{jobId}:{first16hex(agreementHash)}`. `demos-native`:
  the same string in the transaction's data payload where the type supports it, else SB-4.
- **SB-2 (address rails)** `evm-erc20` / `solana-spl` / `bridge-usdc`: payment MUST go to a **session-unique deposit
  address** declared by the payee in the agreement (`rail.parameters.depositAddress`, derived per session), or carry
  the SB-1 string in calldata/memo where the chain supports it. Evidence MUST state which binding was used.
- **SB-3 (preimage rails)** `cross-chain-htlc` binds via the jobId/agreementHash-derived preimage (HTLC-3). No
  further binding needed.
- **SB-4 (script rails)** `demoswork-conditional` and `demos-escrow`: the DemoScript / escrow payload embeds `jobId`
  (escrow `message` field; DemoScript operation params). The GCR-edit determinism of the node (client and node both
  derive edits and hash-compare) makes this binding consensus-checked.

Verifiers MUST check the binding when validating evidence: resolve the referenced tx (`getTxByHash` or foreign-chain
RPC) and confirm the binding material. One transaction MUST NOT satisfy evidence in two sessions (the binding makes
this mechanically checkable).

## 5. Escrow semantics (`demos-escrow`)

- **ES-1 deposit**: payer escrows `amount` with `expiryDays` ≥ the pipeline's delivery deadline + 2 days, `message`
  carrying the SB-4 binding. Recipient is identified by Demos account or by social handle
  (`platform`, `username`) — the node's deterministic social-escrow address lets agents pay counterparties who haven't
  onboarded yet; claiming then requires the matching chain-native identity (spec/02 §1).
- **ES-2 claim**: seller claims after anchoring delivery evidence; the claim evidence references the delivery
  evidence hash.
- **ES-3 refund**: payer refunds after `expiryDays` if no claim occurred. Refund is an actual value movement
  (GCREditEscrow refund), not just an amendment record — the v0.1 "refunds are evidence of refunds" gap is closed on
  this rail.
- **ES-4** Claim/refund races resolve by chain ordering; evidence records the winning edit.

## 6. SettlementEvidence and amendments

Schema carried over from v0.1 (`jobId`, `phase`, `outcome: success|failure`, `paymentTxRefs`, `paymentAmount` required
on success, `deliverableContentHash/Anchor`, `settlementFinality {model, …}`, `observedAt`, `sig`) with amendments:

- **EV-1** New `binding: {rule: "SB-1"|"SB-2"|"SB-3"|"SB-4", material: string}` — REQUIRED on every pay-* evidence.
- **EV-2** `ChainTxRef` gains `demos-escrow {depositTxHash, claimTxHash?, refundTxHash?}` and
  `demoswork {txHash, stepResults}` variants; `liquidity-tank` is replaced by `bridge {bridgeId, originChain, destinationChain, lockTxHash, releaseTxHash?}`.
- **EV-3** Evidence anchors at `(executor, "dacs2:evidence:{jobId}:{phaseIndex}")` (AD-2) and is signed by the phase
  executor (spec/00 §4); the counterparty acknowledges via `settle-notice`/`deliver-notice` envelope, and that
  acknowledgement hash is included in both bundles.
- `SettlementAmendment` (refund / partial-refund / correction; Σ refunds ≤ paymentAmount, same currency) is unchanged;
  on `demos-escrow` an amendment MUST reference the on-chain refund edit.

## 7. Quote/commit at the node edge

The node's two-phase `confirmTx → ValidityData (RPC-signed) → broadcastTx` applies to every Demos-side transaction.
Implementations SHOULD retain `ValidityData` for settlement transactions: it is an RPC-signed pre-execution quote
(gas, reference block) and is admissible DACS-6 evidence of what a node committed to execute.
