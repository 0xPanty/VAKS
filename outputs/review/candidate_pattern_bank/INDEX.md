---
type: candidate_pattern_bank_index
status: pilot
created_at: 2026-06-05
truth_boundary: candidate patterns only; not reviewed knowledge; not project decisions
---

# Candidate Pattern Bank Pilot

这是跨项目候选模式库试点。它的作用不是判真，也不是替 VAKS 做架构决策，而是把外部资料中明显可复用、可能跨项目出现的机制抽成少量候选模式。

Pro 调研后的降重口径：

```text
通用原子知识点才是可复用层的主角。
Candidate Pattern Bank 只收更高阶、反复出现、问题中心明确的模式。
```

## 什么能进

一个候选模式必须回答：

- 它解决什么问题？
- 它的机制是什么？
- 它适用于什么情况？
- 它不适用于什么情况？
- 它从哪些 source / source family 抽象出来？
- 它有哪些近义词或重复表达？
- 它有哪些越权风险？

## 什么不能进

- 一次性事实。
- 只在某个工具按钮或某个视频教程里成立的做法。
- 没有 problem statement 的漂亮名词。
- 不能回源的 AI 总结。
- 只是 VAKS 自己想做的功能。
- 每个通用原子知识点的简单复制。
- 只有名字好听、但没有 recurring problem / mechanism / boundary 的标签墙。

## 状态

```text
draft:
  刚抽出，还需要合并/命名/补来源。

active:
  作为候选模式继续保留，适合被项目 ledger 引用。

parked:
  暂时不处理，价值不够或太模糊。

superseded:
  被更清晰的候选模式替代。
```

注意：这里不用 `adopted`。采用是某个项目的姿态，应该写在 Project Lens sidecar，不写在全局候选模式库。

## Patterns

| Pattern | Status | Problem | Main Source Families |
|---|---|---|---|
| [[source-structure-first-rag]] | active | RAG/检索前丢失原文结构，导致召回和回答失真 | sf-rag-engineering, sf-obsidian-workflow, sf-graph-ontology |
| [[retrieval-is-activation-not-truth]] | active | 检索命中、rerank、GraphRAG 层容易被误读成 truth/support | sf-rag-engineering, sf-memory-retrieval, sf-graph-ontology |
| [[file-first-agent-workbench]] | active | Agent/LLM 工作台黑盒，prompt/memory/tool trace 不可审阅 | sf-agent-workbench, sf-obsidian-workflow |
| [[adaptive-retrieval-depth]] | active | 所有查询都走同样检索深度，成本和召回都不稳 | sf-memory-retrieval, sf-rag-engineering |
| [[memory-granularity-and-quarantine]] | active | 记忆粒度、更新和 agent 写入容易污染长期知识 | sf-memory-retrieval, sf-agent-workbench |
| [[graph-and-ontology-as-candidate-context]] | active | 图谱/本体/社区摘要容易被误当 reviewed relation | sf-graph-ontology, sf-rag-engineering |
| [[visual-workbench-for-retrieval-diagnostics]] | active | 检索/上下文流程不可见，用户无法定位失败环节 | sf-rag-engineering, sf-obsidian-workflow |
| [[skills-and-prompts-as-visible-files]] | active | 技能、prompt、角色设定藏在代码或模型上下文里，不可复盘 | sf-agent-workbench |
| [[search-to-analysis-before-answer]] | active | 检索结果直接生成答案，缺少结构化分析和证据组织 | sf-rag-engineering |
| [[simple-first-retrieval-baseline]] | draft | 过早使用复杂向量/图检索，忽略 BM25/SQLite/FTS 等简单基线 | sf-rag-engineering |

## 与 Project Ledger 的关系

Candidate Pattern Bank 只说“这个模式可能有跨项目价值”。某个项目是否可能借、借到哪里、为什么先这么看，主记录写在：

```text
outputs/review/project_lens_overlays/
```

旧 Project Borrowing Ledger 目录只作为派生视图：

```text
outputs/review/project_borrowing_ledgers/
```
