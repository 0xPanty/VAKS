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
    source_access:
      access_level:
      has_direct_quote:
      has_source_range:
      confidence_cap:
      cap_reason:
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
    source_access:
      access_level: full_text | source_span | abstract_only | snippet_only | url_only | summary_only | unknown
      has_direct_quote: true | false
      has_source_range: true | false
      confidence_cap: low | medium | high
      cap_reason:
    evidence_support:
      span_supports_target: supported | partial | unsupported | unclear
      evidence_role: direct_support | inferential_support | background_context | counterexample
      reviewer_note:
```

规则：

- 只有 URL 的 source 只是 provenance，不是 support。
- 没有 full text / source span / direct quote 的 claim 不能给 high confidence。
- abstract_only / snippet_only 通常最多 medium，除非 claim 明确只关于摘要或片段本身。
- `background_context` 不能计入 supported。
- `inferential_support` 必须写 `reviewer_note` 才能用于 promotion。
- `counterexample` 应进入反例 / 冲突证据。
- evidence support 不自动提高 confidence。

CI-08 Source Range Boundary:

- `source_range` may use `file.md:42-58` or `file.md#L42-L58` when the source is line-addressable.
- `source_range` / `source_anchor` is provenance until the target-specific support check is filled.
- A line range alone cannot be `direct_support`; fill `span_supports_target`, `evidence_role`, `warrant` / `scope`, and `reviewer_note` when needed.
- URL-only, summary-only, `background_context`, malformed range, out-of-bounds range, missing source, or range-without-warrant cannot support promotion, truth confidence, reviewed relation, or action basis.

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

## Temporal Applicability Check

用于判断这个 claim 在当前时间、版本、项目、环境和条件下是否仍然适用。

```yaml
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
  check_state: in_scope | out_of_scope | stale | superseded | unknown | needs_review
  reviewer_note:
```

边界：

- Truth is source-backed.
- Applicability is time-, version-, and scope-bound.
- `out_of_scope` / `stale` / `superseded` 不等于 false，但不能直接作为当前 ready action basis。
- 不清楚时间窗口时留空或 `unknown`，不要编造。

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
