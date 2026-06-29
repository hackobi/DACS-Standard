import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_FILES = [
    ROOT / "spec" / "CORE.md",
    ROOT / "spec" / "DACS-1-IDENTIFY.md",
    ROOT / "spec" / "DACS-2-VET.md",
    ROOT / "spec" / "DACS-3-NEGOTIATE.md",
    ROOT / "spec" / "DACS-4-SETTLE.md",
    ROOT / "spec" / "DACS-5-VERIFY.md",
]


class SpecConsistencyRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = "\n".join(f.read_text(encoding="utf-8") for f in SPEC_FILES if f.exists())

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
                r"`terms\.rail` MUST be present if and only if the listing pipeline contains a `pay-\*` phase",
                re.DOTALL,
            ),
            "§8.5.2 should make rail validation conditional on whether the pipeline contains pay-*",
        )

    def test_rfq_fixed_price_fallback_is_type_expressible_and_validatable(self):
        """§8.8 fixedPriceFallback should not be rejected by Agreement validation."""
        self.assertIn(
            "fixedPriceFallback: true",
            self.spec,
        )
        self.assertRegex(
            self.spec,
            re.compile(
                r"fallback path produces a normal AgreementDocument with derivedFromPattern: \"fixed-price\"",
                re.DOTALL,
            ),
            "§8.8 should admit the explicit RFQ fixed-price fallback path",
        )

    def test_reputation_windowing_basis_is_an_input_to_derive(self):
        """The determinism receipt records a basis, so derive() must use it."""
        self.assertIn(
            "windowingBasis",
            self.spec,
        )
        self.assertRegex(
            self.spec,
            re.compile(
                r"windowingBasis.*\"finalisedAt\".*\"sr2-anchor-timestamp\"",
                re.DOTALL,
            ),
            "§10.5 should define both windowing bases",
        )


if __name__ == "__main__":
    unittest.main()
