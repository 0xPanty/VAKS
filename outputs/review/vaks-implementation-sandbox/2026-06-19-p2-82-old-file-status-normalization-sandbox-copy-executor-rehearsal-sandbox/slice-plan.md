---
slice_id: 2026-06-19-p2-82-old-file-status-normalization-sandbox-copy-executor-rehearsal-sandbox
status: plan_ready
---

# Slice Plan

## Goal

Create a sandbox-only copy executor rehearsal for the p2-80 transaction package.

The rehearsal copies the 75 old-slice target reports into this slice's fixtures, applies the status-only change to the copies, verifies the result, rolls the copies back, and verifies final copy hashes match the original target hashes. It never writes the old slice files.

## Scope

Write only:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-82-old-file-status-normalization-sandbox-copy-executor-rehearsal-sandbox/
```

Read-only inputs:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox/
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-77-old-file-status-normalization-executor-readiness-gate-sandbox/
outputs/review/vaks-implementation-sandbox/2026-06-16-p2-67-user-decision-strict-status-package-sandbox/
```

## Acceptance Criteria

- fixture_copy_count: 75
- fixture_apply_write_count: 75
- fixture_rollback_write_count: 75
- after_status_match_count: 75
- body_unchanged_after_apply_count: 75
- final_copy_sha_match_count: 75
- final_copy_status_match_count: 75
- old_slice_writes_applied: 0
- executor_write_allowed_now: false
- Local verifier, Reviewer, Boundary Auditor, GPT-5.5 Product Acceptance, and final gate pass.

## Non-Scope

- No old slice edits.
- No status normalization execution against original files.
- No mainline merge or promotion.
- No main architecture, wiki truth-layer, templates/tools, or Obsidian edits.
- No commit, push, sync, background service, hook, or dependency install.

## Stop Conditions

Stop before any old slice write, mainline edit, template/tool edit, wiki truth-layer edit, Obsidian sync, commit, push, or attempt to treat sandbox copy rehearsal as approval.
