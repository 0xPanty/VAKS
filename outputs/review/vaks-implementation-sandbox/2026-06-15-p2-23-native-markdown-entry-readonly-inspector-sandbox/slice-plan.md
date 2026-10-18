---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p2-23-native-markdown-entry-readonly-inspector-sandbox
status: built_pending_review
truth_boundary: sandbox_only
---

# Slice Plan

## Goal

Create a sandbox-only native Markdown entry plus read-only inspector pilot. This
tests whether the P2-22 formalization route can feel more like an Obsidian
operator surface without writing to the formal vault or creating real Bases.

## Why This Slice

P2-22 received `PASS_PRODUCT_GRADE` and recommended
`native-markdown-entry-plus-readonly-inspector-sandbox`.

## Write Scope

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p2-23-native-markdown-entry-readonly-inspector-sandbox/
```

## Explicit Non-Scope

- No protected root docs.
- No `wiki/claims/`, `wiki/patterns/`, `wiki/decisions/`, `templates/`, or
  `tools/` edits.
- No formal Obsidian vault write.
- No sync, commit, push, promotion, dependency install, background service,
  MCP write tool, hooks, production UI, real `.base`, network post, or
  local-storage write.

## Acceptance Standard

- Native Markdown entry pages exist and resolve as an Obsidian-style graph.
- Read-only inspector has no write controls.
- Positive fixtures pass and failure cases fail.
- Local file/link dry-run proves the main journeys.
- Reviewer returns `REVIEW_PASS`.
- Boundary Auditor returns `BOUNDARY_PASS`.
- GPT-5.5 xhigh Product Acceptance returns `PASS_PRODUCT_GRADE`.
- `--final-gate` passes after Product Acceptance.

## Start Git Status Summary

```text
pre-existing dirty tree recorded before build; final audit scoped to this slice path
```

The dirty tree is treated as pre-existing baseline. Final audit is scoped to
this slice path only.
