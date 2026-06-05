---
type: project_lens_overlay_index
status: pilot
created_at: 2026-06-05
truth_boundary: project lens overlays only; not reviewed knowledge; not ADR; not action basis; not schema
---

# Project Lens Overlays

Project Lens Overlay 是项目侧联标记层。

人话：

```text
通用知识点像书。
Project Lens 像贴在书上的透明纸。
项目判断写在透明纸上，不写进书本身。
```

它记录的是某个项目当前怎么看某个知识点：

```text
可能能借什么
不能借什么
可能借到哪里
为什么先这么看
落地前还要过什么 gate
```

它不是：

```text
source card
reviewed knowledge
architecture decision
action basis
truth confidence
formal schema
permanent project status
```

## Main Fields

```text
project
kp_id
kp_ref
stance: watch | partial | avoid | park
borrow_scope
target_hint
reason_1liner
```

`target_hint` is structured:

```yaml
target_hint:
  - type: doc | repo_symbol | repo_line | module | workflow | pr | unknown
    value: "<locator>"
    status: active | healthy | conceptual | not_checked | drifted | unanchored
    anchor_version: "<optional version/date/commit/check note>"
```

Keep the name `target_hint` because it is a possible inspection location, not a code-change decision.

`kp_ref` points back to the candidate/core knowledge point file so an agent can navigate:

```text
Lens -> kp_ref -> Derived From Sources -> raw source
```

Optional:

```text
non_borrow_scope
gate_hint
review_origin
outcome_ref
updated_at
anchor_health
```

## Current Layer Vocabulary

Sandbox vocabulary:

```text
Core = generic knowledge point body / evidence anchors
Lens = project-scoped sidecar view
Snapshot = landed_snapshot or boundary_snapshot after real outcome/review
```

This is not a formal folder/schema split yet.

High-intensity sandbox result:

```text
kp_ref and conceptual target status are useful for agent maintenance.
Knowledge Graph Lite, Warrant pipeline, governance automation, and formal Core_KP/Lenses/Snapshots folders remain deferred.
```

## Closeout

Closeout rule:

```text
Project Lens is scaffolding.
At project closeout, live Lens entries must drain into landed snapshot, boundary snapshot, archive, or restricted delete+tombstone.
carry-forward and supersede are actions, not durable states.
```

Retrieval priority:

```text
reviewed core / decision / action basis
> landed_snapshot / boundary_snapshot
> active Project Lens for current project only
> archived Lens
> tombstone never
```

## Overlays

- [[CLOSEOUT_PROTOCOL]]
- [[CLOSEOUT_PROTOCOL_OBSIDIAN_TEST_2026-06-05]]
- [[VAKS]]
- [[VAKS-closeout-manifest-2026-06-05]]
