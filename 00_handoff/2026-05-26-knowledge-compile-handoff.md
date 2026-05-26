# 2026-05-26 资料库 handoff：Obsidian + LLM 知识编译系统

> 2026-05-27 更新：本文件已不是最新恢复入口。后续窗口优先读 `00_handoff/2026-05-27-verified-action-knowledge-system-handoff.md`。当前主架构已升级为 `Verified Action Knowledge System`，目标是融合 Karpathy LLM Wiki、llm-wiki-compiler、gbrain、obsidian-second-brain 等设计，形成可拓展的可信知识与行动依据系统。

## 当前结论

用户适合做 Obsidian 类资料库，但不应该做成普通收藏夹或复杂 PKM 玩具。更合适的方向是：

> 把资料库当成本地知识代码仓库，把 LLM 当编译器，把 Obsidian 当 IDE。

也就是：原始资料进入 `raw/`，LLM 增量整理成 `wiki/`，重要问答和检查结果沉淀到 `outputs/`。

## Karpathy 思路的大白话总结

普通资料库是在囤东西：

```text
看到好东西 -> 剪藏 -> 放进笔记库 -> 以后自己找
```

Karpathy 的思路是在炼东西：

```text
看到好东西 -> 放进 raw 原料区 -> 让 LLM 定期整理 -> 生成 wiki 知识区 -> 以后直接查结构化知识
```

核心不是“我有多少笔记”，而是“这些资料有没有被编译成以后能直接用的知识”。

## 三层结构

```text
raw/       原始资料，不轻易改
wiki/      LLM 编译后的知识条目、摘要、概念、索引
outputs/   AI 问答、方案推导、健康检查报告
```

保留 `products/` 是因为用户未来要做 AI 短剧和内容发布，成品内容需要和自用知识分开：

```text
products/x/
products/公众号/
products/小红书/
```

## 工具判断

当前推荐主方案：

```text
Obsidian 原生 Properties + Bases
```

理由：

- 官方核心插件，长期更稳。
- 数据仍然是本地 Markdown + YAML Properties。
- 适合做项目库、短剧库、角色库、素材库、提示词库、复盘库。
- 对多项目开发者很友好，后续也适合 Git 管理和 AI 读取。

辅助工具判断：

- Dataview：后续需要复杂查询、任务聚合、内联字段时再加。
- Datacore：前沿但偏 power user，暂时不作为第一阶段主力。
- RAG：不要一开始就上。先用索引文件 + LLM 直接读 Markdown。等笔记规模到一万级、搜索明显不够时再考虑。

## 第一版目录

```text
raw/
  articles/
  x/
  papers/
  repos/

wiki/
  indexes/
  concepts/
  summaries/

outputs/
  qa/
  health/

products/
  x/
  公众号/
  小红书/
```

## 后续建议

下一步可以补 4 类模板：

1. `raw` 原始资料模板：来源、作者、发布时间、采集时间、主题标签。
2. `wiki/summaries` 摘要模板：核心结论、证据、疑点、可复用点。
3. `wiki/concepts` 概念模板：定义、适用场景、反例、来源。
4. `outputs/qa` 问答模板：问题、结论、推理、引用来源、不确定性。

再下一步可以创建 Obsidian Bases：

```text
项目库.base
短剧库.base
角色库.base
素材库.base
提示词库.base
复盘库.base
```

## 2026-05-26 追加：开发阶段知识图谱与优秀库正向融合

用户进一步明确：现在处在开发阶段，每个阶段理解到的新思路都应该记录下来。后续还会找很多优秀库、框架、产品或论文，希望提炼每个库的优秀设计，把它们和自己的项目、AI 短剧生产、资料库系统串起来。

这不是简单收藏，而是构建第二大脑：

```text
Source/Library -> Concept/Pattern -> Project/Decision/Problem -> Output
```

关键原则：

- 新理解要记录为可连接的知识节点。
- 当前处于开发阶段，先持续记录优秀设计点和上下文，不急着马上落地。
- 优秀库要先提炼设计，积累足够样本后，再从全貌角度综合理解和取舍。
- 每个重要设计点都要量化打标签，并寻找相似思路、相似库、论文证据或历史项目影子做交叉验证。
- 借鉴点进入落地候选前，必须记录来源、支持证据、反例、风险和最小验证方式。
- 不可行路线、踩坑、反模式也要记录，并同样打标签、交叉验证、记录失败条件和替代方案。
- 最终目标是科学、合理地应用采纳，等样本足够后再统一设计，而不是边看边拼贴。
- 整个体系必须保持可拓展、可演化。以后出现更强的新思路时，先进入采集、验证、比较、迁移和回退流程，而不是推翻整个系统。
- 融合不是照搬，也不是看到厉害就加。
- 只有能解决真实问题、降低复杂度、增强现有工作流、可验证、可回退的设计，才算正向融合。

已新增：

- `wiki/concepts/second-brain-knowledge-graph.md`
- `wiki/concepts/library-design-extraction.md`
- `wiki/concepts/positive-design-fusion.md`
- `wiki/concepts/staged-design-harvest-and-synthesis.md`
- `wiki/concepts/evidence-backed-design-validation.md`
- `wiki/concepts/negative-evidence-and-avoidance.md`
- `wiki/concepts/evolvable-design-system.md`
- `wiki/concepts/obsidian-ai-integrated-production-system.md`
- `wiki/concepts/source-verification-and-trust-model.md`
- `wiki/indexes/knowledge-graph-index.md`
- `templates/library-review.md`
- `templates/anti-pattern.md`
- `templates/design-pattern.md`
- `templates/development-insight.md`
- `templates/decision-record.md`
- `templates/source-record.md`
- `templates/claim-record.md`
- `raw/articles/2026-01-thinking-os-with-ai-vault-source.md`
- `wiki/summaries/2026-01-thinking-os-with-ai-vault.md`
- `wiki/patterns/agentic-vault-orientation-index.md`
- `wiki/patterns/purpose-specific-vault-philosophy.md`
- `wiki/patterns/composable-claim-notes.md`
- `wiki/claims/vault-index-guides-context-loading.md`
- `wiki/claims/each-vault-needs-purpose-specific-philosophy.md`
- `wiki/anti-patterns/overgrown-always-on-instructions.md`
- `outputs/qa/2026-05-26-thinking-os-vault-analysis.md`
- `raw/articles/2026-05-obsidian-claude-ai-superbrain-content-factory-source.md`
- `wiki/summaries/2026-05-obsidian-claude-ai-superbrain-content-factory.md`
- `wiki/patterns/source-to-publish-content-pipeline.md`
- `wiki/patterns/skills-as-action-modules.md`
- `wiki/patterns/container-intelligence-hands-architecture.md`
- `wiki/claims/purpose-specific-vaults-change-the-system-goal.md`
- `wiki/claims/skills-turn-knowledge-vaults-into-action-systems.md`
- `wiki/anti-patterns/yolo-permissions-for-production-vault.md`
- `outputs/qa/2026-05-26-yanhua-superbrain-content-factory-analysis.md`
- `wiki/patterns/verified-vault-api-for-agent-brain.md`
- `wiki/claims/verified-vault-api-should-stay-separate-from-agent-gbrain.md`
- `wiki/anti-patterns/do-not-blindly-merge-vault-and-agent-brain.md`
- `outputs/qa/2026-05-26-verified-vault-api-for-agent-gbrain.md`
- `raw/repos/2026-05-26-obsidian-ai-orange-book-source.md`
- `wiki/summaries/2026-05-26-obsidian-ai-orange-book-architecture-review.md`
- `wiki/patterns/claude-md-index-md-navigation-layer.md`
- `wiki/patterns/schema-md-as-ai-wiki-contract.md`
- `wiki/patterns/lifecycle-folders-topic-tags-relationship-links.md`
- `wiki/claims/orange-book-is-guide-not-turnkey-vault-template.md`
- `wiki/anti-patterns/markdown-only-vault-for-media-heavy-production.md`
- `outputs/qa/2026-05-26-second-brain-design-fusion.md`
- `outputs/qa/2026-05-26-obsidian-ai-series-integration.md`

## 2026-05-26 追加：Yanhua Obsidian + AI 系列整合判断

用户提到 Yanhua 的三篇延伸文章：

- 《如何基于 Obsidian 和 Claude 打造 AI 时代超级大脑？》
- 《Obsidian + Claude Code：你的笔记库就是你最强大的 AI 上下文》
- 《我用 Podwise 把播客变成了可检索的知识库》

当前判断：这三篇和 Karpathy 的 LLM Knowledge Bases 工作流不冲突，可以按同一套系统的不同层来理解。

分层如下：

```text
Podwise 文章
  = 信息摄取层，把播客/音频/视频变成结构化 Markdown 原料

Karpathy 工作流
  = 知识编译治理层，raw -> wiki -> outputs，加索引、摘要、概念、健康检查

Obsidian + Claude Code 上下文文章
  = 上下文激活层，让笔记库成为 AI 的长期上下文

超级大脑文章
  = 工作流执行层，用 CLAUDE.md + Skills + Claudian/Claude Code 把资料变成成品
```

统一链路：

```text
信息摄取 -> 知识编译 -> AI 上下文激活 -> 工作流执行 -> 成品输出 -> 复盘和健康检查
```

风险边界：

- `wiki/` 和 `products/` 必须分开，避免知识库被成品污染。
- 不要把整个 Vault 无脑塞给 AI，应先读索引再读相关原文。
- Podwise 摘要不能替代原始转录。
- 早期不要开太激进的自动发布/自动修改权限。

证据状态：

- Karpathy 工作流文章已通过 Rattibha 镜像较完整读取。
- 超级大脑文章已通过 Lumina/ClawHow 镜像较完整读取。
- 上下文文章和 Podwise 文章目前只看到标题级定位，后续需要全文确认。

## 2026-05-26 追加：资料来源验证与可信度治理

用户明确：资料库不能是一堆未经验证的垃圾信息。资料本身也要打标签、量化、记录消息来源、验证状态、置信度和证据等级。

当前判断：这个思路合理，而且外部已有类似成熟思想：

- Zettelkasten 区分临时笔记、文献/来源笔记、永久笔记，强调来源和自有理解的转换。
- Obsidian Properties/Bases 支持把结构化字段写入 Markdown，并以数据库视图筛选和排序。
- 知识图谱研究里有 provenance、confidence、claim verification 等方向，用于追踪来源、解释答案和判断可信度。

本资料库采用：

```text
Source 来源记录
  = 资料从哪里来、作者是谁、来源质量如何、是否过时

Claim 主张记录
  = 某条具体结论是什么、有哪些来源支持、是否有反例、置信度多少
```

关键字段：

- `source_status`
- `evidence_level`
- `verification_status`
- `confidence`
- `source_quality`
- `cross_source_count`
- `last_verified`
- `next_review`

新增：

- `wiki/concepts/source-verification-and-trust-model.md`
- `templates/source-record.md`
- `templates/claim-record.md`

原则：资料可以先进入 `unverified`，但重要结论进入设计、决策或生产流程前，必须有来源、验证状态、证据等级、风险/反例和复查计划。

## 2026-05-26 追加：一月 AI Thinking OS / Vault 文章分析

用户提供一篇一月文章，主题是“用 Claude Code 运行 Obsidian vault，构建 thinking with AI 的操作系统”。用户提醒可能有点落后。

处理方式：

- 按单来源资料记录，不把工具细节直接当事实。
- 只提炼稳定设计思想。
- 用官方 Claude Code docs / Obsidian docs / Karpathy 工作流做初步交叉验证。

高信号设计点：

- `vault index` 作为 agent 的上下文路由器：先读索引，再按需读 notes。
- 每个 vault 需要自己的 `philosophy`：不同目的对应不同规则，不能照搬通用模板。
- 笔记要 `claim-style` 且可组合：标题尽量表达判断，链接自然嵌入句子。
- Agent 操作流程应先 orientation，再读 index/topic page/相关 notes，再修改。
- Markdown 是底座，Obsidian/Claude Code 是窗口和操作层。

已沉淀：

- `wiki/patterns/agentic-vault-orientation-index.md`
- `wiki/patterns/purpose-specific-vault-philosophy.md`
- `wiki/patterns/composable-claim-notes.md`
- `wiki/claims/vault-index-guides-context-loading.md`
- `wiki/claims/each-vault-needs-purpose-specific-philosophy.md`
- `wiki/anti-patterns/overgrown-always-on-instructions.md`

风险：

- 一月文章的具体 hooks 写法可能过时。
- `CLAUDE.md` 约 2000 行不是目标，可能形成常驻指令膨胀。
- “每条 note 都是 skill”是类比，不应机械化执行。
- Agent 自动写 topic page breadcrumb 需要人工审查。

## 2026-05-26 追加：Yanhua 超级大脑 / 内容工厂文章分析

用户提供 Yanhua 根据 Heinrich 一月英文文章写出的实践文章。核心差异：Heinrich 用 vault 做深度思考系统，Yanhua 用同一套底层模式做多平台内容生产流水线。

当前判断：这篇是高信号，因为它交叉验证了“每个 vault 要按目的定制”的方向。

高信号设计：

- `purpose-specific vault transformation`：同样的 Markdown vault + AI agent + instructions + skills，可以变成 thinking OS，也可以变成 content factory，用户这里可以变成开发 + AI短剧生产系统。
- `skills as action modules`：Skills 把知识库从“能被 AI 读取”推进到“能被 AI 执行动作”，如网页转 Markdown、配图、发布、格式转换。
- `source-to-publish pipeline`：信息源进入后，经 AI 初稿、人工编辑、自动配图、多平台发布，形成完整生产链。
- `CLAUDE.md as operating manual`：把身份、读者、风格、短板、质量标准、工作流和错误教训文字化。
- `human judgment gate`：AI 可以快速产出，但人决定什么值得留下和发布。

已沉淀：

- `wiki/patterns/source-to-publish-content-pipeline.md`
- `wiki/patterns/skills-as-action-modules.md`
- `wiki/patterns/container-intelligence-hands-architecture.md`
- `wiki/claims/purpose-specific-vaults-change-the-system-goal.md`
- `wiki/claims/skills-turn-knowledge-vaults-into-action-systems.md`
- `wiki/anti-patterns/yolo-permissions-for-production-vault.md`

风险：

- 默认 yolo 权限不可取，应只在低风险、受限目录、可回退任务中局部使用。
- 平台自动发布属于高风险动作，需要人工确认和回退。
- Skills 数量增长会带来维护债，需要版本、权限和测试。
- 内容流水线没有质量 gate 会加速低质量内容生产。

工具复核：

- Claudian GitHub README 当前支持 Claude Code/Codex/Opencode agent 嵌入 Obsidian、BRAT 安装、Skills、slash commands、@mention 等。
- Claude Code 官方文档支持项目级 `.claude/skills/` 和权限模式。

## 2026-05-26 追加：Verified Vault API for Agent + gbrain

用户提出：我们的笔记是已经提炼好的知识库，gbrain 是给 AI 认识关系图谱、储存自己对世界认知的系统。等资料库做好后，是否可以给 agent 一个 API 来调用我们的知识库内容，再结合它自己的 gbrain。

当前判断：合理，而且是高信号中期方向。

关键边界：

```text
Verified Vault
  = 用户确认、来源可追溯、带验证状态的 compiled knowledge

Agent gbrain
  = agent 自己的关系图谱、世界模型、任务经验和推理结构

Session
  = 当前任务的短期上下文和目标
```

三者不应混成一锅，应通过 API / resolver / context pack 连接。

合理链路：

```text
用户问题
  -> agent 判断需要哪些知识
  -> 调用资料库 API
  -> 返回 concepts / patterns / claims / anti-patterns
  -> 每条带 sources / evidence_level / confidence / negative_evidence
  -> agent 结合 gbrain 和当前 session 推理
  -> 输出结论
  -> 新洞察回写 outputs/qa 或 candidate claim
```

中期 API 候选：

- `GET /search?q=`
- `GET /node/{id}`
- `GET /related/{id}`
- `GET /claims?topic=`
- `GET /anti-patterns?topic=`
- `POST /context-pack`

短期不急着搭完整服务。先用 Markdown index + 脚本/agent 读文件模拟 API，等资料库有足够节点后再考虑本地 HTTP API、MCP、graph query 或 RAG。

已沉淀：

- `wiki/patterns/verified-vault-api-for-agent-brain.md`
- `wiki/claims/verified-vault-api-should-stay-separate-from-agent-gbrain.md`
- `wiki/anti-patterns/do-not-blindly-merge-vault-and-agent-brain.md`
- `outputs/qa/2026-05-26-verified-vault-api-for-agent-gbrain.md`

## 2026-05-26 追加：alchaincyf/obsidian-ai-orange-book 结构样本分析

用户提供 GitHub 仓库 `alchaincyf/obsidian-ai-orange-book`，并说明自己已经 fork，询问其设计思路和是否比较全。

检查方式：

- 浅克隆 GitHub 仓库到本地临时目录。
- 查看 README、README_en、文件树、最新 commit。
- 用 `pypdf` 抽取中文 PDF 文本，重点检查 §05 Vault 架构、§06 AI 维护知识库、§07 工作流、§09 进阶。
- 浏览 GitHub 页面和 `kepano/obsidian-skills` 页面做部分交叉验证。

当前判断：

```text
它作为“Obsidian + Claude Code 指南 / 架构样本”比较全；
它作为“可直接 fork 后使用的完整 vault 模板”不全。
```

仓库事实：

- 根目录只有 README、PDF、assets、screenshots。
- 没有实际 `CLAUDE.md`、`SCHEMA.md`、`.claude/skills/`、`.base`、示例 notes/wiki。
- GitHub 页面检查时显示约 956 stars、90 forks、6 commits。

高信号设计：

- `CLAUDE.md + index.md` 导航层：根规则 + 目录索引，帮助 AI 以低 token 理解 vault。
- `SCHEMA.md as AI wiki contract`：用 schema 固定命名、frontmatter、标签、链接、文章结构、索引更新。
- `folders / tags / links` 三分法：文件夹管生命周期，标签管主题，双链管关系。
- `raw -> wiki -> output`：和我们当前 `raw -> wiki -> outputs/products` 方向一致。
- `Git as audit/rollback layer`：AI 写入后用 git diff 审查和回退。
- `Skills 小范围测试原则`：触发条件明确、范围限定、输出格式指定、先小范围测试。

需要修正/不照搬：

- 它的 frontmatter 五字段过轻，不包含我们需要的 source_status、evidence_level、confidence、negative_evidence、last_verified。
- “Markdown 是唯一格式”对纯知识 vault 合理，但对 AI短剧/媒体资产库过严，应改成：文本和 metadata 用 Markdown，媒体放 assets/attachments/products 并保留 source record。
- 40 万字以内不需要向量数据库是经验边界，不是硬定律。
- 书中部分 stars、收购、生态数字属于易变信息，不能直接当长期事实。

已沉淀：

- `raw/repos/2026-05-26-obsidian-ai-orange-book-source.md`
- `wiki/summaries/2026-05-26-obsidian-ai-orange-book-architecture-review.md`
- `wiki/patterns/claude-md-index-md-navigation-layer.md`
- `wiki/patterns/schema-md-as-ai-wiki-contract.md`
- `wiki/patterns/lifecycle-folders-topic-tags-relationship-links.md`
- `wiki/claims/orange-book-is-guide-not-turnkey-vault-template.md`
- `wiki/anti-patterns/markdown-only-vault-for-media-heavy-production.md`

## 2026-05-26 追加：nashsu/llm_wiki 实现级参考架构分析

用户提供 GitHub 仓库 `nashsu/llm_wiki`，截图中提到四信号知识图谱、Louvain 社区检测、Chrome 插件、Obsidian 兼容。用户要求按我们的提炼思路深挖其价值。

检查方式：

- Git clone 因 TLS handshake 失败，随后用 GitHub zip 下载成功。
- 解压到本地临时目录。
- 查看 README、`llm-wiki.md`、`package.json`、`src/lib/graph-relevance.ts`、`src/lib/graph-insights.ts`、`src-tauri/src/api_server.rs`。

当前判断：

```text
llm_wiki 不是普通 Obsidian 模板，也不只是方法论文章；
它是 Karpathy LLM Wiki 模式的实现级参考架构。
```

新设计增量：

- `purpose.md`：把知识库使命层和 `schema.md` 结构规则分开。
- 四信号关系图谱：direct link、source overlap、Adamic-Adar common neighbor、type affinity。
- 图谱健康检查：孤岛节点、低内聚社区、桥接节点、意外连接。
- Local Verified Vault API：本地 `127.0.0.1:19828` API 给 Agent 调用 search/file/graph/rescan。
- 异步 review 队列：AI 提出待判断项，人类异步确认。
- 来源生命周期：source watch、SHA256 cache、source rescan、stale/cleanup 思路。

对我们当前路线的影响：

- 强力验证“资料库 API + agent gbrain”的中期方向。
- 给“打标签、量化、交叉验证、高信号指标”提供了可计算雏形。
- 提醒我们 `purpose.md` 是当前 vault 缺失层，应优先补。
- 也提醒不要在 Markdown 契约稳定前做完整桌面 App。

已沉淀：

- `raw/repos/2026-05-26-llm-wiki-source.md`
- `wiki/summaries/2026-05-26-llm-wiki-architecture-review.md`
- `wiki/patterns/purpose-md-as-wiki-mission-layer.md`
- `wiki/patterns/four-signal-graph-relevance.md`
- `wiki/patterns/graph-insights-health-check.md`
- `wiki/patterns/local-verified-vault-api.md`
- `wiki/patterns/async-review-queue-for-ai-ingest.md`
- `wiki/patterns/provenance-safe-source-lifecycle.md`
- `wiki/claims/llm-wiki-is-implemented-reference-architecture.md`
- `wiki/anti-patterns/full-app-overengineering-before-clean-markdown-vault.md`
- `wiki/anti-patterns/algorithmic-graph-scoring-without-source-quality.md`
- `outputs/qa/2026-05-26-llm-wiki-value-analysis.md`

融合冲突检查：

- `llm_wiki` 设计点和当前资料库架构不冲突，但必须分层采用。
- 立即采用：`purpose.md`、来源字段、验证标签、review 思路。
- 轻量适配：四信号关系评分、图谱健康检查、来源生命周期。
- 中期观察：本地 API / context pack。
- 暂不采用：完整 Tauri App、复杂 ingest queue、LanceDB/vector search、完整图谱 UI。
- 已沉淀：
  - `wiki/decisions/2026-05-26-llm-wiki-fusion-compatibility.md`
  - `outputs/qa/2026-05-26-llm-wiki-fusion-conflict-check.md`

本轮追加明确：

- `llm_wiki` 架构层面已经足够理解，但没有做全仓库逐文件接管级审计；UI 层暂不重要。
- 它适合做自动知识编译机、工程发动机和操作台参考。
- 它不适合直接替代本资料库的 verified truth layer。
- 二者关系是互补：`llm_wiki` 负责 raw -> wiki 的自动化和图谱/搜索/API 工程能力，本资料库负责 claim / pattern / anti-pattern / decision / evidence / confidence / risk 的可信判断和采纳规则。
- 已补充：
  - `outputs/qa/2026-05-26-llm-wiki-vs-verified-knowledge-system.md`
  - `outputs/qa/2026-05-26-llm-wiki-implementation-extraction.md`
  - `wiki/patterns/reference-implementation-extraction-notes.md`
  - 更新 `wiki/summaries/2026-05-26-llm-wiki-architecture-review.md`
  - 更新 `wiki/decisions/2026-05-26-llm-wiki-fusion-compatibility.md`
  - 更新 `wiki/indexes/knowledge-graph-index.md`
- 后续规则：如果参考库源码可能影响未来实现，除了 high-level pattern/claim/decision，还要补实现级提取记录，记录源码模块、可复用不变量、防错边界和不照搬的产品层。

## 2026-05-26 追加：cc-note-ops 与 QMD 分层判断

cc-note-ops：

- 用户先要求只看 README，后要求核三点源码。
- 已确认三点源码成立：当前笔记锁定、输出/修改分离、表达/结构分离。
- 判断：它不是大脑核心，而是 AI 操作层 / 当前笔记工作台。
- 已沉淀：
  - `wiki/patterns/current-note-operation-workbench.md`

QMD：

- 用户提供文章，讨论第二大脑规模变大后 index 不够用，QMD 作为本地混合检索层。
- 已用 web 核查：Karpathy gist 确实说小规模 index 足够，长大后 qmd 是好选项；`tobi/qmd` README 确认 BM25 + vector + LLM reranking、本地 CLI/MCP、Qwen3 embedding 可用于多语言。
- 判断：QMD 不属于核心层，而属于搜索扩展层；短期观察，不安装。
- 触发条件：raw/wiki 文件量变大、index 膨胀、需要找 raw 原文细节、跨分类检索变多、检索 token 成本上升。
- 已沉淀：
  - `wiki/patterns/qmd-local-hybrid-search-layer.md`

架构全貌：

- 已补 `wiki/decisions/2026-05-26-architecture-layering-v0-1.md`。
- 当前总架构分层：raw / wiki / claims-patterns-anti-patterns / graph-index-health / qmd-future-retrieval / API-context-pack / operation-workbench-skills / products。
- 当前阿尔法方向：Verified Knowledge Graph = Compiled Wiki + Evidence-backed Claims + Negative Evidence + Relation Scoring + Source Audit + Context Pack for Agents。

## 2026-05-26 追加：Obsidian Bases + Properties 核验

用户提供 Grok 对 Obsidian 2026 数据库方案的判断，核心说法是 Bases + Properties 已经成为最优主力数据库层。

已用 Obsidian 官方 help / changelog、Dataview / Datacore GitHub 页面核验。

当前判断：

- 大方向成立：Obsidian 原生 Properties + Bases 适合作为第一阶段主力视图层和轻数据库层。
- 细节需修正：Bases 在 2025-05-21 的 1.9.0 Desktop early access 引入，公开版 1.9.10 在 2025-08-18 发布。
- Dataview 没有“退休”，复杂查询和 DataviewJS 仍有价值；只是普通表格/过滤/属性管理优先用 Bases。
- Datacore 是 Dataview 方向的新一代尝试，但仍偏 power user / JS/TS，不作为当前核心依赖。
- 对本资料库来说，Bases 只属于 view / metadata layer，不是 truth layer。

已沉淀：

- `outputs/qa/2026-05-26-obsidian-bases-properties-layer-check.md`
- `wiki/decisions/2026-05-26-obsidian-bases-properties-primary-view-layer.md`

## 2026-05-26 追加：主线骨架优先级收束

用户确认：Obsidian 插件生态属于锦上添花，当前应先把资料库架构本体做完。

当前骨架已有：

- `purpose.md`：使命层。
- `raw / wiki / outputs / products / templates`：目录层。
- `source / claim / pattern / anti-pattern / decision`：核心节点类型。
- `wiki/indexes/knowledge-graph-index.md`：索引层。
- `wiki/decisions/2026-05-26-architecture-layering-v0-1.md`：分层架构总览。
- 若干外部资料/仓库已按 pattern / claim / decision / anti-pattern 沉淀。

当前真正缺口：

1. 统一 `SCHEMA.md`：每类节点必填字段、枚举值、状态流转、哪些字段可空。
2. 资料晋级流程：`raw source -> summary -> claim/pattern/anti-pattern -> decision -> adopted implementation`。
3. 验证门槛：single-source、cross-checked、field-tested、conflicted、rejected 的硬规则。
4. 关系模型：supports / contradicts / refines / replaces / implements / inspired_by / risk_of / alternative_to 等关系类型。
5. 冲突裁决机制：两个优秀设计互相冲突时如何判断采纳、暂缓或拆层。
6. 健康检查标准：孤立节点、无来源 claim、过期 source、低置信 decision、缺少反例的 pattern、outputs 未回链等。
7. 最小实现顺序：先 schema，再手工流程，再健康检查，再 AI 编译，再脚本校验，再 API/context pack。

后续用户提供优秀仓库时，不再泛泛分析“这个库厉害在哪”，而是优先判断它补的是哪块主线骨架：

- schema 契约
- ingest / compile 流程
- evidence / verification gate
- relation model
- conflict resolution
- health check
- implementation order

补不上主线骨架的内容，只记录为外围工具、操作层或观察项，避免系统被插件和模板带跑。

## 2026-05-26 追加：nano-NotebookLM 知识图谱与向量索引分析

用户提供 `ArthurYangX/nano-NotebookLM`，要求重点看知识图谱和向量索引设计。

本次已拉取源码到本地临时目录：

- repo: `https://github.com/ArthurYangX/nano-NotebookLM`
- commit: `8458d9c2d3e958b1d5cf448fa4000448b28760b0`
- local snapshot: `C:\Users\Administrator\AppData\Local\Temp\nano_notebooklm_probe\nano-NotebookLM`
- archived snapshot: `raw/repos/_snapshots/nano-NotebookLM-8458d9c2d3e958b1d5cf448fa4000448b28760b0.zip`

当前判断：

- 它的强项是搜索扩展层和关系操作层，不是 verified truth layer。
- 向量索引：FAISS `IndexFlatIP` + normalized embeddings + chunk metadata + cached vector reconstruct + dim mismatch rebuild。
- 关键词索引：BM25，英文 token + 中文 char/bigram，JSON 保存，避免 pickle。
- 混合检索：BM25 + FAISS 用 RRF 融合。
- 图谱：Stage A 按文件抽 macro topics，Stage B 按 chunk 抽 leaf concepts，再合成 `leaf -> topic -> chapter root`。
- GraphRAG：concept embedding 选 seed，BFS 2 hops 扩展关系邻域，再回到 source chunks。
- 人类编辑：系统图谱 `knowledge_graph.json` 和用户编辑 `mindmap_edits.json` 分离，读取时 replay overlay；这个非常适合我们未来做 AI 编译图谱 + 人类审定。
- Embedding preset：不同模型写入不同 FAISS namespace，concept embedding 也按 preset 分 bucket；这是未来 vector index 的硬规则候选。

对本资料库的采纳：

- 短期只记录，不实现。
- 中期可吸收：hybrid search、GraphRAG resolver、generated graph overlay、embedding namespace。
- 不能照搬：它的关系类型偏学习工具，缺少 supports/contradicts/refines/replaces、negative evidence、source_quality、verification_status、adoption decision。

已沉淀：

- `raw/repos/2026-05-26-nano-notebooklm-source.md`
- `wiki/summaries/2026-05-26-nano-notebooklm-kg-vector-index-review.md`
- `wiki/patterns/hybrid-vector-bm25-rrf-with-graph-neighborhood.md`
- `wiki/patterns/generated-graph-human-edit-overlay.md`
- `wiki/patterns/embedding-preset-namespaced-index-cache.md`
- `outputs/qa/2026-05-26-nano-notebooklm-kg-vector-index-analysis.md`

## 2026-05-26 追加：garrytan/gbrain 第二大脑 / 知识引擎分析

用户提供 `garrytan/gbrain` 和关于“RAG 实际有 8 层”的截图，要求判断这个 agent 第二大脑是否有可借鉴之处。

本次已拉取源码到本地临时目录：

- repo: `https://github.com/garrytan/gbrain`
- commit: `32f8be96c2409b8ccd35b7835692fd56b640f5c4`
- local snapshot: `C:\Users\Administrator\AppData\Local\Temp\gbrain_probe\gbrain`
- archived snapshot: `raw/repos/_snapshots/gbrain-32f8be96c2409b8ccd35b7835692fd56b640f5c4.zip`

重点读取：

- README、`docs/guides/brain-vs-memory.md`、`docs/guides/compiled-truth.md`
- `docs/designs/KNOWLEDGE_RUNTIME.md`
- `docs/architecture/RETRIEVAL.md`
- `docs/architecture/schema-packs.md`
- `docs/takes-vs-facts.md`
- `docs/architecture/system-of-record.md`
- `skills/RESOLVER.md`
- `src/core/think/index.ts`、`src/core/think/gather.ts`
- `src/core/search/hybrid.ts`、`query-intent.ts`、`expansion.ts`、`rerank.ts`、`graph-signals.ts`
- `src/core/chunkers/recursive.ts`、`src/core/chunkers/code.ts`
- `src/core/facts/extract.ts`
- `src/core/cycle.ts`、`src/core/cycle/phases/consolidate.ts`、`src/core/cycle/synthesize.ts`、`patterns.ts`
- `src/core/schema-pack/base/gbrain-base.yaml`

当前判断：

- gbrain 是目前最贴近本资料库核心架构的外部参考之一。
- 它补强的不是 UI，也不是单纯向量搜索，而是 verified knowledge engine 的核心层：epistemology、compiled truth、timeline、schema contract、answer synthesis、dream cycle。
- 它强力验证：我们不应该做普通 RAG，而应该做带来源、立场、时间、置信度、反例和采纳门槛的 verified knowledge system。

可吸收点：

- `brain / memory / session` 分层：世界知识、agent 操作偏好、当前任务上下文不要混。
- Markdown system-of-record：Markdown/YAML 是主记录，DB/vector/cache/graph 都是可重建派生层。
- `compiled truth + timeline`：当前结论和证据流水分离。
- `facts / takes / bet / hunch`：把事实、观点、预测、猜测和持有人/置信度/时间分清。
- `schema packs`：未来 `SCHEMA.md` 可演化为可版本化契约，但当前不做 runtime pack。
- `think`：gather 多路证据 -> synthesize answer -> citations -> gaps，是未来 context pack 形态。
- `dream cycle`：周期性维护、沉淀、找 pattern、找矛盾、更新索引。

不采用 / 风险边界：

- 不 fork gbrain。
- 不现在复制 MCP、OAuth、minions、scheduler、company brain、完整 HNSW/reranker/query cache。
- 不用 gbrain 默认 schema 替代我们的 source / claim / pattern / anti-pattern / decision。
- 不把 LLM 自动抽取出来的 facts/takes 直接当 truth。
- gbrain 的 benchmark / 宣传数字未独立复现，只作为 repo claim。

已沉淀：

- `raw/repos/2026-05-26-gbrain-source.md`
- `wiki/summaries/2026-05-26-gbrain-architecture-review.md`
- `wiki/patterns/markdown-system-of-record-derived-indexes.md`
- `wiki/patterns/compiled-truth-plus-append-only-timeline.md`
- `wiki/patterns/epistemology-takes-facts-layer.md`
- `wiki/patterns/schema-packs-as-living-contract.md`
- `wiki/patterns/think-gather-synthesize-gap-analysis.md`
- `wiki/anti-patterns/copying-full-second-brain-runtime-before-schema-stabilizes.md`
- `outputs/qa/2026-05-26-gbrain-second-brain-design-analysis.md`

对后续主线的影响：

1. `SCHEMA.md` 必须区分 fact / take / hypothesis / bet / decision。
2. claim/pattern/decision 应记录 holder、source、confidence、evidence_level、verification_status、valid_from、valid_until。
3. decision 应有 current synthesis 和 evidence timeline。
4. 关系类型应包括 supports / contradicts / refines / replaces / derived_from / risk_of / alternative_to。
5. context pack 未来应返回 answer、citations、supporting claims、contradicting claims、gaps、confidence。
6. 健康检查应查 unsupported claim、conflicted claim、stale decision、missing evidence timeline。

## 2026-05-26 追加：rafafields/Obsidian-Base-Hub 视图层样板分析

用户提供 `rafafields/Obsidian-Base-Hub`，要求看看。

本次已拉取源码到本地临时目录：

- repo: `https://github.com/rafafields/Obsidian-Base-Hub`
- commit: `ca4c927b42a74c63911aa5aa97d1d0694e6e126b`
- local snapshot: `C:\Users\Administrator\AppData\Local\Temp\obsidian_base_hub_probe\Obsidian-Base-Hub`
- archived snapshot: `raw/repos/_snapshots/Obsidian-Base-Hub-ca4c927b42a74c63911aa5aa97d1d0694e6e126b.zip`

重点读取：

- `Readme.md`
- `How it works (with screenshots!).md`
- `Changelog.md`
- `.obsidian/core-plugins.json`
- `.obsidian/types.json`
- 8 个 `.base` 文件：Inbox、Project、Area、Tasks、Daily、Meetings、People、Locations
- `999 - Templates/New Task.md`
- `999 - Templates/New Meeting.md`
- `999 - Templates/New People.md`

当前判断：

- 它不是知识引擎，也不是 verified truth layer。
- 它是一个 Obsidian Bases 视图/工作台样板。
- 它补的是“人怎么扫视、筛选、复查、快速创建结构化笔记”，不是“资料怎么可信”。

可吸收点：

- 根页面嵌入局部 `.base` 视图：Project/Area 页面嵌入 Team、Tasks、Meetings。
- Base 视图的 `+ New` 按钮作为结构化入口。
- 用 link properties 连接对象。
- 用 status/priority 分组视图提升可扫视性。
- Daily note 通过日期公式嵌入当天会议。

对本资料库的迁移方向：

```text
Source dashboard
  -> 待摘要 / 待验证 / 已废弃

Claim dashboard
  -> unverified / single-source / cross-checked / conflicted

Pattern dashboard
  -> watch / adapt / adopted / rejected

Decision dashboard
  -> active / superseded / needs-review
```

风险和不采用点：

- 不照搬它的个人项目管理目录结构。
- 不照搬 task/project/meeting/person 领域模型。
- 不在 `SCHEMA.md` 稳定前创建大量 `.base`。
- 不采用每个 Project/Area 复制一份 `.base` 的长期维护模式。
- 它存在字段命名混用：`projects/proyectos`、`areas/áreas`、`role/rol`、`scheduled/agendado`、`minutes/minutos`、`guests/invitados`。这是强提醒：我们的 schema 字段必须统一。

已沉淀：

- `raw/repos/2026-05-26-obsidian-base-hub-source.md`
- `wiki/summaries/2026-05-26-obsidian-base-hub-view-layer-review.md`
- `wiki/patterns/obsidian-bases-linked-workbench-views.md`
- `outputs/qa/2026-05-26-obsidian-base-hub-analysis.md`

对后续主线的影响：

1. 先写 `SCHEMA.md`，后写 `.base`。
2. 第一批 `.base` 只做全局复查工作台，不做复杂自动化。
3. Bases 应服务 source / claim / pattern / decision 的状态流，而不是创造新的核心结构。
4. 字段命名必须 schema-first，避免视图层碎裂。

## 2026-05-26 追加：eugeniughelbur/obsidian-second-brain agentic vault runtime 分析

用户提供 `eugeniughelbur/obsidian-second-brain`，要求“好好提炼，榨干”。

本次已拉取源码到本地临时目录：

- repo: `https://github.com/eugeniughelbur/obsidian-second-brain`
- commit: `23a0ed29afe63314c8fe0f8ff8a7d3ba5192b52c`
- local snapshot: `C:\Users\Administrator\AppData\Local\Temp\obsidian_second_brain_probe\obsidian-second-brain`
- archived snapshot: `raw/repos/_snapshots/obsidian-second-brain-23a0ed29afe63314c8fe0f8ff8a7d3ba5192b52c.zip`

重点读取：

- `README.md`
- `architecture.md`
- `SKILL.md`
- `references/ai-first-rules.md`
- `references/vault-schema.md`
- `references/write-rules.md`
- `commands/obsidian-ingest.md`
- `commands/obsidian-reconcile.md`
- `commands/obsidian-synthesize.md`
- `commands/obsidian-health.md`
- `commands/obsidian-challenge.md`
- `commands/obsidian-emerge.md`
- `commands/obsidian-world.md`
- `commands/research-deep.md`
- `hooks/validate-ai-first.sh`
- `hooks/load_vault_context.py`
- `scripts/vault_health.py`
- `scripts/bootstrap_vault.py`

当前判断：

- 它不是 Obsidian 插件，而是 Claude Code / Codex / Gemini / OpenCode 可用的 vault skill/runtime。
- 它不是 verified truth layer，而是 agentic vault operating system。
- 它补的是 AI 如何持续写入、传播、复查、恢复上下文和维护 vault。
- 它和我们的主线互补：我们定义 source/claim/pattern/anti-pattern/decision 的可信采纳逻辑；它提供 AI 写库时的操作纪律。

可吸收点：

- AI-first note contract：frontmatter、短 preamble、recency marker、source URL、confidence。
- Never create in isolation：写入一处时同步更新相关节点、index、log。
- Bi-temporal facts：事实有效时间和资料库学习时间分开。
- raw immutable / wiki workspace：原始证据不改，编译层可更新。
- index.md + log.md：导航入口和操作审计。
- Two-output rule：回答用户 + 回写资料库。
- Progressive context loader：按 L0/L1/L2/L3 恢复上下文。
- health check / validator：先报告结构问题，再考虑自动修复。

不采用 / 风险边界：

- 不 fork。
- 不现在启用 background agent、scheduled agents、自动 vault rewrite。
- 不采用自动冲突裁决作为 truth 机制。
- 不把它的 task/person/project/kanban productivity 模型当成我们的核心 schema。
- 不把外部 research API toolkit 作为第一阶段核心依赖。

已沉淀：

- `raw/repos/2026-05-26-obsidian-second-brain-source.md`
- `wiki/summaries/2026-05-26-obsidian-second-brain-skill-analysis.md`
- `wiki/patterns/ai-first-vault-operating-contract.md`
- `wiki/patterns/never-create-in-isolation-propagation-rule.md`
- `wiki/patterns/bi-temporal-facts-for-knowledge-history.md`
- `wiki/patterns/progressive-vault-context-loader.md`
- `wiki/patterns/vault-health-check-as-maintenance-contract.md`
- `wiki/patterns/two-output-rule-answer-plus-knowledge-writeback.md`
- `wiki/claims/obsidian-second-brain-is-vault-runtime-not-truth-layer.md`
- `wiki/anti-patterns/automatic-agentic-vault-rewrite-before-schema-stability.md`
- `outputs/qa/2026-05-26-obsidian-second-brain-value-analysis.md`
- `outputs/qa/2026-05-26-obsidian-second-brain-implementation-extraction.md`

对后续主线的影响：

1. `SCHEMA.md` 需要加入 AI-readable preamble / context summary 规则。
2. source、claim、pattern、decision 都应有传播规则，不允许孤立写入。
3. high-impact claim / decision 应支持 timeline：valid_from、valid_until、learned_at、source。
4. handoff / context pack 应采用分层加载，不全库塞给 agent。
5. health check 应先做报告，不在 schema 稳定前自动修复。
6. two-output rule 适用于高信号分析：回答后应同步沉淀到 outputs/qa 或知识节点。

## 2026-05-26 追加：Misa relation-strength / edge schema 建议

用户转述 Misa 建议：在第 2 步“程序套模板”时加入“关联强度”字段，让 Claim 和 Project、Pattern、Anti-pattern 等不是孤立卡片，而是有向图中的关系边。向量检索应退居第 4 步中的辅助筛选器。

当前判断：合理，而且应进入核心 schema，不是外围插件。

已有基础：

- 模板已有 `related_projects`、`supporting_sources`、`conflicting_sources`、`negative_evidence` 等轻关联字段。
- handoff 已提出关系类型：`supports / contradicts / refines / replaces / implements / inspired_by / risk_of / alternative_to`。
- `llm_wiki` 已沉淀四信号关系评分：direct link、source overlap、common neighbor、type affinity。
- `nano-NotebookLM` 已验证 GraphRAG 需要沿关系邻域扩展。

新增决定：

```yaml
relations:
  - target: "[[node-name]]"
    type: supports | contradicts | refines | replaces | implements | applies_to | derived_from | risk_of | alternative_to | blocked_by
    strength: 1-5
    confidence: low | medium | high
    evidence:
      - "[[source-or-claim]]"
    rationale: "One sentence explaining why this edge exists."
    created: 2026-05-26
    last_verified: 2026-05-26
```

分层边界：

- Markdown/YAML 主记录保存语义关系边。
- 程序后续派生 graph score、source overlap、common neighbor、vector score。
- 向量检索只做候选召回，不做 truth layer。
- context pack 应优先返回强关系、高证据、带反例的节点。

已沉淀：

- `wiki/patterns/semantic-relation-edge-schema.md`
- `wiki/claims/semantic-relation-strength-should-be-core-schema-field.md`
- 已更新 `templates/source-record.md`
- 已更新 `templates/claim-record.md`
- 已更新 `templates/design-pattern.md`
- 已更新 `templates/anti-pattern.md`
- 已更新 `templates/decision-record.md`
- 已更新 `templates/library-review.md`

对后续 `SCHEMA.md v0.1` 的影响：

1. `relations` 应成为 source / claim / pattern / anti-pattern / decision 的通用字段。
2. 每条关系边必须有方向、类型、强度、证据和一句话理由。
3. `related_projects` 等轻字段可以保留用于 Obsidian/Bases 过滤，但可信图谱以 `relations` 为准。
4. 健康检查要能发现：无证据强边、孤立高影响 claim、decision 缺 risk_of 反模式、pattern 缺 supports 来源。
5. context pack 排序应结合 relation strength、evidence_level、verification_status，而不是只看向量相似度。

## 下一窗口恢复锚点

工作目录：

```text
C:\Users\Administrator\Documents\资料库
```

下一窗口先读：

1. `00_handoff/2026-05-26-knowledge-compile-handoff.md`
2. `wiki/decisions/2026-05-26-architecture-layering-v0-1.md`
3. `wiki/indexes/knowledge-graph-index.md`
4. `purpose.md`
5. `templates/source-record.md`
6. `templates/claim-record.md`
7. `templates/design-pattern.md`
8. `templates/anti-pattern.md`
9. `templates/decision-record.md`

当前最重要的下一步：

```text
创建 SCHEMA.md v0.1
```

`SCHEMA.md v0.1` 必须把本轮已验证的核心设计收束为硬规则：

- 节点类型：source / summary / claim / pattern / anti-pattern / decision / qa / implementation-note。
- 通用字段：type、status、created、updated、tags、sources、verification_status、evidence_level、confidence、last_verified、next_review。
- gbrain 启发：fact / take / hypothesis / bet / decision、holder、valid_from、valid_until、evidence timeline、gaps。
- obsidian-second-brain 启发：AI-readable preamble、never-create-in-isolation、two-output rule、progressive context loading、health check。
- Misa 建议：`relations` 作为核心字段，每条边包含 target、type、strength、confidence、evidence、rationale。
- 晋级流程：raw source -> summary -> claim -> pattern / anti-pattern -> decision。
- 自动化边界：先人工/AI 辅助写入，程序做校验；不做 background rewrite、scheduled agents、自动冲突裁决、重型 RAG。
- 搜索边界：BM25/vector/QMD/Zilliz 只做候选召回，不能替代 verified truth layer。

恢复后不要继续盲目看插件或模板。除非用户给新资料，否则优先写 `SCHEMA.md v0.1`，再升级模板和 health check 规则。

## 当前状态

- 已在 `C:\Users\Administrator\Documents\资料库` 下建立最小目录骨架。
- 已写入根目录 `README.md`。
- 已写入本 handoff 文件。
- 已新增第二大脑/知识图谱/优秀库设计提炼/正向融合的概念节点和模板。
- 已导入并分析多个外部参考仓库：`llm_wiki`、`nano-NotebookLM`、`gbrain`、`Obsidian-Base-Hub`、`obsidian-second-brain`。
- 还没有创建 Obsidian `.base` 文件。
- 还没有导入用户业务/生产资料；当前导入的是架构参考资料和外部仓库样本。
