import csv
import json
from pathlib import Path

import build_phase_b_p0_query_replay as p0
import run_phase_b_pressure as harness


SANDBOX_DIR = harness.SANDBOX_DIR
RESULTS_DIR = harness.RESULTS_DIR
QUERY_FILE = SANDBOX_DIR / "queries_phase_b_agent_blind.jsonl"
AUDIT_JSON = RESULTS_DIR / "phase_b_agent_blind_audit.json"
COMBINED_SUMMARY = RESULTS_DIR / "phase_b_agent_blind_combined_summary.csv"
CLEAN_TOP = RESULTS_DIR / "phase_b_agent_blind_clean_vaks_only_top_results.csv"
CLEAN_QUERY = RESULTS_DIR / "phase_b_agent_blind_clean_vaks_only_query_metrics.csv"
CLEAN_SUMMARY = RESULTS_DIR / "phase_b_agent_blind_clean_vaks_only_summary.csv"
REPORT = SANDBOX_DIR / "PHASE_B_AGENT_BLIND_AUDIT_REPORT.md"
CLEAN_MODE = p0.CLEAN_MODE


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_hit(value: str) -> tuple[int, int]:
    a, b = value.split("/", 1)
    return int(a), int(b)


def fnum(row: dict, key: str) -> float:
    return float(row.get(key) or 0.0)


def build_clean_control() -> tuple[list[dict], list[dict], list[dict]]:
    top_rows: list[dict] = []
    query_rows: list[dict] = []
    queries = harness.load_queries(QUERY_FILE)
    stale_paths = {"SCHEMA.md", "SOURCE_INTAKE.md", "FEEDBACK.md"}
    for corpus in ["primary", "full"]:
        index = harness.CorpusIndex(corpus, stale_paths=stale_paths)
        resolvable_cache = {
            query["id"]: harness.terms_resolvable(index, query.get("expected_terms") or []) for query in queries
        }
        for query in queries:
            results = p0.search_vaks_only_lexical(index, query, p0.METRIC_TOP_K)
            metric = harness.evaluate_results(query, results, resolvable_cache[query["id"]])
            metric.update({"test_set": "agent_blind", "corpus": corpus, "mode": CLEAN_MODE})
            query_rows.append(metric)
            for result in results[: p0.REPLAY_TOP_K]:
                top_rows.append(p0.result_to_enriched_dict(query, result, corpus, "agent_blind"))
    summary_rows = p0.summarize_p0_metrics(query_rows)
    return top_rows, query_rows, summary_rows


def row_for(rows: list[dict], corpus: str, mode: str) -> dict:
    for row in rows:
        if row["corpus"] == corpus and row["mode"] == mode:
            return row
    raise KeyError((corpus, mode))


def build_audit(combined_summary: list[dict]) -> dict:
    criteria = []
    for corpus in ["primary", "full"]:
        skeleton = row_for(combined_summary, corpus, "vaks_b_adapter_skeleton")
        baseline = row_for(combined_summary, corpus, "baseline_file_lexical")
        yuxi = row_for(combined_summary, corpus, "yuxi_native_profile")
        clean = row_for(combined_summary, corpus, CLEAN_MODE)
        sk_hit, total = parse_hit(skeleton["hit_at_5"])
        base_hit, _ = parse_hit(baseline["hit_at_5"])
        clean_hit, _ = parse_hit(clean["hit_at_5"])
        criteria.extend(
            [
                {
                    "criterion": f"{corpus}: skeleton_leakage_zero",
                    "passed": fnum(skeleton, "action_leakage_rate") == 0.0,
                    "observed": skeleton["action_leakage_rate"],
                },
                {
                    "criterion": f"{corpus}: skeleton_hit_not_below_baseline",
                    "passed": sk_hit >= base_hit,
                    "observed": f"{sk_hit}/{total} vs baseline {base_hit}/{total}",
                },
                {
                    "criterion": f"{corpus}: skeleton_mrr_directionally_above_yuxi_proxy",
                    "passed": fnum(skeleton, "mrr") > fnum(yuxi, "mrr"),
                    "observed": f"{skeleton['mrr']} vs yuxi_proxy {yuxi['mrr']}",
                },
                {
                    "criterion": f"{corpus}: skeleton_hit_above_clean_vaks_only",
                    "passed": sk_hit >= clean_hit,
                    "observed": f"{sk_hit}/{total} vs clean {clean_hit}/{total}",
                },
                {
                    "criterion": f"{corpus}: yuxi_proxy_leakage_nonzero",
                    "passed": fnum(yuxi, "action_leakage_rate") > 0.0,
                    "observed": yuxi["action_leakage_rate"],
                },
            ]
        )
    return {
        "artifact_kind": "phase_b_agent_blind_audit",
        "truth_boundary": "agent_blind_not_original_yuxi_runtime",
        "action_basis_allowed": False,
        "query_count": 30,
        "criteria": criteria,
        "passed_criteria": sum(1 for item in criteria if item["passed"]),
        "failed_criteria": sum(1 for item in criteria if not item["passed"]),
        "agent_blind_status": "pass" if all(item["passed"] for item in criteria) else "fail",
    }


def write_report(audit: dict, combined_summary: list[dict]) -> None:
    key_modes = [
        "baseline_file_lexical",
        CLEAN_MODE,
        "vaks_b_bucket_local",
        "vaks_b_adapter_skeleton",
        "yuxi_native_profile",
    ]
    lines = [
        "---",
        "record_kind: sandbox_agent_blind_audit_report",
        f"status: {audit['agent_blind_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: agent_blind_not_original_yuxi_runtime",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Agent-Blind Audit Report",
        "",
        "## Scope",
        "",
        "```text",
        "query_count: 30",
        "query_author: independent sub-agent without parent context",
        "query_author_restriction: no existing Phase B query/results/reports",
        "real original Yuxi runtime: not run",
        "decision: sandbox evidence only; no C-lite or writeback approval",
        "```",
        "",
        "## Summary",
        "",
        "| Corpus | Mode | hit@5 | MRR | action leakage | forbidden top1 | cross-bucket |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for corpus in ["primary", "full"]:
        for mode in key_modes:
            row = row_for(combined_summary, corpus, mode)
            lines.append(
                "| {corpus} | {mode} | {hit_at_5} | {mrr} | {action_leakage_rate} | {forbidden_top1_rate} | {cross_bucket_violation_rate} |".format(
                    **row
                )
            )
    lines.extend(["", "## Criteria", "", "| Criterion | Result | Observed |", "|---|---|---|"])
    for item in audit["criteria"]:
        lines.append(f"| {item['criterion']} | {'pass' if item['passed'] else 'fail'} | {item['observed']} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "```text",
            "This strengthens local pressure evidence with an independently generated query set.",
            "MRR-above-yuxi-proxy is a local directional criterion, not proof of decisive retrieval superiority.",
            "Action leakage is a ranking/governance proxy, not an answer-level safety verdict.",
            "It is not a substitute for original Yuxi runtime rerun.",
            "It is still local evaluation, not mainline adoption evidence by itself.",
            "```",
            "",
        ]
    )
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    clean_top, clean_query, clean_summary = build_clean_control()
    write_csv(CLEAN_TOP, clean_top)
    write_csv(CLEAN_QUERY, clean_query)
    write_csv(CLEAN_SUMMARY, clean_summary)
    existing_query = read_csv(RESULTS_DIR / "phase_b_agent_blind_query_metrics.csv")
    for row in existing_query:
        row["test_set"] = "agent_blind"
    combined_summary = p0.summarize_p0_metrics(existing_query + clean_query)
    write_csv(COMBINED_SUMMARY, combined_summary)
    audit = build_audit(combined_summary)
    AUDIT_JSON.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(audit, combined_summary)
    print(f"agent blind status: {audit['agent_blind_status']}")
    print(f"passed criteria: {audit['passed_criteria']}/{len(audit['criteria'])}")


if __name__ == "__main__":
    main()
