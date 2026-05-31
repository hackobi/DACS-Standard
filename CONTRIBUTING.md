# Contributing to DACS

DACS is an open standard published so that builders can implement against it and
report where it doesn't hold up. Implementation feedback is the most valuable
contribution at this stage.

## What we're looking for

- **Spec defects** — rules that reference undefined values, internal
  inconsistencies, or addressing/serialisation patterns that don't work on a real
  substrate.
- **Composition gaps** — a corner where DACS fails to compose cleanly with one of
  the standards it builds on (W3C VC, ERC-8004, AP2, x402, TLSNotary, A2A, …).
- **Implementation reports** — "I built X against §Y and hit Z." These shape the
  next minor version.
- **Editorial fixes** — typos, broken links, formatting.

## How to file feedback

The highest-signal reports name three things:

1. The **section** (e.g. `§7.7.1`).
2. The **artifact / file path** the issue touches.
3. An **alternate interpretation** or proposed fix.

Open an [issue](https://github.com/DACS-Agent-commerce/DACS-Standard/issues) for
defects and concrete proposals, or a
[discussion](https://github.com/DACS-Agent-commerce/DACS-Standard/discussions) for
open-ended questions.

## Versioning

- Draft phase uses `0.MAJOR.MINOR` (v0.1, v0.2, …); `MAJOR.MINOR` from v1.0.
- Breaking changes bump the major version; additive non-breaking changes bump the
  minor version; editorial-only changes do not bump the version.
- Every normative change is recorded in [CHANGELOG.md](./CHANGELOG.md) with the
  section numbers it affects, so implementers can scan against their own code.

## Governance

DACS v0.1 operates under progressive-anchoring phase **PA-2**: a single steward
(KyneSys Labs) signs the recipe and rail registries. Constitution of multi-party
governance (PA-3) is named follow-on work in §11.2.6 of the specification. Until
then, normative changes are merged by the steward after public discussion.

## Editing the specification

The canonical specification lives in [`spec/`](./spec/). When proposing normative
text changes, quote the affected passage and section number in your issue or PR
description so the change is reviewable inline.
