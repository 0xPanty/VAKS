---
type: source
status: source-captured
title: "Corrective Retrieval Augmented Generation"
source_id: 2026-05-29-crag-source
source_uri: https://arxiv.org/abs/2401.15884
source_url: https://arxiv.org/abs/2401.15884
source_type: paper
authors:
  - Shi-Qi Yan
  - Jia-Chen Gu
  - Yun Zhu
  - Zhen-Hua Ling
publisher: arXiv
venue: arXiv preprint
published_at: 2024-01-29
updated_at: 2024-10-07
captured_at: 2026-05-29
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-05-29
extraction_tool: web
extraction_model: Codex
version_or_commit: arXiv:2401.15884v3
source_status: active
raw_location:
processing_mode: immediate
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: source-only
topics:
  - retrieval-augmented-generation
  - retrieval-evaluation
  - evidence-sufficiency
projects:
  - verified-action-knowledge-system
source_family: crag
upstream_sources: []
verification_status: primary-source-captured
evidence_level: primary
confidence: medium
relations:
  - target: "[[context-pack-evidence-envelope]]"
    type: refines
    relation_state: candidate
    strength: 4
    confidence: medium
    evidence:
      - source_id: "[[2026-05-29-crag-source]]"
        source_range: "arXiv abstract"
        quote_or_excerpt: "Paraphrase: CRAG uses a lightweight retrieval evaluator to assess retrieved document quality and trigger different retrieval actions."
        evidence_support:
          span_supports_target: partial
          evidence_role: inferential_support
          reviewer_note: "The source motivates evaluating whether retrieved evidence is good enough before relying on it, without adopting the automatic evaluator."
    rationale: "CRAG motivates checking retrieved evidence quality before using it in action context."
    created: 2026-05-29
    last_verified: 2026-05-29
tags:
  - source
  - paper
  - crag
  - evidence-sufficiency
---

# 来源记录：CRAG

## 为什么收录

Pro 第八个补充建议吸收 CRAG 的轻量控制思想：不要盲目信任 retrieval；先评估证据质量，再决定是否补查或纠正。

本项目只吸收 retrieval quality gate 的思想，不实现 CRAG 的自动 evaluator、web search extension 或 decompose-then-recompose pipeline。

## 来源信息

- 论文：Corrective Retrieval Augmented Generation
- 作者：Shi-Qi Yan, Jia-Chen Gu, Yun Zhu, Zhen-Hua Ling
- arXiv：https://arxiv.org/abs/2401.15884
- 初版：2024-01-29
- 当前版本：v3, 2024-10-07

## 初步看点

- CRAG 关注检索结果错误时 RAG 会怎样失效。
- 它加入轻量 retrieval evaluator，按质量触发不同 retrieval actions。
- 对本资料库有用的是“证据不足或质量不够时才升级”的闸门思想。

## 吸收方式

```text
Use the gate, not the evaluator.

Before action basis:
  ask whether current evidence is sufficient.

If insufficient:
  recommend ask_user / retrieve_more / create_missing_point / narrow_scope / mark_not_actionable / needs_review.
```

## 边界

```text
Do not implement automatic retrieval evaluator.
Do not trigger automatic web search.
Do not let retrieval quality scores decide truth.
Do not make every query run through a heavy correction loop.
```

## 可抽取 Candidate Points

1. Retrieved context quality should be evaluated before it is trusted for action.
2. Evidence insufficiency can trigger different next steps instead of forcing an answer.
3. Retrieval evaluation belongs to runtime / action support, not truth core.

## 下一步

- Keep `retrieve_more` as a recommendation unless the user explicitly authorizes retrieval.
- Use CRAG only as a boundary source for Evidence Sufficiency Gate.
