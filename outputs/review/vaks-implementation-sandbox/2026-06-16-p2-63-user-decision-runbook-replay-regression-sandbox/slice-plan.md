---
slice_id: 2026-06-16-p2-63-user-decision-runbook-replay-regression-sandbox
status: implementation_ready
---

# Slice Plan

## Purpose

Create a sandbox-only natural-language replay regression for p2-62's operator
runbook. The replay checks that follow-up-agent prompts route to read-only
inspection or stop-and-ask-user without authority confusion.

## Why This Slice Comes Next

P2-62 made a structured runbook decision table. P2-63 tests realistic prompt
wording against that table so later agents cannot bypass boundaries with
ambiguous natural-language requests.

## Only Write Path

`outputs/review/vaks-implementation-sandbox/2026-06-16-p2-63-user-decision-runbook-replay-regression-sandbox/`

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

- read p2-62's runbook and status reports;
- not execute p2-62 scripts;
- replay natural-language prompts deterministically;
- preserve p2-62's allow/stop decisions;
- reject any replay that permits execution, merge, promotion, sync, commit,
  push, reviewed knowledge, evidence support, action basis, or inferred user
  approval.

## Acceptance Criteria

- Required slice files exist.
- JSON, Markdown, and HTML replay artifacts are generated.
- Verifier passes on positive fixtures.
- Failure cases are rejected.
- Reviewer returns `REVIEW_PASS_NO_BLOCKER`.
- Boundary Auditor returns `PASS_BOUNDARY`.
- GPT-5.5 extra-high Product Acceptance returns `PASS_PRODUCT_GRADE`.
- Final gate passes.
- Path audit shows this slice wrote only the approved p2-63 sandbox path.

## Stop Conditions

Stop and ask the user if this slice needs protected file edits, Obsidian sync,
commit, push, dependency installation, background services, hooks, MCP write
tools, mainline promotion, or formal-vault execution.
