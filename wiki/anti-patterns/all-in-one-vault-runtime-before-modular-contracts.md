---
type: anti-pattern
status: draft
created: 2026-05-27
updated: 2026-05-27
domain: architecture
failure_mode: "Copying a full all-in-one Obsidian vault runtime before the system's modular contracts are stable"
severity: 4
likelihood: 4
complexity_cost: 5
cross_validated_with:
  - "[[automatic-agentic-vault-rewrite-before-schema-stability]]"
  - "[[para-folder-taxonomy-as-truth-layer]]"
related_projects:
  - verified-action-knowledge-system
replacement:
  - "[[scope-dashboard-live-context-surface]]"
  - "[[property-driven-context-workbench]]"
  - "[[hierarchical-index-context-routing]]"
verification_status: single-source
evidence_level: primary
confidence: high
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "The current Dusk version is Discord-only and was not inspected; this anti-pattern is based on the GitHub repo's own legacy/current statement."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-dusk-obsidian-vault-source]]"
    observation: "The README says the GitHub all-in-one vault is legacy and the current direction is modular components with faster performance."
    effect: supports
    confidence: high
relations:
  - target: "[[DEV_CONTEXT]]"
    type: protects
    strength: 4
    confidence: high
    evidence:
      - "[[2026-05-27-dusk-obsidian-vault-source]]"
    rationale: "A dev context pack should be a governed temporary working set, not a copied all-in-one vault runtime."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[IMPLEMENTATION_BLUEPRINT]]"
    type: supports
    strength: 4
    confidence: high
    evidence:
      - "[[2026-05-27-dusk-obsidian-vault-source]]"
    rationale: "The finding reinforces staged modular implementation rather than reproducing a full plugin-heavy product stack."
    created: 2026-05-27
    last_verified: 2026-05-27
decision: avoid
tags:
  - anti-pattern
  - architecture
  - obsidian
  - modularity
  - dev-context
---

# Anti-pattern: All-in-one Vault Runtime Before Modular Contracts

## AI-readable preamble

Do not copy a full Obsidian vault runtime before the system's core contracts are stable.

Extract useful workbench patterns, but keep the verified-action architecture modular.

## Problem

All-in-one vault packages can look attractive because they already include:

```text
folders
templates
dashboards
inboxes
hotkeys
plugins
mobile views
project/task workflows
```

But copying the whole package makes the project inherit:

```text
plugin dependencies
hidden state
UI assumptions
folder taxonomy
maintenance burden
write-capable automations
performance cost
```

This can derail the real goal:

```text
verified source -> candidate -> review -> decision/action context -> feedback
```

## Source evidence

`DuskWasHere/dusk-obsidian-vault` explicitly says:

```text
Legacy:
  full vault system, PARA + Zettelkasten, all-in-one approach.

Current:
  modular components, faster performance, choose only what you need.
```

That is a direct migration signal from bundled system to modular surface.

## Why it fails

It confuses three different layers:

```text
Workbench:
  views, dashboards, inboxes, navigation.

Activation:
  what should be read now or kept nearby.

Truth:
  what has been reviewed, verified, and made action-ready.
```

The all-in-one vault may be useful as a workbench, but it cannot be allowed to define truth or action authority.

## Failure conditions

- Adopting a vault template before `SCHEMA.md` and review gates are stable.
- Making plugin dashboards required for core knowledge validity.
- Treating folder location or dashboard status as verification status.
- Letting page-task state modify project truth without review.
- Building around a copied Obsidian environment instead of stable Markdown contracts.

## Replacement

Use modular extraction:

```text
extract scope dashboard idea
extract task inbox idea
extract periodic closeout idea
keep all as optional workbench surfaces
route durable adoption through schema/review/feedback contracts
```

Implementation order:

```text
Markdown contract
-> dev context pack
-> manual/Markdown dashboard
-> optional Obsidian Bases/Dataview view
-> optional runtime cache/API later
```

## Boundary

A full vault can inspire workflow design.

It should not become the architecture.
