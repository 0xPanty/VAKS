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
project_id: VAKS
target_ref: outputs/review/2026-06-07-bilibili-obsidian-claude-code-three-layer-memory-candidate-distillation.md
target_selector: "ref/three-layer-memory-router"
target_hint: "MEMORY_TIER / DEV_CONTEXT / AGENTS.md / handoff / session scratch / closeout"
project_borrow_scope:
  - "Borrow root-router UX: one file or entrypoint tells the agent who the user/project is, where data lives, what rules apply, and what to read first."
  - "Borrow session-memory quarantine: current conversation outputs first land in a scratch/workbench area before long-term storage."
  - "Borrow closeout ritual: end each meaningful session with summarize -> route -> archive/promote/discard."
  - "Borrow five workflow smoke tests: read, analyze, write, connect, archive."
  - "Borrow separation between general agent behavior rules and project/vault-specific routing rules."
project_non_borrow_scope:
  - "For VAKS, do not borrow MEMORY.md or session memory as truth, reviewed evidence, or action basis."
  - "For VAKS, do not let agent-written session notes directly mutate reviewed knowledge, source reliability, or reviewed relations."
  - "For VAKS, do not copy creator-oriented folder taxonomy as schema."
  - "For VAKS, do not make whole-vault scanning the default for ordinary queries."
  - "For VAKS, do not bypass source-card, candidate, review queue, or evidence-aware review gates."
project_reopen_trigger:
  - "Reopen when VAKS designs agent/session writeback permissions."
  - "Reopen when VAKS creates a formal session scratch or closeout workflow."
  - "Reopen when VAKS publishes user-facing AGENTS.md / MEMORY.md templates."
  - "Reopen when VAKS designs non-developer onboarding for memory tiers and dev context."
confirmation_basis: "User explicitly requested this Bilibili video be distilled as the final source in the VAKS intake lane."
last_checked_at: 2026-06-07
expires_at:
reference_layer_tag: ref/three-layer-memory-router
borrow_value: strong
borrow_order:
  - "P1: root router file as activation gateway"
  - "P1: session scratch quarantine"
  - "P1: end-session closeout/promotion ritual"
  - "P1: read/analyze/write/connect/archive smoke tests"
  - "P2: split general behavior rules from vault route/index"
  - "P2: creator-friendly folder/prompt onboarding"
  - "P3: semantic connection plugins as activation aids"
avoid:
  - "MEMORY.md as truth"
  - "session scratch as reviewed knowledge"
  - "automatic long-term promotion"
  - "creator folders as VAKS schema"
  - "whole-vault scan by default"
  - "agent writeback without review gates"
---

# Project Overlay: VAKS -> Obsidian + Claude Code Three-Layer Memory

## Boundary

This is a VAKS-scoped borrowing sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern. It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-07-bilibili-obsidian-claude-code-three-layer-memory-candidate-distillation.md
source_ref: raw/videos/2026-06-07-bilibili-obsidian-claude-code-three-layer-memory-source.md
source_transcript_ref: raw/videos/2026-06-07-bilibili-obsidian-claude-code-three-layer-memory-source/segments.md
target_hint: MEMORY_TIER / DEV_CONTEXT / AGENTS.md / handoff / session scratch / closeout
reference_layer_tag: ref/three-layer-memory-router
```

## Project Borrow Scope

For VAKS, borrow this video as a user-facing agent-memory scaffold:

1. `root_router_file`: an entrypoint tells the agent who/what/where/how/what-first.
2. `session_memory_quarantine`: conversation outputs stay in a scratch layer first.
3. `closeout_promotion_ritual`: session end decides what to archive, route, promote, or discard.
4. `workflow_smoke_tests`: read, analyze, write, connect, archive test whether the memory scaffold works.
5. `behavior_vs_route_split`: global behavior/style rules should be separate from project/vault routing rules.

Best one-line borrowing:

```text
把 VAKS 复杂边界包装成一个朴素仪式：启动先读地图，工作先写草稿，收尾再决定进不进长期知识。
```

## Project Non-Borrow Scope

For VAKS, do not currently borrow:

- `MEMORY.md` as truth authority.
- session memory as reviewed knowledge.
- AI session summaries as source evidence.
- automatic promotion from scratch to durable knowledge.
- creator workflow folders as VAKS schema.
- whole-vault scanning for every ordinary question.
- agent writeback without path, layer, and review gates.

Plain-language warning:

```text
这个视频能教我们怎么让 agent 不失忆。
它不能替我们判断哪些记忆是真的、该不该进真理层。
```

## Reopen Trigger

Reopen this overlay when VAKS is working on:

- agent writeback permissions.
- session scratch / session ledger.
- closeout and recovery handoff UX.
- user-facing `AGENTS.md` / `MEMORY.md` templates.
- non-developer onboarding for activation tiers.
- ordinary workflow smoke tests.

## Confirmation

```yaml
confirmation_basis: "User explicitly requested this Bilibili video be distilled as the final source in the VAKS intake lane."
last_checked_at: 2026-06-07
expires_at:
```

## Borrow Gradient

```yaml
borrow_value: strong
P1:
  - root router file as activation gateway
  - session scratch quarantine
  - closeout/promotion ritual
  - read/analyze/write/connect/archive smoke tests
P2:
  - split behavior file from route/index file
  - creator-friendly folders and prompt examples
  - simple onboarding language
P3:
  - semantic connection plugin as activation enhancement
avoid:
  - MEMORY.md as truth
  - session scratch as reviewed knowledge
  - automatic long-term promotion
  - creator folders as schema
  - default whole-vault scan
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
```
