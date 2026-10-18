---
record_kind: evidence_support_check_candidate
status: candidate
created_at: 2026-06-07T19:36:58+08:00
topic_id: source-intake-routing
truth_boundary: support_check_review_input_not_truth
action_basis_allowed: false
truth_mutation_allowed: false
context_pack_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/source-intake-routing-workbench-pack-query-action-generated.md
claim_spec_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/evidence-support-check-v0-negative-source-intake.json
---

# Evidence Support Check v0: source-intake-routing

## Query

```yaml
query: "pressure test unsupported and scope-mismatched answer claims"
context_pack_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/source-intake-routing-workbench-pack-query-action-generated.md"
claim_spec_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/evidence-support-check-v0-negative-source-intake.json"
anchor_queue_total: 29
truth_boundary: support_check_review_input_not_truth
action_basis_allowed: false
citation_faithfulness_checked: false
```

## Answer Candidate

- The current source-intake-routing sandbox can be used as action basis.
- Selector and snippet fields are evidence support.
- The evidence-support-check v0 is a production RAG grounding evaluator.
- The source-intake-routing sandbox has been promoted into the main truth layer.

## Claim Support Map

```yaml
claims:
  - claim_id: n1
    claim_text: "The current source-intake-routing sandbox can be used as action basis."
    grounding_check_required: true
    support_status: missing_evidence
    support_kind: source_span_support
    required_support_channels: []
    citation_correctness_checked: false
    citation_faithfulness_checked: false
    warrant: "This should fail because the sandbox repeatedly says it is not action basis."
    failure_origin: ["retrieval_gap_or_pattern_miss"]
    supporting_anchors:
      - none
  - claim_id: n2
    claim_text: "Selector and snippet fields are evidence support."
    grounding_check_required: true
    support_status: missing_evidence
    support_kind: source_span_support
    required_support_channels: []
    citation_correctness_checked: false
    citation_faithfulness_checked: false
    warrant: "This should fail because selector/snippet are navigation-only."
    failure_origin: ["retrieval_gap_or_pattern_miss"]
    supporting_anchors:
      - none
  - claim_id: n3
    claim_text: "The evidence-support-check v0 is a production RAG grounding evaluator."
    grounding_check_required: true
    support_status: missing_evidence
    support_kind: source_span_support
    required_support_channels: []
    citation_correctness_checked: false
    citation_faithfulness_checked: false
    warrant: "This should fail as a positive claim because these phrases appear only as non-goals or negations."
    failure_origin: ["retrieval_gap_or_pattern_miss"]
    supporting_anchors:
      - none
  - claim_id: n4
    claim_text: "The source-intake-routing sandbox has been promoted into the main truth layer."
    grounding_check_required: true
    support_status: missing_evidence
    support_kind: source_span_support
    required_support_channels: []
    citation_correctness_checked: false
    citation_faithfulness_checked: false
    warrant: "This should fail because the package remains candidate-only and sandbox-only."
    failure_origin: ["retrieval_gap_or_pattern_miss"]
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
