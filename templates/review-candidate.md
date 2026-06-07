---
record_type: review-candidate
status: pending
knowledge_status: candidate
processing_tier: medium
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
created:
updated:
point_id:
candidate_id:
source_candidate_points: []
point_text:
normalized_point:
point_type: claim | interpretation | hypothesis | pattern | risk | preference | decision | open_question | implementation_note
verifiability:
  state: verifiable | partially_verifiable | not_verifiable | unknown
  reason:
review_route: evidence_check | rationale_check | instance_check | risk_check | action_basis_check | personalization_only | research_question | code_anchor_check
why_checkworthy:
evidence_granularity: metadata_only | abstract_or_summary | excerpt_or_passage | table_or_code_anchor | full_source_reviewed
source_refs:
  - source_id:
    source_url_or_path:
    source_range:
    quote_or_excerpt:
extracted_by:
extracted_at:
uncertainty:
possible_related_points: []
review_status: pending
promotion_target:
proposed_title:
proposed_path:
review_object_state: draft | fixed_for_review | revised_after_review | archived
candidate_body_location: "# Candidate Body"
body_hash:
body_hash_algorithm: sha256_utf8_lf_trim_body_without_heading
evidence_packet_ref:
source_anchor_refs: []
scope_limits: []
risk_flags: []
known_counterevidence: []
missing_evidence: []
approval_integrity:
  approved_by:
  approval_source:
  approved_at:
  llm_assisted: true | false
  checked_specific_evidence: true | false
  checked_body_hash:
archive_reason:
tags:
  - review-candidate
---

# Review Candidate

## Point


## Self-Contained Review Object

Use this block when the candidate is being prepared for promotion, formal
writeback, strong reviewed relation, action basis, or explicit reviewer audit.
Leave it blank for ordinary light capture.

Canonical self-contained review object fields live in top-level frontmatter.
Do not create a second nested schema block here.

Required when `review_object_state` is `fixed_for_review` or later:

- `candidate_id`
- `promotion_target`
- `proposed_title`
- `proposed_path`
- `candidate_body_location`
- `body_hash`
- `body_hash_algorithm`
- `evidence_packet_ref`
- `source_anchor_refs`
- `scope_limits`
- `risk_flags`

Rules:

```text
The self-contained review object is not reviewed knowledge.
It fixes the body being reviewed so approval and writeback refer to the same artifact.
Keep the candidate body in a Markdown section or referenced file, not inside frontmatter/YAML.
If the candidate body changes after review, body_hash changes and review must run again.
Canonical body hash rule: hash the content pointed to by `candidate_body_location`, excluding the heading, normalizing CRLF to LF, trimming leading/trailing whitespace, encoded as UTF-8 SHA256.
Do not use this block as a substitute for Evidence Packet support.
Do not count a source summary, this candidate, or a prior chat as the independent support anchor.
```

## Candidate Body

Use this section only when `review_object_state` is `fixed_for_review` or later.
This is the exact body proposed for writeback.

## Review Queue Routing

Use this only when the candidate needs explicit queue attention.
Ordinary candidates can leave it blank and rely on `point_type`, `verifiability`, and `review_route`.

```yaml
review_queue_item:
  item_type:
  triggered_by:
  suggested_action:
  status:
```

- Item type:
- Why this needs review:
- Suggested action:
- Target refs:
- Resolution note:

## Source Trace

Keep the frontmatter `source_refs` light by default.
Use this block only when a point needs source-span anchoring, confidence cap review, promotion support, a strong reviewed relation, action basis, or explicit audit.

```yaml
source_anchor:
  url_or_path:
  exact_quote:
  prefix:
  suffix:
  captured_at:
  position:
  content_hash:
  archived_url:
  checked_latest_at:
  source_changed: unknown | yes | no

source_access:
  access_level: full_text | source_span | abstract_only | snippet_only | url_only | summary_only | unknown
  has_direct_quote: true | false
  has_source_range: true | false
  confidence_cap: low | medium | high
  cap_reason:
```


## Evidence Packet

Use this only when the candidate may be promoted, used for action, used for a strong reviewed relation, explicitly challenged, high-impact, stale, contested, or reviewer-requested.

```yaml
evidence_packet:
  point:
  evidence_items:
    - source_anchor:
      evidence_granularity: metadata_only | abstract_or_summary | excerpt_or_passage | table_or_code_anchor | full_source_reviewed
      rationale:
      evidence_support:
        span_supports_target: supported | partial | unsupported | unclear
        evidence_role: direct_support | inferential_support | background_context | counterexample
        reviewer_note:
  grounds:
  warrant:
  qualifier:
  strongest_rebuttal:
  challenge_kind: rebuttal | undercut | scope_limit | source_hygiene | stale_assumption | action_failure
  risk_flags:
  omission_check:
    missing_risks:
    missing_scope_limits:
    possible_omissions:
    omission_questions:
    needs_full_source_read:
  review_question:
  minimal_revision_needed: keep | refine_scope | mark_contested | mark_stale | supersede | reject
```

Rules:

```text
Evidence Packet is review input, not a truth layer.
grounds says what evidence is available.
warrant says why the evidence supports or weakens the point.
challenge_kind names the challenge; it does not automatically reject the point.
minimal_revision_needed is a recommendation for review, not an automatic edit.
omission_check is for heavy source digests, important repos, long papers, high-impact decisions, or reviewer request.
```

## Confidence Cap / Source Access

- Access level: full_text / source_span / abstract_only / snippet_only / url_only / summary_only / unknown
- Has source range:
- Has direct quote:
- Confidence cap:
- Cap reason:

Rule:

```text
No source span / full anchor means no high confidence.
URL-only and summary-only are provenance, not support.
```

## Evidence Support Check

Required only when this source_ref is used as support for promotion, strong relation review, or action basis.

```yaml
evidence_support:
  span_supports_target: supported | partial | unsupported | unclear
  evidence_role: direct_support | inferential_support | background_context | counterexample
  reviewer_note:

independent_anchor_check:
  anchor_type: raw_source | source_snapshot | source_summary | reviewed_source_review | transcript_segment | code_anchor | quote_selector | other
  claim_note_only: true | false
  self_support_loop: true | false
  result: pass | weak | missing_anchor | self_support_loop | scope_limited | not_ready
  reviewer_note:
```

Rules:

```text
URL-only source_refs are provenance, not support.
background_context cannot count as support.
inferential_support needs reviewer_note before it can count as promotion support.
counterexample should move into challenge_refs or risk_refs.
The reviewed or review-ready claim can be a trace handle, but it cannot be the only support for itself.
Direct support requires an independent evidence/source anchor.
If support is secondary, partial, missing, circular, or narrower than the candidate says, mark weak / missing_anchor / self_support_loop / scope_limited / not_ready instead of upgrading confidence.
```

## Optional Review Result / Qualification

Use this only after review or when preparing promotion/action basis.

```yaml
review_result:
  knowledge_state: standing | limited | contested | stale | superseded | rejected | not_enough_evidence
  strongest_challenge:
  scope_limit:
  minimal_revision_needed:
  review_due_when:

qualification:
  applies_when:
  does_not_apply_when:
  version_scope:
  project_scope:
  domain_scope:
  time_scope:
  environment_scope:
  assumptions:

attack_assessment:
  severity:
  reason:
  affected_scope:
  requires_review_due:
```

## Optional Temporal Applicability / Action Readiness

Use this only when the candidate is part of a context pack, action basis, decision, strong reviewed relation, or risk-sensitive answer.

```yaml
temporal_applicability:
  valid_from:
  valid_until:
  supersedes:
  superseded_by:
  invalidated_by:
  applies_to:
    project:
    version:
    environment:
    timeframe:
    conditions:
  check_state:
  reviewer_note:

action_readiness:
  state:
  reason:
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
- Challenge kind: rebuttal / undercut / scope_limit / source_hygiene / stale_assumption / action_failure
- Challenge severity: fatal / major / minor / out_of_scope / unresolved
- Scope limits:
- Temporal applicability: valid_from / valid_until / superseded_by / applies_to
- Known risks:
- Review again when:
- Minimal revision needed: keep / refine_scope / mark_contested / mark_stale / supersede / reject
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
