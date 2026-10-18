---
slice_id: 2026-06-19-p2-72-original-slice-normalization-decision-packet-sandbox
status: planned
---

# Slice Plan

## Purpose

Create a sandbox-only decision packet and dry-run manifest for the original 20 slice status normalization choice.

## Why This Slice Now

p2-71 proved that the original 20 implementation slices have Product Acceptance evidence and core pass evidence, but none satisfy the later current strict final-gate convention. This slice packages the exact decision the user would need to make before any old slice status normalization can be performed.

## Write Scope

Only:

`outputs/review/vaks-implementation-sandbox/2026-06-19-p2-72-original-slice-normalization-decision-packet-sandbox/`

## Do Not Touch

- Any older sandbox slice.
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

## Pre-Start Git Status Summary

- Dirty tree is treated as pre-existing baseline.
- Pre-start `git status --short` line count observed for this slice: 254.
- Current p2-72 path did not exist before this slice.

## Acceptance Criteria

- Reads p2-71 audit as source.
- Produces a user-facing decision packet with allowed options.
- Produces a dry-run manifest listing proposed old-slice frontmatter status normalizations, without applying them.
- Explicitly states that user approval is not yet collected.
- Explicitly blocks mainline readiness, promotion, reviewed knowledge, evidence support, action basis, and Obsidian sync.
- Includes fixtures, failure cases, local verification, Reviewer report, Boundary audit, GPT-5.5 extra-high Product Acceptance, and next-step.

## Stop Conditions

Stop if completing this slice requires editing old slices, formal architecture docs, `templates/`, `tools/`, formal wiki layers, Obsidian vault, commit, push, sync, dependency install, background service, hook, MCP write tool, or treating this decision packet as actual user approval.
