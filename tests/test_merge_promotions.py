import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import merge_promotions as mp  # noqa: E402


class MergePromotionTests(unittest.TestCase):
    def merge(self, payload):
        m = mp.Merger()
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "p.json"
            p.write_text(json.dumps(payload), encoding="utf-8")
            m.merge_file(p)
        return m

    def test_held_source_url_maps_to_existing_id(self):
        held = mp.load_data("sources")[0]
        m = self.merge({"sources": [{"id": "SRC-NEW", "name": "x", "publisher": "y", "grade": "A", "url": held["url"]}],
                        "incidents": [{"id": "INCIDENT-T", "name": "t", "confidence": "high", "summary": "s", "source_ids": ["SRC-NEW"], "demonstrates": [{"technique": "LLMI-T028", "confidence": "high"}]}]})
        self.assertEqual(m.added["sources"], 0)
        self.assertEqual(m.d["incidents"][-1]["source_ids"], [held["id"]])
        self.assertEqual(m.d["relationships"][-1]["target"], "LLMI-T028")

    def test_existing_actor_is_not_duplicated_and_bad_links_drop(self):
        actor = mp.load_data("actors")[0]
        src = {"id": "SRC-X", "name": "x", "publisher": "y", "grade": "A", "url": "https://example.org/unique-report-x"}
        m = self.merge({"sources": [src],
                        "actors": [{"id": "ACTOR-DUP", "name": actor["name"], "confidence": "high", "summary": "s", "sources": [{"title": "x", "publisher": "y", "grade": "A", "url": src["url"]}]}],
                        "campaigns": [{"id": "CAMPAIGN-X", "name": "c", "confidence": "high", "summary": "s", "source_ids": ["SRC-X"], "actor_id": "ACTOR-DUP",
                                       "first_seen": "2026-09-xx", "uses": [{"technique": "LLMI-T999", "confidence": "high"}]}]})
        self.assertEqual(m.added["actors"], 0)
        rels = [r for r in m.d["relationships"] if r["target"] == "CAMPAIGN-X" or r["source"] == "CAMPAIGN-X"]
        self.assertEqual([(r["source"], r["relationship"]) for r in rels], [(actor["id"], "conducts")])
        self.assertEqual(m.d["campaigns"][-1]["first_seen"], "2026")
        self.assertTrue(any("unknown technique" in line for line in m.log))

    def test_record_without_resolvable_source_is_dropped(self):
        m = self.merge({"incidents": [{"id": "INCIDENT-Y", "name": "y", "confidence": "high", "summary": "s", "source_ids": ["SRC-NOPE"]}]})
        self.assertEqual(m.added["incidents"], 0)

    def test_ids_never_collide(self):
        existing = mp.load_data("incidents")[0]["id"]
        src = {"id": "SRC-Z", "name": "z", "publisher": "y", "grade": "A", "url": "https://example.org/unique-report-z"}
        m = self.merge({"sources": [src], "incidents": [{"id": existing, "name": "z", "confidence": "high", "summary": "s", "source_ids": ["SRC-Z"]}]})
        self.assertEqual(m.d["incidents"][-1]["id"], existing + "-2")


if __name__ == "__main__":
    unittest.main()
