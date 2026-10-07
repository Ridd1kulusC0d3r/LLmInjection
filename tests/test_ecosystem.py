import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EcosystemTests(unittest.TestCase):
    def setUp(self):
        self.entries = json.loads((ROOT / "data" / "ecosystem.json").read_text(encoding="utf-8"))

    def test_curated_set(self):
        self.assertEqual(len(self.entries), 106)
        self.assertEqual(sum(e["priority"] == "start-here" for e in self.entries), 11)
        self.assertEqual(len({e["url"].lower() for e in self.entries}), len(self.entries))

    def test_no_entry_supports_attribution(self):
        for entry in self.entries:
            self.assertFalse({"attribution", "campaign"} & set(entry.get("supports", [])), entry["id"])

    def test_only_canonical_publishers_get_grade_a(self):
        graded_a = {e["owner"] for e in self.entries if e["source_grade"] == "A"}
        self.assertEqual(graded_a, {"mitre-atlas", "OWASP"})

    def test_verification_is_recorded(self):
        for entry in self.entries:
            ver = entry.get("verification")
            self.assertIsNotNone(ver, entry["id"])
            self.assertIn("reachable", ver)
            if ver["reachable"]:
                self.assertRegex(ver["last_commit"], r"^\d{4}-\d{2}-\d{2}$")
                self.assertTrue(ver["license"])
            self.assertIn("archive flag not visible to git", entry["provenance"])


if __name__ == "__main__":
    unittest.main()
