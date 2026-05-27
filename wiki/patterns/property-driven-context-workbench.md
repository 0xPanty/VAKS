---
type: pattern
status: draft
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - kepano/kepano-obsidian
related_concepts:
  - "[[MEMORY_TIER]]"
  - "[[DEV_CONTEXT]]"
  - "[[obsidian-bases-linked-workbench-views]]"
related_projects:
  - verified-action-knowledge-system
adoption_status: adapt
verification_status: single-source
evidence_level: secondary
evidence_count: 1
confidence: medium
negative_evidence:
  - "Kepano's vault is personal and bottom-up; it does not provide verified-action review gates."
replaces:
superseded_by:
extension_points:
  - memory-tier
  - Obsidian Bases
  - dev-context
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "Needs comparison against more AI-context vaults and actual Obsidian Bases use in this repo."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-kepano-obsidian-source]]"
    observation: "The repo uses categories properties, templates, and .base files to create dynamic views."
    effect: supports
    confidence: medium
relations:
  - target: "[[MEMORY_TIER]]"
    type: refines
    strength: 5
    confidence: medium
    evidence:
      - "[[2026-05-27-kepano-obsidian-source]]"
    rationale: "Memory heat can be surfaced through properties and views without moving files."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[obsidian-bases-linked-workbench-views]]"
    type: supports
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-kepano-obsidian-source]]"
    rationale: "Kepano's Categories notes embed .base views as lightweight workbench pages."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - pattern
  - memory-tier
  - obsidian-bases
  - activation
---

# Property-Driven Context Workbench

## AI-readable preamble

Use properties and view files to surface context instead of moving notes into folders.

This pattern strengthens memory-tier by making hot/warm/cold a metadata and dashboard concern.

It is a view-layer pattern, not a truth-layer pattern.

## One-line definition

Context should be surfaced through reusable properties and dashboards, not primarily through physical file movement.

## Problem solved

Folder-first systems create friction:

```text
Where should this note live?
What if it belongs to several contexts?
Do I need to move it every time the project changes?
```

Kepano's vault shows a lighter way:

```text
write the note where it naturally belongs
add reusable properties
let Bases / dashboards surface it by context
```

## Applicable scenarios

- Building a hot/warm/cold dashboard.
- Creating dev-context candidate lists.
- Surfacing notes by category, status, rating, recency, or link relation.
- Avoiding physical folder churn.

## Not applicable

- Formal promotion into verified truth.
- Replacing review queue.
- Deciding claim confidence.
- Replacing source provenance.

## Evidence

- `[[2026-05-27-kepano-obsidian-source]]`
- Kepano's repo includes `Templates/Bases/*.base`, `Categories/*.md`, and `.obsidian/types.json`.
- Category notes embed `.base` views instead of relying on deep folder hierarchy.

## Tags and scores

- domain: activation-view-layer
- problem: folder-churn
- maturity: emerging
- complexity: low
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 2
- integration_fit: 5
- evidence_strength: 3
- reversibility: 5

## Minimum implementation

Use properties:

```yaml
memory_tier:
activation_status:
scope_key:
last_activated:
activation_reason:
```

Then create view surfaces:

```text
Hot by scope
Warm reusable references
Cold references touched recently
Dev context candidate support
Risk checkpoint list
```

Do not move files just to change heat.

## Fusion suggestion

Adopt for `MEMORY_TIER.md`:

```text
Heat is metadata.
Dashboards surface heat.
Folders remain stable.
```

Use with `DEV_CONTEXT.md`:

```text
Before building a dev context pack, use properties and views to gather candidates.
```

## Verification metrics

- Hot/warm/cold can be listed without moving files.
- A note can appear in several views without duplication.
- Dev context candidate generation becomes easier.
- User does not need to manually refile notes for every new task.
