---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "CyanVoxel/Obsidian-Vault-Template"
source_url: "https://github.com/CyanVoxel/Obsidian-Vault-Template"
checked_commit: "9277193c6b5bc53f5e020fa2e947eda0be767dcf"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/cyanvoxel-obsidian-vault-template-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/cyanvoxel-obsidian-vault-template-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/cyanvoxel-obsidian-vault-template-anchor-manifest.json
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
  - vault_template_reference
fit_layer:
  - workbench
  - activation
  - templates
  - dev-context
  - source-hygiene
not_fit_layer:
  - reviewed-knowledge
  - action-basis
avoid:
  - "Do not copy the template's folder taxonomy or plugin bundle into VAKS wholesale."
  - "Do not treat aesthetic/theming choices as architecture."
  - "Do not ignore the source's own stale/update warning."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing a VAKS template vault, onboarding fixture, or Obsidian environment capture."
  support_when: "When comparing MOC/Projects/Areas/Resources/Permanent/Fleeting/Daily/Archive folder templates and plugin dependency surfaces."
  risk_when: "When template polish or bundled plugins could be mistaken for VAKS reviewed structure."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/cyanvoxel-obsidian-vault-template-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - vault-template
---

# Strong Candidate Distillation: CyanVoxel / Obsidian-Vault-Template

## What This Source Actually Is

This is a scrubbed Obsidian vault template with folder structure, plugin
configuration, templates, CSS/icons, and presentation assets. The README itself
warns that it is not updated often and recommends users build their own vault
from default configurations over time.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Template identity and stale/update warning. | A template should disclose update expectations. | Template age limits reuse. |
| `Vault/.obsidian/community-plugins.json` | Lists many community plugin dependencies. | Plugin dependency surface should be explicit. | Plugin list is not approval. |
| `Vault/.obsidian/core-plugins.json` | Core plugin configuration. | Environment state belongs in template provenance. | Config is not truth. |
| Top-level `Vault/` folders | MOCs, Projects, Areas, Resources, Permanent, Fleeting, Daily, Archives, Meta. | Good onboarding scaffold for a generic vault. | Not VAKS schema. |
| `Vault/99 - Meta/00 - Templates/*.md` | Daily/Unique note templates. | Templates belong in a meta area and should be visible. | Template text is not reviewed knowledge. |

## Strong Borrow Points

1. **Template vaults should be honest about staleness.**  
   The README's warning is valuable: VAKS should mark template/source freshness
   and avoid treating old vault templates as current practice.

2. **Folder scaffold can help onboarding, not core architecture.**  
   The MOC/Projects/Areas/Resources/Permanent/Fleeting/Daily/Archives layout is
   useful as a comparison point for onboarding or sandbox fixtures, but VAKS
   already has stricter candidate/review/truth boundaries.

3. **Plugin dependency surface must be captured.**  
   The template bundles many plugins. VAKS should record dependencies for any
   formal Obsidian template or dashboard and require separate plugin/runtime
   review before adoption.

4. **Meta/template area is useful.**  
   Keeping templates under a visible `99 - Meta` area is a simple pattern VAKS
   can borrow for future user-facing templates, while keeping project-development
   templates separate.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture | Plugin/core config in source card. | Adapt. |
| Activation | MOCs and scaffold folders. | Optional workbench reference. |
| Templates | Meta/template folder organization. | Useful. |
| Dev Context | Environment reproduction. | Support. |
| Risk | Stale template and plugin bundle. | Required warning. |

## Local De-Dup / Collision

The shallow file marked this as `publishing_or_template_reference`. Strong
inspection confirms template value but adds stronger anti-borrow: the folder
layout and plugin bundle must not override VAKS's reviewed/candidate boundaries.

## Fusion Judgment

Adapt lightly as P2 for template/onboarding design and plugin-dependency
recording. Do not copy the template wholesale.
