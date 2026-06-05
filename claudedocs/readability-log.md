# DACS Readability / Clarity Log

Running list of wording/structure issues found while reading the spec, to review and fix in one pass at the end. **No normative meaning changes** — these are *how it reads*, not *what it says*.

Two categories:
- **PL — plain-language**: reader-facing prose (Primer, module Abstracts/Motivation/Rationale). Fix = simpler words.
- **SC — structural-clarity**: dense *normative* text where precision is load-bearing. Fix = better structure (define-once + bullets), wording stays exact.

Status: `open` → `fixed`.

| # | Location | Category | Issue | Proposed fix | Status |
|---|----------|----------|-------|--------------|--------|
| 1 | DACS-1 §6.1 (abstract, "identity claim reference scheme" bullet) | PL | "a typed reference to an external identifier … optionally paired with a DACS-2 verification method" — jargon-dense for an abstract | "A way to **name an identity that already exists somewhere else** (a domain, DID, company LEI, Google account, signing key), written as `type:value` (e.g. `lei:5493…`). Each name can optionally carry **proof it was checked** against that source." | open |
| 2 | DACS-1 §6.1 (abstract, listing bullet) | PL | "The listing is the canonical contract for any transaction against the seller." — "canonical contract" unexplained | "The listing is the seller's **signed, pinned statement of terms** — the single source of truth every deal with that seller is checked against." | open |
| 3 | DACS-1 §6.3.1 (CF-2/CF-3, "A ClaimReference has a canonical byte form — what is embedded …") | SC | "what is embedded" / "what is compared" reads like a question mid-sentence | "a *canonical byte form* — **the bytes embedded** whenever the reference appears in a hashed or signed document … — and a *canonical identity* — **the value compared** for matching, reputation keying, and the §7.3.2 replay defence." | open |
| 4 | DACS-1 §6.3.2 (PresentationSignature signed payload paragraph) | SC | One wall of text mixing one idea + four byte-exact rules; very hard to parse | Define `signed_bytes` once up front, then one bullet per kind (per-claim / session-key / sr1-root / siwd). Keep every byte-exact rule verbatim. Draft in chat 2026-06-05. | open |
| 5 | DACS-1 §6.3.2 (4-tier ranking, inline in the presentedBy sentence) + §6.3.2.1 (3-tier collapse) + §6.3.1 (per-scheme hints) | SC | Claim tiers have **no single citable definition** — the 4-level ranking is buried mid-sentence in §6.3.2, the 3-level IT collapse is restated in §6.3.2.1, scheme hints are scattered in §6.3.1. Reader must reconcile across 3 places, and the 4-tier vs 3-tier views can drift (§6.3.2.1 manually asserts "this is the collapse of §6.3.2"). | Extract a **define-once "Claim tiers" table** (4 levels → schemes → 3-level IT collapse) that §6.3.2 and §6.3.2.1 both *reference* instead of restating. Table drafted in chat 2026-06-05: `1 Authority-issued (lei/finra-crd/sam-uei/fedramp/cmmc/naics)→institutional · 2 DID/ERC-8004+proof→verified · 3 Platform→verified · 4 Plain key→self-declared`. | open |

## Reviewed — correct, no change
- **DACS-1 §6.3.1 "Parsers … SHOULD emit lowercase" then CF-2 "Scheme lowercased (MUST)".** Looked contradictory but is intentional scoping (permissive default → MUST at the hash/sign/compare boundary). CF-2 already flags the escalation. No fix; possibly a one-line inline note if it keeps tripping readers.

## Notes
- PL fixes belong to the plain-language pass on abstracts/motivation/rationale.
- SC fixes are structure-only on normative prose — run them through the rule-ID + validator gate (no rule text altered).
- Append new finds as `#N | location | PL/SC | issue | fix | open` while reading.
