---
record_type: query-run
status: archived
created:
updated:
query_id:
session_id:
turn_id:
parent_query_id:
question_summary:
verbatim_input:
model_interpretation:
query_intent: answer | decision | implementation | research | content | memory
query_scope:
  project:
  domain:
  version:
  time_range:
scope_key:
inferred_keywords: []
seed_points: []
expansion_depth:
activated_points: []
activated_relations: []
activated_routes: []
included_sources: []
excluded_candidates: []
retrieval_mode:
authority_bucket:
rrf_scope: same_authority_bucket_only
overlay_suggestions:
  - target_ref:
    project_ref:
    overlay_state: suggested
    persistent_overlay_allowed: false
    default_retrieval_allowed: false
    action_basis_allowed: false
    warning_code: overlay_unconfirmed
answer_path: []
warnings: []
gaps: []
support_boundary:
  supported_not_truth: true
  answer_ready_not_action_ready: true
  claim_refs_are_trace_handles: true
  independent_anchor_required: true
  self_support_loop_check:
  support_result: supported | weak | missing_anchor | self_support_loop | scope_limited | not_ready
feedback_summary:
  positive_feedback:
  negative_feedback:
  explicit_correction:
  review_pressure:
  review_due_created:
decision_outcome:
  decision_ref:
  recommendation:
  confidence_at_decision:
  user_choice:
  outcome:
intent_confirmation:
  required:
  user_confirmed:
tags:
  - query-run
  - feedback
---

# Query Run

## What Was Asked

- Verbatim input:
- Model interpretation:

## What Was Activated


## What Was Used


## What Was Excluded


## Warnings / Gaps


## Support Boundary

Use this section when the query answer, decision, review note, or action-adjacent
response depends on a claim as support.

```text
claim_refs are trace handles, not proof.
supported does not mean truth.
answer-ready does not mean action-ready.
test / lint / blind review does not mean reviewer approval.
```

Record whether support came from an independent evidence/source anchor:

```yaml
support_checks:
  - claim_ref:
    answer_line:
    independent_anchor:
      anchor_type: raw_source | source_snapshot | source_summary | reviewed_source_review | code_anchor | transcript_segment | quote_selector | other
      url_or_path:
      selector:
      evidence_granularity: metadata_only | abstract_or_summary | excerpt_or_passage | table_or_code_anchor | full_source_reviewed
    claim_note_only: false
    result: supported | weak | missing_anchor | self_support_loop | scope_limited | not_ready
    reviewer_note:
```

If the only support is the claim note restating itself, mark:

```text
self_support_loop
```

If evidence supports a narrower conclusion than the answer draft says, mark:

```text
scope_limited
```

Weak, missing-anchor, self-support, and scope-limited results can still be useful
for orientation, but they cannot be treated as reviewed truth or action basis.

## Follow-Up Signal


## Feedback Boundary

```text
Positive feedback is weak.
Negative feedback creates review pressure.
Explicit correction creates review_due.
Decision outcome improves future recommendation, not truth.
```
