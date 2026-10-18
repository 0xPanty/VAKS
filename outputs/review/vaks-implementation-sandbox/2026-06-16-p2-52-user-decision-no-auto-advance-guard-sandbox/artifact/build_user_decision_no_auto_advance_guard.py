from __future__ import annotations

import json
from pathlib import Path


SLICE_ID = "2026-06-16-p2-52-user-decision-no-auto-advance-guard-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-51-user-decision-request-packet-sandbox"
ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"


FORBIDDEN_OPERATIONS = [
    "commit",
    "push",
    "obsidian_sync",
    "formal_vault_write",
    "mainline_merge",
    "promotion",
    "release",
    "reviewed_knowledge_write",
    "evidence_support_creation",
    "action_basis_creation",
    "template_write",
    "tool_write",
    "dependency_install",
    "background_service",
    "hook_install",
    "mcp_write_tool",
]


RESPONSE_POLICY = [
    {
        "case_id": "no_reply",
        "recognized_input": "no user response after decision packet",
        "decision_state": "no_decision_collected",
        "result": "A_keep_sandbox_reference",
        "action": "no_action",
        "automatic_execution": False,
        "requires_clarification": False,
        "requires_new_scope": False,
        "requires_separate_user_approval": False,
        "allowed_next_message": "wait_for_user_or_report_sandbox_status",
    },
    {
        "case_id": "explicit_A",
        "recognized_input": "user explicitly chooses A",
        "decision_state": "user_selected_keep_reference",
        "result": "A_keep_sandbox_reference",
        "action": "no_action",
        "automatic_execution": False,
        "requires_clarification": False,
        "requires_new_scope": False,
        "requires_separate_user_approval": False,
        "allowed_next_message": "acknowledge_sandbox_reference_only",
    },
    {
        "case_id": "explicit_B",
        "recognized_input": "user explicitly chooses B",
        "decision_state": "future_read_only_planning_requested",
        "result": "future_readonly_promotion_review_planning_request_only",
        "action": "ask_for_separate_read_only_planning_scope_before_any_future_slice",
        "automatic_execution": False,
        "requires_clarification": False,
        "requires_new_scope": True,
        "requires_separate_user_approval": True,
        "allowed_next_message": "ask_user_for_separate_read_only_review_planning_scope",
    },
    {
        "case_id": "explicit_C",
        "recognized_input": "user explicitly chooses C",
        "decision_state": "future_mainline_merge_review_question_requested",
        "result": "future_mainline_merge_scope_question_only",
        "action": "ask_for_separate_mainline_review_scope",
        "automatic_execution": False,
        "requires_clarification": False,
        "requires_new_scope": True,
        "requires_separate_user_approval": True,
        "requires_explicit_allowed_paths": True,
        "allowed_next_message": "ask_user_for_separate_allowed_paths_and_scope",
    },
    {
        "case_id": "explicit_D",
        "recognized_input": "user explicitly chooses D",
        "decision_state": "user_selected_park_or_reject",
        "result": "park_or_reject_sandbox_chain",
        "action": "no_action",
        "automatic_execution": False,
        "requires_clarification": False,
        "requires_new_scope": False,
        "requires_separate_user_approval": False,
        "allowed_next_message": "acknowledge_park_or_reject_status",
    },
    {
        "case_id": "ambiguous_reply",
        "recognized_input": "freeform reply does not clearly select exactly one option",
        "decision_state": "unclear_user_decision",
        "result": "clarify_required",
        "action": "ask_clarifying_question",
        "automatic_execution": False,
        "requires_clarification": True,
        "requires_new_scope": False,
        "requires_separate_user_approval": False,
        "allowed_next_message": "ask_one_short_clarification",
    },
    {
        "case_id": "multiple_options",
        "recognized_input": "reply selects more than one option",
        "decision_state": "conflicting_user_decision",
        "result": "clarify_required",
        "action": "ask_clarifying_question",
        "automatic_execution": False,
        "requires_clarification": True,
        "requires_new_scope": False,
        "requires_separate_user_approval": False,
        "allowed_next_message": "ask_user_to_choose_one_option",
    },
    {
        "case_id": "approval_with_execution_words",
        "recognized_input": "reply mixes decision with commit, push, sync, merge, promote, or action-basis wording",
        "decision_state": "scope_boundary_crossing_detected",
        "result": "stop_and_require_new_scope",
        "action": "no_action",
        "automatic_execution": False,
        "requires_clarification": True,
        "requires_new_scope": True,
        "requires_separate_user_approval": True,
        "allowed_next_message": "stop_and_ask_for_separate_explicit_scope",
    },
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def guard_config() -> dict:
    return {
        "record_kind": "sandbox_user_decision_no_auto_advance_guard",
        "slice_id": SLICE_ID,
        "source_slice_id": SOURCE_SLICE_ID,
        "truth_boundary": "response_handling_guard_not_user_choice_or_execution_authority",
        "status": "built_pending_review",
        "safe_default_if_no_reply": "A_keep_sandbox_reference",
        "scope": {
            "write_scope": f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/",
            "source_packet": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/",
            "source_final_gate_command": (
                "python -B .\\outputs\\review\\vaks-implementation-sandbox\\"
                f"{SOURCE_SLICE_ID}\\artifact\\verify_user_decision_request_packet.py --final-gate"
            ),
            "does_not_modify_mainline": True,
            "does_not_collect_user_decision": True,
            "does_not_execute_any_option": True,
        },
        "response_policy": RESPONSE_POLICY,
        "forbidden_operations": {name: False for name in FORBIDDEN_OPERATIONS},
        "readiness_flags": {
            "guard_ready": True,
            "ready_to_wait_for_user": True,
            "user_choice_collected": False,
            "ready_to_execute": False,
            "auto_advance_allowed": False,
            "mainline_ready": False,
            "promotion_ready": False,
            "release_ready": False,
            "formal_vault_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
        },
        "required_non_claims": [
            "This guard is not a user decision.",
            "This guard is not approval to execute option B or option C.",
            "This guard is not promotion, merge, release, commit, push, or sync authority.",
            "This guard is not reviewed knowledge, evidence support, or action basis.",
            "A future option B or C response must start a separately scoped conversation before any execution.",
        ],
        "ordinary_agent_usage": {
            "default_verifier": "python -B artifact/verify_user_decision_no_auto_advance_guard.py",
            "upstream_verifier": "python -B artifact/verify_user_decision_no_auto_advance_guard.py --run-upstream",
            "final_gate": "python -B artifact/verify_user_decision_no_auto_advance_guard.py --final-gate",
            "rebuild": "Builder-only: python -B artifact/build_user_decision_no_auto_advance_guard.py",
        },
    }


def fixture_payloads() -> dict[str, dict]:
    return {
        "no_reply_default.json": {
            "case_id": "no_reply",
            "input_state": "no_user_response",
            "expected_result": "A_keep_sandbox_reference",
            "expected_action": "no_action",
            "requires_new_scope": False,
            "requires_separate_user_approval": False,
            "requires_explicit_allowed_paths": False,
            "must_not": ["execute_option", "merge", "promote", "sync", "commit", "push"],
        },
        "explicit_a_keep_reference.json": {
            "case_id": "explicit_A",
            "input_text": "A",
            "expected_result": "A_keep_sandbox_reference",
            "expected_action": "no_action",
            "requires_new_scope": False,
            "requires_separate_user_approval": False,
            "requires_explicit_allowed_paths": False,
            "must_not": ["execute_option", "merge", "promote", "sync", "commit", "push"],
        },
        "explicit_b_future_readonly_planning.json": {
            "case_id": "explicit_B",
            "input_text": "B",
            "expected_result": "future_readonly_promotion_review_planning_request_only",
            "expected_action": "ask_for_separate_read_only_planning_scope_before_any_future_slice",
            "requires_new_scope": True,
            "requires_separate_user_approval": True,
            "requires_explicit_allowed_paths": False,
            "must_not": ["mainline_merge", "promotion", "sync", "commit", "push"],
        },
        "explicit_c_future_scope_question.json": {
            "case_id": "explicit_C",
            "input_text": "C",
            "expected_result": "future_mainline_merge_scope_question_only",
            "expected_action": "ask_for_separate_mainline_review_scope",
            "requires_new_scope": True,
            "requires_separate_user_approval": True,
            "requires_explicit_allowed_paths": True,
            "must_not": ["mainline_merge", "promotion", "sync", "commit", "push"],
        },
    }


def failure_case_payloads() -> list[dict]:
    base = [
        ("missing_no_reply_case", "response_policy lacks no_reply safe default"),
        ("no_reply_not_A", "no_reply does not default to A_keep_sandbox_reference"),
        ("no_reply_executes_action", "no_reply allows execution"),
        ("explicit_A_executes_action", "explicit A allows execution"),
        ("explicit_B_executes_now", "explicit B auto-executes planning or promotion"),
        ("explicit_B_missing_new_scope", "explicit B does not require new scope"),
        ("explicit_B_missing_separate_approval", "explicit B does not require separate user approval"),
        ("explicit_C_executes_merge", "explicit C auto-executes merge"),
        ("explicit_C_missing_explicit_paths", "explicit C does not require explicit allowed paths"),
        ("explicit_C_missing_separate_approval", "explicit C does not require separate user approval"),
        ("explicit_D_promotes_rejection", "explicit D mutates mainline or reviewed knowledge"),
        ("ambiguous_reply_executes", "ambiguous reply does anything other than ask clarification"),
        ("ambiguous_reply_no_clarification", "ambiguous reply fails to require clarification"),
        ("multiple_options_executes", "multiple options do anything other than ask clarification"),
        ("execution_words_allowed", "approval with execution words is not stopped"),
        ("commit_enabled", "commit forbidden operation is true"),
        ("push_enabled", "push forbidden operation is true"),
        ("obsidian_sync_enabled", "obsidian_sync forbidden operation is true"),
        ("mainline_merge_enabled", "mainline_merge forbidden operation is true"),
        ("promotion_enabled", "promotion forbidden operation is true"),
        ("release_enabled", "release forbidden operation is true"),
        ("reviewed_knowledge_enabled", "reviewed_knowledge_write forbidden operation is true"),
        ("evidence_support_enabled", "evidence_support_creation forbidden operation is true"),
        ("action_basis_enabled", "action_basis_creation forbidden operation is true"),
        ("template_write_enabled", "template_write forbidden operation is true"),
        ("tool_write_enabled", "tool_write forbidden operation is true"),
        ("dependency_install_enabled", "dependency_install forbidden operation is true"),
        ("background_service_enabled", "background_service forbidden operation is true"),
        ("hook_install_enabled", "hook_install forbidden operation is true"),
        ("mcp_write_enabled", "mcp_write_tool forbidden operation is true"),
        ("auto_advance_true", "auto_advance_allowed readiness flag is true"),
        ("ready_to_execute_true", "ready_to_execute readiness flag is true"),
        ("mainline_ready_true", "mainline_ready readiness flag is true"),
        ("promotion_ready_true", "promotion_ready readiness flag is true"),
        ("action_basis_ready_true", "action_basis_ready readiness flag is true"),
        ("source_slice_missing", "source p2-51 slice is not referenced"),
        ("source_final_gate_missing", "p2-51 final gate command is missing"),
        ("source_final_gate_not_final", "p2-51 command does not include --final-gate"),
        ("truth_boundary_missing", "truth boundary does not say guard is not authority"),
        ("non_claims_missing", "required non-claims are missing"),
        ("rebuild_not_builder_only", "rebuild command is not marked Builder-only"),
        ("ordinary_agent_uses_rebuild", "ordinary usage points agents at rebuild"),
        ("allowed_next_message_allows_open", "allowed_next_message contains open or start wording"),
        ("allowed_next_message_allows_execution", "allowed_next_message contains execute, run, merge, promote, commit, push, sync, or write wording"),
        ("allowed_next_message_missing_approval_scope", "B/C allowed_next_message does not ask for separate scope or approval before future work"),
        ("fixture_result_contract_drift", "positive fixture expected_result no longer matches the response policy"),
        ("fixture_action_contract_drift", "positive fixture expected_action no longer matches the response policy"),
        ("fixture_scope_contract_drift", "positive fixture scope or approval flags no longer match the response policy"),
        ("fixture_missing_false_scope_flags", "positive fixture omits explicit false scope or approval flags"),
        ("fixture_missing_no_reply", "no_reply positive fixture is missing"),
        ("fixture_missing_explicit_A", "explicit A positive fixture is missing"),
        ("fixture_missing_explicit_B", "explicit B positive fixture is missing"),
        ("fixture_missing_explicit_C", "explicit C positive fixture is missing"),
    ]
    return [
        {
            "failure_id": failure_id,
            "description": description,
            "expected_guard_response": "reject_or_stop",
            "must_not": [
                "execute_option",
                "merge_mainline",
                "promote",
                "sync_obsidian",
                "write_reviewed_knowledge",
                "create_action_basis",
            ],
        }
        for failure_id, description in base
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

Create a no-auto-advance guard for the p2-51 user decision request packet.

## Why This Slice Exists

p2-51 asks the user whether to keep the sandbox as reference, open a future
read-only promotion review planning slice, ask for a separately scoped mainline
merge review, or park/reject the sandbox chain. This slice makes the next-agent
behavior explicit: none of those options can be executed by inference.

## In Scope

- Define the response-handling contract for no reply, A, B, C, D, ambiguous
  replies, multiple options, and execution-word replies.
- Preserve p2-51 as the source packet.
- Provide fixtures, failure cases, a static readout/prototype, and a verifier.
- Run p2-51 final gate as an upstream dependency in this slice final gate.

## Out of Scope

- No mainline merge.
- No promotion.
- No formal vault write or Obsidian sync.
- No reviewed knowledge, evidence support, or action basis.
- No commit, push, dependency install, hook, service, automation, or MCP write tool.

## Acceptance Criteria

- Default no-reply behavior is `A_keep_sandbox_reference`.
- Options B and C are future scoped conversations only.
- Ambiguous or conflicting replies stop for clarification.
- Execution words stop and require separate explicit scope.
- All forbidden operation flags are false.
- Local final gate passes, including the p2-51 upstream final gate.
- Reviewer, Boundary Auditor, and GPT-5.5 extra-high Product Acceptance pass.
""",
        "source-map.md": f"""
---
record_kind: sandbox_source_map
slice_id: {SLICE_ID}
status: built_pending_review
---

# Source Map

## Source Inputs

- `outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/product-acceptance-report.md`
- `outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/artifact/user_decision_request_packet.json`
- `outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/artifact/verify_user_decision_request_packet.py`

## Upstream Gate

The final gate for this slice runs:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SOURCE_SLICE_ID}\\artifact\\verify_user_decision_request_packet.py --final-gate
```

## Boundary Interpretation

p2-51 is a product-grade request packet, not a collected user decision. This
slice adds the guard that prevents request-packet options from being treated as
execution authority.
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
python -B artifact\\verify_user_decision_no_auto_advance_guard.py
python -B artifact\\verify_user_decision_no_auto_advance_guard.py --run-upstream
python -B artifact\\verify_user_decision_no_auto_advance_guard.py --final-gate
```

`--rebuild` is Builder-only:

```powershell
python -B artifact\\build_user_decision_no_auto_advance_guard.py
```

## Expected Result

The verifier must reject any contract that turns p2-51 into execution authority.
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

If this slice receives `PASS_PRODUCT_GRADE`, do not execute any p2-51 option.
Wait for an explicit user choice. If the user chooses B or C, open a separate
scoped conversation or slice according to the guard; do not merge, promote,
sync, commit, push, or write reviewed/action layers by inference.
""",
    }


def readout(config: dict, failures: list[dict]) -> str:
    rows = "\n".join(
        f"| `{item['case_id']}` | `{item['result']}` | `{item['action']}` | `{item['automatic_execution']}` | `{item.get('requires_new_scope', False)}` | `{item.get('requires_separate_user_approval', False)}` | `{item['allowed_next_message']}` |"
        for item in config["response_policy"]
    )
    return f"""
---
record_kind: sandbox_artifact_readout
slice_id: {SLICE_ID}
status: built_pending_review
---

# No-Auto-Advance Guard Readout

This artifact guards the p2-51 decision request packet from being mistaken for
execution authority.

## Response Policy

| Case | Result | Action | Automatic Execution | New Scope | Separate Approval | Allowed Next Message |
| --- | --- | --- | --- | --- | --- | --- |
{rows}

## Forbidden Operations

All forbidden operation flags are set to `false`: commit, push, Obsidian sync,
mainline merge, promotion, release, reviewed knowledge write, evidence support
creation, action-basis creation, template/tool writes, dependency install,
background service, hook install, and MCP write tool.

## Positive Fixtures

The package includes {len(fixture_payloads())} positive fixtures.

## Failure Cases

The package includes {len(failures)} failure cases that reject automatic
execution, missing scope separation, missing approval separation, and boundary
confusion.

## Usage

Ordinary agents should run the verifier. `--rebuild` is Builder-only.
"""


def prototype(config: dict) -> str:
    cards = "\n".join(
        f"""
        <section class=\"case\">
          <h2>{item['case_id']}</h2>
          <p><strong>Result:</strong> {item['result']}</p>
          <p><strong>Action:</strong> {item['action']}</p>
          <p><strong>Auto execution:</strong> {str(item['automatic_execution']).lower()}</p>
          <p><strong>New scope:</strong> {str(item.get('requires_new_scope', False)).lower()}</p>
          <p><strong>Separate approval:</strong> {str(item.get('requires_separate_user_approval', False)).lower()}</p>
          <p><strong>Allowed next:</strong> {item['allowed_next_message']}</p>
        </section>
        """
        for item in config["response_policy"]
    )
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <title>{SLICE_ID}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2937; background: #f8fafc; }}
    main {{ max-width: 980px; margin: 0 auto; }}
    h1 {{ font-size: 28px; margin-bottom: 8px; }}
    .summary {{ border-left: 4px solid #2563eb; padding: 12px 16px; background: #eff6ff; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-top: 20px; }}
    .case {{ border: 1px solid #cbd5e1; border-radius: 8px; padding: 14px; background: white; }}
    h2 {{ font-size: 16px; margin: 0 0 8px; }}
    p {{ margin: 6px 0; }}
  </style>
</head>
<body>
  <main>
    <h1>User Decision No-Auto-Advance Guard</h1>
    <div class=\"summary\">
      <p>This sandbox artifact prevents the p2-51 decision request packet from becoming execution authority.</p>
      <p>Safe default: <strong>{config['safe_default_if_no_reply']}</strong>.</p>
    </div>
    <div class=\"grid\">
{cards}
    </div>
  </main>
</body>
</html>
"""


def main() -> None:
    ARTIFACT.mkdir(parents=True, exist_ok=True)
    FIXTURES.mkdir(parents=True, exist_ok=True)
    FAILURE_CASES.mkdir(parents=True, exist_ok=True)

    config = guard_config()
    failures = failure_case_payloads()

    write_json(ARTIFACT / "user_decision_no_auto_advance_guard.json", config)
    write_text(ARTIFACT / "no_auto_advance_guard_readout.md", readout(config, failures))
    write_text(ARTIFACT / "no_auto_advance_guard_prototype.html", prototype(config))

    for filename, payload in fixture_payloads().items():
        write_json(FIXTURES / filename, payload)

    write_json(FAILURE_CASES / "no_auto_advance_failure_cases.json", failures)

    for filename, text in markdown_files().items():
        write_text(ROOT / filename, text)


if __name__ == "__main__":
    main()
