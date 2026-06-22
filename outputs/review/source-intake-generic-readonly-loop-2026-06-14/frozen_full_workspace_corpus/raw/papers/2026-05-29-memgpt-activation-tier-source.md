---
type: source
record_kind: source_card
status: source-captured
title: "MemGPT: Towards LLMs as Operating Systems"
source_id: 2026-05-29-memgpt-activation-tier-source
source_uri: https://arxiv.org/abs/2310.08560
source_url: https://arxiv.org/abs/2310.08560
source_type: paper
version_or_commit: arXiv:2310.08560
captured_at: 2026-05-29
captured_by: Codex
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - activation-tier
  - context-management
  - memory-tier
  - memgpt
projects:
  - verified-action-knowledge-system
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - memgpt
  - activation-tier
  - context-management
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

# MemGPT Activation Tier Source Record

## Why Captured

MemGPT is a conceptual reference for context-window management and fast / slow memory tiers.

For this vault, the useful point is naming and boundary discipline:

```text
The vault has activation tiers, not truth tiers.
Hot means read early, not believe more.
```

## Source Identity

- Paper: `MemGPT: Towards LLMs as Operating Systems`
- arXiv: https://arxiv.org/abs/2310.08560
- Project page: https://research.memgpt.ai/

## Extracted Architecture Point

MemGPT uses an OS-inspired virtual context management analogy, moving information between faster in-context memory and slower external memory.

For this vault, the useful point is:

```text
limited context requires activation priority
```

not:

```text
hot / warm / cold are truth levels
```

## Adopt

```text
Activation Tier as public name
fast / slow context management intuition
hot / warm / cold as read-priority states
explicit movement between active context and cold references
```

## Do Not Adopt

```text
agent OS as core architecture
autonomous memory manager before manual loop works
hot / warm / cold as truth tiers
hidden paging that bypasses context-pack evidence boundaries
```

## Review Notes

This source should be presented to Pro review as supplement 12.

The intended absorption is intentionally small:

```text
memory_tier remains a compatibility field;
Activation Tier is the public concept name.
```
