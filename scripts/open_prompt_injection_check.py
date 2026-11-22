#!/usr/bin/env python3
"""Map Open-Prompt-Injection's attacks, defences and metrics onto LLMInjection (stdlib only).

liu00222/Open-Prompt-Injection (MIT) is the reference toolkit behind three peer-reviewed papers: the USENIX
Security 2024 benchmark of prompt injection attacks and defences, DataSentinel (IEEE S&P 2025) and PromptLocate
(IEEE S&P 2026). This script reads the repository as text, inventories its attack strategies, defences, detectors,
models, tasks and metrics, and maps each defence onto an LLMInjection control with its class (prevention,
detection, response filtering) and the evidence the benchmark gives for it. It also records what a team must
know before running the toolkit (API keys in config files, checkpoints on Google Drive, remote code in one
model loader). Code and prompts are linked, not copied.

    git clone --depth 1 https://github.com/liu00222/Open-Prompt-Injection.git /tmp/opi
    python scripts/open_prompt_injection_check.py --repo /tmp/opi            # report
    python scripts/open_prompt_injection_check.py --repo /tmp/opi --write    # references/crosswalks/open-prompt-injection.json

The repository is untrusted input: files are read as text, nothing in it is imported or executed.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "references" / "crosswalks" / "open-prompt-injection.json"
DOC = ROOT / "docs" / "OPEN-PROMPT-INJECTION.md"
REPO = "https://github.com/liu00222/Open-Prompt-Injection"
BLOB = REPO + "/blob/main/"

PAPERS = [
    {"key": "liu2024promptinjection", "title": "Formalizing and Benchmarking Prompt Injection Attacks and Defenses", "venue": "USENIX Security 2024"},
    {"key": "liu2025datasentinel", "title": "DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks", "venue": "IEEE S&P 2025"},
    {"key": "jia2026promptlocate", "title": "PromptLocate: Localizing Prompt Injection Attacks", "venue": "IEEE S&P 2026"},
]

# Attack strategy -> what it does (paraphrased) and LLMInjection techniques. The benchmark's attacker controls the
# data prompt of an LLM-integrated application, so every strategy is indirect injection first. Analyst mapping.
ATTACKS = {
    "naive": ("Appends the injected instruction and data to the target data.", ["LLMI-T002", "LLMI-T001"]),
    "escape": ("Adds escape characters (such as a newline) so the injected instruction reads as a new segment.", ["LLMI-T002", "LLMI-T001"]),
    "ignore": ("Adds a context-ignoring sentence that tells the model to disregard previous instructions.", ["LLMI-T002", "LLMI-T001"]),
    "fake_comp": ("Adds a fake response so the model treats the target task as already completed.", ["LLMI-T002", "LLMI-T001"]),
    "combine": ("Combines escape characters, a fake completion and a context-ignoring sentence; the strongest strategy in the paper.", ["LLMI-T002", "LLMI-T001"]),
}

# Defence -> (class, how it works, LLMInjection controls). Every one sits inside the model's own channel, so all are
# in-band and probabilistic: none removes the model's ability to act on an instruction it should not follow.
DEFENCES = {
    "instructional": ("prevention", "Warns the model in the instruction that the data may try to change it.", ["CTRL-INSTRUCTION-DATA-SEPARATION"]),
    "sandwich": ("prevention", "Repeats the task after the data.", ["CTRL-INSTRUCTION-DATA-SEPARATION"]),
    "random_seq": ("prevention", "Encloses the data between random strings.", ["CTRL-INPUT-TRANSFORM", "CTRL-INSTRUCTION-DATA-SEPARATION"]),
    "delimiters": ("prevention", "Encloses the data in delimiters.", ["CTRL-INPUT-TRANSFORM", "CTRL-INSTRUCTION-DATA-SEPARATION"]),
    "xml": ("prevention", "Encloses the data in XML tags.", ["CTRL-INPUT-TRANSFORM", "CTRL-INSTRUCTION-DATA-SEPARATION"]),
    "paraphrasing": ("prevention", "Has the model paraphrase the data before the task runs.", ["CTRL-INPUT-TRANSFORM"]),
    "retokenization": ("prevention", "Retokenizes the data with BPE dropout to break crafted sequences.", ["CTRL-INPUT-TRANSFORM"]),
    "response-based": ("response filtering", "Drops answers that do not fit the target task's label set.", ["CTRL-STRUCTURED-OUTPUT", "CTRL-OUTPUT-SANITIZATION"]),
    "ppl": ("detection", "Flags data whose perplexity under a surrogate model passes a threshold.", ["CTRL-IO-GUARDRAIL"]),
    "llm-based": ("detection", "Asks a model whether the data contains instructions.", ["CTRL-IO-GUARDRAIL"]),
    "known-answer": ("detection", "Asks the model to repeat a known secret while ignoring the data; a different answer flags injection.", ["CTRL-IO-GUARDRAIL", "CTRL-CONTEXT-CANARY"]),
}
DETECTORS = {
    "DataSentinel": ("detection", "Fine-tuned known-answer detector trained against adaptive attacks (game-theoretic).", ["CTRL-IO-GUARDRAIL", "CTRL-CONTEXT-CANARY"], "OpenPromptInjection/apps/DataSentinelDetector.py"),
    "PromptLocate": ("localisation and recovery", "Finds the injected segment inside contaminated data and recovers the clean data.", ["CTRL-IO-GUARDRAIL", "CTRL-INPUT-TRANSFORM"], "OpenPromptInjection/apps/PromptLocate.py"),
}
METRICS = {
    "PNA": "Performance under no attack: how well the model does the task (target or injected) on clean data.",
    "ASV": "Attack success value: how well the model does the injected task when the attack is applied.",
    "MR": "Matching rate: how often answers under attack match the answers to the injected task alone.",
}
LAB_MAPPING = {
    "test_case": "TC-PI-002 (indirect, data prompt) or TC-PI-001 (direct)",
    "adapter": "open-prompt-injection@<commit>",
    "result": "ASV and MR under attack, PNA without attack, per attack strategy and defence",
    "context": "model and its config, target task, injected task, number of samples, defence specification",
    "caveat": "A low ASV against a fixed strategy is not robustness: adaptive attacks are outside this matrix.",
}
LIMITS = [
    "The applications are single-turn text tasks (sentiment, spam, grammar, summarisation and others). There are no tools, agents, retrieval or memory, so results do not carry over to agent systems.",
    "Attack strategies are fixed templates. They measure baseline exposure, not robustness against an adaptive attacker.",
    "Every defence in the toolkit is in-band: it changes the prompt, the data or the answer, or asks a model to judge. None limits what a hijacked model can do; out-of-band controls (CTRL-POLICY-OUTSIDE-MODEL, CTRL-PRIVILEGE-SEPARATED-LLM, CTRL-DATAFLOW-TAINT) are outside its scope.",
]


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def build(repo: Path) -> dict:
    attackers = _read(repo / "OpenPromptInjection" / "attackers" / "__init__.py")
    defences = _read(repo / "OpenPromptInjection" / "apps" / "defenses.py")
    found_attacks = re.findall(r"attack_strategy == '([^']+)'", attackers)
    found_defences = re.findall(r"^\s+name = '([^']+)'", defences, re.M)
    if "ppl-" in defences:
        found_defences.append("ppl")
    found_defences = [d for d in dict.fromkeys(found_defences) if d != "no"]
    models = sorted(p.name.removesuffix("_config.json") for p in (repo / "configs" / "model_configs").glob("*_config.json"))
    tasks = sorted(p.name.removesuffix("_config.json") for p in (repo / "configs" / "task_configs").glob("*_config.json"))
    code = "\n".join(_read(p) for p in (repo / "OpenPromptInjection").rglob("*.py"))
    readme = _read(repo / "README.md")
    try:
        commit = subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%h %cs"], capture_output=True, text=True, check=True).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        commit = ["unknown", "unknown"]
    risks = []
    if "api_key_info" in code:
        risks.append("API keys are read from JSON files under configs/model_configs: keep real keys out of the clone and out of version control.")
    if "drive.google.com" in readme:
        risks.append("DataSentinel and PromptLocate checkpoints are downloaded from Google Drive links with no published hash or signature: treat them as unverified model artifacts (CTRL-ARTIFACT-PINNING, CTRL-SIGNATURE-VERIFICATION).")
    if "trust_remote_code=True" in code:
        risks.append("One model loader passes trust_remote_code=True to Hugging Face, which runs code shipped with that model: pin the revision or skip that model.")
    if "environment.yml" in {p.name for p in repo.iterdir()}:
        risks.append("The conda environment pins Python 3.9 and 2024-era libraries: run it in an isolated environment, not next to production tooling.")
    unknown_attacks = sorted(set(found_attacks) - set(ATTACKS))
    unknown_defences = sorted(set(found_defences) - set(DEFENCES))
    return {
        "meta": {"source": REPO, "commit": commit[0], "commit_date": commit[1] if len(commit) > 1 else "",
                 "read": datetime.now(UTC).date().isoformat(), "licence": "MIT", "papers": PAPERS,
                 "policy": "code and prompts are linked, not copied; the toolkit was read as text and not executed",
                 "mapping": "attack to technique and defence to control is an analyst mapping (scripts/open_prompt_injection_check.py)"},
        "summary": {"attacks": len(found_attacks), "defences": len(found_defences), "detectors": len(DETECTORS),
                    "models": len(models), "tasks": len(tasks), "unmapped_attacks": unknown_attacks, "unmapped_defences": unknown_defences},
        "attacks": [{"name": a, "description": ATTACKS.get(a, ("", []))[0], "techniques": ATTACKS.get(a, ("", []))[1],
                     "source": BLOB + "OpenPromptInjection/attackers/__init__.py"} for a in found_attacks],
        "defences": [{"name": d, "class": DEFENCES.get(d, ("", "", []))[0], "layer": "in-band (probabilistic)",
                      "description": DEFENCES.get(d, ("", "", []))[1], "controls": DEFENCES.get(d, ("", "", []))[2],
                      "source": BLOB + "OpenPromptInjection/apps/defenses.py"} for d in found_defences],
        "detectors": [{"name": k, "class": v[0], "layer": "in-band (probabilistic)", "description": v[1], "controls": v[2], "source": BLOB + v[3]} for k, v in DETECTORS.items()],
        "metrics": METRICS,
        "models": models,
        "tasks": tasks,
        "lab_mapping": LAB_MAPPING,
        "limits": LIMITS,
        "before_running": risks,
    }


def markdown(data: dict) -> str:
    m, s = data["meta"], data["summary"]
    L = ["# Open-Prompt-Injection in LLMInjection", "",
         f"Generated by `scripts/open_prompt_injection_check.py` from [{m['source'].removeprefix('https://github.com/')}]({m['source']}) "
         f"at commit `{m['commit']}` ({m['commit_date']}), read on {m['read']}. Licence: {m['licence']}. {m['policy'].capitalize()}.", "",
         "The toolkit backs three peer-reviewed papers: " + "; ".join(f"*{p['title']}* ({p['venue']})" for p in m["papers"]) + ".", "",
         "## What LLMInjection takes from it", "",
         f"- **{s['attacks']} attack strategies**, mapped to `LLMI-T002` (the attacker controls the application's data) and `LLMI-T001`.",
         f"- **{s['defences']} defences and {s['detectors']} detectors**, each mapped to an LLMInjection control and classed as prevention, detection or response filtering. All of them are in-band.",
         "- **Three metrics** (PNA, ASV, MR) as the vocabulary for lab results on `TC-PI-001` and `TC-PI-002`.",
         f"- **{s['models']} model configurations and {s['tasks']} tasks** as the reproducible matrix a team can run.", "",
         "## Attack strategies", "", "| Strategy | What it does | Techniques |", "|---|---|---|"]
    L += [f"| `{a['name']}` | {a['description']} | {', '.join(f'`{t}`' for t in a['techniques'])} |" for a in data["attacks"]]
    L += ["", "## Defences and detectors", "", "| Defence | Class | How it works | Controls |", "|---|---|---|---|"]
    L += [f"| `{d['name']}` | {d['class']} | {d['description']} | {', '.join(f'`{c}`' for c in d['controls'])} |" for d in data["defences"] + data["detectors"]]
    L += ["", "## Metrics", "", "| Metric | Meaning |", "|---|---|"] + [f"| {k} | {v} |" for k, v in data["metrics"].items()]
    L += ["", "## Recording a run as an LLMInjection lab result", ""] + [f"- **{k}:** {v}" for k, v in data["lab_mapping"].items()]
    L += ["", "## Limits", ""] + [f"- {x}" for x in data["limits"]]
    L += ["", "## Before running it", ""] + [f"- {x}" for x in data["before_running"]] + [""]
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    data = build(a.repo)
    print(json.dumps(data["summary"], ensure_ascii=False))
    if a.write:
        OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        DOC.write_text(markdown(data), encoding="utf-8")
        print(f"wrote {OUT.relative_to(ROOT)} and {DOC.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
