---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "shervinsahba/obsidian-icewind"
source_url: "https://github.com/shervinsahba/obsidian-icewind"
checked_commit: "7b090ba92c86de284431c42dfc7badbc7a15f5ef"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/shervinsahba-obsidian-icewind-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/shervinsahba-obsidian-icewind-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/shervinsahba-obsidian-icewind-anchor-manifest.json
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
  - entity_event_workflow
fit_layer:
  - capture
  - activation
  - workbench
  - publishing
  - risk
not_fit_layer:
  - reviewed-knowledge
  - reviewed-relations
  - action-basis
avoid:
  - "Do not import domain content or personal/campaign taxonomy into VAKS."
  - "Do not treat Dataview-generated interaction lists as reviewed relations."
  - "Do not use Digital Garden publication fields as review approval."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing an entity/event log workbench or link-derived activation view."
  support_when: "When comparing session logs, entity pages, templates, and derived interaction dashboards."
  risk_when: "When derived Dataview tables could be mistaken for reviewed relation evidence."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/shervinsahba-obsidian-icewind-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - dataview
  - activation
---

# Strong Candidate Distillation: shervinsahba / obsidian-icewind

## What This Source Actually Is

This is a real Obsidian vault for a tabletop campaign, published as a Digital
Garden site. Its reusable design is the entity/event workflow: session logs link
to entities and locations, then Dataview queries assemble interaction histories.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Explains Dataview plus Digital Garden workflow. | Good plain-language workflow documentation. | Not a VAKS model. |
| `Home.md` | Published home note with Dataview session table. | Home dashboards can expose recent logs. | Dashboard is activation only. |
| `_templates/NPC Template.md` | Entity metadata plus interaction query. | Entity pages can pull linked event traces. | Query result is not reviewed relation. |
| `_templates/Session Template.md` | Session date, participants, summary, log sections. | Event-log templates can drive later retrieval. | Log quality remains manual. |
| `Characters/`, `Places/`, `Journal/`, `Lore/` | Real domain vault folders. | Domain folders show entity/event separation. | Taxonomy is not portable. |
| `Untitled.base` | Small Obsidian Bases artifact. | Bases may appear in live vaults. | Base output is a projection. |

## Strong Borrow Points

1. **Event logs can feed entity activation pages.**  
   Session/event records are a good capture primitive. Entity pages can query
   the logs to show where an entity appeared, but this remains activation.

2. **Manual link quality is the real dependency.**  
   The workflow works because logs consistently link to entities. VAKS should
   make link quality visible before trusting any derived relation view.

3. **Templates can reduce capture friction.**  
   Entity and session templates create enough structure for later queries
   without turning capture into a heavy review process.

4. **Published home dashboards need clear gates.**  
   Digital Garden fields make publication explicit, but they are not review
   approval or action readiness.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture | Event/session templates. | Adapt. |
| Activation | Entity pages assembled from linked logs. | Projection only. |
| Workbench | Home dashboard over recent logs. | Useful reference. |
| Reviewed Relations | None directly. | Reject. |
| Risk | Link-derived relation confusion. | Required warning. |

## Local De-Dup / Collision

This overlaps with Dataview/dashboard sources, but its distinct value is the
event-to-entity activation pattern. Deduplicate under link-derived activation,
not reviewed relation creation.

## Fusion Judgment

Borrow as P2 for event/entity activation and low-friction templates. Keep every
Dataview result candidate-only unless a later evidence-aware review confirms it.
