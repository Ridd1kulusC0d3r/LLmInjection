import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import skills_catalog_check as sc  # noqa: E402
from common import load_data  # noqa: E402

SKILL = """---
name: red-teaming-llms-with-garak
version: '1.0'
license: Apache-2.0
subdomain: ai-security
atlas_techniques:
- AML.T0051
- AML.T0099
---
# Body
"""


class SkillsCatalogTests(unittest.TestCase):
    def test_frontmatter_scalars_and_lists(self):
        fm = sc.frontmatter(SKILL)
        self.assertEqual(fm["subdomain"], "ai-security")
        self.assertEqual(fm["atlas_techniques"], ["AML.T0051", "AML.T0099"])

    def test_read_skills_and_build(self):
        with tempfile.TemporaryDirectory() as d:
            for name, text in (("red-teaming-llms-with-garak", SKILL), ("analyzing-dns-logs", SKILL.replace("ai-security", "soc-operations").replace("garak", "dns"))):
                p = Path(d) / "skills" / name
                p.mkdir(parents=True)
                (p / "SKILL.md").write_text(text, encoding="utf-8")
            skills = sc.read_skills(Path(d))
            report = sc.build(skills, {"AML.T0051": {"name": "x"}}, {"commit": "abc", "date": "2026-01-01"})
        self.assertEqual(report["tiers"]["ai-security"]["count"], 1)
        self.assertEqual(report["tiers"]["other-skills-with-atlas-tags"]["count"], 1)
        entry = next(e for e in report["skills"] if e["name"] == "red-teaming-llms-with-garak")
        self.assertEqual(entry["atlas_unknown"], ["AML.T0099"])
        self.assertIn("curated_skills_missing_from_catalogue", report["audit"])

    def test_offensive_pattern(self):
        self.assertTrue(sc.OFFENSIVE.match("exploiting-sql-injection"))
        self.assertFalse(sc.OFFENSIVE.match("detecting-indirect-prompt-injection"))

    def test_curated_mapping_uses_real_techniques_and_roles(self):
        ids = {t["id"] for t in load_data("techniques")}
        for name, cur in sc.CURATED.items():
            self.assertTrue(set(cur["techniques"]) <= ids, name)
            self.assertIn(cur["role"], {"test", "defend", "detect", "assess", "audit"})

    def test_committed_crosswalk_is_link_only(self):
        data = json.loads(sc.OUT.read_text(encoding="utf-8")) if hasattr(sc, "OUT") else {}
        self.assertEqual(len(data["skills"]), len(sc.CURATED))
        self.assertIn("not affiliated with Anthropic", data["note"])
        for s in data["skills"]:
            self.assertTrue(s["url"].startswith("https://github.com/mukul975/anthropic-cybersecurity-skills/"))
            self.assertNotIn("body", s)


if __name__ == "__main__":
    unittest.main()
