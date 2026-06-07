---
type: source
status: source-captured
title:
source_id:
source_uri:
source_url:
source_type: article
author:
publisher:
published_at:
updated_at:
captured_at:
captured_by:
version_or_commit:
source_status: unknown
raw_location:
processing_mode: inbox
processing_level: light
processing_tier: light
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: normal
review_owner: Codex
formalization_status: raw-only
topics:
projects:
source_family:
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
---

# 来源记录：

## 为什么收录


## 来源信息

- 作者：
- 发布方：
- 发布时间：
- 更新时间：
- 原始链接：
- 原始位置：
- 版本 / commit / DOI：
- source_status: active / legacy / deprecated / unknown
- 采集方式：

## Intake Boundary

```yaml
processing_tier: light | medium | heavy
knowledge_status: raw
overlay_state: none
review_pressure: none | review_due | blocked
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
```

Source records provide provenance and findability. They must not carry
adopt/reject verdicts, truth scores, project borrowing conclusions, or action
basis.

## Medium / Heavy Optional Provenance

```yaml
extraction:
  extracted_at:
  extracted_by:
  model:
  tool:
  source_ranges: []

provenance:
  model: PROV-lite
  activities:
    - type: captured
      at:
      by:
    - type: extracted
      at:
      by:
      tool:
      model:
  agents:
    - id:
      type: human | model | tool
```

说明：

```text
provenance 只记录来源和处理轨迹，不代表这个 source 支持了某个 claim。
claim 是否成立，仍然要进入 candidate / calibration / review。
review、promotion、context-pack use 不放在 Source 主字段里。
```

## 时间线 / 上下文

- 作者/组织背景：
- 当时版本或阶段：
- 后续更新：
- 是否 legacy / deprecated：
- 为什么这个时间点重要：

## 初步看点



## 明显疑点


## 可抽取 Candidate Points


## 当前处理等级

```text
light / medium / heavy
```

升级到 heavy 的条件：

-


## 可选验证字段

```yaml
source_metadata_quality:
freshness:
relevance:
source_hygiene_note:
source_independence_hint:
last_verified:
next_review:
```

These are source hygiene hints only. A Source record does not own truth confidence, and cross-source agreement belongs to review aggregation / coverage rather than the Source node itself.

## 候选关系建议

```yaml
candidate_relation_suggestions:
  - target: "[[claim-or-pattern]]"
    relation_type: derived_from | supports | contradicts | refines | risk_of
    relation_state: candidate
    why_suggested: "One sentence explaining what this source may contribute."
    source_anchor:
    evidence_support:
      span_supports_target:
      evidence_role:
      reviewer_note:
    suggested_at:
```

Source records may suggest candidate relations.
They cannot create reviewed relations, relation strength, or truth confidence.

## 下一步
