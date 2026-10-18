---
record_kind: answer_draft_smoke_candidate
status: candidate
created_at: 2026-06-07T19:05:00+08:00
topic_id: source-intake-routing
truth_boundary: answer_draft_smoke_not_truth
action_basis_allowed: false
truth_mutation_allowed: false
source_skeleton_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/answer-draft-skeleton-v0-pack-repair-generated.md
expected_lint_result: pass
known_limitation: coverage_or_omission_not_checked_by_shape_lint
---

# Answer Draft Smoke v0: omitted claim known limitation

## Gate

```yaml
draft_smoke_state: adversarial_omitted_claim_known_limitation
draft_answer_emitted: true
source_refs_policy: claim_evidence_map_only
claims_used: ["pr1"]
action_basis_allowed: false
truth_mutation_allowed: false
expected_lint_result: pass
known_limitation: coverage_or_omission_not_checked_by_shape_lint
```

## Draft Answer

- [claim_refs: pr1] 这版草稿故意只使用 pr1，不覆盖 skeleton 中的 pr2 和 pr3。

## Expected Boundary

```text
This should pass as a known limitation.
Smoke lint does not require full claim coverage and does not perform omission checks.
Coverage / omission review belongs to a separate review or sufficiency layer.
```
