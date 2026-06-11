# DACS/2 §3 — DACS-2: Vet

Vetting establishes the truth of **authority claims** (spec/02 §1) and gathers supplementary signals. Chain-native
claims are not vetted here (ID-1 suffices).

## 1. Verification methods

The closed method registry, with each method's L1 binding:

| Method | Demos binding | Trust model |
|---|---|---|
| `tlsnotary` | Node TLSNotary service: SDK `demos.tlsnotary().attest({url})` → `TLSNotaryPresentation`; third-party check via `POST /tlsnotary/verify`; on-chain storage via native `tlsn_store(tokenId, proof, "onchain"\|"ipfs")` | Cryptographic (MPC-TLS): proof of an authentic HTTPS exchange, verifiable by anyone, not trust-the-relay |
| `consensus-backed-proxy` | DAHR: `web2Request` tx / `web2ProxyRequest` RPC; `IWeb2Result.responseHash` + `responseHeadersHash` anchored in block `web2data` | Node-attested hash commitment. Honest-validator assumption; TLS-MITM of the authority defeats it |
| `verifiable-credential` | W3C VC presented over the channel; holder binding to `sessionNonce` | Issuer trust |
| `zktls` | zkTLS proof verified per its scheme | Cryptographic |
| `evm-rpc` | XM `contract_read` task via `crosschainOperation`, or direct RPC | RPC honesty (mitigate with multi-RPC quorum in recipe `parameters`) |
| `oauth-attested` | KeyServer OAuth flow (`@kynesyslabs/demosdk/keyserver`), result anchored | Provider + keyserver trust |
| `domain-tls-control` | ACME-style challenge fetched via DAHR or TLSNotary | Control proof |
| `self-signed` | Claim signed by its own subject | None (floor) |

## 2. Tier floor (TF-1) — replaces v0.1's uniform SR-3 routing

**TF-1** A `VerifyResult` for an **institutional scheme** (`lei`, `finra-crd`, `sam-uei`, `fedramp`, `cmmc`, `naics`,
and sanctions checks such as `ofac-clear`) is valid only if `method ∈ {tlsnotary, verifiable-credential, zktls}`.
`consensus-backed-proxy` results for these schemes MUST aggregate as `indeterminate`, never `pass`.

*Rationale:* v0.1 routed its highest-stakes verifications (OFAC, GLEIF, FINRA) through its weakest attestation
primitive — a hash commitment forgeable by authority-TLS MITM and indistinguishable from a single-fetcher result. The
node ships TLSNotary natively; the strong path exists, so the standard requires it where it matters. DAHR remains the
right tool for low-stakes freshness checks and fulfillment evidence.

## 3. Recipes

Recipe schema is carried over from v0.1 substantially unchanged (`scheme`, `defaultMethod`, `alternatives`,
`defaultMaxAgeSec`, `parserRules` with PSP rules, `negativeMatch`, `retryClass/Budget/backoff`, 7-value `availability`,
`governance`, `signature`) with these amendments:

- **RC-1** `governance.anchoring` gains the value `"steward-group"` (§6); `single-signer` recipes MUST set
  `availability: "operator_gated"` at most.
- **RC-2** Recipes for institutional schemes MUST declare `defaultMethod` compliant with TF-1.
- **RC-3** Authority endpoints in recipes (`api.gleif.org`, `api.brokercheck.finra.org`, …) are data, not spec text:
  endpoint churn is a recipe revision, not a standard revision.

## 4. VerifyResult and CompositeVerificationRecord

Both carried over from v0.1 (four-valued `decision: pass|fail|indeterminate|error`; aggregation precedence within
oneOf-groups error > indeterminate > fail, across accumulators fail > error > indeterminate; WN-* advisory warnings),
with amendments:

- **VR-1** `attestation.anchor` MUST follow AD-3/AD-4. Oversized attestation bodies (e.g. full sanctions-list
  snapshots) go to the `ipfs` transaction with cost caps; the anchored record holds `{cid, contentHash, sizeBytes}`.
- **VR-2** `data` at public anchors remains predicate-outcomes-only (no raw authority payloads with third-party PII).
- **VR-3** A composite record's `freshness`/`dealSpecific` entries covering chain-native claims are forbidden
  (MA-2); validators of composites MUST reject them.

## 5. Who vets

Each party vets the other against its own `BundleRequirement` (spec/00 §4): the seller vets the buyer per the
listing's `buyerRequirement`; the buyer vets the seller per the listing's presented bundle and its own policy. Each
side signs its own `CompositeVerificationRecord`. Parties MAY purchase vetting from a third-party verifier — which is
itself a DACS seller whose result artifacts identify it as `signer` and stake its reputation.

## 6. Registry governance (replaces PA-2 single steward)

The registry — schemes, aliases, methods, recipes, rails, separators — lives in the Storage Program
`(stewardDeployer, "dacs2:registry")` with ACL:

```
{ mode: "restricted", groups: { stewards: { members: [<N accounts>], permissions: ["read","write"] } } }
```

- **GV-1** A registry mutation is an `APPEND_ITEM` of a `RegistryEntry {dacs:"2", entryKind: "recipe"|"rail"|"scheme-alias"|"method"|"steward-set", payloadHash, payload?, supersedes?, effectiveAt, signatures: Sig[]}`
  signed with `dacs-registry-entry:v2:` by **M-of-N stewards** (M, N published as the latest `steward-set` entry;
  bootstrap: M=1, N=1 = KyneSys Labs, and any consumer can read exactly how far governance has actually progressed).
- **GV-2** Consumers MUST verify M-of-N on the entry payload itself, not merely trust the ACL write (node ACLs gate
  who can write; signatures prove who agreed).
- **GV-3** Emergency disablement (`availability: "disabled"`) MAY be single-steward-signed but MUST be ratified by
  M-of-N within 14 days or it expires.
- **GV-4** Steward-set rotation is itself an M-of-N entry under the *previous* set — the chain of `steward-set`
  entries is the governance audit trail.
- **GV-5** Sessions pin `registryVersion` = contentHash of the latest entry at session start; mid-session registry
  changes do not apply (carried over from v0.1 pinning, now with an on-chain version object).
