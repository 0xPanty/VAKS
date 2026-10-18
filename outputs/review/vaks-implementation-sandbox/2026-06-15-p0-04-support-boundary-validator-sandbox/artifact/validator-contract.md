---
record_kind: sandbox_validator_contract
slice_id: 2026-06-15-p0-04-support-boundary-validator-sandbox
status: ready_for_recheck
truth_boundary: sandbox_contract_only
---

# Support Boundary Validator Contract

## Purpose

This sandbox validator checks whether a claimed support item violates VAKS
support boundaries.

It does not decide truth. It does not approve a review. It does not create
evidence support. It only blocks known invalid support shapes.

## Input Contract

Input is one Markdown record with frontmatter:

```yaml
record_kind: support_boundary_check
target_ref:
proposed_support_ref:
proposed_support_record_kind:
proposed_support_authority_bucket:
pack_role: support | orientation | review_input
support_claimed: true | false
evidence_role: direct_support | inferential_support | background_context | counterexample | none
independent_anchor_ref:
anchor_type: raw_span | source_snapshot | code_line | quote | transcript_segment | stable_artifact | url_only | none
anchor_selector:
url_only: true | false
rank_counted_as_support: true | false
score_counted_as_support: true | false
graph_rank_as_trust: true | false
retrieval_rank_as_trust: true | false
feedback_used_as_support: true | false
source_summary_self_support: true | false
claim_note_self_support: true | false
legacy_raw_metadata_used_as_support: true | false
reviewer_note:
```

## Blocking Codes

| Code | Meaning |
|---|---|
| `candidate_as_support` | Candidate, source annotation, review candidate, or project overlay is claimed as support. |
| `url_only_direct_support` | URL-only provenance is claimed as direct support. |
| `rank_or_score_as_support_or_trust` | Retrieval rank, graph rank, score, or RRF-like diagnostic is treated as support or trust. |
| `feedback_as_support` | Feedback/use-ledger material is claimed as support. |
| `source_summary_self_support` | A source summary is used to support itself or replace inspected anchors. |
| `claim_note_self_support_loop` | A claim note supports itself or loops back as its own support. |
| `legacy_metadata_support` | Legacy raw metadata is claimed as support. |
| `background_context_counted_as_support` | Background context is counted as support. |
| `support_claim_missing_independent_anchor` | A direct or inferential support claim lacks a current independent anchor. |
| `inferential_support_missing_reviewer_note` | Inferential support lacks reviewer explanation. |

## Pass Conditions

A passing support claim must either:

- not claim support; or
- claim support from a current independent anchor such as raw source span,
  source snapshot, code/file/line selector, excerpt, transcript segment, or
  stable captured artifact.

Inferential support additionally requires a reviewer note explaining why the
anchor bears on the target.

Passing means only "no known invalid support-boundary shape was detected." It is
not reviewer approval and not a positive evidence-support verdict.
