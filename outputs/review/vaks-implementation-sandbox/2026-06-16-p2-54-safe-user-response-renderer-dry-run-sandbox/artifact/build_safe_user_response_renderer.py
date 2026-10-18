from __future__ import annotations

import json
from pathlib import Path


SLICE_ID = "2026-06-16-p2-54-safe-user-response-renderer-dry-run-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-53-user-response-classifier-dry-run-sandbox"
ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"


RENDER_POLICY = [
    {
        "case_id": "no_reply",
        "reply_id": "keep_reference_no_action",
        "reply": "当前没有收到新的选择。我会保持 sandbox 作为参考，不执行任何选项，也不会合并、同步、提交、推送或写入正式层。",
        "next_step": "wait_or_report_reference_only",
    },
    {
        "case_id": "explicit_A",
        "reply_id": "acknowledge_reference_only",
        "reply": "收到，按 A 处理：只保留 sandbox 作为参考。我不会合并、promotion、sync、commit、push，也不会写入 reviewed knowledge、evidence support 或 action basis。",
        "next_step": "no_action_reference_only",
    },
    {
        "case_id": "explicit_B",
        "reply_id": "ask_readonly_planning_scope",
        "reply": "收到 B 的方向。下一步只能先确认单独的只读规划范围；在你明确范围前，我不会启动新 slice，也不会合并、同步、提交、推送或 promotion。",
        "next_step": "ask_for_separate_read_only_scope",
    },
    {
        "case_id": "explicit_C",
        "reply_id": "ask_mainline_review_scope",
        "reply": "收到 C 的方向。需要你单独批准主线评审范围和允许路径；在此之前我不会改主线、合并、同步、提交、推送或写入正式层。",
        "next_step": "ask_for_allowed_paths_and_scope",
    },
    {
        "case_id": "explicit_D",
        "reply_id": "acknowledge_park_or_reject",
        "reply": "收到 D。我会把 sandbox 链按搁置或拒绝理解，但不会改主线、不会删除既有产物，也不会同步、提交或推送。",
        "next_step": "acknowledge_no_mutation",
    },
    {
        "case_id": "ambiguous_reply",
        "reply_id": "ask_one_clarification",
        "reply": "这句话还不能确定是 A、B、C 还是 D。我先停下，不执行任何选项。请只回复一个选项：A、B、C 或 D。",
        "next_step": "ask_one_short_clarification",
    },
    {
        "case_id": "multiple_options",
        "reply_id": "ask_choose_one",
        "reply": "你同时提到了多个选项。我先停下，不执行任何选项。请只选择一个：A、B、C 或 D。",
        "next_step": "ask_user_to_choose_one_option",
    },
    {
        "case_id": "approval_with_execution_words",
        "reply_id": "stop_for_separate_scope",
        "reply": "这条回复包含执行、合并、同步、提交、推送或写入正式层的语义。我现在停止，不执行。若要越过 sandbox 边界，需要你单独给出明确范围和允许路径。",
        "next_step": "stop_and_ask_for_separate_explicit_scope",
    },
    {
        "case_id": "unknown_case_fallback",
        "reply_id": "stop_for_unknown_classifier_case",
        "reply": "分类结果不在已知安全集合内。我现在停止，不执行任何选项。请重新明确选择 A、B、C 或 D，或单独给出明确范围。",
        "next_step": "stop_and_ask_for_clarification",
    },
]


def policy_by_case() -> dict[str, dict]:
    return {item["case_id"]: item for item in RENDER_POLICY}


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def contract() -> dict:
    return {
        "record_kind": "sandbox_safe_user_response_renderer_contract",
        "slice_id": SLICE_ID,
        "source_slice_id": SOURCE_SLICE_ID,
        "truth_boundary": "dry_run_renderer_not_user_decision_or_execution_authority",
        "status": "built_pending_review",
        "purpose": "render safe user-facing replies from p2-53 classifier output without executing any option",
        "source_final_gate_command": (
            "python -B .\\outputs\\review\\vaks-implementation-sandbox\\"
            f"{SOURCE_SLICE_ID}\\artifact\\verify_user_response_classifier_dry_run.py --final-gate"
        ),
        "render_policy": RENDER_POLICY,
        "output_contract": {
            "input_text": "original user text",
            "classifier_case_id": "case from p2-53 classifier",
            "reply_id": "stable renderer reply id",
            "reply": "Chinese safe response text",
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
                "start_future_slice_by_inference",
            ],
        },
        "reply_safety_rules": {
            "required_boundary_terms": ["不会", "不执行"],
            "dangerous_positive_phrases": [
                "我会开始",
                "我将开始",
                "开始执行",
                "正在执行",
                "我会合并",
                "正在合并",
                "已合并",
                "我会提交",
                "已提交",
                "我会推送",
                "已推送",
                "我会同步",
                "已同步",
                "我会写入",
                "已写入",
                "我会 promotion",
                "我会 promote",
            ],
        },
        "ordinary_agent_usage": {
            "render_example": "python -B artifact/render_safe_user_response.py --text \"B\"",
            "default_verifier": "python -B artifact/verify_safe_user_response_renderer.py",
            "upstream_verifier": "python -B artifact/verify_safe_user_response_renderer.py --run-upstream",
            "final_gate": "python -B artifact/verify_safe_user_response_renderer.py --final-gate",
            "rebuild": "Builder-only: python -B artifact/build_safe_user_response_renderer.py",
        },
        "required_non_claims": [
            "The renderer is not a user decision.",
            "The renderer is not execution authority.",
            "The renderer cannot approve merge, promotion, sync, commit, push, reviewed knowledge, evidence support, or action basis.",
            "Replies may explain forbidden operations only in negative, non-executing language.",
            "B and C replies ask for separate scope; they do not start work.",
            "Unknown classifier cases must stop safely instead of raising errors.",
        ],
    }


def fixtures() -> dict[str, dict]:
    examples = {
        "no_reply.json": ("", "no_reply"),
        "option_a.json": ("A", "explicit_A"),
        "option_b.json": ("B", "explicit_B"),
        "option_c.json": ("C", "explicit_C"),
        "option_d.json": ("D", "explicit_D"),
        "ambiguous_continue.json": ("继续", "ambiguous_reply"),
        "multiple_b_c.json": ("B 和 C 都行", "multiple_options"),
        "execution_c_merge.json": ("C，合并主线", "approval_with_execution_words"),
        "safe_c_scope.json": ("选择C，问我主线评审范围", "explicit_C"),
        "english_merge_review.json": ("merge review", "approval_with_execution_words"),
        "unknown_case_fallback_contract.json": ("__synthetic_unknown_case__", "unknown_case_fallback"),
    }
    policy = policy_by_case()
    payloads = {}
    for filename, (input_text, case_id) in examples.items():
        item = policy[case_id]
        payloads[filename] = {
            "input_text": input_text,
            "expected_case_id": case_id,
            "expected_reply_id": item["reply_id"],
            "expected_next_step": item["next_step"],
            "automatic_execution": False,
            "must_contain_any": ["不会", "不执行"],
            "must_not_contain_positive_execution": True,
        }
    return payloads


def failure_cases() -> list[dict]:
    cases = [
        ("missing_boundary_language", "B", "reply lacks negative boundary language"),
        ("positive_start_language", "B", "reply says it will start work"),
        ("positive_merge_language", "C", "reply says it will merge"),
        ("positive_commit_language", "A", "reply says it will commit"),
        ("positive_push_language", "C", "reply says it will push"),
        ("positive_sync_language", "B", "reply says it will sync"),
        ("positive_write_language", "C", "reply says it will write formal layers"),
        ("b_missing_scope_request", "B", "B reply does not ask for separate scope"),
        ("c_missing_allowed_paths", "C", "C reply does not ask for allowed paths"),
        ("ambiguous_executes", "继续", "ambiguous reply executes instead of clarifying"),
        ("multiple_executes", "B 和 C 都行", "multiple options execute instead of clarifying"),
        ("execution_words_not_stopped", "C，合并主线", "execution-word reply is not stopped"),
        ("renderer_claims_user_decision", "A", "renderer claims final user decision authority"),
        ("renderer_claims_product_approval", "B", "renderer claims Product PASS authorizes execution"),
        ("renderer_missing_must_not", "D", "renderer output lacks must_not boundaries"),
        ("source_p2_53_not_checked", "B", "upstream p2-53 final gate is not checked"),
        ("unknown_classifier_case_raises", "__synthetic_unknown_case__", "unknown classifier case raises instead of stopping safely"),
    ]
    policy = policy_by_case()
    return [
        {
            "failure_id": failure_id,
            "input_text": input_text,
            "expected_case_id": expected_case_for_input(input_text),
            "description": description,
            "unsafe_reply": unsafe_reply_for(failure_id),
            "must_reject_if_reply_contains_positive_execution": True,
            "must_require_boundary_language": True,
            "must_not": contract()["output_contract"]["must_not"],
        }
        for failure_id, input_text, description in cases
    ]


def unsafe_reply_for(failure_id: str) -> str:
    if "missing_boundary" in failure_id:
        return "收到，我明白这个选择。"
    if "merge" in failure_id:
        return "收到，我会合并主线。"
    if "commit" in failure_id:
        return "收到，我会提交这些文件。"
    if "push" in failure_id:
        return "收到，我会推送。"
    if "sync" in failure_id:
        return "收到，我会同步到 Obsidian。"
    if "write" in failure_id:
        return "收到，我会写入正式层。"
    if "b_missing_scope" in failure_id:
        return "收到 B，我会开始下一步。"
    if "c_missing_allowed_paths" in failure_id:
        return "收到 C，我会准备合并。"
    if "ambiguous" in failure_id or "multiple" in failure_id:
        return "收到，我会开始执行。"
    if "claims_user_decision" in failure_id:
        return "这已经是正式用户决定，我会执行。"
    if "claims_product_approval" in failure_id:
        return "Product PASS 已授权执行，我会开始。"
    return "收到，我会开始执行。"


def expected_case_for_input(input_text: str) -> str:
    lowered = input_text.lower()
    if input_text == "__synthetic_unknown_case__":
        return "unknown_case_fallback"
    if "合并" in input_text or "merge" in lowered:
        return "approval_with_execution_words"
    if input_text == "继续":
        return "ambiguous_reply"
    if "和" in input_text or " or " in lowered or "/" in lowered:
        return "multiple_options"
    if lowered.strip() == "a":
        return "explicit_A"
    if lowered.strip() == "b":
        return "explicit_B"
    if lowered.strip() == "c":
        return "explicit_C"
    if lowered.strip() == "d":
        return "explicit_D"
    return "ambiguous_reply"


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

Render safe Chinese user-facing replies from p2-53 classifier output without
executing any option.

## In Scope

- Map each p2-53 classification case to a stable reply id and safe reply text.
- Verify reply text avoids positive execution language.
- Verify B/C replies ask for separate scope instead of starting work.
- Run p2-53 final gate as the upstream dependency.

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

- `outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/artifact/classify_user_response_dry_run.py`
- `outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/product-acceptance-report.md`
- `outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/artifact/verify_user_response_classifier_dry_run.py`

## Upstream Gate

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SOURCE_SLICE_ID}\\artifact\\verify_user_response_classifier_dry_run.py --final-gate
```

## Interpretation

p2-54 renders a safe reply after classification. It is not a user decision,
execution authority, promotion, merge, sync, reviewed knowledge, evidence
support, or action basis.
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
python -B artifact\\verify_safe_user_response_renderer.py
python -B artifact\\verify_safe_user_response_renderer.py --run-upstream
python -B artifact\\verify_safe_user_response_renderer.py --final-gate
```

`--rebuild` is Builder-only:

```powershell
python -B artifact\\build_safe_user_response_renderer.py
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

If this slice receives `PASS_PRODUCT_GRADE`, later agents may use the renderer
to draft safe user-facing replies, but must not execute any option by inference.
""",
    }


def readout(data: dict) -> str:
    rows = "\n".join(
        f"| `{item['case_id']}` | `{item['reply_id']}` | {item['reply']} | `{item['next_step']}` |"
        for item in data["render_policy"]
    )
    return f"""
---
record_kind: sandbox_artifact_readout
slice_id: {SLICE_ID}
status: built_pending_review
---

# Safe User Response Renderer Readout

| Case | Reply ID | Reply | Next Step |
| --- | --- | --- | --- |
{rows}

The renderer is dry-run only. It drafts safe wording and never executes an
option.
"""


def prototype(data: dict) -> str:
    cards = "\n".join(
        f"""
        <section class=\"case\">
          <h2>{item['case_id']}</h2>
          <p><strong>{item['reply_id']}</strong></p>
          <p>{item['reply']}</p>
          <p><strong>Next:</strong> {item['next_step']}</p>
        </section>
        """
        for item in data["render_policy"]
    )
    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\">
  <title>{SLICE_ID}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #172033; background: #f8fafc; }}
    main {{ max-width: 1040px; margin: 0 auto; }}
    h1 {{ font-size: 28px; }}
    .summary {{ border-left: 4px solid #2563eb; padding: 12px 16px; background: #eff6ff; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; margin-top: 20px; }}
    .case {{ border: 1px solid #cbd5e1; border-radius: 8px; padding: 14px; background: white; }}
    h2 {{ font-size: 16px; margin: 0 0 8px; }}
  </style>
</head>
<body>
  <main>
    <h1>Safe User Response Renderer</h1>
    <div class=\"summary\">Dry-run replies only. No option execution.</div>
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
    write_json(ARTIFACT / "safe_user_response_renderer_contract.json", data)
    write_text(ARTIFACT / "safe_user_response_renderer_readout.md", readout(data))
    write_text(ARTIFACT / "safe_user_response_renderer_prototype.html", prototype(data))
    for filename, payload in fixtures().items():
        write_json(FIXTURES / filename, payload)
    write_json(FAILURE_CASES / "safe_user_response_renderer_failure_cases.json", failure_cases())
    for filename, text in markdown_files().items():
        write_text(ROOT / filename, text)


if __name__ == "__main__":
    main()
