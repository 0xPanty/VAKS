---
record_kind: sandbox_artifact_readout
slice_id: 2026-06-16-p2-55-user-decision-e2e-dry-run-simulator-sandbox
status: built_pending_review
---

# E2E Dry-Run Simulator Readout

| Scenario | Input | Expected Case | Expected Reply |
| --- | --- | --- | --- |
| `no_reply` | `` | `no_reply` | `keep_reference_no_action` |
| `explicit_a` | `A` | `explicit_A` | `acknowledge_reference_only` |
| `explicit_b` | `B` | `explicit_B` | `ask_readonly_planning_scope` |
| `explicit_c` | `C` | `explicit_C` | `ask_mainline_review_scope` |
| `explicit_d` | `D` | `explicit_D` | `acknowledge_park_or_reject` |
| `ambiguous_continue` | `继续` | `ambiguous_reply` | `ask_one_clarification` |
| `multiple_b_c` | `B 和 C 都行` | `multiple_options` | `ask_choose_one` |
| `execution_c_merge` | `C，合并主线` | `approval_with_execution_words` | `stop_for_separate_scope` |
| `safe_c_scope` | `选择C，问我主线评审范围` | `explicit_C` | `ask_mainline_review_scope` |
| `unknown_case` | `__synthetic_unknown_case__` | `unknown_case_fallback` | `stop_for_unknown_classifier_case` |

The simulator composes p2-53 and p2-54. It is dry-run only and cannot authorize
execution.
