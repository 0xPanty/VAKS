---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: heavy
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
title: obsidian-mind agent workbench overlay for VAKS
target_ref: outputs/review/2026-06-12-breferrari-obsidian-mind-candidate-distillation.md
review_ref: wiki/summaries/2026-06-12-breferrari-obsidian-mind-architecture-review.md
source_ref: raw/repos/2026-06-12-breferrari-obsidian-mind-source.md
target_selector: 'candidate source: breferrari/obsidian-mind'
target_hint:
- type: workflow
  value: agent-access
  status: conceptual
  anchor_version: 2026-06-12-source-review
- type: workflow
  value: obsidian-use-surface
  status: conceptual
  anchor_version: 2026-06-12-source-review
- type: workflow
  value: retrieval-cache
  status: conceptual
  anchor_version: 2026-06-12-source-review
- type: doc
  value: ARCHITECTURE_PRINCIPLES.md
  status: healthy
  anchor_version: 2026-06-12-file-checked
- type: doc
  value: SOURCE_INTAKE.md
  status: healthy
  anchor_version: 2026-06-12-file-checked
project_borrow_scope: Use obsidian-mind as a strong design-only reference for thin
  lifecycle hooks, manifest-scoped derived retrieval, Obsidian Bases workbench views,
  and visible vault-first agent memory with VAKS quarantine.
project_non_borrow_scope: Do not borrow obsidian-mind as VAKS truth architecture,
  reviewed knowledge layer, action-basis engine, autonomous writeback policy, or direct
  mainline dependency.
project_reopen_trigger: Reopen when VAKS explicitly starts agent-access hooks, Obsidian
  Bases dashboards, QMD/MCP retrieval cache, or template packaging work in a sandbox.
confirmation_basis: Repository snapshot at commit 9ae6860d01c4bb563dfe972dae89515866f4fbff
  captured 2026-06-12; local hook tests passed 527/527; no VAKS runtime integration
  performed.
last_checked_at: 2026-06-12
expires_at: 2026-08-12
borrow_value: strong
tags:
- project-overlay
- candidate
- vaks/agent-access
- vaks/obsidian-workbench
- vaks/retrieval-cache
- vaks/agent-memory-quarantine
- risk/authority-pollution
review_pressure: none
legacy_overlay_compatibility: true
canonical_p0_included: false
canonical_current_lint_scope: false
legacy_storage: outputs/review/_legacy_project_lens
truth_boundary: legacy project lens compatibility artifact only; not canonical overlay;
  not reviewed knowledge; not action basis
---

# Project Overlay: obsidian-mind Agent Workbench

## Boundary

This is a VAKS project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-12-breferrari-obsidian-mind-candidate-distillation.md
review_ref: wiki/summaries/2026-06-12-breferrari-obsidian-mind-architecture-review.md
source_ref: raw/repos/2026-06-12-breferrari-obsidian-mind-source.md
target_selector: "candidate source: breferrari/obsidian-mind"
```

## Project Borrow Scope

For VAKS, borrow `obsidian-mind` as a design-only reference for:

```text
thin lifecycle hooks
manifest-scoped derived runtime contracts
QMD/MCP typed retrieval surface
Obsidian Bases as review/workbench dashboards
vault-first visible agent memory
multi-agent operating manuals/config adapters
session context injection without full-vault loading
write-time lint warnings
detached/debounced derived-index refresh
```

The best VAKS-shaped borrowing is:

```text
formal Markdown source of truth
-> read-only / candidate-only hook receipts
-> authority-bucketed derived retrieval
-> Obsidian Bases workbench
-> human/Codex review gate
```

## Project Non-Borrow Scope

Do not borrow it for:

```text
truth storage
reviewed relation creation
truth confidence
claim/pattern/decision promotion
action basis
agent autonomous formal writeback
automatic evidence support
private Slack/people scanning by default
direct ShardMind/QMD/hook install into VAKS main vault
```

For VAKS, `agent memory` can only become:

```text
candidate material
feedback event
routing hint
project overlay suggestion
source card
```

It cannot become:

```text
reviewed truth
reviewed relation
confidence change
promotion
action basis
```

## VAKS Implementation Hint

If VAKS later prototypes an agent workbench, start with this order:

```text
read-only Bases dashboards over existing files
-> candidate-only hook receipts in sandbox
-> write lint / source-anchor health checks
-> authority-bucketed QMD/MCP retrieval adapter
-> context-pack candidate envelope
-> evidence-aware review gate before action basis
```

The important rule:

```text
bucket and boundary before convenience
```

## Suggested Tags For Future Retrieval

Primary:

- `agent-access`
- `agent-memory-quarantine`
- `obsidian-use-surface`
- `review-queue-workbench`
- `derived-retrieval`
- `qmd-mcp`
- `lifecycle-hooks`

Risk tags:

- `authority-pollution`
- `retrieval-not-support`
- `dashboard-not-truth`
- `hook-not-intent`
- `candidate-not-action-basis`

## Reopen Triggers

Reopen this overlay when:

- VAKS starts a sandbox for agent lifecycle hooks.
- VAKS creates real Obsidian Bases dashboards.
- VAKS evaluates QMD/MCP as a retrieval adapter.
- VAKS designs an agent memory write quarantine.
- VAKS explores installable/distributable vault templates.

## Confirmation

```yaml
confirmation_basis:
  repository_head: 9ae6860d01c4bb563dfe972dae89515866f4fbff
  source_snapshot: raw/repos/_snapshots/2026-06-12-breferrari-obsidian-mind-9ae6860d01c4-source.zip
  snapshot_sha256: 84797493e33e30550ba053d069c42543f7945fd7d4e202cfecb46a9c4bfedd82
  local_test_command: "npm test in .claude/scripts"
  local_test_result: "527 passed, 0 failed"
  local_vaks_integration: not_run
last_checked_at: 2026-06-12
expires_at: 2026-08-12
```

## One Sentence For Future Context Packs

`obsidian-mind` is a strong candidate reference for VAKS's future agent workbench and derived retrieval surfaces, but every useful part must stay behind candidate/review/authority-bucket boundaries and cannot become reviewed truth or action basis by convenience.

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
```
