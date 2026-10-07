#!/usr/bin/env python3
"""Build LLMInjection graph, GraphML and STIX 2.1 exports without external dependencies."""

from __future__ import annotations

import html
import json
import uuid
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)

DATASETS = {
    "actor": "actors.json",
    "campaign": "campaigns.json",
    "incident": "incidents.json",
    "technique": "techniques.json",
    "model": "models.json",
    "framework": "frameworks.json",
    "test-case": "test-cases.json",
    "control": "controls.json",
    "detection": "detections.json",
    "source": "sources.json",
    "vulnerability": "vulnerabilities.json",
}
NAMESPACE = uuid.UUID("b2f8bf4d-a6bf-4a9a-99d6-3a08e49fdc2b")

def load(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)

def node_type(record: dict, fallback: str) -> str:
    return record.get("type") or fallback

def label(record: dict) -> str:
    return record.get("name") or record.get("title") or record.get("id", "unknown")

def graph():
    nodes, by_id = [], {}
    for fallback, filename in DATASETS.items():
        for record in load(DATA / filename):
            rid = record["id"]
            n = {"id": rid, "type": node_type(record, fallback), "label": label(record), "data": record}
            nodes.append(n)
            by_id[rid] = n

    relationships = load(DATA / "relationships.json")
    edges = [{
        "id": rel["id"],
        "source": rel["source"],
        "target": rel["target"],
        "relationship": rel["relationship"],
        "confidence": rel["confidence"],
        "evidence_sources": rel.get("evidence_sources", []),
    } for rel in relationships]

    existing = {(e["source"], e["target"], e["relationship"]) for e in edges}
    for n in nodes:
        for source_id in n["data"].get("source_ids", []):
            key = (n["id"], source_id, "sourced-by")
            if key not in existing:
                edges.append({
                    "id": f"AUTO-SRC-{len(edges)+1:04d}",
                    "source": n["id"],
                    "target": source_id,
                    "relationship": "sourced-by",
                    "confidence": n["data"].get("confidence", "confirmed"),
                    "evidence_sources": [source_id],
                })
                existing.add(key)

    return {
        "meta": {
            "title": "LLMInjection Intelligence Graph",
            "generated_at": datetime.now(UTC).isoformat(),
            "node_count": len(nodes),
            "edge_count": len(edges),
        },
        "nodes": nodes,
        "edges": edges,
    }

def write_graph_json(g: dict) -> None:
    with (DIST / "graph.json").open("w", encoding="utf-8") as handle:
        json.dump(g, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

def write_graphml(g: dict) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
        '<key id="type" for="node" attr.name="type" attr.type="string"/>',
        '<key id="label" for="node" attr.name="label" attr.type="string"/>',
        '<key id="relationship" for="edge" attr.name="relationship" attr.type="string"/>',
        '<key id="confidence" for="edge" attr.name="confidence" attr.type="string"/>',
        '<graph id="LLMInjection" edgedefault="directed">',
    ]
    for n in g["nodes"]:
        lines.append(
            f'<node id="{html.escape(n["id"])}">'
            f'<data key="type">{html.escape(n["type"])}</data>'
            f'<data key="label">{html.escape(n["label"])}</data>'
            "</node>"
        )
    for e in g["edges"]:
        lines.append(
            f'<edge id="{html.escape(e["id"])}" source="{html.escape(e["source"])}" target="{html.escape(e["target"])}">'
            f'<data key="relationship">{html.escape(e["relationship"])}</data>'
            f'<data key="confidence">{html.escape(e["confidence"])}</data>'
            "</edge>"
        )
    lines.extend(["</graph>", "</graphml>"])
    (DIST / "graph.graphml").write_text("\n".join(lines) + "\n", encoding="utf-8")

def stix_id(stix_type: str, internal_id: str) -> str:
    return f"{stix_type}--{uuid.uuid5(NAMESPACE, stix_type + ':' + internal_id)}"

def stix_type_for(node: dict) -> str:
    return {
        "actor": "threat-actor",
        "campaign": "campaign",
        "incident": "x-llminjection-incident",
        "technique": "attack-pattern",
        "control": "course-of-action",
        "model": "x-llminjection-model",
        "framework": "x-llminjection-framework",
        "test-case": "x-llminjection-test-case",
        "detection": "x-llminjection-detection",
        "source": "x-llminjection-source",
        "vulnerability": "vulnerability",
    }.get(node["type"], "x-llminjection-object")

def stix_object(node: dict) -> dict:
    st = stix_type_for(node)
    data = node["data"]
    obj = {
        "type": st,
        "spec_version": "2.1",
        "id": stix_id(st, node["id"]),
        "created": "2026-09-30T00:00:00.000Z",
        "modified": "2026-09-30T00:00:00.000Z",
        "name": node["label"],
        "x_llminjection_id": node["id"],
    }
    description = data.get("summary") or data.get("description") or data.get("hypothesis")
    if description:
        obj["description"] = description
    if st == "threat-actor":
        obj["threat_actor_types"] = ["unknown"]
    if st == "vulnerability":
        refs = []
        for identifier in data.get("identifiers", []):
            if identifier.startswith("CVE-"):
                refs.append({
                    "source_name": "cve",
                    "external_id": identifier,
                    "url": f"https://www.cve.org/CVERecord?id={identifier}",
                })
            elif identifier.startswith("GHSA-"):
                refs.append({
                    "source_name": "ghsa",
                    "external_id": identifier,
                    "url": f"https://github.com/advisories/{identifier}",
                })
            elif identifier.startswith("MAL-"):
                refs.append({
                    "source_name": "osv",
                    "external_id": identifier,
                    "url": f"https://osv.dev/vulnerability/{identifier}",
                })
        if refs:
            obj["external_references"] = refs
    return obj

def write_stix(g: dict) -> None:
    id_map, objects = {}, []
    for node in g["nodes"]:
        obj = stix_object(node)
        id_map[node["id"]] = obj["id"]
        objects.append(obj)
    conf = {"confirmed": 95, "high": 80, "medium": 60, "low": 30, "unverified": 10}
    for edge in g["edges"]:
        if edge["source"] not in id_map or edge["target"] not in id_map:
            continue
        objects.append({
            "type": "relationship",
            "spec_version": "2.1",
            "id": stix_id("relationship", edge["id"]),
            "created": "2026-09-30T00:00:00.000Z",
            "modified": "2026-09-30T00:00:00.000Z",
            "relationship_type": edge["relationship"],
            "source_ref": id_map[edge["source"]],
            "target_ref": id_map[edge["target"]],
            "confidence": conf.get(edge["confidence"], 50),
            "x_llminjection_id": edge["id"],
        })
    bundle = {
        "type": "bundle",
        "id": f"bundle--{uuid.uuid5(NAMESPACE, 'bundle:llminjection')}",
        "objects": objects,
    }
    with (DIST / "llminjection-stix.json").open("w", encoding="utf-8") as handle:
        json.dump(bundle, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

def main() -> int:
    g = graph()
    write_graph_json(g)
    write_graphml(g)
    write_stix(g)
    print(f"Built {g['meta']['node_count']} nodes and {g['meta']['edge_count']} edges")
    print("Wrote dist/graph.json, dist/graph.graphml and dist/llminjection-stix.json")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
