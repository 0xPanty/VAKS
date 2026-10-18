# CI-04 Sandbox Test Report: Decision Outcome Precondition Before Calibration

Date: 2026-06-08

Scope:

```text
CI-04 is a Use Ledger / Feedback Ledger hardening rule.
It is not a runtime, dashboard, SQLite store, truth layer, review verdict, or reviewed relation engine.
```

## Sandbox

Sandbox root:

```text
outputs/review/ci-04-decision-outcome-precondition-before-calibration-2026-06-08/
```

Base architecture copied from:

```text
outputs/review/ci-03-source-hash-registry-idempotent-ingest-2026-06-08/architecture/
```

This sandbox tests CI-04 on top of CI-02, CI-02.5, and CI-03.

No permanent Obsidian sync was performed.

## Source Evidence

Promotion packet:

```text
outputs/review/promotion-funnel-pilot-2026-06-08/PROMOTION_EVIDENCE_PACKETS.md
```

Primary local source records:

```text
raw/repos/2026-05-29-rka-source.md
outputs/review/2026-05-30-rka-source-code-anchor-review.md
```

Exact RKA anchors recorded by the evidence packet:

```text
https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/models/decision_option.py#L121-L130
https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/decision_options.py#L234-L280
https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/api/routes/decisions.py#L227-L243
```

Existing VAKS support:

```text
SCHEMA.md already says final decision outcome requires recommendation plus user choice or explicit override.
FEEDBACK.md already routes decision outcome to future recommendation/risk calibration, not truth.
templates/decision-record.md already has a Decision Outcome Calibration section.
```

## Sandbox Changes

Updated only inside the CI-04 sandbox:

```text
architecture/FEEDBACK.md
architecture/templates/decision-record.md
architecture/wiki/indexes/knowledge-graph-index.md
```

Added sandbox-only pattern:

```text
architecture/wiki/patterns/decision-outcome-precondition-before-calibration.md
```

Added test fixtures and runner:

```text
tests/fixtures/decision-outcomes/
tests/pressure-test.ps1
```

## Rule Tested

Plain version:

```text
Do not use an outcome to calibrate future recommendations unless we know:
what was recommended,
how confident the recommendation was,
what the user chose or explicitly overrode,
and what actually happened.
```

Minimum chain:

```text
recommendation
-> confidence_at_decision
-> user_choice OR explicit_user_override
-> outcome_note
-> future recommendation calibration
```

Allowed effects:

```text
future_recommendation
risk_calibration
scope_fit
option_framing
review_due
```

Forbidden effects:

```text
truth_confidence
verification_status
source_reliability
review_verdict
reviewed_relation
reviewed_relation_strength
action_basis_readiness
```

Forbidden imports:

```text
RKA runtime
RKA MCP
RKA API server
RKA dashboard
RKA SQLite database
calibration metrics as truth confidence
```

## Pressure Test

Command used:

```powershell
& "outputs\review\ci-04-decision-outcome-precondition-before-calibration-2026-06-08\tests\pressure-test.ps1"
```

Final result:

```text
RESULT pass=91 fail=0
```

Test dimensions:

- CI-04 pattern contains the recommendation -> user choice / override -> outcome chain.
- FEEDBACK sandbox copy has explicit override, outcome note, allowed targets, and forbidden targets.
- Decision record template sandbox copy exposes the same precondition.
- Knowledge graph index sandbox copy records the CI-04 boundary.
- PASS fixture with recommendation + user_choice + outcome_note succeeds.
- PASS fixture with recommendation + explicit_user_override + outcome_note succeeds.
- BLOCK fixture with outcome only is blocked.
- BLOCK fixture without user_choice / override is blocked.
- BLOCK fixture with casual "looks good" is blocked.
- BLOCK fixture trying to mutate truth_confidence is blocked.
- BLOCK fixture trying to mutate verification_status is blocked.
- BLOCK fixture trying to create reviewed_relation is blocked.
- BLOCK fixture trying to import RKA runtime / MCP / dashboard / SQLite is blocked.
- Compatibility checks confirm CI-02, CI-02.5, and CI-03 still exist in the same sandbox.
- Root pollution checks confirm CI-04 sandbox-only lines were not written into formal root files.

## Result

Positive.

This is not overdesigned if kept as a small precondition. It is mostly already present in the architecture; the sandbox only makes it clearer and testable.

No architecture conflict was found.

It reinforces the existing boundary:

```text
outcome calibration improves future recommendations,
but does not change truth.
```

## Recommended Mainline Merge Shape

If approved later, merge a lightweight version only:

```text
FEEDBACK.md
templates/decision-record.md
wiki/indexes/knowledge-graph-index.md
```

Optional:

```text
wiki/patterns/decision-outcome-precondition-before-calibration.md
```

Do not merge:

```text
tests/fixtures/
tests/pressure-test.ps1
RKA runtime
RKA MCP
RKA API server
RKA dashboard
RKA SQLite database
calibration metrics / Brier / ECE as truth logic
```

## Final Judgment

```text
positive: yes
overdesigned: no, if kept as a small precondition
conflict_with_existing_architecture: no
recommend_mainline_merge_later: yes, lightweight only
```

