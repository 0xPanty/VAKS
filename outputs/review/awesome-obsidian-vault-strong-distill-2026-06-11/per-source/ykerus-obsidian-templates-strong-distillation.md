---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
source_family: awesome-obsidian-vault
repo_key: "ykerus/obsidian-templates"
source_url: "https://github.com/ykerus/obsidian-templates"
checked_commit: "21950d27c40804e2bfe4a6da0f81b816f9473478"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/ykerus-obsidian-templates-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/ykerus-obsidian-templates-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/ykerus-obsidian-templates-anchor-manifest.json
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
  - note_lifecycle_and_activation
fit_layer:
  - activation
  - workbench
  - vault-health
  - templates
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - agent-write-boundary
avoid:
  - "Do not make QuickAdd or Shell Commands automation a default VAKS path."
  - "Do not treat Dataview/Copilot/vector-index output as support or reviewed knowledge."
  - "Do not copy personal todo/lifecycle folder conventions wholesale."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing an Obsidian workbench lifecycle, task activation surface, or cleanup checklist."
  support_when: "When comparing daily notes, scratch notes, meetings, task collections, and attachment/tag cleanup workflows."
  risk_when: "When automation plugins or AI plugin settings could cross VAKS write/truth boundaries."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/ykerus-obsidian-templates-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - activation
  - vault-health
---

# Strong Candidate Distillation: ykerus / obsidian-templates

## What This Source Actually Is

This is a full Obsidian workflow template with daily notes, scratch notes,
meeting templates, task collections, cleanup views, plugin configuration, and
automation guidance. Its strongest VAKS value is lifecycle and activation
design, with a major risk surface around plugins and automation.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Workflow manual for daily notes, todos, cleanup, templates, plugins. | Good example of explicit operating instructions. | Manual is not VAKS policy. |
| `.obsidian/community-plugins.json` | Broad plugin dependency surface. | Plugin environments need provenance and risk labels. | Plugins are not approved. |
| `emoji-prefixed Templates/*.md` | Daily, Meeting, Scratch, Note, Person, Board templates. | Core workflows can have distinct template entry points. | Template text is not reviewed knowledge. |
| Collection/todo notes | Work/personal/soon/later task surfaces. | Activation can separate urgency and domain. | Task lists are not truth. |
| README cleanup sections | Unused attachment, tag, and note cleanup workflows. | Vault health should include cleanup operations. | Cleanup must not mutate reviewed knowledge automatically. |

## Strong Borrow Points

1. **Make note lifecycle explicit.**  
   The scratch to note/info/archive lifecycle is a useful workbench pattern.
   VAKS can borrow the lifecycle idea without importing the exact folders.

2. **Daily notes can act as activation surfaces.**  
   The daily-note workflow is useful for surfacing unresolved tasks, meetings,
   and reminders. In VAKS terms this is activation, not truth or review.

3. **Separate task collections by action horizon.**  
   Work/personal and soon/later collections are a practical idea for context
   packs and active project views.

4. **Vault cleanup should be a visible maintenance workflow.**  
   Unused attachments, untagged notes, and unused notes belong in Vault Health
   or maintenance manifests. They should trigger review/cleanup pressure, not
   silent automatic repair.

5. **Automation is powerful enough to require a risk gate.**  
   QuickAdd, Shell Commands, Templater, Copilot, and similar plugins are useful
   examples, but VAKS should not absorb them into core defaults.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Activation | Daily notes and task horizons. | Strong adaptation. |
| Workbench | Scratch/meeting/note lifecycle. | Adapt. |
| Vault Health | Cleanup workflows. | Strong diagnostic pattern. |
| Agent Gateway | Automation/plugin risk example. | Risk only. |
| Review | None directly. | Do not adopt. |

## Local De-Dup / Collision

This overlaps with DashboardPlusPlus and groepl on dashboards/templates, but it
adds stronger lifecycle and automation-risk signals. Deduplicate under
activation lifecycle, vault health, and plugin boundary warnings.

## Fusion Judgment

Borrow as P2 for lifecycle, daily activation, and cleanup diagnostics. Reject
automation/plugin defaults unless a later explicit VAKS agent gateway task
authorizes review.
