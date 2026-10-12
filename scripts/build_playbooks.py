#!/usr/bin/env python3
"""Generate one defender playbook per technique, from the datasets (stdlib only).

The datasets say what a technique is, what was observed, which safe tests, detections and controls exist and how mature each
one is. A playbook puts those facts in the order a defender works: understand it, test it, detect it, prevent it, close the
loop, and know the limits of what the repository has. It is generated, so it cannot drift from the data and it states plainly
where the repository is thin.

It does not invent procedure. Anything that needs hands-on judgement lives in a hand-written note under
docs/playbooks/notes/<technique>.md, which the page includes verbatim, or in a worked example under examples/.

    python scripts/build_playbooks.py            # write docs/playbooks/
    python scripts/build_playbooks.py --check    # exit 1 if any page is stale
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import coverage_model  # noqa: E402
from common import ROOT, load_data  # noqa: E402
from run_safe_lab import PROFILE_MAP  # noqa: E402

OUT = ROOT / "docs" / "playbooks"
NOTES = OUT / "notes"
EXPLORER = "https://ridd1kulusc0d3r.github.io/LLmInjection/"
CROSSWALK = ROOT / "references" / "crosswalks" / "anthropic-cybersecurity-skills.json"
MATURITY_TEXT = {
    "observed-in-the-wild": "observed in the wild",
    "disclosed-vulnerability": "tied to a disclosed vulnerability",
    "research-demonstrated": "demonstrated in research",
    "no-linked-evidence": "no linked evidence yet",
}
# Worked examples: code in examples/ that makes some of a technique's test cases executable.
EXAMPLES = {
    "LLMI-T008": {"code": "examples/agent_tool_gate.py", "tests": "tests/test_agent_tool_gate.py",
                  "covers": ["TC-MCP-010", "TC-AG-005", "TC-PARAM-019", "TC-AUTHZ-029", "TC-TOOL-030", "TC-AG-006"]},
}


def cell(text: Any) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def md_link(label: str, target: str) -> str:
    return f"[{label}]({target})"


class Data:
    """Everything a page needs, loaded once."""

    def __init__(self) -> None:
        self.cov = {r["id"]: r for r in coverage_model.build()["techniques"]}
        self.techniques = {t["id"]: t for t in load_data("techniques")}
        self.tests = {t["id"]: t for t in load_data("test-cases")}
        self.controls = {c["id"]: c for c in load_data("controls")}
        self.detections = {d["id"]: d for d in load_data("detections")}
        self.records = {r["id"]: r for name in ("incidents", "campaigns", "vulnerabilities") for r in load_data(name)}
        self.actors = {a["id"]: a for a in load_data("actors")}
        self.eco = {e["id"]: e for e in load_data("ecosystem")}
        self.skills = json.loads(CROSSWALK.read_text(encoding="utf-8"))["skills"] if CROSSWALK.exists() else []
        self.rule_paths = self._rule_paths()

    @staticmethod
    def _rule_paths() -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for path in sorted((ROOT / "detections").glob("*/*")):
            if path.is_file() and path.name.lower().startswith("det-"):
                out.setdefault("-".join(path.name.split("-")[:3]).upper(), []).append(path.relative_to(ROOT).as_posix())
        return out


def profiles_for(test: dict[str, Any]) -> list[str]:
    return [p for p, cats in PROFILE_MAP.items() if cats and test["category"] in cats]


def next_step(row: dict[str, Any], data: Data) -> str:
    specs = [d for d in row["detections"] if d["implementation"] == "specification"]
    if not row["tests"]:
        return "Write a safe test case: a goal, a benign stimulus, the expected secure behaviour and the telemetry that proves it."
    if row["detections"] and not any(d["implementation"] == "rule-file" for d in row["detections"]):
        top = max(specs, key=lambda d: ["informational", "low", "medium", "high", "critical"].index(data.detections[d["id"]]["severity"]))
        return f"Turn {top['id']} ({top['name']}) from a specification into a rule file, starting with the telemetry listed in section 3."
    if not row["detections"]:
        return "Write a detection hypothesis with the telemetry it needs, then a rule file if the telemetry exists."
    if not row["controls"]:
        return "Define a control that prevents or contains this technique and say which test validates it."
    if not row["benchmarks"]:
        return "No public benchmark maps to this technique. Check the ecosystem for one, or measure it with your own regression tests."
    return "All layers exist. Re-verify after any change to the model, prompt, tools or policy."


def limits(row: dict[str, Any]) -> list[str]:
    out = []
    if not row["evidence"]:
        out.append("No incident, campaign or vulnerability in this repository is linked to this technique. That is a gap here, not proof that it has not happened.")
    elif row["maturity"] != "observed-in-the-wild":
        out.append(f"The evidence is {MATURITY_TEXT[row['maturity']]}. Do not read it as activity seen against real organisations.")
    if len(row["publishers"]) == 1:
        out.append(f"All the evidence comes from one publisher ({row['publishers'][0]}). Treat it as one voice until a second source confirms it.")
    if row["stale"]:
        out.append(f"The newest evidence ({row['newest_evidence']}) is more than {coverage_model.STALE_DAYS} days older than the newest in the dataset.")
    specs = [d for d in row["detections"] if d["implementation"] == "specification"]
    if specs:
        out.append(f"{len(specs)} of {len(row['detections'])} detection(s) are specifications, not rules. They say what to look for, not how to query it. Nothing here has been run against real telemetry.")
    if not row["controls"]:
        out.append("No control is linked to this technique yet.")
    if not row["benchmarks"]:
        out.append("No benchmark maps to it, so there is no public yardstick for how well a defence performs.")
    out.append("The tests use benign markers and synthetic data. A pass in a lab is not a security rating for a production system.")
    out.append("Ecosystem tools and benchmarks help you test and measure. They never support a claim that an actor used the technique.")
    return out


def page(tid: str, data: Data) -> str:
    t, row = data.techniques[tid], data.cov[tid]
    layers_rules = sum(1 for d in row["detections"] if d["implementation"] == "rule-file")
    lines = [
        f"# {tid}: {t['name']}", "",
        "> Generated from the datasets by `scripts/build_playbooks.py`; do not edit by hand. Change the data, or add hand-written notes in `docs/playbooks/notes/`. "
        "It says what the repository knows and where it stops. Use it only on systems you are authorised to test.", "",
        "| | |", "|---|---|",
        f"| Category | {cell(t['category'])} |",
        f"| Maturity | **{MATURITY_TEXT[row['maturity']]}** |",
        f"| Priority | {row['priority']:g} of {coverage_model.MATURITY_WEIGHT['observed-in-the-wild'] * 4} (see [how it is scored](../../docs/INTELLIGENCE-CHANGELOG.md)) |".replace("(see [how it is scored](../../docs/INTELLIGENCE-CHANGELOG.md))", "(maturity weight times the layers still missing)"),
        "| Frameworks | " + (", ".join(f"[{cell(m['id'])}]({m['url']}) {cell(m['framework'].replace('MITRE ', ''))} ({m['relation']})" for m in t["external_mappings"][:6]) or "none mapped") + " |",
        "", "## Where it stands", "",
        "| Layer | Status |", "|---|---|",
        f"| Evidence | {len(row['evidence'])} record(s), {len(row['publishers'])} publisher(s), best grade {row['best_grade'] or 'n/a'}, newest {row['newest_evidence'] or 'undated'} |",
        f"| Safe tests | {len(row['tests'])} |",
        f"| Detections | {layers_rules} rule file(s), {len(row['detections']) - layers_rules} specification(s) |",
        f"| Controls | {len(row['controls'])} |",
        f"| Benchmarks | {len(row['benchmarks'])} |", "",
        f"**Next step:** {next_step(row, data)}", "",
        "## 1. Understand it", "", t["summary"], "",
    ]
    if row["evidence"]:
        lines += ["What the repository links to it:", ""]
        for rid in row["evidence"]:
            rec = data.records.get(rid, {})
            kind = rec.get("kind") or rid.split("-")[0].lower()
            lines.append(f"- {coverage_model.record_date(rec) or 'undated'} · {md_link(cell(rec.get('name', rid)), EXPLORER + '#node=' + rid)} ({kind}, {rec.get('confidence', 'unrated')})")
        lines.append("")
    if row["actors"]:
        lines += ["Actors whose campaigns use it: " + ", ".join(cell(data.actors[a]["name"]) for a in row["actors"] if a in data.actors) + ". Vendor labels are kept as published and never merged without evidence.", ""]

    lines += ["## 2. Test it safely", ""]
    if row["tests"]:
        lines += ["Run these in a lab you own. Each is a specification: a goal, a benign stimulus, the expected secure behaviour and the telemetry that proves it.", ""]
        for tc_id in row["tests"]:
            tc = data.tests[tc_id]
            lines += [f"### {tc_id} · {tc['name']}", "", f"- **Goal:** {tc['goal']}", f"- **Stimulus:** {tc['stimulus']}", f"- **Expected:** {tc['expected']}",
                      f"- **Telemetry to capture:** {', '.join(f'`{x}`' for x in tc['telemetry'])}",
                      f"- **Controls it exercises:** {', '.join(tc['controls'])}", ""]
        profiles = sorted({p for tc_id in row["tests"] for p in profiles_for(data.tests[tc_id])})
        lines += ["```bash", f"python scripts/query_intel.py coverage {tid}"] + [f"python scripts/run_safe_lab.py --profile {p}   # lists the cases for this surface; plan mode makes no model calls" for p in profiles] + ["```", "",
                  "The runner has plan and mock adapters only: it does not call your system. To run a case, build its stimulus in your own harness (section 7 points at tools that do) and record the outcome in the shape of [`schemas/lab-result.schema.json`](../../schemas/lab-result.schema.json).", ""]
        ex = EXAMPLES.get(tid)
        if ex:
            lines += [f"**Worked example.** [`{ex['code']}`](../../{ex['code']}) is a small tool-invocation gate and [`{ex['tests']}`](../../{ex['tests']}) turns {', '.join(f'`{c}`' for c in ex['covers'])} into assertions you can run with `python -m unittest`.", ""]
    else:
        lines += ["No safe test is linked to this technique yet.", ""]

    lines += ["## 3. Detect it", ""]
    if row["detections"]:
        for d in row["detections"]:
            rec = data.detections[d["id"]]
            lines += [f"### {d['id']} · {d['name']}", "", f"- **Severity:** {rec['severity']}", f"- **Hypothesis:** {rec['hypothesis']}", f"- **Telemetry:** {', '.join(f'`{x}`' for x in rec['telemetry'])}"]
            if d["implementation"] == "rule-file":
                lines.append("- **Implementation:** rule file(s): " + ", ".join(md_link(p.split("/")[1], "../../" + p) for p in data.rule_paths.get(d["id"], [])) + ". Experimental and not run against real telemetry.")
            else:
                lines.append("- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.")
            lines.append("")
    else:
        lines += ["No detection is linked yet.", ""]

    lines += ["## 4. Prevent it", ""]
    if row["controls"]:
        for cid in row["controls"]:
            c = data.controls[cid]
            lines.append(f"- **{cell(c['name'])}** (`{cid}`): {c['description']}")
        lines.append("")
    else:
        lines += ["No control is linked yet.", ""]

    lines += ["## 5. Close the loop", "",
              "- [ ] Run each test in section 2 against your system and keep the outcome with the model, prompt and tool versions.",
              "- [ ] For every failed case, confirm which control in section 4 should have stopped it, and whether it is deployed.",
              "- [ ] Confirm the telemetry named in the tests and detections actually exists in your logs. A detection without its telemetry is silent, not safe.",
              "- [ ] After the fix, re-run the failed cases and confirm the detection fires on the attempt.",
              "- [ ] Re-run all of it after any change to the model, system prompt, tools, retrieval sources or policy.", "",
              "## 6. Limits of this page", ""] + [f"- {x}" for x in limits(row)] + [""]

    note = NOTES / f"{tid}.md"
    if note.exists():
        lines += ["## Practitioner notes", "", note.read_text(encoding="utf-8").strip(), ""]

    lines += ["## 7. Go deeper (links only)", ""]
    tools = [data.eco[e] for e in row["tools"] if e in data.eco]
    bench = [e for e in tools if e["id"] in row["benchmarks"]]
    others = [e for e in tools if e["id"] not in row["benchmarks"]]
    if bench:
        lines.append("- **Benchmarks:** " + ", ".join(md_link(f"{e['owner']}/{e['name']}", e["url"]) for e in bench))
    if others:
        shown = others[:8]
        extra = f", and {len(others) - len(shown)} more in the [Explorer]({EXPLORER}#tab=ecosystem)" if len(others) > len(shown) else ""
        lines.append("- **Tools and projects:** " + ", ".join(md_link(f"{e['owner']}/{e['name']}", e["url"]) for e in shown) + extra)
    skills = [s for s in data.skills if tid in s["llminjection_techniques"]]
    if skills:
        lines.append("- **Third-party procedures (not ours, link only):** " + "; ".join(f"{md_link(s['name'], s['url'])} ({s['role']}: {s['note']})" for s in skills) + ". Independent community project, Apache-2.0, not affiliated with Anthropic; see the [knowledge strategy](../KNOWLEDGE-STRATEGY.md).")
    lines += [f"- **Live record:** {md_link('this technique in the Explorer', EXPLORER + '#node=' + tid)}", ""]
    return "\n".join(lines)


def index(data: Data) -> str:
    rows = sorted(data.cov.values(), key=lambda r: (-r["priority"], r["id"]))
    lines = [
        "# Defender playbooks", "",
        "One page per technique, generated from the datasets, in the order a defender works: understand it, test it, detect it, prevent it, close the loop, know the limits. "
        "Each page says what exists and what does not, and ends with where to go for the hands-on detail. Read the [knowledge strategy](../KNOWLEDGE-STRATEGY.md) for how this fits with the rest of the repository.", "",
        "Sorted by priority, the techniques with the most missing defence first. `E` evidence records, `T` safe tests, `R` rule files, `S` specifications, `C` controls, `B` benchmarks.", "",
        "| Technique | Maturity | Priority | E | T | R | S | C | B |", "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        rules = sum(1 for d in r["detections"] if d["implementation"] == "rule-file")
        lines.append(f"| [{r['id']}]({r['id']}.md) {cell(r['name'])} | {MATURITY_TEXT[r['maturity']]} | {r['priority']:g} | {len(r['evidence'])} | {len(r['tests'])} | {rules} | {len(r['detections']) - rules} | {len(r['controls'])} | {len(r['benchmarks'])} |")
    lines += ["", "Pages with a worked example or hand-written notes: " + (", ".join(f"[{t}]({t}.md)" for t in sorted(set(EXAMPLES) | {p.stem for p in NOTES.glob('*.md')})) or "none yet") + ".", ""]
    return "\n".join(lines)


def build_all() -> dict[str, str]:
    data = Data()
    pages = {f"{tid}.md": page(tid, data) for tid in data.techniques}
    pages["README.md"] = index(data)
    return pages


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    pages = build_all()
    OUT.mkdir(parents=True, exist_ok=True)
    stale = [name for name, text in pages.items() if not (OUT / name).exists() or (OUT / name).read_text(encoding="utf-8") != text]
    extra = sorted(p.name for p in OUT.glob("*.md") if p.name not in pages)
    if args.check:
        if stale or extra:
            print(f"stale playbooks: {stale + extra}")
            return 1
        print(f"{len(pages)} playbook pages are current")
        return 0
    for name, text in pages.items():
        (OUT / name).write_text(text, encoding="utf-8")
    for name in extra:
        (OUT / name).unlink()
    print(f"wrote {len(pages)} pages to {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
