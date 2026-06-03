import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_conformance_vectors.py"
VECTORS = ROOT / "conformance" / "vectors" / "dacs-v0.1-happy-path.json"
INDEX = ROOT / "conformance" / "vectors" / "README.md"


def run_validator(*extra_args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(SCRIPT), *extra_args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


class ConformanceVectorValidationTests(unittest.TestCase):
    def test_happy_path_vector_file_exists_and_is_json_object(self):
        self.assertTrue(VECTORS.exists(), "expected canonical v0.1 happy-path conformance vector")
        data = json.loads(VECTORS.read_text())
        self.assertEqual(data["dacsVersion"], "0.1")
        self.assertEqual(data["vectorId"], "dacs-v0.1-happy-path")

    def test_validator_accepts_repository_vectors(self):
        result = run_validator()
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("validated 1 vector", result.stdout)

    def test_vector_covers_all_five_dacs_stages_in_order(self):
        data = json.loads(VECTORS.read_text())
        stages = [artifact["stage"] for artifact in data["artifacts"]]
        self.assertEqual(stages, ["DACS-1", "DACS-2", "DACS-3", "DACS-4", "DACS-5"])

    def test_artifacts_have_stable_content_hashes_and_spec_refs(self):
        data = json.loads(VECTORS.read_text())
        for artifact in data["artifacts"]:
            with self.subTest(artifact=artifact["id"]):
                self.assertTrue(artifact["contentHash"].startswith("sha256:"))
                self.assertEqual(len(artifact["contentHash"].removeprefix("sha256:")), 64)
                self.assertTrue(artifact["specRefs"])
                self.assertTrue(all(ref.startswith("§") for ref in artifact["specRefs"]))

    def test_vector_readme_documents_how_to_run_validation(self):
        text = INDEX.read_text()
        self.assertIn("python3 scripts/validate_conformance_vectors.py", text)
        self.assertIn("dacs-v0.1-happy-path.json", text)


if __name__ == "__main__":
    unittest.main()
