# DACS Conformance Vectors

This directory contains machine-readable fixtures for implementers who want a
small, repeatable check against the DACS v0.1 artifact lifecycle.

## Included vectors

- [`dacs-v0.1-happy-path.json`](./dacs-v0.1-happy-path.json) — one minimal
  positive session covering all five stages in order:
  `DACS-1 → DACS-2 → DACS-3 → DACS-4 → DACS-5`.

## Validate locally

From the repository root:

```bash
python3 scripts/validate_conformance_vectors.py
```

The validator is stdlib-only. It checks:

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
