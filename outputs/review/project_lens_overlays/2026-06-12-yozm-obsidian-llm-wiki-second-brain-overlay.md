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
target_ref: outputs/review/2026-06-12-yozm-obsidian-llm-wiki-second-brain-candidate-distillation.md
target_selector: candidate_distillation
target_hint:
  - type: operator-command
    value: ingest-query-lint
    status: conceptual
    anchor_version: candidate-workflow-only
  - type: context-entrypoint
    value: root-manual-session-start
    status: conceptual
    anchor_version: candidate-workflow-only
  - type: risk
    value: sensitive-data-full-vault-query
    status: active-risk-reference
    anchor_version: 2026-06-12-source-capture
  - type: doc
    value: SOURCE_INTAKE.md#Medium Processing
    status: healthy
    anchor_version: 2026-06-12-file-read
  - type: doc
    value: DEV_CONTEXT.md#Dev Context Layers
    status: healthy
    anchor_version: 2026-06-12-file-read
project_borrow_scope:
  - Borrow the three-command operator surface: ingest, query, lint.
  - Borrow root operating manual / session-start entrypoint as support for local AGENTS, handoff, and DEV_CONTEXT recovery.
  - Borrow lint categories as maintenance-manifest inputs: sensitive data, broken links, orphan pages, contradiction pressure, missing anchors.
  - Borrow desktop/mobile capture surfaces only as source intake candidates, not as reviewed knowledge writeback.
  - Borrow personal/team wiki boundary as a future scope and privacy design check.
project_non_borrow_scope:
  - Do not copy the article's implicit "all personal data in one AI-accessible wiki" posture into VAKS.
  - Do not let AI agents write reviewed wiki nodes, truth confidence, decisions, reviewed relations, or action basis directly.
  - Do not make full-vault query the default context strategy.
  - Do not use Obsidian graph links as reviewed relations.
  - Do not treat GitHub Private Repo, token setup, or Working Copy as verified security architecture.
  - Do not treat regex masking as sufficient sensitive-data handling.
  - Do not start scheduled lint or hooks without an explicit implementation task.
project_reopen_trigger:
  - User asks to design a VAKS `/ingest`, `/query`, or `/lint` command.
  - VAKS begins an Obsidian operator cockpit or mobile/desktop capture workflow.
  - VAKS needs SessionStart / AGENTS / handoff automation.
  - A future task needs privacy boundaries for personal notes, screenshots, or team sharing.
confirmation_basis:
  - user explicitly said "蒸馏这个"
  - public article read through browser extraction
  - full HTML hash captured without retaining full copyrighted text
  - source card and candidate distillation created with candidate-only boundaries
last_checked_at: 2026-06-12
expires_at:
borrow_value: strong
borrow_order:
  - "P1: ingest / query / lint as VAKS operator commands"
  - "P2: root manual and session-start context entrypoint as recovery/consistency support"
  - "P3: sync/capture mechanics after security and official-doc checks"
avoid:
  - "No full-vault query as default."
  - "No direct AI-to-reviewed-wiki writes."
  - "No scheduled auto-fixes without review."
  - "No sensitive personal data aggregation without explicit privacy design."
tags:
  - project-lens
  - VAKS
  - obsidian-workbench
  - llm-wiki
  - source-intake
  - lint
  - query
  - candidate-only
---

# Project Lens: Yozm Obsidian LLM Wiki for VAKS

## Boundary

This is a project-scoped sidecar. It does not rewrite the source card,
candidate distillation, reviewed note, decision, or pattern.

It can guide future VAKS operator-command design, Obsidian workbench design, or
intake/query/lint workflow design, but it cannot act as reviewed knowledge or
action basis.

## Project Borrow Scope

For VAKS, borrow the source narrowly:

```text
Use the operator workflow shape.
Do not borrow the authority model.
```

Concrete borrow:

- `/ingest` as a future user-visible command for raw capture, candidate extraction, and route suggestion.
- `/query` as authority-bucketed activation, not full-vault belief.
- `/lint` as maintenance manifest generation, not auto-repair.
- Root operating manual as the reason `AGENTS.md` should stay short, local, and file-first.
- Session-start context injection only if it reads current local files and keeps candidate material marked as candidate.
- Personal/team wiki split as a privacy and scope boundary.

## Project Non-Borrow Scope

Do not borrow:

- Full-vault prompting as a default.
- Direct LLM-to-reviewed-vault writes.
- Scheduled lint that silently edits durable knowledge.
- Obsidian links or graph view as reviewed relation evidence.
- Private GitHub repo as a complete security model.
- Regex masking as proof of sensitive-data safety.
- Personal all-context vault as the default shape for a project/team knowledge system.

## Reopen Trigger

Reopen this overlay when:

```text
VAKS starts an operator-command prototype.
The user asks for `/ingest`, `/query`, or `/lint`.
The project designs Obsidian desktop/mobile capture.
The project considers session-start hooks or automatic handoff loading.
The project handles personal/private notes or team-share boundaries.
```

## Minimal Pilot Shape

```yaml
pilot_scope: sandbox_only
first_candidate_command: lint
why_lint_first: "It can surface risk without writing truth-bearing content."
inputs:
  - source cards
  - candidate distillations
  - project overlays
  - reviewed docs only as read-only targets
checks:
  - authority bucket visible
  - no action_basis_allowed true from raw/candidate/overlay
  - no reviewed note mutation
  - sensitive-data warning reported as review_pressure, not auto-redaction
  - broken links and missing anchors emitted as maintenance manifest rows
pass_result:
  - candidate operator-command pattern
fail_result:
  - keep as design-only reference
```

## Confirmation

```yaml
confirmation_basis:
  user_request: "蒸馏这个"
  inspected_source:
    - raw/articles/2026-06-12-yozm-obsidian-llm-wiki-second-brain-source.md
    - raw/articles/2026-06-12-yozm-obsidian-llm-wiki-second-brain-source/capture-notes.md
  conclusion: "strong operator-workflow reference; high-risk if copied as full-vault query or direct AI write authority"
last_checked_at: 2026-06-12
```
