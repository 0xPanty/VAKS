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
target_ref: outputs/review/2026-06-07-mindstudio-ai-second-brain-obsidian-folder-architecture-candidate-distillation.md
source_card: raw/articles/2026-06-07-mindstudio-ai-second-brain-obsidian-vault-folder-architecture-source.md
target_selector: ai_obsidian_folder_architecture
target_hint: "Use only as active-project borrowing context for VAKS source intake UX, project manuals, and optional workbench modules."
project_borrow_scope:
  - raw -> processed -> wiki as a plain source-state spine
  - agents.md as inspectable project behavior spec
  - index.md as pointer/navigation layer
  - log.md as operation trace
  - journal and CRM as optional use-context modules
  - question-generated wiki as candidate synthesis only
project_non_borrow_scope:
  - For VAKS, do not borrow the article's "7 folders" count as schema because the body actually describes five folders plus root files.
  - For VAKS, do not borrow generated wiki pages as reviewed truth because candidate/reviewed/action-basis are separate.
  - For VAKS, do not borrow hourly Codex automation as default because ordinary capture and intake must remain explicit.
  - For VAKS, do not borrow auto commit/push as default because commit and push are separate user decisions.
  - For VAKS, do not borrow journal/CRM into core before privacy, scope, and retrieval boundaries exist.
borrow_tags:
  - P1/raw_processed_wiki_state_spine
  - P1/agents_md_as_behavior_spec
  - P1/index_log_as_navigation_and_trace
  - P2/journal_crm_as_optional_use_context
  - P2/question_generated_wiki_as_candidate_synthesis
  - P3/web_clipper_hourly_automation_as_tool_reference
do_not_borrow_tags:
  - avoid/folder_count_as_schema
  - avoid/generated_wiki_as_reviewed_truth
  - avoid/hourly_automation_default
  - avoid/auto_commit_push_default
  - avoid/journal_crm_as_core_without_privacy_boundary
project_reopen_trigger:
  - "When designing VAKS source intake folder/state UX."
  - "When writing a plain-language VAKS vault architecture explanation."
  - "When considering journal, CRM, or personal context modules."
  - "When considering scheduled source processing or auto commit/push."
  - "When defining project-local manuals as agent behavior specs."
confirmation_basis: "User explicitly requested distillation; public MindStudio page observed on 2026-06-07 with HTTP 200 and HTML hash."
last_checked_at: 2026-06-07
expires_at:
---

# VAKS Overlay: MindStudio AI Second Brain Folder Architecture

## Boundary

This is a VAKS project-side overlay.

It can guide active design discussion, but it cannot act as reviewed knowledge, decision, truth confidence, or action basis.

## Project Borrow Scope

For VAKS, the useful borrow is:

```text
source state should be visible in the file structure;
agent behavior should be visible in markdown manuals;
navigation and operation traces should be first-class files;
use-context modules should stay optional and scoped.
```

Practical borrowing:

- Use `/raw` / processed-state / candidate wiki as a plain explanation layer for source intake.
- Treat `agents.md` as a good analogy for VAKS `AGENTS.md`, handoffs, and skill manuals.
- Treat `index.md` as navigation and `log.md` as operation trace.
- Treat journal/CRM as optional project/personal modules, not VAKS core.
- Treat question-generated notes as candidate synthesis, not reviewed knowledge.

## 借鉴标签

```yaml
P1:
  - raw_processed_wiki_state_spine
  - agents_md_as_behavior_spec
  - index_log_as_navigation_and_trace
P2:
  - journal_crm_as_optional_use_context
  - question_generated_wiki_as_candidate_synthesis
P3:
  - web_clipper_hourly_automation_as_tool_reference
avoid:
  - folder_count_as_schema
  - generated_wiki_as_reviewed_truth
  - hourly_automation_default
  - auto_commit_push_default
  - journal_crm_as_core_without_privacy_boundary
```

## Project Non-Borrow Scope

For VAKS, do not currently borrow:

```text
7 folders as schema
generated wiki as reviewed truth
hourly Codex automation as default
auto commit/push as default
journal/CRM as core modules
```

Why:

```text
VAKS is stricter than an AI second-brain demo.
It needs source provenance, candidate comprehension, review, reviewed relations,
action basis, and feedback boundaries.
```

## Minimal Absorption Suggestion

No schema change now.

Useful near-term wording:

```text
raw = incoming source
processed/ledger = handled source trail
candidate wiki = understood but not reviewed
index = navigation
log = operation receipt
manual = behavior spec
```

Keep the actual VAKS implementation names governed by local manuals and templates.

## Reopen Trigger

Reopen when adding:

- source intake state view;
- human-facing VAKS architecture explainer;
- journal/CRM/personal context module;
- scheduled intake;
- Git backup/commit policy;
- project-local manual or behavior-spec design.

## Confirmation

```yaml
confirmation_basis: "User explicitly said to distill this article."
last_checked_at: 2026-06-07
```
