---
type: sandbox_design_note
status: candidate_only
created_at: 2026-06-07
scope: context pack builder v0 contract
truth_boundary: sandbox design note only; context pack is activation/action-prep, not reviewed knowledge
---

# Context Pack Builder v0 Contract

## Plain Rule

```text
Build a small, labeled working set for the question.
Do not turn the pack into truth.
```

## Local Evidence

Borrowed from existing VAKS materials:

```text
SCHEMA.md:
  context pack is a call/use layer output, not a reviewed knowledge layer.

IMPLEMENTATION_BLUEPRINT.md:
  make-context-pack is a future script; search similarity runs after trust fields.

DEV_CONTEXT.md and templates/dev-context-pack.md:
  Core / Support / Risk / Cold References are the working-memory model.

RAG eval / citation distillations:
  query-run receipt and pack item receipt need selectors, citable status, warnings.

source-intake control flow:
  action-facing support must return to raw or stable reviewed anchors.
```

## Inputs

```yaml
query:
mode: current-rule | research | action | source-inspection | audit | project-exploration
project_scope:
topic_scope:
time_or_version_scope:
action_facing: true | false
artifact_registry_ref:
hard_filters:
  knowledge_status_allowed: []
  retrieval_policy_allowed: []
  overlay_state_allowed: []
  path_roles_allowed: []
  path_roles_excluded: []
budgets:
  max_items:
  max_raw_drilldowns:
  max_candidate_items:
  max_audit_items:
```

## Build Pipeline

```text
1. Understand query and mode.
2. Read artifact registry / topic entry first.
3. Apply authority/status/project/path-role hard filters.
4. Retrieve inside allowed lanes.
5. Add link/entity/topic-pack expansion only inside allowed lanes.
6. Create pack item receipts.
7. Create query-run receipt.
8. For action-facing use, bind final claims to raw or reviewed anchors.
9. If support is missing, mark not_ready instead of filling with candidate material.
```

## Pack Manifest Shape

```yaml
record_kind: context_pack_manifest_candidate
pack_id:
created_at:
query_run_ref:
mode:
project_scope:
topic_scope:
action_facing:
truth_boundary: activation_pack_not_truth
artifact_registry_refs: []
items: []
coverage_overview:
  supported:
  weakly_supported:
  challenged:
  missing_evidence:
  out_of_scope:
  risk_flags:
action_readiness:
  state: ready | not_ready | risky | needs_review
  reason:
final_support:
  state: none | checked
  reason:
anchor_queue:
  total:
  note: navigation_queue_only_not_support
evidence_sufficiency:
  state: sufficient | weak | insufficient | out_of_scope | risky
  checked_for:
  missing: []
  required_next_step:
warnings: []
```

## Pack Item Shape

```yaml
item_id:
display_label:
lane: mainline_current | reviewed_support | candidate_orientation | raw_drilldown | active_project_overlay | audit_evidence | feedback_diagnostics
source_ref:
selector_or_offset:
snippet:
snippet_status: navigation_snippet_not_evidence
contextualized_snippet:
selection_priority:
selection_reason:
citable_status: activation_only | drilldown_required | span_ready
action_basis_allowed: true | false
action_role: navigation_only | anchor_queue_rule_or_template | anchor_queue_reviewed_or_review_ready | anchor_queue_raw_provenance | excluded_from_action_support
matched_channels: []
channel_ranks: []
rrf_rank:
rerank_score:
why_included:
exclusion_or_caution_note:
```

## Citable Status Rule

```text
activation_only:
  useful for orientation, never final support.

drilldown_required:
  useful as a pointer; open raw/reviewed anchor before support use.

span_ready:
  allowed only when a specific source selector or reviewed support item is ready
  for the current claim and scope.
```

Candidate, overlay, audit, feedback, score, graph, and dashboard items default to:

```text
activation_only or drilldown_required
action_basis_allowed: false
```

Selector and snippet rule:

```text
selector_or_offset:
  where to start reading.

snippet:
  a small preview for navigation.

snippet_status:
  must stay navigation_snippet_not_evidence unless a later evidence support
  check creates a separate reviewed support item.
```

Selection priority rule:

```text
pinned_ref
> exact_topic_match
> entity_match
> recent_scout_or_current_sandbox
> ordinary_match
```

This is navigation priority only. It is not authority, confidence, truth, or
action readiness.

## Mode Rules

```text
current-rule:
  mainline_current first; sandbox/candidate/audit excluded unless explicitly asked.

research:
  candidate and support review output allowed as orientation.

action:
  reviewed/mainline/raw anchors only for final support; candidate remains excluded
  from action basis.

audit:
  checks, packages, and sandbox evidence visible; not current rule by itself.

project-exploration:
  active project overlay allowed; other projects and archived overlays excluded.
```

## Query-Run Receipt

Every important pack should have a receipt:

```yaml
query_run_id:
timestamp:
mode:
query_type:
risk_type:
planner_output:
retrieval_profile:
hard_filters:
artifact_registry_refs: []
retrievers_called:
candidate_counts_by_lane:
fusion_method:
rank_window_size:
rerank_window:
selected_pack_id:
trace_events:
  - stage:
    input_refs: []
    output_refs: []
    warnings: []
content_trace_policy: refs_only | snippets_allowed | full_content_allowed
diagnostics:
  context_relevance:
  groundedness:
  answer_relevance:
  evidence_binding_status:
feedback_ref:
```

Default:

```text
content_trace_policy: refs_only
```

## Non-Goals

```text
No automatic answer generation.
No automatic promotion.
No hidden full-vault scan for every ordinary query.
No evidence sufficiency claim for ordinary orientation.
No cross-lane RRF.
No action basis from candidate, overlay, audit, feedback, or retrieval score.
```

## MVP Implementation Path

Do not start with a big engine.

Start with:

```text
1. manual/semi-manual pack manifest fixture
2. usage-layer lint
3. retrieval MVP lane output
4. one real topic pack trial
5. only then optional script wrapper
```

## Pressure Cases

```text
candidate match is top-ranked:
  include in research pack, exclude as final action support.

raw source has keyword match:
  include as drilldown pointer; require selector/warrant before support.

old sandbox explains why:
  include only in audit mode or explicit why/how query.

archived overlay matches project:
  exclude from default project pack.

pack lacks supporting anchor:
  action_readiness: not_ready.
```
