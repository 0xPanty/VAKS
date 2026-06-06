---
type: sandbox_pressure_test_results
status: candidate_only
created_at: 2026-06-06
scope: Source Intake Control Flow sandbox pressure test
truth_boundary: diagnostic only; not reviewed knowledge; not mainline policy
---

# Source Intake Control Flow Sandbox Pressure Test Results

## Test Summary

First run result: 10/11 passed.

Final rerun result: 11/11 passed.

The failed check was useful: the medium candidate fixture used `retrieval_policy: orientation_only`, but did not mechanically state that action-basis use is blocked. That meant the design intent was readable to a human, but not hard enough for retrieval or agent policy.

Patch applied:

- Changed candidate `retrieval_policy` from a plain string to a small machine-readable policy block.
- Added `action_basis_allowed: false`.
- Added `pack_allowed: activation_only`.
- Added `warning_code: candidate_not_action_basis`.

## Final Checks

| Check | Expected | Status |
| --- | --- | --- |
| Sandbox package has expected files. | 15 or more files | PASS |
| Candidate has `knowledge_status: candidate`. | true | PASS |
| Candidate has no project borrow fields. | true | PASS |
| Candidate blocks direct action-basis use. | true | PASS |
| Suggested overlay is trace-only. | true | PASS |
| Confirmed overlay has project scope. | true | PASS |
| Confirmed overlay avoids decision/reviewed status. | true | PASS |
| Feedback event forbids truth mutation fields. | true | PASS |
| Blocked heavy review is excluded from answer pool. | true | PASS |
| RRF does not cross authority buckets. | true | PASS |
| Overlay storage split is present. | true | PASS |

## Interpretation

This pressure test supports the Pro recommendation: the improved Source Intake Control Flow is not mainly about adding a new source type. Its real upgrade is making runtime boundaries executable:

- processing strength is not authority;
- candidate is not action basis;
- suggested overlay is not persistent overlay;
- confirmed overlay is still project-scoped;
- feedback does not mutate truth;
- retrieval fuses relevance only inside an allowed bucket.

## Final Rerun Output

```text
file_count_15                             True file_count=15
candidate_status_candidate                True candidate has candidate status
candidate_no_project_borrow_fields        True candidate keeps routing_hint only
candidate_action_basis_false              True candidate cannot action basis
suggested_overlay_trace_only              True suggested overlay blocked from persistence/default retrieval
confirmed_overlay_has_project_scope       True confirmed overlay has project-scoped non-borrow and reopen trigger
confirmed_overlay_no_decision_status      True confirmed overlay not decision/reviewed
feedback_append_only_no_truth_delta       True feedback forbids truth mutation fields
heavy_review_open_blocked_not_answer_pool True blocked heavy review excluded
rrf_no_cross_authority_fusion             True RRF boundary present
overlay_storage_split_present             True overlay split present
```
