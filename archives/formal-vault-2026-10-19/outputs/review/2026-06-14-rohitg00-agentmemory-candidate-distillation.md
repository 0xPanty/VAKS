---
record_kind: candidate_distillation
status: draft
provisional: true
title: "agentmemory：MISA runtime memory / VAKS bridge 候选蒸馏"
created_at: "2026-06-14"
created_by: Codex
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: review_due
source_ref: "raw/repos/2026-06-14-rohitg00-agentmemory-source.md"
derived_from:
  - "raw/repos/2026-06-14-rohitg00-agentmemory-source.md"
  - "raw/repos/_snapshots/2026-06-14-rohitg00-agentmemory-f6f9e3c-source.zip"
  - "wiki/summaries/2026-06-14-rohitg00-agentmemory-architecture-review.md"
  - "outputs/review/project_lens_overlays/2026-06-14-rohitg00-agentmemory-misa-vaks-bridge-overlay.md"
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
  - misa
  - hermes
  - agent-runtime-memory
  - context-pack-adapter
  - feedback-quarantine
possible_project_refs:
  - verified-action-knowledge-system
  - misa
point_anchor_refs:
  - "raw/repos/2026-06-14-rohitg00-agentmemory-source.md#Inspected Repository Areas"
  - "raw/repos/_snapshots/2026-06-14-rohitg00-agentmemory-f6f9e3c-source.zip:README.md"
  - "raw/repos/_snapshots/2026-06-14-rohitg00-agentmemory-f6f9e3c-source.zip:src/types.ts"
  - "raw/repos/_snapshots/2026-06-14-rohitg00-agentmemory-f6f9e3c-source.zip:src/functions/observe.ts"
  - "raw/repos/_snapshots/2026-06-14-rohitg00-agentmemory-f6f9e3c-source.zip:src/functions/remember.ts"
  - "raw/repos/_snapshots/2026-06-14-rohitg00-agentmemory-f6f9e3c-source.zip:src/functions/context.ts"
  - "raw/repos/_snapshots/2026-06-14-rohitg00-agentmemory-f6f9e3c-source.zip:src/functions/smart-search.ts"
  - "raw/repos/_snapshots/2026-06-14-rohitg00-agentmemory-f6f9e3c-source.zip:integrations/hermes/__init__.py"
  - "raw/repos/_snapshots/2026-06-14-rohitg00-agentmemory-f6f9e3c-source.zip:.github/security-advisories"
borrow_value: strong_for_misa_runtime_medium_for_vaks_core
borrow_order:
  - "P1: MISA runtime memory quarantine and project/agent-scoped recall"
  - "P1: VAKS context-pack read-only adapter for MISA"
  - "P1: feedback_event / candidate_signal / review_due writeback only"
  - "P2: MCP/REST bridge, slots, retention, viewer/governance concepts after safety gates"
avoid:
  - "Do not install agentmemory into formal VAKS as a truth layer."
  - "Do not let MISA write reviewed claims, patterns, decisions, or reviewed relations through runtime memory."
  - "Do not treat agentmemory confidence, strength, rank, graph score, lesson confidence, or retention score as VAKS truth confidence."
  - "Do not export runtime memories into H:\\Obsidian\\资料库 as reviewed knowledge."
  - "Do not allow memory_write mirroring to bypass VAKS operation receipts."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "the task is specifically about MISA runtime memory, Hermes memory provider, or MISA reading VAKS context packs"
  support_when: "designing agent memory quarantine, context injection, MCP bridge, or cross-session recall"
  risk_when: "someone proposes using runtime memory as reviewed truth, support, action basis, or direct vault writeback"
  cold_references:
    - "raw/repos/2026-06-14-rohitg00-agentmemory-source.md"
    - "raw/repos/_snapshots/2026-06-14-rohitg00-agentmemory-f6f9e3c-source.zip"
tags:
  - candidate
  - provisional
  - agentmemory
  - misa
  - hermes
  - runtime-memory
  - context-pack
  - candidate-only
---

# 候选蒸馏：agentmemory

## 说人话

这个对 MISA 有帮助，而且帮助不小。

但它帮的是：

```text
让 MISA 记住自己做过什么、用户偏好是什么、上次为什么这么决策、
下一次怎么更快拿到 VAKS context pack。
```

不是帮：

```text
让 MISA 直接拥有资料库、直接改 reviewed knowledge、直接判断什么是真的。
```

一句话：

```text
agentmemory 适合做 MISA 的运行时记忆参考；
VAKS 仍然是权威资料库；
MISA 只能通过 context pack 读，通过反馈/候选信号写回。
```

## 直接评分

| 维度 | 分数 | 判断 |
|---|---:|---|
| 帮 MISA 跨会话记忆 | 8.5/10 | 很贴，尤其是 Hermes/MCP/hooks/context 注入形状。 |
| 帮 MISA 使用 VAKS | 8/10 | 适合借做 VAKS context-pack adapter。 |
| 帮 VAKS 核心真值层 | 2/10 | 不应该进真值层。 |
| 直接生产采用 | 4/10 | 功能强，但写/删/导出/注入面太大，需 sandbox。 |
| 设计借鉴价值 | 9/10 | runtime memory plane 很完整，值得强蒸馏。 |

## 它到底是什么逻辑

agentmemory 的核心链路可以拆成：

```text
agent hooks / MCP / REST
-> session / observation capture
-> compression / summaries / memories / lessons
-> BM25 + vector + graph-style hybrid search
-> budgeted context injection
-> retention / working memory / slots
-> viewer / governance / forget / export
```

它解决的是 coding agent 的老问题：

```text
每次开新会话都要重新解释项目、偏好、历史 bug、上次决策。
```

它的强点是“运行时连续性”：

```text
让 agent 记得自己和用户一起做过什么。
```

VAKS 的强点是“知识权威性”：

```text
什么能当证据、什么能行动、什么只是候选、什么必须复查。
```

所以二者不是替代关系。

正确融合：

```text
agentmemory-like layer = MISA runtime memory
VAKS = reviewed/candidate/source/action boundary authority
```

## 对 MISA 最有用的部分

### 1. Hermes adapter 形状

repo 里已经有 Hermes 集成：

```text
prefetch()
sync_turn()
on_session_end()
on_pre_compress()
on_memory_write()
system_prompt_block()
```

这对 MISA 很有参考价值。

MISA 未来可以有自己的 VAKS bridge：

```text
pre_llm_call:
  ask VAKS adapter for relevant context pack / dev context

post_turn:
  record runtime observation to MISA memory

session_end:
  summarize runtime session

user_correction:
  create feedback_event / review_due candidate, not truth mutation
```

关键区别：

```text
agentmemory 默认偏“记住”。
MISA + VAKS 必须偏“分层记住”：运行时记忆归运行时，资料库权威归资料库。
```

### 2. Project / agent scope

agentmemory 有 project 和 agentId 过滤，还有 isolated mode 的 fail-closed 思路。

这对 MISA 很重要，因为 MISA 以后可能同时接：

```text
MISA 自己的 runtime memory
VAKS 资料库 context pack
代码仓库上下文
用户偏好
工具结果
```

必须分桶：

```text
misa_runtime
vaks_context_pack
vaks_candidate_signal
vaks_feedback_event
code_runtime
user_preference
```

不能混成一个“记忆池”。

### 3. Context injection 但必须有收据

agentmemory 会生成预算内 context。

MISA 可以借这个 UX：

```text
开局不再从零开始；
重要偏好和项目约束提前进上下文；
历史 session 的关键点能被召回。
```

但 VAKS 版本必须加：

```text
context_pack_ref
authority_bucket
selected_by
support_boundary
warnings
action_readiness
```

也就是说：

```text
能注入上下文，不代表能行动。
```

### 4. SourceObservationIds / verify 思路

agentmemory 的 memory 可以回指 source observations。

这个模式可借：

```text
runtime memory
-> source observation ids
-> session metadata
-> verify/debug why this memory exists
```

但不能直接等价成 VAKS evidence support。

VAKS 需要的是：

```text
source anchor
evidence item
warrant
scope
challenge
sufficiency
action readiness
```

agentmemory 的 verify 更像：

```text
这条记忆从哪次会话来的？
```

不是：

```text
这条结论是否足够支持行动？
```

### 5. Slots / retention / working memory

agentmemory 的 slots 很像 agent 的“常驻提示槽”：

```text
persona
user_preferences
tool_guidelines
project_context
guidance
pending_items
session_patterns
self_notes
```

MISA 可以借。

VAKS 要改名和降权：

```text
Runtime slots = MISA prompt/runtime preferences
Activation Tier = read early / read later
Truth status = still owned by VAKS reviewed layer
```

## VAKS 有没有比它好

有，而且不是同一个战场。

agentmemory 强在：

```text
记住 agent 会话
把记忆搜索出来
跨工具/跨 agent 共享
快速注入上下文
```

VAKS 强在：

```text
raw / candidate / reviewed / action 分层
证据支持边界
证据充分性
时间/版本/范围适用性
反馈不能改 truth
agent 写入隔离
operation receipt
review-gated writeback
```

所以如果问“谁更适合当资料库权威系统”：

```text
VAKS 更强。
```

如果问“谁更适合让 agent 跨会话记住工作过程”：

```text
agentmemory 这类 runtime memory 更成熟。
```

融合后最强：

```text
agentmemory-like runtime memory helps MISA remember process.
VAKS tells MISA what can be trusted, reviewed, and acted on.
```

## 推荐融合设计

### MISA -> VAKS 读路径

```text
MISA intent / task
-> VAKS Context Adapter
-> query mode / authority bucket selection
-> context pack / dev context pack
-> MISA runtime prompt
```

读路径必须带：

```yaml
context_pack_ref:
authority_bucket:
included_buckets:
excluded_buckets:
selected_by:
warnings:
action_readiness:
```

### MISA runtime memory 路径

```text
MISA conversation / tool use / action result
-> runtime observation
-> session summary
-> runtime memory / slots / pending items
-> future activation
```

这些属于：

```text
MISA operational memory
```

不是：

```text
VAKS reviewed knowledge
```

### MISA -> VAKS 写回路径

只允许三种低权限写回：

```text
feedback_event
candidate_signal
review_due
```

禁止：

```text
claim reviewed
pattern reviewed
decision reviewed
reviewed relation
action basis ready
truth_confidence update
schema update
```

写回必须有 operation receipt：

```yaml
actor: MISA
actor_tier: suggest_only | candidate_write
operation_mode: suggest | propose_write
basis:
  runtime_memory_ref:
  context_pack_ref:
target:
  record_kind: feedback_event | candidate_signal | review_due
truth_mutation_allowed: false
action_basis_allowed: false
```

## 建议的最小架构补充

不要现在就安装 agentmemory。

先把设计补进规划：

```text
P1.5-MISA-MEM: MISA Runtime Memory / VAKS Bridge Sandbox
```

这个 sandbox 做四件事：

```text
1. 设计 MISA runtime memory bucket。
2. 设计 VAKS context-pack read-only adapter。
3. 设计 feedback/candidate/review_due quarantine writeback。
4. 设计 operation receipt + permission gate。
```

通过条件：

```text
MISA can remember runtime context.
MISA can read VAKS context packs.
MISA cannot write reviewed VAKS knowledge.
MISA feedback/corrections become review pressure, not truth.
All action-facing output still passes VAKS action readiness.
```

## Borrow / Avoid

### Borrow

- hook / MCP / REST adapter split.
- session observation schema.
- project/agent scoped recall.
- fail-closed isolated memory search.
- explicit memory save with source observation IDs.
- budgeted context generation.
- pinned slots for preferences/guidance/pending items.
- retention/access logs as activation signals.
- verify/debug endpoint for runtime memory provenance.
- governance delete/audit minimum.
- Hermes provider hook names and lifecycle shape.

### Adapt

- Rename memory confidence/strength to runtime salience/activation.
- Require VAKS context-pack receipts for any VAKS-sourced context.
- Require operation receipts for any writeback.
- Keep feedback/correction as review pressure.
- Keep source exports outside the formal reviewed vault.

### Avoid

- Direct `remember` into reviewed VAKS nodes.
- `on_memory_write` mirroring to VAKS without quarantine.
- Treating lessons/reflections as reviewed truth.
- Treating memory search rank as support.
- Treating source observation as evidence sufficiency.
- Obsidian export into `H:\Obsidian\资料库` as formal knowledge.
- Shared cross-agent memory without project/agent isolation.
- Installing broad MCP write/delete/export tools before permission gates.

## VAKS Fit

| VAKS layer | Fit | Borrow |
|---|---:|---|
| Capture / Provenance | Medium | Runtime observations and sourceObservationIds as process trace. |
| Candidate Distillation | Medium | MISA can propose candidate signals from repeated runtime observations. |
| Review Queue | Medium | Corrections can create review_due, not reviewed truth. |
| Reviewed Knowledge | Low | No direct adoption. |
| Activation / Dev Context | High | Strong context injection and recall reference. |
| Context Pack | High | Good UX shape, but VAKS must add receipts/action readiness. |
| Action Basis | No | Runtime memory cannot create action basis. |
| Feedback | High | Runtime outcomes can feed feedback ledger. |
| Agent Gateway | High | Very useful MCP/hooks permission-surface reference. |
| Productization | Medium | Viewer/governance/skills UX worth studying later. |

## Open Questions

- MISA 当前 Hermes runtime 的 memory provider / pre_llm_call 接口实际是什么形状？
- MISA 是否已经有 `.hermes.md` / context builder / recent-discord-continuity 等现有链路需要兼容？
- VAKS context pack 是否先做 read-only file adapter，还是 MCP/API adapter？
- feedback_event / candidate_signal 文件格式是否先复用现有 templates，还是建 MISA-specific overlay？
- 是否需要单独 `misa_runtime_memory` 目录，避免污染 VAKS mainline？

## Routing Hint

Route this source to:

```text
MISA runtime memory
Hermes provider
VAKS context-pack read-only adapter
feedback quarantine
agent gateway permission model
operation receipt
```

Do not route to:

```text
VAKS truth layer
reviewed claim/pattern/decision
evidence support
action readiness
schema authority
formal Obsidian writeback
```

## Bottom Line

对 MISA 使用我们的资料库，有帮助。

最聪明的用法不是：

```text
MISA 接管 VAKS。
```

而是：

```text
MISA 有自己的运行时记忆；
VAKS 输出有收据的 context pack；
MISA 写回只能是反馈、候选信号、复查压力；
VAKS review gate 决定什么能升级。
```

这样 MISA 会更聪明，但 VAKS 不会被 runtime memory 污染。
