---
slice_id: 2026-06-20-p2-109-obsidian-disposable-vault-absorption-pilot-sandbox
status: planned
---

# Slice Plan

## Goal

Run a sandbox-only absorption pilot for the seven highest-value VAKS guard candidates against a disposable Obsidian-style vault.

This slice tests whether the candidates can behave like future main-architecture lazy gates without writing to `tools/`, protected architecture files, wiki truth layers, templates, or the formal Obsidian vault.

## Candidate Guards

- P0-03 body hash validator
- P0-04 support boundary validator
- P0-05 action readiness validator
- P0-06 feedback validator
- P0-07 action-boundary failure matrix
- P1-08 retrieval/operation receipt validator
- P1-10 runtime artifact exclusion validator

## Write Scope

Only this sandbox path may be written:

`outputs/review/vaks-implementation-sandbox/2026-06-20-p2-109-obsidian-disposable-vault-absorption-pilot-sandbox/`

## Non-Goals

- No mainline merge.
- No `tools/` promotion.
- No `templates/` edit.
- No main architecture document edit.
- No wiki truth-layer write.
- No formal Obsidian vault write or sync.
- No commit, push, hook, or background service.

## Acceptance Criteria

- The runner creates a disposable Obsidian-style vault under this slice only.
- Positive vault samples pass.
- Contaminated vault samples fail with expected issue codes.
- The temporary vault is deleted after the run.
- The report preserves evidence without preserving the test vault samples.
- Local verifier and final gate pass.
- Reviewer, Boundary Auditor, and GPT-5.5 extra-high Product Acceptance pass.

## Stop Conditions

- Any required write would touch protected paths or the formal Obsidian vault.
- Any test sample must be retained outside this sandbox.
- Any result would need to be claimed as mainline integration, reviewed knowledge, evidence support, action basis, or Opus approval.
