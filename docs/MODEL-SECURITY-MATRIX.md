# Model & Architecture Security Matrix

A model name is not a security posture. Deployment architecture, tools, permissions, retrieval, memory and supply-chain controls often matter more than the base model.

This matrix evaluates **deployment classes**, not vendor popularity.

| Architecture | Primary exposure | High-priority risks | Critical controls |
|---|---|---|---|
| Closed model API | API, prompt/context, provider identity | injection, data disclosure, key theft, unsafe output | least privilege, gateway policy, egress control, logging, output validation |
| Open-weight hosted model | weights, serving stack, app | model tampering, insecure serving, extraction, injection | provenance, artifact integrity, serving hardening, access control |
| Local/offline LLM | endpoint, local files, runtime | unauthorized use, ungoverned data access, model provenance | software inventory, endpoint visibility, model inventory, policy |
| RAG application | ingestion, vector store, retrieval | indirect injection, knowledge poisoning, sensitive retrieval | provenance, ingestion policy, retrieval isolation, content labeling |
| Coding agent | source tree, package manager, shell/tools | dependency manipulation, secret exposure, unsafe code/action | sandboxing, dependency policy, human review, secret isolation |
| Tool-using agent | tool/API boundary | excessive agency, confused deputy, privilege misuse | capability allowlist, contextual authz, confirmation, audit |
| Multi-agent system | agent identity/message bus | impersonation, message injection, trust propagation | identity, message integrity, capability isolation, observability |
| AI gateway/proxy | central credentials/routing | secret concentration, supply-chain compromise, route tampering | hardened CI/CD, secret isolation, provenance, admin monitoring |
| Fine-tuning pipeline | data and training process | poisoning, backdoors, unauthorized data | dataset provenance, integrity checks, review, evaluation |
| Model registry / hub | artifact distribution | malicious model, dependency tampering, provenance loss | signatures/digests, trusted publishers, scanning, allowlists |

## Evaluation dimensions

For every model/system, document:

1. **Model provenance** — who published it, where, digest/signature, license.
2. **Data boundaries** — what content can enter context or training.
3. **Instruction hierarchy** — what sources can influence behavior.
4. **Tool authority** — which real-world capabilities are reachable.
5. **Credential scope** — what secrets the system can access.
6. **Memory** — what persists across requests and who can modify it.
7. **Retrieval trust** — where RAG content originates and how provenance is preserved.
8. **Network access** — which external systems are reachable.
9. **Observability** — which model/tool/action events are logged.
10. **Recovery** — how to revoke credentials, roll back models/data and reconstruct actions.

## Minimum control set for agentic systems

- explicit capability inventory;
- least-privilege tool credentials;
- separation of untrusted content from control instructions;
- user confirmation for high-impact actions;
- deterministic policy enforcement outside the model;
- provenance for memory and RAG content;
- complete tool-call audit trail;
- rate and cost controls;
- artifact/dependency provenance;
- kill switch / credential revocation path.

## Key principle

Model safety and system security overlap but are not identical. A well-aligned model connected to over-privileged tools can still create a dangerous system. Conversely, a tightly sandboxed architecture can substantially limit the impact of model failure.
