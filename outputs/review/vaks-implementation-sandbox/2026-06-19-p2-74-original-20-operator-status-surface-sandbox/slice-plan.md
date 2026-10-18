---
slice_id: 2026-06-19-p2-74-original-20-operator-status-surface-sandbox
status: planned
---

# Slice Plan

## Goal

Create a sandbox-only operator status surface for the original 20 VAKS implementation items.

The purpose is to make the p2-70 through p2-73 closeout state understandable:

- what is product-grade now;
- what is still not old-file current strict final-gate complete;
- what requires separate user approval;
- what a future agent may safely do next.

## Write Scope

Only this path:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-74-original-20-operator-status-surface-sandbox/
```

## Inputs

- p2-71 normalization audit JSON
- p2-72 decision packet JSON
- p2-73 sidecar closeout ledger JSON
- p2-67 strict status parser for local final-gate status checks

## Non-Goals

- No old slice edits.
- No status normalization execution.
- No mainline merge.
- No promotion.
- No reviewed knowledge, evidence support, or action basis creation.
- No Obsidian sync.

## Acceptance Criteria

- The surface says in plain language that original 20 legacy evidence exists, p2-73 sidecar closeout is product-grade, and old slice files still have 0 of 20 current strict final-gate completion.
- The surface exposes allowed and blocked next actions.
- The machine JSON, Markdown, and HTML outputs agree.
- Fixtures and failure cases protect against authority confusion.
- Local verifier, Reviewer, Boundary Auditor, and GPT-5.5 Product Acceptance pass.

## Stop Conditions

Stop if completing this slice requires writing outside the p2-74 sandbox path or treating sandbox evidence as old-file normalization, mainline readiness, reviewed knowledge, evidence support, action basis, or user approval.
