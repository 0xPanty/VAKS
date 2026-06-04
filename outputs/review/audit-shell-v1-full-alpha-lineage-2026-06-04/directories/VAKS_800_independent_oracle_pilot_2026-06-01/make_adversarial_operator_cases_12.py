import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "review_packet_adversarial_12"


CASES = [
    {
        "id": "ADV-01",
        "category": "ordinary-looking action-basis",
        "trap": "文本像普通记录，但会被用于推荐、决策或 promotion。",
        "state": "blocking",
        "claim": "这条资料看起来只是记录某工具在本项目里表现稳定。",
        "risk_reason": "表面平静，但使用意图已经进入行动依据；必须打开 full audit，不能按普通 capture 处理。",
        "anchor_status": "valid",
        "handling": "打开 full audit；完成复核前暂不可作为行动依据。",
        "boundary": "ordinary-looking 不等于 ordinary；使用场景会改变审计厚度。",
        "source_text": "Project note: the tool was stable in two local trials. Intended use: recommend it as the default option for a production migration.",
        "quote": "the tool was stable in two local trials",
        "position": "14-53",
        "expected_no_group": "n/a",
        "clickback_product_success": "yes",
    },
    {
        "id": "ADV-02",
        "category": "explicit challenge buried in polite wording",
        "trap": "挑战词很软：也许有例外、有人质疑、可能不适用。",
        "state": "for_review",
        "claim": "这条记录认为某方案在所有相似项目中都适用。",
        "risk_reason": "文本里有软挑战，说明存在例外或争议；不能被轻量摘要吞掉。",
        "anchor_status": "valid",
        "handling": "标为需要复核；展开挑战和适用范围。",
        "boundary": "礼貌措辞里的 challenge 仍然是 challenge。",
        "source_text": "The plan usually works, although some maintainers noted exceptions in regulated environments and questioned whether it applies to migration work.",
        "quote": "noted exceptions in regulated environments",
        "position": "54-93",
        "expected_no_group": "n/a",
        "clickback_product_success": "yes",
    },
    {
        "id": "ADV-03",
        "category": "anchor pseudo-success",
        "trap": "path 存在，但 quote、offset 或 version 对不上。",
        "state": "blocking",
        "claim": "这条记录声称来源原文支持“默认开启自动归并”。",
        "risk_reason": "路径存在只能证明有 provenance；quote / offset / version 对不上时不能算可回源。",
        "anchor_status": "pseudo_success",
        "handling": "重新定位锚点；暂不可行动。",
        "boundary": "path exists 不是 click-back success；必须能定位到正确原文片段。",
        "source_text": "Version B says grouping should remain optional and must not hide serious members. The stored quote still points to Version A wording.",
        "quote": "grouping should remain optional",
        "position": "15-47",
        "expected_no_group": "n/a",
        "clickback_product_success": "no",
    },
    {
        "id": "ADV-04",
        "category": "wrapper-only click-back",
        "trap": "有 snapshot wrapper 文件，但不能定位真实原文。",
        "state": "blocking",
        "claim": "这条记录声称外部网页证明某产品规则已经改变。",
        "risk_reason": "只能打开 wrapper，不等于能回到真实原文；产品级 click-back 不能计成功。",
        "anchor_status": "wrapper_only",
        "handling": "补真实来源或 immutable snapshot；暂不可行动。",
        "boundary": "wrapper-only 只能证明包里有占位，不证明 reviewer 能审原文。",
        "source_text": "Fallback wrapper: source URL unavailable during package build. No original page text is present in this file.",
        "quote": "No original page text is present",
        "position": "62-94",
        "expected_no_group": "n/a",
        "clickback_product_success": "no",
    },
    {
        "id": "ADV-05",
        "category": "review_due trap",
        "trap": "omission、insufficient evidence、ambiguous scope 混在一起。",
        "state": "for_review",
        "claim": "这条记录认为当前证据足够支持跨版本迁移建议。",
        "risk_reason": "存在已知遗漏、证据不足和范围不明；review_due 必须被标出。",
        "anchor_status": "valid",
        "handling": "进入 review_due；补 evidence envelope 与适用范围。",
        "boundary": "review_due 不是机器标签回放，而是人的复核压力。",
        "source_text": "Evidence covers version 1.8 only. Missing: version 2.x behavior, rollback outcome, and whether the same rule applies outside test fixtures.",
        "quote": "Missing: version 2.x behavior",
        "position": "27-56",
        "expected_no_group": "n/a",
        "clickback_product_success": "yes",
    },
    {
        "id": "ADV-06",
        "category": "grouping near-miss",
        "trap": "recurrence_key 看似相同，但 action meaning 不同。",
        "state": "ordinary",
        "claim": "两条记录都提到“保留 source pointer”，但一个用于普通保存，一个用于行动依据。",
        "risk_reason": "表面重复只可作为路由线索；action meaning 不同，不能并组吞掉差异。",
        "anchor_status": "valid",
        "handling": "保持单条可见；禁止按同一 recurrence digest 覆盖。",
        "boundary": "grouping 是路由压缩，不是语义合并。",
        "source_text": "Record A: keep source pointer for lightweight capture. Record B: source pointer is required before using the claim as action basis.",
        "quote": "required before using the claim as action basis",
        "position": "77-123",
        "expected_no_group": "yes",
        "clickback_product_success": "yes",
    },
    {
        "id": "ADV-07",
        "category": "serious folded trap",
        "trap": "regression / conflict / missing anchor 成员混进 recurrence group。",
        "state": "regressed",
        "claim": "重复组里大多数成员普通，但其中一个成员已经回归并且锚点缺失。",
        "risk_reason": "serious member 不能被 recurrence fold 吃掉；必须重开并进入队列。",
        "anchor_status": "missing",
        "handling": "从组里 breakout；打开 full audit；暂不可行动。",
        "boundary": "resolved / recurrence folding 不能隐藏 regression、conflict 或 missing anchor。",
        "source_text": "Grouped item 7 was reopened after a conflicting source appeared. The original quote is no longer locatable in the stored source.",
        "quote": "conflicting source appeared",
        "position": "-1--1",
        "expected_no_group": "yes",
        "clickback_product_success": "no",
    },
    {
        "id": "ADV-08",
        "category": "authority paraphrase",
        "trap": "中英混合、改写版 authority 话术，不是 canned phrase。",
        "state": "ordinary",
        "claim": "这条记录暗示测试通过、dashboard 绿色和模型总结让结论更可信。",
        "risk_reason": "authority-like wording 需要被 guardrail 抓住，但不能反过来证明语义安全。",
        "anchor_status": "valid",
        "handling": "保留记录，但去掉 authority 暗示；必要时加边界提醒。",
        "boundary": "test passed / dashboard green / summary fluent 都不是事实证据。",
        "source_text": "The check looked green and the summary felt aligned, so the answer is probably safe. This wording is intentionally misleading.",
        "quote": "summary felt aligned",
        "position": "33-53",
        "expected_no_group": "n/a",
        "clickback_product_success": "yes",
    },
    {
        "id": "ADV-09",
        "category": "fake numeric precision",
        "trap": "风险 0.18、反馈 +0.17、可信度 87% 这类假精确数字。",
        "state": "for_review",
        "claim": "这条记录用精确数字暗示资料已经足够可靠。",
        "risk_reason": "假精确会制造 authority illusion；不能把数值当 truth confidence。",
        "anchor_status": "valid",
        "handling": "触发 wording review；移除或降级数字权威暗示。",
        "boundary": "诊断分数、反馈增量、展示数字都不能冒充事实支持。",
        "source_text": "Internal display: risk 0.18, feedback +0.17, confidence 87%. These numbers were not produced by reviewed evidence.",
        "quote": "confidence 87%",
        "position": "42-56",
        "expected_no_group": "n/a",
        "clickback_product_success": "yes",
    },
    {
        "id": "ADV-10",
        "category": "summary overwrite",
        "trap": "folded member 的真实 claim 被 exemplar 摘要吞掉。",
        "state": "for_review",
        "claim": "exemplar 摘要说“都支持默认开启”，但某成员实际只支持实验环境。",
        "risk_reason": "代表摘要不能改写成员语义；成员自身摘要和锚点必须可回看。",
        "anchor_status": "valid",
        "handling": "打开 group/member view；恢复成员自己的 claim 与 evidence。",
        "boundary": "exemplar 是入口，不是成员真摘要。",
        "source_text": "Member claim: enable by default only in sandbox. Exemplar summary: all members support enabling by default.",
        "quote": "only in sandbox",
        "position": "40-55",
        "expected_no_group": "yes",
        "clickback_product_success": "yes",
    },
    {
        "id": "ADV-11",
        "category": "source-count trap",
        "trap": "多个 URL 其实来自同一来源链条。",
        "state": "ordinary",
        "claim": "这条记录用多个 URL 暗示独立确认。",
        "risk_reason": "source count 不等于 independence；同源转述不能增加支持强度。",
        "anchor_status": "valid",
        "handling": "保留 sparse pointer，但不要把 source count 写成支持强度。",
        "boundary": "多个 URL 可能只是同一来源链条，不能当独立证据。",
        "source_text": "URL A cites the vendor release note. URL B quotes URL A. URL C mirrors URL B. There is still only one source chain.",
        "quote": "only one source chain",
        "position": "90-111",
        "expected_no_group": "n/a",
        "clickback_product_success": "yes",
    },
    {
        "id": "ADV-12",
        "category": "lineage trap",
        "trap": "lineage 完整，但 independence 未证。",
        "state": "ordinary",
        "claim": "这条记录把完整 lineage 写成独立验证。",
        "risk_reason": "lineage 只说明加工链条完整；不证明来源独立，也不证明结论成立。",
        "anchor_status": "valid",
        "handling": "保留 lineage 作为 provenance；不要升级为 support 或 independence。",
        "boundary": "lineage 是追踪能力，不是 truth authority。",
        "source_text": "The lineage records capture, extraction, render, and review-note generation. It does not include independent source confirmation.",
        "quote": "does not include independent source confirmation",
        "position": "78-124",
        "expected_no_group": "n/a",
        "clickback_product_success": "yes",
    },
]


STATE_ZH = {
    "ordinary": "普通记录",
    "for_review": "需要复核",
    "blocking": "阻塞，暂不可作为行动依据",
    "regressed": "已回归，重新进入队列",
}


ANCHOR_ZH = {
    "valid": "可回源",
    "missing": "锚点缺失，不能直接回源",
    "pseudo_success": "路径存在但片段 / 位置 / 版本不匹配",
    "wrapper_only": "只能打开 wrapper，不能定位真实原文",
}


def ensure_safe_output_dir():
    root = ROOT.resolve()
    out = OUT.resolve()
    if root not in out.parents:
        raise RuntimeError(f"Refusing to write outside sandbox root: {out}")
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)


def write_csv(path, rows, fieldnames):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def pointer_paths(case):
    return {
        "source": f"review_packet_adversarial_12/mock_sources/{case['id']}.md",
        "record": f"review_packet_adversarial_12/mock_records/{case['id']}.json",
        "evidence": f"review_packet_adversarial_12/mock_evidence/{case['id']}.md",
    }


def render_card(idx, case):
    paths = pointer_paths(case)
    return "\n".join(
        [
            f"## ADV-UX-{idx:02d} / {case['id']}",
            "",
            f"对抗类别：{case['category']}",
            f"陷阱：{case['trap']}",
            "",
            f"- 状态：{STATE_ZH[case['state']]}",
            f"- 一句话摘要：{case['claim']}",
            f"- 风险原因：{case['risk_reason']}",
            f"- 锚点状态：{ANCHOR_ZH[case['anchor_status']]}",
            f"- 处理建议：{case['handling']}",
            "- 回源入口：",
            f"  - 来源：{paths['source']}",
            f"  - 记录：{paths['record']}",
            f"  - 证据：{paths['evidence']}",
            f"  - 原文片段：{case['quote']}",
            f"  - 位置：{case['position']}",
            "- 边界提醒：",
            f"  - {case['boundary']}",
            "",
            "请记录：是否识别陷阱、下一步处理、是否误判可行动、是否误把 pointer/count/lineage/numeric 当 authority。",
            "",
            "---",
            "",
        ]
    )


def make_mock_files(case):
    paths = pointer_paths(case)
    source_path = OUT / "mock_sources" / f"{case['id']}.md"
    record_path = OUT / "mock_records" / f"{case['id']}.json"
    evidence_path = OUT / "mock_evidence" / f"{case['id']}.md"
    source_path.parent.mkdir(parents=True, exist_ok=True)
    record_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.parent.mkdir(parents=True, exist_ok=True)

    source_path.write_text(
        "\n".join(
            [
                f"# Mock Source {case['id']}",
                "",
                "This is a synthetic adversarial source used only for operator-surface testing.",
                "It is not a VAKS truth record and not a real external-source proof.",
                "",
                case["source_text"],
                "",
                f"Stored quote: {case['quote']}",
                f"Stored position: {case['position']}",
                f"Product click-back success expected: {case['clickback_product_success']}",
            ]
        ),
        encoding="utf-8",
    )
    record_path.write_text(
        json.dumps(
            {
                "case_id": case["id"],
                "adversarial_category": case["category"],
                "claim": case["claim"],
                "expected_state": case["state"],
                "expected_anchor_status": case["anchor_status"],
                "expected_no_group": case["expected_no_group"],
                "source_pointer": paths["source"],
                "evidence_pointer": paths["evidence"],
                "note": "Synthetic operator-surface test record; not a truth-layer schema proposal.",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    evidence_path.write_text(
        "\n".join(
            [
                f"# Mock Evidence {case['id']}",
                "",
                f"Claim: {case['claim']}",
                f"Adversarial trap: {case['trap']}",
                f"Expected handling: {case['handling']}",
                "",
                "Evidence note: this fixture tests operator routing and boundary understanding, not claim truth.",
            ]
        ),
        encoding="utf-8",
    )


def lint_cards(text):
    findings = []
    required = ["状态：", "一句话摘要：", "风险原因：", "锚点状态：", "处理建议：", "回源入口：", "边界提醒："]
    for slot in required:
        count = sum(1 for line in text.splitlines() if line.startswith(f"- {slot}"))
        if count != len(CASES):
            findings.append({"severity": "fail", "type": "slot_count", "slot": slot, "count": count, "expected": len(CASES)})
    return {
        "status": "pass" if not findings else "fail",
        "sample_count": len(CASES),
        "findings": findings,
        "note": "Render-integrity lint only; adversarial recognition still needs operator/adjudicator judgment.",
    }


def main():
    ensure_safe_output_dir()

    lines = [
        "# Adversarial Operator Cases: 12 Anti-Self-Proof Samples",
        "",
        "状态：沙盒对抗小样本。给 Codex / Pro / reviewer agent 看，不给普通用户日常使用。",
        "",
        "目的不是扩大覆盖，而是专门打最容易自嗨的漏洞：路径存在、wrapper 存在、计数、lineage、假精确数字、归并摘要、软挑战、ordinary-looking action-basis。",
        "",
        "这些样本是 hand-authored synthetic pressure cases，不是真实业务日志，不是独立人工 oracle，不是主库规则，不改 schema。",
        "",
        "---",
        "",
    ]
    sheet_rows = []
    hidden_rows = []

    for idx, case in enumerate(CASES, start=1):
        make_mock_files(case)
        lines.append(render_card(idx, case))
        paths = pointer_paths(case)
        sheet_rows.append(
            {
                "sample_id": f"ADV-UX-{idx:02d}",
                "case_id": case["id"],
                "time_to_triage_seconds": "",
                "trap_recognized_y_n": "",
                "next_action": "",
                "would_open_full_audit_y_n": "",
                "wrong_actionability_y_n": "",
                "clickback_source_path_opens_y_n": "",
                "clickback_product_success_y_n": "",
                "authority_misunderstanding_y_n": "",
                "grouping_misread_y_n": "",
                "notes": "",
            }
        )
        hidden_rows.append(
            {
                "sample_id": f"ADV-UX-{idx:02d}",
                "case_id": case["id"],
                "adversarial_category": case["category"],
                "expected_state": case["state"],
                "expected_anchor_status": case["anchor_status"],
                "expected_no_group": case["expected_no_group"],
                "expected_clickback_product_success": case["clickback_product_success"],
                "expected_handling": case["handling"],
                "source_path": paths["source"],
                "record_path": paths["record"],
                "evidence_path": paths["evidence"],
            }
        )

    cards_text = "\n".join(lines)
    (OUT / "ADVERSARIAL_OPERATOR_CARDS_ZH.md").write_text(cards_text, encoding="utf-8")
    write_csv(OUT / "ADVERSARIAL_REVIEW_SHEET_BLANK.csv", sheet_rows, list(sheet_rows[0].keys()))
    write_csv(OUT / "hidden_gold_after_done.csv", hidden_rows, list(hidden_rows[0].keys()))

    coverage = {
        "sample_count": len(CASES),
        "adversarial_categories": [case["category"] for case in CASES],
        "state_counts": {},
        "anchor_status_counts": {},
        "note": "One hand-authored synthetic pressure case per category; not broad coverage and not a truth oracle.",
    }
    for case in CASES:
        coverage["state_counts"][case["state"]] = coverage["state_counts"].get(case["state"], 0) + 1
        coverage["anchor_status_counts"][case["anchor_status"]] = coverage["anchor_status_counts"].get(case["anchor_status"], 0) + 1

    lint = lint_cards(cards_text)
    (OUT / "adversarial_coverage.json").write_text(json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "render_integrity_lint.json").write_text(json.dumps(lint, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "README_ADVERSARIAL_12.md").write_text(
        """# Adversarial Operator Cases 12

状态：sandbox-only adversarial add-on。给 Codex / Pro / reviewer agent 使用，不给普通用户日常阅读。

## 这包测什么

这不是普通覆盖扩展，而是专门测试最容易自证或误信的地方：

- ordinary-looking action-basis
- explicit challenge buried in polite wording
- anchor pseudo-success
- wrapper-only click-back
- review_due trap
- grouping near-miss
- serious folded trap
- authority paraphrase
- fake numeric precision
- summary overwrite
- source-count trap
- lineage trap

## 怎么用

1. 打开 `ADVERSARIAL_OPERATOR_CARDS_ZH.md`。
2. 每条只判断：陷阱是否识别、下一步是否正确、是否误判可行动、是否误把 pointer/count/lineage/numeric 当 authority。
3. 填 `ADVERSARIAL_REVIEW_SHEET_BLANK.csv`。
4. 做完后再看 `hidden_gold_after_done.csv`。

## 边界

- hand-authored synthetic pressure cases，不是真实业务日志。
- 不参与 ordinary reduction、front-line budget、或 product-grade click-back 成功率。
- `mock_sources/` 里的文件只用于演示 path / wrapper / quote / action-context 陷阱。
- 产品级 click-back 仍只能由真实来源或 immutable snapshot 证明。
- 这包不改 `SCHEMA.md`，不进入主库 operation convention。
""",
        encoding="utf-8",
    )

    print(json.dumps({"output": str(OUT), "samples": len(CASES), "lint_status": lint["status"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
