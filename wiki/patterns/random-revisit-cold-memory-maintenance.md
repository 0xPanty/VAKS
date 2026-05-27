---
type: pattern
status: draft
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - kepano/kepano-obsidian
related_concepts:
  - "[[MEMORY_TIER]]"
  - "[[archive-first-lazy-reactivation]]"
  - "[[conversation-derived-feedback-routing]]"
related_projects:
  - verified-action-knowledge-system
adoption_status: watch
verification_status: single-source
evidence_level: secondary
evidence_count: 1
confidence: medium
negative_evidence:
  - "Random revisit can become distraction if not bounded by review or maintenance goals."
replaces:
superseded_by:
extension_points:
  - memory-tier
  - feedback-event
  - review-queue
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "Needs a low-friction trial on this vault before adoption."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-kepano-obsidian-source]]"
    observation: "The linked article describes random revisit and fractal review as maintenance for old ideas."
    effect: supports
    confidence: medium
relations:
  - target: "[[MEMORY_TIER]]"
    type: refines
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-kepano-obsidian-source]]"
    rationale: "Cold material can be reactivated by deliberate maintenance, not only by current project demand."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[archive-first-lazy-reactivation]]"
    type: refines
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-kepano-obsidian-source]]"
    rationale: "Random revisit adds a second reactivation route for archive/cold material."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - pattern
  - memory-tier
  - cold-memory
  - maintenance
---

# Random Revisit Cold Memory Maintenance

## AI-readable preamble

Cold memory should not only wait for search or project demand.

Bounded random revisit can surface old material, create missing links, and generate review candidates.

It must not automatically promote truth or make random old notes hot forever.

## One-line definition

Periodically revisit random old notes to discover missing links, stale assumptions, and reusable context.

## Problem solved

Cold archives can become invisible.

Search only finds what you know how to ask for.

Random revisit can reveal:

```text
forgotten useful sources
missing links
stale notes
unexpected project relevance
new pattern candidates
```

## Applicable scenarios

- Maintenance pass over cold/raw material.
- Looking for inspiration or forgotten context.
- Detecting orphan notes.
- Preparing a synthesis pass after many source records.

## Not applicable

- Urgent implementation mode.
- Formal truth promotion.
- High-stakes decision making.
- Unbounded scheduled agent rewrites.

## Evidence

- `[[2026-05-27-kepano-obsidian-source]]`
- Kepano's design article describes random note revisits and review cycles as a way to revisit old ideas, create missing links, and do maintenance.

## Tags and scores

- domain: memory-maintenance
- problem: cold-archive-invisibility
- maturity: emerging
- complexity: low
- problem_fit: 4
- reuse_value: 4
- implementation_cost: 2
- integration_fit: 4
- evidence_strength: 3
- reversibility: 5

## Minimum implementation

Run a bounded maintenance pass:

```text
1. Pick 5-10 cold/raw/old notes.
2. For each note, ask:
   - still useful?
   - linked to current pattern/decision?
   - stale?
   - missing source?
   - should stay cold, warm, or become a dev-context candidate?
3. Write only small activation/review candidates.
4. Do not rewrite formal truth automatically.
```

## Fusion suggestion

Keep as `watch` until a trial proves it helps.

Possible future addition to `MEMORY_TIER.md`:

```text
random revisit can create reactivation candidates,
but persistent heat requires scope and reason.
```

## Verification metrics

- Random revisit finds useful notes that search did not.
- It creates missing links or review candidates.
- It does not create distracting hot inflation.
- It stays bounded and user-visible.
