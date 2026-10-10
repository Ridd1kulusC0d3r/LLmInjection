import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = [p for p in ROOT.rglob("*.md") if not {".git", "node_modules", "dist", "_site"} & set(p.parts)]


def prose(path):
    """Markdown with code spans and fences removed, so text that merely mentions a tag is not counted as markup."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


class PagesRenderTests(unittest.TestCase):
    """GitHub Pages renders the README with kramdown, which is stricter than GitHub's own renderer."""

    def test_config_parses_markdown_inside_details(self):
        config = (ROOT / "_config.yml").read_text(encoding="utf-8")
        self.assertRegex(config, r"parse_block_html:\s*true")
        self.assertTrue((ROOT / "_layouts" / "default.html").exists())
        self.assertTrue((ROOT / "assets" / "css" / "style.scss").exists())

    def test_every_summary_is_span_parsed(self):
        # a one-line <summary>...</summary> otherwise swallows the closing tag and nests every <details> inside the last
        for path in MARKDOWN:
            text = prose(path)
            for match in re.finditer(r"<summary(?![^>]*markdown=)[^>]*>", text):
                self.fail(f"{path.relative_to(ROOT)}: <summary> without markdown=\"span\" at offset {match.start()}")

    def test_generated_blocks_are_separated_from_their_markers(self):
        # a table glued to an HTML comment is rendered by kramdown as paragraph text
        for path in MARKDOWN:
            text = path.read_text(encoding="utf-8")
            for match in re.finditer(r"<!-- gen:[\w-]+:start -->\n(?!\n)", text):
                self.fail(f"{path.relative_to(ROOT)}: no blank line after {match.group(0).strip()}")
            for _ in re.finditer(r"(?<!\n)\n<!-- gen:[\w-]+:end -->", text):
                self.fail(f"{path.relative_to(ROOT)}: no blank line before an end marker")

    def test_details_are_balanced(self):
        for path in MARKDOWN:
            text = prose(path)
            self.assertEqual(len(re.findall(r"<details\b", text)), len(re.findall(r"</details>", text)), path.name)


if __name__ == "__main__":
    unittest.main()
