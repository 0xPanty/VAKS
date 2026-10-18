---
slice_id: 2026-06-19-p2-86-approval-to-prewrite-gate-chain-sandbox
status: planned
---

# Slice Plan

## Goal

Build a sandbox-only integrated gate chain for future old-file status-only normalization:

```text
exact p2-75 approval fixture
-> fresh hash preflight
-> p2-82 byte-safe rehearsal evidence
-> boundary conditions
-> ready_for_prewrite_confirmation
```

The chain must never authorize old-file writes in this slice.

## Why This Slice Now

p2-85 makes approval classification executable. p2-80 defines 75 prewrite hashes. p2-82 proves byte-safe apply/rollback on sandbox copies. This slice combines those pieces into one prewrite gate so a future agent cannot treat any single green check as sufficient write authority.

## Write Scope

Allowed write root:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-86-approval-to-prewrite-gate-chain-sandbox/
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
- p2-75 / p2-80 / p2-82 / p2-85 source files
- Git commit, push, sync, hooks, background automation

## Acceptance Criteria

- Required slice files exist.
- Positive fixture reaches `ready_for_prewrite_confirmation` only, not old-file write authority.
- Fresh hash preflight confirms 75/75 current target hashes match p2-80 required hashes.
- Negative fixtures cover no exact approval, hash drift, missing rehearsal evidence, failed boundary, Product Acceptance as approval, mainline authority request, and immediate write request.
- Local verifier passes.
- Reviewer returns REVIEW_PASS_NO_BLOCKER.
- Boundary Auditor returns PASS_BOUNDARY.
- GPT-5.5 extra-high Product Acceptance returns PASS_PRODUCT_GRADE.
- Final gate passes.

## Stop Conditions

Stop if this slice would require writing old slice files, applying the 75 status-only changes, editing prior sandbox slices, editing mainline docs, writing wiki truth layers, modifying templates/tools, syncing Obsidian, committing, or pushing.
