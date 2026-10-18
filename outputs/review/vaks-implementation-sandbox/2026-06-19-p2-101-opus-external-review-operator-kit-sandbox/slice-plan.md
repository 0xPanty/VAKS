---
slice_id: 2026-06-19-p2-101-opus-external-review-operator-kit-sandbox
status: planned
---

# Slice Plan

## Goal

Create an operator kit for external Opus review submission and result intake.

## Why This Slice Now

p2-100 created a product-grade transfer ZIP. This slice makes the human/operator step explicit: what to verify before submission, what message to send with the ZIP, and how to retain the raw Opus response afterward without confusing the transfer package with approval.

## Write Scope

Only this path may be written:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-101-opus-external-review-operator-kit-sandbox/
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

- Generate an operator runbook for submitting p2-100 to external Opus.
- Generate an exact submission message that references the transfer ZIP and SHA256.
- Generate a result-intake template that follows p2-96 allowed conclusion tokens.
- Generate a control card linking p2-100 transfer evidence and p2-96 intake schema.
- Include fixtures and failure cases.
- Verify the transfer ZIP hash, required intake tokens, required boundaries, and final-gate statuses.
- Pass local verifier, Reviewer, Boundary Auditor, and GPT-5.5 Product Acceptance.

## Stop Conditions

- A real Opus result is needed.
- Any old slice or protected path would need modification.
- The kit would claim Opus approval, mainline readiness, reviewed knowledge, evidence support, action basis, or goal completion.
