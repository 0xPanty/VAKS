---
type: source
record_kind: source_card
status: source-captured
title: "infiniflow/ragflow"
source_id: github-infiniflow-ragflow-2026-06-07
source_uri: https://github.com/infiniflow/ragflow
source_url: https://github.com/infiniflow/ragflow
source_type: repository
author: infiniflow
publisher: GitHub
published_at: 2023-12-12
updated_at: 2026-06-06
captured_at: 2026-06-07
captured_by: Codex
version_or_commit: 5a04ac0864808bb3309e0b5735b56ad5a03d2efd
source_status: active
raw_location: raw/repos/2026-06-07-infiniflow-ragflow-source.md
processing_mode: source-intake-routing-github-scout
processing_level: medium
processing_tier: medium
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
  - source-intake
  - context-pack
entities:
  - RAGFlow
  - DeepDoc
  - ingestion pipeline
  - chunk metadata
aliases:
  - infiniflow/ragflow
projects:
  - VAKS
source_family: github_repo_workbench_scout
upstream_sources: []
verification_status: source_metadata_checked
tags:
  - github-scout
  - source-intake-routing
---

# 来源记录：infiniflow/ragflow

## 为什么收录

为 `source-intake-routing` 工作台调研。RAGFlow 的价值集中在“复杂文档解析、ingestion pipeline 模板、chunk metadata、connector、document/chunk API”，很适合压测 VAKS 的 source card -> candidate -> context pack 路由体验。

这张卡只记录来源，不代表 VAKS 采用 RAGFlow。

## 来源信息

- 作者/组织：infiniflow
- 发布方：GitHub
- 原始链接：https://github.com/infiniflow/ragflow
- 版本 / commit：`5a04ac0864808bb3309e0b5735b56ad5a03d2efd`
- commit time：2026-06-05T13:16:25Z
- GitHub pushed_at：2026-06-05T13:59:26Z
- stars captured：82040
- forks captured：9454
- default branch：main
- license：Apache-2.0
- source_status：active
- 采集方式：GitHub API metadata + raw file anchor inspection; no clone; no runtime execution.

## Intake Boundary

```yaml
processing_tier: medium
knowledge_status: raw
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
```

## Source / Code Anchors

| Anchor | What exists | Why it matters for source-intake-routing | Boundary |
|---|---|---|---|
| `README.md:77` | Describes RAGFlow as RAG engine with context layer and workflow. | Good source for context-layer product framing. | Marketing/README claim only. |
| `README.md:95-96` | Notes document parsing methods and orchestrable ingestion pipeline support. | Directly relevant to source intake pipeline UX. | Needs code/runtime validation before implementation. |
| `agent/templates/advanced_ingestion_pipeline.json:4-13` | Advanced ingestion pipeline template. | Strong signal for recipe-based intake routes. | Template inspiration only. |
| `agent/templates/advanced_ingestion_pipeline.json:24-40` | Metadata and chunk content fields. | Useful for source/chunk metadata separation. | Metadata still not authority. |
| `api/apps/restful_apis/chunk_api.py:31-51` | Chunk API imports document/task/metadata services and image/reference metadata utilities. | Suggests chunk is a managed workbench object. | VAKS should not make chunk object a truth layer. |
| `common/data_source/github/connector.py:22-36` | GitHub connector dependencies and interfaces. | Connector pattern relevant to source acquisition routes. | Do not start connector runtime now. |
| `deepdoc/parser/pdf_parser.py:57,428` | PDF parser class and table rotation tracking. | Shows source hygiene/parser complexity for PDFs. | Parser output is raw extraction, not evidence support. |

## 初步看点

- RAGFlow 比普通 RAG demo 更贴近 source-intake-routing，因为它有 ingestion pipeline 模板、document/chunk API、connector、parser 这些“前处理工作台”要素。
- 对 VAKS 的候选启发是：topic pack builder 前面可能需要“source type / parser / chunk method / metadata”可见，而不是只看搜索结果。
- `advanced_ingestion_pipeline` 的“为 chunk 生成摘要/关键词/metadata 支持多样 retrieval”很贴近 VAKS 的 metadata prefill，但必须保持低 authority。

## 明显疑点

- 未 clone、未运行、未验证模板实际行为。
- RAGFlow 是完整平台，吸收它的 pipeline 对 VAKS 可能过重。
- Chunk metadata 很容易被误读为 evidence support，需要强边界。

## 可抽取 Candidate Points

- source-intake-routing 可以借鉴“ingestion recipe”而不是统一强流程。
- Chunk metadata / summaries 可提升检索发现，但不能替代 raw anchor 或 reviewed support。
- Connector / parser / document / chunk 应作为 routing/workbench 维度，不应成为 truth object。

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- 需要针对 PDF / repo / article 三类 source 做 intake route 原型比较。
- 需要验证 RAGFlow ingestion template 如何保存 metadata 与 chunk trace。

## 下一步

进入 `source-intake-routing` GitHub scout candidate distillation。
