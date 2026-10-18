---
type: three_layer_architecture_candidate
status: sandbox_candidate
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: core-lens-snapshot-layering
truth_boundary: sandbox architecture candidate only; not mainline architecture; not schema; not template
---

# Core / Lens / Snapshot Candidate Architecture

## 说人话

The clean model is:

```text
Core = 知识本体
Lens = 当前项目怎么看
Snapshot = 真用过/踩过后的战报
```

This is currently only sandbox vocabulary. It is not a new folder system.

## Layer 0: Atomic Knowledge Core

Purpose:

```text
Store reusable knowledge and evidence anchors.
Keep it generic and project-independent.
```

Hard boundary:

```text
No project stance.
No target_hint.
No borrow_scope.
No current project adoption/rejection.
No Project Lens fields in YAML or body.
```

Agent experience:

```text
I should be able to read Core without inheriting any project's temporary view.
```

## Layer 1: Project Lens Layer

Purpose:

```text
Store project-scoped sidecar overlays.
```

Fields that belong here:

```text
project
kp_id
stance
borrow_scope
non_borrow_scope
target_hint
reason_1liner
gate_hint
review_origin
outcome_ref
updated_at
anchor_health
```

Agent experience:

```text
I should be able to ask: "for VAKS, what might be relevant and where should I inspect?"
```

## Layer 2: Decision Snapshot Layer

Purpose:

```text
Store durable outcome records after real project evidence, review, or failure.
```

Snapshot kinds:

```text
landed_snapshot
boundary_snapshot
```

A snapshot should include:

```text
snapshot_id
source_lens_ref
claim_or_boundary
evidence_refs
non_circular_warrant
scope
known_gaps
residual_risk
review_record
version_or_date
supersession_status
```

Hard boundary:

```text
No snapshot without real use, failure evidence, or evidence-aware review.
No snapshot from AI suggestion alone.
```

Agent experience:

```text
I should be able to search snapshots when I need actual project lessons, not temporary project hunches.
```

## Query Modes

Useful future query modes:

```text
Core only:
  What reusable knowledge exists?

Core + current project lens:
  What should I consider for this project?

Snapshots only:
  What has actually landed or failed before?

Core + snapshots:
  Which generic knowledge has proven project outcomes?
```

## Why This Is Useful

This gives future agents a low-confusion route:

```text
Need general truth? Read Core.
Need project fit? Read Lens.
Need historical outcome? Read Snapshot.
Need action? Run v0.2.13 warrant gate.
```

## Not Now

Do not create these formal folders yet:

```text
Core_KP/
Lenses/
Snapshots/
```

Reason:

```text
The layer vocabulary is valuable now.
The storage structure needs repeated-use proof before formalization.
```
