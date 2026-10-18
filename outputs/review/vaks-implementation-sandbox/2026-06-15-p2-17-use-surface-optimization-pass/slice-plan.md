---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p2-17-use-surface-optimization-pass
status: implemented_pending_review
truth_boundary: sandbox_plan_only
---

# Slice Plan

## Scope

Build a sandbox-only use-surface optimization pass for VAKS.

This slice proves that a product-facing operator surface can make strict VAKS
flows easier to use without weakening boundaries:

- one entry surface for capture, process, ask, check, context-pack, review,
  feedback, and act-adjacent work;
- short status surfaces before long manuals;
- receipt-backed search and action-mode guardrails;
- clear layer badges that display state but do not promote;
- worktree, hash, receipt, and dirty-state visibility as operator state only.

## Approved Write Path

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p2-17-use-surface-optimization-pass/
```

## Non-Goals

- Do not build or modify the real Obsidian Bases cockpit.
- Do not modify main architecture docs, templates, tools, raw records, reviewed
  claims, reviewed patterns, decisions, or the Obsidian vault.
- Do not create reviewed knowledge, evidence support, action basis, promotion,
  mainline readiness, commit, push, or sync.
- Do not start a server, background service, hook, MCP tool, automation, or
  dependency installation.

## Artifacts

- `artifact/use_surface_optimizer.py`
- `artifact/verify_use_surface_optimization_pass.py`
- `artifact/use-surface-contract.md`
- `artifact/failure-case-oracle.md`
- `prototype/operator-use-surface-blueprint.json`
- `fixtures/**`
- `failure-cases/*.json`

## Acceptance Criteria

- Positive fixtures cover the entry matrix, status/navigation layer, receipt
  search, layer badges, and dirty-state guardrail.
- Failure cases cover approval confusion, reviewed-write confusion, promotion,
  action-basis confusion, raw top-k trust, selected_by-as-support, missing
  receipts, missing action gates, badge promotion, dirty-state-as-truth,
  hash-as-support, sync authority confusion, protected paths, and mainline
  readiness.
- Verification runs with `python -B` and leaves no target `__pycache__`.
- Reviewer finds no blocker.
- Boundary Auditor finds no VAKS boundary violation.
- GPT-5.5 xhigh Product Acceptance returns `PASS_PRODUCT_GRADE`.

## Stop Conditions

Stop and ask the user if this slice needs:

- writes outside the approved sandbox path;
- protected-path edits;
- dependency installation;
- real UI deployment, server, watcher, MCP write tool, hook, automation, or
  Obsidian sync;
- commit or push;
- Product Acceptance returns `BLOCKED_NEEDS_USER`.
