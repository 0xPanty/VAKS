---
slice_id: 2026-06-16-p2-65-user-decision-frontmatter-status-hardening-sandbox
status: planned
---

# Slice Plan

## Slice

`2026-06-16-p2-65-user-decision-frontmatter-status-hardening-sandbox`

## Why This Slice

p2-64 reached Product Acceptance, but Reviewer and Product Acceptance both noted that its status helper scans the first `status:` line instead of strictly parsing YAML frontmatter. This slice hardens that seam in sandbox without modifying older slices.

## Scope

Write only inside:

```text
outputs/review/vaks-implementation-sandbox/2026-06-16-p2-65-user-decision-frontmatter-status-hardening-sandbox/
```

Read-only source slice:

```text
outputs/review/vaks-implementation-sandbox/2026-06-16-p2-64-user-decision-replay-portability-audit-sandbox/
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

- strict frontmatter status parser prototype
- builder and verifier
- JSON contract
- JSON, Markdown, and HTML hardening outputs
- positive fixtures
- failure cases
- verification report
- Reviewer report
- Boundary Auditor report
- GPT-5.5 extra-high Product Acceptance report
- next-step recommendation

## Acceptance Criteria

- Parser requires opening and closing `---` frontmatter delimiters.
- Parser accepts exactly one non-empty lower-case `status` field inside frontmatter.
- Parser ignores body `status:` lines and body pass-token mentions.
- p2-64 closeout reports parse to their expected statuses.
- Fixtures prove positive status reads and body-status ignore behavior.
- Failure cases reject ambiguous or misleading status documents.
- Reviewer, Boundary Auditor, and GPT-5.5 Product Acceptance pass.
- Final gate passes.

## Stop Conditions

- Any required write would leave this slice path.
- Any task requires dependency install, commit, push, sync, hook, service, background automation, or MCP write tool.
- Any output claims sandbox success as reviewed knowledge, evidence support, action basis, mainline readiness, promotion readiness, Obsidian sync, user approval, or execution authority.
- Product Acceptance returns `BLOCKED_NEEDS_USER`.
