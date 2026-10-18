---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "groepl/Obsidian-Templates"
source_url: "https://github.com/groepl/Obsidian-Templates"
checked_commit: "d815ef9275ce7d0c5ea2e4dc2fdabb1d71182a83"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/groepl-obsidian-templates-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/groepl-obsidian-templates-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/groepl-obsidian-templates-anchor-manifest.json
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
  - template_health_views
fit_layer:
  - templates
  - vault-health
  - workbench
  - activation
  - source-hygiene
not_fit_layer:
  - reviewed-knowledge
  - action-basis
avoid:
  - "Do not copy the Zettelkasten ontology or folder model into VAKS."
  - "Do not treat Dataview maintenance results as evidence review."
  - "Do not adopt inactive or sprawling plugin dependencies without separate plugin review."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing VAKS template families or vault-health diagnostic views."
  support_when: "When comparing template metadata, template snippets, or missing-link/tag/task maintenance views."
  risk_when: "When Dataview dashboards or plugin dependencies could be mistaken for reviewed knowledge."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/groepl-obsidian-templates-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - templates
  - vault-health
---

# Strong Candidate Distillation: groepl / Obsidian-Templates

## What This Source Actually Is

This is a broad Obsidian template collection for Zettelkasten-oriented personal
knowledge management. Its strongest VAKS value is not the ontology itself, but
the combination of typed templates, template versioning, reusable snippets, and
maintenance views.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Workflow description and plugin requirements. | Dependencies and stale plugin notes should be explicit. | Plugin list is not approval. |
| `Templates/*.md` | Many note/template families. | Typed templates and snippets can reduce repeated structure. | Template text is not truth. |
| `5_Structure Notes/*.md` | Maintenance dashboards for tags, links, tasks, orphans, timestamps, stale notes. | Health views can surface review pressure. | Dataview output is diagnostic only. |
| `EXAMPLES.md` | Example usage. | Templates need usage context. | Examples are not architecture proof. |
| README plugin sections | Mandatory/optional plugin split and stale plugin warning. | Plugin runtime state belongs in source hygiene. | Requires separate plugin review. |

## Strong Borrow Points

1. **Template families should be typed and versioned.**  
   The templates expose fields such as template type/version. VAKS can borrow
   this for user-facing templates and maintenance fixtures so future changes do
   not silently mix old and new record shapes.

2. **Vault-health views are high-value diagnostics.**  
   The structure notes for missing tags, timestamps, links, in-links, out-links,
   unresolved links, and stale permanent notes map well to VAKS health checks.
   They should create review pressure or cleanup tasks, not truth changes.

3. **Snippets are a useful middle layer.**  
   Reusable front/back matter snippets are worth borrowing for VAKS templates
   where repeated metadata needs to stay consistent without adding a new system.

4. **Plugin dependency disclosure is part of source hygiene.**  
   The mandatory/optional plugin list and stale plugin warning are directly
   useful for future Obsidian workbench docs.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Templates | Typed templates, versioning, snippets. | Strong adaptation. |
| Vault Health | Missing metadata/link/task diagnostics. | Strong diagnostic pattern. |
| Activation | Structure notes as workbench views. | Adapt. |
| Review Queue | Health findings can become review pressure. | Candidate only. |
| Risk | Plugin sprawl and inactive plugin dependency. | Required warning. |

## Local De-Dup / Collision

This overlaps with DashboardPlusPlus and other Obsidian template vaults, but it
adds a distinct value: diagnostic structure notes. It should be deduped under a
future vault-health pattern rather than copied as another folder taxonomy.

## Fusion Judgment

Borrow strongly as P2 for template governance and vault-health diagnostics.
Reject the ontology and plugin bundle as direct imports.
