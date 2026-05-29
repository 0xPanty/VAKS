---
type: claim
status: unverified
review_state: candidate
knowledge_state:
claim:
created:
topics:
related_projects:
sources:
supporting_sources:
conflicting_sources:
evidence:
  - source_id:
    source_range:
    quote_or_excerpt:
    evidence_support:
      span_supports_target:
      evidence_role:
      reviewer_note:
relations: []
evidence_level: unknown
verification_status: unverified
confidence:
impact:
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
evidence_sufficiency:
  state:
  checked_for:
  missing: []
  required_next_step:
  reviewer_note:
last_verified:
next_review:
tags:
---

# 主张 / 结论：

## 主张


## 为什么重要


## 支持证据

Claim drafts may leave `evidence_support` blank.
Fill it only when this evidence item is used for promotion support, reviewed relation, decision, or action basis.

```yaml
evidence:
  - source_id:
    source_range:
    quote_or_excerpt:
    evidence_support:
      span_supports_target: supported | partial | unsupported | unclear
      evidence_role: direct_support | inferential_support | background_context | counterexample
      reviewer_note:
```

规则：

- 只有 URL 的 source 只是 provenance，不是 support。
- `background_context` 不能计入 supported。
- `inferential_support` 必须写 `reviewer_note` 才能用于 promotion。
- `counterexample` 应进入反例 / 冲突证据。
- evidence support 不自动提高 confidence。

## Evidence Sufficiency Gate

只在这个 claim 要晋级、进入 action basis、支撑 decision 或作为强 relation evidence 时使用。
Claim drafts may omit `evidence_sufficiency` until promotion, decision, action basis, or strong relation use.

```yaml
evidence_sufficiency:
  state: sufficient | weak | insufficient | out_of_scope | risky
  checked_for: promotion | action_basis | decision | reviewed_relation | risk_sensitive_answer
  missing: []
  required_next_step: proceed | ask_user | retrieve_more | create_missing_point | narrow_scope | mark_not_actionable | needs_review
  reviewer_note:
```

边界：

- 普通候选 claim 不强制填。
- `insufficient` / `out_of_scope` 不能作为 ready action basis。
- `weak` 必须带 gaps。
- `risky` 必须反映到 `action_readiness`。

## 反例 / 冲突证据


## 支持-反对式 Review

完整面板只在 claim 晋级、进入 action basis / decision / context pack、支撑强 relation、被明确挑战、变 stale / contested，或 reviewer 要求 standing check 时展开。

- 为什么它现在还站得住：
- 已知最强反对：
- 反对严重度：fatal / major / minor / out_of_scope / unresolved
- 适用范围：
- 不适用范围：
- 已知风险：
- 什么时候需要复查：
- 当前行动可用性：ready / not_ready / risky / needs_review

边界：

- 有引用不等于有支持。
- derived_from 只是来源，不是 support。
- 支持变多不自动提高 confidence。

## 标签与量化

- evidence_level: primary / secondary / anecdotal / synthetic / unknown
- verification_status: unverified / single-source / cross-checked / field-tested / conflicted / deprecated / rejected
- confidence: 1-5
- impact: 1-5
- relevance: 1-5

## 关系边 / 关联强度

```yaml
relations:
  - target: "[[node-name]]"
    type: supports | contradicts | refines | risk_of | derived_from
    relation_state: candidate | reviewed | rejected | stale
    strength: 1-5
    confidence: low | medium | high
    evidence:
      - source_id: "[[source-or-claim]]"
        source_range:
        quote_or_excerpt:
        evidence_support:
          span_supports_target:
          evidence_role:
          reviewer_note:
    rationale: "One sentence explaining why this edge exists."
    created:
    last_verified:
```

## 验证方式


## 当前结论


## 复查计划
