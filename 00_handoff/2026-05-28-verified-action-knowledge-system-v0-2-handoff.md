# 2026-05-28 handoff：Verified Action Knowledge System v0.2

## 工作目录

```text
C:\Users\Administrator\Documents\资料库
```

## 当前最新架构基线

本 handoff 接续 commit：

```text
7d344d3 Document fusion architecture v0.2 and review synthesis
```

这次更新后的核心判断：

```text
Karpathy-simple outside.
Dusk-style workbench nearby.
Reviewed-action core inside.
Optional retrieval, synthesis, publishing, and agent tooling around it.
```

说人话：

```text
日常入口要简单。
项目工作台要顺手。
真正决定长期知识和行动依据的，是 reviewed knowledge core。
dashboard、retrieval、metadata、brief、feedback 都可以帮忙，但不能当 truth。
```

## 下个窗口先读

```text
00_handoff/2026-05-28-verified-action-knowledge-system-v0-2-handoff.md
README.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
SECOND_BRAIN_MODEL.md
ARCHITECTURE_PRINCIPLES.md
SCHEMA.md
IMPLEMENTATION_BLUEPRINT.md
SOURCE_INTAKE.md
REFERENCE_REVIEW_PROTOCOL.md
MEMORY_TIER.md
DEV_CONTEXT.md
REVIEW_QUEUE.md
FEEDBACK.md
wiki/indexes/knowledge-graph-index.md
wiki/indexes/memory-tier-reference-index.md
templates/architecture-review-window-prompt.md
```

如果只是继续看文章/仓库/论文，先读 handoff、README、FUSION、SECOND_BRAIN、REFERENCE_REVIEW_PROTOCOL、architecture review prompt 就够；需要落地实现或改 schema 时，再读完整清单。

## 对外主叙事

不要再用十几层大脑结构做开源第一叙事。

对外只讲五层：

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

边界句：

```text
The system can suggest.
Only reviewed evidence can support action.
Feedback improves activation, not truth.
```

## 内部主循环

内部可以用 verified loop 解释：

```text
raw source
-> Capture / Provenance
-> Candidate Comprehension
-> Review / Consolidation
-> Association / Point Collision
-> Activation / Dev Context
-> Context Pack
-> Decision / Action
-> Use Ledger / Feedback
-> Cooling / Reactivation / Review Due
```

横切控制：

```text
Provenance
Risk / Inhibition
Traceability
Safety Gate
```

旁路能力：

```text
Proactive Synthesis:
  on-demand first, scheduled later, candidate only.

Expression / Publishing:
  future output surface.

Agent Tool Safety:
  future execution safety, only needed when agents can write or execute.
```

## 第二大脑模型怎么用

`SECOND_BRAIN_MODEL.md` 是解释模型和设计校验表，不是工程模块目录。

它有价值的点是：

```text
入库时建立连接。
查询时激活连接。
用后修正连接。
风险层负责刹车。
主动思考负责后台回放。
```

但不要把每个脑结构都做成独立模块。

正确用法：

```text
对外 README:
  五层主叙事。

内部设计:
  用大脑模型检查有没有漏掉 capture / activation / review / association / feedback / risk。

实现路线:
  仍然按最小 verified loop 试跑，不按脑层开十几个子系统。
```

## Pro review 后已采纳的修正

已采纳：

```text
Attention -> Activation
Memory Tier -> Activation Tier where possible
Verified Memory -> Reviewed Memory / Evidence-backed Memory
Forgetting -> Cooling
Feedback Learning -> Use Ledger when referring to records
Risk Control -> Cross-cutting Risk / Inhibition
```

已收缩：

```text
MVP relation types:
  supports
  contradicts
  refines
  risk_of
  derived_from
```

暂缓：

```text
replaces
implements
applies_to
inspired_by
alternative_to
blocked_by
```

这些不是永远拒绝，只是不进入第一版核心关系集合。

## 已更新的关键文件

```text
README.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
SECOND_BRAIN_MODEL.md
ARCHITECTURE_PRINCIPLES.md
SCHEMA.md
IMPLEMENTATION_BLUEPRINT.md
SOURCE_INTAKE.md
REFERENCE_REVIEW_PROTOCOL.md
MEMORY_TIER.md
DEV_CONTEXT.md
REVIEW_QUEUE.md
FEEDBACK.md
templates/architecture-review-window-prompt.md
templates/claim-record.md
templates/decision-record.md
templates/design-pattern.md
templates/library-review.md
templates/anti-pattern.md
wiki/indexes/knowledge-graph-index.md
wiki/indexes/memory-tier-reference-index.md
```

## 当前明确没有做

```text
没有实现脚本。
没有跑 dev context pack。
没有跑 query-run。
没有写 feedback-event。
没有做 PUBLISHING_PIPELINE。
没有做自动化 daily / weekly synthesis。
没有做 API / MCP / viewer。
没有 push。
```

## 下一步建议

方向已经清晰，不建议继续无止境看资料堆设计。

下一步应该从“架构设计”转入“最小闭环试跑”，但要很小：

```text
1. 选 3-5 条已有资料。
2. 生成 candidate point。
3. 做 supports / contradicts / refines / risk_of / derived_from 关系试撞。
4. 人工 review 一个小 cluster。
5. 产出一个 context pack / action basis 样例。
6. 记录一次 feedback / review_due。
```

验证目标不是自动化，而是判断：

```text
这套 reviewed second brain 是否真的比普通 Karpathy wiki 更会形成行动依据？
point collision 是否真的减少重复阅读？
Use Ledger 是否真的改善下次激活路径？
Risk / Inhibition 是否能防止漂亮但错误的连接？
```

## 当前风险提醒

```text
1. 不要把大脑模型变成十几个工程模块。
2. 不要把 scheduled synthesis 做进 MVP。
3. 不要让 dashboard / retrieval / metadata / brief 变成 reviewed knowledge。
4. 不要把 feedback 写成 truth confidence 自动更新。
5. 不要为了兼容旧关系类型，把 relation enum 重新扩成一长串。
6. 不要急着做 agent security platform；现在只需要轻规则，等 agent 真能写/执行再升级。
```

## 给下个窗口的口径

```text
当前主线成立，而且比单纯 Karpathy LLM Wiki 更强：
Karpathy 负责简单可用，
Dusk 负责项目桌面，
Reviewed-action core 负责来源、证据、关系、风险和行动依据，
Use Ledger 负责用后校准，
Proactive Synthesis 只做候选生成器。

但现在必须收缩。
不要继续把所有好点子塞进核心。
下一步优先做最小闭环试跑。
```
