---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "obsidian-pkm-vault/gatekeeperwiki"
source_url: "https://github.com/obsidian-pkm-vault/gatekeeperwiki"
resolved_source_url: "https://github.com/Mondrethos/gatekeeperwiki"
checked_commit: "a333fb66f7fbdc67cc6b00971da0635416dae7be"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/obsidian-pkm-vault-gatekeeperwiki-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/obsidian-pkm-vault-gatekeeperwiki-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/obsidian-pkm-vault-gatekeeperwiki-anchor-manifest.json
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
  - quartz_public_wiki
fit_layer:
  - publishing
  - source-hygiene
  - capture
  - activation
  - risk
not_fit_layer:
  - reviewed-knowledge
  - reviewed-relations
  - action-basis
avoid:
  - "Do not import game wiki content into VAKS knowledge."
  - "Do not treat public edit/publish workflow as evidence review."
  - "Do not trust awesome-list repo URLs without checking the active site provenance."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing public wiki contribution flow, Quartz publishing gates, or source URL recovery checks."
  support_when: "When comparing Markdown content folders, Edit-on-GitHub contribution flow, ignore patterns, RSS-to-Markdown ingest, and GitHub Pages publishing."
  risk_when: "When a stale source URL or automated feed import could create unsupported candidate content."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/obsidian-pkm-vault-gatekeeperwiki-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - quartz
  - source-hygiene
---

# Strong Candidate Distillation: Gatekeeper Wiki

## What This Source Actually Is

The awesome-list entry points to `obsidian-pkm-vault/gatekeeperwiki`, but that
GitHub URL could not be cloned without authentication and has no ledger commit.
The public site exposes Edit-on-GitHub links to `Mondrethos/gatekeeperwiki`,
which was cloned and inspected. The actual project is an Obsidian/Quartz public
wiki with a Markdown content folder, contribution page, Quartz configuration,
GitHub Pages deployment, and a feed-to-Markdown helper.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| Public site | Explorer, search, graph, TOC, backlinks, edit links. | Public wiki projection should expose navigation and edit affordances. | Site UI is not truth. |
| `content/contribute.md` | Branch-based edit/add page workflow. | Contribution gates should be explicit. | Approval is not evidence review. |
| `README.md` | Repo identity and Quartz/Obsidian stack. | Source identity can be recovered from active site links. | Original awesome URL is stale. |
| `content/**/*.md` | Markdown content tree. | Content folder is the canonical publish input. | Domain content is not reusable. |
| `quartz.config.ts` | Ignore patterns, remove drafts, crawl links, index, RSS/sitemap. | Publish exclusions and generated indexes are strong guardrails. | Index is projection. |
| `.github/workflows/deploy.yml` | Quartz build and GitHub Pages deploy. | Publish automation should be isolated. | Build is not review. |
| `process_steam_rss.py` | RSS parse, filename sanitize, hash state, Markdown output. | External feed intake needs cleaning and change detection. | Auto-ingest is candidate only. |

## Strong Borrow Points

1. **Recover active provenance from the published site when the listed repo is stale.**  
   The strongest lesson is source hygiene: the listed repo was not the usable
   source, but the public site's edit links exposed the active repository.

2. **Publish exclusions should be explicit.**  
   Quartz `ignorePatterns` for private, templates, and Obsidian config paths
   map well to VAKS future publishing gates.

3. **Contribution flow can be simple and branch-based.**  
   The public docs explain edit page, add page, branch, approval, merge, and
   automated site update. VAKS can borrow the clarity, not the authority model.

4. **External feed intake needs filename and content hygiene.**  
   The RSS script sanitizes filenames and tracks content hashes. VAKS can adapt
   this for candidate-only external update intake.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Source Hygiene | Stale URL recovery and active repo verification. | Strong adoption. |
| Publishing | Quartz config, ignore patterns, deploy workflow. | Adapt. |
| Capture | Feed-to-Markdown candidate intake. | Candidate only. |
| Activation | Search/graph/backlinks. | Projection only. |
| Review | Branch approval as process evidence. | Not support. |

## Local De-Dup / Collision

This overlaps with other Quartz/Digital Garden publishing examples, but its
distinct value is active provenance recovery plus publish ignore patterns and
feed-ingest hygiene.

## Fusion Judgment

Borrow as P2 for source-hygiene recovery, Quartz publish gates, and feed-intake
sanitization. Do not borrow its content or treat merged wiki edits as reviewed
knowledge.
