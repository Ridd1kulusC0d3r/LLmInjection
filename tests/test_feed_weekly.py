import datetime as dt
import json
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_feed  # noqa: E402
import build_weekly  # noqa: E402

ATOM = "{http://www.w3.org/2005/Atom}"


class FeedTests(unittest.TestCase):
    def test_atom_and_json_feeds_are_valid_and_list_reports(self):
        reports = [{"path": "reports/trends/2026-W47.md", "title": "Tendências da semana · 2026-W47", "kind": "trends", "date": "2026-11-20",
                    "page": "relatorios/2026-W47.html"},
                   {"path": "reports/templates/dossie.md", "title": "x", "kind": "template", "date": ""}]
        with tempfile.TemporaryDirectory() as d:
            n = build_feed.build(Path(d), reports)
            root = ET.parse(Path(d) / "feed.xml").getroot()
            jf = json.loads((Path(d) / "feed.json").read_text(encoding="utf-8"))
        titles = [e.find(ATOM + "title").text for e in root.findall(ATOM + "entry")]
        self.assertEqual(len(titles), n)
        self.assertIn("Tendências da semana · 2026-W47", titles)
        self.assertFalse(any(t.endswith(": x") for t in titles), "templates stay out of the feed")
        self.assertEqual(jf["version"], "https://jsonfeed.org/version/1.1")
        self.assertEqual(len(jf["items"]), n)


class WeeklyTests(unittest.TestCase):
    def test_draft_counts_signals_and_marks_the_analytic_parts(self):
        path, text = build_weekly.draft(dt.date(2026, 11, 20))
        self.assertEqual(path.name, "2026-W47.md")
        self.assertIn("## Sinais", text)
        self.assertIn("CVE-2026-40217", text)
        self.assertIn(build_weekly.TODO, text)

    def test_expanded_digest_does_not_double_count_daily_items(self):
        # 2026-11-21.json and 2026-11-21-ampliado.json share items 23-27; each must appear once.
        _, text = build_weekly.draft(dt.date(2026, 11, 21))
        for n in range(23, 36):
            self.assertEqual(text.count(f"`LLMI-20261121-{n}`"), 1, n)

    def test_published_editions_have_no_unfilled_sections(self):
        for p in (ROOT / "reports" / "trends").glob("*.md"):
            self.assertNotIn("A PREENCHER", p.read_text(encoding="utf-8"), p.name)
