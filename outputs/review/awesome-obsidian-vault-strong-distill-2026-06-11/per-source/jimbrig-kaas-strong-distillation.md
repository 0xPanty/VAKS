---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "jimbrig/KaaS"
source_url: "https://github.com/jimbrig/KaaS"
checked_commit: "028fcf40521403c1b8a9fa6b28c3b9b2cd8cebbc"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/jimbrig-kaas-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/jimbrig-kaas-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/jimbrig-kaas-anchor-manifest.json
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
  - branch_projection_and_vault_risk
fit_layer:
  - publishing
  - source-hygiene
  - vault-health
  - activation
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - agent-write-boundary
avoid:
  - "Do not copy the personal vault taxonomy or content."
  - "Do not adopt force-push conversion workflows as a VAKS default."
  - "Do not ignore plugin sprawl, Readwise-derived long paths, and private sync issues."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing branch projections, Obsidian-to-publish conversion, or vault-health/path-portability checks."
  support_when: "When comparing develop/main/gh-pages separation, MOC/meta docs, plugin inventory, and MkDocs publishing."
  risk_when: "When generated branches, plugin sprawl, or long paths could blur canonical source and projection."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/jimbrig-kaas-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - branch-projection
  - source-hygiene
---

# Strong Candidate Distillation: jimbrig / KaaS

## What This Source Actually Is

This is a large personal Obsidian vault published through multiple projections.
Its useful architecture is the separation between an Obsidian working branch,
a converted GitHub Markdown branch, and a MkDocs/GitHub Pages output branch.
The repo also exposes major risks: long paths, huge plugin surface, personal
content, and self-mutating conversion workflows.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Vault purpose, MOCs, content types, publishing setup. | Public self-map helps orientation. | Personal content not reusable. |
| `2-Areas/Meta/Publish Workflow.md` | develop/main/gh-pages projection model. | Canonical vault and publish projection can be separate. | Projection is not source of truth. |
| `2-Areas/Meta/Vault Setup.md` | Note types, tags, source types, utility notes. | Meta docs should describe local conventions. | Taxonomy is not VAKS schema. |
| `convert-links.yml` | Obsidian link conversion and force push to main. | Conversion should be automated only behind gates. | Too risky as default. |
| `mkdocs.yml` workflow | Publishes converted output. | Publish pipeline can be isolated. | Build success is not review. |
| `.obsidian/community-plugins.json` | Very large plugin list. | Plugin surface must be captured as runtime provenance. | Plugin list is not approval. |
| Long Readwise paths | Windows filename-too-long checkout failures. | Path/attachment health checks are mandatory. | Retention is incomplete. |

## Strong Borrow Points

1. **Branch projection is a useful architecture pattern.**  
   The develop/main/gh-pages split maps well to VAKS repo vs projection vs
   publish separation, as long as the canonical layer remains explicit.

2. **Meta docs are worth keeping close to the vault.**  
   `Vault Setup` and `Publish Workflow` are good examples of project-local
   operating manuals that explain the vault's conventions and risks.

3. **Plugin inventory is source provenance.**  
   The large plugin list is valuable as a warning: plugin state belongs in
   environment provenance and Vault Health, not reviewed knowledge.

4. **Generated conversion branches are risky.**  
   Obsidian-export plus force-push workflow can support publishing, but VAKS
   should require explicit approval and hash/audit checks before any such path.

5. **Long paths are not edge cases.**  
   Checkout failures show why VAKS source snapshots need path-length checks and
   portable retention policy.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Publishing | Branch projection and MkDocs deployment. | Adapt with gates. |
| Source Hygiene | Long path and plugin-surface risk. | Strong adoption. |
| Vault Health | Plugin, attachment, Readwise path diagnostics. | Strong diagnostic pattern. |
| Activation | MOCs and meta docs. | Reference only. |
| Reviewed Knowledge | None directly. | Reject. |

## Local De-Dup / Collision

This overlaps with Blue Book and Digital Garden publication sources, but KaaS is
the strongest source for branch-projection risks and real Obsidian plugin/path
surface.

## Fusion Judgment

Borrow as P2 for branch projection, meta docs, plugin inventory, and path health.
Reject personal taxonomy, content, and force-push automation as defaults.
