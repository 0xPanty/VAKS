---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/hundredrabbits/100r.co"
repo_key: "hundredrabbits/100r.co"
checked_commit: "951d91d6e6c4c0b5f3605fd00bf090719c5e1534"
checked_at: 2026-06-11
derived_from:
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/hundredrabbits-100r-co-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: high
borrow_order: P3
routing_hint:
  - static-site-generator
  - orphan-detection
  - edit-link-affordance
fit_layer:
  - publishing
  - maintenance
  - activation
  - capture-provenance
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - automatic-truth-update
avoid:
  - "Do not copy the C generator as core VAKS infrastructure."
  - "Do not treat generated references as reviewed relation support."
  - "Do not import project content or assets."
dev_context_hint:
  default_layer: support
  core_only_when: "When designing a tiny generated projection or orphan-page check for Markdown sources."
  support_when: "When comparing source-to-site publishing affordances."
  risk_when: "When generated navigation could be mistaken for reviewed knowledge structure."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/hundredrabbits-100r-co-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - static-site
  - orphan-detection
---

# Strong Candidate Distillation: hundredrabbits / 100r.co

## Boundary

This file extracts source-to-site mechanics from the Hundred Rabbits website
repository. It does not import project content, media, or the C implementation
as VAKS core architecture.

## What This Source Actually Is

This is the source for the Hundred Rabbits website. It uses a small C static
site generator with `src`, `site`, `media`, `links`, a makefile, generated index
behavior, edit links, orphan inspection, RSS, and separate code/content licenses.

For VAKS, this is useful because it shows how a simple source tree can generate
a public site while still making edits and maintenance visible.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Identifies source repo, C build, license split, and contribution path. | Static site source identity. | Site content not imported. |
| `makefile` | Builds `site` and binary from source. | Reproducible projection. | Build stack not adopted. |
| `src/main.c` | Template injection, link normalization, generated index, edit links, footer, orphan inspection. | Minimal publishing/maintenance mechanics. | Generated references are not truth relations. |
| `links/rss.xml` | Update feed for site/project changes. | Public change log can aid source episode tracking. | RSS entries are provenance, not support. |
| `site/` | Generated output. | Rendered projection separate from source. | Do not edit generated projection. |

## Strong Borrow Points

1. **Every rendered page can expose an edit/source affordance.**  
   The generator writes edit links back to the source. VAKS public views should
   make source/candidate/review lineage easy to inspect.

2. **Generated-file warnings reduce projection confusion.**  
   The generated pages identify themselves as generated output. VAKS indexes and
   published projections should similarly avoid pretending to be canonical truth.

3. **Orphan inspection is a cheap but useful vault-health check.**  
   The generator tracks references and warns on orphan pages. VAKS can borrow
   this as maintenance lint, not as relation validation.

4. **Local link normalization protects publishing stability.**  
   Title-to-filename normalization and local link handling keep the site
   navigable. VAKS can borrow this for generated static projections.

5. **RSS/change feeds can become source episodes.**  
   A feed of updates is useful for provenance and reactivation. It should not be
   treated as evidence support for individual claims.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Provenance | RSS/change events and edit links. | Source episode trace. |
| Activation | References counter and index. | Navigation hints. |
| Publishing | Generated static site. | Projection layer only. |
| Maintenance | Orphan inspection and generated warnings. | Vault health lint. |
| Risk / Inhibition | License split and generated relation confusion. | Boundary warnings. |

## Local De-Dup / Collision

This overlaps with Grimgrains and kokorobot:

- Grimgrains covers recipe-focused minimalist source publishing.
- kokorobot adds art/image feed and case-collision risks.
- 100r.co is strongest for source edit affordances, generated index, and orphan
  inspection.

The unique borrow is a small, inspectable publishing loop with visible source
links and orphan detection.

## Anti-Borrow

- Do not adopt the C generator as VAKS infrastructure.
- Do not use reference counts as confidence or relation review.
- Do not import project pages or assets.
- Do not treat RSS updates as evidence support.

## Candidate Tags

```yaml
domain: minimalist_static_site_generation
problem: publishing_a_source_tree_without_hiding_source_lineage
pattern:
  - generated-file-warning
  - edit-source-link
  - local-link-normalization
  - orphan-page-inspection
  - rss-source-episode-feed
maturity: active-public-site
problem_fit: 4
reuse_value: 5
implementation_cost: 2
integration_fit: 4
evidence_strength: 4
reversibility: 5
```

## Fusion Judgment

Borrow strongly for publishing and maintenance affordances. Keep generated
navigation out of reviewed knowledge.
