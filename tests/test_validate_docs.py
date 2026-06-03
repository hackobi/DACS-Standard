import importlib.util
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate-docs.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_docs", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidateDocsTests(unittest.TestCase):
    def test_accepts_existing_relative_markdown_links_and_anchors(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Root\n\nSee [Guide](docs/guide.md#deep-section).\n",
                encoding="utf-8",
            )
            docs = root / "docs"
            docs.mkdir()
            (docs / "guide.md").write_text("# Guide\n\n## Deep Section\n", encoding="utf-8")

            validator = load_validator()

            self.assertEqual(validator.validate_repo(root), [])

    def test_reports_missing_relative_markdown_target(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Root\n\nSee [Missing](docs/missing.md).\n",
                encoding="utf-8",
            )

            validator = load_validator()

            errors = validator.validate_repo(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("missing target", errors[0])
            self.assertIn("docs/missing.md", errors[0])

    def test_reports_missing_anchor(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Root\n\nSee [Guide](docs/guide.md#does-not-exist).\n",
                encoding="utf-8",
            )
            docs = root / "docs"
            docs.mkdir()
            (docs / "guide.md").write_text("# Guide\n\n## Different Section\n", encoding="utf-8")

            validator = load_validator()

            errors = validator.validate_repo(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("missing anchor", errors[0])
            self.assertIn("#does-not-exist", errors[0])


if __name__ == "__main__":
    unittest.main()
