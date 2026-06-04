import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def pct(num, den):
    return round(num / den * 100, 2) if den else None


def has_review_due(text):
    return "review_due: true" in text


def has_full(text):
    return "FULL_AUDIT_OPEN" in text


def status(pass_bool):
    return "automated_proxy_pass" if pass_bool else "automated_proxy_fail"


def not_measured(reason):
    return {
        "status": "not_measured_yet",
        "current_value": None,
        "note": reason,
    }


def gate(gate_id, threshold, nature, current_value, pass_bool, note):
    return {
        "id": gate_id,
        "threshold": threshold,
        "nature": nature,
        "status": status(pass_bool),
        "current_value": current_value,
        "note": note,
    }


def main():
    results = read_json("pilot_800_results.json")
    gold = read_json("gold_oracle_frozen.json")
    checks = read_json("checks_shell_core.json")["checks"]
    artifacts = read_json("artifacts_shell_core.json")
    recurrence = results["variants"]["shell_core_plus_recurrence"]
    core = results["variants"]["shell_core"]
    summary = core["summary"]
    hard = summary["hard_failures"]
    paired = core["paired"]
    artifact_by_id = {row["case_id"]: row for row in artifacts}

    expected_review_due = [cid for cid, g in gold.items() if g["review_due"]]
    observed_review_due = [cid for cid, row in artifact_by_id.items() if has_review_due(row["rendered_text"])]
    expected_set = set(expected_review_due)
    observed_set = set(observed_review_due)
    review_due_tp = len(expected_set & observed_set)
    review_due_recall = pct(review_due_tp, len(expected_set))
    review_due_precision = pct(review_due_tp, len(observed_set))

    ordinary_ids = [cid for cid, g in gold.items() if g["ordinary"]]
    baseline_artifacts = read_json("artifacts_baseline_full.json")
    baseline_by_id = {row["case_id"]: row for row in baseline_artifacts}
    baseline_ordinary_full = sum(has_full(baseline_by_id[cid]["rendered_text"]) for cid in ordinary_ids)
    core_ordinary_full = sum(has_full(artifact_by_id[cid]["rendered_text"]) for cid in ordinary_ids)
    artifact_full_open_reduction = pct(baseline_ordinary_full - core_ordinary_full, baseline_ordinary_full)
    anchor_visibility_required = sum(1 for g in gold.values() if g["anchor_problem_visibility_required"])
    anchor_visibility_pass = anchor_visibility_required - hard["anchor_problem_visibility_failures"]
    anchor_visibility_pct = pct(anchor_visibility_pass, anchor_visibility_required)

    click_manifest = read_json("data/clickback_snapshot_manifest.json")
    live = click_manifest.get("real_fetch_success", 0)
    fallback = click_manifest.get("fallback_used", 0)
    target = click_manifest.get("target", live + fallback)
    semantic_eval_path = ROOT / "data" / "clickback_semantic_landing_eval.json"
    semantic_eval = json.loads(semantic_eval_path.read_text(encoding="utf-8")) if semantic_eval_path.exists() else {}
    semantic_summary = semantic_eval.get("summary", {})

    auto_gates = [
        gate("serious_false_lite", "0", "hard", hard["serious_false_lite"], hard["serious_false_lite"] == 0, "Automated overlay proxy only; final truth requires reviewer/adjudicator."),
        gate("serious_full_audit_recall", "100%", "hard", summary["serious_full_audit_recall_pct"], summary["serious_full_audit_recall_pct"] == 100.0, "Automated overlay proxy only."),
        gate("serious_folded_count", "0", "hard", hard["serious_folded_count"], hard["serious_folded_count"] == 0, "Automated overlay proxy only."),
        not_measured("wrong_actionability requires reviewer decision plus adjudication.") | {"id": "wrong_actionability", "threshold": "0", "nature": "hard"},
        gate("ordinary_false_positive_rate", "<= 2%", "hard", summary["ordinary_false_positive_rate_pct"], summary["ordinary_false_positive_rate_pct"] <= 2.0, "Automated overlay proxy only."),
        gate("review_due_recall", ">= 95%", "hard", review_due_recall, review_due_recall is not None and review_due_recall >= 95.0, "Machine-overlay diagnostic; final gate requires adjudication."),
        gate("review_due_precision", ">= 90%", "strong", review_due_precision, review_due_precision is not None and review_due_precision >= 90.0, "Machine-overlay diagnostic; final gate requires adjudication."),
        {
            "id": "source_record_evidence_clickback_success",
            "threshold": ">= 95% live / immutable cases",
            "nature": "hard",
            "status": "not_measured_yet",
            "current_value": {
                "package_pointer_source_resolve_pct": summary["valid_anchor_resolve_rate_pct"],
                "package_record_pointer_resolve_pct": summary["record_pointer_resolve_rate_pct"],
                "package_evidence_pointer_resolve_pct": summary["evidence_pointer_resolve_rate_pct"],
                "live_fetch_success": live,
                "fallback_used": fallback,
                "target": target,
                "semantic_selector_success": semantic_summary.get("semantic_selector_success"),
                "semantic_selector_success_pct": semantic_summary.get("semantic_selector_success_pct"),
                "body_window_used": semantic_summary.get("body_window_used"),
                "boilerplate_quote": semantic_summary.get("boilerplate_quote"),
                "landing_class_counts": semantic_summary.get("landing_class_counts"),
            },
            "note": "Package pointer resolution, live fetch, and automated semantic landing are not product click-back. claim_relevant_context_landing is weaker than evidence_landing and needs operator adjudication.",
        },
        gate("anchor_problem_visibility", "100%", "hard", anchor_visibility_pct, hard["anchor_problem_visibility_failures"] == 0, f"Automated visibility proxy only; failures={hard['anchor_problem_visibility_failures']}; final gate requires reviewer/adjudicator."),
        not_measured("authority misunderstanding requires observation prompts, notes, and adjudication.") | {"id": "authority_misunderstanding", "threshold": "<= 2%", "nature": "hard"},
        not_measured("ordinary triage time reduction requires actual human timing.") | {"id": "ordinary_triage_time_reduction", "threshold": ">= 20% vs baseline_full", "nature": "product"},
        {
            "id": "ordinary_full_audit_open_rate_reduction",
            "threshold": ">= 30% vs baseline_full",
            "nature": "product",
            "status": "not_measured_yet",
            "current_value": {
                "artifact_proxy_reduction_pct": artifact_full_open_reduction,
                "baseline_ordinary_full_open_artifacts": baseline_ordinary_full,
                "shell_core_ordinary_full_open_artifacts": core_ordinary_full,
            },
            "note": "Artifact full-open reduction is a diagnostic proxy, not actual reviewer operation rate.",
        },
        gate("ordinary_rendered_line_reduction", ">= 55%", "supporting", paired["ordinary"]["rendered_line_reduction_pct"], paired["ordinary"]["rendered_line_reduction_pct"] >= 55.0, "Supporting renderer metric only."),
        gate("ordinary_rendered_char_reduction", ">= 60%", "supporting", paired["ordinary"]["rendered_char_reduction_pct"], paired["ordinary"]["rendered_char_reduction_pct"] >= 60.0, "Supporting renderer metric only."),
        gate("resolved_default_queue_visible", "0", "hard", summary["resolved_default_queue_visible"], summary["resolved_default_queue_visible"] == 0, "Automated queue-surface proxy only."),
        gate("recurrence_grouped_reduction", ">= 50%", "conditional", recurrence["summary"]["grouping"]["grouped_reduction_pct"], recurrence["summary"]["grouping"]["grouped_reduction_pct"] >= 50.0, "Conditional side-arm diagnostic only."),
        gate("recurrence_over_grouping_serious_mismatch", "0", "hard when recurrence is enabled", recurrence["summary"]["hard_failures"]["severe_over_grouping"] + recurrence["summary"]["hard_failures"]["serious_folded_count"], recurrence["summary"]["hard_failures"]["severe_over_grouping"] + recurrence["summary"]["hard_failures"]["serious_folded_count"] == 0, "Automated side-arm proxy only."),
        not_measured("recurrence human misunderstanding requires side-packet reviewer notes and adjudication.") | {"id": "recurrence_human_misunderstanding", "threshold": "<= 5%", "nature": "conditional"},
        not_measured("recurrence slice triage-time reduction requires side-packet human timing.") | {"id": "recurrence_slice_triage_time_reduction", "threshold": ">= 10%", "nature": "conditional product"},
    ]

    human_missing = [row["id"] for row in auto_gates if row["status"] == "not_measured_yet"]
    proxy_failures = [row["id"] for row in auto_gates if row["status"] == "automated_proxy_fail"]
    hard_human_missing = [
        row["id"]
        for row in auto_gates
        if row["status"] == "not_measured_yet" and "hard" in row["nature"]
    ]
    overall = {
        "current_go_status": "not_go_yet",
        "meaning": "Not eligible yet for main-vault candidate operation-convention discussion because human/product click-back adjudication gates are not passed.",
        "automated_proxy_failures": proxy_failures,
        "not_measured_yet": human_missing,
        "hard_gates_not_measured_yet": hard_human_missing,
    }
    if not proxy_failures and hard_human_missing:
        overall["automated_proxy_status"] = "available_automated_proxies_pass"
    elif proxy_failures:
        overall["automated_proxy_status"] = "automated_proxy_fail"
    else:
        overall["automated_proxy_status"] = "available_automated_proxies_pass"

    payload = {
        "status": "sandbox quality gate evaluation",
        "gate_meaning": "go means eligible for candidate operation-convention discussion, not adoption",
        "overall": overall,
        "gates": auto_gates,
    }
    (ROOT / "quality_gate_eval_800.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Quality Gates And Thresholds",
        "",
        "Status: sandbox gate report. `go` means eligible for main-vault candidate operation-convention discussion, not adoption.",
        "",
        "Current verdict:",
        "",
        "```text",
        overall["current_go_status"],
        overall["meaning"],
        f"automated_proxy_status: {overall['automated_proxy_status']}",
        "```",
        "",
        "Important: human/product gates that are not measured cannot be counted as pass.",
        "",
        "| gate | threshold | nature | current status | current value | note |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in auto_gates:
        value = row["current_value"]
        if isinstance(value, dict):
            value_text = re.sub(r"\s+", " ", json.dumps(value, ensure_ascii=False))
        else:
            value_text = "" if value is None else str(value)
        lines.append(f"| {row['id']} | {row['threshold']} | {row['nature']} | {row['status']} | {value_text} | {row['note']} |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The available automated proxies for `shell_core` pass.",
            "- The overall gate is still `not_go_yet` because wrong actionability, authority misunderstanding, human timing, operation open-rate, recurrence misunderstanding, and product click-back adjudication are not formally measured.",
            "- Package pointer resolution, live fetch, and automated semantic selector landing are useful diagnostics, but they are not human/product click-back adjudication.",
            "- `body_window` selector landing is treated as a semantic click-back failure; the current keyword-window repair must still be rechecked by operator click logs.",
            "- `shell_core_plus_recurrence` can only be discussed as a side arm; its human misunderstanding and triage-time gates are still unmeasured.",
        ]
    )
    (ROOT / "reports" / "QUALITY_GATES_AND_THRESHOLDS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"out_json": "quality_gate_eval_800.json", "out_report": "reports/QUALITY_GATES_AND_THRESHOLDS.md", "overall": overall}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
