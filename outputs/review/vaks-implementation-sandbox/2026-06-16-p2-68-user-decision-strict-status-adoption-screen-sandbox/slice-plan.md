---
slice_id: 2026-06-16-p2-68-user-decision-strict-status-adoption-screen-sandbox
status: planned
---

# Slice Plan

## Slice

`2026-06-16-p2-68-user-decision-strict-status-adoption-screen-sandbox`

## Why This Slice

p2-67 packaged strict status parsing in a sandbox-local module. This slice screens adoption routes before any verifier adoption, old-slice backfill, shared helper migration, tools edit, or mainline change.

## Scope

Write only inside:

```text
outputs/review/vaks-implementation-sandbox/2026-06-16-p2-68-user-decision-strict-status-adoption-screen-sandbox/
```

Read-only source slice:

```text
outputs/review/vaks-implementation-sandbox/2026-06-16-p2-67-user-decision-strict-status-package-sandbox/
```

## Do Not Touch

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
- old sandbox slices, except read-only inspection

## Deliverables

- adoption screen builder
- adoption screen verifier
- JSON contract
- JSON, Markdown, and HTML adoption outputs
- positive fixtures
- failure cases
- verification report
- Reviewer report
- Boundary Auditor report
- GPT-5.5 extra-high Product Acceptance report
- next-step recommendation

## Acceptance Criteria

- p2-67 source slice is verified as `PASS_PRODUCT_GRADE`.
- Future new sandbox verifier adoption is the only recommended route.
- Package-only hold is allowed as a parked option.
- Old-slice backfill, shared helper/tools adoption, and mainline integration require separate user approval.
- Failure cases reject unsafe adoption, authority drift, and dependency/network/MCP drift.
- Reviewer, Boundary Auditor, and Product Acceptance pass.
- Final gate passes.

## Stop Conditions

- Any required write would leave this slice path.
- Any task requires dependency install, commit, push, sync, hook, service, background automation, MCP write tool, old-slice rewrite, shared helper edit, tools edit, or mainline edit.
- Any output claims sandbox screening as reviewed knowledge, evidence support, action basis, mainline readiness, promotion readiness, Obsidian sync, user approval, or execution authority.
- Product Acceptance returns `BLOCKED_NEEDS_USER`.
