---
type: candidate_pattern
status: active
pattern_id: source-structure-first-rag
created_at: 2026-06-05
truth_boundary: candidate pattern only; not reviewed knowledge
source_family_ids:
  - sf-rag-engineering
  - sf-obsidian-workflow
  - sf-graph-ontology
project_fit_refs:
  - outputs/review/project_borrowing_ledgers/VAKS.md
---

# Source Structure First for RAG

## One-Line Pattern

在检索、切分、向量化、摘要之前，先尽量保留来源本身的结构：标题、章节、表格、段落、条款、页面、时间戳、文件层级。

## Problem Addressed

RAG 或知识库经常在入口处就把资料切碎。机械按字数切分会破坏原文结构，后续向量检索、rerank、GraphRAG、摘要再强，也可能是在被破坏的材料上工作。

## Mechanism

- intake 时保留 source structure。
- chunking 参考文档结构，而不是只按固定字数。
- context pack 尽量带回结构锚点。
- 对表格、条款、标题层级、页面区域、时间戳做轻量记录。

## Applicability

- RAG / 企业知识库。
- PDF / Office / Markdown / 法律文档 / 产品文档。
- 需要引用、回源、审查证据的系统。
- VAKS 的 source intake / context-pack preparation。

## Non-Goals and Trade-Offs

- 不等于所有项目都要复杂文档解析。
- 不等于结构完整就能自动判真。
- 对短文本、临时聊天、轻 capture 不应过重。
- 表格/OCR/layout 解析本身也可能出错，仍要保留原始锚点。

## Derived From Sources

- `raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source.md`
- `raw/videos/2026-06-04-bilibili-rag-failure-chunking-rerank-prompt-source.md`
- `raw/videos/2026-06-04-bilibili-rag-back-to-bm25-sqlite-source.md`
- `raw/videos/2026-06-04-bilibili-claude-code-obsidian-local-knowledge-base-source.md`
- `raw/papers/2026-06-04-methontology-source.md`

## Aliases or Near-Duplicates

- structure-aware chunking
- document hierarchy preservation
- source-layout-aware retrieval
- chunking after structure

## Risk of Overreach

- 把“结构保留”误当“证据支持”。
- 为所有资料引入重解析，拖慢 ordinary capture。
- 对 ASR/视觉 OCR 的 UI 文案过度相信。

## Project Fit Refs

- VAKS: `adapt` as source intake / context-pack design pressure.
