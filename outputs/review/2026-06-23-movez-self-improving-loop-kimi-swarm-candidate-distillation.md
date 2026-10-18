---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
source_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source.md
derived_from:
  - raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source.md
  - raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source/pasted-text.txt
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
  - self-improving-loop
  - swarm-loop
  - verify-gate
  - constraints-file
  - skill-capture
possible_project_refs:
  - verified-action-knowledge-system
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-spec-not-prompt.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-decomposition-before-execution.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-verify-gate-refuter.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-workflow-saved-as-skill.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-constraints-from-verifier-feedback.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-background-agent-after-stability.md
point_anchor_refs:
  - "pasted-text.txt:36-50"
  - "pasted-text.txt:53-65"
  - "pasted-text.txt:95-99"
  - "pasted-text.txt:101-114"
  - "pasted-text.txt:129-139"
  - "pasted-text.txt:153-164"
borrow_value: medium
borrow_order: P2_support
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "An approved task is specifically designing a bounded swarm/source-intake/operator loop with explicit verification and learning artifacts."
  support_when: "Prompt/spec design, decomposition-review gates, skill capture, constraints files, and background-loop trigger design."
  risk_when: "Model/product claims, pricing, benchmark numbers, background automation, or verifier output is being treated as evidence support, reviewed knowledge, or action basis."
  cold_references:
    - raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source.md
    - raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source/pasted-text.txt
avoid:
  - "Do not treat Kimi/Opus/pricing/benchmark/product-capability claims as verified."
  - "Do not treat a verifier's fix list as truth or action basis; it is review input."
  - "Do not promote background agents for ordinary VAKS intake without explicit user scope, stop conditions, and review gates."
  - "Do not let a constraints file mutate reviewed knowledge directly."
tags:
  - candidate
  - provisional
  - self-improving-loop
  - swarm-agents
  - verify-gate
---

# 候选蒸馏：Movez / The Self-Improving Loop

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 一句话结论

这篇文章有价值，但价值不在“Kimi/K2.6/Opus 4.8 的具体能力主张”。这些主张没有被验证。

真正可借的是一个自改进 loop 的操作形状：

```text
spec
-> inspect decomposition before execution
-> run parallel workers
-> demand real files
-> independent verify gate
-> save repeatable workflow as skill
-> turn verifier feedback into constraints
-> replay skill on new inputs
-> only then background-trigger
```

和前两条 Loop 源的关系：

```text
Agent-Loop-Skills:
  loop 怎么抽象成 skill / ledger / signal / stop

loop-engineer-template:
  loop 住在哪、怎么记账、怎么让 repo 可运行可验证

Movez/Kimi swarm post:
  一个更偏实操的 swarm-loop playbook，强调 spec、verify、skill、constraints、background trigger
```

## Source

```yaml
derived_from:
  - raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source.md
  - raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source/pasted-text.txt
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-spec-not-prompt.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-decomposition-before-execution.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-verify-gate-refuter.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-workflow-saved-as-skill.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-constraints-from-verifier-feedback.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-background-agent-after-stability.md
point_anchor_refs:
  - snapshot_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source/pasted-text.txt
    selector_type: line_range
    selector_value: pasted-text.txt:36-50
  - snapshot_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source/pasted-text.txt
    selector_type: line_range
    selector_value: pasted-text.txt:95-99
```

## Candidate Points

### Candidate Point 1: Spec Is The Seed Artifact

The article's strongest early move is to downgrade "prompt" and upgrade "spec".

The spec includes:

```text
goal
scope in/out
validation rules
allowed sources
output format
conflict handling
stop condition
```

For VAKS, this maps cleanly to:

```text
source-intake task contract
review-input generation contract
operator loop contract
MISA work-order contract
```

But the spec is still a task contract, not a truth source.

### Candidate Point 2: Decomposition Review Before Execution

The pre-run decomposition check is very valuable:

```text
agent count
subtask ownership
dependency order
step budget
largest quality-drop risk
wait for confirmation before execution
```

This can become a VAKS/MISA loop gate:

```text
no execution until the task decomposition is inspectable
no background loop until the budget and stop conditions are visible
```

### Candidate Point 3: Verify Gate Is A Refuter

The article's best safety framing:

```text
generation model does the volume work
verification model only refutes / catches silent flaws
```

Borrowable principle:

```text
verify gate should be designed to fail the output,
not to praise or summarize it.
```

VAKS boundary:

```text
verifier output = review input
verifier output != reviewed knowledge
verifier output != action basis
```

### Candidate Point 4: Self-Improvement Means Skill/Constraint Accumulation

The article explicitly says the model is not retraining between runs. The "learning" is in the system around it:

```text
workflow saved as Skill
documents captured as domain/style skills
verifier feedback converted into CONSTRAINTS.md
future runs apply skill + constraints
```

This is a useful phrasing for VAKS:

```text
self-improving loop = accumulated external artifacts,
not hidden model weight updates.
```

### Candidate Point 5: Background Agent Is Last, Not First

The final step is background triggering:

```text
schedule / file drop / monitored URL
execute saved skill
apply constraints
verify
deliver output + diff
only ping above threshold
```

This is attractive but risky. For VAKS, the order matters:

```text
manual run first
verified skill shape
constraints file
replay on new input
then limited background trigger
```

Do not invert that order.

## Borrow / Avoid

Borrow as candidate design:

```text
spec-first task contract
decomposition preview gate
real-file output contract
independent refutation gate
workflow-to-skill capture
verifier-feedback-to-constraints
replay with deviations-only report
background trigger only after stability
```

Avoid:

```text
Kimi product claims as evidence
Opus claims as evidence
pricing claims as current facts
benchmark claims as quality proof
background automation by default
skill capture without verify gate
constraints mutating reviewed truth
```

## Comparison With Prior Loop Sources

| Dimension | Agent-Loop-Skills | loop-engineer-template | Movez/Kimi swarm article |
|---|---|---|---|
| Source shape | Repository / skill library | Repository / project template | Social-post article / playbook |
| Strongest value | Loop contract and ledgers | Workspace substrate and code harness | Spec/decomposition/verify/skill/constraints sequence |
| Evidence strength | Inspectable repo | Inspectable repo | Pasted article, unverified claims |
| Borrow priority | P1 for loop mechanics | P1/P2 for operating substrate | P2 support, high-risk warning |
| Main risk | Metrics/judges mistaken for truth | Minimal signal/doc model replacing VAKS layers | Product hype and background automation mistaken for authority |

## Open Questions

- What parts of Kimi's reported swarm capability are actually available in the user's environment?
- What does Kimi mean by Skill in this context, and is it equivalent to Claude/Codex skills?
- How should a VAKS loop store verifier feedback without mutating reviewed truth?
- What minimal background-agent receipt would be required before any scheduled loop is allowed?

## Not Promoted

This note does not promote the source to reviewed knowledge, evidence support, a VAKS decision, or action basis.

