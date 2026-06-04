import csv
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "review_packet_risk_tiered_24"

TARGETS = {
    "ordinary_stable": 3,
    "action_challenge_conflict": 3,
    "anchor_problem": 3,
    "omission_insufficiency_ambiguity": 3,
    "full_anchor_click": 2,
    "resolved_repeated_recurrence": 2,
    "authority_leak_bait": 2,
    "over_grouping_near_miss": 2,
    "anchor_jumpback_failure": 2,
    "serious_folded_violation": 2,
}

STATE_ZH = {
    "ordinary": "普通记录",
    "for_review": "需要复核",
    "blocking": "阻塞，暂不可作为行动依据",
    "regressed": "已回归，重新进入队列",
    "resolved_folded": "已解决，默认折叠，可回看",
}

ANCHOR_ZH = {
    "valid": "可回源",
    "missing": "锚点缺失，不能直接回源",
    "stale": "锚点可能过期，需要复核来源版本",
    "drift": "锚点漂移，当前定位可能不准",
    "moved": "来源位置移动，需要重新定位",
}

LAYER_ZH = {
    "ordinary_stable": "普通稳定记录",
    "action_challenge_conflict": "行动依据 / 明确挑战 / 冲突",
    "anchor_problem": "锚点问题",
    "omission_insufficiency_ambiguity": "已知遗漏 / 证据不足 / 范围不明",
    "full_anchor_click": "完整锚点回源",
    "resolved_repeated_recurrence": "已解决 / 重复形态",
    "authority_leak_bait": "authority 误读诱饵",
    "over_grouping_near_miss": "过度归并近失误",
    "anchor_jumpback_failure": "回源跳转失败风险",
    "serious_folded_violation": "严重项折叠 / 回归陷阱",
}

LANDING_CLASS_ZH = {
    "evidence_landing": "证据段落落点，强",
    "claim_landing": "claim 原文落点，中",
    "claim_relevant_context_landing": "claim 相关上下文落点，弱；需要人审确认是否是证据段",
    "selector_failure": "语义落点失败",
    "": "未显示",
}

RAW_LABELS_TO_HIDE = [
    "pointer_triad",
    "unresolved_gate",
    "missing_anchor",
    "review_due",
    "FULL_AUDIT_OPEN",
]


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def forbidden_wording_rules():
    return load_json(ROOT / "forbidden_wording_zh.json")


def write_csv(path, rows, fieldnames):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def artifact_map(filename):
    return {row["case_id"]: row for row in load_json(ROOT / filename)}


def checks_map():
    raw = load_json(ROOT / "checks_shell_core.json")
    rows = raw["checks"] if isinstance(raw, dict) and "checks" in raw else raw
    return {row["case_id"]: row for row in rows}


def first_line(text, prefix):
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    return ""


def select_cases(cases, artifacts, checks):
    by_layer = defaultdict(list)
    for case in cases:
        if case["id"] in artifacts and case["id"] in checks:
            by_layer[case["layer"]].append(case)

    selected = []
    for layer, count in TARGETS.items():
        pool = by_layer[layer]
        if len(pool) < count:
            raise RuntimeError(f"Not enough cases for {layer}: need {count}, have {len(pool)}")

        picked = []
        used_families = set()
        for case in pool:
            family = case.get("dataset_family", "")
            if family not in used_families:
                picked.append(case)
                used_families.add(family)
            if len(picked) == count:
                break

        if len(picked) < count:
            for case in pool:
                if case not in picked:
                    picked.append(case)
                if len(picked) == count:
                    break

        selected.extend(picked)
    return selected


def risk_reasons(case, check):
    signals = list(case.get("signals") or [])
    anchor = case.get("anchor_status", "")
    layer = case.get("layer", "")
    reasons = []

    if "action_basis" in signals:
        reasons.append("涉及行动依据，必须打开 full audit。")
    if "explicit_challenge" in signals:
        reasons.append("存在明确挑战，必须复核。")
    if "conflict" in signals:
        reasons.append("存在冲突，不能轻量跳过。")
    if "known_omission" in signals or "missing_evidence" in signals:
        reasons.append("存在已知遗漏或证据缺口，不能直接行动。")
    if "ambiguous_scope" in signals or layer == "omission_insufficiency_ambiguity":
        reasons.append("适用范围或证据充分性不清，需要复核。")
    if "regression" in signals or check.get("observed_state") == "regressed":
        reasons.append("已回归，必须重新进入队列。")
    if anchor != "valid":
        reasons.append(f"{ANCHOR_ZH.get(anchor, '锚点异常')}，需要先处理回源问题。")
    if layer == "authority_leak_bait":
        reasons.append("包含容易被误读成 authority 的表述，需要边界提醒。")
    if layer == "over_grouping_near_miss":
        reasons.append("存在过度归并近失误，只能作为路由提示，不能当支持强度。")
    if layer == "anchor_jumpback_failure":
        reasons.append("回源跳转可能失败，需要确认 source-first drilldown。")
    if layer == "serious_folded_violation":
        reasons.append("严重项不能被折叠，必须保持可见。")
    if check.get("resolved"):
        reasons.append("已解决项可折叠，但必须可回看；回归时必须重开。")

    if not reasons:
        reasons.append("普通稳定记录，无硬触发；保持轻量即可。")
    return reasons


def handling_suggestion(case, check):
    anchor = case.get("anchor_status", "")
    state = check.get("observed_state", "")
    signals = set(case.get("signals") or [])
    layer = case.get("layer", "")

    if anchor == "missing":
        return "补锚点；暂不可行动"
    if anchor in {"stale", "drift", "moved"}:
        return "重新定位来源；暂不可行动"
    if state in {"blocking", "regressed"}:
        return "打开 full audit；暂不可行动"
    if state == "for_review":
        return "打开 full audit；完成复核前不要作为行动依据"
    if check.get("resolved"):
        return "默认折叠，可回看；如回归则重新进入队列"
    if layer == "authority_leak_bait":
        return "轻量保存；保留边界提醒；不要把诊断、计数或 lint 当证据；作为行动依据时再打开 full audit"
    if layer == "over_grouping_near_miss":
        return "轻量保存；仅保留归并边界提醒；不要把 group count 当支持强度；作为行动依据时再打开 full audit"
    if layer == "anchor_jumpback_failure":
        return "先确认来源落点；无法确认语义落点时补锚点；暂不要作为行动依据"
    if signals:
        return "打开 full audit；完成复核前不要作为行动依据"
    return "轻量保存；如需行动依据，请打开完整审计包"


def operator_gloss(case, check):
    state = check.get("observed_state", "")
    anchor = case.get("anchor_status", "")
    layer = case.get("layer", "")

    if anchor == "missing":
        return "先判断为暂不可行动；本轮重点是识别锚点缺失并要求补锚点。"
    if anchor in {"stale", "drift", "moved"}:
        return "先判断为需要重新定位来源；不要因为有路径就算回源成功。"
    if state == "blocking":
        return "先判断为不可行动并打开 full audit；英文 claim 只作原文内容，不替代复核。"
    if state == "for_review":
        return "先判断为需要复核；重点看缺口、挑战、范围和证据充分性。"
    if state == "regressed":
        return "先判断为回归重开；不能被 resolved 或 recurrence 折叠吞掉。"
    if state == "resolved_folded":
        return "先判断为默认折叠且可回看；若出现新冲突或回归必须重开。"
    if layer in {"authority_leak_bait", "over_grouping_near_miss"}:
        return "先当普通路由样本处理，但要特别防止把 count、lineage、test 或 dashboard 误读成证据。"
    return "先轻量保存；只有进入行动依据或出现硬触发时才打开 full audit。"


def boundary_notes(case, check):
    layer = case.get("layer", "")
    signals = set(case.get("signals") or [])
    landing_class = ((case.get("source_anchor") or {}).get("landing_class") or "")
    notes = []

    if layer in {"authority_leak_bait", "authority_leakage_paraphrase"}:
        notes.append("dashboard、test、LLM summary 或 lint 只能作诊断，不能当事实证据。")
    if layer in {"resolved_repeated_recurrence", "over_grouping_near_miss"} or check.get("can_group"):
        notes.append("重复数 / group count 只代表路由压缩，不代表支持更强。")
    if "feedback" in signals or "scope_fit" in signals:
        notes.append("feedback 只影响激活、适用性或复核队列，不改变 truth。")
    if case.get("anchor_status") != "valid":
        notes.append("有 provenance 不等于有可用 support；锚点异常时不能作为行动依据。")
    if landing_class == "claim_relevant_context_landing":
        notes.append("当前只是 claim 相关上下文落点，不等于证据段落落点；行动前需要 full audit。")
    elif landing_class == "claim_landing":
        notes.append("当前落点是 claim 原文，不等于 support；行动前需要证据段落或 full audit。")
    return notes


def boundary_note_required(case, check):
    return bool(boundary_notes(case, check))


def short_text(text, limit=260):
    text = re.sub(r"\s+", " ", str(text)).strip()
    return text[:limit] + ("..." if len(text) > limit else "")


def drilldown(case):
    anchor = case.get("source_anchor") or {}
    return {
        "source": anchor.get("path", ""),
        "record": case.get("record_path", ""),
        "evidence": case.get("evidence_path", ""),
        "quote": short_text(anchor.get("text_quote", "")),
        "start": anchor.get("start", ""),
        "end": anchor.get("end", ""),
        "quote_strategy": anchor.get("quote_strategy", ""),
        "landing_class": anchor.get("landing_class", ""),
        "semantic_selector_success": anchor.get("semantic_selector_success", None),
        "boilerplate_quote": anchor.get("boilerplate_quote", None),
    }


def entry(label, path):
    if not path:
        return f"{label}入口：未显示"
    return f"{label}入口：打开{label}（句柄：{path}）"


def render_card(case_no, case, artifact, check):
    state = check.get("observed_state") or first_line(artifact["rendered_text"], "state:")
    anchor_status = case.get("anchor_status", "")
    d = drilldown(case)
    reasons = risk_reasons(case, check)
    notes = boundary_notes(case, check)
    anchor_line = ANCHOR_ZH.get(anchor_status, anchor_status or "未知")
    if d["semantic_selector_success"] is False:
        anchor_line = f"{anchor_line}；来源可打开，但原文片段未确认落到 claim-relevant 证据，不能算产品级 click-back"

    lines = [
        f"## RISK-UX-{case_no:02d} / {case['id']}",
        "",
        f"样本类型：{LAYER_ZH.get(case['layer'], case['layer'])}",
        "",
        f"- 状态：{STATE_ZH.get(state, state or '未显示')}",
        f"- 一句话摘要：这条记录声称：{case.get('claim', '').strip()}",
        f"- 中文导读：{operator_gloss(case, check)}",
        f"- 风险原因：{'；'.join(reasons)}",
        f"- 锚点状态：{anchor_line}",
        f"- 处理建议：{handling_suggestion(case, check)}",
        "- 回源入口：",
        f"  - {entry('来源', d['source'])}",
        f"  - {entry('记录', d['record'])}",
        f"  - {entry('证据', d['evidence'])}",
        f"  - 原文片段：{d['quote'] or '未显示'}",
        f"  - 位置：{d['start']}-{d['end']}",
        f"  - 语义落点：{LANDING_CLASS_ZH.get(d['landing_class'], d['landing_class'] or '未显示')}",
    ]
    if notes:
        lines.append("- 定向边界提醒：")
        for note in notes:
            lines.append(f"  - {note}")
    lines.extend(
        [
            "",
            "请记录：耗时、是否看懂状态、是否看懂升级原因、下一步处理、是否会打开 full audit、回源是否成功、是否误读 authority。",
            "",
            "---",
            "",
        ]
    )
    return "\n".join(lines)


def sheet_row(case_no, case):
    return {
        "sample_id": f"RISK-UX-{case_no:02d}",
        "case_id": case["id"],
        "time_to_triage_seconds": "",
        "state_understood_y_n": "",
        "risk_reason_understood_y_n": "",
        "next_action_save_review_fix_anchor_full_audit_not_actionable": "",
        "would_open_full_audit_y_n": "",
        "wrong_actionability_y_n": "",
        "serious_miss_y_n": "",
        "clickback_source_ok_y_n": "",
        "clickback_record_ok_y_n": "",
        "clickback_evidence_ok_y_n": "",
        "authority_misunderstanding_y_n": "",
        "burden_1_light_5_heavy": "",
        "notes": "",
    }


def hidden_row(case_no, case, check):
    anchor = case.get("source_anchor") or {}
    return {
        "sample_id": f"RISK-UX-{case_no:02d}",
        "case_id": case["id"],
        "layer": case.get("layer", ""),
        "surface_state": case.get("surface_state", ""),
        "observed_state": check.get("observed_state", ""),
        "expected_state": check.get("expected_state", ""),
        "serious": check.get("serious", ""),
        "ordinary": check.get("ordinary", ""),
        "resolved": check.get("resolved", ""),
        "full_audit_expected": check.get("full_audit", ""),
        "anchor_status": case.get("anchor_status", ""),
        "signals": "|".join(case.get("signals") or []),
        "source_path": anchor.get("path", ""),
        "record_path": case.get("record_path", ""),
        "evidence_path": case.get("evidence_path", ""),
        "quote_strategy": anchor.get("quote_strategy", ""),
        "landing_class": anchor.get("landing_class", ""),
        "semantic_selector_success": anchor.get("semantic_selector_success", ""),
        "boilerplate_quote": anchor.get("boilerplate_quote", ""),
    }


def lint_cards(cards_text, selected_count, boundary_expected_count):
    findings = []
    required = ["状态：", "一句话摘要：", "风险原因：", "锚点状态：", "处理建议：", "回源入口："]
    wording_rules = forbidden_wording_rules()

    for phrase in wording_rules["exact_banned_phrases"]:
        if phrase in cards_text:
            findings.append({"severity": "fail", "type": "forbidden_phrase", "phrase": phrase})

    for rule in wording_rules.get("regex_banned_patterns", []):
        if re.search(rule["pattern"], cards_text, flags=re.IGNORECASE):
            findings.append({"severity": "fail", "type": "forbidden_pattern", "id": rule["id"], "pattern": rule["pattern"]})

    for label in RAW_LABELS_TO_HIDE:
        if label in cards_text:
            findings.append({"severity": "warn", "type": "raw_machine_label_visible", "label": label})

    for req in required:
        count = sum(1 for line in cards_text.splitlines() if line.startswith(f"- {req}"))
        if count != selected_count:
            findings.append({"severity": "fail", "type": "required_slot_count", "slot": req, "count": count, "expected": selected_count})

    boundary_count = sum(1 for line in cards_text.splitlines() if line.startswith("- 定向边界提醒："))
    if boundary_count != boundary_expected_count:
        findings.append(
            {
                "severity": "fail",
                "type": "targeted_boundary_slot_count",
                "count": boundary_count,
                "expected": boundary_expected_count,
            }
        )

    return {
        "status": "pass" if not any(f["severity"] == "fail" for f in findings) else "fail",
        "sample_count": selected_count,
        "findings": findings,
        "rules": "forbidden_wording_zh.json",
        "note": "Render-integrity and Chinese forbidden-wording lint only; targeted boundary reminders appear only when relevant. Not semantic safety proof.",
    }


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    cases = load_json(ROOT / "candidate_cases.json")
    artifacts = artifact_map("artifacts_shell_core.json")
    checks = checks_map()
    selected = select_cases(cases, artifacts, checks)

    lines = [
        "# Risk-Tiered Reviewer UX Preflight: 24 Chinese Operator Samples",
        "",
        "状态：沙盒小样本预演材料。给 AI / reviewer operator 使用，不是普通用户日常流程，不是正式 human timing，不是 independent human oracle，不是主库规则。",
        "",
        "使用者是 Codex / Pro / reviewer agent。每条记录只看中文 operator 前脸，判断它为什么轻量或加厚、下一步怎么处理、能不能回源、有没有 authority 误读。",
        "",
        "普通用户不需要读这些卡片；用户只应在风险影响回答或行动时看到一句人话提醒。",
        "",
        "全局边界：本卡用于分流与回源，不替代原始证据；重复数不表示支持强度；lineage 不证明独立性；test/dashboard/lint 不证明事实成立。",
        "",
        "---",
        "",
    ]
    sheet_rows = []
    hidden_rows = []
    boundary_expected_count = 0

    for idx, case in enumerate(selected, start=1):
        artifact = artifacts[case["id"]]
        check = checks[case["id"]]
        if boundary_note_required(case, check):
            boundary_expected_count += 1
        lines.append(render_card(idx, case, artifact, check))
        sheet_rows.append(sheet_row(idx, case))
        hidden_rows.append(hidden_row(idx, case, check))

    cards_text = "\n".join(lines)
    (OUT / "RISK_TIERED_REVIEWER_CARDS_ZH.md").write_text(cards_text, encoding="utf-8")

    sheet_fields = list(sheet_rows[0].keys())
    hidden_fields = list(hidden_rows[0].keys())
    write_csv(OUT / "RISK_TIERED_REVIEWER_SHEET_BLANK.csv", sheet_rows, sheet_fields)
    write_csv(OUT / "hidden_gold_after_done.csv", hidden_rows, hidden_fields)

    coverage = {
        "sample_count": len(selected),
        "targets": TARGETS,
        "layers": dict(defaultdict(int)),
        "anchor_status": dict(defaultdict(int)),
        "states": dict(defaultdict(int)),
        "note": "Default-core shell_core only; recurrence side arm is not under test.",
    }
    for case in selected:
        check = checks[case["id"]]
        coverage["layers"][case["layer"]] = coverage["layers"].get(case["layer"], 0) + 1
        coverage["anchor_status"][case["anchor_status"]] = coverage["anchor_status"].get(case["anchor_status"], 0) + 1
        coverage["states"][check.get("observed_state", "")] = coverage["states"].get(check.get("observed_state", ""), 0) + 1

    lint = lint_cards(cards_text, len(selected), boundary_expected_count)
    forbidden_lint = {
        "status": "pass" if not any(f["severity"] == "fail" for f in lint["findings"] if f["type"] in {"forbidden_phrase", "forbidden_pattern"}) else "fail",
        "rules": "forbidden_wording_zh.json",
        "sample_count": len(selected),
        "findings": [f for f in lint["findings"] if f["type"] in {"forbidden_phrase", "forbidden_pattern"}],
        "note": "Chinese forbidden-wording lint for normal operator-facing renderer text.",
    }
    (OUT / "sample_coverage.json").write_text(json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "render_integrity_lint.json").write_text(json.dumps(lint, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "forbidden_wording_lint_zh.json").write_text(json.dumps(forbidden_lint, ensure_ascii=False, indent=2), encoding="utf-8")

    (OUT / "README_RISK_TIERED_24.md").write_text(
        """# Risk-Tiered Reviewer UX Preflight 24

状态：沙盒小样本预演材料。给 AI / reviewer operator 使用，不是普通用户日常流程，不是正式 human timing，不是 independent human oracle，不是主库 operation convention。

普通用户不需要读这些卡片。用户只应在风险影响回答或行动时看到一句人话提醒。

## 怎么用

1. 打开 `RISK_TIERED_REVIEWER_CARDS_ZH.md`。
2. 每条只看中文 operator 前脸，判断状态、升级原因、处理建议和回源入口。
3. 把答案填到 `RISK_TIERED_REVIEWER_SHEET_BLANK.csv`。
4. 做完后再看 `hidden_gold_after_done.csv`。

## 这轮看什么

- time-to-triage：多久能判断下一步。
- serious miss rate：有没有漏掉严重项。
- wrong-actionability rate：有没有把不可行动项当可行动。
- click-back success：source / record / evidence 能不能跳回。
- authority misunderstanding：有没有把 count、test、dashboard、lineage、feedback、shell summary 当证据。
- forbidden wording：中文 operator 文案不能出现 `forbidden_wording_zh.json` 中的 truth/readiness 越权措辞。

## 这轮不看什么

- 不看 line reduction。
- 不比较 recurrence side arm。
- 不生成人审结论。
- 不证明 product-grade click-back。
- 不证明 semantic firewall。
""",
        encoding="utf-8",
    )

    print(json.dumps({"output": str(OUT), "samples": len(selected), "lint_status": lint["status"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
