---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p1-09-read-only-query-loop-pilot-sandbox
status: implemented_pending_review
truth_boundary: sandbox_source_map_only
---

# Source Map

## Governing User Boundary

- Writes are restricted to this sandbox path.
- Protected paths and Obsidian vault remain untouched.
- No commit, push, Obsidian sync, long-running automation, background service,
  MCP write tool, hook, or dependency install.
- Current dirty tree is pre-existing baseline; final audit checks only this
  slice's write path.

## Local Project Sources Read

| Source | Used For |
|---|---|
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md:2273-2296` | P1 target and six pilot stories. |
| `outputs/review/vaks-implementation-sandbox/2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox/product-acceptance-report.md` | Confirms P1-08 `PASS_PRODUCT_GRADE` and P1-09 entry. |
| `outputs/review/vaks-implementation-sandbox/2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox/artifact/receipt_validator_pilot.py` | Reused as the sandbox receipt validator for generated receipts. |
| `outputs/review/vaks-implementation-sandbox/2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox/artifact/validator-contract.md` | Receipt input/output contract and issue codes. |
| `SOURCE_INTAKE.md` | Action-facing anchors, retrieval rank not trust, candidate/overlay/feedback not final support. |
| `DEV_CONTEXT.md` | Retrieval receipts and context packs are not action basis by themselves. |
| `FEEDBACK.md` | Feedback can create review pressure/review_due but cannot mutate truth. |
| `REVIEW_QUEUE.md` | Decision/action basis requires reviewed source-backed basis, risk, rollback, evidence sufficiency; no automatic promotion/support. |

## Implemented P1 Stories

| Story | Positive Fixture | Boundary |
|---|---|---|
| Ordinary question | `fixtures/ordinary-orientation-answer.md` | Orientation answer does not require full audit. |
| Action-adjacent question | `fixtures/action-adjacent-gated-answer.md` | Context pack, support check, and action readiness check are required; action basis is not claimed. |
| Candidate temptation | `fixtures/candidate-temptation-blocked.md` | Candidate remains review input, not support/action basis. |
| Stale decision | `fixtures/stale-decision-historical-only.md` | Historical explanation allowed; ready action blocked. |
| Feedback correction | `fixtures/feedback-correction-review-due.md` | Emits sandbox review_due envelope; truth unchanged. |
| Agent propose write | `fixtures/agent-propose-write-operation-receipt.md` | Operation receipt required; proposal-only; no reviewed write. |

## Dependency Boundary

This slice calls the P1-08 sandbox receipt validator by local path. That is a
sandbox-to-sandbox reuse of a product-accepted artifact, not a mainline `tools/`
promotion.

## Non-Authority Note

This source map explains the sandbox prototype. It is not reviewed knowledge,
evidence support, reviewer approval, action basis, or a mainline implementation
decision.
