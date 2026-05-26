---
type: pattern
status: candidate
source:
  - [[2026-05-26-obsidian-second-brain-source]]
related:
  - [[compiled-truth-plus-append-only-timeline]]
  - [[epistemology-takes-facts-layer]]
confidence: high
adoption_layer: schema
tags:
  - timeline
  - provenance
  - verification
---

# Bi-Temporal Facts For Knowledge History

## Pattern

For changing facts, keep both:

- event time: when the fact was true in the world
- transaction time: when the vault learned or recorded it

`obsidian-second-brain` uses top-level current fields plus a `timeline:` array with `from`, `until`, `learned`, and `source`.

## Why It Matters

Without this, new evidence tends to overwrite old evidence. That destroys the ability to answer:

- what did we believe before?
- why did we change our mind?
- which source caused the update?
- was it a contradiction or a normal evolution?

For a verified knowledge system, this is critical.

## Our Adaptation

Use timeline fields for claims, decisions, patterns, and source status changes:

```yaml
current_status: accepted
timeline:
  - state: proposed
    valid_from: 2026-05-26
    valid_until: 2026-05-26
    learned_at: 2026-05-26
    source: "[[source-note]]"
  - state: accepted
    valid_from: 2026-05-26
    valid_until: present
    learned_at: 2026-05-26
    source: "[[decision-note]]"
```

This should complement, not replace, `compiled truth + append-only timeline`.

## Risk

Timeline for every small note is overkill.

Apply it first to:

- decisions
- high-impact claims
- changing source facts
- adopted patterns
- disputed claims

