import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AgenticAttackDetectionMapTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "references" / "crosswalks" / "agentic-attack-detections.json").read_text(encoding="utf-8"))

        def ids(name):
            return {x["id"] for x in json.loads((ROOT / "data" / f"{name}.json").read_text(encoding="utf-8"))}

        self.detections, self.tools = ids("detections"), ids("tools")
        self.records = ids("actors") | ids("campaigns") | ids("incidents")

    def test_every_rule_file_is_assigned(self):
        self.assertEqual(self.data["summary"]["unassigned_files"], [])

    def test_mapped_ids_exist(self):
        self.assertEqual(self.data["summary"]["unknown_detections"], [])
        for f in self.data["frameworks"]:
            self.assertTrue(set(f["detections"]) <= self.detections, f["framework"])
            self.assertTrue(set(f["tools"]) <= self.tools, f["framework"])
        for s in self.data["intrusion_sets"]:
            self.assertTrue(set(s["llminjection"]) <= self.records, s["name"])

    def test_links_point_upstream(self):
        for f in self.data["frameworks"]:
            self.assertTrue(f["folder"].startswith("https://github.com/ThreatDefence/agentic-attack-detections/"))
        for s in self.data["shared_behaviours"]:
            self.assertTrue(s["url"].startswith("https://github.com/ThreatDefence/agentic-attack-detections/"))


if __name__ == "__main__":
    unittest.main()
