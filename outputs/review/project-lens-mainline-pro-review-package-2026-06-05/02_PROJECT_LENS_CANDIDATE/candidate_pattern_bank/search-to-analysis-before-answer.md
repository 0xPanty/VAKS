---
type: candidate_pattern
status: active
pattern_id: search-to-analysis-before-answer
created_at: 2026-06-05
truth_boundary: candidate pattern only; not reviewed knowledge
source_family_ids:
  - sf-rag-engineering
project_fit_refs:
  - outputs/review/project_borrowing_ledgers/VAKS.md
---

# Search to Analysis Before Answer

## One-Line Pattern

检索之后不要立刻生成答案；先把候选材料组织成问题结构、论证结构、关系图、证据包或上下文 envelope，再回答。

## Problem Addressed

很多 RAG 失败不是没检索到东西，而是把散乱片段直接塞给模型，导致答案没有结构、证据不足、遗漏反例或混淆来源。

## Mechanism

- 检索后先做 outline / relation map / argument tree。
- 明确 source anchors、support/challenge/gap。
- 形成 answer draft 前的 context envelope。
- 对行动相关答案再跑 evidence sufficiency gate。

## Applicability

- complex RAG QA。
- evidence-aware answer drafting。
- VAKS context-pack preparation。

## Non-Goals and Trade-Offs

- 不要求每个普通查询都做完整论证树。
- 结构化分析不是 truth。
- LLM 生成的 outline 仍是 candidate。

## Derived From Sources

- `raw/videos/2026-06-04-bilibili-disco-rag-search-to-analysis-source.md`
- `raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source.md`
- `raw/videos/2026-06-04-bilibili-rag-seven-layer-architecture-source.md`

## Aliases or Near-Duplicates

- evidence envelope before answer
- outline-before-answer
- context pack drafting
- retrieval-to-reasoning pipeline

## Risk of Overreach

- 变成每次回答都很重。
- LLM 分析树看似严谨但没有证据支持。
- 把 answer draft 当 action basis。

## Project Fit Refs

- VAKS: `watch`; useful for high-impact answers only.

