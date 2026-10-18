---
type: source_intake_minimum_test_cases
status: mixed_static_pass_runtime_not_run
created_at: 2026-06-13
scope: Source Intake hardening minimum acceptance tests
truth_boundary: test plan and evidence map only; not Source Intake P0 approval
---

# Minimum Test Cases

## Plain Verdict

The static test layer is mostly covered and rerunnable in this package.

The runtime / answer-loop layer is not covered yet. Those tests are acceptance
criteria for a future read-only runtime pass, not evidence already produced by
this package.

## Test Matrix

| Test | Type | Target | Pass criteria | Current status | Evidence / next step |
|---|---|---|---|---|---|
| current lint rerun | static | Reproduce 0 hard errors and warning classification. | Rerun produces the same current counts and issue classes. | pass | `validate_source_intake_contract.py --scope current`: 219 collected, 166 validated, 122 warnings, 0 errors. |
| duplicate YAML regression | static | Ensure YAML last-wins no longer hides duplicate keys. | Duplicate key must produce an error. | pass | Failure matrix includes duplicate YAML case. |
| canonical overlay placeholder test | static | Verify canonical overlay core placeholders fail. | Placeholder `target_ref` / borrow / non-borrow / reopen fields error in canonical scope. | pass | Failure matrix includes confirmed-overlay placeholder case; current hard errors 0 after cleanup/exclusion. |
| raw confidence / relations fail test | static | Verify raw source authority-like fields fail when top-level. | Top-level raw `confidence` and `relations` error. | pass | Failure matrix includes both; current top-level red-zone fields are absent. |
| migration replay on sample files | migration replay | Manually compare representative before/after semantics. | No obvious invented semantics; semantic compression documented. | partial / not independently complete | Mapping policy and migration report exist, but no pre-normalization snapshot or 10-20 file manual replay packet is included. |
| read-only answer-loop | runtime | Check source/candidate/overlay are not used as final support. | Receipt support items must have independent anchors; candidate/overlay remain orientation/review_input. | not run | Needs read-only query -> retrieval -> answer/use-loop pilot. |
| external blind relevance judgment | runtime / external review | Validate receipts/packs are useful beyond self-scoring. | External relevance judgments align with bucket/warning semantics. | not run | Needs external blind relevance packet and judgments. |
| promotion-gate stress test | runtime | Ensure candidate/raw/feedback cannot bypass gate into action support. | All forbidden promotions are blocked or downgraded. | not run | Needs dry-run writeback / forbidden action tests. |
| graph compiler quarantine test | runtime | Ensure raw legacy relations do not become formal graph/support edges. | Graph contains no raw authority edge; every edge has candidate/review provenance. | not run | Needs graph build sandbox. |
| overlay retrieval leak test | runtime | Ensure archived/legacy overlays do not enter default retrieval. | Default retrieval returns no archived/legacy overlay unless active project and explicit drilldown allow it. | not run | Needs rebuilt-index before/after receipt diff. |
| feedback scope aggregation test | runtime | Ensure local negative feedback does not become global suppression. | Feedback effects stay in same project/context scope. | not run | Needs multi-project negative-feedback replay. |
| anchor freshness test | runtime | Ensure stale/broken anchors block action mode. | Broken/stale anchors create blocked/review_due or missing_anchor, not supported/action-ready. | not run | Needs anchor existence/content replay. |

## Boundary

Passing the static tests is not enough for Source Intake P0. P0 requires the
runtime tests to be executed read-only, with receipts/traces that can be audited.

Runtime test results can create review pressure and implementation confidence.
They must not directly create reviewed truth, reviewed relations, or action
basis.
