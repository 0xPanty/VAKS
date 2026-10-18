---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/clarklab/chowdown"
repo_key: "clarklab/chowdown"
checked_commit: "48d56ea7a0115f722653dac6466b861f7eed4ca3"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/clarklab-chowdown-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/clarklab-chowdown-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/clarklab-chowdown-anchor-manifest.json
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
  - componentized-markdown-records
  - generated-search-index
fit_layer:
  - candidate-comprehension
  - association
  - activation
  - publishing
  - source-hygiene
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - reviewed-relations
avoid:
  - "Do not treat component references as reviewed relations."
  - "Do not treat search JSON or schema.org markup as evidence support."
  - "Do not copy recipe tags into VAKS taxonomy."
dev_context_hint:
  default_layer: support
  core_only_when: "When designing composable candidate records, generated activation indexes, or Markdown collection rendering."
  support_when: "When comparing component records, search-index generation, and source/render separation."
  risk_when: "When rendered schema or search output could be mistaken for reviewed knowledge."
  cold_references:
    - raw/repos/2026-06-11-awesome-obsidian-vault/clarklab-chowdown-source.md
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/clarklab-chowdown-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - component-records
  - search-index
---

# Strong Candidate Distillation: clarklab / chowdown

## Boundary

This file extracts VAKS design lessons from Chowdown's collection mechanics. It
does not promote recipe content, rendered schema markup, tags, or generated
search records to reviewed knowledge.

## What This Source Actually Is

Chowdown is a Jekyll-based plaintext recipe database. Recipes live in
`_recipes/`, reusable sub-recipes live in `_components/`, and layouts render
those records into a website with tags, images, credits, schema.org Recipe
microdata, and a generated search JSON endpoint.

For VAKS, the value is composable Markdown records and generated activation
surfaces over a simple file collection.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `readme.md` | Explains Jekyll build, recipe frontmatter, ingredients/directions, and component recipes. | Contributor-facing source contract. | Not a review protocol. |
| `_config.yml` | Declares recipes/components as output collections and translation labels. | Explicit collection boundaries. | Collection membership is not truth. |
| `_recipes/red-berry-tart.md` | A recipe assembled from components. | Composition can be represented by references. | Composition is candidate structure only. |
| `_components/graham-cracker-crust.md` | Reusable component note with its own ingredients and directions. | Reusable sub-record pattern. | Sub-record reuse is not evidence support. |
| `_layouts/recipe.html` | Renders ingredients, directions, components, tags, images, and schema.org microdata. | Rendering contract separates source fields from page view. | Rendered markup is not authority. |
| `search.json` | Emits search records from recipes. | Search index as activation cache. | Search hit is not review. |

## Strong Borrow Points

1. **Composable candidate records.**  
   Component recipes show how one note can include smaller source records without
   duplicating their contents. VAKS can borrow this for candidate bundles:
   evidence packets, risks, and source anchors can be referenced instead of
   pasted repeatedly.

2. **Collection boundaries can stay simple.**  
   `_recipes` and `_components` are easy to understand. VAKS can use this as a
   reminder that folder-level lanes should be plain when they are only capture or
   workbench lanes.

3. **Generated search indexes should be declared as caches.**  
   `search.json` emits title, ingredients, tags, URL, image, and description.
   VAKS can borrow the generated-cache idea for activation, but every generated
   search record must point back to canonical Markdown.

4. **Rendering can add structured markup without changing source truth.**  
   Schema.org microdata is useful for websites. In VAKS terms, rendered metadata
   can improve publishing or retrieval, but it must not rewrite source records or
   create reviewed relations.

5. **Image credits belong close to media rendering.**  
   Chowdown records `imagecredit` and renders credit links. VAKS should preserve
   the same principle for screenshots, diagrams, and retained source media.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Candidate Comprehension | Recipe/component split models composable notes. | Candidate bundles only. |
| Association / Activation | Tags and search JSON activate related records. | Activation cache. |
| Source Hygiene | Image credit field. | Media provenance field. |
| Publishing | Layout adds schema.org markup. | Downstream render only. |
| Context Pack | Components can be assembled on demand. | Must keep source pointers. |

## Local De-Dup / Collision

This overlaps with `dpapathanasiou/recipes` on generated search/index surfaces,
and with `based.cooking` on simple Markdown recipes. Chowdown's distinct value
is component composition: canonical notes can stay small while rendered views
assemble them.

For VAKS, this is useful for context-pack assembly and activation indexes, not
for reviewed relation creation.

## Anti-Borrow

- Do not treat component inclusion as a reviewed relation.
- Do not treat schema.org output as evidence support.
- Do not make search JSON a second source of truth.
- Do not copy recipe categories as VAKS concepts.

## Candidate Tags

```yaml
domain: jekyll_markdown_collection
problem: compose_small_markdown_records_into_readable_generated_pages
pattern:
  - component-record-reference
  - collection-boundary-as-folder
  - generated-search-cache
  - render-structured-markup-downstream
  - media-credit-near-render
maturity: small-working-static-site
problem_fit: 4
reuse_value: 4
implementation_cost: 2
integration_fit: 4
evidence_strength: 4
reversibility: 5
```

## Fusion Judgment

Borrow as a P3 support reference for composable candidate records and generated
activation caches. Keep all component links and rendered schema in the
activation/publish layer.
