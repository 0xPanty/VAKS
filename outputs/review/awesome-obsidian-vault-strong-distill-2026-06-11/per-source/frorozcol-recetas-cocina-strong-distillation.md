---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://huggingface.co/datasets/Frorozcol/recetas-cocina"
repo_key: "Frorozcol/recetas-cocina"
checked_commit: "3b640b0d91c6aad648168a3cae9293328e4a285a"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/frorozcol-recetas-cocina-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/frorozcol-recetas-cocina-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/frorozcol-recetas-cocina-anchor-manifest.json
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
  - dataset-card-reference
  - structured-split-risk
fit_layer:
  - capture-provenance
  - source-hygiene
  - candidate-comprehension
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - activation-tier
  - truth-confidence
avoid:
  - "Do not treat train/test/valid splits as VAKS review stages."
  - "Do not import scraped recipe rows without source/license review."
  - "Do not let dataset size imply evidence strength."
dev_context_hint:
  default_layer: risk
  core_only_when: "When designing dataset-style source cards, field-level provenance checks, or large scraped-corpus quarantine rules."
  support_when: "When comparing simple structured fields and split metadata."
  risk_when: "When scraped datasets, ML task labels, or row counts could be mistaken for reviewed knowledge."
  cold_references:
    - raw/repos/2026-06-11-awesome-obsidian-vault/frorozcol-recetas-cocina-source.md
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/frorozcol-recetas-cocina-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - dataset-card
  - scraped-corpus-risk
---

# Strong Candidate Distillation: Frorozcol / recetas-cocina Dataset

## Boundary

This file extracts dataset-handling lessons. It does not import recipes, scraped
rows, source URLs, or generated task labels into reviewed VAKS knowledge.

## What This Source Actually Is

This is a Hugging Face dataset repository for Spanish recipe text generation. It
contains a dataset card and CSV splits with fields for title, URL, ingredients,
steps, and UUID. The card says the data was scraped from multiple Spanish
recipe pages and split into train, test, and validation sets.

For VAKS, the strongest lesson is not the content. It is how quickly a large,
structured corpus can look authoritative while still requiring provenance,
license, and source-quality quarantine.

## Source / Data Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Dataset card with license, tasks, language, size category, origin summary, and field descriptions. | Dataset-card style metadata is useful for source cards. | Card claims need verification. |
| `data/train.csv` | 20,526 data rows, main split. | Simple field schema supports bulk parsing. | ML split is not review. |
| `data/test.csv` | 3,904 data rows. | Split metadata should be recorded, not overinterpreted. | Test rows are not stronger evidence. |
| `data/valid.csv` | 2,781 data rows. | Validation split is workflow metadata. | Not VAKS validation. |
| CSV header | `title,url,ingredients,steps,uuid`. | Minimal fields show what a bulk content source can preserve. | URL field is provenance, not support. |

## Strong Borrow Points

1. **Dataset card as source-card inspiration.**  
   The README records license, language, task category, size category, origin,
   and fields. VAKS can borrow this structure for large source batches:
   identity, scope, origin, fields, known use, and limits.

2. **Field inventory before content interpretation.**  
   The useful first pass is not summarizing 30k rows; it is confirming fields,
   row counts, split names, and provenance columns. VAKS should use the same
   approach for large corpora: inspect shape before extracting candidate points.

3. **URL column is provenance, not evidence support.**  
   Each row has a URL, but the dataset row itself does not prove that the source
   page is current, licensed, or accurately scraped. This reinforces VAKS's
   evidence support rule: citations and source URLs must support the specific
   point before they count.

4. **Bulk corpora need quarantine defaults.**  
   Scraped data should enter VAKS as candidate/raw material only. License,
   source ownership, duplicates, stale URLs, and malformed rows require later
   review before any extracted claim is usable.

5. **ML workflow labels must not leak into VAKS semantics.**  
   Train/test/valid are dataset engineering partitions. VAKS should not map them
   to hot/warm/cold, reviewed/unreviewed, or confidence tiers.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Provenance | Dataset card and URL field. | Source-card metadata only. |
| Candidate Comprehension | Field schema enables bulk candidate extraction. | Candidate-only parser input. |
| Source Hygiene | Row counts, split names, license/origin claims. | Maintenance manifest checks. |
| Risk / Inhibition | Scrape provenance and licensing uncertainty. | Quarantine until reviewed. |
| Review Queue | Potential missing evidence or duplicate source issues. | Review pressure only. |

## Local De-Dup / Collision

This overlaps with `dpapathanasiou/recipes` because both are large structured
recipe corpora. The distinction:

- Frorozcol is a CSV dataset framed for ML text generation, with split metadata
  and scrape-origin risk.
- `dpapathanasiou/recipes` is a JSON recipe collection with generated browsing
  indexes.

For VAKS, Frorozcol is primarily a risk/reference source for large scraped
datasets, while `dpapathanasiou/recipes` is more useful for JSON record and
component-index mechanics.

## Anti-Borrow

- Do not treat dataset row count as authority.
- Do not treat Hugging Face task labels as VAKS routing truth.
- Do not reuse scraped rows without license/provenance review.
- Do not map train/test/valid to VAKS activation or review tiers.

## Candidate Tags

```yaml
domain: scraped_text_generation_dataset
problem: preserve_large_corpus_shape_without_confusing_dataset_metadata_with_truth
pattern:
  - dataset-card-source-card
  - field-inventory-before-extraction
  - url-as-provenance-not-support
  - scraped-corpus-quarantine
  - ml-split-semantic-boundary
maturity: public-dataset
problem_fit: 3
reuse_value: 3
implementation_cost: 2
integration_fit: 3
evidence_strength: 2
reversibility: 5
```

## Fusion Judgment

Borrow lightly as a P3 risk/source-hygiene reference. The useful VAKS lesson is
how to quarantine and describe a large structured scraped corpus, not how to use
its content.
