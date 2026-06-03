#!/usr/bin/env python3
"""Validate DACS conformance vector files.

This is intentionally stdlib-only so implementers can run it from a clean clone:

    python3 scripts/validate_conformance_vectors.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VECTOR_DIR = ROOT / "conformance" / "vectors"
EXPECTED_STAGES = ["DACS-1", "DACS-2", "DACS-3", "DACS-4", "DACS-5"]
REQUIRED_TOP_LEVEL = {
    "vectorId",
    "title",
    "dacsVersion",
    "description",
    "artifacts",
    "expectedResult",
}
REQUIRED_ARTIFACT = {
    "id",
    "stage",
    "kind",
    "specRefs",
    "domainSeparator",
    "artifact",
    "contentHash",
}


def canonical_json(value: Any) -> bytes:
    """Return stable JSON bytes approximating RFC 8785 for these vectors.

    The vectors deliberately avoid floats and non-string map keys, so sorted-key JSON
    with compact separators is sufficient for deterministic test fixtures.
    """

    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_uri(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value)).hexdigest()


def fail(path: Path, message: str) -> str:
    return f"{path.relative_to(ROOT)}: {message}"


def validate_vector(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [fail(path, f"invalid JSON: {exc}")]

    if not isinstance(data, dict):
        return [fail(path, "top-level value MUST be an object")]

    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        errors.append(fail(path, f"missing top-level keys: {', '.join(missing)}"))

    if data.get("dacsVersion") != "0.1":
        errors.append(fail(path, "dacsVersion MUST be '0.1' for this vector set"))

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append(fail(path, "artifacts MUST be a non-empty array"))
        return errors

    stages = []
    artifact_ids = set()
    for idx, artifact in enumerate(artifacts):
        prefix = f"artifact[{idx}]"
        if not isinstance(artifact, dict):
            errors.append(fail(path, f"{prefix} MUST be an object"))
            continue

        missing_artifact = sorted(REQUIRED_ARTIFACT - set(artifact))
        if missing_artifact:
            errors.append(fail(path, f"{prefix} missing keys: {', '.join(missing_artifact)}"))
            continue

        artifact_id = artifact["id"]
        if artifact_id in artifact_ids:
            errors.append(fail(path, f"duplicate artifact id: {artifact_id}"))
        artifact_ids.add(artifact_id)

        stage = artifact["stage"]
        stages.append(stage)
        if stage not in EXPECTED_STAGES:
            errors.append(fail(path, f"{artifact_id}: unknown stage {stage!r}"))

        refs = artifact["specRefs"]
        if not isinstance(refs, list) or not refs or not all(isinstance(ref, str) and ref.startswith("§") for ref in refs):
            errors.append(fail(path, f"{artifact_id}: specRefs MUST be non-empty § references"))

        separator = artifact["domainSeparator"]
        if not isinstance(separator, str) or not separator.endswith(":v1:"):
            errors.append(fail(path, f"{artifact_id}: domainSeparator SHOULD end with ':v1:'"))

        expected_hash = sha256_uri(artifact["artifact"])
        if artifact["contentHash"] != expected_hash:
            errors.append(
                fail(
                    path,
                    f"{artifact_id}: contentHash mismatch; expected {expected_hash}, got {artifact['contentHash']}",
                )
            )

    if stages != EXPECTED_STAGES:
        errors.append(fail(path, f"artifacts MUST cover stages in order: {EXPECTED_STAGES}; got {stages}"))

    expected = data.get("expectedResult", {})
    if not isinstance(expected, dict) or expected.get("verifies") is not True:
        errors.append(fail(path, "expectedResult.verifies MUST be true for happy-path vectors"))

    return errors


def iter_vector_files(vector_dir: Path) -> list[Path]:
    return sorted(p for p in vector_dir.glob("*.json") if p.is_file())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate DACS conformance vector JSON files")
    parser.add_argument("paths", nargs="*", help="Specific vector files to validate")
    args = parser.parse_args(argv)

    paths = [Path(p) for p in args.paths] if args.paths else iter_vector_files(DEFAULT_VECTOR_DIR)
    if not paths:
        print(f"no vector files found under {DEFAULT_VECTOR_DIR.relative_to(ROOT)}", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for path in paths:
        all_errors.extend(validate_vector(path))

    if all_errors:
        print("conformance vector validation failed:", file=sys.stderr)
        for error in all_errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    plural = "s" if len(paths) != 1 else ""
    print(f"validated {len(paths)} vector{plural}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
