---
type: candidate_pattern
status: active
pattern_id: visual-workbench-for-retrieval-diagnostics
created_at: 2026-06-05
truth_boundary: candidate pattern only; not reviewed knowledge
source_family_ids:
  - sf-rag-engineering
  - sf-obsidian-workflow
project_fit_refs:
  - outputs/review/project_borrowing_ledgers/VAKS.md
---

# Visual Workbench for Retrieval Diagnostics

## One-Line Pattern

把 intake、chunking、retrieval、rerank、context pack、tool call、answer draft、evaluation diagnostic 等过程可视化，帮助人定位失败环节。

## Problem Addressed

用户看到“回答离谱”时，很难知道问题出在来源、切分、召回、重排、prompt、上下文不足还是模型编造。

## Mechanism

- 用 canvas / inspector / timeline 展示流程节点。
- 显示 source anchor、retrieval hits、rerank、context assembly。
- 显示 diagnostic results，但明确不是 truth。
- 支持回源和逐层检查。

## Applicability

- RAGLab-style RAG canvas。
- VAKS future context-pack workbench。
- reviewer/operator surfaces。
- Obsidian local knowledge workflows。

## Non-Goals and Trade-Offs

- 可视化不是证据充分性。
- dashboard 不产生 truth confidence。
- UI 不能替代 reviewed relation。
- 对普通 query 不应过重。

## Derived From Sources

- `raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source.md`
- `raw/videos/2026-06-04-bilibili-dify-enterprise-knowledge-base-rag-source.md`
- `raw/videos/2026-06-04-bilibili-obsidian-one-page-workbench-source.md`
- `raw/repos/2026-06-04-langchain-miniopenclaw-source.md`

## Aliases or Near-Duplicates

- RAG canvas
- inspector workbench
- retrieval diagnostic cockpit
- transparent context pack

## Risk of Overreach

- 漂亮 UI 让人误以为流程可靠。
- 评估分数被误用为 truth。
- 一开始做太重，阻碍核心闭环。

## Project Fit Refs

- VAKS: `prototype`; good candidate for future workbench trial.
