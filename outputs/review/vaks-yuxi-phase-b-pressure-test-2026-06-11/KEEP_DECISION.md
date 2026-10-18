---
record_kind: sandbox_keep_decision
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: sandbox_decision_not_mainline_adoption
action_basis_allowed: false
---

# Phase B Keep Decision

## Decision

Keep Phase B as a sandbox candidate.

Do not promote it to mainline yet.

## Why

The bucket-local Phase B mode showed clear positive value:

```text
primary hit@5:
  baseline: 27/30
  VAKS+B bucket-local: 30/30
  Yuxi-native profile: 29/30

full noisy hit@5:
  baseline: 27/30
  VAKS+B bucket-local: 30/30
  Yuxi-native profile: 28/30
```

Governance result:

```text
action leakage:
  baseline: 1.0000
  VAKS+B bucket-local: 0.0000
  Yuxi-native profile: 1.0000
```

Operational coverage:

```text
VAKS+B bucket-local:
  click-back: 1.0000
  source/chunk hash: 1.0000
  adapter fields: 1.0000
  retrieval receipt: 1.0000
  stale-index detection: 1.0000
```

## What Passed

- Parser/chunk/index style retrieval improved recall.
- Bucket-local ordering prevented authority collapse.
- Adapter labels and warnings were visible.
- Source/chunk hashes and click-back anchors were present.
- Stale index simulation was detected by the VAKS+B adapter.

## What Did Not Pass

Yuxi-like retrieval without bucket-local authority ordering is not enough.

It had strong retrieval, but still allowed risky candidate/diagnostic material to occupy top rank in action/evidence questions.

## Boundary

This decision only supports:

```text
Phase B sandbox continuation
```

It does not approve:

```text
C-lite
Skills
MCP write tools
subagents
formal writeback
mainline adoption
production readiness
```

