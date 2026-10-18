---
slice_id: 2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox
status: plan_ready
---

# Slice Plan

## Goal

Create a sandbox-only no-write transaction package for the future old-file status-only normalization.

The package records the 75 p2-72 status changes as transaction operations with current file hashes, before status, proposed status, rollback status, and strict preconditions for any future executor. It does not execute the transaction.

## Scope

Write only:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox/
```

Read-only inputs:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-72-original-slice-normalization-decision-packet-sandbox/
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-77-old-file-status-normalization-executor-readiness-gate-sandbox/
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-79-old-file-status-normalization-fresh-preflight-drift-recheck-sandbox/
outputs/review/vaks-implementation-sandbox/2026-06-16-p2-67-user-decision-strict-status-package-sandbox/
```

## Acceptance Criteria

- Transaction operation count is 75.
- Unique target file count is 75.
- Old slice count is 20.
- Each operation records:
  - target path
  - old slice id
  - current file SHA256
  - before status
  - proposed status
  - rollback status
  - current status matches manifest
  - proposed status not already applied
  - write_applied: false
- `requires_exact_p2_75_approval` is true.
- `requires_fresh_hash_check_before_write` is true.
- `executor_write_allowed_now` is false.
- `old_slice_writes_applied` is 0.
- Local verifier, Reviewer, Boundary Auditor, GPT-5.5 Product Acceptance, and final gate pass.

## Non-Scope

- No old slice edits.
- No status normalization execution.
- No mainline merge or promotion.
- No main architecture, wiki truth-layer, templates/tools, or Obsidian edits.
- No commit, push, sync, background service, hook, or dependency install.

## Stop Conditions

Stop before any old slice write, mainline edit, template/tool edit, wiki truth-layer edit, Obsidian sync, commit, push, or attempt to treat this transaction package as approval.
