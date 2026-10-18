---
type: project_overlay
status: candidate_only
created_at: 2026-06-06
project: misa-vaks-integration
source_record: raw/repos/2026-06-06-datawhalechina-agent-learning-hub-source.md
distillation: outputs/review/2026-06-06-datawhalechina-agent-learning-hub-candidate-distillation.md
truth_boundary: project overlay only; not reviewed knowledge; not architecture decision; not action basis
retrieval_policy:
  policy_kind: project_context_only
  default_retrieval: false
  action_basis_allowed: false
  warning_code: project_overlay_not_authority
tags:
  - project-overlay
  - misa
  - vaks-integration
  - agent-learning-hub
  - hermes
  - skills
  - candidate-research
---

# MISA Overlay: Agent Learning Hub Integration Notes

## 对 MISA 接入 VAKS 的一句话关系

Agent Learning Hub 给 MISA 的价值不是“照着学一套 agent 课程”，而是给我们一个接入资料库前的刹车片：

```text
别让 MISA 一上来读写整个资料库。
先把它当成一个受控调用方：
只读 context pack，
记录 trace，
反馈 usefulness / gap / correction，
需要写候选材料时再过 permission 和 review。
```

## 大白话版本

现在如果说“MISA 接入资料库”，这个词太大。应该拆成几种完全不同的事情：

```text
问资料库拿上下文
让资料库解释某个来源
让 MISA 帮忙起草候选点
把 MISA 使用后的反馈写回
让 MISA 发起 review_due
让 MISA 直接改知识
```

前五个可以逐步试。最后一个现在不该开。

## 可借的项目用法

### 1. Read-Only Context Provider First

MISA 第一阶段只应该拿：

```text
reviewed_support
candidate_orientation
project_overlay_context
raw_source_drilldown
known_gaps
warnings
```

返回给 MISA 的包必须显式写：

```text
action_basis_allowed: false
raw_is_provenance_only
candidate_not_action_basis
project_overlay_not_authority
```

这样 MISA 不会把“资料库里搜到了”误当成“资料库审过了”。

### 2. Context Request Contract

MISA 发请求时必须说清楚：

```yaml
request_id: string
caller: misa
task: string
project_scope: misa|global|other
risk_level: low|medium|high
requested_authority:
  - reviewed_only
  - reviewed_plus_candidate
  - raw_source_drilldown
intended_use:
  - answer
  - plan
  - code_change
  - external_action
  - review_draft
```

VAKS 根据这个决定：

```text
普通回答：轻 context pack
代码/行动：必须暴露 support/challenge/gap/risk
高风险：不给 action basis，要求 review/action gate
```

### 3. Context Pack Response Contract

候选 response 形状：

```yaml
context_pack_id: string
source_time: string
authority_buckets:
  reviewed_support: []
  reviewed_relations: []
  candidate_orientation: []
  project_overlays: []
  raw_source_drilldown: []
  feedback_hints: []
warnings:
  - raw_is_provenance_only
  - candidate_not_action_basis
  - overlay_not_authority
known_gaps: []
known_conflicts: []
temporal_scope: string
action_basis_allowed: false
required_next_gate: none|review|evidence_sufficiency|human_confirmation
```

重点不是字段名字，而是桶要分开：

```text
已审支持
候选理解
项目侧便签
原始来源
反馈痕迹
风险/缺口
```

### 4. Skill Pack Boundary

Agent Learning Hub 对 Skills 的拆法可以借给 MISA：

```text
retrieve-vaks-context
drilldown-source-anchor
draft-candidate-distillation
draft-evidence-packet
record-feedback-event
flag-review-due
```

每个 skill 必须有：

```text
when to use
allowed reads
allowed writes
forbidden writes
acceptance criteria
smoke test
rollback / failure wording
```

特别禁止：

```text
skill 直接写 wiki/claims
skill 直接写 wiki/decisions
skill 修改 truth_confidence
skill 创建 reviewed relation
skill 把 feedback 当 evidence
```

### 5. Feedback Event Writeback

MISA 可以帮助 VAKS 学会“哪些上下文有用”，但不能改 truth。

可写候选：

```yaml
feedback_event:
  context_pack_id: string
  caller: misa
  task: string
  outcome:
    usefulness: useful|partial|wrong_scope|missing|unsafe
    missing_context: []
    overincluded_context: []
    explicit_correction: string|null
  review_pressure:
    level: none|low|review_due
    reason: string|null
  raw_trace_location: string
```

边界：

```text
positive feedback -> weak usefulness signal
negative feedback -> review pressure
explicit correction -> review_due
none of these -> truth mutation
```

### 6. Eval Before More Agent Power

MISA 接 VAKS 前，先做 10-20 个固定任务：

```text
普通查询能否区分 reviewed/candidate/raw
项目 overlay 是否只作为 active-project context
raw URL 是否不被当成 support evidence
feedback event 是否不会改 truth
explicit correction 是否创建 review_due
stale/superseded 内容是否有 warning
高风险 action 是否拒绝 action_basis_allowed
MISA 是否能解释自己用了哪些 source anchors
permission denied 是否可恢复
context compaction 是否保留 provenance
```

验收看：

```text
success/failure
failure type
trace replay
cost/latency/tool_count
manual review notes
```

不看：

```text
回答看起来聪明
agent 自己说它遵守了
多个 agent 同意
一次 demo 成功
```

## MISA 接入台阶

### Step 0: No-Agent Backbrief

先回答：

```text
这个任务为什么需要 MISA 作为 agent？
普通 context pack 是否够？
是否涉及写文件、发消息、执行命令、外部行动？
```

### Step 1: Read-Only Context Pack

只开放：

```text
read-only search / assemble
no write
no review mutation
no action basis
```

### Step 2: Source Drilldown

允许 MISA 请求：

```text
source card
snapshot anchor
candidate distillation
project overlay
known gaps
```

仍然禁止：

```text
direct promotion
reviewed relation creation
truth confidence edit
```

### Step 3: Feedback Event

允许 MISA 写：

```text
outputs/feedback candidate event
```

不允许写：

```text
wiki/claims
wiki/decisions
wiki/patterns as reviewed
```

### Step 4: Skill Pack

把重复动作包成 skills，但每个 skill 都要声明权限和验收线。

### Step 5: Gateway / Permission Gate

如果 MISA 要触发工具或写文件：

```text
human confirmation
path scope
dry-run preview
trace
rollback note
```

### Step 6: Production Harness

只有前面都稳定后，才谈：

```text
long-running memory
background wakeups
automated context injection
multi-agent scouting
VPS integration
```

## 不借的部分

```text
不借整个学习路线作为 VAKS 主线架构。
不借 localStorage progress 作为 review status。
不借项目列表作为 adoption proof。
不借 MCP/A2A/ACP 名字作为安全证明。
不借 old/new framework 排名作为永久技术裁决。
不借 eval pass 作为 truth confidence。
不让 MISA 直接写 reviewed truth。
```

## 和当前 VAKS 主线的关系

当前主线仍然是：

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

MISA 最多先插在：

```text
activation / context pack / feedback event / candidate drafting
```

不能跳过：

```text
Evidence Packet
Evidence Support Check
Evidence Sufficiency Gate
Support-Challenge Review
Temporal Applicability Check
Action Guardrails
```

## Reopen 条件

可以重开这个 overlay，当用户明确要求：

```text
设计 MISA <-> VAKS connector
写 MISA 使用资料库的 skill pack
给 Hermes official gateway 接入 VAKS context builder
做 MISA-VAKS eval set
设计 feedback_event / context_pack schema
```

## 建议状态

```text
keep_as_candidate_overlay
project_scope_only
no_mainline_writeback_now
no_action_basis
```
