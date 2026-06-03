#!/usr/bin/env python3
"""Validate DACS v0.1 domain separator registry consistency.

This is intentionally narrow: it checks quoted `dacs...:v1:` domain strings in
the normative specification against the §7.7 registered signature separators and
registered non-signature commitment prefixes. It does not scan logical addresses
such as `dacs2:registry:v0.1`.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "spec" / "SPECIFICATION.md"
DOMAIN_RE = re.compile(r'"(dacs[-a-z0-9]*:v1:)"')


def extract_domains(text: str) -> set[str]:
    """Return quoted DACS v1 domain separators/prefixes from text."""
    return set(DOMAIN_RE.findall(text))


def section_between(text: str, start_marker: str, end_marker: str) -> str:
    start = text.find(start_marker)
    if start == -1:
        raise ValueError(f"missing section marker: {start_marker}")
    end = text.find(end_marker, start)
    if end == -1:
        raise ValueError(f"missing section end marker: {end_marker}")
    return text[start:end]


def registered_domains(spec_text: str) -> set[str]:
    registry = section_between(
        spec_text,
        "The v0.1 registry of domain separators is closed:",
        "**Payload shape — single-hash vs composite.**",
    )
    return extract_domains(registry)


def used_domains(spec_text: str) -> set[str]:
    # Scope to the current normative spec only. Repository vectors and changelog
    # may contain historical or deliberately invalid examples.
    return extract_domains(spec_text)


def validate_spec(path: Path = SPEC) -> list[str]:
    spec_text = path.read_text(encoding="utf-8")
    registered = registered_domains(spec_text)
    used = used_domains(spec_text)
    missing = sorted(used - registered)
    unused = sorted(registered - used)
    errors: list[str] = []
    for domain in missing:
        errors.append(f"domain separator/prefix used but not registered in §7.7: {domain}")
    for domain in unused:
        # This should be rare because table entries are themselves quoted uses;
        # keep the check for parser sanity and future refactors.
        errors.append(f"domain separator/prefix registered but not discoverable as quoted literal: {domain}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate DACS domain separator registry consistency")
    parser.add_argument("path", nargs="?", type=Path, default=SPEC)
    args = parser.parse_args(argv)
    errors = validate_spec(args.path)
    if errors:
        print("domain separator validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("domain separator registry OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
