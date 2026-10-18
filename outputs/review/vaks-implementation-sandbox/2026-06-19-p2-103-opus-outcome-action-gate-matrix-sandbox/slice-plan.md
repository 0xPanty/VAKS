---
slice_id: 2026-06-19-p2-103-opus-outcome-action-gate-matrix-sandbox
status: planned
---

# Slice Plan

## Goal

Create an action-gate matrix for the three possible external Opus result tokens.

## Why This Slice Now

p2-102 validates future Opus result records. This slice defines what a later agent may do after each valid outcome, especially preventing `OPUS_PASS_SANDBOX_CLOSEOUT` from being misread as automatic mainline merge, reviewed knowledge, evidence support, action basis, commit, push, or sync.

## Write Scope

Only this path may be written:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-103-opus-outcome-action-gate-matrix-sandbox/
```

## Non-Write Scope

- No old slice edits.
- No root architecture document edits.
- No README edits.
- No wiki truth layer edits.
- No templates or tools edits.
- No Obsidian vault writes or sync.
- No commit, push, promotion, or mainline merge.
- No claim that Opus has approved anything.

## Acceptance Criteria

- Read p2-96 allowed Opus conclusion tokens and p2-102 dry-run validator state.
- Generate an action-gate matrix for PASS, REVISE, and BLOCKED.
- Include fixtures for all three allowed outcomes.
- Include failure cases for unsafe transitions and authority confusion.
- Verify that no outcome authorizes automatic merge, promotion, reviewed knowledge, evidence support, action basis, commit, push, or sync.
- Pass local verifier, Reviewer, Boundary Auditor, and GPT-5.5 Product Acceptance.

## Stop Conditions

- A real Opus result is needed.
- Any old slice or protected path would need modification.
- The matrix would need to treat Opus PASS as user approval or mainline merge permission.
