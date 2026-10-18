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
target_ref: outputs/review/2026-06-07-donghuixin-ai-vibe-writing-skills-candidate-distillation.md
target_selector: "AI Vibe Writing Skills as spec-driven review loop"
target_hint: "source-intake / review-queue / dev-context / operator-workflow"
project_borrow_scope:
  - "Borrow spec/task-contract as a readable operator surface for significant VAKS work."
  - "Borrow DoD and failed_specs as review package mechanics for important candidate/action-facing outputs."
  - "Borrow defensive red-team framing as an optional candidate pressure-test aid."
  - "Borrow hard/soft/reference/error separation only as activation and feedback boundary, not truth."
project_non_borrow_scope:
  - "For VAKS, do not borrow AI detector/PPL scores as evidence, truth confidence, reviewer status, or action readiness."
  - "For VAKS, do not let hard_memory/reference_library style stores directly mutate reviewed knowledge."
  - "For VAKS, do not copy self-healing script execution without explicit tool-safety and user authorization."
project_reopen_trigger:
  - "Reopen if VAKS is designing a real review package UI/operator checklist."
  - "Reopen if Evidence Packet needs a human-readable attack-surface table."
  - "Reopen if agent writeback or tool-loop automation becomes an active implementation task."
confirmation_basis: "User explicitly requested strong distillation for VAKS and said the repository logic seems close to VAKS."
last_checked_at: 2026-06-07
expires_at:
borrow_value: strong
borrow_order:
  - "P1: task contract + DoD + defensive red-team + failed review backflow"
  - "P2: hard/soft/reference/error memory separation and context router/compactor"
  - "P3: PDF/MinerU/AI-style/LaTeX tooling as peripheral diagnostics or future tooling references"
avoid:
  - "AI detector as authority"
  - "hard memory as truth"
  - "workflow pass as evidence support"
  - "self-healing scripts without safety gate"
---

# Project Overlay: VAKS -> AI Vibe Writing Skills

## Boundary

This is a VAKS-scoped borrowing sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern. It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-07-donghuixin-ai-vibe-writing-skills-candidate-distillation.md
source_ref: raw/repos/2026-06-07-donghuixin-ai-vibe-writing-skills-source.md
snapshot_ref: raw/repos/_snapshots/donghuixin-AI-Vibe-Writing-Skills-dbfee78dac29c0c347354ffe696cf124b80c1817.zip
target_hint: source-intake / review-queue / dev-context / operator-workflow
```

## Project Borrow Scope

For VAKS, borrow the repository as a practical operator-surface reference:

1. `task_contract` before significant generation/action/review work.
2. `DoD` as a small, checkable output contract.
3. `failed_specs` as review failure state, not soft advice.
4. `defensive red-team` as optional candidate pressure test.
5. `router / compactor` as dev-context loading discipline.
6. `hard / soft / reference / error` separation as memory quarantine intuition.

Best one-line borrowing:

```text
把严格性做成可读工作流，而不是藏成抽象原则。
```

## Project Non-Borrow Scope

For VAKS, do not currently borrow:

- AI detector / PPL / GPTZero score as evidence support, truth confidence, reviewer status, or action readiness.
- direct hard_memory writeback as reviewed fact mutation.
- reference_library as evidence support without raw source anchors.
- self-healing script execution without explicit safety gate.
- full prompt-agent stack as a new VAKS architecture lane.
- defensive reframing as rhetorical excuse for weak evidence.

Plain-language warning:

```text
这个库可以教我们怎么把流程做顺。
它不能替我们判断什么是真的。
```

## Reopen Trigger

Reopen this overlay when VAKS is working on:

- review package ergonomics,
- action-facing answer workflow,
- Evidence Packet human-readable challenge table,
- dev-context router / context pack compaction,
- agent writeback boundaries,
- tool self-healing safety policy.

## Confirmation

```yaml
confirmation_basis: "User explicitly requested strong distillation for VAKS and asked to put the video/repo logic into one knowledge point; later user narrowed scope to repository only because video audio was unclear."
last_checked_at: 2026-06-07
expires_at:
```

## Borrow Gradient

```yaml
borrow_value: strong
borrow_order:
  P1:
    - task contract
    - DoD
    - defensive red-team
    - failed review backflow
  P2:
    - memory separation
    - reference ingestion target list
    - router / compactor
  P3:
    - local AI-style lint
    - MinerU/PDF helper scripts
    - LaTeX self-healing loop
avoid:
  - detector as authority
  - hard memory as truth
  - workflow pass as evidence support
  - unsafe self-healing script automation
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
```
