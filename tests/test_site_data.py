import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_charts  # noqa: E402
import readme_stats  # noqa: E402
import re


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

    def test_readme_statistics_are_current(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertEqual(readme_stats.updated(text), text, "run python scripts/readme_stats.py")
        eco = (ROOT / "docs" / "ECOSYSTEM.md").read_text(encoding="utf-8")
        self.assertEqual(readme_stats.updated(eco), eco, "run python scripts/readme_stats.py")

    def test_relative_markdown_links_resolve(self):
        pages = [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md")), *sorted((ROOT / "references").glob("*.md"))]
        broken = []
        for page in pages:
            for target in re.findall(r"\]\(([^)\s]+)\)", page.read_text(encoding="utf-8")):
                if re.match(r"(https?:|mailto:|#)", target):
                    continue
                if not (page.parent / target.split("#")[0]).exists():
                    broken.append(f"{page.relative_to(ROOT)} -> {target}")
        self.assertEqual(broken, [])

    def test_ids_cited_in_readme_exist(self):
        known = set()
        for path in (ROOT / "data").glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                known |= {row["id"] for row in data if isinstance(row, dict) and "id" in row}
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        cited = set(re.findall(r"\b(?:TC-[A-Z]+-\d{3}|DET-AI-\d{3}|LLMI-T\d{3}|CTRL-[A-Z]+(?:-[A-Z]+)*)\b", text))
        self.assertEqual(sorted(cited - known), [])


if __name__ == "__main__":
    unittest.main()
