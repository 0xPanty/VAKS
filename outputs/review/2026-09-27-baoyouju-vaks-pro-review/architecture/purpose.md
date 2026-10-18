---
type: vault_purpose
status: active
created: 2026-05-26
updated: 2026-05-27
scope:
  - multi-project-development
  - ai-short-drama
  - knowledge-compile
  - agent-context
review_cycle: weekly
---

# Purpose

这个 vault 的目标不是收藏资料，而是把高质量资料编译成可验证、可连接、可复用、可行动的知识系统。

最终目标不是比普通笔记库更整洁，而是比已分析的 LLM Wiki、知识编译器、agentic vault、RAG/search 方案都更可靠、更可拓展：既能形成可信知识，也能形成行动依据。

## 当前使命

服务两个长期方向：

1. 多项目开发：沉淀项目经验、库设计、架构判断、可行路线、踩坑和复盘。
2. AI 短剧和内容生产：沉淀素材、叙事结构、角色设定、视觉风格、平台发布经验。

共同目标是构造一个可被人和 Agent 调用的第二大脑：既有来源和证据，又有关系图谱、上下文、决策记录和行动反馈。

## 核心问题

- 哪些设计点真正值得吸收，而不是看起来高级？
- 哪些想法被多个优秀来源交叉验证？
- 哪些路线已经有负面证据，需要避开？
- 某个项目或创作任务需要调用哪些概念、模式、主张和反模式？
- 资料库如何持续扩展，而不是越来越乱？
- 哪些结论已经足够成为行动依据？
- 行动结果如何反馈回知识库，修正置信度和复查计划？

## 当前阶段

当前处于“设计采集和验证阶段”。

优先做：

- 收集高质量资料和开源库。
- 提炼 pattern / claim / anti-pattern。
- 给每条结论记录 source、evidence_level、verification_status、confidence。
- 用交叉验证找高信号方向。
- 把重要问答和阶段理解写入文件。

不先做：

- 完整桌面 App。
- 复杂图数据库。
- 一上来就做 RAG / vector search。
- 没有来源和验证状态的自动采纳。

这些不是永远不做。最终实现要包含 ingest、compile、index/log、query、lint、review queue、provenance、context pack、API/MCP、viewer/Obsidian view，但每一层都必须服从可信知识和行动依据的契约。

## 采用原则

一个设计点进入实践前，必须回答：

- 来源是什么？
- 解决什么真实问题？
- 和我们已有思路是否互相验证？
- 是否有反例或失败边界？
- 最小可行实现是什么？
- 怎么验证它真的有用？
- 如果以后出现更强方案，能不能替换？

## Agent 使用边界

Agent 可以读取并整理本 vault，但不能把未验证资料当成确定事实。

默认规则：

- 先读 `purpose.md` 理解当前目标。
- 再读 `wiki/indexes/knowledge-graph-index.md` 定位相关节点。
- 重要结论必须带来源和验证状态。
- 新发现写入 `outputs/qa/`、`wiki/claims/`、`wiki/patterns/` 或 `wiki/anti-patterns/`。
- 不确定内容进入 review 或标记 unverified。

## 成功标准

- 新资料进来后能被编译成结构化节点。
- 相似设计能被连起来，而不是散落。
- 高信号方向能被多源验证。
- 负面证据和踩坑能被主动查询。
- Agent 下次调用信息时能获得更完整的关系结构，而不是只拿零散片段。
- 重要 claim 能追溯证据、置信度、反例和复查时间。
- 重要 decision 能说明行动建议、风险、前提、回退和成功指标。
- 新 source adapter、retrieval engine、lint rule、context pack mode 或 agent 接入时，不需要改写 truth layer。
