"""Shared spec source resolver.

DACS v0.1 is authored as a Core document plus one module per stage
(spec/CORE.md, spec/DACS-1-IDENTIFY.md … spec/DACS-5-VERIFY.md). The
validators operate on the concatenation of these documents — the same
text the former single spec/SPECIFICATION.md carried — so grep/marker
based checks behave identically after the split.
"""
from __future__ import annotations

from pathlib import Path

# Authored order: Core first, then the five stage modules, then the CORE
# companion references (moved-out back matter: §A, ch.12, ch.13, ch.14 —
# section numbering retained, so concatenated grep checks see the same
# text the unified spec carried).
SPEC_FILES = [
    "spec/CORE.md",
    "spec/DACS-1-IDENTIFY.md",
    "spec/DACS-2-VET.md",
    "spec/DACS-3-NEGOTIATE.md",
    "spec/DACS-4-SETTLE.md",
    "spec/DACS-5-VERIFY.md",
    "spec/DEMOS-MAPPING.md",
    "spec/THREAT-MODEL.md",
    "spec/GLOSSARY.md",
    "spec/CONFORMANCE-PLAN.md",
]


def spec_paths(root: Path) -> list[Path]:
    return [root / rel for rel in SPEC_FILES]


def spec_text(root: Path) -> str:
    """Concatenated text of all spec documents, in authored order.

    Falls back to the legacy single spec/SPECIFICATION.md when no split
    documents are present (e.g. synthetic fixtures in unit tests that write
    their own SPECIFICATION.md into a temp root)."""
    parts = [p.read_text(encoding="utf-8") for p in spec_paths(root) if p.exists()]
    if parts:
        return "\n".join(parts)
    legacy = root / "spec" / "SPECIFICATION.md"
    return legacy.read_text(encoding="utf-8") if legacy.exists() else ""
