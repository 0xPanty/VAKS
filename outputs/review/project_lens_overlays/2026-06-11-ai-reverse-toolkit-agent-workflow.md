---
type: project_overlay
record_kind: project_lens_overlay
status: candidate
title: "ai-reverse-toolkit agent workflow overlay for VAKS"
project_id: verified-action-knowledge-system
source_ref: "raw/repos/2026-06-11-zhizhuodemao-ai-reverse-toolkit-source.md"
review_ref: "wiki/summaries/2026-06-11-zhizhuodemao-ai-reverse-toolkit-architecture-review.md"
distillation_ref: "outputs/review/2026-06-11-zhizhuodemao-ai-reverse-toolkit-candidate-distillation.md"
general_pattern_ref: "outputs/review/2026-06-11-ai-reverse-toolkit-general-workflow-patterns.md"
created_at: "2026-06-11"
created_by: Codex
knowledge_status: candidate
processing_tier: heavy
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
action_basis_allowed: false
truth_mutation_allowed: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: evidence_aware_review_required
borrow_value: strong
target_layers:
  - source-intake-workflow
  - retrieval-query-run
  - blackbox-product-analysis
  - context-pack-builder
  - evidence-sufficiency-gate
  - skill-evaluation
non_target_layers:
  - reviewed-truth
  - evidence-support
  - action-basis
  - security-bypass-operations
tags:
  - project-overlay
  - candidate
  - ai/skill-workflow
  - vaks/process-inspiration
  - vaks/retrieval-diagnostics
  - risk/security-bypass-excluded
---

# ai-reverse-toolkit Agent Workflow Overlay For VAKS

## Overlay Purpose

This overlay records how `zhizhuodemao/ai-reverse-toolkit` should be retrieved
for the Verified Action Knowledge System project. It is a project-side
candidate lens, not reviewed knowledge, not a decision, and not action basis.

Use it when discussing future VAKS agent workflows, black-box product analysis,
retrieval diagnostics, context-pack construction, or VAKS skill design.

Do not use it as a source for security bypass operations.

## Project-Specific Answer

For VAKS, the main value is:

```text
expert workflow as AI-executable skill
```

Not:

```text
reverse engineering tactics as project behavior
```

VAKS adaptation:

```text
user intent
-> trigger bounded skill
-> choose allowed tools and data layers
-> run diagnostic loop
-> produce candidate artifacts
-> stop at completion standard
-> review/action gates remain separate
```

## Borrow Scope

Borrow strongly:

- Skill trigger and do-not-trigger boundaries.
- Stage-scoped completion standards.
- Strategy selection based on signal.
- Diagnostic loop with failure taxonomy.
- Progressive disclosure via references.
- Intermediate artifacts and rollback.
- Skill evaluation with baselines, assertions, grading, and human feedback.

Borrow carefully:

- Black-box product analysis workflow as controlled probes and before/after diffs.
- Tool adapter pattern for future browser/local-file inspection.
- Eval viewer/workbench idea for reviewing skill outputs.

## Non-Borrow Scope

Do not borrow:

- Signature bypass operations.
- Anti-debug evasion tactics.
- Login/member/authorization bypass.
- Private implementation extraction.
- Any workflow that turns tool success into truth confidence.

## VAKS Implementation Hint

Potential first VAKS skills inspired by this source:

```text
vaks-source-intake
vaks-blackbox-product-analysis
vaks-retrieval-query-run
vaks-context-pack-builder
vaks-evidence-sufficiency-gate
vaks-feedback-ledger
```

Each should include:

```text
trigger
do-not-trigger
input contract
allowed artifacts
diagnostic tree
forbidden promotions
completion standard
minimal eval fixture
```

## Reopen Triggers

Reopen this overlay when:

- VAKS formalizes agent/skill workflows.
- A retrieval query-run tool is designed.
- A black-box product analysis lane is created.
- VAKS builds a context-pack builder.
- Skill evaluations become part of maintenance lint.

## One Sentence For Future Context Packs

`ai-reverse-toolkit` is a strong candidate reference for turning expert workflows
into bounded, testable AI skills; VAKS should borrow that workflow discipline
while excluding security-bypass tactics and preserving truth/action boundaries.
