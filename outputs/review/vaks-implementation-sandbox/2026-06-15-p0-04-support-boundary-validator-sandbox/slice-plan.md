---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p0-04-support-boundary-validator-sandbox
status: ready_for_recheck
truth_boundary: sandbox_artifact_only
---

# Slice Plan

## Slice

P0-04 Support Boundary Validator Sandbox.

## Why This Slice Comes Next

P0-01 created retrieval receipt boundaries, P0-02 created operation receipt
boundaries, and P0-03 created body-hash validator boundaries. P0-04 is next
because a retrieved, selected, ranked, summarized, or feedback-derived item must
not become evidence support unless it has the right source-span-to-target shape.

This slice creates a sandbox-local validator prototype. It does not create
`tools/validate_support_boundary.py`, does not modify `templates/`, and does
not approve any support claim.

## Approved Write Scope

Only this directory is in scope:

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p0-04-support-boundary-validator-sandbox/
```

## Explicit Non-Write Scope

Do not modify:

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

Do not run:

```text
commit
push
Obsidian sync
long-running automation
background service
MCP write tool
hooks
dependency installation
```

## Pre-Start Git Status Summary

The current dirty tree is treated as pre-existing baseline under the user rule.
At slice start, the worktree remained large and dirty, including modified raw
source records, modified `templates/` and `tools/` files, many untracked
`outputs/review/*` and `raw/*` artifacts, and prior P0 sandbox directories.

The P0-04 target directory did not exist before this slice.

This slice audits only whether files created or changed by this round are
strictly inside the approved P0-04 sandbox directory.

## Acceptance Criteria

The slice is acceptable only if all are true:

- required slice files exist;
- `artifact/support_boundary_validator_sandbox.py` runs with standard Python and
  no dependency installation;
- positive fixtures pass;
- failure cases block:
  - candidate as support;
  - URL-only as direct support;
  - rank/score as support or trust;
  - feedback as support;
  - source summary self-support;
  - claim note self-support loop;
  - legacy metadata support;
  - background context counted as support;
- verification records actual command results;
- Reviewer concludes no blocker;
- Boundary Auditor concludes no VAKS boundary blocker;
- GPT-5.5 extra-high Product Acceptance returns `PASS_PRODUCT_GRADE`.

## Stop Conditions

Stop and ask the user if this slice needs to:

- write outside the approved sandbox directory;
- create or edit mainline `tools/` or `templates/`;
- modify protected architecture files;
- install dependencies;
- start services or automation;
- claim validator pass is evidence support, reviewer approval, reviewed
  knowledge, mainline readiness, or action basis;
- proceed after Product Acceptance returns `REVISE_BEFORE_NEXT` without fixing
  the current slice;
- proceed after Product Acceptance returns `BLOCKED_NEEDS_USER`.
