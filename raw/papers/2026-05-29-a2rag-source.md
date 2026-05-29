---
type: source
status: source-captured
title: "A2RAG: Adaptive Agentic Graph Retrieval for Cost-Aware and Reliable Reasoning"
source_id: 2026-05-29-a2rag-source
source_uri: https://arxiv.org/abs/2601.21162
source_url: https://arxiv.org/abs/2601.21162
source_type: paper
authors:
  - Jiate Liu
  - Zebin Chen
  - Shaobo Qiao
  - Mingchen Ju
  - Danting Zhang
  - Bocheng Han
  - Shuyue Yu
  - Xin Shu
  - Jingling Wu
  - Dong Wen
  - Xin Cao
  - Guanfeng Liu
  - Zhengyi Yang
publisher: arXiv
venue: arXiv preprint
published_at: 2026-01-29
captured_at: 2026-05-29
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-05-29
extraction_tool: web
extraction_model: Codex
version_or_commit: arXiv:2601.21162v1
source_status: active
raw_location:
processing_mode: immediate
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: source-only
topics:
  - adaptive-retrieval
  - graph-rag
  - evidence-sufficiency
  - provenance-text
projects:
  - verified-action-knowledge-system
source_family: a2rag
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
      - source_id: "[[2026-05-29-a2rag-source]]"
        source_range: "arXiv abstract"
        quote_or_excerpt: "Paraphrase: A2RAG verifies evidence sufficiency, escalates retrieval effort only when necessary, and maps graph signals back to provenance text."
        evidence_support:
          span_supports_target: supported
          evidence_role: direct_support
          reviewer_note: "The source directly motivates the vault's Evidence Sufficiency Gate, while the vault rejects the full agentic retrieval implementation for MVP."
    rationale: "A2RAG directly motivates evidence sufficiency gating and progressive evidence discovery as an adaptive control idea."
    created: 2026-05-29
    last_verified: 2026-05-29
tags:
  - source
  - paper
  - a2rag
  - evidence-sufficiency
---

# 来源记录：A2RAG

## 为什么收录

Pro 第八个补充建议吸收 A2RAG 的核心控制思想：先轻量判断证据是否足够，只有不足时才逐步升级证据发现。

本项目只吸收 Evidence Sufficiency Gate，不实现 adaptive controller、agentic retriever 或 GraphRAG pipeline。

## 来源信息

- 论文：A2RAG: Adaptive Agentic Graph Retrieval for Cost-Aware and Reliable Reasoning
- 作者：Jiate Liu, Zebin Chen, Shaobo Qiao, Mingchen Ju, Danting Zhang, Bocheng Han, Shuyue Yu, Xin Shu, Jingling Wu, Dong Wen, Xin Cao, Guanfeng Liu, Zhengyi Yang
- arXiv：https://arxiv.org/abs/2601.21162
- 提交时间：2026-01-29

## 初步看点

- A2RAG 关注 one-size-fits-all retrieval 的成本浪费和困难查询失败问题。
- 它明确提出 adaptive controller 检查 evidence sufficiency，并在必要时触发 targeted refinement。
- 它还强调把 graph signals 映射回 provenance text，以避免图抽象丢失细节。

## 吸收方式

```text
Use the adaptive gate, not the GraphRAG runtime.

Evidence Sufficiency Gate:
  sufficient -> proceed
  weak -> expose gaps
  insufficient -> retrieve_more / create_missing_point / ask_user
  out_of_scope -> scope mismatch
  risky -> action_readiness: risky / needs_review
```

## 边界

```text
Do not implement A2RAG.
Do not add agentic retriever.
Do not make graph signals truth.
Do not auto-escalate retrieval without user authorization.
Do not make every query pay the heavy evidence-discovery cost.
```

## 可抽取 Candidate Points

1. Evidence sufficiency should be checked before expensive or action-bearing escalation.
2. Evidence discovery should be progressive, not one-size-fits-all.
3. Graph signals should map back to provenance text before they influence action.
4. The vault can use sufficiency states without adopting GraphRAG runtime.

## 下一步

- Use A2RAG as the strongest source record for Evidence Sufficiency Gate.
- Keep gate manual/review-mediated in MVP.
