---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox
status: built_pending_review
truth_boundary: sandbox_only
---

# Slice Plan

## Slice

`2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox`

## Goal

Define a sandbox-only gate for how a future explicit user decision would be
captured, validated, and classified before any later formal-vault write slice.

## Why Now

P2-26 proved synthetic approve/deny/revise classification. The next smallest
safe step is to define the future intake contract that prevents a later agent
from treating silence, prior Product Acceptance, or casual chat as formal write
approval.

## Write Scope

Only:

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox/
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

- Contract states required future decision fields and exact hash bindings.
- Positive fixtures cover approve, deny, and revise reference records.
- Approval remains not actionable in this slice.
- Deny and revise block write.
- Real user text is not captured or stored.
- Formal vault is not read, scanned, written, hashed, snapshotted, or synced.
- Failure cases prove bad paths are caught.
- Reviewer, Boundary, and GPT-5.5 xhigh Product Acceptance pass.
- Final gate passes after Product Acceptance.

## Stop Conditions

Stop if the slice requires real user approval collection, real user text
storage, formal vault access, sync, commit, push, promotion, dependency
installation, background service, hook, or MCP write tool.

## Start Git Status Summary

```text
pre-existing dirty tree recorded before build; final audit scoped to this slice path
```

The dirty tree is treated as pre-existing baseline. Final audit is scoped to
this slice path only.
