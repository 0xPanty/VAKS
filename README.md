# 资料库

这个资料库不是普通收藏夹，而是一个本地 verified action knowledge system。

当前路线已经确认：

```text
外层像 Karpathy LLM Wiki 一样简单。
内层用 verified-action 规则保证可信和可行动。
其他参考库只作为可替换模块接入。
```

核心思路：

- `raw/`：原始资料区。文章、X 推文、论文、repo、截图、播客转录等先放这里，尽量保留原文和来源。
- `wiki/`：编译产物区。由 LLM/Codex 把 raw 里的资料整理成 summary、claim、pattern、anti-pattern、decision 和项目知识。
- `outputs/`：运行输出区。把和 AI 的重要问答、方案推导、健康检查报告落成 Markdown，避免结论死在聊天记录里。
- `products/`：发布成品区。X、公众号、小红书等面向读者的内容放这里，不和 wiki 混在一起。
- `templates/`：模板区。用于统一记录库分析、设计模式、阶段洞察、决策记录。
- `purpose.md`：资料库使命层。说明这个 vault 为什么存在、当前阶段优先级、采用原则和 Agent 使用边界。
- `ARCHITECTURE_PRINCIPLES.md`：架构原则层。规定主架构、分层职责、参考库吸收边界、采纳裁决和防四不像规则。
- `SCHEMA.md`：资料库结构契约。定义节点类型、通用字段、验证状态、关系边、晋级流程和自动化边界。

当前默认方案：

- 主骨架用 Karpathy-style LLM Wiki：`raw/`、`wiki/`、`index`、`log`、`ingest`、`query`、`lint`。
- Codex 作为默认 review/write gate，AI 和外部 agent 只能先生成 candidate。
- Obsidian 作为 IDE、图谱和人工 workbench。
- 严格字段藏在后台，只在晋级为 claim、pattern、decision、context pack 时启用。
- 暂时不急着上重型 RAG，先跑通 source -> candidate -> reviewed node -> context pack。

最小闭环：

1. 把新资料放进 `raw/`。
2. 生成 review candidate。
3. lint / review 后晋级到正式 `wiki/` 节点。
4. 需要行动时生成 context pack。
5. 行动结果回流为 feedback，更新 confidence、gaps、next_review。

开发阶段的新增原则：

- 每个阶段理解到的新思路都要落成可连接的知识节点。
- 后续遇到优秀开源库、产品、框架时，先提炼其优秀设计，再判断是否适合融合。
- 融合不是照搬。只有能解决真实问题、降低复杂度、增强现有工作流、并能被追溯验证的设计，才进入项目实践。
- 每条重要设计都应该能回答：来源是什么、解决什么问题、适合哪个项目、关联哪些概念、是否已经采用、采用后怎么验证。
- 不可行路线、踩坑、反模式也要记录。负面证据同样需要标签、交叉验证、失败条件和替代方案，后续统一设计前要主动查询。
- 资料库本身要保持可拓展和可演化。以后出现更强的新思路时，先进入采集和验证流程，通过比较、适配、迁移和回退机制再决定是否替换旧方案。
- 资料库需要可信度治理。资料和重要结论都要记录来源、验证状态、证据等级、置信度和复查时间，避免把未经验证的信息当成确定事实。
