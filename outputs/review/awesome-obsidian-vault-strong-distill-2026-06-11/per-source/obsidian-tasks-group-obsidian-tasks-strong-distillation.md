---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/obsidian-tasks-group/obsidian-tasks"
repo_key: "obsidian-tasks-group/obsidian-tasks"
checked_commit: "141feb186d5ad4d260d86ff5afd950fc73185546"
checked_at: 2026-06-11
derived_from:
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/obsidian-tasks-group-obsidian-tasks-anchor-manifest.json
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
  - task-query-dsl
  - explanation-surface
  - source-line-writeback
fit_layer:
  - activation
  - decision-action
  - maintenance
  - risk-inhibition
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - truth-confidence
avoid:
  - "Do not treat task queries, urgency, or status as truth confidence."
  - "Do not enable JavaScript-in-query behavior by default."
  - "Do not let query result writeback mutate reviewed knowledge."
dev_context_hint:
  default_layer: support
  core_only_when: "When designing action/workbench query surfaces, explainable filters, or task-state writeback boundaries."
  support_when: "When comparing Obsidian plugin docs, query DSLs, or source-line mutation safety."
  risk_when: "When executable query expressions, urgency scores, or task statuses could be mistaken for truth/action readiness."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/obsidian-tasks-group-obsidian-tasks-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - task-dsl
  - explainable-query
---

# Strong Candidate Distillation: obsidian-tasks-group / obsidian-tasks

## Boundary

This file extracts query/workbench mechanics from the Obsidian Tasks plugin. It
does not adopt task status, urgency score, or query results as reviewed
knowledge, truth confidence, or action basis.

## What This Source Actually Is

Obsidian Tasks is a production Obsidian plugin for tracking Markdown tasks
across a vault. It parses checklist lines, exposes a `tasks` query block DSL,
can edit source tasks from query results, supports statuses, dates, recurrence,
grouping, sorting, limits, query explanations, and optional JavaScript
expressions.

The repository includes extensive documentation, TypeScript source, tests,
approved documentation samples, plugin metadata, and an Obsidian Publish docs
vault. Local Windows checkout surfaced filename-length failures in approved
test fixtures, so path-length risk is also part of this distillation.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Plugin identity, global filter setup, query examples, source-file update behavior, limit warning. | Query blocks can gather distributed items while preserving source-line writeback. | Query result is not evidence. |
| `docs/Queries/About Queries.md` | DSL overview, global query, query file defaults, presets, limits, sorting, grouping. | Layered query assembly and reusable instructions. | Query assembly is activation only. |
| `docs/Queries/Explaining Queries.md` | `explain` instruction expands dates, booleans, global query, file defaults, grouping, sorting. | Explainability surface for interpreted filters. | Explanation is not review. |
| `docs/Getting Started/Global Filter.md` | Optional global filter such as `#task`. | Capture scope filter. | Scope filter is not truth filter. |
| `docs/Getting Started/Statuses.md` | Custom statuses with symbol, name, next symbol, and type. | State machine-like task lifecycle. | Status type is not truth state. |
| `docs/Advanced/Urgency.md` | Numeric urgency score based on dates and priorities with documented limits. | Useful ranking can expose its formula and limits. | Urgency is not action readiness. |
| `docs/Scripting/About Scripting.md` and `src/Config/EnableJsInTasksQueries.ts` | JavaScript query expressions are disabled by default and require trust. | Executable query logic must be opt-in and vault-trust scoped. | Do not enable by default. |
| `src/Query/Explain/Explainer.ts` | Builds human-readable query explanations. | Interpreted context should be explainable. | Not evidence-aware review. |
| `src/Obsidian/FileParser.ts` | Parses Obsidian cached list items and file lines, handles stale cache line mismatch. | Source mutation/parsing must tolerate cache drift. | Parser robustness is not truth. |
| `tests/...approved.*` | Approved documentation/test samples, some with long Windows paths. | Docs-as-tests and fixture approval. | Long path risk needs intake lint. |

## Strong Borrow Points

1. **Distributed source, centralized view.**  
   Tasks keeps task lines in their original Markdown files while query blocks
   gather them anywhere. VAKS can borrow this for action/workbench views: surface
   candidate/action items without moving source notes.

2. **Query interpretation must be explainable.**  
   The `explain` instruction shows date expansion, boolean structure, global
   query, file defaults, grouping, sorting, and limits. VAKS context packs and
   activation views should expose why an item appeared, especially when used for
   decisions.

3. **Global defaults + local overrides need visible assembly order.**  
   Tasks assembles global query, query-file defaults, and code-block query
   source. VAKS can borrow this shape for context-pack policies: global
   guardrails, file/project defaults, then explicit task intent.

4. **State machines are useful, but not truth.**  
   Custom statuses define symbols, names, next status, and type. VAKS can borrow
   explicit transition tables for review queue/work items, while keeping truth
   confidence and evidence review separate.

5. **Ranking formulas need limitations next to the score.**  
   Urgency documents both formula and limits, including ignored dependencies.
   VAKS should expose rank/routing signals with their known omissions.

6. **Executable query logic must be opt-in.**  
   JavaScript in Tasks queries is disabled by default and tied to trust in the
   vault. This maps cleanly to VAKS risk/inhibition: no executable query
   behavior in ordinary capture or ordinary query.

7. **Docs-as-tests are valuable for behavior stability.**  
   Approved samples document query/status output. VAKS can borrow fixture-backed
   examples for helpers and projections, with the boundary that tests diagnose
   behavior but do not create truth.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Activation | Query DSL, global/local defaults, grouping, sorting, limits. | Context/workbench views. |
| Decision / Action | Source-line update from query result. | Human-approved action workbench only. |
| Maintenance | Explain output, docs fixtures, long path risk. | Query lint and fixture checks. |
| Risk / Inhibition | JavaScript disabled by default. | Explicit trust gate. |
| Reviewed Knowledge | No direct fit. | Keep separate. |

## Local De-Dup / Collision

This overlaps with DashboardPlusPlus and Obsidian Bases:

- DashboardPlusPlus is a dashboard composition reference.
- Bases-style workbench is metadata/view activation.
- Tasks adds a mature example of query DSL, explainability, source-line
  writeback, and status-transition modeling.

The unique borrow is the combination of explainable query assembly and
source-preserving mutation.

## Anti-Borrow

- Do not treat task completion as reviewed knowledge.
- Do not treat urgency as action readiness.
- Do not allow query blocks to mutate reviewed claims or relations.
- Do not enable JavaScript expressions without explicit trust and scope.
- Do not ignore Windows path-length risks in source snapshots and fixtures.

## Candidate Tags

```yaml
domain: explainable_task_query_workbench
problem: surfacing_distributed_markdown_items_without_moving_sources
pattern:
  - distributed-source-centralized-query
  - query-explain-output
  - global-local-query-assembly
  - status-transition-table
  - executable-query-opt-in
  - docs-as-approved-fixtures
maturity: production-obsidian-plugin
problem_fit: 5
reuse_value: 5
implementation_cost: 4
integration_fit: 4
evidence_strength: 5
reversibility: 4
```

## Fusion Judgment

Borrow strongly for activation/workbench query design, explanation surfaces,
and explicit executable-query risk gates. Do not borrow task status or urgency
as truth or action readiness.
