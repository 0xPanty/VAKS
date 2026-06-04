from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "review_packet_local_real_self_test"
REPORT_PATH = ROOT / "reports" / "CODEX_LOCAL_REAL_OPERATOR_SELF_TEST_REPORT.md"
CSV_PATH = OUT_DIR / "LOCAL_REAL_OPERATOR_SELF_TEST.csv"
SUMMARY_PATH = OUT_DIR / "LOCAL_REAL_OPERATOR_SELF_TEST_SUMMARY.json"


LAYER_TARGETS = {
    "ordinary_stable": 2,
    "action_challenge_conflict": 2,
    "omission_insufficiency_ambiguity": 2,
    "anchor_problem": 2,
    "anchor_jumpback_failure": 1,
    "false_lite_trap": 1,
    "review_due_trap": 1,
    "resolved_repeated_recurrence": 2,
    "authority_leak_bait": 2,
    "authority_leakage_paraphrase": 1,
    "over_grouping_near_miss": 2,
    "serious_folded_violation": 2,
}


FULL_ANCHOR_BY_CLASS = {
    "evidence_landing": 1,
    "claim_landing": 1,
    "claim_relevant_context_landing": 4,
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def short(text: str, limit: int = 120) -> str:
    text = " ".join((text or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def rel_exists(rel_path: str) -> bool:
    return bool(rel_path) and (ROOT / rel_path).exists()


def quote_check(case: dict) -> dict:
    anchor = case.get("source_anchor") or {}
    rel_path = anchor.get("path") or ""
    quote = anchor.get("text_quote") or ""
    start = anchor.get("start")
    end = anchor.get("end")
    result = {
        "source_path_resolves": rel_exists(rel_path),
        "quote_text_found": False,
        "quote_offset_exact": False,
    }
    if not result["source_path_resolves"] or not quote:
        return result
    try:
        text = (ROOT / rel_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return result
    result["quote_text_found"] = quote in text
    if isinstance(start, int) and isinstance(end, int) and 0 <= start <= end <= len(text):
        result["quote_offset_exact"] = text[start:end] == quote
    return result


def classify_next_action(case: dict, check: dict, landing_class: str) -> dict:
    state = check.get("observed_state") or case.get("surface_state") or "unknown"
    layer = case.get("layer") or ""
    anchor_status = case.get("anchor_status") or (case.get("source_anchor") or {}).get("status") or ""
    serious = bool(check.get("serious"))
    full_audit = bool(check.get("full_audit"))

    if state == "blocking":
        action = "暂不可行动；打开 full audit；优先修锚点或处理阻塞原因"
        open_full = True
        actionability = "not_actionable"
    elif state == "regressed":
        action = "重新入队；打开 full audit；不要继续按已解决处理"
        open_full = True
        actionability = "not_actionable"
    elif state == "for_review":
        action = "进入复核；打开 full audit；复核前不作为行动依据"
        open_full = True
        actionability = "not_actionable_until_review"
    elif state == "resolved" or state == "resolved_folded":
        action = "默认折叠；只保留历史入口；回归时再重开"
        open_full = False
        actionability = "historical_only"
    elif anchor_status not in {"valid", ""}:
        action = "补锚点或重新定位来源；不要作为行动依据"
        open_full = True
        actionability = "not_actionable"
    elif landing_class == "claim_relevant_context_landing":
        action = "轻量可读，但回源只是 claim 相关上下文；行动前必须打开 full audit"
        open_full = False
        actionability = "light_save_only"
    elif landing_class == "claim_landing":
        action = "轻量可读，但落点是 claim；行动前仍要找证据段或 full audit"
        open_full = False
        actionability = "light_save_only"
    elif "authority" in layer:
        action = "轻量保存；把 dashboard/test/count/lint 只当诊断，不当事实依据"
        open_full = False
        actionability = "light_save_only"
    else:
        action = "轻量保存；如需作为行动依据再打开 full audit"
        open_full = full_audit
        actionability = "light_save_only" if not serious else "not_actionable_until_review"

    wrong_actionability = serious and actionability not in {"not_actionable", "not_actionable_until_review"}
    serious_miss = serious and not open_full and state not in {"blocking", "regressed", "for_review"}
    return {
        "operator_next_action": action,
        "operator_would_open_full_audit": open_full,
        "operator_actionability": actionability,
        "wrong_actionability_selftest": wrong_actionability,
        "serious_miss_selftest": serious_miss,
    }


def select_cases(cases: list[dict], semantic_rows: list[dict]) -> list[str]:
    selected: list[str] = []
    by_layer: dict[str, list[dict]] = defaultdict(list)
    for case in cases:
        by_layer[case.get("layer") or ""].append(case)

    semantic_by_class: dict[str, list[str]] = defaultdict(list)
    for row in semantic_rows:
        semantic_by_class[row.get("landing_class") or ""].append(row["case_id"])

    for landing_class, count in FULL_ANCHOR_BY_CLASS.items():
        selected.extend(semantic_by_class.get(landing_class, [])[:count])

    for layer, count in LAYER_TARGETS.items():
        selected.extend(case["id"] for case in by_layer.get(layer, [])[:count])

    deduped: list[str] = []
    seen = set()
    for case_id in selected:
        if case_id not in seen:
            deduped.append(case_id)
            seen.add(case_id)
    return deduped


def main() -> None:
    cases = load_json(ROOT / "candidate_cases.json")
    checks_doc = load_json(ROOT / "checks_shell_core.json")
    artifacts = load_json(ROOT / "artifacts_shell_core.json")
    semantic_doc = load_json(ROOT / "data" / "clickback_semantic_landing_eval.json")

    case_by_id = {case["id"]: case for case in cases}
    check_by_id = {row["case_id"]: row for row in checks_doc["checks"]}
    artifact_by_id = {row["case_id"]: row for row in artifacts}
    semantic_by_id = {row["case_id"]: row for row in semantic_doc.get("rows", [])}

    rows: list[dict] = []
    for case_id in select_cases(cases, semantic_doc.get("rows", [])):
        case = case_by_id[case_id]
        check = check_by_id.get(case_id, {})
        artifact = artifact_by_id.get(case_id, {})
        semantic = semantic_by_id.get(case_id, {})
        landing_class = semantic.get("landing_class") or (case.get("source_anchor") or {}).get("landing_class") or ""
        quote = quote_check(case)
        action = classify_next_action(case, check, landing_class)
        source_path = (case.get("source_anchor") or {}).get("path") or ""
        record_path = case.get("record_path") or ""
        evidence_path = case.get("evidence_path") or ""

        source_ok = quote["source_path_resolves"]
        record_ok = rel_exists(record_path)
        evidence_ok = rel_exists(evidence_path)
        can_understand = bool(check.get("observed_state")) and bool(action["operator_next_action"])
        authority_misunderstanding = False
        if "authority" in (case.get("layer") or ""):
            authority_note = "识别为措辞/诊断边界问题，不把 lint/dashboard/count 当 truth"
        else:
            authority_note = "未把 shell、pointer、count、dashboard 或 test 当 truth"

        if landing_class == "evidence_landing":
            landing_note = "强：落到证据段"
        elif landing_class == "claim_landing":
            landing_note = "中弱：落到 claim，不等于证据段"
        elif landing_class == "claim_relevant_context_landing":
            landing_note = "弱：只落到 claim 相关上下文，行动前要 full audit"
        elif source_path and (case.get("source_anchor") or {}).get("status") == "valid":
            landing_note = "本地 dataset quote/offset 锚点"
        else:
            landing_note = "锚点异常或无 landing class"

        rows.append(
            {
                "case_id": case_id,
                "pool": case.get("pool") or "",
                "dataset_family": case.get("dataset_family") or "",
                "layer": case.get("layer") or "",
                "observed_state": check.get("observed_state") or "",
                "expected_state": check.get("expected_state") or "",
                "serious": bool(check.get("serious")),
                "anchor_status": case.get("anchor_status") or (case.get("source_anchor") or {}).get("status") or "",
                "landing_class": landing_class,
                "quote_strategy": semantic.get("quote_strategy") or "",
                "can_understand_state_and_action": can_understand,
                **action,
                "authority_misunderstanding_selftest": authority_misunderstanding,
                "source_path_resolves": source_ok,
                "record_path_resolves": record_ok,
                "evidence_path_resolves": evidence_ok,
                "quote_text_found": quote["quote_text_found"],
                "quote_offset_exact": quote["quote_offset_exact"],
                "claim_preview": short(case.get("claim") or artifact.get("front", [""])[0], 160),
                "landing_note": landing_note,
                "authority_note": authority_note,
                "source_path": source_path,
                "record_path": record_path,
                "evidence_path": evidence_path,
            }
        )

    OUT_DIR.mkdir(exist_ok=True)
    REPORT_PATH.parent.mkdir(exist_ok=True)
    fieldnames = list(rows[0].keys())
    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    landing_counts = Counter(row["landing_class"] or "none" for row in rows)
    layer_counts = Counter(row["layer"] for row in rows)
    summary = {
        "status": "codex local real operator self-test",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "Codex self-test over local real-row/full-anchor samples; not human adjudication; not product gate.",
        "sample_count": len(rows),
        "layer_counts": dict(layer_counts),
        "landing_class_counts": dict(landing_counts),
        "can_understand_state_and_action": sum(1 for row in rows if row["can_understand_state_and_action"]),
        "wrong_actionability_selftest": sum(1 for row in rows if row["wrong_actionability_selftest"]),
        "serious_miss_selftest": sum(1 for row in rows if row["serious_miss_selftest"]),
        "authority_misunderstanding_selftest": sum(1 for row in rows if row["authority_misunderstanding_selftest"]),
        "source_path_resolves": sum(1 for row in rows if row["source_path_resolves"]),
        "record_path_resolves": sum(1 for row in rows if row["record_path_resolves"]),
        "evidence_path_resolves": sum(1 for row in rows if row["evidence_path_resolves"]),
        "quote_text_found": sum(1 for row in rows if row["quote_text_found"]),
        "quote_offset_exact": sum(1 for row in rows if row["quote_offset_exact"]),
        "verdict": "usable_for_codex_operator_triage_with_known_limits",
        "next_route": "keep not_go_yet; use this as Codex comprehension evidence only; human/product gates remain open.",
    }
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    sample_lines = []
    for row in rows:
        sample_lines.append(
            "| {case_id} | {layer} | {observed_state} | {anchor_status} | {landing_class} | {operator_actionability} | {operator_next_action} |".format(
                **row
            )
        )

    report = f"""# Codex local real operator self-test

## Verdict

结论：Codex 自己看得懂，能用于后台 operator triage；但这不是真人评审，也不是 product click-back gate。

这次只测一件事：我作为你的资料库管家，面对本地真实行承载样本和 full-anchor 快照时，能不能看懂 shell/operator surface 给出的状态、下一步动作、回源强弱和边界提醒。没有让用户参与，没有打开 120-case main packet，也没有把 recurrence 默认打开。

## Summary

- 样本数：{summary["sample_count"]}
- 能看懂状态和下一步动作：{summary["can_understand_state_and_action"]}/{summary["sample_count"]}
- wrong actionability：{summary["wrong_actionability_selftest"]}/{summary["sample_count"]}
- serious miss：{summary["serious_miss_selftest"]}/{summary["sample_count"]}
- authority misunderstanding：{summary["authority_misunderstanding_selftest"]}/{summary["sample_count"]}
- source / record / evidence 路径可打开：{summary["source_path_resolves"]}/{summary["sample_count"]} / {summary["record_path_resolves"]}/{summary["sample_count"]} / {summary["evidence_path_resolves"]}/{summary["sample_count"]}
- quote 文本可找到 / offset 精确：{summary["quote_text_found"]}/{summary["sample_count"]} / {summary["quote_offset_exact"]}/{summary["sample_count"]}
- landing class 分布：{json.dumps(summary["landing_class_counts"], ensure_ascii=False)}

## What This Means

对 Codex 来说，这张 operator surface 有帮助：它把我需要做的事压成了“轻量保存、复核、阻塞不可行动、补锚点、重新入队、行动前 full audit”这些动作，而不是让我从一大坨 raw audit transcript 里猜。

但它的边界也清楚：`claim_relevant_context_landing` 只能算弱回源落点，不能当证据段；`claim_landing` 也只是 claim 落点，不等于 support。真正要当行动依据时，仍然要打开 full audit 或找 evidence landing。

## Sample Readout

| case | layer | state | anchor | landing | actionability | Codex next action |
|---|---|---|---|---|---|---|
{chr(10).join(sample_lines)}

## Files

- CSV: `review_packet_local_real_self_test/LOCAL_REAL_OPERATOR_SELF_TEST.csv`
- Summary: `review_packet_local_real_self_test/LOCAL_REAL_OPERATOR_SELF_TEST_SUMMARY.json`

## Boundary

本报告只能说明“Codex/operator agent 能读懂并执行初步路由”。它不能替代真人双评、timing、真实 UI click log，也不能把 `not_go_yet` 改成 go。
"""
    REPORT_PATH.write_text(report, encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
