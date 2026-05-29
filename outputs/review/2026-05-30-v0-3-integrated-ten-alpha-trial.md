---
type: integrated-trial
status: completed
created: 2026-05-30
project: verified-action-knowledge-system
scope:
  - v0-3
  - ten-alpha
  - local-material-trial
tags:
  - evidence-discipline
  - pro-review
  - local-validation
---

# v0.3 Integrated Ten-Alpha Trial

## Trial Goal

Run the 10 v0.3 alpha points together on one local architecture case, instead of validating them one by one in isolation.

Question:

```text
Can the system absorb a useful design idea from RKA source code while keeping truth authority thin, review-gated, and auditable?
```

## Inputs

Local / exact-commit material:

```text
raw/repos/2026-05-29-rka-source.md
outputs/review/2026-05-30-rka-source-code-anchor-review.md
outputs/review/2026-05-30-rka-evidence-packet-source-record-trial.md
SCHEMA.md
REVIEW_QUEUE.md
FEEDBACK.md
templates/review-candidate.md
templates/dev-context-pack.md
templates/feedback-event.md
```

External exact source anchors used through the local review:

```text
https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/decision_options.py#L234-L280
https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/api/routes/decisions.py#L227-L243
https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/decisions.py#L217-L333
https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/models/review_queue.py#L10-L36
```

No RKA runtime was executed.

## Candidate Points

```yaml
candidate_points:
  - id: cp-rka-outcome-precondition
    point_text: Final decision_outcome should not be recorded unless the recommendation and the user choice, or explicit user override, are recorded.
    point_type: implementation_note
    verifiability:
      state: verifiable
      reason: Exact RKA code anchors show selection / override preconditions around outcome recording.
    review_route: code_anchor_check
    intended_use: use_ledger_schema_hardening

  - id: cp-rka-review-queue-routing
    point_text: Review queue items should route attention and workflow resolution; they should not directly mutate truth.
    point_type: interpretation
    verifiability:
      state: partially_verifiable
      reason: RKA code anchors verify routing mechanics; the vault truth-boundary interpretation is a local architecture judgment.
    review_route: rationale_check
    intended_use: review_queue_boundary

  - id: cp-rka-superseding-review-pressure
    point_text: Decision superseding should preserve old decisions, link the replacement, and create review pressure for affected downstream material.
    point_type: interpretation
    verifiability:
      state: partially_verifiable
      reason: RKA code anchors support superseding mechanics; downstream review pressure is local architecture adaptation.
    review_route: code_anchor_check
    intended_use: decision_superseding_boundary

  - id: cp-rka-runtime-rejection
    point_text: RKA runtime, MCP, dashboard, and SQLite storage should not be adopted as this vault's truth architecture.
    point_type: risk
    verifiability:
      state: partially_verifiable
      reason: The existence of RKA runtime surfaces is source-checkable; rejecting them is a fit/risk judgment for this Markdown vault.
    review_route: risk_check
    intended_use: scope_guardrail
```

## Evidence Packet

```yaml
evidence_packet:
  point: cp-rka-outcome-precondition
  point_type: implementation_note
  evidence_items:
    - source_anchor:
        url_or_path: https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/decision_options.py#L234-L280
        exact_quote: "At least one of ``selected_option_id`` or ``override_rationale`` must be set."
        prefix: "Persist the PI's selection"
        suffix: "UPDATE decisions SET pi_selected_option_id"
        captured_at: 2026-05-30
        position: rka/services/decision_options.py#L234-L280
        content_hash: not_computed
        source_changed: unknown
      evidence_granularity: table_or_code_anchor
      rationale: RKA records PI selection separately and rejects empty selection / override.
      evidence_support:
        span_supports_target: supported
        evidence_role: direct_support
        reviewer_note: This code anchor directly supports the narrower precondition that selection or override must exist before the selected option record is meaningful.
    - source_anchor:
        url_or_path: https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/api/routes/decisions.py#L227-L243
        exact_quote: "cannot record outcome"
        prefix: "Outcomes only make sense for decisions the PI has resolved"
        suffix: "pi_selected_option_id nor pi_override_rationale"
        captured_at: 2026-05-30
        position: rka/api/routes/decisions.py#L227-L243
        content_hash: not_computed
        source_changed: unknown
      evidence_granularity: table_or_code_anchor
      rationale: RKA refuses outcome recording when no PI selection or override exists.
      evidence_support:
        span_supports_target: supported
        evidence_role: direct_support
        reviewer_note: This code anchor directly supports the outcome-recording guard; the vault adopts the narrower calibration precondition, not the whole RKA workflow.
  grounds: RKA source code contains explicit checks for selected option / override before outcome recording.
  warrant: If an outcome is recorded without knowing what the user actually selected or overrode, the outcome cannot calibrate the recommendation. It would mix recommendation quality with execution divergence.
  qualifier: Applies to decision_outcome and action-basis recommendation outcome, not to ordinary feedback notes.
  strongest_rebuttal: RKA is a runtime research assistant, not this Markdown vault; direct schema copying could overfit to its PI workflow.
  challenge_kind: scope_limit
  risk_flags:
    - overfit_to_rka_runtime
    - outcome_as_truth_mutation
  omission_check:
    missing_risks:
      - No runtime test was run against RKA.
      - No large outcome dataset exists in this vault.
    missing_scope_limits:
      - Applies only to final outcome calibration, not quick feedback.
    possible_omissions:
      - RKA also tracks override_rate / escape_hatch_rate / near_miss_rate, but these are future metrics, not current schema requirements.
    omission_questions:
      - Are there other outcome paths in RKA not covered by the two selected anchors?
    needs_full_source_read: false
  review_question: Should this precondition be added to decision_outcome in SCHEMA, FEEDBACK, FUSION, and feedback-event template?
  minimal_revision_needed: refine_scope
  review_due_when:
    - action_failure
    - missed_feedback
```

Review result:

```yaml
review_result:
  knowledge_state: standing
  strongest_challenge: RKA runtime workflow is not identical to this vault.
  scope_limit: Only final decision_outcome needs the precondition; ordinary feedback can remain lightweight.
  minimal_revision_needed: refine_scope
  action_taken:
    - added outcome_precondition to SCHEMA.md
    - added outcome_precondition to FEEDBACK.md
    - added outcome_precondition to FUSION_ARCHITECTURE_V0_2_DRAFT.md
    - added outcome_precondition to templates/feedback-event.md
  truth_boundary: This changes Use Ledger discipline, not truth confidence.
```

## Evidence Support Negative Tests

These checks were added after Pro review because the first integrated trial had source anchors and rationale but did not directly exercise `evidence_support`.

```yaml
negative_evidence_support_tests:
  url_only_source_ref:
    source_ref: https://github.com/infinitywings/rka
    attempted_use: promotion_support
    evidence_support:
      span_supports_target: unclear
      evidence_role: background_context
      reviewer_note:
    result: blocked
    reason: URL-only source refs are provenance, not evidence support.

  background_context_item:
    source_anchor:
      url_or_path: raw/repos/2026-05-29-rka-source.md
      exact_quote: "source identity confirmed"
      captured_at: 2026-05-29
    attempted_use: support_for_outcome_precondition
    evidence_support:
      span_supports_target: partial
      evidence_role: background_context
      reviewer_note: This confirms source identity, not the outcome-precondition logic.
    result: blocked_as_support
    reason: background_context can stay in the packet, but cannot count as supported.

  inferential_support_without_reviewer_note:
    source_anchor:
      url_or_path: https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/decisions.py#L217-L333
      exact_quote: "outcome"
      captured_at: 2026-05-30
    attempted_use: promotion_support
    evidence_support:
      span_supports_target: partial
      evidence_role: inferential_support
      reviewer_note:
    result: blocked
    reason: inferential_support without reviewer_note cannot count as promotion support.
```

## Challenge Taxonomy Exercise

```yaml
challenge_taxonomy_cases:
  rebuttal:
    case: A source directly says outcome can be recorded without user choice.
    result_in_trial: not_found
    action: no rebuttal pressure

  undercut:
    case: RKA's PI-selection workflow may not generalize to all vault actions.
    result_in_trial: present
    action: narrow rule to final decision_outcome / action-basis outcome

  scope_limit:
    case: The rule is too heavy for ordinary answer_helpful feedback.
    result_in_trial: present
    action: keep ordinary feedback light

  source_hygiene:
    case: Source record alone lacked exact code anchors.
    result_in_trial: present_and_resolved
    action: escalated to exact commit source-code anchors

  stale_assumption:
    case: RKA repository may change after checked commit.
    result_in_trial: possible_future
    action: if relying on latest RKA behavior, recheck latest commit

  action_failure:
    case: Future outcome review finds failures were recorded without user_choice.
    result_in_trial: simulated_trigger
    action: create review_due and maintenance-manifest item
```

Pass condition:

```text
Every challenge kind can be represented without automatic truth mutation.
```

Result:

```text
PASS
```

## Minimal Revision Exercise

```yaml
minimal_revision_cases:
  keep:
    point: review queue is routing metadata
    reason: code supports queue status / priority / resolution as workflow fields

  refine_scope:
    point: decision_outcome needs precondition
    reason: applies only to final outcome, not all feedback

  mark_contested:
    point: context ranking should be imported
    reason: ranking is useful but not accepted as trust signal

  mark_stale:
    point: source-record-only RKA code proof
    reason: superseded by exact code anchor review

  supersede:
    point: "RKA source record alone is enough for code-level proof"
    reason: replaced by code-anchor review conclusion

  reject:
    point: adopt RKA runtime / MCP / dashboard as core vault architecture
    reason: conflicts with Markdown source-of-truth and thin Truth Core
```

Pass condition:

```text
All six minimal revision outcomes are meaningful and non-destructive.
```

Result:

```text
PASS
```

## Evidence Granularity Escalation

```yaml
granularity_escalation:
  metadata_only:
    allowed_use: source identity only
    blocked_use: code-level proof

  abstract_or_summary:
    allowed_use: conceptual candidate
    blocked_use: high-confidence implementation claim

  excerpt_or_passage:
    allowed_use: support for textual claim if warrant is clear
    blocked_use: broad architecture adoption without scope limit

  table_or_code_anchor:
    allowed_use: code-level support for a narrow design claim
    blocked_use: adopting runtime without runtime review

  full_source_reviewed:
    allowed_use: stronger source review
    blocked_use: automatic truth or automatic action readiness
```

Trial path:

```text
RKA source record started at abstract_or_summary / source-record level.
Code review escalated relevant claims to table_or_code_anchor.
Runtime adoption stayed blocked because no runtime review was needed or authorized.
```

Result:

```text
PASS
```

## Omission Check

```yaml
omission_check:
  missing_risks:
    - RKA runtime behavior was not tested.
    - RKA metrics need enough outcome data; this vault has no such dataset yet.
    - RKA context ranking could be mistaken for trust if copied carelessly.
  missing_scope_limits:
    - Outcome precondition applies to final decision_outcome, not every feedback event.
    - Review queue taxonomy should stay optional.
    - Code anchors support narrow points, not the whole RKA system.
  possible_omissions:
    - RKA has more runtime features than this vault should absorb.
    - RKA knowledge pack has critical/warning import integrity logic; this remains future watch, not current core.
  omission_questions:
    - Are there additional RKA outcome paths not covered by the selected code anchors?
  needs_full_source_read: false
```

Result:

```text
PASS
```

## Context Pack Trace

```yaml
context_pack_trace:
  used_sources:
    - outputs/review/2026-05-30-rka-source-code-anchor-review.md
    - raw/repos/2026-05-29-rka-source.md
    - SCHEMA.md
    - FEEDBACK.md
    - REVIEW_QUEUE.md
  ignored_sources:
    - RKA dashboard code
    - RKA MCP server runtime surface
    - RKA React/UI details
    - RKA worker/job runtime
  ignored_reason:
    RKA runtime is outside current v0.3 scope; the useful layer is review discipline, not platform adoption.
  activation_role:
    outputs/review/2026-05-30-rka-source-code-anchor-review.md: core
    raw/repos/2026-05-29-rka-source.md: support
    SCHEMA.md: core
    FEEDBACK.md: core
    REVIEW_QUEUE.md: core
  unresolved_contradictions:
    - none for the narrow outcome precondition
  risk_flags:
    - runtime_over_adoption
    - ranking_as_trust
    - feedback_as_truth
```

Result:

```text
PASS
```

## Agent Memory Quarantine Simulation

Input:

```yaml
agent_memory_write:
  source: future_agent_runtime
  proposed_write: "RKA-style decision outcome succeeded, raise confidence on related claim."
```

Expected routing:

```yaml
agent_memory_write:
  status: candidate_only
  allowed_effect:
    - activation
    - usefulness
    - scope_fit
    - review_due
  forbidden_effect:
    - truth_confidence
    - reviewed_relation
    - promotion
```

Decision:

```text
Reject direct confidence mutation.
Allow a feedback_event / review_due candidate.
```

Result:

```text
PASS
```

## Review Due Trigger Simulation

```yaml
review_due_cases:
  new_primary_source:
    trigger: RKA changes outcome API in a later commit.
    action: recheck code anchor and mark affected adoption note review_due.

  contradiction:
    trigger: another source argues outcomes can be recorded without user choice.
    action: create contradiction_candidate.

  correction_or_retraction:
    trigger: user says the outcome rule was misread.
    action: explicit correction creates review_due.

  source_version_change:
    trigger: RKA release changes decision_options model.
    action: source_changed yes; review_due.

  dependency_release_change:
    trigger: future implementation depends on RKA-like package version.
    action: dependency_release_change review_due.

  action_failure:
    trigger: a recorded outcome cannot be interpreted because user_choice is missing.
    action: mark outcome record incomplete and create review_due.

  missed_feedback:
    trigger: feedback said recommendation was ignored but ledger treated it as success.
    action: review_due for feedback event and action basis.

  stale_assumption:
    trigger: assumption that RKA outcome discipline maps to this vault no longer holds.
    action: refine_scope or mark_stale.
```

Result:

```text
PASS
```

## Final Integrated Judgment

```text
The 10 alpha points work together.

The useful RKA idea was absorbed narrowly.
The runtime was rejected.
The code anchors raised evidence granularity.
The warrant explained why the code mattered.
Challenges narrowed scope.
Minimal revision prevented over-editing.
Omission check recorded what was not reviewed.
Context trace explained used vs ignored material.
Agent memory quarantine blocked truth mutation.
Review_due triggers remain pressure, not invalidation.
```

This is the intended v0.3 behavior.
