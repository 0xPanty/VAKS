---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p1-09-read-only-query-loop-pilot-sandbox
status: implemented_pending_review
truth_boundary: sandbox_plan_only
---

# Slice Plan

## Slice ID

`2026-06-15-p1-09-read-only-query-loop-pilot-sandbox`

## Why This Slice Comes First

P1-08 received `PASS_PRODUCT_GRADE`. The architecture upgrade plan orders the
next P1 implementation as the read-only query loop pilot. This slice proves that
a query loop can honor P0/P1 receipt and authority boundaries under the six P1
pilot stories before runtime artifact exclusion, semantic anchor checks, or RAG
enhancement slices are attempted.

## Opening Baseline

Opened from a pre-existing dirty tree.

```text
git status --short count before this slice: 253
target path existed before this slice: false
git status for target path before this slice: empty
```

The dirty tree is treated as pre-existing baseline per user instruction. Final
audit for this slice checks only whether new or modified files from this slice
are strictly inside the approved sandbox path.

## Only Write Path

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p1-09-read-only-query-loop-pilot-sandbox/
```

## Paths Not To Modify

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
H:\Obsidian\资料库
```

## Actions Not To Perform

```text
commit
push
Obsidian sync
promotion
long-running automation
background service
MCP write tool
hooks
dependency install
mainline validator/tool promotion
```

## Artifact Shape

- `artifact/read_only_query_loop_pilot.py`: sandbox-only query-loop state
  machine that consumes flat scenario frontmatter.
- `artifact/verify_read_only_query_loop_pilot.py`: suite runner for all
  fixtures and failure cases.
- `artifact/scenario-contract.md`: input/output contract and issue codes.
- `artifact/failure-case-oracle.md`: expected failure mapping.
- `fixtures/`: six positive P1 pilot stories.
- `failure-cases/`: boundary and receipt-invalid negative scenarios.

## Acceptance Criteria

- Ordinary question returns orientation without requiring full audit.
- Action-adjacent question requires context pack, support check, and action
  readiness check, while not claiming action basis.
- Candidate temptation is kept as review input/orientation and cannot support
  action.
- Stale decision can explain history but cannot produce ready action.
- Feedback correction emits a review_due envelope while truth remains unchanged.
- Agent propose-write requires a valid operation receipt and performs no write.
- Generated retrieval and operation receipts are validated through the P1-08
  sandbox receipt validator.
- Positive fixtures and failure cases pass local verification.
- Reviewer, Boundary Auditor, and GPT-5.5 extra-high Product Acceptance Agent
  complete read-only inspection.
- The slice does not touch protected paths or claim mainline readiness.

## Stop Conditions

Stop and ask the user if any step requires writes outside the approved sandbox
path, protected-file edits, dependency install, commit, push, Obsidian sync,
long-running automation, background service, hooks, MCP write tools, or
mainline promotion.

Stop and stay on this slice if Product Acceptance returns
`REVISE_BEFORE_NEXT`.

Stop and ask the user if Product Acceptance returns `BLOCKED_NEEDS_USER`.
