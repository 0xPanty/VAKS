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
known_limitation: semantic_mismatch_not_checked_by_shape_lint
---

# Answer Draft Smoke v0: mismatched ref known limitation

## Gate

```yaml
draft_smoke_state: adversarial_mismatched_ref_known_limitation
draft_answer_emitted: true
source_refs_policy: claim_evidence_map_only
claims_used: ["pr1"]
action_basis_allowed: false
truth_mutation_allowed: false
expected_lint_result: pass
known_limitation: semantic_mismatch_not_checked_by_shape_lint
```

## Draft Answer

- [claim_refs: pr1] 这句话故意说一个和 pr1 不同语义的结论，用来证明 smoke lint 只检查引用句柄存在，不检查语义支撑。

## Expected Boundary

```text
This should pass as a known limitation.
The claim_ref exists and the line is structurally tagged.
Semantic support / citation faithfulness belongs to evidence support, faithfulness, or human review layers, not this smoke lint.
```
