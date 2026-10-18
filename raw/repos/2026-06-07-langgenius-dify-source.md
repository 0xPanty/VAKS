---
type: source
record_kind: source_card
status: source-captured
title: "langgenius/dify"
source_id: github-langgenius-dify-2026-06-07
source_uri: https://github.com/langgenius/dify
source_url: https://github.com/langgenius/dify
source_type: repository
author: langgenius
publisher: GitHub
published_at: 2023-04-12
updated_at: 2026-06-06
captured_at: 2026-06-07
captured_by: Codex
version_or_commit: 76fb1b6ea81660475cfb32164823db6b47060397
source_status: active
raw_location: raw/repos/2026-06-07-langgenius-dify-source.md
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
  - retrieval
entities:
  - Dify
  - RAG Pipeline
  - datasets
  - document ingestion
aliases:
  - langgenius/dify
  - Dify knowledge base
projects:
  - VAKS
source_family: github_repo_workbench_scout
upstream_sources: []
verification_status: source_metadata_checked
tags:
  - github-scout
  - source-intake-routing
---

# 来源记录：langgenius/dify

## 为什么收录

为 `source-intake-routing` 工作台调研。Dify 是高星、近期活跃的 LLM 应用/RAG 平台，适合作为“知识库入口、文档 ingest、dataset metadata、retrieval routing、可观测性”这一类产品化参考。

这张卡只记录来源和可回钻 anchor，不代表 VAKS 采用 Dify。

## 来源信息

- 作者/组织：langgenius
- 发布方：GitHub
- 原始链接：https://github.com/langgenius/dify
- 版本 / commit：`76fb1b6ea81660475cfb32164823db6b47060397`
- commit time：2026-06-06T02:39:07Z
- GitHub pushed_at：2026-06-06T16:00:22Z
- stars captured：144154
- forks captured：22685
- default branch：main
- license：NOASSERTION
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
| `README.md:63` | Platform description includes workflow, RAG pipeline, model management, observability. | Shows product surface bundles ingest/retrieval/workflow/observability. | Product claim only; not VAKS evidence. |
| `README.md:104-105` | RAG pipeline covers document ingestion to retrieval and common document extraction. | Good reference for workbench top-level source-intake lane. | Do not inherit Dify pipeline semantics. |
| `api/controllers/console/datasets/datasets_document.py:31-39` | Dataset document controller imports datasource/document response fields. | Confirms document-level management is first-class. | Path anchor only; not reviewed design. |
| `api/controllers/console/datasets/metadata.py:16-25` | Dataset metadata API surface. | Useful hint for metadata as filter/discovery surface. | Metadata is not authority. |
| `api/core/rag/retrieval/router/multi_dataset_function_call_router.py:9-39` | Multi-dataset router class and tool selection. | Routing multiple datasets is relevant to lane-aware retrieval. | Do not copy function-call routing into VAKS by default. |

## 初步看点

- Dify 的强项是产品工作台：dataset、document、metadata、retrieval、observability 都在用户能理解的界面附近。
- 对 VAKS 的候选启发是“source-intake-routing 需要一个清楚前门”，不是“上一个 Dify 式平台”。
- Dataset metadata 与 multi-dataset routing 可作为检索入口设计参考，但必须继续服从 `knowledge_status` / `retrieval_policy`。

## 明显疑点

- 未 clone、未运行、未检查完整代码路径。
- GitHub stars 是热度和成熟度线索，不是质量、真理或适配证据。
- Dify 是生产平台，复杂度远高于当前 VAKS 沙盒需要。

## 可抽取 Candidate Points

- source-intake-routing 工作台应把 “dataset/document/source type” 作为用户可见入口，而不是只暴露全文搜索框。
- Metadata 可以支持检索切片，但不能表达 reviewed / action-ready。
- 多数据集路由值得借鉴为 lane routing 的 UI/运行模型，但不能绕过 VAKS authority bucket。

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- 需要比较 Dify / RAGFlow / AnythingLLM 的实际知识库 UI 与 VAKS Obsidian 工作台设计。
- 需要复现 Dify dataset/document/metadata/retrieval behavior。

## 下一步

进入 `source-intake-routing` GitHub scout candidate distillation，作为候选参考之一。
