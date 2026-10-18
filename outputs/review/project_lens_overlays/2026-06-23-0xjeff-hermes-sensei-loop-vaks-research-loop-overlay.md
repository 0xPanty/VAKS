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
target_ref: outputs/review/2026-06-23-0xjeff-hermes-sensei-loop-candidate-distillation.md
target_selector: "VAKS/MISA research-agent loop and feedback-to-holdout improvement sidecar"
target_hint: "research cron QA / champion loop / holdout promotion / feedback sweep / thesis stress test"
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-research-cron-problem.md
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-champion-holdout-promotion.md
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-one-change-stop-rules.md
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-feedback-sweep.md
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-workflow-bootstrapping.md
project_borrow_scope: "For VAKS, borrow this article as a candidate research-loop quality-control reference: adversarial thesis stress testing for recurring research outputs, champion/challenger prompt versioning, working/holdout split, defined promotion margins, must-pass rules, one-failure-at-a-time prompt edits, stop conditions, and Feedback Sweep as complaint-to-improvement-backlog. This is most relevant for future source-intake summaries, research crons, MISA alpha triage, and recurring project reports."
project_non_borrow_scope: "For project VAKS, do not currently borrow Hermes product behavior, Loop Library details, author workflow outcomes, investment examples, holdout scores, or buy/hold/sell outputs as verified facts, reviewed knowledge, or action basis. Do not let agent feedback replace human/evidence review, and do not let holdout pass results mutate truth-layer files. Reopen only if a bounded local pilot defines datasets, labels, rubric, must-pass rules, receipts, and action_basis_allowed=false boundaries."
project_reopen_trigger: "Reopen when VAKS designs a real recurring research-output quality loop or Feedback Sweep pilot; require source-visible working/holdout sets, scoring rubric, must-pass rules, stop conditions, scoped feedback ledger, and evidence/action separation before mainline adoption."
confirmation_basis: "User explicitly requested distillation of this article/post; overlay is limited to project borrow/non-borrow boundaries and does not imply adoption."
last_checked_at: 2026-06-23
expires_at:
tags:
  - hermes
  - champion-loop
  - feedback-sweep
  - research-crons
---

# Project Overlay: Hermes Sensei Loop For VAKS Research Loops

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide future VAKS/MISA research-loop design, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-23-0xjeff-hermes-sensei-loop-candidate-distillation.md
target_selector: VAKS/MISA research-agent loop and feedback-to-holdout improvement sidecar
target_hint: research cron QA / champion loop / holdout promotion / feedback sweep / thesis stress test
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-research-cron-problem.md
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-champion-holdout-promotion.md
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-one-change-stop-rules.md
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-feedback-sweep.md
  - outputs/review/source_annotations/2026-06-23-0xjeff-hermes-sensei-loop/hermes-workflow-bootstrapping.md
```

## Project Borrow Scope

For VAKS, borrow this source as a candidate design for:

```text
recurring research-output quality control
source-intake summary improvement
MISA alpha triage prompt evaluation
research-cron thesis stress testing
feedback-to-improvement backlog
```

Borrow the loop contract:

```text
champion prompt
-> one recorded failure
-> challenger prompt
-> working-set check
-> holdout check
-> defined margin + must-pass rules
-> keep/reject
-> logged round
-> stop on target/budget/no-improvement
```

Borrow the feedback route:

```text
complaint / correction / preference
-> organize by workflow
-> rank by recurrence
-> feed Champion Loop
-> do not mutate truth directly
```

## Project Non-Borrow Scope

For project VAKS, do not currently borrow:

```text
Hermes product claims as verified
Loop Library details as verified
portfolio/research output examples as action basis
buy/hold/sell recommendations as reusable truth
holdout pass as truth confidence
agent feedback as replacement for evidence review
```

Reason:

```text
This source is a pasted social-post/article.
It provides a strong candidate loop shape.
It does not provide the actual datasets, scoring rubric, ground-truth labels, holdout examples, implementation receipts, or independently checked outcomes.
```

## Reopen Trigger

Reopen this boundary when:

```text
VAKS designs a real recurring research-output quality loop
or a Feedback Sweep pilot
and source-visible working/holdout sets exist
and a scoring rubric exists
and must-pass rules exist
and stop conditions exist
and feedback is scoped through Feedback Ledger
and action_basis_allowed=false remains explicit
```

## Recommended Use Shape

```yaml
research_loop_prompt_eval:
  record_kind: loop_run
  knowledge_status: candidate
  source_ref: raw/articles/2026-06-23-0xjeff-hermes-sensei-loop-source.md
  workflow_id:
  champion_prompt_ref:
  challenger_prompt_ref:
  failure_ref:
  working_set_ref:
  holdout_set_ref:
  rubric_ref:
  must_pass_rules_ref:
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
holdout-score-as-truth
research-cron-as-investment-advice
feedback-as-truth-mutation
agent-feedback-without-human/evidence-gate
```

