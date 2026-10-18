---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: review_due
derived_from:
  - raw/articles/2026-06-07-google-research-agentic-rag-sufficient-context-source.md
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
  - evidence-sufficiency
  - context-pack
  - known-omissions
  - agentic-rag
  - retrieval-routing
  - cross-corpus-retrieval
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - source_ref: raw/articles/2026-06-07-google-research-agentic-rag-sufficient-context-source.md
    selector_type: source_section
    selector_value: "Sufficient Context Agent / Agentic RAG"
  - source_ref: raw/articles/2026-06-07-google-research-agentic-rag-sufficient-context-source.md
    selector_type: source_section
    selector_value: "cross-corpus retrieval / reported results"
borrow_value: strong
borrow_order:
  - "P1: Sufficient Context Agent as a context-pack sufficiency gate before answer/action"
  - "P1: missing-context feedback loop that asks what is absent instead of blindly retrieving more"
  - "P1: cross-corpus routing by corpus descriptions and query intent"
  - "P1: sufficiency signal kept separate from truth confidence"
  - "P2: agentic query decomposition and iterative retrieval as candidate context assembly"
  - "P3: vendor-reported accuracy/latency figures as diagnostic motivation only"
avoid:
  - "Do not treat sufficiency classification as reviewed truth."
  - "Do not treat Google-reported metrics as VAKS benchmark authority."
  - "Do not adopt Gemini Enterprise infrastructure from this candidate note."
  - "Do not let an agentic retrieval loop promote knowledge or create action basis."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "approved VAKS task designs Evidence Sufficiency Gate, known-omission checks, context-pack assembly, or retrieval routing."
  support_when: "designing risk-sensitive answers, action-basis gates, context-pack coverage, or cross-source retrieval workflows."
  risk_when: "retrieval agent output, sufficiency labels, or vendor evaluation claims might be mistaken for truth confidence or action readiness."
  cold_references:
    - raw/articles/2026-06-07-google-research-agentic-rag-sufficient-context-source.md
tags:
  - candidate
  - provisional
  - google-research
  - gemini-enterprise
  - agentic-rag
  - sufficient-context-agent
  - context-pack
  - evidence-sufficiency
  - known-omissions
  - cross-corpus-retrieval
  - strong-borrow
  - P1
  - candidate-only
---

# Google Research Agentic RAG / Sufficient Context Candidate Distillation

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 人话压缩

这篇确实硬，算 `strong-borrow / P1`。

它强的地方不是“让 agent 多搜几次”。真正有价值的是：

```text
先问：当前 context pack 够不够？
不够的话：到底缺什么？
缺的东西应该去哪一个 corpus/source 里找？
找完再判断，而不是直接生成答案。
```

这刚好打中 VAKS 的关键问题：

```text
context pack coverage
known omissions
Evidence Sufficiency Gate
risk-sensitive answer
action basis boundary
```

## Candidate Points

### 1. `sufficient-context-gate-before-generation`

候选结论：在生成最终回答或行动建议之前，应先判断当前 context pack 是否足够支撑这个任务。

对 VAKS 的适配：

```text
question / task
-> candidate context pack
-> sufficiency check
-> answer if sufficient
-> otherwise produce missing-context request
```

边界：

```text
sufficient context != true answer
sufficient context != reviewed evidence
sufficient context != action basis by itself
```

### 2. `missing-context-feedback-loop`

候选结论：检索不足时，不应该只说 "retrieve more"。更好的方式是输出具体缺口：

```text
missing entity
missing source
missing comparison
missing time/version scope
missing counterevidence
missing warrant
```

对 VAKS 的适配：

- 能增强 `known_omission_check`。
- 能让 Evidence Sufficiency Gate 从抽象检查变成可执行下一步。
- 能把 "not enough evidence" 转成具体 review queue item。

### 3. `cross-corpus-retrieval-routing`

候选结论：复杂任务不应把所有来源放进一个平面检索池。不同 corpus 应有描述和路由逻辑。

对 VAKS 的适配：

```text
raw source cards
candidate distillations
review queue
wiki summaries
project overlays
feedback ledger
decisions / action records
```

这些应该能按任务意图路由，而不是都混在一个向量库里。

边界：

```text
corpus route = where to search
corpus route != source reliability
corpus route != truth tier
```

### 4. `sufficiency-signal-not-truth-confidence`

候选结论：sufficient context 是“回答准备度”信号，不是事实真值信号。

对 VAKS 的适配：

```text
context sufficiency = enough material to evaluate or answer within scope
evidence support = source span actually supports a point
truth confidence = later reviewed claim judgment
action basis = stricter action-facing gate
```

这个边界非常适合写进 VAKS 风险提示。

### 5. `agentic-rag-as-context-pack-assembly`

候选结论：Agentic RAG 对 VAKS 最合理的借法，是把它看作 context-pack assembly / coverage audit，而不是自动知识引擎。

可借：

- query decomposition
- corpus selection
- iterative retrieval
- missing-context feedback
- source-grounded final context pack

不借：

- agent 自动判断真理
- agent 自动晋级 reviewed knowledge
- agent 自动生成 action basis

## 与已有 Google Hybrid Search 条目的关系

之前的 Google Cloud hybrid-search 条目解决的是：

```text
召回通道怎么组合：keyword/token + semantic/vector + RRF + rerank
```

这篇解决的是：

```text
召回之后，上下文够不够？
缺什么？
要不要跨 corpus 继续查？
```

所以两者不是重复：

```text
hybrid search = recall mechanics
agentic sufficient context = context-pack sufficiency and omission repair
```

## 标签等级

```yaml
tagging_decision: tagged
tag_level: strong-borrow
borrow_value: strong
borrow_order_primary: P1
```

人话：

```text
强，P1。
它能补 VAKS 最关键的“证据够不够 / context pack 是否可答 / 缺口怎么回补”。
但只能进候选层，不能替代 reviewed knowledge 或 action basis。
```

## 不吸收

- 不吸收 Google 产品依赖。
- 不吸收 vendor metrics 作为 VAKS 评测结论。
- 不吸收 "sufficient" 作为 truth/confidence。
- 不吸收 agentic retrieval as automatic promotion。

## Reopen Trigger

重新打开这条候选的条件：

- VAKS 设计 Evidence Sufficiency Gate。
- VAKS 设计 context-pack coverage map。
- VAKS 设计 known omissions / missing evidence workflow。
- VAKS 设计跨 source/corpus 检索。
- VAKS 要回答 risk-sensitive 或 action-facing 问题。
