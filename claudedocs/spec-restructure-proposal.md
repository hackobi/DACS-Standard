# DACS Spec — Structural Deep-Dive Review

/ 2026-06-04. Non-normative working analysis. Grounded in measured coupling + size data. /

## 0. Three different "size" problems — don't conflate them

| Symptom | Root cause (measured) | Lever | Risk |
|---|---|---|---|
| **Feels bulky** (4,008 lines) | **904 lines (23%) are blank lines inside airy schema formatting** (one blank between every field) | Compact schema formatting | ~zero (whitespace only) |
| **Long to read** (52k words) | over-written normative prose | Lever 1 prose dedup (−14% prose, measured on Ch.9) | low (behavior-preserving) |
| **Hard to navigate / not composable like 8004** | monolith with a shared data model | Restructure → Core + Modules (this doc) | high (do later) |

The first is the highest-ROI surprise: nearly a quarter of the document is blank lines in the type blocks. Compacting them removes ~900 lines with **zero semantic change** — bigger than the entire prose-compression lever, and trivially safe.

## 1. What the coupling data forces

Measured cross-reference + type-usage graph:

- **The data model is the hub.** ~30 shared types, each referenced across **3–7 chapters**: `PhaseHandlerResult` (7), `SettlementEvidence` (6), `VerifyResult` (6), `Listing` (6), `AttestationRef` (6), `IdentityBundle` (5), `SessionContext` (5), `CompositeVerificationRecord` (5)… The model cannot live inside any one stage module — **it must be a shared Core.** This is the dominant constraint.
- **Stages are a coupled pipeline, not independent units.** Heaviest edges: ch6↔ch7 (Identify↔Vet, 11/8 — very tight), ch9→ch8 (Settle→Negotiate's Agreement, 13), ch6→ch10 (Identify→Reputation, 8).
- **Threat model / conformance / glossary are cross-cutting aggregators** (ch12→everything: ch7:19, ch10:12, ch9:11…; ch14→ch10:14…). They span the whole spec by nature.

**Conclusion:** a flat "5 independent stage specs" split is **wrong** — it would duplicate the data model and create heavy cross-document dependencies. The correct shape is **layered: one shared Core + feature Modules** — the **CSS-Modules / W3C-profile** pattern.

## 2. Proposed architecture (CSS-module style)

### Layer 1 — **DACS-Core** (everyone reads & implements; ~1,200–1,400 ln)
- Framing (§1–5): problem, approach, 5 stages, substrate requirements SR-1..5.
- **Data-Model registry** — all cross-cutting types in one normative home (Identity/Listing/Agreement/Settlement/Reputation/Session/Phase types + VerifyResult/Recipe).
- **Universal mechanisms** — SIG-* signatures, CF-*/CD-* canonical form & decimal, the session state machine ST-*, the phase-handler contract.
- 5-stage lifecycle skeleton — the abstract per-stage MUSTs (the *what*; the *how* lives in modules).
- Governance, versioning, and the **profile manifest** mechanism.
- Cross-cutting *frames*: adversary model; conformance frame.

### Layer 2 — **Feature Modules** (each self-contained: rules + procedures + own Security Considerations + own Conformance vectors; imports Core types)
| Module | Holds | ~ln |
|---|---|---|
| **DACS-Vet-Methods** | 8 methods, recipe schema/registry, PSP/RA/RAV/VP-*, match() detail | 450 |
| **DACS-Settle-Rails** | PC contract, 6 rail procedures, HTLC-*, tank, SE atomicity | 550 |
| **DACS-Negotiate-Patterns** | RFQ, sealed-envelope, channels (CH/SE/RFQ) | 400 |
| **DACS-Reputation** | bundle production/consumption, derive(), two-sided reconciliation, RT, category-scope | 300 |
| **DACS-X-Dispute** | dispute/correction (design seam #98/#99) | future |

### Layer 3 — **Cross-cutting** (Core frame + per-module sections)
- **Threat model** — Core defines adversary classes; each module carries its own "Security Considerations" (invert today's aggregator).
- **Conformance** — Core vectors + each module ships its own vectors. **PR #119's `conformance/fixtures/{area}/` tree already anticipates module-scoped conformance.**
- **Glossary** — auto-generated index across Core + modules (PR #119's `glossary-index` tooling already does cross-doc indexing).

## 3. The five hard problems & resolutions

1. **Shared data model (dominant).** One normative Data-Model section in Core; modules import by reference. A type change still ripples to dependents — true today too — but the home becomes unambiguous.
2. **Cross-document references.** Replace bare `§9.5.4` with stable shortnames, W3C-style: `[RAILS §5.4]`, `[CORE: SettlementEvidence]`. A ref-map table in Core.
3. **Conformance.** Core vectors + per-module vectors; the **profile** is their union. (PR #119 layout fits.)
4. **Threat model.** Core adversary classes + self-contained per-module Security Considerations.
5. **Versioning + scope.** Each module versions independently (CSS model). A **Profile** doc pins `DACS v0.1 = Core 0.1 + Vet-Methods 0.1 + Settle-Rails 0.1 + Negotiate 0.1 + Reputation 0.1`. **This also answers Lever 3 (scope trimming): dropping a feature = leaving its module out of the profile, not deleting text.**

## 4. Keep-together decisions (forced by coupling)

- **Identify + Vet** share the bundle/verification data model (11/8 coupling) → both their *types* live in Core; Vet's *method procedures* go to the Vet-Methods module; the `match()` algorithm (the bridge) stays in Core.
- **AgreementDocument** in Core (Settle needs it); Negotiate *patterns* in the module.

## 5. Peer comparison — which model fits

- **CSS**: CSS2 monolith → CSS3 modules (Flexbox, Grid…) advancing independently on a stable core. Same problem (a spec too big to advance as one unit), same shared-core need. **Closest precedent.**
- **EIP/ERC**: core ERC + extension ERCs by number, each self-contained (Spec/Rationale/Security/Test). 8004 stays small *because* it's a registry others extend. But ERCs are loosely coupled *contracts* — DACS shares a data model, so it's less like this.
- **OAuth/IETF**: core RFC + extension RFCs.

DACS's coupling profile (one shared data model) is **most like CSS** — needs a shared Core — **not** like independent ERCs. The CSS-module model fits best.

## 6. Honest tradeoffs of modularizing

- **Cost:** cross-document refs, profile-version management, more files, harder to read end-to-end, citation churn for anyone already referencing v0.1 sections.
- **Benefit:** a newcomer reads a ~1,300-line Core; implementers pull only the modules they need; modules advance independently; scope becomes a profile decision; each module is independently reviewable.
- **Risk of doing it now:** content just stabilized through 9 rounds; Marius's #117 is mid-flight; v0.1 hasn't shipped. A full split now churns every cross-reference.

## 7. Recommended sequencing (reversible-first)

**Now — safe, in-place, NO file split (single shareable v0.1 document):**
1. **Schema formatting compaction** — remove the 904 intra-schema blank lines → 4,008 ≈ 3,100 lines, zero semantic change. *Biggest, safest win.*
2. **Lever-1 prose dedup** per chapter → −14% prose (≈ −270 more lines), behavior-preserving (rule-ID + validator gate).
3. **Extract the Data Model into a labeled "Core Data Model" section in-place** — establishes the Core/Module import boundary *without splitting files* (fully reversible). After this, the eventual physical split is mechanical.

   → Net: **4,008 → ~2,800 lines**, navigable, still one document to ship/cite for v0.1.

**v0.2 — post-v0.1-ship, post-#117:** physically split Core + Modules into separate documents with the profile manifest and shortname cross-refs. Easier to review/cite as a monolith for the launch; the in-place data-model boundary makes the split low-risk.

## 8. Bottom line

"How to structure it better" has a layered answer: **Core + feature Modules (CSS-module model), driven by the shared data model** — but the *value* arrives mostly from the cheap in-place steps (formatting compaction + data-model extraction + prose dedup), which get the doc to ~2,800 navigable lines now. The physical module split is the v0.2 move, and it doubles as the clean mechanism for scope decisions (profiles) and independent feature evolution.

---

## 9. Concrete structure outline (the document set)

### Tier 1 — `PRIMER.md` (~5–6 pp) — *read to understand*
1. Abstract — what DACS is, in one paragraph
2. The problem (← current §1)
3. The approach — claims-not-roots; compose existing standards (← §2)
4. The five stages — lifecycle diagram + table (← §3/§4)
5. **The spine** — the 9 artifacts and how they chain, one diagram (NEW, short)
6. Substrate requirements SR-1..5 — one table (← §5)
7. **Worked example** — one transaction end-to-end through all five stages (NEW)
8. How to read the rest — map: Core + which module for what (NEW, ½ pp)

### Tier 2 — `CORE.md` (~24 pp) — *the normative reference everyone implements*
1. Conventions — RFC 2119; canonical form (CF-1..4); canonical decimal (CD-1); universal signatures (SIG-1..5) + the domain-separator registry (← §B.7, §7.2 anchoring)
2. **Data model** — the 9 spine artifacts + shared sub-structures (the ~30 cross-cutting types) (← type blocks pulled from chs 6–10)
3. Session & phase model — SessionContext, PhaseHandlerResult, PhaseStep/Type, session state machine ST-1..8 (← §B.5, §10.3.1)
4. 5-stage lifecycle skeleton — abstract per-stage MUSTs (the *what*; *how* → modules)
5. Substrate requirements SR-1..5 — normative (← §5 normative parts)
6. Governance & versioning — the **profile** mechanism, progressive anchoring, steward (← §11, §7.4.4)
7. Threat-model frame — adversary classes, cross-cutting goals/non-goals (← §12.1–12.3)
8. Conformance frame — how modules declare conformance; the profile (← §14 intro)

### Tier 3 — Module specs (~6–8 pp each; self-contained: rules + procedures + own Security Considerations + own Conformance index; import Core types)
- `DACS-1-IDENTIFY` — listing schema, bundle-requirement matching (match()), discovery (.well-known + catalog), publish/read rules (LP/LR/BP/BR/CF), identity-tier (IT) (← §6.3 rules)
- `DACS-2-VET` — 8 methods, recipe registry, ParserSpec (PSP), retry/cache (VP-R/VP-C), aggregation, availability (RAV), vet phase (VPC/MA), warnings (WN) (← §7.3–7.9)
- `DACS-3-NEGOTIATE` — channel model (CH), 3 patterns + RFQ/SE rules, agreement validation, commit (CA), pattern selection (PS) (← §8.3–8.9)
- `DACS-4-SETTLE` — payment common contract (PC), 6 rail procedures, HTLC (HTLC), liquidity-tank, delivery phases, amendments (AMEND), pipeline (PIPE), cross-chain atomicity (← §9.4–9.9)
- `DACS-5-VERIFY` — bundle production/consumption, derivation (derive()/reconciliation/determinism receipt), rating (RT), category-scoping, ERC-8004 publication (← §10.4–10.8)
- `DACS-X-DISPUTE` (future) — dispute/correction (#98/#99)

### Tier 4 — `PROFILE.md` (~1 pp) + `conformance/`
- **Profile** pins the version set: `DACS v0.1 = Core 0.1 + Identify 0.1 + Vet 0.1 + Negotiate 0.1 + Settle 0.1 + Verify 0.1`. Scope decisions (which modules/methods/rails ship) live here — Lever 3 = editing the profile, not deleting text.
- **conformance/** (the #119 tree) — executable vectors per module + MANIFEST; each module's Conformance section is a rule-ID → vector index (the §14 dedup pattern).

### Conventions
- **Cross-refs:** stable shortnames — `[CORE: SettlementEvidence]`, `[SETTLE §5.4]`, `[VET §3.2]` — not bare `§9.5.4`.
- **Versioning:** each document versions independently (CSS-module model); the Profile pins the coherent set.

### Reader paths
- Newcomer / evaluator → Primer (~6 pp).
- Single-stage implementer → Primer + Core + 1 module (~36 pp).
- Whole-stack implementer → everything (~78 pp, ~same total as today).

---

## 10. Pre-v0.2 fix list — rule-family Core-boundary moves

Surfaced reading DACS-2 (the CF-4 reference in CM-2, 2026-06-06). The **types** belong in Core (§2); so do the **cross-cutting rule families** — but several are currently written inside a stage module. Test: **used across ≥2 modules / shared infrastructure → CORE; specific to one stage → that module.** ("Common" ≠ "cross-module" — CM-1..5 is the *verification-method* common contract, common only *within* Vet, so it stays in DACS-2.)

**Already in CORE (correct):** SIG-1..5 (§B.7), CF-1 (§B.2), GOV-1..3 (§11).

**Hoist into CORE before the v0.2 split (currently mis-homed in a module):**

| Family | What | Current home | Why it's cross-cutting |
|---|---|---|---|
| **CF-2, CF-3** | ClaimReference canonical byte form / identity | DACS-1 §6.3.1 | DACS-1 matching, DACS-5 reputation keying + replay defence |
| **CF-4** | logical-address delimiter encoding | DACS-1 §6.3.4 | addresses in DACS-1 / 2 / 4 / 5 |
| **CD-1** | canonical decimal | DACS-3 §8.5.1 | DACS-3 pricing + DACS-4 settlement amounts |
| **ST-1..8** | session state machine | DACS-5 §10.3.1 | the session model; DACS-4 references it (settle-asymmetric / ST-8) |

After the move, CORE holds the full **universal-mechanisms** set (SIG + CF-* + CD-1 + ST-* + GOV + the phase-handler contract), and each module keeps only its stage-specific families:
- DACS-1: BP, BR, LP, LR, IT (**MA / match() is borderline** — the Identify↔Vet bridge; deep-dive §4 already flags it for Core).
- DACS-2: CM, RA, RAV, PSP, VP-R, VP-C, VPC, WN.
- DACS-3: CH, SE, RFQ, PS, CA.
- DACS-4: PC, HTLC, RD, AMEND, PIPE, RAV-R.
- DACS-5: RT.

Do this at the physical Core/module split (§7 step "v0.2"), not before — it churns cross-references (a `§6.3.4` CF-4 cite becomes `[CORE: CF-4]`, etc.). It's a *move*, not a rewrite: the rule text is unchanged, only its home document.
