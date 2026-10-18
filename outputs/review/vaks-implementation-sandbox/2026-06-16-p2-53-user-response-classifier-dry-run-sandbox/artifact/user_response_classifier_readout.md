---
record_kind: sandbox_artifact_readout
slice_id: 2026-06-16-p2-53-user-response-classifier-dry-run-sandbox
status: built_pending_review
---

# User Response Classifier Dry-Run Readout

This artifact classifies future user replies to the p2-51 decision request. It
does not execute any option.

| Case | Result | Safe Next Step | Automatic Execution | New Scope | Separate Approval | Explicit Paths |
| --- | --- | --- | --- | --- | --- | --- |
| `no_reply` | `A_keep_sandbox_reference` | `no_action` | `False` | `False` | `False` | `False` |
| `explicit_A` | `A_keep_sandbox_reference` | `acknowledge_sandbox_reference_only` | `False` | `False` | `False` | `False` |
| `explicit_B` | `future_readonly_promotion_review_planning_request_only` | `ask_user_for_separate_read_only_review_planning_scope` | `False` | `True` | `True` | `False` |
| `explicit_C` | `future_mainline_merge_scope_question_only` | `ask_user_for_separate_allowed_paths_and_scope` | `False` | `True` | `True` | `True` |
| `explicit_D` | `park_or_reject_sandbox_chain` | `acknowledge_park_or_reject_status` | `False` | `False` | `False` | `False` |
| `ambiguous_reply` | `clarify_required` | `ask_one_short_clarification` | `False` | `False` | `False` | `False` |
| `multiple_options` | `clarify_required` | `ask_user_to_choose_one_option` | `False` | `False` | `False` | `False` |
| `approval_with_execution_words` | `stop_and_require_new_scope` | `stop_and_ask_for_separate_explicit_scope` | `False` | `True` | `True` | `True` |

## Coverage

- Positive fixtures: 14
- Failure cases: 42
- Upstream source: `2026-06-16-p2-52-user-decision-no-auto-advance-guard-sandbox`

## Usage

```powershell
python -B artifact\classify_user_response_dry_run.py --text "B"
```

`--rebuild` is Builder-only. Ordinary agents should run the verifier, not
rewrite the artifact.
