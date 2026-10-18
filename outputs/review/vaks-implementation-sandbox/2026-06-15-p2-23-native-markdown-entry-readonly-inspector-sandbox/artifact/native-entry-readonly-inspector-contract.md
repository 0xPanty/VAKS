# Native Entry + Readonly Inspector Contract

## Input Contract

- P2-22 sandbox reports and pilot home.
- No formal vault content as a writable input.
- No runtime, sync, dependency install, commit, push, or promotion.

## Output Contract

- Sandbox-only Obsidian-style Markdown entry pages.
- Static read-only inspector HTML.
- Build receipt with source hashes and forbidden-operation flags.
- Validator and failure oracle.

## Native Markdown Pages

- `native_home` / `00 Native Home.md`: entry
- `inbox` / `01 Inbox.md`: capture_triage
- `status_board` / `02 Status Board.md`: status_surface
- `receipt_index` / `03 Receipt Index.md`: receipt_surface
- `boundary_stop` / `04 Boundary Stop.md`: stop_surface
- `readonly_inspector_guide` / `05 Readonly Inspector Guide.md`: inspection_surface
- `next_safe_step` / `06 Next Safe Step.md`: handoff_surface
- `dry_run_results` / `07 Dry Run Results.md`: verification_surface

## Inspector Views

- `entry_map`: shows Native Markdown pages and their next links.; does not show reviewed knowledge or approval
- `status_lanes`: shows blocked, dirty, stale, missing-anchor, review_due, action-risk; does not show truth confidence
- `receipt_lanes`: shows source reports, validator output, hash receipt, Product Acceptance; does not show evidence support
- `boundary_lanes`: shows stop conditions and forbidden operations; does not show permission to execute

## Product Promise

The operator can start from a Markdown note, follow wikilinks, inspect status and
receipts, and hit an explicit boundary stop without leaving the sandbox.

## Boundary Promise

Native Markdown is navigation, not authority. The inspector is read-only, not a
write tool. Receipts are process trail, not evidence support. Status grouping is
not approval. This slice is sandbox only, not action basis.
