---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "ThatOtherAndrew/obsidian-digital-garden"
source_url: "https://github.com/ThatOtherAndrew/obsidian-digital-garden"
checked_commit: "9990f8ad0a35157cf96a436c381b3779087ffb5a"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/thatotherandrew-obsidian-digital-garden-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/thatotherandrew-obsidian-digital-garden-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/thatotherandrew-obsidian-digital-garden-anchor-manifest.json
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
  - publishing_projection
fit_layer:
  - publishing
  - workbench
  - activation
  - source-hygiene
not_fit_layer:
  - canonical-markdown
  - reviewed-knowledge
  - reviewed-relations
  - action-basis
avoid:
  - "Do not make the published static site the canonical VAKS source."
  - "Do not treat graph/search/backlink components as reviewed relations or support evidence."
  - "Do not publish candidate/private notes without explicit publication gates."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing VAKS publishing projection gates or Obsidian-to-static transform boundaries."
  support_when: "When comparing graph, search, filetree, backlink, callout, image, and table render projections."
  risk_when: "When publication output could leak notes or be mistaken for reviewed knowledge."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/thatotherandrew-obsidian-digital-garden-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - publishing
  - digital-garden
---

# Strong Candidate Distillation: ThatOtherAndrew / obsidian-digital-garden

## What This Source Actually Is

This is an Eleventy-based digital garden template for publishing Obsidian notes
through the Digital Garden plugin. It is useful to VAKS as a publication
projection reference: frontmatter gates, Obsidian syntax transforms, search,
graph, filetree, backlinks, and deployment scripts.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Digital Garden plugin and Vercel deployment template. | Publishing setup needs a clear runtime boundary. | Not a knowledge model. |
| `package.json` | Eleventy build/watch scripts and dependencies. | Build pipeline should be separate from canonical notes. | Build output is not canonical. |
| `.eleventy.js` | Link/tag/callout/image/table/Dataview transforms. | Obsidian-specific syntax needs explicit projection transforms. | Transform success is not truth. |
| `src/site/_includes/components/*.njk` | Search, graph, filetree, references, navbar, timestamps. | UI components are useful activation projections. | UI relations are not reviewed relations. |
| Published-note frontmatter fields | `dg-publish`, path, permalink controls. | Publication gates should be explicit and per note. | Gates are not review approval. |

## Strong Borrow Points

1. **Publication must be an explicit projection.**  
   The repo cleanly separates source notes from the Eleventy build. VAKS should
   preserve this boundary: canonical Markdown remains local; public output is a
   generated projection.

2. **Per-note publish gates are worth borrowing.**  
   Fields such as publish/path/permalink are directly useful for preventing
   accidental publication. VAKS can adapt this to public/export eligibility.

3. **Obsidian syntax transforms need their own layer.**  
   Links, tags, callouts, images, tables, and Dataview hiding are projection
   concerns. They should not mutate source records or reviewed knowledge.

4. **Graph/search/backlinks are activation UI only.**  
   These components help exploration, but cannot be treated as evidence,
   confidence, or reviewed relation creation.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Publishing | Explicit static-site projection. | Strong adaptation. |
| Source Hygiene | Per-note publish gates. | Strong adaptation. |
| Activation | Search, graph, filetree, backlinks. | Projection only. |
| Reviewed Relations | None directly. | Reject. |
| Risk | Privacy/candidate leakage. | Required gate. |

## Local De-Dup / Collision

This overlaps with Topobon and other digital-garden templates. This source is a
cleaner baseline for projection gates and Eleventy transforms; Topobon is more
customized and risk-heavy.

## Fusion Judgment

Borrow strongly as P2 for publishing boundary design. Keep all generated UI
outputs as projections, not VAKS truth.
