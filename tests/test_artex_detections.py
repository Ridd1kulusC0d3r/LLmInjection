import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ArtexDetectionMapTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "references" / "crosswalks" / "artex-detections.json").read_text(encoding="utf-8"))
        self.detections = {d["id"] for d in json.loads((ROOT / "data" / "detections.json").read_text(encoding="utf-8"))}

    def test_every_rule_file_is_assigned(self):
        self.assertEqual(self.data["summary"]["unassigned_files"], [])

    def test_mapped_detections_exist(self):
        for b in self.data["behaviours"]:
            if b["detection"]:
                self.assertIn(b["detection"], self.detections, b["behaviour"])

    def test_rules_are_links_to_the_upstream_repository(self):
        for b in self.data["behaviours"]:
            for r in b["rules"]:
                self.assertTrue(r["url"].startswith("https://github.com/ThreatDefence/artex-detections/"), r["path"])


if __name__ == "__main__":
    unittest.main()
