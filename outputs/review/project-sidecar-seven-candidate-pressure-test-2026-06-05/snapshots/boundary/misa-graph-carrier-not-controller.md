---
type: candidate_boundary_snapshot
status: sandbox_trial
created_at: 2026-06-05
project: MISA
kp_ref: outputs/review/candidate_pattern_bank/graph-and-ontology-as-candidate-context.md
from_lens_ref: outputs/review/project-sidecar-seven-candidate-pressure-test-2026-06-05/misa_overlay/MISA.md#entry-graph-and-ontology-as-candidate-context
truth_boundary: candidate boundary only; not universal ban; not reviewed knowledge; not Misa decision; not action basis
---

# Misa Graph Carrier Is Not The Controller

## Trap Title

Graph or orchestration layer starts owning deterministic control.

## Bad Move / Non-Fit

Using graph nodes, LangGraph routing, community reports, or ontology-like object
models to decide Misa route authority, winner authority, setpoint mutation,
provider route, memory writes, skill publication, VPS updates, or production
rollout.

## Evidence Refs

```text
docs/current/control-boundaries.md
ARCHITECTURE.md LangGraph bridge section
```

The observed project boundary says graph/carrier layers may be useful, but the
Qianxuesen deterministic control path owns route, metric, signal extraction,
candidate reducer, and authority boundaries.

## Scope Boundary

This is not a ban on graph/carrier tooling. It only says graph structure must
remain context/candidate plumbing unless separately reviewed as a control
contract change.

## Safer Alternative

Use graph-like surfaces as typed context and replayable candidate routing
inputs. Keep controller authority in deterministic reducers and human-owner
gates.
