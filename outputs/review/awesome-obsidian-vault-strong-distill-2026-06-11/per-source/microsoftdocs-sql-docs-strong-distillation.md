---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "MicrosoftDocs/sql-docs"
source_url: "https://github.com/MicrosoftDocs/sql-docs"
checked_commit: "1baa2aac5834779c08b6b3ae191e2211a976211e"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/microsoftdocs-sql-docs-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/microsoftdocs-sql-docs-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/microsoftdocs-sql-docs-anchor-manifest.json
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
  - multi_docset_publishing
  - redirect_ledger
fit_layer:
  - publishing
  - source-ingest
  - source-hygiene
  - workbench
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
avoid:
  - "Do not treat product documentation hub placement as evidence support."
  - "Do not copy Microsoft-scale publishing machinery into VAKS core."
  - "Do not ignore path-length failures when retaining source snapshots on Windows."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing multi-surface publishing, redirect ledgers, source-retention path checks, or large documentation navigation."
  support_when: "When comparing hub pages, product directories, TOCs, redirect files, and preview PR publishing boundaries."
  risk_when: "When navigation metadata, product docs, or build configuration could be mistaken for reviewed VAKS support."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/microsoftdocs-sql-docs-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - docs-publishing
  - redirect-ledger
---

# Strong Candidate Distillation: MicrosoftDocs / sql-docs

## What This Source Actually Is

This is a large product documentation repository for Microsoft SQL. It includes
multiple docsets, product-area TOCs, hub pages, redirection files, dependent
repositories, and OpenPublishing configuration. Windows checkout produced many
long-path failures, so this review used Git object inspection for key anchors.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `ReadMe.md` | Repo identity, contribution route, code of conduct, CLA note. | Large public docs need explicit contribution/legal boundary. | Process boundary, not content truth. |
| `.openpublishing.publish.config.json` | Multiple docsets, build folders, dependent repos, preview PR requirement. | Strong model for publishing many surfaces from one source tree. | Too heavy for VAKS core. |
| `docs/index.yml` | Hub metadata, product directory, highlighted content, conceptual content, item types. | Good structured hub-page pattern for workbench/publishing. | Hub placement is not support. |
| `docs/**/toc.yml` | Many area/product TOCs. | Navigation is split by product/domain area. | TOC links are activation only. |
| `.openpublishing.redirection*.json` | Redirect files for moved/renamed documentation. | Excellent reference for supersession and moved-source ledgers. | Redirect is applicability metadata, not truth. |
| Checkout long-path failures | Many paths exceed Windows limits. | Retained-source strategy must detect path portability before relying on checkout. | Source risk, not source rejection by itself. |

## Strong Borrow Points

1. **Redirect ledgers are a missing VAKS primitive candidate.**  
   VAKS already has supersession/review_due ideas. SQL docs shows a practical
   publishing version: moved content needs durable redirects so old paths remain
   interpretable.

2. **Hub pages should be structured data, not freeform dashboards.**  
   `docs/index.yml` uses metadata, product directories, highlighted content, and
   item types. VAKS can borrow this for public-facing indexes where every tile
   has explicit type and target.

3. **Multi-docset publishing should remain a projection layer.**  
   The OpenPublishing config maps source folders to output docsets. VAKS can
   adapt the source-vs-output mapping but must keep the Markdown repo as the
   canonical source and Obsidian/publish outputs as projections.

4. **Path portability must be audited for external vaults/repos.**  
   The checkout failure is concrete evidence that source retention can fail on
   Windows. VAKS should record snapshot retention method and fallback to archive
   or object inspection when needed.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture | Path portability and source-retention risk. | Strongly adapt. |
| Review Queue | Redirect/supersession ledgers. | Candidate for stale/moved content tracking. |
| Activation | Structured hub pages and TOCs. | Workbench only. |
| Publishing | Multi-docset source/output mapping. | Later-stage reference. |
| Risk | Long path failures and product-navigation authority confusion. | Record as source hygiene. |

## Local De-Dup / Collision

The earlier shallow file labeled this `technical_docs_reference`. Strong
inspection narrows the useful borrow to publishing metadata, redirects, hub
structure, and source-retention risk, not SQL technical content.

## Fusion Judgment

Adapt as a P2 reference for redirect ledgers, structured hub pages, and
multi-surface publishing boundaries. Do not import product-doc content or
Microsoft-scale publishing complexity into the core.
