---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: verified-action-knowledge-system
target_ref: outputs/review/2026-06-07-bilibili-obsidian-activation-graph-cockpit-candidate-distillation.md
target_selector: "ref/activation-graph-cockpit"
target_hint: "VAKS visual/operator reference for activation, point collision, review queue, and project overlay cockpit."
reference_layer_tag: ref/activation-graph-cockpit
reference_layer_label_zh: 图谱碰撞驾驶舱
tagging_decision: tagged
tag_level: reference-layer-p1-ux
tag_level_reason: "High-value UX/operator reference for making candidate collision and review pressure visible; not a new core architecture mechanism."
project_borrow_scope:
  - "Use as a reference-layer tag for visualizing candidate collision, conflict, limited-rule, generalized-rule, and review_due states."
  - "Borrow the idea of a graph cockpit for review queue and activation/context-pack navigation."
  - "Borrow folder/status taxonomy only as a visual lifecycle hint."
  - "Use the tag when evaluating future Obsidian Graph, Bases, static HTML, or cockpit/dashboard designs."
project_non_borrow_scope:
  - "For VAKS, do not treat graph edge, node size, color, centrality, cluster, or animation as reviewed relation, truth confidence, evidence support, source independence, or action readiness."
  - "For VAKS, do not copy the paper-writing vault folder schema into mainline docs or schema."
  - "For VAKS, do not treat this no-subtitle visual demo as a reproducible workflow or complete author method."
  - "For VAKS, do not treat `GPT5.5` title wording as verified product evidence."
project_reopen_trigger:
  - "Reopen when VAKS designs a review queue cockpit, activation dashboard, Obsidian/Bases view, or static graph report."
  - "Reopen when visual graph outputs are proposed as support, confidence, or reviewed relations."
  - "Reopen if a later repository/article from the author explains the graph generation and color/status mapping."
confirmation_basis:
  - "User explicitly asked to record this and design a reference-layer tag."
  - "Public Bilibili metadata captured without cookies."
  - "Public subtitle list was empty; interpretation is visual-only."
  - "Video was inspected through keyframes and visual observations, not a transcript."
last_checked_at: 2026-06-07
expires_at: 2026-07-07
borrow_value: medium
borrow_order:
  - "P1-UX: graph cockpit for candidate collision, conflict, limited-rule, generalized-rule, and review_due visibility."
  - "P2-core: lifecycle/status taxonomy can inform future cockpit state design if reviewed later."
  - "P3: graph animation and node aesthetics as presentation inspiration only."
avoid:
  - "graph edge as reviewed relation"
  - "node color/size/centrality as truth confidence"
  - "cluster as source independence"
  - "paper-writing folder schema as VAKS schema"
  - "GPT5.5 title wording as verified fact"
tags:
  - VAKS
  - project-overlay
  - reference-layer
  - activation-graph-cockpit
  - point-collision-visualization
  - graph-is-activation-not-truth
  - P1-UX
  - P2-core
  - candidate-only
---

# VAKS Project Overlay: Activation Graph Cockpit

## Boundary

This is a project-scoped reference sidecar.

It does not rewrite the source card, candidate distillation, reviewed note,
decision, or pattern. It can guide the active project, but it cannot act as
reviewed knowledge or action basis.

## 参考层标签

Canonical:

```text
ref/activation-graph-cockpit
```

中文：

```text
图谱碰撞驾驶舱
```

一句话：

```text
用图谱/看板展示候选知识如何互相碰撞、冲突、受限、泛化、复查和迭代。
```

## 标签等级

```yaml
tagging_decision: tagged
tag_level: reference-layer-p1-ux
borrow_value: medium
borrow_order_primary: P1-UX
secondary_core_value: P2-core
```

人话：

```text
给标签。
它是 P1-UX，不是 P1 主架构。
核心逻辑我们已有；它补的是看见和操作。
```

## Project Borrow Scope

VAKS 当前可以借：

1. **图谱驾驶舱**：让候选点、冲突点、受限规则、泛化规则、review_due 显眼。
2. **状态可视化**：用颜色、大小、分区、聚类提示操作优先级。
3. **Point Collision 入口**：让“哪些点正在互相碰撞”更容易被看见。
4. **Review Queue 入口**：让复查压力不埋在长文档里。
5. **Project Overlay 导航**：把项目借鉴/不借鉴边界也做成可导航视图。

## Project Non-Borrow Scope

VAKS 当前不要借：

- 不要把图谱边当 reviewed relation。
- 不要把节点颜色、大小、中心性当 truth confidence。
- 不要把聚类当 source independence。
- 不要把动画当 self-learning 证明。
- 不要照搬论文写作 vault 的目录结构。
- 不要把 `GPT5.5` 标题当产品事实。

## Reopen Trigger

重新打开这条 overlay 的条件：

- VAKS 要做 review queue cockpit。
- VAKS 要做 Activation Tier / Context Pack dashboard。
- VAKS 要做 Point Collision visualization。
- VAKS 要做 Obsidian Graph / Bases / static HTML 视图。
- 有人开始把图谱结果当证据、confidence、reviewed relation 或 action basis。
- 找到作者解释图谱生成、颜色状态、自动化方式的仓库/文章。

## Confirmation

```yaml
confirmation_basis:
  - user_requested_record: true
  - user_requested_reference_layer_tag: true
  - source_ref: raw/videos/2026-06-07-bilibili-obsidian-activation-graph-cockpit-source.md
  - candidate_ref: outputs/review/2026-06-07-bilibili-obsidian-activation-graph-cockpit-candidate-distillation.md
  - transcript_method: none
  - visual_only: true
  - runtime_executed: false
last_checked_at: 2026-06-07
expires_at: 2026-07-07
```

## 人话结论

这条不是来教 VAKS 新的“真理系统”。

它提醒我们：

```text
VAKS 以后不能只在文档里说候选点会碰撞、冲突会触发复查、受限规则不能泛化。
这些东西最好能被看见。
```

所以标签就定为：

```text
ref/activation-graph-cockpit
```

以后凡是提到“把知识碰撞/复查压力/受限规则/泛化路径可视化”的参考，都可以先挂这个参考层标签。

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
```
