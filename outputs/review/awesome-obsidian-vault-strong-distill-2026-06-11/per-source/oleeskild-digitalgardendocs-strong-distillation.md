---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "oleeskild/digitalgardendocs"
source_url: "https://github.com/oleeskild/digitalgardendocs"
checked_commit: "9af25f78cc32214fe7cb828876f7a94faaf8860b"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/oleeskild-digitalgardendocs-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/oleeskild-digitalgardendocs-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/oleeskild-digitalgardendocs-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: strong
borrow_order: P2
routing_hint:
  - digital_garden_publication_controls
fit_layer:
  - publishing
  - source-hygiene
  - activation
  - workbench
  - risk
not_fit_layer:
  - reviewed-knowledge
  - reviewed-relations
  - action-basis
avoid:
  - "Do not treat publication frontmatter as review approval."
  - "Do not treat graph, backlinks, search, Dataview, or Bases output as reviewed relations."
  - "Do not use broad access tokens or build hooks without security review."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing VAKS public publishing gates, note-level projection controls, or Obsidian Bases publication boundaries."
  support_when: "When comparing Digital Garden settings, CSS variables, build hooks, token scope, and published-note-only query limits."
  risk_when: "When published projections could leak candidate notes or be mistaken for evidence-aware review."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/oleeskild-digitalgardendocs-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - publishing
  - projection-boundary
---

# Strong Candidate Distillation: oleeskild / digitalgardendocs

## What This Source Actually Is

This is the documentation/template repository for publishing Obsidian notes with
the Digital Garden plugin. It is highly relevant to VAKS publication boundaries:
per-note settings, global defaults, build hooks, token scope, styling variables,
and published-note-only Bases behavior.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Template identity and CSS variable surface. | Publication presentation should be configurable. | Styling is not architecture. |
| `package.json` | Eleventy/Sass/build/test scripts. | Publishing runtime should be explicit. | Build output is not canonical. |
| `Getting Started/03 Note settings.md` | Global/note-specific search, graph, backlinks, TOC, filetree settings. | Projection controls need global defaults and note overrides. | Settings are not review approval. |
| `Advanced/Configure build pipeline.md` | User hooks for Eleventy and markdown-it. | Extension points should be named and isolated. | Hooks require review. |
| `Advanced/Fine grained access token.md` | Repo-scoped token guidance. | Credential scope belongs in publishing hygiene. | Token use needs security gate. |
| `Advanced/Obsidian Bases.md` | Bases queries run at build time against published notes only. | Published projection may differ from local vault. | Bases output is not reviewed knowledge. |

## Strong Borrow Points

1. **Publication controls need both global defaults and per-note overrides.**  
   VAKS should borrow this for future public/export layers: publish eligibility,
   graph/search/backlink display, and note-specific suppression must be explicit.

2. **Projection settings are not review status.**  
   The repo is a strong reminder that `published` means visible, not verified.
   VAKS must keep `publish_allowed` separate from `reviewed` and `action_basis`.

3. **Published-note-only query scope must be exposed.**  
   Bases queries on the public site only see published notes. VAKS should record
   query scope wherever a dashboard or base is generated from a subset.

4. **Build extension hooks need isolation.**  
   User Eleventy/markdown-it hooks are useful, but VAKS should treat extension
   points as plugin-like risk surfaces.

5. **Credential scope is part of source hygiene.**  
   Fine-grained repo tokens are directly relevant for any future publishing
   connector, especially to avoid broad account access.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Publishing | Per-note/global projection controls. | Strong adaptation. |
| Source Hygiene | Token scope and build hook boundaries. | Strong adaptation. |
| Activation | Search, graph, backlinks, filetree. | Projection only. |
| Workbench | Bases/public query views. | Scope-labeled projection. |
| Reviewed Relations | None directly. | Reject. |

## Local De-Dup / Collision

This supersedes generic digital-garden template signals for publication-control
details. Keep ThatOtherAndrew as baseline Eleventy projection, Topobon as stress
test, and this source as the strongest control-surface reference.

## Fusion Judgment

Borrow strongly as P2 for future publication/export controls and projection
scope labels. Do not let any public-site setting imply VAKS review.
