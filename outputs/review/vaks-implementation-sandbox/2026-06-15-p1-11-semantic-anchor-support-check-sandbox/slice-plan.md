---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p1-11-semantic-anchor-support-check-sandbox
status: implemented_pending_review
truth_boundary: sandbox_plan_only
---

# Slice Plan

## Slice ID

```text
2026-06-15-p1-11-semantic-anchor-support-check-sandbox
```

## Why This Slice

P1-10 received `PASS_PRODUCT_GRADE`. The next P1 item in the upgrade plan is
the semantic anchor support check. P1 is proving that the read-only query loop
can honor P0 boundaries under realistic flow.

This slice closes a specific P1 gap:

```text
semantic/vector/graph retrieval can locate candidate anchors,
but retrieval rank, semantic score, graph rank, summaries, feedback, runtime
artifacts, and candidate distillations cannot become evidence support.
```

## Only Write Path

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p1-11-semantic-anchor-support-check-sandbox/
```

## Non-Write Paths

No changes are allowed to:

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

No commit, push, sync, background service, long-running automation, MCP write
tool, hook, or dependency installation is allowed.

## Artifact

- `artifact/semantic_anchor_support_check.py`
- `artifact/verify_semantic_anchor_support_check.py`
- `artifact/anchor-contract.md`
- `artifact/failure-case-oracle.md`
- `fixtures/*.json`
- `failure-cases/*.json`

The implementation uses only the Python standard library and imports the P1-10
runtime artifact detector in read-only mode.

## Acceptance Criteria

- Input/output contract is explicit and reusable by later P1/P1.5 slices.
- Positive fixtures prove:
  - raw excerpt support;
  - code line support;
  - transcript segment inferential support;
  - semantic orientation without support;
  - captured URL with stable selector/hash;
  - reviewed support reference.
- Failure cases block:
  - semantic score as support;
  - graph rank/relation as support;
  - URL-only and metadata-only support;
  - summaries as support;
  - candidate/project overlay as support;
  - feedback as support;
  - runtime artifacts and generated receipts as anchors/support;
  - missing source or selector;
  - unknown anchor kinds;
  - action-basis or reviewed-knowledge claims;
  - self-support loops;
  - invalid support roles and authority buckets.
- `python -B -m py_compile ...` passes.
- `python -B artifact/verify_semantic_anchor_support_check.py` passes.
- Reviewer finds no blocker.
- Boundary Auditor finds no VAKS boundary violation.
- GPT-5.5 extra-high Product Acceptance Agent returns
  `PASS_PRODUCT_GRADE`.
- Final git audit shows this slice only writes inside the allowed sandbox path.

## Stop Conditions

Stop and ask the user if:

- any protected path must be edited;
- a production validator under `tools/` is required;
- Obsidian sync is needed;
- commit or push is needed;
- a background service, hook, dependency install, or MCP write tool would be
  required;
- Product Acceptance returns `BLOCKED_NEEDS_USER`.

## Non-Claims

Passing this slice is not evidence support, reviewer approval, reviewed
knowledge, action basis, promotion, mainline readiness, commit approval, push
approval, or Obsidian sync approval.
