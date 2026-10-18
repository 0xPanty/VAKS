---
slice_id: 2026-06-19-p2-88-old-file-normalization-user-decision-packet-sandbox
status: planned
---

# Slice Plan

## Goal

Create a product-grade, human-reviewable decision packet for the unresolved old-file status-only normalization decision. The packet must make the p2-75 exact approval phrase, the p2-87 all-75-row diff preview, the no-write boundary, and the possible user choices clear without applying any old-file changes.

## Why This Slice Comes Next

p2-87 proved that the proposed 75 status-only changes are previewable and clean, but it did not collect user approval or grant write authority. The next useful sandbox artifact is a decision surface that lets a human decide whether to approve, reject, revise, or keep the old files unchanged.

## Allowed Write Root

`outputs/review/vaks-implementation-sandbox/2026-06-19-p2-88-old-file-normalization-user-decision-packet-sandbox/`

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

- Build a decision packet artifact in JSON, Markdown, and HTML.
- Include the exact p2-75 approval phrase verbatim.
- Include clear decision options: approve with exact phrase, withhold approval, request revision, reject/park.
- Prove the packet is not approval and not write authority.
- Preserve p2-75 exact approval gap.
- Reuse p2-87 preview metrics: 75 previews, 75 hash matches, body unchanged, non-status frontmatter unchanged, 0 old writes.
- Include fixtures, failure cases, local verifier, Reviewer, Boundary Auditor, GPT-5.5 Product Acceptance, final gate, and path audit.

## Stop Conditions

- Stop if any old slice write is needed.
- Stop if any protected path edit is needed.
- Stop if approval, write authority, merge, promotion, reviewed knowledge, evidence support, or action basis would be inferred from the packet.
- Stop on `REVISE_BEFORE_NEXT` or `BLOCKED_NEEDS_USER`.
