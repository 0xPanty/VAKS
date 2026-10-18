---
type: project_overlay
status: candidate_only
created_at: 2026-06-07
project: misa-vaks-integration
source_record: raw/repos/2026-06-07-infiniflow-ragflow-source.md
distillation: outputs/review/2026-06-07-infiniflow-ragflow-candidate-distillation.md
architecture_review: wiki/summaries/2026-06-07-infiniflow-ragflow-architecture-review.md
truth_boundary: project overlay only; not reviewed knowledge; not architecture decision; not action basis
retrieval_policy:
  policy_kind: project_context_only
  default_retrieval: false
  action_basis_allowed: false
  warning_code: project_overlay_not_authority
borrow_value: strong
borrow_order:
  - "P1: scoped read-only context engine for MISA/VAKS."
  - "P1: authority-bucketed retrieval response and all-access MCP rejection."
  - "P1: feedback event writeback as activation-only, not truth mutation."
  - "P2: retrieval knobs as diagnostics and adapter shapes for future tools."
  - "P3: memory/code-sandbox/full runtime as later-stage references."
avoid:
  - "MISA all-access retrieval"
  - "MISA writes truth from memory or feedback"
  - "score/rank/citation/KG as proof"
dev_context_hint:
  recommended_layer: support_with_required_risk
  core_when: "Only during an approved MISA/VAKS read-only context contract task."
  support_when: "Designing scoped retrieval, context packs, feedback events, or agent gateway boundaries."
  risk_when: "Any plan involves writeback, action basis, all-access retrieval, code execution, or truth mutation."
tags:
  - project-overlay
  - misa
  - vaks-integration
  - ragflow
  - context-engine
  - retrieval
  - mcp
  - candidate-research
---

# MISA / VAKS Overlay: RAGFlow Context Engine Notes

## 对 MISA 接入 VAKS 的一句话关系

RAGFlow 给 MISA 的价值不是“让 MISA 用一个 RAG 产品读全库”，而是提醒我们：

```text
MISA 接资料库，第一步应该是受控读取 context pack。
不是全库 retrieval。
不是直接写 memory。
不是直接改 wiki。
不是拿相似度分数当判断。
```

## 大白话版本

RAGFlow 很强，但它强在“把资料加工成上下文”和“把上下文给 agent 用”。这正好可以帮我们拆 MISA 接入：

```text
MISA 问：这件事需要哪些资料？
VAKS 回：这里是分桶后的上下文，哪些是已审，哪些是候选，哪些只是原始来源，哪些只是项目便签。
MISA 用：只读、带警告、留 trace。
MISA 反馈：这个上下文有用/不够/错范围/需要 review。
VAKS 记录：feedback event 或 review_due。
VAKS 不做：让 MISA 自动改 truth。
```

## 借鉴序位 / 开发上下文梯度

```yaml
borrow_value: strong
borrow_order:
  P1:
    - scoped read-only context engine for MISA/VAKS
    - authority-bucketed retrieval response
    - all-access MCP rejection
    - feedback event writeback as activation-only
  P2:
    - retrieval knobs as diagnostics
    - Dify/MCP/API adapter shape
    - execution receipt / task trace
  P3:
    - memory stream taxonomy
    - code sandbox risk contract
    - full RAGFlow runtime
avoid:
  - MISA all-access retrieval
  - MISA writes truth from memory or feedback
  - score/rank/citation/KG as proof
dev_context_layer:
  recommended: Support with required Risk
  Core: only for an approved MISA/VAKS read-only context contract task
  Support: scoped retrieval / context pack / feedback event / agent gateway design
  Risk: writeback / action basis / all-access retrieval / code execution / truth mutation
  Cold References: source record and snapshot
```

这条 overlay 在开发区里的正确位置：

```text
不是常驻 Core。
是强 Support。
一旦开始讨论 MISA 写回、action basis、全库 retrieval、code execution，就必须同时加载 Risk。
```

## 可借的项目用法

### 1. Context Engine as Read-Only Service

RAGFlow 的 Agent Context Engine 思路可以借，但在 VAKS 里要换成更硬的边界：

```text
Knowledge Core -> reviewed / candidate / raw source buckets
Memory Layer -> MISA trace and derived memory, not truth
Tool Orchestrator -> skill/tool retrieval, not tool permission
```

MISA 第一阶段只应该拿：

```text
reviewed_support
reviewed_relations
candidate_orientation
project_overlay_context
raw_source_drilldown
known_gaps
known_conflicts
warnings
```

默认：

```yaml
action_basis_allowed: false
truth_mutation_allowed: false
writeback_allowed: false
```

### 2. Scope Is Mandatory

RAGFlow MCP retrieval 如果省略 dataset IDs，可以解析所有可访问 dataset。对 VAKS 这是危险便利。

MISA 请求必须显式写：

```yaml
request_id: string
caller: misa
project_scope: misa-vaks-integration
task: string
intended_use:
  - answer
  - plan
  - code_change
  - review_draft
  - external_action
risk_level: low|medium|high
requested_authority:
  - reviewed_only
  - reviewed_plus_candidate
  - raw_source_drilldown
```

拒绝条件：

```text
no project_scope -> reject
no intended_use -> reject
no requested_authority -> reviewed_only fallback or reject
external_action with candidate/raw only -> reject action basis
```

### 3. Context Pack Must Separate Buckets

RAGFlow API 返回 chunks/content/score/title/metadata。VAKS 不能只返回一个混合文本块。

候选 response 形状：

```yaml
context_pack_id: string
source_time: string
request_scope: string
authority_buckets:
  reviewed_support: []
  reviewed_relations: []
  candidate_orientation: []
  project_overlays: []
  raw_source_drilldown: []
  feedback_hints: []
diagnostics:
  retrieval_backend: string
  query_rewrite_used: false
  filters_applied: {}
  top_k: integer
  known_overinclude_risk: []
warnings:
  - raw_is_provenance_only
  - candidate_not_action_basis
  - project_overlay_not_authority
known_gaps: []
known_conflicts: []
temporal_scope: string
action_basis_allowed: false
required_next_gate: none|review|evidence_sufficiency|human_confirmation
```

重点：

```text
score 放 diagnostics。
support 放 evidence bucket。
candidate 放 orientation bucket。
overlay 放 active-project bucket。
raw source 放 drilldown bucket。
```

### 4. Retrieval Knobs Are Diagnostics

RAGFlow 暴露：

```text
similarity_threshold
vector_similarity_weight
top_k
rerank_id
metadata filters
KG toggle
child-parent expansion
```

VAKS 可以借这些，但字段意义必须改清楚：

```text
这些是“怎么找”的参数。
不是“找到以后能不能信”的参数。
```

MISA 不应该看到：

```text
score 0.92 therefore true
rerank top 1 therefore action-ready
KG says related therefore reviewed relation
```

MISA 应该看到：

```text
retrieval found possible context
authority bucket says candidate/raw/reviewed
warnings say whether action basis is blocked
```

### 5. Feedback Writeback Is Activation-Only

RAGFlow 的 chunk feedback 会调 `pagerank_fea`。这个对 VAKS 很有启发，但只能这么用：

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
  activation_hint:
    allowed: true
    truth_mutation_allowed: false
```

边界：

```text
positive feedback -> weak usefulness signal
negative feedback -> review pressure
explicit correction -> review_due
none of these -> truth mutation
```

### 6. Memory Needs Quarantine

RAGFlow memory 把 raw conversation、semantic memory、episodic memory、procedural memory 分开。MISA 可以借这个，但不能把 memory 写进 VAKS truth。

候选规则：

```text
raw conversation -> raw trace / agent ledger
semantic memory -> derived summary, project-scoped
episodic memory -> continuity hint
procedural memory -> MISA-side operating note
explicit correction -> feedback event + review_due
truth update -> separate review gate
```

禁止：

```text
MISA says user corrected it -> auto change wiki claim
MISA remembers preference -> auto change general knowledge
MISA summary says X -> auto reviewed support
```

### 7. Code / Tool Execution Stays Later

RAGFlow has a code component with sandbox controls. That is useful as a warning, not a green light.

MISA access stages should be:

```text
stage 1: read-only context retrieval
stage 2: draft candidate distillation under explicit folder boundary
stage 3: record feedback events and review_due suggestions
stage 4: limited tool/script execution after explicit human confirmation
```

Do not start with:

```text
MISA can execute code based on retrieved context
MISA can run arbitrary tools because retrieval found a relevant doc
MISA can modify the vault after answering correctly once
```

## Direct Borrowing Candidates

| Borrow | Project Use | Boundary |
|---|---|---|
| Agent Context Engine decomposition | Split documents/memory/tools for MISA access. | Not truth architecture. |
| Retrieval endpoint shape | Build read-only VAKS context request/response. | Add authority buckets. |
| Child-parent locate-then-expand | Return enough context without overfeeding. | Expansion not support. |
| Retrieval testing | Validate fixed MISA tasks before rollout. | Diagnostics only. |
| Dify-compatible adapter idea | External consumers need simple adapter contracts. | Compatibility not authority. |
| MCP retrieval tool idea | Future local tool for MISA. | Scope required; no all-access default. |
| Chunk feedback ranking | Feedback affects activation usefulness. | No truth mutation. |
| RecordingContext | Execution receipts for source-intake/context-pack builders. | Trace not verdict. |
| Sandbox risk controls | Later code/tool execution contract. | Not stage-one scope. |

## What Not To Borrow

```text
Do not make RAGFlow the vault source of truth.
Do not map similarity score to truth confidence.
Do not map citation markers to evidence support.
Do not map auto KG/RAPTOR output to reviewed relations.
Do not let feedback mutate reviewed knowledge.
Do not let MISA omit scope and query all accessible knowledge.
Do not enable code execution before read-only context access is stable.
```

## Minimal MISA Trial Inspired by RAGFlow

Candidate trial:

```text
10 fixed MISA tasks
read-only VAKS context pack
bucketed response
MISA must state which bucket it used
MISA must not claim candidate/raw as action basis
MISA may submit feedback_event
VAKS records diagnostic result only
```

Pass criteria:

```text
MISA distinguishes reviewed/candidate/raw/project overlay.
MISA refuses action basis when only candidate/raw exists.
MISA asks for review/evidence gate on high-risk use.
MISA feedback does not mutate truth.
Retrieval diagnostics are visible but not authoritative.
```

Fail criteria:

```text
MISA says "found in VAKS" as if it means reviewed.
MISA uses score/rank/citation as proof.
MISA ignores scope.
MISA treats project overlay as global knowledge.
MISA writes directly to wiki truth.
```

## Suggested Next Candidate Contract

This overlay suggests a future candidate file, not a mainline edit yet:

```text
outputs/review/2026-xx-xx-misa-vaks-readonly-context-contract-candidate.md
```

It should include:

- required request fields
- bucketed response fields
- warning codes
- feedback event writeback
- retrieval diagnostics
- rejection conditions
- 10-task test set

## Bottom Line

RAGFlow is a strong pressure test for MISA/VAKS integration.

The keeper:

```text
Give MISA a scoped context engine, not a truth backdoor.
```

The guardrail:

```text
Every retrieved thing must say what kind of thing it is:
reviewed support, candidate orientation, project overlay, raw source, feedback hint, or diagnostic.
```
