from __future__ import annotations

import json
from pathlib import Path


SLICE_ID = "2026-06-16-p2-53-user-response-classifier-dry-run-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-52-user-decision-no-auto-advance-guard-sandbox"
ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"


RESPONSE_POLICY = [
    {
        "case_id": "no_reply",
        "result": "A_keep_sandbox_reference",
        "safe_next_step": "no_action",
        "automatic_execution": False,
        "requires_clarification": False,
        "requires_new_scope": False,
        "requires_separate_user_approval": False,
        "requires_explicit_allowed_paths": False,
    },
    {
        "case_id": "explicit_A",
        "result": "A_keep_sandbox_reference",
        "safe_next_step": "acknowledge_sandbox_reference_only",
        "automatic_execution": False,
        "requires_clarification": False,
        "requires_new_scope": False,
        "requires_separate_user_approval": False,
        "requires_explicit_allowed_paths": False,
    },
    {
        "case_id": "explicit_B",
        "result": "future_readonly_promotion_review_planning_request_only",
        "safe_next_step": "ask_user_for_separate_read_only_review_planning_scope",
        "automatic_execution": False,
        "requires_clarification": False,
        "requires_new_scope": True,
        "requires_separate_user_approval": True,
        "requires_explicit_allowed_paths": False,
    },
    {
        "case_id": "explicit_C",
        "result": "future_mainline_merge_scope_question_only",
        "safe_next_step": "ask_user_for_separate_allowed_paths_and_scope",
        "automatic_execution": False,
        "requires_clarification": False,
        "requires_new_scope": True,
        "requires_separate_user_approval": True,
        "requires_explicit_allowed_paths": True,
    },
    {
        "case_id": "explicit_D",
        "result": "park_or_reject_sandbox_chain",
        "safe_next_step": "acknowledge_park_or_reject_status",
        "automatic_execution": False,
        "requires_clarification": False,
        "requires_new_scope": False,
        "requires_separate_user_approval": False,
        "requires_explicit_allowed_paths": False,
    },
    {
        "case_id": "ambiguous_reply",
        "result": "clarify_required",
        "safe_next_step": "ask_one_short_clarification",
        "automatic_execution": False,
        "requires_clarification": True,
        "requires_new_scope": False,
        "requires_separate_user_approval": False,
        "requires_explicit_allowed_paths": False,
    },
    {
        "case_id": "multiple_options",
        "result": "clarify_required",
        "safe_next_step": "ask_user_to_choose_one_option",
        "automatic_execution": False,
        "requires_clarification": True,
        "requires_new_scope": False,
        "requires_separate_user_approval": False,
        "requires_explicit_allowed_paths": False,
    },
    {
        "case_id": "approval_with_execution_words",
        "result": "stop_and_require_new_scope",
        "safe_next_step": "stop_and_ask_for_separate_explicit_scope",
        "automatic_execution": False,
        "requires_clarification": True,
        "requires_new_scope": True,
        "requires_separate_user_approval": True,
        "requires_explicit_allowed_paths": True,
    },
]


def policy(case_id: str) -> dict:
    return next(item for item in RESPONSE_POLICY if item["case_id"] == case_id)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def classifier_contract() -> dict:
    return {
        "record_kind": "sandbox_user_response_classifier_dry_run_contract",
        "slice_id": SLICE_ID,
        "source_slice_id": SOURCE_SLICE_ID,
        "truth_boundary": "dry_run_classifier_not_user_decision_or_execution_authority",
        "status": "built_pending_review",
        "purpose": "classify a future user reply to the p2-51 decision packet without executing any option",
        "source_final_gate_command": (
            "python -B .\\outputs\\review\\vaks-implementation-sandbox\\"
            f"{SOURCE_SLICE_ID}\\artifact\\verify_user_decision_no_auto_advance_guard.py --final-gate"
        ),
        "classification_cases": [item["case_id"] for item in RESPONSE_POLICY],
        "response_policy": RESPONSE_POLICY,
        "token_policy": {
            "option_tokens": {
                "A": ["a", "option a", "choose a", "选a", "选择a", "保留参考", "只保留", "reference only"],
                "B": ["b", "option b", "choose b", "选b", "选择b", "只读规划"],
                "C": ["c", "option c", "choose c", "选c", "选择c", "主线评审"],
                "D": ["d", "option d", "choose d", "选d", "选择d", "park", "reject", "搁置", "拒绝"],
            },
            "execution_boundary_tokens": [
                "commit",
                "push",
                "sync",
                "merge",
                "promote",
                "promotion",
                "release",
                "write",
                "execute",
                "run",
                "start",
                "open",
                "合并",
                "入主线",
                "合并主线",
                "同步",
                "提交",
                "推送",
                "执行",
                "开工",
                "开始",
                "落地",
                "写入",
                "发布",
            ],
        },
        "dry_run_output_contract": {
            "input_text": "original user text or empty string",
            "normalized_text": "lowercase normalized text",
            "detected_options": "array of A/B/C/D",
            "detected_execution_tokens": "array of execution boundary tokens",
            "case_id": "one classification case",
            "result": "policy result",
            "safe_next_step": "safe next message category",
            "automatic_execution": False,
            "must_not": [
                "execute_option",
                "merge_mainline",
                "promote",
                "sync_obsidian",
                "commit",
                "push",
                "write_reviewed_knowledge",
                "create_evidence_support",
                "create_action_basis",
            ],
        },
        "ordinary_agent_usage": {
            "classify_example": "python -B artifact/classify_user_response_dry_run.py --text \"B\"",
            "default_verifier": "python -B artifact/verify_user_response_classifier_dry_run.py",
            "upstream_verifier": "python -B artifact/verify_user_response_classifier_dry_run.py --run-upstream",
            "final_gate": "python -B artifact/verify_user_response_classifier_dry_run.py --final-gate",
            "rebuild": "Builder-only: python -B artifact/build_user_response_classifier_dry_run.py",
        },
        "required_non_claims": [
            "The classifier is not a user decision.",
            "The classifier is not execution authority.",
            "The classifier cannot approve merge, promotion, sync, commit, push, reviewed knowledge, evidence support, or action basis.",
            "Ambiguous, multiple-option, and execution-word replies require stop or clarification.",
            "B and C remain future scoped conversations, not work started by classification.",
        ],
    }


def fixture_payloads() -> dict[str, dict]:
    base = {
        "no_reply_empty.json": {"input_text": "", "case_id": "no_reply"},
        "explicit_a_letter.json": {"input_text": "A", "case_id": "explicit_A"},
        "explicit_a_chinese.json": {"input_text": "选择A，只保留参考", "case_id": "explicit_A"},
        "explicit_b_letter.json": {"input_text": "B", "case_id": "explicit_B"},
        "explicit_b_chinese.json": {"input_text": "选B，先做只读规划", "case_id": "explicit_B"},
        "explicit_c_letter.json": {"input_text": "C", "case_id": "explicit_C"},
        "explicit_c_chinese.json": {"input_text": "选择C，问我主线评审范围", "case_id": "explicit_C"},
        "explicit_d_letter.json": {"input_text": "D", "case_id": "explicit_D"},
        "ambiguous_continue.json": {"input_text": "继续", "case_id": "ambiguous_reply"},
        "ambiguous_freeform.json": {"input_text": "你看着办", "case_id": "ambiguous_reply"},
        "multiple_b_c.json": {"input_text": "B 和 C 都行", "case_id": "multiple_options"},
        "execution_word_with_b.json": {"input_text": "B，直接开工", "case_id": "approval_with_execution_words"},
        "execution_word_with_c.json": {"input_text": "C，合并主线", "case_id": "approval_with_execution_words"},
        "execution_word_without_option.json": {"input_text": "直接合并吧", "case_id": "approval_with_execution_words"},
    }
    fixtures: dict[str, dict] = {}
    for filename, payload in base.items():
        item = policy(payload["case_id"])
        fixtures[filename] = {
            **payload,
            "expected_result": item["result"],
            "expected_safe_next_step": item["safe_next_step"],
            "automatic_execution": False,
            "requires_clarification": item["requires_clarification"],
            "requires_new_scope": item["requires_new_scope"],
            "requires_separate_user_approval": item["requires_separate_user_approval"],
            "requires_explicit_allowed_paths": item["requires_explicit_allowed_paths"],
        }
    return fixtures


def executable_failure_case(failure_id: str, input_text: str, expected_case_id: str, description: str) -> dict:
    item = policy(expected_case_id)
    return {
        "failure_id": failure_id,
        "description": description,
        "input_text": input_text,
        "expected_case_id": expected_case_id,
        "expected_result": item["result"],
        "expected_safe_next_step": item["safe_next_step"],
        "automatic_execution": False,
        "requires_clarification": item["requires_clarification"],
        "requires_new_scope": item["requires_new_scope"],
        "requires_separate_user_approval": item["requires_separate_user_approval"],
        "requires_explicit_allowed_paths": item["requires_explicit_allowed_paths"],
        "must_not": [
            "execute_option",
            "merge_mainline",
            "promote",
            "sync_obsidian",
            "commit",
            "push",
            "write_reviewed_knowledge",
            "create_evidence_support",
            "create_action_basis",
        ],
    }


def failure_cases() -> list[dict]:
    cases = [
        ("whitespace_no_reply_executes", "   ", "no_reply", "whitespace-only replies must not execute"),
        ("ambiguous_continue_auto_selects", "继续", "ambiguous_reply", "ambiguous continue wording must clarify"),
        ("ambiguous_freeform_auto_selects", "你看着办", "ambiguous_reply", "freeform delegation must clarify"),
        ("ambiguous_go_ahead_auto_selects", "go ahead", "ambiguous_reply", "English go-ahead wording must clarify"),
        ("ambiguous_best_option_auto_selects", "do the best option", "ambiguous_reply", "best-option wording must clarify"),
        ("multiple_b_c_auto_selects", "B 和 C 都行", "multiple_options", "multiple B/C must not auto-select"),
        ("multiple_a_d_auto_selects", "A or D", "multiple_options", "multiple A/D must not auto-select"),
        ("multiple_chinese_options", "选B和C", "multiple_options", "Chinese multiple options must clarify"),
        ("multiple_slash_options", "A/B", "multiple_options", "slash options must clarify"),
        ("execution_without_option_merge", "直接合并吧", "approval_with_execution_words", "merge wording must stop"),
        ("execution_without_option_commit", "please commit", "approval_with_execution_words", "commit wording must stop"),
        ("execution_without_option_push", "push it", "approval_with_execution_words", "push wording must stop"),
        ("execution_without_option_sync", "sync to Obsidian", "approval_with_execution_words", "sync wording must stop"),
        ("execution_without_option_promote", "promote it", "approval_with_execution_words", "promote wording must stop"),
        ("execution_without_option_release", "release it", "approval_with_execution_words", "release wording must stop"),
        ("execution_without_option_write", "write to reviewed knowledge", "approval_with_execution_words", "write wording must stop"),
        ("execution_without_option_run", "run it", "approval_with_execution_words", "run wording must stop"),
        ("execution_without_option_open", "open the next slice", "approval_with_execution_words", "open wording must stop"),
        ("execution_without_option_start", "start the work", "approval_with_execution_words", "start wording must stop"),
        ("execution_without_option_chinese_sync", "同步到 Obsidian", "approval_with_execution_words", "Chinese sync must stop"),
        ("execution_without_option_chinese_commit", "提交一下", "approval_with_execution_words", "Chinese commit must stop"),
        ("execution_without_option_chinese_push", "推送一下", "approval_with_execution_words", "Chinese push must stop"),
        ("execution_without_option_chinese_execute", "直接执行", "approval_with_execution_words", "Chinese execute must stop"),
        ("execution_without_option_chinese_start", "开始下一步", "approval_with_execution_words", "Chinese start must stop"),
        ("execution_without_option_chinese_write", "写入正式库", "approval_with_execution_words", "Chinese write must stop"),
        ("explicit_b_plus_start", "B，直接开工", "approval_with_execution_words", "B plus start must stop"),
        ("explicit_b_plus_commit", "B and commit", "approval_with_execution_words", "B plus commit must stop"),
        ("explicit_b_plus_sync", "选B然后同步", "approval_with_execution_words", "B plus sync must stop"),
        ("explicit_b_plus_open", "choose B and open a planning slice", "approval_with_execution_words", "B plus open must stop"),
        ("explicit_b_plus_run", "B run it", "approval_with_execution_words", "B plus run must stop"),
        ("explicit_c_plus_merge", "C，合并主线", "approval_with_execution_words", "C plus merge must stop"),
        ("explicit_c_plus_push", "C and push", "approval_with_execution_words", "C plus push must stop"),
        ("explicit_c_plus_promote", "choose C and promote", "approval_with_execution_words", "C plus promote must stop"),
        ("explicit_c_plus_write", "C 写入主线", "approval_with_execution_words", "C plus write must stop"),
        ("explicit_c_plus_release", "C release", "approval_with_execution_words", "C plus release must stop"),
        ("explicit_d_plus_push", "D and push", "approval_with_execution_words", "D plus push must stop"),
        ("safe_c_scope_phrase", "选择C，问我主线评审范围", "explicit_C", "safe C scope wording must not be stopped"),
        ("safe_b_planning_phrase", "选B，先做只读规划", "explicit_B", "safe B planning wording must not start work"),
        ("english_promotion_review_planning_ambiguous", "promotion review planning", "approval_with_execution_words", "ambiguous English promotion wording must stop"),
        ("english_merge_review_ambiguous", "merge review", "approval_with_execution_words", "ambiguous English merge wording must stop"),
        ("option_b_without_execution", "option b", "explicit_B", "English option B token remains safe"),
        ("option_c_without_execution", "option c", "explicit_C", "English option C token remains safe"),
    ]
    return [executable_failure_case(*case) for case in cases]


def markdown_files(contract: dict, failures: list[dict]) -> dict[str, str]:
    return {
        "slice-plan.md": f"""
---
record_kind: sandbox_slice_plan
slice_id: {SLICE_ID}
status: built_pending_review
---

# Slice Plan

## Target

Create a dry-run classifier for future user replies to the p2-51 decision
packet, using p2-52 as the upstream no-auto-advance guard.

## In Scope

- Classify no reply, A, B, C, D, ambiguous replies, multiple options, and
  execution-word replies.
- Return a safe next-message category.
- Never execute any option.
- Verify fixtures against the classifier output and response policy.
- Run p2-52 final gate as the upstream dependency in the final gate.

## Out of Scope

- No merge, promotion, release, sync, commit, push, reviewed knowledge, evidence
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

- `outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/artifact/user_decision_no_auto_advance_guard.json`
- `outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/product-acceptance-report.md`
- `outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/artifact/verify_user_decision_no_auto_advance_guard.py`

## Upstream Gate

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SOURCE_SLICE_ID}\\artifact\\verify_user_decision_no_auto_advance_guard.py --final-gate
```

## Interpretation

p2-53 only classifies a reply and names the safe next message. It does not
collect the user's decision as authority and does not execute A, B, C, or D.
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
python -B artifact\\verify_user_response_classifier_dry_run.py
python -B artifact\\verify_user_response_classifier_dry_run.py --run-upstream
python -B artifact\\verify_user_response_classifier_dry_run.py --final-gate
```

`--rebuild` is Builder-only:

```powershell
python -B artifact\\build_user_response_classifier_dry_run.py
```

## Expected Result

The verifier must reject any classifier drift that turns a user reply into
execution authority or lets fixtures diverge from the classifier contract.
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

If this slice receives `PASS_PRODUCT_GRADE`, later agents may use the dry-run
classifier to understand a future user reply, but must still follow the
classifier's safe next step and must not execute options by inference.
""",
    }


def readout(contract: dict, fixtures: dict[str, dict], failures: list[dict]) -> str:
    rows = "\n".join(
        f"| `{item['case_id']}` | `{item['result']}` | `{item['safe_next_step']}` | `{item['automatic_execution']}` | `{item['requires_new_scope']}` | `{item['requires_separate_user_approval']}` | `{item['requires_explicit_allowed_paths']}` |"
        for item in contract["response_policy"]
    )
    return f"""
---
record_kind: sandbox_artifact_readout
slice_id: {SLICE_ID}
status: built_pending_review
---

# User Response Classifier Dry-Run Readout

This artifact classifies future user replies to the p2-51 decision request. It
does not execute any option.

| Case | Result | Safe Next Step | Automatic Execution | New Scope | Separate Approval | Explicit Paths |
| --- | --- | --- | --- | --- | --- | --- |
{rows}

## Coverage

- Positive fixtures: {len(fixtures)}
- Failure cases: {len(failures)}
- Upstream source: `{SOURCE_SLICE_ID}`

## Usage

```powershell
python -B artifact\\classify_user_response_dry_run.py --text "B"
```

`--rebuild` is Builder-only. Ordinary agents should run the verifier, not
rewrite the artifact.
"""


def prototype(contract: dict) -> str:
    cards = "\n".join(
        f"""
        <section class=\"case\">
          <h2>{item['case_id']}</h2>
          <p><strong>Result:</strong> {item['result']}</p>
          <p><strong>Safe next:</strong> {item['safe_next_step']}</p>
          <p><strong>Auto execution:</strong> {str(item['automatic_execution']).lower()}</p>
          <p><strong>New scope:</strong> {str(item['requires_new_scope']).lower()}</p>
          <p><strong>Separate approval:</strong> {str(item['requires_separate_user_approval']).lower()}</p>
        </section>
        """
        for item in contract["response_policy"]
    )
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <title>{SLICE_ID}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #172033; background: #f7fafc; }}
    main {{ max-width: 1040px; margin: 0 auto; }}
    h1 {{ font-size: 28px; margin-bottom: 8px; }}
    .summary {{ border-left: 4px solid #0f766e; padding: 12px 16px; background: #ecfdf5; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; margin-top: 20px; }}
    .case {{ border: 1px solid #cbd5e1; border-radius: 8px; padding: 14px; background: white; }}
    h2 {{ font-size: 16px; margin: 0 0 8px; }}
    p {{ margin: 6px 0; }}
  </style>
</head>
<body>
  <main>
    <h1>User Response Classifier Dry Run</h1>
    <div class=\"summary\">
      <p>Classifies a reply, names a safe next step, and never executes an option.</p>
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

    contract = classifier_contract()
    fixtures = fixture_payloads()
    failures = failure_cases()

    write_json(ARTIFACT / "user_response_classifier_contract.json", contract)
    write_text(ARTIFACT / "user_response_classifier_readout.md", readout(contract, fixtures, failures))
    write_text(ARTIFACT / "user_response_classifier_prototype.html", prototype(contract))
    for filename, payload in fixtures.items():
        write_json(FIXTURES / filename, payload)
    write_json(FAILURE_CASES / "user_response_classifier_failure_cases.json", failures)
    for filename, text in markdown_files(contract, failures).items():
        write_text(ROOT / filename, text)


if __name__ == "__main__":
    main()
