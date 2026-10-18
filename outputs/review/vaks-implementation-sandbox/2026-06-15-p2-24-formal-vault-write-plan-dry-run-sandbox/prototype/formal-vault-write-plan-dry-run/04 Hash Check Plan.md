---
record_kind: sandbox_hash_check_plan
slice_id: 2026-06-15-p2-24-formal-vault-write-plan-dry-run-sandbox
status: sandbox_pilot
sandbox_only: true
truth_boundary: sandbox_only
---

# Hash Check Plan

## Algorithm

`sha256`

## Phases

- `before_snapshot`
- `after_write`
- `after_rollback_if_needed`

## Requirements

- abort_on_missing_before_hash: `True`
- abort_on_unexpected_after_hash: `True`
- abort_on_dirty_state: `True`
- abort_on_unexpected_file: `True`
- verify_after_rollback: `True`
- per_file_records_required: `True`
- record_format: `json-lines`
- no_executable_commands: `True`
- command_templates: `0`

## Per-File Hash Records

| File ID | Relative Target | Before Hash | After Hash | Rollback Hash |
| --- | --- | --- | --- | --- |
| `native_home` | `VAKS-Workbench-Draft/00 Native Home.md` | `before_hash_sha256` | `after_hash_sha256` | `rollback_hash_sha256` |
| `status_board` | `VAKS-Workbench-Draft/02 Status Board.md` | `before_hash_sha256` | `after_hash_sha256` | `rollback_hash_sha256` |
| `receipt_index` | `VAKS-Workbench-Draft/03 Receipt Index.md` | `before_hash_sha256` | `after_hash_sha256` | `rollback_hash_sha256` |
| `boundary_stop` | `VAKS-Workbench-Draft/04 Boundary Stop.md` | `before_hash_sha256` | `after_hash_sha256` | `rollback_hash_sha256` |
| `readonly_inspector` | `VAKS-Workbench-Draft/readonly-inspector.html` | `before_hash_sha256` | `after_hash_sha256` | `rollback_hash_sha256` |

## Boundary

Hash checks are process integrity checks. They are not evidence support,
reviewed knowledge, action basis, sync approval, commit approval, push approval,
or formal vault approval.
