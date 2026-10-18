---
type: sandbox_check
status: completed
created_at: 2026-06-05
scope: misa-second-project-anchor-evidence
truth_boundary: test report only; not reviewed knowledge; not action basis
---

# Misa Anchor And Test Evidence

## Anchor Count

From `misa_overlay/MISA.md`:

```text
entries: 11
healthy anchors: 17
conceptual anchors: 0
not_checked anchors: 9
unanchored anchors: 1
```

The single unanchored entry is intentional and is routed to delete+tombstone.

## Concrete Anchor Examples

```text
scripts/lib/runtime-thread.mjs::SAFETY
scripts/lib/runtime-thread.mjs::determineNextStep
scripts/lib/component-health.mjs::buildComponentHealthDiagnostics
scripts/lib/component-health.mjs::diagnosticCandidateForComponent
scripts/lib/perception-sidecar.mjs::buildPerceptionDigest
scripts/lib/factor-candidate-reducer.mjs
docs/current/runtime-thread-v0.28.md
docs/current/component-health-diagnostics-v0.29.md
docs/current/control-boundaries.md
test/v028-runtime-thread.test.mjs
test/component-health.test.mjs
test/sidecar-status.test.mjs
test/vps-shadow-deploy.test.mjs
```

## Misa Test Run

Command run from:

```text
C:\Users\Administrator\Documents\New project\misa-cybernetic-evolution
```

Command:

```powershell
node --test --test-concurrency=1 test/v028-runtime-thread.test.mjs test/component-health.test.mjs test/sidecar-status.test.mjs test/vps-shadow-deploy.test.mjs
```

Result:

```text
tests: 25
pass: 25
fail: 0
duration_ms: 5548.0188
```

## What The Tests Prove For This Sandbox

They prove Misa is a strong second-project sample:

- Runtime thread pauses for human escalation and fails closed.
- Runtime thread local gate remains no-effect.
- Component health diagnostics are replayable candidates only.
- Sidecar status exposes safe mode without mutation authority.
- VPS shadow scripts are covered by tests that check ordering and commit pin behavior.

They do not prove the VAKS sidecar overlay should be mainlined. They only prove
the Misa targets are real enough for pressure testing.
