---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p0-02-operation-receipt-template-sandbox
status: draft
truth_boundary: source_map_for_sandbox_only
---

# Source Map

## Source Files Read

| Source | Used For | Boundary |
|---|---|---|
| `AGENTS.md` | Workspace router, protected paths, VAKS boundaries. | Local operating rule, not a new artifact source. |
| `00_handoff/2026-06-08-answer-boundary-and-three-window-execution-handoff.md` | Current recovery posture: dirty tree, frozen spine, diagnostics not truth. | Handoff state only; current worktree remains authoritative. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 596-619 | Operation receipt purpose and acceptance: actor, tier, mode, intent, basis, paths, approval, rollback, result. | Plan input, not implemented in mainline. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 2145-2178 | Minimum P0-02 frontmatter fields. | Sandbox template target only. |
| `REVIEW_QUEUE.md` lines 331-388 | Approval integrity and fixed body hash rules. | Review queue rule source; this slice does not validate hashes. |
| `SOURCE_INTAKE.md` lines 1440-1452 | Retrieval rank not trust; intent confirmation only for significant action; candidate cannot be action basis. | Boundary source for non-claims and failure cases. |
| `outputs/review/vaks-implementation-sandbox/2026-06-15-p0-01-retrieval-receipt-template-sandbox/product-acceptance-report.md` | Confirms P0-01 `PASS_PRODUCT_GRADE`. | Prior slice state only. |
| `outputs/review/vaks-implementation-sandbox/2026-06-15-p0-01-retrieval-receipt-template-sandbox/artifact/retrieval-receipt-template.md` | Style and boundary pattern reused for P0-02. | Reuse pattern only, not a mainline dependency. |

## Requirement Mapping

| Requirement | Implemented In |
|---|---|
| `record_kind: operation_receipt` | `artifact/operation-receipt-template.md`, all fixtures and failure cases |
| `actor`, `actor_tier`, `operation_mode` | Template frontmatter and permission matrix |
| `intent_confirmation` | Template frontmatter, fixtures, missing-intent failure |
| `basis` with context pack, reviewed support, candidates | Template basis rules, candidate-as-basis failure |
| `target_paths`, `proposed_changes` | Template and fixtures |
| `approval.checked_body_hash` | Template, reviewed-write failure cases |
| `rollback` | Template, destructive-delete failure |
| `result` | Template and fixtures |
| Non-authority boundary | Template non-claims, contract notes, boundary audit |
| Future validator fixture oracle | `artifact/failure-case-oracle.md`, `expected_failure_reason` in all failure cases |

## Out Of Scope

- No `templates/operation-receipt.md` mainline file is created.
- No `tools/validate_operation_receipts.py` validator is created.
- No reviewed write, promotion, schema change, commit, push, or Obsidian sync is
  performed.
