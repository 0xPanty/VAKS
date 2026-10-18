from __future__ import annotations

import json
from pathlib import Path


SLICE_ID = "2026-06-16-p2-56-user-decision-demo-transcript-smoke-runner-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-55-user-decision-e2e-dry-run-simulator-sandbox"
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

DEMO_SCENARIOS = [
    {"scenario_id": "no_reply", "input_text": "", "expected_case_id": "no_reply", "expected_reply_id": "keep_reference_no_action"},
    {"scenario_id": "option_a", "input_text": "A", "expected_case_id": "explicit_A", "expected_reply_id": "acknowledge_reference_only"},
    {"scenario_id": "option_b", "input_text": "B", "expected_case_id": "explicit_B", "expected_reply_id": "ask_readonly_planning_scope"},
    {"scenario_id": "option_c", "input_text": "C", "expected_case_id": "explicit_C", "expected_reply_id": "ask_mainline_review_scope"},
    {"scenario_id": "option_d", "input_text": "D", "expected_case_id": "explicit_D", "expected_reply_id": "acknowledge_park_or_reject"},
    {"scenario_id": "ambiguous", "input_text": "继续", "expected_case_id": "ambiguous_reply", "expected_reply_id": "ask_one_clarification"},
    {"scenario_id": "multiple", "input_text": "B 和 C 都行", "expected_case_id": "multiple_options", "expected_reply_id": "ask_choose_one"},
    {"scenario_id": "execution_words", "input_text": "C，合并主线", "expected_case_id": "approval_with_execution_words", "expected_reply_id": "stop_for_separate_scope"},
    {"scenario_id": "unknown_fallback", "input_text": "__synthetic_unknown_case__", "expected_case_id": "synthetic_unknown_case", "expected_reply_id": "stop_for_unknown_classifier_case"},
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def contract() -> dict:
    return {
        "record_kind": "sandbox_user_decision_demo_transcript_smoke_runner_contract",
        "slice_id": SLICE_ID,
        "source_slice_id": SOURCE_SLICE_ID,
        "truth_boundary": "demo_transcript_not_user_decision_or_execution_authority",
        "status": "built_pending_review",
        "purpose": "produce a human-readable transcript from p2-55 e2e dry-run scenarios without executing options",
        "source_final_gate_command": (
            "python -B .\\outputs\\review\\vaks-implementation-sandbox\\"
            f"{SOURCE_SLICE_ID}\\artifact\\verify_user_decision_e2e_simulator.py --final-gate"
        ),
        "demo_scenarios": DEMO_SCENARIOS,
        "output_contract": {
            "automatic_execution": False,
            "decision_collected": False,
            "ready_to_execute": False,
            "mainline_ready": False,
            "promotion_ready": False,
            "action_basis_ready": False,
            "must_not": MUST_NOT,
        },
        "transcript_safety_rules": {
            "must_include_phrases": ["不执行", "sandbox", "must_not"],
            "dangerous_positive_phrases": [
                "我会开始",
                "我将开始",
                "开始执行",
                "正在执行",
                "我会合并",
                "已合并",
                "我会同步",
                "已同步",
                "我会提交",
                "已提交",
                "我会推送",
                "已推送",
                "我会写入",
                "已写入",
                "执行授权",
                "可以合并",
            ],
        },
        "ordinary_agent_usage": {
            "run_demo": "python -B artifact/run_user_decision_demo_transcript.py",
            "default_verifier": "python -B artifact/verify_user_decision_demo_transcript_smoke_runner.py",
            "upstream_verifier": "python -B artifact/verify_user_decision_demo_transcript_smoke_runner.py --run-upstream",
            "final_gate": "python -B artifact/verify_user_decision_demo_transcript_smoke_runner.py --final-gate",
            "rebuild": "Builder-only: python -B artifact/build_user_decision_demo_transcript_smoke_runner.py",
        },
        "required_non_claims": [
            "The transcript is not a user decision.",
            "The transcript is not execution authority.",
            "The transcript cannot approve merge, promotion, sync, commit, push, reviewed knowledge, evidence support, or action basis.",
            "The transcript is a demo of safe next replies only.",
            "The transcript must preserve must_not boundaries for every scenario.",
        ],
    }


def fixtures() -> dict[str, dict]:
    return {
        f"{item['scenario_id']}.json": {
            **item,
            "automatic_execution": False,
            "decision_collected": False,
            "ready_to_execute": False,
            "must_not": MUST_NOT,
        }
        for item in DEMO_SCENARIOS
    }


def failure_cases() -> list[dict]:
    return [
        {
            "failure_id": "transcript_claims_execution",
            "mutation": {"transcript_append": "我会开始执行。"},
            "must_fail_reason": "positive execution language must be rejected",
        },
        {
            "failure_id": "transcript_claims_merge",
            "mutation": {"transcript_append": "可以合并主线。"},
            "must_fail_reason": "merge authorization wording must be rejected",
        },
        {
            "failure_id": "missing_must_not_section",
            "mutation": {"remove_top_level_must_not": True},
            "must_fail_reason": "top-level must_not is required",
        },
        {
            "failure_id": "scenario_missing_must_not",
            "mutation": {"scenario_id": "option_b", "remove_scenario_must_not": "commit"},
            "must_fail_reason": "scenario must_not boundary must be complete",
        },
        {
            "failure_id": "scenario_execution_true",
            "mutation": {"scenario_id": "option_c", "set_scenario_automatic_execution": True},
            "must_fail_reason": "scenario automatic_execution must remain false",
        },
        {
            "failure_id": "scenario_ready_to_execute_true",
            "mutation": {"scenario_id": "execution_words", "set_scenario_ready_to_execute": True},
            "must_fail_reason": "scenario ready_to_execute must remain false",
        },
        {
            "failure_id": "scenario_case_mismatch",
            "mutation": {"scenario_id": "multiple", "set_case_id": "explicit_B"},
            "must_fail_reason": "scenario classifier case must match expected fixture",
        },
        {
            "failure_id": "scenario_reply_mismatch",
            "mutation": {"scenario_id": "ambiguous", "set_reply_id": "ask_readonly_planning_scope"},
            "must_fail_reason": "scenario reply id must match expected fixture",
        },
        {
            "failure_id": "unknown_fallback_missing",
            "mutation": {"scenario_id": "unknown_fallback", "set_reply_id": "ask_one_clarification"},
            "must_fail_reason": "unknown fallback scenario must keep stop_for_unknown_classifier_case",
        },
        {
            "failure_id": "upstream_not_checked",
            "mutation": {"upstream_gate_required": False},
            "must_fail_reason": "final gate must require upstream p2-55 final gate",
        },
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

Create a human-readable demo transcript and smoke runner for the p2-55 user
decision E2E dry-run simulator.

## In Scope

- Run representative p2-55 scenarios.
- Produce a safe transcript that shows input, classifier case, reply id, reply,
  and forbidden action boundaries.
- Verify transcript safety and scenario consistency.
- Run p2-55 final gate as upstream dependency.

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

- `outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/artifact/simulate_user_decision_dry_run.py`
- `outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/product-acceptance-report.md`
- `outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/artifact/verify_user_decision_e2e_simulator.py`

## Upstream Gate

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SOURCE_SLICE_ID}\\artifact\\verify_user_decision_e2e_simulator.py --final-gate
```

## Interpretation

p2-56 is a demo/smoke-runner layer. It is not a user decision, execution
authority, promotion, merge, sync, reviewed knowledge, evidence support, or
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
python -B artifact\\verify_user_decision_demo_transcript_smoke_runner.py
python -B artifact\\verify_user_decision_demo_transcript_smoke_runner.py --run-upstream
python -B artifact\\verify_user_decision_demo_transcript_smoke_runner.py --final-gate
```

`--rebuild` is Builder-only:

```powershell
python -B artifact\\build_user_decision_demo_transcript_smoke_runner.py
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

If this slice receives `PASS_PRODUCT_GRADE`, later agents may use this demo
transcript for smoke checks and operator understanding, but must not execute any
option by inference.
""",
    }


def readout() -> str:
    rows = "\n".join(
        f"| `{item['scenario_id']}` | `{item['input_text'] or '(empty)'}` | `{item['expected_case_id']}` | `{item['expected_reply_id']}` |"
        for item in DEMO_SCENARIOS
    )
    return f"""
---
record_kind: sandbox_artifact_readout
slice_id: {SLICE_ID}
status: built_pending_review
---

# Demo Transcript Smoke Runner Readout

| Scenario | Input | Expected Case | Expected Reply |
| --- | --- | --- | --- |
{rows}

Run:

```powershell
python -B artifact\\run_user_decision_demo_transcript.py
```
"""


def prototype() -> str:
    cards = "\n".join(
        f"<section><h2>{item['scenario_id']}</h2><p>{item['input_text'] or '(empty)'}</p><p>{item['expected_case_id']} -> {item['expected_reply_id']}</p></section>"
        for item in DEMO_SCENARIOS
    )
    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head><meta charset=\"utf-8\"><title>{SLICE_ID}</title>
<style>body{{font-family:Arial,sans-serif;margin:32px;background:#f8fafc;color:#172033}}main{{max-width:1040px;margin:auto}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}}section{{background:white;border:1px solid #cbd5e1;border-radius:8px;padding:14px}}</style></head>
<body><main><h1>User Decision Demo Transcript Smoke Runner</h1><p>Human-readable dry-run transcript. No execution.</p><div class=\"grid\">{cards}</div></main></body></html>
"""


def main() -> None:
    ARTIFACT.mkdir(parents=True, exist_ok=True)
    FIXTURES.mkdir(parents=True, exist_ok=True)
    FAILURE_CASES.mkdir(parents=True, exist_ok=True)
    data = contract()
    write_json(ARTIFACT / "user_decision_demo_transcript_contract.json", data)
    write_text(ARTIFACT / "user_decision_demo_transcript_readout.md", readout())
    write_text(ARTIFACT / "user_decision_demo_transcript_prototype.html", prototype())
    for filename, payload in fixtures().items():
        write_json(FIXTURES / filename, payload)
    write_json(FAILURE_CASES / "user_decision_demo_transcript_failure_cases.json", failure_cases())
    for filename, text in markdown_files().items():
        write_text(ROOT / filename, text)


if __name__ == "__main__":
    main()
