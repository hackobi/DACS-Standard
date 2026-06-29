# DACS Spec Style Guide

How normative text in `spec/` is written so humans can read it, retain it, and still implement
from it. Applies to all new spec text; existing chapters migrate module-by-module (see
*Migration* below). Enforced by `scripts/prose_lint.py`.

## The two voices

Every section separates **rule text** (normative) from **notes** (non-normative). They are
different voices for different readers:

- **Rule text** — what an implementer does. Terse, RFC-style, scannable.
- **Notes** — why the rule exists, what attack it closes, design context. Written as a
  blockquote starting with `> **Note (non-normative).**`. A note can never be cited to
  establish a conformance obligation.

History — drift archaeology, "earlier drafts", version genealogy — belongs in the
[CHANGELOG](CHANGELOG.md), not in either voice.

### Triage rule: what must stay in rule text

When splitting an existing paragraph, text MUST stay in rule text (not move to a note) if it:

1. contains an RFC 2119 keyword, or
2. narrows the interpretation of a rule (definitions, scope boundaries, "X means Y", exclusion
   conditions), or
3. is needed to apply the rule (formulas, byte-exact encodings, ordering constraints).

Everything else — motivation, the attack scenario, cross-design comparisons, implementation
status — moves to a note. When in doubt, keep it normative; demotion is the lossy direction.

## The micro-template

Each concept follows the same internal order, so a reader always knows where to look:

1. **Definition** — one or two sentences saying what the thing is.
2. **Rules** — one rule per bullet, each carrying its ID as `(XX-N)` at the start. The
   parenthesized ID form is load-bearing: `validate_rule_ids.py` detects definitions by it.
3. **Example** — a worked, concrete example whenever the rules involve encoding, addressing,
   ordering, or arithmetic.
4. **Note** — the non-normative block(s), last.

Not every section needs all four parts; the *order* is what is fixed.

## Sentence budget (normative text only)

- One normative statement per sentence. A sentence carries at most one RFC keyword
  (a paired prohibition like "MUST do X and MUST NOT do Y" is acceptable when the two
  halves are one rule).
- Rule sentences: target ≤ 30 words; the linter flags > 35.
- Paragraphs (non-list prose): the linter flags > 100 words.
- At most one parenthetical per sentence. No em-dash chains (one em-dash pair per sentence).
- Use the defined term; do not re-describe it inline. If the term needs a reminder, that is
  a note or a cross-reference, not a re-definition.

Notes are exempt from the sentence budget but not from the paragraph cap.

### Waivers

Some normative sentences are irreducible. Suppress a finding by placing an HTML comment on
the line before the flagged paragraph:

```
<!-- prose-lint: allow reason="HTLC-7 inequality is one indivisible constraint" -->
```

The linter reports waiver counts so they stay visible.

## Things that never change in a readability pass

- Rule IDs, their `(XX-N)` definition form, and their meaning.
- Section numbers and anchors.
- Quoted domain-separator strings (e.g. `"dacs-rail:v1:"`), logical-address patterns,
  type/field names, enum values, and code blocks.
- The set of RFC-keyword obligations. Splitting one sentence holding two obligations into
  two bullets is allowed (the keyword census may grow); dropping or weakening one is not.

## Migration and verification protocol

Rewording normative sentences is **meaning-preserving, not byte-preserving**, so each
module pass runs the full protocol:

1. **Census before/after** — rule-ID definition sites, RFC-keyword counts (intentional
   splits documented in the PR), domain separators, address patterns.
2. **Validators + tests green** — `scripts/validate_*.py`, `tests/`.
3. **Cold adversarial review** — an independent reader compares old and new text
   rule-by-rule, looking specifically for: weakened or dropped obligations, demoted
   load-bearing rationale (triage-rule violations), and new contradictions introduced by
   restructuring (the C1 failure mode: a derived table/summary encoding a claim the source
   never made).
4. **CHANGELOG entry** — "editorial revision, no normative change intended, verified by
   the SPEC-STYLE protocol", per module.

A meaning change *caught by review* is expected operation. A meaning change *found after
merge* is a stop-and-rethink signal for the whole migration.

## Chapter openers

Each stage module opens with a half-page **Shape of this stage** block (non-normative):
the artifacts in and out, the states it can leave a session in, and the handful of rules a
reader must know before the detail. Written last, after the chapter stabilises.
