---
record_type: dev-context-pack
context_id:
project:
task:
scope_key:
created:
updated:
created_by:
status: active
mode: development
base_memory_policy: "Use base activation tiers as input signals, but this pack is task-specific."
activation_policy: "Core requires likely-next-use for this task; cold references are opened only for evidence/history/conflict."
verification_status: draft
---

# Dev Context Pack

## AI-readable preamble

This is a temporary development-mode context pack.

Use Core first. Expand to Support when needed. Check Risk before decisions or writes. Open Cold References only for evidence, history, or contradiction checks.

Activation Tier rule:

```text
The vault has activation tiers, not truth tiers.
Hot means read early, not believe more.
```

## Task

```text

```

## Project Gate

This pack is valid only if the current task has a concrete goal, next action, or stop condition.

Goal:

```text

```

Next action:

```text

```

Stop condition:

```text

```

## Scope

In scope:

```text

```

Out of scope:

```text

```

## Context Briefing

Low-token summary used to decide what to open in full.

| File | Summary | Why suggested | Suggested layer |
|---|---|---|---|
|  |  |  |  |

Briefing rule:

```text
Use the briefing to choose reads. Do not treat the briefing as evidence.
```

## Core

Files that must be read and obeyed for this task.

| File | Why core | Required use |
|---|---|---|
|  |  |  |

Core rule:

```text
A file is Core only when the current task cannot safely proceed without it.
```

## Support

Relevant background to expand when design or implementation choices appear.

| File | Why support | When to open |
|---|---|---|
|  |  |  |

## Risk

Anti-patterns, negative evidence, contradictions, and do-not-build-first constraints.

| File | Risk | Checkpoint |
|---|---|---|
|  |  |  |

Risk rule:

```text
Check Risk before decisions, writes, or scope expansion.
```

## Association Neighborhood

Use this when the task needs context activation around a query, action basis, decision, contradiction, or risk check.
It is a retrieval / activation surface, not proof.

| Item | Why activated | Layer | Boundary |
|---|---|---|---|
|  |  | Core / Support / Risk / Decision / Scope / Cold |  |

Association rule:

```text
The pack activates an evidence-backed neighborhood, not isolated chunks.
Graph traversal, PPR, similarity, or association score can explain why something was recalled.
They cannot count as support, confidence, coverage, or reviewed relation.
Key judgments still need evidence_support, coverage_map, and evidence_sufficiency when used for action.
```

## Graph Retrieval Strata

Use this to show what kind of retrieval brought material into the pack.
It is an audit surface for recall, not a trust surface.

```yaml
retrieval_strata:
  low_level:
    source_refs: []
    text_unit_refs: []
    claim_refs: []
    entity_refs: []
  high_level:
    pattern_refs: []
    theme_refs: []
    community_refs: []
    community_report_refs: []
  relation_neighborhood:
    seed_refs: []
    relation_refs: []
    traversal_basis:
    boundary_note:
```

Strata rule:

```text
Low-level retrieval finds concrete anchors.
High-level retrieval finds themes, patterns, and community briefings.
Relation-neighborhood retrieval finds nearby reviewed relations and context.
TextUnit anchors are provenance, not support.
Community reports are briefings, not truth.
Graph rank is retrieval priority, not trust.
Auto-extracted relations are candidates until reviewed.
If relation-neighborhood retrieval uses candidate relations, label it candidate_relation_neighborhood.
```

## Temporal Applicability

Use this when a key judgment may depend on time, version, project, environment, supersession, or stale state.

```yaml
temporal_applicability:
  valid_from:
  valid_until:
  superseded_by:
  invalidated_by:
  applies_to:
    project:
    version:
    environment:
    timeframe:
    conditions:
  check_state: in_scope | out_of_scope | stale | superseded | unknown | needs_review
  reviewer_note:
```

Applicability rule:

```text
Truth is source-backed.
Applicability is time-, version-, and scope-bound.
Stale is review pressure.
valid_until / out-of-scope is applicability.
Stale, superseded, or out-of-scope points can remain useful history, but they cannot make an action basis ready.
```

## Decision Superseding

Use this when a decision used by the pack may have been replaced or narrowed by a newer decision.

```yaml
decision_superseding:
  old_decision:
  replacement_decision:
  supersession_reason:
  affected_claims:
    -
  affected_patterns:
    -
  affected_relations:
    -
  mark_review_due: true | false
  audit_note:
```

Superseding rule:

```text
Old decisions stay auditable.
Replacement changes the current action basis only within its scope.
Affected downstream items should be marked review_due before the pack is treated as action-ready.
```

## Intent Confirmation / Backbrief

Use this only for significant action, architecture change, implementation, deployment, high-impact decision, or hard-to-rollback work.

```yaml
intent_confirmation:
  required: true | false
  restated_intent:
  assumptions:
    -
  scope_in:
    -
  scope_out:
    -
  success_criteria:
    -
  verification_plan:
  user_confirmed: true | false
  confirmation_ref:

backbrief:
  plan_summary:
  acceptance_criteria_interpretation:
  numbered_assumptions:
    -
  risks:
    -
  verification_method:
  approved_by:
```

Intent rule:

```text
Evidence sufficiency asks whether the basis is good enough.
Intent confirmation asks whether the system is about to do the right thing.
Do not trigger for ordinary query or simple capture.
```

## Coverage Map

Use this only for key judgments in the answer or action basis. Do not turn the pack into a full audit report.
Every pack should be coverage-aware, but ordinary use can keep only the overview plus high-risk, challenged, or missing-evidence items.
Expand full `coverage_map` detail only for decisions, action basis, agent context packs, high-impact answers, explicit audit requests, or challenged answers.

## Context Pack Trace

Use this to explain why material entered the pack and what was ignored. It is a trace / use-ledger surface, not a trust surface.

```yaml
context_pack_trace:
  used_sources:
    -
  ignored_sources:
    -
  ignored_reason:
  activation_role: core | support | risk | cold_reference
  unresolved_contradictions:
    -
  risk_flags:
    -
```

Trace rule:

```text
Trace explains selection and omission.
It does not create support, confidence, or reviewed relations.
Retrieved-but-ignored material can still matter later as a missing-context or review_due candidate.
```

```yaml
coverage_overview:
  supported:
  weakly_supported:
  challenged:
  missing_evidence:
  out_of_scope:
  risk_flags:

coverage_map:
  - point:
    point_type:
    coverage_status: supported | weakly_supported | challenged | missing_evidence | out_of_scope | not_verifiable
    support_refs:
    challenge_refs:
    risk_refs:
    critical_omissions:
    note:

action_readiness:
  state: ready | not_ready | risky | needs_review
  reason:
```

Coverage rule:

```text
Citations are not enough.
Coverage status does not change truth confidence.
Coverage can consume evidence_support, but background_context cannot count as supported.
Risk flags are only overview signals; concrete risks stay in risk_refs and action_readiness.
Critical omissions are known major omissions only, not a full omission scan.
```

## Evidence Sufficiency Gate

Use this only before action basis, decision, promotion, strong reviewed relation, risk_sensitive_answer, or when the user asks whether evidence is enough.
Run it after the draft evidence/context envelope is assembled, before marking the pack action-ready.

```yaml
evidence_sufficiency:
  state: sufficient | weak | insufficient | out_of_scope | risky
  checked_for: context_pack | action_basis | decision | promotion | reviewed_relation | risk_sensitive_answer
  missing:
    -
  required_next_step: proceed | ask_user | retrieve_more | create_missing_point | narrow_scope | mark_not_actionable | needs_review
  reviewer_note:
```

Gate rule:

```text
Ordinary capture and ordinary query do not trigger this gate.
If evidence is insufficient, do not output a ready action basis.
If evidence is weak, expose gaps and weak support.
If evidence is out of scope, show the scope mismatch.
If evidence is out of scope only for the broad request, narrow_scope may be the right next step.
If evidence is risky, set action_readiness to risky or needs_review.
retrieve_more is a recommendation unless the user explicitly authorizes retrieval.
```

## Decision Outcome Calibration

Use after action or decision follow-up, not while constructing the original evidence basis.

```yaml
decision_outcome:
  decision_ref:
  action_basis_ref:
  recommendation:
  confidence_at_decision:
  user_choice:
  outcome: succeeded | failed | mixed | unresolved
  outcome_note:
  affects:
    - future_recommendation
    - risk_calibration
    - scope_fit
    - option_framing
  never_affects_directly:
    - truth_confidence
    - verification_status
    - source_reliability
```

Outcome rule:

```text
Outcome calibration improves future recommendation.
It does not prove the underlying claims true.
```

## Cold References

Traceable sources and historical records. Do not load by default.

| File | Why retained | Open when |
|---|---|---|
|  |  |  |

Cold rule:

```text
Cold can be relevant without being loaded. Open it only for source evidence, history, or contradiction checks.
```

## Open Questions

-

## Stop Conditions

Stop or refresh this pack when:

-

## Writeback Targets

If the task produces durable knowledge, update:

-

## Exit Notes

At completion, record:

```text
What changed:
What should stay hot:
What cools to warm:
What returns to cold:
Follow-up:
```

## Closeout Scan

Before archiving this pack, decide:

```text
Reusable pattern / decision / implementation note:
One-off evidence returning to cold:
New risk or anti-pattern:
Missing source or review work:
Session/fix capture needed:
```
