---
type: source
status: source-captured
title: "Hermes Agent Just Changed Local AI Forever: Here's How to Run It Yourself"
source_id: x-pasted-leopardracer-hermes-self-improving-agent
source_uri: x:pasted:leopardracer:hermes-self-improving-agent
source_url: unknown_not_provided
source_type: article_thread
platform: x
author: "leopardracer"
publisher: X
published_at:
updated_at:
captured_at: "2026-06-04"
captured_by: Codex
raw_location: raw/articles/2026-06-04-x-hermes-self-improving-agent-source.md
raw_text_location: raw/articles/2026-06-04-x-hermes-self-improving-agent-source/pasted-text.txt
processing_mode: pasted-text-plus-entity-check
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
topics:
  - hermes-agent
  - local-agent
  - self-improving-agent
  - procedural-memory
  - skills
  - persistent-memory
  - agent-runtime
  - local-model
  - qwen
  - dgx-spark
  - activation
  - dev-context
  - use-ledger
projects:
  - verified-action-knowledge-system
source_family: x-hermes-agent-local-ai-article
upstream_sources:
  - https://blogs.nvidia.com/blog/rtx-ai-garage-hermes-agent-dgx-spark/
  - https://github.com/NousResearch/hermes-agent
  - https://github.com/NousResearch/hermes-agent-self-evolution
verification_status: unverified-pasted-source-with-entity-check
candidate_relation_suggestions:
  - candidate:agent_skill_memory_layer
  - candidate:procedural_memory_is_activation_not_truth
  - candidate:self_improvement_requires_review_gates
  - candidate:local_agent_runtime_separate_from_truth_layer
  - candidate:task_feedback_as_use_ledger_input
  - candidate:gateway_entrypoints_require_agent_access_policy
  - candidate:local_model_server_as_runtime_not_knowledge_authority
tags:
  - raw-article
  - x
  - pasted-text
  - candidate-only
---

# 来源记录：Hermes self-improving local agent architecture

## 为什么收录

用户提供了一段 X/长文正文和三张架构图，询问“看看他的思路”，随后确认是否写入 Obsidian。本卡保留为外部资料 candidate source。

这条资料的价值不是证明 Hermes 或 Qwen 的性能主张，而是呈现一种正在变得常见的 agent 架构思路：

```text
本地常驻 agent
-> 持久 memory / session history
-> skills procedural memory
-> task feedback
-> skill extraction / refinement
-> 下次任务复用
```

对 VAKS 来说，它最值得借鉴的是 agent runtime / procedural memory / Use Ledger / Dev Context 方向；不能借成 truth layer。

## 来源信息

- 来源平台：X
- 作者 / handle：leopardracer / @leopardracer
- 原始 URL：未提供
- 原始正文：用户粘贴文本，保存于 `raw/articles/2026-06-04-x-hermes-self-improving-agent-source/pasted-text.txt`
- 配图：用户在对话中附了三张 Hermes 架构图；当前未另存图片文件。
- 采集方式：用户粘贴正文 + Codex 对 NVIDIA / GitHub 公开页面做实体校验。

来源边界：

```text
X/文章/图片 = provenance candidate。
粘贴正文 = raw source text。
本卡摘要 = candidate comprehension。
抽取点 = candidate points。
NVIDIA/GitHub 链接只做 entity/context check，不证明 X 作者全部主张。
```

## 实体校验

```text
confirmed:
  - NVIDIA 2026-05-13 blog 存在，主题为 Hermes Agent on RTX PCs / DGX Spark。
  - NVIDIA blog 提到 Hermes Agent、Nous Research、Qwen 3.6、RTX / DGX Spark、本地 agent、self-evolving skills。
  - NousResearch/hermes-agent GitHub 仓库存在。
  - NousResearch/hermes-agent-self-evolution GitHub 仓库存在，README 描述 DSPy + GEPA 用于优化 skills / tool descriptions / prompts / code。
  - Hermes README 中列出 CLI、model、tools、gateway、skills、memory、context files 等文档入口。

likely:
  - 文章里的三层 persistent model 可对应 Hermes skills / memory / session or conversation history。
  - 文章里的 gateway 入口与 Hermes README 的 messaging gateway 描述一致。
  - 图里的 local model server 与 Hermes model-provider 分离思路一致。

unclear:
  - X 原帖 URL、发布时间、完整 thread 边界未提供。
  - “140,000 GitHub stars in three months”“most-used agent according to OpenRouter”“40% faster”等量化主张未独立复核为 action-grade 证据。
  - Qwen 3.6 具体模型名、参数结构、上下文长度、硬件需求和本机可运行性未做实测。
  - 图中的 "47+ built-in tools"、"Qwen 3.6 278/35B models"、"3 skills written" 等画面文字只作为视觉/营销表达记录。
```

## 人话摘要

作者的核心判断是：agent 的关键不只是会调用工具，而是能把完成任务时学到的流程写成可复用 skill，并在后续任务中调用和改进。普通 chatbot 每个 session 都像 fresh start；Hermes 的卖点是 memory 和 skills 持久化，任务之间可以复利。

文章把 Hermes 拆成几层：

```text
入口层:
  CLI / Telegram / Slack / email / optional web workspace

agent core:
  session management / prompt assembly / tool dispatch / provider runtime resolution

持久层:
  persistent memory / context compression / session storage / conversation history

学习回路:
  task feedback -> skill extraction -> skill refinement -> reusable skill library

运行时:
  local model server such as LM Studio / Ollama / Qwen
```

它的宏观叙事是：本地模型、GPU/DGX 硬件和 self-improving agent 框架正在把一部分 agentic work 从云端拉回本机。

## 图中思路解读

第一张图强调全架构：

- 左边是入口：CLI、gateway、ACP adapter。
- 中间是 Hermes agent core：session、prompt、tools、provider runtime。
- 下方是 persistence：memory、context compression、session storage、conversation history。
- 右边是 skill compounding：task feedback、skill extraction、skill refinement、reusable skill library。
- 底层是 local acceleration / always-on agentic computing。

第二张图强调复利：

- typical chatbot：每个 session 从零开始，知识丢弃。
- Hermes agent：session 之间有 skills / memory 积累，`~/.hermes/` 变成长期工作记忆。

第三张图强调操作入口和职责分离：

- 用户可以通过 terminal、messaging gateway、web workspace 对话。
- Hermes agent 是 orchestration layer，不是模型本身。
- planner 负责拆任务，tool runner 负责调用工具，skill writer 负责沉淀流程。
- local model server 执行推理。
- persistent storage 保存 skills 和 memory。

## 可抽取 Candidate Points

- `agent_skill_memory_layer`：VAKS 未来可以有一层 procedural memory，保存“怎么做任务”的 skill，而不是“什么是真的”的 claim。
- `procedural_memory_is_activation_not_truth`：skill、session history、conversation memory 只能帮助下次激活和执行，不能成为 evidence support。
- `task_feedback_as_use_ledger_input`：任务反馈可进入 Use Ledger，用于改善流程、工具选择、context pack 装配和下次说明方式。
- `self_improvement_requires_review_gates`：self-improving skill 不能直接自动生效到高风险流程；需要测试、diff、review、rollback 或人工批准。
- `agent_runtime_separate_from_model_runtime`：agent orchestration 与 local model server 分离是好设计；模型是 runtime，不是知识权威。
- `gateway_requires_access_policy`：Telegram/Slack/email 等 gateway 可改善 UX，但必须有身份、权限、路径和动作边界。
- `local_first_privacy_is_runtime_value`：本地 agent 对隐私和成本有价值，但隐私/本地运行不等于输出可信。
- `skill_library_as_dev_context_workbench`：skills 可以和 `DEV_CONTEXT.md` / context-pack workbench 互补，帮助 agent 少从零开始。

## 可借鉴

- 把 skills 视为“过程记忆”：记录成功流程、失败教训、工具顺序、验证步骤。
- 把 memory / session history 作为 activation input，减少重复 briefing。
- 把 task feedback 进入 Use Ledger，影响未来执行路径，而不是改 truth。
- 把本地 agent runtime 与模型 runtime 分离：Hermes-like agent 可调 OpenAI-compatible local server，也可调云模型。
- 把 gateway 做成入口层，而不是知识层。
- 引入 context compression / session storage，但只作为上下文准备。
- 对 skill evolution 设置硬闸门：测试、大小限制、语义保持、人工 review。

## 不能直接借鉴

- 不能把 Hermes memory 当 VAKS memory truth。
- 不能把 session history 当 source support。
- 不能把 skill 成功执行当 claim verified。
- 不能让 agent 自己改 formal schema、review rules、decision records 或 reviewed relations。
- 不能把 local model 输出当更可信；本地只是运行位置，不是证据质量。
- 不能把 gateway 收到的用户消息自动写入 formal vault。
- 不能把 “self-improving” 作为无闸门自动优化。对 VAKS，高风险流程必须保留 review 和 rollback。

## 风险和不确定

- X 文章带有明显营销叙事，硬件、star、benchmark、速度提升等数字需要独立复核。
- self-improving agent 有目标漂移风险：优化 prompt/skill 后可能更会完成局部 benchmark，却偏离用户真实目标。
- skill poisoning / prompt injection / malicious tool / MCP server 安装都是现实攻击面。
- 长期 memory 可能积累过时偏好、错误项目事实和过度个性化。
- gateway 入口会扩大攻击面，需要权限和意图确认。
- 本机常驻 agent 能执行代码，安全边界应按“可执行软件”看待，而不是普通聊天工具。

## VAKS 归位

```text
Capture:
  本条保留为 raw/articles，原始粘贴文本进入 raw_text_location。

Understand:
  本卡摘要、图解、candidate points 是 candidate comprehension。

Review:
  不创建 reviewed claim。若未来要采用 Agent Skill Memory Layer，需要独立 review。

Connect:
  可连接到 DEV_CONTEXT、MEMORY_TIER、Use Ledger、agent memory quarantine、agent access policy、context pack preparation。

Activation / Context Pack:
  skills / memory / session history / context compression 都归入 activation/context preparation。

Decision / Action:
  本条不产生行动依据。不建议现在安装 Hermes 或改 VAKS 主架构。

Use Ledger / Feedback:
  任务反馈和 skill refinement 可启发 Use Ledger：记录任务结果、失败模式、改进建议、下次激活策略。
```

## 价值判断

价值：中高，但只在 future agent runtime / procedural memory / workbench 层。

它不是 NotebookLM 资料，也不是 RAG 资料；它更像 agent 操作系统路线。对 VAKS 当前阶段的意义是提醒我们：未来 agent 真正好用，靠的不只是检索到知识，而是能沉淀“怎么用这些知识做事”的程序化流程。

不过它不能推翻当前 VAKS 主线。VAKS 仍应保持：

```text
truth 由 source-backed review 决定；
activation 只负责把上下文拿出来；
skill 只负责把流程跑稳；
feedback 只负责改进下一次使用。
```

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- 准备把 `Agent Skill Memory Layer` 写成正式设计模式。
- 准备把 Hermes / OpenClaw / Codex skills 作为 VAKS agent runtime 实现参考。
- 准备允许 agent 写入、修改或启用项目内 skills。
- 准备用 task feedback 自动影响 context-pack 或 action workflow。

## 下一步

先作为 candidate source 保留。后续 Direction Review 可把它和 Hermes/Obsidian、OpenClaw、langchain-miniopenclaw、Claude Code + Obsidian、agent memory 资料放在一起比较，形成一条单独的 `agent runtime / procedural memory` 方向评审。
