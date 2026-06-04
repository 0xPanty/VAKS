---
type: claim
status: reviewed
review_state: reviewed
knowledge_state: standing
claim: "Citation-backed LLM outputs need citation quality review separate from answer fluency and correctness."
created: 2026-06-01
topics:
  - citation-evaluation
  - evidence-support
  - attributed-llm
related_projects:
  - verified-action-knowledge-system
sources:
  - source-alce-2305-14627
supporting_sources:
  - source-alce-2305-14627
conflicting_sources: []
evidence:
  - source_id: source-alce-2305-14627
    source_range: arXiv abstract line 43
    quote_or_excerpt: "citation quality"
    source_access:
      access_level: abstract_only
      has_direct_quote: true
      has_source_range: true
      confidence_cap: medium
      cap_reason: "Abstract-only source span."
    evidence_support:
      span_supports_target: supported
      evidence_role: direct_support
      reviewer_note: "Supports ALCE's framing; does not imply VAKS action readiness."
relations: []
evidence_level: secondary
verification_status: single-source
confidence: medium
impact: medium
attack_assessment:
  severity: minor
  reason: "Overreading benchmark framing into VAKS architecture would be the main risk."
  affected_scope: "citation-backed answer review"
  requires_review_due: false
qualification:
  applies_when: "Reviewing citation-backed LLM answers or context packs."
  does_not_apply_when: "Treating citation metrics as truth confidence or action readiness."
  version_scope: "VAKS v0.3 evidence discipline"
  project_scope: "verified-action-knowledge-system"
  domain_scope: "LLM citation / attribution evaluation"
  time_scope: "As of captured source version v2, 2023-10-31."
  environment_scope:
  assumptions:
    - "Citation quality is a review dimension, not a truth layer."
temporal_applicability:
  valid_from: 2023-10-31
  valid_until:
  supersedes:
  superseded_by:
  invalidated_by:
  applies_to:
    project: verified-action-knowledge-system
    version: v0.3
    environment:
    timeframe: 2026-06-01 trial
    conditions: "When answering with citations or source-backed generated text."
  check_state: in_scope
  reviewer_note: "No known superseding source in this trial."
review_summary:
  why_it_still_holds: "The source directly separates citation quality from other evaluation dimensions."
  strongest_challenge: "Single abstract source; no full metric analysis."
  scope_limits: "Do not convert into schema field or action gate without more evidence."
  known_risks:
    - benchmark_scope_overread
  review_due_when:
    - new_primary_source
    - contradiction
    - source_version_change
action_readiness:
  state: not_ready
  reason: "This is a review framing claim, not an action basis by itself."
evidence_sufficiency:
  state: weak
  checked_for: promotion
  missing:
    - full paper method details
    - cross-source support
  required_next_step: proceed
  reviewer_note: "Weak but enough for single-source scoped promotion in a sandbox trial."
last_verified: 2026-06-01
next_review: 2026-06-15
tags:
  - claim
  - e2e-trial
---

# Claim: Citation Quality Needs Separate Review

## Claim

Citation-backed LLM outputs need citation quality review separate from answer fluency and correctness.

## Why It Matters

This prevents VAKS from treating "has citations" as the same thing as "is correct" or "is action-ready."

## Supporting Evidence

ALCE names citation quality as a separate evaluation dimension alongside other answer qualities.

Evidence support:

```text
supported / direct_support
```

## Scope Boundary

This claim supports review framing only.

It does not create:

```text
truth confidence upgrade
new schema field
runtime evaluator
action readiness
```

## Trial Note

This is deliberately a small verified node. It is useful enough for a context pack, but not strong enough to settle architecture.

