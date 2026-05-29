---
type: source
status: source-captured
title: "ProVe: A Pipeline for Automated Provenance Verification of Knowledge Graphs against Textual Sources"
source_id: 2026-05-29-prove-provenance-verification-source
source_uri: https://arxiv.org/abs/2210.14846
source_url: https://arxiv.org/abs/2210.14846
source_type: paper
authors:
  - Gabriel Amaral
  - Odinaldo Rodrigues
  - Elena Simperl
publisher: arXiv
venue: arXiv preprint
published_at: 2022-10-26
captured_at: 2026-05-29
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-05-29
extraction_tool: web
extraction_model: Codex
version_or_commit: arXiv:2210.14846
source_status: active
raw_location:
processing_mode: immediate
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: source-only
topics:
  - provenance-verification
  - evidence-support
  - knowledge-graph
  - citation-support
projects:
  - verified-action-knowledge-system
source_family: prove
upstream_sources: []
verification_status: primary-source-captured
evidence_level: primary
confidence: medium
relations:
  - target: "[[REVIEW_QUEUE]]"
    type: refines
    relation_state: candidate
    strength: 4
    confidence: medium
    evidence:
      - source_id: "[[2026-05-29-prove-provenance-verification-source]]"
        source_range: "paper abstract / problem statement"
        quote_or_excerpt: "Paraphrase: the paper frames provenance verification as checking whether documented provenance text supports a KG triple."
        evidence_support:
          span_supports_target: partial
          evidence_role: inferential_support
          reviewer_note: "The source motivates this vault's source-span-to-target support check, but the vault narrows it to manual review fields rather than adopting the automated pipeline."
    rationale: "ProVe motivates checking whether documented provenance text supports the specific triple or point being reviewed."
    created: 2026-05-29
    last_verified: 2026-05-29
tags:
  - source
  - paper
  - prove
  - evidence-support
---

# 来源记录：ProVe

## 为什么收录

Pro 第七个补充建议吸收 ProVe 的一个核心问题意识：有 documented provenance 不等于 provenance 里的文本真的支持目标 triple。

本项目只吸收这个 review 规则，不实现完整 ProVe pipeline，也不引入自动 NLI / RTE / support score。

## 来源信息

- 论文：ProVe: A Pipeline for Automated Provenance Verification of Knowledge Graphs against Textual Sources
- 作者：Gabriel Amaral, Odinaldo Rodrigues, Elena Simperl
- arXiv：https://arxiv.org/abs/2210.14846
- 提交时间：2022-10-26
- 后续版本：Semantic Web 2024 版本存在，但当前 source record 只按 arXiv 页面轻量记录

## 初步看点

- ProVe 关注 Knowledge Graph triple 和 documented provenance 之间的支撑关系。
- 它的问题不是“source 是否存在”，而是“source 文本是否支持目标 triple”。
- 这正好补上本资料库 Source Provenance 和 Evidence-Aware Review 之间的缺口。

## 吸收方式

```text
Use the control idea, not the pipeline.

Source provenance:
  where material came from.

Evidence support:
  whether a specific source span supports a specific point, node, or relation.
```

## 边界

```text
Do not implement automated ProVe.
Do not add support probability scores.
Do not let model entailment automatically decide truth.
Do not make evidence support a Source-node property.
```

## 可抽取 Candidate Points

1. A source link or documented provenance is not evidence support by itself.
2. Evidence support should be checked at source-span-to-target granularity.
3. Reviewed relations need evidence that supports the edge itself, not only the endpoint nodes.
4. Automated provenance verification is useful inspiration but too heavy for the current MVP.

## 下一步

- Keep `evidence_support` as a review field on evidence items.
- Test it only during promotion, strong relation review, context pack, action basis, or high-impact review.
