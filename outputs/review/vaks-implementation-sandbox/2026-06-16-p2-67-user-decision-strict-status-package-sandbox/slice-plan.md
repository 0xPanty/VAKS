---
slice_id: 2026-06-16-p2-67-user-decision-strict-status-package-sandbox
status: planned
---

# Slice Plan

## Slice

`2026-06-16-p2-67-user-decision-strict-status-package-sandbox`

## Why This Slice

p2-66 chose the safe route: package p2-65's strict status helper only in a new sandbox path. This slice creates that reusable sandbox package without modifying old slices, shared helpers, tools, or mainline.

## Scope

Write only inside:

```text
outputs/review/vaks-implementation-sandbox/2026-06-16-p2-67-user-decision-strict-status-package-sandbox/
```

Read-only source slice:

```text
outputs/review/vaks-implementation-sandbox/2026-06-16-p2-66-user-decision-chain-hardening-readiness-sandbox/
```

## Do Not Touch

- `SCHEMA.md`
- `ARCHITECTURE_PRINCIPLES.md`
- `FUSION_ARCHITECTURE_V0_2_DRAFT.md`
- `README.md`
- `wiki/claims/`
- `wiki/patterns/`
- `wiki/decisions/`
- `templates/`
- `tools/`
- Obsidian vault
- old sandbox slices, except read-only inspection

## Deliverables

- sandbox-local strict status package module
- package builder and verifier
- JSON contract
- JSON, Markdown, and HTML package manifest
- positive fixtures
- failure cases
- verification report
- Reviewer report
- Boundary Auditor report
- GPT-5.5 extra-high Product Acceptance report
- next-step recommendation

## Acceptance Criteria

- Package exposes `parse_strict_frontmatter_status` and `status_matches`.
- Package rejects missing/duplicate/empty frontmatter status.
- Package ignores body `status:` lines and body pass-token mentions.
- Package manifest verifies p2-66 source closeout status.
- Fixtures and failure cases cover the public package API.
- Reviewer, Boundary Auditor, and Product Acceptance pass.
- Final gate passes.

## Stop Conditions

- Any required write would leave this slice path.
- Any task requires dependency install, commit, push, sync, hook, service, background automation, MCP write tool, old-slice rewrite, shared helper edit, tools edit, or mainline edit.
- Any output claims sandbox package success as reviewed knowledge, evidence support, action basis, mainline readiness, promotion readiness, Obsidian sync, user approval, or execution authority.
- Product Acceptance returns `BLOCKED_NEEDS_USER`.
