---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/hundredrabbits/Grimgrains"
repo_key: "hundredrabbits/Grimgrains"
checked_commit: "8e39b292837f3889bb591e4c10fd2ec09af93866"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/hundredrabbits-grimgrains-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/hundredrabbits-grimgrains-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/hundredrabbits-grimgrains-anchor-manifest.json
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
  - typed-content-model
  - generated-site-from-source
fit_layer:
  - candidate-comprehension
  - association
  - activation
  - source-hygiene
  - publishing
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - markdown-mainline-schema
avoid:
  - "Do not replace VAKS Markdown source-of-truth with a C content generator."
  - "Do not treat generated crosslinks or ingredient descriptions as reviewed relations."
  - "Do not import recipe or nutrition content as evidence."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing optional typed extraction helpers, generated crosslink checks, or strict lint for generated workbench outputs."
  support_when: "When comparing content-as-code, ontology side records, and generated static surfaces."
  risk_when: "When code generation could move VAKS away from human-readable Markdown authority."
  cold_references:
    - raw/repos/2026-06-11-awesome-obsidian-vault/hundredrabbits-grimgrains-source.md
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/hundredrabbits-grimgrains-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - content-as-code
  - generated-links
---

# Strong Candidate Distillation: hundredrabbits / Grimgrains

## Boundary

This file extracts architectural ideas from the repository mechanics. It does
not adopt the C generator, the recipe content, ingredient statements, or
generated links as VAKS reviewed knowledge.

## What This Source Actually Is

Grimgrains is a recipe website whose content is authored as C declarations and
constructor calls. A build script formats and compiles the C source, runs the
generator, and produces a static website. Recipes, ingredients, serving
quantities, parts, instructions, and crosslinks are represented as typed source
objects.

For VAKS, this is valuable as an extreme contrast case: it shows the benefits of
typed content, but also the cost of moving human knowledge into a programming
language.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | States that the site source is written in C and built with `gcc`. | Strong source/build separation. | Not a model for normal VAKS authoring. |
| `src/main.c` | Defines content structures and constructor helpers. | Shows a typed internal model for generated pages. | Internal model is not Markdown truth. |
| `src/recipes.c` | Recipe entries use `create_recipe`, `create_part`, `add_instruction`, and linked ingredients. | Content atoms are explicit and machine-checkable. | Constructor calls are too rigid for VAKS notes. |
| `src/ingredients.c` | Ingredient records and child ingredients create a linked ingredient graph. | Side ontology can support navigation and consistency. | Extracted links are not reviewed relations. |
| `src/build.sh` | Runs formatter, strict compiler flags, sanitizers, generator, and cleanup. | Generated workbench outputs deserve strict build checks. | Build success is maintenance evidence only. |

## Strong Borrow Points

1. **Typed intermediary, not typed source-of-truth.**  
   The repository proves that typed content objects make generated outputs
   consistent. VAKS should borrow this only as an optional compiler/checker idea:
   Markdown remains source, typed objects may be derived for linting and
   publishing.

2. **Separate entities from procedural content.**  
   Ingredients are side records while recipes refer to them. VAKS can adapt the
   principle for source entities, reviewed concepts, and candidate points: do not
   duplicate entity definitions inside every note.

3. **Crosslinks can be generated from structured references.**  
   Recipe instructions link ingredients directly. VAKS can borrow this for
   candidate workbench views where source anchors, candidate points, risks, and
   related concepts are generated from explicit references.

4. **Generated outputs should have a strict maintenance gate.**  
   `build.sh` uses formatting, warnings, and sanitizers before output generation.
   For VAKS, generated indexes or dashboards should have lint/hash checks before
   sync, while still staying outside reviewed truth.

5. **Output count and asset count are separate from knowledge quality.**  
   The repo has many generated pages and media files, but those counts do not
   prove correctness. VAKS should keep volume/coverage dashboards as maintenance
   signals only.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Candidate Comprehension | Typed intermediate objects can normalize extracted points. | Optional derived model only. |
| Association / Activation | Crosslinks and side entities improve browsing. | Activation links only. |
| Source Hygiene | Strict build/lint around generated outputs. | Maintenance manifest input. |
| Publishing | Generated site from source declarations. | Reference for compiler-style export. |
| Risk / Inhibition | Code-as-content is hard to review by humans. | Anti-borrow warning. |

## Local De-Dup / Collision

This overlaps with `dpapathanasiou/recipes` on structured recipe data. The
distinction is important:

- Grimgrains shows a typed generator and ontology-style crosslinks.
- `dpapathanasiou/recipes` shows large JSON records and generated component
  indexes.
- VAKS should borrow neither as source-of-truth; both are support references for
  derived indexes and lintable workbench outputs.

## Anti-Borrow

- Do not make VAKS notes require C or another programming language.
- Do not treat generated crosslinks as reviewed relations.
- Do not count build success, page count, or asset count as truth confidence.
- Do not import ingredient/nutrition descriptions as evidence.

## Candidate Tags

```yaml
domain: typed_static_content_generator
problem: produce_consistent_generated_pages_from_structured_source_objects
pattern:
  - typed-derived-content-model
  - side-entity-records
  - generated-crosslink-workbench
  - strict-build-before-publish
  - human-readability-risk
maturity: mature-niche-generator
problem_fit: 3
reuse_value: 4
implementation_cost: 4
integration_fit: 2
evidence_strength: 4
reversibility: 3
```

## Fusion Judgment

Borrow as a P3 support/risk reference. It is useful for thinking about derived
typed layers, but VAKS should keep Markdown as the human-readable authority and
use typed generation only downstream.
