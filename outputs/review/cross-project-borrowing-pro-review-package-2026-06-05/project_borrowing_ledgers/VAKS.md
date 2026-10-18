---
type: project_borrowing_ledger
status: pilot
project_id: VAKS
project_name: Verified Action Knowledge System / 资料库
created_at: 2026-06-05
truth_boundary: project fit ledger only; not reviewed knowledge; not ADR; not action basis
---

# VAKS Project Borrowing Ledger

## 边界

这份 ledger 记录 VAKS 对 candidate patterns 的项目姿态。

它不是：

- source card；
- reviewed knowledge；
- architecture decision；
- action basis；
- truth confidence；
- 自动 promotion。

`watch / prototype / adapt / reject` 只是项目借鉴姿态。真正进入主架构、reviewed relation 或 action basis，必须另走 review / decision。

## Entries

| Pattern | Disposition | Target Locus | Why Fit / Not Fit | Required Gates Before Promotion |
|---|---|---|---|---|
| `source-structure-first-rag` | adapt | future source intake, context-pack preparation, retrieval workbench | VAKS 的 raw/source/candidate/review 边界要求保留原文结构；RAG 资料反复显示机械切分会污染后续检索和理解 | Direction Review; source card template update review; evidence-aware review if promoted to architecture principle |
| `retrieval-is-activation-not-truth` | adapt | MEMORY_TIER, context-pack rules, review queue wording | 这已经与 VAKS 核心边界一致；新资料只是增加重复设计压力 | Already aligned with main boundary; still needs wording review before any template patch |
| `file-first-agent-workbench` | watch | future dev context viewer, workbench, inspector surfaces | miniopenclaw / Obsidian / Karpathy 类资料显示文件可见性有价值，但 VAKS 不能让 memory/tool output 越权 | UI/workbench prototype; agent memory quarantine review; tool-safety review |
| `adaptive-retrieval-depth` | watch | activation tier, context-pack budget, query mode selection | RF-Mem/CoMe 表明快慢检索和预算控制有价值；但 VAKS 目前不需要重检索 runtime | Direction Review; small retrieval simulation; cost/latency/usefulness ledger |
| `memory-granularity-and-quarantine` | watch | MEMORY_TIER, feedback ledger, future agent memory write path | 多粒度记忆有用，但 agent 写入风险高；更像 quarantine / review_due 设计压力 | agent memory quarantine review; feedback boundary review; no direct truth mutation |
| `graph-and-ontology-as-candidate-context` | watch | relation review, optional point graph fragments, context-pack neighborhood | 本体/GraphRAG/Palantir 资料有助于组织候选关系，但不能自动创建 reviewed relation | evidence-aware relation review; relation schema sanity check; no graph rank as trust |
| `visual-workbench-for-retrieval-diagnostics` | prototype | future reviewer/operator workbench, context-pack diagnostics | RAGLab 和 Obsidian 工作台显示可视化流程能帮助定位失败；适合先做轻量原型 | UX prototype; diagnostic-not-truth labeling; no dashboard-as-confidence |
| `skills-and-prompts-as-visible-files` | watch | future agent workbench, skill registry, prompt component files | 可见 skill/prompt 降低黑盒，但 prompt/skill 可编辑会引入写入污染 | agent tool-safety review; skill write quarantine; no auto-promotion |
| `search-to-analysis-before-answer` | watch | context-pack drafting, evidence envelope preparation | DISCO-RAG 类资料提示先组织分析再回答；适合做 answer drafting 改良 | evidence envelope review; ordinary query lightweighting check |
| `simple-first-retrieval-baseline` | watch | ordinary query, lightweight capture/query | BM25/SQLite/FTS baseline 可降低复杂度；但不应反向否定向量/图检索 | small local retrieval baseline test; scope fit review |

## 明确不借

- 不借任何把 retrieval score / rerank / dashboard / feedback heat 当 truth confidence 的做法。
- 不借任何把 AI summary 直接写成 reviewed knowledge 的做法。
- 不借任何把 source family 多报告当独立支持数的做法。
- 不借 terminal tool 只靠简单 blacklist 的安全边界。
- 不借“single source of truth”把 raw / insight / decision 全揉在一起的 framing。

## 当前结论

这个 ledger 证明三层拆分有实际用处：同一个 candidate pattern 可以同时被多个 source family 支持为“设计压力”，但 VAKS 的借鉴姿态和限制必须单独写。

下一步不是主架构改版，而是继续用这个 ledger 跑几轮外部资料 intake，看它是否减轻 source card 里的项目化判断负担。

