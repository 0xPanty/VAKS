---
record_kind: sandbox_iteration_decision
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: diagnostic_not_mainline_decision
action_basis_allowed: false
---

# Phase B Contract Test Decision

## Decision

Keep the adapter skeleton after contract hardening.

Do not promote it to mainline yet.

## What Changed

The previous skeleton tied v1.1 on retrieval metrics and emitted manifest /
receipt artifacts, but the first contract test exposed real structure issues:

```text
contract status: fail
error count: 5569
```

The adapter output was then fixed:

- click-back line ranges are clamped to existing source file line counts
- manifest rows include warning codes for raw / candidate / diagnostic / overlay / feedback buckets
- receipt rows include `indexed_source_hash`

After the fix:

```text
contract status: pass
error count: 0
```

## Contract Coverage

Validated:

```text
manifest required fields
receipt required fields
policy kind and policy booleans
source and chunk hash shape
click-back target existence and line range
no action-basis permission leaks
risky action/evidence results carry warnings
risky rows cannot claim reviewed relation state
```

Validated rows:

| Section | Rows | Errors |
|---|---:|---:|
| manifest:primary | 3991 | 0 |
| manifest:full | 18785 | 0 |
| main_receipts:primary | 300 | 0 |
| main_receipts:full | 300 | 0 |
| holdout_receipts:primary | 150 | 0 |
| holdout_receipts:full | 150 | 0 |

## Metric Comparison

The contract hardening preserves the previous skeleton metrics:

```text
main primary:
  hit@5: 30/30
  MRR:   1.0000
  leakage: 0.0000

main full:
  hit@5: 30/30
  MRR:   1.0000
  leakage: 0.0000

holdout primary:
  hit@5: 12/15
  MRR:   0.7811
  leakage: 0.0000

holdout full:
  hit@5: 13/15
  MRR:   0.7591
  leakage: 0.0000
```

## Why This Is Positive

This iteration did not improve ranking score. It improved implementation
readiness:

```text
same retrieval quality
+ same zero leakage
+ contract validator passes
+ click-back and warning defects fixed
```

That is a positive step because Phase B now has a tested structural boundary,
not only good retrieval numbers.

## Boundary

This decision supports:

```text
continue Phase B sandbox from the contract-passing adapter skeleton
```

It does not approve:

```text
mainline adoption
C-lite
Skills
MCP writes
subagents
formal writeback
production readiness
```

## Next Step

Next step should be a small "integration readiness" package:

```text
adapter API shape
input / output contract
failure modes
mainline insertion point
rollback path
same pressure metrics
same contract test
```

It may continue only if it keeps the contract pass and does not regress from
the current skeleton metrics.
