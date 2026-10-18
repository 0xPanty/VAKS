---
record_kind: sandbox_integration_readiness_check
status: pass
project_id: VAKS
created_at: 2026-06-11
truth_boundary: diagnostic_not_mainline_decision
action_basis_allowed: false
---

# Phase B Integration Readiness Check

## Result

```text
readiness status: pass
error count: 0
```

## Compared Floor

```text
previous version: contract-passing adapter skeleton
required: tie or beat skeleton metrics, keep zero leakage, keep contract pass
```

## Metrics Checked

| Set | Corpus | hit@5 | hit@10 | MRR | Leakage | Forbidden top1 | Cross-bucket violation |
|---|---|---:|---:|---:|---:|---:|---:|
| main | primary | 30/30 | 30/30 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| main | full | 30/30 | 30/30 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| holdout | primary | 12/15 | 13/15 | 0.7811 | 0.0000 | 0.0000 | 0.0000 |
| holdout | full | 13/15 | 13/15 | 0.7591 | 0.0000 | 0.0000 | 0.0000 |

## Contract Checked

```text
contract status: pass
contract errors: 0
```

## Package Coverage

```text
required headings checked: 11
required artifacts checked: 12
```

## Errors

- none
