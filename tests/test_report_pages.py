import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_report_pages  # noqa: E402


class ReportPageTests(unittest.TestCase):
    def test_every_analyst_report_gets_a_page_with_toc_and_ascii_anchors(self):
        with tempfile.TemporaryDirectory() as d:
            made = build_report_pages.build(Path(d))
            self.assertGreaterEqual(len(made), 2)
            for row in made:
                html = (Path(d) / Path(row["page"]).name).read_text(encoding="utf-8")
                self.assertIn('nav class="toc"', html)
                self.assertIn("TLP:", html)
                for anchor in re.findall(r'<h[23] id="([^"]+)"', html):
                    self.assertRegex(anchor, r"^s-[a-z0-9-]+$")

    def test_held_cves_link_to_the_explorer_and_kev_is_marked(self):
        with tempfile.TemporaryDirectory() as d:
            build_report_pages.build(Path(d))
            html = (Path(d) / "2026-11-20-vulnerabilidades-e-incidentes-ia.html").read_text(encoding="utf-8")
        self.assertIn('class="cve kev" href="../#node=VULN-LITELLM-CVE-2026-42208"', html)
        self.assertIn('<figure class="chart">', html)
        self.assertNotIn("<script>alert", html)

    def test_markdown_subset(self):
        link = build_report_pages.Linker([])
        out, toc = build_report_pages.render("## 1. Um\n\ntexto **forte** e `x<y`\n\n| a | Conf. |\n| --- | --- |\n| [l](https://e.x) | A |\n", link)
        self.assertIn('<h2 id="s-1-um">', out)
        self.assertIn("<code>x&lt;y</code>", out)
        self.assertIn('<span class="wgrade g-A">A</span>', out)
        self.assertEqual(toc[0][1], "s-1-um")

