import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "spec" / "SPECIFICATION.md"


class SpecConsistencyRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = SPEC.read_text(encoding="utf-8")

    def test_zero_pay_agreements_do_not_require_payment_rail(self):
        """PIPE-1 zero-pay listings must be able to produce valid agreements."""
        self.assertIn(
            "rail?: PaymentRailRef",
            self.spec,
            "AgreementDocument.terms.rail should be optional for pipelines with no pay-* phase",
        )
        self.assertRegex(
            self.spec,
            re.compile(
                r"if the resolved listing pipeline contains any `pay-\*` phase.*terms\.rail MUST appear in listing\.acceptedRails.*if the resolved listing pipeline contains no `pay-\*` phase.*terms\.rail MUST be absent",
                re.DOTALL,
            ),
            "§8.5.2 should make rail validation conditional on whether the pipeline contains pay-*",
        )
        self.assertIn(
            "If the resolved listing pipeline contains no `pay-*` phase, rail resolution is skipped",
            self.spec,
        )

    def test_rfq_fixed_price_fallback_is_type_expressible_and_validatable(self):
        """§8.8 fixedPriceFallback should not be rejected by Agreement validation."""
        self.assertIn(
            "negotiate-rfq — {maxTurns, timeoutSec, channelSubnet?, rfqInitiator?, fixedPriceFallback?}",
            self.spec,
        )
        self.assertRegex(
            self.spec,
            re.compile(
                r"derivedFromPattern MUST match the listing's selected negotiation path.*fixedPriceFallback.*derivedFromPattern == \"fixed-price\"",
                re.DOTALL,
            ),
            "§8.5.2 should admit the explicit RFQ fixed-price fallback path",
        )

    def test_reputation_windowing_basis_is_an_input_to_derive(self):
        """The determinism receipt records a basis, so derive() must use it."""
        self.assertIn(
            "derive(party, bundles, windowStart, windowEnd, windowingBasis):",
            self.spec,
        )
        self.assertIn(
            "bundle_window_time(b, windowingBasis)",
            self.spec,
        )
        self.assertRegex(
            self.spec,
            re.compile(
                r"where party in \{p\.primaryClaim for p in b\.parties\}\s+AND windowStart <= bundle_window_time\(b, windowingBasis\) <= windowEnd",
                re.DOTALL,
            ),
            "§10.5.1 should filter using the recorded windowingBasis, not always finalisedAt",
        )


if __name__ == "__main__":
    unittest.main()
