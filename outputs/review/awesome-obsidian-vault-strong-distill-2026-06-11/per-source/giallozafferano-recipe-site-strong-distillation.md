---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://www.giallozafferano.com/"
repo_key: null
checked_commit: null
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/giallozafferano-recipe-site-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/giallozafferano-recipe-site-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/giallozafferano-recipe-site-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: low
borrow_order: P3
routing_hint:
  - editorial-site-structure
  - live-web-source-risk
fit_layer:
  - capture-provenance
  - candidate-comprehension
  - activation
  - publishing
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - source-code-reference
avoid:
  - "Do not treat live website rankings, ratings, or editorial claims as reviewed VAKS knowledge."
  - "Do not copy commercial content structure into VAKS mainline."
  - "Do not treat AI-translation disclosure as source support."
dev_context_hint:
  default_layer: risk
  core_only_when: "When designing source cards for live websites, editorial provenance fields, or page-structure capture."
  support_when: "When comparing publication surfaces, related-content modules, author/process disclosures, and policy links."
  risk_when: "When live pages, ratings, AI-translated text, or commercial editorial claims could be mistaken for stable evidence."
  cold_references:
    - raw/repos/2026-06-11-awesome-obsidian-vault/giallozafferano-recipe-site-source.md
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/giallozafferano-recipe-site-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - live-website
  - editorial-provenance
---

# Strong Candidate Distillation: Giallozafferano Recipe Site

## Boundary

This file extracts publication and live-source handling lessons. It does not
import recipe content, rankings, ratings, editorial claims, or translated text
into reviewed VAKS knowledge.

## What This Source Actually Is

Giallozafferano is a commercial recipe and food media website. The checked pages
show a rich publication surface: categories, latest recipes, curated
collections, editorial features, regional/theme blocks, recipe detail pages,
author/process disclosures, multilingual links, legal links, and a sample note
that some translated text may involve AI tools.

For VAKS, this is useful mainly as a live-web source risk and publication
surface reference.

## Web Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| Home page | Category navigation, latest recipes, curated collections, regional/theme blocks, ratings/time cards, editorial features. | Live sites provide many activation routes over content. | Navigation and ranking are not truth. |
| Sample recipe page | Category, badges, difficulty, prep time, serving, cost, author, ingredients, preparation, storage, tips, related recipes. | Detail page fields can guide live-source capture. | Recipe content is not VAKS evidence. |
| Recipe page translation note | Says AI tools may have been used for some text translation. | Translation/tool disclosure should be captured as provenance risk. | AI translation is not source support. |
| About page | Describes team, editorial selection, repeated testing, shoots, publishing, owner, and channels. | Editorial process is useful source-context metadata. | Process claim still needs trust assessment. |
| Footer/legal links | Terms, privacy, cookie policy, disclaimer, code of ethics, owner links. | Policy links belong in source cards for commercial sites. | Legal links do not prove content quality. |

## Strong Borrow Points

1. **Live website source cards need page-level anchors.**  
   A homepage, article page, about page, and policy links carry different
   provenance value. VAKS should capture them separately rather than storing only
   one URL.

2. **Publication modules are activation surfaces.**  
   Curated collections, latest lists, regional blocks, related recipes, and
   ratings help users browse. VAKS can borrow the idea for activation views, but
   not as evidence or reviewed relations.

3. **Editorial process should be captured as context, not proof.**  
   The about page describes testing and production workflow. VAKS should record
   such claims under source credibility/context, then still require evidence for
   any adopted point.

4. **Translation/tool disclosure is a first-class provenance risk.**  
   The sample recipe page notes that AI tools may have been used for some
   translations. VAKS should preserve similar disclosures for any source where
   translated, AI-assisted, or generated text may affect reliability.

5. **Policy links should be retained for commercial sources.**  
   Terms, privacy, cookie, disclaimer, owner, and code-of-ethics links are not
   evidence, but they help future reviewers evaluate reuse, retention, and risk.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Provenance | Page-level URL anchors and policy links. | Source-card fields. |
| Candidate Comprehension | Recipe-page field inventory. | Candidate extraction shape. |
| Activation | Collections, related links, ratings, categories. | Activation only. |
| Source Hygiene | AI translation and commercial owner disclosure. | Risk metadata. |
| Publishing | Rich page modules. | Inspiration for viewer surface only. |

## Local De-Dup / Collision

This differs from the GitHub cooking repos because it is not a source repository.
Its value is live-source handling: capture page type, checked date, editorial
context, translation/tool disclosure, and policy links.

It should not drive VAKS schema decisions except for live-web provenance fields
and risk labels.

## Anti-Borrow

- Do not treat ratings, "latest", or curated blocks as evidence.
- Do not copy commercial page structure into VAKS as architecture.
- Do not treat editorial process statements as verified support.
- Do not ignore live-page drift after the checked date.

## Candidate Tags

```yaml
domain: commercial_live_recipe_site
problem: capture_live_web_source_context_without_confusing_publication_with_evidence
pattern:
  - page-level-live-source-anchors
  - publication-module-as-activation
  - editorial-process-as-context
  - ai-translation-disclosure-risk
  - policy-links-in-source-card
maturity: large-commercial-site
problem_fit: 3
reuse_value: 3
implementation_cost: 2
integration_fit: 3
evidence_strength: 2
reversibility: 5
```

## Fusion Judgment

Borrow lightly as a P3 risk/provenance reference for live websites. Its main
lesson is to separate publication polish from evidence support and to capture
checked-date/page-type context.
