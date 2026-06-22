---
type: source
record_kind: source_card
status: source-captured
title: "ArthurYangX/nano-NotebookLM"
source_url: https://github.com/ArthurYangX/nano-NotebookLM
source_type: repo
author: ArthurYangX
captured_at: 2026-05-26
captured_by: codex
source_commit: 8458d9c2d3e958b1d5cf448fa4000448b28760b0
local_snapshot: C:\Users\Administrator\AppData\Local\Temp\nano_notebooklm_probe\nano-NotebookLM
archived_snapshot: raw/repos/_snapshots/nano-NotebookLM-8458d9c2d3e958b1d5cf448fa4000448b28760b0.zip
license: Apache-2.0
topics:
  - notebooklm
  - knowledge-graph
  - graph-rag
  - vector-index
  - bm25
  - faiss
projects:
  - verified-vault
evidence_level: primary
source_integrity:
  capture_confidence: 4
source_status: source-captured
related_patterns:
  - wiki/patterns/hybrid-vector-bm25-rrf-with-graph-neighborhood.md
  - wiki/patterns/generated-graph-human-edit-overlay.md
  - wiki/patterns/embedding-preset-namespaced-index-cache.md
tags:
  - repo-source
  - architecture-reference
knowledge_status: raw
processing_tier: light
source_id: https://github.com/ArthurYangX/nano-NotebookLM
why_saved: see_body_or_legacy_record
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
legacy_raw_metadata:
  source_quality: 4
  freshness: 5
  relevance: 5
  cross_source_count: 1
---
# 来源记录：ArthurYangX/nano-NotebookLM

## 为什么收录

用户指定该仓库，要求重点分析其知识图谱和向量索引设计，判断对当前 verified knowledge system 有什么可借鉴之处。

## 本次读取范围

高层文档：

- `README.md`
- `README.zh-CN.md`
- `CLAUDE.md`
- `pyproject.toml`
- `LICENSE`

核心源码：

- `nano_notebooklm/kb/vector_index.py`
- `nano_notebooklm/kb/bm25_index.py`
- `nano_notebooklm/kb/hybrid_search.py`
- `nano_notebooklm/kb/graph_search.py`
- `nano_notebooklm/kb/store.py`
- `nano_notebooklm/kg/extractor.py`
- `nano_notebooklm/kg/graph.py`
- `nano_notebooklm/kg/merger.py`
- `nano_notebooklm/ingest/chunker.py`
- `nano_notebooklm/types.py`
- `nano_notebooklm/config.py`
- `nano_notebooklm/orchestrator/router_intent.py`
- `nano_notebooklm/skills/qa_skill.py`
- `api/server.py`

验证辅助：

- `tests/test_graph_search.py`
- `tests/test_mindmap_edit.py`
- `tests/test_embedding_preset.py`

## 核心内容

该仓库是一个自托管学习助手，面向课程资料：

```text
PDF / PPTX / DOCX / Markdown
  -> chunks
  -> BM25 + FAISS + RRF
  -> two-stage knowledge graph
  -> GraphRAG retrieval
  -> cited chat / notes / quiz / editable mindmap
```

## 高信号设计

- 混合检索：BM25 处理关键词和 CJK 字符/二元组，FAISS 处理语义相似，RRF 融合结果。
- GraphRAG：用 concept embedding 选 seed concept，再 BFS 扩展邻居，返回邻域里的 source chunks。
- 两阶段图谱抽取：Stage A 先按文件抽 macro topics，Stage B 再按 chunk 抽 leaf concepts，并挂到 topic/root 下。
- 可编辑生成图谱：系统生成 `knowledge_graph.json`，用户编辑保存为 `mindmap_edits.json` sidecar，每次读取时 overlay replay。
- 引用回溯：chunk 带 source_file、page/slide/location，GraphRAG 最终仍回到 chunks.json 取原文。
- Embedding preset 命名空间：不同 embedding 模型写到不同 FAISS 目录，避免模型切换污染旧索引。

## 初步判断

它适合作为“搜索扩展层 + 关系层操作机制 + GraphRAG 实现参考”。

它不适合作为本资料库的 truth layer。其知识图谱主要服务学习检索和可视化，不处理 verified claim、反证、采纳决策和来源质量治理。
