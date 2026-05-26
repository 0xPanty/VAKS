---
type: pattern
status: active
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - OpenKB
  - PageIndex
related_concepts:
  - "[[2026-05-27-openkb-architecture-review]]"
  - "[[source-adapter-ingest-contract]]"
related_projects:
  - verified-knowledge-system
adoption_status: adopt-candidate
tags:
  - pattern/source-adapter
  - long-document
  - pageindex
  - retrieval
evidence_count: 1
confidence: high
negative_evidence:
replaces:
superseded_by:
relations:
  - target: "[[source-adapter-ingest-contract]]"
    type: refines
    strength: 4
    confidence: high
    evidence:
      - "[[long-document-tree-index-source-adapter]]"
    rationale: "Long documents need a source adapter that exposes navigable tree summaries and targeted page windows."
    created: 2026-05-27
    last_verified: 2026-05-27
extension_points:
  - source adapters
  - retrieval engines
  - context pack modes
---

# 设计模式：Long Document Tree Index Source Adapter

## 一句话定义

长文档不要直接塞给 LLM，也不要只切成向量 chunk；先生成结构树和页面级 source windows，让 agent 按章节/page range 精准读取。

## 解决的问题

长 PDF、书、论文集有三个问题：

- 全文太长，直接读成本高且容易 context rot。
- 普通 chunk retrieval 容易丢结构。
- 摘要太短，又无法支持可验证 claim。

OpenKB 用 PageIndex 把长 PDF 变成：

```text
document tree
summary with page ranges
wiki/sources/<doc>.json
get_page_content(doc, "3-5,9")
```

这对 verified system 很有价值，因为 source window 可以被引用、复核和纳入 context pack。

## 适用场景

- PDF 大于普通上下文窗口。
- 需要从论文/书中抽 claim、pattern、decision。
- agent 需要按章节追证据。
- 不想 v0.1 就依赖重型向量数据库。

## 不适用场景

- 短文章、短 markdown、单页网页。
- 必须做语义相似搜索的超大语料库。
- PageIndex 树质量不稳定且无法人工校验的场景。

## 反例与避坑

- 失败条件：只相信树摘要，不回读页面原文。
- 相似反模式：把 retrieval summary 当成 truth。
- 复杂度风险：引入 PageIndex/云 OCR/多模态成本。
- 替代方案：markitdown + manual sections；BM25 + page window；Zilliz/QMD 作为候选召回。

## 来源证据

OpenKB 的 `converter.py` 按 PDF 页数 threshold 分流，长 PDF 进入 PageIndex；`indexer.py` 写出 per-page JSON 和 summary；query/skill tools 通过 page range 读取。

## 标签与量化

- domain: source ingest
- problem: long document grounding
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 4
- integration_fit: 5
- evidence_strength: 4
- reversibility: 4

## 交叉验证

- 相似来源：OpenKB/PageIndex、nano-NotebookLM GraphRAG/BM25+FAISS、QMD local search。
- 历史项目影子：资料库会持续吸收论文、repo 文档、长文章，必须能定位原文。
- 支持证据：OpenKB 把 long doc 处理作为核心卖点。
- 反例：如果文档很短，直接 full text 更简单。

## 最小实现方式

先不接 PageIndex，也可以设计 contract：

```yaml
source_windows:
  - source_id:
    locator_type: page | heading | line
    locator:
    text:
    checksum:
```

接入 OpenKB/PageIndex 时，把 per-page JSON 映射到 source windows。

## 项目融合建议

吸收为 `source adapter` 候选。

优先级高，但不作为 SCHEMA v0.1 阻塞项。它可以在 `IMPLEMENTATION_BLUEPRINT.md` 中作为长文档路线：

```text
short docs -> direct markdown source
long docs -> tree index + source windows
```

## 可拓展性

- 可以通过什么接口/适配层接入：source adapter、retrieval adapter、context pack source windows。
- 未来可能被什么替代：QMD、Zilliz、custom PDF parser、Docling、Marker。
- 替换或升级成本：中等，只要 source window contract 稳定即可。
- 回退方式：保留 raw PDF，人工/LLM 摘要，按页手动引用。

## 验证指标

- 给定一个长 PDF，能否生成可追溯 summary。
- claim 是否能回到具体 page range。
- context pack 是否能带出小窗口，而不是整篇 dump。
- adapter 失败时 raw source 是否仍可用。
