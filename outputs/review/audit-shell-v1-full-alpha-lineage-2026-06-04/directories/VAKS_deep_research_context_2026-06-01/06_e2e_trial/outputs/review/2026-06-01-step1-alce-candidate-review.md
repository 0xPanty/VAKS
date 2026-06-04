---
record_type: candidate-point
status: reviewed
created: 2026-06-01
updated: 2026-06-01
point_id: cp-alce-citation-quality-separate
point_text: "Citation-backed LLM outputs need citation quality review separate from answer fluency and correctness."
normalized_point: "citation_quality_is_separate_review_dimension"
point_type: claim
verifiability:
  state: verifiable
  reason: "The ALCE abstract explicitly names citation quality as a separate metric dimension."
review_route: evidence_check
why_checkworthy: "This tests whether VAKS can promote one small source-backed point without inflating it into action readiness."
evidence_granularity: abstract_or_summary
source_refs:
  - source_id: source-alce-2305-14627
    source_url_or_path: https://arxiv.org/abs/2305.14627
    source_range: arXiv abstract lines 42-44
    quote_or_excerpt: "citation quality"
extracted_by: Codex
extracted_at: 2026-06-01
uncertainty: "Only abstract inspected; claim is scoped to ALCE's framing, not to all citation evaluation research."
possible_related_points:
  - citation_support_incomplete_in_current_systems
  - document_level_citation_not_fine_grained_support
review_status: accepted_for_single_source_claim
promotion_target: wiki/claims/2026-06-01-citation-quality-needs-separate-review.md
tags:
  - review-candidate
  - e2e-trial
---

# Candidate Point: Citation Quality Needs Separate Review

## Point

Citation-backed LLM outputs need citation quality review separate from answer fluency and correctness.

## Review Queue Routing

```yaml
review_queue_item:
  item_type: low_confidence_claim
  triggered_by: first_source_trial
  suggested_action: promote_as_single_source_scoped_claim
  status: resolved
```

- Why this needs review: The point may shape how VAKS treats citation-backed answers.
- Suggested action: Promote only as a scoped, single-source claim.
- Resolution note: Accepted with confidence cap because only the arXiv abstract was inspected.

## Source Trace

```yaml
source_anchor:
  url_or_path: https://arxiv.org/abs/2305.14627
  exact_quote: "citation quality"
  prefix: "fluency, correctness, and"
  suffix: "and demonstrate their strong correlation"
  captured_at: 2026-06-01
  position: arXiv abstract line 43
  content_hash:
  archived_url:
  checked_latest_at: 2026-06-01
  source_changed: unknown

source_access:
  access_level: abstract_only
  has_direct_quote: true
  has_source_range: true
  confidence_cap: medium
  cap_reason: "The source span is from the abstract, not a full paper review."
```

## Evidence Packet

```yaml
evidence_packet:
  point: "Citation-backed LLM outputs need citation quality review separate from answer fluency and correctness."
  evidence_items:
    - source_anchor: "source-alce-2305-14627 / arXiv abstract line 43"
      evidence_granularity: abstract_or_summary
      rationale: "ALCE explicitly separates citation quality from fluency and correctness as metric dimensions."
      evidence_support:
        span_supports_target: supported
        evidence_role: direct_support
        reviewer_note: "Supported only for ALCE's benchmark framing."
  grounds: "ALCE proposes automatic metrics along three dimensions including citation quality."
  warrant: "If citation quality is separately measured, VAKS should not collapse it into correctness or fluency."
  qualifier: "Scoped to citation-backed LLM answer review, not all evidence review."
  strongest_rebuttal: "A benchmark dimension does not itself prove VAKS needs a durable field or new lane."
  challenge_kind: scope_limit
  risk_flags:
    - benchmark_scope_overread
  omission_check:
    missing_risks: "No full paper methods review; no comparison to other citation-evaluation work yet."
    missing_scope_limits: "Abstract-only evidence."
    possible_omissions: "Metric definitions may matter."
    omission_questions: "Does citation quality in ALCE mean source support, citation placement, or both?"
    needs_full_source_read: false
  review_question: "Can this become a single-source reviewed claim?"
  minimal_revision_needed: refine_scope
```

## Manual Review

Reviewer: Codex, manual sandbox simulation.

Decision: Accept as a single-source, scoped reviewed claim.

Reason:

```text
The source supports that ALCE treats citation quality as a distinct evaluation dimension.
It does not support a broader architecture claim that VAKS needs new schema or metrics.
```

Promotion boundary:

```text
Promote as single-source claim with medium confidence cap.
Do not mark as action-ready.
```

## Friction Observed

- `review_queue_item.item_type` felt awkward: this was not exactly low confidence, contradiction, missing evidence, synthesis_needed, or decision_superseded.
- The Evidence Packet was useful but heavy for a single abstract-backed point.
- `needs_full_source_read: false` felt like a judgment call. It was true for this narrow point, but the field creates pressure to justify not reading the full paper.

