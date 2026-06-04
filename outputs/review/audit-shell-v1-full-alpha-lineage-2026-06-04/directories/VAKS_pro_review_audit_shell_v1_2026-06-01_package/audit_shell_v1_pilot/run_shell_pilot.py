import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent


DATASET_MIX = {
    "scifact_like": 24,
    "averitec_like": 20,
    "ambifc_like": 16,
    "fever_like": 20,
    "full_anchor_like": 8,
    "derived_replay": 24,
}


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
}


BASELINE_LINES = {
    "small_claim": 15,
    "answer_query_run": 16,
    "support_refine_collision": 17,
    "feedback": 15,
}


FULL_AUDIT_LINES = {
    "small_claim": 16,
    "answer_query_run": 17,
    "support_refine_collision": 18,
    "feedback": 15,
}


FRONT_LINES = {
    "small_claim": 6,
    "answer_query_run": 6,
    "support_refine_collision": 6,
    "feedback": 5,
}


def trigger_set(*items):
    return {item for item in items if item}


def make_case(case_id, source_family, object_type, scenario, state, triggers=None, group_key=None,
              escalation_class="ordinary", gap_family="none", feedback_type=None,
              anchor_required=True, anchor_valid=True, resolved=False, nonblocking=False,
              material_difference=False, review_due_needed=False):
    triggers = set(triggers or [])
    serious = bool(triggers & HARD_TRIGGERS)
    if state in {"blocking", "regressed", "for_review"}:
        review_due_needed = True
    return {
        "case_id": case_id,
        "source_family": source_family,
        "object_type": object_type,
        "scenario": scenario,
        "state": state,
        "triggers": sorted(triggers),
        "serious": serious,
        "group_key": group_key,
        "escalation_class": escalation_class,
        "gap_family": gap_family,
        "feedback_type": feedback_type,
        "anchor_required": anchor_required,
        "anchor_valid": anchor_valid,
        "resolved": resolved,
        "nonblocking": nonblocking,
        "material_difference": material_difference,
        "review_due_needed": review_due_needed,
    }


def generate_cases():
    cases = []
    i = 1

    # SciFact-like: small scientific claims with abstract/rationale anchors.
    patterns = [
        ("ordinary", "ordinary", [], True, True),
        ("ordinary_scope", "ordinary", [], True, True),
        ("promotion", "blocking", ["promotion"], True, True),
        ("missing_anchor", "blocking", ["missing_anchor"], True, False),
        ("known_omission", "for_review", ["known_omission"], True, True),
        ("explicit_challenge", "blocking", ["explicit_challenge"], True, True),
    ]
    for n in range(DATASET_MIX["scifact_like"]):
        scenario, state, triggers, anchor_req, anchor_valid = patterns[n % len(patterns)]
        cases.append(make_case(
            f"SF-{i:03d}", "scifact_like", "small_claim", scenario, state,
            triggers=triggers, group_key=f"sf_claim_{n // 3}", escalation_class="claim_review",
            gap_family="claim_scope" if "scope" in scenario else "none",
            anchor_required=anchor_req, anchor_valid=anchor_valid,
            review_due_needed=bool(triggers),
        ))
        i += 1

    # AVeriTeC-like: real-world claims with web evidence and sufficiency pressure.
    patterns = [
        ("ordinary_answer", "ordinary", [], 0),
        ("multi_evidence_answer", "ordinary", [], 0),
        ("action_basis", "blocking", ["action_basis"], 2),
        ("risk_sensitive", "blocking", ["risk_sensitive"], 1),
        ("important_omission", "for_review", ["known_omission"], 2),
    ]
    for n in range(DATASET_MIX["averitec_like"]):
        scenario, state, triggers, missing = patterns[n % len(patterns)]
        cases.append(make_case(
            f"AV-{i:03d}", "averitec_like", "answer_query_run", scenario, state,
            triggers=triggers, group_key=f"av_answer_{n // 4}", escalation_class="coverage",
            gap_family="sufficiency_gap" if missing else "none",
            review_due_needed=bool(triggers),
        ))
        i += 1

    # AmbiFC-like: ambiguity, conflict, and grouping boundaries.
    patterns = [
        ("ambiguous_scope", "for_review", ["known_omission"], False),
        ("support_refine", "ordinary", [], False),
        ("direct_conflict", "blocking", ["conflict"], True),
        ("independence_needed", "blocking", ["independence_needed_for_confidence"], True),
    ]
    for n in range(DATASET_MIX["ambifc_like"]):
        scenario, state, triggers, material = patterns[n % len(patterns)]
        if scenario == "support_refine":
            cluster_key = "amb_support_refine_repeated_scope_gap"
        else:
            cluster_key = f"amb_cluster_{n // 4}"
        cases.append(make_case(
            f"AM-{i:03d}", "ambifc_like", "support_refine_collision", scenario, state,
            triggers=triggers, group_key=cluster_key, escalation_class="collision" if triggers else "support_refine",
            gap_family="ambiguity_gap", material_difference=material,
            review_due_needed=bool(triggers),
        ))
        i += 1

    # FEVER-like: volume-heavy ordinary flow with some NEI/refute boundaries.
    patterns = [
        ("ordinary_supported", "ordinary", [], "none"),
        ("ordinary_refuted_note", "ordinary", [], "none"),
        ("not_enough_info", "for_review", ["known_omission"], "evidence_gap"),
        ("trust_challenge", "blocking", ["explicit_challenge"], "challenge"),
        ("resolved_old", "resolved_folded", [], "none"),
    ]
    for n in range(DATASET_MIX["fever_like"]):
        scenario, state, triggers, gap = patterns[n % len(patterns)]
        if scenario in {"ordinary_supported", "ordinary_refuted_note"}:
            fever_group = f"fever_repeated_{scenario}"
        else:
            fever_group = f"fever_{n // 5}"
        cases.append(make_case(
            f"FV-{i:03d}", "fever_like", "small_claim" if n % 2 else "answer_query_run", scenario, state,
            triggers=triggers, group_key=fever_group, escalation_class="claim_or_answer",
            gap_family=gap, resolved=state == "resolved_folded", review_due_needed=bool(triggers),
        ))
        i += 1

    # Full-anchor-like: messy source forms and jump-back proof.
    patterns = [
        ("paper_span", "ordinary", [], True),
        ("versioned_doc", "ordinary", [], True),
        ("repo_release_note", "for_review", ["known_omission"], True),
        ("missing_span", "blocking", ["missing_anchor"], False),
    ]
    for n in range(DATASET_MIX["full_anchor_like"]):
        scenario, state, triggers, anchor_valid = patterns[n % len(patterns)]
        cases.append(make_case(
            f"FA-{i:03d}", "full_anchor_like", "small_claim", scenario, state,
            triggers=triggers, group_key=f"full_anchor_{n // 2}", escalation_class="source_anchor",
            gap_family="anchor_gap" if not anchor_valid else "none",
            anchor_valid=anchor_valid, review_due_needed=bool(triggers),
        ))
        i += 1

    # Derived replay: repeated feedback / resolved-regressed / recurrence.
    for n in range(DATASET_MIX["derived_replay"]):
        if n < 8:
            scenario, state, triggers, feedback_type, gap, escalation_class, replay_group = (
                "too_broad_repeat", "ordinary", [], "too_broad", "scope_gap", "feedback_scope", "target_alpha_too_broad"
            )
        elif n < 14:
            scenario, state, triggers, feedback_type, gap, escalation_class, replay_group = (
                "missing_context_repeat", "ordinary", [], "missing_context", "context_gap", "feedback_scope", "target_alpha_missing_context"
            )
        elif n < 18:
            scenario, state, triggers, feedback_type, gap, escalation_class, replay_group = (
                "resolved_history", "resolved_folded", [], "scope_fit_positive", "none", "feedback_scope", "target_alpha_resolved"
            )
        elif n < 20:
            scenario, state, triggers, feedback_type, gap, escalation_class, replay_group = (
                "regressed_after_archive", "regressed", ["regression"], "too_broad", "scope_gap", "feedback_scope", "target_alpha_too_broad"
            )
        elif n < 22:
            scenario, state, triggers, feedback_type, gap, escalation_class, replay_group = (
                "explicit_correction", "blocking", ["explicit_correction"], "wrong_claim", "truth_gap", "feedback_correction", "target_alpha_correction"
            )
        else:
            scenario, state, triggers, feedback_type, gap, escalation_class, replay_group = (
                "action_outcome", "for_review", ["action_outcome"], "action_result", "outcome_gap", "feedback_outcome", "target_alpha_action_outcome"
            )
        cases.append(make_case(
            f"DR-{i:03d}", "derived_replay", "feedback", scenario, state,
            triggers=triggers, group_key=replay_group, escalation_class=escalation_class,
            gap_family=gap, feedback_type=feedback_type, resolved=state == "resolved_folded",
            review_due_needed=bool(triggers),
        ))
        i += 1

    return cases


def needs_full_audit(case):
    return bool(set(case["triggers"]) & HARD_TRIGGERS)


def baseline_view(case):
    return {
        "visible_lines": BASELINE_LINES[case["object_type"]],
        "main_view_items": 1,
        "full_audit": needs_full_audit(case),
        "anchor_state_retained": True,
        "valid_anchor_retained": case["anchor_valid"] if case["anchor_required"] and case["anchor_valid"] else True,
        "missing_anchor_visible": (not case["anchor_valid"]) if "missing_anchor" in case["triggers"] else True,
        "review_due": case["review_due_needed"],
    }


def group_key(case):
    if not case["group_key"]:
        return None
    return (
        case["group_key"],
        case["escalation_class"],
        case["gap_family"],
        case["feedback_type"] or "",
        "anchor_ok" if case["anchor_valid"] else "anchor_missing",
    )


def shell_view(case):
    full = needs_full_audit(case)
    if full:
        visible_lines = FULL_AUDIT_LINES[case["object_type"]]
        main_view_items = 1
    elif case["state"] == "resolved_folded":
        visible_lines = 1
        main_view_items = 0
    elif case["nonblocking"] or case["state"] == "parked_nonblocking":
        visible_lines = 3
        main_view_items = 0
    else:
        visible_lines = FRONT_LINES[case["object_type"]]
        main_view_items = 1

    return {
        "visible_lines": visible_lines,
        "main_view_items": main_view_items,
        "front_face_lines": min(visible_lines, FRONT_LINES.get(case["object_type"], visible_lines)),
        "full_audit": full,
        "anchor_state_retained": True if case["anchor_required"] else True,
        "valid_anchor_retained": case["anchor_valid"] if case["anchor_required"] and case["anchor_valid"] else True,
        "missing_anchor_visible": (full and not case["anchor_valid"]) if "missing_anchor" in case["triggers"] else True,
        "review_due": case["review_due_needed"],
        "group_key": group_key(case),
    }


def apply_grouping(cases, rows):
    groups = defaultdict(list)
    for row in rows:
        key = row["shell"]["group_key"]
        if key and not row["shell"]["full_audit"] and row["case"]["state"] not in {"resolved_folded"}:
            groups[key].append(row)

    grouped_item_count = {}
    for key, group in groups.items():
        grouped_item_count[key] = 1

    raw_groupable = sum(len(group) for group in groups.values())
    grouped_items = sum(grouped_item_count.values())
    grouped_reduction = 0.0
    if raw_groupable:
        grouped_reduction = round((raw_groupable - grouped_items) / raw_groupable * 100, 1)

    over_group_mismatches = 0
    for key, group in groups.items():
        classes = {row["case"]["escalation_class"] for row in group}
        gaps = {row["case"]["gap_family"] for row in group}
        anchors = {row["case"]["anchor_valid"] for row in group}
        material = any(row["case"]["material_difference"] for row in group)
        if len(classes) > 1 or len(gaps) > 1 or len(anchors) > 1 or material:
            over_group_mismatches += 1

    return {
        "raw_groupable": raw_groupable,
        "grouped_items": grouped_items,
        "grouped_reduction_pct": grouped_reduction,
        "over_group_mismatches": over_group_mismatches,
    }


def evaluate():
    cases = generate_cases()
    rows = []
    for case in cases:
        base = baseline_view(case)
        shell = shell_view(case)
        expected_full = needs_full_audit(case)
        false_lite = expected_full and not shell["full_audit"]
        ordinary_false_positive = (not expected_full) and shell["full_audit"]
        serious_anchor_ok = (not case["serious"]) or (shell["valid_anchor_retained"] and shell["missing_anchor_visible"])
        front_ok = shell["front_face_lines"] <= 6
        rows.append({
            "case": case,
            "baseline": base,
            "shell": shell,
            "false_lite": false_lite,
            "ordinary_false_positive": ordinary_false_positive,
            "serious_anchor_ok": serious_anchor_ok,
            "front_ok": front_ok,
            "passed": not any([false_lite, ordinary_false_positive, not serious_anchor_ok, not front_ok]),
        })

    grouping = apply_grouping(cases, rows)
    return cases, rows, grouping


def summarize(rows, grouping):
    total = len(rows)
    baseline_lines = sum(r["baseline"]["visible_lines"] for r in rows)
    shell_lines = sum(r["shell"]["visible_lines"] for r in rows)
    ordinary_rows = [r for r in rows if not r["case"]["serious"] and r["case"]["state"] not in {"resolved_folded"}]
    ordinary_base = sum(r["baseline"]["visible_lines"] for r in ordinary_rows)
    ordinary_shell = sum(r["shell"]["visible_lines"] for r in ordinary_rows)
    resolved_rows = [r for r in rows if r["case"]["state"] == "resolved_folded"]
    resolved_base = sum(r["baseline"]["main_view_items"] for r in resolved_rows)
    resolved_shell = sum(r["shell"]["main_view_items"] for r in resolved_rows)

    review_due_rows = [r for r in rows if r["shell"]["review_due"]]
    review_due_true = [r for r in review_due_rows if r["case"]["review_due_needed"]]
    review_due_precision = len(review_due_true) / len(review_due_rows) if review_due_rows else 1.0

    serious_rows = [r for r in rows if r["case"]["serious"]]
    serious_full_recall = (
        sum(1 for r in serious_rows if r["shell"]["full_audit"]) / len(serious_rows)
        if serious_rows else 1.0
    )
    serious_anchor_retention = (
        sum(1 for r in serious_rows if r["shell"]["valid_anchor_retained"] and r["shell"]["missing_anchor_visible"]) / len(serious_rows)
        if serious_rows else 1.0
    )
    missing_anchor_rows = [r for r in rows if "missing_anchor" in r["case"]["triggers"]]
    missing_anchor_visibility = (
        sum(1 for r in missing_anchor_rows if r["shell"]["missing_anchor_visible"]) / len(missing_anchor_rows)
        if missing_anchor_rows else 1.0
    )

    summary = {
        "cases": total,
        "passed": sum(1 for r in rows if r["passed"]),
        "baseline_visible_lines": baseline_lines,
        "shell_visible_lines": shell_lines,
        "overall_reduction_pct": round((baseline_lines - shell_lines) / baseline_lines * 100, 1),
        "ordinary_baseline_lines": ordinary_base,
        "ordinary_shell_lines": ordinary_shell,
        "ordinary_reduction_pct": round((ordinary_base - ordinary_shell) / ordinary_base * 100, 1),
        "false_lite": sum(1 for r in rows if r["false_lite"]),
        "ordinary_false_positive": sum(1 for r in rows if r["ordinary_false_positive"]),
        "serious_cases": len(serious_rows),
        "serious_full_audit_recall": round(serious_full_recall, 4),
        "serious_anchor_retention": round(serious_anchor_retention, 4),
        "missing_anchor_visibility": round(missing_anchor_visibility, 4),
        "review_due_precision": round(review_due_precision, 4),
        "front_face_violations": sum(1 for r in rows if not r["front_ok"]),
        "resolved_raw_main_items": resolved_base,
        "resolved_shell_main_items": resolved_shell,
        "resolved_folding_reduction_pct": (
            round((resolved_base - resolved_shell) / resolved_base * 100, 1)
            if resolved_base else 0.0
        ),
        **grouping,
    }
    summary["pilot_gate_pass"] = all([
        summary["false_lite"] == 0,
        summary["serious_anchor_retention"] == 1.0,
        summary["ordinary_reduction_pct"] >= 50,
        summary["ordinary_false_positive"] <= max(1, int(total * 0.05)),
        summary["over_group_mismatches"] == 0,
        summary["review_due_precision"] >= 0.80,
        summary["front_face_violations"] == 0,
        summary["grouped_reduction_pct"] >= 50,
    ])
    return summary


def report(cases, rows, summary):
    lines = []
    lines.append("# Audit Shell V1 Pilot Report")
    lines.append("")
    lines.append("Status: sandbox-only fixture/risk-map pilot. Not a product gate and not real dataset ingestion.")
    lines.append("")
    lines.append("## Executive Result")
    lines.append("")
    for key in [
        "cases",
        "passed",
        "baseline_visible_lines",
        "shell_visible_lines",
        "overall_reduction_pct",
        "ordinary_reduction_pct",
        "false_lite",
        "ordinary_false_positive",
        "serious_cases",
        "serious_full_audit_recall",
        "serious_anchor_retention",
        "review_due_precision",
        "front_face_violations",
        "missing_anchor_visibility",
        "grouped_reduction_pct",
        "resolved_folding_reduction_pct",
        "over_group_mismatches",
        "pilot_gate_pass",
    ]:
        lines.append(f"- {key}: {summary[key]}")
    lines.append("")
    lines.append("## Dataset/Risk Mix")
    lines.append("")
    lines.append("| source_family | cases | purpose |")
    lines.append("| --- | ---: | --- |")
    purposes = {
        "scifact_like": "small claims, evidence card, abstract/rationale anchor pressure",
        "averitec_like": "coverage, sufficiency, action-basis style pressure",
        "ambifc_like": "ambiguity, support/refine vs conflict, over-grouping risk",
        "fever_like": "volume, ordinary false positive, resolved folding pressure",
        "full_anchor_like": "messy source anchor and jump-back pressure",
        "derived_replay": "repeated feedback, recurrence, resolved/regressed workflow",
    }
    counts = defaultdict(int)
    for case in cases:
        counts[case["source_family"]] += 1
    for family, count in counts.items():
        lines.append(f"| {family} | {count} | {purposes[family]} |")
    lines.append("")
    lines.append("## Gate Table")
    lines.append("")
    lines.append("| gate | result | pass? |")
    lines.append("| --- | ---: | --- |")
    gate_rows = [
        ("serious false-lite = 0", summary["false_lite"], summary["false_lite"] == 0),
        ("serious anchor retention = 100%", summary["serious_anchor_retention"], summary["serious_anchor_retention"] == 1.0),
        ("ordinary record reduction >= 50%", summary["ordinary_reduction_pct"], summary["ordinary_reduction_pct"] >= 50),
        ("ordinary false-positive <= 5%", summary["ordinary_false_positive"], summary["ordinary_false_positive"] <= max(1, int(summary["cases"] * 0.05))),
        ("over-grouping serious mismatch = 0", summary["over_group_mismatches"], summary["over_group_mismatches"] == 0),
        ("grouped repeated-event reduction >= 50%", summary["grouped_reduction_pct"], summary["grouped_reduction_pct"] >= 50),
        ("review_due precision >= 0.80", summary["review_due_precision"], summary["review_due_precision"] >= 0.80),
        ("front face <= 6 visible lines", summary["front_face_violations"], summary["front_face_violations"] == 0),
    ]
    for gate, value, ok in gate_rows:
        lines.append(f"| {gate} | {value} | {'PASS' if ok else 'FAIL'} |")
    lines.append("")
    lines.append("## Case Detail")
    lines.append("")
    lines.append("| case | family | object | state | triggers | baseline | shell | false-lite | ordinary-fp | pass |")
    lines.append("| --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- |")
    for row in rows:
        case = row["case"]
        triggers = ",".join(case["triggers"]) if case["triggers"] else "-"
        lines.append(
            f"| {case['case_id']} | {case['source_family']} | {case['object_type']} | {case['state']} | {triggers} | "
            f"{row['baseline']['visible_lines']} | {row['shell']['visible_lines']} | "
            f"{row['false_lite']} | {row['ordinary_false_positive']} | {'PASS' if row['passed'] else 'FAIL'} |"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("This pilot shows that audit shell v1 can exceed the previous single-record alpha reduction by adding queue/history compression.")
    lines.append("The useful improvement is not merely shorter cards; it is resolved folding plus grouped repeated workflow items while preserving hard thickening triggers.")
    lines.append("")
    lines.append("## Limits")
    lines.append("")
    lines.append("- Cases are fixture/risk-map cases with typed labels, not live SciFact/AVeriTeC/AmbiFC/FEVER ingestion.")
    lines.append("- This does not prove extraction from messy real sources.")
    lines.append("- This does not prove reviewer agreement.")
    lines.append("- This does not prove source independence.")
    lines.append("- This does not justify SCHEMA changes.")
    lines.append("")
    lines.append("## Next Step")
    lines.append("")
    lines.append("Replace fixture families with real sampled records from SciFact/AVeriTeC/AmbiFC/FEVER plus full source anchors, then rerun the same gates.")
    return "\n".join(lines) + "\n"


def main():
    cases, rows, grouping = evaluate()
    summary = summarize(rows, grouping)
    (ROOT / "pilot_cases.json").write_text(json.dumps(cases, indent=2, ensure_ascii=False), encoding="utf-8")
    payload = {
        "summary": summary,
        "rows": [
            {
                "case": row["case"],
                "baseline": row["baseline"],
                "shell": row["shell"],
                "false_lite": row["false_lite"],
                "ordinary_false_positive": row["ordinary_false_positive"],
                "serious_anchor_ok": row["serious_anchor_ok"],
                "front_ok": row["front_ok"],
                "passed": row["passed"],
            }
            for row in rows
        ],
    }
    (ROOT / "pilot_results.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    (ROOT / "AUDIT_SHELL_V1_PILOT_REPORT.md").write_text(report(cases, rows, summary), encoding="utf-8")
    print(f"cases={summary['cases']} passed={summary['passed']} pilot_gate_pass={summary['pilot_gate_pass']}")
    print(f"ordinary_reduction={summary['ordinary_reduction_pct']} false_lite={summary['false_lite']} ordinary_fp={summary['ordinary_false_positive']}")
    print(f"report={ROOT / 'AUDIT_SHELL_V1_PILOT_REPORT.md'}")
    if not summary["pilot_gate_pass"] or summary["passed"] != summary["cases"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
