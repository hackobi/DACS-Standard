# DACS Conformance Vectors

This directory contains machine-readable fixtures for implementers who want a
small, repeatable check against the DACS v0.1 artifact lifecycle.

## Included vectors

- [`dacs-v0.1-happy-path.json`](./dacs-v0.1-happy-path.json) — one minimal
  positive session covering all five stages in order:
  `DACS-1 → DACS-2 → DACS-3 → DACS-4 → DACS-5`.
- [`dacs-v0.1-negative-paths.json`](./dacs-v0.1-negative-paths.json) — negative
  examples that conforming implementations are expected to reject or classify as
  failures, with rule references for the expected failures.

## Core artifact examples

- [`examples/identity-bundle.json`](./examples/identity-bundle.json) — a
  machine-readable IdentityBundle example for §6.3.2.
- [`examples/rating-record.json`](./examples/rating-record.json) — a
  machine-readable RatingRecord example for §10.6.

## Production trust-signal fixtures

The repository also includes small shared fixtures outside this vector directory:

- `conformance/fixtures/identity/identity-tier-*.json` — deterministic
  `identityTier` cases for institutional, verified, and self-declared bundles.
- `conformance/fixtures/reputation/reputation-suspicious-pattern-flags.json` —
  advisory `suspiciousPatternFlags` on a ReputationRecord / derivation surface.
- `conformance/fixtures/settlement/htlc9-asymmetric.json` — the HTLC-9
  `dest-revealed-source-unclaimed` interim evidence state.
- `conformance/fixtures/dacsx/dispute-outcome-htlc9-correction.json` — the
  provisional DACS-X DisputeOutcome seam that emits a correction amendment.

## Validate locally

From the repository root:

```bash
python3 scripts/validate_conformance_vectors.py
python3 scripts/verify_dacsx_dispute_pack.py
```

The validators are stdlib-only. The vector validator checks:

- required top-level vector fields
- exactly ordered five-stage coverage
- per-artifact required fields
- `§`-style spec references
- domain separators ending in `:v1:`
- deterministic `sha256:` content hashes over each artifact payload

## Scope

These vectors are non-normative tooling around the standard. The normative source
remains [`spec/SPECIFICATION.md`](../../spec/SPECIFICATION.md). When a vector and
the specification disagree, the specification wins and the vector should be fixed.
