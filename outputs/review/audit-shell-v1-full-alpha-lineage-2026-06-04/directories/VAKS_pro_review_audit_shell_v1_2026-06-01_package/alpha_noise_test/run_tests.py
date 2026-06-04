import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


STRICT_GATE_KEYS = {
    "promotion",
    "action_basis",
    "explicit_challenge",
    "conflict",
    "regression",
    "known_omission",
    "risk_sensitive",
    "explicit_enough_question",
    "memory_only",
    "transformed_anchor_missing",
}


BASELINE_FIELDS = {
    "compact_evidence_card": [
        "claim",
        "source_anchor",
        "evidence_item",
        "warrant",
        "support_judgment",
        "scope_limit",
        "risk_note",
        "challenge_note",
        "counterevidence_slot",
        "omission_slot",
        "minimal_revision",
        "reviewer_note",
        "jump_back_pointer",
    ],
    "compact_coverage_card": [
        "answer_point",
        "coverage_row_1",
        "coverage_row_2",
        "coverage_row_3",
        "coverage_row_4",
        "missing_items",
        "scope_limit",
        "omission_check",
        "risk_note",
        "source_list",
        "reviewer_note",
        "jump_back_pointer",
    ],
    "support_refine_cluster": [
        "collision_item",
        "source_a",
        "source_b",
        "source_contributions",
        "support_note",
        "refine_note",
        "challenge_note",
        "unresolved_gap",
        "why_not_upgrade",
        "source_independence",
        "review_due",
        "reviewer_note",
        "jump_back_pointer",
    ],
    "categorical_feedback_stub": [
        "feedback_event",
        "query_context",
        "activation_delta",
        "scope_fit_delta",
        "outcome_score",
        "positive_signal",
        "negative_signal",
        "affected_claim",
        "affected_context_pack",
        "review_due",
        "manual_trace",
        "reviewer_note",
        "jump_back_pointer",
    ],
}


FULL_FIELDS = {
    "compact_evidence_card": BASELINE_FIELDS["compact_evidence_card"],
    "compact_coverage_card": [
        "answer_point",
        "full_coverage_rows",
        "covered_points",
        "missing_items",
        "counterevidence",
        "omission_check",
        "scope_limit",
        "risk_note",
        "source_list",
        "reviewer_note",
        "jump_back_pointer",
    ],
    "support_refine_cluster": BASELINE_FIELDS["support_refine_cluster"],
    "categorical_feedback_stub": [
        "feedback_type",
        "short_reason",
        "affected_claim",
        "affected_context_pack",
        "review_due",
        "next_activate",
        "next_avoid",
        "recurrence",
        "regressed",
        "no_truth_change",
        "manual_trace",
        "jump_back_pointer",
    ],
}


def has_strict_gate(signals):
    return any(bool(signals.get(key)) for key in STRICT_GATE_KEYS)


def alpha_record(case):
    candidate = case["candidate"]
    signals = case["signals"]
    strict = has_strict_gate(signals)

    if candidate == "compact_evidence_card":
        if strict or not signals.get("source_anchor"):
            fields = list(FULL_FIELDS[candidate])
            if not signals.get("source_anchor") or signals.get("memory_only"):
                fields.extend(["missing_anchor_note", "review_due"])
            return "full_audit", dedupe(fields)
        fields = [
            "claim",
            "source_anchor",
            "support_judgment",
            "scope_limit",
            "risk_note",
            "jump_back_pointer",
        ]
        return "compact_card", fields

    if candidate == "compact_coverage_card":
        if strict:
            return "full_coverage", FULL_FIELDS[candidate]
        fields = [
            "answer_point",
            "covered_points",
            "missing_items",
            "scope_limit",
            "upgrade_condition",
            "jump_back_pointer",
        ]
        return "compact_coverage", fields

    if candidate == "support_refine_cluster":
        if signals.get("conflict") or signals.get("explicit_challenge") or signals.get("action_basis"):
            fields = list(FULL_FIELDS[candidate]) + ["cluster_key", "conflict"]
            return "blocking_review_cluster", dedupe(fields)
        if signals.get("nonblocking"):
            return "linked_stub", ["linked_stub", "unresolved_gap", "why_not_upgrade", "jump_back_pointer"]
        fields = [
            "cluster_key",
            "source_contributions",
            "unresolved_gap",
            "why_not_upgrade",
            "not_auto_resolved",
            "jump_back_pointer",
        ]
        return "support_refine_cluster", fields

    if candidate == "categorical_feedback_stub":
        if signals.get("explicit_correction") or signals.get("regression"):
            return "review_due_feedback", FULL_FIELDS[candidate]
        fields = [
            "feedback_type",
            "short_reason",
            "next_activate",
            "next_avoid",
            "recurrence",
            "manual_trace_not_proof",
            "no_truth_change",
            "jump_back_pointer",
        ]
        return "feedback_stub", fields

    raise ValueError(f"unknown candidate: {candidate}")


def dedupe(items):
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def evaluate_case(case):
    candidate = case["candidate"]
    baseline_fields = BASELINE_FIELDS[candidate]
    alpha_mode, fields = alpha_record(case)
    expected = case["expected"]

    baseline_lines = len(baseline_fields) + 2
    alpha_lines = len(fields) + 2
    saved_lines = baseline_lines - alpha_lines

    expected_escalate = bool(expected["should_escalate"])
    escalated = alpha_mode in {
        "full_audit",
        "full_coverage",
        "blocking_review_cluster",
        "review_due_feedback",
    }
    ordinary = bool(expected["ordinary"])

    missing_preserved = [item for item in expected["must_preserve"] if item not in fields]
    false_lite = expected_escalate and not escalated
    ordinary_false_positive = ordinary and escalated
    added_burden = ordinary and alpha_lines > baseline_lines
    fake_precision = candidate == "categorical_feedback_stub" and any(
        item in fields for item in ["activation_delta", "scope_fit_delta", "outcome_score"]
    )

    passed = not any([missing_preserved, false_lite, ordinary_false_positive, added_burden, fake_precision])

    return {
        "case_id": case["case_id"],
        "candidate": candidate,
        "scenario": case["scenario"],
        "alpha_mode": alpha_mode,
        "baseline_lines": baseline_lines,
        "alpha_lines": alpha_lines,
        "saved_lines": saved_lines,
        "saved_pct": round(saved_lines / baseline_lines * 100, 1),
        "expected_escalate": expected_escalate,
        "escalated": escalated,
        "ordinary": ordinary,
        "ordinary_false_positive": ordinary_false_positive,
        "false_lite": false_lite,
        "added_burden": added_burden,
        "fake_precision": fake_precision,
        "missing_preserved": missing_preserved,
        "passed": passed,
    }


def summarize(results):
    by_candidate = {}
    for row in results:
        item = by_candidate.setdefault(
            row["candidate"],
            {
                "cases": 0,
                "passed": 0,
                "baseline_lines": 0,
                "alpha_lines": 0,
                "ordinary_false_positive": 0,
                "false_lite": 0,
                "added_burden": 0,
                "fake_precision": 0,
                "missing_preserved_cases": 0,
                "ordinary_cases": 0,
                "ordinary_baseline_lines": 0,
                "ordinary_alpha_lines": 0,
                "true_failures_caught": 0,
                "true_failures_total": 0,
            },
        )
        item["cases"] += 1
        item["passed"] += int(row["passed"])
        item["baseline_lines"] += row["baseline_lines"]
        item["alpha_lines"] += row["alpha_lines"]
        item["ordinary_false_positive"] += int(row["ordinary_false_positive"])
        item["false_lite"] += int(row["false_lite"])
        item["added_burden"] += int(row["added_burden"])
        item["fake_precision"] += int(row["fake_precision"])
        item["missing_preserved_cases"] += int(bool(row["missing_preserved"]))
        if row["ordinary"]:
            item["ordinary_cases"] += 1
            item["ordinary_baseline_lines"] += row["baseline_lines"]
            item["ordinary_alpha_lines"] += row["alpha_lines"]
        if row["expected_escalate"]:
            item["true_failures_total"] += 1
            item["true_failures_caught"] += int(row["escalated"])

    for item in by_candidate.values():
        saved = item["baseline_lines"] - item["alpha_lines"]
        item["saved_lines"] = saved
        item["saved_pct"] = round(saved / item["baseline_lines"] * 100, 1)
        ordinary_saved = item["ordinary_baseline_lines"] - item["ordinary_alpha_lines"]
        item["ordinary_saved_lines"] = ordinary_saved
        item["ordinary_saved_pct"] = (
            round(ordinary_saved / item["ordinary_baseline_lines"] * 100, 1)
            if item["ordinary_baseline_lines"]
            else 0.0
        )
        if item["false_lite"] or item["ordinary_false_positive"] or item["missing_preserved_cases"]:
            item["recommendation"] = "needs_narrowing"
        elif item["ordinary_saved_pct"] >= 35:
            item["recommendation"] = "strong_next_round"
        elif item["ordinary_saved_pct"] >= 20:
            item["recommendation"] = "worth_next_round"
        else:
            item["recommendation"] = "weak_benefit"
    return by_candidate


def make_report(cases, results, summary):
    lines = []
    lines.append("# VAKS Alpha Noise-Reduction Test Report")
    lines.append("")
    lines.append("Status: sandbox-only, typed-case A/B test, not a truth benchmark.")
    lines.append("")
    lines.append("## Executive Result")
    lines.append("")
    total_cases = len(results)
    passed = sum(int(r["passed"]) for r in results)
    baseline = sum(r["baseline_lines"] for r in results)
    alpha = sum(r["alpha_lines"] for r in results)
    saved = baseline - alpha
    saved_pct = round(saved / baseline * 100, 1)
    false_lite = sum(int(r["false_lite"]) for r in results)
    ordinary_fp = sum(int(r["ordinary_false_positive"]) for r in results)
    lines.append(f"- cases: {total_cases}")
    lines.append(f"- passed: {passed}/{total_cases}")
    lines.append(f"- baseline lines: {baseline}")
    lines.append(f"- alpha lines: {alpha}")
    lines.append(f"- saved lines: {saved} ({saved_pct}%)")
    lines.append(f"- false-lite cases: {false_lite}")
    lines.append(f"- ordinary false positives: {ordinary_fp}")
    ordinary_baseline = sum(r["baseline_lines"] for r in results if r["ordinary"])
    ordinary_alpha = sum(r["alpha_lines"] for r in results if r["ordinary"])
    ordinary_saved = ordinary_baseline - ordinary_alpha
    ordinary_saved_pct = round(ordinary_saved / ordinary_baseline * 100, 1)
    lines.append(f"- ordinary-case saved lines: {ordinary_saved} ({ordinary_saved_pct}%)")
    lines.append("")
    lines.append("## Candidate Summary")
    lines.append("")
    lines.append("| candidate | cases | passed | all-case saved | ordinary-case saved | true failures caught | ordinary false positives | false-lite | recommendation |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
    for candidate, item in sorted(summary.items()):
        tf = f"{item['true_failures_caught']}/{item['true_failures_total']}" if item["true_failures_total"] else "n/a"
        lines.append(
            f"| {candidate} | {item['cases']} | {item['passed']} | {item['saved_lines']} ({item['saved_pct']}%) | "
            f"{item['ordinary_saved_lines']} ({item['ordinary_saved_pct']}%) | {tf} | {item['ordinary_false_positive']} | {item['false_lite']} | {item['recommendation']} |"
        )
    lines.append("")
    lines.append("## Case Detail")
    lines.append("")
    lines.append("| case | candidate | scenario | mode | baseline | alpha | saved | escalated as expected? | ordinary overburdened? | preserved? | pass |")
    lines.append("| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |")
    for row in results:
        expected_ok = (row["expected_escalate"] == row["escalated"]) or (not row["expected_escalate"] and not row["false_lite"])
        preserved = "yes" if not row["missing_preserved"] else ",".join(row["missing_preserved"])
        lines.append(
            f"| {row['case_id']} | {row['candidate']} | {row['scenario']} | {row['alpha_mode']} | "
            f"{row['baseline_lines']} | {row['alpha_lines']} | {row['saved_lines']} | "
            f"{'yes' if expected_ok else 'no'} | {'yes' if row['ordinary_false_positive'] else 'no'} | {preserved} | {'PASS' if row['passed'] else 'FAIL'} |"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("The alphas reduced record surface in typed cases without missing strict-gate escalation.")
    lines.append("The strongest immediate candidates are compact coverage cards, categorical feedback stubs, and compact evidence cards.")
    lines.append("Support/refine clustering is useful, but should be tested against messier real source material because over-grouping is the main risk.")
    lines.append("")
    lines.append("## Limits")
    lines.append("")
    lines.append("- This test uses typed signals plus prose cases. It does not test extraction from messy raw papers.")
    lines.append("- It measures record burden and gate behavior, not factual correctness.")
    lines.append("- It does not prove source independence. Lineage can prompt review, not replace review.")
    lines.append("- It does not justify SCHEMA changes.")
    lines.append("")
    lines.append("## Next Suggested Test")
    lines.append("")
    lines.append("Run the same four alphas on 10 to 20 real/distilled claim-evidence cases from SciFact/AVeriTeC plus 3 to 5 full source anchors from the existing E2E trial.")
    return "\n".join(lines) + "\n"


def main():
    cases = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
    results = [evaluate_case(case) for case in cases]
    summary = summarize(results)

    payload = {"results": results, "summary": summary}
    (ROOT / "results.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    (ROOT / "ALPHA_NOISE_TEST_REPORT.md").write_text(make_report(cases, results, summary), encoding="utf-8")

    failed = [row for row in results if not row["passed"]]
    print(f"cases={len(results)} passed={len(results) - len(failed)} failed={len(failed)}")
    print(f"report={ROOT / 'ALPHA_NOISE_TEST_REPORT.md'}")
    if failed:
        for row in failed:
            print(f"FAIL {row['case_id']} {row['missing_preserved']} false_lite={row['false_lite']} ordinary_fp={row['ordinary_false_positive']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
