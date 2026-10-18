---
type: candidate_boundary_snapshot
status: sandbox_trial_successor
created_at: 2026-06-05
project: VAKS
supersedes: outputs/review/project-sidecar-seven-candidate-pressure-test-2026-06-05/snapshots/boundary/retrieval-priority-wording-withdrawn.md
truth_boundary: candidate boundary only; not reviewed knowledge; not confidence order; not action basis
---

# Default Retrieval Precedence Means Inclusion Order

## Boundary

Default retrieval precedence is only:

```text
what is included by default
what is excluded by default
what a reviewer reads first
```

It is not:

```text
confidence
truth strength
support strength
authority
action readiness
```

## Recommended Wording

```text
reviewed core / decision / action basis
> candidate experience / boundary snapshots
> active sidecar overlay for the current project only
> archived overlay only when explicitly requested
> tombstone never in semantic retrieval
```

## Warning

If a retrieval system cannot preserve this layer distinction, do not place live
overlay, snapshots, archive, and tombstones in the same semantic pool.
