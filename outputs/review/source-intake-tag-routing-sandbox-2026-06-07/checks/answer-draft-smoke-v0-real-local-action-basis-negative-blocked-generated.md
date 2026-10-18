---
record_kind: answer_draft_smoke_candidate
status: candidate
created_at: 2026-06-07T19:30:00+08:00
topic_id: source-intake-routing
truth_boundary: answer_draft_smoke_not_truth
action_basis_allowed: false
truth_mutation_allowed: false
source_skeleton_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/answer-draft-skeleton-v0-real-local-action-basis-negative-blocked-generated.md
---

# Answer Draft Smoke v0: real local action-basis negative blocked

## Gate

```yaml
draft_smoke_state: blocked_not_ready_real_local
draft_answer_emitted: false
source_refs_policy: claim_evidence_map_only
claims_used: []
action_basis_allowed: false
truth_mutation_allowed: false
block_reasons:
  - input_answer_readiness_not_ready_for_answer_draft
  - claim_evidence_map_contains_non_supported_claim
forbidden_use: ["truth", "reviewed_relation", "action_basis", "agent_action"]
```

## Draft Answer

```text
blocked: real-local negative sample is not ready_for_human_draft
draft_answer_emitted: false
draft_answer_lines: 0
```

## Boundary Banner

```text
The negative real-local sample overclaims action basis, reviewer approval, semantic proof, and coverage review.
The blocked path must emit no answer text.
```
