---
record_kind: sandbox_verification
slice_id: 2026-06-16-p2-55-user-decision-e2e-dry-run-simulator-sandbox
status: local_verification_passed
---

# Verification

Run from this slice root:

```powershell
python -B artifact\verify_user_decision_e2e_simulator.py
python -B artifact\verify_user_decision_e2e_simulator.py --run-upstream
python -B artifact\verify_user_decision_e2e_simulator.py --final-gate
```

`--rebuild` is Builder-only:

```powershell
python -B artifact\build_user_decision_e2e_simulator.py
```

## Result

Default verifier:

```json
{
  "passed": true,
  "fixture_count": 10,
  "failure_case_count": 19
}
```

Upstream verifier:

```json
{
  "passed": true,
  "run_upstream_p2_54": true,
  "upstream_p2_54_passed": true
}
```

Sample simulation:

```json
{
  "input_text": "C，合并主线",
  "classifier_case": "approval_with_execution_words",
  "reply_id": "stop_for_separate_scope",
  "automatic_execution": false,
  "decision_collected": false,
  "ready_to_execute": false
}
```

Repair coverage:

- Failure cases are executable mutations of real simulation output.
- The verifier recomputes classifier/renderer/reply consistency instead of
  trusting stored `case_consistent`.
- Unknown fallback is allowed only when classifier output is outside the known
  case set.
- Known classifier cases falling into unknown fallback are rejected.
