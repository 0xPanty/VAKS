---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
source_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source.md
derived_from:
  - raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source.md
  - raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source/pasted-text.txt
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
  - agentic-loop-design
  - loop-engineering
  - verify-state-stop
  - cost-per-accepted-change
  - automation-skill-verifier
  - self-checking-loop
possible_project_refs:
  - verified-action-knowledge-system
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-loop-core-verify-state-stop.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-loop-worth-building-test.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-coding-loop-spec.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-five-building-blocks.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-cost-per-accepted-change.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-manual-skill-loop-schedule-order.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-self-checking-light-loop.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-mira-everyday-loop-claims.md
point_anchor_refs:
  - "pasted-text.txt:28-40"
  - "pasted-text.txt:41-47"
  - "pasted-text.txt:48-63"
  - "pasted-text.txt:63-73"
  - "pasted-text.txt:75-84"
  - "pasted-text.txt:85-91"
  - "pasted-text.txt:92-124"
  - "pasted-text.txt:125-137"
borrow_value: strong
borrow_order: P1_support
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "An approved task is specifically deciding whether to build a loop, designing a loop guardrail, or explaining lightweight vs heavy loop adoption."
  support_when: "Loop evaluation, recurring task automation, coding-loop scaffolding, operator loop cost controls, self-checking prompt design, and everyday-loop UX comparison."
  risk_when: "Mira/product claims, Codex/Claude capability claims, app counts, cost estimates, or productized automations are being treated as verified facts or action basis."
  cold_references:
    - raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source.md
    - raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source/pasted-text.txt
avoid:
  - "Do not treat platform/product claims as verified."
  - "Do not build loops for tasks that fail the repeated/objective/end-to-end/auto-reject test."
  - "Do not treat model self-scoring as equivalent to external verification."
  - "Do not schedule a loop before one manual run is reliable."
  - "Do not treat Mira examples as confirmed capability evidence without separate source checks."
tags:
  - candidate
  - provisional
  - loop-engineering
  - verify-state-stop
  - cost-control
---

# 候选蒸馏：Anatoli Kopadze / Loops explained

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 一句话结论

这篇是目前这一组 Loop 材料里最像“解释层 / 入门边界层”的一篇。

它最值得借的不是 Mira 产品描述，而是把 loop 说成三个硬条件：

```text
verify:
  有东西能自动拒绝坏结果

state:
  每轮记住试过什么、失败什么、下一步是什么

stop:
  成功停止，或者到硬限制停止并报告
```

再加一个非常重要的准入测试：

```text
只有当任务重复、可自动拒绝坏输出、agent 能端到端完成、done 是客观的，
才值得做重型 loop。
```

## Source

```yaml
derived_from:
  - raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source.md
  - raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source/pasted-text.txt
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-loop-core-verify-state-stop.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-loop-worth-building-test.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-coding-loop-spec.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-five-building-blocks.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-cost-per-accepted-change.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-manual-skill-loop-schedule-order.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-self-checking-light-loop.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-mira-everyday-loop-claims.md
```

## Candidate Points

### Candidate Point 1: Loop Is Not Repetition; It Is Repetition With A Gate

The article's best definition:

```text
DISCOVER
PLAN
EXECUTE
VERIFY
ITERATE
```

But the author correctly says verify is the heart. For VAKS:

```text
no gate
-> not a loop
-> just an agent agreeing with itself repeatedly
```

This should be a standing warning for future loop designs.

### Candidate Point 2: State And Stop Are As Important As Verify

Useful triad:

```text
verify = know whether result meets goal
state = know what was tried and what failed
stop = know when to stop or give up
```

For VAKS source-intake/operator loops, this maps to:

```text
ledger / run state
candidate output
diagnostic gate
stop condition
summary on stop
```

### Candidate Point 3: The Four-Condition Test Prevents Loop Overuse

The article gives a clean filter:

```text
task repeats at least weekly
bad output can be automatically rejected
agent can do the work end-to-end
done is objective
```

If any condition fails, keep it manual or semi-manual.

This is a strong VAKS borrow because it protects ordinary capture from becoming heavy process.

### Candidate Point 4: Five Building Blocks Are Useful, But Product Claims Are Not Proof

The article names:

```text
automation
skill
sub-agents
connectors
verifier
```

This aligns with prior Loop sources:

```text
Agent-Loop-Skills:
  skill + artifact + signal + ledger + stop

loop-engineer-template:
  shared memory + harness + verifier/PR proof

Anatoli:
  automation + skill + sub-agent + connector + verifier
```

But claims about which product ships what are not accepted as verified here.

### Candidate Point 5: Cost Per Accepted Change Is The Right Economic Metric

The article's cost warning is high-value:

```text
context is resent each iteration
context grows each pass
maker/checker doubles model reads
parallel fleets multiply cost
```

The proposed useful metric:

```text
cost per accepted change
```

For VAKS/MISA, this is better than:

```text
tokens spent
number of loops
number of agent runs
```

because rejected outputs still require human review.

### Candidate Point 6: Build Order Matters More Than Tool Choice

The article gives a compact production order:

```text
one manual run reliable first
turn that into a skill
wrap the skill in a loop
then schedule it
```

This directly agrees with prior sources and should be preserved as an anti-failure route:

```text
do not schedule a fragile workflow
```

### Candidate Point 7: Light Self-Checking Loops Are Useful, But Weaker

The self-checking prompt is useful for ordinary users:

```text
goal
strict success criteria
PLAN / DO / VERIFY / DECIDE
score each criterion
fix weakest point
stop at threshold
```

VAKS boundary:

```text
model self-score = weak diagnostic
external test / independent verifier = stronger diagnostic
reviewed evidence = separate gate
```

### Candidate Point 8: Everyday Loops Are UX Inspiration, Not Evidence

The Mira section is useful as product/workflow inspiration:

```text
natural-language scheduled task
connected apps
background action
memory across sessions
Telegram interface
```

But all concrete claims require separate verification.

For VAKS, borrow only the UX shape:

```text
loop written as one plain-language instruction
trigger + action + delivery
user sees result, not infrastructure
```

## Comparison With Prior Loop Sources

| Dimension | Agent-Loop-Skills | loop-engineer-template | Movez/Kimi swarm | Hermes Sensei Loop | Anatoli Loops Explained |
|---|---|---|---|---|---|
| Source shape | Repo / skill library | Repo / template | Social post / swarm playbook | Social post / research-cron loop | Social post / broad explainer |
| Strongest value | Loop mechanics | Workspace and harness | Spec -> verify -> skill -> constraints | Holdout-gated prompt improvement | Boundary, cost, build order |
| Best VAKS use | Generic loop contract | Operator/workspace substrate | Swarm/background sequence | Research-output QA | Decide when not to loop |
| Main risk | Metrics as truth | Minimal model replacing VAKS layers | Product hype | Holdout score as action basis | Product claims and self-grading |

## Borrow / Avoid

Borrow as candidate design:

```text
verify/state/stop triad
four-condition loop-worth test
coding loop spec shape
automation/skill/subagent/connector/verifier checklist
cost per accepted change
manual -> skill -> loop -> schedule order
light self-checking loop prompt
everyday loop UX pattern
```

Avoid:

```text
product/platform claims as evidence
model self-grading as strong verification
looping non-repeated work
looping subjective taste tasks
scheduling before manual reliability
acceptance-rate blindness
Mira examples as confirmed capabilities
```

## Open Questions

- What is a VAKS-native minimum loop receipt for verify/state/stop?
- What is the minimum accept-rate threshold before a loop is worth keeping?
- How should "cost per accepted change" be tracked for source-intake or MISA loops?
- Which ordinary user loops should stay light and never enter heavy VAKS process?
- What productized UX should VAKS borrow without inheriting unverified platform claims?

## Not Promoted

This note does not promote the source to reviewed knowledge, evidence support, a VAKS decision, or action basis.

