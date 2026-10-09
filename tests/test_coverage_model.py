import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import coverage_model  # noqa: E402
from common import load_data  # noqa: E402


class CoverageModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = coverage_model.build()
        cls.rows = {r["id"]: r for r in cls.model["techniques"]}

    def test_one_row_per_technique_in_data_order(self):
        self.assertEqual([r["id"] for r in self.model["techniques"]], [t["id"] for t in load_data("techniques")])

    def test_rule_files_are_found_from_the_filesystem(self):
        files = coverage_model.rule_files()
        for det in ("DET-AI-001", "DET-AI-002", "DET-AI-011"):
            self.assertIn(det, files)
        implemented = {d["id"] for r in self.model["techniques"] for d in r["detections"] if d["implementation"] == "rule-file"}
        self.assertEqual(implemented, set(files) & {d["id"] for d in load_data("detections")})

    def test_every_detection_is_linked_to_a_known_record(self):
        known = {d["id"] for d in load_data("detections")}
        for row in self.model["techniques"]:
            for d in row["detections"]:
                self.assertIn(d["id"], known)
                self.assertEqual(bool(d["platforms"]), d["implementation"] == "rule-file")

    def test_maturity_matches_the_derivation(self):
        import maturity
        for tid, level in maturity.derive_all().items():
            self.assertEqual(self.rows[tid]["maturity"], level)

    def test_benchmarks_are_ecosystem_benchmarks_only(self):
        eco = {e["id"]: e for e in load_data("ecosystem")}
        for row in self.model["techniques"]:
            for b in row["benchmarks"]:
                self.assertEqual(eco[b]["evidence_class"], "benchmark")
                self.assertIn(row["id"], eco[b]["techniques"])

    def test_ecosystem_never_counts_as_evidence(self):
        for row in self.model["techniques"]:
            for e in row["evidence"]:
                self.assertTrue(e.startswith(coverage_model.EVIDENCE_PREFIXES), e)

    def test_priority_follows_the_documented_formula(self):
        for row in self.model["techniques"]:
            det = 1 if any(d["implementation"] == "rule-file" for d in row["detections"]) else (0.5 if row["detections"] else 0)
            layers = bool(row["tests"]) + det + bool(row["controls"]) + bool(row["benchmarks"])
            self.assertEqual(row["layers"], layers)
            self.assertEqual(row["priority"], round(coverage_model.MATURITY_WEIGHT[row["maturity"]] * (4 - layers), 1))

    def test_partial_dates_count_as_the_end_of_their_period(self):
        self.assertEqual(coverage_model.latest_day("2026").isoformat(), "2026-12-31")
        self.assertEqual(coverage_model.latest_day("2026-02").isoformat(), "2026-02-28")
        self.assertEqual(coverage_model.latest_day("2026-02-03").isoformat(), "2026-02-03")

    def test_reference_date_is_never_a_bare_year(self):
        self.assertEqual(len(self.model["as_of"]), 10)

    def test_matrix_only_links_actors_to_techniques_through_campaigns(self):
        campaigns = {c["id"] for c in load_data("campaigns")}
        for m in self.model["matrix"]:
            self.assertTrue(m["via"])
            self.assertTrue(set(m["via"]) <= campaigns)

    def test_summary_matches_rows(self):
        s = self.model["summary"]
        self.assertEqual(s["techniques"], len(self.model["techniques"]))
        self.assertEqual(s["with_rule_file"] + s["specification_only"] + s["no_detection"], s["techniques"])
        self.assertEqual(s["detections_total"], len(load_data("detections")))

    def test_output_is_valid_json_round_trip(self):
        self.assertEqual(json.loads(json.dumps(self.model)), self.model)


if __name__ == "__main__":
    unittest.main()
