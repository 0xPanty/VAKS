---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "MaggieAppleton/digital-gardeners"
source_url: "https://github.com/MaggieAppleton/digital-gardeners"
checked_commit: "5bdd8509dc6e142a889d3343c8f8e1af674f287a"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/maggieappleton-digital-gardeners-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/maggieappleton-digital-gardeners-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/maggieappleton-digital-gardeners-anchor-manifest.json
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
  - digital_garden_directory
fit_layer:
  - source-scouting
  - publishing
  - workbench
  - activation
not_fit_layer:
  - reviewed-knowledge
  - evidence-support
  - action-basis
avoid:
  - "Do not treat directory inclusion or garden popularity as support for a VAKS design."
  - "Do not collapse digital-garden ethos into VAKS truth or review semantics."
  - "Do not import broad public link lists into reviewed knowledge without separate source intake."
dev_context_hint:
  default_layer: support
  core_only_when: "When designing a public source directory, reference catalog, or garden-style browsing projection."
  support_when: "When comparing how curated source catalogs expose examples, tools, theory, and searchable entries."
  risk_when: "When garden-style public curation could be mistaken for evidence-aware review."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/maggieappleton-digital-gardeners-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - digital-garden
---

# Strong Candidate Distillation: MaggieAppleton / digital-gardeners

## What This Source Actually Is

This repository is a public directory and resource site for digital gardens. It
combines curated examples, explanatory resources, tool references, MDX entries,
and a searchable Next.js projection.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Digital garden directory and resource framing. | Useful for source scouting categories. | Curation is not review. |
| `gardens/*.mdx` | Individual garden entries as content records. | Directory entries can be kept as structured source records. | Entry format is not VAKS schema. |
| `utils/mdxUtils.js` | Loads MDX garden files. | Canonical content can feed a projection. | Loader output is not truth. |
| `scripts/build-search.js` | Search index generation. | Search is a projection aid. | Search rank is not authority. |
| `pages/*.js` and `components/*` | Public browsing UI. | Directory cards and detail pages help exploration. | Public UI is not review. |

## Strong Borrow Points

1. **Use explicit source-scouting categories.**  
   The split between examples, tools, resources, and theory is a useful public
   directory pattern for VAKS source scouting and reference discovery.

2. **Keep catalog entries structured.**  
   MDX entries make each garden inspectable and individually renderable. VAKS
   can borrow the idea for source directory cards, while keeping raw source
   cards and candidate distillations separate.

3. **Generate searchable projections from canonical entries.**  
   The search build path is a good reminder that browsing/search outputs should
   be generated from source records rather than becoming the canonical layer.

4. **Public explanation can be lighter than internal review.**  
   The garden metaphor helps make knowledge work approachable, but VAKS should
   keep its stricter review language behind the scenes.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture | Curated external source directory. | Adapt. |
| Activation | Browsable cards and search. | Useful projection. |
| Publishing | Garden-style public explanation. | Lightly adapt. |
| Review | None directly. | Do not adopt. |
| Risk | Curation mistaken for support. | Required warning. |

## Local De-Dup / Collision

The shallow file treated this as a digital-garden/publishing reference. Strong
inspection narrows the useful part: source directory structure and projection
mechanics are reusable, while the garden ethos must not override VAKS evidence
discipline.

## Fusion Judgment

Use as P2 inspiration for source scouting, public directory pages, and garden
language. Do not borrow it as a knowledge-review model.
