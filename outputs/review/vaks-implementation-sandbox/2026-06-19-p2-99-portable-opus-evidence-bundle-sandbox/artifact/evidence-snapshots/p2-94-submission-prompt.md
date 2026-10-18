# Prompt For Opus External Review

You are Opus acting as an independent external reviewer for a VAKS sandbox closeout. Review the local evidence files listed below. Do not assume sandbox closeout means mainline merge, reviewed knowledge, evidence support, action basis, or user approval. This submission packet does not claim Opus approval before you review it.

## Evidence Files To Inspect

- `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-93-opus-reviewable-closeout-packet-sandbox/artifact/opus_reviewable_closeout_packet.md`: Human-readable closeout packet for external Opus review.
- `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-93-opus-reviewable-closeout-packet-sandbox/artifact/opus-review-checklist.md`: External review checklist.
- `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-93-opus-reviewable-closeout-packet-sandbox/artifact/opus_reviewable_closeout_packet.json`: Machine-readable closeout packet summary.
- `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-93-opus-reviewable-closeout-packet-sandbox/verification.md`: p2-93 final gate evidence.
- `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-93-opus-reviewable-closeout-packet-sandbox/product-acceptance-report.md`: GPT-5.5 Product Acceptance for p2-93.
- `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-92-post-apply-current-strict-closeout-audit-sandbox/artifact/post_apply_current_strict_closeout_audit.json`: Post-apply current-strict closeout audit for original 20 slices.
- `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox/artifact/old_file_status_normalization_executor_apply.json`: Approved old-file status-only normalization executor evidence.

## Review Questions

1. Does the packet prove p2-91 applied only the approved 75 old-file frontmatter status changes?
2. Does p2-92 prove the original 20 sandbox slices now satisfy current strict closeout labels?
3. Is body content preserved for all 75 old report files?
4. Is non-status frontmatter preserved for all 75 old report files?
5. Does any artifact confuse sandbox closeout with mainline merge, reviewed knowledge, evidence support, action basis, or Opus approval?
6. Is the evidence sufficient for external acceptance of sandbox closeout, while still requiring separate user approval for any mainline integration?

## Required Output Format

Return exactly one conclusion token on the first line:

- `OPUS_PASS_SANDBOX_CLOSEOUT`
- `OPUS_REVISE_SANDBOX_CLOSEOUT`
- `OPUS_BLOCKED_NEEDS_USER`

Then provide:

- key evidence checked;
- any blockers or missing proof;
- whether the packet is understandable to a future agent;
- explicit boundary verdict: whether it avoids claiming mainline merge, reviewed knowledge, evidence support, action basis, user approval, or Opus approval before this review.

## Current Packet Summary

```json
{
  "prior_sandbox_slice_count": 92,
  "original_item_count": 20,
  "status_operation_count": 75,
  "p2_80_transaction_operation_count": 75,
  "p2_91_old_slice_writes_applied": 75,
  "p2_91_protected_path_writes": 0,
  "p2_92_current_strict_status_operation_count": 75,
  "p2_92_current_file_hash_match_count": 75,
  "p2_92_body_unchanged_count": 75,
  "p2_92_non_status_frontmatter_unchanged_count": 75,
  "p2_92_current_strict_complete_original_item_count": 20,
  "p2_92_old_slice_writes_applied": 0,
  "p2_92_protected_path_writes": 0,
  "p2_92_final_gate_statuses_complete": true,
  "external_review_packet_ready": true,
  "opus_approval_claimed": false,
  "mainline_ready": false,
  "promotion_ready": false,
  "reviewed_knowledge_ready": false,
  "evidence_support_ready": false,
  "action_basis_ready": false,
  "goal_complete_now": false
}
```
