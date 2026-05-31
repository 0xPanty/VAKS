# 资料库

这个资料库不是普通收藏夹，而是一个本地 verified action knowledge system。

当前路线已经确认：

```text
外层像 Karpathy LLM Wiki 一样简单。
内层用 verified-action 规则保证来源、复核和行动依据。
其他参考库只作为可替换模块接入，不抢 truth 裁决权。
```

路线锁死口径：

```text
不是双架构。
是一条主路 + 分级入口 + 懒证据闸门。
```

人话理解：

```text
轻中重是门。
主脊椎是路。
证据纪律是关卡。
```

`Karpathy-light / VAKS-strict` 只是解释层：日常体验保持轻，关键判断和行动依据才触发 verified-action gate。它不是新的 lane 结构，也不替代下面的五层主架构。

对外主架构固定为五层：

```text
1. Capture
   先保存来源，不强迫立刻判断。

2. Understand
   把资料整理成 summary、candidate point、candidate claim / pattern / risk。

3. Review
   只有有来源、有证据、经过 review 的内容进入 reviewed memory。

4. Connect
   新点和旧点做 supports / contradicts / refines / risk_of / derived_from。

5. Act and Learn
   生成 context pack / action basis，记录使用反馈，改进下一次激活路径，但不直接改 truth。
```

一句话：

```text
The system can suggest.
Only reviewed evidence can support action.
Feedback improves activation, not truth.
```

Strict checks are lazy gates:

```text
Capture stays light.
Promotion gets strict.
Action basis gets auditable.
Feedback improves activation, not truth.
```

2026-05-31 minimal review-boundary tightening:

```text
Approval / agreement / LLM-assisted review notes are process evidence, not evidence support.
Known counterevidence / gaps / conflicts must stay visible in important sufficiency reviews, but this is review input, not action readiness.
Test / benchmark / fixture / LLM-judge results are lint and diagnostics, not truth or mainline readiness.
```

Candidate points may stay lightweight until they are promoted, used for action, used as evidence for a strong reviewed relation, included in an action basis, high-impact, stale, contested, or explicitly challenged.

内部可以继续用 verified loop 和第二大脑模型解释细节，但它们不能替代这五层主架构。
第二大脑模型只做解释和设计校验，不做实现模块目录。

内部主循环是：

```text
source
-> candidate
-> calibration / point collision
-> review
-> reviewed node / reviewed relation
-> context pack / action basis
-> action
-> use ledger / feedback
```

这条线回答的是：

```text
资料怎么从来源变成候选？
候选点怎么和本地 reviewed knowledge 做校准？
哪些旧判断被支持、被挑战、被细化、暴露风险或需要复查？
候选怎么经过 review 进入 reviewed memory？
新点怎么和旧点发生支持、冲突、细化、风险和来源关系？
知识怎么变成行动依据？
用后反馈怎么改善下一次激活，而不是改写 truth？
```

这里的 calibration / point collision 不是整篇 raw source 直接撞库。
它的意思是：

```text
外部资料先被拆成少量 candidate points。
这些 candidate points 再和本地 reviewed knowledge 做双向校准。
校准只浮出候选关系、矛盾、适用范围不匹配、旧判断可能过时、缺失证据和复查问题。
校准结果是 review input，不是 truth。
```

Review 也不是简单盖章。
它要看一个判断在支持、反对、适用范围和风险都摆出来后，现在还站不站得住：

```text
有来源，不等于已经被支持。
有反对，不等于立刻作废。
相似不是支持。
重复出现不会自动提高 confidence。
能不能行动要单独看当前场景、风险和回退。
```

Source 会保留轻量 provenance：资料是什么、从哪里来、什么时候收录、谁/什么工具处理过；这只负责追溯，不负责判断 truth、support 或 confidence。

不是所有 candidate 都是 claim：进入 review 前，系统会先判断它是什么、是否可验证，避免把事实、解释、偏好、决策、风险和开放问题都当成 truth。

引用不够：context pack 会显示关键判断的覆盖状态，被支持、证据弱、被挑战、证据缺失、范围不适用；风险单独通过 risk flags、risk refs 和 action readiness 显示。

查询也不是只拿几个相似 chunk。
它应该点亮一片带复核意识的联想邻域：

```text
supporting points
challenging points
risk / anti-pattern
old decisions
scope notes
source / evidence anchors
gaps and review_due
```

这借鉴 HippoRAG 的 association retrieval 思路，但只放在 activation / context pack 层。
Graph traversal、PPR、similarity、association score 只能帮助召回和排序，不能决定 truth、support、confidence 或 action readiness。

GraphRAG / LightRAG 再补一层说法：检索要分层。

```text
low-level:
  找具体 source、text unit、claim、entity。

high-level:
  找 pattern、theme、community。

relation neighborhood:
  找 reviewed relation 周边的相关上下文。
```

这些只决定先读什么、一起带出什么，不决定什么是真的。
Community summary 不是 truth，graph rank 不是 trust，auto-extracted relation 不是 reviewed relation。

第 10 条补强是 temporal applicability：

```text
Truth is source-backed.
Applicability is time-, version-, and scope-bound.
```

一个判断可以是真的，但已经过时；也可以在原项目成立，但对当前版本、环境或时间窗口不适用。

冷热也不是可信度等级，而是 activation tier：

```text
The vault has activation tiers, not truth tiers.
Hot means read early, not believe more.
```

目录角色：

- `raw/`：原始资料区。文章、X 推文、论文、repo、截图、播客转录等先放这里，尽量保留原文和来源。
- `wiki/`：编译产物区。由 LLM/Codex 把 raw 里的资料整理成 summary、claim、pattern、anti-pattern、decision 和项目知识。
- `outputs/`：运行输出区。把和 AI 的重要问答、方案推导、健康检查报告落成 Markdown，避免结论死在聊天记录里。
- `outputs/feedback/`：query-run 和 feedback-event 的 append-only 事件日志区；未来 SQLite 只能作为可重建缓存。
- `products/`：发布成品区。X、公众号、小红书等面向读者的内容放这里，不和 wiki 混在一起。
- `templates/`：模板区。用于统一记录库分析、设计模式、阶段洞察、决策记录。
- `purpose.md`：资料库使命层。说明这个 vault 为什么存在、当前阶段优先级、采用原则和 Agent 使用边界。
- `ARCHITECTURE_PRINCIPLES.md`：架构原则层。规定主架构、分层职责、参考库吸收边界、采纳裁决和防四不像规则。
- `SCHEMA.md`：资料库结构契约。定义节点类型、通用字段、验证状态、关系边、晋级流程和自动化边界。
- `REVIEW_QUEUE.md`：候选审查层。定义 source trace、candidate point、collision signal、point cluster，以及 point collision alpha 机制。
- `FEEDBACK.md`：反馈校准层。定义 query feedback 如何影响 usefulness、scope fit 和 activation ranking，但不直接改 truth。

当前默认方案：

- 主骨架用 Karpathy-style LLM Wiki：`raw/`、`wiki/`、`index`、`log`、`ingest`、`query`、`lint`。
- Codex 作为默认 review/write gate，AI 和外部 agent 只能先生成 candidate。
- Obsidian 作为 IDE、图谱和人工 workbench。
- 严格字段藏在后台，只在晋级为 claim、pattern、decision、context pack 时启用。
- 当前 alpha 机制是 knowledge calibration / point collision：新资料先抽 candidate point，再和本地 reviewed knowledge 做双向校准，生成 supports / contradicts / refines / risk_of / derived_from 等候选关系和复查问题，review 后才影响晋级。
- Review 采用支持-反对式判断：不仅看来源，还看支持、挑战、范围限制、风险和行动可用性。
- 查询反馈只校准激活路径：usefulness、scope fit、activation ranking、missing-point candidate；不会直接把用户偏好写成真理。
- 新增 conversation-derived feedback：从连续追问、问题变窄、纠偏、说漏了、换题等行为反推 route / keyword / scope 信号；默认是弱信号，先 session-local，不直接改 point truth。
- 新增 Reflexion / RMM-inspired feedback ledger：反馈像 reflection / use memory，只影响 usefulness、scope fit、activation ranking 和 review_due，不直接影响 truth confidence、verification_status 或 source reliability。
- 正反馈弱；负反馈制造 review pressure；明确纠错触发 review_due。
- 新增 RKA-inspired review queue taxonomy：low_confidence_claim、contradiction、missing_evidence、synthesis_needed、decision_superseded 只作为 review routing；旧 decision 被替代时不删除，链接 replacement，并把受影响内容标记 review_due。
- 新增 RKA-inspired action guardrails：重大行动前确认 intent / assumptions / scope / success criteria；用户原话和模型理解分开；maintenance manifest 只报健康问题不自动修；`valid_until` 表示适用期，`stale/review_due` 表示复查压力；没有全文/原文 span 的 claim 不能给高 confidence；decision outcome calibration 只改进未来 recommendation，不直接改 truth。
- 暂时不急着上重型 RAG，先跑通 source -> candidate points -> calibration -> review -> reviewed node / reviewed relation -> context pack。

最小闭环：

1. 把新资料放进 `raw/`。
2. 生成 candidate points。
3. 和本地 reviewed knowledge 做 calibration / point collision，浮出候选关系、矛盾、scope mismatch、stale assumption 和 review questions。
4. lint / review 后晋级到正式 `wiki/` 节点或 reviewed relations。
5. 需要行动时生成 context pack。
6. 重大行动前确认意图和成功标准。
7. 行动结果回流为 feedback / decision outcome，校准 activation、usefulness、scope fit、risk calibration 和 future recommendation，并触发 gaps、review_due 或 missing-point。

开发阶段的新增原则：

- 每个阶段理解到的新思路都要落成可连接的知识节点。
- 后续遇到优秀开源库、产品、框架时，先提炼其优秀设计，再判断是否适合融合。
- 融合不是照搬。只有能解决真实问题、降低复杂度、增强现有工作流、并能被追溯验证的设计，才进入项目实践。
- 每条重要设计都应该能回答：来源是什么、解决什么问题、适合哪个项目、关联哪些概念、是否已经采用、采用后怎么验证。
- 不可行路线、踩坑、反模式也要记录。负面证据同样需要标签、交叉验证、失败条件和替代方案，后续统一设计前要主动查询。
- 资料库本身要保持可拓展和可演化。以后出现更强的新思路时，先进入采集和验证流程，通过比较、适配、迁移和回退机制再决定是否替换旧方案。
- 资料库需要可信度治理，但不让验证阻碍收集。raw/source 的底线是来源可追溯；验证状态、证据等级、置信度、反例和复查时间主要在 claim、pattern、decision、context pack 晋级或行动使用时补齐。
