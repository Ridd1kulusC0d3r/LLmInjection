import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import check_ecosystem  # noqa: E402

ENTRIES = [
    {"id": "ECO-001", "owner": "a", "name": "active", "status": "listed"},
    {"id": "ECO-002", "owner": "a", "name": "gone", "status": "listed"},
    {"id": "ECO-003", "owner": "a", "name": "old", "status": "archived-reported"},
    {"id": "ECO-004", "owner": "a", "name": "moved", "status": "listed"},
    {"id": "ECO-005", "owner": "a", "name": "wrong", "status": "archived-reported"},
]


def fake(url):
    name = url.rsplit("/", 1)[1]
    if name == "gone":
        raise check_ecosystem.NotFound(url)
    return {
        "active": {"archived": False, "pushed_at": "2026-09-30T10:00:00Z", "full_name": "a/active"},
        "old": {"archived": True, "pushed_at": "2025-01-02T00:00:00Z", "full_name": "a/old"},
        "moved": {"archived": False, "pushed_at": "2026-01-01T00:00:00Z", "full_name": "b/moved"},
        "wrong": {"archived": False, "pushed_at": "2026-02-01T00:00:00Z", "full_name": "a/wrong"},
    }[name]


class EcosystemCheckTests(unittest.TestCase):
    def test_states_and_drift(self):
        updated, notes = check_ecosystem.run(ENTRIES, fake, today="2026-10-07")
        by_id = {e["id"]: e for e in updated}
        self.assertEqual(by_id["ECO-001"]["status"], "active-verified")
        self.assertEqual(by_id["ECO-001"]["last_push"], "2026-09-30")
        self.assertEqual(by_id["ECO-002"]["status"], "not-found")
        self.assertEqual(by_id["ECO-003"]["status"], "archived-verified")
        self.assertEqual(by_id["ECO-004"]["renamed_to"], "b/moved")
        text = "\n".join(notes)
        self.assertIn("ECO-002", text)
        self.assertIn("ECO-004", text)
        self.assertIn("recorded as archived but active", text)
        self.assertNotIn("ECO-001", text)

    def test_never_changes_analyst_fields(self):
        entry = {**ENTRIES[0], "evidence_class": "benchmark", "section": "evaluation", "techniques": ["LLMI-T001"]}
        updated, _ = check_ecosystem.run([entry], fake, today="2026-10-07")
        for key in ("evidence_class", "section", "techniques"):
            self.assertEqual(updated[0][key], entry[key])

    def test_rate_limit_stops_without_losing_entries(self):
        def limited(url):
            raise check_ecosystem.RateLimited(url)

        updated, notes = check_ecosystem.run(ENTRIES, limited, today="2026-10-07")
        self.assertEqual(len(updated), len(ENTRIES))
        self.assertIn("rate limited", notes[0])


if __name__ == "__main__":
    unittest.main()
