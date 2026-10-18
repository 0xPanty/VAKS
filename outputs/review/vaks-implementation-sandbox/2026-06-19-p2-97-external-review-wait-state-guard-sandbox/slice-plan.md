---
slice_id: 2026-06-19-p2-97-external-review-wait-state-guard-sandbox
status: planned
---

# Slice Plan

## Goal

Create a machine-verifiable wait-state guard that prevents future agents from mistaking product-grade sandbox closeout for Opus approval or mainline readiness.

## Why This Slice Now

p2-96 prepared Opus result intake, but no actual Opus result exists. This slice turns the waiting state into an explicit guard: stop before merge, stop before truth/action claims, and wait for valid external Opus intake.

## Write Scope

Only this path may be written:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-97-external-review-wait-state-guard-sandbox/
```

## Non-Write Scope

- No old slice edits.
- No root architecture document edits.
- No README edits.
- No wiki truth layer edits.
- No templates or tools edits.
- No Obsidian vault writes or sync.
- No commit, push, promotion, or mainline merge.
- No claim that Opus has approved anything.

## Acceptance Criteria

- Produce a STOP/WAIT guard artifact.
- Produce a no-merge checklist.
- Verify p2-96 still says actual Opus result is absent.
- Verify p2-95 still says goal complete is false.
- Verify mainline/truth/action/commit/push/sync readiness are false.
- Include fixtures and failure cases.
- Pass local verifier, Reviewer, Boundary Auditor, and GPT-5.5 Product Acceptance.

## Stop Conditions

- The guard would need to claim Opus approval or goal completion.
- The guard would need to write outside its sandbox.
- Reviewer, Boundary Auditor, or Product Acceptance returns a blocking result.

