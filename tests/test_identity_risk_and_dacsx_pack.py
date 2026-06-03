import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "spec" / "SPECIFICATION.md"
VERIFY_DACSX = ROOT / "scripts" / "verify_dacsx_dispute_pack.py"


class IdentityRiskAndDacsXPackTests(unittest.TestCase):
    def test_spec_defines_identity_tier_derivation_and_reputation_flags(self):
        text = SPEC.read_text(encoding="utf-8")
        self.assertIn('identityTier?: "institutional" | "verified" | "self-declared"', text)
        self.assertIn("Identity tier derivation", text)
        self.assertIn("Only verified claims count toward identityTier", text)
        self.assertIn("suspiciousPatternFlags?: string[]", text)
        self.assertIn("MUST NOT change core reputation derivation", text)
        self.assertIn("high-volume-single-counterparty-cluster", text)

    def test_identity_tier_fixture_set_is_machine_readable(self):
        cases = {
            "institutional": "conformance/fixtures/identity/identity-tier-institutional.json",
            "verified": "conformance/fixtures/identity/identity-tier-verified.json",
            "self-declared": "conformance/fixtures/identity/identity-tier-self-declared.json",
        }
        for expected_tier, rel in cases.items():
            with self.subTest(rel=rel):
                data = json.loads((ROOT / rel).read_text(encoding="utf-8"))
                self.assertEqual(data["kind"], "IdentityTierCase")
                self.assertEqual(data["expectedIdentityTier"], expected_tier)
                self.assertIn("identityBundle", data)
                self.assertIn("claims", data["identityBundle"])

    def test_reputation_risk_fixture_is_advisory_only(self):
        fixture = ROOT / "conformance/fixtures/reputation/reputation-suspicious-pattern-flags.json"
        data = json.loads(fixture.read_text(encoding="utf-8"))
        self.assertEqual(data["kind"], "ReputationRiskCase")
        record = data["reputationRecord"]
        self.assertIsInstance(record["suspiciousPatternFlags"], list)
        self.assertTrue(record["suspiciousPatternFlags"])
        self.assertEqual(data["expectedCoreMetricsUnchanged"], True)

    def test_dacsx_dispute_outcome_fixture_links_to_htlc9_correction(self):
        fixture = ROOT / "conformance/fixtures/dacsx/dispute-outcome-htlc9-correction.json"
        data = json.loads(fixture.read_text(encoding="utf-8"))
        self.assertEqual(data["kind"], "DisputeOutcomeCase")
        outcome = data["disputeOutcome"]
        self.assertEqual(outcome["outcomeVersion"], "1")
        self.assertEqual(outcome["disputeKind"], "htlc9-asymmetric-settlement")
        correction = outcome["settlementAmendment"]
        self.assertEqual(correction["amendmentType"], "correction")
        self.assertNotIn("refundAmount", correction)
        self.assertEqual(correction["reason"], "dacsx-htlc9-source-claim-confirmed")

    def test_shared_dacsx_verifier_accepts_repository_fixtures(self):
        result = subprocess.run(
            ["python3", str(VERIFY_DACSX)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("validated DACS-X dispute pack", result.stdout)


if __name__ == "__main__":
    unittest.main()
