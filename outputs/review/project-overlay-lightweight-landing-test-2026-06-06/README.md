---
type: sandbox_landing_readme
status: active_test
created_at: 2026-06-06
truth_boundary: sandbox only; not reviewed knowledge; not architecture decision; not action basis
---

# Project Overlay Lightweight Landing Test

## One Sentence

This sandbox lands Pro's lightweight recommendation as a testable operating
pattern:

```text
keep the small project overlay note
do not mainline the object model
do not change schema / review queue / templates
```

In plain Chinese:

```text
保留项目借鉴清单，不再造项目知识子系统。
```

## What This Package Tests

This package tests whether a project can see reusable knowledge points through a
small project-scoped overlay note without tagging the knowledge point itself,
creating a formal workspace, or turning the overlay into truth / ADR / action
basis.

## Files

```text
protocol/PROJECT_OVERLAY_ONE_PAGE_PROTOCOL.md
project_overlays/MISA.md
project_overlays/VAKS.md
candidate_notes/experience/misa-runtime-memory-quarantine-no-effect-gate.md
candidate_notes/boundary/misa-retrieval-hints-not-control-authority.md
candidate_notes/boundary/misa-graph-carrier-not-controller.md
closeout/MISA-closeout-drain-note.md
checks/
package/
```

## Mainline Boundary

The real mainline files must stay unchanged in this phase:

```text
ARCHITECTURE_PRINCIPLES.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
SCHEMA.md
REVIEW_QUEUE.md
templates/
```

The current mainline already has enough:

```text
generic project-scoped sidecar overlay boundary principle
v0.2.13 action-facing warrant gate
```

## Naming

Near mainline:

```text
project-scoped sidecar overlay
```

Sandbox/operator shorthand:

```text
Project Overlay
```

Deprecated as a formal target:

```text
Project Lens
```

