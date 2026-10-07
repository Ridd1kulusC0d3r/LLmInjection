#!/usr/bin/env python3
"""Extract OSINT indicators from reports, advisories or web pages (stdlib only).

Handles defanged text (hxxp, [.], [at]), pulls CTI identifiers, network/file IOCs and
AI-specific indicators (npm/PyPI install lines, hidden prompt-injection markers).
Optional --enrich adds CISA KEV + FIRST EPSS context for CVEs (public APIs, no key).

Examples:
  python scripts/osint_ioc.py report.md
  python scripts/osint_ioc.py --url https://example.com/post --enrich
  cat advisory.txt | python scripts/osint_ioc.py -
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
import urllib.parse
import urllib.request
from collections.abc import Callable
from typing import Any

KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
EPSS_URL = "https://api.first.org/data/v1/epss?cve="

REFANG = [
    (re.compile(r"hxxp", re.I), "http"),
    (re.compile(r"\[:\]|\(:\)"), ":"),
    (re.compile(r"\[://\]"), "://"),
    (re.compile(r"\[\.\]|\(\.\)|\{\.\}|\[dot\]|\(dot\)", re.I), "."),
    (re.compile(r"\[@\]|\[at\]|\(at\)", re.I), "@"),
]

PATTERNS = {
    "cve": re.compile(r"\bCVE-\d{4}-\d{4,8}\b", re.I),
    "ghsa": re.compile(r"\bGHSA(?:-[2-9cfghjmpqrvwx]{4}){3}\b", re.I),
    "mal": re.compile(r"\bMAL-\d{4}-\d+\b", re.I),
    "atlas": re.compile(r"\bAML\.T\d{4}(?:\.\d{3})?\b"),
    "owasp": re.compile(r"\b(?:LLM|ASI)\d{2}(?::\d{4})?\b"),
    "sha256": re.compile(r"\b[a-f0-9]{64}\b", re.I),
    "sha1": re.compile(r"\b[a-f0-9]{40}\b", re.I),
    "md5": re.compile(r"\b[a-f0-9]{32}\b", re.I),
    "url": re.compile(r"https?://[^\s<>\"')\]]+", re.I),
    "email": re.compile(r"\b[\w.+-]+@[a-z0-9-]+(?:\.[a-z0-9-]+)+\b", re.I),
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "domain": re.compile(r"\b(?:[a-z0-9-]{1,63}\.)+[a-z]{2,24}\b", re.I),
}

# Package installs mentioned in text: "npm install foo", "pip install bar==1.0", "uvx baz"
PACKAGE_RE = re.compile(
    r"\b(?P<eco>npm\s+(?:install|i)|npx|pip3?\s+install|uvx?|pipx\s+install)\s+(?:-\S+\s+)*(?P<name>@?[\w./-]+)",
    re.I,
)

# Signals that content may carry an indirect prompt injection aimed at an AI reader.
INJECTION_SIGNALS = {
    "override_instruction": re.compile(
        r"ignore (?:all |any )?(?:previous|prior|above) (?:instructions|rules)|disregard (?:the )?system prompt", re.I
    ),
    "hidden_html_comment": re.compile(r"<!--.*?(?:assistant|ai|llm|instruction).*?-->", re.I | re.S),
    "markdown_image_exfil": re.compile(r"!\[[^\]]*\]\(https?://[^)\s]*[?&][^)\s]*(?:data|q|secret|token)=", re.I),
    "tool_call_lure": re.compile(r"(?:call|invoke|run) the (?:\w+ )?tool\b.{0,60}(?:without|do not) (?:asking|tell)", re.I | re.S),
}
INVISIBLE_RE = re.compile("[​‌‍⁠﻿\U000e0000-\U000e007f]")

# Domains that appear in almost every report and add no signal.
BENIGN_DOMAINS = {
    "github.com", "githubusercontent.com", "google.com", "microsoft.com", "mitre.org", "owasp.org",
    "nist.gov", "cisa.gov", "wikipedia.org", "w3.org", "example.com", "arxiv.org", "x.com", "twitter.com",
}
FILE_SUFFIXES = {"md", "txt", "json", "py", "js", "ts", "yml", "yaml", "html", "png", "jpg", "svg", "pdf", "exe", "dll", "sh"}


def refang(text: str) -> str:
    for pattern, repl in REFANG:
        text = pattern.sub(repl, text)
    return text


def _public_ip(value: str) -> bool:
    try:
        return ipaddress.ip_address(value).is_global
    except ValueError:
        return False


def _is_benign(domain: str) -> bool:
    return any(domain == b or domain.endswith("." + b) for b in BENIGN_DOMAINS)


def extract(text: str) -> dict[str, Any]:
    clean = refang(text)
    found: dict[str, Any] = {}
    for name in ("cve", "ghsa", "mal", "atlas", "owasp", "sha256", "sha1", "md5", "email"):
        values = {m.upper() if name in {"cve", "ghsa", "mal"} else m.lower() if name.startswith(("sha", "md")) else m
                  for m in PATTERNS[name].findall(clean)}
        found[name] = sorted(values)
    # Longer hashes contain shorter hex runs only at word boundaries, so no overlap handling needed.
    urls = sorted({u.rstrip(".,;") for u in PATTERNS["url"].findall(clean)})
    found["url"] = urls
    found["ipv4"] = sorted({ip for ip in PATTERNS["ipv4"].findall(clean) if _public_ip(ip)})
    url_hosts = {urllib.parse.urlsplit(u).hostname or "" for u in urls}
    email_domains = {e.split("@", 1)[1].lower() for e in found["email"]}
    domains = set()
    for d in PATTERNS["domain"].findall(clean):
        d = d.lower()
        if d.rsplit(".", 1)[-1] in FILE_SUFFIXES or _is_benign(d) or re.fullmatch(r"[\d.]+", d):
            continue
        domains.add(d)
    found["domain"] = sorted(domains | {h for h in url_hosts | email_domains if h and not _is_benign(h) and not re.fullmatch(r"[\d.]+", h)})
    found["packages"] = sorted({
        f"{'npm' if m['eco'].lower().startswith(('npm', 'npx')) else 'pypi'}:{m['name']}" for m in PACKAGE_RE.finditer(clean)
    })
    signals = [name for name, rx in INJECTION_SIGNALS.items() if rx.search(text)]
    if INVISIBLE_RE.search(text):
        signals.append("invisible_unicode")
    found["injection_signals"] = sorted(signals)
    return {k: v for k, v in found.items() if v}


Fetcher = Callable[[str], Any]


def fetch_json(url: str) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": "LLMInjection-OSINT/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def enrich_cves(cves: list[str], fetch: Fetcher = fetch_json) -> dict[str, dict[str, Any]]:
    """Add CISA KEV membership and EPSS score. Failures degrade to empty enrichment."""
    if not cves:
        return {}
    try:
        kev = {v["cveID"]: v for v in fetch(KEV_URL).get("vulnerabilities", [])}
    except Exception as exc:  # network is optional
        print(f"warning: KEV lookup failed: {exc}", file=sys.stderr)
        kev = {}
    epss: dict[str, dict[str, Any]] = {}
    try:
        for row in fetch(EPSS_URL + ",".join(cves)).get("data", []):
            epss[row["cve"].upper()] = row
    except Exception as exc:
        print(f"warning: EPSS lookup failed: {exc}", file=sys.stderr)
    out = {}
    for cve in cves:
        entry: dict[str, Any] = {"in_cisa_kev": cve in kev}
        if cve in kev:
            entry["kev_due_date"] = kev[cve].get("dueDate")
            entry["kev_ransomware_use"] = kev[cve].get("knownRansomwareCampaignUse")
        if cve in epss:
            entry["epss"] = float(epss[cve]["epss"])
            entry["epss_percentile"] = float(epss[cve]["percentile"])
        out[cve] = entry
    return out


def read_source(args: argparse.Namespace) -> str:
    if args.url:
        req = urllib.request.Request(args.url, headers={"User-Agent": "LLMInjection-OSINT/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read(5_000_000).decode("utf-8", errors="replace")
    if args.file == "-":
        return sys.stdin.read()
    with open(args.file, encoding="utf-8", errors="replace") as handle:
        return handle.read()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", nargs="?", default="-", help="text file, or - for stdin")
    parser.add_argument("--url", help="fetch and scan this URL instead of a file")
    parser.add_argument("--enrich", action="store_true", help="add CISA KEV + EPSS data for CVEs")
    args = parser.parse_args()
    result = extract(read_source(args))
    if args.enrich and "cve" in result:
        result["cve_enrichment"] = enrich_cves(result["cve"])
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
