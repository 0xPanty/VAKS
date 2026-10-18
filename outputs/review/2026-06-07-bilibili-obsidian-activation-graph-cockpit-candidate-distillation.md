---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from:
  - raw/videos/2026-06-07-bilibili-obsidian-activation-graph-cockpit-source.md
  - raw/videos/2026-06-07-bilibili-obsidian-activation-graph-cockpit-source/visual-observations.md
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint:
  - activation-cockpit
  - point-collision-visualization
  - review-queue-ux
  - project-overlay-reference
  - graph-is-activation-not-truth
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - source_ref: raw/videos/2026-06-07-bilibili-obsidian-activation-graph-cockpit-source.md
    selector_type: public_metadata
    selector_value: "BV1DcEc6KEpw title/author/published_at/duration"
  - source_ref: raw/videos/2026-06-07-bilibili-obsidian-activation-graph-cockpit-source/visual-observations.md
    selector_type: visual_observation
    selector_value: "left sidebar taxonomy and Obsidian Graph View growth"
reference_layer_tag: ref/activation-graph-cockpit
reference_layer_label_zh: 图谱碰撞驾驶舱
reference_layer_scope: "visual/operator/activation reference layer only"
borrow_value: medium
borrow_order:
  - "P1-UX: graph cockpit for seeing candidate collisions, conflicts, limited rules, generalized rules, and review_due pressure."
  - "P2-core: folder/status taxonomy as a lifecycle hint for candidate -> conflict/limited -> generalized/review routing."
  - "P3: graph animation and node-color aesthetics as presentation inspiration only."
avoid:
  - "Do not treat graph edges as reviewed relations."
  - "Do not treat node color, size, centrality, or link count as truth confidence, support, or action readiness."
  - "Do not copy the paper-writing vault structure as VAKS schema."
  - "Do not treat the title's GPT5.5 wording as verified product evidence."
dev_context_hint:
  default_layer: support
  core_only_when: "Designing VAKS cockpit/dashboard/operator surface for activation, review queue, point collision, or project overlay navigation."
  support_when: "Discussing how to make candidate collision, review_due, conflict, limited-rule, or generalized-rule status visible."
  risk_when: "Any graph, dashboard, node color, similarity, rank, or edge starts being used as support, confidence, reviewed relation, or action basis."
  cold_references:
    - raw/videos/2026-06-07-bilibili-obsidian-activation-graph-cockpit-source.md
    - raw/videos/2026-06-07-bilibili-obsidian-activation-graph-cockpit-source/visual-observations.md
tags:
  - candidate
  - provisional
  - visual-only
  - bilibili
  - obsidian-graph
  - activation-graph-cockpit
  - point-collision-visualization
  - graph-is-activation-not-truth
  - candidate-only
---

# Candidate Distillation: Obsidian Activation Graph Cockpit

## Boundary

This note is provisional orientation.

It distills a visual-only Bilibili demo into a VAKS reference-layer tag. It is
not reviewed knowledge, not a decision, not a formal pattern, and not action
basis.

## 一句话

这个视频值得记，但不是因为它提供了新架构。

它值得记的是一个参考层标签：

```text
ref/activation-graph-cockpit
```

中文名：

```text
图谱碰撞驾驶舱
```

意思是：

```text
用图谱/看板展示候选知识如何互相碰撞、冲突、受限、泛化、复查和迭代。
```

## 为什么不是主架构新东西

VAKS 已经有核心逻辑：

```text
source
-> candidate point
-> calibration / point collision
-> evidence-aware review
-> reviewed node / relation
-> context pack / action basis
-> use ledger / feedback
```

这条视频没有挑战这条主路。它补的是可视化和操作员体验：

```text
让人一眼看见哪些知识正在碰撞、哪些冲突突出、哪些只能局部使用、哪些可能已经泛化成规则。
```

## Candidate Points

### 1. `activation_graph_cockpit`

候选结论：

```text
VAKS 可以有一个图谱/看板驾驶舱，用于显示候选知识和已审知识周边的激活状态。
```

适用范围：

- review queue scanning
- point collision triage
- project overlay navigation
- activation/context-pack preparation
- conflict / limited / generalized rule visibility

边界：

```text
cockpit 只能帮助看见和召回，不能判断真伪。
```

### 2. `visual_collision_surface`

候选结论：

```text
冲突、受限、泛化、复查压力这些状态应该被视觉化，而不是藏在长文档里。
```

可能的 VAKS 视觉编码：

```text
green: candidate / ordinary activation
yellow: review_due / needs attention
red: conflict / blocked / high-risk
grey: cold reference / weak signal
large node: hub/index/high-activation item
edge: candidate relation or reviewed relation, but must be visually distinguished
```

注意：这只是 UX 候选，不是 schema。

### 3. `graph_is_activation_not_truth`

候选结论：

```text
图谱结果属于 activation 和 orientation，不属于 truth。
```

在 VAKS 中必须钉死：

- edge is not reviewed relation unless promoted elsewhere
- centrality is not confidence
- color is not evidence
- cluster is not source independence
- graph animation is not self-learning proof

### 4. `folder_taxonomy_as_status_hint`

候选结论：

```text
目录/分区可以提示知识生命周期，但不能直接变成 VAKS schema。
```

这个视频里的 `Conflicts`、`Limited_Rules`、`Final_Generalized_Rules`、`Workflow_Governance` 对 VAKS 有启发，因为它们对应：

```text
conflict candidate
scope-limited candidate
reviewed or generalized rule candidate
workflow governance / operator convention
```

但它们必须通过 VAKS 自己的 review gate 才能进入正式层。

## 参考层标签设计

Canonical tag:

```yaml
reference_layer_tag: ref/activation-graph-cockpit
label_zh: 图谱碰撞驾驶舱
tag_scope: reference_layer
default_retrieval: false
retrieval_policy: activation_only
truth_boundary: graph_is_activation_not_truth
borrow_level: P1-UX / P2-core
```

建议别名：

```text
activation-graph-cockpit
point-collision-visualization
visual-collision-surface
graph-is-activation-not-truth
```

使用时机：

```text
当一个来源启发“把知识碰撞/冲突/复查/泛化做成可视化工作台”时使用。
```

不用在：

```text
普通 source card
正式 reviewed knowledge
证据支持字段
decision/action basis
```

## Borrow Gradient

```yaml
borrow_value: medium
borrow_order:
  P1-UX:
    - graph cockpit for candidate collision and review pressure
    - visible conflict / limited / generalized rule lanes
  P2-core:
    - folder/status taxonomy as lifecycle hint
    - project overlay and review queue navigation hints
  P3:
    - graph animation / node aesthetics / presentation style
avoid:
  - graph as truth
  - node color as evidence
  - edge as reviewed relation
  - exact paper-writing folder schema
  - GPT5.5 title wording as verified fact
```

## Project Fit

For VAKS, this is:

```text
P1-UX: worth remembering for dashboard/cockpit design.
P2-core: only if we later formalize how candidate/review/conflict states appear visually.
```

It is not:

```text
P1 architecture change
reviewed pattern
implementation requirement
automation permission
truth-layer material
```

## Open Questions

- What exact mechanism produced the graph: manual Obsidian links, plugin, script, or AI writeback?
- What do red/yellow/green/grey nodes mean in the author's system?
- Is there a matching repository or article that explains the color/status mapping?
- If VAKS builds this, should the cockpit be Obsidian-native Graph View, Bases-style dashboard, static HTML, or repo-generated report?

## Routing Hint

Route to:

```text
Activation / Context Pack UX
Review Queue cockpit
Point Collision visualization
Project Overlay navigation
Graph-is-activation-not-truth guardrail
```

Do not route to:

```text
truth confidence
reviewed relation creation
source independence proof
action basis
```
