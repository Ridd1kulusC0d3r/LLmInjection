import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_charts  # noqa: E402


class SiteDataTests(unittest.TestCase):
    def test_coverage_chart_is_current(self):
        """assets/coverage-matrix.svg must match the data; run scripts/build_charts.py to refresh."""
        self.assertEqual((ROOT / "assets" / "coverage-matrix.svg").read_text(encoding="utf-8"), build_charts.build())

    def test_landscape_metric_values_are_renderable(self):
        landscape = json.loads((ROOT / "data" / "threat-landscape-2026.json").read_text(encoding="utf-8"))
        for metric in landscape["key_metrics"]:
            value = metric["value"]
            ok = isinstance(value, (int, float)) or (isinstance(value, dict) and {"from", "to"} <= value.keys())
            self.assertTrue(ok, f"{metric['id']} has a value the Explorer cannot format: {value!r}")


if __name__ == "__main__":
    unittest.main()
