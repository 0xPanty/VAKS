---
record_kind: sandbox_slice_plan
slice_id: 2026-06-16-p2-58-user-decision-static-boundary-scan-regression-sandbox
status: built_pending_review
---

# Slice Plan

## Objective

Make the p2-57 static boundary scan regression-testable without changing p2-57
or any main architecture file.

## Why This Slice

p2-57 reached Product Acceptance, but its remaining non-blocking risk was that
static boundary scanning was phrase-based and not mutation-tested directly.
p2-58 adds a small sandbox scanner regression around the command surfaces that
ordinary follow-up agents would run.

## Write Scope

Only:

```text
outputs/review/vaks-implementation-sandbox/2026-06-16-p2-58-user-decision-static-boundary-scan-regression-sandbox/
```

## Do Not Touch

```text
SCHEMA.md
ARCHITECTURE_PRINCIPLES.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
README.md
wiki/claims/
wiki/patterns/
wiki/decisions/
templates/
tools/
Obsidian vault
old sandbox slices
```

## Acceptance

- Live p2-57 runner/build files scan clean under allowed write rules.
- Positive fixtures pass.
- Failure cases cover git, dependency install, shell=True, service/task/hook/MCP
  strings, unauthorized writes, and destructive remove strings.
- p2-57 final gate remains pass.
- Reviewer, Boundary Auditor, and GPT-5.5 extra-high Product Acceptance pass.

