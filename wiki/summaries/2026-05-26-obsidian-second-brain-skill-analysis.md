---
type: summary
source: [[2026-05-26-obsidian-second-brain-source]]
repo: eugeniughelbur/obsidian-second-brain
commit: 23a0ed29afe63314c8fe0f8ff8a7d3ba5192b52c
created: 2026-05-26
verification_status: source-reviewed
evidence_level: primary-source
confidence: high
tags:
  - obsidian
  - ai-first-vault
  - workflow-runtime
  - second-brain
---

# obsidian-second-brain 架构提炼

## 一句话结论

这个库不是知识可信度系统，而是一套让 AI 持续读写、维护、复查 Obsidian vault 的操作系统。

它能补我们当前资料库的执行层、维护层和上下文加载层，但不能替代我们的 verified truth layer。

## 大白话理解

我们现在的主线是：

```text
source -> summary -> claim/pattern/anti-pattern -> decision
```

`obsidian-second-brain` 关心的是另一件事：

```text
AI 每次写入 vault 时，怎么不乱写？
新东西进来时，怎么更新旧页面？
一次回答后，怎么把有价值的东西回写到资料库？
下个窗口怎么快速知道当前 vault 里发生了什么？
资料库乱了以后，怎么体检？
```

所以它像一个 vault runtime，不像一个 truth schema。

## 最值得吸收的设计

| 设计 | 它的做法 | 对我们的意义 | 采纳状态 |
|---|---|---|---|
| AI-first note contract | 每条 note 有 frontmatter、未来 AI 摘要、来源、时间、置信度 | 让未来 agent 可检索、可判断、可复核 | 进入 `SCHEMA.md` 候选 |
| Never create in isolation | 创建/更新一条笔记时，同时更新相关项目、日记、索引、日志 | 防止孤立节点和知识断链 | 立即吸收为写入规则 |
| Bi-temporal facts | 当前字段 + timeline，记录事实有效时间和资料库学习时间 | 补 `valid_from / valid_until / learned_at / source` | 强吸收 |
| raw immutable / wiki workspace | 原始资料不改，wiki 可重写 | 和我们 raw/wiki 分层一致 | 已采用，强化 |
| index.md + log.md | 一个导航入口，一个操作审计日志 | 补我们的恢复和审计链路 | 立即吸收 |
| Two-output rule | 回答用户 + 回写 vault | 避免重要结论只留在聊天里 | 强吸收，但需人工边界 |
| ingest rewrite | 新来源进入后重写相关旧页面，不只是新增摘要 | 提醒我们要做增量融合，不做资料堆积 | 候选，先人工执行 |
| reconcile/synthesize/challenge | 找冲突、找 pattern、用历史反驳当前想法 | 补健康检查和思考工具 | 中期吸收 |
| progressive context loader | L0/L1/L2/L3 分层加载身份、索引、当前状态、深上下文 | 补新窗口恢复和 context pack | 进入 implementation blueprint |
| write-time validator | 写 Markdown 后检查 frontmatter / preamble / ai-first | 补 schema enforcement | `SCHEMA.md` 稳定后做 |
| vault_health.py | 查 duplicate、orphan、broken link、missing frontmatter 等 | 给健康检查脚本提供雏形 | 中期改写 |

## 它补我们现有框架的缺口

1. 写入传播规则不够硬。

我们已有节点类型，但还没严格规定“写一个 source 后，要同步更新哪些 summary、claim、index、log”。它的 propagation rule 正好补这块。

2. 时间维度还不够强。

我们有 `last_verified`、`next_review`，但还需要更清楚地区分：

```text
事实什么时候在现实中成立？
资料库什么时候知道这件事？
什么时候被替换或废弃？
```

这就是 bi-temporal timeline。

3. 新窗口恢复还不够工程化。

它的 `/obsidian-world` 提醒我们，恢复上下文不能靠一口气读全库，而应该：

```text
L0 purpose/schema/critical facts
L1 index/log
L2 active decisions/current work
L3 按需读深层材料
```

4. 健康检查还没有脚本化标准。

它的 health check 虽然偏普通 vault，但方向对。我们后续应改成 verified knowledge health：

```text
unsupported claim
claim without source
decision without evidence
pattern without negative evidence
conflicted claim
stale source
orphan output
```

5. 回答和沉淀之间还没有强约束。

它的 two-output rule 提醒我们：如果一次分析形成了新判断，就应该进入 `outputs/qa` 或 candidate claim，而不是停在聊天窗口。

## 它不能直接解决的问题

- 没有足够细的 `source_quality` 模型。
- 没有我们需要的 `source -> claim -> pattern -> anti-pattern -> decision` 晋级门槛。
- `confidence` 只有 stated/high/medium/speculation，太粗。
- 自动 reconcile 容易过度自信，需要人类 gate。
- scheduled/background agent 在 schema 未稳前风险很高。
- 研究工具依赖外部 API 和费用，不应进入第一阶段核心。

## 量化标签

| 维度 | 分数 | 说明 |
|---|---:|---|
| 架构相关度 | 8.5/10 | 强相关，但偏 runtime |
| schema 启发 | 7/10 | AI-first + timeline 很有价值，字段还需重写 |
| workflow 启发 | 9/10 | propagation、two-output、context loader、health 都很强 |
| truth-layer 完整度 | 4/10 | 不足以支撑 verified knowledge system |
| 立即可采用度 | 7.5/10 | 可以吸收规则，不应吸收整套自动化 |
| 过度设计风险 | 8/10 | wholesale adoption 会变成自动化系统维护 |

## 分层采纳建议

立即采用：

- AI-readable preamble 思想
- raw immutable / wiki derived
- index + operation log
- search before create
- never create in isolation
- bi-temporal timeline 字段
- two-output rule 的人工版本

等 `SCHEMA.md` 后采用：

- write-time validator
- health check script
- context loader
- source/claim/pattern/decision dashboard

中期再看：

- scheduled agents
- background agent
- research-deep pipeline
- cross-CLI command packaging

暂不采用：

- 自动重写整个 vault
- 自动解决高风险冲突
- API-key research toolkit 作为核心依赖
- 大量 preset / role template
- 完整 Claude skill runtime

## 与已有参考库的关系

- 和 `gbrain` 互补：gbrain 补 epistemology/truth/timeline，obsidian-second-brain 补 vault operation/runtime。
- 和 `llm_wiki` 互补：llm_wiki 补工程编译和图谱/API，obsidian-second-brain 补 AI 写库时的纪律。
- 和 `nano-NotebookLM` 互补：nano 补检索/GraphRAG，obsidian-second-brain 补写回与维护。
- 和 `Obsidian-Base-Hub` 互补：Base-Hub 补人类视图，obsidian-second-brain 补 AI 操作规则。

## 最终判断

它是正向增量，但必须降维吸收。

正确吸法：

```text
吸收 AI-first 规则、传播规则、timeline、context loader、health check。
不吸收完整自动化 runtime。
```

它把我们的系统从“设计上可信”往“操作时不容易散架”推进了一步。

