---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "rstacruz/cheatsheets"
source_url: "https://github.com/rstacruz/cheatsheets/tree/master#documentation"
checked_commit: "6b3b35472a9b6dee90645ea0a833731855a1914d"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/rstacruz-cheatsheets-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/rstacruz-cheatsheets-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/rstacruz-cheatsheets-anchor-manifest.json
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
  - atomic_reference_pages
fit_layer:
  - capture
  - source-scouting
  - activation
  - publishing
  - source-hygiene
not_fit_layer:
  - reviewed-knowledge
  - evidence-support
  - action-basis
avoid:
  - "Do not treat cheatsheet brevity as evidence sufficiency."
  - "Do not let search index, related posts, or popularity signals imply truth."
  - "Do not store source URLs with tree/hash fragments when the repo root is needed for reproducible inspection."
dev_context_hint:
  default_layer: support
  core_only_when: "When designing short reference cards, source-directory cards, or publication/search projections."
  support_when: "When comparing atomic Markdown page structure, frontmatter governance, redirects, tests, and search index generation."
  risk_when: "When concise lookup pages could be mistaken for reviewed evidence."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/rstacruz-cheatsheets-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - reference-cards
  - publishing
---

# Strong Candidate Distillation: rstacruz / cheatsheets

## What This Source Actually Is

This is Devhints: a large, public collection of short developer cheatsheets.
It stores many topic pages as root Markdown files and publishes them through an
Astro-based site with search, SEO, redirects, tests, formatting, and contribution
rules.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | TLDR-style documentation collection. | Short reference cards can be useful for fast lookup. | Lookup is not review. |
| `CONTRIBUTING.md` | Runtime, frontmatter, redirects, localization, tests, publishing notes. | Contribution rules and metadata policy should be explicit. | Contributor process is not truth. |
| Root `*.md` sheets | Many atomic topic pages. | One-topic pages are easy to index and reuse. | Page content is unreviewed by VAKS. |
| `src/lib/page*` | Page loading/query model. | Markdown can remain canonical while projections query it. | Query output is not authority. |
| `src/lib/fuseSearch/*` and `searchindex.json.ts` | Search projection. | Fast activation/search layer. | Search ranking is not support. |
| `astro.config.mjs` and `package.json` | Build/test/format/publish runtime. | Publishing pipeline should be reproducible. | Build success is not truth. |

## Strong Borrow Points

1. **Atomic reference cards are useful when kept narrow.**  
   VAKS can borrow the one-topic page discipline for quick-reference surfaces,
   especially command/config snippets and architecture glossary cards.

2. **Frontmatter policy belongs in contribution docs.**  
   The contribution guide documents fields such as title, category, updated,
   deprecated, redirects, and special pages. VAKS should keep similar metadata
   policy close to any public template or source-card system.

3. **Search should be generated from canonical Markdown.**  
   The site builds search from source pages. This fits VAKS: search/activation
   can be generated, while Markdown records remain the durable layer.

4. **Redirects and deprecation are first-class hygiene.**  
   Redirect/deprecated metadata is useful for VAKS supersession and stale-source
   handling, but it must route review pressure rather than silently replace
   reviewed knowledge.

5. **Source URL normalization is required.**  
   The awesome-list link pointed into a page fragment. Strong intake had to
   normalize to the repo root for reproducible clone/inspection.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture | Atomic topic pages and metadata. | Adapt. |
| Activation | Search index and related pages. | Projection only. |
| Publishing | Astro build/test pipeline. | Reference only. |
| Review Queue | Deprecation/redirect can create review pressure. | Candidate only. |
| Risk | Cheatsheet brevity can hide missing evidence. | Required warning. |

## Local De-Dup / Collision

This overlaps with ByteByteGo and docs repos as public documentation examples.
Its distinct value is the short-card lookup model plus frontmatter/redirect
governance, not long-form architecture review.

## Fusion Judgment

Borrow as P2 for quick-reference cards, metadata governance, redirects, and
search projection. Do not use cheatsheets as evidence support.
