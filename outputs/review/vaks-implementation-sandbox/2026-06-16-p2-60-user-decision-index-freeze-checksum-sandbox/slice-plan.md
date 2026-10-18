---
slice_id: 2026-06-16-p2-60-user-decision-index-freeze-checksum-sandbox
status: implementation_ready
---

# Slice Plan

## Purpose

Create a sandbox-only checksum freeze for the p2-51 through p2-59 user-decision
guard artifacts. The freeze lets a later agent detect whether the operator
handoff chain drifted before using it as a next-slice input.

## Why This Slice Comes Next

P2-59 made an operator handoff index over the user-decision guard chain. The
next useful hardening step is to freeze the actual source files behind that
index with byte-level SHA256 checksums. That gives later work a fast drift
detector before it trusts the handoff index shape.

## Only Write Path

`outputs/review/vaks-implementation-sandbox/2026-06-16-p2-60-user-decision-index-freeze-checksum-sandbox/`

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

## Artifact Contract

The artifact must:

- recompute SHA256 and byte sizes for required root docs plus artifact,
  fixtures, and failure-cases files from p2-51 through p2-59;
- record whether the latest source final gate, p2-59, still passes;
- reject drift in path, hash, bytes, source list, readiness flags, and
  boundary terms;
- keep all authority flags false.

## Acceptance Criteria

- Required slice files exist.
- Manifest is generated from live source files.
- Verifier passes on positive fixtures.
- Failure cases are rejected by the verifier.
- Reviewer returns `REVIEW_PASS_NO_BLOCKER`.
- Boundary Auditor returns `PASS_BOUNDARY`.
- GPT-5.5 extra-high Product Acceptance returns `PASS_PRODUCT_GRADE`.
- Final gate passes.
- Git/path audit shows this slice wrote only its sandbox path.

## Stop Conditions

Stop and ask the user if the slice needs protected file edits, Obsidian sync,
commit, push, dependency installation, background service, MCP write tool,
mainline promotion, or formal-vault execution.
