---
slice_id: 2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox
status: generated
---

# Write Attribution Audit

## Scope

This audit attributes p2-91 current-turn writes only. The broader dirty tree is treated as pre-existing baseline under the user rule.

## Allowed Writes

- p2-91 sandbox directory
- 75 p2-80 old sandbox report `frontmatter.status` lines only

## Execution Summary
- passed_prewrite: True
- transaction_operation_count: 75
- unique_target_file_count: 75
- prewrite_hash_match_count: 75
- prewrite_status_match_count: 75
- post_apply_status_match_count: 75
- body_unchanged_count: 75
- non_status_frontmatter_unchanged_count: 75
- old_slice_writes_applied: 75
- protected_path_writes: 0
- normalization_applied: True
- mainline_ready: False
- promotion_ready: False
- reviewed_knowledge_ready: False
- evidence_support_ready: False
- action_basis_ready: False

## Protected Path Status

Protected path dirty entries are current workspace baseline, not attributed to p2-91. p2-91 verifier reports `protected_path_writes: 0`.

## Boundary

p2-91 does not authorize body edits, artifact edits outside p2-91, tools/templates edits, wiki truth edits, mainline edits, Obsidian sync, commit, push, reviewed knowledge, evidence support, or action basis.
