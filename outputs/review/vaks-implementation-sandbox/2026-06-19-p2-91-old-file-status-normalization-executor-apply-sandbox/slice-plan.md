---
slice_id: 2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox
status: planned
---

# Slice Plan

## Goal

Apply the p2-75 approved old-file status-only normalization to the original 20 sandbox slice reports by changing only the 75 `frontmatter.status` lines from the p2-72/p2-80 transaction package.

## Approval Basis

The user provided the exact p2-75 approval phrase:

```text
I explicitly approve p2-75 old-file status-only normalization: apply the 75 dry-run frontmatter status changes from p2-72 to the original 20 sandbox slice reports only. Do not edit body content, artifacts, tools, templates, wiki truth layers, main architecture docs, README, Obsidian vault, commit, push, or sync.
```

## Allowed Writes

- This p2-91 sandbox directory.
- The 75 old sandbox report files listed by the p2-80 transaction package, status line only.

## Do Not Touch

- Report body content
- Report non-status frontmatter
- Old slice artifacts / prototypes / fixtures / failure cases
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
- commit / push / sync

## Acceptance Criteria

- 75/75 prewrite hashes match before writing.
- 75/75 current statuses match p2-80 expected before statuses before writing.
- 75/75 writes change only `frontmatter.status`.
- 75/75 body hashes remain unchanged.
- 75/75 non-status frontmatter hashes remain unchanged.
- No protected path writes.
- Local verifier, Reviewer, Boundary Auditor, GPT-5.5 Product Acceptance, and final gate pass.

## Stop Conditions

- Stop before writing if any target hash drifts.
- Stop before writing if any current status differs from p2-80 expected status.
- Stop before writing if any target is missing or frontmatter is invalid.
- Stop if any body, non-status frontmatter, artifact, tool, template, wiki truth layer, root architecture doc, README, Obsidian, commit, push, or sync write would be required.
