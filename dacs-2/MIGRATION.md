# Migration: DACS v0.1 → DACS/2

This document maps v0.1 concepts to their DACS/2 replacements and records the disposition of every known v0.1 defect.
Domain separators bump from `:v1:` to `:v2:`; v0.1 and DACS/2 artifacts are not cross-verifiable by design.

## 1. Concept mapping

| v0.1 | DACS/2 | Notes |
|---|---|---|
| SR-1..SR-5 substrate requirements | L1 Demos binding | Abstract capabilities replaced by concrete node surfaces. SR-3 → DAHR + TLSNotary; SR-4 → IM/L2PS envelope transport; SR-2 → Storage Programs; SR-5 → HTLC + nativeBridge + escrow. |
| Orchestrator | (removed) | Peer-driven sessions; per-phase executor responsibility (spec/00 §4). Third-party facilitators are ordinary DACS sellers. |
| `IdentityBundle` 4 presentation kinds (SIWD / per-claim / session-key / sr1-root) | 2 kinds: `demos-account`, `session-key` | SIWD required a Demos wallet to verify; `demos-account` verifies via the open `getAddressInfo` RPC read instead. |
| CCI claims verified via VerifyResults | **Chain-native claims** read directly from GCR | `cci-*` claims are on-chain state; freshness = chain head. VerifyResults remain for **authority claims** (lei, finra-crd, …). |
| `dacs1-revoked:` revocation marker anchor | `status` field on the listing Storage Program | Listings are mutable programs; revocation is a `SET_FIELD`. |
| `ChannelMessage` (body implementation-defined) | `DacsEnvelope` with normative bodies | offer/counter/accept/reject/cancel/abort bodies are specified (spec/05 §3). |
| PhaseTypes `pay-evm-erc20`, `pay-solana-spl`, `pay-ap2`, `pay-x402` | Retained, plus session-binding rules SB-1..SB-4 | Unbound rails were the replay gap; now every rail MUST bind to `jobId`. |
| (no escrow) | `pay-demos-escrow`, `pay-demoswork-conditional` | Escrow availability-gated per network (node GCR handler maturity). |
| `pay-cross-chain-liquidity-tank` | `pay-bridge-usdc` (nativeBridge) | Binds to the node's actual USDC bridge instead of testnet tank contracts. |
| `SettlementAmendment` refund (evidence-only) | Retained; escrow rail adds an actual refund mechanism (`GCREditEscrow refund`) | |
| AttestationBundle anchored at `stor-{sha256(jobId+"-bundle-"+role)}` | Storage Program deployed by each party: `deriveStorageAddress(party, "dacs2:bundle:{jobId}", …)` | Fixes DACS-VERIFY-0003; enables the completeness oracle. |
| Reputation: no completeness oracle | REP-C completeness rule via `getTransactionHistory` | Omitted negative history is detectable on-chain. |
| `observedTransactionalVolume` (self-declared, weak) | `verifiedVolume` from on-chain settlement txs | Derivers re-check the bound settlement transactions. |
| PA-2 single steward | Steward group via Storage Program ACL `groups` + M-of-N artifact co-signatures | PA-3 now has a mechanism, not just a name. |
| DACS-X (prototype fixtures only) | DACS-6 Resolve (normative) | spec/08. |
| Outcomes (no `cancelled`) | Adds `cancelled` terminal outcome | Policy-compliant cancellation is reputation-neutral. |
| Listing signature algorithms `ed25519 / ecdsa-secp256k1 / sr1-aggregate` | `ed25519 / falcon / ml-dsa` | Matches node `SigningAlgorithm`. secp256k1 keys participate as `cci-xm` claims, not artifact signers. |
| Catalog API (read-only hints) | Retained as non-authoritative mirror of on-chain listing programs; free REST reads are primary | `/storage-program/search` is the canonical query surface. |
| §14 conformance plan (prose) | JSON Schemas + binding tables | Machine-validatable artifacts. |

## 2. Disposition of known v0.1 defects

| Defect | Disposition in DACS/2 |
|---|---|
| **DACS-VERIFY-0001** — `cci-lei:` claim does not satisfy a bare `lei` requirement (exact-scheme `find_claim` vs two-axis registry) | Fixed: normative scheme-alias table (spec/01 §6). A requirement scheme matches its own name and all registered aliases; `lei` ≡ `cci-lei`, etc. |
| **DACS-VERIFY-0002** — separator-registry drift | The v2 registry is closed, machine-listed in spec/01 §4, and every schema carries its separator in a `$comment`; CI SHOULD diff schemas against the registry. |
| **DACS-VERIFY-0003** — spec-derived `stor-<64hex>` addresses do not resolve on the node (`stor-<40hex>`, deployer+nonce keyed) | Fixed: the only normative addressing rule is the node's `StorageProgram.deriveStorageAddress(deployer, programName, nonce, salt)` (spec/01 §7). No DACS-side digest addressing remains. |
| Happy-path vector schema divergence (`agentId/serviceId`, wrong composite separator, foreign evidence shape) | v0.1 vectors are not carried forward. DACS/2 vectors MUST validate against `schemas/` before publication. |
| `validate_conformance_vectors.py` approximated JCS | DACS/2 requires a true RFC 8785 implementation in tooling; sorted-key JSON is non-conformant (spec/01 §2). |
| Single-chain evidence replay across sessions | Closed by SB-1..SB-4 (spec/06 §4). |
| `completionRate` griefing via `aborted-by-other` denominator | `aborted-by-other` removed from the fault denominator; tracked as a separate `abortRate` signal (spec/07 §6). |
| HTLC-10 free option (disclosed, unremedied) | Optional `optionFee` term: a non-refundable d402 micro-payment from payer at lock time, recorded in the agreement (spec/06 §5). Disclosure retained. |
| `negotiable.maxPct` unbounded | `maxPct` MUST be finite; buyer ceiling is part of the normative accept rule (spec/05 §4). |
| Key-compromise signalling missing | `dacs-revocation:v2:` artifact + on-chain revocation program; new sessions MUST check it (spec/02 §7). |
| RFQ flooding / sealed-envelope commit spam ("partial") | Commit anchors cost real fees on Demos (anchoring economics) and listings MAY require a `listingBond` escrow deposit from bidders (spec/04 §6, spec/05 §5). Residual risk disclosed. |
| Timestamps producer-controlled; dual `windowingBasis` | Single normative windowing basis: the anchoring transaction's block timestamp (spec/07 §6). Wall-clock fields remain informational. |
| `ofac-clear` multi-MB fetch vs 128 KB anchor cap | Attestation bodies above the program cap MUST use the `ipfs` tx (cost-capped via `custom_charges.ipfs.max_cost_os`) with the on-chain anchor holding the CID + content hash (spec/03 §5). |
| Fault-attribution chain fragility (decision → errorClass → state → outcome → flip) | Chain shortened: `errorClass` is assigned by the phase executor and counter-signed by the counterparty in the bundle; un-countersigned classifications are excluded from reputation (spec/07 §5). |

## 3. What v0.1 implementers must change first

1. Re-derive all anchor addresses with the node rule (every v0.1 address is wrong on-chain).
2. Replace channel plumbing with `DacsEnvelope` over the IM SignalingServer (spec/05 §2).
3. Add session binding to every payment rail you ship (spec/06 §4) — this is a MUST and rejects old evidence shapes.
4. Move amounts to OS decimal strings (`1 DEM = 10^9 OS`). Fresh chains are OS-native from block 0
   (`osDenomination` fork at `activationHeight: 0`); only legacy chains need the dual-encoding gate via the fork registry.
5. Re-sign everything: separators are `:v2:` and the algorithm set changed.
