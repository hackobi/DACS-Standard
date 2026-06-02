# DACS Quick Wins

This is the lightweight, contributor-friendly quick-wins list for the
DACS-Standard repository. It focuses on changes that improve implementation
readiness without changing v0.1 conformance semantics. Normative roadmap items
remain tracked in [ROADMAP.md](./ROADMAP.md).

## Current quick wins

1. [x] Add a visible quick-wins inventory so contributors can pick off small,
   reviewable work without guessing from the full roadmap.
2. [x] Add dependency-free markdown documentation validation for relative links
   and section anchors, with tests.
3. [x] Add a minimal conformance-vector manifest for §14 with stable IDs and
   expected pass/fail outcomes.
4. [x] Add a small script that recomputes deterministic JSON content hashes for
   the example artifacts.
5. [ ] Add a CI workflow that runs the documentation and conformance validators
   on every pull request.
6. [ ] Add machine-readable JSON examples for the remaining core artifacts named
   in the spec: IdentityBundle, RatingRecord, and negative-path examples.
7. [ ] Add a glossary index mapping key terms to specification sections.
8. [ ] Add a rule-ID index for conformance rules such as BP-*, LP-*, SIG-*,
   PC-*, RT-*, RAV-*.
9. [ ] Add an operational-builder-guide outline for the roadmap's implementation
   and capital/finality topics.
10. [ ] Add issue templates for spec defects, implementation reports, and
    editorial fixes matching CONTRIBUTING.md's preferred report format.

## Implemented in `feat/dacs-quickwins-10pct`

This branch completes 2 of 10 identified quick wins (20%):

- Quick win 1: this inventory.
- Quick win 2: `scripts/validate-docs.py` plus
  `tests/test_validate_docs.py`.

## Selection criteria

A quick win should be:

- additive and non-breaking;
- small enough for a focused pull request;
- useful to implementers or reviewers immediately;
- safe to land without resolving future v0.2 design questions.
