---
type: sandbox_manifest
status: candidate_only
created_at: 2026-06-06
scope: Source Intake Control Flow sandbox package
truth_boundary: sandbox manifest only
---

# Manifest

## Source Design

```text
../2026-06-06-source-intake-control-flow-state-machine-candidate-design.md
```

## Protocol Files

| File | Purpose |
|---|---|
| `01_PROTOCOL.md` | Short lifecycle, four dimensions, transition rules. |
| `02_FIELD_CONTRACT.md` | Required / optional / forbidden fields for each record type. |
| `03_RETRIEVAL_BUCKET_POLICY.md` | Mode-based bucket filtering before hybrid / RRF. |
| `04_FEEDBACK_CACHE_PROTOCOL.md` | Append-only feedback event rules. |
| `05_PRO_ROUND2_STRENGTH_TEST.md` | Pro round-2 failure cases and strength matrix. |

## Fixtures

| Fixture | Expected status |
|---|---|
| `fixtures/source-card-light.md` | raw + light + no action basis |
| `fixtures/candidate-distillation-medium.md` | candidate + medium + orientation only |
| `fixtures/query-run-suggested-overlay-trace.md` | suggested overlay stays trace-only |
| `fixtures/confirmed-project-overlay.md` | confirmed project sidecar only |
| `fixtures/feedback-event-misleading-orientation.md` | feedback creates review pressure, no truth mutation |
| `fixtures/heavy-review-open-blocked.md` | heavy review open but blocked, not answer pool |
| `fixtures/action-facing-anchor-pass.md` | selector-grade raw/stable anchor shape |
| `fixtures/action-facing-anchor-fail-candidate-anchor.md` | expected block: candidate anchor as final support |
| `fixtures/archived-project-overlay.md` | archived overlay excluded from default retrieval |
| `fixtures/source-changed-blocked.md` | broken/changed source blocks action-facing use |

## Checks

| Check | Purpose |
|---|---|
| `checks/lint-matrix.md` | Minimal field / boundary expectations. |
| `checks/completion-audit.md` | Sandbox completion audit. |
| `checks/pressure-test-results.md` | Static pressure-test results and post-failure patch note. |
| `checks/pro-round2-strength-results.md` | Pro round-2 strength-test results and improvement verdict. |
| `checks/mainline-merge-audit.md` | Audit showing round1 and round2 design logic merged into SOURCE_INTAKE and templates. |

## Non-Goals

```text
mainline schema edit
SOURCE_INTAKE.md edit
automatic promotion
full W3C Annotation / PROV implementation
full toolchain implementation
```
