---
type: pattern
status: draft
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - byarbrough/obsidian-para
related_concepts:
  - "[[MEMORY_TIER]]"
  - "[[DEV_CONTEXT]]"
related_projects:
  - verified-action-knowledge-system
adoption_status: adapt
verification_status: single-source
evidence_level: secondary
evidence_count: 1
confidence: medium
negative_evidence:
  - "PARA does not provide truth verification, review gates, or source provenance."
replaces:
superseded_by:
extension_points:
  - memory-tier
  - dev-context
  - query activation
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "Only one PARA template repo reviewed; needs comparison with more PARA/ACE/AI-context systems."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-obsidian-para-source]]"
    observation: "The repo organizes knowledge by Projects, Areas, Resources, and Archive, with placement based on likely next use."
    effect: supports
    confidence: medium
relations:
  - target: "[[MEMORY_TIER]]"
    type: refines
    strength: 5
    confidence: medium
    evidence:
      - "[[2026-05-27-obsidian-para-source]]"
    rationale: "Memory tier should use likely next action as activation reason rather than generic importance."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[DEV_CONTEXT]]"
    type: refines
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-obsidian-para-source]]"
    rationale: "Dev context core/support/cold selection can inherit PARA's actionability routing while adding a risk layer."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - pattern
  - memory-tier
  - actionability
  - context-engineering
---

# Actionability-Based Memory Routing

## AI-readable preamble

Route knowledge by where it is likely to be needed next, not only by topic or generic importance.

This pattern refines `memory_tier` and `dev context` selection.

It is an activation rule, not a truth rule.

## 一句话定义

资料的默认激活位置由“下一次最可能在哪里被使用”决定，而不是由主题、文件夹美观度或抽象重要性决定。

## 解决的问题

资料库越大，纯主题分类会导致两个问题：

```text
相关资料太多，回答时噪音高。
当前任务真正需要的资料不一定在最显眼的位置。
```

Actionability routing 让 agent 先问：

```text
What will this help us do next?
```

而不是只问：

```text
What topic does this belong to?
```

## 适用场景

- 为项目建立 `DEV_CONTEXT`。
- 给资料加 `memory_tier` / `activation_reason`。
- 在多个相关文件中选择 Core / Support / Cold References。
- 判断某条资料是否应该从 cold 重新激活。

## 不适用场景

- 判断 claim 是否为真。
- 判断 source 是否可靠。
- 替代 review gate。
- 替代 provenance 和 evidence。
- 决定是否发布或采纳某个 decision。

## 反例与避坑

- 失败条件：把“下一次会用到”误当成“已经验证”。
- 相似反模式：`[[para-folder-taxonomy-as-truth-layer]]`
- 复杂度风险：如果要求用户不断手动搬文件，会变成整理负担。
- 替代方案：用 metadata / context pack 记录 activation，而不是先重构文件夹。

## 来源证据

- `[[2026-05-27-obsidian-para-source]]`：PARA 模板强调 Projects / Areas / Resources / Archive 的行动性差异，并建议把资料放在下一次最可能使用的位置。

## 标签与量化

- domain: knowledge-activation
- problem: context-selection
- maturity: emerging
- complexity: low
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 1
- integration_fit: 5
- evidence_strength: 3
- reversibility: 5

## 交叉验证

- 相似来源：待比较更多 PARA / ACE / AI context engineering 系统。
- 历史项目影子：当前 `MEMORY_TIER.md` 已把 hot 定义为 scope 下的激活优先级。
- 支持证据：`DEV_CONTEXT.md` 已区分 Core / Support / Risk / Cold References。
- 反例：如果无 review gate，行动性 routing 可能把未验证资料推到前台。

## 最小实现方式

在节点或 context pack 中写：

```yaml
memory_tier: hot
scope_key: project-or-task
activation_reason: "Needed next because ..."
```

在 dev context pack 中写：

```text
Core:
  files needed for the next implementation step

Support:
  files useful when choices appear

Cold References:
  files kept for traceability
```

## 项目融合建议

采用为 `MEMORY_TIER.md` 的核心解释之一：

```text
hot is not important.
hot is likely-needed-next for a scope.
```

同时采用为 `DEV_CONTEXT.md` 的文件选择规则：

```text
Core requires near-term action use, not merely relevance.
```

## 可拓展性

- 可以通过什么接口/适配层接入：metadata、Obsidian Bases、query-run activation log、dev context builder。
- 未来可能被什么替代：更精细的 activation scoring，但仍应解释 `why needed next`。
- 替换或升级成本：低。
- 回退方式：忽略 activation metadata，回到 manual file selection。

## 验证指标

- dev context Core 文件数量减少但任务不漏关键约束。
- second query/run 比 first query/run 少召回无关资料。
- cold source 被打开时能说明具体 evidence/reuse reason。
- 用户纠偏“不是这个范围”的次数下降。
