import argparse
import json
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def percentile(values, pct):
    if not values:
        return 0
    ordered = sorted(values)
    idx = min(len(ordered) - 1, round((pct / 100) * (len(ordered) - 1)))
    return ordered[idx]


def summarize_checks(checks, grouping):
    hard_failures = {
        "state_mismatch": sum(1 for row in checks if not row["state_ok"]),
        "false_lite": sum(1 for row in checks if row["false_lite"]),
        "review_due_fn": sum(1 for row in checks if row["review_due_fn"]),
        "queue_fn": sum(1 for row in checks if row["queue_fn"]),
        "source_anchor_failures": sum(1 for row in checks if not row["source_anchor_ok"]),
        "anchor_problem_visibility_failures": sum(1 for row in checks if not row["anchor_problem_visibility_ok"]),
        "record_pointer_failures": sum(1 for row in checks if not row["record_pointer_ok"]),
        "evidence_pointer_failures": sum(1 for row in checks if not row["evidence_pointer_ok"]),
        "authority_leakage": sum(1 for row in checks if row["authority_leakage"]),
        "authority_boundary_failures": sum(1 for row in checks if not row["authority_boundary_ok"]),
        "severe_over_grouping": len(grouping["severe_over_grouping"]),
        "serious_folded_count": grouping["serious_folded_count"],
    }
    valid_anchor_rows = [row for row in checks if row["source_anchor_ok"]]
    return {
        "safety_pass": all(value == 0 for value in hard_failures.values()),
        "hard_failures": hard_failures,
        "front_budget_warnings": sum(1 for row in checks if row["front_budget_warning"]),
        "front_lines_total": sum(row["front_lines"] for row in checks),
        "front_chars_total": sum(row["front_chars"] for row in checks),
        "front_chars_p50": percentile([row["front_chars"] for row in checks], 50),
        "front_chars_p95": percentile([row["front_chars"] for row in checks], 95),
        "max_front_line_chars_p95": percentile([row["max_front_line_chars"] for row in checks], 95),
        "rendered_lines_total": sum(row["rendered_lines"] for row in checks),
        "rendered_chars_total": sum(row["rendered_chars"] for row in checks),
        "source_anchor_ok_rows": len(valid_anchor_rows),
        "grouping": grouping,
    }


def artifact_size(artifact):
    text = artifact["rendered_text"]
    return {
        "lines": len(artifact["front"]) + len(artifact["back"]) + len(artifact["full"]),
        "chars": len(text),
        "front_lines": len(artifact["front"]),
        "front_chars": len("\n".join(artifact["front"])),
        "has_full": bool(artifact["full"]),
        "pointer_count": sum(1 for line in artifact["front"] + artifact["back"] + artifact["full"] if "pointer:" in line or "path=" in line),
    }


def by_id(artifacts):
    return {artifact["case_id"]: artifact for artifact in artifacts}


def reduction(before, after):
    return round((before - after) / before * 100, 1) if before else 0.0


def review_proxy(sizes):
    # Proxy only: chars dominate, expansions and pointers add a navigation cost.
    return sum(size["chars"] / 90 + size["lines"] * 0.25 + (4 if size["has_full"] else 0) + size["pointer_count"] * 0.4 for size in sizes)


def paired_metrics(gold, baseline_artifacts, candidate_artifacts, subset=None):
    baseline = by_id(baseline_artifacts)
    candidate = by_id(candidate_artifacts)
    ids = list(candidate)
    if subset:
        ids = [cid for cid in ids if subset(cid, gold[cid])]

    baseline_sizes = [artifact_size(baseline[cid]) for cid in ids]
    candidate_sizes = [artifact_size(candidate[cid]) for cid in ids]

    before_lines = sum(size["lines"] for size in baseline_sizes)
    after_lines = sum(size["lines"] for size in candidate_sizes)
    before_chars = sum(size["chars"] for size in baseline_sizes)
    after_chars = sum(size["chars"] for size in candidate_sizes)
    before_front_chars = sum(size["front_chars"] for size in baseline_sizes)
    after_front_chars = sum(size["front_chars"] for size in candidate_sizes)
    before_proxy = review_proxy(baseline_sizes)
    after_proxy = review_proxy(candidate_sizes)

    return {
        "case_count": len(ids),
        "rendered_line_reduction_pct": reduction(before_lines, after_lines),
        "rendered_char_reduction_pct": reduction(before_chars, after_chars),
        "front_char_reduction_pct": reduction(before_front_chars, after_front_chars),
        "review_proxy_delta_pct": round((after_proxy - before_proxy) / before_proxy * 100, 1) if before_proxy else 0.0,
        "baseline_lines": before_lines,
        "candidate_lines": after_lines,
        "baseline_chars": before_chars,
        "candidate_chars": after_chars,
    }


def make_report(result):
    candidate = result["variants"]["shell_core_plus_recurrence"]
    core = result["variants"]["shell_core"]
    control = result["variants"].get("shell_core_plus_unversioned_control")
    lines = [
        "# VAKS 480 Real-Data Paired Pilot Report",
        "",
        "Status: sandbox-only pilot. No main-vault writeback, no SCHEMA change, no operation-convention promotion.",
        "",
        "## Verdict",
        "",
        f"`shell_core`: safety_pass={core['summary']['safety_pass']}.",
        f"`shell_core_plus_recurrence`: safety_pass={candidate['summary']['safety_pass']}.",
    ]
    if control:
        lines.append(f"`shell_core_plus_unversioned_control`: safety_pass={control['summary']['safety_pass']} (negative control).")
    lines.extend(
        [
            "",
            "Interpretation: core shell is the minimum design under test; recurrence bundle is only evaluated as an optional add-on for recurrence-heavy slices.",
            "",
            "## Dataset Mix",
            "",
            "| family | cases | source status | fetched rows |",
            "| --- | ---: | --- | ---: |",
        ]
    )
    for family, row in result["dataset_manifest"].items():
        lines.append(f"| {family} | {row['pilot_cases']} | {row['source_status']} | {row['fetched_rows']} |")

    for variant_name, payload in result["variants"].items():
        summary = payload["summary"]
        lines.extend(
            [
                "",
                f"## {variant_name}",
                "",
                "| hard gate | count |",
                "| --- | ---: |",
            ]
        )
        for key, value in summary["hard_failures"].items():
            lines.append(f"| {key} | {value} |")
        lines.extend(
            [
                f"| safety_pass | {summary['safety_pass']} |",
                f"| front_budget_warnings | {summary['front_budget_warnings']} |",
                f"| grouping_recall | {summary['grouping']['grouping_recall']} |",
                f"| severe_over_grouping | {len(summary['grouping']['severe_over_grouping'])} |",
                "",
                "| paired metric | all cases | ordinary slice | serious slice | recurrence slice |",
                "| --- | ---: | ---: | ---: | ---: |",
            ]
        )
        paired = payload["paired"]
        metric_keys = [
            "rendered_line_reduction_pct",
            "rendered_char_reduction_pct",
            "front_char_reduction_pct",
            "review_proxy_delta_pct",
        ]
        for key in metric_keys:
            lines.append(
                f"| {key} | {paired['all'][key]} | {paired['ordinary'][key]} | {paired['serious'][key]} | {paired['recurrence'][key]} |"
            )
        lines.extend(
            [
                "",
                "| front realism metric | value |",
                "| --- | ---: |",
                f"| front_chars_p50 | {summary['front_chars_p50']} |",
                f"| front_chars_p95 | {summary['front_chars_p95']} |",
                f"| max_front_line_chars_p95 | {summary['max_front_line_chars_p95']} |",
            ]
        )

    lines.extend(
        [
            "",
            "## Alpha Readout",
            "",
            "- Strongest core alpha: hard-trigger shell + required unresolved gate + anchor health strip + sparse provenance pointer. It is the minimum set that preserves serious escalation while reducing ordinary surface.",
            "- Positive optional alpha: representative recurrence card + open-only versioned dedup. It should stay scoped to recurrence-heavy, ordinary, valid-anchor items; serious, regressed, challenge, action-basis, and anchor-problem members break out.",
            "- Guardrail-only items: authority boundary lint and categorical feedback wording. They are useful constraints, not value engines and not truth authority.",
            "",
            "## Limits",
            "",
            "- This is a real-row paired shell pilot with deterministic pressure overlays; it does not adjudicate factual truth of dataset claims.",
            "- Review-time numbers are proxy units, not observed human timings.",
            "- Anchor resolution is local path/marker plus record/evidence file resolution, not a full UI selector click-through.",
            "- Grouping still depends on supplied recurrence fields; messy extraction remains a future runtime risk.",
        ]
    )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", required=True)
    parser.add_argument("--dataset-manifest", required=True)
    parser.add_argument("--baseline-artifacts", required=True)
    parser.add_argument("--variant", action="append", nargs=3, metavar=("NAME", "ARTIFACTS", "CHECKS"), required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-report", required=True)
    args = parser.parse_args()

    gold = load_json(args.gold)
    dataset_manifest = load_json(args.dataset_manifest)
    baseline_artifacts = load_json(args.baseline_artifacts)

    result = {"dataset_manifest": dataset_manifest, "variants": {}}
    for name, artifacts_path, checks_path in args.variant:
        artifacts = load_json(artifacts_path)
        checks_payload = load_json(checks_path)
        checks = checks_payload["checks"]
        summary = summarize_checks(checks, checks_payload["grouping"])
        paired = {
            "all": paired_metrics(gold, baseline_artifacts, artifacts),
            "ordinary": paired_metrics(gold, baseline_artifacts, artifacts, lambda _cid, g: not g["full_audit"] and g["state"] in {"ordinary", "resolved_folded", "parked_nonblocking"}),
            "serious": paired_metrics(gold, baseline_artifacts, artifacts, lambda _cid, g: g["full_audit"] or g["queue_visible"]),
            "recurrence": paired_metrics(gold, baseline_artifacts, artifacts, lambda _cid, g: bool(g.get("recurrence_candidate"))),
        }
        result["variants"][name] = {"summary": summary, "paired": paired}

    Path(args.out_json).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.out_report).write_text(make_report(result), encoding="utf-8")
    print(f"wrote {args.out_report}")


if __name__ == "__main__":
    main()
