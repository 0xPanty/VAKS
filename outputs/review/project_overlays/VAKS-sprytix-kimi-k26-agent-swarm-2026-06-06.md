---
record_kind: project_overlay
type: project_overlay
status: candidate
knowledge_status: candidate
created_at: 2026-06-06
processing_tier: medium
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project: verified-action-knowledge-system
project_id: verified-action-knowledge-system
source_record: raw/articles/2026-06-06-x-sprytix-kimi-k26-agent-swarm-source.md
distillation: outputs/review/2026-06-06-x-sprytix-kimi-k26-agent-swarm-candidate-distillation.md
target_ref: raw/articles/2026-06-06-x-sprytix-kimi-k26-agent-swarm-source.md
target_selector: source_record:2026-06-06-x-sprytix-kimi-k26-agent-swarm
target_hint: "Use as a future candidate-scouting / multi-worker research reference, not as review authority or action basis."
truth_boundary: project overlay only; not reviewed knowledge; not architecture decision; not action basis
tagging_decision: tagged
tag_level: medium-borrow
tag_level_reason: "Useful for future parallel candidate scouting and worker-notebook discipline; kept medium because it is a scouting/runtime idea, not a truth, review, or action mechanism."
project_borrow_scope:
  - parallel source and counterexample scouting
  - worker notebook for query scope, anchors, uncertainty, and skipped areas
  - aggregation manifest for merged, conflicting, dropped, and still-unreviewed findings
  - document-to-skill idea for review workflow helpers
project_non_borrow_scope:
  - agent count as credibility signal
  - generated swarm report as action basis
  - automatic decomposition as audit substitute
  - deep research as truth update
  - document-to-skill as knowledge promotion
project_reopen_trigger:
  - "VAKS starts a parallel source scouting or coverage-scan lane."
  - "VAKS needs a worker notebook / aggregation manifest format."
  - "Agent-generated research needs to be kept candidate-only before review."
confirmation_basis:
  - source card and candidate distillation already exist
  - overlay content is project-scoped and candidate-only
  - no agent runtime execution; no promotion to reviewed knowledge
last_checked_at: 2026-06-07
expires_at: 2026-07-07
borrow_value: medium
borrow_order:
  - "P2: parallel source/counterexample/coverage scouting as candidate discovery"
  - "P2: worker notebook fields for source scope, anchors, negative findings, uncertainty, and skipped areas"
  - "P2: aggregation manifest before anything becomes review-ready"
  - "P3: document-to-skill as later procedural-memory reference"
avoid:
  - "Do not treat many agents or generated reports as credibility."
  - "Do not let parallel scouting bypass Evidence Packet or review gates."
  - "Do not turn Document to Skill into knowledge promotion."
tags:
  - VAKS
  - project-overlay
  - kimi
  - agent-swarm
  - candidate-research
  - parallel-scouting
  - worker-notebook
  - aggregation-manifest
  - medium-borrow
  - P2
  - candidate-only
---

# VAKS Overlay: Kimi K2.6 Agent Swarm

## 对 VAKS 的一句话关系

Kimi Agent Swarm 给 VAKS 的启发是：

```text
大规模资料侦察可以并行。
但可信结论仍然必须串行过 review gate。
```

## 标签等级

```yaml
tagging_decision: tagged
tag_level: medium-borrow
borrow_value: medium
borrow_order_primary: P2
```

人话：

```text
有帮助，打标签。
它适合未来 VAKS 做并行资料侦察、反例扫描、coverage scan 时借用。
但它不能提高可信度本身，所以不是 P1 strong；它是 P2 支撑参考。
```

## 可借的项目用法

### 1. Candidate Scouting Lane

可临时借为：

```text
并行搜 source
并行找反例
并行检查竞品 / repo / paper
并行补 known omissions
```

落点只能是：

```text
raw source
candidate point
review question
missing evidence
coverage note
```

### 2. Worker Notebook

如果以后跑多 agent，VAKS 应要求每个 worker 留：

```text
worker goal
search query / source scope
source anchors
candidate findings
negative findings
uncertainty
skipped areas
```

没有 worker notebook 的最终报告，不应进入 review-ready。

### 3. Aggregation Manifest

coordinator 汇总时要留：

```text
what was merged
what conflicted
what was dropped
which source anchors support which candidate
what still needs review
```

这可以变成未来 `outputs/review` 的候选格式，但不是当前主线必需项。

### 4. Document to Skill Boundary

VAKS 可以借 `Document to Skill` 的思想做：

```text
source-review skill
evidence-packet drafting skill
paper-scouting skill
context-pack assembly skill
```

但 skill 只管怎么做，不管什么是真的。

## 不借的部分

```text
不借 300 agents 作为可信度信号。
不借 cost-saving marketing claim。
不借 automatic decomposition as audit substitute。
不借 generated report as action basis。
不借 Document to Skill as knowledge promotion。
不借 Deep Research as automatic truth update。
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

Kimi Agent Swarm 最多插在：

```text
source discovery / candidate discovery / coverage scan
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

## 建议状态

```text
keep_as_candidate_overlay
revisit_if_user_reopens_agent_runtime_or_parallel_scouting
no_mainline_writeback_now
```
