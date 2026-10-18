---
type: project_overlay_note
status: active_sandbox_sample
project_id: MISA
created_at: 2026-06-06
truth_boundary: project overlay only; not truth; not ADR; not action basis
source_project_path: C:\Users\Administrator\Documents\New project\misa-cybernetic-evolution
tags:
  - project-overlay
  - project-misa
  - sandbox
---

# MISA Borrowing List

## Boundary

This file is a borrowing list for Misa. It points to reusable knowledge points
and says how Misa can look at them right now.

It does not change the reusable knowledge point.

## Entries

### retrieval-is-activation-not-truth

- kp_ref: outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
- stance: partial
- borrow_scope: Treat perception digest, vector ranker, and diagnostic output as hints only.
- non_borrow_scope: Do not let rank, queue order, digest text, or diagnostic color become control authority.
- target_hint:
  - scripts/lib/perception-sidecar.mjs::buildPerceptionDigest
  - scripts/lib/component-health.mjs::buildComponentHealthDiagnostics
  - README.md
- updated_at: 2026-06-06

### memory-granularity-and-quarantine

- kp_ref: outputs/review/candidate_pattern_bank/memory-granularity-and-quarantine.md
- stance: partial
- borrow_scope: Preserve the no-effect boundary for runtime memory, health output, and adapter output.
- non_borrow_scope: Do not let runtime-thread, health diagnostics, perception digest, or adapter output write durable memory directly.
- target_hint:
  - scripts/lib/runtime-thread.mjs::SAFETY
  - scripts/lib/component-health.mjs::SAFETY
  - test/v028-runtime-thread.test.mjs
- updated_at: 2026-06-06

### file-first-agent-workbench

- kp_ref: outputs/review/candidate_pattern_bank/file-first-agent-workbench.md
- stance: partial
- borrow_scope: Keep contracts, schemas, examples, tests, and handoff surfaces visible as files.
- non_borrow_scope: File visibility does not create permission to run or ship changes.
- target_hint:
  - ARCHITECTURE.md
  - docs/current/runtime-thread-v0.28.md
  - docs/current/component-health-diagnostics-v0.29.md
  - docs/templates/distillation
- updated_at: 2026-06-06

### graph-and-ontology-as-candidate-context

- kp_ref: outputs/review/candidate_pattern_bank/graph-and-ontology-as-candidate-context.md
- stance: avoid
- borrow_scope: Use graph or LangGraph only as carrier/context shape when deterministic control stays outside it.
- non_borrow_scope: Do not let graph nodes, route edges, or summaries own winner authority or route mutation.
- target_hint:
  - ARCHITECTURE.md
  - docs/current/control-boundaries.md
- updated_at: 2026-06-06

### visual-workbench-for-retrieval-diagnostics

- kp_ref: outputs/review/candidate_pattern_bank/visual-workbench-for-retrieval-diagnostics.md
- stance: partial
- borrow_scope: Use diagnostics to expose component health and tool-loop failure modes for human review.
- non_borrow_scope: Do not treat dashboards, health colors, or clean reports as readiness.
- target_hint:
  - scripts/lib/component-health.mjs::diagnosticCandidateForComponent
  - test/component-health.test.mjs
- updated_at: 2026-06-06

### skills-and-prompts-as-visible-files

- kp_ref: outputs/review/candidate_pattern_bank/skills-and-prompts-as-visible-files.md
- stance: watch
- borrow_scope: Watch prompt and skill surfaces as visible review material for a later Misa skill-control pass.
- non_borrow_scope: Do not allow prompt or template edits to publish skills, install skills, or mutate runtime authority.
- target_hint:
  - docs/current/skill-control-intake-template.md
  - prompts
- updated_at: 2026-06-06

### adaptive-retrieval-depth

- kp_ref: outputs/review/candidate_pattern_bank/adaptive-retrieval-depth.md
- stance: defer
- borrow_scope: Revisit only after local or shadow checks show repeated recall failure.
- non_borrow_scope: Do not add adaptive depth as a runtime controller or automatic route mutation path.
- target_hint:
  - package.json
  - scripts/lib/perception-sidecar.mjs::priorityFor
- updated_at: 2026-06-06

### search-to-analysis-before-answer

- kp_ref: outputs/review/candidate_pattern_bank/search-to-analysis-before-answer.md
- stance: partial
- borrow_scope: Use before answering whether a diagnostic or route change should affect Misa control behavior.
- non_borrow_scope: Do not make ordinary Misa status checks into heavy review packets.
- target_hint:
  - CONTROL_CONTRACT.md
  - docs/current/control-boundaries.md
  - scripts/lib/component-health.mjs::buildComponentHealthDiagnostics
- updated_at: 2026-06-06

