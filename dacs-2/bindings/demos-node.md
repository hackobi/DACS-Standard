# DACS/2 Binding: Demos Node (`binding: "demos/1"`)

The normative wire format for the `dacs2-demos` conformance class. Reference implementation: the
`kynesyslabs/node` **`stabilisation` branch** (node 0.9.8, pins `@kynesyslabs/demosdk 4.0.5`) — the most advanced
branch, ~3.5k commits ahead of `testnet`. Where deployed networks differ, the §6 feature gates apply; gates are
expressed in terms of the node's own **fork registry** (`src/forks/`, declared in genesis with per-fork
`activationHeight`) wherever a fork exists.

## 1. Operation → wire table

| DACS/2 operation | Node surface (exact) |
|---|---|
| Resolve listing | `GET /storage-program/:address/field/current`; verify per LP-4 |
| Enumerate listings | `GET /storage-program/search/:name` (prefix `dacs2:listing:`), `GET /storage-program/owner/:address` |
| Publish/update listing | `storageProgram` tx: `CREATE_STORAGE_PROGRAM` / `SET_FIELD current` / `APPEND_ITEM versions` / `SET_FIELD status` (SDK `demos.storagePrograms`, `StorageProgram.deriveStorageAddress`) |
| Read identity (chain-native claims) | `nodeCall getAddressInfo` → `AddressInfo.identities {xm, web2}`; reverse: SDK `Identities.getDemosIdsByWeb2Identity / getDemosIdsByWeb3Identity` |
| Bind identity | `identity` tx: `web2_identity_assign` / `xm_identity_assign` / `tlsn_identity_assign` / `ud_identity_assign` / `pqc_identity_assign` |
| ZK claims | `identity` tx `zk_commitmentadd`; `GET /zk/merkle-root`, `GET /zk/merkle/proof/:commitment`, `GET /zk/nullifier/:hash`; RPC `verifyProof` |
| Vet via TLSNotary | `nodeCall tlsnotary.getToken` (paid token) → `demos.tlsnotary().attest({url})` → `POST /tlsnotary/verify`; store: native op `tlsn_store(tokenId, proof, "onchain"\|"ipfs")` |
| Vet via DAHR | RPC `web2ProxyRequest` (`create` → `startProxy`) or `web2Request` tx; result `IWeb2Result {responseHash, responseHeadersHash, …}` |
| Envelope transport (TB-1) | IM SignalingServer WebSocket (`register`/`message`); SDK `@kynesyslabs/demosdk/instant_messaging`; milestone anchor: `instantMessaging` tx `{targetId, senderId, messageHash}` |
| Envelope transport (TB-2) | `l2psInstantMessaging` payloads in the shared L2PS; integrity via `l2ps_hash_update` |
| Commit / evidence / bundle / rating / dispute anchors | `storageProgram` tx with the AD-2 program names; free reads via `/storage-program/*` |
| Pay `demos-native` | `demos.pay(to, amountOS)` → `confirm` → `broadcast` (two-phase, §3) |
| Pay `demos-d402` | `d402_payment {to, amount, memo: "dacs2:{jobId}:{hash16}"}`; SDK `D402Client.createPayment/settle`, server side `D402Server.require/verify/validatePayment`; HTTP header `X-Payment-Proof: <txHash>` |
| Pay `demos-escrow` | `escrow` tx → `GCREditEscrow {deposit/claim/refund, expiryDays, message}`; SDK `EscrowTransaction.sendToIdentity / claimEscrow`, `EscrowQueries` |
| Pay `demoswork-conditional` | `demoswork` tx: `DemoScript` (conditional op: DAHR/TLSN predicate step → native pay step), SDK `@kynesyslabs/demosdk/demoswork` |
| Pay `xm-pay` | `crosschainOperation` tx: `XMScript {operations, operations_order}`, task `pay`, client-pre-signed `signedPayloads`; SDK `demos.xm.createPayload` |
| Pay `bridge-usdc` | RPC `nativeBridge` (compile `BridgeOperation`) → `nativeBridge` tx `{operation, bridgeId}` |
| Deliver storage-program / ipfs | `storageProgram` writes with buyer-readable ACL / `ipfs` tx (`IPFS_ADD`, `custom_charges.ipfs.max_cost_os`; quote via `demos.ipfs.quote`) |
| Verify settlement tx | `nodeCall getTxByHash` / `getTransactionStatus` / `getTransactionHistory(address, type)`; SB-1 memo check reads `content.data[1].memo` of the settled tx; foreign chains via own RPC |
| Reputation enumeration (REP-C) | `nodeCall getTransactionHistory(party, "storageProgram")`, filter `programName` prefix `dacs2:bundle:` |
| Network/fee/fork introspection | `GET /info`, `GET /health`, `GET /health/subsystems`; `nodeCall getNetworkInfo`; SDK `getNetworkParameters / getValidators / getStakedAmount` |
| Identity overview | `GET /identities` (added on stabilisation), `nodeCall getAddressInfo` |

**Dispatch note (BW-0):** the node's broadcast switch has **no default-reject** — transaction types without a
dedicated case (`d402_payment`, `storageProgram`, `storage`, `instantMessaging`) execute through the generic path:
confirm-phase `GCRGeneration.generate(tx)` hash-compare → simulated `HandleGCR.applyTransaction` → mempool. A type is
therefore *live* iff the pinned SDK generates its edits **and** `HandleGCR.applyEdit` implements every edit kind they
produce. `d402_payment` qualifies (SDK `HandleD402Operations` emits plain `balance` edits); `escrow` does not (its
`escrow` edit kind is a stub — §6).

## 2. Transaction envelope (what gets signed at the node layer)

`Transaction.content {type, from, from_ed25519_address, to, amount, data: [type, payload], gcr_edits[], nonce, timestamp, transaction_fee}` —
**BW-1**: implementations MUST build transactions with the SDK (`demos.tx.*`, module builders), never hand-rolled
JSON: the node regenerates GCR edits via `GCRGeneration.generate(tx)` and **hash-compares** against
`content.gcr_edits`; tx hash is `sha256(JSON.stringify(content))`. Byte-exactness is consensus-enforced.
**BW-2**: nonces are strict — `GCREditNonce.expectedPrior` plus, on networks with the `nonceEnforcement` fork active,
a consensus rule enforcing sequential nonces and blocking replay. Concurrent agent payments from one account MUST
serialize nonces locally or shard across session keys/accounts.

## 3. Two-phase lifecycle

`RPCRequest {method: "execute", params: [bundle]}` with `extra: "confirmTx"` → node validates and returns **signed
`ValidityData`** (gas, `reference_block`, the exact transaction; on stabilisation the confirm phase snapshots
`gcr_edits` pre-sign and synthesizes staking/governance edits inside `confirmTransaction`, so the signed ValidityData
is the complete execution commitment) → `extra: "broadcastTx"` → simulate → mempool → DTR relay to the validator
shard → PoRBFT inclusion (~10 s blocks) → poll `getTxByHash` / `getTransactionStatus` (SDK `broadcastAndWait`). **BW-3**: persist
`ValidityData` for all settlement transactions (DACS-6 evidence, spec/06 §7). **BW-4**: a `reference_block` expiry or
ValidityData rejection is `errorClass: "transient"`.

## 4. Amounts

All DACS/2 amounts are CD-1 strings in OS (`1 DEM = 10^9 OS`; node constant `OS_PER_DEM = 1_000_000_000n`) or foreign
base units. **BW-5**: fresh chains declare the `osDenomination` fork at `activationHeight: 0` and are OS-string-native
from genesis; only legacy chains have a pre-fork DEM-number regime below the activation height. Serialize per the
fork status (`getNetworkInfo` / genesis fork registry) using SDK `denomination.demToOs/osToDem` and the serializer
gate — never `Number()` on amount strings.

## 5. Keys and signatures

Node account = ed25519 (bip39 seed via SDK `connectWallet`). PQC artifact signers (`falcon`, `ml-dsa`) MUST be bound
on-chain via `pqc_identity_assign` before first use (SIG-3). Encryption for TB-1/TB-2 payloads uses SDK `encryption`
primitives (`ml-kem-aes` preferred).

## 6. Feature gates

Networks upgrade asynchronously; the binding is gated, not versioned monolithically. The node now ships explicit
**fork machinery** (`src/forks/`; forks declared in genesis with `activationHeight`, `null` = registered but
unscheduled) — where a fork exists, the gate IS the fork status, read from the genesis fork registry /
`getNetworkInfo`. At session start, implementations MUST probe and record in the agreement's rail parameters:

| Gate | Probe | If closed |
|---|---|---|
| `escrowEnabled` | `escrow` GCR edit handler live — **stubbed ("Not implemented") on all current branches incl. `stabilisation`**; probe via a dust deposit/refund until a capability flag or fork exists | `demos-escrow` rail MUST NOT be offered; availability `operator_gated` |
| `demosworkEnabled` | `demoswork` dispatch case (present on stabilisation); probe a no-op script on non-reference networks | `demoswork-conditional` unavailable |
| `bridgeEnabled` | `nativeBridge` RPC responds for the route | `bridge-usdc` unavailable |
| `tlsnotaryEnabled` | `GET /tlsnotary/health` | TF-1 schemes cannot be vetted on this node — use another RPC node or VC/zkTLS |
| `osDenomination` fork | genesis fork registry (`activationHeight: 0` on fresh chains) | amount serialization per §4 |
| `nonceEnforcement` fork | genesis fork registry | BW-2 still applies via `expectedPrior`; strict consensus-level replay blocking absent |
| `gasFeeSeparation` fork | genesis fork registry (**registered but unscheduled** on stabilisation: `activationHeight: null`) | fee split (burn/treasury/rpc-operator via `feeDistribution`) inactive; fees flow through plain GCR balance edits |
| `sdkMajor` | pinned `@kynesyslabs/demosdk` major = 4 (stabilisation pins `4.0.5`) | d402/escrow/governance payload shapes unavailable on SDK 2.x networks |

**BW-6**: a listing MUST NOT advertise a rail whose gate is closed on the listing's declared network; doing so is a
listing validation failure, mirroring the v0.1 `availability` consumer rules.

Live on stabilisation (no gate needed): validator staking (`validatorStake/validatorUnstake/validatorExit` dispatched;
`GCRValidatorStakeRoutines`; min stake 10^18 OS, 1000-block unstake lock), on-chain governance
(`networkUpgrade`/`networkUpgradeVote`), `zk_attestationadd`, TLSNotary, storage programs (REST + new nodeCall reads),
DAHR, IM SignalingServer + `L2PSMessagingServer`, `d402_payment` via the generic path (BW-0).

## 7. Known node-side gaps (tracked, not assumed)

As of `stabilisation` @ `e4b87686`: escrow + smartContract GCR edit handlers remain stubs; `registerIMPData` remains
TODO (IM milestone anchoring works at tx level; GCR-side IM indexing pending); `determineGasForOperation` still
returns 0 — the full fee architecture (`FeeBreakdown`, `feeDistribution` burn/treasury/rpc split, governance-mutable
percentages) exists in code but sits behind the unscheduled `gasFeeSeparation` fork. These are why §6 exists. Spec
features depending on them degrade per their gates rather than failing silently (coding rule: fail visibly).
