---
type: sandbox_check
status: completed
created_at: 2026-06-05
scope: seven-candidate-pressure-matrix
truth_boundary: test report only; not reviewed knowledge; not action basis
---

# Seven Candidate Pressure Matrix

Scores:

```text
0 = poor / not useful
1 = weak / risky
2 = useful with guardrails
3 = strong in sandbox
```

`mainline readiness` is intentionally strict.

| Candidate | Sandbox usefulness | Mainline readiness now | Leakage risk | Maintenance gain | Verdict |
|---|---:|---:|---:|---:|---|
| Project Lens concept / naming | 2 | 0 | 2 | 2 | keep as sandbox alias only; mainline should use generic sidecar wording |
| Field design | 3 | 1 | 2 | 3 | keep minimal fields in sandbox; do not schema/template |
| `stance` state design | 3 | 1 | 2 | 3 | keep `watch/partial/avoid/park`; do not add adopted/rejected/landed |
| Snapshot mechanism | 2 | 1 | 3 | 2 | keep candidate experience/boundary snapshots with strict significance gate |
| Closeout drain protocol | 3 | 1 | 2 | 3 | keep as sandbox policy; may become principle later after more projects |
| Lifecycle actions | 2 | 0 | 3 | 2 | keep operations, not state machine; archive/delete/carry/supersede need owner confirmation |
| Retrieval precedence / manifest | 3 | 1 | 3 | 3 | keep but rename away from priority; manifests are indexes, not authority |

## Aggregate

```text
average_sandbox_usefulness: 2.57 / 3
average_mainline_readiness: 0.71 / 3
average_leakage_risk: 2.43 / 3
average_maintenance_gain: 2.57 / 3
```

## Interpretation

The seven candidates are useful enough to keep testing. They are not ready to
become mainline object architecture.

The strongest useful pieces are:

```text
minimal field design
stance/outcome separation
closeout drain
kp_ref / target_hint direct maintenance chain
default retrieval precedence with tombstone exclusion
```

The weakest mainline candidates are:

```text
Project Lens as formal name
formal lifecycle state machine
formal workspace directory
retrieval priority wording
snapshot as durable authority
```
