---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "rknightuk/intersect"
source_url: "https://github.com/rknightuk/intersect"
checked_commit: "1d521377d7170362c20fe88569a4277ed6e8c537"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/rknightuk-intersect-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/rknightuk-intersect-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/rknightuk-intersect-anchor-manifest.json
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
  - personal_wiki_link_index
fit_layer:
  - activation
  - publishing
  - source-scouting
  - vault-health
  - risk
not_fit_layer:
  - reviewed-knowledge
  - evidence-support
  - reviewed-relations
  - action-basis
avoid:
  - "Do not treat outbound-link counts or domain frequency as source quality."
  - "Do not infer maintenance commitment from a shared personal wiki."
  - "Do not make analytics/API integrations a VAKS default."
dev_context_hint:
  default_layer: support
  core_only_when: "When designing a personal-wiki style link index, navigation index, or source/history link projection."
  support_when: "When comparing nested Markdown content roots, computed breadcrumbs, page indexes, outbound-link extraction, and search modes."
  risk_when: "When link counts or external analytics could be mistaken for evidence or authority."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/rknightuk-intersect-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - personal-wiki
  - link-index
---

# Strong Candidate Distillation: rknightuk / intersect

## What This Source Actually Is

This is a personal Eleventy wiki shared for others to adapt, with an explicit
maintenance boundary. Its reusable value is a simple nested Markdown content
tree plus generated navigation, breadcrumbs, search, outbound-link indexing,
domain counts, and source/history links.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Personal wiki boundary and basic usage. | Source records should capture maintenance expectations. | Not a maintained product. |
| `src/pages/meta/readme.md` | Expanded setup and architecture notes. | Good self-documenting project pattern. | Notes are not VAKS policy. |
| `src/pages/**/*.md` | Nested Markdown content root. | One content root eases migration. | Folder position is not truth. |
| `links.js` | Extracts external links, dedupes, counts domains, records source page. | Outbound links can become source-scouting diagnostics. | Link count is not evidence. |
| `pages.js` | Featured/standard page ordering and page index. | Explicit page index supports navigation. | Order is not authority. |
| `pages.11tydata.js` | Breadcrumbs, source/history links, content index, link counts. | Computed metadata can aid audit and navigation. | Computed data is projection only. |

## Strong Borrow Points

1. **Maintenance expectations should be explicit.**  
   The README says this is shared for adaptation, not maintained as a general
   open-source product. VAKS source cards should preserve that kind of posture.

2. **A single content root reduces migration friction.**  
   Keeping content under `src/pages` while Eleventy machinery stays elsewhere is
   a useful publishing separation.

3. **Outbound-link indexes are useful diagnostics.**  
   The link extractor records link title, URL, source page, and domain counts.
   VAKS could adapt this for source scouting and link rot checks, not evidence.

4. **Computed source/history links improve auditability.**  
   Page-level GitHub and history links are useful for public docs and recovery.

5. **Search modes can separate page search from link search.**  
   This is a useful activation idea for VAKS: search source content separately
   from external references.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Activation | Search, breadcrumbs, page index. | Adapt. |
| Source Scouting | External link index and domain counts. | Diagnostic only. |
| Publishing | Content/machinery separation. | Reference. |
| Vault Health | Link rot/link inventory potential. | Adapt. |
| Risk | Link metrics mistaken for authority. | Required warning. |

## Local De-Dup / Collision

This overlaps with digital-garden publication sources, but its distinct value is
link inventory and computed audit/navigation metadata rather than Obsidian
publication controls.

## Fusion Judgment

Borrow as P2 for outbound-link inventory, content-root separation, and computed
source/history links. Reject link counts as evidence support.
