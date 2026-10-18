---
record_kind: sandbox_adapter_contract_test
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: diagnostic_not_mainline_decision
action_basis_allowed: false
---

# Phase B Adapter Contract Test

## Verdict

- contract status: pass
- error count: 0

## Sections

| Section | Rows | Errors |
|---|---:|---:|
| manifest:primary | 3991 | 0 |
| manifest:full | 18785 | 0 |
| main_receipts:primary | 300 | 0 |
| main_receipts:full | 300 | 0 |
| holdout_receipts:primary | 150 | 0 |
| holdout_receipts:full | 150 | 0 |

## Checks

- manifest required fields
- receipt required fields
- policy kind and policy booleans
- source and chunk hash shape
- click-back target existence and line range
- no action-basis permission leaks
- risky action/evidence results carry warnings
- risky rows cannot claim reviewed relation state

## Boundary

The contract test is diagnostic only. It does not approve mainline adoption, C-lite, Skills, MCP writes, subagents, formal writeback, or production readiness.
