import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import tcem_validate as tv  # noqa: E402


class TcemCaseTests(unittest.TestCase):
    def setUp(self):
        self.dirs = sorted(p for p in (ROOT / "tcem" / "cases").iterdir() if (p / "case.json").exists())
        self.known = tv._known_ids()

    def test_there_are_cases(self):
        self.assertGreaterEqual(len(self.dirs), 6)

    def test_cases_are_well_formed_and_reference_real_records(self):
        for d in self.dirs:
            self.assertEqual(tv.check_case(tv.load_case(d), self.known), [], d.name)

    def test_replay_validations_pass(self):
        for d in self.dirs:
            for r in tv.run_validations(tv.load_case(d), d):
                self.assertTrue(r["passed"], f"{d.name} {r['spec']}: {r['matches']} matches")

    def test_recorded_status_matches_the_replay(self):
        for d in self.dirs:
            case = tv.load_case(d)
            ok = all(r["passed"] for r in tv.run_validations(case, d))
            self.assertEqual(case["validations"][0]["status"], "passed" if ok else "failed", d.name)

    def test_figures_exist(self):
        report = (ROOT / "reports" / "dossiers" / "tcem-artex.md").read_text(encoding="utf-8")
        for name in __import__("re").findall(r"assets/tcem/([\w.-]+\.svg)", report):
            self.assertTrue((ROOT / "assets" / "tcem" / name).exists(), name)

    def test_ordered_sequence_matches_tcem_semantics(self):
        logic = {"pattern": "ordered-sequence", "group_by": ["a.id"],
                 "stages": [{"all": [{"field": "event.action", "op": "eq", "value": "x"}]},
                            {"all": [{"field": "event.action", "op": "eq", "value": "y"}]}]}
        ev = lambda a, i: {"event": {"action": a}, "a": {"id": i}}  # noqa: E731
        self.assertEqual(tv.evaluate_logic(logic, [ev("x", 1), ev("y", 2), ev("y", 1)])["matches"], 1)
        self.assertEqual(tv.evaluate_logic(logic, [ev("y", 1), ev("x", 1)])["matches"], 0)


if __name__ == "__main__":
    unittest.main()
