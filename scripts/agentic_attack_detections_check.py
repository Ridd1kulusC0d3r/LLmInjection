#!/usr/bin/env python3
"""Map ThreatDefence's agentic-attack-detections onto LLMInjection (stdlib only).

ThreatDefence/agentic-attack-detections (MIT) is what ThreatDefence/artex-detections became: the same repository,
renamed and widened from ARTEX to eight agentic offensive frameworks (ARTEX/AntiFox, Cairn, PentAGI, HexStrike,
CyberStrikeAI, Strix, Hermes Agent, Agent Zero) plus behaviours shared across them. This script reads it as text,
counts its rules per framework and format, assigns every rule file to a signal class and maps that class to an
LLMInjection detection, links each framework to a tool record, and lists the intrusion sets in its STIX bundle
next to the matching records in data/ (or none). Rules are linked, not copied; indicators are counted, not
imported. ARTEX files keep the finer behaviour map of scripts/artex_detections_check.py.

    git clone --depth 1 https://github.com/ThreatDefence/agentic-attack-detections.git /tmp/aad
    python scripts/agentic_attack_detections_check.py --repo /tmp/aad            # report
    python scripts/agentic_attack_detections_check.py --repo /tmp/aad --write    # references/crosswalks/agentic-attack-detections.json

The repository is untrusted input: files are read as text, nothing in it is executed.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from artex_detections_check import BEHAVIOURS, behaviour_of  # noqa: E402
from common import load_data  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "references" / "crosswalks" / "agentic-attack-detections.json"
DOC = ROOT / "docs" / "AGENTIC-ATTACK-DETECTIONS.md"
REPO = "https://github.com/ThreatDefence/agentic-attack-detections"
BLOB = REPO + "/blob/main/"

FRAMEWORKS = {  # folder -> (name, LLMInjection tool records)
    "artex": ("ARTEX and AntiFox", ["TOOL-ARTEX", "TOOL-ANTIFOX"]),
    "cairn": ("Cairn", ["TOOL-CAIRN"]),
    "pentagi": ("PentAGI", ["TOOL-PENTAGI"]),
    "hexstrike": ("HexStrike", ["TOOL-HEXSTRIKE-AI"]),
    "cyberstrikeai": ("CyberStrikeAI", ["TOOL-CYBERSTRIKEAI"]),
    "strix": ("Strix", ["TOOL-STRIX"]),
    "hermes": ("Hermes Agent", []),
    "agent-zero": ("Agent Zero", []),
}

# Signal class -> (keywords in the file name, LLMInjection detection or None, what it looks for). Checked in order;
# the first class with a matching keyword wins. Analyst mapping.
CLASSES = [
    ("Agent in auto-approve, jailbreak or attack mode", ["yolo", "godmode", "attack-mode", "attack-persona", "bypass", "auto-approve"], "DET-AI-032",
     "A coding or general agent runs without human approval, with a jailbreak persona, and drives attack tools."),
    ("Model API traffic from servers", ["model-api", "model_api"], "DET-AI-001",
     "Servers that should not talk to LLM providers do. Context, not proof: legitimate AI services look the same."),
    ("Cloud credentials used at machine speed", ["machine-speed"], "DET-AI-047",
     "A stolen cloud key tried across services faster than a person would."),
    ("Probes, callbacks and out-of-band lookups", ["out-of-band", "out_of_band", "callback", "page-reader", "page_reader", "rotating-prox", "fetched-twice", "webfetch"], "DET-AI-048",
     "Agent-driven probing: out-of-band test domains, a server calling back to the address that probed it, an agent page reader beside attack traffic, rotating proxies on one site."),
    ("Indicator sweeps", ["indicator", "watchlist", "-ip.rules", ".intel", "skimmer_hosts", "campaign-infrastructure", "campaign_skimmer"], None,
     "Reported addresses, domains and hashes. Counted, not imported; addresses expire 180 days after report."),
    ("Framework running on a host or console on the network", ["on-a-host", "on_host", "on-host", "server_or_mcp", "server-on-host", "console", "cli_or_sandbox", "command_wrapper",
                                                               "command-wrapper", "worker", "dispatcher", "container", "tunnel", "wired-to", "exposed", "update", "tool_api", "host_artifacts", "host-artifacts", "artifacts"], "DET-AI-052",
     "The framework itself: its server, workers, CLI, console API, update check or files on a host you own."),
    ("Framework fingerprints in traffic", ["user_agent", "user-agent", "probe", "xss", "telemetry", "viewer", "attack_files", ".rules", ".yar"], "DET-AI-048",
     "User agents, probe markers, telemetry and signatures that name the framework."),
    ("Post-exploitation seen with the framework", ["webshell", "uploader", "card-data", "persistence", "run_key", "launchagent", "beacon", "check-ins", "implant",
                                                   "host_escape", "carbonato", "kerbrute", "kerberos", "netexec", "config-backup", "config_backup", "wsus", "kali"], None,
     "Web shells, implants, persistence, container escape and AD enumeration. Classic detections; kept as links."),
]
# Intrusion sets whose names do not match a record here by name, matched by the analyst to the record of the same activity.
SET_MATCH = {"Gambit retail card-theft operator": ["INCIDENT-GAMBIT-AI-AGENT-RETAIL-SKIMMING"],
             "PaperCut exploitation operator": ["INCIDENT-PAPERCUT-AI-AGENT-EXPLOITATION"],
             "FortiGate mass-exploitation actor": ["INCIDENT-FORTIGATE-AI-AUGMENTED-ACCESS"]}
FORMAT = {"sentinel/hunting": "KQL hunts", "sentinel/analytics": "Sentinel analytics", "sigma": "Sigma", "suricata": "Suricata", "yara": "YARA",
          "zeek": "Zeek", "splunk": "Splunk", "elastic": "Elastic", "osquery": "osquery"}
SKIP = ("README.md", "coverage.md", "hunting-order.md", "source-code-signals.md", "app.conf", "default.meta", "macros.conf",
        "transforms.conf", "__load__.zeek", "main.zeek", "savedsearches.conf", ".csv", ".pcap", ".sh", ".py")


def _class_of(name: str) -> int | None:
    low = name.lower()
    for i, (_, keys, *_r) in enumerate(CLASSES):
        if any(k in low for k in keys):
            return i
    return None


def _fmt(rel: str) -> str | None:
    for k, v in FORMAT.items():
        if f"/{k}/" in f"/{rel}" or rel.split("/")[2:3] == [k.split("/")[0]] and "/" not in k:
            return v
    return None


def _files(repo: Path, base: str) -> list[Path]:
    root = repo / base
    return sorted(p for p in root.rglob("*") if p.is_file() and not p.name.endswith(SKIP) and "/tests/" not in p.as_posix()) if root.is_dir() else []


def build(repo: Path) -> dict:
    known = {d["id"] for d in load_data("detections")}
    tools = {t["id"] for t in load_data("tools")}
    records = {r["name"].lower(): r["id"] for n in ("actors", "campaigns", "incidents") for r in load_data(n)}
    classes = [{"class": c, "detection": d, "what": w, "rules": 0, "frameworks": Counter()} for c, _, d, w in CLASSES]
    fw_rows, unassigned = {}, []
    ioc_path = repo / "iocs" / "indicators.csv"
    iocs = list(csv.DictReader(ioc_path.open(encoding="utf-8"))) if ioc_path.is_file() else []
    for folder, (name, tool_ids) in FRAMEWORKS.items():
        counts, dets = Counter(), Counter()
        for p in _files(repo, f"frameworks/{folder}"):
            rel = p.relative_to(repo).as_posix()
            fmt = next((v for k, v in FORMAT.items() if rel.startswith(f"frameworks/{folder}/{k}/") or rel.startswith(f"frameworks/{folder}/{k}")), None)
            if fmt:
                counts[fmt] += 1
            if folder == "artex":
                b = behaviour_of(p.name)
                if b is not None:
                    if BEHAVIOURS[b][2]:
                        dets[BEHAVIOURS[b][2]] += 1
                    continue
            i = _class_of(p.name)
            if i is None:
                unassigned.append(rel)
                continue
            classes[i]["rules"] += 1
            classes[i]["frameworks"][name] += 1
            if CLASSES[i][2]:
                dets[CLASSES[i][2]] += 1
        n_ind = sum(1 for x in iocs if x.get("framework") == folder)
        fw_rows[folder] = {"framework": name, "folder": f"{BLOB}frameworks/{folder}", "tools": [t for t in tool_ids if t in tools],
                           "tool_record_missing": not any(t in tools for t in tool_ids), "formats": dict(sorted(counts.items())),
                           "indicators": n_ind, "detections": dict(sorted(dets.items()))}
    shared = []
    for p in _files(repo, "behaviors"):
        rel = p.relative_to(repo).as_posix()
        i = _class_of(p.name)
        if i is None:
            unassigned.append(rel)
            continue
        classes[i]["rules"] += 1
        classes[i]["frameworks"]["shared behaviours"] += 1
        shared.append({"path": rel, "class": CLASSES[i][0], "detection": CLASSES[i][2], "url": BLOB + rel})
    bundle = json.loads((repo / "feeds" / "stix2.1-bundle.json").read_text(encoding="utf-8"))
    sets = []
    for o in bundle.get("objects", []):
        if o.get("type") != "intrusion-set":
            continue
        low = o["name"].lower()
        match = [rid for rname, rid in records.items() if rname.split(" (")[0] in low or low.split(" (")[0] in rname]
        match += next((v for k, v in SET_MATCH.items() if o["name"].startswith(k)), [])
        sets.append({"name": o["name"], "llminjection": sorted(set(match))[:3], "status": "in the graph" if match else "candidate: read the cited report"})
    for c in classes:
        c["frameworks"] = dict(c["frameworks"])
    try:
        commit = subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%h %cs"], capture_output=True, text=True, check=True).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        commit = ["unknown", ""]
    return {
        "meta": {"source": REPO, "formerly": "https://github.com/ThreatDefence/artex-detections", "commit": commit[0], "commit_date": commit[1] if len(commit) > 1 else "",
                 "read": datetime.now(UTC).date().isoformat(), "licence": "MIT", "attribution": "ThreatDefence Pty Ltd and contributors, Agentic Attack Detections",
                 "policy": "rules are linked, not copied; indicators are counted, not imported; nothing in the repository was executed",
                 "maintainers_caveat": "No rule has been tested against a captured intrusion. Treat every rule as experimental until it has run on your own data.",
                 "mapping": "signal class to detection is an analyst mapping (scripts/agentic_attack_detections_check.py)"},
        "summary": {"frameworks": len(fw_rows), "rule_files": sum(sum(f["formats"].values()) for f in fw_rows.values()) + len(shared),
                    "shared_behaviour_files": len(shared), "indicators": sum(f["indicators"] for f in fw_rows.values()),
                    "tool_records_missing": [f["framework"] for f in fw_rows.values() if f["tool_record_missing"]],
                    "detections_used": sorted({d for f in fw_rows.values() for d in f["detections"]} | {s["detection"] for s in shared if s["detection"]}),
                    "unknown_detections": sorted({c["detection"] for c in classes if c["detection"] and c["detection"] not in known}),
                    "intrusion_sets": len(sets), "intrusion_sets_not_in_graph": sum(1 for s in sets if not s["llminjection"]),
                    "unassigned_files": unassigned},
        "frameworks": list(fw_rows.values()),
        "classes": classes,
        "shared_behaviours": shared,
        "intrusion_sets": sets,
    }


def markdown(d: dict) -> str:
    m, s = d["meta"], d["summary"]
    L = ["# Agentic attack detections in LLMInjection", "",
         f"Generated by `scripts/agentic_attack_detections_check.py` from [ThreatDefence/agentic-attack-detections]({m['source']}) "
         f"(formerly `artex-detections`), commit `{m['commit']}` ({m['commit_date']}), read on {m['read']}. Licence: {m['licence']}. "
         f"{m['policy'].capitalize()}.", "",
         f"> Maintainers: \"{m['maintainers_caveat']}\"", "",
         f"{s['frameworks']} frameworks, {s['rule_files']} rule files ({s['shared_behaviour_files']} of them shared behaviours) and "
         f"{s['indicators']} indicators. The ARTEX rules keep the finer map in [ARTEX-DETECTION-MAP.md](ARTEX-DETECTION-MAP.md).", "",
         "## Frameworks", "", "| Framework | Tool record | Rules by format | Indicators | LLMInjection detections |", "|---|---|---|---|---|"]
    for f in d["frameworks"]:
        fm = ", ".join(f"{k} {v}" for k, v in f["formats"].items())
        dets = ", ".join(f"`{k}` ({v})" for k, v in f["detections"].items()) or "–"
        tool = ", ".join(f"`{t}`" for t in f["tools"]) or "**missing**"
        L.append(f"| [{f['framework']}]({f['folder']}) | {tool} | {fm} | {f['indicators']} | {dets} |")
    L += ["", "## Signal classes", "", "| Class | Detection | What it looks for | Rules |", "|---|---|---|---|"]
    L += [f"| {c['class']} | {('`' + c['detection'] + '`') if c['detection'] else 'link only'} | {c['what']} | {c['rules']} |" for c in d["classes"]]
    L += ["", "## Shared behaviours", "", "| File | Class | Detection |", "|---|---|---|"]
    L += [f"| [{x['path'].split('/')[-1]}]({x['url']}) | {x['class']} | {('`' + x['detection'] + '`') if x['detection'] else 'link only'} |" for x in d["shared_behaviours"]]
    L += ["", "## Intrusion sets in the STIX bundle", "", "Names as ThreatDefence gives them. A match means a record with that name exists here; "
          "a candidate is a lead to read in the cited report before anything enters the graph.", "", "| Intrusion set | LLMInjection | Status |", "|---|---|---|"]
    L += [f"| {x['name']} | {', '.join(f'`{r}`' for r in x['llminjection']) or '–'} | {x['status']} |" for x in d["intrusion_sets"]]
    L += [""]
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    data = build(a.repo)
    print(json.dumps({k: v for k, v in data["summary"].items() if k != "unassigned_files"}, ensure_ascii=False))
    print("unassigned:", data["summary"]["unassigned_files"])
    if a.write:
        OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        DOC.write_text(markdown(data), encoding="utf-8")
        print(f"wrote {OUT.relative_to(ROOT)} and {DOC.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
