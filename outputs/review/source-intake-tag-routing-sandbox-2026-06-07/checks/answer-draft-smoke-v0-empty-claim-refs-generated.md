---
record_kind: answer_draft_smoke_candidate
status: candidate
created_at: 2026-06-07T19:05:00+08:00
topic_id: source-intake-routing
truth_boundary: answer_draft_smoke_not_truth
action_basis_allowed: false
truth_mutation_allowed: false
source_skeleton_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/answer-draft-skeleton-v0-pack-repair-generated.md
expected_lint_result: fail
expected_issue: ready_draft_has_empty_claim_refs
---

# Answer Draft Smoke v0: empty claim refs

## Gate

```yaml
draft_smoke_state: adversarial_empty_claim_refs
draft_answer_emitted: true
source_refs_policy: claim_evidence_map_only
claims_used: []
action_basis_allowed: false
truth_mutation_allowed: false
expected_lint_result: fail
expected_issue: ready_draft_has_empty_claim_refs
```

## Draft Answer

- [claim_refs:] 这句看起来带了 claim_refs 标签，但实际上没有绑定任何 claim_id。

## Expected Boundary

```text
This should fail as a shape problem.
The smoke lint must not treat an empty claim_refs tag as a real claim handle.
```
