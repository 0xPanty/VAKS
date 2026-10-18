from __future__ import annotations

import json
from pathlib import Path


SLICE_ID = "2026-06-16-p2-55-user-decision-e2e-dry-run-simulator-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-54-safe-user-response-renderer-dry-run-sandbox"
ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"

MUST_NOT = [
    "execute_option",
    "merge_mainline",
    "promote",
    "sync_obsidian",
    "commit",
    "push",
    "write_reviewed_knowledge",
    "create_evidence_support",
    "create_action_basis",
    "start_future_slice_by_inference",
]

SCENARIOS = {
    "no_reply": ("", "no_reply", "keep_reference_no_action"),
    "explicit_a": ("A", "explicit_A", "acknowledge_reference_only"),
    "explicit_b": ("B", "explicit_B", "ask_readonly_planning_scope"),
    "explicit_c": ("C", "explicit_C", "ask_mainline_review_scope"),
    "explicit_d": ("D", "explicit_D", "acknowledge_park_or_reject"),
    "ambiguous_continue": ("继续", "ambiguous_reply", "ask_one_clarification"),
    "multiple_b_c": ("B 和 C 都行", "multiple_options", "ask_choose_one"),
    "execution_c_merge": ("C，合并主线", "approval_with_execution_words", "stop_for_separate_scope"),
    "safe_c_scope": ("选择C，问我主线评审范围", "explicit_C", "ask_mainline_review_scope"),
    "unknown_case": ("__synthetic_unknown_case__", "unknown_case_fallback", "stop_for_unknown_classifier_case"),
}


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def contract() -> dict:
    return {
        "record_kind": "sandbox_user_decision_e2e_dry_run_simulator_contract",
        "slice_id": SLICE_ID,
        "source_slice_id": SOURCE_SLICE_ID,
        "truth_boundary": "e2e_dry_run_not_user_decision_or_execution_authority",
        "status": "built_pending_review",
        "purpose": "simulate user input through p2-53 classifier and p2-54 renderer without executing any option",
        "source_final_gate_command": (
            "python -B .\\outputs\\review\\vaks-implementation-sandbox\\"
            f"{SOURCE_SLICE_ID}\\artifact\\verify_safe_user_response_renderer.py --final-gate"
        ),
        "expected_flow": [
            "input_text",
            "p2_53_classifier_result",
            "p2_54_renderer_result",
            "consistency_checks",
            "forbidden_action_boundaries",
        ],
        "simulation_output_contract": {
            "automatic_execution": False,
            "decision_collected": False,
            "ready_to_execute": False,
            "mainline_ready": False,
            "promotion_ready": False,
            "action_basis_ready": False,
            "must_not": MUST_NOT,
        },
        "required_non_claims": [
            "The simulator is not a user decision.",
            "The simulator is not execution authority.",
            "The simulator cannot approve merge, promotion, sync, commit, push, reviewed knowledge, evidence support, or action basis.",
            "The simulator only shows what a later agent should say next.",
            "Unknown or inconsistent upstream output must fail closed.",
        ],
        "ordinary_agent_usage": {
            "simulate_example": "python -B artifact/simulate_user_decision_dry_run.py --text \"B\"",
            "default_verifier": "python -B artifact/verify_user_decision_e2e_simulator.py",
            "upstream_verifier": "python -B artifact/verify_user_decision_e2e_simulator.py --run-upstream",
            "final_gate": "python -B artifact/verify_user_decision_e2e_simulator.py --final-gate",
            "rebuild": "Builder-only: python -B artifact/build_user_decision_e2e_simulator.py",
        },
    }


def fixtures() -> dict[str, dict]:
    return {
        f"{name}.json": {
            "input_text": input_text,
            "expected_case_id": case_id,
            "expected_reply_id": reply_id,
            "automatic_execution": False,
            "decision_collected": False,
            "ready_to_execute": False,
            "must_not": MUST_NOT,
        }
        for name, (input_text, case_id, reply_id) in SCENARIOS.items()
    }


def failure_cases() -> list[dict]:
    cases = [
        ("classifier_renderer_mismatch", "B", {"renderer.classifier_case_id": "explicit_C"}),
        ("renderer_reply_mismatch", "C", {"renderer.reply_id": "ask_readonly_planning_scope"}),
        ("known_case_bad_unknown_fallback", "B", {"renderer.reply_id": "stop_for_unknown_classifier_case"}),
        ("automatic_execution_true", "A", {"automatic_execution": True}),
        ("decision_collected_true", "B", {"decision_collected": True}),
        ("ready_to_execute_true", "C", {"ready_to_execute": True}),
        ("mainline_ready_true", "C，合并主线", {"mainline_ready": True}),
        ("promotion_ready_true", "B", {"promotion_ready": True}),
        ("action_basis_ready_true", "A", {"action_basis_ready": True}),
        ("classifier_executes", "B", {"classifier.automatic_execution": True}),
        ("renderer_executes", "C", {"renderer.automatic_execution": True}),
        ("case_consistency_false", "B", {"consistency.case_consistent": False}),
        ("reply_missing", "A", {"consistency.reply_present": False}),
        ("must_not_missing_commit", "D", {"must_not_remove": "commit"}),
        ("must_not_missing_action_basis", "继续", {"must_not_remove": "create_action_basis"}),
        ("unknown_case_not_fallback", "__synthetic_unknown_case__", {"renderer.reply_id": "ask_one_clarification"}),
        ("execution_word_not_stopped", "C，合并主线", {"classifier.case_id": "explicit_C", "renderer.reply_id": "ask_mainline_review_scope"}),
        ("multiple_options_not_clarified", "B 和 C 都行", {"classifier.case_id": "explicit_B", "renderer.reply_id": "ask_readonly_planning_scope"}),
        ("ambiguous_not_clarified", "继续", {"classifier.case_id": "explicit_B", "renderer.reply_id": "ask_readonly_planning_scope"}),
    ]
    return [
        {
            "failure_id": failure_id,
            "input_text": input_text,
            "mutation": mutation,
            "must_fail_reason": "simulator verifier must reject this executable mutated state",
            "must_not": MUST_NOT,
        }
        for failure_id, input_text, mutation in cases
    ]


def markdown_files() -> dict[str, str]:
    return {
        "slice-plan.md": f"""
---
record_kind: sandbox_slice_plan
slice_id: {SLICE_ID}
status: built_pending_review
---

# Slice Plan

## Target

Create an end-to-end dry-run simulator that composes p2-53 classification with
p2-54 safe reply rendering.

## In Scope

- Simulate user input through classifier and renderer.
- Verify classifier/render consistency.
- Verify no execution, no decision authority, and complete `must_not` boundary.
- Run p2-54 final gate as upstream dependency.

## Out of Scope

No merge, promotion, release, sync, commit, push, reviewed knowledge, evidence
support, action basis, mainline write, template/tool write, hook, service,
dependency install, or MCP write tool.
""",
        "source-map.md": f"""
---
record_kind: sandbox_source_map
slice_id: {SLICE_ID}
status: built_pending_review
---

# Source Map

## Upstream Source

- `outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/artifact/render_safe_user_response.py`
- `outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/product-acceptance-report.md`
- `outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/artifact/verify_safe_user_response_renderer.py`

## Upstream Gate

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SOURCE_SLICE_ID}\\artifact\\verify_safe_user_response_renderer.py --final-gate
```

## Interpretation

p2-55 is a composition simulator. It does not execute, approve, merge, promote,
sync, commit, push, create reviewed knowledge, create evidence support, or create
action basis.
""",
        "verification.md": f"""
---
record_kind: sandbox_verification
slice_id: {SLICE_ID}
status: local_verification_pending
---

# Verification

Run from this slice root:

```powershell
python -B artifact\\verify_user_decision_e2e_simulator.py
python -B artifact\\verify_user_decision_e2e_simulator.py --run-upstream
python -B artifact\\verify_user_decision_e2e_simulator.py --final-gate
```

`--rebuild` is Builder-only:

```powershell
python -B artifact\\build_user_decision_e2e_simulator.py
```
""",
        "reviewer-report.md": f"""
---
record_kind: sandbox_reviewer_report
slice_id: {SLICE_ID}
reviewer_role: Reviewer
status: pending
truth_boundary: reviewer_report_not_product_acceptance
---

# Reviewer Report

Pending read-only Reviewer inspection.
""",
        "boundary-audit.md": f"""
---
record_kind: sandbox_boundary_audit
slice_id: {SLICE_ID}
auditor_role: Boundary Auditor
status: pending
truth_boundary: boundary_audit_not_product_acceptance
---

# Boundary Audit

Pending read-only Boundary Auditor inspection.
""",
        "product-acceptance-report.md": f"""
---
record_kind: sandbox_product_acceptance_report
slice_id: {SLICE_ID}
agent_requirement: GPT-5.5 reasoning=xhigh
status: pending
truth_boundary: product_acceptance_only_for_this_sandbox_slice
---

# Product Acceptance Report

Pending GPT-5.5 extra-high Product Acceptance Agent inspection.
""",
        "next-step.md": f"""
---
record_kind: sandbox_next_step
slice_id: {SLICE_ID}
status: pending_product_acceptance
---

# Next Step

If this slice receives `PASS_PRODUCT_GRADE`, later agents may use the simulator
for end-to-end dry-run checks, but must not execute any option by inference.
""",
    }


def readout(data: dict) -> str:
    rows = "\n".join(
        f"| `{name}` | `{input_text}` | `{case_id}` | `{reply_id}` |"
        for name, (input_text, case_id, reply_id) in SCENARIOS.items()
    )
    return f"""
---
record_kind: sandbox_artifact_readout
slice_id: {SLICE_ID}
status: built_pending_review
---

# E2E Dry-Run Simulator Readout

| Scenario | Input | Expected Case | Expected Reply |
| --- | --- | --- | --- |
{rows}

The simulator composes p2-53 and p2-54. It is dry-run only and cannot authorize
execution.
"""


def prototype() -> str:
    cards = "\n".join(
        f"""
        <section class=\"case\">
          <h2>{name}</h2>
          <p><strong>Input:</strong> {input_text or "(empty)"}</p>
          <p><strong>Case:</strong> {case_id}</p>
          <p><strong>Reply:</strong> {reply_id}</p>
        </section>
        """
        for name, (input_text, case_id, reply_id) in SCENARIOS.items()
    )
    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\">
  <title>{SLICE_ID}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #172033; background: #f8fafc; }}
    main {{ max-width: 1040px; margin: 0 auto; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; }}
    .case {{ border: 1px solid #cbd5e1; border-radius: 8px; padding: 14px; background: white; }}
  </style>
</head>
<body>
  <main>
    <h1>User Decision E2E Dry-Run Simulator</h1>
    <p>Input to classifier to safe renderer. No execution.</p>
    <div class=\"grid\">{cards}</div>
  </main>
</body>
</html>
"""


def main() -> None:
    ARTIFACT.mkdir(parents=True, exist_ok=True)
    FIXTURES.mkdir(parents=True, exist_ok=True)
    FAILURE_CASES.mkdir(parents=True, exist_ok=True)
    data = contract()
    write_json(ARTIFACT / "user_decision_e2e_simulator_contract.json", data)
    write_text(ARTIFACT / "user_decision_e2e_simulator_readout.md", readout(data))
    write_text(ARTIFACT / "user_decision_e2e_simulator_prototype.html", prototype())
    for filename, payload in fixtures().items():
        write_json(FIXTURES / filename, payload)
    write_json(FAILURE_CASES / "user_decision_e2e_failure_cases.json", failure_cases())
    for filename, text in markdown_files().items():
        write_text(ROOT / filename, text)


if __name__ == "__main__":
    main()
