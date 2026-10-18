# User Decision Replay Portability Audit

Sandbox-only portability audit for the p2-63 replay regression. It checks hidden dependencies, process execution risk, command clarity, stable paths, and operator rerun instructions.

- portability ready: `True`
- source replay ready: `True`
- replay count: `15`
- standard library only: `True`
- stable paths: `True`
- clear commands: `True`
- builder execution tokens: `[]`

## Commands

### build_replay

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-16-p2-63-user-decision-runbook-replay-regression-sandbox\artifact\build_user_decision_runbook_replay_regression.py
```

### verify_replay

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-16-p2-63-user-decision-runbook-replay-regression-sandbox\artifact\verify_user_decision_runbook_replay_regression.py
```

### final_gate

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-16-p2-63-user-decision-runbook-replay-regression-sandbox\artifact\verify_user_decision_runbook_replay_regression.py --final-gate
```

## Operator Sequence

1. Read the p2-64 audit first.
2. Run the p2-63 default verifier before using replay outputs.
3. Run the p2-63 final gate only when validating closeout state.
4. Stop if either command fails.
5. Do not treat a pass as execution, merge, promotion, sync, reviewed knowledge, evidence support, action basis, or user approval.

## Hard No

- `do_not_execute_user_decision_option`
- `do_not_merge_mainline`
- `do_not_promote`
- `do_not_sync_obsidian`
- `do_not_commit`
- `do_not_push`
- `do_not_install_dependencies`
- `do_not_start_background_service`
- `do_not_use_mcp_write_tool`
- `do_not_create_reviewed_knowledge`
- `do_not_create_evidence_support`
- `do_not_create_action_basis`
- `do_not_collect_user_approval_by_inference`
