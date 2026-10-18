---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
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
project_id: verified-action-knowledge-system
target_ref: outputs/review/2026-06-23-AI-Builder-Club-loop-engineer-template-candidate-distillation.md
target_selector: "VAKS/MISA loop-engineer substrate and codebase-harness sidecar"
target_hint: "loop workspace substrate / operator memory / repo harness / verify-before-PR"
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-loop-shared-memory-substrate.md
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-artifact-kind-domain-field.md
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-timeline-log-operational-memory.md
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-codebase-harness-legible-executable-verifiable.md
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-verify-before-pr-fresh-verifier.md
project_borrow_scope: "For VAKS, borrow loop-engineer-template as an operational substrate and engineering-harness reference: artifact-kind/domain-field split, domain README as loop live state, append-only Timeline plus global LOG, deterministic metrics collectors, earned artifact kinds, map-not-manual docs, custom lints with remediation, dev-local launcher, e2e gate, independent verifier before PR, and worktree containment."
project_non_borrow_scope: "For project VAKS, do not borrow loop-engineer-template as a truth layer, reviewed knowledge model, evidence support mechanism, action-basis validator, or Codex runtime default. Do not collapse VAKS raw/candidate/reviewed/action-basis boundaries into the repo's simplified signal/doc substrate. Timelines, logs, e2e proofs, and PR videos are operational traces unless later routed through VAKS evidence-aware review."
project_reopen_trigger: "Reopen when VAKS designs a real loop_run schema, source-intake loop, operator cockpit memory surface, or MISA repo-harnessing workflow; require a bounded sandbox pilot, host-runtime compatibility check, and explicit authority-boundary audit before any mainline adoption."
confirmation_basis: "User explicitly requested distillation of this repo after Agent-Loop-Skills; overlay is limited to project borrow/non-borrow boundaries and does not imply adoption."
last_checked_at: 2026-06-23
expires_at:
tags:
  - loop-engineer
  - agentic-loops
  - operator-loop
  - codebase-harness
---

# Project Overlay: loop-engineer-template for VAKS Loop Engineering

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide future VAKS/MISA loop design and repo harness work, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-23-AI-Builder-Club-loop-engineer-template-candidate-distillation.md
target_selector: VAKS/MISA loop-engineer substrate and codebase-harness sidecar
target_hint: loop workspace substrate / operator memory / repo harness / verify-before-PR
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-loop-shared-memory-substrate.md
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-artifact-kind-domain-field.md
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-timeline-log-operational-memory.md
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-codebase-harness-legible-executable-verifiable.md
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-verify-before-pr-fresh-verifier.md
```

## Project Borrow Scope

For VAKS, borrow this source as an optional operational sidecar for:

```text
loop_run workspace design
operator cockpit memory surfaces
source-intake loop status
MISA repo harnessing
agent worktree containment
verify-before-ship workflows
```

Borrow the substrate shape:

```text
artifact home by kind
domain as loop-state field / sidecar
Timeline for per-artifact history
LOG for short global feed
metrics written by deterministic collectors
new kinds earned by status machine + fields + body shape
```

Borrow the engineering harness shape:

```text
legible:
  root context as map
  docs as system of record
  hard rules encoded as lints

executable:
  one-command local stack
  reachable logs
  app drivable

verifiable:
  real e2e gate
  independent verifier before PR
  objective regression sweep
  proof linked in PR
```

## Project Non-Borrow Scope

For project VAKS, do not currently borrow this source as:

```text
truth layer
review engine
evidence support mechanism
action-basis validator
Claude runtime default
replacement for raw/candidate/reviewed/action-basis layers
```

Reason:

```text
signals are source observations
docs are durable notes
domain README is loop state
Timeline is history
LOG is work feed
e2e proof is operational evidence
none of these are VAKS reviewed knowledge by default
```

## Recommended Use Shape

```yaml
loop_workspace_sidecar:
  record_kind: loop_workspace_sidecar
  knowledge_status: candidate
  source_ref: raw/repos/2026-06-23-AI-Builder-Club-loop-engineer-template-source.md
  loop_id:
  owner_project:
  charter_ref:
  current_focus:
  backlog_ref:
  timeline_ref:
  log_ref:
  metrics_collector_ref:
  harness_state:
    legible: unknown
    executable: unknown
    verifiable: unknown
  result_status: diagnostic_only
  retrieval_policy:
    policy_kind: project_context_only
    pack_allowed: activation_only
    action_basis_allowed: false
    warning_code: overlay_not_authority
  truth_mutation_allowed: false
  action_basis_allowed: false
```

## Confirmation

```yaml
confirmation_basis: user requested distillation of this repo after Agent-Loop-Skills
last_checked_at: 2026-06-23
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
loop-output-as-evidence
timeline-as-truth
pr-proof-as-policy-correctness
signal-doc-collapse
```

