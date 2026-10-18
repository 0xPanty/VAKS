---
record_kind: sandbox_slice_plan
slice_id: 2026-06-16-p2-57-user-decision-chain-regression-bundle-sandbox
status: built_pending_review
---

# Slice Plan

## Objective

Build a sandbox-only regression bundle for the user-decision guard chain from
p2-51 through p2-56.

This slice proves that the user decision request packet, no-auto-advance guard,
classifier, renderer, e2e dry-run simulator, and demo transcript still form a
non-executing chain. It does not collect a user decision and does not authorize
execution, mainline merge, promotion, Obsidian sync, reviewed knowledge,
evidence support, or action basis.

## Why This Slice

p2-56 made the chain human-readable. p2-57 makes the same chain regression
checkable by a later ordinary agent with one verifier command.

## Write Scope

Only this path is in scope:

```text
outputs/review/vaks-implementation-sandbox/2026-06-16-p2-57-user-decision-chain-regression-bundle-sandbox/
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

## Pre-Worktree Summary

The worktree was already dirty before this slice. The visible pre-existing
baseline included modified root/raw/templates/tools files and many untracked
raw/output/wiki artifacts. This slice treats those as baseline and audits only
new or modified paths under the p2-57 sandbox directory.

## Acceptance

- Required root files are present.
- Artifact runner reads p2-51 through p2-56 and reruns p2-56 final gate.
- Positive fixtures bind expected source-slice and demo-guard outcomes.
- Failure cases mutate the bundle output and are rejected by the verifier.
- Reviewer reports no blocking quality issue.
- Boundary Auditor reports no authority or write-scope violation.
- GPT-5.5 extra-high Product Acceptance returns PASS_PRODUCT_GRADE.
- Final git audit shows this slice only added files under the p2-57 sandbox path.

## Stop Conditions

Stop if the slice needs mainline edits, protected-path edits, commit/push/sync,
dependency installation, background service, hook, MCP write tool, or Product
Acceptance returns BLOCKED_NEEDS_USER.

