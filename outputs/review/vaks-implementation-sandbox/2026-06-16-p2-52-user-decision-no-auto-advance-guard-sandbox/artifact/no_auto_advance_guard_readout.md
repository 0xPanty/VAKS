---
record_kind: sandbox_artifact_readout
slice_id: 2026-06-16-p2-52-user-decision-no-auto-advance-guard-sandbox
status: built_pending_review
---

# No-Auto-Advance Guard Readout

This artifact guards the p2-51 decision request packet from being mistaken for
execution authority.

## Response Policy

| Case | Result | Action | Automatic Execution | New Scope | Separate Approval | Allowed Next Message |
| --- | --- | --- | --- | --- | --- | --- |
| `no_reply` | `A_keep_sandbox_reference` | `no_action` | `False` | `False` | `False` | `wait_for_user_or_report_sandbox_status` |
| `explicit_A` | `A_keep_sandbox_reference` | `no_action` | `False` | `False` | `False` | `acknowledge_sandbox_reference_only` |
| `explicit_B` | `future_readonly_promotion_review_planning_request_only` | `ask_for_separate_read_only_planning_scope_before_any_future_slice` | `False` | `True` | `True` | `ask_user_for_separate_read_only_review_planning_scope` |
| `explicit_C` | `future_mainline_merge_scope_question_only` | `ask_for_separate_mainline_review_scope` | `False` | `True` | `True` | `ask_user_for_separate_allowed_paths_and_scope` |
| `explicit_D` | `park_or_reject_sandbox_chain` | `no_action` | `False` | `False` | `False` | `acknowledge_park_or_reject_status` |
| `ambiguous_reply` | `clarify_required` | `ask_clarifying_question` | `False` | `False` | `False` | `ask_one_short_clarification` |
| `multiple_options` | `clarify_required` | `ask_clarifying_question` | `False` | `False` | `False` | `ask_user_to_choose_one_option` |
| `approval_with_execution_words` | `stop_and_require_new_scope` | `no_action` | `False` | `True` | `True` | `stop_and_ask_for_separate_explicit_scope` |

## Forbidden Operations

All forbidden operation flags are set to `false`: commit, push, Obsidian sync,
mainline merge, promotion, release, reviewed knowledge write, evidence support
creation, action-basis creation, template/tool writes, dependency install,
background service, hook install, and MCP write tool.

## Positive Fixtures

The package includes 4 positive fixtures.

## Failure Cases

The package includes 53 failure cases that reject automatic
execution, missing scope separation, missing approval separation, and boundary
confusion.

## Usage

Ordinary agents should run the verifier. `--rebuild` is Builder-only.
