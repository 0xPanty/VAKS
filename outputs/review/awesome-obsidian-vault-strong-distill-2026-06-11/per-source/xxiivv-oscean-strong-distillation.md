---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/XXIIVV/oscean"
repo_key: "XXIIVV/oscean"
checked_commit: "6e16d5d139a6d84b363865172ab60a8a195945ec"
checked_at: 2026-06-11
derived_from:
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/xxiivv-oscean-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: medium
borrow_order: P3
routing_hint:
  - static-wiki-generator
  - plain-text-tables
  - generated-link-map
fit_layer:
  - capture-provenance
  - publishing
  - maintenance
  - activation
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - automatic-truth-update
avoid:
  - "Do not import the idiosyncratic VM/toolchain as a VAKS dependency."
  - "Do not treat generated maps or logs as reviewed relations."
  - "Do not import personal wiki content as VAKS knowledge."
dev_context_hint:
  default_layer: cold-reference
  core_only_when: "When designing constrained static publishing or source-to-generated-index flows."
  support_when: "When comparing generated link maps, chronological logs, or plain-text table sources."
  risk_when: "When generated relation maps could be mistaken for reviewed relation evidence."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/xxiivv-oscean-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - static-wiki
  - generated-index
---

# Strong Candidate Distillation: XXIIVV / oscean

## Boundary

This file extracts publishing and maintenance mechanics from Oscean. It does not
adopt the content, the Uxn toolchain, or generated link maps as reviewed VAKS
relations.

## What This Source Actually Is

Oscean is a static wiki/site built around a small custom toolchain. The README
states that the site is written in Uxntal for the Uxn virtual machine and that
its plain-text tables are designed to fit within memory constraints. The repo
contains source code, generated site output, media, links, docs, and a makefile
that builds ROMs and generated indexes.

For VAKS, this is a cold-reference publishing source: useful for thinking about
plain-text source tables and generated maps, not as a content model.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Explains Oscean identity, Uxn/Uxntal implementation, plain-text tables, build commands, and licenses. | Source identity and constrained publishing philosophy. | VM choice is not a VAKS dependency. |
| `makefile` | Builds ROMs, generated link XML, docs index, and site output. | Generated outputs can be reproducible artifacts. | Generated site is not source of truth. |
| `src/` | Source program and table handling. | Source-to-site compilation. | Do not copy implementation. |
| `links/tw.txt` | Chronological event/link feed. | Timeline feeds can retain episode provenance. | Timeline entries are not reviewed evidence. |
| `site/` | Generated rendered pages. | Output can be inspected separately from source. | Do not edit generated projection. |

## Strong Borrow Points

1. **Generated projections should stay visibly separate from source.**  
   Oscean has source, tables, generated links, and rendered site files. VAKS
   should preserve this separation between source records, candidate
   distillation, indexes, and published projections.

2. **Plain-text tables can be good when constraints are explicit.**  
   The memory-constrained table design is extreme, but the principle is useful:
   simple source formats remain durable when their constraints are documented.

3. **Chronological link feeds are useful provenance, not truth.**  
   `links/tw.txt` is a timeline-style feed. VAKS can borrow timeline/event
   capture for source episodes while keeping evidence support separate.

4. **Build recipes can regenerate derived navigation.**  
   The makefile creates link maps and indexes. VAKS can borrow the idea for
   maintenance indexes, with a hard boundary that generated relations are not
   reviewed relations.

5. **Code and media licenses need separate treatment.**  
   The repo distinguishes source code license from media/content license. VAKS
   should preserve license/source type per artifact, especially for public
   publishing.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Provenance | Timeline and source tables. | Source episode records. |
| Activation | Generated maps and indexes. | Retrieval/navigation aids only. |
| Publishing | Static projection from source. | Derived output. |
| Maintenance | Build recipe and inspectable generated artifacts. | Rebuild/check lane. |
| Risk / Inhibition | License split and generated relation confusion. | Boundary warnings. |

## Local De-Dup / Collision

This overlaps with Grimgrains and 100r.co:

- Grimgrains and 100r.co show C/static-site authoring patterns.
- Oscean is more constrained and VM/toolchain-specific.

The unique borrow is the explicit constrained plain-text table model plus
generated link-map/log separation.

## Anti-Borrow

- Do not adopt Uxn/Uxntal for VAKS.
- Do not treat generated link maps as reviewed relations.
- Do not import personal content or media.
- Do not assume generated HTML is the canonical source.

## Candidate Tags

```yaml
domain: constrained_static_wiki_publishing
problem: preserving_plain_text_sources_while_generating_navigation
pattern:
  - source-generated-output-separation
  - plain-text-table-source
  - generated-link-map
  - chronological-link-feed
  - license-split
maturity: active-personal-site
problem_fit: 3
reuse_value: 3
implementation_cost: 4
integration_fit: 3
evidence_strength: 4
reversibility: 4
```

## Fusion Judgment

Borrow selectively for source/projection separation, generated indexes, and
license discipline. Keep it cold because the implementation stack is deliberately
idiosyncratic.
