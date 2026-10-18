---
record_kind: retrieval_receipt
status: template_sandbox
template_version: p0_01_sandbox_v1
query_id:
query_time:
question_summary:
verbatim_input_hash:
query_mode: orientation | source_inspection | review | action
active_project:
requested_authority_bucket: reviewed | raw_anchor | candidate | project_overlay | feedback | mixed_for_orientation
included_buckets: []
excluded_buckets: []
rrf_scope: same_authority_bucket_only
retrieval_engines:
  - engine_id:
    engine_type: lexical | semantic | graph | metadata | manual
    engine_scope:
retrieval_filters:
  include_reviewed: true
  include_raw_anchors: false
  include_candidates: false
  include_project_overlays: active_project_only
  include_feedback: false
  exclude_runtime_artifacts: true
  exclude_legacy_raw_metadata: true
selected_items:
  - ref:
    title:
    record_kind:
    knowledge_status: raw | candidate | reviewed
    authority_bucket: reviewed | raw_anchor | candidate | project_overlay | feedback
    pack_role: orientation | review_input | support | anchor
    action_basis_allowed: false
    warning_code:
    source_anchor:
      source_ref:
      selector:
      source_hash:
      chunk_hash:
      evidence_granularity: metadata_only | abstract_or_summary | excerpt_or_passage | table_or_code_anchor | full_source_reviewed
    selected_by:
      lexical:
      semantic:
      graph:
      metadata:
      manual:
      legacy_raw_metadata: false
    diagnostic_scores:
      lexical_score:
      semantic_score:
      graph_rank:
      rrf_rank:
      scores_are_support: false
excluded_items:
  - ref:
    record_kind:
    authority_bucket:
    excluded_reason:
support_checks:
  - target_ref:
    proposed_support_item_ref:
    independent_anchor_ref:
    evidence_role: direct_support | inferential_support | background_context | counterexample | none
    result: supported | weak | missing_anchor | self_support_loop | scope_limited | not_ready
    reviewer_note:
warnings: []
gaps: []
human_confirmation_required: false
support_boundary:
  selected_by_is_not_support: true
  same_bucket_rrf_only: true
  cross_bucket_rank_not_authority: true
  legacy_raw_metadata_excluded: true
  candidate_overlay_feedback_not_support: true
  url_only_not_direct_support: true
  graph_rank_not_trust: true
  receipt_not_review_approval: true
  receipt_not_action_basis: true
  receipt_not_reviewed_knowledge: true
---

# Retrieval Receipt Template

## Purpose

This receipt records how a query selected material for attention, inspection,
review, or possible support checking.

It does not certify truth, reviewer approval, reviewed knowledge, or action
readiness.

## Contract

Inputs:

- a query or task;
- query mode;
- requested authority bucket;
- retrieval filters;
- retrieval engines or manual selection path;
- selected and excluded items.

Outputs:

- item-level authority bucket;
- item-level pack role;
- selected-by trace;
- explicit warnings and gaps;
- optional support checks that must point to an independent anchor when support
  is claimed.

## Authority Buckets

Use buckets before ranking:

```text
reviewed: reviewed notes, decisions, reviewed relations, or reviewed summaries
raw_anchor: raw source span, source snapshot, transcript segment, code anchor
candidate: candidate distillation, review candidate, source annotation
project_overlay: project-local borrow/non-borrow sidecar
feedback: feedback event or use-ledger record
```

Rules:

- Orientation mode may include mixed buckets, but must label each item.
- Review/action mode defaults to reviewed material and may include raw anchors
  only for evidence checks.
- Candidate, overlay, and feedback items may appear as `orientation` or
  `review_input`; they are not final support.
- `raw_anchor` can support only after the support check targets a specific
  claim, relation, decision, or action basis.

## Selected-By Boundary

`selected_by` explains how the item entered attention.

It is never support:

```text
lexical match != support
semantic similarity != support
graph neighborhood != support
metadata match != support
manual pick != support
rank / score / RRF != support
```

## RRF Boundary

`rrf_scope` must be `same_authority_bucket_only`.

Allowed:

```text
BM25 + vector + graph signals rerank reviewed items inside the reviewed bucket.
```

Not allowed:

```text
reviewed + candidate + raw + feedback are merged into one authority-looking top-k.
```

## Support Check Boundary

Support requires a target and an independent anchor.

Bad:

```text
candidate summary supports itself
URL-only citation is direct support
source annotation is support just because it says possible_support
graph rank is trust
feedback correction changes truth
```

Good:

```text
target_ref + independent raw/source/code/transcript anchor + checked evidence_role
```

If the anchor is missing, circular, only background, stale, or narrower than the
target, use `weak`, `missing_anchor`, `self_support_loop`, `scope_limited`, or
`not_ready`.

## Product Use

A future agent should be able to read a receipt and answer:

1. What question was asked?
2. Which authority bucket was requested?
3. Which buckets were included or excluded?
4. Why was each item selected?
5. Which items were excluded and why?
6. Did any item claim support?
7. If support was claimed, where is the independent anchor?
8. What warnings or gaps remain?

## Non-Claims

This receipt is not:

- a validator;
- an Evidence Packet;
- a review approval;
- a source of truth confidence;
- an action-readiness gate;
- a mainline template.
