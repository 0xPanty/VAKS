---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/TfTHacker/DashboardPlusPlus"
repo_key: "TfTHacker/DashboardPlusPlus"
checked_commit: "e202bb286cd92d7986407293c0a4a33789fef2bd"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/tfthacker-dashboardplusplus-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/tfthacker-dashboardplusplus-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/tfthacker-dashboardplusplus-anchor-manifest.json
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
  - workbench_dashboard
  - activation_surface
fit_layer:
  - workbench
  - activation
  - dev-context
  - retrieval-cache
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - evidence-support
avoid:
  - "Do not treat dashboard visibility, Dataview output, plugin state, or recent-file ordering as review approval."
  - "Do not enable inline JavaScript or bundled plugins in VAKS without a separate plugin/runtime review."
  - "Do not make a dashboard the canonical source of truth."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing a VAKS home/workbench surface, vault health dashboard, activation dashboard, or dev-context entry panel."
  support_when: "When comparing dashboard layout, section buckets, live recent/favorite queries, and presentation-vs-content separation."
  risk_when: "When live queries or visual prominence could be mistaken for reviewed support or action readiness."
  cold_references:
    - raw/repos/2026-06-11-awesome-obsidian-vault/tfthacker-dashboardplusplus-source.md
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/tfthacker-dashboardplusplus-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - dashboard
  - activation
---

# Strong Candidate Distillation: TfTHacker / DashboardPlusPlus

## Boundary

This is a strong candidate distillation of a dashboard/template vault. It does
not promote any dashboard item, Dataview output, plugin state, or visible link
to reviewed knowledge.

## What This Source Actually Is

DashboardPlusPlus is a complete Obsidian vault template demonstrating a home
dashboard method. It includes real `.obsidian` settings, plugin bundles,
snippets, example notes, images, and a `Dashboard++.md` note that acts as the
front door.

For VAKS, the value is not the personal/family/work taxonomy. The value is the
activation surface pattern: a human-scannable home view that mixes stable
manual links with live lightweight queries.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | States that the repo is an Obsidian vault demonstrating Dashboard++. | Template-vault packaging can make a UX pattern inspectable. | Template popularity is not VAKS fit. |
| `Dashboard++.md` frontmatter | Uses `cssclasses: dashboard`, banner image, and banner position metadata. | Presentation can be scoped per note through metadata rather than global vault rules. | Metadata is display context, not knowledge. |
| `Dashboard++.md` body | Sections for Family, Personal Projects, Work, and Vault Info with manual links. | Stable buckets plus curated links create a fast activation surface. | Buckets should be VAKS-specific, not copied. |
| `Dashboard++.md` Dataview snippets | Inline recent updates, tagged favorite links, and vault stats. | Live query widgets are useful for workbench awareness. | Live query output is not evidence support. |
| `.obsidian/community-plugins.json` | Bundles homepage, emoji toolbar, Dataview, page header buttons, reveal-active-file, banners. | Demo vault declares runtime dependencies explicitly. | Plugin bundle must not be silently adopted. |
| `.obsidian/plugins/dataview/data.json` | Inline query/JS settings, refresh interval, render null behavior. | Query runtime settings should be treated as operational config with risk. | Inline JS needs separate review. |
| `.obsidian/snippets/dashboard.css` | CSS scopes dashboard layout, hides bullets, uses flex-wrapped columns, supports Dataview lists. | Presentation is isolated in a class-based snippet. | CSS polish is not architecture proof. |

## Strong Borrow Points

1. **A vault needs a front door.**  
   VAKS has many boundaries and queues. A dashboard-style activation surface can
   reduce friction if it links to source inbox, review queue, hot/warm context,
   feedback ledger, and vault health without claiming those links are truth.

2. **Manual anchors plus live queries is the right mix.**  
   The dashboard combines stable hand-curated sections with dynamic recent,
   favorite, and count queries. VAKS can adapt this: manual architecture links
   plus live candidate/review/feedback counters.

3. **Presentation should be note-scoped.**  
   `cssclasses: dashboard` and `dashboard.css` keep layout styling scoped to the
   dashboard note. VAKS should avoid global theme assumptions for workbench
   surfaces.

4. **Dashboard entries must not become evidence.**  
   This source is the cleanest reminder that visibility is not validity.
   Dashboard links can activate attention, but only reviewed evidence can
   support action.

5. **Plugin/runtime dependencies need explicit manifests.**  
   The template exposes required plugins and settings. VAKS should do the same
   for any optional Obsidian dashboard: list dependencies, risks, and disabled
   paths.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Source Ingest | Dashboard can expose recent source intake and inbox counts. | Workbench only. |
| Candidate Comprehension | Favorite/hot candidate surfaces. | Activation only. |
| Review Queue | Review queue and review_due widgets. | Do not auto-approve. |
| Association / Activation | Stable entry point for hot/warm/cold navigation. | Strong activation reference. |
| Dev Context | Could show active project context, risks, and next gates. | Support layer. |
| Feedback | Use Ledger and negative feedback queue widgets. | Review pressure only. |
| Action / Use Ledger | Not action basis. | Link to action records, never replace them. |

## Local De-Dup / Collision

The earlier shallow file captured `workbench_dashboard`. This strong file adds
mechanisms:

- note-scoped dashboard class;
- stable buckets plus live Dataview widgets;
- explicit plugin/runtime dependency list;
- clear warning that dashboard output is activation only.

This reinforces existing VAKS decisions: dashboard, retrieval, metadata, brief,
and feedback are not reviewed knowledge.

## Anti-Borrow

- Do not copy the family/work/personal taxonomy.
- Do not enable Dataview inline JS in the formal VAKS vault without a plugin
  review and user approval.
- Do not make visual prominence influence borrow order, truth, or review state.
- Do not rely on a dashboard as the only recovery artifact.

## Candidate Tags

```yaml
domain: obsidian-dashboard-template
problem: human-scannable-vault-activation-without-truth-confusion
pattern:
  - home-dashboard-front-door
  - manual-links-plus-live-queries
  - note-scoped-presentation-class
  - explicit-plugin-dependency-surface
  - dashboard-not-evidence-warning
maturity: proven-template
problem_fit: 5
reuse_value: 4
implementation_cost: 2
integration_fit: 4
evidence_strength: 4
reversibility: 5
```

## Fusion Judgment

Adapt as a P1 workbench/activation reference. The usable borrow is a VAKS home
surface with explicit boundary labels, not a new truth dashboard.
