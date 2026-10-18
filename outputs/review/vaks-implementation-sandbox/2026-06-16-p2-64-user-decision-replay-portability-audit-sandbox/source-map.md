---
slice_id: 2026-06-16-p2-64-user-decision-replay-portability-audit-sandbox
status: source_mapped
---

# Source Map

## Primary Source Slice

`outputs/review/vaks-implementation-sandbox/2026-06-16-p2-63-user-decision-runbook-replay-regression-sandbox/`

## Read Inputs

- `artifact/user_decision_runbook_replay_regression.json`
- `artifact/build_user_decision_runbook_replay_regression.py`
- `artifact/verify_user_decision_runbook_replay_regression.py`
- `verification.md`
- `reviewer-report.md`
- `boundary-audit.md`
- `product-acceptance-report.md`
- `next-step.md`

## Current Slice Outputs

- `artifact/user_decision_replay_portability_audit_contract.json`
- `artifact/build_user_decision_replay_portability_audit.py`
- `artifact/verify_user_decision_replay_portability_audit.py`
- `artifact/user_decision_replay_portability_audit.json`
- `artifact/user_decision_replay_portability_audit.md`
- `artifact/user_decision_replay_portability_audit.html`
- `fixtures/dependency-portable.json`
- `fixtures/command-portable.json`
- `fixtures/path-portable.json`
- `failure-cases/user-decision-replay-portability-audit-failures.json`

## Source Boundaries

The audit reads p2-63 outputs and source files. It does not execute p2-63 builder, verifier, operator commands, user-decision options, shell commands, network calls, MCP tools, hooks, services, sync operations, commits, or pushes.

## Authority Boundaries

This source map is a locator and audit map only. It does not create reviewed knowledge, evidence support, action basis, mainline readiness, promotion readiness, Obsidian readiness, or user approval.
