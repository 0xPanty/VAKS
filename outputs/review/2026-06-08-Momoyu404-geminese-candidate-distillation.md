---
type: candidate_distillation
record_kind: candidate_distillation
status: draft
title: "Geminese：Obsidian 内的 Gemini / Ollama agent workbench"
created_at: "2026-06-08"
created_by: Codex
processing_tier: medium
knowledge_status: candidate
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
derived_from:
  - raw/repos/2026-06-08-Momoyu404-geminese-source.md
  - raw/repos/_snapshots/2026-06-08-Momoyu404-geminese-d8623d8-source.zip
  - wiki/summaries/2026-06-08-Momoyu404-geminese-architecture-review.md
projects:
  - verified-action-knowledge-system
topics:
  - agent-gateway
  - obsidian-workbench
  - permission-boundary
  - local-model-agent
  - mcp
  - skills
borrow_value: strong
borrow_order: P1
evidence_strength: medium_for_design_low_for_vaks_fit
tags:
  - candidate-only
  - source-distillation
  - github
  - obsidian
  - design-only
provisional: true
---

# 候选蒸馏：Geminese

## 一句话

`geminese` 对 VAKS 是 `P1 / strong`，但借鉴对象不是核心 truth schema，而是 **Obsidian 内 agent workbench + 权限边界 + vault-local workflow 扩展**。

说人话：它把“AI 进 Obsidian”做成了一个比较完整的产品壳。Gemini 走 CLI，Ollama 走本地工具协议，用户在侧栏里聊天、选模型、带当前笔记、提及文件、拖图、inline edit、开 Plan/Agent 模式、接 MCP、加 slash commands / skills / subagents。VAKS 可以借它想清楚：未来 agent 怎么安全进入资料库，而不是只靠命令行窗口。

## 候选知识点

### 1. Agent Gateway 应该是一个可见的权限界面

Geminese 把权限做成可见的 Plan / Agent 模式：

```text
Plan:
  read-only planning

Agent:
  can execute tools and edit files
```

VAKS 可以借鉴这个交互，但要更严格：Agent 模式也不能直接写 reviewed truth，只能写 candidate、feedback event、use ledger 或受控 staging。

### 2. Vault-local storage 适合保存 agent 工作流配置

Geminese 把 commands、skills、agents、sessions、MCP configs、settings 放在 `.gemini` 路径下。这个对 VAKS 有启发：agent workflow 配置可以作为 vault-local operational layer，而不是混进 wiki truth layer。

可借鉴：

```text
.vaks/agents
.vaks/commands
.vaks/skills
.vaks/mcp
.vaks/sessions
```

但这些只应是操作配置和候选上下文，不是 reviewed knowledge。

### 3. Local model 也需要工具协议，不只是聊天框

Geminese 的 Ollama 路径不是单纯聊天，而是用受限工具：Read、LS、Glob、Grep、Write、Edit、LoadSkill。这个很贴 VAKS：本地模型如果要参与 vault 工作，必须走显式工具协议和权限模式。

VAKS 可借鉴：

```text
local model -> structured tool call -> gateway validates -> candidate-only operation
```

### 4. 外部上下文和导出路径要分开

Geminese 区分：

```text
vault: read/write
external context: read/write
export paths: write-only
none: denied
```

这对 VAKS 很重要。资料库未来如果允许 agent 读项目外部文件或导出报告，必须把“读上下文”和“写导出结果”拆开，否则很容易越界。

### 5. MCP 需要按需激活和禁用工具

Geminese 的 MCP manager 支持 context-saving：server 可以启用，但只有被 `@mention` 时才进上下文；也能收集 disabled tools。VAKS 可以借鉴这个思路，把 MCP 从“全量接入”改成“按任务点亮”。

### 6. Inline edit 是一个低风险写入模式

Inline edit 单独限制 read-only 工具，最后以替换/插入结果返回给 UI。这个比让 agent 直接编辑整篇笔记更可控。VAKS 未来对候选笔记、摘要、source card 的轻编辑可以借这个交互。

## Borrow Gradient

```yaml
borrow_value: strong
borrow_order: P1
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "task is specifically about VAKS Agent Gateway, Obsidian workbench, permission UI, local model tooling, or MCP activation"
  support_when: "designing inbox/workbench/agent-facing command layer"
  risk_when: "agent write access, external context access, MCP activation, or cloud API privacy is in scope"
  cold_references:
    - raw/repos/2026-06-08-Momoyu404-geminese-source.md
    - raw/repos/_snapshots/2026-06-08-Momoyu404-geminese-d8623d8-source.zip
```

## 对 VAKS 的具体借鉴

| VAKS 区域 | 可借鉴点 | 不要越界 |
|---|---|---|
| Capture | 当前笔记、@file、图片、外部目录作为上下文入口 | 上下文不是 evidence support |
| Understand | slash commands / skills 做结构化理解流程 | skill 输出不是 reviewed truth |
| Review | Plan 模式先读后计划，降低误写风险 | Plan 不是 evidence-aware review |
| Connect | MCP 和 external context 可作为按需连接层 | 连接器输出不是 reviewed relation |
| Activation | `.gemini` 风格的 workflow 配置可映射为 VAKS operational layer | activation 配置不是真值层 |
| Context Pack | 文件、选择区、图片、浏览器选择共同组成 context envelope | context pack 仍需覆盖和边界说明 |
| Agent Gateway | Plan / Agent、blocklist、path access、approval、tool allowlist | Agent 不能直接写 reviewed knowledge |
| Feedback | sessions / history 可成为 use ledger 原料 | session continuity 不等于反馈校准 |

## 不要借鉴

- 不要把 Obsidian 插件 UI 当成 VAKS core 架构。
- 不要把默认 Agent mode 照搬到 VAKS；VAKS 默认应更接近 Plan / candidate-only。
- 不要把 Gemini API 路径误认为本地隐私安全。
- 不要把 MCP server 全量常驻上下文。
- 不要让 agent 直接写 `wiki/claims`、`wiki/patterns`、`wiki/decisions`。
- 不要把 Bash path validator 当成完整安全沙箱。

## 和已有 VAKS 的关系

Geminese 强化的是 VAKS 已有边界：

```text
Activation is not truth.
Tool output is not reviewed support.
Agent writes must be quarantined.
Context pack must expose source/context boundaries.
Feedback/session continuity must not mutate truth.
```

它挑战 VAKS 的地方是产品面：如果 VAKS 只停留在文件规则和命令行流程，会很难让普通用户感受到 agent workbench 的价值。

## 融合判断

```text
fusion_decision: adapt
borrow_value: strong
borrow_order: P1
direct_use: no
fork: no
design_only: yes
schema_change: no
current_branch_value: high_for_agent_gateway_and_workbench
whole_architecture_value: medium_to_high
implementation_evidence: medium
action_readiness: not_ready
```

## 最小吸收建议

先不改主文档。后续如果设计 VAKS Agent Gateway，可以从 Geminese 抽三个最小实验：

```text
1. visible permission mode:
   Plan / Candidate Write / Agent Action 三段，而不是只有 Plan / Agent。

2. command-mediated vault access:
   agent 通过白名单命令写 candidate / feedback / use ledger，不直接改 reviewed 层。

3. context source chips:
   当前笔记、@file、外部目录、图片、MCP server 都显示成可见上下文 chip，并带权限边界。
```

这条应作为 VAKS workbench / agent gateway 的 P1 参考，不作为 reviewed decision。
