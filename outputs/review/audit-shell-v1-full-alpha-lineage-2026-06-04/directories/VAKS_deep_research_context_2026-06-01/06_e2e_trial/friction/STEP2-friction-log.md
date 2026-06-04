---
record_type: friction-log
status: active
created: 2026-06-01
step: 2
scope: point-collision
---

# Step 2 Friction Log: Small Collision

## Flow Completed

```text
3 additional sources
-> overlapping candidate points
-> point collision
-> Evidence Packet
-> review queue item
-> scoped reviewed claim
```

## Field Pain

| Question | Observation |
|---|---|
| Which field could not be filled without guessing? | Source independence was hard. `source_family` says all are attributed-LLM/citation papers, but not whether their evidence is independent enough. |
| Which gate felt too heavy? | Evidence Packet repeated similar `rationale` and `reviewer_note` for every source. Useful but tiring. |
| Where did it get stuck? | `item_type` taxonomy: this was synthesis_needed, missing_evidence, and scope_limit at once. One enum made the item feel artificially narrower than the real review problem. |
| Which rule looked good but was hard to execute? | "Point Collision" works as a concept, but the name suggests contradiction. In practice the first useful collision was support/refine convergence. |

## Lazy-Gate Check

This was not ordinary capture, so the heavier gate was allowed.

But if every cross-source overlap requires a full Evidence Packet and queue item, the flow will become too heavy fast.

## Pain Classification

- Too heavy: repeated Evidence Packet fields across four abstract-only sources.
- Missing: compact support/refine collision format.
- Ambiguous: source independence vs same source family.
- Not stuck: The reviewed claim could be created with scoped confidence.

