---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p2-20-product-workflow-prototype
status: in_progress
truth_boundary: sandbox_plan_only
---

# Slice Plan

## Opening Card

Slice id:

```text
2026-06-15-p2-20-product-workflow-prototype
```

Why this slice now:

- P2-19 returned `PASS_PRODUCT_GRADE`.
- The architecture plan orders P2 product workflow after product experience
  screening.
- This slice converts P2-19 kept product surfaces into a sandbox-only workflow
  prototype that later agents can inspect, validate, and reuse.

Allowed write path:

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p2-20-product-workflow-prototype/
```

Protected paths not touched:

```text
SCHEMA.md
ARCHITECTURE_PRINCIPLES.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
README.md
wiki/claims/
wiki/patterns/
wiki/decisions/
templates/
tools/
H:/Obsidian/
```

Forbidden actions:

```text
commit
push
Obsidian sync
promotion
production UI
real .base files
runtime/server/background service
dependency install
MCP write tool
hooks
long-running automation
```

## Baseline

Start-of-slice status:

```text
git status --short count: 253
target path existed before slice: False
target path status before slice: empty / missing path warning only
```

Dirty tree outside this target path is treated as pre-existing baseline by user
instruction. Final audit only attributes writes inside this slice path.

## Work Items

- Create workflow contract.
- Create sandbox-only workflow prototype using P2-19 kept candidates.
- Create validator and verification runner.
- Create positive fixture and independent failure-case oracle.
- Cover boundary failures for production UI, real Bases, authority confusion,
  missing workflow steps, missing receipts, and incomplete gates.
- Run Reviewer, Boundary Auditor, and GPT-5.5 reasoning=xhigh Product
  Acceptance.

## Acceptance Criteria

- Required slice files exist.
- Workflow prototype covers the kept P2-19 candidates:
  - capability / boundary;
  - onboarding;
  - home / operator status;
  - layer badge;
  - quick capture;
  - candidate funnel;
  - review due;
  - context / evidence export;
  - sync + hash receipt view;
  - dirty-state guardrail.
- Every workflow step has input, output, required validators, blocking states,
  boundary copy, and non-authority flags.
- Workflow explicitly answers:
  - where do I put this?
  - what state is it in?
  - can I use it for orientation, review input, or action?
  - what blocks promotion/action?
  - what source/hash/receipt proves authority did not silently mutate?
- Local verification passes.
- Reviewer returns `REVIEW_PASS`.
- Boundary Auditor returns `BOUNDARY_PASS`.
- GPT-5.5 reasoning=xhigh Product Acceptance returns `PASS_PRODUCT_GRADE`.

## Stop Conditions

- Workflow requires writes outside this sandbox path.
- Workflow requires production UI, real Bases, runtime, sync, dependency install,
  MCP write tools, commit, push, or protected-path edits.
- Reviewer, Boundary Auditor, or Product Acceptance returns a blocking result.

## Non-Claims

This plan does not approve production UI, real Bases, reviewed knowledge,
evidence support, action basis, promotion, commit, push, or Obsidian sync.
