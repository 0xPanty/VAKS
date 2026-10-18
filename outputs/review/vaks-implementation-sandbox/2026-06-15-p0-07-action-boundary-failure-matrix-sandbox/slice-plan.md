---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p0-07-action-boundary-failure-matrix-sandbox
created_at: 2026-06-15
status: in_progress
truth_boundary: sandbox_artifact_not_mainline_architecture
---

# Slice Plan

## Opening Card

slice id:

```text
2026-06-15-p0-07-action-boundary-failure-matrix-sandbox
```

Why this slice now:

P0-06 has GPT-5.5 `xhigh` Product Acceptance with `PASS_PRODUCT_GRADE`.
P0-07 is next in the approved P0 order. This slice converts the P0 action
boundary blockers into a cross-slice failure matrix, so later P1 validators and
pilots can reuse the same case IDs without treating any sandbox validator as
mainline architecture.

This round only writes:

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p0-07-action-boundary-failure-matrix-sandbox/
```

This round does not write:

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

Forbidden operations:

```text
commit
push
Obsidian sync
long-running automation
background service
MCP write tool
hooks
dependency install
mainline promotion
```

## Pre-Work Git Baseline

Opening `git status --short` summary:

```text
status_count=253
```

The dirty tree is treated as a pre-existing baseline per user instruction. This
slice only audits whether files created or modified during this round stay under
the P0-07 sandbox directory.

Target path before write:

```text
exists=false
git_status_for_target=no tracked or untracked entries before creation
```

## Acceptance Criteria

- Sandbox-local matrix artifact exists under `artifact/`.
- Matrix covers all P0-07 minimum cases `AB-01` through `AB-12`.
- Each matrix row has source refs, guard refs, detection, expected outcome,
  fixture refs, verifier/check refs, and explicit non-authority claims.
- A sandbox-local verifier checks matrix completeness and boundary fields.
- Positive fixtures pass and failure cases fail with expected codes.
- Reviewer checks coverage, missing cases, maintainability, and overdesign.
- Boundary Auditor checks VAKS authority boundaries and forbidden writes.
- GPT-5.5 extra-high Product Acceptance Agent is the only product-grade
  acceptance authority.
- No P1 slice may start without `PASS_PRODUCT_GRADE`.

## Stop Conditions

- Any required write outside the current sandbox path.
- Any need to modify protected mainline architecture files or truth-layer wiki
  paths.
- Any need for commit, push, sync, dependency install, background service, hook,
  or MCP write tool.
- Product Acceptance returns `REVISE_BEFORE_NEXT`, in which case this slice is
  repaired and rechecked.
- Product Acceptance returns `BLOCKED_NEEDS_USER`, in which case execution stops.

