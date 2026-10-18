---
record_kind: project_overlay
type: project_lens_overlay
status: candidate
knowledge_status: candidate
processing_tier: heavy
overlay_state: confirmed
review_pressure: none
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
project_id: MISA_VAKS
project_name: "MISA using VAKS / 资料库"
target_ref: "outputs/review/2026-06-14-rohitg00-agentmemory-candidate-distillation.md"
target_selector: candidate_distillation
target_hint:
  - type: workflow
    value: "misa-runtime-memory-vaks-context-pack-bridge"
    status: conceptual
    anchor_version: candidate-workflow-only
  - type: source_card
    value: "raw/repos/2026-06-14-rohitg00-agentmemory-source.md"
    status: healthy
    anchor_version: "2026-06-14"
  - type: repo_snapshot
    value: "raw/repos/_snapshots/2026-06-14-rohitg00-agentmemory-f6f9e3c-source.zip"
    status: healthy
    anchor_version: "sha256:F894BF00ECE2ED84B476B436ED7FDEFDC54E064132E25F1A43630ED4DAE09055"
project_borrow_scope:
  - "Use agentmemory as a strong design reference for MISA runtime memory, not VAKS reviewed knowledge."
  - "Borrow Hermes/MCP/hook lifecycle ideas for a VAKS-owned read-only context-pack adapter."
  - "Borrow project/agent scoped recall and fail-closed isolation for MISA memory buckets."
  - "Borrow sourceObservationIds/verify-style runtime provenance for debugging memory origin."
  - "Borrow slots/retention only as activation/runtime salience, not truth confidence."
  - "Allow MISA writeback only as feedback_event, candidate_signal, or review_due through operation receipts."
project_non_borrow_scope:
  - "Do not let MISA directly write reviewed claims, patterns, decisions, reviewed relations, or action basis."
  - "Do not treat agentmemory confidence, strength, rank, graph score, lesson confidence, or retention score as VAKS evidence/truth."
  - "Do not export runtime memory into H:\\Obsidian\\资料库 as formal knowledge."
  - "Do not expose broad MCP save/delete/export tools to VAKS before permission tiers and validators exist."
  - "Do not copy `on_memory_write` mirroring into VAKS without quarantine and receipts."
project_reopen_trigger:
  - "User asks to design MISA using VAKS."
  - "A new MISA/Hermes runtime inspection window starts."
  - "VAKS context-pack adapter design begins."
  - "MISA feedback/candidate writeback needs a format or sandbox."
  - "Agent gateway permission model moves from planning to implementation."
confirmation_basis:
  - "User explicitly requested distillation and MISA usefulness judgment."
  - "Official repo, npm metadata, README, TypeScript source, Hermes integration, MCP tool registry, and security advisory drafts were inspected."
last_checked_at: "2026-06-14"
expires_at: null
borrow_value: strong_for_misa
borrow_order:
  - "P1: MISA runtime memory quarantine"
  - "P1: VAKS context-pack read-only adapter"
  - "P1: feedback/candidate/review_due writeback"
  - "P2: MCP/REST bridge and viewer/governance UX after safety gates"
avoid:
  - "No runtime memory as reviewed truth."
  - "No MISA direct reviewed write."
  - "No memory rank/confidence as evidence support."
  - "No formal Obsidian export."
  - "No broad MCP tools before permission gates."
tags:
  - project-lens
  - MISA
  - VAKS
  - agentmemory
  - hermes
  - runtime-memory
  - context-pack
  - candidate-only
legacy_overlay_compatibility: true
canonical_p0_included: false
canonical_current_lint_scope: false
legacy_storage: outputs/review/project_lens_overlays
truth_boundary: "project lens compatibility artifact only; not canonical reviewed knowledge; not action basis"
---

# Project Lens: agentmemory as MISA Runtime Memory / VAKS Bridge Reference

## Boundary

This is a project-scoped sidecar. It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide a future MISA/VAKS bridge sandbox, but it cannot act as reviewed knowledge or action basis.

## Project Borrow Scope

For MISA + VAKS, borrow agentmemory narrowly:

```text
Use it to help MISA remember operational context and fetch VAKS context.
Do not use it to decide or mutate VAKS truth.
```

Concrete borrow:

- Hermes provider lifecycle: `prefetch`, `sync_turn`, `on_session_end`, `on_pre_compress`, `system_prompt_block`.
- MCP/REST adapter split for agent-facing recall.
- Project/agent scope and fail-closed isolation.
- Runtime observation -> memory -> verify source observation trace.
- Slots for user preferences, tool rules, guidance, pending items.
- Retention/access as activation.
- Governance/delete/audit as minimum runtime-memory hygiene.

## Project Non-Borrow Scope

Do not borrow:

- agentmemory as VAKS reviewed truth.
- memory confidence/strength/rank as evidence.
- runtime lessons/reflections as reviewed claims.
- Obsidian export into formal reviewed vault.
- direct MISA writes into `wiki/claims`, `wiki/patterns`, `wiki/decisions`, or reviewed relations.
- `on_memory_write` mirroring as VAKS writeback.
- broad MCP write/delete/export before permission tiers.

## MISA/VAKS Bridge Shape

```text
MISA runtime
  -> records session observations and operational memory

VAKS Context Adapter
  -> reads source/candidate/reviewed context through context-pack rules
  -> labels authority bucket and warnings

MISA answer/action path
  -> uses VAKS action readiness when action-facing

MISA writeback
  -> feedback_event / candidate_signal / review_due only
  -> operation receipt required
  -> no truth mutation
```

## Minimal Pilot Gate

```yaml
pilot_scope: sandbox_only
inputs:
  - one MISA runtime task
  - one VAKS context-pack fixture
  - one user correction fixture
  - one candidate discovery fixture
commands_or_steps:
  - build MISA runtime memory bucket
  - fetch VAKS context pack read-only
  - generate runtime prompt context with authority labels
  - emit feedback_event from correction
  - emit candidate_signal from discovery
checks:
  - no reviewed VAKS mutation
  - no action basis from runtime memory
  - project/agent scope explicit
  - context pack ref present
  - operation receipt present for writeback
  - feedback creates review pressure only
pass_result:
  - candidate bridge contract
fail_result:
  - keep agentmemory as design-only reference
```

## Reopen Trigger

Reopen this overlay when:

```text
MISA/Hermes bridge design starts.
VAKS context pack adapter becomes implementation work.
MISA needs a memory quarantine spec.
Agent gateway permission tiers are implemented.
```

## Confirmation

```yaml
confirmation_basis:
  user_request: "蒸馏这个 到时候对misa使用我们的资料库有没有帮助"
  inspected_source:
    - raw/repos/2026-06-14-rohitg00-agentmemory-source.md
    - raw/repos/_snapshots/2026-06-14-rohitg00-agentmemory-f6f9e3c-source.zip
  conclusion: "strong MISA runtime memory and VAKS bridge reference, not VAKS authority layer"
last_checked_at: 2026-06-14
```
