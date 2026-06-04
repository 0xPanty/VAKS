---
type: anti_pattern
status: draft
review_state: candidate
knowledge_state:
created:
domain:
failure_mode:
severity:
likelihood:
complexity_cost:
cross_validated_with:
related_projects:
replacement:
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
relations: []
decision: avoid
---

# 反模式 / 踩坑：

## 问题描述


## 为什么不可行


## 失败条件


## 支持-反对式 Review

- 为什么这个反模式现在还站得住：
- 已知最强反对：
- 反对严重度：fatal / major / minor / out_of_scope / unresolved
- 适用条件：
- 不适用条件：
- 已知风险：
- 什么时候需要复查：
- 当前行动可用性：ready / not_ready / risky / needs_review

## Temporal Applicability Check

- 这个风险/反模式从什么时候开始适用：
- 是否已被新版本、环境或替代方案缓解：
- 适用 project / version / environment / timeframe / conditions：
- 当前 check_state：in_scope / out_of_scope / stale / superseded / unknown / needs_review

## 标签与量化

- domain:
- failure_mode:
- severity: 1-5
- likelihood: 1-5
- complexity_cost: 1-5
- evidence_strength: 1-5
- reversibility: 1-5

## 交叉验证

- 相似失败来源：
- 历史项目证据：
- 支持证据：
- 是否可能只是局部失败：

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

## 应该避开什么


## 替代方案


## 后续是否需要复测
