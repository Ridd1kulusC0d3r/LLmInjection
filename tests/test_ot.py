import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import ot_intake  # noqa: E402
import validate_ot  # noqa: E402


class CyberOTTests(unittest.TestCase):
    def test_registry_and_scenarios_validate(self):
        self.assertEqual(validate_ot.validate(), [])

    def test_offline_directory_metadata(self):
        source = next(s for s in validate_ot.load("ot-source-registry.json")["sources"]
                      if s["id"] == "OT-SRC-CISA-CSAF")
        fixture = [
            {"type": "file", "name": "icsa-26-example.json",
             "path": "csaf_files/OT/white/2026/icsa-26-example.json",
             "sha": "abc123", "html_url": "https://github.com/cisagov/CSAF/blob/develop/fictional"},
            {"type": "dir", "name": "ignore.json", "path": "ignored", "html_url": "https://github.com/example"},
        ]
        rows = ot_intake.discover(source, fixture, now="2026-10-09T00:00:00Z")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["evidence_status"], "unreviewed-metadata")
        self.assertEqual(rows[0]["status"], "candidate")
        self.assertEqual(rows[0]["id"], ot_intake.discover(source, fixture)[0]["id"])

    def test_metadata_change_forces_review(self):
        source = next(s for s in validate_ot.load("ot-source-registry.json")["sources"]
                      if s["id"] == "OT-SRC-ATTACK-ICS")
        row = {"type": "file", "name": "ics-attack-19.2.json",
               "path": "ics-attack/ics-attack-19.2.json", "sha": "old",
               "html_url": "https://github.com/mitre-attack/attack-stix-data/blob/master/ics-attack/ics-attack-19.2.json"}
        first = ot_intake.discover(source, [row])[0]
        queue = {"items": []}
        self.assertEqual(ot_intake.merge(queue, [first]), (1, 0))
        row["sha"] = "new"
        second = ot_intake.discover(source, [row])[0]
        self.assertEqual(ot_intake.merge(queue, [second]), (0, 1))
        self.assertEqual(queue["items"][0]["status"], "reviewing")

    def test_reject_automatic_incident_claim(self):
        sources = validate_ot.load("ot-source-registry.json")
        scenarios = validate_ot.load("ot-scenarios.json")
        scenarios[0]["status"] = "observed-in-the-wild"
        errors = validate_ot.validate(
            registry=sources, scenarios=scenarios,
            datasets=validate_ot.load("ot-datasets.json"),
            queue=validate_ot.load("ot-review-queue.json"))
        self.assertTrue(any("must not claim" in e for e in errors))

    def test_block_non_github_hosts(self):
        with self.assertRaises(ValueError):
            ot_intake.checked_url("https://example.net/private")
        with self.assertRaises(ValueError):
            ot_intake.checked_url("http://api.github.com/repos/a/b")


if __name__ == "__main__":
    unittest.main()
