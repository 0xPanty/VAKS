---
record_kind: sandbox_verification
slice_id: 2026-06-16-p2-56-user-decision-demo-transcript-smoke-runner-sandbox
status: local_verification_passed
---

# Verification

Run from this slice root:

```powershell
python -B artifact\verify_user_decision_demo_transcript_smoke_runner.py
python -B artifact\verify_user_decision_demo_transcript_smoke_runner.py --run-upstream
python -B artifact\verify_user_decision_demo_transcript_smoke_runner.py --final-gate
```

`--rebuild` is Builder-only:

```powershell
python -B artifact\build_user_decision_demo_transcript_smoke_runner.py
```

## Result

Default verifier:

```json
{
  "passed": true,
  "scenario_count": 9,
  "fixture_count": 9,
  "failure_case_count": 10
}
```

Upstream verifier:

```json
{
  "passed": true,
  "run_upstream_p2_55": true,
  "upstream_p2_55_passed": true
}
```

Transcript smoke sample:

```text
C，合并主线 -> approval_with_execution_words -> stop_for_separate_scope
```

Repair coverage:

- Runner and verifier stdout are explicitly UTF-8 so the Chinese transcript is
  readable in PowerShell.
- The verifier checks every transcript row against fixture expectations.
- Failure cases mutate transcript, scenario flags, case/reply ids, and
  `must_not` boundaries and must be rejected.
