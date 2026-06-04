import csv
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "review_packet_user_8"

CASES = [
    ("USER-MAIN-01", "QUICK-MAIN-001"),
    ("USER-MAIN-02", "QUICK-MAIN-005"),
    ("USER-MAIN-03", "QUICK-MAIN-009"),
    ("USER-MAIN-04", "QUICK-MAIN-017"),
    ("USER-MAIN-05", "QUICK-MAIN-019"),
    ("USER-SIDE-01", "QUICK-SIDE-001"),
    ("USER-SIDE-02", "QUICK-SIDE-004"),
    ("USER-SIDE-03", "QUICK-SIDE-006"),
]


def load_artifacts(filename):
    data = json.loads((ROOT / filename).read_text(encoding="utf-8"))
    return {row["case_id"]: row for row in data}


def find_line(text, prefix):
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    return ""


def has_line(text, needle):
    return any(needle in line for line in text.splitlines())


def short_quote(line):
    m = re.search(r'quote="(.*?)"', line)
    if not m:
        return ""
    q = m.group(1).replace("\n", " ").strip()
    return q[:180] + ("..." if len(q) > 180 else "")


def simplify_pointer(text):
    pointer = ""
    for line in text.splitlines():
        if "pointer_triad:" in line or line.startswith("source_pointer:"):
            pointer = line
            break
    if not pointer:
        return "没有看到 source pointer"
    source = re.search(r"(?:source_path|path)=([^ ]+)", pointer)
    start = re.search(r"start=([^ ]+)", pointer)
    end = re.search(r"end=([^ ]+)", pointer)
    h = re.search(r"(?:source_hash|hash)=([^ ]*)", pointer)
    quote = short_quote(pointer)
    if (h and not h.group(1)) or (start and start.group(1) == "-1"):
        status = "锚点异常：看起来不能直接回跳"
    else:
        status = "锚点可读：看起来能回源"
    return f"{status}; source={source.group(1) if source else '?'}; span={start.group(1) if start else '?'}-{end.group(1) if end else '?'}; quote={quote}"


def risk_lines(text):
    keep = []
    keywords = [
        "review_due:",
        "queue:",
        "FULL_AUDIT_OPEN",
        "open_gap:",
        "why:",
        "authority_boundary:",
        "feedback:",
        "group_id:",
        "anchor_problem_visibility",
        "no truth change",
        "not authority",
        "not support",
        "blocking",
        "for_review",
        "regressed",
    ]
    for line in text.splitlines():
        if any(k in line for k in keywords):
            keep.append(line)
    return keep[:8]


def view_card(label, artifact):
    text = artifact["rendered_text"]
    state = find_line(text, "state:")
    summary = find_line(text, "summary:")
    full_open = "是" if "FULL_AUDIT_OPEN" in text else "否"
    lines = [
        f"### {label}",
        "",
        f"- 状态：`{state or '未显示'}`",
        f"- 摘要：{summary or '未显示'}",
        f"- 是否打开 full audit：{full_open}",
        f"- 回源/锚点：{simplify_pointer(text)}",
    ]
    risks = risk_lines(text)
    if risks:
        lines.append("- 风险/提示：")
        for r in risks:
            lines.append(f"  - `{r}`")
    else:
        lines.append("- 风险/提示：没有明显风险提示")
    return "\n".join(lines)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    hidden = {row["quick_id"]: row for row in csv.DictReader((ROOT / "review_packet_quick_30" / "hidden_variant_map.csv").open("r", encoding="utf-8"))}
    artifacts = {
        "artifacts_baseline_full.json": load_artifacts("artifacts_baseline_full.json"),
        "artifacts_shell_core.json": load_artifacts("artifacts_shell_core.json"),
        "artifacts_shell_core_plus_recurrence.json": load_artifacts("artifacts_shell_core_plus_recurrence.json"),
    }

    map_rows = []
    card_lines = [
        "# VAKS 真人预演 8 题版",
        "",
        "你现在模拟 reviewer。每题只看 A/B 两版，不需要懂系统实现。",
        "",
        "每题只回答四件事：",
        "",
        "1. A 更清楚、B 更清楚、还是差不多？",
        "2. 有没有 serious 风险被藏起来？",
        "3. 你会不会想打开 full audit？",
        "4. 锚点/回源信息看起来顺不顺？",
        "",
        "先不要看 `hidden_map_after_done.csv`。做完 8 题后再看。",
        "",
    ]
    answer_rows = []

    for user_id, quick_id in CASES:
        row = hidden[quick_id]
        a = artifacts[row["first_artifact_file"]][row["case_id"]]
        b = artifacts[row["second_artifact_file"]][row["case_id"]]
        card_lines.extend(
            [
                f"## {user_id} ({row['case_id']})",
                "",
                f"场景标签：`{row['layer']}`；锚点状态：`{row['anchor_status']}`",
                "",
                view_card("View A", a),
                "",
                view_card("View B", b),
                "",
                "你的回答：A / B / 差不多；是否藏风险；是否想打开 full audit；备注。",
                "",
                "---",
                "",
            ]
        )
        answer_rows.append(
            {
                "user_id": user_id,
                "case_id": row["case_id"],
                "prefer_a_b_tie": "",
                "hidden_serious_risk_y_n_unsure": "",
                "would_open_full_audit_a_b_both_neither": "",
                "clickback_clear_a_b_both_neither": "",
                "burden_1_light_5_heavy": "",
                "notes": "",
            }
        )
        map_rows.append(
            {
                "user_id": user_id,
                "quick_id": quick_id,
                "case_id": row["case_id"],
                "view_a_variant": row["view_a_variant"],
                "view_b_variant": row["view_b_variant"],
                "layer": row["layer"],
                "anchor_status": row["anchor_status"],
            }
        )

    (OUT / "USER_TEST_8_CARDS.md").write_text("\n".join(card_lines), encoding="utf-8")

    with (OUT / "USER_TEST_8_ANSWER_SHEET.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(answer_rows[0].keys()))
        writer.writeheader()
        writer.writerows(answer_rows)

    with (OUT / "hidden_map_after_done.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(map_rows[0].keys()))
        writer.writeheader()
        writer.writerows(map_rows)

    (OUT / "README.md").write_text(
        """# VAKS 真人预演 8 题版

打开 `USER_TEST_8_CARDS.md`，从上往下看 8 题。

每题只要判断：

- A / B 哪个更清楚？
- 有没有 serious 风险被藏起来？
- 你会不会想打开 full audit？
- 锚点/回源信息顺不顺？

可以把答案填到 `USER_TEST_8_ANSWER_SHEET.csv`，也可以直接口头告诉 Codex。

先不要看 `hidden_map_after_done.csv`。做完再看它，才知道 A/B 分别是哪一版。

这只是单人预演，不是正式 human timing，不是 independent human oracle。
""",
        encoding="utf-8",
    )

    print(json.dumps({"output": str(OUT), "cases": len(CASES)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
