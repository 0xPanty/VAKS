---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
source_ref: raw/articles/2026-06-23-0xjeff-hermes-sensei-loop-source.md
derived_from:
  - raw/articles/2026-06-23-0xjeff-hermes-sensei-loop-source.md
  - raw/articles/2026-06-23-0xjeff-hermes-sensei-loop-source/pasted-text.txt
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
  - research-agent-loop
  - champion-loop
  - holdout-promotion
  - feedback-sweep
  - research-crons
possible_project_refs:
  - verified-action-knowledge-system
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-research-cron-problem.md
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-champion-holdout-promotion.md
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-one-change-stop-rules.md
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-feedback-sweep.md
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-workflow-bootstrapping.md
point_anchor_refs:
  - "pasted-text.txt:9-17"
  - "pasted-text.txt:36-52"
  - "pasted-text.txt:60-68"
  - "pasted-text.txt:69-72"
borrow_value: strong
borrow_order: P1_support
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "An approved task is specifically designing feedback-driven research-agent loops, source-intake quality loops, or evaluation gates for recurring research outputs."
  support_when: "Research cron design, prompt optimization with holdouts, thesis stress testing, feedback backlog design, and recurring report quality control."
  risk_when: "Holdout scores, agent feedback, research crons, or buy/hold/sell outputs are being treated as reviewed knowledge, action basis, or investment advice."
  cold_references:
    - raw/articles/2026-06-23-0xjeff-hermes-sensei-loop-source.md
    - raw/articles/2026-06-23-0xjeff-hermes-sensei-loop-source/pasted-text.txt
avoid:
  - "Do not treat Hermes product behavior or Loop Library details as verified."
  - "Do not treat holdout scores as truth confidence or action basis."
  - "Do not let agent feedback replace human/evidence review for action-adjacent research."
  - "Do not promote buy/hold/sell or portfolio outputs without separate evidence/action gates."
tags:
  - candidate
  - provisional
  - hermes
  - champion-loop
  - research-agents
---

# 候选蒸馏：0xJeff / The Hermes Sensei Loop

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 一句话结论

这篇比上一篇 Movez/Kimi swarm 更接近 VAKS 可以立刻理解的质量控制问题：

```text
 recurring research output 会 stale
 prompt 改进容易靠 vibes
 AI 会过度顺从
 thesis 缺少 stress test
 cron 质量依赖人类零散反馈
```

它最值得借的不是 Hermes 产品本身，而是：

```text
Champion Loop:
  current prompt = champion
  one-failure fix = challenger
  working set = editable examples
  holdout set = untouched examples
  promote only if holdout beats champion by margin and must-pass rules still pass

Feedback Sweep:
  collect complaints
  group by workflow
  rank by repeated pain
  feed Champion Loop
```

## Source

```yaml
derived_from:
  - raw/articles/2026-06-23-0xjeff-hermes-sensei-loop-source.md
  - raw/articles/2026-06-23-0xjeff-hermes-sensei-loop-source/pasted-text.txt
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-research-cron-problem.md
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-champion-holdout-promotion.md
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-one-change-stop-rules.md
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-feedback-sweep.md
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-workflow-bootstrapping.md
point_anchor_refs:
  - snapshot_ref: raw/articles/2026-06-23-0xjeff-hermes-sensei-loop-source/pasted-text.txt
    selector_type: line_range
    selector_value: pasted-text.txt:9-17
  - snapshot_ref: raw/articles/2026-06-23-0xjeff-hermes-sensei-loop-source/pasted-text.txt
    selector_type: line_range
    selector_value: pasted-text.txt:36-52
```

## Candidate Points

### Candidate Point 1: Research Agents Need Adversarial Review, Not Just Helpfulness

The article starts from a real failure mode:

```text
research cron quality depends on model + tools + prompt + cron format
the agent improves only when the user keeps talking to it
AI may be too agreeable
no adversarial review
no thesis stress test
```

For VAKS, this maps to:

```text
candidate synthesis should be stress-tested
research cron should expose contradictions
helpfulness is not enough for review
```

### Candidate Point 2: Champion Loop Is Holdout-Gated Prompt Improvement

The strongest candidate mechanism:

```text
champion = current prompt
challenger = one targeted fix
working set = examples used for editing
holdout set = untouched examples
promote only if challenger beats champion on holdouts by margin
must-pass rules cannot break
```

This is better than ordinary prompt tweaking because it attacks:

```text
overfitting
silent regression
vibes-based prompt edits
```

### Candidate Point 3: One Change At A Time Preserves Attribution

The article's step sequence is small but important:

```text
freeze baseline
fix one recorded failure
test on working set
then test on holdout
stop when target reached / budget exhausted / no holdout improvement
```

For VAKS, this fits the loop discipline from `Agent-Loop-Skills`:

```text
one change
same gate
same metric/rubric
keep only if better
otherwise reject
log every round
```

### Candidate Point 4: Feedback Sweep Feeds The Champion Loop

Feedback Sweep is the intake mechanism:

```text
listen to complaints
organize by workflow
rank by repeated pain
hand a clean fix-list to the Champion Loop
```

This is useful for VAKS because feedback should not directly mutate truth. Instead:

```text
feedback
-> ranked improvement backlog
-> candidate prompt/workflow change
-> holdout gate
-> promotion only inside the loop artifact
```

### Candidate Point 5: Working/Holdout Sets Must Exist Before Automation

The article says the author is first gathering feedback, scores, and preferences before the Champion Loop can run.

That is the right order:

```text
collect examples
score/rubric them
split working vs holdout
then run loop
```

For VAKS:

```text
do not start a research-quality loop before the dataset, rubric, must-pass rules, and stop condition exist.
```

## Comparison With Prior Loop Sources

| Dimension | Agent-Loop-Skills | loop-engineer-template | Movez/Kimi swarm | Hermes Sensei Loop |
|---|---|---|---|---|
| Source shape | Repo / skill library | Repo / template | Social post / swarm playbook | Social post / research-cron loop |
| Strongest value | Loop contract and keep/revert | Workspace/harness substrate | Spec -> verify -> skill -> constraints | Holdout-gated prompt improvement |
| Best VAKS use | Generic loop mechanics | Loop workspace and code harness | Swarm/background-loop sequence | Research output QA and feedback backlog |
| Main risk | Metric/judge as truth | Minimal model replacing VAKS layers | Product hype/background automation | Holdout score or research output becoming action basis |

## Borrow / Avoid

Borrow as candidate design:

```text
adversarial thesis stress test for research crons
Champion/challenger prompt versioning
working/holdout split
defined margin + must-pass rules
one recorded failure per challenger
stop after no holdout improvement
Feedback Sweep as complaint-to-backlog converter
structured feedback before agent-feedback automation
```

Avoid:

```text
Hermes product claims as evidence
Loop Library claims as evidence
holdout score as truth confidence
research cron output as action basis
agent feedback replacing human/evidence review
buy/hold/sell outputs without evidence/action gates
```

## Open Questions

- What rubric defines "why it matters for you" in a way that is hard to game?
- What counts as ground-truth labels for research-cron outputs?
- How should VAKS store working and holdout sets without turning them into truth authority?
- How does Feedback Sweep integrate with VAKS Feedback Ledger without mutating reviewed knowledge?
- What guard is required before any research cron produces action-adjacent recommendations?

## Not Promoted

This note does not promote the source to reviewed knowledge, evidence support, a VAKS decision, or action basis.

