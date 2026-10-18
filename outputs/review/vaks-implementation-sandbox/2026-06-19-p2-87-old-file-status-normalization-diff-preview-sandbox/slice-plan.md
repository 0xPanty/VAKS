---
slice_id: 2026-06-19-p2-87-old-file-status-normalization-diff-preview-sandbox
status: planned
---

# Slice Plan

## Goal

Create a sandbox-only human-reviewable diff preview for the 75 old-file status-only normalization operations.

The preview must prove, without writing old files, that each proposed operation changes only `frontmatter.status` and preserves body content plus non-status frontmatter.

## Why This Slice Now

p2-86 proves the integrated no-write gate can reach `ready_for_prewrite_confirmation`. The next useful artifact is a concrete review surface for the 75 operations so a future user or agent can inspect what would change before any separately approved executor slice.

## Write Scope

Allowed write root:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-87-old-file-status-normalization-diff-preview-sandbox/
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
- p2-80 / p2-86 source files
- Git commit, push, sync, hooks, background automation

## Acceptance Criteria

- Required slice files exist.
- Diff preview includes all 75 p2-80 operations.
- Each preview has before/proposed/rollback status, before/proposed SHA256, and a one-line status delta.
- Each preview proves body content is unchanged.
- Each preview proves non-status frontmatter is unchanged.
- The preview writes no old slice files and grants no write authority.
- Local verifier passes.
- Reviewer returns REVIEW_PASS_NO_BLOCKER.
- Boundary Auditor returns PASS_BOUNDARY.
- GPT-5.5 extra-high Product Acceptance returns PASS_PRODUCT_GRADE.
- Final gate passes.

## Stop Conditions

Stop if this slice would require applying the 75 status-only changes, editing old slices, editing p2-80 or p2-86, editing mainline docs, writing wiki truth layers, modifying templates/tools, syncing Obsidian, committing, or pushing.
