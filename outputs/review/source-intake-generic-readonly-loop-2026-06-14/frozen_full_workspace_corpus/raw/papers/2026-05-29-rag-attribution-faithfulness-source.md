---
type: source
record_kind: source_card
status: source-captured
title: "Correctness is not Faithfulness in RAG Attributions"
source_id: 2026-05-29-rag-attribution-faithfulness-source
source_uri: https://arxiv.org/abs/2412.18004
source_url: https://arxiv.org/abs/2412.18004
source_type: paper
authors:
  - Jonas Wallat
  - Maria Heuss
  - Maarten de Rijke
  - Avishek Anand
publisher: arXiv
venue: arXiv preprint
published_at: 2024-12-23
captured_at: 2026-05-29
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-05-29
extraction_tool: web
extraction_model: Codex
version_or_commit: arXiv:2412.18004
source_status: active
raw_location:
review_priority: normal
review_owner: Codex
formalization_status: source-only
topics:
  - rag-attribution
  - citation-correctness
  - citation-faithfulness
  - evidence-support
projects:
  - verified-action-knowledge-system
source_family: rag-attribution-faithfulness
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

# 来源记录：Correctness is not Faithfulness in RAG Attributions

## 为什么收录

Pro 第七个补充建议借这篇论文提醒：citation correctness 和 citation faithfulness 不是一回事。

本项目吸收的是“citation / source link 不能冒充 evidence support”的警告；不宣称实现完整 citation faithfulness，因为当前系统不记录或验证生成过程是否真的因果依赖该 citation。

## 来源信息

- 论文：Correctness is not Faithfulness in RAG Attributions
- 作者：Jonas Wallat, Maria Heuss, Maarten de Rijke, Avishek Anand
- arXiv：https://arxiv.org/abs/2412.18004
- 提交时间：2024-12-23

## 初步看点

- 论文区分 citation correctness 和 citation faithfulness。
- Citation correctness 关注 cited document 是否支持对应 statement。
- Citation faithfulness 更严格，要求模型实际依赖引用文档，而不是事后贴相关引用。
- 本资料库当前只做 evidence support / citation correctness 级别的人工复核，不做因果 faithfulness verification。

## 吸收方式

```text
Use as a warning, not as a claim of full implementation.

A source link is not evidence.
Evidence must support the specific point.
Full causal citation faithfulness is out of scope.
```

## 边界

```text
Do not claim the system verifies citation faithfulness.
Do not record model-generation causal reliance in MVP.
Do not build a RAG attribution evaluator.
Do not score citation faithfulness.
```

## 可抽取 Candidate Points

1. Citation correctness and citation faithfulness should not be conflated.
2. The current architecture should implement source-span evidence support, not full causal faithfulness.
3. Background citations cannot count as support in coverage maps.
4. Context packs should expose whether cited spans actually support key points.

## 下一步

- Use this source as a boundary reference when wording Evidence Support Check.
- Avoid saying "the system verifies citation faithfulness" in README, schema, or architecture docs.
