---
type: sandbox_check
status: completed
created_at: 2026-06-05
scope: project-sidecar-to-v0-2-13-action-facing-escalation
truth_boundary: test report only; not reviewed knowledge; not action basis
---

# Action-Facing Escalation Check

## Scenario

Question under test:

```text
Should Misa allow a component-health diagnostic candidate to directly trigger a
repair path or route mutation when a repeated runtime-thread failure appears?
```

Relevant overlay entry:

```text
misa_overlay/MISA.md#entry-search-to-analysis-before-answer
```

Related candidates:

```text
retrieval-is-activation-not-truth
memory-granularity-and-quarantine
visual-workbench-for-retrieval-diagnostics
```

## Unsafe Shortcut

Bad path:

```text
Lens entry says component health is useful.
Component health diagnostic has a replay key.
Therefore Misa should let the sidecar start repair automatically.
```

Verdict:

```text
blocked
```

Reason:

```text
This treats overlay posture and diagnostic presence as action basis.
It skips the non-circular warrant.
```

## Required v0.2.13 Envelope

Action-facing claim:

```text
Misa should not let component-health diagnostic candidates auto-trigger repair
or route mutation; they should remain replay-required human-owner candidates.
```

Anchored evidence:

```text
docs/current/component-health-diagnostics-v0.29.md:
  diagnostics become replayable candidates for a human owner, not automatic fixes

scripts/lib/component-health.mjs:
  diagnostic candidates include auto_execute=false, human-owner delivery,
  replay_required=true, and no production/VPS/provider/memory authority

test/component-health.test.mjs:
  repeated failures become replayable diagnostic candidates only;
  control-plane write-deny drift is critical evidence;
  cooldown suppresses repeated diagnostics

docs/current/control-boundaries.md:
  LLMs must not decide route, setpoints, winner authority, persistent memory
  writes, skill publication, VPS updates, or production rollout
```

Non-circular warrant:

```text
The anchors all point to the same authority boundary: component health can
classify local degradation and open replayable diagnostic candidates, but the
consumer is the human owner and any repair must go through existing replay and
local-gate paths. Therefore the evidence supports keeping diagnostics as
candidate/control signals, not allowing automatic repair or route mutation.
```

Scope / assumptions:

```text
Scope is local Misa component-health and runtime-thread surfaces read in this
test. It does not cover future production services or uninspected scripts.
```

Known gaps / risks:

```text
Not every Misa command was inspected.
The test did not execute a real degraded production incident.
VPS update scripts were tested for order/pin behavior only, not deployed here.
```

Residual review status:

```text
sufficient_for_sandbox_boundary_test
not sufficient for production or VPS action
```

## Result

```text
Lens alone: insufficient
v0.2.13 gate: required and useful
relationship: complementary
```

The overlay helped locate the relevant Misa surfaces, but it did not carry the
warrant. That is the desired behavior.
