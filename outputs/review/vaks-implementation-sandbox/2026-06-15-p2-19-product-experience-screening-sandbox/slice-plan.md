---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p2-19-product-experience-screening-sandbox
status: in_progress
truth_boundary: sandbox_plan_only
---

# Slice Plan

## Opening Card

Slice id:

```text
2026-06-15-p2-19-product-experience-screening-sandbox
```

Why this slice now:

- P2-18 returned `PASS_PRODUCT_GRADE`.
- The architecture plan orders P2 after use-surface optimization and Bases
  cockpit as product experience screening before product workflow.
- This slice turns P2-PX-01 through P2-PX-15 into a screened, ranked, reusable
  sandbox backlog for P2-20 without building production UI.

Allowed write path:

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p2-19-product-experience-screening-sandbox/
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
real .base creation
production UI build
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

- Create product-experience screening contract.
- Create ranked backlog prototype covering all 15 P2-PX candidates.
- Create validator and verification runner.
- Create positive fixture and failure-case oracle.
- Verify that every candidate has keep / park / reject, required validators,
  target layer, boundary warning, source inspiration, and minimal wireflow.
- Run Reviewer, Boundary Auditor, and GPT-5.5 reasoning=xhigh Product
  Acceptance.

## Acceptance Criteria

- All required slice files exist.
- The prototype covers P2-PX-01 through P2-PX-15 exactly once.
- Screening output includes `keep / park / reject`, required validators, target
  layer, boundary warning, source inspiration, and minimal wireflow.
- No product surface can approve, promote, mutate truth, infer action readiness,
  create evidence support, create reviewed relations, or replace validators.
- No real UI, real Bases, dependency install, runtime, sync, MCP write, commit,
  or push is introduced.
- Local verification passes.
- Reviewer returns `REVIEW_PASS`.
- Boundary Auditor returns `BOUNDARY_PASS`.
- GPT-5.5 reasoning=xhigh Product Acceptance returns `PASS_PRODUCT_GRADE`.

## Stop Conditions

- A required product-screening artifact needs writes outside the allowed
  sandbox path.
- A candidate requires production UI, real Bases, dependency install, sync,
  MCP write, background service, commit, push, or a protected-path edit.
- Reviewer, Boundary Auditor, or Product Acceptance returns a blocking result.

## Non-Claims

This plan does not approve any product feature build, UI release, real Obsidian
Base, reviewed knowledge, evidence support, action basis, promotion, commit,
push, or Obsidian sync.
