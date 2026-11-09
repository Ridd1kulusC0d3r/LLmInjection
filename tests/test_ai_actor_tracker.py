import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import ai_actor_tracker_check as t  # noqa: E402
from common import ROOT, load_data  # noqa: E402

TRACKER = {"entries": [
    {"table": "main", "name": "GTG-1002", "akas": "", "brief": "x", "ttp_md": "T1059 and T1566.001", "reported": "Nov 2025", "activity": ""},
    {"table": "main", "name": "NEWCLUSTER", "akas": "Some Panda", "brief": "x", "ttp_md": "T9999", "reported": "Jul 2026", "activity": ""},
    {"table": "deepfake", "name": "Deepfake case", "akas": "", "brief": "x", "ttp_md": "", "reported": "2024", "activity": ""},
]}
STIX = {"objects": [
    {"type": "identity", "id": "identity--1", "name": "Vendor"},
    {"type": "intrusion-set", "id": "intrusion-set--1", "name": "NEWCLUSTER", "external_references": [
        {"source_name": "Vendor", "url": "https://unit42.paloaltonetworks.com/new-cluster"},
        {"source_name": "Press", "url": "https://news.example/new-cluster"}]},
    {"type": "report", "id": "report--1", "name": "Vendor report", "published": "2026-07-01T00:00:00Z", "created_by_ref": "identity--1",
     "external_references": [{"url": "https://unit42.paloaltonetworks.com/new-cluster"}, {"url": "http://insecure.example/x"}]},
]}


class AiActorTrackerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        (root / "stix").mkdir()
        (root / "tracker.json").write_text(json.dumps(TRACKER), encoding="utf-8")
        (root / t.STIX).write_text(json.dumps(STIX), encoding="utf-8")
        (root / "Sources.md").write_text("[a](https://github.com/cybershujin/x) [b](https://www.anthropic.com/news/disrupting-AI-espionage)", encoding="utf-8")
        attack = {"T1059": {"name": "Command and Scripting Interpreter", "retired": False}, "T1566.001": {"name": "Spearphishing Attachment", "retired": True}}
        self.report = t.build(t.read_tracker(root), t.report_urls(root), attack, {"commit": "abc", "date": "2026-11-09"})

    def tearDown(self):
        self.tmp.cleanup()

    def test_known_actor_matches_and_new_one_does_not(self):
        by = {a["name"]: a for a in self.report["actors"]}
        self.assertEqual(by["GTG-1002"]["llminjection_actor"], "ACTOR-GTG-1002")
        self.assertIsNone(by["NEWCLUSTER"]["llminjection_actor"])
        self.assertTrue(by["NEWCLUSTER"]["has_primary_reference"])
        self.assertEqual(by["NEWCLUSTER"]["score"], 20 + 30 + 20 + 20)

    def test_sources_skip_tracker_pages_http_and_urls_we_hold(self):
        urls = {s["url"] for s in self.report["sources_not_held"]}
        self.assertEqual(urls, {"https://unit42.paloaltonetworks.com/new-cluster"})

    def test_attack_ids_are_checked(self):
        rows = {r["id"]: r["status"] for r in self.report["attack_ids"]}
        self.assertEqual(rows, {"T1059": "ok", "T1566.001": "retired", "T9999": "unknown-id"})

    def test_queue_items_are_candidates_without_copied_text(self):
        new = next(a for a in self.report["actors"] if a["name"] == "NEWCLUSTER")
        item = t.actor_item(new, "2026-11-09T00:00:00Z")
        self.assertEqual((item["status"], item["kind"], item["source_grade"]), ("candidate", "actor-candidate", "D"))
        self.assertEqual(item["url"], "https://unit42.paloaltonetworks.com/new-cluster")
        self.assertNotIn("x", item["summary"].split())  # the tracker's description is never copied

    def test_committed_crosswalk_and_queue_are_consistent(self):
        data = json.loads(t.OUT.read_text(encoding="utf-8"))
        self.assertEqual(data["source"]["license"], "none declared")
        for a in data["actors"]:
            self.assertNotIn("brief", a)
        ids = {i["id"] for i in load_data("research-queue")["items"]}
        for a in data["actors"]:
            if a["table"] == "main" and not a["llminjection_actor"] and (t.year(a["reported"]) or 0) >= 2025:
                self.assertIn(f"RQ-AIT-ACTOR-{t.slug(a['name'])}", ids)
        self.assertTrue((ROOT / "docs" / "ACTORS-USING-AI.md").read_text(encoding="utf-8").count("RQ-") == 0)


if __name__ == "__main__":
    unittest.main()
