# Publishing & Release Process

## GitHub Pages one-time setup

The Explorer workflow is already committed. GitHub Pages itself must be enabled once for the repository:

```text
Repository
  → Settings
  → Pages
  → Build and deployment
  → Source: GitHub Actions
```

After that, run **Deploy AI Threat Intelligence Explorer** manually or push a relevant change.

Expected public URL:

https://ridd1kulusc0d3r.github.io/LLmInjection/

The workflow validates intelligence and builds the graph before publishing. A failed validation therefore prevents stale or structurally broken graph data from being deployed.

## Static API

The build generates a versioned read-only API:

```text
/api/v1/index.json
/api/v1/actors.json
/api/v1/campaigns.json
/api/v1/incidents.json
/api/v1/techniques.json
/api/v1/models.json
/api/v1/frameworks.json
/api/v1/test-cases.json
/api/v1/controls.json
/api/v1/detections.json
/api/v1/sources.json
/api/v1/relationships.json
/api/v1/vulnerabilities.json
/api/v1/threat-landscape-2026.json
/api/v1/graph.json
/api/v1/llminjection-stix.json
```

This is intentionally a static API. A future TAXII endpoint requires a stateful service and is not represented as already implemented.

## Data releases

Tagged releases matching `data-v*` invoke the release pipeline.

Example:

```text
data-v0.2.0
```

The workflow:

1. validates all datasets;
2. builds graph/STIX/GraphML/API outputs;
3. creates a release archive;
4. creates a SHA-256 checksum;
5. generates a signed GitHub artifact provenance attestation;
6. publishes the archive/checksum as GitHub Release assets.

Consumers can verify the GitHub attestation with GitHub CLI:

```bash
gh attestation verify <release-archive.zip> --repo Ridd1kulusC0d3r/LLmInjection
```

## Versioning

The dataset manifest uses a schema version separate from the snapshot date.

- **schema_version** changes when consumers may need to adapt parsing.
- **snapshot** indicates the intelligence snapshot.
- Git tags version the published release artifact.

This separation avoids the delightful mistake of treating “new intelligence” and “breaking schema change” as the same event.

## Local build

```bash
python scripts/validate_intel.py
python scripts/build_graph.py
python scripts/build_api.py
python scripts/build_release.py
```

Outputs live under `dist/`.

## ATT&CK Navigator layers

`python scripts/build_navigator.py` writes `dist/navigator/atlas-coverage.layer.json` and `attack-coverage.layer.json` (layer format 4.5), published with the Explorer at `/navigator/`. Each external technique ID is scored 0 to 3: one point each for a linked safe test, detection and control, taking the best of the LLMInjection techniques that map to it. The `domain` value of the ATLAS layer is an assumption about how an ATLAS-aware Navigator names its matrix; adjust it if your build expects another.

## Ecosystem verification

`scripts/check_ecosystem.py` checks each project in `data/ecosystem.json` against the GitHub API (existence, archived flag, last push, renames). The weekly workflow `ecosystem-verify.yml` runs it and uploads a report and a refreshed dataset as an artifact; it never edits the repository on its own. Analyst fields (evidence class, section, techniques) are never changed by the script.

