---
type: source
status: source-captured
title: "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection"
source_id: 2026-05-29-self-rag-source
source_uri: https://arxiv.org/abs/2310.11511
source_url: https://arxiv.org/abs/2310.11511
source_type: paper
authors:
  - Akari Asai
  - Zeqiu Wu
  - Yizhong Wang
  - Avirup Sil
  - Hannaneh Hajishirzi
publisher: arXiv
venue: arXiv preprint
published_at: 2023-10-17
captured_at: 2026-05-29
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-05-29
extraction_tool: web
extraction_model: Codex
version_or_commit: arXiv:2310.11511v1
source_status: active
raw_location:
processing_mode: immediate
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: source-only
topics:
  - retrieval-augmented-generation
  - adaptive-retrieval
  - evidence-sufficiency
projects:
  - verified-action-knowledge-system
source_family: self-rag
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions: []

---

# 来源记录：Self-RAG

## 为什么收录

Pro 第八个补充建议吸收 Self-RAG 的轻量控制思想：不要固定塞入一批文档；检索和复核应按需要触发。

本项目只吸收“按需升级”的思想，不实现 Self-RAG 训练、reflection tokens 或自动自评流程。

## 来源信息

- 论文：Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection
- 作者：Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, Hannaneh Hajishirzi
- arXiv：https://arxiv.org/abs/2310.11511
- 提交时间：2023-10-17

## 初步看点

- Self-RAG 指出固定数量的 indiscriminate retrieval 会降低灵活性或带来无用生成。
- 它训练模型按需检索，并对 retrieved passages 和 generation 做 reflection。
- 对本资料库有用的是控制思想：不是所有 query 都重流程，只有用途需要时才升级证据检查。

## 吸收方式

```text
Use the control idea, not the model pipeline.

Ordinary query:
  stay light.

Action / promotion / decision:
  check evidence sufficiency.
```

## 边界

```text
Do not implement Self-RAG.
Do not add reflection tokens.
Do not let LLM self-reflection decide truth.
Do not auto-retrieve unless the user authorizes retrieval.
```

## 可抽取 Candidate Points

1. Retrieval should be on demand, not indiscriminate.
2. Evidence checks should escalate only when the intended use needs stricter support.
3. Reflection is useful as inspiration, but review still decides confidence in this vault.

## 下一步

- Use this source only to support Evidence Sufficiency Gate wording.
- Do not make ordinary capture or ordinary query heavier.
