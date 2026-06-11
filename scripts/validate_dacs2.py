#!/usr/bin/env python3
"""Validate fork-native DACS/2 draft package.

This intentionally stays dependency-free. It does not try to implement JSON Schema;
it validates the repository contract around the DACS/2 package: required files,
parseable schemas, local links, and domain-separator consistency between the
spec registry and schema comments.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DACS2 = ROOT / "dacs-2"

REQUIRED_FILES = [
    "README.md",
    "MIGRATION.md",
    "spec/00-architecture.md",
    "spec/01-canonical-form-and-signatures.md",
    "spec/02-identity.md",
    "spec/03-vetting.md",
    "spec/04-discovery.md",
    "spec/05-negotiation.md",
    "spec/06-settlement.md",
    "spec/07-attestation-reputation.md",
    "spec/08-disputes.md",
    "bindings/demos-node.md",
    "bindings/mcp-tools.md",
    "schemas/common.json",
    "schemas/listing.schema.json",
    "schemas/envelope.schema.json",
    "schemas/agreement.schema.json",
    "schemas/settlement-evidence.schema.json",
    "schemas/attestation-bundle.schema.json",
]

EXPECTED_SCHEMA_IDS = {
    "common.json": "https://dacs.demos.network/schemas/2/common.json",
    "listing.schema.json": "https://dacs.demos.network/schemas/2/listing.schema.json",
    "envelope.schema.json": "https://dacs.demos.network/schemas/2/envelope.schema.json",
    "agreement.schema.json": "https://dacs.demos.network/schemas/2/agreement.schema.json",
    "settlement-evidence.schema.json": "https://dacs.demos.network/schemas/2/settlement-evidence.schema.json",
    "attestation-bundle.schema.json": "https://dacs.demos.network/schemas/2/attestation-bundle.schema.json",
}

# Schema title -> separator registry kind. Only schema-backed core artifacts are
# required here; spec-only artifacts may exist without a schema at this draft stage.
SCHEMA_TITLE_TO_REGISTRY_KIND = {
    "Listing": "Listing",
    "DacsEnvelope": "DacsEnvelope",
    "AgreementDocument": "AgreementDocument",
    "SettlementEvidence": "SettlementEvidence",
    "AttestationBundle": "AttestationBundle",
}

REGISTRY_ROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*`([^`]+:v2:)`\s*\|", re.MULTILINE)
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def fail(errors: list[str]) -> None:
    if errors:
        for err in errors:
            print(f"DACS/2 validation error: {err}", file=sys.stderr)
        raise SystemExit(1)


def anchor_for_heading(text: str) -> str:
    # GitHub-ish anchor approximation good enough for local package links.
    text = text.strip().lower()
    text = re.sub(r"[`*_[\]()]", "", text)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def anchors_in(path: Path) -> set[str]:
    anchors: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            if heading:
                anchors.add(anchor_for_heading(heading))
    return anchors


def validate_required_files(errors: list[str]) -> None:
    if not DACS2.exists():
        errors.append("missing dacs-2/ package")
        return
    for rel in REQUIRED_FILES:
        if not (DACS2 / rel).is_file():
            errors.append(f"missing required file dacs-2/{rel}")


def validate_json_schemas(errors: list[str]) -> dict[Path, dict]:
    schemas: dict[Path, dict] = {}
    for path in sorted((DACS2 / "schemas").glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - error path exercised by tests
            errors.append(f"{path.relative_to(ROOT)} is not valid JSON: {exc}")
            continue
        schemas[path] = data
        expected_id = EXPECTED_SCHEMA_IDS.get(path.name)
        if expected_id and data.get("$id") != expected_id:
            errors.append(
                f"{path.relative_to(ROOT)} has $id {data.get('$id')!r}; expected {expected_id!r}"
            )
        if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{path.relative_to(ROOT)} must declare JSON Schema 2020-12")
        if path.name != "common.json" and "dacs" not in json.dumps(data):
            errors.append(f"{path.relative_to(ROOT)} does not appear to constrain DACS major version")
    return schemas


def validate_markdown_links(errors: list[str]) -> None:
    for path in sorted(DACS2.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for match in MD_LINK_RE.finditer(text):
            href = match.group(1).strip()
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            if href.startswith("#"):
                target = path
                anchor = href[1:]
            else:
                target_part, _, anchor = href.partition("#")
                target = (path.parent / target_part).resolve()
                try:
                    target.relative_to(DACS2.resolve())
                except ValueError:
                    errors.append(f"{path.relative_to(ROOT)} link escapes dacs-2/: {href}")
                    continue
            if not target.exists():
                errors.append(f"{path.relative_to(ROOT)} broken link target: {href}")
                continue
            if anchor and target.suffix == ".md":
                if anchor not in anchors_in(target):
                    errors.append(f"{path.relative_to(ROOT)} broken markdown anchor: {href}")


def parse_separator_registry(errors: list[str]) -> dict[str, str]:
    spec = DACS2 / "spec/01-canonical-form-and-signatures.md"
    text = spec.read_text(encoding="utf-8")
    registry: dict[str, str] = {}
    for kind, sep in REGISTRY_ROW_RE.findall(text):
        normalized = kind.strip().replace("**", "")
        if normalized in registry:
            errors.append(f"duplicate DACS/2 separator registry kind: {normalized}")
        registry[normalized] = sep
    if len(registry) < 10:
        errors.append("DACS/2 separator registry appears incomplete")
    for kind, sep in registry.items():
        if not sep.startswith("dacs-") or not sep.endswith(":v2:"):
            errors.append(f"invalid DACS/2 separator for {kind}: {sep}")
    return registry


def validate_schema_separator_comments(errors: list[str], schemas: dict[Path, dict], registry: dict[str, str]) -> None:
    for path, data in schemas.items():
        title = data.get("title")
        kind = SCHEMA_TITLE_TO_REGISTRY_KIND.get(title)
        if not kind:
            continue
        expected = registry.get(kind)
        if not expected:
            errors.append(f"schema {path.name} maps to registry kind {kind!r}, but registry lacks it")
            continue
        dumped = json.dumps(data, sort_keys=True)
        if expected not in dumped:
            errors.append(
                f"{path.relative_to(ROOT)} should carry separator {expected!r} in a $comment or equivalent"
            )


def validate_migration_and_readme(errors: list[str]) -> None:
    readme = (DACS2 / "README.md").read_text(encoding="utf-8")
    migration = (DACS2 / "MIGRATION.md").read_text(encoding="utf-8")
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for required in ["Identify → Vet → Negotiate → Settle → Verify → Resolve", "dacs/2.0-draft.1", "Demos binding"]:
        if required not in readme:
            errors.append(f"dacs-2/README.md missing required phrase: {required}")
    for required in ["v0.1 → DACS/2", ":v2:", "getTransactionHistory"]:
        if required not in migration:
            errors.append(f"dacs-2/MIGRATION.md missing required phrase: {required}")
    if "Fork-native DACS/2 track" not in root_readme or "dacs-2/" not in root_readme:
        errors.append("root README must point readers at fork-native dacs-2/ track")


def main() -> None:
    errors: list[str] = []
    validate_required_files(errors)
    if not DACS2.exists():
        fail(errors)
    schemas = validate_json_schemas(errors)
    validate_markdown_links(errors)
    registry = parse_separator_registry(errors)
    validate_schema_separator_comments(errors, schemas, registry)
    validate_migration_and_readme(errors)
    fail(errors)
    print(f"DACS/2 package OK: {len(schemas)} schemas, {len(registry)} domain separators")


if __name__ == "__main__":
    main()
