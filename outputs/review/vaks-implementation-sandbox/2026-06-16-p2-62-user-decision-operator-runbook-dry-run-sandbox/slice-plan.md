---
slice_id: 2026-06-16-p2-62-user-decision-operator-runbook-dry-run-sandbox
status: implementation_ready
---

# Slice Plan

## Purpose

Create a sandbox-only dry-run operator runbook that uses the p2-61 readiness
brief to decide which follow-up requests may continue as read-only inspection
and which requests must stop for separate explicit user approval.

## Why This Slice Comes Next

P2-61 made p2-60's checksum freeze readable. P2-62 turns that readable brief
into a small decision table that later agents can apply without confusing
read-only inspection with execution, promotion, merge, sync, reviewed knowledge,
evidence support, action basis, or user approval.

## Only Write Path

`outputs/review/vaks-implementation-sandbox/2026-06-16-p2-62-user-decision-operator-runbook-dry-run-sandbox/`

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

- read p2-61's readiness brief and report statuses;
- not execute p2-61 scripts;
- permit read-only inspection only;
- allow manual read-only drift verification as operator guidance only;
- stop execution, merge, promotion, sync, commit, push, reviewed knowledge,
  evidence support, action basis, and inferred user approval;
- keep all authority flags false.

## Acceptance Criteria

- Required slice files exist.
- JSON, Markdown, and HTML runbook dry-run artifacts are generated.
- Verifier passes on positive fixtures.
- Failure cases are rejected.
- Reviewer returns `REVIEW_PASS_NO_BLOCKER`.
- Boundary Auditor returns `PASS_BOUNDARY`.
- GPT-5.5 extra-high Product Acceptance returns `PASS_PRODUCT_GRADE`.
- Final gate passes.
- Path audit shows this slice wrote only the approved p2-62 sandbox path.

## Stop Conditions

Stop and ask the user if this slice needs protected file edits, Obsidian sync,
commit, push, dependency installation, background services, hooks, MCP write
tools, mainline promotion, or formal-vault execution.
