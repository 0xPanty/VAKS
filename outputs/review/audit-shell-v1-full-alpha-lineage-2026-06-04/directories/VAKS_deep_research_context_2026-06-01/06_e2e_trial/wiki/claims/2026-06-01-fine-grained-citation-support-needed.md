---
type: claim
status: reviewed
review_state: reviewed
knowledge_state: standing
claim: "Citation-backed LLM answers need fine-grained source evidence before they can count as VAKS support."
created: 2026-06-01
topics:
  - citation-evaluation
  - evidence-support
  - attributed-llm
related_projects:
  - verified-action-knowledge-system
sources:
  - source-alce-2305-14627
  - source-attributed-qa-2212-08037
  - source-gophercite-2203-11147
  - source-front-2408-04568
supporting_sources:
  - source-gophercite-2203-11147
  - source-front-2408-04568
supporting_context_sources:
  - source-alce-2305-14627
  - source-attributed-qa-2212-08037
conflicting_sources: []
evidence_level: secondary
verification_status: cross-checked
confidence: medium
impact: high
qualification:
  applies_when: "Using citation-backed LLM answers as support in VAKS review or context packs."
  does_not_apply_when: "Treating the cited answer as a general claim about all attribution systems."
  version_scope: "VAKS v0.3 trial"
  project_scope: "verified-action-knowledge-system"
  domain_scope: "LLM citation / attribution review"
  time_scope: "2026-06-01 trial"
  environment_scope:
  assumptions:
    - "Source-span support is enough wording for this trial; quote-level support may be stronger."
temporal_applicability:
  valid_from: 2026-06-01
  valid_until:
  supersedes:
  superseded_by:
  invalidated_by:
  applies_to:
    project: verified-action-knowledge-system
    version: v0.3
    environment:
    timeframe: 2026-06-01 trial
    conditions: "When cited/generated text is used as support."
  check_state: in_scope
  reviewer_note: "No dynamic data; no query-scope issue."
review_summary:
  why_it_still_holds: "Multiple sources converge that attribution/citation needs measurable or fine-grained evidence support."
  strongest_challenge: "All source anchors are abstract-level and from the same research family."
  scope_limits: "No action-readiness conclusion."
  known_risks:
    - same_research_family
    - abstract_only_evidence
    - architecture_overread
  review_due_when:
    - full_source_review
    - adversarial_citation_error_source
    - contradiction
action_readiness:
  state: needs_review
  reason: "Useful for answering a trial question, but not enough for a production action basis."
evidence_sufficiency:
  state: weak
  checked_for: promotion
  missing:
    - full paper review
    - adversarial or negative source
    - non-benchmark operational source
  required_next_step: proceed
  reviewer_note: "Sufficient for sandbox cross-source claim; weak for real action basis."
last_verified: 2026-06-01
next_review: 2026-06-15
tags:
  - claim
  - e2e-trial
---

# Claim: Fine-Grained Citation Support Is Needed

## Claim

Citation-backed LLM answers need fine-grained source evidence before they can count as VAKS support.

## Why It Matters

This is the bridge between "the answer has citations" and "the answer can support a reviewed point or action basis."

## Support / Challenge

Support:

- GopherCite supports claim-level evidence and fact-checking.
- FRONT supports fine-grained quotes over coarse document identifiers.
- ALCE and Attributed QA support the broader citation / attribution evaluation frame.

Challenge:

- The source set is same-family and abstract-only.
- The claim is a VAKS synthesis, not a direct quote from any one source.

## Boundary

This claim can be used in the trial context pack, but it should not become a mainline architecture conclusion without stronger review.

