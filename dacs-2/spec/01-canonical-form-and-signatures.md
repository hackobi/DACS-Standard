# DACS/2 §1 — Canonical Form, Signatures, Addressing

## 1. Canonical JSON (CF-1)

Every signed or hashed DACS/2 document is canonicalised as **RFC 8785 (JCS)** with these additional rules:

- **CF-1a** All string values MUST be Unicode NFC-normalised before serialisation.
- **CF-1b** JSON numbers MUST NOT exceed 2^53 − 1 in magnitude; larger or precise values are canonical-decimal strings (CD-1).
- **CF-1c** Tooling that "approximates" JCS (e.g. sorted-key `JSON.stringify`) is non-conformant. Implementations MUST
  use a verified RFC 8785 serialiser; conformance vectors MUST be generated with one.

## 2. Canonical decimals (CD-1)

Amounts and other precise quantities are strings matching `^(0|[1-9][0-9]*)(\.[0-9]+)?$` — no sign, no exponent, no
leading zeros, no trailing fractional zeros, and no trailing dot. **DEM amounts are expressed in OS**
(`1 DEM = 10^9 OS`) as integer CD-1 strings; foreign-asset amounts use that asset's base units. The `number`-typed
pre-fork DEM wire format MUST NOT appear in DACS/2 artifacts (the binding converts at the node edge, see
[bindings/demos-node.md](../bindings/demos-node.md) §5).

## 3. Content addressing

`contentHash(doc) := sha256hex(JCS(doc))` computed over the document **without** its `signature` field(s).
References between artifacts are `{kind, contentHash, anchor?}` where `anchor` locates the bytes (§7).

## 4. Domain-separator registry (closed)

`signed_bytes := separator || contentHash(doc)` (ASCII concatenation; the hash is lowercase hex).

| Artifact | Separator | Defined in |
|---|---|---|
| Listing | `dacs-listing:v2:` | spec/04 |
| Identity-bundle presentation | `dacs-presentation:v2:` | spec/02 |
| Key/claim revocation | `dacs-revocation:v2:` | spec/02 |
| VerifyResult | `dacs-verifyresult:v2:` | spec/03 |
| CompositeVerificationRecord | `dacs-composite:v2:` | spec/03 |
| Recipe | `dacs-recipe:v2:` | spec/03 |
| Registry entry | `dacs-registry-entry:v2:` | spec/03 |
| DacsEnvelope | `dacs-envelope:v2:` | spec/05 |
| AgreementDocument | `dacs-agreement:v2:` | spec/05 |
| CommitmentRecord | `dacs-commitment:v2:` | spec/05 |
| ChannelTranscript | `dacs-transcript:v2:` | spec/05 |
| Auto-accept commitment | `dacs-auto-accept:v2:` | spec/05 |
| Sealed-bid commitment tag (not a signature) | `dacs-sealed-bid:v2:` | spec/05 |
| RailDefinition | `dacs-rail:v2:` | spec/06 |
| SettlementEvidence | `dacs-evidence:v2:` | spec/06 |
| SettlementAmendment | `dacs-amendment:v2:` | spec/06 |
| EntitlementRecord | `dacs-entitlement:v2:` | spec/06 |
| AttestationBundle | `dacs-bundle:v2:` | spec/07 |
| RatingRecord | `dacs-rating:v2:` | spec/07 |
| Session-key binding | `dacs-session-binding:v2:` | spec/02 |
| DisputeRecord | `dacs-dispute:v2:` | spec/08 |
| DisputeOutcome | `dacs-dispute-outcome:v2:` | spec/08 |

Experimental kinds use `dacs-x-<kind>:v2:` and are excluded from reputation and registries.

## 5. Signature rules (SIG-1..SIG-5)

```ts
type Sig = { algorithm: "ed25519" | "falcon" | "ml-dsa", signer: string /* ClaimReference, §6 */, value: string /* hex */ }
```

- **SIG-1** Sign exactly `signed_bytes` from §4. Verifiers MUST reconstruct it independently; never trust embedded hashes.
- **SIG-2** A signature that cannot be reproduced from the received bytes MUST cause rejection of the artifact.
- **SIG-3** `algorithm` matches the node's `SigningAlgorithm` set. `falcon` and `ml-dsa` signers MUST be bound to the
  ed25519 root via an on-chain `pqc_identity_assign` (verified through `getAddressInfo`); an unbound PQC signer is invalid.
- **SIG-4** Unregistered separators MUST be rejected outside the `dacs-x-` namespace.
- **SIG-5 (preserve-unknown)** Hash the document exactly as received, including unknown fields. Unknown fields MUST NOT
  be dropped, reordered semantically, or cause rejection within a major version.

## 6. ClaimReference and scheme aliasing (CF-2, MA-1)

Canonical form: `<scheme>:<identifier>[?<k>=<v>&…]` — scheme lowercase, identifier NFC, params sorted by key,
percent-encoding per RFC 3986 minimal set. The root scheme is **`demos:<account>`**.

**Scheme alias table (normative — fixes DACS-VERIFY-0001):** a `ClaimRequirement.scheme` matches a claim whose scheme
equals it **or** equals a registered alias of it:

| Requirement scheme | Aliases |
|---|---|
| `lei` | `cci-lei` |
| `finra-crd` | `cci-finra-crd` |
| `sam-uei` | `cci-sam-uei` |
| `fedramp` | `cci-fedramp` |
| `naics` | `cci-naics` |
| `cmmc` | `cci-cmmc` |
| `domain` | `cci-ud` (a UD domain satisfies a domain requirement only if `parameters.allowUd == true`) |

The alias table is part of the on-chain registry (spec/03 §6) and is extended only by steward-group entries.
Matching is otherwise exact; there is no transitive aliasing.

## 7. Anchoring and addressing (AD-1..AD-4)

All on-chain anchors are **Storage Programs** addressed by the node's own derivation — there is no DACS-side address
formula (this replaces v0.1 §6.3.4 addressing, which produced addresses that do not resolve on the node):

- **AD-1** `address := StorageProgram.deriveStorageAddress(deployerAccount, programName, nonce, salt?)` exactly as
  implemented by `@kynesyslabs/demosdk`. The `(deployer, programName)` pair is the logical identity; the resolved
  `stor-…` address is recorded in artifacts next to it.
- **AD-2** Normative program names (NFC, literal prefixes):

  | Purpose | Deployer | `programName` |
  |---|---|---|
  | Listing | seller | `dacs2:listing:{listingId}` |
  | Commitment | buyer | `dacs2:commit:{jobId}` |
  | Settlement evidence | phase executor | `dacs2:evidence:{jobId}:{phaseIndex}` |
  | Attestation bundle | each party | `dacs2:bundle:{jobId}` |
  | Rating | rater | `dacs2:rating:{jobId}` |
  | Dispute record | opener | `dacs2:dispute:{jobId}` |
  | Revocations | key owner | `dacs2:revocations` |
  | Registry | steward group | `dacs2:registry` |

- **AD-3** Anchor reference shape: `Anchor = {kind: "storage-program", address, programName, deployer, field?}` |
  `{kind: "ipfs", cid, contentHash}` | `{kind: "https", url, contentHash}`. HTTPS anchors are valid only for
  discovery-time artifacts (listings dereferenced before verification), never for evidence or bundles.
- **AD-4 (oversize rule)** A body exceeding the Storage Program limit (1 MB program / fee-chunked at 10 KB) MUST be
  stored via the `ipfs` transaction with `custom_charges.ipfs.max_cost_os` set, and the Storage Program anchor holds
  `{cid, contentHash, sizeBytes}`. This is the normative path for large attestation bodies (e.g. sanctions-list proofs).

**Pairwise privacy salt (AD-5, optional):** parties MAY agree (in the AgreementDocument) on a `pairSalt` and deploy
session programs with `salt = sha256(pairSalt || programName)`, making session anchors unlinkable to passive observers
while remaining resolvable by both parties and any arbitrator given the agreement. Reputation derivation over salted
bundles requires the party to disclose its salts to the deriver (spec/07 §6).

## 8. Timestamps

Producer wall-clock timestamps (`sentAt`, `generatedAt`, …) are informational. Wherever ordering or windowing has
protocol meaning — commitment deadlines, reveal windows, reputation windows — the normative clock is the **block
timestamp of the anchoring transaction** (TS-1). Artifacts whose wall-clock fields contradict their anchor's block
time by more than 300 s SHOULD be flagged but MUST NOT be rejected on that basis alone.
