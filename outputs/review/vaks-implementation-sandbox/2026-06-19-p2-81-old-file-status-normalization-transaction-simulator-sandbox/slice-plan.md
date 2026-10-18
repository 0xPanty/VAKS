---
slice_id: 2026-06-19-p2-81-old-file-status-normalization-transaction-simulator-sandbox
status: plan_ready
---

# Slice Plan

## Goal

Create a sandbox-only simulator for the p2-80 no-write transaction package.

The simulator applies each proposed frontmatter `status` change in memory, verifies that only the status field changes, verifies rollback restores the original content hash, and records that no old slice file was written.

## Scope

Write only:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-81-old-file-status-normalization-transaction-simulator-sandbox/
```

Read-only inputs:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox/
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-77-old-file-status-normalization-executor-readiness-gate-sandbox/
outputs/review/vaks-implementation-sandbox/2026-06-16-p2-67-user-decision-strict-status-package-sandbox/
```

## Acceptance Criteria

- Simulates 75 operations from the p2-80 transaction package.
- For every operation:
  - before status matches p2-80 before status;
  - simulated after status equals proposed status;
  - simulated rollback status equals rollback status;
  - body content after frontmatter is unchanged;
  - rollback SHA256 equals original target SHA256;
  - no old slice write is applied.
- Aggregate counts:
  - simulated_operation_count: 75
  - after_status_match_count: 75
  - rollback_status_match_count: 75
  - body_unchanged_count: 75
  - rollback_sha_match_count: 75
  - old_slice_writes_applied: 0
  - executor_write_allowed_now: false
- Local verifier, Reviewer, Boundary Auditor, GPT-5.5 Product Acceptance, and final gate pass.

## Non-Scope

- No old slice edits.
- No status normalization execution.
- No mainline merge or promotion.
- No main architecture, wiki truth-layer, templates/tools, or Obsidian edits.
- No commit, push, sync, background service, hook, or dependency install.

## Stop Conditions

Stop before any old slice write, mainline edit, template/tool edit, wiki truth-layer edit, Obsidian sync, commit, push, or attempt to treat simulation success as approval.
