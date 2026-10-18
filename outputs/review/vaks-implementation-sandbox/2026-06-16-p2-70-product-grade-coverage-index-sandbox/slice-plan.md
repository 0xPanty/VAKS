---
slice_id: 2026-06-16-p2-70-product-grade-coverage-index-sandbox
status: planned
---

# Slice Plan

## Purpose

Build a sandbox-only product-grade coverage index for the VAKS implementation sandbox.

This answers whether sandbox slices have current strict product-grade closeout evidence without treating chat memory, code literals, fixture strings, or legacy next-step text as acceptance.

## Why This Slice Now

The previous slice proved a future verifier can reuse the p2-67 strict status package. The next operational gap is coverage clarity: the user asked whether all landed points are tested, positive improvements, and product grade.

## Write Scope

Only:

`outputs/review/vaks-implementation-sandbox/2026-06-16-p2-70-product-grade-coverage-index-sandbox/`

## Do Not Touch

- `SCHEMA.md`
- `ARCHITECTURE_PRINCIPLES.md`
- `FUSION_ARCHITECTURE_V0_2_DRAFT.md`
- `README.md`
- `wiki/claims/`
- `wiki/patterns/`
- `wiki/decisions/`
- `templates/`
- `tools/`
- Obsidian vault
- older sandbox slices

## Pre-Start Git Status Summary

- Dirty tree is treated as pre-existing baseline.
- Pre-start `git status --short` line count observed for this slice: 254.
- Current p2-70 path did not exist before this slice.

## Acceptance Criteria

- Generates a coverage index from actual sandbox report files.
- Distinguishes report frontmatter statuses from code/fixture/body literals.
- Maps the original P0/P1/P1.5/P2 plan items to discovered sandbox slices.
- Separates canonical strict pass, legacy pass variants, pending closeout, and missing evidence.
- Includes positive fixtures, failure cases, local verification, Reviewer report, Boundary audit, GPT-5.5 extra-high Product Acceptance, and next step.

## Stop Conditions

Stop if the slice requires editing older slices, formal architecture docs, `templates/`, `tools/`, formal wiki knowledge layers, Obsidian vault, commit, push, sync, dependency install, background service, hook, or MCP write tool.
