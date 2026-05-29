---
type: pattern
status: draft
review_state: candidate
knowledge_state:
created:
source_libraries:
related_concepts:
related_projects:
adoption_status: watch
tags:
evidence_count:
confidence: medium
negative_evidence:
attack_assessment:
  severity:
  reason:
  affected_scope:
  requires_review_due:
qualification:
  applies_when:
  does_not_apply_when:
  version_scope:
  project_scope:
  domain_scope:
  time_scope:
  environment_scope:
  assumptions:
temporal_applicability:
  valid_from:
  valid_until:
  supersedes:
  superseded_by:
  invalidated_by:
  applies_to:
    project:
    version:
    environment:
    timeframe:
    conditions:
  check_state:
  reviewer_note:
review_summary:
  why_it_still_holds:
  strongest_challenge:
  scope_limits:
  known_risks:
  review_due_when:
action_readiness:
  state:
  reason:
replaces:
superseded_by:
relations: []
extension_points:
---

# 设计模式：

## 一句话定义


## 解决的问题


## 适用场景


## 不适用场景


## 时间 / 版本 / Scope 适用性

- 何时开始适用：
- 何时失效或需要重审：
- 替代了什么：
- 被什么替代：
- 适用项目 / 版本 / 环境 / 时间段：
- 当前 check_state：in_scope / out_of_scope / stale / superseded / unknown / needs_review

## 反例与避坑

- 失败条件：
- 相似反模式：
- 复杂度风险：
- 替代方案：

## 支持-反对式 Review

- 为什么这个 pattern 现在还站得住：
- 已知最强反对：
- 反对严重度：fatal / major / minor / out_of_scope / unresolved
- 适用条件：
- 不适用条件：
- 已知风险：
- 什么时候需要复查：
- 当前行动可用性：ready / not_ready / risky / needs_review

## 来源证据


## 标签与量化

- domain:
- problem:
- maturity: experimental / emerging / proven
- complexity: low / medium / high
- problem_fit: 1-5
- reuse_value: 1-5
- implementation_cost: 1-5
- integration_fit: 1-5
- evidence_strength: 1-5
- reversibility: 1-5

## 交叉验证

- 相似来源：
- 历史项目影子：
- 支持证据：
- 反例：

## 关系边 / 关联强度

```yaml
relations:
  - target: "[[node-name]]"
    type: supports | contradicts | refines | risk_of | derived_from
    relation_state: candidate | reviewed | rejected | stale
    strength: 1-5
    confidence: low | medium | high
    evidence:
      - "[[source-or-claim]]"
    rationale: "One sentence explaining why this edge exists."
    created:
    last_verified:
```

## 最小实现方式


## 项目融合建议


## 可拓展性

- 可以通过什么接口/适配层接入：
- 未来可能被什么替代：
- 替换或升级成本：
- 回退方式：

## 验证指标
