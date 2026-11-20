#!/usr/bin/env python3
"""Map ThreatDefence's ARTEX detection repository onto LLMInjection's detections and techniques (stdlib only).

ThreatDefence/artex-detections (MIT) ships Sigma rules and correlations, Sentinel hunts and analytics, a Splunk
app, Elastic rules, Zeek, Suricata, YARA, osquery and an indicator feed for ARTEX and its forks. Its
docs/coverage.md lists the behaviours it covers. This script inventories every rule file, assigns each one to a
behaviour, and maps the behaviour to an LLMInjection detection (existing or new), technique and ATT&CK IDs, or
marks it as generic (not specific to AI) and kept as a link. Rules are linked, not copied.

    git clone --depth 1 https://github.com/ThreatDefence/artex-detections.git /tmp/artex-detections
    python scripts/artex_detections_check.py --repo /tmp/artex-detections            # report
    python scripts/artex_detections_check.py --repo /tmp/artex-detections --write    # references/crosswalks/artex-detections.json

The repository is untrusted input: files are read as text, nothing in it is executed.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import load_data  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "references" / "crosswalks" / "artex-detections.json"
DOC = ROOT / "docs" / "ARTEX-DETECTION-MAP.md"
REPO = "https://github.com/ThreatDefence/artex-detections"
BLOB = REPO + "/blob/main/"

# behaviour -> (file-name keywords, LLMInjection detection or None, techniques, ATT&CK). Analyst mapping.
BEHAVIOURS = [
    ("ARTEX user agents", ["user_agent", "user-agent-any", "user-agent-naming", "indicator-sweep", "01-artex-user-agent"], "DET-AI-048", ["LLMI-T015"], ["T1595.002"]),
    ("Network signatures: user agents, probe artifacts, console pages and C2 (Zeek, Suricata)", ["artex.rules", "main.zeek"], "DET-AI-048", ["LLMI-T015"], ["T1595.002", "T1071.001"]),
    ("Placeholder probe paths and probe artifacts", ["placeholder_probe", "probe_artifacts", "web_probe", "web-probe", "06-web-probe", "application-reconnaissance"], "DET-AI-048", ["LLMI-T015"], ["T1595.003", "T1190"]),
    ("alg:none JWT spray on SSO routes", ["jwt_alg_none"], "DET-AI-048", ["LLMI-T015"], ["T1606.001", "T1190"]),
    ("OAuth callback probe", ["oauth_callback"], "DET-AI-048", ["LLMI-T015"], ["T1190"]),
    ("X-ARTX-KEY header and probe markers", ["probe_header"], "DET-AI-048", ["LLMI-T015"], ["T1595.002"]),
    ("ARTEX artifact names on hosts and in files", ["artifact_names", "artifact-names", "artex-names", "05-artex-artifact"], "DET-AI-048", ["LLMI-T015"], ["T1105"]),
    ("Callbacks to webhook and DNS log services", ["callback_services", "webhook-and-tunnel"], "DET-AI-048", ["LLMI-T015"], ["T1071.001", "T1567.004"]),
    ("User agent family burst from one source", ["user-agent-family-burst", "03-user-agent-family"], "DET-AI-049", ["LLMI-T015"], ["T1595.002"]),
    ("Password spray at a one-second rhythm", ["password-spray", "password_spray", "02-password-spray", "fixed-rhythm"], "DET-AI-049", ["LLMI-T015"], ["T1110.003"]),
    ("Spray that ends in a success", ["ends-in-a-successful", "signin_failure"], "DET-AI-049", ["LLMI-T015"], ["T1110.003", "T1078.004"]),
    ("Service principal secret guessing then success", ["service-principal-secret"], "DET-AI-050", ["LLMI-T015"], ["T1110.001", "T1078.004"]),
    ("One application hitting many resources", ["one-application-hitting"], "DET-AI-050", ["LLMI-T015"], ["T1526"]),
    ("Application adds credentials or assigns itself a role", ["app_credential_added", "app_role_assignment", "changing-their-own-access", "self-role-assignment", "role-to-itself"], "DET-AI-050", ["LLMI-T015"], ["T1098.001", "T1098.003"]),
    ("Scripted Microsoft Graph bursts", ["graph-bursts"], "DET-AI-050", ["LLMI-T015"], ["T1087.004"]),
    ("Bulk Key Vault secret reads", ["key-vault"], "DET-AI-047", ["LLMI-T015", "LLMI-T016"], ["T1555.006"]),
    ("CloudWatch secret search with a stolen key", ["cloudwatch", "filterlogevents"], "DET-AI-047", ["LLMI-T015", "LLMI-T016"], ["T1552"]),
    ("Access denied sweep", ["access_denied", "access-denied"], "DET-AI-047", ["LLMI-T015"], ["T1580"]),
    ("EC2 DryRun burst", ["dryrun", "aws-permission-testing"], "DET-AI-046", ["LLMI-T015"], ["T1580"]),
    ("Azure validate sweep and Kudu sign-ins", ["arm_validate", "validate-sweep", "azure-capability-checks"], "DET-AI-046", ["LLMI-T015"], ["T1580", "T1526"]),
    ("Cognito sign-up abuse and the discovery after it", ["cognito"], "DET-AI-051", ["LLMI-T015"], ["T1136.003"]),
    ("ARTEX console or backdoored image inside your network", ["console-or-backdoored", "artex.conf", "artex.yar"], "DET-AI-052", ["LLMI-T027", "LLMI-T011"], ["T1610", "T1195.002"]),
    ("Web or database service spawning shells", ["spawns_shell", "spawns-a-shell", "starting-shells", "04-web-service-spawns", "sqlserver_spawns"], None, ["LLMI-T015"], ["T1505.003", "T1059"]),
    ("Scripts written into web directories, JSP web shell names", ["webshell", "web-directories"], None, ["LLMI-T015"], ["T1505.003"]),
    ("BLOODALCHEMY files, svchost outside System32, system binary masquerade, fake Edge update task", ["bloodalchemy", "svchost", "masquerade", "fake_edge"], None, [], ["T1036.005", "T1053.005"]),
    ("Remote tasklist fan-out", ["tasklist"], None, [], ["T1057"]),
    ("Kerberoasting, DCSync and WinRM fan-out", ["kerberoasting"], None, [], ["T1558.003", "T1003.006", "T1021.006"]),
    ("SQL Server toolkit payload hosts", ["sql-server-toolkit", "toolkit_payload_hosts"], None, [], ["T1105"]),
    ("Reported C2 domains and addresses", ["infrastructure", "artex.intel", "artex-ip.rules", "watchlist"], None, ["LLMI-T015"], ["T1071"]),
]
PLATFORMS = {"sigma": "Sigma", "generated": "Sigma conversions", "sentinel": "Sentinel / Defender", "splunk": "Splunk",
             "elastic": "Elastic", "zeek": "Zeek", "suricata": "Suricata", "yara": "YARA", "osquery": "osquery"}
NEW_DETECTIONS = {  # proposed in data/detections.json with this crosswalk
    "DET-AI-048", "DET-AI-049", "DET-AI-050", "DET-AI-051", "DET-AI-052"}


def rule_files(repo: Path) -> list[Path]:
    keep = []
    for path in repo.rglob("*"):
        rel = path.relative_to(repo).as_posix()
        skip = ("README.md", "SUMMARY.md", "app.conf", "default.meta", "macros.conf", "transforms.conf", "savedsearches.conf", "__load__.zeek", ".csv")
        if path.is_file() and rel.split("/")[0] in PLATFORMS and not rel.endswith(skip):
            keep.append(path)
    return sorted(keep)


def splunk_searches(repo: Path) -> list[str]:
    conf = repo / "splunk" / "default" / "savedsearches.conf"
    return re.findall(r"^\[([^\]]+)\]", conf.read_text(encoding="utf-8", errors="replace"), re.M) if conf.is_file() else []


def behaviour_of(name: str) -> int | None:
    low = name.lower()
    for i, (_, keys, *_rest) in enumerate(BEHAVIOURS):
        if any(k in low for k in keys):
            return i
    return None


def build(repo: Path) -> dict:
    known = {d["id"] for d in load_data("detections")}
    rows = [{"behaviour": b, "detection": d, "techniques": t, "attack": a, "rules": []} for b, _, d, t, a in BEHAVIOURS]
    unassigned = []
    for path in rule_files(repo):
        rel = path.relative_to(repo).as_posix()
        i = behaviour_of(path.name) if rel.split("/")[0] != "generated" else behaviour_of(path.name)
        entry = {"path": rel, "platform": PLATFORMS[rel.split("/")[0]], "url": BLOB + rel}
        (rows[i]["rules"] if i is not None else unassigned).append(entry)
    for name in splunk_searches(repo):
        i = behaviour_of(re.sub(r"[^a-z0-9]+", "-", name.lower()))
        entry = {"path": f"splunk/default/savedsearches.conf [{name}]", "platform": "Splunk", "url": BLOB + "splunk/default/savedsearches.conf"}
        (rows[i]["rules"] if i is not None else unassigned).append(entry)
    for r in rows:
        r["platforms"] = sorted({x["platform"] for x in r["rules"]})
        r["status"] = ("existing" if r["detection"] in known and r["detection"] not in NEW_DETECTIONS else
                       "new" if r["detection"] else "generic-link-only")
    ioc_path = repo / "iocs" / "indicators.csv"
    iocs = list(csv.DictReader(ioc_path.open(encoding="utf-8"))) if ioc_path.is_file() else []
    commit = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    return {
        "meta": {"source": REPO, "commit": commit, "read": datetime.now(UTC).strftime("%Y-%m-%d"), "licence": "MIT",
                 "attribution": "ThreatDefence Pty Ltd, ARTEX Detections", "policy": "rules are linked, not copied; indicators are counted, not imported",
                 "mapping": "behaviour to detection, technique and ATT&CK is an analyst mapping (scripts/artex_detections_check.py)"},
        "summary": {"rule_files": sum(len(r["rules"]) for r in rows) + len(unassigned), "behaviours": len(rows),
                    "to_existing_detections": sorted({r["detection"] for r in rows if r["status"] == "existing"}),
                    "to_new_detections": sorted({r["detection"] for r in rows if r["status"] == "new"}),
                    "generic_link_only": [r["behaviour"] for r in rows if r["status"] == "generic-link-only"],
                    "unassigned_files": [u["path"] for u in unassigned],
                    "indicators": {"total": len(iocs), "by_type": dict(Counter(x["type"] for x in iocs)),
                                   "by_confidence": dict(Counter(x["confidence"] for x in iocs))}},
        "behaviours": rows,
        "detection_links": {d: sorted({x["url"] for r in rows if r["detection"] == d for x in r["rules"]})
                            for d in sorted({r["detection"] for r in rows if r["detection"]})},
    }


def markdown(data: dict) -> str:
    s, m = data["summary"], data["meta"]
    lines = [
        "# ARTEX detection map",
        "",
        f"Every rule in [ThreatDefence/artex-detections]({m['source']}) (MIT, commit `{m['commit']}`, read {m['read']}), grouped by the "
        "behaviour it detects and mapped to an LLMInjection detection, technique and ATT&CK IDs. Generated by "
        "`scripts/artex_detections_check.py`; the rules are linked, not copied.",
        "",
        f"**{s['rule_files']} rule files, {s['behaviours']} behaviours, {s['indicators']['total']} indicators.** "
        f"Existing detections they implement: {', '.join(s['to_existing_detections'])}. New specifications they back: {', '.join(s['to_new_detections'])}. "
        f"{len(s['generic_link_only'])} behaviours are generic intrusion detection, not specific to AI, and stay as links.",
        "",
        "| Behaviour | LLMInjection | Techniques | ATT&CK | Platforms | Rules |",
        "|---|---|---|---|---|---|",
    ]
    for r in data["behaviours"]:
        det = r["detection"] or "link only"
        rules = " · ".join(f"[{x['path'].split('/')[-1]}]({x['url']})" for x in r["rules"][:4]) + (f" · +{len(r['rules']) - 4}" if len(r["rules"]) > 4 else "")
        lines.append(f"| {r['behaviour']} | {det} ({r['status']}) | {', '.join(r['techniques']) or '–'} | {', '.join(r['attack'])} | {', '.join(r['platforms'])} | {rules} |")
    ind = s["indicators"]
    lines += ["", "## Indicators", "",
              f"{ind['total']} indicators, by type: " + ", ".join(f"{k} {v}" for k, v in sorted(ind["by_type"].items(), key=lambda kv: -kv[1])) + ". "
              "By confidence: " + ", ".join(f"{k} {v}" for k, v in ind["by_confidence"].items()) + ". "
              "They are not imported: use the repository's STIX 2.1 bundle or Sentinel watchlist, respect each address's review date, and never block on a low-confidence indicator alone.",
              "", "Context: [ARTEX dossier](../reports/dossiers/artex.md), [Detection engineering](DETECTION-ENGINEERING.md).", ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    data = build(a.repo)
    s = data["summary"]
    print(f"rule files {s['rule_files']} · behaviours {s['behaviours']} · indicators {s['indicators']['total']}")
    for r in data["behaviours"]:
        print(f"  {len(r['rules']):3}  {r['behaviour'][:58]:58}  {r['detection'] or '-':11} {r['status']}")
    print("unassigned:", s["unassigned_files"])
    if a.write:
        OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        DOC.write_text(markdown(data), encoding="utf-8")
        print(f"wrote {OUT.relative_to(ROOT)} and {DOC.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
