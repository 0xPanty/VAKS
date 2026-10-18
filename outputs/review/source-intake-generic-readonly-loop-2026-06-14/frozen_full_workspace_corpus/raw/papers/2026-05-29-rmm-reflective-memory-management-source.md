---
type: source
record_kind: source_card
status: source-captured
title: "In Prospect and Retrospect: Reflective Memory Management for Long-term Personalized Dialogue Agents"
source_id: 2026-05-29-rmm-reflective-memory-management-source
source_uri: https://arxiv.org/abs/2503.08026
source_url: https://arxiv.org/abs/2503.08026
source_type: paper
version_or_commit: arXiv:2503.08026 / ACL 2025
captured_at: 2026-05-29
captured_by: Codex
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - feedback
  - reflection
  - retrieval
  - dialogue-memory
projects:
  - verified-action-knowledge-system
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - rmm
  - reflective-memory-management
  - conversation-derived-feedback
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

# Reflective Memory Management Source Record

## Why Captured

Reflective Memory Management is a conceptual reference for conversation-derived feedback and feedback-driven retrieval refinement.

## Source Identity

- Paper: `In Prospect and Retrospect: Reflective Memory Management for Long-term Personalized Dialogue Agents`
- arXiv: https://arxiv.org/abs/2503.08026
- ACL Anthology: https://aclanthology.org/2025.acl-long.413/

## Extracted Architecture Point

RMM separates:

```text
prospective / forward-looking reflection:
  summarize interactions across granularities for future retrieval

retrospective / backward-looking reflection:
  refine retrieval based on cited evidence
```

For this vault, the useful point is:

```text
conversation feedback can improve future retrieval and activation
```

not:

```text
conversation feedback can decide truth
```

## Adopt

```text
forward-looking feedback cues
backward-looking cited-evidence checks
conversation-derived missing / scope / correction signals
retrieval refinement as activation adjustment
```

## Do Not Adopt

```text
feedback-driven truth confidence changes
hidden RL as reviewed knowledge control
positive feedback as proof
automatic source reliability updates from one answer
```

## Review Notes

This source should be presented to Pro review as part of supplement 11.

The intended absorption is intentionally small:

```text
feedback_event types and safety boundaries
positive feedback weak
negative feedback creates review pressure
explicit correction creates review_due
```
