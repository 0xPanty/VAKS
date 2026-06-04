import argparse
import json
from pathlib import Path


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def summarize(checks, grouping):
    failures = {
        "state_mismatch": sum(1 for row in checks if not row["state_ok"]),
        "false_lite": sum(1 for row in checks if row["false_lite"]),
        "review_due_fn": sum(1 for row in checks if row["review_due_fn"]),
        "anchor_failures": sum(1 for row in checks if not row["anchor_ok"]),
        "anchor_problem_visibility_failures": sum(1 for row in checks if not row["anchor_problem_visibility_ok"]),
        "authority_leakage": sum(1 for row in checks if row["authority_leakage"]),
        "authority_boundary_failures": sum(1 for row in checks if not row["authority_boundary_ok"]),
        "queue_failures": sum(1 for row in checks if not row["queue_ok"]),
        "front_violations": sum(1 for row in checks if not row["front_ok"]),
        "severe_over_grouping": len(grouping["severe_over_grouping"]),
    }
    return {
        "safety_pass": all(value == 0 for value in failures.values()),
        "hard_failures": failures,
        "front_lines": sum(row["front_lines"] for row in checks),
        "rendered_lines": sum(row["rendered_lines"] for row in checks),
        "anchor_resolve_rate": round(sum(1 for row in checks if row["anchor_ok"]) / len(checks), 4),
        "grouping_recall": grouping["grouping_recall"],
        "grouped_reduction_pct": grouping["grouped_reduction_pct"],
    }


def paired_metrics(gold, baseline_artifacts, candidate_artifacts):
    def line_count(artifact):
        return len(artifact["front"]) + len(artifact["back"]) + len(artifact["full"])

    baseline_by_id = {a["case_id"]: a for a in baseline_artifacts}
    candidate_by_id = {a["case_id"]: a for a in candidate_artifacts}
    ids = list(candidate_by_id)
    ordinary = [cid for cid in ids if not gold[cid]["full_audit"] and gold[cid]["state"] in {"ordinary", "resolved_folded", "parked_nonblocking"}]
    serious = [cid for cid in ids if gold[cid]["full_audit"] or gold[cid]["queue_visible"]]

    def total(cids, by_id):
        return sum(line_count(by_id[cid]) for cid in cids)

    def reduction(before, after):
        return round((before - after) / before * 100, 1) if before else 0.0

    baseline_total = total(ids, baseline_by_id)
    candidate_total = total(ids, candidate_by_id)
    ordinary_before = total(ordinary, baseline_by_id)
    ordinary_after = total(ordinary, candidate_by_id)
    serious_before = total(serious, baseline_by_id)
    serious_after = total(serious, candidate_by_id)

    baseline_review_time = baseline_total + len(baseline_artifacts) * 2
    candidate_review_time = candidate_total + sum(1 for a in candidate_artifacts if a["full"]) * 2

    return {
        "paired_total_rendered_line_reduction_pct": reduction(baseline_total, candidate_total),
        "paired_ordinary_rendered_line_reduction_pct": reduction(ordinary_before, ordinary_after),
        "paired_serious_rendered_line_delta_pct": round((serious_after - serious_before) / serious_before * 100, 1) if serious_before else 0.0,
        "paired_review_time_delta_pct": round((candidate_review_time - baseline_review_time) / baseline_review_time * 100, 1) if baseline_review_time else 0.0,
        "baseline_total_lines": baseline_total,
        "candidate_total_lines": candidate_total,
        "baseline_ordinary_lines": ordinary_before,
        "candidate_ordinary_lines": ordinary_after,
        "baseline_serious_lines": serious_before,
        "candidate_serious_lines": serious_after,
    }


def make_report(results, paired, variant):
    s = results["summary"]
    f = s["hard_failures"]
    lines = [
        "# Independent Oracle Hardening Patch Report",
        "",
        "Status: sandbox-only. No main-vault writeback, no SCHEMA change, not 480 real-data proof.",
        "",
        "## Verdict",
        "",
        f"Candidate variant `{variant}` passes the independent-runner output oracle hard gates." if s["safety_pass"] else f"Candidate variant `{variant}` does not pass hard gates.",
        "",
        "## Hard Gates",
        "",
        "| gate | result |",
        "| --- | ---: |",
    ]
    for key, value in f.items():
        lines.append(f"| {key} | {value} |")
    lines.extend([
        f"| safety_pass | {s['safety_pass']} |",
        f"| anchor_resolve_rate | {s['anchor_resolve_rate']} |",
        f"| grouping_recall | {s['grouping_recall']} |",
        f"| grouped_reduction_pct | {s['grouped_reduction_pct']} |",
        "",
        "## Paired Metrics",
        "",
        "| metric | value |",
        "| --- | ---: |",
    ])
    for key, value in paired.items():
        lines.append(f"| {key} | {value} |")
    lines.extend([
        "",
        "## Interpretation",
        "",
        "This patch addresses Pro's requested split: gold labels, renderer, checker, and aggregator are separate files/runners.",
        "Authority leakage is checked through paraphrase regex families against rendered text.",
        "Versioned fingerprint grouping is tested by hard cases where all non-version grouping fields are identical.",
        "Headline reduction uses paired baseline-vs-candidate rendered lines rather than a synthetic total*12 baseline.",
        "Anchor health is reported as anchor_problem_visibility for missing/stale/drift/moved pointers.",
        "",
        "This still remains a fixture patch. If accepted, the next step is the 480 real-data paired pilot.",
    ])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", required=True)
    parser.add_argument("--baseline-artifacts", required=True)
    parser.add_argument("--candidate-artifacts", required=True)
    parser.add_argument("--candidate-checks", required=True)
    parser.add_argument("--variant", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-report", required=True)
    args = parser.parse_args()

    gold = load_json(args.gold)
    baseline_artifacts = load_json(args.baseline_artifacts)
    candidate_artifacts = load_json(args.candidate_artifacts)
    candidate = load_json(args.candidate_checks)
    summary = summarize(candidate["checks"], candidate["grouping"])
    paired = paired_metrics(gold, baseline_artifacts, candidate_artifacts)
    result = {"variant": args.variant, "summary": summary, "paired_metrics": paired, "grouping": candidate["grouping"]}
    Path(args.out_json).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.out_report).write_text(make_report(result, paired, args.variant), encoding="utf-8")


if __name__ == "__main__":
    main()
