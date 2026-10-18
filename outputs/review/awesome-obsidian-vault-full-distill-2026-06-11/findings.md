---
record_kind: findings
status: active
project_id: VAKS
created_at: 2026-06-11
truth_boundary: candidate_findings_not_reviewed_knowledge
action_basis_allowed: false
truth_mutation_allowed: false
---

# Findings: awesome-obsidian-vault Full Distillation

## Starting Context

Already written before this full pass:

- `raw/repos/2026-06-11-obsidian-pkm-vault-awesome-obsidian-vault-source.md`
- `outputs/review/2026-06-11-awesome-obsidian-vault-candidate-triage.md`
- `outputs/review/2026-06-11-awesome-obsidian-vault-p1-batch-scout.md`

Initial strict exact-source skip:

- `kepano/kepano-obsidian`
- `obsidian-tasks-group/obsidian-tasks`

Initial P1 scout correction:

- `nikitavoloboev/knowledge` current GitHub repo no longer looks like the listed
  knowledge vault; treat as source-freshness warning unless a fresh vault source
  is found.

## Working Rule

Every entry gets one of:

- `skip_existing`
- `distilled_p1`
- `distilled_p2`
- `distilled_p3_cold`
- `downgraded_stale_or_no_vaks_fit`

No entry is promoted to reviewed knowledge.

## Batch Metadata Result

- total entries: 48
- exact local processed/skipped: 2
- not exact-processed before this batch: 46
- generated metadata files:
  - `batch-source-ledger.json`
  - `batch-source-ledger.csv`

Exact skips:

- `kepano/kepano-obsidian`
- `obsidian-tasks-group/obsidian-tasks`

Current high-value batch shape:

- P1: agent-boundary, skill registry, workbench, source catalog.
- P2: publishing, templates, docs-as-vault, directory/link health.
- P3: domain content, curriculum, static/personal sites, cold source-shape references.

## Per-Source Distillation Result

- awesome-list entries checked: 48
- exact local skips: 2
- individual source cards written: 46
- individual candidate distillations written: 46
- per-source index: `per-source-index.md`
- skip ledger: `skip-ledger.md`

The per-source files use VAKS-specific labels: `borrow_value`, `borrow_order`,
`fit_layer`, `avoid`, `routing_hint`, and `dev_context_hint`. These labels are
routing/activation hints only; they do not create reviewed knowledge, truth
confidence, reviewed relations, adoption decisions, or action basis.
