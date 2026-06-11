import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_dacs2.py"


class Dacs2ValidationTests(unittest.TestCase):
    def run_validator(self):
        return subprocess.run(
            [sys.executable, str(VALIDATOR)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_repository_dacs2_package_validates(self):
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("DACS/2 package OK", result.stdout)

    def test_schema_ids_are_stable_and_versioned(self):
        schemas = sorted((ROOT / "dacs-2" / "schemas").glob("*.json"))
        self.assertGreaterEqual(len(schemas), 6)
        for path in schemas:
            data = json.loads(path.read_text())
            self.assertEqual(data.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
            self.assertIn("/schemas/2/", data.get("$id", ""))

    def test_dacs2_is_separate_from_v01_spec_tree(self):
        root_readme = (ROOT / "README.md").read_text()
        self.assertIn("Fork-native DACS/2 track", root_readme)
        self.assertTrue((ROOT / "dacs-2" / "README.md").exists())
        self.assertTrue((ROOT / "spec" / "CORE.md").exists())


if __name__ == "__main__":
    unittest.main()
