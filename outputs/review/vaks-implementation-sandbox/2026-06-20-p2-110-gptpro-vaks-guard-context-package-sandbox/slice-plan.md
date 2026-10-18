---
slice_id: 2026-06-20-p2-110-gptpro-vaks-guard-context-package-sandbox
status: context_package_plan_complete
---

# Slice Plan

## Purpose

Create a compact upload/context package for a new GPT Pro project so it can review the proposed positioning of the seven VAKS guard candidates against the existing VAKS architecture.

This slice does not implement tools, modify architecture, promote sandbox artifacts, or write to the formal Obsidian vault.

## Why This First

The current decision risk is conceptual, not code-level: whether the seven candidates should become a new architecture layer, a lightweight tool layer, or remain sandbox-only. A Pro review should receive a clean context packet before any mainline absorption work.

## Paths Allowed

Only:

```text
outputs/review/vaks-implementation-sandbox/2026-06-20-p2-110-gptpro-vaks-guard-context-package-sandbox/
```

## Paths Not Touched

- `SCHEMA.md`
- `ARCHITECTURE_PRINCIPLES.md`
- `FUSION_ARCHITECTURE_V0_2_DRAFT.md`
- `README.md`
- `wiki/claims/`
- `wiki/patterns/`
- `wiki/decisions/`
- `templates/`
- `tools/`
- formal Obsidian vault

## Pre-Start Git Status Summary

The worktree was already heavily dirty before this slice. Existing modified/untracked/deleted files include raw source records, candidate distillations, `outputs/review/` artifacts, some `templates/`, some `tools/`, and unrelated local files. This is treated as pre-existing baseline per user instruction.

This slice audits only newly written files under the allowed p2-110 sandbox path.

## Acceptance Criteria

- A Pro-uploadable context brief exists.
- The brief clearly separates main architecture, proposed tool layer, smart workbench, and sandbox evidence.
- The brief lists the seven guard candidates and their role.
- The brief states that p2-109 proved sandbox readiness only, not mainline absorption.
- The brief asks Pro to judge whether a lightweight tool layer is reasonable and not overbuilt.
- No protected path is edited.

## Stop Conditions

- Any need to modify `tools/`, templates, wiki truth layers, architecture docs, or formal Obsidian vault.
- Any request to claim product-grade mainline absorption from this context package alone.
- Any request to commit, push, sync, start services, or install dependencies.

