---
record_kind: sandbox_verification
slice_id: 2026-06-16-p2-53-user-response-classifier-dry-run-sandbox
status: local_verification_passed
---

# Verification

Run from this slice root:

```powershell
python -B artifact\verify_user_response_classifier_dry_run.py
python -B artifact\verify_user_response_classifier_dry_run.py --run-upstream
python -B artifact\verify_user_response_classifier_dry_run.py --final-gate
```

`--rebuild` is Builder-only:

```powershell
python -B artifact\build_user_response_classifier_dry_run.py
```

## Result

Default verifier:

```json
{
  "passed": true,
  "fixture_count": 14,
  "failure_case_count": 42,
  "response_case_count": 8
}
```

Upstream verifier:

```json
{
  "passed": true,
  "run_upstream_p2_52": true,
  "upstream_p2_52_passed": true
}
```

Repair coverage:

- Each failure case is now executable: it has `input_text`, expected case,
  expected result, expected safe next step, flags, and `must_not`.
- The verifier runs the classifier against every positive fixture and every
  failure case.
- English phrases `promotion review planning` and `merge review` are not option
  tokens. They are conservatively stopped as execution-boundary wording.
- Safe C scope wording such as `选择C，问我主线评审范围` remains classified as
  `explicit_C`, not as execution.

Sample classification:

```json
{
  "input_text": "C，合并主线",
  "case_id": "approval_with_execution_words",
  "automatic_execution": false,
  "requires_new_scope": true,
  "requires_separate_user_approval": true,
  "requires_explicit_allowed_paths": true
}
```

## Expected Result

The verifier must reject any classifier drift that turns a user reply into
execution authority or lets fixtures diverge from the classifier contract.
