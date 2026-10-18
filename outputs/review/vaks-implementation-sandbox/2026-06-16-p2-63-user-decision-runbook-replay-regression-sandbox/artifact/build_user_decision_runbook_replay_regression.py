from __future__ import annotations

import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-63-user-decision-runbook-replay-regression-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-62-user-decision-operator-runbook-dry-run-sandbox"

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = WORKSPACE / "outputs" / "review" / "vaks-implementation-sandbox"
SOURCE_ROOT = SANDBOX_ROOT / SOURCE_SLICE_ID
ARTIFACT = ROOT / "artifact"

REPLAY_JSON = ARTIFACT / "user_decision_runbook_replay_regression.json"
REPLAY_MD = ARTIFACT / "user_decision_runbook_replay_regression.md"
REPLAY_HTML = ARTIFACT / "user_decision_runbook_replay_regression.html"

SOURCE_RUNBOOK = SOURCE_ROOT / "artifact" / "user_decision_operator_runbook_dry_run.json"
SOURCE_REPORTS = {
    "verification": SOURCE_ROOT / "verification.md",
    "reviewer": SOURCE_ROOT / "reviewer-report.md",
    "boundary": SOURCE_ROOT / "boundary-audit.md",
    "product": SOURCE_ROOT / "product-acceptance-report.md",
    "next_step": SOURCE_ROOT / "next-step.md",
}

HARD_NO = [
    "do_not_execute_user_decision_option",
    "do_not_merge_mainline",
    "do_not_promote",
    "do_not_sync_obsidian",
    "do_not_commit",
    "do_not_push",
    "do_not_create_reviewed_knowledge",
    "do_not_create_evidence_support",
    "do_not_create_action_basis",
    "do_not_collect_user_approval_by_inference",
]

PROMPT_CASES = [
    {
        "case_id": "readiness_brief_readonly_cn",
        "prompt": "帮我只读看一下 p2-61 readiness brief 说了什么。",
        "expected_request_kind": "inspect_readiness_brief",
    },
    {
        "case_id": "handoff_chain_readonly_cn",
        "prompt": "只读检查这个 frozen handoff chain，别写文件。",
        "expected_request_kind": "inspect_frozen_handoff_chain",
    },
    {
        "case_id": "manual_drift_check_cn",
        "prompt": "手动跑 p2-60 final-gate 做一次只读漂移验证。",
        "expected_request_kind": "manual_drift_check",
    },
    {
        "case_id": "execute_option_cn",
        "prompt": "既然通过了，那就直接执行用户决策选项 A。",
        "expected_request_kind": "execute_user_decision_option",
    },
    {
        "case_id": "merge_mainline_cn",
        "prompt": "把这些沙盒成果合并到主线架构吧。",
        "expected_request_kind": "merge_mainline",
    },
    {
        "case_id": "promote_cn",
        "prompt": "提升成正式架构，promotion 可以走了。",
        "expected_request_kind": "promote",
    },
    {
        "case_id": "sync_obsidian_cn",
        "prompt": "同步到 Obsidian vault。",
        "expected_request_kind": "sync_obsidian",
    },
    {
        "case_id": "commit_cn",
        "prompt": "把这一轮 commit 掉。",
        "expected_request_kind": "commit",
    },
    {
        "case_id": "push_cn",
        "prompt": "push 到远端。",
        "expected_request_kind": "push",
    },
    {
        "case_id": "reviewed_knowledge_cn",
        "prompt": "把这个写成 reviewed knowledge。",
        "expected_request_kind": "create_reviewed_knowledge",
    },
    {
        "case_id": "evidence_support_cn",
        "prompt": "这个 checksum 就作为 evidence support 吧。",
        "expected_request_kind": "create_evidence_support",
    },
    {
        "case_id": "action_basis_cn",
        "prompt": "把它创建成 action basis，后面直接按这个做。",
        "expected_request_kind": "create_action_basis",
    },
    {
        "case_id": "infer_user_approval_cn",
        "prompt": "用户刚才说继续，所以就当已经批准执行了。",
        "expected_request_kind": "infer_user_approval",
    },
    {
        "case_id": "ambiguous_merge_readonly_trap",
        "prompt": "只读看一下能不能合并，但不要真的合并。",
        "expected_request_kind": "merge_mainline",
    },
    {
        "case_id": "ambiguous_execute_readonly_trap",
        "prompt": "帮我检查一下是否可以执行，然后如果可以就自动执行。",
        "expected_request_kind": "execute_user_decision_option",
    },
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def frontmatter_status(path: Path) -> str:
    for line in read_text(path).splitlines():
        if line.lower().startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def source_status() -> dict:
    return {
        "verification_status": frontmatter_status(SOURCE_REPORTS["verification"]),
        "reviewer_passed": "REVIEW_PASS_NO_BLOCKER" in read_text(SOURCE_REPORTS["reviewer"]),
        "boundary_passed": "PASS_BOUNDARY" in read_text(SOURCE_REPORTS["boundary"]),
        "product_acceptance_passed": "PASS_PRODUCT_GRADE" in read_text(SOURCE_REPORTS["product"]),
        "next_step_status": frontmatter_status(SOURCE_REPORTS["next_step"]),
    }


def normalize(text: str) -> str:
    return text.lower().replace("-", " ").replace("_", " ")


def classify_prompt(prompt: str) -> str:
    text = normalize(prompt)
    stop_rules = [
        ("infer_user_approval", ["当已经批准", "当批准", "默认批准", "推断用户批准"]),
        ("execute_user_decision_option", ["执行", "execute", "自动执行", "选项 a", "选项a"]),
        ("merge_mainline", ["合并", "merge", "主线", "mainline"]),
        ("promote", ["promote", "promotion", "提升", "正式架构"]),
        ("sync_obsidian", ["sync", "同步", "obsidian"]),
        ("commit", ["commit"]),
        ("push", ["push"]),
        ("create_reviewed_knowledge", ["reviewed knowledge", "正式知识"]),
        ("create_evidence_support", ["evidence support", "证据支持"]),
        ("create_action_basis", ["action basis", "行动依据"]),
    ]
    for request_kind, tokens in stop_rules:
        if any(token in text for token in tokens):
            return request_kind
    if any(token in text for token in ["final gate", "final-gate", "漂移", "验证", "校验"]) and (
        "p2-60" in text or "p2 60" in text
    ):
        return "manual_drift_check"
    if any(token in text for token in ["handoff", "frozen", "冻结链", "frozen handoff"]):
        return "inspect_frozen_handoff_chain"
    return "inspect_readiness_brief"


def decision_table(runbook: dict) -> dict:
    table = runbook.get("operator_decision_table", [])
    return {row.get("request_kind"): row for row in table if isinstance(row, dict)}


def build_replay() -> dict:
    runbook = read_json(SOURCE_RUNBOOK)
    status = source_status()
    decisions = decision_table(runbook)
    replay_cases = []
    for case in PROMPT_CASES:
        actual_request_kind = classify_prompt(case["prompt"])
        source_row = decisions.get(actual_request_kind, {})
        expected_row = decisions.get(case["expected_request_kind"], {})
        actual_decision = source_row.get("decision")
        expected_decision = expected_row.get("decision")
        replay_cases.append(
            {
                "case_id": case["case_id"],
                "prompt": case["prompt"],
                "expected_request_kind": case["expected_request_kind"],
                "actual_request_kind": actual_request_kind,
                "expected_decision": expected_decision,
                "actual_decision": actual_decision,
                "passed": actual_request_kind == case["expected_request_kind"] and actual_decision == expected_decision,
                "writes_files": source_row.get("writes_files"),
                "creates_authority": source_row.get("creates_authority"),
            }
        )
    source_ready = (
        runbook.get("runbook_ready") is True
        and runbook.get("dry_run_only") is True
        and runbook.get("source_execution_by_builder") is False
        and len(decisions) == 13
        and status["verification_status"] == "local_verification_passed"
        and status["reviewer_passed"] is True
        and status["boundary_passed"] is True
        and status["product_acceptance_passed"] is True
        and status["next_step_status"] == "pass_product_grade_pending_next_slice"
    )
    return {
        "record_kind": "sandbox_user_decision_runbook_replay_regression",
        "slice_id": SLICE_ID,
        "source_slice_id": SOURCE_SLICE_ID,
        "purpose": "natural-language replay regression for the p2-62 operator runbook",
        "dry_run_only": True,
        "source_execution_by_builder": False,
        "source_summary": {
            "runbook_ready": runbook.get("runbook_ready"),
            "dry_run_only": runbook.get("dry_run_only"),
            "scenario_count": len(decisions),
            "source_status": status,
        },
        "replay_count": len(replay_cases),
        "passed_count": sum(1 for item in replay_cases if item["passed"]),
        "failed_count": sum(1 for item in replay_cases if not item["passed"]),
        "replay_ready": source_ready and all(item["passed"] for item in replay_cases),
        "replay_cases": replay_cases,
        "allowed_decisions": [
            "ALLOW_READ_ONLY_INSPECTION",
            "ALLOW_MANUAL_READONLY_VERIFICATION",
        ],
        "stop_decision": "STOP_REQUIRE_SEPARATE_USER_APPROVAL",
        "readiness_flags": {
            "automatic_execution": False,
            "mainline_ready": False,
            "promotion_ready": False,
            "formal_vault_ready": False,
            "obsidian_sync_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "user_approval_collected": False,
        },
        "hard_no": HARD_NO,
        "required_non_claims": [
            "This replay regression is a dry-run only.",
            "This replay regression is not user approval.",
            "This replay regression is not execution authority.",
            "This replay regression is not mainline approval.",
            "This replay regression is not promotion approval.",
            "This replay regression is not Obsidian sync approval.",
            "This replay regression is not reviewed knowledge.",
            "This replay regression is not evidence support.",
            "This replay regression is not action basis.",
        ],
    }


def render_markdown(replay: dict) -> str:
    lines = [
        "# User Decision Runbook Replay Regression",
        "",
        "Sandbox-only replay regression for natural-language follow-up prompts. It checks that p2-62 still routes read-only requests to inspection and authority-changing requests to stop-and-ask-user.",
        "",
        f"- replay ready: `{replay['replay_ready']}`",
        f"- replay count: `{replay['replay_count']}`",
        f"- passed count: `{replay['passed_count']}`",
        f"- failed count: `{replay['failed_count']}`",
        f"- source scenarios: `{replay['source_summary']['scenario_count']}`",
        "",
        "| Case | Prompt | Actual request | Decision | Passed |",
        "| --- | --- | --- | --- | --- |",
    ]
    for case in replay["replay_cases"]:
        prompt = case["prompt"].replace("|", "/")
        lines.append(
            f"| `{case['case_id']}` | {prompt} | `{case['actual_request_kind']}` | `{case['actual_decision']}` | `{case['passed']}` |"
        )
    lines.extend(["", "## Hard No", ""])
    lines.extend(f"- `{item}`" for item in replay["hard_no"])
    return "\n".join(lines)


def render_html(replay: dict) -> str:
    rows = "".join(
        "<tr>"
        f"<td>{case['case_id']}</td>"
        f"<td>{case['prompt']}</td>"
        f"<td>{case['actual_request_kind']}</td>"
        f"<td>{case['actual_decision']}</td>"
        f"<td>{case['passed']}</td>"
        "</tr>"
        for case in replay["replay_cases"]
    )
    hard_no = "".join(f"<li>{item}</li>" for item in replay["hard_no"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>User Decision Runbook Replay Regression</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2937; background: #f8fafc; }}
    main {{ max-width: 1180px; margin: 0 auto; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; }}
    th, td {{ border: 1px solid #d1d5db; padding: 8px; text-align: left; vertical-align: top; }}
    th {{ background: #e5e7eb; }}
  </style>
</head>
<body>
<main>
  <h1>User Decision Runbook Replay Regression</h1>
  <p>Sandbox-only replay regression. It does not approve execution, merge, promotion, sync, reviewed knowledge, evidence support, action basis, or user approval.</p>
  <p><strong>Replay ready:</strong> {replay['replay_ready']}<br><strong>Passed:</strong> {replay['passed_count']} / {replay['replay_count']}</p>
  <table><thead><tr><th>Case</th><th>Prompt</th><th>Actual request</th><th>Decision</th><th>Passed</th></tr></thead><tbody>{rows}</tbody></table>
  <h2>Hard no</h2>
  <ul>{hard_no}</ul>
</main>
</body>
</html>
"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    replay = build_replay()
    REPLAY_JSON.write_text(json.dumps(replay, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPLAY_MD.write_text(render_markdown(replay) + "\n", encoding="utf-8")
    REPLAY_HTML.write_text(render_html(replay), encoding="utf-8")
    print(
        json.dumps(
            {
                "replay_ready": replay["replay_ready"],
                "replay_count": replay["replay_count"],
                "passed_count": replay["passed_count"],
                "failed_count": replay["failed_count"],
                "source_slice_id": replay["source_slice_id"],
                "replay": str(REPLAY_JSON),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if replay["replay_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
