---
record_kind: evidence_support_check_candidate
status: candidate
created_at: 2026-06-07T19:33:41+08:00
topic_id: source-intake-routing
truth_boundary: support_check_review_input_not_truth
action_basis_allowed: false
truth_mutation_allowed: false
context_pack_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/real-local-question-pack-smoke-boundary-generated.md
claim_spec_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/evidence-support-check-v0-real-local-smoke-boundary.json
---

# Evidence Support Check v0: source-intake-routing

## Query

```yaml
query: "real local sample: what does answer draft smoke lint guarantee, and what does it not guarantee"
context_pack_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/real-local-question-pack-smoke-boundary-generated.md"
claim_spec_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/evidence-support-check-v0-real-local-smoke-boundary.json"
anchor_queue_total: 0
truth_boundary: support_check_review_input_not_truth
action_basis_allowed: false
citation_faithfulness_checked: false
```

## Answer Candidate

- Smoke lint assumes the skeleton readiness label is correct and leaves readiness correctness to the upstream evidence support check.
- Smoke lint checks shape compliance and reference-handle existence.
- Semantic support, citation faithfulness, coverage, and omissions remain outside the smoke lint layer.
- Mismatched-ref and omitted-claim cases are expected-pass known limitations.
- Empty claim refs, paragraph-style blocked answers, and fenced-heading blocked answers are expected-fail shape adversaries.

## Claim Support Map

```yaml
claims:
  - claim_id: rl1
    claim_text: "Smoke lint assumes the skeleton readiness label is correct and leaves readiness correctness to the upstream evidence support check."
    grounding_check_required: true
    support_status: supported
    support_kind: source_span_support
    required_support_channels: []
    citation_correctness_checked: true
    citation_faithfulness_checked: false
    warrant: "The smoke test and README explicitly state the readiness trust boundary."
    failure_origin: []
    supporting_anchors:
      - source_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/answer-draft-smoke-v0-test.md"
        selector_or_offset: "line:30"
        snippet: "smoke lint assumes the skeleton readiness label is correct"
        support_channel: "explicit_fixture_ref"
        matched_pattern: "smoke lint assumes the skeleton readiness label is correct"
      - source_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/README.md"
        selector_or_offset: "line:498"
        snippet: "smoke lint assumes skeleton readiness is correct upstream; it checks shape and"
        support_channel: "explicit_fixture_ref"
        matched_pattern: "smoke lint assumes skeleton readiness is correct upstream"
  - claim_id: rl2
    claim_text: "Smoke lint checks shape compliance and reference-handle existence."
    grounding_check_required: true
    support_status: supported
    support_kind: source_span_support
    required_support_channels: []
    citation_correctness_checked: true
    citation_faithfulness_checked: false
    warrant: "The local smoke test describes the actual lint guarantee."
    failure_origin: []
    supporting_anchors:
      - source_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/answer-draft-smoke-v0-test.md"
        selector_or_offset: "line:32"
        snippet: "smoke lint checks shape compliance and reference-handle existence"
        support_channel: "explicit_fixture_ref"
        matched_pattern: "smoke lint checks shape compliance and reference-handle existence"
  - claim_id: rl3
    claim_text: "Semantic support, citation faithfulness, coverage, and omissions remain outside the smoke lint layer."
    grounding_check_required: true
    support_status: supported
    support_kind: source_span_support
    required_support_channels: []
    citation_correctness_checked: true
    citation_faithfulness_checked: false
    warrant: "The local test, landing note, and review brief all state the non-goals."
    failure_origin: []
    supporting_anchors:
      - source_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/21_EVIDENCE_SUPPORT_CHECK_V0_LANDING.md"
        selector_or_offset: "line:379"
        snippet: "faithfulness, coverage, and omissions remain outside this layer."
        support_channel: "explicit_fixture_ref"
        matched_pattern: "faithfulness, coverage, and omissions remain outside this layer"
  - claim_id: rl4
    claim_text: "Mismatched-ref and omitted-claim cases are expected-pass known limitations."
    grounding_check_required: true
    support_status: supported
    support_kind: source_span_support
    required_support_channels: []
    citation_correctness_checked: true
    citation_faithfulness_checked: false
    warrant: "The known-limitation cases are documented as expected-pass tests."
    failure_origin: []
    supporting_anchors:
      - source_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/answer-draft-smoke-v0-test.md"
        selector_or_offset: "line:179"
        snippet: "known-limitation cases: 2 expected pass"
        support_channel: "explicit_fixture_ref"
        matched_pattern: "known-limitation cases: 2 expected pass"
      - source_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/22_ANSWER_DRAFT_SMOKE_V0_OPUS_REVIEW_BRIEF.md"
        selector_or_offset: "line:90"
        snippet: "mismatched ref known limitation: expected pass / actual pass"
        support_channel: "explicit_fixture_ref"
        matched_pattern: "mismatched ref known limitation: expected pass / actual pass"
      - source_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/README.md"
        selector_or_offset: "line:480"
        snippet: "mismatched ref: expected pass known limitation"
        support_channel: "explicit_fixture_ref"
        matched_pattern: "mismatched ref: expected pass known limitation"
  - claim_id: rl5
    claim_text: "Empty claim refs, paragraph-style blocked answers, and fenced-heading blocked answers are expected-fail shape adversaries."
    grounding_check_required: true
    support_status: supported
    support_kind: source_span_support
    required_support_channels: []
    citation_correctness_checked: true
    citation_faithfulness_checked: false
    warrant: "The shape adversaries are documented as expected-fail tests."
    failure_origin: []
    supporting_anchors:
      - source_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/22_ANSWER_DRAFT_SMOKE_V0_OPUS_REVIEW_BRIEF.md"
        selector_or_offset: "line:87"
        snippet: "empty claim_refs adversary: expected fail / actual fail"
        support_channel: "explicit_fixture_ref"
        matched_pattern: "empty claim_refs adversary: expected fail / actual fail"
      - source_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/README.md"
        selector_or_offset: "line:479"
        snippet: "fenced heading blocked answer: expected fail / actual fail"
        support_channel: "explicit_fixture_ref"
        matched_pattern: "fenced heading blocked answer: expected fail / actual fail"
```

## Coverage Overview

```yaml
coverage_overview:
  supported: 5
  weakly_supported: 0
  unsupported: 0
  missing_evidence: 0
  not_checked: 0
  known_omissions: []
  support_channels: ["explicit_fixture_ref"]
answer_readiness:
  state: ready_for_answer_draft
  reason: "All grounding-required claims have at least source-span support in this sandbox check."
final_support:
  state: checked
  scope: answer_draft_only
  not_action_basis: true
warnings:
  - citation_faithfulness_not_checked
  - scores_are_diagnostic_only
  - answer_ready_is_not_action_basis
```
