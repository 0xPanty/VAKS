---
type: pro_response_landing_note
status: candidate-only-landing
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: project-lens-overlay-and-knowledge-flywheel
truth_boundary: candidate design landing note only; not reviewed knowledge; not schema; not template; not architecture decision; not action basis
write_scope: outputs/review only
---

# Project Lens Pro Response Landing Note

## 说人话结论

Pro verdict:

```text
accept_direction
```

但是 Pro 支持的不是一个更大的“开发区 / 账本 / 真理库”，而是一个更轻的结构：

```text
外部来源
-> Source Card / source record
-> 通用原子知识点
-> Project Lens sidecar overlay
-> 只有需要 promotion / decision / action basis 时
   才进入 evidence-aware review / non-circular warrant gate
```

人话：

```text
不要在通用知识点正文上写项目判断。
给当前项目贴一层可拆、可撤、可归档的透明透镜。
真的落地或踩坑以后，再把少数结果快照成经验资产或边界资产。
```

## What Changed From The Earlier Candidate

Earlier wording:

```text
development borrowing tags / Project Borrowing Ledger
watch / borrow / avoid / landed / parked
```

Revised candidate wording:

```text
Project Lens / project-lens overlay
stance: watch | partial | avoid | park
outcome_ref: empty | landed_snapshot | boundary_snapshot
```

Meaning:

```text
stance = current project posture during development
outcome_ref = link to a real project outcome snapshot, if one exists
```

`landed` and `踩坑` should not be ordinary live tags. They should become snapshots only after real use, review, or failure experience.

## Minimal Candidate Implementation

This window applies the Pro direction only in `outputs/review`:

```text
outputs/review/project_lens_overlays/VAKS.md
```

This file is the candidate sidecar overlay for VAKS. It is not a formal schema, not a template, not reviewed knowledge, and not a mainline architecture object.

The old `outputs/review/project_borrowing_ledgers/VAKS.md` should be read as a derived project view, not the main authoring surface.

## Minimum Fields

Recommended required fields:

```text
project
kp_id
kp_ref
stance
borrow_scope
target_hint
reason_1liner
```

Optional fields:

```text
non_borrow_scope
gate_hint
review_origin
outcome_ref
updated_at
anchor_health
```

## Target Hint Convention

`target_hint` should help future agents jump from knowledge to engineering context, but it is still only a possible action location, not a decision.

Candidate structured format:

```yaml
target_hint:
  - type: doc | repo_symbol | repo_line | module | workflow | pr | unknown
    value: "<locator>"
    status: active | healthy | conceptual | not_checked | drifted | unanchored
    anchor_version: "<optional version/date/commit/check note>"
```

Prefer `path + heading/symbol/module`. Line numbers are useful hints but may drift.

Keep the field name `target_hint`, not `code_anchor`, because the field remains a weak project hint, not a code-change decision.

Current high-intensity sandbox patch:

```text
kp_ref is useful and should stay in the candidate sidecar because it lets agents jump from Lens entry to candidate pattern/source chain.
conceptual target status is useful for workflow/module hints that cannot be file-checked yet.
```

## Source Card Boundary

Future source-card wording should use routing language only:

```text
transferable candidate points
source-bound constraints
project_routes_optional
```

`project_routes_optional` may say:

```text
may route to ...
possible fit area ...
not a project decision
```

It must not say:

```text
VAKS should adopt ...
VAKS should reject ...
```

## Candidate Pattern Bank Boundary

Candidate Pattern Bank should not copy every atomic knowledge point.

Only promote a candidate pattern when it has:

```text
recurring problem
clear mechanism
applicability boundary
non-goal / non-fit boundary
trade-off or risk
source anchors or repeated source-family pressure
```

Otherwise, the reusable unit remains the generic atomic knowledge point.

## v0.2.13 Relationship

Project Lens does not make v0.2.13 heavier.

Ordinary source intake, ordinary lens tags, and ordinary candidate patterns stay light.

v0.2.13 triggers only when a point is about to become:

```text
project decision
architecture absorption
action basis
risk-sensitive answer
significant promotion
```

At that point:

```text
Evidence is not enough; show the non-circular warrant.
```

## What Must Stay Sandbox-Only

```text
Project Lens tags
unreviewed Candidate Pattern entries
project route hints
reuse count / source count / project count
dashboard / feedback / retrieval / rerank signals
GraphRAG graph or summary
AI-generated adoption / rejection explanations
landed or boundary drafts without evidence-aware review
```

These are activation, diagnosis, and candidate-work signals. They are not truth confidence, support strength, reviewed knowledge, or action basis.

## Current Disposition

```yaml
direction: accept_direction
implementation_level: candidate-only
high_intensity_gauntlet: pass_after_patches
blocking_issue_remaining: none_found_in_current_sandbox
mainline_change_now: no
schema_change_now: no
template_change_now: no
formal_workspace_directory_now: no
sidecar_overlay_pilot: yes
v0_2_13_scoped_commit_impact: no
```
