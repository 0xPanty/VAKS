---
record_kind: project_overlay
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
project_id: verified-action-knowledge-system
target_ref: outputs/review/2026-06-07-bilibili-obsidian-content-automation-jarvis-candidate-distillation.md
target_selector: automation_logic
target_hint: "Use only as active-project borrowing context for VAKS automation/workbench design."
project_borrow_scope:
  - project operating manual as AI entrypoint
  - feedback-to-constraint loop for future runs
  - version control as AI file-write safety net
  - local Markdown as executable context
borrow_tags:
  - P1/project_operating_manual_as_ai_entrypoint
  - P1/feedback_to_constraints_not_truth
  - P1/local_markdown_as_executable_context
  - P2/version_control_required_for_ai_file_work
  - P2/publishing_pipeline_as_tool_layer
project_non_borrow_scope:
  - auto-publishing in ordinary capture
  - feedback as truth confidence
  - ASR as reviewed evidence
  - private account/cookie/API-key routes by default
do_not_borrow_tags:
  - avoid/auto_publish_default
  - avoid/feedback_as_truth_confidence
  - avoid/asr_as_reviewed_evidence
  - avoid/private_account_routes_default
project_reopen_trigger:
  - "When designing VAKS project workbench or skill routing."
  - "When adding any external publishing/export connector."
  - "When promoting feedback-derived constraints into reviewed patterns."
confirmation_basis: "Derived from local ASR transcript and Bilibili public metadata; candidate-only."
last_checked_at: 2026-06-07
expires_at:
---

# VAKS Overlay: Obsidian Content Automation / Jarvis Workflow

## Boundary

This is a VAKS project-side overlay. It can guide active design discussion, but it cannot act as reviewed knowledge, decision, truth confidence, or action basis.

## Project Borrow Scope

For VAKS, the strong borrow is:

```text
project-local manual
-> skill trigger
-> source/context activation
-> candidate work output
-> feedback ledger
-> next-run constraints
-> versioned/synced file safety
```

## 借鉴标签

```yaml
P1:
  - project_operating_manual_as_ai_entrypoint
  - feedback_to_constraints_not_truth
  - local_markdown_as_executable_context
P2:
  - version_control_required_for_ai_file_work
  - publishing_pipeline_as_tool_layer
avoid:
  - auto_publish_default
  - feedback_as_truth_confidence
  - asr_as_reviewed_evidence
  - private_account_routes_default
```

Useful absorption:

- Treat `AGENTS.md`, handoffs, and project manuals as the local equivalent of the video's "workflow manual."
- Let repeated VAKS intake operations become skills/helpers only when trigger words and write boundaries are explicit.
- Keep feedback visible and reusable, but route it to usefulness, activation, review pressure, and constraints.
- Require Git/hash/sync safety whenever AI writes many files or artifacts.
- Use local Markdown to encode state, rules, and allowed operations, not just source text.

## Project Non-Borrow Scope

Do not absorb:

- automatic publication to WeChat/Feishu/GitHub as a default VAKS lane;
- automatic conversion of user preference into reviewed knowledge;
- automatic action basis from ASR, summary, dashboard, or skill output;
- project-specific creative style as global skill behavior;
- account/cookie/private-source operations without explicit authorization.

## Minimal Absorption Suggestion

No schema change needed now.

Use this as support for the existing direction:

- global skill stays generic;
- project-local manuals define VAKS-specific paths and write rules;
- file/video conversion creates raw text only;
- distillation creates candidate-only artifacts;
- feedback affects activation and review pressure, not truth.

## Reopen Trigger

Reopen when adding:

- a formal project workbench UI;
- an export/publishing connector;
- a feedback-to-constraint helper;
- stronger AI file-write automation;
- a reviewed pattern for "project operating manual as activation entrypoint."
