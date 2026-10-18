---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p2-22-formalization-readiness-polish-sandbox
status: built_pending_review
truth_boundary: sandbox_only
---

# Slice Plan

## Goal

Convert the P2-21 sandbox workbench from a product-grade prototype into a
formalization-readiness pilot pack. The output must make the next user-visible
step clear without writing to the formal vault or changing main architecture.

## Why This Slice

P2-21 already proved a workbench can exist in sandbox form. What is still needed
is the product handoff layer: first-run path, daily-use path, receipt inspection,
formalization decision matrix, acceptance gates, and failure rules that prevent
authority confusion.

## Write Scope

Only this path may be written:

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p2-22-formalization-readiness-polish-sandbox/
```

## Explicit Non-Scope

- No `SCHEMA.md`, `ARCHITECTURE_PRINCIPLES.md`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md`, or root `README.md` edits.
- No `wiki/claims/`, `wiki/patterns/`, `wiki/decisions/`, `templates/`, or `tools/` edits.
- No formal Obsidian vault write.
- No sync, commit, push, promotion, background service, hooks, dependency install, MCP write tool, or real `.base` file.

## Acceptance Standard

- Build the pilot pack under this slice.
- Provide at least 2 positive fixtures.
- Provide at least 18 failure cases.
- Verify default read-only validation and explicit rebuild validation.
- Reviewer returns `REVIEW_PASS`.
- Boundary Auditor returns `BOUNDARY_PASS`.
- GPT-5.5 reasoning=xhigh Product Acceptance returns `PASS_PRODUCT_GRADE`.

## Start Git Status Summary

```text
pre-existing dirty tree recorded by orchestrator before build; final audit scoped to this slice path
```

The dirty tree is treated as pre-existing baseline. Final audit is scoped to
new or modified files under this slice.
