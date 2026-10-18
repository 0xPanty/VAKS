---
record_kind: answer_draft_smoke_candidate
status: candidate
created_at: 2026-06-07T19:05:00+08:00
topic_id: source-intake-routing
truth_boundary: answer_draft_smoke_not_truth
action_basis_allowed: false
truth_mutation_allowed: false
source_skeleton_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/answer-draft-skeleton-v0-e2e-mixed-blocked-generated.md
expected_lint_result: fail
expected_issue: blocked_draft_has_answer_text
---

# Answer Draft Smoke v0: paragraph blocked

## Gate

```yaml
draft_smoke_state: adversarial_blocked_paragraph_answer
draft_answer_emitted: false
source_refs_policy: claim_evidence_map_only
claims_used: []
action_basis_allowed: false
truth_mutation_allowed: false
expected_lint_result: fail
expected_issue: blocked_draft_has_answer_text
```

## Draft Answer

这里虽然没有 bullet，也没有 claim_refs，但它仍然是在 blocked skeleton 下发出的实质回答文本。

## Expected Boundary

```text
This should fail as a shape problem.
Blocked skeletons must not emit substantive Draft Answer text outside fenced diagnostic blocks.
```
