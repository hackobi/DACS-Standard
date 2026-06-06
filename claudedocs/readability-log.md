# DACS Readability / Clarity Log

Running list of wording/structure issues found while reading the spec, to review and fix in one pass at the end. **No normative meaning changes** — these are *how it reads*, not *what it says*.

Two categories:
- **PL — plain-language**: reader-facing prose (Primer, module Abstracts/Motivation/Rationale). Fix = simpler words.
- **SC — structural-clarity**: dense *normative* text where precision is load-bearing. Fix = better structure (define-once + bullets), wording stays exact.

Status: `open` → `fixed`.

**DACS-1 (Identify): pass complete 2026-06-06** — first 7 items (read-through finds) fixed, THEN a comprehensive whole-module sweep added #8–#11 and caught a self-inflicted duplication. 27/27 rule IDs + 103/103 MUSTs preserved throughout, 5 validators + 35 tests green.

**Comprehensive sweep (2026-06-06):** assessed all 14 prose paragraphs ≥110 words. Fixed #8–#11 below. **Corrected a duplication SC#7 introduced** — my CF-4 table came with a "**The rule.**" sentence that duplicated the pre-existing formal **Rule CF-4** (§6.3.4 L422); removed it, folded the MUST/MUST-NOT into the table lead-in. The other ~8 dense paragraphs are single-topic/coherent or already-structured (session-nonce binding, selective-disclosure scope note, SIWD-preferred, sr1-root, revocation, §6.6 security threats, the write-input-mapping (a)(b)(c) block, the formal Rule CF-4 with its worked example, the CF-2 (a)(b)(c) bullet) — left as-is (not the fused-rule+enumeration anti-pattern).

| # | Location | Category | Issue | Proposed fix | Status |
|---|----------|----------|-------|--------------|--------|
| 1 | DACS-1 §6.1 (abstract, "identity claim reference scheme" bullet) | PL | "a typed reference to an external identifier … optionally paired with a DACS-2 verification method" — jargon-dense for an abstract | "A way to **name an identity that already exists somewhere else** (a domain, DID, company LEI, Google account, signing key), written as `type:value` (e.g. `lei:5493…`). Each name can optionally carry **proof it was checked** against that source." | fixed |
| 2 | DACS-1 §6.1 (abstract, listing bullet) | PL | "The listing is the canonical contract for any transaction against the seller." — "canonical contract" unexplained | "The listing is the seller's **signed, pinned statement of terms** — the single source of truth every deal with that seller is checked against." | fixed |
| 3 | DACS-1 §6.3.1 (CF-2/CF-3, "A ClaimReference has a canonical byte form — what is embedded …") | SC | "what is embedded" / "what is compared" reads like a question mid-sentence | "a *canonical byte form* — **the bytes embedded** whenever the reference appears in a hashed or signed document … — and a *canonical identity* — **the value compared** for matching, reputation keying, and the §7.3.2 replay defence." | fixed |
| 4 | DACS-1 §6.3.2 (PresentationSignature signed payload paragraph) | SC | One wall of text mixing one idea + four byte-exact rules; very hard to parse | Define `signed_bytes` once up front, then one bullet per kind (per-claim / session-key / sr1-root / siwd). Keep every byte-exact rule verbatim. Draft in chat 2026-06-05. | fixed |
| 5 | DACS-1 §6.3.2 (4-tier ranking, inline in the presentedBy sentence) + §6.3.2.1 (3-tier collapse) + §6.3.1 (per-scheme hints) | SC | Claim tiers have **no single citable definition** — the 4-level ranking is buried mid-sentence in §6.3.2, the 3-level IT collapse is restated in §6.3.2.1, scheme hints are scattered in §6.3.1. Reader must reconcile across 3 places, and the 4-tier vs 3-tier views can drift (§6.3.2.1 manually asserts "this is the collapse of §6.3.2"). | Extract a **define-once "Claim tiers" table** (4 levels → schemes → 3-level IT collapse) that §6.3.2 and §6.3.2.1 both *reference* instead of restating. Table drafted in chat 2026-06-05: `1 Authority-issued (lei/finra-crd/sam-uei/fedramp/cmmc/naics)→institutional · 2 DID/ERC-8004+proof→verified · 3 Platform→verified · 4 Plain key→self-declared`. | fixed |

| 6 | DACS-1 §6.3.2 ("For a BundleClaim with verifiedBy present: …" + the freshness-window paragraph) | SC | One dense paragraph fuses *two* things: the 5-step verification checklist **and** the freshness-window formula (with clamping + fail-closed). The inline `min(…)` and the "ignore later wrapper timestamps" clamp are very hard to parse in prose. | Split into (1) a numbered **verification steps** list (fetch → hash-check → parse+recipe → identifier-match → decision==pass → else unverified), and (2) a **Freshness window** sub-block: issuance = `verifiedAt`; `expiry = min(expiresAt ?? ∞, validUntil ?? verifiedAt+defaultMaxAgeSec×1000)`; presenter timestamps clamp (narrow-only, never widen); `defaultMaxAgeSec` from the result's own `recipeVersion` (not latest); fail-closed when undeterminable. Keep the formula verbatim. | fixed |

| 7 | DACS-1 §6.3.4 (CF-4 logical-address encoding paragraph) | SC | One dense paragraph carries: what CF-4 is/isn't + the full list of 7 address kinds it applies to + which segment is variable in each + the why. The per-address variable-vs-fixed detail is impossible to scan in prose. | Lead with the one rule (encode internal `:` of variable segments → `%3A`; leave structural delimiters), then a **table** (address → variable segment(s) → fixed segments), then the one-line why (undecidable boundaries → divergent native addresses). Note CF-4 governs the *name's* parseability, not the native-address formula. Keep all address patterns verbatim. Table drafted in chat 2026-06-06. | fixed |

| 8 | DACS-1 §6.3.2 (presentedBy selection paragraph, 206w) | SC | Fuses the selection rule + reader-acceptance + the big "Reputation MUST NOT be keyed against an unverified presentedBy" anti-laundering rule in one 206-word block | Split: selection-rule paragraph + a separate **Verified-presentedBy for reputation** rule. | fixed |
| 9 | DACS-1 §6.3.4 (listing validation order) | SC | "validate in the following order, halting on first failure: (1)…(9)" — an ordered sequence flattened into prose | Numbered list (1–9), each step verbatim. | fixed |
| 10 | DACS-1 §6.3.2 (canonical serialisation paragraph) | SC | General canonical-form/hash rule fused with the SIWD-specific verifier re-derivation MUST | Split: general rule + a separate **SIWD bundle-binding check** block. | fixed |
| 11 | DACS-1 §6.3.2 (BP-1..BP-4 / BR-1..BR-5 conformance) | SC | Inline `(BP-1) … (BP-4)` and `(BR-1) … (BR-5)` lists in running prose | Bullet lists, one rule per bullet, verbatim. | fixed |

## Post-pass review (fresh-eyes, 2026-06-06)
A read-only critical review of the edited DACS-1 (independent reviewer) found **two contradictions the readability pass introduced/hardened** — both fixed:
- **C1 (critical).** The new **Claim tiers** table carried an `identityTier` column mapping `key` → `self-declared`, but the §6.3.2.1 derivation (step 2) maps a *verified* `key:` → `verified`. They are **different axes** (scheme-strength for `presentedBy` vs verification-status for `identityTier`) that SC#5 wrongly merged (a latent pre-restructure tension the table hardened into an authoritative contradiction). Fix: dropped the `identityTier` column from the tiers table; reworded the governance line + the §6.3.2.1 sentence to state the two axes distinctly (verified `key:` → `verified`).
- **C2 (minor).** Rule CF-4 prose listed `listingId` as MUST-percent-encode, but the new CF-4 table (and worked example) treat it as fixed. `listingId` is URL-safe ASCII (§6.3.4) so carries no reserved delimiters — fixed the prose to match the table.

Everything else the restructure touched verified behavior-preserving (signed-bytes bullets, BP/BR, validation list, verify+freshness, CF-4 table all sound; tables well-formed; no dropped MUSTs). Lesson: **a readability table that adds a *derived* column can encode a contradiction the source prose only had latently — always cross-check new tables against the surviving derivation rules.**

## Post-pass review — round 2 (independent, cold, 2026-06-06)
A second fresh-eyes reviewer (no knowledge of C1/C2) read DACS-1 cold. **Clean on criticals** — explicitly confirmed the C1/C2 fixes hold (verified-`key:` → `verified` consistent in all 3 places; CF-4 `listingId` consistent across prose/table/example; no false "cannot disagree" claim; no dropped MUSTs; rule families single-defined; tables well-formed). Two **minor** items fixed:
- §6.4 rationale listed **"OFAC"** among shipped DACS-1 schemes — but OFAC is a DACS-2 sanctions *check*, not an identity scheme (**pre-existing error from the monolith**, count 1 on main). Corrected to the real registry (LEI, FINRA-CRD, SAM-UEI, FedRAMP, NAICS, CMMC).
- `BundleClaim.expiresAt` schema comment "when verifiedBy becomes stale" overstated the field (it only *narrows* the authority window) — aligned to §6.3.2.
- (no-op) two `signed_bytes :=` definitions share the name but are disambiguated by their domain prefixes — cosmetic, left.

**Convergence:** round 2 found no new criticals → DACS-1 treated as clean.

## DACS-2 (Vet) — finds (read-through in progress)

| # | Location | Category | Issue | Proposed fix | Status |
|---|----------|----------|-------|--------------|--------|
| 12 | DACS-2 §7.3.1 (method common contract, CM-1..CM-5) | SC | Inline `(CM-1) … (CM-5)` list in one running sentence — same hard-to-scan pattern as DACS-1 BP/BR | Bullet list, one CM rule per bullet; keep the CM-2 address `dacs2:{jobId}:{scheme}:{identifier}:v{recipeVersion}` + CF-4 note verbatim. | open |
| 13 | DACS-2 §7.3.2 (verifiable-credential `Procedure`, 278w) | SC | One semicolon-chained sentence fusing: the verification step sequence + the holder-binding security rule (incl. the §6.3.2 nonce disjunction + its rationale) + the 4-way pass/fail/error/indeterminate outcome mapping + trust-model/substrate footer | Numbered **verification steps** list; pull holder-binding into its own labelled sub-block (the MUST + nonce disjunction + the replay rationale); render the outcome mapping as a small pass/fail/error/indeterminate list. Keep all MUSTs verbatim. **NB: all 8 method subsections §7.3.2–7.3.9 are "Procedure." prose of this shape — assess each in the DACS-2 sweep.** | open |

| 14 | DACS-2 §7.3.2–7.3.9 (every method `Procedure` restates the session-nonce binding) | SC (define-once) | The session-nonce anti-replay binding (the §6.3.2 disjunction: SIWD Nonce else `bundleToVet.sessionNonce`, reject on mismatch) is **repeated in each method procedure** — VC calls it "holder-binding" (§7.3.2), oauth-attested restates it (§7.3.6 "consistent with §7.3.2"), etc. "Describe it N times" at the method level. | **Define once** in the common contract — add a CM rule (e.g. CM-6 "every method MUST bind its attestation to the session nonce per §6.3.2") — and have each method `Procedure` reference it + state only its method-specific caveat (e.g. oauth's "if the service can't carry a nonce, document residual replay risk"). Bigger dedup than bulletizing each procedure (which is #13). | open |

## Reviewed — correct, no change
- **DACS-1 §6.3.1 "Parsers … SHOULD emit lowercase" then CF-2 "Scheme lowercased (MUST)".** Looked contradictory but is intentional scoping (permissive default → MUST at the hash/sign/compare boundary). CF-2 already flags the escalation. No fix; possibly a one-line inline note if it keeps tripping readers.

## Notes
- PL fixes belong to the plain-language pass on abstracts/motivation/rationale.
- SC fixes are structure-only on normative prose — run them through the rule-ID + validator gate (no rule text altered).
- Append new finds as `#N | location | PL/SC | issue | fix | open` while reading.
