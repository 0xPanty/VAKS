---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p1-10-runtime-artifact-exclusion-test-sandbox
status: implemented_pending_review
truth_boundary: sandbox_plan_only
---

# Slice Plan

## Slice ID

`2026-06-15-p1-10-runtime-artifact-exclusion-test-sandbox`

## Why This Slice Comes First

P1-09 received `PASS_PRODUCT_GRADE`. The architecture upgrade plan lists
runtime artifact exclusion as the next P1 runtime/pilot artifact after the
read-only query loop. This slice proves that runtime outputs cannot leak back
into retrieval selection, support, reviewed authority, or action basis.

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
outputs/review/vaks-implementation-sandbox/2026-06-15-p1-10-runtime-artifact-exclusion-test-sandbox/
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

- `artifact/runtime_artifact_exclusion_test.py`: sandbox-only manifest
  validator.
- `artifact/verify_runtime_artifact_exclusion_test.py`: suite runner.
- `artifact/exclusion-contract.md`: JSON manifest contract, runtime/durable
  kind boundaries, issue codes, non-claims.
- `artifact/failure-case-oracle.md`: expected failure mapping.
- `fixtures/`: positive JSON manifests.
- `failure-cases/`: negative JSON manifests.

## Acceptance Criteria

- Runtime artifacts are detected by explicit flag, artifact kind, or path
  pattern.
- Retrieval-visible runtime artifacts must be excluded with
  `runtime_artifact_excluded`.
- Runtime artifacts cannot be selected, support, reviewed/raw/support authority,
  action basis, or authority-claiming receipts.
- Durable sandbox documentation is not falsely treated as runtime artifact.
- Derived indexes/caches/logs/suite outputs/generated receipts/bytecode are
  excluded.
- The suite has positive fixtures, failure cases, and actual verification.
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
