import argparse
import json
from pathlib import Path


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def pct(num, den):
    return round(num / den * 100, 2) if den else 100.0


def reduction(before, after):
    return round((before - after) / before * 100, 1) if before else 0.0


def percentile(values, p):
    if not values:
        return 0
    values = sorted(values)
    index = round((p / 100) * (len(values) - 1))
    return values[index]


def summarize(checks, grouping):
    serious = [r for r in checks if r["serious"]]
    ordinary = [r for r in checks if r["ordinary"]]
    valid_anchor = [r for r in checks if r["source_anchor_ok"] or r["pool"]]
    anchor_required = [r for r in checks if r["pool"]]
    hard = {
        "state_mismatch": sum(not r["state_ok"] for r in checks),
        "serious_false_lite": sum(r["false_lite"] for r in serious),
        "review_due_fn": sum(r["review_due_fn"] for r in checks),
        "serious_review_due_fn": sum(r["review_due_fn"] for r in serious),
        "queue_fn": sum(r["queue_fn"] for r in checks),
        "source_anchor_failures": sum(not r["source_anchor_ok"] for r in checks),
        "anchor_problem_visibility_failures": sum(not r["anchor_problem_visibility_ok"] for r in checks),
        "record_pointer_failures": sum(not r["record_pointer_ok"] for r in checks),
        "evidence_pointer_failures": sum(not r["evidence_pointer_ok"] for r in checks),
        "authority_leakage": sum(r["authority_leakage"] for r in checks),
        "authority_boundary_failures": sum(not r["authority_boundary_ok"] for r in checks),
        "ordinary_false_positive": sum(r["ordinary_false_positive"] for r in ordinary),
        "front_line_violations": sum(r["front_line_violation"] for r in checks),
        "severe_over_grouping": len(grouping["severe_over_grouping"]),
        "serious_folded_count": grouping["serious_folded_count"],
    }
    return {
        "safety_pass": all(value == 0 for value in hard.values()),
        "hard_failures": hard,
        "serious_count": len(serious),
        "ordinary_count": len(ordinary),
        "serious_full_audit_recall_pct": pct(sum(r["full_audit"] for r in serious), len(serious)),
        "ordinary_false_positive_rate_pct": pct(hard["ordinary_false_positive"], len(ordinary)),
        "valid_anchor_resolve_rate_pct": pct(sum(r["source_anchor_ok"] for r in checks), len(checks)),
        "record_pointer_resolve_rate_pct": pct(sum(r["record_pointer_ok"] for r in checks), len(checks)),
        "evidence_pointer_resolve_rate_pct": pct(sum(r["evidence_pointer_ok"] for r in checks), len(checks)),
        "front_chars_p95": percentile([r["front_chars"] for r in checks], 95),
        "serious_front_chars_p95": percentile([r["front_chars"] for r in serious], 95),
        "ordinary_front_chars_p95": percentile([r["front_chars"] for r in ordinary], 95),
        "max_front_line_chars_p95": percentile([r["max_front_line_chars"] for r in checks], 95),
        "queue_visible_count": sum(not r["queue_fn"] and (r["serious"] or r["layer"] == "anchor_problem") for r in checks),
        "resolved_count": len([r for r in checks if r["resolved"]]),
        "resolved_default_queue_visible": sum(r["resolved"] and not r["queue_fn"] and r["serious"] for r in checks),
        "resolved_front_line_violations": sum(r["resolved"] and r["front_line_violation"] for r in checks),
        "grouping": grouping,
    }


def by_id(items):
    return {item["case_id"]: item for item in items}


def size(artifact):
    text = artifact["rendered_text"]
    return {
        "lines": len(artifact["front"]) + len(artifact["back"]) + len(artifact["full"]),
        "chars": len(text),
        "front_chars": len("\n".join(artifact["front"])),
        "full_open": bool(artifact["full"]),
    }


def review_proxy(sizes):
    return sum(s["chars"] / 100 + s["lines"] * 0.2 + (3 if s["full_open"] else 0) for s in sizes)


def paired(gold, baseline, candidate, selector):
    b = by_id(baseline)
    c = by_id(candidate)
    ids = [cid for cid, g in gold.items() if selector(cid, g)]
    bs = [size(b[cid]) for cid in ids]
    cs = [size(c[cid]) for cid in ids]
    return {
        "case_count": len(ids),
        "rendered_line_reduction_pct": reduction(sum(s["lines"] for s in bs), sum(s["lines"] for s in cs)),
        "rendered_char_reduction_pct": reduction(sum(s["chars"] for s in bs), sum(s["chars"] for s in cs)),
        "front_char_reduction_pct": reduction(sum(s["front_chars"] for s in bs), sum(s["front_chars"] for s in cs)),
        "review_proxy_delta_pct": round((review_proxy(cs) - review_proxy(bs)) / review_proxy(bs) * 100, 1) if bs else 0.0,
    }


NEGATIVE_CONTROLS = {
    "leaky_or_unversioned_control",
    "authority_leaky_renderer",
    "fake_precision_feedback_renderer",
}


def threshold_eval(summary, paired_metrics, variant):
    if variant in NEGATIVE_CONTROLS:
        return {"negative_control_failed": not summary["safety_pass"], "expected": "must fail"}
    hard = summary["hard_failures"]
    ordinary = paired_metrics["ordinary"]
    recurrence = paired_metrics["recurrence"]
    resolved = paired_metrics["resolved"]
    gates = {
        "serious_false_lite_zero": hard["serious_false_lite"] == 0,
        "serious_full_audit_recall_100": summary["serious_full_audit_recall_pct"] == 100.0,
        "serious_folded_zero": hard["serious_folded_count"] == 0,
        "valid_anchor_resolve_ge_99": summary["valid_anchor_resolve_rate_pct"] >= 99.0,
        "record_evidence_pointer_ge_99_5": summary["record_pointer_resolve_rate_pct"] >= 99.5 and summary["evidence_pointer_resolve_rate_pct"] >= 99.5,
        "review_due_serious_fn_zero": hard["serious_review_due_fn"] == 0,
        "ordinary_false_positive_le_2_pct": summary["ordinary_false_positive_rate_pct"] <= 2.0,
        "front_line_violations_zero": hard["front_line_violations"] == 0,
        "ordinary_line_reduction_ge_55": ordinary["rendered_line_reduction_pct"] >= 55.0,
        "ordinary_char_reduction_ge_60": ordinary["rendered_char_reduction_pct"] >= 60.0,
        "recurrence_grouped_reduction_ge_50": summary["grouping"]["grouped_reduction_pct"] >= 50.0 if variant == "shell_core_plus_recurrence" else True,
        "resolved_default_surface_folded": summary["resolved_default_queue_visible"] == 0 and summary["resolved_front_line_violations"] == 0,
        "front_chars_p95_budget": summary["ordinary_front_chars_p95"] <= 320 and summary["serious_front_chars_p95"] <= 420 and summary["max_front_line_chars_p95"] <= 140,
    }
    return {"all_continue_gates_pass": all(gates.values()), "gates": gates}


def report(result):
    lines = [
        "# VAKS 800 Pressure-Overlay Pilot Report",
        "",
        "Status: sandbox-only. No main-vault writeback, no SCHEMA change, no human timing fabricated.",
        "",
        "Gold status: frozen machine oracle from explicit overlays. Human adjudication packet is generated separately; this is not independent human gold.",
        "",
        "## Dataset Mix",
        "",
        "| pool/family | cases | source rows | status |",
        "| --- | ---: | ---: | --- |",
    ]
    for key, row in result["case_manifest"].items():
        lines.append(f"| {key} | {row.get('pilot_cases', '')} | {row.get('source_rows', '')} | {row.get('source_status', '')} |")
    for variant, payload in result["variants"].items():
        lines.extend(["", f"## {variant}", "", f"safety_pass: `{payload['summary']['safety_pass']}`", ""])
        lines.extend(["| hard gate | count |", "| --- | ---: |"])
        for key, value in payload["summary"]["hard_failures"].items():
            lines.append(f"| {key} | {value} |")
        lines.extend(["", "| metric | all | ordinary | serious | recurrence | resolved |", "| --- | ---: | ---: | ---: | ---: | ---: |"])
        for metric in ["rendered_line_reduction_pct", "rendered_char_reduction_pct", "front_char_reduction_pct", "review_proxy_delta_pct"]:
            p = payload["paired"]
            lines.append(f"| {metric} | {p['all'][metric]} | {p['ordinary'][metric]} | {p['serious'][metric]} | {p['recurrence'][metric]} | {p['resolved'][metric]} |")
        lines.extend(["", "| front density | value |", "| --- | ---: |"])
        for key in ["ordinary_front_chars_p95", "serious_front_chars_p95", "front_chars_p95", "max_front_line_chars_p95"]:
            lines.append(f"| {key} | {payload['summary'][key]} |")
        lines.extend(["", "| resolved view metric | value |", "| --- | ---: |"])
        for key in ["resolved_count", "resolved_default_queue_visible", "resolved_front_line_violations"]:
            lines.append(f"| {key} | {payload['summary'][key]} |")
        lines.extend(["", "Threshold audit:", ""])
        lines.append(json.dumps(payload["threshold_eval"], indent=2))
    lines.extend([
        "",
        "## Human Timing Status",
        "",
        "Human review timing is not fabricated. See `review_packet/` for randomized assignment and blank timing sheets.",
        "",
        "## Interpretation",
        "",
        "- `shell_core` is the only default-core candidate.",
        "- `shell_core_plus_recurrence` is a conditional arm and must be judged on recurrence-heavy slices, not mixed averages.",
        "- Negative controls must fail: `leaky_or_unversioned_control`, `authority_leaky_renderer`, and `fake_precision_feedback_renderer`. If any negative control is not caught, the harness is not valid.",
        "- This run proves the automated scaffold and frozen-gold workflow. It still requires human adjudication/timing before operation-convention promotion.",
    ])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", required=True)
    parser.add_argument("--case-manifest", required=True)
    parser.add_argument("--baseline-artifacts", required=True)
    parser.add_argument("--variant", action="append", nargs=3, metavar=("NAME", "ARTIFACTS", "CHECKS"), required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-report", required=True)
    args = parser.parse_args()
    gold = read_json(args.gold)
    manifest = read_json(args.case_manifest)
    baseline = read_json(args.baseline_artifacts)
    result = {"case_manifest": manifest, "variants": {}}
    selectors = {
        "all": lambda _cid, _g: True,
        "ordinary": lambda _cid, g: g["ordinary"],
        "serious": lambda _cid, g: g["serious"],
        "recurrence": lambda _cid, g: g["recurrence_candidate"],
        "resolved": lambda _cid, g: g["resolved"],
    }
    for name, artifacts_path, checks_path in args.variant:
        artifacts = read_json(artifacts_path)
        checks_payload = read_json(checks_path)
        summary = summarize(checks_payload["checks"], checks_payload["grouping"])
        paired_metrics = {key: paired(gold, baseline, artifacts, selector) for key, selector in selectors.items()}
        result["variants"][name] = {
            "summary": summary,
            "paired": paired_metrics,
            "threshold_eval": threshold_eval(summary, paired_metrics, name),
        }
    Path(args.out_json).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.out_report).write_text(report(result), encoding="utf-8")
    print(f"wrote {args.out_report}")


if __name__ == "__main__":
    main()
