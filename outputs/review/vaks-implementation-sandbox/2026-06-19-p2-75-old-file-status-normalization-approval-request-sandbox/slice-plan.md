---
slice_id: 2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox
status: planned
---

# Slice Plan

## Goal

Create a sandbox-only authorization request packet for old-file status-only normalization of the original 20 VAKS implementation slices.

This slice does not collect approval and does not edit old files. It defines the exact approval language and decision boundaries needed before a future slice may touch old slice frontmatter status fields.

## Write Scope

Only this path:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/
```

## Inputs

- p2-72 decision packet: 75 dry-run status-only changes
- p2-73 sidecar ledger: 20 sidecar closeouts passed, old-file strict final-gate still 0
- p2-74 operator status surface: human-readable current state and blocked old-file normalization
- p2-67 strict status parser: final-gate status parsing

## Non-Goals

- No old slice edits.
- No normalization execution.
- No approval inference from generic user language.
- No mainline merge.
- No promotion.
- No reviewed knowledge, evidence support, or action basis creation.

## Acceptance Criteria

- Packet states that current approval is not collected.
- Packet contains one exact approval phrase and multiple non-approval examples.
- Packet limits future allowed edits to frontmatter `status` fields listed in the p2-72 dry-run manifest.
- Packet blocks content/body edits, artifact edits, old slice file creation/deletion, mainline changes, template/tool changes, wiki truth-layer writes, and Obsidian sync.
- Fixtures and failure cases prove generic continuation language is not approval.
- Local verifier, Reviewer, Boundary Auditor, and GPT-5.5 Product Acceptance pass.

## Stop Conditions

Stop if completing this slice requires writing old slice files or treating this request packet as actual user approval.
