---
record_kind: task_plan
status: active
project_id: VAKS
created_at: 2026-06-11
truth_boundary: planning_state_not_reviewed_knowledge
action_basis_allowed: false
truth_mutation_allowed: false
---

# Task Plan: awesome-obsidian-vault Full Distillation

## Goal

Distill every relevant entry from `obsidian-pkm-vault/awesome-obsidian-vault`.
Skip entries already distilled. Keep all outputs candidate-only, targeted to VAKS
architecture layers, then sync to `H:\Obsidian\资料库` with hash verification.
After completion, shut down the computer as requested.

## Correction After User Clarification

The first pass produced batch-level routing. The user clarified that they want
each original linked repo/source distilled one by one. Reopen the plan:

```text
awesome list entry
-> original linked repo/source
-> per-entry source card
-> per-entry candidate distillation
-> skip only if exact local distillation already exists
```

## Boundaries

- Candidate-only artifacts.
- No reviewed knowledge promotion.
- No mainline architecture edits unless explicitly approved.
- No commit or push.
- Do not treat stars, list inclusion, install counts, dashboards, or websites as
  evidence support.
- Use VAKS layers for every borrow label: source-ingest, candidate-review,
  activation, dev-context, context-pack, workbench, publishing, agent-boundary,
  retrieval-cache, source-hygiene, risk.

## Phases

| Phase | Status | Output |
|---|---|---|
| 1. Recover rules and initialize workspace | complete | task_plan/findings/progress |
| 2. Build exact list and processed/skip ledger | complete | `batch-source-ledger.json/csv` |
| 3. Distill P1/P2 entries with VAKS layer tags | complete | `full-batch-candidate-distillation.md` |
| 4. Distill P3/cold entries by group | complete | `full-batch-candidate-distillation.md` |
| 5. Sync and hash-verify all new/updated files | complete | `sync-report.json`, `sync-report.md` |
| 6. Final status and shutdown | reopened | shutdown canceled or absent; continue work |
| 7. Per-original-source distillation | complete | 46 source cards + 46 candidate distillations; 2 exact skips |
| 8. Sync per-source outputs and hash-verify | complete | `final-sync-report.json`, `final-sync-report.md` |
| 9. Shutdown after individual distillation completes | complete | Windows shutdown scheduled with 120-second delay |

## Errors

| Time | Error | Resolution |
|---|---|---|
| 2026-06-11 | PowerShell `$host` is read-only when building batch metadata | Rename script variable to `$sourceHost` and rerun |
| 2026-06-11 | PowerShell `-replace` inside array literal parsed too many arguments | Remove unnecessary inline replace and rerun generator |
| 2026-06-11 | First per-source output had Markdown fence/property interpolation defects | Rewrote 46 source cards and 46 distillations, normalized code fences, then rechecked samples |
