# DACS Profile — v0.1

A DACS **profile** pins a coherent set of document versions that implement and conform together. Each document versions independently thereafter (per-stage minor versions per [CONTRIBUTING](../CONTRIBUTING.md)); a profile is the snapshot an implementer targets.

## DACS v0.1

| Document | Version | Status |
| --- | --- | --- |
| [CORE](CORE.md) | 0.1 | Draft |
| [DACS-1-IDENTIFY](DACS-1-IDENTIFY.md) | 0.1 | Draft |
| [DACS-2-VET](DACS-2-VET.md) | 0.1 | Draft |
| [DACS-3-NEGOTIATE](DACS-3-NEGOTIATE.md) | 0.1 | Draft |
| [DACS-4-SETTLE](DACS-4-SETTLE.md) | 0.1 | Draft |
| [DACS-5-VERIFY](DACS-5-VERIFY.md) | 0.1 | Draft |

**Conformance to "DACS v0.1"** means conformance to every document at the version pinned above, exercised by the [conformance vectors](../conformance/).

## Scope is a profile decision

Which stages, methods, and rails a release ships is decided here, not by deleting specification text. A future profile MAY:

- omit a module (e.g. ship without `DACS-3-NEGOTIATE` on a substrate lacking SR-4 — only `negotiate-fixed-price` is then available, which needs no private channel);
- pin a reduced module variant (e.g. a `DACS-2-VET` profile exposing a subset of the eight verification methods, or a `DACS-4-SETTLE` profile exposing a subset of rails);
- add a module (e.g. `DACS-X-DISPUTE`, or a `pay-evm-erc8183` escrow rail) once it reaches the shipped-path + reference-implementation bar (see [ROADMAP](../ROADMAP.md)).

This makes scope trimming and feature addition version events on the profile, not edits that churn the normative documents.
