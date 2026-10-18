---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/rekkabell/kokorobot"
repo_key: "rekkabell/kokorobot"
checked_commit: "8ac603595f0b936d1a34055912ccaca7ed5c7482"
checked_at: 2026-06-11
derived_from:
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/rekkabell-kokorobot-anchor-manifest.json
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
  - personal-site-generator
  - image-feed
  - case-collision-risk
fit_layer:
  - publishing
  - maintenance
  - capture-provenance
  - risk-inhibition
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - automatic-truth-update
avoid:
  - "Do not import art/media/content."
  - "Do not treat generated public folders as source."
  - "Do not ignore case-collision risks on Windows."
dev_context_hint:
  default_layer: cold-reference
  core_only_when: "When designing media/source publishing checks or Windows path safety checks."
  support_when: "When comparing small static site generators with media feeds."
  risk_when: "When source archives contain case collisions or generated public copies."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/rekkabell-kokorobot-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - static-site
  - path-risk
---

# Strong Candidate Distillation: rekkabell / kokorobot

## Boundary

This file extracts site-generation and media/provenance lessons from the
kokorobot repository. It does not import art, images, personal content, or
generated public output into VAKS.

## What This Source Actually Is

This is a personal art/site source repository with media, generated public/site
folders, link feeds, a C static site generator, image feed generation, edit
links, social/no-AI widgets, and separate code/content licenses.

The local checkout also exposed Windows case-insensitive path collisions in
media files. That makes the repo useful as a path-safety and generated-output
boundary example.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Identifies site source and license split. | Public source identity and licensing. | Content not imported. |
| `makefile` | Builds site, image page, and directory listing. | Media-heavy static generation. | Generated output is projection. |
| `src/main.c` | Source-to-site generator with edit links, footer widgets, template injection, index, and inspect behavior. | Publishing affordances and maintenance checks. | Not core VAKS engine. |
| `links/img.xml` | Image RSS feed with dated entries. | Media episode feed. | Images/descriptions are not VAKS evidence. |
| `media/` and `public/` | Source media and generated/public copies. | Need source/projection separation and path checks. | Do not duplicate generated media. |

## Strong Borrow Points

1. **Path safety is part of source intake.**  
   The clone produced case-collision warnings on Windows. VAKS should record
   path/case hazards for source archives and avoid assuming a clean checkout.

2. **Generated public copies must not be confused with source.**  
   The repo contains source media and generated/public output. VAKS should keep
   retained source, candidate notes, and projections clearly separated.

3. **Media feeds can act as provenance episodes.**  
   `links/img.xml` gives dated image entries. VAKS can borrow a media/source
   episode shape, but not treat media captions as evidence support.

4. **Edit links and footer metadata help public accountability.**  
   The generator writes source/edit affordances and license/social widgets.
   VAKS can expose source lineage in public projections.

5. **No-AI/content-license signals belong in risk metadata.**  
   The site has content/asset licensing and no-AI style affordances. VAKS should
   preserve licensing and use restrictions when distilling public sources.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Provenance | Image/feed episodes and source license. | Source card metadata. |
| Publishing | Static generation and public projection. | Derived output. |
| Maintenance | Case-collision warning and generated/source split. | Intake lint. |
| Activation | Index and edit/source affordances. | Navigation only. |
| Risk / Inhibition | Media rights and path collision risk. | Safety flags. |

## Local De-Dup / Collision

This overlaps with 100r.co and Grimgrains:

- 100r.co is stronger for orphan/reference inspection.
- Grimgrains is stronger for recipe/plain-content extraction.
- Kokorobot is strongest for media-heavy source/projection separation and
  case-collision risk.

## Anti-Borrow

- Do not import images or personal artwork.
- Do not treat generated `public` or `site` folders as canonical source.
- Do not ignore case-sensitive filename collisions when cloning on Windows.
- Do not make no-AI/license widgets substitute for source review.

## Candidate Tags

```yaml
domain: media_heavy_static_site_source
problem: preserving_source_projection_and_path_boundaries_for_media_sites
pattern:
  - case-collision-source-lint
  - media-episode-feed
  - generated-public-copy-boundary
  - edit-source-affordance
  - license-use-restriction-metadata
maturity: active-personal-site
problem_fit: 3
reuse_value: 3
implementation_cost: 2
integration_fit: 3
evidence_strength: 4
reversibility: 5
```

## Fusion Judgment

Borrow moderately for path-safety and media/projection boundary checks. Keep it
cold for VAKS core architecture.
