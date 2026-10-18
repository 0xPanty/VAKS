---
record_kind: project_overlay
type: project_lens_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: VAKS
project_name: Verified Action Knowledge System / 资料库
target_ref: outputs/review/2026-06-11-cyrilxbt-n8n-obsidian-business-brain-candidate-distillation.md
target_selector: candidate_distillation
target_hint:
- type: workflow
  value: obsidian-operator-cockpit/daily-weekly-monthly-cadence
  status: conceptual
  anchor_version: candidate-workflow-only
- type: workflow
  value: decision-review-loop
  status: conceptual
  anchor_version: candidate-workflow-only
- type: doc
  value: DEV_CONTEXT.md#Dev Context Layers
  status: healthy
  anchor_version: 2026-06-11-file-read
- type: doc
  value: SOURCE_INTAKE.md#Medium Processing
  status: healthy
  anchor_version: 2026-06-11-file-read
project_borrow_scope:
- Borrow the daily/weekly/monthly cadence as a future VAKS operator cockpit reference.
- Borrow the shared context-file idea as a DEV_CONTEXT/context-pack surface, not as
  truth authority.
- Borrow the decision logger fields: decision, assumption, expected outcome, review
    date, review criteria, risk.
- Borrow pattern detector prompts as synthesis pressure only when several independent
  source classes point in the same direction.
- Consider N8N only as a future connector surface after a small sandbox, not as the
  core vault engine.
project_non_borrow_scope:
- Do not let N8N, Claude, or any automation write reviewed wiki nodes, truth confidence,
  decisions, or action basis directly.
- Do not auto-update core context files from generated briefings; updates must be
  candidate patches or human-reviewed edits.
- Do not treat daily/weekly/monthly generated summaries as independent evidence.
- Do not run private CRM/email/support/finance ingestion unless the user explicitly
  authorizes source scope, retention, and privacy boundaries.
- Do not create a new formal "business brain" lane; map useful pieces into existing
  Capture, Understand, Review, Connect, Act and Learn layers.
project_reopen_trigger:
- User asks to build an Obsidian/N8N workflow, daily brief, weekly review, or operator
  cockpit.
- VAKS needs a first automation prototype for intake routing, review_due reminders,
  or decision outcome reviews.
- A future implementation task can verify N8N filesystem behavior and official API
  details.
confirmation_basis:
- user explicitly said "蒸馏"
- pasted text retained as raw article snapshot
- source card and candidate distillation created with candidate-only boundaries
last_checked_at: 2026-06-11
expires_at: null
borrow_value: medium
borrow_order:
- 'P1: operator cadence and shared context surface'
- 'P2: decision review and pattern synthesis prompt shapes'
- 'P3: N8N implementation mechanics only after sandbox verification'
avoid:
- No automatic truth mutation from LLM or N8N outputs.
- No generated-output-as-evidence chain.
- No private business-system ingestion without explicit authorization.
tags:
- project-lens
- VAKS
- obsidian-workbench
- n8n
- automation
- candidate-only
review_pressure: none
legacy_overlay_compatibility: true
canonical_p0_included: false
canonical_current_lint_scope: false
legacy_storage: outputs/review/_legacy_project_lens
truth_boundary: legacy project lens compatibility artifact only; not canonical overlay;
  not reviewed knowledge; not action basis
---

# Project Lens: N8N + Obsidian Business Brain for VAKS

## Boundary

This is a project-scoped sidecar. It does not rewrite the source card,
candidate distillation, reviewed note, decision, or pattern.

It can guide future VAKS automation or Obsidian workbench design, but it cannot
act as reviewed knowledge or action basis.

## Project Borrow Scope

For VAKS, borrow the source narrowly:

```text
Use the workflow rhythm.
Do not borrow the authority model.
```

Concrete borrow:

- Daily activation surface: what needs attention, what is review_due, what changed recently.
- Weekly closeout surface: what moved, what stalled, what assumptions changed, what needs review.
- Monthly synthesis surface: candidate patterns from multiple source classes.
- Decision review loop: assumption, expected outcome, review criteria, review date.
- Shared context surface: a visible context file or cockpit that reads VAKS layers by authority bucket.

## Project Non-Borrow Scope

Do not borrow:

- Direct LLM-to-reviewed-vault writes.
- Auto updates to core context files.
- Full-vault prompting as a default.
- Briefings as evidence.
- Repeated generated summaries as independent support.
- Private business-tool ingestion without explicit user authorization.
- N8N as a required core dependency before a small sandbox proves value.

## Reopen Trigger

Reopen this overlay when:

```text
VAKS starts an Obsidian operator cockpit.
The user asks for N8N automation.
The project needs daily/weekly/monthly review surfaces.
The project needs decision outcome review reminders.
```

## Minimal Pilot Shape

```yaml
pilot_scope: sandbox_only
first_candidate_workflow:
  - review_due_and_recent_intake_brief
inputs:
  - reviewed records bucket
  - candidate records bucket
  - project overlays bucket
  - review_due / blocked markers
checks:
  - authority badge visible
  - no action_basis_allowed true from candidate material
  - source anchors shown for important claims
  - generated output saved as outputs/review or outputs/qa, not reviewed wiki
  - context-file update emitted as patch suggestion only
pass_result:
  - candidate operator cockpit pattern
fail_result:
  - keep as design-only reference
```

## Confirmation

```yaml
confirmation_basis:
  user_request: "蒸馏"
  inspected_source:
    - raw/articles/2026-06-11-cyrilxbt-n8n-obsidian-business-brain-source.md
    - raw/articles/2026-06-11-cyrilxbt-n8n-obsidian-business-brain-source/pasted-text.txt
  conclusion: "medium-value workflow/cadence reference; high-risk if copied as direct automation authority"
last_checked_at: 2026-06-11
```
