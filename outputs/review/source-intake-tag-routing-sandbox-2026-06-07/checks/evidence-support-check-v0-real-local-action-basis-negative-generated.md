---
record_kind: evidence_support_check_candidate
status: candidate
created_at: 2026-06-07T19:33:45+08:00
topic_id: source-intake-routing
truth_boundary: support_check_review_input_not_truth
action_basis_allowed: false
truth_mutation_allowed: false
context_pack_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/real-local-question-pack-action-basis-generated.md
claim_spec_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/evidence-support-check-v0-real-local-action-basis-negative.json
---

# Evidence Support Check v0: source-intake-routing

## Query

```yaml
query: "real local negative sample: overclaim smoke lint as action basis or semantic proof"
context_pack_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/real-local-question-pack-action-basis-generated.md"
claim_spec_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/evidence-support-check-v0-real-local-action-basis-negative.json"
anchor_queue_total: 29
truth_boundary: support_check_review_input_not_truth
action_basis_allowed: false
citation_faithfulness_checked: false
```

## Answer Candidate

- The answer draft smoke output can be used as action basis.
- Smoke lint is reviewer approval.
- Existing claim_refs prove semantic support.
- Smoke lint performs coverage and omission review.

## Claim Support Map

```yaml
claims:
  - claim_id: rn1
    claim_text: "The answer draft smoke output can be used as action basis."
    grounding_check_required: true
    support_status: missing_evidence
    support_kind: source_span_support
    required_support_channels: []
    citation_correctness_checked: false
    citation_faithfulness_checked: false
    warrant: "This should fail because the local docs say answer-draft smoke is not action basis."
    failure_origin: ["scope_mismatch_or_overclaim"]
    supporting_anchors:
      - none
  - claim_id: rn2
    claim_text: "Smoke lint is reviewer approval."
    grounding_check_required: true
    support_status: missing_evidence
    support_kind: source_span_support
    required_support_channels: []
    citation_correctness_checked: false
    citation_faithfulness_checked: false
    warrant: "This should fail because the local brief labels smoke lint as diagnostic, not approval."
    failure_origin: ["scope_mismatch_or_overclaim"]
    supporting_anchors:
      - none
  - claim_id: rn3
    claim_text: "Existing claim_refs prove semantic support."
    grounding_check_required: true
    support_status: missing_evidence
    support_kind: source_span_support
    required_support_channels: []
    citation_correctness_checked: false
    citation_faithfulness_checked: false
    warrant: "This should fail because the local docs say claim_refs are handles, not semantic proof."
    failure_origin: ["semantic_faithfulness_not_checked"]
    supporting_anchors:
      - none
  - claim_id: rn4
    claim_text: "Smoke lint performs coverage and omission review."
    grounding_check_required: true
    support_status: missing_evidence
    support_kind: source_span_support
    required_support_channels: []
    citation_correctness_checked: false
    citation_faithfulness_checked: false
    warrant: "This should fail because coverage and omission are explicitly outside smoke lint."
    failure_origin: ["coverage_or_omission_not_checked"]
    supporting_anchors:
      - none
```

## Coverage Overview

```yaml
coverage_overview:
  supported: 0
  weakly_supported: 0
  unsupported: 0
  missing_evidence: 4
  not_checked: 0
  known_omissions: []
  support_channels: []
answer_readiness:
  state: not_ready
  reason: "One or more grounding-required claims lack required source-span support or only have weak support."
final_support:
  state: checked
  scope: answer_draft_only
  not_action_basis: true
warnings:
  - citation_faithfulness_not_checked
  - scores_are_diagnostic_only
  - answer_ready_is_not_action_basis
```
