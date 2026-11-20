import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_site  # noqa: E402


class SiteSpacesTests(unittest.TestCase):
    def test_report_index_lists_every_report_with_the_platform_first(self):
        platform = {"path": "reports/platform-report.md", "title": "Platform report", "kind": "platform", "date": "", "github": ""}
        rows = build_site.report_index(platform)
        self.assertEqual(rows[0]["kind"], "platform")
        paths = {r["path"] for r in rows}
        for md in (ROOT / "reports").rglob("*.md"):
            if md.parent.name == "reports" and md.name == "README.md":
                continue
            self.assertIn(md.relative_to(ROOT).as_posix(), paths)
        kinds = [r["kind"] for r in rows]
        self.assertEqual(kinds[-kinds.count("template"):], ["template"] * kinds.count("template"))

    def test_every_new_tab_has_a_panel_and_a_label(self):
        html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        en = json.loads((ROOT / "site" / "i18n" / "en.json").read_text(encoding="utf-8"))
        for tab in re.findall(r'data-tab="([\w-]+)"', html):
            self.assertIn(f'<section id="{tab}"', html, tab)
            self.assertIn(f"tab.{tab}", en, tab)

    def test_site_build_publishes_reports_and_rule_files(self):
        with tempfile.TemporaryDirectory() as d:
            build_site.build(Path(d) / "site")
            index = json.loads((Path(d) / "site" / "reports.json").read_text(encoding="utf-8"))
            for row in index["reports"]:
                self.assertTrue((Path(d) / "site" / row["path"]).is_file(), row["path"])
            for det, files in index["rule_files"].items():
                self.assertTrue(det.startswith("DET-AI-"))
                for f in files:
                    self.assertTrue((ROOT / f).is_file(), f)


if __name__ == "__main__":
    unittest.main()
