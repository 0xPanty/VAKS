---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "uroybd/topobon"
source_url: "https://github.com/uroybd/topobon"
checked_commit: "b1a9043f7c7dcdc69de329bbc0497feccc2a0570"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/uroybd-topobon-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/uroybd-topobon-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/uroybd-topobon-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: medium
borrow_order: P2
routing_hint:
  - customized_publishing_projection
fit_layer:
  - publishing
  - workbench
  - source-hygiene
  - risk
not_fit_layer:
  - canonical-markdown
  - reviewed-knowledge
  - reviewed-relations
  - action-basis
avoid:
  - "Do not copy personal published notes or theme decisions into VAKS."
  - "Do not treat Bases, Canvas, graph, or component output as reviewed knowledge."
  - "Do not ignore invalid Windows paths or cross-platform filename risk."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing advanced VAKS publishing projection components or path-portability checks."
  support_when: "When comparing Digital Garden customization, CSS variables, Bases/Canvas rendering, and site component injection."
  risk_when: "When published-vault repos contain personal content, generated views, or Windows-invalid paths."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/uroybd-topobon-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - publishing
  - source-hygiene
---

# Strong Candidate Distillation: uroybd / topobon

## What This Source Actually Is

This is a heavily customized Digital Garden / Eleventy publication repo for an
Obsidian vault. It contains public site components, helper code, theme variables,
Bases/Canvas rendering support, deployment config, patches, and personal
published content. Normal Windows checkout encountered an invalid filename,
which makes it especially useful as a source-hygiene risk example.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Digital garden identity and extensive style/customization manual. | Publishing layer can expose user-configurable surfaces. | Theme choices are not architecture. |
| `.eleventy.js` and `package.json` | Static-site build/runtime. | Publication remains a generated projection. | Build output is not canonical. |
| `src/helpers/bases-engine/*` | Bases-like query/rendering helpers. | Bases can be rendered as a projection. | Bases output is not reviewed knowledge. |
| `src/site/_includes/components/*` | Bases, Canvas, graph, search, filetree, and other components. | Rich site components can improve browsing. | UI output is activation only. |
| `Personal/Musings/Understood?.md` | Windows-invalid filename observed during checkout. | Published vault repos need path-portability audits. | Path failures limit retention and sync. |

## Strong Borrow Points

1. **Advanced publishing should stay outside the canonical vault.**  
   Topobon shows how far a public projection can go: Bases, Canvas, theme
   variables, components, random pages, and patches. VAKS should keep this
   power in the publishing layer, never in reviewed knowledge.

2. **User customization belongs in explicit projection settings.**  
   The extensive variables and component hooks are useful for a future public
   workbench/publishing layer where presentation needs to vary without changing
   source records.

3. **Bases rendering is valuable but dangerous if misread.**  
   Rendering Bases-like views can help browsing and dashboards, but the view is
   still a projection. It cannot create reviewed relations, confidence, or
   action basis.

4. **Path portability needs a real audit.**  
   The Windows-invalid filename is not theoretical. Any VAKS repo/publication
   sync should include filename portability checks before promising retention.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Publishing | Advanced static-site customization. | Adapt later. |
| Workbench | Bases/Canvas/search/filetree browsing. | Projection only. |
| Vault Health | Path portability checks. | Strong risk pattern. |
| Reviewed Knowledge | None directly. | Reject. |
| Risk | Personal content and invalid paths. | Required warning. |

## Local De-Dup / Collision

This overlaps with ThatOtherAndrew's digital garden template. Topobon is less
clean as a baseline but stronger as a stress test for customization, Bases
projection, and path-portability risk.

## Fusion Judgment

Use as P2 risk-rich publishing reference. Borrow path-portability and projection
guardrails before borrowing any advanced component ideas.
