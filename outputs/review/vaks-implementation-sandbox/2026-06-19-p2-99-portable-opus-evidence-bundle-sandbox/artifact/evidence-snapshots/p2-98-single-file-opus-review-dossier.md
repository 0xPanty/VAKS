# Single-File Opus Review Dossier

## Instruction To Opus

You are reviewing VAKS sandbox closeout evidence. Decide whether the sandbox closeout evidence is acceptable for sandbox closeout only. Do not treat any pass as mainline approval, reviewed knowledge, evidence support, action basis, commit, push, or sync.

## Current Boundary

Actual Opus result is not present. Opus approval is not claimed. Mainline is not ready. Goal is not complete.

## Summary

| Field | Value |
| --- | --- |
| `dossier_ready` | `True` |
| `evidence_digest_count` | `5` |
| `allowed_conclusion_token_count` | `3` |
| `p2_91_old_slice_writes_applied` | `75` |
| `p2_91_protected_path_writes` | `0` |
| `p2_92_original_item_count` | `20` |
| `p2_92_current_strict_complete_original_item_count` | `20` |
| `p2_94_submission_packet_ready` | `True` |
| `p2_96_result_intake_ready` | `True` |
| `p2_97_guard_state` | `STOP_WAIT_EXTERNAL_OPUS_REVIEW` |
| `actual_opus_result_present` | `False` |
| `opus_approval_claimed` | `False` |
| `mainline_ready` | `False` |
| `reviewed_knowledge_ready` | `False` |
| `evidence_support_ready` | `False` |
| `action_basis_ready` | `False` |
| `goal_complete_now` | `False` |

## Evidence Digest

### p2-91

Verdict: approved old-file status-only normalization applied

  - `old_slice_writes_applied`: `75`
  - `protected_path_writes`: `0`
  - `body_unchanged_count`: `75`
  - `non_status_frontmatter_unchanged_count`: `75`

### p2-92

Verdict: original 20 slices current-strict complete

  - `original_item_count`: `20`
  - `status_operation_count`: `75`
  - `current_strict_complete_original_item_count`: `20`
  - `body_unchanged_count`: `75`
  - `non_status_frontmatter_unchanged_count`: `75`

### p2-94

Verdict: external review submission packet ready

  - `evidence_item_count`: `7`
  - `review_question_count`: `6`
  - `submission_packet_ready`: `True`

### p2-96

Verdict: future Opus result intake skeleton ready

  - `result_intake_ready`: `True`
  - `actual_opus_result_present`: `False`
  - `opus_approval_claimed`: `False`

### p2-97

Verdict: STOP/WAIT guard active

  - `guard_state`: `STOP_WAIT_EXTERNAL_OPUS_REVIEW`
  - `external_opus_review_pending`: `True`
  - `may_merge_mainline`: `False`
  - `may_claim_complete`: `False`

## Review Questions

1. Does the packet prove p2-91 applied only the approved 75 old-file frontmatter status changes?
2. Does p2-92 prove the original 20 sandbox slices now satisfy current strict closeout labels?
3. Is body content preserved for all 75 old report files?
4. Is non-status frontmatter preserved for all 75 old report files?
5. Does any artifact confuse sandbox closeout with mainline merge, reviewed knowledge, evidence support, action basis, or Opus approval?
6. Is the evidence sufficient for external acceptance of sandbox closeout, while still requiring separate user approval for any mainline integration?

## Allowed First-Line Conclusion Tokens

- `OPUS_PASS_SANDBOX_CLOSEOUT`
- `OPUS_REVISE_SANDBOX_CLOSEOUT`
- `OPUS_BLOCKED_NEEDS_USER`

## Required Output

First line must be one allowed token. Then list evidence checked, blockers if any, and an explicit boundary verdict.

## No-Merge Rule

Do not merge mainline, do not claim completion, and do not create reviewed knowledge, evidence support, or action basis from this dossier. A later sandbox-only result intake slice must validate the real Opus response.
