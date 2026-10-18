---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p0-01-retrieval-receipt-template-sandbox
status: draft_for_review
created_at: 2026-06-15
truth_boundary: sandbox_artifact_only_not_reviewed_knowledge
---

# P0-01 Retrieval Receipt Template Sandbox

## Slice

`2026-06-15-p0-01-retrieval-receipt-template-sandbox`

## Why This Slice Comes First

The upgrade plan orders P0 as receipt templates before validators and runtime
pilots. Retrieval is the first authority-risk surface because a retrieved item
can look like support even when it is only an activation or discovery result.

This slice therefore turns the retrieval boundary into a reusable sandbox
contract before any validator or query-loop pilot depends on it.

## Allowed Write Scope

Only this directory is in scope:

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p0-01-retrieval-receipt-template-sandbox/
```

## Explicitly Out Of Scope

- No edits to `SCHEMA.md`.
- No edits to `ARCHITECTURE_PRINCIPLES.md`.
- No edits to `FUSION_ARCHITECTURE_V0_2_DRAFT.md`.
- No edits to `README.md`.
- No writes under `wiki/claims/`, `wiki/patterns/`, or `wiki/decisions/`.
- No edits to `templates/` or `tools/`.
- No Obsidian sync.
- No commit or push.
- No validator implementation.
- No P1 read-only query-loop pilot.
- No GraphRAG, MCP, plugin, service, hook, or long-running automation.

## Pre-Start Git Status Summary

User approved treating the current dirty tree as pre-existing baseline for this
slice.

Observed before writing this package:

```text
git status --short total lines: 252
target sandbox directory: not present before start
latest commits:
  5c75121e docs: record source annotation closeout state
  db7b6bb2 docs: land source annotation pilot workbench
  c715fd59 docs: adopt source annotations for intake anchors
```

Pre-existing dirty entries in protected areas included:

```text
 M templates/query-run.md
 M templates/video-source.md
 M tools/run_source_intake_generic_readonly_loop.py
 M tools/validate_source_intake_contract.py
 M tools/validate_source_intake_failure_matrix.py
?? tools/__pycache__/
?? tools/build_source_intake_hardening_package.py
?? tools/clear_source_intake_red_zone.py
?? tools/preserve_source_intake_legacy_fields.py
?? tools/relocate_legacy_project_lens.py
?? tools/source_intake_readonly_shared.py
?? tools/validate_source_intake_hardening_package.py
```

These are baseline observations only. They are not part of this slice and must
not be modified by this slice.

## Deliverables

- `slice-plan.md`
- `source-map.md`
- `artifact/retrieval-receipt-template.md`
- `artifact/contract-notes.md`
- `fixtures/valid-orientation-receipt.md`
- `fixtures/valid-review-anchor-receipt.md`
- `failure-cases/candidate-as-support.md`
- `failure-cases/cross-bucket-rrf.md`
- `failure-cases/feedback-as-support.md`
- `failure-cases/legacy-metadata-support.md`
- `failure-cases/rank-as-trust.md`
- `failure-cases/url-only-direct-support.md`
- `verification.md`
- `reviewer-report.md`
- `boundary-audit.md`
- `product-acceptance-report.md`
- `next-step.md`

## Acceptance Standard For This Slice

This slice may pass only if all are true:

1. The retrieval receipt template has a clear input/output contract.
2. The template makes authority buckets visible.
3. `selected_by` is explicitly trace metadata, not support.
4. RRF is limited to the same authority bucket.
5. Candidate, overlay, feedback, rank, graph score, and legacy raw metadata
   cannot become support through receipt wording.
6. Positive fixtures show ordinary orientation and review-anchor use.
7. Failure cases cover obvious misuse paths future validators must block.
8. Verification proves all written files are inside the approved sandbox path.
9. Reviewer and Boundary Auditor find no blocker.
10. GPT-5.5 extra-high Product Acceptance Agent returns
    `PASS_PRODUCT_GRADE`.

## Stop Conditions

- Any required write outside the approved sandbox path.
- Any need to edit `templates/`, `tools/`, `SCHEMA.md`, or the frozen spine.
- Any Product Acceptance result other than `PASS_PRODUCT_GRADE`.
- Any uncertainty that the receipt wording has confused retrieval with support,
  reviewer approval, reviewed knowledge, or action basis.

## Supported Conclusion

If accepted, this package supports only:

```text
The P0-01 retrieval receipt template sandbox is product-grade enough to be used
as input for the next sandbox slice.
```

## Unsupported Conclusions

This package does not prove:

- P0 has passed.
- A retrieval receipt validator exists.
- The runtime query loop is validated.
- Retrieved items are evidence support.
- Any output is reviewed knowledge.
- Any action basis is ready.
- The template should be merged into mainline without separate approval.
