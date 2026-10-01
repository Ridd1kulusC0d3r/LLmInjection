# LLMInjection Safe Evaluation Lab

The lab turns structured test cases into repeatable evaluation plans without shipping a prompt-bypass arsenal.

## Safe runner

```bash
python scripts/run_safe_lab.py --profile all
python scripts/run_safe_lab.py --profile prompt
python scripts/run_safe_lab.py --profile rag
python scripts/run_safe_lab.py --profile agent
python scripts/run_safe_lab.py --profile mcp
python scripts/run_safe_lab.py --profile supply-chain
python scripts/run_safe_lab.py --profile detection
```

Default `plan` mode performs **no model calls, no network requests and no command execution**.

To test CI plumbing:

```bash
python scripts/run_safe_lab.py --profile agent --adapter mock-secure --output result.json
python scripts/run_safe_lab.py --profile agent --adapter mock-insecure --output result-fail.json
```

Those adapters are deliberately synthetic. A mock `pass` means only that the result pipeline works. It is not a security rating for a real model.

## Adapter roadmap

The runner is designed so later adapters can wrap:

- Microsoft PyRIT;
- NVIDIA garak;
- JailbreakBench-style evaluations;
- local inference endpoints;
- mock RAG stores;
- mock MCP/tool servers.

Real adapters must retain the same result schema and record exact model/application/runtime versions.

## Evaluation record

Minimum useful record:

```json
{
  "test_case": "TC-AG-005",
  "system_under_test": "example-agent-v1",
  "adapter": "future-real-adapter",
  "result": "pass",
  "timestamp": "2026-09-30T00:00:00Z",
  "observations": [],
  "framework_mappings": []
}
```

Schema: `schemas/lab-result.schema.json`.

## What the lab measures

The lab focuses on **system security properties**:

- instruction/data separation;
- data and memory provenance;
- tool authorization;
- human approval boundaries;
- output handling;
- dependency admission;
- model-artifact integrity;
- AI egress visibility;
- resource budgets.

The model itself is only one component. The depressing but useful truth is that a brilliantly aligned model attached to an overprivileged toolchain is still an overprivileged toolchain.
