---
slice_id: 2026-06-19-p2-85-exact-approval-classifier-hardening-sandbox
status: planned
---

# Slice Plan

## Goal

Create a sandbox-only exact approval classifier hardening package for the p2-75 old-file status-only normalization approval phrase.

## Why This Slice Now

The remaining critical path is not technical execution; it is user approval integrity. p2-75 defines the exact approval phrase and p2-77 keeps generic continuation blocked. This slice turns that boundary into a reusable executable classifier with positive and negative fixtures.

## Write Scope

Allowed write root:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-85-exact-approval-classifier-hardening-sandbox/
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
- p2-75 / p2-77 / p2-83 / p2-84 source files
- Git commit, push, sync, hooks, background automation

## Acceptance Criteria

- Required slice files exist.
- The exact p2-75 phrase is read from p2-75, not retyped as authority.
- Only the exact phrase fixture classifies as approval.
- Negative fixtures cover generic Chinese continuation, generic English continuation, paraphrase, partial phrase, wrong count, missing prohibitions, extra authority, and whitespace/case variation.
- Classifier pass is explicitly not user approval collected by this slice.
- Local verifier passes.
- Reviewer returns REVIEW_PASS_NO_BLOCKER.
- Boundary Auditor returns PASS_BOUNDARY.
- GPT-5.5 extra-high Product Acceptance returns PASS_PRODUCT_GRADE.
- Final gate passes.

## Stop Conditions

Stop if this slice would require editing p2-75, p2-77, old slices, mainline docs, wiki truth layers, templates, tools, Obsidian vault, or applying old-file normalization.
