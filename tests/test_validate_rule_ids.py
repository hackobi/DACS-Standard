import importlib.util
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_rule_ids.py"
ROOT = Path(__file__).resolve().parents[1]


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_rule_ids", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RuleIdValidationTests(unittest.TestCase):
    def test_repository_rule_ids_resolve_and_index_covers_defined_families(self):
        validator = load_validator()
        self.assertEqual(validator.validate_repo(ROOT), [])

    def test_reports_reference_to_undefined_rule_in_defined_family(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec = root / "spec"
            docs = root / "docs"
            spec.mkdir()
            docs.mkdir()
            (spec / "SPECIFICATION.md").write_text(
                "# Spec\n\n"
                "Conformance: (ABC-1) Producers MUST do the thing.\n\n"
                "The §14 plan references ABC-2, which does not exist.\n",
                encoding="utf-8",
            )
            (docs / "rule-id-index.md").write_text(
                "# Rule-ID index\n\n"
                "| Rule family | Role / surface | Spec section | Test-plan hook |\n"
                "|-------------|----------------|--------------|----------------|\n"
                "| ABC-* | Example rules | §1 | §14 |\n",
                encoding="utf-8",
            )
            validator = load_validator()
            errors = validator.validate_repo(root)
            self.assertEqual(errors, ["spec/SPECIFICATION.md: referenced rule ABC-2 is not defined"])

    def test_reports_missing_rule_family_index_entry(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec = root / "spec"
            docs = root / "docs"
            spec.mkdir()
            docs.mkdir()
            (spec / "SPECIFICATION.md").write_text("Conformance: (XYZ-1) Readers MUST reject bad input.\n", encoding="utf-8")
            (docs / "rule-id-index.md").write_text(
                "# Rule-ID index\n\n"
                "| Rule family | Role / surface | Spec section | Test-plan hook |\n"
                "|-------------|----------------|--------------|----------------|\n",
                encoding="utf-8",
            )
            validator = load_validator()
            errors = validator.validate_repo(root)
            self.assertEqual(errors, ["docs/rule-id-index.md: missing rule family entry: XYZ-*"])


if __name__ == "__main__":
    unittest.main()
