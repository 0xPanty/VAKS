---
type: sandbox_task_plan
status: in_progress
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: seven-project-sidecar-candidates-full-pressure-test
truth_boundary: planning file only; not reviewed knowledge; not action basis; not mainline architecture
---

# Seven Candidate Sidecar Pressure Test Plan

## Goal

在 `outputs/review` 沙盒里，把七个 Project Lens / project-scoped sidecar 候选当作“如果并入主架构会怎样”的全量测试对象，做多维度高压测试、量化对比、Obsidian 沙盒同步和保留/降级建议。

## Non-Negotiable Boundaries

- Do not edit `SCHEMA.md`, `REVIEW_QUEUE.md`, `templates/`, `ARCHITECTURE_PRINCIPLES.md`, or `FUSION_ARCHITECTURE_V0_2_DRAFT.md` in place.
- Do not stage, commit, push, clean, reset, or delete existing dirty/untracked work.
- Only write under `outputs/review/project-sidecar-seven-candidate-pressure-test-2026-06-05/` and the matching Obsidian sandbox path.
- Treat mainline insertion as sandbox copy insertion only.

## Seven Candidates Under Test

1. Project Lens concept / naming.
2. Field design.
3. `stance` state design.
4. Snapshot mechanism.
5. Project closeout drain protocol.
6. Archive / delete+tombstone / carry-forward / supersede lifecycle actions.
7. Retrieval precedence / manifest operating checklist.

## Phases

| Phase | Status | Evidence |
|---|---|---|
| Confirm repo and sandbox boundary | complete | git status/log checked; sandbox directory created |
| Verify second-project sample anchors | complete | Misa docs/scripts/tests inspected; concrete anchors confirmed |
| Build sandbox mainline copy with seven candidates inserted | complete | `mainline_with_seven_candidates/` diff |
| Build Misa second-project overlay sample | complete | `misa_overlay/MISA.md` |
| Exercise lifecycle outcomes | complete | landed, boundary, archive, tombstone, carry-forward/supersede files |
| Run quant matrix and authority leakage checks | complete | `checks/*.md` and score table |
| Sync to Obsidian sandbox and verify hashes | complete | `checks/obsidian-sync.md` |
| Produce final report and Pro package | complete | report, manifest, upload prompt, zip |

## Metrics

Use 0-3 scores unless otherwise stated.

- Boundary clarity: does it avoid truth/ADR/action-basis leakage?
- Maintenance usefulness: does it make agent/Codex work faster or clearer?
- Anchor concreteness: does it point to real files/modules/symbols?
- Lifecycle hygiene: does it drain rather than create zombie overlays?
- Retrieval hygiene: does it avoid authority/confidence ordering?
- Mainline pollution risk: does sandbox insertion bloat or confuse the architecture?
- Obsidian usability: can a reviewer navigate without confusion?

## Current Assumption

Misa appears suitable as phase-2 sample because it has concrete files, schemas, scripts, tests, and strong safety boundaries. This remains under verification until the overlay and checks are complete.
