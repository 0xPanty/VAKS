---
record_kind: answer_draft_skeleton_candidate
status: candidate
created_at: 2026-06-07T19:33:48+08:00
topic_id: source-intake-routing
truth_boundary: answer_draft_skeleton_not_truth
action_basis_allowed: false
truth_mutation_allowed: false
source_answer_ready_pack_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/answer-ready-context-pack-v0-real-local-smoke-boundary-generated.md
---

# Answer Draft Skeleton v0: source-intake-routing

## Gate

```yaml
source_answer_ready_pack_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/answer-ready-context-pack-v0-real-local-smoke-boundary-generated.md"
source_pack_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/real-local-question-pack-smoke-boundary-generated.md"
evidence_support_check_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/evidence-support-check-v0-real-local-smoke-boundary-generated.md"
input_answer_readiness: ready_for_answer_draft
draft_skeleton_state: ready_for_human_draft
claims_seen: 5
draft_claims_emitted: 5
source_refs_policy: claim_evidence_map_only
action_basis_allowed: false
truth_mutation_allowed: false
final_support:
  state: checked_for_draft
  scope: answer_draft_only
  not_action_basis: true
  input_final_support_answer_only: true
forbidden_use: ["truth", "reviewed_relation", "action_basis", "agent_action"]
block_reasons: []
```

## Draft Spine

- claim_id: rl1
  answer_sentence: "Smoke lint assumes the skeleton readiness label is correct and leaves readiness correctness to the upstream evidence support check."
  support_status: supported
  required_support_channels: []
  support_channels: ["explicit_fixture_ref"]
  source_refs: ["outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/answer-draft-smoke-v0-test.md", "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/README.md"]
  selectors: ["line:30", "line:498"]
  warrant: "The smoke test and README explicitly state the readiness trust boundary."
- claim_id: rl2
  answer_sentence: "Smoke lint checks shape compliance and reference-handle existence."
  support_status: supported
  required_support_channels: []
  support_channels: ["explicit_fixture_ref"]
  source_refs: ["outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/answer-draft-smoke-v0-test.md"]
  selectors: ["line:32"]
  warrant: "The local smoke test describes the actual lint guarantee."
- claim_id: rl3
  answer_sentence: "Semantic support, citation faithfulness, coverage, and omissions remain outside the smoke lint layer."
  support_status: supported
  required_support_channels: []
  support_channels: ["explicit_fixture_ref"]
  source_refs: ["outputs/review/source-intake-tag-routing-sandbox-2026-06-07/21_EVIDENCE_SUPPORT_CHECK_V0_LANDING.md"]
  selectors: ["line:379"]
  warrant: "The local test, landing note, and review brief all state the non-goals."
- claim_id: rl4
  answer_sentence: "Mismatched-ref and omitted-claim cases are expected-pass known limitations."
  support_status: supported
  required_support_channels: []
  support_channels: ["explicit_fixture_ref"]
  source_refs: ["outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/answer-draft-smoke-v0-test.md", "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/22_ANSWER_DRAFT_SMOKE_V0_OPUS_REVIEW_BRIEF.md", "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/README.md"]
  selectors: ["line:179", "line:90", "line:480"]
  warrant: "The known-limitation cases are documented as expected-pass tests."
- claim_id: rl5
  answer_sentence: "Empty claim refs, paragraph-style blocked answers, and fenced-heading blocked answers are expected-fail shape adversaries."
  support_status: supported
  required_support_channels: []
  support_channels: ["explicit_fixture_ref"]
  source_refs: ["outputs/review/source-intake-tag-routing-sandbox-2026-06-07/22_ANSWER_DRAFT_SMOKE_V0_OPUS_REVIEW_BRIEF.md", "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/README.md"]
  selectors: ["line:87", "line:479"]
  warrant: "The shape adversaries are documented as expected-fail tests."

## Guardrails

```text
This skeleton is only a drafting aid.
It must not introduce claims outside claim_evidence_map.
It must not convert answer readiness into action basis.
Human review is still required before action-facing use.
```
