---
type: source
record_kind: source_card
status: source-captured
title: "Reflexion: Language Agents with Verbal Reinforcement Learning"
source_id: 2026-05-29-reflexion-source
source_uri: https://arxiv.org/abs/2303.11366
source_url: https://arxiv.org/abs/2303.11366
source_type: paper
version_or_commit: arXiv:2303.11366 / NeurIPS 2023
captured_at: 2026-05-29
captured_by: Codex
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - feedback
  - reflection
  - episodic-memory
  - agent-learning
projects:
  - verified-action-knowledge-system
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - reflexion
  - feedback-ledger
  - activation-feedback
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

# Reflexion Source Record

## Why Captured

Reflexion is a conceptual reference for the vault's rule that feedback improves future activation without directly changing truth.

## Source Identity

- Paper: `Reflexion: Language Agents with Verbal Reinforcement Learning`
- arXiv: https://arxiv.org/abs/2303.11366
- NeurIPS proceedings: https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html

## Extracted Architecture Point

Reflexion agents transform task feedback into verbal reflection and store it in episodic memory for later decisions instead of updating model weights.

For this vault, the useful point is:

```text
feedback -> reflection / use memory -> future activation
```

not:

```text
feedback -> truth update
```

## Adopt

```text
feedback as reflection record
episodic/use ledger memory
future activation adjustment
review pressure from failures
```

## Do Not Adopt

```text
feedback as truth confidence update
hidden reinforcement learning over reviewed knowledge
model weight updates as memory
positive feedback as proof
```

## Review Notes

This source should be presented to Pro review as part of supplement 11.

The intended absorption is intentionally small:

```text
Feedback improves activation, not truth.
Positive feedback is weak.
Negative feedback creates review pressure.
Explicit correction creates review_due.
```
