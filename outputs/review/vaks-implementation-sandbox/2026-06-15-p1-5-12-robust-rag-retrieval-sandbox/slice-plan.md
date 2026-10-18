---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p1-5-12-robust-rag-retrieval-sandbox
status: implemented_pending_review
truth_boundary: sandbox_plan_only
---

# Slice Plan

## Slice ID

```text
2026-06-15-p1-5-12-robust-rag-retrieval-sandbox
```

## Why This Slice

P1-11 received `PASS_PRODUCT_GRADE`. P0 and P1 boundaries now cover receipts,
read-only query flow, runtime artifact exclusion, and semantic anchor support
checks.

The next required item is P1.5-12:

```text
robust RAG retrieval sandbox
```

This slice proves that stronger retrieval mechanics can be shaped as a
sandbox-only retrieval contract while preserving VAKS authority boundaries.

## Only Write Path

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p1-5-12-robust-rag-retrieval-sandbox/
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

No commit, push, sync, dependency installation, long-running automation,
background service, hook, or MCP write tool is allowed.

## Artifact

- `artifact/robust_rag_retrieval_sandbox.py`
- `artifact/verify_robust_rag_retrieval_sandbox.py`
- `artifact/robust-rag-contract.md`
- `artifact/failure-case-oracle.md`
- `fixtures/*.json`
- `failure-cases/*.json`

The implementation uses Python standard library only and imports P1-10 and
P1-11 sandbox validators in read-only mode.

## Acceptance Criteria

- Query construction preserves verbatim input for action-sensitive tasks.
- Route selection records included and excluded authority buckets.
- Bucket filter is applied before ranking/fusion.
- RRF/rerank fusion stays inside authority buckets.
- Runtime artifacts are excluded.
- Selected items expose `selected_by`.
- Vector/rerank/graph/community scores cannot set support, confidence, or trust.
- Graph paths and LLM-extracted relations cannot create reviewed relations.
- Community/RAPTOR/tree summaries cannot become support or action basis without
  raw/reviewed drilldown.
- Eval diagnostics cannot become reviewer approval.
- Generated answers with citations still need support and sufficiency checks in
  action mode.
- Active retrieval cannot auto-promote candidates.
- P1-11 semantic anchor support checks are reused for support claims.
- Positive fixtures and failure cases pass.
- Reviewer returns `REVIEW_PASS_NO_BLOCKER`.
- Boundary Auditor returns `BOUNDARY_PASS_NO_BLOCKER`.
- GPT-5.5 extra-high Product Acceptance returns `PASS_PRODUCT_GRADE`.

## Stop Conditions

Stop and ask the user if this slice would require:

- writing outside the approved sandbox path;
- editing protected docs, wiki truth layers, templates, tools, or Obsidian vault;
- installing dependencies;
- starting a server, watcher, MCP tool, hook, or background service;
- commit, push, sync, or promotion;
- Product Acceptance returns `BLOCKED_NEEDS_USER`.

## Non-Claims

Passing this slice is not production RAG, evidence support, reviewed knowledge,
reviewer approval, action basis, mainline readiness, commit approval, push
approval, or Obsidian sync approval.
