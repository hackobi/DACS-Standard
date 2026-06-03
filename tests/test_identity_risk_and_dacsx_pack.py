import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "spec" / "SPECIFICATION.md"
ROADMAP = ROOT / "ROADMAP.md"
VERIFY_DACSX = ROOT / "scripts" / "verify_dacsx_dispute_pack.py"


class IdentityRiskAndDacsXPackTests(unittest.TestCase):
    def test_v01_spec_does_not_absorb_future_risk_or_dispute_improvements(self):
        text = SPEC.read_text(encoding="utf-8")
        self.assertNotIn('identityTier?: "institutional" | "verified" | "self-declared"', text)
        self.assertNotIn("suspiciousPatternFlags?: string[]", text)
        self.assertNotIn("DACS-X interface seam (non-normative pack)", text)

    def test_roadmap_tracks_identity_reputation_and_dacsx_improvements(self):
        text = ROADMAP.read_text(encoding="utf-8")
        self.assertIn("`identityTier` on IdentityBundle (#103)", text)
        self.assertIn("`suspiciousPatternFlags` on ReputationRecord + min-bundleCount gating advice (#101)", text)
        self.assertIn("DACS-X (dispute / execution-verification)", text)
        self.assertIn("DACS-X shared dispute fixtures / verifier pack (#99)", text)
        self.assertIn("HTLC-9 correction-amendment", text)
        self.assertIn("non-normative", text)

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
