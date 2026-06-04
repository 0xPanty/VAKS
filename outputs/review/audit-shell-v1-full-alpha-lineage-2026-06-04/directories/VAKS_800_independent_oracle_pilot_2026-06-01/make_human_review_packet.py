import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "review_packet"


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_csv(path, rows, fieldnames):
    with Path(path).open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def add_bucket(selected, cases, count, predicate):
    seen = {case["id"] for case in selected}
    for case in cases:
        if len([c for c in selected if predicate(c)]) >= count:
            break
        if case["id"] not in seen and predicate(case):
            selected.append(case)
            seen.add(case["id"])


def fill_to(selected, cases, total):
    seen = {case["id"] for case in selected}
    for case in cases:
        if len(selected) >= total:
            break
        if case["id"] not in seen:
            selected.append(case)
            seen.add(case["id"])


def choose_main_cases(cases, gold):
    selected = []
    add_bucket(selected, cases, 22, lambda c: c["layer"] == "ordinary_stable" and gold[c["id"]]["ordinary"])
    add_bucket(selected, cases, 22, lambda c: gold[c["id"]]["serious"] and c["layer"] in {"action_challenge_conflict", "omission_insufficiency_ambiguity", "false_lite_trap", "review_due_trap"})
    add_bucket(selected, cases, 10, lambda c: c["layer"] == "anchor_problem")
    add_bucket(selected, cases, 8, lambda c: c["layer"] == "anchor_jumpback_failure")
    add_bucket(selected, cases, 14, lambda c: gold[c["id"]]["resolved"])
    add_bucket(selected, cases, 14, lambda c: gold[c["id"]]["can_group"])
    add_bucket(selected, cases, 10, lambda c: bool(c.get("authority_family")))
    add_bucket(selected, cases, 10, lambda c: c["layer"] == "over_grouping_near_miss")
    add_bucket(selected, cases, 10, lambda c: c["layer"] == "serious_folded_violation")
    fill_to(selected, cases, 120)
    return selected[:120]


def choose_side_recurrence_cases(cases, gold):
    selected = []
    add_bucket(selected, cases, 24, lambda c: gold[c["id"]]["can_group"])
    add_bucket(selected, cases, 12, lambda c: c["layer"] == "over_grouping_near_miss")
    add_bucket(selected, cases, 8, lambda c: c["layer"] == "serious_folded_violation")
    add_bucket(selected, cases, 8, lambda c: c.get("recurrence_key") and c.get("anchor_status") != "valid")
    add_bucket(selected, cases, 8, lambda c: c.get("recurrence_key") and bool(c.get("authority_family")))
    fill_to(selected, [c for c in cases if c.get("recurrence_key")], 60)
    return selected[:60]


def category_stats(cases, gold):
    return {
        "unique_cases": len(cases),
        "resolved_cases": sum(1 for c in cases if gold[c["id"]]["resolved"]),
        "can_group_cases": sum(1 for c in cases if gold[c["id"]]["can_group"]),
        "non_valid_anchor_cases": sum(1 for c in cases if c.get("anchor_status") != "valid"),
        "authority_family_cases": sum(1 for c in cases if c.get("authority_family")),
        "anchor_jumpback_failure_layer": sum(1 for c in cases if c["layer"] == "anchor_jumpback_failure"),
        "over_grouping_near_miss_layer": sum(1 for c in cases if c["layer"] == "over_grouping_near_miss"),
        "serious_folded_violation_layer": sum(1 for c in cases if c["layer"] == "serious_folded_violation"),
        "layer_counts": dict(Counter(c["layer"] for c in cases)),
        "pool_counts": dict(Counter(c["pool"] for c in cases)),
    }


def make_assignments(cases, packet_name, variants):
    rows = []
    timing = []
    adjudication = []
    for idx, case in enumerate(cases):
        order = variants if idx % 2 == 0 else list(reversed(variants))
        for reviewer in ["reviewer_a", "reviewer_b"]:
            aid = f"{packet_name.upper()}-{idx + 1:03d}-{reviewer}"
            rows.append(
                {
                    "assignment_id": aid,
                    "case_id": case["id"],
                    "reviewer_id": reviewer,
                    "order_first": order[0],
                    "order_second": order[1],
                    "pool": case["pool"],
                    "layer": case["layer"],
                    "anchor_status": case.get("anchor_status", ""),
                    "authority_family": case.get("authority_family", ""),
                    "expected_state_hidden_for_reviewer": "",
                    "first_artifact_file": f"artifacts_{order[0]}.json",
                    "second_artifact_file": f"artifacts_{order[1]}.json",
                }
            )
            timing.append(
                {
                    "assignment_id": aid,
                    "case_id": case["id"],
                    "reviewer_id": reviewer,
                    "variant_reviewed": "",
                    "started_at": "",
                    "ended_at": "",
                    "triage_time_seconds": "",
                    "opened_full_audit": "",
                    "state_selected": "",
                    "review_due_selected": "",
                    "anchor_click_success": "",
                    "grouping_helped_or_hurt": "",
                    "error_or_missed_serious": "",
                    "subjective_burden_1_low_5_high": "",
                    "notes": "",
                }
            )
        adjudication.append(
            {
                "case_id": case["id"],
                "reviewer_a_state": "",
                "reviewer_b_state": "",
                "agreement": "",
                "adjudicated_state": "",
                "adjudicated_review_due": "",
                "adjudicated_anchor_ok": "",
                "adjudicated_grouping_ok": "",
                "adjudicator_notes": "",
            }
        )
    return rows, timing, adjudication


def write_packet(prefix, cases, variants):
    assignments, timing, adjudication = make_assignments(cases, prefix, variants)
    write_csv(OUT / f"{prefix}_assignments.csv", assignments, list(assignments[0].keys()))
    write_csv(OUT / f"{prefix}_timing_sheet_blank.csv", timing, list(timing[0].keys()))
    write_csv(OUT / f"{prefix}_dual_review_adjudication_blank.csv", adjudication, list(adjudication[0].keys()))
    return {"assignments": len(assignments), "unique_cases": len(cases), "variants": variants}


def main():
    OUT.mkdir(exist_ok=True)
    cases = read_json(ROOT / "candidate_cases.json")
    gold = read_json(ROOT / "gold_oracle_frozen.json")
    main_cases = choose_main_cases(cases, gold)
    side_cases = choose_side_recurrence_cases(cases, gold)
    main_info = write_packet("main_core", main_cases, ["baseline_full", "shell_core"])
    side_info = write_packet("side_recurrence", side_cases, ["shell_core", "shell_core_plus_recurrence"])

    summary = {
        "timing_prefilled": False,
        "main_core": {**main_info, "coverage": category_stats(main_cases, gold)},
        "side_recurrence": {**side_info, "coverage": category_stats(side_cases, gold)},
        "note": "Review sheets are intentionally blank. Expected state/gold is not exposed in assignment rows.",
    }
    (OUT / "packet_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "README_HUMAN_REVIEW.md").write_text(
        "\n".join(
            [
                "# Human Review Packet",
                "",
                "Timing and dual-review fields are intentionally blank. Do not prefill human timing or adjudication results.",
                "",
                "## Main Core Packet",
                "",
                "`main_core_*` compares `baseline_full` vs `shell_core` over 120 stratified cases. It covers ordinary stable, serious, resolved, recurrence-capable, bad-anchor, authority-bait, over-grouping-near-miss, and serious-folded-violation samples.",
                "",
                "## Side Recurrence Packet",
                "",
                "`side_recurrence_*` compares `shell_core` vs `shell_core_plus_recurrence` over 60 recurrence-heavy cases. Use it only to judge recurrence bundle value and misunderstanding risk.",
                "",
                "Record triage time, full-audit open, state/review_due choice, anchor click success, grouping helped/hurt, missed serious, and subjective burden.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    # Compatibility copies for older package readers.
    (OUT / "review_assignments.csv").write_text((OUT / "main_core_assignments.csv").read_text(encoding="utf-8"), encoding="utf-8")
    (OUT / "timing_sheet_blank.csv").write_text((OUT / "main_core_timing_sheet_blank.csv").read_text(encoding="utf-8"), encoding="utf-8")
    (OUT / "dual_review_adjudication_blank.csv").write_text((OUT / "main_core_dual_review_adjudication_blank.csv").read_text(encoding="utf-8"), encoding="utf-8")
    print(json.dumps({"main_core": main_info, "side_recurrence": side_info, "timing_prefilled": False}, indent=2))


if __name__ == "__main__":
    main()
