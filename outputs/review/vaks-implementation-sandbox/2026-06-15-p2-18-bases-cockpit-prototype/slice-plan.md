---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p2-18-bases-cockpit-prototype
status: implemented_pending_review
truth_boundary: sandbox_plan_only
---

# Slice Plan

## Scope

Build a sandbox-only Bases cockpit prototype for VAKS.

This slice proves the four planned Bases-style cockpit surfaces can be described
and validated without creating real Obsidian Bases files:

- `review-candidates.base` for review queue visibility;
- `context-packs.base` for context/action visibility;
- `feedback-events.base` for feedback pressure visibility;
- `operator-cockpit.base` for total operator status visibility.

## Approved Write Path

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p2-18-bases-cockpit-prototype/
```

## Non-Goals

- Do not create, modify, or sync real `.base` files.
- Do not write templates, tools, raw records, reviewed claims, reviewed
  patterns, decisions, main architecture docs, or the Obsidian vault.
- Do not create reviewed knowledge, evidence support, action basis, promotion,
  approval, mainline readiness, commit, push, or sync.
- Do not start a server, background service, hook, watcher, MCP tool,
  automation, or dependency installation.

## Artifacts

- `artifact/bases_cockpit_validator.py`
- `artifact/verify_bases_cockpit_prototype.py`
- `artifact/bases-cockpit-contract.md`
- `artifact/failure-case-oracle.md`
- `prototype/bases-cockpit-prototype.json`
- `fixtures/**`
- `failure-cases/*.json`

## Acceptance Criteria

- Positive fixtures cover all four bases, cross-cockpit navigation, key columns,
  status flags, and non-authority boundaries.
- Failure cases cover approval, reviewed write, promotion, action-basis
  confusion, context-pack ready inference, feedback truth mutation, dirty/hash
  authority confusion, activity-as-confidence, replacement of validators,
  missing columns, protected paths, real Bases write, sync, MCP write, runtime,
  hooks, background service, dependency install, commit, and push.
- Verification runs with `python -B` and leaves no target `__pycache__`.
- Reviewer finds no blocker.
- Boundary Auditor finds no VAKS boundary violation.
- GPT-5.5 xhigh Product Acceptance returns `PASS_PRODUCT_GRADE`.

## Stop Conditions

Stop and ask the user if this slice needs:

- writes outside the approved sandbox path;
- protected-path edits;
- real Obsidian Bases files;
- dependency installation;
- real UI/server/runtime execution;
- Obsidian sync/export;
- MCP write tools;
- background service, watcher, automation, or hooks;
- commit or push;
- Product Acceptance returns `BLOCKED_NEEDS_USER`.
