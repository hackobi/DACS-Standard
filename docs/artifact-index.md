# DACS artifact index

*Non-normative. This index helps readers locate the principal DACS artifacts. The normative definitions live in the cited spec sections.*

| Artifact / type | Defined in | Signature domain | Role in lifecycle |
| --- | --- | --- | --- |
| `ClaimReference` | [`§6.3.1`](../spec/DACS-1-IDENTIFY.md#631-identity-claim-reference-scheme), [`§B.1`](../spec/CORE.md#b1-claim-references-and-identity) | — | Typed pointer to an external identity/authority claim. |
| `IdentityBundle` | [`§6.3.2`](../spec/DACS-1-IDENTIFY.md#632-identity-bundle) | `dacs-bundle-presentation:v1:` for presentation | Ordered claims presented by a party. |
| `BundleRequirement` | [`§6.3.3`](../spec/DACS-1-IDENTIFY.md#633-bundle-requirement-schema) | — | Listing-side requirements for acceptable identity bundles. |
| `Listing` | [`§6.3.4`](../spec/DACS-1-IDENTIFY.md#634-service-listing) | `dacs-listing:v1:` | Seller's signed/anchored offer and canonical transaction contract. |
| Listing revocation marker | [`§6.3.4`](../spec/DACS-1-IDENTIFY.md#634-service-listing) | `dacs-revocation:v1:` | Revokes or supersedes a listing. |
| Bundle session-key root binding | [`§6.3.2`](../spec/DACS-1-IDENTIFY.md#632-identity-bundle) | `dacs-session-binding:v1:` | Binds session keys to the presented identity bundle. |
| `RecipeDefinition` | [`§7.4`](../spec/DACS-2-VET.md#74-recipe-registry) | `dacs-recipe:v1:` | Defines how a claim scheme is verified. |
| `VerifyResult` | [`§7.5`](../spec/DACS-2-VET.md#75-verifyresult) | `dacs-verifyresult:v1:` | Uniform output from a verification method. |
| `CompositeVerificationRecord` | [`§7.7`](../spec/DACS-2-VET.md#77-composite-verification-record) | `dacs-composite:v1:` | Aggregates freshness checks, signals, and deal-specific claims for Vet. |
| `ChannelMessage` | [`§8.3.3`](../spec/DACS-3-NEGOTIATE.md#833-message-envelope-substrate-independent) | `dacs-channelmsg:v1:` | Signed private-channel negotiation message. |
| Auto-accept commitment | [`§8.4.1`](../spec/DACS-3-NEGOTIATE.md#841-negotiate-fixed-price) | `dacs-auto-accept-commitment:v1:` | Commits fixed-price acceptance parameters. |
| Auto-accept instance | [`§8.4.1`](../spec/DACS-3-NEGOTIATE.md#841-negotiate-fixed-price) | `dacs-auto-accept-instance:v1:` | Instance record for fixed-price acceptance. |
| `AgreementDocument` | [`§8.5`](../spec/DACS-3-NEGOTIATE.md#85-agreement-document) | `dacs-agreement:v1:` | Final agreed terms signed by parties. |
| Commitment record | [`§8.6`](../spec/DACS-3-NEGOTIATE.md#86-commitment-phase-commit-agreement) | `dacs-commitment:v1:` | Public commitment to the agreement hash. |
| Channel transcript | [`§8.7`](../spec/DACS-3-NEGOTIATE.md#87-channel-transcript-and-disclosure) | `dacs-transcript:v1:` | Exportable transcript evidence for private negotiation. |
| `RailDefinition` | [`§9.4`](../spec/DACS-4-SETTLE.md#94-payment-rail-registry) | `dacs-rail:v1:` | Registry entry for a supported payment rail. |
| `SettlementEvidence` | [`§9.7`](../spec/DACS-4-SETTLE.md#97-settlement-evidence) | `dacs-evidence:v1:` | Uniform evidence produced by payment and delivery phases. |
| Settlement amendment | [`§9.7.1`](../spec/DACS-4-SETTLE.md#971-refunds-and-partial-refunds) | `dacs-amendment:v1:` | Refund or correction linked to prior settlement evidence. |
| `EntitlementRecord` | [`§9.6.2`](../spec/DACS-4-SETTLE.md#962-deliver-entitlement) | `dacs-entitlement:v1:` | Delivery artifact granting service access. |
| `SessionRecord` | [`§10.3`](../spec/DACS-5-VERIFY.md#103-session-record) | — | Live off-chain session state maintained by the orchestrator. |
| `AttestationBundle` | [`§10.4`](../spec/DACS-5-VERIFY.md#104-attestation-bundle) | `dacs-bundle:v1:` | Frozen end-of-session audit artifact. |
| `ReputationDerivation` | [`§10.5`](../spec/DACS-5-VERIFY.md#105-reputation-derivation) | — | Deterministic derivation over closed bundles. |
| `RatingRecord` | [`§10.6`](../spec/DACS-5-VERIFY.md#106-the-rate-phase-optional) | `dacs-rating:v1:` | Optional buyer/seller rating referenced from a bundle. |

## Maintenance rule

When a new signed artifact kind is added to [`§B.7`](../spec/CORE.md#b7-universal-signature-scheme-domain-separated-signing), update this index and the relevant conformance-vector metadata in the same PR.
