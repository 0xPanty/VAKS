---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/xy-241/CS-Notes"
repo_key: "xy-241/CS-Notes"
checked_commit: "2a4f9dbf7aee76bca161b38616dbe1b8b8a877f9"
checked_at: 2026-06-11
derived_from:
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/xy-241-cs-notes-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: high
borrow_order: P3
routing_hint:
  - public-second-brain
  - generated-navigator
  - quartz-publish
  - path-portability-risk
fit_layer:
  - activation
  - publishing
  - maintenance
  - source-hygiene
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - automatic-truth-update
avoid:
  - "Do not treat graph view, tag counts, or README navigator links as reviewed relations."
  - "Do not copy inherited Quartz workflows without repository-gate cleanup."
  - "Do not ignore Windows path portability failures."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing public second-brain navigation, tag/domain maps, or Quartz-style publication checks."
  support_when: "When comparing activation indexes, generated README navigators, and ignore/publish filters."
  risk_when: "When generated navigators or graph views could be mistaken for truth or when filenames break Windows tooling."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/xy-241-cs-notes-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - second-brain
  - quartz
  - path-portability
---

# Strong Candidate Distillation: xy-241 / CS-Notes

## Boundary

This file extracts public second-brain, navigation, Quartz, and maintenance
lessons. It does not treat the repository's CS content, graph view, tag counts,
or generated README navigator as reviewed VAKS relations.

## What This Source Actually Is

`CS-Notes` is a large public computing second brain published with Quartz. The
README presents it as an interconnected note system with hand-crafted diagrams,
long-running project intent, and a generated "Notes Navigator" grouping notes by
domain and tag.

The checkout also exposed a practical risk: some tracked paths are invalid on
Windows, so inspection had to use Git object access for complete evidence.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Public story, graph/second-brain explanation, domain/tag navigator with counts. | Generated navigation can orient users quickly. | Navigator is not reviewed relation graph. |
| `quartz.config.ts` | Quartz config, ignored private folders, site map/RSS, content index, OG images. | Publication filter and projection controls. | Publish config is not truth authority. |
| `.github/workflows/ci.yaml` | Quartz upstream build/test workflow gated to `jackyzha0/quartz`. | Inherited workflow residue can be harmless but confusing. | Do not copy without cleanup. |
| `.gitignore` | Ignores `.quartz-cache`, `.makemd`, `.space`, and local vault artifacts. | Keep tool caches and workspace state out of source. | Ignore file does not classify truth. |
| Invalid Windows paths | Checkout reported invalid names such as `exec "$@" example.png` and `?` in filenames. | Source portability should be part of intake health. | Path failure is maintenance risk only. |

## Strong Borrow Points

1. **Generated README navigators are useful as activation maps.**  
   The domain/tag navigator makes a large vault scannable. VAKS can borrow this
   for `wiki/indexes`, but must label it as activation/navigation, not truth.

2. **Tag counts can reveal coverage without proving quality.**  
   Counts like `system_design`, `aws`, and `docker` help estimate corpus shape.
   They should route attention, not determine confidence.

3. **Publication filters should exclude private/workbench material.**  
   `quartz.config.ts` ignores private folders, templates, Obsidian state,
   archives, and raw notes. VAKS should keep the same mental line between
   source repo, vault state, workbench, and public projection.

4. **Inherited generator workflows need quarantine.**  
   The CI workflow remains gated to the upstream Quartz repository. This is a
   concrete reminder that starter-template automation can survive in downstream
   repos and mislead maintainers.

5. **Path portability is not optional for VAKS.**  
   Invalid Windows paths directly affected inspection. VAKS should lint path
   portability before treating a repo as a reliable source snapshot.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Activation | Domain/tag navigator and public graph story. | Navigation index only. |
| Publishing | Quartz config, sitemap/RSS, ignore patterns. | Downstream projection controls. |
| Source Hygiene | Git object inspection when checkout fails. | Snapshot health manifest. |
| Maintenance | Inherited workflow detection. | Template residue lint. |
| Risk / Inhibition | Graph/counts can look authoritative. | Never promote automatically. |

## Local De-Dup / Collision

This overlaps with `MaggieAppleton/digital-gardeners`, `ThatOtherAndrew`
Digital Garden, and Quartz-based repos:

- Digital Garden sources focus on public garden philosophy or plugin publish.
- `CS-Notes` is a concrete large-scale public second-brain with generated
  navigation and visible path-portability risk.

Its unique borrow is the full combination: generated navigator, Quartz
publication config, and path-health warning.

## Anti-Borrow

- Do not adopt graph view as reviewed knowledge graph.
- Do not let tag counts imply coverage sufficiency.
- Do not copy upstream Quartz workflows without repository-specific cleanup.
- Do not ignore OS-specific filename failures.

## Candidate Tags

```yaml
domain: public_second_brain_navigation
problem: orienting_large_interconnected_note_corpus_without_promoting_it_to_truth
pattern:
  - generated-domain-tag-navigator
  - activation-counts-not-confidence
  - quartz-publication-filters
  - inherited-workflow-lint
  - path-portability-check
maturity: active-public-vault
problem_fit: 4
reuse_value: 5
implementation_cost: 3
integration_fit: 4
evidence_strength: 4
reversibility: 4
```

## Fusion Judgment

Borrow strongly for activation and maintenance design. Do not borrow its graph,
tags, or content as reviewed VAKS relations.
