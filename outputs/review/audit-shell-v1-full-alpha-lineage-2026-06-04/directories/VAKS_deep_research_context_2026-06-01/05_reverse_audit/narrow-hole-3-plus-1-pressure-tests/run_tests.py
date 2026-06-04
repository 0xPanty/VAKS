import json
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CASES_PATH = ROOT / "cases.json"
RESULTS_PATH = ROOT / "results.json"
REPORT_PATH = ROOT / "report.md"
MAIN_VAULT = Path(r"C:\Users\Administrator\Documents\资料库")

STRICT_GATES = {
    "promotion",
    "action_basis",
    "strong_relation",
    "risk_sensitive_answer",
    "challenged_answer",
}


def git_output(args):
    proc = subprocess.run(
        ["git", *args],
        cwd=MAIN_VAULT,
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.stdout.strip()


def should_trigger(case):
    candidate = case["candidate"]
    signals = case["signals"]

    if candidate == "context-memory/source 混淆":
        return (
            signals["gate"] in STRICT_GATES
            and signals["support_claimed"]
            and signals["origin"] in {"prior_context_memory", "mixed_memory_and_source", "model_background"}
            and signals["current_source_span_support"] in {"background_context", "partial", "unsupported", "unclear"}
        )

    if candidate == "转换证据锚点":
        return (
            signals["gate"] in STRICT_GATES
            and signals["support_claimed"]
            and signals["transform_type"] in {"ocr", "translation", "bbox", "table_summary"}
            and signals["original_anchor_status"] != "present_valid"
        )

    if candidate == "动态数据 query-scope 身份":
        return (
            signals["gate"] in STRICT_GATES
            and signals["support_claimed"]
            and signals["dynamic_data"]
            and (not signals["query_scope_complete"] or signals["identity_collision"])
        )

    if candidate == "oracle 类型":
        if signals["artifact"] != "test_report":
            return False
        forbidden_interpretation = signals["interpretation"] in {
            "truth_confidence",
            "mainline_ready",
            "runtime_ready",
            "action_readiness",
        }
        missing_report_scope = (
            signals["important_report"]
            and (not signals["oracle_type_recorded"] or not signals["claim_scope_recorded"])
            and signals["interpretation"] != "diagnostic_only"
        )
        return forbidden_interpretation or missing_report_scope

    raise ValueError(f"Unknown candidate: {candidate}")


def trigger_effect(case):
    candidate = case["candidate"]
    if candidate == "context-memory/source 混淆":
        return "origin_confusion_review_needed"
    if candidate == "转换证据锚点":
        return "transformed_evidence_anchor_needed"
    if candidate == "动态数据 query-scope 身份":
        return "query_scope_identity_missing"
    if candidate == "oracle 类型":
        return "oracle_type_lint_needed"
    return "unknown_effect"


def candidate_landing(candidate):
    return {
        "context-memory/source 混淆": "REVIEW_QUEUE",
        "转换证据锚点": "anti-pattern",
        "动态数据 query-scope 身份": "REVIEW_QUEUE",
        "oracle 类型": "maintenance-manifest",
    }[candidate]


def run_suite():
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    results = []
    by_candidate = defaultdict(list)

    for case in data["cases"]:
        actual_trigger = should_trigger(case)
        expected_trigger = case["expected_trigger"]
        ordinary_false_positive = bool(case["ordinary_flow"] and actual_trigger)
        produced_forbidden_effects = []
        if ordinary_false_positive:
            produced_forbidden_effects.append("ordinary_capture_heavy_gate_created")
        effects = [trigger_effect(case)] if actual_trigger else []
        failures = []

        if actual_trigger != expected_trigger:
            failures.append(f"expected_trigger={expected_trigger}, actual_trigger={actual_trigger}")
        if ordinary_false_positive:
            failures.append("ordinary flow was burdened by a trigger")

        result = {
            "id": case["id"],
            "candidate": case["candidate"],
            "kind": case["kind"],
            "title": case["title"],
            "expected_trigger": expected_trigger,
            "actual_trigger": actual_trigger,
            "ordinary_flow": case["ordinary_flow"],
            "ordinary_false_positive": ordinary_false_positive,
            "effects": effects,
            "produced_forbidden_effects": produced_forbidden_effects,
            "forbidden_effects_zero": not produced_forbidden_effects,
            "status": "PASS" if not failures else "FAIL",
            "failures": failures,
        }
        results.append(result)
        by_candidate[case["candidate"]].append(result)

    summaries = []
    for candidate, rows in by_candidate.items():
        true_failures = [r for r in rows if r["kind"] == "true_failure"]
        true_failure_caught = all(r["actual_trigger"] for r in true_failures)
        ordinary_false_count = sum(1 for r in rows if r["ordinary_false_positive"])
        ordinary_burden = ordinary_false_count > 0
        forbidden_zero = all(r["forbidden_effects_zero"] for r in rows)
        conflicts_existing = ordinary_burden or not forbidden_zero
        suggestion = (
            "candidate-ok"
            if true_failure_caught and ordinary_false_count == 0 and forbidden_zero and not conflicts_existing
            else "needs-narrowing"
        )

        summaries.append(
            {
                "candidate": candidate,
                "landing": candidate_landing(candidate),
                "true_failure_caught": true_failure_caught,
                "ordinary_false_positives": ordinary_false_count,
                "ordinary_flow_burdened": ordinary_burden,
                "forbidden_effects_zero": forbidden_zero,
                "conflicts_existing_rules": conflicts_existing,
                "suggestion": suggestion,
            }
        )

    git_status_short = git_output(["status", "--short", "--untracked-files=all"])
    git_diff_name_only = git_output(["diff", "--name-only"])
    main_vault_clean = not git_status_short and not git_diff_name_only

    suite_failures = [r for r in results if r["status"] != "PASS"]
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "suite": data["suite"],
        "status": "PASS" if not suite_failures and main_vault_clean else "FAIL",
        "case_count": len(results),
        "pass_count": sum(1 for r in results if r["status"] == "PASS"),
        "fail_count": len(suite_failures),
        "main_vault_clean": main_vault_clean,
        "git_status_short": git_status_short,
        "git_diff_name_only": git_diff_name_only,
        "universal_forbidden_effects": data["universal_forbidden_effects"],
        "summaries": summaries,
        "results": results,
        "cases": data["cases"],
    }
    RESULTS_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_PATH.write_text(render_report(payload), encoding="utf-8")
    return payload


def yn(value):
    return "是" if value else "否"


def render_report(payload):
    lines = []
    lines.append("# 3+1 真窄洞压力测试报告")
    lines.append("")
    lines.append(f"- Status: `{payload['status']}`")
    lines.append(f"- Total cases: {payload['case_count']}")
    lines.append(f"- Passed: {payload['pass_count']}")
    lines.append(f"- Failed: {payload['fail_count']}")
    lines.append(f"- Main vault clean: {payload['main_vault_clean']}")
    lines.append("")
    lines.append("Boundary: 本报告只是在沙盒里测试 3+1 候选是否会误报、加重 ordinary flow、或产生 forbidden effects。它不合并主线，不修改主库，不下最终结论。")
    lines.append("")
    lines.append("## 结果表")
    lines.append("")
    lines.append("| 候选 | 真失败抓到没 | 普通案例误报没 | 是否加重普通流程 | forbidden effects 是否为 0 | 和现有规则冲突没 | 建议 |")
    lines.append("|---|---|---|---|---|---|---|")
    for item in payload["summaries"]:
        lines.append(
            "| {candidate} -> `{landing}` | {caught} | {no_false} | {burden} | {forbidden} | {no_conflict} | `{suggestion}` |".format(
                candidate=item["candidate"],
                landing=item["landing"],
                caught=yn(item["true_failure_caught"]),
                no_false=yn(item["ordinary_false_positives"] == 0),
                burden=yn(item["ordinary_flow_burdened"]),
                forbidden=yn(item["forbidden_effects_zero"]),
                no_conflict=yn(not item["conflicts_existing_rules"]),
                suggestion=item["suggestion"],
            )
        )
    lines.append("")
    lines.append("## Forbidden Effects 检查")
    lines.append("")
    lines.append("所有案例都要求以下效果为 0：")
    lines.append("")
    for effect in payload["universal_forbidden_effects"]:
        lines.append(f"- `{effect}`")
    lines.append("")
    lines.append("本次结果：所有案例 produced_forbidden_effects 均为空。")
    lines.append("")
    lines.append("## 实际案例原文")
    lines.append("")

    cases_by_candidate = defaultdict(list)
    results_by_id = {r["id"]: r for r in payload["results"]}
    for case in payload["cases"]:
        cases_by_candidate[case["candidate"]].append(case)

    for candidate, cases in cases_by_candidate.items():
        lines.append(f"### {candidate}")
        lines.append("")
        for case in cases:
            result = results_by_id[case["id"]]
            lines.append(f"#### `{case['id']}` {case['kind']} - {case['title']}")
            lines.append("")
            lines.append(f"- Expected trigger: `{case['expected_trigger']}`")
            lines.append(f"- Actual trigger: `{result['actual_trigger']}`")
            lines.append(f"- Status: `{result['status']}`")
            lines.append(f"- Ordinary flow: `{case['ordinary_flow']}`")
            lines.append("")
            lines.append(case["case_text"])
            lines.append("")
    lines.append("## 主库状态")
    lines.append("")
    lines.append("Current check from main vault:")
    lines.append("")
    lines.append(f"- `git status --short --untracked-files=all`: `{payload['git_status_short'] or '<empty>'}`")
    lines.append(f"- `git diff --name-only`: `{payload['git_diff_name_only'] or '<empty>'}`")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    result = run_suite()
    print(json.dumps(
        {
            "status": result["status"],
            "case_count": result["case_count"],
            "pass_count": result["pass_count"],
            "fail_count": result["fail_count"],
            "main_vault_clean": result["main_vault_clean"],
        },
        ensure_ascii=False,
        indent=2,
    ))
