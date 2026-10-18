---
slice_id: 2026-06-19-p2-76-old-file-status-normalization-executor-preflight-sandbox
status: planned
---

# Slice Plan

## Goal

Create a sandbox-only executor preflight dry-run for future old-file status-only normalization.

This slice proves what an executor would check before applying the p2-72 dry-run status changes. It does not collect approval and does not write old slice files.

## Write Scope

Only this path:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-76-old-file-status-normalization-executor-preflight-sandbox/
```

## Inputs

- p2-72 decision packet dry-run manifest
- p2-75 approval request packet and exact approval phrase
- p2-67 strict status parser
- old slice report files read-only, to verify current frontmatter status

## Non-Goals

- No old slice writes.
- No status normalization application.
- No user approval collection.
- No mainline merge.
- No promotion.
- No reviewed knowledge, evidence support, or action basis.

## Acceptance Criteria

- Preflight covers all 75 p2-72 dry-run status changes.
- Preflight verifies each target file exists and its current frontmatter status matches the p2-72 dry-run current status.
- Preflight records proposed status and rollback status for each change.
- Preflight records `approval_present=false`, `executor_write_allowed=false`, and `old_slice_writes_applied=0`.
- Fixtures and failure cases cover missing approval, target drift, body-edit attempts, and rollback absence.
- Local verifier, Reviewer, Boundary Auditor, and GPT-5.5 Product Acceptance pass.

## Stop Conditions

Stop if completing this slice requires applying any old-file change or treating p2-75 as actual approval.
