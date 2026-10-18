---
slice_id: 2026-06-19-p2-100-opus-review-transfer-package-sandbox
status: planned
---

# Slice Plan

## Goal

Create a portable transfer package for external Opus review from the already accepted p2-99 evidence bundle.

## Why This Slice Now

p2-99 made the evidence portable as a sandbox folder. This slice turns that folder into a single transfer package with a ZIP hash, a content manifest, and operator-facing instructions, so external review can receive one artifact instead of many scattered paths.

## Write Scope

Only this path may be written:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-100-opus-review-transfer-package-sandbox/
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

- Generate a deterministic transfer ZIP from p2-99 evidence.
- Generate a ZIP SHA256 file and external manifest.
- Include a content manifest and transfer README.
- Include positive fixtures and failure cases.
- Verify ZIP content hashes against source files.
- Preserve no-approval, no-mainline, no-truth/action authority boundaries.
- Pass local verifier, Reviewer, Boundary Auditor, and GPT-5.5 Product Acceptance.

## Stop Conditions

- The package would need a real Opus output.
- The package would need to modify p2-99 or any older slice.
- The package would need to write outside its sandbox.
- Reviewer, Boundary Auditor, or Product Acceptance returns a blocking result.
