---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "interneto/interneto.github.io"
source_url: "https://github.com/interneto/interneto.github.io"
checked_commit: "9ff6e8efe2a686052d844d9d6028baa7b9469060"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/interneto-interneto-github-io-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/interneto-interneto-github-io-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/interneto-interneto-github-io-anchor-manifest.json
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
  - resource_directory_and_agent_map
fit_layer:
  - source-scouting
  - activation
  - workbench
  - dev-context
  - risk
not_fit_layer:
  - reviewed-knowledge
  - evidence-support
  - action-basis
avoid:
  - "Do not treat curated package/resource directories as evidence support."
  - "Do not execute generated install commands from a candidate context pack."
  - "Do not let generated Markdown hide its CSV/source provenance."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing VAKS source-directory catalogs, agent-facing repo maps, or tool/package directory projections."
  support_when: "When comparing content collections, static JSON catalogs, generated directory pages, filter chips, count metrics, and local agent instructions."
  risk_when: "When a directory or generated command could be mistaken for action-ready guidance."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/interneto-interneto-github-io-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - source-directory
  - dev-context
---

# Strong Candidate Distillation: interneto / interneto.github.io

## What This Source Actually Is

This is an Astro resource discovery and curation site. It has content
collections, generated category pages, static JSON catalogs, interactive
toolbox/compatibility pages, and an unusually useful `CLAUDE.md` that explains
the repo to coding agents.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Resource discovery platform purpose and stack. | Source directories need clear scope and runtime. | Directory is not review. |
| `CLAUDE.md` | Agent-facing repo map and commands. | Local agent docs can reduce unsafe edits. | Agent map is not policy authority. |
| `src/content.config.ts` | Astro collections for categories and posts. | Content schema should be explicit. | Loose schema needs provenance. |
| `scripts/` | CSV conversion, lint, icon download, SVG optimization. | Generated content needs source/config distinction. | Generated output is projection. |
| `web-directory.ts` | Tag sanitization, icon fallback, search/filter/counts. | Directory UI should sanitize and expose counts. | Counts are not evidence. |
| `public/pkgs/*` and `src/data/*` | Static catalogs for tools/packages/bookmarks. | Data catalogs can drive workbench views. | Catalog entries not action-ready. |

## Strong Borrow Points

1. **Agent-facing repo maps are directly useful.**  
   `CLAUDE.md` gives commands, CI, architecture, content/data boundaries, and
   editing warnings. VAKS should borrow this for repo-local recovery docs.

2. **Separate build-time scripts from browser-side scripts.**  
   The repo explicitly distinguishes root `scripts/` from `src/scripts/`.
   This is a clean pattern for preventing tool confusion.

3. **Static catalogs can power rich workbench views.**  
   JSON catalogs plus client filters are useful for VAKS source scouting or
   tool directories, but they remain activation/workbench surfaces.

4. **Sanitize directory metadata before rendering.**  
   Tag allowlists, icon fallbacks, URL protocol checks, and count summaries are
   reusable source-directory hygiene.

5. **Command-generation UI is a risk boundary.**  
   The toolbox can generate install commands. VAKS should treat similar output
   as candidate guidance until an explicit action gate approves execution.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Source Scouting | Resource/catalog directory. | Adapt. |
| Dev Context | Agent-facing repo map. | Strong adoption. |
| Activation | Search/filter/count UI. | Projection only. |
| Workbench | Static JSON catalogs. | Candidate support. |
| Action Basis | Command generation. | Reject by default. |

## Local De-Dup / Collision

This overlaps with FMHY as a resource-directory source. Interneto is stronger
for typed architecture, agent guidance, and catalog workbench design; FMHY is
stronger for community contribution and risk reporting.

## Fusion Judgment

Borrow as P2 for agent-facing repo maps, catalog/workbench design, and metadata
sanitization. Keep generated commands outside action basis.
