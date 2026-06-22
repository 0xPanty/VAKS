---
type: source
record_kind: source_card
status: source-captured
title: "VERISCORE: Evaluating the factuality of verifiable claims in long-form text generation"
source_id: 2026-05-29-veriscore-source
source_uri: https://aclanthology.org/2024.findings-emnlp.552/
source_url: https://aclanthology.org/2024.findings-emnlp.552/
source_type: paper
authors:
  - Yixiao Song
  - Yekyung Kim
  - Mohit Iyyer
publisher: Association for Computational Linguistics
venue: Findings of EMNLP 2024
published_at: 2024
captured_at: 2026-05-29
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-05-29
extraction_tool: web
extraction_model: Codex
version_or_commit: ACL Anthology 2024.findings-emnlp.552
source_status: active
raw_location:
review_priority: normal
review_owner: Codex
formalization_status: source-only
topics:
  - factuality
  - verifiability
  - candidate-routing
projects:
  - verified-action-knowledge-system
source_family: veriscore
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions: []

knowledge_status: raw
processing_tier: light
why_saved: see_body_or_legacy_record
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
---

# 来源记录：VERISCORE

## 为什么收录

Pro 第四个补充建议吸收 VERISCORE 的一个核心启发：长文本里不是所有内容都可验证，不应该把所有 candidate 都当作 atomic claim 处理。

本项目只吸收这个 review-routing 思路，不实现 VERISCORE metric，也不引入自动 factuality evaluator。

## 来源信息

- 论文：VERISCORE: Evaluating the factuality of verifiable claims in long-form text generation
- 作者：Yixiao Song, Yekyung Kim, Mohit Iyyer
- 会议：Findings of EMNLP 2024
- 官方页面：https://aclanthology.org/2024.findings-emnlp.552/
- arXiv：https://arxiv.org/abs/2406.19276

## 初步看点

- 论文指出，很多长文本 factuality metrics 会把输入拆成 atomic claims，然后假设每个 claim 都能被验证。
- VERISCORE 的问题意识是：真实长文本任务同时包含可验证和不可验证内容。
- 它只评估 verifiable claims，而不是把所有内容拉进同一条事实验证管道。

## 吸收方式

```text
Use the idea, not the metric.

Candidate point = atomic review unit.
Not every candidate point = atomic claim.

Before review:
  identify point_type
  identify verifiability
  route to the right review path
```

## 边界

```text
Unverifiable does not mean useless.
It means no truth confidence.

Only verifiable claims can receive truth / evidence confidence.
Preferences, interpretations, hypotheses, open questions, and decisions need other review signals.
```

## 可抽取 Candidate Points

1. Candidate points should be routed by point type and verifiability before review.
2. Atomic review unit is a better term than atomic claim for this project.
3. Useful but unverifiable content should not receive truth confidence.
4. Review routes should differ for claims, interpretations, hypotheses, patterns, risks, preferences, decisions, open questions, and implementation notes.

## 下一步

- Keep routing fields light.
- Do not turn verifiability routing into a new module or automated metric.
