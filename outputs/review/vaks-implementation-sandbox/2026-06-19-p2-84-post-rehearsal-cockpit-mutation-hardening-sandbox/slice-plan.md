---
slice_id: 2026-06-19-p2-84-post-rehearsal-cockpit-mutation-hardening-sandbox
status: planned
---

# Slice Plan

## Goal

Harden the p2-83 post-rehearsal cockpit by turning its declaration-style failure cases into executable mutation tests.

## Why This Slice Now

p2-83 passed Product Acceptance, but Product Acceptance noted that its failure cases are declaration-style rather than mutation tests. This slice removes that remaining product-quality weakness without editing p2-83 or old slices.

## Write Scope

Allowed write root:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-84-post-rehearsal-cockpit-mutation-hardening-sandbox/
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
- p2-83 source files
- Git commit, push, sync, hooks, background automation

## Acceptance Criteria

- Required slice files exist.
- A positive baseline copy of p2-83 cockpit passes mutation validation.
- Eight negative mutant fixtures are generated.
- All eight mutants fail validation for the expected reason.
- Local verifier passes.
- Reviewer returns REVIEW_PASS_NO_BLOCKER.
- Boundary Auditor returns PASS_BOUNDARY.
- GPT-5.5 extra-high Product Acceptance returns PASS_PRODUCT_GRADE.
- Final gate passes.

## Stop Conditions

Stop if any implementation requires modifying p2-83, old slices, mainline docs, wiki truth layers, templates, tools, Obsidian vault, or applying old-file normalization.
