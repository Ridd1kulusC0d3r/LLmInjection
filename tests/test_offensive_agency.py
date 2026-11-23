"""offensive.agency exposure snapshot: parsing, mapping to the graph, history and the committed snapshot."""

from __future__ import annotations

import csv
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import offensive_agency_sync as oa  # noqa: E402

STATS = {
    "active": 3, "total": 5, "new": 1, "multi": 1, "with_c2": 1, "domains": 2, "domains_cdn": 1, "ref_day": "2026-11-22",
    "active_since": "2026-11-16", "days": ["2026-11-21", "2026-11-22"],
    "kinds": {"hosting": 2, "cdn": 1}, "c2": [["Sliver", 1]], "pairs": [["ARTEX + PentAGI", 1]],
    "orgs": [["Example Hosting", 2]], "countries": [["US", 2], ["BR", 1]], "clusters": {"antifox": 1, "<bad>": 9},
    "series": {"artex": [1, 2], "pentagi": [0, 1]},
    "tools": {
        "artex": {"name": "ARTEX", "active": 2, "confirmed": 2, "new": 1, "total": 4, "ports": [[8787, 2]],
                  "countries": [["US", 1], ["BR", 1]], "orgs": [["Example Hosting", 2]]},
        "pentagi": {"name": "PentAGI<script>", "active": "1", "confirmed": None, "new": 0, "total": 1, "ports": []},
        "Bad Slug!": {"name": "x", "active": 99},
    },
}
HOSTS = [
    {"ip": "192.0.2.1", "country": "US", "kind": "hosting", "tools": {"artex": "confirmed"}},
    {"ip": "192.0.2.2", "country": "BR", "kind": "hosting", "tools": {"artex": "confirmed", "pentagi": "probable"}},
    {"ip": "198.51.100.7", "country": "US", "kind": "cdn", "tools": {"pentagi": "probable"}},
]
PAGE = """<html><body><h2>How it is detected</h2><p>ONYPHE category:ctiscan queries.</p>
<code>html.title.raw:&#34;ARTEX&#34;</code> <code>favicon.data.md5:cd3ebd16437d6d3963592f7365dd3980</code>
<a href="https://github.com/BaaRai/ARTEX">project</a><h2>Hosts</h2><code>html.title.raw:&#34;after&#34;</code></body></html>"""


class Summarise(unittest.TestCase):
    def setUp(self):
        self.snap = oa.summarise(STATS, HOSTS, "2026-11-23T00:00:00Z", {"artex": PAGE})

    def test_untrusted_input_is_coerced(self):
        slugs = [a["slug"] for a in self.snap["agents"]]
        self.assertEqual(slugs, ["artex", "pentagi"])  # bad slug dropped, sorted by active
        pentagi = self.snap["agents"][1]
        self.assertEqual((pentagi["active"], pentagi["confirmed"], pentagi["probable"]), (1, 0, 1))
        self.assertNotIn("<", pentagi["name"])
        self.assertEqual([c["slug"] for c in self.snap["clusters"]], ["antifox"])

    def test_maps_agents_and_clusters_to_graph_records(self):
        self.assertEqual(self.snap["agents"][0]["tool_id"], "TOOL-ARTEX")
        self.assertEqual(self.snap["clusters"][0]["tool_id"], "TOOL-ANTIFOX")
        tools = {t["id"] for t in json.loads((ROOT / "data" / "tools.json").read_text(encoding="utf-8"))}
        self.assertTrue({v for v in oa.TOOLS.values() if v} | {v for v in oa.CLUSTERS.values() if v} <= tools)

    def test_latam_and_cdn_counts_come_from_hosts(self):
        self.assertEqual(self.snap["latam"]["total"], 1)
        self.assertEqual(self.snap["latam"]["by_agent"]["BR"], {"artex": 1, "pentagi": 1})
        self.assertEqual(self.snap["totals"]["cdn_front_ips_in_hosts"], 1)

    def test_agent_page_fingerprints_stop_at_the_hosts_table(self):
        a = self.snap["agents"][0]
        self.assertEqual(a["fingerprints"], ['html.title.raw:"ARTEX"', "favicon.data.md5:cd3ebd16437d6d3963592f7365dd3980"])
        self.assertEqual(a["project"], "https://github.com/BaaRai/ARTEX")
        self.assertEqual(self.snap["agents"][1]["fingerprints"], [])

    def test_doc_renders_and_cites_the_source(self):
        doc = oa.render_doc(self.snap)
        self.assertIn("offensive.agency", doc)
        self.assertIn("SRC-OFFENSIVE-AGENCY-TRACKER", doc)
        self.assertNotIn("192.0.2.", doc)  # aggregates only, never the IP list


class History(unittest.TestCase):
    def test_same_day_is_replaced_not_duplicated(self):
        snap = oa.summarise(STATS, HOSTS, "2026-11-23T00:00:00Z")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "h.csv"
            self.assertEqual(oa.append_history(snap, p), 2)
            self.assertEqual(oa.append_history(snap, p), 2)
            snap["meta"]["ref_day"] = "2026-11-23"
            self.assertEqual(oa.append_history(snap, p), 4)
            self.assertEqual(len(list(csv.DictReader(io.StringIO(p.read_text(encoding="utf-8"))))), 4)


class CommittedSnapshot(unittest.TestCase):
    def test_snapshot_is_aggregate_and_consistent(self):
        snap = json.loads((ROOT / "data" / "exposure" / "offensive-agency.json").read_text(encoding="utf-8"))
        self.assertEqual(snap["meta"]["source_id"], oa.SOURCE_ID)
        self.assertGreater(snap["totals"]["active_ips"], 0)
        self.assertEqual(sum(a["active"] >= 0 for a in snap["agents"]), snap["totals"]["agents"])
        self.assertNotRegex(json.dumps(snap), r'"ip"\s*:')
        sources = {s["id"] for s in json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8"))}
        self.assertIn(oa.SOURCE_ID, sources)
        rows = list(csv.DictReader(io.StringIO((ROOT / "data" / "exposure" / "offensive-agency-history.csv").read_text(encoding="utf-8"))))
        self.assertIn(snap["meta"]["ref_day"], {r["day"] for r in rows})

    def test_unreachable_tracker_keeps_the_snapshot(self):
        before = (ROOT / "data" / "exposure" / "offensive-agency.json").read_bytes()
        self.assertEqual(oa.main(["--stats", "/nonexistent/stats.json"]), 0)
        self.assertEqual(oa.main(["--stats", "/nonexistent/stats.json", "--strict"]), 1)
        self.assertEqual((ROOT / "data" / "exposure" / "offensive-agency.json").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
