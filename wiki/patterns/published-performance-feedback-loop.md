---
type: pattern
status: draft
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - "[[2026-05-27-jarvis-obsidian-claude-code-source]]"
sources:
  - "[[2026-05-27-jarvis-content-vault-review]]"
related_concepts:
  - "[[source-to-publish-content-pipeline]]"
  - "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
related_projects:
  - verified-action-knowledge-system
adoption_status: adopt
verification_status: single-source
evidence_level: anecdotal
evidence_count: 1
confidence: medium
negative_evidence:
  - "Performance metrics can overfit to platform dynamics and do not prove truth."
  - "Vanity metrics can mislead if not tied to the intended action or learning goal."
replaces:
superseded_by:
extension_points:
  - feedback adapters
  - output adapters
  - context pack modes
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "Only one article source currently supports this exact workflow."
  - "No local field test in this vault yet."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-jarvis-content-vault-review]]"
    observation: "The article archives published content with metrics and runs a monthly analysis over outcomes."
    effect: supports
    confidence: medium
relations:
  - target: "[[source-to-publish-content-pipeline]]"
    type: refines
    strength: 4
    confidence: medium
    evidence:
      - "[[published-performance-feedback-loop]]"
    rationale: "The pattern adds measured post-publication feedback to a source-to-publish pipeline."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
    type: supports
    strength: 4
    confidence: medium
    evidence:
      - "[[published-performance-feedback-loop]]"
    rationale: "Measured outcome feedback is one way to update future action guidance without rewriting truth silently."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - pattern/feedback
  - pattern/content-pipeline
  - action-feedback
---

# Published Performance Feedback Loop

## AI-readable preamble

This pattern turns shipped outputs into measured feedback.

It does not make metrics equal truth. It records outcomes so future action recommendations can learn from what happened.

Current status: useful feedback adapter candidate, not a core schema change.

## 一句话定义

把已经发布或执行过的成果连同结果数据一起归档，再定期复盘，让系统从行动结果中学习。

## 解决的问题

很多知识系统只记录输入，不记录输出后的结果。

这样系统永远知道“我看过什么”，但不知道“我做了什么、效果怎样、下次该怎么调整”。

## 适用场景

- 内容发布后记录表现。
- Agent 执行动作后记录成功/失败。
- 决策落地后记录指标变化。
- 产品、营销、实验、工作流优化的复盘。

## 不适用场景

- 没有明确输出的纯资料阅读。
- 指标很容易被平台随机波动污染的短期判断。
- 高风险决策不能只看单次结果。
- 需要事实验证的 claim，不能用表现数据替代证据。

## 最小记录字段

```yaml
output:
published_at:
source_nodes:
action_taken:
metrics:
  impressions:
  bookmarks:
  engagement_rate:
  conversion:
qualitative_feedback:
what_worked:
what_failed:
next_bet:
confidence_change:
related_decisions:
```

## 反例与避坑

- 失败条件：把流量好当成观点正确。
- 相似反模式：用 vanity metrics 替代 evidence。
- 复杂度风险：为了记录数据创建重型 analytics 系统。
- 替代方案：先手动记录少量关键结果，再做自动采集。

## 来源证据

- JARVIS article 建议把 published 内容和 impressions、bookmarks、engagement、top comment、what_worked 放在一起。
- 本资料库架构已有 feedback timeline 和 action basis 目标。

## 最小实现方式

先不做自动抓取。

```text
products/ 或 outputs/
-> 手动记录 action result
-> monthly review
-> 产生 action feedback candidate
-> Codex/user review 后更新 decision / gaps / confidence
```

## 项目融合建议

作为 `IMPLEMENTATION_BLUEPRINT.md` 的 feedback adapter 候选。

优先级低于：

```text
REVIEW_QUEUE.md
CONTEXT_PACK.md
LINT_RULES.md
```

但高于重型 analytics / dashboard。

## 验证指标

- 是否能把行动结果反向连接到 decision。
- 是否能降低重复犯错。
- 是否能识别哪些建议真的有效。
- 是否明确区分 performance signal 和 truth evidence。
