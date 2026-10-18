---
slice_id: 2026-06-19-p2-99-portable-opus-evidence-bundle-sandbox
status: planned
---

# Slice Plan

## Goal

Create a portable Opus evidence bundle that contains the single-file dossier plus immutable snapshots of the key evidence files and checksums.

## Why This Slice Now

p2-98 reduced external review to a single dossier. This slice makes that review portable by bundling the dossier and key source evidence into one sandbox folder with a manifest and SHA256 hashes.

## Write Scope

Only this path may be written:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-99-portable-opus-evidence-bundle-sandbox/
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

- Include snapshot copies of the p2-98 dossier and key p2-91/p2-92/p2-94/p2-96/p2-97 artifacts.
- Include a SHA256 manifest mapping each snapshot to its source path.
- Include a bundle README with no-merge and no-truth/action boundaries.
- Verify snapshot hashes against current source files.
- Include fixtures and failure cases.
- Pass local verifier, Reviewer, Boundary Auditor, and GPT-5.5 Product Acceptance.

## Stop Conditions

- The bundle would need to claim Opus approval or goal completion.
- The bundle would need to write outside its sandbox.
- Reviewer, Boundary Auditor, or Product Acceptance returns a blocking result.

