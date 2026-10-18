---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "ByteByteGoHq/system-design-101"
source_url: "https://github.com/ByteByteGoHq/system-design-101"
checked_commit: "b28380a4710c5ec9638ec037d4168e288f334cba"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/bytebytegohq-system-design-101-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/bytebytegohq-system-design-101-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/bytebytegohq-system-design-101-anchor-manifest.json
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
  - visual_explanation_reference
  - technical_docs_reference
fit_layer:
  - candidate-comprehension
  - source-ingest
  - publishing
  - workbench
not_fit_layer:
  - reviewed-knowledge
  - action-basis
avoid:
  - "Do not absorb system-design claims as VAKS architecture without independent evidence-aware review."
  - "Do not treat visual clarity as evidence support."
dev_context_hint:
  default_layer: support
  core_only_when: "When designing VAKS explanation pages, visual summaries, or source-card metadata for guide-like material."
  support_when: "When comparing frontmatter-driven guide catalogs, visual-first explanation, and single-topic contribution discipline."
  risk_when: "When appealing diagrams could bypass VAKS evidence gates."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/bytebytegohq-system-design-101-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - system-design
  - visual-explanation
---

# Strong Candidate Distillation: ByteByteGoHq / system-design-101

## What This Source Actually Is

This is a visual-first system-design guide collection. It uses category files
under `data/categories/`, guide files under `data/guides/`, frontmatter for
metadata, and a large README table of contents that routes readers to published
guide pages.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Category-oriented guide index. | A public-facing index can route many atomic guide pages without making the index itself authoritative. | Index inclusion is not support. |
| `data/categories/software-architecture.md` | Category frontmatter with title, description, image, icon, sort. | Useful shape for source/category cards and workbench filters. | Category description is not reviewed knowledge. |
| `data/guides/a-cheat-sheet-for-system-designs.md` | Guide frontmatter with title, description, image, createdAt, draft, categories, tags. | Strong simple model for candidate point metadata and publish readiness flags. | Draft=false is publishing state only. |
| `CONTRIBUTING.md` | Single-topic PR rule; diagram issues should be separate; AI-generated content disallowed. | Good governance for candidate point atomicity and human-authored review expectations. | Contribution policy is not evidence of correctness. |

## Strong Borrow Points

1. **Atomic guide files map well to candidate points.**  
   VAKS can borrow the habit of keeping one topic/concept per file and using
   metadata for category, tag, creation time, and draft state.

2. **Visual/simple explanation can live below review.**  
   The repo's style is useful for candidate comprehension and public summaries,
   but VAKS must keep explanation quality separate from truth confidence.

3. **Single-topic PR discipline fits point collision.**  
   The contribution rule to avoid multi-topic PRs mirrors VAKS's atomic
   candidate-point review: one topic, one change, one reviewable unit.

4. **Image/diagram corrections should not be casual drive-by edits.**  
   Their instruction to open separate issues for diagram problems suggests a
   useful VAKS split: visual asset fix requests should become maintenance input,
   not silent knowledge edits.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture | Frontmatter shape for guide-like source cards. | Adapt. |
| Understand | Visual summaries for candidate comprehension. | Use below review only. |
| Review Queue | Single-topic contribution/review unit. | Strongly compatible. |
| Connect | Categories/tags can aid activation. | Candidate relation only. |
| Publishing | Public guide index and images. | Useful but not truth. |

## Local De-Dup / Collision

The earlier shallow file marked this as `technical_docs_reference`. Strong
inspection narrows the borrow: not the system-design knowledge itself, but the
metadata-driven, visual-first, atomic-guide publishing pattern.

## Fusion Judgment

Adapt as a P2 reference for VAKS public explanation and candidate-comprehension
surfaces. Do not use it as an architecture authority.
