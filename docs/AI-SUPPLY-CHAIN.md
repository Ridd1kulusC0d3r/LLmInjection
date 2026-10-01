# AI Supply-Chain Security

AI systems inherit ordinary software supply-chain risk and add new assets: model weights, datasets, adapters, vector stores, agent frameworks, MCP servers, gateways and model registries.

## Asset chain

```text
source code
   ↓
dependencies
   ↓
training / fine-tuning data
   ↓
model / adapter artifacts
   ↓
registry / hub
   ↓
serving image
   ↓
AI gateway
   ↓
agent / application
   ↓
MCP / tools / external services
```

## Minimum provenance record

For a production AI asset, record:

- artifact name and immutable digest;
- publisher / owner;
- source repository or registry;
- model family and exact version;
- dataset or fine-tuning provenance where applicable;
- build / release identity;
- signature or attestation status;
- dependencies;
- deployment environment;
- approval state.

## AI/ML-BOM

CycloneDX's AI/ML-BOM capability represents models, datasets, configurations and dependencies. LLMInjection treats it as a useful supply-chain transparency layer alongside ordinary SBOM practice.

Recommended relationship:

```text
AI/ML-BOM
   + SBOM
   + provenance / attestation
   + signatures
   + deployment inventory
   = useful supply-chain context
```

No single BOM format proves that an artifact is trustworthy. It makes trust decisions inspectable.

## Vulnerability and advisory enrichment

Machine-readable records live in `data/vulnerabilities.json`. The initial set includes the 2026 LiteLLM malicious-package incident, MCP authentication flaws and Trivy supply-chain / artifact-processing advisories. Records retain affected/fixed versions and primary GHSA/CVE/OSV identifiers.

These are not treated as actors or campaigns. They are separate graph objects that can be linked to incidents, techniques and controls.

## Controls already modeled

- `CTRL-AIML-BOM`
- `CTRL-ARTIFACT-PINNING`
- `CTRL-SIGNATURE-VERIFICATION`
- `CTRL-DEPENDENCY-POLICY`
- `CTRL-SECRET-ISOLATION`
- `CTRL-AI-INVENTORY`

## Detection hypotheses

- model digest drift before promotion;
- package installation before review completion;
- unexpected model registry publisher;
- AI gateway credential access anomaly;
- new MCP server/capability without configuration approval.

## Reference standards

- CycloneDX AI/ML-BOM;
- Sigstore / Cosign for artifact signing and verification;
- OpenSSF / SLSA concepts for build provenance;
- OWASP GenAI Supply Chain risk;
- CSA AI Controls Matrix;
- Google SAIF.
