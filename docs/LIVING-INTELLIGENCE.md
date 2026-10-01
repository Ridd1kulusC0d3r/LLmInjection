# Living Intelligence Pipeline

LLMInjection treats AI threat intelligence as a **continuous evidence process**, not a periodically rewritten README.

## Operating model

```text
allow-listed primary sources
          ↓
automated metadata collection
          ↓
deduplication + relevance scoring
          ↓
research queue
          ↓
human evidence review
          ↓
promotion into structured CTI
          ↓
graph / STIX / API
          ↓
snapshot
          ↓
entity-level diff
          ↓
monthly landscape report
```

Collection is automated. **Promotion is not.**

The intake pipeline cannot create or modify official actor attribution, campaign intelligence, incidents, technique mappings, vulnerabilities, relationships or landscape metrics by itself.

## Daily intake

Workflow:

`.github/workflows/intelligence-intake.yml`

Schedule: daily.

The job reads `data/source-feeds.json` and collects metadata from enabled feeds. New items are normalized into `data/research-queue.json`.

If no new candidates are found, no PR is created.

If new candidates are found, the workflow updates a dedicated automation branch and opens or refreshes a review PR.

### Initial monitored feeds

| Feed | Role |
|---|---|
| MITRE ATLAS releases | canonical behavior / case-study changes |
| OWASP GenAI LLM Top 10 repository | canonical application-risk changes |
| Model Context Protocol releases | protocol/security evolution |
| GitHub Advisory Database | reviewed vulnerabilities |
| GitHub malware advisories | malicious-package intelligence |
| CISA KEV | authoritative exploited-vulnerability prioritization |

The registry is intentionally explicit. Arbitrary URLs are not fetched simply because a model decided they looked interesting.

## Research queue

`data/research-queue.json` is **not** an intelligence database.

It contains review candidates with:

- source feed;
- source grade;
- publication timestamp;
- candidate type;
- relevance score;
- matched terms;
- extracted CVE/GHSA/ATLAS/OWASP identifiers;
- review status;
- analyst notes.

Statuses:

`candidate → reviewing → accepted / rejected / duplicate`

An accepted queue item still needs to be represented correctly in the relevant official dataset.

## Relevance scoring

Scoring is transparent and intentionally simple.

Canonical framework/repository feeds receive maximum intake priority because they are already allow-listed by role.

Broad feeds such as advisories or KEV require AI/LLM/agent/MCP-related keyword matches. Identifiers such as CVE or GHSA increase triage priority.

The score is a **review-priority signal**, not analytic confidence.

## Monthly snapshots

Workflow:

`.github/workflows/landscape-snapshot.yml`

A monthly run generates:

```text
data/snapshots/YYYY-MM.json
reports/monthly/YYYY-MM.md
reports/monthly/YYYY-MM-diff.json
reports/monthly/YYYY-MM-diff.md
```

Snapshots include stable entity IDs and SHA-256 fingerprints for each structured object.

The diff engine therefore distinguishes:

- **added** objects;
- **removed** objects;
- **changed** objects.

This lets LLMInjection answer “what changed?” without pretending that a modified paragraph is a new threat.

## Explorer integration

The Pages build generates a current snapshot and compares it to the latest committed monthly baseline.

The Explorer exposes this as **What’s New**.

The diff is also published as:

```text
/intelligence-diff.json
/intelligence-diff.md
/current-snapshot.json
```

## Failure behavior

A temporary feed failure:

- is recorded in the intake report;
- does not promote stale or partial data;
- emits a workflow warning;
- does not convert missing evidence into a negative finding.

If a source disappears permanently, its registry entry should be disabled only after review.

## Promotion checklist

Before a candidate becomes official intelligence, verify:

1. Is the source primary or otherwise appropriate for the claim?
2. Is the candidate an observed fact, an assessment, research, or a proof of concept?
3. Does an existing object already represent it?
4. Are actor aliases and attribution claims explicitly supported?
5. Is the external framework mapping exact or only related?
6. Is confidence independent from source grade?
7. Are time window and affected population preserved?
8. Does the object need relationships, detections, tests or controls?
9. Does the change belong in the intelligence changelog?

## Design principle

The collector is allowed to be fast.

The intelligence layer is required to be careful.
