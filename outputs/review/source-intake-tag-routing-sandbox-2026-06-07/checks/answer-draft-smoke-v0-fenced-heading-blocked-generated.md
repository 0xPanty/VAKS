---
record_kind: answer_draft_smoke_candidate
status: candidate
created_at: 2026-06-07T19:20:00+08:00
topic_id: source-intake-routing
truth_boundary: answer_draft_smoke_not_truth
action_basis_allowed: false
truth_mutation_allowed: false
source_skeleton_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/answer-draft-skeleton-v0-e2e-mixed-blocked-generated.md
expected_lint_result: fail
expected_issue: blocked_draft_has_answer_text
---

# Answer Draft Smoke v0: fenced heading blocked

## Gate

```yaml
draft_smoke_state: adversarial_blocked_fenced_heading_then_answer
draft_answer_emitted: false
source_refs_policy: claim_evidence_map_only
claims_used: []
action_basis_allowed: false
truth_mutation_allowed: false
expected_lint_result: fail
expected_issue: blocked_draft_has_answer_text
```

## Draft Answer

```markdown
# This heading is inside a fenced diagnostic block
```

这行在围栏之后，是 blocked skeleton 下的实质答案文本，必须被检测出来。

## Expected Boundary

```text
This should fail.
Headings inside fenced blocks must not prematurely end Draft Answer scanning.
Substantive text after the fenced block must still be detected.
```
