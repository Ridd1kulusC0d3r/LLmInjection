import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CODES = ["en", "pt", "es", "zh", "ru"]
PH = re.compile(r"\{(\w+)\}")
CJK = "一-鿿"


def load(code):
    return json.loads((SITE / "i18n" / f"{code}.json").read_text(encoding="utf-8"))


def luminance(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4  # noqa: E731
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


class DictionaryTests(unittest.TestCase):
    def setUp(self):
        self.d = {c: load(c) for c in CODES}

    def test_same_keys_everywhere(self):
        base = set(self.d["en"])
        for code in CODES[1:]:
            self.assertEqual(sorted(base - set(self.d[code])), [], f"{code} is missing keys")
            self.assertEqual(sorted(set(self.d[code]) - base), [], f"{code} has extra keys")

    def test_placeholders_and_empty_values(self):
        for code in CODES:
            for key, value in self.d[code].items():
                self.assertTrue(value.strip(), f"{code}:{key} is empty")
                self.assertEqual(sorted(PH.findall(value)), sorted(PH.findall(self.d["en"][key])), f"{code}:{key} placeholders differ")

    def test_non_english_values_are_actually_translated(self):
        # allow identical text only for names, acronyms and numbers
        for code in CODES[1:]:
            same = [k for k, v in self.d[code].items() if v == self.d["en"][k]]
            for key in same:
                self.assertTrue(re.fullmatch(r"[A-Z0-9 .,\-/&{}a-z]*", self.d["en"][key]) and len(self.d["en"][key]) < 24, f"{code}:{key} looks untranslated: {self.d['en'][key]!r}")

    def test_chinese_uses_full_width_punctuation_next_to_han(self):
        for key, value in self.d["zh"].items():
            self.assertIsNone(re.search(rf"[{CJK}][,:;]|[,:;](?=[{CJK}])|[{CJK}]\(", value), f"zh:{key} has ASCII punctuation next to Han text: {value!r}")

    def test_keys_used_by_the_page_exist(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        js = (SITE / "app.js").read_text(encoding="utf-8")
        used = set(re.findall(r'data-i18n="([\w.-]+)"', html))
        for attr in re.findall(r'data-i18n-attr="([^"]+)"', html):
            used |= {pair.split(":")[1].strip() for pair in attr.split(";") if ":" in pair}
        used |= set(re.findall(r'\bt\("([\w.-]+)"', js))
        used |= set(re.findall(r'\bt\("([\w.-]+)"', (SITE / "i18n.js").read_text(encoding="utf-8")))
        static = {k for k in used if not k.endswith(".")}  # "stat." + name style keys are checked below
        self.assertEqual(sorted(k for k in static if k not in self.d["en"]), [], "keys used but not defined")

    def test_dynamic_label_groups_are_complete(self):
        en = self.d["en"]
        for prefix, values in {
            "conf.": ["confirmed", "high", "medium", "low", "unverified"],
            "mat.": ["observed-in-the-wild", "disclosed-vulnerability", "research-demonstrated", "no-linked-evidence"],
            "type.": ["actor", "campaign", "incident", "vulnerability", "technique", "test-case", "detection", "control", "framework", "model", "source"],
            "trend.": ["rising", "stable", "falling"],
            "confnote.": ["confirmed", "high", "medium", "low", "unverified"],
            "stat.": ["actors", "campaigns", "incidents", "vulnerabilities", "techniques", "sources"],
        }.items():
            for v in values:
                self.assertIn(prefix + v, en)
        eco = json.loads((ROOT / "data" / "ecosystem.json").read_text(encoding="utf-8"))
        for e in eco:
            self.assertIn("ecoclass." + e["evidence_class"], en, e["id"])
            self.assertIn("ecosec." + e["section"], en, e["id"])
        rels = {r["relationship"] for r in json.loads((ROOT / "data" / "relationships.json").read_text(encoding="utf-8"))}
        for r in rels:
            self.assertIn("rel." + r, en)


class ManifestTests(unittest.TestCase):
    def test_manifest_matches_languages_and_files(self):
        manifest = json.loads((SITE / "translations.json").read_text(encoding="utf-8"))
        listed = [m["code"] for m in manifest["languages"]]
        self.assertEqual(listed, CODES)
        js_codes = re.findall(r'\{code:"(\w+)"', (SITE / "i18n.js").read_text(encoding="utf-8"))
        self.assertEqual(js_codes, CODES)
        for m in manifest["languages"]:
            for key in ("readme", "regional"):
                if m[key]:
                    self.assertTrue((ROOT / m[key]).exists(), f"{m['code']} {key}: {m[key]} is missing")

    def test_every_readme_has_the_language_bar(self):
        for name in ("README.md", "README.pt-BR.md", "README.es.md", "README.zh-CN.md", "README.ru.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            bar = re.search(r"<!-- lang-bar -->\n(.*?)\n<!-- /lang-bar -->", text, re.S)
            self.assertIsNotNone(bar, name)
            for target in ("README.md", "README.pt-BR.md", "README.es.md", "README.zh-CN.md", "README.ru.md"):
                if target != name:  # the current language is shown in bold, without a link
                    self.assertIn(f"]({target})", bar.group(1), f"{name} bar lacks a link to {target}")
            self.assertEqual(bar.group(1).count("**"), 2, f"{name} bar should mark exactly the current language")

    def test_translated_readmes_state_that_they_are_machine_assisted(self):
        for name in ("README.pt-BR.md", "README.es.md", "README.zh-CN.md", "README.ru.md"):
            self.assertIn("TRANSLATIONS.md", (ROOT / name).read_text(encoding="utf-8"), name)


class ContrastTests(unittest.TestCase):
    """WCAG AA (4.5:1) for the text colours on the surfaces they sit on."""

    def tokens(self):
        css = (SITE / "style.css").read_text(encoding="utf-8")
        light = dict(re.findall(r"--([\w-]+):(#[0-9a-fA-F]{6})", re.search(r":root\{(.*?)\}", css, re.S).group(1)))
        dark = dict(re.findall(r"--([\w-]+):(#[0-9a-fA-F]{6})", re.search(r':root\[data-theme="dark"\]\{(.*?)\}', css, re.S).group(1)))
        return light, dark

    def test_text_tokens(self):
        for name, theme in zip(("light", "dark"), self.tokens(), strict=True):
            for text in ("ink", "ink-2", "ink-3", "signal"):
                for surface in ("paper", "paper-2"):
                    self.assertGreaterEqual(contrast(theme[text], theme[surface]), 4.5, f"{name}: {text} on {surface}")

    def test_heat_cells(self):
        light, dark = self.tokens()
        # (text, background) as set in style.css
        pairs_light = [(light["ink"], light["seq-1"]), (light["ink"], light["seq-2"]), ("#ffffff", light["seq-3"]), ("#ffffff", light["seq-4"])]
        pairs_dark = [("#ffffff", dark["seq-2"]), ("#131210", dark["seq-3"]), ("#131210", dark["seq-4"])]
        for text, bg in pairs_light + pairs_dark:
            self.assertGreaterEqual(contrast(text, bg), 4.5, f"{text} on {bg}")


if __name__ == "__main__":
    unittest.main()
