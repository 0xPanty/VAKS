---
type: decision
status: active
created: 2026-05-26
decision_scope:
  - verified-vault
  - architecture-overview
  - alpha-design
confidence: high
---

# 架构全貌 v0.1：分层吸收，最终完整实现

## 当前总判断

我们现在要做的是一个可持续扩展的 verified knowledge system。它不是只做底层契约，也不是把外部工具排除在外；最终实现要完整吸收 Karpathy LLM Wiki / llm-wiki-compiler 这类系统的操作能力。

分层的目的不是缩小范围，而是防止运行时能力、搜索能力、viewer、API 反过来污染 verified truth layer。

## 当前分层

```text
1. 资料层 raw
   原始文章、repo、论文、播客、截图、日记、项目材料。

2. 编译层 wiki
   摘要、概念、术语、项目知识、结构化 wiki。

3. 验证层 claims / patterns / anti-patterns
   可采用设计、可验证主张、不可行路线、负面证据。

4. 关系层 graph / index / health
   双链、语义关系边、关联强度、索引、四信号关系评分、孤岛/桥接/冲突检查。

5. 搜索扩展层 qmd / future retrieval
   当 index 变大后，用本地混合检索找 raw/wiki 片段。

6. 调用层 API / context pack
   给 Agent 返回带来源、置信度、反例的上下文包。

7. 操作层 note workbench / skills
   当前笔记操作台、一键生成、一键整理、安全修改。

8. 应用层 products
   公众号、小红书、X、AI短剧脚本、项目产出。
```

## 已吸收设计的位置

| 来源 | 吸收点 | 所属层 | 当前状态 |
|---|---|---|---|
| Karpathy LLM Wiki | raw/wiki/schema、index/log、ingest/query/lint | 资料层/编译层/健康层 | 已采用 |
| Heinrich thinking vault | vault index、claim-style notes、purpose-specific philosophy | 编译层/关系层 | 已采用候选 |
| Yanhua 内容工厂 | Skills、source-to-publish pipeline、CLAUDE.md 工作流 | 操作层/应用层 | 候选 |
| Orange Book | CLAUDE.md + index.md、SCHEMA.md、folders/tags/links | 编译层/规则层 | 候选 |
| Obsidian Properties + Bases | YAML metadata、`.base` 视图、低代码筛选和复查 | 视图层/metadata 层 | 采用 |
| Obsidian-Base-Hub | `.base` 工作台、嵌入式局部视图、`+ New` 结构化入口 | 视图层/操作入口 | 适配，等 schema 稳定 |
| llm_wiki | purpose.md、四信号图谱、本地 API、review 队列 | 关系层/调用层/验证层 | 部分采用 |
| cc-note-ops | 当前笔记锁定、输出/修改分离、表达/结构分离 | 操作层 | 候选 |
| QMD | 本地 BM25 + vector + rerank 检索 | 搜索扩展层 | 观察 |
| nano-NotebookLM | BM25+FAISS+RRF、GraphRAG、generated graph overlay、embedding preset namespace | 搜索扩展层/关系操作层 | 观察/中期适配 |
| gbrain | Markdown system-of-record、compiled truth + timeline、facts/takes epistemology、schema packs、think + gaps、dream cycle | 验证层/关系层/调用层/健康层 | 适配，不 fork |
| obsidian-second-brain | AI-first note contract、传播规则、bi-temporal facts、index/log、context loader、health check、write validator | 操作层/维护层/上下文层 | 适配，不 fork |
| Misa relation-strength 建议 | `relations` 语义边：target/type/strength/confidence/evidence/rationale | 关系层/schema 层/context pack 排序 | 采用为 `SCHEMA.md v0.1` 候选 |
| 用户旧 Zilliz 方案 | 向量召回 + 原文回溯审计 | 搜索扩展层/验证层 | 观察 |

## 当前阿尔法方向

不是某一个工具，而是一条组合路线：

```text
Extensible Verified Action Knowledge System
  = Compiled Wiki
  + Evidence-backed Claims
  + Epistemic Status
  + Negative Evidence
  + Relation Scoring
  + Source Audit
  + Context Pack for Agents
  + Decision / Action Basis
  + Feedback Timeline
```

搜索工具、操作台、API 都是外围增强，不是核心。

## 当前不先做 / 不让它定义核心契约

- 不先做完整桌面 App，但最终可以有 viewer / Obsidian view。
- 不先做图谱 UI，但最终可以有 graph health 和可视化。
- 不先做 RAG / QMD / Zilliz 接入，但最终可以作为候选召回层。
- 不先做复杂 API，但最终要有 context pack API / MCP。
- 不把操作按钮塞进核心资料库。
- 不把 Bases 视图当成 truth layer。
- 不在 `SCHEMA.md` 未稳定前批量创建 `.base` 工作台。
- 不复制 gbrain 级别完整 runtime / MCP / OAuth / minions / scheduler。
- 不复制 obsidian-second-brain 的 background agent / scheduled agents / 自动 vault rewrite / 自动冲突裁决。
- 不在 schema 未稳定前做重型 HNSW / reranker / query cache 系统。

这些“不先做”不是“永远不做”。最终实现目标包含：

```text
ingest
compile
index / log
query
lint
review queue
provenance
context pack
API / MCP
viewer / Obsidian views
```

但每一项都必须服从：

```text
source -> summary -> claim -> pattern / anti-pattern -> decision -> context pack
```

## 当前要做

- 持续收集高质量资料。
- 每个资料提炼 source / summary / pattern / claim / anti-pattern。
- 每个设计点打标签和量化。
- 每次吸收外部点，都更新架构全貌。
- 定期做冲突检查：这个点属于哪一层，会不会污染核心？
- 在 `SCHEMA.md` 中吸收 gbrain 启发：fact / take / hypothesis / bet / decision、holder、confidence、valid_from、valid_until、evidence timeline、gaps。
- 在 `SCHEMA.md` 和 implementation blueprint 中吸收 obsidian-second-brain 启发：AI-first preamble、never-create-in-isolation、bi-temporal timeline、index/log、two-output rule、progressive context loading、health check。
- 在 `SCHEMA.md` 中把 `relations` 定为核心字段：每条边记录 target、type、strength、confidence、evidence、rationale；程序后续可从这些主记录派生 graph score、context pack ranking 和健康检查。
- 把 Karpathy LLM Wiki 的完整操作闭环纳入实现目标：`raw/`、`wiki/`、`index.md`、`log.md`、ingest、query、lint。
- 把 llm-wiki-compiler 的工程能力纳入实现目标：review queue、claim-level provenance、context pack、MCP/read-only API、viewer，但不采用其 generic page kinds 替代本资料库节点类型。
- 按 [[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]] 提升质量标准：最终系统要形成可信知识和行动依据，并通过 source adapters、schema packs、lint rule packs、retrieval engines、context pack modes、agent access tiers、feedback adapters 扩展。

## 后续全盘验证逻辑

等资料积累到一定量后，做一次总验证：

1. 哪些 pattern 被多源验证？
2. 哪些 pattern 只有单源，暂不采用？
3. 哪些 anti-pattern 反复出现，必须避开？
4. 哪些层已经足够稳定，可以自动化？
5. 哪些工具只是外围增强，不进入核心？
6. 哪些设计可以形成最小实现？

## 分寸原则

任何新工具或新库都先回答：

```text
它属于哪一层？
它解决当前真实问题吗？
它会不会增加核心复杂度？
不用它能不能先跑通？
以后能不能替换？
```

答不清楚，就只记录，不采用。
