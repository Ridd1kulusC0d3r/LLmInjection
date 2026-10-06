import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import intel_intake  # noqa: E402


class IntakeHelpers(unittest.TestCase):
    def test_compact_collapses_whitespace_and_truncates(self):
        self.assertEqual(intel_intake.compact("a \n  b", 10), "a b")
        self.assertEqual(len(intel_intake.compact("x" * 50, 5)), 5)
        self.assertEqual(intel_intake.compact(None), "")

    def test_matched_terms_short_terms_need_word_boundary(self):
        self.assertEqual(intel_intake.matched_terms("fair trade", ["ai"]), [])
        self.assertEqual(intel_intake.matched_terms("new AI agent", ["ai"]), ["ai"])

    def test_identifier_regex(self):
        text = "CVE-2025-1234 GHSA-abcd-efgh-ijkl AML.T0051"
        self.assertEqual(len(intel_intake.IDENTIFIER_RE.findall(text)), 3)


if __name__ == "__main__":
    unittest.main()
