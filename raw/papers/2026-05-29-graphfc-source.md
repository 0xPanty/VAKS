---
type: source
status: source-captured
title: "A Graph-based Verification Framework for Fact-Checking"
source_id: 2026-05-29-graphfc-source
source_uri: https://arxiv.org/abs/2503.07282
source_url: https://arxiv.org/abs/2503.07282
source_type: paper
authors:
  - Yani Huang
  - Richong Zhang
  - Zhijie Nie
  - Junfan Chen
  - Xuefeng Zhang
publisher: arXiv
venue:
published_at: 2025-03-10
captured_at: 2026-05-29
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-05-29
extraction_tool: web
extraction_model: Codex
version_or_commit: arXiv:2503.07282v1
source_status: active
raw_location:
processing_mode: immediate
processing_level: light
review_priority: normal
review_owner: Codex
formalization_status: source-only
topics:
  - fact-checking
  - claim-graph
  - point-graph-fragment
  - review-queue
projects:
  - verified-action-knowledge-system
source_family: graphfc
upstream_sources: []
verification_status: primary-source-captured
evidence_level: primary
confidence: medium
relations:
  - target: "[[REVIEW_QUEUE]]"
    type: refines
    relation_state: candidate
    strength: 3
    confidence: low
    evidence:
      - "[[2026-05-29-graphfc-source]]"
    rationale: "GraphFC motivates optional entity-relation decomposition for complex candidate points without adopting the full automated fact-checking pipeline."
    created: 2026-05-29
    last_verified: 2026-05-29
tags:
  - source
  - paper
  - graphfc
  - point-graph-fragment
---

# 来源记录：GraphFC

## 为什么收录

Pro 第六个补充建议吸收 GraphFC 的一个核心启发：复杂判断如果只保留成自然语言句子，后续 collision、review 和 coverage 容易不精确。

本项目只吸收轻量 `point_graph_fragment` 思路，不实现完整 GraphFC pipeline、不自动构建 claim/evidence graph、不自动生成 fact-checking label。

## 来源信息

- 论文：A Graph-based Verification Framework for Fact-Checking
- 框架名：GraphFC
- 作者：Yani Huang, Richong Zhang, Zhijie Nie, Junfan Chen, Xuefeng Zhang
- arXiv：https://arxiv.org/abs/2503.07282
- 提交时间：2025-03-10
- 收录方式：arXiv 摘要页核验

## 初步看点

- 复杂 claim 可以拆成 entity-relation triplets。
- Claim graph / evidence graph 可以辅助 graph-guided planning / checking。
- 对本项目最有价值的是：复杂 candidate point 可选拆成小的 point graph fragment，帮助 reviewer 看清实体、关系、qualifier、scope 和 source anchor。

## 吸收方式

```text
Use the idea, not the pipeline.

Ordinary candidate:
  natural-language atomic review unit

Complex candidate:
  optional point_graph_fragment
```

## 边界

```text
point_graph_fragment is a review aid, not a reviewed relation.
triplet extraction is not truth.
triplet similarity is not support.
triplet conflict is not automatic rejection.
Only reviewed relations enter the formal knowledge graph.
Do not build full GraphFC in MVP.
```

## 可抽取 Candidate Points

1. Complex candidate points may need entity-relation decomposition to support precise review.
2. Triplet-level structure can make point collision more precise than semantic similarity alone.
3. Extracted triplets must remain candidate review aids until reviewed.
4. Too many triplets means the candidate point is too broad and should be split.

## 下一步

- Verify the exact GraphFC paper metadata before promoting this source record.
- Keep `point_graph_fragment` optional and use it only for high-impact / ambiguous candidates.
