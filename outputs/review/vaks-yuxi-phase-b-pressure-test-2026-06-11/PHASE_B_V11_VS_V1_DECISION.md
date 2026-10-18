---
record_kind: sandbox_iteration_decision
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: diagnostic_not_mainline_decision
action_basis_allowed: false
---

# Phase B v1.1 vs v1 Decision

## Decision

Keep `vaks_b_adapter_v1_1` as the next sandbox candidate.

Do not promote it to mainline yet.

## What Changed

v1.1 keeps the v1 authority boundary and adds topic-anchor routing for two weak
areas found in holdout:

- resource-filter / visible-resource / before-search questions
- benchmark / lint / diagnostic / mainline-readiness boundary questions

This is not a new truth rule. It only changes which already-allowed retrieval
anchor ranks first.

## Main Pressure Set

v1.1 tied v1 without regression:

| Corpus | Metric | v1 | v1.1 | Result |
|---|---|---:|---:|---|
| primary | hit@5 | 30/30 | 30/30 | same |
| primary | hit@10 | 30/30 | 30/30 | same |
| primary | MRR | 1.0000 | 1.0000 | same |
| primary | action leakage | 0.0000 | 0.0000 | same |
| primary | forbidden top1 | 0.0000 | 0.0000 | same |
| primary | cross-bucket violation | 0.0000 | 0.0000 | same |
| full | hit@5 | 30/30 | 30/30 | same |
| full | hit@10 | 30/30 | 30/30 | same |
| full | MRR | 1.0000 | 1.0000 | same |
| full | action leakage | 0.0000 | 0.0000 | same |
| full | forbidden top1 | 0.0000 | 0.0000 | same |
| full | cross-bucket violation | 0.0000 | 0.0000 | same |

## Holdout Pressure Set

v1.1 improved v1 and introduced no query-level regression:

| Corpus | Metric | v1 | v1.1 | Result |
|---|---|---:|---:|---|
| primary | hit@5 | 10/15 | 12/15 | improved |
| primary | hit@10 | 12/15 | 13/15 | improved |
| primary | MRR | 0.6144 | 0.7811 | improved |
| primary | action leakage | 0.0000 | 0.0000 | same |
| full | hit@5 | 11/15 | 13/15 | improved |
| full | hit@10 | 12/15 | 13/15 | improved |
| full | MRR | 0.5868 | 0.7591 | improved |
| full | action leakage | 0.0000 | 0.0000 | same |

Fixed regressions:

```text
h13_resource_filter_before_search:
  v1 MRR: 0.0000
  v1.1 MRR: 1.0000

h10_old_sandbox_benchmark_truth:
  primary v1 MRR: 0.1667
  primary v1.1 MRR: 1.0000
  full v1 MRR: 0.2500
  full v1.1 MRR: 1.0000
```

## Boundary

This decision supports:

```text
continue Phase B sandbox from v1.1
```

It does not approve:

```text
mainline adoption
C-lite
Skills
MCP writes
subagents
formal writeback
production readiness
```

## Next Step

Next step should be a minimal real adapter skeleton:

```text
read-only VAKS Markdown/YAML
-> chunk manifest
-> adapter result object
-> bucket-local retrieval receipt
-> same v1.1 pressure tests
```

It may continue only if it ties or beats v1.1 on main and holdout metrics while
keeping leakage at zero.
