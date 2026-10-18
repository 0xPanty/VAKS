---
type: source
record_kind: source_card
status: source-captured
title: "WiCER: Wiki-memory Compile, Evaluate, Refine Iterative Knowledge Compilation for LLM Wiki Systems"
source_id: 2026-05-30-wicer-source
source_uri: https://arxiv.org/abs/2605.07068
source_url: https://arxiv.org/abs/2605.07068
source_type: paper
version_or_commit: arXiv:2605.07068v1; checked 2026-05-30
captured_at: 2026-05-30
captured_by: Codex
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - omission-check
  - compiled-wiki
  - source-digest
  - evidence-discipline
projects:
  - verified-action-knowledge-system
verification_status: primary-source-captured
candidate_relation_suggestions: []
tags:
  - wicer
  - omission-check
  - llm-wiki
knowledge_status: raw
processing_tier: light
why_saved: see_body_or_legacy_record
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
---

# WiCER Source Record

## Why Captured

This source supports the v0.3 Omission Check rule.

The useful design point is:

```text
generated or compiled wiki/digest output can fail by dropping important facts, not only by stating false facts.
```

## Source Identity

```text
Paper: WiCER: Wiki-memory Compile, Evaluate, Refine Iterative Knowledge Compilation for LLM Wiki Systems
arXiv: https://arxiv.org/abs/2605.07068
Checked: 2026-05-30
```

## Source Anchor

Short exact source wording:

```text
"discarding critical facts"
"identifies dropped facts"
"forces their preservation"
```

Extracted point:

```text
For heavy source digests, long papers, important repositories, and compiled wiki artifacts, review should ask what key risks, scope limits, or facts may have been omitted.
```

Readable source context:

```text
The paper frames blind wiki compilation as lossy and says WiCER finds dropped facts during evaluation, then makes later compilations preserve them. This supports an omission question in review; it does not prove any specific missing fact exists.
```

## Adopt

```text
omission_check:
  missing_risks
  missing_scope_limits
  possible_omissions
  omission_questions
  needs_full_source_read
```

## Do Not Adopt

```text
automatic wiki rewriting as truth
CEGAR-style full loop as core runtime
benchmark workflow as required review workflow
blind compilation as reviewed knowledge
```

## Fit To This Vault

Place in:

```text
SOURCE_INTAKE heavy mode
REVIEW_QUEUE evidence_packet
templates/review-candidate.md
maintenance-manifest missing_omission_check
```

Boundary:

```text
omission_check creates review pressure.
It does not prove the omitted fact exists.
```
