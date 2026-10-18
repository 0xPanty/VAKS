---
slice_id: 2026-06-19-p2-79-old-file-status-normalization-fresh-preflight-drift-recheck-sandbox
status: plan_ready
---

# Slice Plan

## Goal

Refresh the old-file status-only normalization preflight as a sandbox-only drift recheck.

This slice verifies that the 75 p2-72 dry-run frontmatter status targets still match their manifest `current_status` values and therefore have not drifted since earlier preflight work. It does not write old slice files and does not authorize execution.

## Scope

Write only:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-79-old-file-status-normalization-fresh-preflight-drift-recheck-sandbox/
```

Read-only inputs:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-72-original-slice-normalization-decision-packet-sandbox/
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-77-old-file-status-normalization-executor-readiness-gate-sandbox/
outputs/review/vaks-implementation-sandbox/2026-06-16-p2-67-user-decision-strict-status-package-sandbox/
```

## Acceptance Criteria

- `target_change_count` is 75.
- `target_file_count` is 75.
- `target_old_slice_count` is 20.
- `missing_target_count` is 0.
- `current_status_mismatch_count` is 0.
- `proposed_status_already_applied_count` is 0.
- `old_slice_writes_applied` is 0.
- `executor_write_allowed` is false.
- Local verifier, Reviewer, Boundary Auditor, GPT-5.5 Product Acceptance, and final gate pass.

## Non-Scope

- No old slice edits.
- No status normalization execution.
- No mainline merge or promotion.
- No main architecture, wiki truth-layer, templates/tools, or Obsidian edits.
- No commit, push, sync, background service, hook, or dependency install.

## Stop Conditions

Stop and ask the user before any old slice write, mainline edit, template/tool edit, wiki truth-layer edit, Obsidian sync, or attempt to treat generic continuation text as p2-75 exact approval.
