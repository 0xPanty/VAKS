---
slice_id: 2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox
status: drafted
---

# Source Map

## Inputs

- p2-80 transaction package:
  `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox/artifact/old_file_status_normalization_transaction_package.json`
- p2-90 post-approval executor handoff:
  `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-90-post-approval-executor-handoff-sandbox/artifact/post_approval_executor_handoff.json`
- Exact user approval phrase, provided in conversation before this slice.

## Output Contract

p2-91 is the old-file status-only executor apply slice. It may modify only the 75 report `frontmatter.status` lines listed by p2-80. It must leave body content, non-status frontmatter, artifacts, protected paths, Obsidian, git commit, push, and sync untouched.

## Reuse Contract

Later audit slices may use p2-91's execution report to prove that original old sandbox reports were normalized to current strict status labels. This report is still sandbox evidence, not mainline architecture, reviewed knowledge, evidence support, or action basis.
