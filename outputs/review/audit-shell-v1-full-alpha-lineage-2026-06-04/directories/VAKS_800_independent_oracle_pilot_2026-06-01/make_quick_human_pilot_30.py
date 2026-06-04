import csv
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "review_packet_quick_30"


MAIN_TARGETS = {
    "ordinary_stable": 4,
    "action_challenge_conflict": 4,
    "anchor_problem": 3,
    "anchor_jumpback_failure": 2,
    "resolved_repeated_recurrence": 3,
    "authority_leak_bait": 2,
    "over_grouping_near_miss": 1,
    "serious_folded_violation": 1,
}

SIDE_TARGETS = {
    "resolved_repeated_recurrence": 5,
    "over_grouping_near_miss": 3,
    "serious_folded_violation": 2,
}


def load_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fieldnames):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_artifacts(filename):
    data = json.loads((ROOT / filename).read_text(encoding="utf-8"))
    return {row["case_id"]: row for row in data}


def unique_reviewer_a(rows):
    seen = {}
    for row in rows:
        if row["reviewer_id"] != "reviewer_a":
            continue
        seen.setdefault(row["case_id"], row)
    return list(seen.values())


def stratified_pick(rows, targets):
    by_layer = defaultdict(list)
    for row in rows:
        by_layer[row["layer"]].append(row)

    selected = []
    used = set()
    for layer, count in targets.items():
        pool = by_layer[layer]
        if len(pool) < count:
            raise RuntimeError(f"Not enough rows for {layer}: need {count}, have {len(pool)}")
        for row in pool[:count]:
            selected.append(row)
            used.add(row["case_id"])
    return selected


def artifact_text(artifacts, case_id):
    row = artifacts[case_id]
    return row["rendered_text"].strip()


def pointer_summary(text):
    pointer_line = ""
    for line in text.splitlines():
        if "pointer_triad:" in line or "source_path=" in line:
            pointer_line = line
            break
        if line.startswith("anchor_health:"):
            pointer_line = line
    source = re.search(r"source_path=([^ ]+)", pointer_line)
    start = re.search(r" start=([^ ]+)", pointer_line)
    end = re.search(r" end=([^ ]+)", pointer_line)
    quote = re.search(r' quote="(.*)"$', pointer_line)
    return {
        "source_path": source.group(1) if source else "",
        "start": start.group(1) if start else "",
        "end": end.group(1) if end else "",
        "quote": quote.group(1) if quote else "",
    }


def render_review_md(path, title, rows, artifact_maps):
    lines = [
        f"# {title}",
        "",
        "先不要看 `hidden_variant_map.csv`，做完这一轮再看。",
        "每个 assignment 先读 View A，再读 View B。用对应的 blank sheet 记录粗略耗时、是否会打开 full audit、有没有漏 serious 风险、click-back 是否顺、哪一版更轻、主观负担。",
        "",
    ]
    for idx, row in enumerate(rows, start=1):
        first_map = artifact_maps[row["first_artifact_file"]]
        second_map = artifact_maps[row["second_artifact_file"]]
        lines.extend(
            [
                f"## {row['quick_id']} / {row['case_id']}",
                "",
                f"Layer: `{row['layer']}` | Anchor status: `{row['anchor_status']}` | Pool: `{row['pool']}`",
                "",
                "### View A",
                "",
                "```text",
                artifact_text(first_map, row["case_id"]),
                "```",
                "",
                "### View B",
                "",
                "```text",
                artifact_text(second_map, row["case_id"]),
                "```",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def make_sheet_rows(rows, artifact_maps):
    out = []
    for row in rows:
        first_text = artifact_text(artifact_maps[row["first_artifact_file"]], row["case_id"])
        second_text = artifact_text(artifact_maps[row["second_artifact_file"]], row["case_id"])
        first_pointer = pointer_summary(first_text)
        second_pointer = pointer_summary(second_text)
        out.append(
            {
                "quick_id": row["quick_id"],
                "case_id": row["case_id"],
                "layer": row["layer"],
                "anchor_status": row["anchor_status"],
                "view_a_seconds": "",
                "view_b_seconds": "",
                "view_a_would_open_full_audit_y_n": "",
                "view_b_would_open_full_audit_y_n": "",
                "view_a_state_seen": "",
                "view_b_state_seen": "",
                "serious_risk_missed_y_n": "",
                "anchor_clickback_view_a_ok_fail_na": "",
                "anchor_clickback_view_b_ok_fail_na": "",
                "which_view_easier_a_b_tie": "",
                "burden_1_light_5_heavy": "",
                "notes": "",
                "view_a_source_path": first_pointer["source_path"],
                "view_b_source_path": second_pointer["source_path"],
            }
        )
    return out


def make_hidden_rows(rows):
    return [
        {
            "quick_id": row["quick_id"],
            "case_id": row["case_id"],
            "view_a_variant": row["order_first"],
            "view_b_variant": row["order_second"],
            "first_artifact_file": row["first_artifact_file"],
            "second_artifact_file": row["second_artifact_file"],
            "pool": row["pool"],
            "layer": row["layer"],
            "anchor_status": row["anchor_status"],
            "authority_family": row["authority_family"],
        }
        for row in rows
    ]


def add_quick_ids(rows, prefix):
    out = []
    for idx, row in enumerate(rows, start=1):
        row = dict(row)
        row["quick_id"] = f"{prefix}-{idx:03d}"
        out.append(row)
    return out


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    main_rows = add_quick_ids(
        stratified_pick(unique_reviewer_a(load_csv(ROOT / "review_packet" / "main_core_assignments.csv")), MAIN_TARGETS),
        "QUICK-MAIN",
    )
    side_rows = add_quick_ids(
        stratified_pick(unique_reviewer_a(load_csv(ROOT / "review_packet" / "side_recurrence_assignments.csv")), SIDE_TARGETS),
        "QUICK-SIDE",
    )

    artifact_maps = {
        "artifacts_baseline_full.json": load_artifacts("artifacts_baseline_full.json"),
        "artifacts_shell_core.json": load_artifacts("artifacts_shell_core.json"),
        "artifacts_shell_core_plus_recurrence.json": load_artifacts("artifacts_shell_core_plus_recurrence.json"),
    }

    render_review_md(OUT / "quick_main_core_review.md", "Quick Main Core Review: baseline_full vs shell_core", main_rows, artifact_maps)
    render_review_md(OUT / "quick_side_recurrence_review.md", "Quick Side Recurrence Review: shell_core vs shell_core_plus_recurrence", side_rows, artifact_maps)

    sheet_fields = [
        "quick_id",
        "case_id",
        "layer",
        "anchor_status",
        "view_a_seconds",
        "view_b_seconds",
        "view_a_would_open_full_audit_y_n",
        "view_b_would_open_full_audit_y_n",
        "view_a_state_seen",
        "view_b_state_seen",
        "serious_risk_missed_y_n",
        "anchor_clickback_view_a_ok_fail_na",
        "anchor_clickback_view_b_ok_fail_na",
        "which_view_easier_a_b_tie",
        "burden_1_light_5_heavy",
        "notes",
        "view_a_source_path",
        "view_b_source_path",
    ]
    write_csv(OUT / "quick_main_core_sheet_blank.csv", make_sheet_rows(main_rows, artifact_maps), sheet_fields)
    write_csv(OUT / "quick_side_recurrence_sheet_blank.csv", make_sheet_rows(side_rows, artifact_maps), sheet_fields)

    hidden_fields = [
        "quick_id",
        "case_id",
        "view_a_variant",
        "view_b_variant",
        "first_artifact_file",
        "second_artifact_file",
        "pool",
        "layer",
        "anchor_status",
        "authority_family",
    ]
    write_csv(OUT / "hidden_variant_map.csv", make_hidden_rows(main_rows + side_rows), hidden_fields)

    coverage = {
        "main_count": len(main_rows),
        "side_count": len(side_rows),
        "main_layers": dict(defaultdict(int)),
        "side_layers": dict(defaultdict(int)),
    }
    for row in main_rows:
        coverage["main_layers"][row["layer"]] = coverage["main_layers"].get(row["layer"], 0) + 1
    for row in side_rows:
        coverage["side_layers"][row["layer"]] = coverage["side_layers"].get(row["layer"], 0) + 1

    (OUT / "README_QUICK_30.md").write_text(
        """# Quick 30 Human Pilot

状态：本地单人预演，不是正式 human timing study。

## 怎么做

1. 打开 `quick_main_core_review.md`。
2. 每个 assignment 先读 View A，再读 View B。
3. 在 `quick_main_core_sheet_blank.csv` 里记录粗略秒数、是否会打开 full audit、看到的 state、click-back 结果、哪一版更轻、主观负担和备注。
4. 然后打开 `quick_side_recurrence_review.md`，填写 `quick_side_recurrence_sheet_blank.csv`。
5. 全部做完后再打开 `hidden_variant_map.csv`，看 View A / View B 分别是哪一个 variant。

表格里的 `view_a_source_path` / `view_b_source_path` 如果为空，表示那一侧没有暴露出可解析 pointer；可以把 click-back 记为 `na` 或在备注里写明。

## 范围

- 主预演：20 个 case，`baseline_full` vs `shell_core`。
- 侧预演：10 个 recurrence-heavy case，`shell_core` vs `shell_core_plus_recurrence`。

## 这轮能回答什么

- 人审流程顺不顺。
- `shell_core` 是否真的更轻，同时没有藏住 serious 风险。
- click-back 字段对真人 reviewer 是否足够好理解。
- recurrence grouping 是帮忙，还是制造误解。

## 这轮不能证明什么

- 这不是双人复核。
- 这不是产品级 click-back 验证。
- 这不是 independent human oracle。
- 不能写进主库 operation convention。
""",
        encoding="utf-8",
    )

    (OUT / "quick_coverage.json").write_text(json.dumps(coverage, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(OUT), **coverage}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
