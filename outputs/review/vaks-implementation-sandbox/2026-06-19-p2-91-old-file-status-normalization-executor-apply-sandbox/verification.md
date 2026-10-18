---
slice_id: 2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox
status: local_verification_passed
---

# Verification

## Commands

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox\artifact\apply_old_file_status_normalization.py
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox\artifact\repair_line_endings_after_apply.py
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox\artifact\verify_old_file_status_normalization_executor_apply.py
```

## Result

Local verifier passed after executor apply and line-ending repair.

```json
{
  "passed": true,
  "failures": [],
  "summary": {
    "fixture_count": 5,
    "failure_case_count": 8,
    "transaction_operation_count": 75,
    "old_slice_writes_applied": 75,
    "post_apply_status_match_count": 75,
    "body_unchanged_count": 75,
    "non_status_frontmatter_unchanged_count": 75,
    "protected_path_writes": 0,
    "final_gate": false
  }
}
```

## Repair Note

The first executor run used Python text-mode writing on Windows, which changed line-ending bytes. The verifier caught this immediately. `repair_line_endings_after_apply.py` restored all 75 target files to the exact p2-87 proposed byte hashes:

```json
{
  "status": "repaired",
  "repaired_count": 75,
  "expected_proposed_hash_match_count": 75
}
```

After repair, the local verifier proves 75/75 status matches, 75/75 body unchanged, 75/75 non-status frontmatter unchanged, and 0 protected path writes.

## Reviewer-Driven Fixture Repair

Reviewer found two fixtures still reflected the pre-repair `0` counts. The repair script now updates those fixtures, and the verifier now checks fixture contents, not only fixture existence.

Current verifier result after fixture repair:

```json
{
  "passed": true,
  "failures": [],
  "summary": {
    "fixture_count": 5,
    "failure_case_count": 8,
    "transaction_operation_count": 75,
    "old_slice_writes_applied": 75,
    "post_apply_status_match_count": 75,
    "body_unchanged_count": 75,
    "non_status_frontmatter_unchanged_count": 75,
    "protected_path_writes": 0,
    "final_gate": false
  }
}
```

## Attribution Audit

`artifact/write_attribution_audit.json` records the allowed write set for this slice:

- p2-91 sandbox directory;
- 75 p2-80 old sandbox report `frontmatter.status` lines only.

The broader dirty tree is treated as pre-existing baseline under the user rule. p2-91 verifier records `protected_path_writes: 0`.

## Boundary Note

This verification proves only the approved old sandbox report `frontmatter.status` normalization. It does not merge mainline, promote knowledge, create reviewed knowledge, create evidence support, create action basis, commit, push, sync, or edit protected paths.

## Final Gate

Final gate passed after Reviewer, Boundary Auditor, GPT-5.5 extra-high Product Acceptance, and next-step statuses were recorded.

```json
{
  "passed": true,
  "failures": [],
  "summary": {
    "fixture_count": 5,
    "failure_case_count": 8,
    "transaction_operation_count": 75,
    "old_slice_writes_applied": 75,
    "post_apply_status_match_count": 75,
    "body_unchanged_count": 75,
    "non_status_frontmatter_unchanged_count": 75,
    "protected_path_writes": 0,
    "final_gate": true
  }
}
```
