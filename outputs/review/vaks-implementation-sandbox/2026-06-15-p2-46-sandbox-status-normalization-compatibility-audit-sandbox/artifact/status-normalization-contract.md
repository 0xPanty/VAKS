# Status Normalization Compatibility Contract

Slice: `2026-06-15-p2-46-sandbox-status-normalization-compatibility-audit-sandbox`

This contract normalizes legacy sandbox report statuses for display and handoff only.
It is not re-acceptance, release approval, promotion approval, mainline readiness,
formal vault approval, reviewed knowledge, evidence support, or action basis.

## Compatibility Rules

- Product Acceptance remains the decisive gate.
- Legacy `draft`, `pending`, `in_progress`, and missing planning/source-map statuses are nonblocking when gate booleans pass.
- `next-step` pending means stop before auto-advance; it does not mean Product Acceptance failed.
- Unknown raw statuses are blocking until a later sandbox maps or explains them.
- Old slices must not be edited just to make status strings prettier.
