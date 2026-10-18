---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox
status: implemented_pending_review
truth_boundary: sandbox_plan_only
---

# Slice Plan

## Slice ID

`2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox`

## Why This Slice Comes First

P0-07 received `PASS_PRODUCT_GRADE`, and the architecture upgrade plan orders
the next implementation step as P1 retrieval/operation receipt validators before
the read-only query loop pilot.

This slice turns the P0-01 retrieval receipt template and P0-02 operation
receipt template into a sandbox-local machine-checkable pilot. It proves that
the core receipt boundaries can be validated before any runtime query loop or
mainline tool is attempted.

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
outputs/review/vaks-implementation-sandbox/2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox/
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

- `artifact/receipt_validator_pilot.py`: sandbox-only validator for normalized
  flat frontmatter retrieval and operation receipt instances.
- `artifact/verify_receipt_validator_pilot.py`: suite runner for all fixtures
  and failure cases.
- `artifact/validator-contract.md`: input/output contract and non-claims.
- `artifact/failure-case-oracle.md`: expected issue code mapping.
- `fixtures/`: positive examples.
- `failure-cases/`: negative examples.

## Acceptance Criteria

- Positive retrieval and operation receipts pass.
- Retrieval failure cases block:
  - unknown authority bucket or pack role;
  - cross-bucket RRF;
  - selected-by / score as support;
  - candidate, overlay, source annotation, or feedback as support/action basis;
  - legacy raw metadata as support path;
  - graph rank as trust;
  - URL-only direct support;
  - missing independent anchor for claimed support;
  - receipt authority claims;
  - false support-boundary flags.
- Operation failure cases block:
  - unknown actor tier or operation mode;
  - read-only or suggest-only actors writing;
  - reviewed writes missing approval/body hash;
  - mainline/formal writes missing approval/body hash;
  - body hash mismatch;
  - schema change without owner-final authority;
  - destructive operation without rollback;
  - missing intent confirmation;
  - candidate write outside sandbox/candidate scope;
  - candidate/feedback/retrieval/rank/summary/context material as action basis;
  - operation receipt authority claims;
  - false operation-boundary flags.
- Verification runs locally with Python standard library only.
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
