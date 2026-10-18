---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/obsidian-community/obsidian-hub"
repo_key: "obsidian-community/obsidian-hub"
checked_commit: "b11036f9a4db77917a4f07804541cceffc96cc66"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/obsidian-community-obsidian-hub-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/obsidian-community-obsidian-hub-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/obsidian-community-obsidian-hub-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: strong
borrow_order: P1
routing_hint:
  - source_catalog_workbench
  - generated_navigation
fit_layer:
  - source-ingest
  - workbench
  - activation
  - publishing
  - source-hygiene
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - automatic-reviewed-relations
avoid:
  - "Do not treat generated MOCs, plugin catalog pages, or community pages as reviewed relations."
  - "Do not let scheduled catalog automation mutate VAKS mainline truth."
  - "Do not ignore cross-platform filename/path constraints when cloning or syncing vaults."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing VAKS source catalogs, generated navigation, publish/edit footers, or automated candidate-only workbench refreshes."
  support_when: "When comparing community-maintained vault structure, templates, MOC generation, and PR-based automation."
  risk_when: "When generated catalog structure could be mistaken for reviewed knowledge or when path portability matters."
  cold_references:
    - raw/repos/2026-06-11-awesome-obsidian-vault/obsidian-community-obsidian-hub-source.md
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/obsidian-community-obsidian-hub-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - obsidian-hub
  - generated-navigation
---

# Strong Candidate Distillation: obsidian-community / obsidian-hub

## Boundary

This is a strong candidate distillation for VAKS design extraction. It does not
promote Hub content, generated pages, or catalog relations to reviewed
knowledge.

## What This Source Actually Is

Obsidian Hub is a community-maintained Obsidian vault and publish site. It
combines human-edited notes, templates, generated directory MOCs, plugin/theme
catalog enrichment scripts, scheduled update workflows, and GitHub edit/copy
footers.

For VAKS, its value is not the plugin catalog itself. Its value is how a large
community vault keeps navigation, contribution templates, generated updates, and
publication surfaces in a manageable candidate/workbench layer.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Identifies the Hub as an experimental community-maintained vault with local download and publish-site entry. | Clear distinction between vault source and publish surface. | Publish availability is not review. |
| Top-level folders | `00 - Contribute`, `01 - Community`, `02 - Community Expansions`, guides, concepts, inbox. | Large vault separates contribution workflow, community objects, catalogs, guides, and inbox. | Folder taxonomy should not be copied as VAKS ontology. |
| `.github/scripts/make_mocs.py` | Walks the vault, generates directory MOCs, filters hidden/generated files, and updates delimited sections. | Strong pattern: generated navigation should live in marked blocks and preserve manual text. | Generated links are navigation only. |
| `.github/scripts/plugins.py` | Fetches plugin manifest data, validates IDs, adds mobile compatibility, sanitizes descriptions, and records errors. | Good source-hygiene pattern for external catalog enrichment. | Manifest data is metadata, not evidence support. |
| `T - Plugin Category.md` | Template with aliases, tags, publish flag, placeholders, plugin links, and related categories. | Lightweight reusable template for catalog category notes. | Template placeholders are not reviewed content. |
| `.github/workflows/update_hub.yml` | Scheduled update workflow runs scripts, commits changes, and opens a PR. | Strong automation boundary: generated changes become reviewable diffs. | VAKS should not auto-merge truth changes. |
| Git checkout failure on Windows | Repo contains filenames that Windows cannot checkout normally. | Path portability must be recorded as source-retention risk. | Do not assume every vault is filesystem-portable. |

## Strong Borrow Points

1. **Generated navigation must be fenced and replaceable.**  
   `make_mocs.py` updates generated MOC sections via delimiters. VAKS can borrow
   this for candidate indexes, dashboards, and activation maps: generated areas
   should be clearly marked so manual notes are not overwritten.

2. **Catalog enrichment should validate identifiers.**  
   `plugins.py` checks upstream metadata consistency, including plugin IDs. VAKS
   should use the same principle for source cards: source URL, repo key, version,
   and extracted identity should be checked against each other before routing.

3. **Automation should create reviewable diffs, not silent truth updates.**  
   The scheduled workflow commits generated catalog changes and opens a pull
   request. VAKS should borrow this as candidate-only automation posture:
   generate, diff, review; do not promote automatically.

4. **Templates can keep contribution intake light.**  
   Hub templates use placeholders and simple metadata. VAKS can borrow this for
   future source-category or tool-category intake, but only as candidate record
   shapes.

5. **Publish/edit footers are useful provenance affordances.**  
   Hub notes expose GitHub edit/copy/download affordances. VAKS can adapt the
   idea for source-visible retained artifacts: every generated/published view
   should point back to the canonical Markdown source.

6. **Filesystem portability is part of source hygiene.**  
   The Windows checkout failure is not incidental. VAKS should record path
   compatibility risks for external vault snapshots and prefer archive/object
   inspection when normal checkout fails.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Source Ingest | Identifier validation and source metadata enrichment. | Adapt as source-card lint. |
| Candidate Comprehension | Templates and placeholders for contributor intake. | Candidate only. |
| Review Queue | Generated changes routed through PR-style review. | Useful for future maintenance manifests. |
| Association / Activation | Directory MOCs and category pages as navigation. | Activation, not reviewed relations. |
| Context Pack | Publish/edit/download links back to source. | Provenance affordance. |
| Workbench / Viewer | Large community vault as browsable catalog. | Strong workbench reference. |
| Publishing | Publish surface distinct from repo source. | Preserve repo-vs-vault-vs-publish boundary. |

## Local De-Dup / Collision

The earlier shallow file correctly tagged `source_catalog_workbench`. This strong
file adds the mechanisms VAKS can actually borrow:

- delimiter-based generated blocks;
- source metadata validation;
- PR-based automation boundary;
- lightweight category templates;
- publish/edit provenance affordances;
- path-portability risk recording.

This aligns with VAKS's existing rule that dashboard/retrieval/index layers do
not become reviewed truth.

## Anti-Borrow

- Do not create automatic reviewed relations from directory links or MOCs.
- Do not turn community plugin/theme popularity into evidence support.
- Do not auto-run weekly update workflows against VAKS mainline.
- Do not use Hub's taxonomy as VAKS architecture.

## Candidate Tags

```yaml
domain: community-obsidian-catalog-vault
problem: maintain_large_candidate_catalog_without_confusing_navigation_with_truth
pattern:
  - generated-moc-delimiters
  - catalog-metadata-validation
  - pr-based-candidate-automation
  - source-linked-publish-footer
  - vault-path-portability-warning
maturity: proven-community-workbench
problem_fit: 5
reuse_value: 5
implementation_cost: 3
integration_fit: 4
evidence_strength: 4
reversibility: 4
```

## Fusion Judgment

Adapt as a P1 reference for VAKS workbench/catalog mechanics. The core borrow is
not "Obsidian community content"; it is the disciplined separation between
source vault, generated navigation, contribution templates, automation diffs,
and publish surface.
