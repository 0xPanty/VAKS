---
schema: urn:vaks:schema:fragment-candidate:v1
record_kind: fragment_candidate
fragment_id:
created_at:
created_by: user
knowledge_status: candidate
candidate_class: fragment_only
processing_tier: light
fragment:
  kind: idea | claim_like | quote_like | question | pattern_hint | risk_hint | task_hint | term
  language: zh | en | unknown
  content_digest:
  quote_exactness: not_applicable | unverified
  literal_quote_allowed: false
provenance:
  status: self_authored | memory_trace | source_hint_only | source_unknown
  source_hint:
    hint_text:
    possible_title:
    possible_author:
    possible_url:
    possible_platform:
    possible_timeframe:
    hint_confidence: none | low | medium
  source_recovery:
    status: not_attempted | needed | failed | found
    recovered_source_ref:
    attempts: []
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: missing_source_provenance
usage_policy:
  pack_content_allowed: false
  pack_pointer_allowed: true
  action_basis_allowed: false
  evidence_support_allowed: false
  reviewed_knowledge_allowed: false
state:
  fragment_state: inbox | source_recovery_needed | parked | merged | discarded
  merged_into:
  discarded_reason:
tags:
  - fragment
  - source-missing
---

# Fragment Candidate: <short title>

## Fragment

Keep the raw fragment here. Preserve the wording, but do not present it as a
literal quote unless a source is recovered.

## Why It Might Matter


## Source Recovery Hints

- possible source:
- remembered context:
- search terms:
- related projects:

## Boundaries

- Not a Source Card.
- Not a Source Capture.
- Not a Source Annotation.
- Not evidence support.
- Not reviewed knowledge.
- Not action basis.
- Pack builders may use a pointer to this note for activation only.

## Next Step

source_recovery_needed | merge_into_candidate | park | discard
