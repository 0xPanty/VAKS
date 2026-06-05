---
type: snapshot_trials
status: pass
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: project-lens-landed-boundary-snapshot-trials
truth_boundary: sandbox snapshot trials only; not reviewed knowledge; not mainline architecture
---

# Snapshot Trials

## Purpose

Test whether Pro's split works in practice:

```text
stance = current project posture
outcome_ref = real or candidate outcome snapshot
```

The key question:

```text
Can we attach outcomes without turning `stance` into landed/avoid?
```

## Created Candidate Snapshots

### Landed Candidate

```text
snapshots/landed/project-lens-sidecar-agent-maintenance-sandbox.md
```

Meaning:

```text
kp_ref + conceptual target status landed as useful sandbox maintenance behavior.
```

Boundary:

```text
Not reviewed knowledge.
Not mainline architecture.
Not schema.
```

### Boundary Candidate 1

```text
snapshots/boundary/retrieval-score-is-not-support.md
```

Linked from:

```text
retrieval-is-activation-not-truth
```

Meaning:

```text
Retrieval/rerank/dashboard/GraphRAG hits are activation signals, not support or action readiness.
```

### Boundary Candidate 2

```text
snapshots/boundary/graph-lite-core-pollution.md
```

Linked from:

```text
graph-and-ontology-as-candidate-context
```

Meaning:

```text
Graph-lite relations may help navigation, but should not enter Core before relation review.
```

### Boundary Candidate 3

```text
snapshots/boundary/project-lens-as-adr.md
```

Not linked to a single Lens Entry yet.

Meaning:

```text
Project Lens must not be written as a tiny ADR or cited as action basis.
```

## Boundary Snapshot Shape Check

```text
snapshot_files=4
boundary_snapshots=3
missing_boundary_sections=0
```

Required boundary sections checked:

```text
Trap Title
Bad Move Or Non-Fit
Failure Context
Trigger Conditions
Why It Failed
Boundary Of Applicability
Warning One-Liner
Safer Alternative Or Escalation
Evidence Refs
```

## Result

```yaml
stance_outcome_split: pass
outcome_ref_resolution: pass
boundary_shape: pass
landed_shape: useful_for_sandbox
authority_leakage: contained_by_candidate_snapshot_truth_boundary
```

## Agent Experience Verdict

The split is workable.

The important rule is:

```text
Never change stance to landed.
Never change stance to failed.
Keep the result in a snapshot and link it through outcome_ref.
```
