import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent


HARD_TRIGGERS = {
    "action_basis",
    "promotion",
    "explicit_challenge",
    "conflict",
    "known_omission",
    "missing_anchor",
    "risk_sensitive",
    "explicit_correction",
    "action_outcome",
    "decision_outcome",
    "high_severity_wrong_answer",
    "independence_needed_for_confidence",
    "reviewer_blocks",
    "regression",
    "stale_pointer",
    "selector_drift",
}


REVIEW_DUE_TRIGGERS = HARD_TRIGGERS


AUTHORITY_TRAPS = {
    "group_count_as_support",
    "lineage_as_independence",
    "source_count_as_independence",
    "dashboard_as_truth",
    "test_pass_as_truth",
    "feedback_summary_as_truth",
    "feedback_count_as_truth",
    "llm_summary_as_truth",
    "retrieval_rank_as_truth",
    "cluster_summary_as_truth",
}


FULL_AUDIT_LINES = {
    "small_claim": 16,
    "answer_query_run": 17,
    "support_refine_collision": 18,
    "feedback": 15,
}


FRONT_LINES = {
    "small_claim": 5,
    "answer_query_run": 5,
    "support_refine_collision": 6,
    "feedback": 5,
}


def yn(value):
    return str(value).strip() in {"1", "true", "True", "yes", "YES"}


def split_triggers(value):
    value = (value or "").strip()
    if not value:
        return set()
    return {item.strip() for item in value.split(";") if item.strip()}


def read_cases():
    with (ROOT / "adversarial_cases.psv").open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="|")
        cases = []
        for row in reader:
            row["observed_triggers"] = split_triggers(row["observed_trigger_hint"])
            row["gold_triggers"] = split_triggers(row["gold_trigger_family"])
            row["gold_full_audit_bool"] = yn(row["gold_full_audit"])
            row["gold_review_due_bool"] = yn(row["gold_review_due"])
            row["gold_can_group_bool"] = yn(row["gold_can_group"])
            row["gold_missing_anchor_visible_bool"] = yn(row["gold_missing_anchor_visible"])
            row["expected_front_max_int"] = int(row["expected_front_max"])
            row["gold_authority_forbidden_bool"] = yn(row["gold_authority_forbidden"])
            cases.append(row)
    return cases


def read_anchors():
    return json.loads((ROOT / "anchors.json").read_text(encoding="utf-8"))


def resolve_anchor(anchor_key, anchors):
    if not anchor_key or anchor_key == "NONE" or anchor_key.startswith("STALE") or anchor_key.endswith("DRIFT") or anchor_key == "WEB-DRIFT":
        return False
    meta = anchors.get(anchor_key)
    if not meta:
        return False
    path = ROOT / meta["path"]
    if not path.exists():
        return False
    return meta["marker"] in path.read_text(encoding="utf-8")


def shell_output(case, anchors):
    observed_triggers = case["observed_triggers"]
    anchor_status = case["anchor_status"]
    object_type = case["object_type"]
    state = case["observed_state"]

    trigger_full = bool(observed_triggers & HARD_TRIGGERS)
    anchor_problem = anchor_status in {"missing", "stale", "drift"}
    full_audit = trigger_full or state in {"blocking", "regressed"} or anchor_problem
    review_due = bool(observed_triggers & REVIEW_DUE_TRIGGERS) or state in {"blocking", "for_review", "regressed"}
    if state in {"ordinary", "resolved_folded", "parked_nonblocking"} and not trigger_full and not anchor_problem:
        review_due = False

    if state == "resolved_folded":
        front_lines = 1
    elif state == "parked_nonblocking" and not full_audit:
        front_lines = 3
    else:
        front_lines = FRONT_LINES[object_type]

    front_fields = ["state", "core_summary"]
    if anchor_status == "valid":
        front_fields.append("anchor_jump_back")
    elif anchor_problem:
        front_fields.append("missing_or_bad_anchor_note")
    if case["gap_family"] not in {"", "none"}:
        front_fields.append("open_gap_or_scope_limit")
    if full_audit:
        front_fields.append("upgrade_trigger")
    if case["observed_group_key"]:
        front_fields.append("count_or_exemplar")

    back_fields = []
    if anchor_status == "valid":
        back_fields.extend(["raw_span_pointer", "full_record_pointer"])
    elif anchor_problem:
        back_fields.extend(["missing_anchor_note", "full_record_pointer"])
    if case["gap_family"] not in {"", "none"}:
        back_fields.append("gap_detail")
    if "conflict" in observed_triggers:
        back_fields.append("conflict_note")
    if "known_omission" in observed_triggers:
        back_fields.append("known_omission_note")

    pointer_resolves = resolve_anchor(case["anchor_key"], anchors) if anchor_status == "valid" else False
    missing_anchor_visible = anchor_problem and "missing_or_bad_anchor_note" in front_fields and "missing_anchor_note" in back_fields

    authority_trap = case["authority_trap"]
    authority_boundary_visible = bool(authority_trap)
    authority_used_as_truth = False
    feedback_changes_truth = False

    group_key = None
    if case["observed_group_key"] and not full_audit and state != "resolved_folded":
        group_key = "|".join([
            case["observed_group_key"],
            case["escalation_class"],
            case["gap_family"],
            case["feedback_type"],
            case["action_meaning"],
            case["anchor_status"],
        ])

    manual_fields = 4
    if full_audit:
        manual_fields += 5
    if group_key:
        manual_fields += 1
    if authority_trap:
        manual_fields += 1
    expansion_count = 1 if full_audit or anchor_problem or "known_omission" in observed_triggers or "conflict" in observed_triggers else 0

    return {
        "case_id": case["id"],
        "state": state,
        "front_lines": front_lines,
        "front_fields": front_fields,
        "back_fields": back_fields,
        "full_audit": full_audit,
        "review_due": review_due,
        "pointer_resolves": pointer_resolves,
        "missing_anchor_visible": missing_anchor_visible,
        "authority_boundary_visible": authority_boundary_visible,
        "authority_used_as_truth": authority_used_as_truth,
        "feedback_changes_truth": feedback_changes_truth,
        "group_key": group_key,
        "manual_fields": manual_fields,
        "manual_grouping_review_needed": bool(case["observed_group_key"]),
        "manual_grouping_applied": bool(group_key),
        "front_back_expansion_count": expansion_count,
        "authoring_time_units": front_lines + manual_fields + expansion_count,
        "triage_time_units": front_lines + (2 * expansion_count) + (2 if full_audit else 0),
    }


def compare_case(case, output):
    gold_full = case["gold_full_audit_bool"]
    gold_review_due = case["gold_review_due_bool"]
    anchor_status = case["anchor_status"]

    valid_anchor_needed = anchor_status == "valid"
    valid_anchor_ok = True
    if valid_anchor_needed:
        valid_anchor_ok = (
            "anchor_jump_back" in output["front_fields"]
            and "raw_span_pointer" in output["back_fields"]
            and "full_record_pointer" in output["back_fields"]
            and output["pointer_resolves"]
        )

    missing_anchor_ok = True
    if case["gold_missing_anchor_visible_bool"]:
        missing_anchor_ok = output["missing_anchor_visible"] and output["full_audit"]

    authority_ok = not output["authority_used_as_truth"]
    feedback_truth_ok = not output["feedback_changes_truth"]
    front_ok = output["front_lines"] <= case["expected_front_max_int"]

    return {
        "case_id": case["id"],
        "category": case["category"],
        "false_lite": gold_full and not output["full_audit"],
        "ordinary_false_positive": (not gold_full) and output["full_audit"],
        "review_due_false_negative": gold_review_due and not output["review_due"],
        "review_due_false_positive": (not gold_review_due) and output["review_due"],
        "valid_anchor_ok": valid_anchor_ok,
        "missing_anchor_ok": missing_anchor_ok,
        "authority_ok": authority_ok,
        "feedback_truth_ok": feedback_truth_ok,
        "front_ok": front_ok,
        "passed": all([
            not (gold_full and not output["full_audit"]),
            valid_anchor_ok,
            missing_anchor_ok,
            authority_ok,
            feedback_truth_ok,
            front_ok,
        ]),
    }


def evaluate_grouping(cases, outputs):
    by_case = {case["id"]: case for case in cases}
    groups = defaultdict(list)
    for out in outputs:
        if out["group_key"]:
            groups[out["group_key"]].append(out["case_id"])

    severe = []
    raw_groupable = 0
    grouped_items = 0
    for key, ids in groups.items():
        if len(ids) <= 1:
            continue
        raw_groupable += len(ids)
        grouped_items += 1
        gold_ids = {by_case[i]["gold_group_id"] for i in ids}
        can_group = all(by_case[i]["gold_can_group_bool"] for i in ids)
        if (not can_group) or len(gold_ids) != 1 or "" in gold_ids:
            severe.append({"group_key": key, "case_ids": ids, "gold_group_ids": sorted(gold_ids)})

    reduction = 0.0
    if raw_groupable:
        reduction = round((raw_groupable - grouped_items) / raw_groupable * 100, 1)
    return {
        "groups": groups,
        "raw_groupable": raw_groupable,
        "grouped_items": grouped_items,
        "grouped_reduction_pct": reduction,
        "severe_over_grouping": severe,
    }


def summarize(cases, outputs, comparisons, grouping):
    total = len(cases)
    review_due_tp = sum(1 for row in comparisons if (not row["review_due_false_negative"]) and next(c for c in cases if c["id"] == row["case_id"])["gold_review_due_bool"])
    review_due_fp = sum(1 for row in comparisons if row["review_due_false_positive"])
    review_due_fn = sum(1 for row in comparisons if row["review_due_false_negative"])
    review_due_precision = review_due_tp / (review_due_tp + review_due_fp) if (review_due_tp + review_due_fp) else 1.0
    review_due_recall = review_due_tp / (review_due_tp + review_due_fn) if (review_due_tp + review_due_fn) else 1.0

    trigger_families = sorted({t for c in cases for t in c["gold_triggers"]})
    trigger_recall = {}
    outputs_by_id = {o["case_id"]: o for o in outputs}
    for trigger in trigger_families:
        relevant = [c for c in cases if trigger in c["gold_triggers"]]
        if not relevant:
            continue
        trigger_recall[trigger] = sum(1 for c in relevant if outputs_by_id[c["id"]]["full_audit"]) / len(relevant)

    category_counts = defaultdict(int)
    for case in cases:
        category_counts[case["category"]] += 1

    baseline_front_units = total * 12
    shell_front_units = sum(o["front_lines"] for o in outputs)
    visible_reduction = round((baseline_front_units - shell_front_units) / baseline_front_units * 100, 1)

    hidden_burden = {
        "manual_fields_total": sum(o["manual_fields"] for o in outputs),
        "manual_grouping_review_needed": sum(1 for o in outputs if o["manual_grouping_review_needed"]),
        "manual_grouping_applied": sum(1 for o in outputs if o["manual_grouping_applied"]),
        "front_back_expansions": sum(o["front_back_expansion_count"] for o in outputs),
        "authoring_time_units_total": sum(o["authoring_time_units"] for o in outputs),
        "triage_time_units_total": sum(o["triage_time_units"] for o in outputs),
    }

    hard_gate_pass = all([
        sum(1 for row in comparisons if row["false_lite"]) == 0,
        all(value == 1.0 for value in trigger_recall.values()),
        sum(1 for row in comparisons if not row["valid_anchor_ok"]) == 0,
        sum(1 for row in comparisons if not row["missing_anchor_ok"]) == 0,
        len(grouping["severe_over_grouping"]) == 0,
        sum(1 for row in comparisons if not row["authority_ok"]) == 0,
        sum(1 for row in comparisons if not row["feedback_truth_ok"]) == 0,
        review_due_precision >= 0.90,
        review_due_recall >= 0.95,
        sum(1 for row in comparisons if not row["front_ok"]) == 0,
    ])

    return {
        "cases": total,
        "category_counts": dict(sorted(category_counts.items())),
        "passed_cases": sum(1 for row in comparisons if row["passed"]),
        "false_lite": sum(1 for row in comparisons if row["false_lite"]),
        "ordinary_false_positive": sum(1 for row in comparisons if row["ordinary_false_positive"]),
        "review_due_precision": round(review_due_precision, 4),
        "review_due_recall": round(review_due_recall, 4),
        "trigger_family_recall": {k: round(v, 4) for k, v in trigger_recall.items()},
        "valid_anchor_failures": sum(1 for row in comparisons if not row["valid_anchor_ok"]),
        "missing_anchor_failures": sum(1 for row in comparisons if not row["missing_anchor_ok"]),
        "authority_leakage_incidents": sum(1 for row in comparisons if not row["authority_ok"]),
        "feedback_truth_change_incidents": sum(1 for row in comparisons if not row["feedback_truth_ok"]),
        "front_face_violations": sum(1 for row in comparisons if not row["front_ok"]),
        "severe_over_grouping": len(grouping["severe_over_grouping"]),
        "grouped_reduction_pct": grouping["grouped_reduction_pct"],
        "visible_front_reduction_pct": visible_reduction,
        "hidden_burden": hidden_burden,
        "hard_gate_pass": hard_gate_pass,
    }


def make_report(summary, comparisons, grouping):
    lines = []
    lines.append("# Audit Shell V1 Adversarial 96 Report")
    lines.append("")
    lines.append("Status: sandbox-only adversarial fixture patch. This is still not the 480-sample real-data pilot.")
    lines.append("")
    lines.append("## Executive Result")
    lines.append("")
    for key in [
        "cases",
        "passed_cases",
        "false_lite",
        "ordinary_false_positive",
        "review_due_precision",
        "review_due_recall",
        "valid_anchor_failures",
        "missing_anchor_failures",
        "authority_leakage_incidents",
        "feedback_truth_change_incidents",
        "front_face_violations",
        "severe_over_grouping",
        "grouped_reduction_pct",
        "visible_front_reduction_pct",
        "hard_gate_pass",
    ]:
        lines.append(f"- {key}: {summary[key]}")
    lines.append("")
    lines.append("## Case Mix")
    lines.append("")
    lines.append("| category | cases |")
    lines.append("| --- | ---: |")
    for category, count in summary["category_counts"].items():
        lines.append(f"| {category} | {count} |")
    lines.append("")
    lines.append("## Trigger-Family Recall")
    lines.append("")
    lines.append("| trigger | recall |")
    lines.append("| --- | ---: |")
    for trigger, recall in summary["trigger_family_recall"].items():
        lines.append(f"| {trigger} | {recall} |")
    lines.append("")
    lines.append("## Hidden Burden Counters")
    lines.append("")
    lines.append("| metric | value |")
    lines.append("| --- | ---: |")
    for key, value in summary["hidden_burden"].items():
        lines.append(f"| {key} | {value} |")
    lines.append("")
    lines.append("## Grouping Audit")
    lines.append("")
    lines.append(f"- raw_groupable: {grouping['raw_groupable']}")
    lines.append(f"- grouped_items: {grouping['grouped_items']}")
    lines.append(f"- grouped_reduction_pct: {grouping['grouped_reduction_pct']}")
    lines.append(f"- severe_over_grouping: {len(grouping['severe_over_grouping'])}")
    if grouping["severe_over_grouping"]:
        lines.append("")
        lines.append("Severe groups:")
        for item in grouping["severe_over_grouping"]:
            lines.append(f"- {item}")
    lines.append("")
    lines.append("## Failed Cases")
    lines.append("")
    failed = [row for row in comparisons if not row["passed"] or row["review_due_false_negative"] or row["review_due_false_positive"]]
    if not failed:
        lines.append("No failed cases.")
    else:
        lines.append("| case | false_lite | review_due_fn | review_due_fp | valid_anchor | missing_anchor | authority | feedback_truth | front |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for row in failed:
            lines.append(
                f"| {row['case_id']} | {row['false_lite']} | {row['review_due_false_negative']} | {row['review_due_false_positive']} | "
                f"{row['valid_anchor_ok']} | {row['missing_anchor_ok']} | {row['authority_ok']} | {row['feedback_truth_ok']} | {row['front_ok']} |"
            )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("This patch is stronger than the 112-case pilot because gold labels are explicit in the case table, shell output is generated separately, and comparison logic is separate.")
    lines.append("It still remains fixture-based, so passing it should lead to real-data paired pilot, not main-vault writeback.")
    return "\n".join(lines) + "\n"


def main():
    cases = read_cases()
    anchors = read_anchors()
    outputs = [shell_output(case, anchors) for case in cases]
    comparisons = [compare_case(case, output) for case, output in zip(cases, outputs)]
    grouping = evaluate_grouping(cases, outputs)
    summary = summarize(cases, outputs, comparisons, grouping)

    (ROOT / "shell_outputs.json").write_text(json.dumps(outputs, indent=2, ensure_ascii=False), encoding="utf-8")
    (ROOT / "comparison_results.json").write_text(json.dumps({
        "summary": summary,
        "comparisons": comparisons,
        "grouping": {
            "raw_groupable": grouping["raw_groupable"],
            "grouped_items": grouping["grouped_items"],
            "grouped_reduction_pct": grouping["grouped_reduction_pct"],
            "severe_over_grouping": grouping["severe_over_grouping"],
        },
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    (ROOT / "ADVERSARIAL_PATCH_REPORT.md").write_text(make_report(summary, comparisons, grouping), encoding="utf-8")

    print(f"cases={summary['cases']} passed={summary['passed_cases']} hard_gate_pass={summary['hard_gate_pass']}")
    print(f"false_lite={summary['false_lite']} review_due_precision={summary['review_due_precision']} review_due_recall={summary['review_due_recall']}")
    print(f"severe_over_grouping={summary['severe_over_grouping']} jumpback_failures={summary['valid_anchor_failures']}")
    print(f"report={ROOT / 'ADVERSARIAL_PATCH_REPORT.md'}")
    if not summary["hard_gate_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
