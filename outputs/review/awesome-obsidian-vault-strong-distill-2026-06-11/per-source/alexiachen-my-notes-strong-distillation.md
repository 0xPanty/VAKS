---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "AlexiaChen/my-notes"
source_url: "https://github.com/AlexiaChen/my-notes"
checked_commit: "6b6bd62462c8542f8c3e26b6e8b6f4fd67ee7ac6"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/alexiachen-my-notes-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/alexiachen-my-notes-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/alexiachen-my-notes-anchor-manifest.json
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
  - personal_vault_scale_reference
fit_layer:
  - memory
  - dev-context
  - source-hygiene
  - workbench
not_fit_layer:
  - reviewed-knowledge
  - action-basis
avoid:
  - "Do not copy another user's domain taxonomy or note contents into VAKS."
  - "Do not treat personal-note volume as quality or review depth."
dev_context_hint:
  default_layer: support
  core_only_when: "When evaluating personal-vault scale, attachment handling, Obsidian core-plugin choices, or multilingual path hygiene."
  support_when: "When comparing domain-folder organization and large vault operational constraints."
  risk_when: "When personal content, domain folders, or attachment counts could be mistaken for reusable architecture."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/alexiachen-my-notes-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - personal-vault
---

# Strong Candidate Distillation: AlexiaChen / my-notes

## What This Source Actually Is

This is a personal notes vault with a broad domain-folder taxonomy, a large
attachment corpus, and normal Obsidian configuration. It is useful as a
scale/operations reference for personal vaults, not as an architecture authority.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Minimal repo identity plus an rsync backup reminder. | Backup semantics matter: directory content vs directory itself. | Backup tip is operational, not VAKS design proof. |
| `.obsidian/core-plugins.json` | Enables graph, canvas, daily notes, templates, bookmarks, file recovery, Bases; disables publish/sync. | Useful snapshot of core-plugin choices in a real vault. | Plugin choices are not recommendations. |
| `.obsidian/appearance.json` | Theme dependency. | Visual config should be recorded as environment context. | Theme is not knowledge structure. |
| Top-level folders | AI, backend, blockchain, compiler, PL, security, software-engineering, MOOCs, tools, etc. | Shows domain-folder growth in a real personal vault. | Do not copy taxonomy. |
| File counts | About 804 Markdown files and 1642 attachment entries observed. | Attachment management and media bloat are real vault health concerns. | Counts do not imply quality. |

## Strong Borrow Points

1. **Large personal vaults accumulate attachment gravity.**  
   VAKS should keep attachment/media retention visible in vault health. Large
   attachment count can affect sync, search, portability, and backups.

2. **Plugin/core-plugin state is part of environment provenance.**  
   The vault records enabled core plugins and theme. VAKS source cards for
   vaults should capture Obsidian configuration separately from note content.

3. **Domain folders are convenient but can become ontology drift.**  
   This vault uses many domain folders. VAKS should resist copying such domain
   organization into the reviewed schema; domain folders are navigation, not
   knowledge calibration.

4. **Backup semantics should be explicit.**  
   The README's rsync note is a small but useful reminder: source retention and
   sync tools need exact path semantics. VAKS already treats sync/hash as a
   separate decision; this source reinforces that.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture | Vault config and attachment counts as source metadata. | Adapt. |
| Activation | Domain folders can help browsing. | Candidate/cold only. |
| Dev Context | Environment/plugin state for reproduction. | Support. |
| Vault Health | Attachment volume and backup semantics. | Useful signal. |
| Review | No direct review value. | Do not promote. |

## Local De-Dup / Collision

The shallow file marked this as publishing/template reference. Strong inspection
shows it is better routed as `personal_vault_scale_reference`: useful for vault
operations and path/plugin hygiene, weaker for VAKS architecture.

## Fusion Judgment

Watch/adapt lightly as P2. Borrow vault-health and configuration-capture ideas,
not content taxonomy.
