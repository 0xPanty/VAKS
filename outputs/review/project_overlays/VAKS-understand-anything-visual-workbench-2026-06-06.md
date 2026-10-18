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
source_record: raw/repos/2026-06-06-lum1104-understand-anything-source.md
distillation: outputs/review/2026-06-06-lum1104-understand-anything-candidate-distillation.md
target_ref: raw/repos/2026-06-06-lum1104-understand-anything-source.md
target_selector: source_record:2026-06-06-lum1104-understand-anything
target_hint: "Use as a future VAKS visual workbench / graph dashboard pilot reference, not as truth graph or reviewed relation engine."
truth_boundary: project overlay only; not reviewed knowledge; not architecture decision; not action basis
tagging_decision: tagged
tag_level: medium-borrow
tag_level_reason: "Useful for future visual workbench and candidate/review map design; kept medium because it needs a VAKS adapter and must not become a truth or relation authority."
project_borrow_scope:
  - source-to-candidate visual map
  - collision map
  - evidence packet completeness map
  - project overlay map
  - feedback loop map
  - VAKS node/edge adapter for candidate and review preparation
project_non_borrow_scope:
  - truth graph
  - evidence support engine
  - reviewed relation generator
  - decision approval surface
  - action basis
  - default VAKS mechanism
project_reopen_trigger:
  - "VAKS starts a visual workbench or knowledge graph dashboard pilot."
  - "VAKS needs onboarding/recovery maps for a batch of sources and candidate distillations."
  - "VAKS needs to inspect candidate collisions, missing evidence, or project-overlay contamination visually."
confirmation_basis:
  - source card and candidate distillation already exist
  - overlay content is project-scoped and candidate-only
  - no Understand Anything runtime installed or executed
  - no promotion to reviewed knowledge
last_checked_at: 2026-06-07
expires_at: 2026-07-07
borrow_value: medium
borrow_order:
  - "P2: source-to-candidate, collision, evidence packet, project overlay, and feedback-loop maps"
  - "P2: VAKS-specific node/edge adapter for visual workbench use"
  - "P2: onboarding/recovery and maintenance diagnostic dashboard"
  - "P3: full graph-dashboard automation after sandbox validation"
avoid:
  - "Do not treat visual graph edges as reviewed relations."
  - "Do not treat supports_candidate, related, cites, or contradicts edges as evidence support."
  - "Do not install or run it as a default VAKS mechanism from this overlay."
tags:
  - VAKS
  - project-overlay
  - understand-anything
  - visual-workbench
  - knowledge-graph
  - candidate-review-map
  - collision-map
  - medium-borrow
  - P2
  - candidate-only
---

# VAKS Overlay: Understand Anything Visual Workbench

## 对用户问题的直接回答

可以帮，但要说准：

```text
它不是把资料“做成好看的图标包”。
它更像把资料做成“可点击、可搜索、可聚焦邻域的知识图谱 dashboard”。
```

对 VAKS 最有用的不是 icon，而是：

```text
source / candidate / claim / topic / relation / conflict / review_due 的可视化分析工作台。
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
它适合未来 VAKS 做 visual workbench / candidate review map / recovery dashboard。
但图谱边不能当 reviewed relation，所以不是 strong；它是 P2 支撑参考。
```

## 放在 VAKS 哪一层

只能放这里：

```text
Retrieval / Activation
Candidate Review Preparation
Maintenance Diagnostic
Onboarding / Recovery
Visual Workbench
```

不能放这里：

```text
Truth Layer
Evidence Support
Reviewed Relation
Decision Approval
Action Basis
```

人话：

```text
图谱负责帮我们看见“该查哪里、哪里可能撞了、哪里没证据”。
review 负责决定“什么能算数”。
```

## VAKS 适配图谱节点

如果我们以后为 VAKS 做 adapter，不建议照抄它的 5 类节点，而是映射成 VAKS 自己的节点：

```text
source_record
raw_artifact
source_anchor
candidate_distillation
candidate_point
claim_under_review
evidence_item
reviewed_claim
reviewed_relation
candidate_pattern
anti_pattern
decision
risk
project_overlay
context_pack
action_basis
feedback_event
review_due
```

Understand Anything 原生类型可以粗映射为：

```text
source  -> source_record / raw_artifact
article -> source_card / distillation / overlay
claim   -> candidate_point / claim_under_review
topic   -> VAKS section / review lane / knowledge family
entity  -> tool / repo / paper / person / project
```

## VAKS 适配边

它的边可以借，但要扩充：

```text
captured_from
extracted_as
mentions
related_candidate
supports_candidate
challenges_candidate
scopes_candidate
contradicts
builds_on
supersedes
promoted_to
review_due_from
used_in_context_pack
used_in_action_basis
feedback_on
activates
```

关键边界：

```text
supports_candidate != reviewed support
cites != evidence support
related != reviewed relation
contradicts != settled contradiction
```

## 最有价值的 VAKS 画法

### 1. Source To Candidate Map

画：

```text
raw source
-> source card
-> candidate distillation
-> candidate point
-> review queue
```

用处：

```text
看哪些资料已经消化；
哪些只有 source 没有 distillation；
哪些 candidate 没有 evidence anchor；
哪些已经进 review queue。
```

### 2. Collision Map

画：

```text
candidate point A
<-> contradiction / challenge / scope conflict
candidate point B
```

用处：

```text
帮 reviewer 快速找到“冲突在哪里”。
```

边界：

```text
图上出现冲突，只代表 review pressure，不代表谁对谁错。
```

### 3. Evidence Packet Map

画：

```text
candidate point
-> source anchor
-> evidence item
-> warrant
-> scope/risk
-> challenge check
```

用处：

```text
看一个点够不够 review-ready。
```

边界：

```text
这张图是 evidence packet completeness view，不是 truth score。
```

### 4. Project Overlay Map

画：

```text
generic knowledge point
-> borrowed by project overlay
-> project-specific usage
-> feedback / outcome
```

用处：

```text
防止 project layer 污染 generic knowledge point。
```

### 5. Feedback Loop Map

画：

```text
action / answer
-> use ledger
-> feedback event
-> activation adjustment / review_due
```

用处：

```text
解释反馈为什么只改激活和复查压力，不直接改 truth。
```

## 最小试验建议

不要直接扫整个 `C:\Users\Administrator\Documents\资料库`。

先用 sandbox：

```text
outputs/review/understand-anything-vaks-visual-pilot-2026-06-06/
```

放入 10-20 个文件的复制件或 adapter 输出：

```text
raw/repos/*source.md
raw/articles/*source.md
outputs/review/*candidate-distillation.md
outputs/review/project_overlays/*.md
REVIEW_QUEUE.md 的一小段
```

目标不是生成全库图，而是验证：

```text
能否暴露孤立 source
能否暴露 candidate collision
能否暴露 missing evidence
能否帮新窗口快速理解一批资料
会不会误导人把候选边当 truth
```

## 现在不做的事

```text
不安装 Understand Anything skill。
不运行 /understand-knowledge。
不生成 .understand-anything/。
不写入 wiki/ 正式知识层。
不改 README / SCHEMA / ARCHITECTURE_PRINCIPLES。
不把它设为 VAKS 默认机制。
```

## 建议状态

```text
keep_as_candidate_overlay
strong_candidate_for_visual_workbench_pilot
requires_vaks_adapter_before_use
no_mainline_writeback_now
```

一句话：

```text
这是一个值得压榨的“看图分析层”，但必须拴在 VAKS 的 candidate/review 边界外面。
```
