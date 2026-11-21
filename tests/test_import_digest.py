import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import import_digest  # noqa: E402

DIGEST = {"digest_id": "LLMI-20990101"}
ITEM = {"id": "LLMI-20990101-01", "title": "t", "url": "https://example.org/a", "published": None, "seal": "original",
        "source_grade": "A", "kind": "threat-report", "techniques": ["LLMI-T001", "LLMI-T999"], "summary": "s",
        "brazil_latam": True}


class ImportDigestTests(unittest.TestCase):
    def test_item_keeps_its_own_grade_and_drops_unknown_techniques(self):
        row = import_digest.to_queue(ITEM, DIGEST, {"LLMI-T001"}, "2099-01-01T00:00:00Z")
        self.assertEqual(row["id"], "RQ-DIG-20990101-01")
        self.assertEqual(row["source_grade"], "A")
        self.assertEqual(row["status"], "candidate")
        self.assertEqual(row["matched_terms"], ["LLMI-T001", "brazil-latam"])

    def test_score_orders_grade_then_seal(self):
        a = import_digest.score({**ITEM, "brazil_latam": False})
        b = import_digest.score({**ITEM, "source_grade": "C", "seal": "secondary", "brazil_latam": False})
        self.assertGreater(a, b)
        self.assertLessEqual(import_digest.score(ITEM), 100)

    def test_digest_files_are_well_formed(self):
        for path in (Path(__file__).resolve().parents[1] / "intake" / "digests").glob("*.json"):
            digest = import_digest.json.loads(path.read_text(encoding="utf-8"))
            for item in digest["items"]:
                self.assertRegex(item["id"], import_digest.ITEM_ID, path.name)
                self.assertIn(item["seal"], import_digest.SEALS, item["id"])
                self.assertIn(item["source_grade"], import_digest.GRADES, item["id"])
                self.assertTrue(item["url"].startswith("https://"), item["id"])

    def test_colliding_queue_id_is_refused_not_duplicated(self):
        import json
        import tempfile
        from unittest import mock

        queue = {"meta": {}, "items": [{"id": "RQ-DIG-20990101-01", "url": "https://example.org/other"}]}
        digest = {**DIGEST, "items": [ITEM, {**ITEM, "id": "LLMI-20990101-02", "url": "https://example.org/b"}]}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "d.json"
            path.write_text(json.dumps(digest), encoding="utf-8")
            data = {"research-queue": queue, "sources": [], "techniques": [{"id": "LLMI-T001"}]}
            with mock.patch.object(import_digest, "load_data", side_effect=lambda name: data[name]):
                report = import_digest.run([path], dry_run=True)
        self.assertEqual(report["added"], ["LLMI-20990101-02"])
        self.assertTrue(any("already in the queue" in r for r in report["refused"]))


if __name__ == "__main__":
    unittest.main()
