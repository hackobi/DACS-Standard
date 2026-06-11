# DACS/2 §2 — DACS-1: Identify

## 1. Model: one root, two claim classes

Every DACS/2 participant is rooted in a **Demos account** (ed25519 public key). Identity is the set of claims bound to
that root. DACS/2 splits claims into two classes with different verification paths — this replaces v0.1's uniform
"every claim needs a VerifyResult" model:

| Class | Examples | Verified by | Freshness |
|---|---|---|---|
| **Chain-native claims** | `cci-web2` (GitHub/X/Discord/Telegram), `cci-xm` (EVM/Solana/Aptos/… wallets), `cci-ud`, `cci-pqc`, `cci-tlsn`, reputation scores (`cci-nomis`, `cci-ethos`, `cci-humanpassport`) | Reading GCR state: `getAddressInfo(account)` / `getDemosIdsBy*` reverse lookup. The binding proof was already validated by consensus when the `identity` transaction executed. | Chain head — a claim present in current state is fresh by definition; removal is equally visible. |
| **Authority claims** | `lei`, `finra-crd`, `sam-uei`, `fedramp`, `naics`, `cmmc`, `domain`, `did`, `erc8004`, `stor-cred:*` | DACS-2 vetting (recipes → VerifyResults), spec/03. | `validUntil ?? verifiedAt + recipe.defaultMaxAgeSec` (unchanged from v0.1). |

*Rationale:* on Demos, web2 and web3 bindings are consensus-validated state (`web2_identity_assign` proofs are checked
by the node via `getTweet`/`getDiscordMessage`/gist fetch; `xm_identity_assign` by signature/on-chain-write proof;
`tlsn_identity_assign` by TLSNotary verification). Re-attesting them through DACS-2 recipes, as v0.1 did, duplicated
work the chain already does and added a weaker trust path. A verifier needs one free RPC read.

## 2. IdentityBundle

```ts
type IdentityBundle = {
  dacs: "2"
  root: string                      // "demos:<0x…>" ClaimReference
  presentedAt: string               // ISO 8601, informational (TS-1 applies)
  sessionNonce: string              // REQUIRED in session contexts; ≥128-bit, hex
  claims: BundleClaim[]
  presentation: Presentation
}
type BundleClaim = {
  ref: string                       // ClaimReference canonical form (spec/01 §6)
  class: "chain-native" | "authority"
  verifiedBy?: { kind: "verify-result", contentHash: string, anchor: Anchor }   // REQUIRED iff class == "authority" and requirement demands verification
  zk?: ZkClaimProof                 // §6 — replaces the cleartext ref when selective disclosure is used
}
```

- **ID-1** `claims[].ref` of class `chain-native` MUST be present in the root account's current GCR identity state at
  verification time; the verifier resolves via `getAddressInfo` (or `getDemosIdsBy*` for reverse checks). A bundle
  asserting an unbound chain-native claim is invalid in full, not per-claim (it evidences either staleness or fraud).
- **ID-2** Authority claims follow spec/03; bundles MAY present them unverified when the counterparty's
  `BundleRequirement` sets `verificationRequired: false`.

## 3. Presentation (two kinds)

All presentations sign `"dacs-presentation:v2:" || contentHash(bundle minus presentation)`.

```ts
type Presentation =
  | { kind: "demos-account", sig: Sig }          // signer == root account key, or a PQC key bound via pqc_identity_assign
  | { kind: "session-key",   key: string, sig: Sig, rootBinding: SessionKeyBinding }
type SessionKeyBinding = {                        // signed by the root: "dacs-session-binding:v2:" || contentHash(this minus sig)
  sessionKey: string, validFrom: string, validUntil: string, scope?: string[] /* jobIds or "any" */, sig: Sig
}
```

- **PR-1** `demos-account` verification requires only the bundle bytes and an open node read — no wallet software, no
  vendor SDK. This replaces v0.1's four presentation kinds; in particular SIWD (which only a Demos wallet could verify)
  is removed.
- **PR-2** Session keys are how facilitators/delegated runtimes act for a principal (spec/00 §2). The binding is
  root-signed, time-boxed, and optionally job-scoped. Artifacts signed by a session key attribute to the root for
  reputation; the binding MUST accompany or be anchored alongside the first artifact the key signs in a session.
- **PR-3** `sessionNonce` MUST be unique per session and echoed in the counterparty's `AgreementDocument` reference to
  this bundle — replay of a presentation across sessions is thereby detectable.

## 4. BundleRequirement and matching

Unchanged in structure from v0.1 (`required` AND-list + `oneOf` OR-groups, `maxAge` tighten-only, `recipeVersion` pin),
with two amendments:

- **MA-1** Scheme matching uses the alias table (spec/01 §6).
- **MA-2** A requirement on a chain-native scheme is satisfied by ID-1 alone; `verificationRequired` is meaningless for
  chain-native claims and MUST be ignored.

## 5. identityTier

Deterministic, never self-asserted (IT rules unchanged from v0.1): `institutional` (≥1 verified authority claim of an
institutional scheme) > `verified` (≥1 chain-native claim beyond `cci-pqc`, or verified non-institutional authority
claim) > `self-declared` (root key only).

## 6. Selective disclosure (ZK claims)

Demos provides Poseidon commitments in an incremental Merkle tree (`zk_commitmentadd`), attestation insertion
(`zk_attestationadd`, groth16-verified at apply time), public roots (`GET /zk/merkle-root`,
`GET /zk/merkle/proof/:commitment`), groth16 verification (`verifyProof` RPC), and a nullifier registry
(`GET /zk/nullifier/:hash`).

```ts
type ZkClaimProof = {
  statement: "has-claim-scheme" | "tier-at-least" | "score-at-least"
  parameters: Record<string, string>     // e.g. {scheme: "lei"} or {tier: "verified"}
  merkleRoot: string, nullifier: string, proof: string /* groth16, base64 */
}
```

- **ZK-1** A `zk` claim proves the statement about the root's committed claims **without revealing the claim
  identifier**. Verifiers MUST check the proof via `verifyProof`, the root against a recent `/zk/merkle-root`, and the
  nullifier as unused for this `sessionNonce` context.
- **ZK-2** Listings declare whether ZK satisfaction is acceptable per requirement (`ClaimRequirement.zkAcceptable`,
  default false for institutional schemes — regulated flows usually need the identifier).
- **ZK-3** Sessions satisfied entirely by ZK claims combine with pairwise-salted anchors (AD-5) for full counterparty-
  graph privacy. The reputation linkage cost of this choice is disclosed in spec/07 §6.

## 7. Revocation and key compromise

- **RV-1** Removing a chain-native claim (`*_identity_remove`) takes effect at chain state; verifiers see it on the
  next read. Nothing further needed.
- **RV-2** **Key compromise:** the owner (or its pre-designated recovery key, declared as a `recoveryKey` field in any
  prior anchored listing or bundle) anchors a `RevocationRecord` in its `dacs2:revocations` program:
  `{dacs:"2", revokes: string /* key or claim ref */, reason: "compromise"|"rotation"|"retired", effectiveAt, sig}`
  signed with separator `dacs-revocation:v2:`.
- **RV-3** Before relying on any presentation, verifiers MUST read the root's `dacs2:revocations` program (free REST
  read). Artifacts signed after `effectiveAt` by a revoked key are invalid for new sessions; in-flight sessions MAY
  complete under the agreement's existing signatures. Reputation derived for a root is not transferred by key rotation
  (the root account is the reputation subject, not the key).
