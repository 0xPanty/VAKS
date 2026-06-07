# Real Sample Test Report

## Plain Result

Real sample test result:

```text
PASS_FOR_OBJECT_INTEGRITY
FINAL_APPROVAL_BLOCKED_AS_EXPECTED
```

This test used real promotion-funnel candidates, not only synthetic examples.

Samples:

```text
CI-02 Review-Gated Compile Queue
CI-03 Source Hash Registry And Idempotent Ingest
CI-04 Decision Outcome Precondition Before Calibration
```

Each sample was converted into a fixed self-contained review candidate under:

```text
variant/outputs/review/candidates/
```

## Real Sample Candidate Files

```text
variant/outputs/review/candidates/CI-02-review-gated-compile-queue.candidate.md
variant/outputs/review/candidates/CI-03-source-hash-registry-and-idempotent-ingest.candidate.md
variant/outputs/review/candidates/CI-04-decision-outcome-precondition-before-calibration.candidate.md
```

## Object Gate Result

| Candidate | Object Gate | Final Approval Gate |
| --- | --- | --- |
| CI-02 | PASS | BLOCKED_EXPECTED |
| CI-03 | PASS | BLOCKED_EXPECTED |
| CI-04 | PASS | BLOCKED_EXPECTED |

Meaning:

```text
The fixed candidate objects are reviewable.
They are not final approval-ready because approved_by, checked_specific_evidence,
and checked_body_hash are still empty.
```

That is the intended behavior.

## Body Hashes

Hash rule:

```text
sha256_utf8_lf_trim_body_without_heading
```

Computed body hashes:

```text
CI-02 sha256:8064a811d4bc48d36a88d615e4140229571b230efe5fcd2e874613465ee41c62
CI-03 sha256:cdafe6e912ae5fc9799aab46d5021534b685262128bad1a27ee18bf85ccfd9b7
CI-04 sha256:a52bb75af5d80c1ddc033b83e6098729a34c1a56444a59278a1eb0945edc94b6
```

## Negative Tests On Real Samples

Each real sample was tested with three bad variants:

```text
body_mutation
missing_hash_algorithm
source_summary_only_anchor
```

Results:

| Candidate | body_mutation | missing_hash_algorithm | source_summary_only_anchor |
| --- | --- | --- | --- |
| CI-02 | FAIL as expected | FAIL as expected | FAIL as expected |
| CI-03 | FAIL as expected | FAIL as expected | FAIL as expected |
| CI-04 | FAIL as expected | FAIL as expected | FAIL as expected |

What was caught:

```text
body mutation -> body_hash_mismatch
missing hash algorithm -> missing required hash rule
source summary only anchor -> no independent code/span anchor
```

## Anchor Coverage

CI-02 used local llm-wiki-compiler source snapshot anchors:

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip::...
```

CI-03 used local OpenKB source snapshot anchors:

```text
raw/repos/_snapshots/openkb-main-2026-05-27.zip::...
```

CI-04 used exact RKA GitHub commit line anchors:

```text
https://github.com/infinitywings/rka/blob/7bc2d76...#L...
```

The real-sample gate accepts both local code-span anchors and exact commit URL
line anchors.

## Interpretation

The real samples show that the self-contained candidate pattern is not only
working for CI-01. It also holds for three different candidate types:

```text
generated-wiki review boundary
source ingest lifecycle hygiene
decision/use-ledger calibration precondition
```

The gate improves object integrity and review reproducibility. It still does not
create reviewer approval, truth confidence, action readiness, or automatic
promotion.

## Updated Recommendation

After real-sample testing:

```text
recommendation: adoptable_as_small_mainline_patch_after_user_approval
scope: REVIEW_QUEUE.md + templates/review-candidate.md + existing pattern note
do_not_touch: SCHEMA.md + ARCHITECTURE_PRINCIPLES.md + FUSION_ARCHITECTURE_V0_2_DRAFT.md
```
