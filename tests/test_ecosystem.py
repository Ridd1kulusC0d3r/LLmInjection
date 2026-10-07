import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EcosystemTests(unittest.TestCase):
    def setUp(self):
        self.entries = json.loads((ROOT / "data" / "ecosystem.json").read_text(encoding="utf-8"))

    def test_curated_set(self):
        self.assertEqual(len(self.entries), 75)
        self.assertEqual(sum(e["priority"] == "start-here" for e in self.entries), 10)
        self.assertEqual(len({e["url"].lower() for e in self.entries}), 75)

    def test_no_entry_supports_attribution(self):
        for entry in self.entries:
            self.assertFalse({"attribution", "campaign"} & set(entry.get("supports", [])), entry["id"])

    def test_only_canonical_publishers_get_grade_a(self):
        graded_a = {e["owner"] for e in self.entries if e["source_grade"] == "A"}
        self.assertEqual(graded_a, {"mitre-atlas", "OWASP"})

    def test_unverified_state_is_disclosed(self):
        for entry in self.entries:
            self.assertIn("not independently verified", entry["provenance"])


if __name__ == "__main__":
    unittest.main()
