---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p0-03-body-hash-validator-sandbox
status: in_progress
truth_boundary: sandbox_artifact_only
---

# Slice Plan

## Slice

P0-03 Body Hash Validator Sandbox.

## Why This Slice Comes Next

P0-01 fixed retrieval receipts. P0-02 fixed operation receipts. P0-03 is next
because review and writeback need a stable exact object: a candidate body must
be hashed canonically before approval, and a later body change must return the
object to review instead of silently reusing stale approval.

This slice creates a sandbox-local validator prototype. It does not create
`tools/validate_review_candidate_body_hash.py`, does not modify `templates/`,
and does not approve any reviewed write.

## Approved Write Scope

Only this directory is in scope:

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p0-03-body-hash-validator-sandbox/
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
At slice start, the worktree was already large and dirty, including modified
raw source records, modified `templates/` and `tools/` files, many untracked
`outputs/review/*` and `raw/*` artifacts, and the completed P0-01/P0-02 sandbox
directories.

The P0-03 target directory did not exist before this slice.

This slice audits only whether files created or changed by this round are
strictly inside the approved P0-03 sandbox directory.

## Acceptance Criteria

The slice is acceptable only if all are true:

- required slice files exist;
- `artifact/body_hash_validator_sandbox.py` runs with standard Python and no
  dependency installation;
- validator implements canonical body hash rule:
  - resolve `candidate_body_location`;
  - exclude the first Markdown heading;
  - normalize CRLF/CR to LF;
  - trim leading/trailing whitespace;
  - UTF-8 SHA256;
- positive fixtures pass;
- failure cases block:
  - body hash mismatch;
  - checked body hash mismatch;
  - fixed/approved review object with missing body hash;
  - writeback-ready object with changed body;
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
- claim validator pass is reviewer approval, reviewed knowledge, mainline
  readiness, or action basis;
- proceed after Product Acceptance returns `REVISE_BEFORE_NEXT` without fixing
  the current slice;
- proceed after Product Acceptance returns `BLOCKED_NEEDS_USER`.
