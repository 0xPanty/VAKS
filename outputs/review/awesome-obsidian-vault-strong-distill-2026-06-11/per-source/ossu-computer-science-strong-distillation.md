---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/ossu/computer-science"
repo_key: "ossu/computer-science"
checked_commit: "78b1ef4953105761535af668e02cad505bcc6a79"
checked_at: 2026-06-11
derived_from:
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/ossu-computer-science-anchor-manifest.json
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
  - curriculum-route-map
  - selection-criteria
  - prerequisite-gates
  - stale-resource-warning
fit_layer:
  - activation
  - decision-support
  - candidate-comprehension
  - maintenance
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - automatic-truth-update
avoid:
  - "Do not treat course lists as evidence for technical claims."
  - "Do not import the curriculum route without checking current course availability."
  - "Do not make Discord/community status a truth signal."
dev_context_hint:
  default_layer: support
  core_only_when: "When designing route maps, prerequisite gates, or learning-plan context packs."
  support_when: "When comparing criteria-backed curation, extras/core split, and help/contribution channels."
  risk_when: "When external course availability, pricing, or platform access has drifted."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/ossu-computer-science-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - curriculum
  - route-map
---

# Strong Candidate Distillation: ossu / computer-science

## Boundary

This file extracts route-map and curation-governance lessons. It does not treat
OSSU course lists, prerequisites, or community advice as reviewed technical
knowledge or current enrollment guidance.

## What This Source Actually Is

OSSU Computer Science is a maintained open curriculum for a self-taught CS
education. It organizes a learning path into prerequisites, Intro CS, Core CS,
Advanced CS, and Final Project. It also states selection criteria, curricular
guidelines, expected duration/effort, cost warnings, help paths, contribution
rules, and stale-resource warnings.

For VAKS, this is most useful as a model of criteria-backed curation and route
maps.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Summary, selection criteria, route, prerequisites, duration, cost, process, stale warnings. | Route map should explain selection basis and caveats. | Course list drifts. |
| `CURRICULAR_GUIDELINES.md` | Points to ACM/IEEE CS2013 and notes CS2023 development. | External standard anchors can justify curation. | Standard link is not local evidence review. |
| `FAQ.md` | Explains no degree, deprecated app, Coursera audit/access changes, ordering options. | Stale/deprecated ecosystem notes belong near user decision points. | Facts are time-sensitive. |
| `HELP.md` | Routes help by course-specific vs general problems and asks users to state prior attempts. | Help routing can preserve scope and reduce noise. | Community answer not truth. |
| `CONTRIBUTING.md` | Separates non-substantive and substantive curriculum changes. | Change type determines review path. | Issue discussion is not automatic adoption. |
| `coursepages/ostep/README.md` | Base vs extended route, prerequisites, environment setup, warnings. | Course pages can add local gates and alternatives. | Commands/resources drift. |
| `extras/courses.md` | High-quality courses that did not fit curriculum. | Core vs extras split prevents route bloat. | Extras are not hidden core. |

## Strong Borrow Points

1. **Curation needs explicit selection criteria.**  
   OSSU states what courses must satisfy. VAKS should require explicit adoption
   reasons for patterns or references promoted from candidate status.

2. **Route maps should expose prerequisites, effort, and alternatives.**  
   The curriculum tables show duration, effort, prerequisites, and discussion
   links. VAKS context packs can borrow this shape for learning/action routes.

3. **Core vs extras prevents taxonomy sprawl.**  
   High-quality but non-fitting resources go to `extras`. VAKS can mirror this:
   valuable but non-core references should remain support, not inflate the core
   architecture.

4. **Stale-resource warnings belong in the user-facing route.**  
   OSSU warns about outdated third-party materials and platform access changes.
   VAKS should surface temporal applicability warnings before decisions.

5. **Change proposals should separate typo/link fixes from substantive changes.**  
   `CONTRIBUTING.md` gives a simple governance split. VAKS review queue can use
   similar routing: maintenance lint vs architecture/pattern promotion.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Activation | Route tables and prerequisites. | Context-pack route map. |
| Candidate Comprehension | Course/resource description. | Candidate resource card. |
| Review Queue | Substantive vs non-substantive change routing. | Queue taxonomy. |
| Temporal Applicability | Deprecated/outdated resource warnings. | Staleness check. |
| Decision Support | Effort/cost/prerequisite disclosure. | Decision envelope. |

## Local De-Dup / Collision

This overlaps with `javascript-tutorial` and `keyvanakbary/learning-notes`:

- JavaScript.info is a tutorial source tree.
- Learning Notes is personal recall over consumed sources.
- OSSU is a curated route map with selection criteria and community governance.

Its unique VAKS value is criteria-backed routing, not note content.

## Anti-Borrow

- Do not import course links without current availability checks.
- Do not treat a curriculum as evidence for any CS claim.
- Do not make community channels part of truth confidence.
- Do not collapse `extras` into core just because the resources are high value.

## Candidate Tags

```yaml
domain: curated_learning_route
problem: building_a_criteria_backed_curriculum_without_overloading_core
pattern:
  - explicit-selection-criteria
  - prerequisite-effort-route-table
  - core-vs-extras-split
  - stale-resource-warning
  - substantive-change-routing
maturity: maintained-community-curriculum
problem_fit: 4
reuse_value: 5
implementation_cost: 3
integration_fit: 4
evidence_strength: 4
reversibility: 4
```

## Fusion Judgment

Borrow strongly for route-map governance and temporal caveats. Keep all course
availability and learning recommendations as time-sensitive support, not truth.
