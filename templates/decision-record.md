---
type: decision
status: draft
review_state: candidate
knowledge_state:
created:
decision:
related_projects:
based_on:
patterns:
outcome: pending
evidence_strength:
validation_status: pending
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
relations: []
migration_path:
rollback_path:
---

# 决策记录：

## 决策


## 背景


## 依据


## 支持-反对式 Review

- 为什么这个决策现在还站得住：
- 已知最强反对：
- 反对严重度：fatal / major / minor / out_of_scope / unresolved
- 适用条件：
- 不适用条件：
- 已知风险：
- 当前行动可用性：ready / not_ready / risky / needs_review
- 什么时候需要复查：

## 量化判断

- problem_fit:
- reuse_value:
- implementation_cost:
- integration_fit:
- evidence_strength:
- reversibility:

## 交叉验证

- 相似库/产品/论文：
- 历史项目证据：
- 支持证据：
- 反例或失败边界：

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

## 备选方案


## 可拓展性与迁移

- 是否绑定特定工具/库：
- 后续新方案如何接入：
- 迁移路径：
- 回退路径：

## 为什么这样选


## 风险


## 避坑与反模式

- 相关反模式：
- 不采用哪些做法：
- 失败边界：
- 回退方案：

## 验证方式


## 复盘
