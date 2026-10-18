---
slice_id: 2026-06-19-p2-105-external-review-chain-readiness-preflight-sandbox
status: planned
---

# Slice Plan

## Goal

Create a single preflight cockpit for the external Opus review chain.

## Why This Slice Now

p2-100 through p2-104 are individually product-grade. This slice provides one auditable readiness view for the whole chain: transfer package, operator kit, result-intake validator, outcome action gate, and post-Opus user decision packet.

## Write Scope

Only this path may be written:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-105-external-review-chain-readiness-preflight-sandbox/
```

## Non-Write Scope

- No old slice edits.
- No root architecture document edits.
- No README edits.
- No wiki truth layer edits.
- No templates or tools edits.
- No Obsidian vault writes or sync.
- No commit, push, promotion, or mainline merge.
- No claim that Opus or the user has approved anything.

## Acceptance Criteria

- Read p2-100 through p2-104 as inputs.
- Confirm their final-gate evidence and product-grade statuses.
- Confirm the external Opus result is still absent.
- Confirm user approval and mainline readiness are still absent.
- Produce one cockpit, runbook, fixtures, failure cases, and verifier.
- Pass local verifier, Reviewer, Boundary Auditor, and GPT-5.5 Product Acceptance.

## Stop Conditions

- A real Opus result is needed.
- A real user approval is needed.
- Any old slice or protected path would need modification.
- The cockpit would claim goal completion, merge, promotion, reviewed knowledge, evidence support, or action basis.
