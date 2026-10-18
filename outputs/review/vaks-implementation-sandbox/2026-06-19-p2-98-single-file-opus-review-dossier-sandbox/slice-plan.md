---
slice_id: 2026-06-19-p2-98-single-file-opus-review-dossier-sandbox
status: planned
---

# Slice Plan

## Goal

Create a single-file Opus review dossier that can be sent to external Opus without manually stitching together multiple sandbox artifacts.

## Why This Slice Now

p2-94 provides a submission prompt and manifest, p2-96 provides result intake, and p2-97 provides a STOP/WAIT guard. This slice reduces external review friction by producing one human-readable dossier that carries the prompt, evidence digest, allowed conclusions, and no-merge boundary.

## Write Scope

Only this path may be written:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-98-single-file-opus-review-dossier-sandbox/
```

## Non-Write Scope

- No old slice edits.
- No root architecture document edits.
- No README edits.
- No wiki truth layer edits.
- No templates or tools edits.
- No Obsidian vault writes or sync.
- No commit, push, promotion, or mainline merge.
- No claim that Opus has approved anything.

## Acceptance Criteria

- Produce `artifact/single-file-opus-review-dossier.md`.
- Include evidence digest from p2-91, p2-92, p2-94, p2-96, and p2-97.
- Include exactly the allowed Opus conclusion tokens.
- Include no-merge and no-truth/action boundaries.
- Include fixtures and failure cases.
- Pass local verifier, Reviewer, Boundary Auditor, and GPT-5.5 Product Acceptance.

## Stop Conditions

- The dossier would need to invent or simulate an Opus result.
- The dossier would need to write outside its sandbox.
- Reviewer, Boundary Auditor, or Product Acceptance returns a blocking result.

