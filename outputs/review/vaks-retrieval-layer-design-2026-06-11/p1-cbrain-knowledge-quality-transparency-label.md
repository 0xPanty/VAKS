---
type: candidate_point
record_kind: candidate_design_point
status: candidate
title: "P1: cBrain-style knowledge quality transparency label for VAKS"
created_at: "2026-06-11"
created_by: Codex
project_id: VAKS
knowledge_status: candidate
processing_tier: medium
overlay_state: retrieval_layer_workspace
truth_status: not_reviewed
source_refs:
  - "user-provided cBrain/Kimi quality label excerpt, 2026-06-11"
  - "outputs/review/vaks-retrieval-layer-design-2026-06-11/cbrain-official-mindmap-2026-06-11/candidate-distillation.md"
  - "outputs/review/vaks-retrieval-layer-design-2026-06-11/cbrain-official-mindmap-2026-06-11/offline-package-blackbox-notes.md"
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_quality_label_not_reviewed
action_basis_allowed: false
truth_mutation_allowed: false
promotion_gate: retrieval_workbench_design_review_required
borrow_value: strong
borrow_order: P1_for_retrieval_workbench_quality_transparency
target_layers:
  - retrieval-workbench
  - anchor-queue
  - context-pack-preparation
  - personal-model-transparency
  - candidate-review-routing
non_target_layers:
  - reviewed-truth
  - evidence-support
  - confidence-update
  - action-basis
tags:
  - candidate-only
  - p1-knowledge-point
  - cbrain
  - retrieval-workbench
  - quality-transparency
  - personal-model
  - boundary/not-action-basis
---

# P1 候选知识点：知识质检透明标签

## 说人话

cBrain 这条逻辑值得进 VAKS 的 P1 知识点，但不是作为“可信度算法”进入。

它最有价值的是：

```text
把一条知识能不能信、能用在哪、不能用在哪、有什么风险，
用一块普通人看得懂的标签说清楚。
```

这对 VAKS 很重要，因为 VAKS 不能只在后台有 `confidence`、`evidence_level`、`scope` 这些字段；用户和 agent 在检索时也要一眼看懂：

```text
这条是个人模型，还是学术结论？
证据来自实践，还是论文？
适用范围是什么？
最大风险是什么？
能不能拿来行动？
```

## 归属开发区

主落点：

```text
outputs/review/vaks-retrieval-layer-design-2026-06-11/
```

原因：

```text
它首先影响的是检索工作台和结果卡片：
query result -> anchor card -> quality transparency label -> allowed use
```

后续如果主线化，再考虑拆到：

```text
templates/candidate-distillation.md
templates/context-pack.md
SCHEMA.md
REVIEW_QUEUE.md
```

现在不改主线 schema。

## cBrain 标签的大意

用户提供的 cBrain/Kimi 示例包含这些层：

```text
严谨性要求程度
来源等级
可信等级
共识等级
适用条件
不适用条件
证据类型
风险检查
前代模型
后代模型
审核意见
最后验证
质检员
```

这不是学术 peer review。它更像个人知识体系里的：

```text
透明式严谨
```

即明确告诉读者：

```text
这是什么性质的知识？
它从哪里来？
它能用到哪里？
它有什么风险？
它最后什么时候被检查过？
```

## VAKS 已有对应项

VAKS 已经有更严格的后台字段：

| cBrain 标签 | VAKS 已有对应 |
|---|---|
| 严谨性要求程度 | `processing_tier` / lazy gates |
| 来源等级 | source record / source integrity / source access |
| 可信等级 | `verification_status` / `evidence_level` / `confidence` |
| 共识等级 | support/challenge/cross-source review，尚无轻量单字段 |
| 适用条件 | `scope_in` / `scope_limits` / `temporal_applicability` |
| 不适用条件 | `scope_out` / `out_of_scope` |
| 证据类型 | evidence item / evidence support / evidence granularity |
| 风险检查 | `risk_flags` / `risk_refs` / challenge review |
| 前代模型 | `derived_from` / refines / superseded |
| 后代模型 | replacement / supersedes / downstream refs |
| 审核意见 | review note / reviewer rationale |
| 最后验证 | `last_verified` / `reviewed_at` |
| 质检员 | `reviewed_by` / `captured_by` / model agent |

差异是：

```text
VAKS 有字段，但不一定有一块好读的标签。
cBrain 有好读标签，但不能替代 evidence review。
```

## P1 借鉴点

### 1. 给 personal model 一个透明标签

很多个人体系、方法论、纲领不是论文结论，也不是严格事实 claim。

VAKS 可以加一类显示层：

```yaml
transparency_label:
  rigor_need: medium
  source_grade: S3_general
  trust_grade: C3_practice_based
  consensus_grade: K1_personal_or_niche
  applies_to:
    - personal knowledge management
    - cross-disciplinary learning
  not_for:
    - academic proof
    - precise prediction
  evidence_types:
    - personal practice
    - historical induction
    - philosophical reasoning
  risk_checks:
    macro_theory: medium
    closed_loop: medium
    over_abstraction: low
    authority_bias: low
  review_note: "透明式严谨：标注为个人模型，非学术体系。"
```

这是检索/阅读展示层，不是 truth 层。

### 2. 让检索结果先暴露“能不能用”

VAKS 检索结果卡可以显示：

```text
status: candidate / reviewed / personal_model
allowed_use: orientation_only / review_input / reviewed_support
confidence_cap: low / medium / high
scope_in / scope_out
risk_flags
last_checked
```

这样用户不会把“搜到了”误读成“可信”。

### 3. 给非学术知识一个合适严谨度

VAKS 不应该把所有知识都逼成论文式证据。

更好的规则是：

```text
学术 claim -> 证据严格
工程 decision -> 风险/回滚严格
个人模型 -> 透明边界严格
普通灵感 -> 来源和候选状态清楚即可
```

cBrain 这块标签正好补“个人模型透明边界”。

### 4. 共识等级值得保留，但不能自动算 truth

`K1 小众` 这类标签很有用，因为它提醒读者：

```text
这是个人独创或小众模型，不是广泛共识。
```

VAKS 可以保留为：

```yaml
consensus_hint: personal | niche | emerging | common | mainstream
```

但边界是：

```text
共识高不等于真。
共识低不等于错。
它只影响阅读姿态和 review route。
```

## 不要借

```text
不要把 S3/C3/K1 变成自动可信分数。
不要让质检标签替代 evidence support。
不要让“透明式严谨”进入 action basis。
不要把个人体系纲领包装成 reviewed claim。
不要让模型自己给自己盖章后自动晋级。
```

## VAKS 融合建议

候选字段名：

```yaml
transparency_label:
  label_kind: personal_model | method_note | field_claim | decision_note
  rigor_need: low | medium | high
  source_grade:
  trust_grade:
  consensus_hint:
  applies_to: []
  not_for: []
  evidence_types: []
  risk_checks: {}
  reviewer_note:
  last_checked:
  checked_by:
```

检索层显示方式：

```text
anchor card
-> title / source / status
-> transparency label
-> allowed use
-> risks / out-of-scope
-> open source / open review / build context pack
```

## P1 判断

```yaml
p1_reason: "It makes VAKS boundaries visible at retrieval time, especially for personal models and method notes."
borrow_value: strong
borrow_order: P1_for_retrieval_workbench_quality_transparency
mainline_change_now: no
pilot_needed: yes
best_next_test:
  - apply this label to 3 candidate notes
  - apply this label to 1 reviewed claim
  - apply this label to 1 context-pack card
  - check whether users can distinguish personal model vs reviewed support
```

## 边界

```text
quality transparency label = user-facing explanation layer
not truth confidence
not evidence support
not reviewed relation
not action readiness
```
