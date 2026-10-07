import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import check_ecosystem  # noqa: E402

ENTRIES = [
    {"id": "ECO-001", "owner": "a", "name": "active", "status": "listed", "verification": {"method": "git clone --depth 1", "last_commit": "2026-09-30"}},
    {"id": "ECO-002", "owner": "a", "name": "gone", "status": "listed"},
    {"id": "ECO-003", "owner": "a", "name": "old", "status": "archived-reported"},
    {"id": "ECO-004", "owner": "a", "name": "moved", "status": "listed"},
    {"id": "ECO-005", "owner": "a", "name": "wrong", "status": "archived-reported"},
    {"id": "ECO-006", "owner": "a", "name": "surprise", "status": "listed"},
]


def fake(url):
    name = url.rsplit("/", 1)[1]
    if name == "gone":
        raise check_ecosystem.NotFound(url)
    return {
        "active": {"archived": False, "full_name": "a/active"},
        "old": {"archived": True, "full_name": "a/old"},
        "moved": {"archived": False, "full_name": "b/moved"},
        "wrong": {"archived": False, "full_name": "a/wrong"},
        "surprise": {"archived": True, "full_name": "a/surprise"},
    }[name]


class EcosystemCheckTests(unittest.TestCase):
    def setUp(self):
        self.updated, self.notes = check_ecosystem.run(ENTRIES, fake, today="2026-10-07")
        self.by_id = {e["id"]: e for e in self.updated}
        self.text = "\n".join(self.notes)

    def test_drift_is_reported(self):
        self.assertIn("ECO-002", self.text)  # not found
        self.assertIn("ECO-004", self.text)  # renamed
        self.assertIn("recorded as archived but active", self.text)  # ECO-005
        self.assertIn("archived on GitHub but not recorded as archived", self.text)  # ECO-006
        self.assertNotIn("ECO-001", self.text)
        self.assertNotIn("ECO-003", self.text)  # reported archived and still archived: consistent

    def test_adds_api_fields_and_keeps_git_fields(self):
        v = self.by_id["ECO-001"]["verification"]
        self.assertEqual(v["method"], "git clone --depth 1")
        self.assertEqual(v["last_commit"], "2026-09-30")
        self.assertIs(v["archived"], False)
        self.assertEqual(v["api_checked"], "2026-10-07")
        self.assertEqual(self.by_id["ECO-004"]["verification"]["renamed_to"], "b/moved")

    def test_never_changes_analyst_fields(self):
        for before, after in zip(ENTRIES, self.updated, strict=True):
            for key in ("status", "evidence_class", "section", "techniques"):
                self.assertEqual(before.get(key), after.get(key))

    def test_rate_limit_stops_without_losing_entries(self):
        def limited(url):
            raise check_ecosystem.RateLimited(url)

        updated, notes = check_ecosystem.run(ENTRIES, limited, today="2026-10-07")
        self.assertEqual(len(updated), len(ENTRIES))
        self.assertIn("rate limited", notes[0])


if __name__ == "__main__":
    unittest.main()
