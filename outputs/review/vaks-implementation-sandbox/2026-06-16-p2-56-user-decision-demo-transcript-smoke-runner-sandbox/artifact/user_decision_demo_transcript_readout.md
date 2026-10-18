---
record_kind: sandbox_artifact_readout
slice_id: 2026-06-16-p2-56-user-decision-demo-transcript-smoke-runner-sandbox
status: built_pending_review
---

# Demo Transcript Smoke Runner Readout

| Scenario | Input | Expected Case | Expected Reply |
| --- | --- | --- | --- |
| `no_reply` | `(empty)` | `no_reply` | `keep_reference_no_action` |
| `option_a` | `A` | `explicit_A` | `acknowledge_reference_only` |
| `option_b` | `B` | `explicit_B` | `ask_readonly_planning_scope` |
| `option_c` | `C` | `explicit_C` | `ask_mainline_review_scope` |
| `option_d` | `D` | `explicit_D` | `acknowledge_park_or_reject` |
| `ambiguous` | `继续` | `ambiguous_reply` | `ask_one_clarification` |
| `multiple` | `B 和 C 都行` | `multiple_options` | `ask_choose_one` |
| `execution_words` | `C，合并主线` | `approval_with_execution_words` | `stop_for_separate_scope` |
| `unknown_fallback` | `__synthetic_unknown_case__` | `synthetic_unknown_case` | `stop_for_unknown_classifier_case` |

Run:

```powershell
python -B artifact\run_user_decision_demo_transcript.py
```
