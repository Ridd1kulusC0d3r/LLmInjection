import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "lab-result.schema.json").read_text(encoding="utf-8"))


class LabResultTests(unittest.TestCase):
    def test_runner_passes_and_negative_control_fails(self):
        with tempfile.TemporaryDirectory() as d:
            run = subprocess.run([sys.executable, str(ROOT / "examples" / "run_gate_lab.py"), "--output", d], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            results = json.loads((Path(d) / "llmi-t008-gate.json").read_text(encoding="utf-8"))["results"]
        gate = [r for r in results if r["adapter"].startswith("examples/")]
        naive = [r for r in results if r["adapter"].startswith("naive")]
        self.assertEqual({r["result"] for r in gate}, {"pass"})
        self.assertEqual({r["result"] for r in naive}, {"fail"})  # a case the naive gate passes would prove nothing

    def test_committed_results_follow_the_schema_and_name_real_cases(self):
        ids = {c["id"] for c in json.loads((ROOT / "data" / "test-cases.json").read_text(encoding="utf-8"))}
        files = sorted((ROOT / "lab-results").glob("*.json"))
        self.assertTrue(files)
        for f in files:
            for r in json.loads(f.read_text(encoding="utf-8"))["results"]:
                self.assertTrue(set(SCHEMA["required"]) <= set(r), f.name)
                self.assertIn(r["result"], SCHEMA["properties"]["result"]["enum"])
                self.assertIn(r["test_case"], ids)
                self.assertTrue(r["observations"])


if __name__ == "__main__":
    unittest.main()
