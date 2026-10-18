# User Decision Freeze Operator Readiness Brief

Sandbox-only operator brief for the p2-60 checksum freeze. It explains what is frozen, how to manually verify drift, and what still cannot be executed without separate user approval.

- brief ready: `True`
- source slice: `2026-06-16-p2-60-user-decision-index-freeze-checksum-sandbox`
- frozen source slices: `9`
- frozen file entries: `268`
- missing count: `0`
- hash algorithm: `sha256_bytes`
- freeze ready: `True`

## Manual Drift Verification

Run this only when an operator needs to re-check p2-60 before using the handoff chain:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-16-p2-60-user-decision-index-freeze-checksum-sandbox\artifact\verify_user_decision_index_freeze_checksum.py --final-gate
```

This p2-61 builder does not run that command. It only records the manual read-only check.

## Operator Steps

1. Read this brief and confirm the source slice is p2-60.
2. If drift must be checked, run the manual read-only verification command.
3. If the command fails, stop and inspect p2-60 before using the handoff index.
4. If the command passes, use the freeze only as sandbox handoff integrity input.
5. Ask the user separately before any execution, merge, promotion, sync, commit, or push.

## Readiness Flags

- `automatic_execution`: `False`
- `mainline_ready`: `False`
- `promotion_ready`: `False`
- `formal_vault_ready`: `False`
- `obsidian_sync_ready`: `False`
- `reviewed_knowledge_ready`: `False`
- `evidence_support_ready`: `False`
- `action_basis_ready`: `False`
- `user_approval_collected`: `False`

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
- `do_not_treat_checksum_as_user_approval`
