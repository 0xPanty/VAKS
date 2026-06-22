---
record_kind: candidate_distillation
status: draft
provisional: true
title: "Rahul Loop Engineering 2026：通用 AI Agent 闭环工程知识点蒸馏"
created_at: 2026-06-22
updated_at: 2026-06-22
created_by: Codex
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
source_ref: raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source.md
derived_from:
  - raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source.md
  - raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source/pasted-text.txt
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint:
  - loop-engineering
  - ai-agent-workflow
  - closed-loop-execution
  - agent-orchestration
  - verification-gates
  - workflow-memory
possible_project_refs: []
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-22-rahul-loops-ai-engineer-2026/ann-five-stage-loop.md
  - outputs/review/source_annotations/2026-06-22-rahul-loops-ai-engineer-2026/ann-closed-loop-first.md
  - outputs/review/source_annotations/2026-06-22-rahul-loops-ai-engineer-2026/ann-maker-checker-split.md
  - outputs/review/source_annotations/2026-06-22-rahul-loops-ai-engineer-2026/ann-external-memory.md
point_anchor_refs:
  - raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source/pasted-text.txt#PART-2-WHAT-LOOP-ENGINEERING-ACTUALLY-IS
  - raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source/pasted-text.txt#PART-3-ONE-AGENT-VS-A-FLEET
  - raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source/pasted-text.txt#PART-4-OPEN-LOOPS-VS-CLOSED-LOOPS
  - raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source/pasted-text.txt#PART-5-THE-6-BUILDING-BLOCKS
  - raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source/pasted-text.txt#PART-7-PROMPT-ENGINEER-VS-LOOP-ENGINEER
tags:
  - candidate
  - provisional
  - source-distillation
  - loop-engineering
  - ai-agents
  - general-knowledge
  - candidate-only
---

# 通用知识点蒸馏：Loop Engineering 2026

## 边界

这是一份通用 AI agent / loop engineering 候选蒸馏。

它不是 VAKS 项目借鉴结论，不是 reviewed knowledge，不是工具选型建议，不是模型价格证明，也不是行动依据。原文中的人物引用、模型能力、价格、上下文窗口和并发数字都没有独立核验。

## 一句话结论

这篇文章的核心知识点是：

```text
AI agent 的杠杆点正在从“写更好的单次 prompt”
转向“设计一个可重复运行、可检查、可纠错、知道何时停止的反馈循环”。
```

通俗说：

```text
prompt = 让 AI 做一次事
loop = 让 AI 在规则里反复做、检查、修正，直到达到停止条件
```

## 1. 旧方式：人是循环本身

文章说过去两年的常见工作方式是：

```text
人写 prompt
-> agent 输出
-> 人检查
-> 人指出问题
-> 再 prompt
-> 重复
```

这里真正的反馈循环在“人”身上。AI 只是每轮执行一次。

这个模式的优点是稳、可控、成本低；缺点是人一直在当调度器、检查器和修补器，任务一长就很累。

## 2. 新方式：把反馈循环设计出来

文章把 loop engineering 定义成一种可重复反馈周期：

```text
Discover
-> Plan
-> Execute
-> Verify
-> Iterate
```

也就是：

```text
先弄清楚目标和环境
再做计划
然后执行
执行后检查
没过就带着错误信息再来一轮
通过就停止
```

这不是“让 AI 随便自己跑”，而是把人以前手动做的检查、反馈和重试，部分写进流程里。

## 3. 单 Agent Loop vs Fleet Loop

文章区分两种规模：

| 类型 | 适合什么 | 风险 |
|---|---|---|
| Single-agent loop | 聚焦、小范围、一个 agent 能完成的任务 | 自己写自己评，容易自我合理化 |
| Fleet loop | 复杂任务、多角色协作、需要研究/实现/测试分工 | 成本高、协调复杂、容易写入冲突 |

实用理解：

```text
单 agent loop = 一个人反复改自己的稿子。
fleet loop = 一个小团队分工做项目。
```

不要一上来就 fleet。只有当任务天然需要多个角色、并行分支或独立检查时，才值得拆成多个 agent。

## 4. Open Loop vs Closed Loop

这是文章里最实用的区分。

Open loop：

```text
目标宽泛
agent 自己探索路径
可能发现意外方案
但很烧 token，也更容易漂移
```

Closed loop：

```text
目标明确
步骤有边界
每步有检查
有停止条件或交还给人的条件
```

通用建议：

```text
先做 closed loop。
等质量门、边界和停止条件成熟后，再考虑开放更大探索空间。
```

这也是我觉得这篇最有价值的实践点：不要把“循环”误解成“自动乱跑”。好的 loop 首先是有边界的。

## 5. 一个好 Loop 的五个基本要素

从文章里可以压缩成五个要素：

| 要素 | 问题 |
|---|---|
| Goal | 到底要完成什么？ |
| Context | agent 需要读哪些背景？ |
| Action | agent 可以做哪些动作？ |
| Feedback | 用什么检查对不对？ |
| Stop condition | 什么情况下停止、重试或交还给人？ |

如果没有 stop condition，loop 就容易变成烧 token 的长跑。

如果没有 feedback，loop 就只是“自动重复生成”，不会真正变好。

## 6. 六个常见构件

文章列了六个构件，可以理解成 agent loop 的基础设施菜单：

| 构件 | 通俗解释 |
|---|---|
| Automations | 什么时候启动这个 loop，例如每天早上、测试失败后、收到新 issue 后 |
| Worktrees | 给不同 agent 独立工作区，避免互相改同一份文件 |
| Skills | 让 agent 记住一类任务怎么做，不用每次从零解释 |
| Plugins / Connectors | 让 loop 接触真实环境，如浏览器、GitHub、数据库、Slack |
| Subagents | 把研究、实现、检查拆给不同角色 |
| Memory | 把历史尝试、错误、结论放在对话之外的持久位置 |

这些不是“必须全上”的豪华套餐。更像工具箱：任务需要哪个，就拿哪个。

## 7. Maker / Checker 分离

文章里一个很重要的工程直觉是：

```text
写东西的 agent 不应该是唯一判断自己是否完成的人。
```

因为同一个模型很容易对自己的输出宽容，或者沿着错误假设继续自洽。

更稳的形状是：

```text
maker agent: 负责产出
checker agent / test / human: 负责检查
```

但注意：checker 通过也只是诊断结果，不等于事实已经被证明，也不等于人类批准。

## 8. 外部 Memory 是长循环的脊柱

文章说 loop 需要 conversation 之外的 memory。这个点很朴素，但很关键：

```text
模型会忘。
线程会断。
文件、issue、ledger、handoff 不会那么容易断。
```

一个能长期运行的 loop，至少要保存：

- 目标是什么
- 上一轮做了什么
- 哪些检查通过
- 哪些检查失败
- 哪些尝试不要重复
- 下一轮从哪里继续

最简单的 memory 不一定是数据库，Markdown 文件也可以。

## 9. 成本是 Loop 的现实约束

文章强调 loop 会大量消耗 token。这个方向是合理的风险提醒：

```text
每次重试都花钱。
每个 subagent 都花钱。
每次验证和上下文加载都花钱。
```

但原文里关于 DeepSeek、Kimi、MiniMax、上下文窗口、输出上限、价格和并发的具体说法不能直接当事实。那些属于高漂移信息，需要按当前官方资料重新核验。

可保留的通用知识是：

```text
loop 设计必须有预算意识。
不要把 open loop 当默认。
限制重试次数、上下文大小、agent 数量和运行频率。
```

## 10. Prompt Engineer vs Loop Engineer

文章的对比可以这样理解：

| 角色 | 关注点 |
|---|---|
| Prompt engineer | 怎样让 AI 这一次答得更好 |
| Loop engineer | 怎样让系统反复产出、检查、纠错，最终稳定达到标准 |

这不是说 prompt 不重要，而是 prompt 变成 loop 的一个零件。

更高层的问题变成：

```text
谁触发？
读什么？
能做什么？
谁检查？
失败怎么处理？
什么时候停？
结果写到哪里？
```

## 可迁移的通用原则

1. 先定义 done，再让 agent 开始。
2. 先做 closed loop，再考虑 open loop。
3. 每个 loop 都要有反馈信号，不然只是重复生成。
4. 产出者和检查者尽量分离。
5. 长任务必须有外部 memory。
6. 并行 agent 需要隔离工作区。
7. 工具和连接器越强，权限和边界越要清楚。
8. 成本、上下文、重试次数和运行频率要算进设计。
9. 不要用 loop 逃避理解任务本身。

## 不要吸收成事实的部分

- “某某高级工程师说过什么”没有原始链接，暂不当可靠引用。
- “DeepSeek V4 具体能力 / 价格 / 并发”没有核验，暂不当模型事实。
- “最高薪 AI 工程师”属于观点和营销表达。
- “Chinese LLMs solve the loop economics problem”太宽泛，需要拆成具体模型、价格、质量和使用场景后再判断。

## 与 VAKS 的关系

```yaml
relation_to_vaks: weak_relevance_only
project_overlay_created: false
reason: "This is primarily general AI-agent workflow knowledge, not a VAKS-specific architecture/reference source."
```

如果以后要设计具体 Codex/VAKS loop，可以再打开这篇作为一般背景；但当前不把它挂成 VAKS project borrow / non-borrow scope。

## Open Questions

- 原帖 URL 和发布时间是什么？
- Peter Steinberger / Boris Cherny 的原始上下文是否支持文章的解释？
- 具体模型和价格主张在 2026-06-22 是否成立？
- 哪些任务最适合 closed loop，哪些任务仍然该由人手动判断？
- 对个人工作流来说，最小可用 loop 是什么？

## Current Judgment

```yaml
direct_use: no
project_specific: no
general_knowledge: yes
project_overlay_created: false
reviewed_knowledge_created: false
action_basis_allowed: false
truth_mutation_allowed: false
```

