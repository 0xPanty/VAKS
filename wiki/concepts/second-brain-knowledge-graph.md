---
type: concept
status: active
created: 2026-05-26
aliases:
  - 第二大脑
  - 知识图谱
  - knowledge graph
related:
  - "[[positive-design-fusion]]"
  - "[[library-design-extraction]]"
---

# 第二大脑知识图谱

## 定义

第二大脑不是单纯存资料，而是把项目、概念、决策、问题、来源、问答和产出连接成一张可查询的关系网。

核心目标：

- 下次调用某个信息时，不只拿到单点资料，还能看到上下文、来源、相关项目、历史决策和风险。
- 把开发阶段的新理解持续沉淀下来，避免每次从零开始分析。
- 让 AI 能基于用户自己的历史项目和知识结构做更完整的判断。

## 节点类型

- `Source`：原始资料，如文章、X 推文、论文、repo、视频、播客。
- `Library`：被分析的优秀库、框架、产品或工具。
- `Concept`：抽象概念，如 RAG、知识编译、增量索引。
- `Pattern`：可复用设计模式，如插件架构、事件驱动、任务队列。
- `Project`：用户自己的项目。
- `Decision`：关键技术或产品决策。
- `Problem`：踩坑、瓶颈、约束或失败案例。
- `Workflow`：可重复执行的工作流。
- `Output`：AI 问答、复盘、报告、内容成品。

## 关系类型

- `Source -> supports -> Concept`
- `Library -> demonstrates -> Pattern`
- `Pattern -> applies_to -> Project`
- `Project -> has_problem -> Problem`
- `Decision -> based_on -> Source/Concept/Pattern`
- `Problem -> solved_by -> Decision/Pattern`
- `Output -> references -> Source/Concept/Project`
- `Concept -> related_to -> Concept`

## Obsidian 实现方式

- 用 `[[双链]]` 记录显性关系。
- 用 Properties 记录结构化字段，如 `type`、`status`、`source_url`、`related_projects`、`patterns`。
- 用 Bases 查看不同节点集合，如项目库、模式库、库分析库、决策库。
- 用 LLM 定期补链接、查重复、查冲突、查孤岛节点。

## 使用原则

不要为了图谱而图谱。关系图只是展示层，真正有价值的是节点质量和关系质量。

每个重要节点至少要具备：

- 清楚定义。
- 来源或证据。
- 关联项目或适用场景。
- 当前状态。
- 后续行动或验证方式。

