---
type: sandbox_findings
status: in_progress
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: seven-project-sidecar-candidates-full-pressure-test
truth_boundary: findings log only; not reviewed knowledge; not action basis
---

# Findings

## Starting State

- Current repo branch: `master`.
- Current latest local commit: `e19a3c6 docs: land v0.2.13 action gate and sidecar boundary`.
- Staging area: empty at start.
- Known dirty tracked files: `AGENTS.md`, `00_handoff/2026-06-04-audit-shell-v1-formal-graduation-handoff.md`.
- Many pre-existing untracked `outputs/review`, `raw`, `tools`, and `wiki/summaries` files exist. They are not cleanup targets.

## Misa Sample Anchor Findings

Misa path:

```text
C:\Users\Administrator\Documents\New project\misa-cybernetic-evolution
```

Initial suitability signal:

- Has concrete docs: `README.md`, `ARCHITECTURE.md`, `CONTROL_CONTRACT.md`, `GOVERNANCE.md`, `docs/current/*`.
- Has concrete modules: `scripts/lib/runtime-thread.mjs`, `scripts/lib/component-health.mjs`, `scripts/lib/factor-candidate-reducer.mjs`, `scripts/lib/perception-sidecar.mjs`.
- Has concrete schemas: `schemas/control_contract.schema.json`, `schemas/sidecar-status.schema.json`, `schemas/component_health_diagnostics.schema.json`.
- Has concrete tests: `test/runtime-thread.test.mjs`, `test/component-health.test.mjs`, `test/sidecar-status.test.mjs`, `test/vps-shadow-deploy.test.mjs`.
- Has strong boundaries: `production_authority=false`, no VPS touch by default, no provider calls in control path, human owner for execution/rollout.

Concrete anchor evidence:

- `docs/current/runtime-thread-v0.28.md`: runtime thread records launch/pause/resume/next local step; it must not execute work orders, call providers/APIs, write memory, start services, touch VPS, or change authority.
- `scripts/lib/runtime-thread.mjs`: exports deterministic `determineNextStep`, replay, local-gate, and fail-closed error handling; `SAFETY` keeps execution, provider calls, external APIs, memory writes, services, and VPS touch false.
- `test/v028-runtime-thread.test.mjs`: asserts pause for human escalation, local-gate after human decision, deterministic replay, fail-closed runtime errors, and no provider/API/VPS authority.
- `docs/current/component-health-diagnostics-v0.29.md`: health is a pure deterministic reducer; diagnostics are replayable candidates for human owner, not automatic fixes.
- `scripts/lib/component-health.mjs`: diagnostic candidates carry `auto_execute=false`, human-owner delivery, replay-required fingerprints, and no production/VPS/provider/memory authority.
- `test/component-health.test.mjs`: asserts positive feedback without diagnostics for healthy checks, repeated failures become replayable diagnostic candidates only, control-plane write-deny drift is critical evidence, and cooldown suppresses repeated diagnostics.
- `docs/current/control-boundaries.md`: LLMs must not decide route, metrics, setpoints, winner authority, persistent memory writes, skill publication, VPS updates, or production rollout.
- `scripts/lib/perception-sidecar.mjs`: perception digest output uses `authority: hint_only`, `shadow_only=true`, and blocked effects for memory, Zilliz, embedding, skill installation, public publish, route changes, winner changes, and service starts.

## Candidate Pattern Fit Signals

- `retrieval-is-activation-not-truth` maps strongly to Misa vector retrieval, perception digest, runtime adapter candidate pressure, and no-authority boundaries.
- `memory-granularity-and-quarantine` maps strongly to Misa memory candidate quarantine and no persistent memory writes.
- `file-first-agent-workbench` maps to file-visible docs/schemas/tests/scripts and local shadow artifacts.
- `simple-first-retrieval-baseline` maps to Misa's local deterministic commands and vector ranker being support, not authority.

## Open Risks

- If most Misa target hints stay conceptual, Misa fails the phase-2 sample requirement.
- If `landed_snapshot` is self-referential, it does not prove cross-project value.
- If the sandbox mainline copy reads like a real architecture mandate, the seven-candidate bundle fails mainline-readiness.

## Quant Findings

- Sandbox mainline insertion size:
  - `ARCHITECTURE_PRINCIPLES.md`: +131 / -0
  - `FUSION_ARCHITECTURE_V0_2_DRAFT.md`: +15 / -0
- Misa overlay:
  - entries: 11
  - healthy anchors: 17
  - not_checked anchors: 9
  - unanchored anchors: 1, intentionally routed to tombstone
- Selected Misa tests:
  - 25 passed
  - 0 failed
- Pressure matrix:
  - average sandbox usefulness: 2.57 / 3
  - average mainline readiness: 0.71 / 3
  - average leakage risk: 2.43 / 3
  - average maintenance gain: 2.57 / 3

Interim interpretation:

```text
useful enough to keep testing in sandbox
not ready as mainline object model
```

## Tool / Read Errors

- Attempted to read `test/runtime-thread.test.mjs`; actual filename is `test/v028-runtime-thread.test.mjs`. Resolved by reading the correct file.
