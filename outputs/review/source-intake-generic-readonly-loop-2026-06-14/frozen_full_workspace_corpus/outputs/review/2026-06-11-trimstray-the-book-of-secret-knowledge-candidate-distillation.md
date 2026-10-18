---
type: candidate_distillation
record_kind: candidate_distillation
status: draft
provisional: true
title: "The Book of Secret Knowledge 是人工策展索引，不是知识真理层"
created_at: "2026-06-11"
created_by: Codex
processing_tier: medium
knowledge_status: candidate
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
derived_from:
  - raw/repos/2026-06-11-trimstray-the-book-of-secret-knowledge-source.md
projects:
  - verified-action-knowledge-system
topics:
  - curated-index
  - reference-catalog
  - link-hygiene
  - retrieval-workbench
  - source-intake
  - shell-one-liners
  - security-tooling
borrow_value: medium
borrow_order: P2
evidence_strength: low-medium
routing_hint:
  - retrieval-layer-workbench
  - source-ingest
  - link-health
  - tool-catalog-sandbox
possible_project_refs:
  - outputs/review/vaks-retrieval-layer-design-2026-06-11/
tags:
  - candidate-only
  - source-distillation
  - design-only
  - vaks-borrow-P2
---

# 候选蒸馏：The Book of Secret Knowledge 是人工策展索引，不是知识真理层

## 说人话

这个库本质上不是“书”，也不是程序库；它是一份很大的技术资源清单。

它像一个老练工程师的收藏夹：

```text
工具
手册
教程
安全资源
cheatsheet
shell one-liners
博客和信息源
```

它对 VAKS 的价值不是让我们照搬里面的链接，而是提醒我们：

```text
资料库需要“发现入口”和“策展目录”，
但策展目录不能冒充审查后的知识。
```

## Borrow Tag

```yaml
borrow_value: medium
borrow_order: P2
borrow_scope:
  - curated-reference-index
  - retrieval-scaffolding
  - external-tool-catalog
  - link-health-check
  - source-freshness-monitor
  - command-risk-gating
not_borrow_scope:
  - reviewed truth
  - action basis
  - evidence support
  - reviewed relations
  - automatic tool endorsement
```

## Candidate Point

VAKS 可以吸收它的“策展索引”模式：

```text
外部资源很多时，
不要一开始就全部 review。

先做:
  category
  short description
  source URL
  status / broken marker
  topic routing
  review pressure
  action risk warning
```

然后把它们作为检索层的候选入口，而不是 reviewed knowledge。

## 应该吸收

- **目录先行**：大规模外部资源先通过 TOC / category / subsection 让人找得到。
- **人工筛选**：不是“收集一切”，而是明确 good quality stuff 的策展意图。
- **链接健康意识**：临时不可用链接不要立刻删除，确认永久过期后再处理。
- **RSS/Atom 更新流**：把上游变化作为 source freshness 输入。
- **贡献规则**：要求解释问题和解决方案，避免随手堆链接。
- **命令风险隔离**：one-liners 很有用，但默认只能作为参考，不能直接行动。

## 不应该吸收

- 不要把 awesome-list 热度当权威。
- 不要把 TOC 当知识本体。
- 不要把链接描述当证据支持。
- 不要把 shell one-liner 直接给 agent 执行。
- 不要把安全工具目录直接变成推荐清单。
- 不要让单 README 巨型清单成为 VAKS 的主结构。

## 对 VAKS 的具体启发

### 1. Curated Index 是一种候选层

VAKS 可以有：

```text
curated_reference_index:
  title
  url
  category
  short_description
  source_status
  last_seen
  broken_marker
  risk_flag
  review_pressure
```

但它必须默认：

```yaml
knowledge_status: candidate
action_basis_allowed: false
truth_mutation_allowed: false
```

### 2. Retrieval 需要区分“发现”和“支持”

这个库适合回答：

```text
有什么工具/资料可以查？
这个领域有哪些入口？
哪里能找到 cheatsheet？
```

不适合直接回答：

```text
这个命令在我机器上能不能执行？
这个安全工具是不是安全？
这个建议是否适合当前行动？
```

### 3. One-liners 要进 Risk Gate

shell one-liners 对 VAKS 是高风险材料。未来如果检索层召回这类内容，应显示：

```text
command_candidate_only
requires_environment_check
requires_dry_run
requires_rollback_plan
not_action_basis
```

## 与 VAKS 层级的关系

```text
Capture:
  适合作为外部资源目录来源。

Understand:
  可以抽 category、description、风险标签、适用场景。

Review:
  每个具体工具/命令/建议需要单独 review；总目录不能替代审查。

Connect:
  可以生成 candidate relation，例如 topic -> resource；不能生成 reviewed relation。

Activation / Context Pack:
  很适合做 context pack 的 discover/reference section。

Decision / Action:
  不允许直接作为行动依据，尤其是命令和安全工具。

Use Ledger / Feedback:
  使用某个资源后的成功/失败可以进入 feedback，形成后续 review pressure。
```

## Risk / Inhibition

```text
risk:
  链接漂移和过期。
  工具停更或被替代。
  命令在不同系统上危险。
  安全/渗透测试资源被误用。
  大清单让人以为“多就是完整”。
  GitHub stars 被误解为可信度。

inhibition:
  每个链接只作为 source candidate。
  命令类内容默认加 action-risk badge。
  link health 是 source hygiene，不改变 truth。
  热度是 discovery signal，不是 review signal。
  具体行动必须进入 sufficiency / environment / rollback gate。
```

## 融合判断

```text
fusion_decision: adapt
borrow_value: medium
borrow_order: P2
evidence_strength: low-medium
implementation_cost: medium
integration_fit: medium
reversibility: high
```

## 后续行动

- 放入 VAKS 检索层 / source ingest / link-health 参考池。
- 当前不建议改 `SCHEMA.md`。
- 如果要做外部工具目录，可以先在 sandbox 建 curated index manifest，而不是写入 reviewed wiki。
