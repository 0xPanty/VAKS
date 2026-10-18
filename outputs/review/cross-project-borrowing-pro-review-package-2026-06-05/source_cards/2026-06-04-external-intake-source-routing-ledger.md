---
type: source_routing_ledger
status: pilot
created_at: 2026-06-05
source_batch: 2026-06-04 external video/repo/paper intake
truth_boundary: routing hints only; candidate-only
---

# 2026-06-04 External Intake Source Routing Ledger

## 目的

这份 ledger 不是重写 source card，也不是判断 VAKS 应该采用什么。

它只做一件事：把 2026-06-04 已 intake 的视频、repo、paper 重新路由成：

```text
可迁移候选点
源内限定 / 不可泛化点
可能关联的 candidate pattern
可能路由到哪些 project borrowing ledger
source family
```

## Source Family

```text
sf-rag-engineering:
  RAG 工程、chunking、BM25、rerank、query rewriting、RAGLab、Dify、RAG 七层等。

sf-graph-ontology:
  GraphRAG / ontology / knowledge graph / Palantir / METHONTOLOGY 等。

sf-agent-workbench:
  miniopenclaw、OpenClaw、Karpathy LLM Wiki、Hermes/Obsidian、本地 AI 工作台等。

sf-memory-retrieval:
  RF-Mem、MemGAS、CoMe、个性化记忆、多粒度记忆、快慢检索等。

sf-obsidian-workflow:
  Obsidian 插件、第二大脑、本地知识库、单页工作台、使用门槛等。
```

## Routing Table

| Source | Source Family | Transferable Candidates | Source-Bound Constraints | Candidate Pattern Routes | Project Ledger Routes |
|---|---|---|---|---|---|
| `raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source.md` | sf-rag-engineering | visual RAG workbench; source structure; retrieval pipeline visibility; RAGAS as diagnostics | RAGLab UI and demo workflow are source-specific; RAGAS score is not truth | `visual-workbench-for-retrieval-diagnostics`, `source-structure-first-rag`, `retrieval-is-activation-not-truth` | VAKS: watch/adapt for future context-pack workbench |
| `raw/videos/2026-06-04-bilibili-rag-failure-chunking-rerank-prompt-source.md` | sf-rag-engineering | source structure before chunking; rerank/query expansion; prompt boundary | example metrics and tool names are unverified ASR/case claims | `source-structure-first-rag`, `retrieval-is-activation-not-truth` | VAKS: adapt as source-intake/context-pack pressure |
| `raw/videos/2026-06-04-bilibili-rag-back-to-bm25-sqlite-source.md` | sf-rag-engineering | retrieval-first not vector-first; BM25/SQLite/FTS baseline; local simple retrieval | not a universal rejection of vectors | `retrieval-is-activation-not-truth`, `simple-first-retrieval-baseline` | VAKS: watch/adapt for lightweight ordinary query |
| `raw/videos/2026-06-04-bilibili-disco-rag-search-to-analysis-source.md` | sf-rag-engineering | search-to-analysis pipeline; outline/relation map before answer | DISCO-RAG method claims not independently verified | `search-to-analysis-before-answer`, `retrieval-is-activation-not-truth` | VAKS: watch for evidence envelope/context-pack drafting |
| `raw/videos/2026-06-04-bilibili-rag-seven-layer-architecture-source.md` | sf-rag-engineering | layered RAG thinking; separating ingestion/retrieval/rerank/generation/eval | layer count and vendor framing may be marketing | `retrieval-is-activation-not-truth`, `visual-workbench-for-retrieval-diagnostics` | VAKS: routing only, no architecture adoption |
| `raw/videos/2026-06-04-bilibili-dify-enterprise-knowledge-base-rag-source.md` | sf-rag-engineering | enterprise KB workflow; RAG product surfaces; ingestion/retrieval/eval pressure | product-specific UI and workflow; may optimize for demo speed | `visual-workbench-for-retrieval-diagnostics`, `source-structure-first-rag` | VAKS: watch for workbench/user-facing friction |
| `raw/videos/2026-06-04-bilibili-rf-mem-user-memory-retrieval-source.md` | sf-memory-retrieval | familiarity vs recollection; fast/slow retrieval depth; uncertainty-guided activation | paper/video claims require paper anchors; applies mainly text memory | `adaptive-retrieval-depth`, `memory-granularity-and-quarantine` | VAKS: watch/adapt for activation tier and context pack budget |
| `raw/papers/2026-06-04-rf-mem-recollection-familiarity-source.md` | sf-memory-retrieval | probe retrieval; entropy/similarity as uncertainty proxy; budgeted recollection | metrics are benchmark context, not truth for VAKS | `adaptive-retrieval-depth` | VAKS: watch for activation strategy only |
| `raw/videos/2026-06-04-bilibili-memgas-multi-granularity-memory-source.md` | sf-memory-retrieval | multi-granularity memory; memory association structure | video-only/ASR entity uncertainty; not a memory truth layer | `memory-granularity-and-quarantine`, `adaptive-retrieval-depth` | VAKS: watch for memory/context organization |
| `raw/repos/2026-06-04-come-context-memory-source.md` | sf-memory-retrieval | bucket-tree memory; local retrieval; cooling/expiry; alias-only LLM payload | no local tests; not direct runtime adoption | `memory-granularity-and-quarantine`, `adaptive-retrieval-depth`, `file-first-agent-workbench` | VAKS: design-only watch |
| `raw/repos/2026-06-04-langchain-miniopenclaw-source.md` | sf-agent-workbench | file-first memory; prompt/skills/workspace as files; inspector; visible tool/retrieval stream | no license observed; no local runtime test; safety thin | `file-first-agent-workbench`, `skills-and-prompts-as-visible-files`, `agent-memory-quarantine` | VAKS: adapt as workbench idea, not runtime |
| `raw/videos/2026-06-04-bilibili-openclaw-karpathy-knowledge-base-source.md` | sf-agent-workbench | local AI knowledge base; Karpathy-style wiki/workbench | video framing and demo choices source-bound | `file-first-agent-workbench`, `skills-and-prompts-as-visible-files` | VAKS: watch for workbench/UI route |
| `raw/videos/2026-06-04-bilibili-karpathy-llm-wiki-not-recommend-source.md` | sf-agent-workbench | LLM-maintained wiki caution; AI wiki can solidify errors | anti-hype judgment not universal rejection | `file-first-agent-workbench`, `agent-memory-quarantine` | VAKS: record caution, no direct adoption |
| `raw/videos/2026-06-04-bilibili-hermes-obsidian-llm-wiki-source.md` | sf-agent-workbench | Obsidian + LLM wiki workflow; local file surface | project-specific Hermes framing | `file-first-agent-workbench`, `skills-and-prompts-as-visible-files` | VAKS: watch for local workbench |
| `raw/videos/2026-06-04-youtube-hermes-obsidian-source.md` | sf-agent-workbench | Obsidian as interface; local knowledge workflow | source-specific tooling | `file-first-agent-workbench` | VAKS: watch |
| `raw/videos/2026-06-04-bilibili-claude-code-obsidian-local-knowledge-base-source.md` | sf-obsidian-workflow | Office/PDF to Markdown; citation clickback; local KB as workbench | tutorial-specific workflow | `file-first-agent-workbench`, `source-structure-first-rag` | VAKS: adapt for source intake workbench |
| `raw/videos/2026-06-04-bilibili-obsidian-one-page-workbench-source.md` | sf-obsidian-workflow | one-page workbench; user-facing organization | UI preference source-bound | `visual-workbench-for-retrieval-diagnostics`, `file-first-agent-workbench` | VAKS: watch for reviewer/operator surfaces |
| `raw/videos/2026-06-04-bilibili-obsidian-8-plugins-source.md` | sf-obsidian-workflow | plugin ecosystem as capability source | plugin output is not authority | `file-first-agent-workbench`, `agent-memory-quarantine` | VAKS: watch, not truth |
| `raw/videos/2026-06-04-bilibili-obsidian-claude-second-brain-source.md` | sf-obsidian-workflow | AI-assisted second brain; daily synthesis/workflow | AI synthesis candidate-only | `file-first-agent-workbench`, `agent-memory-quarantine` | VAKS: watch |
| `raw/videos/2026-06-04-bilibili-ontology-methodology-knowledge-graph-source.md` | sf-graph-ontology | CQ; ontology methodology; knowledge graph relation discipline | lecture/source-specific wording; not direct ontology adoption | `graph-and-ontology-as-candidate-context`, `source-structure-first-rag` | VAKS: watch for Direction Review only |
| `raw/papers/2026-06-04-methontology-source.md` | sf-graph-ontology | competency questions; intermediate representations; evaluation ledger | older methodology; heavy if copied wholesale | `graph-and-ontology-as-candidate-context` | VAKS: adapt as review/evaluation inspiration only |
| `raw/videos/2026-06-04-bilibili-palantir-ontology-multi-agent-source.md` | sf-graph-ontology | ontology/object-action model; multi-agent coordination through semantic layer | enterprise/Palantir-specific; not source truth | `graph-and-ontology-as-candidate-context`, `agent-memory-quarantine` | VAKS: watch |
| `raw/videos/2026-06-04-bilibili-obsidian-exam-knowledge-graph-source.md` | sf-graph-ontology | graph view for study/exam knowledge; relation visualization | visual graph is not reviewed relation | `graph-and-ontology-as-candidate-context`, `visual-workbench-for-retrieval-diagnostics` | VAKS: watch |
| `raw/videos/2026-06-04-bilibili-notion-vs-obsidian-system-source.md` | sf-obsidian-workflow | system choice trade-offs; local vs cloud/workflow fit | comparison is user/workflow-specific | `file-first-agent-workbench` | VAKS: watch |
| `raw/videos/2026-06-04-bilibili-obsidian-usage-barriers-source.md` | sf-obsidian-workflow | user friction; setup burden; workflow adoption risk | experience-specific | `visual-workbench-for-retrieval-diagnostics` | VAKS: watch for UX burden |

## 防污染提醒

- `source_family_id` 用来避免“同一个家族的多个材料 = 多个独立支持”的错觉。
- 本表里的 pattern route 只是路由建议，不是 support。
- Project ledger route 只是“可能值得项目看”，不是项目采用。

