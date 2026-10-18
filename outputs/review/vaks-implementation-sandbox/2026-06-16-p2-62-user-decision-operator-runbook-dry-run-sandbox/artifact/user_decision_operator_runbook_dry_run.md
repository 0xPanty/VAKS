# User Decision Operator Runbook Dry Run

Sandbox-only dry-run runbook. It uses the p2-61 readiness brief to decide whether a follow-up agent may inspect the frozen handoff chain. It cannot execute, merge, promote, sync, commit, push, create reviewed knowledge, create evidence support, create action basis, or infer user approval.

- runbook ready: `True`
- dry run only: `True`
- source slice: `2026-06-16-p2-61-user-decision-freeze-operator-readiness-brief-sandbox`
- frozen entries: `268`

## Decision Table

| Request kind | Decision | Manual only |
| --- | --- | --- |
| `inspect_readiness_brief` | `ALLOW_READ_ONLY_INSPECTION` | `False` |
| `inspect_frozen_handoff_chain` | `ALLOW_READ_ONLY_INSPECTION` | `False` |
| `manual_drift_check` | `ALLOW_MANUAL_READONLY_VERIFICATION` | `True` |
| `execute_user_decision_option` | `STOP_REQUIRE_SEPARATE_USER_APPROVAL` | `False` |
| `merge_mainline` | `STOP_REQUIRE_SEPARATE_USER_APPROVAL` | `False` |
| `promote` | `STOP_REQUIRE_SEPARATE_USER_APPROVAL` | `False` |
| `sync_obsidian` | `STOP_REQUIRE_SEPARATE_USER_APPROVAL` | `False` |
| `commit` | `STOP_REQUIRE_SEPARATE_USER_APPROVAL` | `False` |
| `push` | `STOP_REQUIRE_SEPARATE_USER_APPROVAL` | `False` |
| `create_reviewed_knowledge` | `STOP_REQUIRE_SEPARATE_USER_APPROVAL` | `False` |
| `create_evidence_support` | `STOP_REQUIRE_SEPARATE_USER_APPROVAL` | `False` |
| `create_action_basis` | `STOP_REQUIRE_SEPARATE_USER_APPROVAL` | `False` |
| `infer_user_approval` | `STOP_REQUIRE_SEPARATE_USER_APPROVAL` | `False` |

## Manual Verification Command

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-16-p2-60-user-decision-index-freeze-checksum-sandbox\artifact\verify_user_decision_index_freeze_checksum.py --final-gate
```

This runbook records the command only; it does not run it.

## Hard No

- `do_not_execute_user_decision_option`
- `do_not_merge_mainline`
- `do_not_promote`
- `do_not_sync_obsidian`
- `do_not_commit`
- `do_not_push`
- `do_not_install_dependencies`
- `do_not_start_background_service`
- `do_not_install_hooks`
- `do_not_use_mcp_write_tool`
- `do_not_create_reviewed_knowledge`
- `do_not_create_evidence_support`
- `do_not_create_action_basis`
- `do_not_collect_user_approval_by_inference`
