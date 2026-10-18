---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p0-01-retrieval-receipt-template-sandbox
status: draft_for_review
truth_boundary: source_map_only_not_evidence_support
---

# Source Map

This file records the local sources used to shape the sandbox contract. It is
not an evidence packet and does not promote any architecture change.

## Core Sources

| Source | Used For |
|---|---|
| `AGENTS.md` | Workspace write boundaries, sandbox-only rule, Chinese reporting default, no promotion/commit/sync without explicit approval. |
| `00_handoff/2026-06-08-answer-boundary-and-three-window-execution-handoff.md` | Current frozen-spine warnings, dirty tree caution, diagnostic-not-truth wording. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` | P0 order, P0-01 minimum retrieval receipt fields, forbidden authority shortcuts. |
| `SOURCE_INTAKE.md` | Bucketed retrieval policy, query-run trace shape, support boundary, enum-like fields, source annotation boundary. |
| `REFERENCE_REVIEW_PROTOCOL.md` | Independent anchor and self-support-loop warnings. |
| `DEV_CONTEXT.md` | Dev context as temporary working set, not reviewed knowledge. |
| `REVIEW_QUEUE.md` | Body-hash/review/promotion boundaries and evidence sufficiency not being automatic action readiness. |
| `FEEDBACK.md` | Feedback affects activation/usefulness/scope fit/review pressure, not truth confidence or verification status. |

## Similar Sandbox References

| Source | Borrowed Pattern | Boundary |
|---|---|---|
| `templates/query-run.md` | Existing query-run trace fields: authority buckets, selected items, support checks, warnings, gaps. | Query-run is not an independent receipt template; this slice does not edit it. |
| `templates/review-candidate.md` | Clear boundary prose: URL-only is provenance, source range is handle, support requires check. | Review candidate is not a retrieval receipt. |
| `outputs/review/source-intake-generic-readonly-loop-2026-06-14/README.md` | Supported/unsupported conclusion style and conservative package claims. | Prior package remains separate sandbox evidence. |
| `outputs/review/source-intake-runtime-readonly-loop-2026-06-13/README.md` | Runtime dry-run boundary wording and unsupported conclusions. | This slice does not claim runtime validation. |
| `outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/results/phase_b_skeleton_main_primary_retrieval_receipts.jsonl` | Prior receipt-like field idea: hashes, warning code, usage badge, retrieval policy. | Prior file is a pilot artifact, not the formal contract. |

## Local Facts Checked Before Writing

- `templates/retrieval-receipt.md` was not present in `templates/`.
- `tools/validate_retrieval_receipts.py` was not present in `tools/`.
- `outputs/review/vaks-implementation-sandbox/2026-06-15-p0-01-retrieval-receipt-template-sandbox/` was not present before this run.
- Current dirty tree was explicitly approved as pre-existing baseline by the user.

## Design Implication

The template must preserve this distinction:

```text
retrieval selection -> attention / trace / inspection candidate
evidence support -> independent anchor checked against a specific target
reviewer approval -> separate review process
action basis -> separate sufficiency and readiness gate
```
