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
supersedes:
superseded_by:
supersession_reason:
affected_claims_review_due: []
affected_patterns_review_due: []
affected_relations_review_due: []
affected_context_packs_review_due: []
verbatim_input:
model_interpretation:
intent_confirmation:
  required:
  restated_intent:
  assumptions: []
  scope_in: []
  scope_out: []
  success_criteria: []
  verification_plan:
  user_confirmed:
backbrief:
  plan_summary:
  acceptance_criteria_interpretation:
  numbered_assumptions: []
  risks: []
  verification_method:
decision_outcome:
  recommendation:
  confidence_at_decision:
  user_choice:
  outcome: succeeded | failed | mixed | unresolved
  outcome_note:
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
relations: []
migration_path:
rollback_path:
---

# 决策记录：

## 决策


## 背景


## Intent Confirmation / Backbrief

- 用户原话：
- 模型理解：
- 复述的意图：
- 假设：
- 范围内：
- 范围外：
- 成功标准：
- 验证方式：
- 是否已确认：

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

## Temporal Applicability Check

- 决策从什么时候开始有效：
- 是否有失效时间或重审时间：
- 替代了哪些旧决策：
- 被什么新决策替代：
- 适用 project / version / environment / timeframe / conditions：
- 当前 check_state：in_scope / out_of_scope / stale / superseded / unknown / needs_review

## Decision Superseding

- 被本决策替代的旧决策：
- 替代本决策的新决策：
- 替代原因：
- 替代适用范围：
- 受影响并需要 review_due 的 claim / pattern / relation / context pack：
- 审计备注：

## Decision Outcome Calibration

- 当时推荐：
- 当时 confidence：
- 用户选择：
- explicit user override：
- override rationale：
- 后来结果：succeeded / failed / mixed / unresolved
- 结果说明：
- outcome precondition：
  - recommendation_recorded
  - confidence_at_decision_recorded
  - user_choice_or_explicit_override_recorded
  - outcome_note_recorded
- 对 future recommendation / risk_calibration / scope_fit / option_framing 的影响：
- 不直接影响 truth_confidence / verification_status / source_reliability：
- 不直接影响 review_verdict / reviewed_relation / action_basis_readiness：
- 不吸收 RKA runtime / MCP / API server / dashboard / SQLite：

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
