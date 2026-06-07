# Obsidian Full Test Report

## Scope

Formal Obsidian vault:

```text
H:\Obsidian\资料库
```

Temporary test directory:

```text
H:\Obsidian\资料库\_codex_temp_self_contained_candidate_fulltest_20260608-040252
```

The temporary directory was deleted after the test.

## Files Copied Into Obsidian Temp Directory

Main framework files:

```text
REVIEW_QUEUE.md
templates/review-candidate.md
wiki/patterns/self-contained-review-candidate-record.md
```

Candidate samples:

```text
outputs/review/candidates/CI-01-self-contained-review-candidate-record.candidate.md
outputs/review/candidates/CI-02-review-gated-compile-queue.candidate.md
outputs/review/candidates/CI-03-source-hash-registry-and-idempotent-ingest.candidate.md
outputs/review/candidates/CI-04-decision-outcome-precondition-before-calibration.candidate.md
```

Copy verification:

```text
SHA256 source/destination hash match: PASS for all copied files
```

## Obsidian Path Test Results

Document checks:

```text
REVIEW_QUEUE has 3.2.1 gate                PASS
REVIEW_QUEUE keeps Evidence Packet support PASS
Template top-level review-candidate        PASS
Pattern active adopted                     PASS
No misleading promote_ready in copied pack PASS
```

Object gate:

```text
CI-01 Self-Contained Review Candidate Record           PASS
CI-02 Review-Gated Compile Queue                       PASS
CI-03 Source Hash Registry And Idempotent Ingest       PASS
CI-04 Decision Outcome Precondition Before Calibration PASS
```

Final approval gate:

```text
CI-01 BLOCKED_EXPECTED
CI-02 BLOCKED_EXPECTED
CI-03 BLOCKED_EXPECTED
CI-04 BLOCKED_EXPECTED
```

Reason:

```text
approved_by, checked_specific_evidence, and checked_body_hash were intentionally empty.
```

Strong positive on Obsidian copy:

```text
synthetic approval-ready CI-02 copy PASS
```

This simulated:

```text
approved_by: obsidian-test-reviewer
approval_source: obsidian-fulltest
checked_specific_evidence: true
checked_body_hash: same as body_hash
```

Negative tests on Obsidian copies:

```text
body_mutation                 FAIL as expected
missing_hash_algorithm        FAIL as expected
source_summary_only_anchor    FAIL as expected
```

Run across four candidates:

```text
12 / 12 bad variants were blocked.
```

Overall:

```text
OVERALL=True
```

## Cleanup Verification

Deletion command was guarded by resolved-path check:

```text
resolved path must match:
H:\Obsidian\资料库\_codex_temp_self_contained_candidate_fulltest_*
```

Deletion result:

```text
DELETED_PATH=H:\Obsidian\资料库\_codex_temp_self_contained_candidate_fulltest_20260608-040252
STILL_EXISTS=False
```

## Interpretation

The Obsidian full test confirms that the mainline addition works when copied
into the formal vault path:

```text
fixed candidate body + body_hash + independent anchors
-> object gate passes
-> final approval remains blocked without human approval facts
-> mutated body / missing hash rule / source-summary-only anchors are blocked
```

The test left no temporary files in the formal Obsidian vault.
