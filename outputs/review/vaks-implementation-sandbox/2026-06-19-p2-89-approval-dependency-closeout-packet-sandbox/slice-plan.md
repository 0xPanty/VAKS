---
slice_id: 2026-06-19-p2-89-approval-dependency-closeout-packet-sandbox
status: planned
---

# Slice Plan

## Goal

Create a product-grade approval-dependency closeout packet for the old-file status-only normalization lane. The packet must make clear that the technical sandbox evidence is ready for a future gated executor path, but the real old-file write is still blocked by missing exact user approval.

## Why This Slice Comes Next

p2-88 produced the user decision packet. The next smallest useful artifact is a closeout packet that a future agent can read first to avoid conflating "sandbox product-grade" with "old files normalized" or "goal complete".

## Allowed Write Root

`outputs/review/vaks-implementation-sandbox/2026-06-19-p2-89-approval-dependency-closeout-packet-sandbox/`

## Do Not Touch

- Old slice files under `outputs/review/vaks-implementation-sandbox/2026-06-15-*`
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
- commit / push / sync / hooks / background automation

## Acceptance Criteria

- Produce JSON, Markdown, and HTML closeout packet artifacts.
- State technical evidence: 75 previews, 75 hash matches, body unchanged, non-status frontmatter unchanged, 0 old writes.
- State approval gap: exact p2-75 approval is not collected.
- State executor status: blocked until exact approval plus fresh prewrite gate.
- Keep `goal_complete_now=false`.
- Include fixtures, failure cases, verifier, Reviewer, Boundary Auditor, GPT-5.5 Product Acceptance, final gate, and path audit.

## Stop Conditions

- Stop if old-file writes are needed.
- Stop if protected path edits are needed.
- Stop if the artifact would claim approval, write authority, merge, promotion, reviewed knowledge, evidence support, action basis, or goal completion.
