---
slice_id: 2026-06-19-p2-83-post-rehearsal-goal-state-cockpit-sandbox
status: planned
---

# Slice Plan

## Goal

Build a post-p2-82 operator cockpit that states the current goal state in one product-grade sandbox artifact.

The cockpit must make these distinctions explicit:

- The original 20 items have legacy Product Acceptance/pass evidence.
- The original 20 items have product-grade sidecar closeout evidence.
- The old slice files are still 0/20 current strict final-gate complete.
- The 75 status-only old-file changes remain unapplied.
- p2-82 proves byte-safe sandbox-copy rehearsal, not old-file write authority.
- Generic continuation language is not the exact p2-75 approval phrase.

## Why This Slice Now

p2-82 proved the copy executor rehearsal at byte level. The next useful sandbox-only improvement is not another executor mutation. It is an operator-facing status cockpit that prevents a future agent from confusing "this slice passed" with "the whole goal is complete."

## Write Scope

Allowed write root:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-83-post-rehearsal-goal-state-cockpit-sandbox/
```

## Do Not Touch

- SCHEMA.md
- ARCHITECTURE_PRINCIPLES.md
- FUSION_ARCHITECTURE_V0_2_DRAFT.md
- README.md
- wiki/claims/
- wiki/patterns/
- wiki/decisions/
- templates/
- tools/
- Obsidian vault
- Old slice files
- Git commit, push, sync, hooks, background automation

## Acceptance Criteria

- Required slice files exist.
- Artifact includes JSON, Markdown, and HTML cockpit surfaces.
- Fixtures include positive state, decision, byte-safety, authority-boundary, and user-answer classification examples.
- Failure cases cover all-done overclaim, approval confusion, rehearsal authority confusion, stale pre-p2-82 surface, byte-evidence omission, and mainline/action authority confusion.
- Local verifier passes.
- Reviewer returns REVIEW_PASS_NO_BLOCKER.
- Boundary Auditor returns PASS_BOUNDARY.
- GPT-5.5 extra-high Product Acceptance returns PASS_PRODUCT_GRADE.
- Final gate passes.
- Git path audit shows this slice is the only current-turn write scope.

## Stop Conditions

Stop immediately if this slice would require editing old slices, mainline docs, wiki truth layers, templates, tools, Obsidian vault, or executing commit/push/sync.
