---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
review_pressure: none
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
project_id: verified-action-knowledge-system
target_ref: outputs/review/2026-06-23-movez-self-improving-loop-kimi-swarm-candidate-distillation.md
target_selector: "VAKS/MISA self-improving swarm-loop playbook sidecar"
target_hint: "spec-first loop / decomposition gate / verify refuter / skill capture / constraints learning / background trigger"
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-spec-not-prompt.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-decomposition-before-execution.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-verify-gate-refuter.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-workflow-saved-as-skill.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-constraints-from-verifier-feedback.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-background-agent-after-stability.md
project_borrow_scope: "For VAKS, borrow this article as a candidate loop-playbook reference: spec-first task contracts, pre-run decomposition preview, real-file output contracts, independent refutation-style verify gates, workflow-to-skill capture, verifier-feedback-to-constraints, replay with deviations-only reporting, and background triggering only after stability. This is most useful for future source-intake loops, operator cockpit loops, MISA work-order loops, and bounded research/update monitors."
project_non_borrow_scope: "For project VAKS, do not currently borrow this article as evidence that Kimi, Opus, K2.6, pricing, benchmark, 300-agent, 4,000-step, or product-capability claims are true. Do not borrow background agents as ordinary intake defaults, verifier output as reviewed knowledge, Skill capture as promotion, or CONSTRAINTS.md as a mechanism for mutating truth-layer files. Reopen only if official product docs, reproducible local tests, and a VAKS guard/receipt design support a bounded loop pilot."
project_reopen_trigger: "Reopen when VAKS designs a real swarm/source-intake/background monitor pilot; require official source checks, explicit user trigger, budget/stop condition, retained receipts, verification outputs stored as review input, and action_basis_allowed=false boundaries."
confirmation_basis: "User explicitly requested distillation of this article/post; overlay is limited to project borrow/non-borrow boundaries and does not imply adoption."
last_checked_at: 2026-06-23
expires_at:
tags:
  - self-improving-loop
  - swarm-agents
  - verify-gate
  - constraints-file
---

# Project Overlay: Movez/Kimi Self-Improving Loop For VAKS

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide future VAKS/MISA loop design, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-23-movez-self-improving-loop-kimi-swarm-candidate-distillation.md
target_selector: VAKS/MISA self-improving swarm-loop playbook sidecar
target_hint: spec-first loop / decomposition gate / verify refuter / skill capture / constraints learning / background trigger
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-spec-not-prompt.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-decomposition-before-execution.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-verify-gate-refuter.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-workflow-saved-as-skill.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-constraints-from-verifier-feedback.md
  - outputs/review/source_annotations/2026-06-23-movez-self-improving-loop-kimi-swarm/movez-background-agent-after-stability.md
```

## Project Borrow Scope

For VAKS, borrow the playbook shape:

```text
1. Write a spec, not a prompt.
2. Inspect decomposition before execution.
3. Let workers parallelize only inside explicit scope.
4. Demand structured files, not chat answers.
5. Use an independent verifier as a refuter.
6. Save repeatable workflow as a skill.
7. Capture domain/style documents as reusable references.
8. Convert verifier feedback into constraints.
9. Replay the saved skill on new inputs.
10. Background-trigger only after stability and with thresholds.
```

Best candidate use inside VAKS/MISA:

```text
source-intake loop
research/update monitor
operator cockpit loop
MISA work-order loop
competitive/market watch
candidate-review input generator
```

## Project Non-Borrow Scope

For project VAKS, do not currently borrow:

```text
Kimi product claims as evidence
Opus product claims as evidence
pricing claims as current facts
benchmark claims as quality proof
social-post claims as source support
background agents as default intake behavior
verifier output as reviewed knowledge
Skill capture as promotion
CONSTRAINTS.md as truth mutation mechanism
```

Reason:

```text
This source is a pasted social-post/article.
It is useful as a playbook orientation.
It is not official docs, a reproducible benchmark, or a local pilot receipt.
```

## Reopen Trigger

Reopen this boundary when:

```text
VAKS designs a real swarm/source-intake/background monitor pilot
and official source checks exist
and the user explicitly approves the trigger
and budget/stop conditions are visible
and receipts are retained
and verification output is stored as review input
and action_basis_allowed=false remains explicit
```

## Recommended Use Shape

```yaml
self_improving_loop_run:
  record_kind: loop_run
  knowledge_status: candidate
  source_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source.md
  spec_ref:
  decomposition_plan_ref:
  output_contract_ref:
  verify_gate_ref:
  verifier_findings_ref:
  skill_ref:
  constraints_ref:
  replay_inputs_ref:
  background_trigger_ref:
  result_status: diagnostic_only
  retrieval_policy:
    policy_kind: orientation_only
    pack_allowed: review_input_only
    action_basis_allowed: false
    warning_code: loop_signal_not_support
  truth_mutation_allowed: false
  action_basis_allowed: false
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
loop-output-as-evidence
verifier-as-reviewer
constraints-as-truth-mutation
background-agent-without-explicit-scope
```

