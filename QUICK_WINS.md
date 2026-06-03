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
5. [x] Add a CI workflow that runs the documentation and conformance validators
   on every pull request.
6. [x] Add machine-readable JSON examples for the remaining core artifacts named
   in the spec: IdentityBundle, RatingRecord, and negative-path examples.
7. [x] Add a glossary index mapping key terms to specification sections.
8. [x] Add a rule-ID index for conformance rules such as BP-*, LP-*, SIG-*,
   PC-*, RT-*, RAV-*.
9. [x] Add an operational-builder-guide outline for the roadmap's implementation
   and capital/finality topics.
10. [x] Add issue templates for spec defects, implementation reports, and
    editorial fixes matching CONTRIBUTING.md's preferred report format.

## Implemented in `feat/dacs-quickwins-10pct`

This branch completes 10 of 10 identified quick wins (100%):

- Quick win 1: this inventory.
- Quick win 2: `scripts/validate-docs.py` plus
  `tests/test_validate_docs.py`.
- Quick win 3: `conformance/vectors/dacs-v0.1-happy-path.json`.
- Quick win 4: `scripts/validate_conformance_vectors.py` plus
  `tests/test_validate_conformance_vectors.py`.
- Quick win 5: `.github/workflows/validate.yml` runs validators and unit tests on
  pull requests.
- Quick win 6: `conformance/vectors/examples/identity-bundle.json`,
  `conformance/vectors/examples/rating-record.json`, and
  `conformance/vectors/dacs-v0.1-negative-paths.json`.
- Quick win 7: `docs/glossary-index.md` maps key terms to specification sections.
- Quick win 8: `docs/rule-id-index.md` maps labelled rule families to spec
  sections and §14 test-plan hooks.
- Quick win 9: `docs/operational-builder-guide.md` outlines implementation,
  capital/float, undercapitalised-session, key-custody, and settlement-finality
  topics.
- Quick win 10: `.github/ISSUE_TEMPLATE/` includes spec-defect,
  implementation-report, and editorial-fix templates aligned with
  `CONTRIBUTING.md`.

## Selection criteria

A quick win should be:

- additive and non-breaking;
- small enough for a focused pull request;
- useful to implementers or reviewers immediately;
- safe to land without resolving future v0.2 design questions.
