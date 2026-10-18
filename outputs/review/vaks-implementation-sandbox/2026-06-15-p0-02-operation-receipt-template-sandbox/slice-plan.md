---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p0-02-operation-receipt-template-sandbox
status: in_progress
truth_boundary: sandbox_artifact_only
---

# Slice Plan

## Slice

P0-02 Operation Receipt Template Sandbox.

## Why This Slice Comes Next

P0-01 fixed the retrieval receipt boundary. P0-02 is the next P0 item because
agent, tool, or operator actions need a separate operation receipt that records
who acted, under which permission tier, on what basis, against which paths, with
what approval, rollback, and result.

This slice does not implement a mainline template or validator. It only proves a
sandbox contract shape that future slices can validate.

## Approved Write Scope

Only this directory is in scope:

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p0-02-operation-receipt-template-sandbox/
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

The current dirty tree is treated as pre-existing baseline under the updated
user rule. Pre-start `git status --short` showed a large dirty tree with:

- modified root/project files such as `MEMORY_TIER.md`;
- deleted historical `outputs/review/project_lens_overlays/*` files;
- modified raw article, paper, repo, and video source records;
- modified `templates/query-run.md`, `templates/video-source.md`;
- modified and untracked `tools/*`;
- many untracked `outputs/review/*`, `raw/*`, `wiki/summaries/*`, and media files;
- existing untracked `outputs/review/vaks-implementation-sandbox/` from prior
  sandbox work.

This slice will audit only whether new or changed files made by this round are
strictly inside the approved P0-02 sandbox directory.

## Acceptance Criteria

The slice is acceptable only if all are true:

- required slice files exist;
- artifact defines operation receipt inputs, outputs, permission tier, operation
  mode, intent confirmation, basis, target paths, proposed changes, approval,
  rollback, result, and non-claims;
- positive fixtures cover allowed propose/write receipt patterns;
- failure cases cover read-only/suggest-only write, reviewed write without
  approval or checked body hash, schema change without owner-final,
  destructive operation without rollback, missing intent confirmation, and
  candidate/action-basis confusion;
- local verification is recorded;
- Reviewer concludes no blocker;
- Boundary Auditor concludes no VAKS boundary blocker;
- GPT-5.5 extra-high Product Acceptance Agent returns `PASS_PRODUCT_GRADE`.

## Stop Conditions

Stop and ask the user if this slice needs to:

- write outside the approved sandbox directory;
- modify protected files or paths;
- install dependencies;
- start background services or automation;
- use MCP write tools;
- claim that this sandbox is a mainline template, reviewed knowledge, approval,
  or action basis;
- proceed after Product Acceptance returns `REVISE_BEFORE_NEXT` without fixing
  the current slice;
- proceed after Product Acceptance returns `BLOCKED_NEEDS_USER`.
