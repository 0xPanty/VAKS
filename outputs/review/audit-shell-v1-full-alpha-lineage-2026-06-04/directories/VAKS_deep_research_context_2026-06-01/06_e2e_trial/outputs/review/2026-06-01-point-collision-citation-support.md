---
record_type: point-collision
status: reviewed
created: 2026-06-01
updated: 2026-06-01
collision_id: collision-citation-support-001
scope_key: v0.3-citation-support
topic: "citation-backed LLM answers and evidence support"
sources:
  - source-alce-2305-14627
  - source-attributed-qa-2212-08037
  - source-gophercite-2203-11147
  - source-front-2408-04568
collision_type: supports_and_refines
review_status: accepted_as_scoped_synthesis
promotion_target: wiki/claims/2026-06-01-fine-grained-citation-support-needed.md
tags:
  - point-collision
  - e2e-trial
---

# Point Collision: Citation Support Needs Fine-Grained Evidence

## Collision Question

Do multiple sources converge on the point that citation-backed LLM answers need evidence support beyond source labels?

## Candidate Points Compared

| Candidate | Source | Source anchor | Relation to cluster |
|---|---|---|---|
| Citation systems should retrieve supporting evidence and evaluate citation quality. | ALCE | arXiv abstract lines 42-44 | supports |
| Attribution is crucial for information-seeking LLMs and needs measurement. | Attributed QA | arXiv abstract lines 40-41 | supports |
| Users cannot trust model claims without fact-checking; specific evidence helps appraisal. | GopherCite | arXiv abstract lines 42-43 | supports with caution |
| Coarse document identifiers make fine-grained verification hard. | FRONT | arXiv abstract line 39 | refines |

## Normalized Cluster Point

```text
Citation-backed LLM answers need fine-grained source evidence before they can count as VAKS support.
```

## Evidence Packet

```yaml
evidence_packet:
  point: "Citation-backed LLM answers need fine-grained source evidence before they can count as VAKS support."
  evidence_items:
    - source_anchor: "source-alce-2305-14627 / arXiv abstract lines 42-44"
      evidence_granularity: abstract_or_summary
      rationale: "ALCE links citation generation with retrieving supporting evidence and measures citation quality separately."
      evidence_support:
        span_supports_target: partial
        evidence_role: inferential_support
        reviewer_note: "Supports evidence-backed citation evaluation, but does not define VAKS support."
    - source_anchor: "source-attributed-qa-2212-08037 / arXiv abstract lines 40-41"
      evidence_granularity: abstract_or_summary
      rationale: "Attributed QA frames attribution as crucial and measurable."
      evidence_support:
        span_supports_target: partial
        evidence_role: inferential_support
        reviewer_note: "Supports attribution importance, not action readiness."
    - source_anchor: "source-gophercite-2203-11147 / arXiv abstract lines 42-43"
      evidence_granularity: abstract_or_summary
      rationale: "GopherCite says users still need fact-checking and that specific evidence aids appraisal."
      evidence_support:
        span_supports_target: supported
        evidence_role: direct_support
        reviewer_note: "Directly supports the boundary that claims need fact-checking and evidence."
    - source_anchor: "source-front-2408-04568 / arXiv abstract line 39"
      evidence_granularity: abstract_or_summary
      rationale: "FRONT says coarse document identifiers make fine-grained verification hard."
      evidence_support:
        span_supports_target: supported
        evidence_role: direct_support
        reviewer_note: "Directly supports fine-grained evidence over document-level citation."
  grounds: "Four papers converge on attribution/citation as useful but needing measurable or fine-grained evidence support."
  warrant: "If document-level or unsupported citations are hard to verify, VAKS should require source-span evidence before treating a cited answer as support."
  qualifier: "This supports VAKS review behavior, not a new runtime or citation benchmark."
  strongest_rebuttal: "All four sources are from the attributed-LLM research family; this is not independent field evidence."
  challenge_kind: scope_limit
  risk_flags:
    - same_research_family
    - abstract_only_evidence
    - architecture_overread
  omission_check:
    missing_risks: "No adversarial citation-error source; no production user study."
    missing_scope_limits: "All anchors are abstracts."
    possible_omissions: "Full papers may define attribution/citation differently."
    omission_questions: "Does VAKS need quote-level evidence or just source-span evidence?"
    needs_full_source_read: true
  review_question: "Can this become a cross-source scoped claim for the trial context pack?"
  minimal_revision_needed: refine_scope
```

## Collision Resolution

Decision:

```text
Accepted as scoped synthesis for sandbox trial.
```

Why:

```text
The sources do not contradict each other. They converge on attribution/citation as useful and refine the support requirement toward fine-grained evidence.
```

Why not stronger:

```text
All evidence is abstract-level. The sources are topically close. This is enough for a trial context pack, not for mainline architecture conclusion.
```

## Review Queue Item

```yaml
review_queue_item:
  item_id: rq-citation-support-001
  item_type: synthesis_needed
  triggered_by: point_collision
  target_point: "citation-backed LLM answers need fine-grained source evidence before VAKS support"
  suggested_action: "promote sandbox scoped claim; keep action_readiness not_ready"
  status: resolved
```

## Friction Observed

- `source_family` helped flag same-topic clustering, but did not tell whether four papers are independent enough.
- `evidence_role: inferential_support` plus `reviewer_note` was useful but slow to write repeatedly.
- The collision was not a contradiction. The queue language still made it feel like "collision" should be more dramatic than support/refine convergence.

