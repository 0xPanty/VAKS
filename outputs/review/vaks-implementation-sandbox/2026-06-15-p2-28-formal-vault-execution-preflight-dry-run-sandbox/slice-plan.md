---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p2-28-formal-vault-execution-preflight-dry-run-sandbox
status: built_pending_review
truth_boundary: sandbox_only
---

# Slice Plan

## Slice

`2026-06-15-p2-28-formal-vault-execution-preflight-dry-run-sandbox`

## Goal

Define a sandbox-only execution preflight dry-run for a future formal-vault
write path. This slice checks that the future execution checklist is complete,
but it does not inspect the formal vault and does not execute anything.

## Why Now

P2-27 defined how a future user decision must be referenced and validated. The
next safe step is to prevent a valid decision reference from becoming an
immediate write by requiring a separate preflight and a separate execution
slice.

## Write Scope

Only:

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p2-28-formal-vault-execution-preflight-dry-run-sandbox/
```

## Non-Touched Paths

- `SCHEMA.md`
- `ARCHITECTURE_PRINCIPLES.md`
- `FUSION_ARCHITECTURE_V0_2_DRAFT.md`
- `README.md`
- `wiki/claims/`
- `wiki/patterns/`
- `wiki/decisions/`
- `templates/`
- `tools/`
- Obsidian vault

## Acceptance Criteria

- Contract separates preflight completeness from execution permission.
- Target manifest is relative-path only and dry-run only.
- Positive fixtures cover approved-reference dry-run, denial block, and revision
  block.
- Failure cases prove bad paths are caught.
- No formal vault read, scan, state check, write, hash, snapshot, or sync.
- No actual approval collection or real user text storage.
- Reviewer, Boundary, and GPT-5.5 xhigh Product Acceptance pass.
- Final gate passes after Product Acceptance.

## Stop Conditions

Stop if the slice requires real user approval collection, real user text
storage, formal vault access, formal vault state inspection, sync, commit, push,
promotion, dependency installation, background service, hook, or MCP write tool.

## Start Git Status Summary

```text
pre-existing dirty tree recorded before build; final audit scoped to this slice path
```

The dirty tree is treated as pre-existing baseline. Final audit is scoped to
this slice path only.
