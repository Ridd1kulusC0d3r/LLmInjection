# Source Grading & Analytic Confidence

AI threat reporting is noisy. LLMInjection uses two separate dimensions: **source quality** and **analytic confidence**.

## Source grades

| Grade | Source class | Examples |
|---|---|---|
| A | Primary / authoritative | original vendor investigation, government advisory, project security notice, original paper |
| B | Strong secondary | established security research reproducing or independently analyzing primary evidence |
| C | Reputable journalism | professional reporting with named sources and clear attribution |
| D | Community / aggregator | blog, repository, forum or list compiling third-party claims |
| E | Unknown / unsupported | unattributed claims, screenshots without provenance, circular citations |

A lower-grade source is not automatically false. It simply carries less evidentiary weight.

## Analytic confidence

| Confidence | Meaning |
|---|---|
| confirmed | Direct authoritative evidence supports the claim |
| high | Strong evidence and/or multiple independent credible sources |
| medium | Plausible and partially supported, but material gaps remain |
| low | Limited support or meaningful contradictory evidence |
| unverified | Retained as a research lead, not treated as fact |

## Claim language

Use language that exposes uncertainty:

- **Observed:** the source directly reports the behavior.
- **Assessed:** the source makes an analytic judgment.
- **Linked:** evidence indicates an association, but not necessarily identity.
- **Overlaps with:** behavior/infrastructure/naming intersects with another cluster.
- **Unverified:** no adequate primary/independent support found.

Avoid converting vendor tracking labels into universal aliases without evidence.

## Time

Every record must include `last_verified`. AI security changes quickly; a correct 2024 statement may be misleading in 2026.

## Citation hierarchy

When several sources exist, prefer:

1. incident owner / affected project advisory;
2. primary threat-intelligence report;
3. government or standards body;
4. independent technical reproduction;
5. reputable journalism;
6. community summary.

## Research note

The initial repository corpus includes user-supplied 2025–2026 notes describing multiple APT/AI cases. Those notes are treated as leads, not as self-authenticating evidence. Claims are promoted into the tracker only after source validation.
