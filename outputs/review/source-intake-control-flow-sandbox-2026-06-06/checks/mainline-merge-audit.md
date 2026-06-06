---
type: mainline_merge_audit
status: pass
created_at: 2026-06-06
scope: Source Intake Control Flow round1 + round2 design merge audit
truth_boundary: audit only; not reviewed knowledge; not decision; not action basis
---

# Mainline Merge Audit

## Purpose

This audit checks whether the design logic discovered in both sandbox pressure
tests has been merged into the mainline source-intake rules and templates.

It does not ask whether the sandbox evidence files were moved into mainline.
The sandbox evidence remains diagnostic output.

## Rounds Checked

Round 1 checked the basic runtime boundary:

```text
candidate is not action basis
suggested overlay is trace-only
confirmed overlay is project-scoped
feedback does not mutate truth
RRF does not cross authority buckets
retrieval_policy is machine-filterable, not just prose
```

Round 2 checked the stronger Pro recommendations:

```text
final action-facing support cannot anchor to candidate / overlay
archived overlays are excluded from default retrieval
broken or changed sources create blocked / review_due pressure
confirmed overlays are active-project-only
feedback event data must not leak truth-mutation fields
project borrowing fields must stay project-scoped
```

## First Mainline Audit

The first mainline audit after manual merge did not fully pass:

```text
round1: 10/11
round2: 14/16
```

Missing pieces:

```text
1. Round1 retrieval_policy block was not fully merged into candidate/mainline templates.
2. RRF boundary was described in prose but did not use the explicit machine-checkable phrase.
3. Project non-borrow universal-ban rule was not anchored clearly enough in SOURCE_INTAKE.
4. Candidate distillation and suggested overlay trace did not have full template support.
```

## Patch Applied

Mainline and templates were updated:

```text
SOURCE_INTAKE.md
templates/candidate-distillation.md
templates/review-candidate.md
templates/query-run.md
templates/project-overlay.md
templates/feedback-event.md
templates/source-record.md
templates/video-source.md
```

Key additions:

```text
retrieval_policy.policy_kind
retrieval_policy.pack_allowed
retrieval_policy.action_basis_allowed
retrieval_policy.warning_code
candidate_not_action_basis
overlay_unconfirmed
overlay_not_authority
archived_overlay_excluded
feedback_not_truth
forbidden_truth_mutation_fields_absent
reviewed_note_mutation_allowed: false
source_reliability_mutation_allowed: false
rrf_scope: same_authority_bucket_only
```

## Final Mainline Audit

Final audit result:

```text
mainline_round1=11/11
mainline_round2=16/16
```

## Verdict

```text
round1 design logic: merged into mainline
round2 design logic: merged into mainline
sandbox evidence files: retained as diagnostic output
truth layer: unchanged
```

This means the design logic, not the test artifacts, is now present in the
mainline Source Intake Control Flow and its operational templates.
