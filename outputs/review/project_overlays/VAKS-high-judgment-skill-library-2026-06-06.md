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
source_record: raw/articles/2026-06-06-pasted-high-judgment-skill-library-source.md
distillation: outputs/review/2026-06-06-pasted-high-judgment-skill-library-candidate-distillation.md
target_ref: raw/articles/2026-06-06-pasted-high-judgment-skill-library-source.md
target_selector: source_record:2026-06-06-pasted-high-judgment-skill-library
target_hint: "Use as a future VAKS skill-library / procedural-memory reference, not as reviewed knowledge or agent runtime adoption."
truth_boundary: project overlay only; not reviewed knowledge; not architecture decision; not action basis
tagging_decision: tagged
tag_level: medium-borrow
tag_level_reason: "Useful for future VAKS procedural-memory and high-judgment workflow skill design; kept medium because it is a conceptual source and no skill registry/runtime is being adopted now."
project_borrow_scope:
  - high-judgment VAKS skill candidates
  - skill boundary and state-source fields
  - failure-record to skill-maintenance loop
  - workflow-based skill map instead of prompt collection
  - human stop rules for high-risk review/action tasks
project_non_borrow_scope:
  - complete skill library now
  - skill runtime as truth layer
  - automatic reviewed-knowledge mutation by skills
  - old project experience as global default
  - trigger evaluation as evidence or truth test
project_reopen_trigger:
  - "VAKS starts designing a source-review, evidence-packet, context-pack, feedback, or action-guardrail skill."
  - "VAKS opens an agent runtime / procedural memory lane."
  - "A skill failure record needs to update routing, boundaries, stop rules, or maintenance guidance."
confirmation_basis:
  - source card and candidate distillation already exist
  - overlay content is project-scoped and candidate-only
  - no runtime adoption; no promotion to reviewed knowledge
last_checked_at: 2026-06-07
expires_at: 2026-07-07
borrow_value: medium
borrow_order:
  - "P2: high-judgment workflow skills for source review, evidence packet drafting, context-pack assembly, and action guardrails"
  - "P2: skill field schema with when_to_use, when_not_to_use, state_source, judgment_points, stop rules, output format, failure modes, and maintenance"
  - "P2: failure records feeding skill maintenance without mutating truth"
  - "P3: full skill-library organization as later agent-runtime reference"
avoid:
  - "Do not build a complete skill library before VAKS has approved agent-runtime scope."
  - "Do not let skills write reviewed knowledge or truth confidence."
  - "Do not treat trigger evaluation as evidence support."
tags:
  - VAKS
  - project-overlay
  - skill-library
  - procedural-memory
  - agent-runtime
  - high-judgment-workflow
  - medium-borrow
  - P2
  - candidate-only
---

# VAKS Overlay: High-Judgment Skill Library

## 对 VAKS 的一句话关系

这篇文章给 VAKS 的启发是：

```text
未来如果做 skill library，不要先收集 prompt。
先把那些我们每次都要亲自复核的高判断流程，做成可继承的操作记忆。
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
它适合未来 VAKS 做 skill library / procedural memory 时使用。
现在不算 P1，因为还没有进入 agent runtime 实装阶段；它是 P2 支撑参考。
```

## 可借的项目用法

### 1. VAKS 第一批候选 skill 类型

如果未来要做 VAKS skills，优先候选不是“帮我总结文章”这种轻任务，而是：

```text
source review skill
evidence packet drafting skill
support-challenge review skill
context pack assembly skill
feedback triage skill
action guardrail / backbrief skill
project closeout / handoff skill
```

原因：

```text
这些流程高频、判断重、容易受旧状态污染、错误代价高。
```

### 2. 每个 skill 的最小字段

未来 VAKS skill 至少需要：

```text
when_to_use
when_not_to_use
read_first / state_source
judgment_points
stop_and_ask_human_rules
output_format
failure_modes
maintenance_rules
```

### 3. Skill Library 五层可作为候选组织法

```text
Skill Map:
  按 workflow，而不是按工具。

Boundaries:
  防止 skill 抢别人的职责。

State Source:
  防止旧项目状态污染当前任务。

Routing:
  渐进加载，不全量塞 context。

Maintenance:
  失败修规则，过期删规则，误触发收窄边界。
```

### 4. Failure Records 接入 Use Ledger

这篇文章和 VAKS feedback 机制可以对齐：

```text
feedback-event:
  用户说不好 / 跑偏 / 漏证据

failure mode:
  为什么跑偏，可以怎样修 skill

skill maintenance:
  修改入口、边界、state source、stop rule 或 examples
```

注意：

```text
failure mode 更新 skill，不直接更新 truth。
```

## 不借的部分

```text
不借成“现在就建完整 skill library”。
不把 skill library 放进 truth core。
不让 skill 自动改 reviewed knowledge。
不让旧项目经验默认变成新项目规则。
不把 trigger eval 当作 truth/evidence 测试。
```

## 和当前主线关系

当前 VAKS 主线仍然是：

```text
source
-> candidate
-> calibration / point collision
-> review
-> reviewed node / relation
-> context pack / action basis
-> action
-> use ledger / feedback
```

Skill library 最多属于：

```text
future agent runtime
procedural memory
activation / routing support
review/action workflow helper
```

它不能跳过：

```text
review gate
evidence support
evidence sufficiency
human stop rules
owner-final decisions
```

## 建议状态

```text
keep_as_candidate_overlay
use_when_reopening_agent_skill_registry_or_procedural_memory
no_mainline_writeback_now
```
