---
record_type: candidate-point
status: pending
created:
updated:
point_id:
point_text:
normalized_point:
point_type: claim | interpretation | hypothesis | pattern | risk | preference | decision | open_question | implementation_note
verifiability:
  state: verifiable | partially_verifiable | not_verifiable | unknown
  reason:
review_route: evidence_check | rationale_check | instance_check | risk_check | action_basis_check | personalization_only | research_question | code_anchor_check
topics: []
entities: []
scope:
  domain:
  project:
  version:
  time_range:
  conditions:
source_refs:
  - source_id:
    source_url_or_path:
    source_range:
    quote_or_excerpt:
    evidence_support:
      span_supports_target:
      evidence_role:
      reviewer_note:
extracted_by:
extracted_at:
uncertainty:
possible_related_points: []
collision_signals: []
review_status: pending
review_state: candidate
knowledge_state:
attack_assessment:
  severity:
  reason:
  affected_scope:
  requires_review_due:
qualification:
  applies_when:
  does_not_apply_when:
  version_scope:
  project_scope:
  domain_scope:
  time_scope:
  environment_scope:
  assumptions:
review_summary:
  why_it_still_holds:
  strongest_challenge:
  scope_limits:
  known_risks:
  review_due_when:
action_readiness:
  state:
  reason:
reviewed_by:
reviewed_at:
promotion_target:
tags:
  - review-candidate
---

# Candidate Point

## Point


## Source Trace


## Evidence Support Check

Required only when this source_ref is used as support for promotion, strong relation review, or action basis.

```yaml
evidence_support:
  span_supports_target: supported | partial | unsupported | unclear
  evidence_role: direct_support | inferential_support | background_context | counterexample
  reviewer_note:
```

Rules:

```text
URL-only source_refs are provenance, not support.
background_context cannot count as support.
inferential_support needs reviewer_note before it can count as promotion support.
counterexample should move into challenge_refs or risk_refs.
```

## Why It Matters


## Uncertainty


## Verifiability Routing

```text
Candidate point = atomic review unit, not necessarily atomic claim.

Default routes:
claim -> evidence_check
interpretation -> rationale_check
hypothesis -> research_question
pattern -> instance_check
risk -> risk_check
preference -> personalization_only
decision -> action_basis_check
open_question -> research_question
implementation_note -> code_anchor_check
```

Only verifiable claims can receive truth / evidence confidence.

Optional route-specific fields:

```yaml
evidence_check:
  evidence:
  verification_status:
  evidence_confidence:

rationale_check:
  rationale:
  source_basis:
  scope_limits:

instance_check:
  instances:
  counterexamples:
  scope_limits:

risk_check:
  failure_modes:
  triggers:
  risk_evidence_level:

action_basis_check:
  preconditions:
  risks:
  rollback:
  success_metric:

personalization_only:
  personalization_scope:
  usefulness:

research_question:
  why_it_matters:
  needed_evidence:
  research_value:

code_anchor_check:
  repo:
  file:
  commit:
  line_range:
  version_scope:
```

## Optional Point Graph Fragment

Use only when the candidate is complex, high-impact, cross-document, multi-hop, action-relevant, ambiguous, or reviewer-requested.

```yaml
point_graph_fragment:
  purpose: collision_check | evidence_review | scope_clarification | action_basis | ambiguity_resolution
  entities:
    - id:
      label:
      type:
      aliases: []
      resolution:
        status: resolved | unresolved | ambiguous
        note:
  relation_triplets:
    - subject:
      predicate:
      object:
      qualifier:
      scope:
      source_anchor:
      note:
  open_questions:
    - question:
      blocks_review: true | false
```

Rules:

```text
This fragment is a review aid, not a reviewed relation.
Triplet extraction is not truth.
Triplet similarity is not support.
Triplet conflict is not automatic rejection.
If this needs more than 3-5 essential triplets, split the candidate point.
```

## Possible Collisions

```yaml
collision_signals:
  - signal_id:
    target_point:
    relation: supports | contradicts | refines | risk_of | derived_from | duplicates | near_miss | unrelated
    source_independence: independent | same-origin | derived | unknown
    rationale:
    review_status: pending
```

## Review Notes


## Support / Challenge Review

For ordinary candidates, keep this lightweight: one uncertainty / risk note is enough.
Expand this full panel only for promotion, action basis, strong reviewed relation, explicit contradiction, stale / contested review, or reviewer request.

- What supports it:
- What challenges it:
- Challenge severity: fatal / major / minor / out_of_scope / unresolved
- Scope limits:
- Known risks:
- Review again when:
- Action readiness: ready / not_ready / risky / needs_review

## Promotion Notes

Use this only when promoting this candidate, creating a strong reviewed relation, or using it in an action basis.

```yaml
evidence_sufficiency:
  state: sufficient | weak | insufficient | out_of_scope | risky
  checked_for: promotion | reviewed_relation | action_basis | decision | risk_sensitive_answer
  missing: []
  required_next_step: proceed | ask_user | retrieve_more | create_missing_point | narrow_scope | mark_not_actionable | needs_review
  reviewer_note:
```

Rules:

```text
insufficient or out_of_scope cannot be promoted as ready support.
weak must carry gaps.
risky must set action_readiness to risky or needs_review.
```
