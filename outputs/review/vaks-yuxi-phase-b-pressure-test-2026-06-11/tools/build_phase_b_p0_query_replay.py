import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

import run_phase_b_pressure as harness


SANDBOX_DIR = harness.SANDBOX_DIR
RESULTS_DIR = harness.RESULTS_DIR

REPLAY_PATH = RESULTS_DIR / "phase_b_p0_query_level_replay.csv"
QUERY_METRICS_PATH = RESULTS_DIR / "phase_b_p0_query_level_metrics.csv"
SUMMARY_PATH = RESULTS_DIR / "phase_b_p0_summary.csv"
CLEAN_TOP_RESULTS_PATH = RESULTS_DIR / "phase_b_p0_clean_vaks_only_top_results.csv"
CLEAN_QUERY_METRICS_PATH = RESULTS_DIR / "phase_b_p0_clean_vaks_only_query_metrics.csv"
CLEAN_SUMMARY_PATH = RESULTS_DIR / "phase_b_p0_clean_vaks_only_summary.csv"
METRIC_DICT_JSON = RESULTS_DIR / "phase_b_metric_dictionary.json"
METRIC_DICT_MD = SANDBOX_DIR / "PHASE_B_METRIC_DICTIONARY.md"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_P0_QUERY_LEVEL_REPLAY_REPORT.md"

CLEAN_MODE = "vaks_only_lexical_bucket"
METRIC_TOP_K = 20
REPLAY_TOP_K = 10
TOP_K = METRIC_TOP_K
GOVERNANCE_K = 10
MODE_ORDER = [
    "baseline_file_lexical",
    "vaks_b_bucketless",
    "vaks_b_bucket_local",
    "vaks_b_adapter_v1",
    "vaks_b_adapter_v1_1",
    "vaks_b_adapter_skeleton",
    "yuxi_native_profile",
    CLEAN_MODE,
]
TEST_SETS = {
    "main": {
        "query_file": SANDBOX_DIR / "queries_phase_b.jsonl",
        "top_results": RESULTS_DIR / "phase_b_top_results.csv",
        "query_metrics": RESULTS_DIR / "phase_b_query_metrics.csv",
        "summary": RESULTS_DIR / "phase_b_summary.csv",
    },
    "holdout_used": {
        "query_file": SANDBOX_DIR / "queries_phase_b_holdout.jsonl",
        "top_results": RESULTS_DIR / "phase_b_holdout_top_results.csv",
        "query_metrics": RESULTS_DIR / "phase_b_holdout_query_metrics.csv",
        "summary": RESULTS_DIR / "phase_b_holdout_summary.csv",
    },
}

TOP_RESULT_FIELDS = [
    "corpus",
    "mode",
    "query_id",
    "query_group",
    "intent",
    "rank",
    "path",
    "heading",
    "score",
    "bucket",
    "status",
    "record_kind",
    "selector_or_line_range",
    "retrieval_reasons",
    "warning_code",
    "authority_badge",
    "usage_badge",
    "temporal_badge",
    "stale",
    "source_hash",
    "chunk_hash",
    "local_bucket_rank",
    "snippet",
]


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames or list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def truthy(value) -> bool:
    return value is True or str(value).lower() == "true"


def avg_bool(values) -> float:
    items = list(values)
    if not items:
        return 0.0
    return sum(1 for item in items if item) / len(items)


def f4(value: float) -> str:
    return f"{value:.4f}"


def bool_text(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return "true" if str(value).lower() == "true" else "false"


def load_queries(path: Path) -> dict[str, dict]:
    return {query["id"]: query for query in harness.load_queries(path)}


def path_heading_hits(chunk: harness.Chunk, query_text: str) -> int:
    blob = f"{chunk.path} {chunk.heading}".lower()
    terms = harness.query_terms_for_ranking(query_text)
    phrases = harness.query_phrases_for_ranking(query_text)
    return sum(1 for term in terms if term in blob) + (2 * sum(1 for phrase in phrases if phrase in blob))


def search_vaks_only_lexical(index: harness.CorpusIndex, query: dict, top_k: int) -> list[harness.SearchResult]:
    scores = index.chunk_bm25.scores(query["query"])
    candidate_ids = harness.ranked_indices(scores, limit=250)
    if not candidate_ids:
        return []

    local_ranks: dict[int, int] = {}
    by_bucket: dict[str, list[int]] = defaultdict(list)
    for idx in candidate_ids:
        by_bucket[index.chunks[idx].bucket].append(idx)
    for bucket, ids in by_bucket.items():
        ids.sort(
            key=lambda idx: (
                harness.support_source_priority(index.chunks[idx], query["intent"]),
                -float(scores[idx]),
                -path_heading_hits(index.chunks[idx], query["query"]),
                index.chunks[idx].path,
            )
        )
        for rank, idx in enumerate(ids, start=1):
            local_ranks[idx] = rank

    candidate_ids.sort(
        key=lambda idx: (
            harness.authority_priority(index.chunks[idx].bucket, query["intent"]),
            harness.support_source_priority(index.chunks[idx], query["intent"]),
            local_ranks.get(idx, 999999),
            -float(scores[idx]),
            -path_heading_hits(index.chunks[idx], query["query"]),
            index.chunks[idx].path,
        )
    )

    results: list[harness.SearchResult] = []
    for rank, idx in enumerate(candidate_ids[:top_k], start=1):
        chunk = index.chunks[idx]
        warning = harness.warning_for(chunk, query["intent"], True)
        temporal = "stale" if chunk.stale else ""
        if chunk.stale:
            warning = "stale_index" if not warning else f"{warning};stale_index"
        reasons = ["lexical"]
        if path_heading_hits(chunk, query["query"]):
            reasons.append("path_heading_rerank")
        results.append(
            harness.SearchResult(
                mode=CLEAN_MODE,
                rank=rank,
                path=chunk.path,
                heading=chunk.heading,
                text=chunk.text[:1600],
                score=float(scores[idx]),
                bucket=chunk.bucket,
                status=chunk.status,
                record_kind=chunk.record_kind,
                source_hash=chunk.source_hash,
                chunk_hash=chunk.chunk_hash,
                selector_or_line_range=chunk.selector_or_line_range,
                retrieval_reasons=reasons,
                warning_code=warning,
                authority_badge=harness.authority_badge_for(chunk, True),
                usage_badge=harness.usage_badge_for(chunk, query["intent"], True),
                temporal_badge=temporal,
                stale=chunk.stale,
                adapter_present=True,
                clickback_present=True,
                hash_present=True,
                receipt_present=True,
                local_bucket_rank=local_ranks.get(idx),
            )
        )
    return results


def search_mode(index: harness.CorpusIndex, query: dict, mode: str, top_k: int) -> list[harness.SearchResult]:
    if mode == "baseline_file_lexical":
        return harness.search_baseline(index, query, top_k)
    if mode == CLEAN_MODE:
        return search_vaks_only_lexical(index, query, top_k)
    return harness.search_chunk_mode(index, query, mode, top_k)


def result_to_enriched_dict(query: dict, result: harness.SearchResult, corpus: str, test_set: str) -> dict:
    row = harness.result_to_dict(query, result, corpus)
    row["test_set"] = test_set
    row["result_hits_expected"] = bool_text(harness.term_hit(result, query.get("expected_terms") or []))
    row["clickback_present"] = bool_text(result.clickback_present)
    row["hash_present"] = bool_text(result.hash_present)
    row["adapter_present"] = bool_text(result.adapter_present)
    row["receipt_present"] = bool_text(result.receipt_present)
    return row


def build_p0_rows() -> tuple[list[dict], list[dict], list[dict]]:
    top_rows: list[dict] = []
    query_rows: list[dict] = []
    stale_paths = {"SCHEMA.md", "SOURCE_INTAKE.md", "FEEDBACK.md"}
    for test_set, config in TEST_SETS.items():
        queries = list(load_queries(config["query_file"]).values())
        for corpus in ["primary", "full"]:
            index = harness.CorpusIndex(corpus, stale_paths=stale_paths)
            resolvable_cache = {
                query["id"]: harness.terms_resolvable(index, query.get("expected_terms") or []) for query in queries
            }
            for query in queries:
                for mode in MODE_ORDER:
                    results = search_mode(index, query, mode, TOP_K)
                    metric = harness.evaluate_results(query, results, resolvable_cache[query["id"]])
                    metric.update({"test_set": test_set, "corpus": corpus, "mode": mode})
                    query_rows.append(metric)
                    for result in results:
                        top_rows.append(result_to_enriched_dict(query, result, corpus, test_set))
    summary_rows: list[dict] = []
    for test_set in TEST_SETS:
        scoped = [row for row in query_rows if row["test_set"] == test_set]
        for row in harness.summarize_metrics(scoped):
            row["test_set"] = test_set
            summary_rows.append(row)
    return top_rows, query_rows, summary_rows


def build_clean_control() -> tuple[list[dict], list[dict], list[dict]]:
    top_rows: list[dict] = []
    query_rows: list[dict] = []
    for test_set, config in TEST_SETS.items():
        queries = list(load_queries(config["query_file"]).values())
        for corpus in ["primary", "full"]:
            index = harness.CorpusIndex(corpus)
            for query in queries:
                results = search_vaks_only_lexical(index, query, top_k=METRIC_TOP_K)
                resolvable = harness.terms_resolvable(index, query.get("expected_terms") or [])
                metric = harness.evaluate_results(query, results, resolvable)
                metric.update({"test_set": test_set, "corpus": corpus, "mode": CLEAN_MODE})
                query_rows.append(metric)
                for result in results[:REPLAY_TOP_K]:
                    top_rows.append(result_to_enriched_dict(query, result, corpus, test_set))
    summary_rows = []
    for test_set in ["main", "holdout_used"]:
        scoped = [row for row in query_rows if row["test_set"] == test_set]
        for row in harness.summarize_metrics(scoped):
            row["test_set"] = test_set
            summary_rows.append(row)
    return top_rows, query_rows, summary_rows


def load_existing_rows() -> tuple[list[dict], list[dict], list[dict]]:
    top_rows: list[dict] = []
    query_rows: list[dict] = []
    summary_rows: list[dict] = []
    for test_set, config in TEST_SETS.items():
        for row in read_csv(config["top_results"]):
            row["test_set"] = test_set
            top_rows.append(row)
        for row in read_csv(config["query_metrics"]):
            row["test_set"] = test_set
            query_rows.append(row)
        for row in read_csv(config["summary"]):
            row["test_set"] = test_set
            summary_rows.append(row)
    return top_rows, query_rows, summary_rows


def build_hit_text_lookup() -> dict[str, dict]:
    lookup: dict[str, dict] = {}
    for corpus in ["primary", "full"]:
        files = harness.build_file_docs(corpus)
        chunks = harness.build_chunks(files, set())
        lookup[corpus] = {
            "files": {doc.path: doc.text[:1200] for doc in files},
            "chunks_by_hash": {chunk.chunk_hash: chunk.text[:1600] for chunk in chunks},
            "chunks_by_key": {
                (chunk.path, chunk.heading, chunk.selector_or_line_range): chunk.text[:1600] for chunk in chunks
            },
        }
    return lookup


def top_row_hit(row: dict, expected_terms: list[str], lookup: dict[str, dict]) -> str:
    if "result_hits_expected" in row:
        return bool_text(row["result_hits_expected"])
    corpus_lookup = lookup[row["corpus"]]
    if row["mode"] == "baseline_file_lexical":
        text = corpus_lookup["files"].get(row["path"], row.get("snippet", ""))
    else:
        text = ""
        if row.get("chunk_hash"):
            text = corpus_lookup["chunks_by_hash"].get(row["chunk_hash"], "")
        if not text:
            key = (row["path"], row["heading"], row.get("selector_or_line_range", ""))
            text = corpus_lookup["chunks_by_key"].get(key, row.get("snippet", ""))
    blob = f"{row.get('path','')}\n{row.get('heading','')}\n{text}".lower()
    return bool_text(any(term.lower() in blob for term in expected_terms))


def result_presence(row: dict, field: str) -> str:
    if field in row:
        return bool_text(row[field])
    mode = row["mode"]
    adapter_mode = mode in harness.VAKS_ADAPTER_MODES or mode == CLEAN_MODE
    if field == "clickback_present":
        return bool_text(mode != "baseline_file_lexical")
    if field in {"hash_present", "adapter_present", "receipt_present"}:
        return bool_text(adapter_mode)
    return "false"


def summarize_p0_metrics(rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(row["test_set"], row["corpus"], row["mode"])].append(row)

    summary: list[dict] = []
    for (test_set, corpus, mode), items in sorted(grouped.items()):
        resolvable = [row for row in items if truthy(row.get("resolvable"))]
        base = resolvable or items
        risk = [row for row in items if row["intent"] in {"action", "evidence"}]
        stale = [row for row in items if row["group"] in {"stale_pressure", "holdout_stale"}]
        stale_exposed = sum(int(row.get("stale_exposed") or 0) for row in stale)
        stale_detected = sum(int(row.get("stale_detected") or 0) for row in stale)
        summary.append(
            {
                "test_set": test_set,
                "corpus": corpus,
                "mode": mode,
                "queries": len(items),
                "resolvable_queries": len(resolvable),
                "hit_at_5": f"{sum(1 for row in base if truthy(row.get('hit_at_5')))}/{len(base)}",
                "hit_at_10": f"{sum(1 for row in base if truthy(row.get('hit_at_10')))}/{len(base)}",
                "mrr": f4(statistics.mean(float(row.get("mrr") or 0.0) for row in base)),
                "action_leakage_rate": f4(avg_bool(truthy(row.get("action_leakage")) for row in risk)) if risk else "0.0000",
                "forbidden_top1_rate": f4(avg_bool(truthy(row.get("forbidden_top1")) for row in risk)) if risk else "0.0000",
                "cross_bucket_violation_rate": f4(avg_bool(truthy(row.get("cross_bucket_authority_violation")) for row in risk)) if risk else "0.0000",
                "warning_coverage_risk": f4(statistics.mean(float(row.get("warning_coverage") or 0.0) for row in risk)) if risk else "1.0000",
                "clickback_coverage": f4(statistics.mean(float(row.get("clickback_coverage") or 0.0) for row in items)),
                "hash_coverage": f4(statistics.mean(float(row.get("hash_coverage") or 0.0) for row in items)),
                "adapter_coverage": f4(statistics.mean(float(row.get("adapter_coverage") or 0.0) for row in items)),
                "receipt_coverage": f4(statistics.mean(float(row.get("receipt_coverage") or 0.0) for row in items)),
                "stale_detection_rate": f4((stale_detected / stale_exposed) if stale_exposed else 0.0),
            }
        )
    return summary


def build_replay(top_rows: list[dict], query_rows: list[dict]) -> list[dict]:
    query_by_set: dict[str, dict[str, dict]] = {
        test_set: load_queries(config["query_file"]) for test_set, config in TEST_SETS.items()
    }
    hit_lookup = build_hit_text_lookup()
    metric_by_key = {
        (row["test_set"], row["corpus"], row["mode"], row["query_id"]): row for row in query_rows
    }
    replay = []
    for row in top_rows:
        query = query_by_set[row["test_set"]][row["query_id"]]
        metric = metric_by_key[(row["test_set"], row["corpus"], row["mode"], row["query_id"])]
        expected_terms = query.get("expected_terms") or []
        result_hits_expected = top_row_hit(row, expected_terms, hit_lookup)
        bucket = row["bucket"]
        risky_bucket = bucket in harness.RISK_BUCKETS
        support_bucket = bucket in harness.SUPPORT_BUCKETS
        rank = int(row["rank"])
        warning_code = row.get("warning_code") or ""
        replay.append(
            {
                "test_set": row["test_set"],
                "corpus": row["corpus"],
                "mode": row["mode"],
                "query_id": row["query_id"],
                "query_group": row["query_group"],
                "intent": row["intent"],
                "query_text": query["query"],
                "expected_terms_json": json.dumps(expected_terms, ensure_ascii=False),
                "needs_boundary_warning": bool_text(query.get("needs_boundary_warning", False)),
                "query_resolvable": bool_text(metric["resolvable"]),
                "query_hit_at_5": bool_text(metric["hit_at_5"]),
                "query_hit_at_10": bool_text(metric["hit_at_10"]),
                "query_mrr": metric["mrr"],
                "query_first_hit_rank": metric["first_hit_rank"],
                "query_action_leakage": bool_text(metric["action_leakage"]),
                "query_forbidden_top1": bool_text(metric["forbidden_top1"]),
                "query_cross_bucket_violation": bool_text(metric["cross_bucket_authority_violation"]),
                "query_warning_coverage": metric["warning_coverage"],
                "query_clickback_coverage": metric["clickback_coverage"],
                "query_hash_coverage": metric["hash_coverage"],
                "query_adapter_coverage": metric["adapter_coverage"],
                "query_receipt_coverage": metric["receipt_coverage"],
                "query_stale_exposed": metric["stale_exposed"],
                "query_stale_detected": metric["stale_detected"],
                "rank": row["rank"],
                "path": row["path"],
                "heading": row["heading"],
                "score": row["score"],
                "bucket": bucket,
                "is_support_bucket": bool_text(support_bucket),
                "is_risky_bucket": bool_text(risky_bucket),
                "status": row["status"],
                "record_kind": row["record_kind"],
                "selector_or_line_range": row.get("selector_or_line_range", ""),
                "retrieval_reasons": row.get("retrieval_reasons", ""),
                "warning_code": warning_code,
                "authority_badge": row.get("authority_badge", ""),
                "usage_badge": row.get("usage_badge", ""),
                "temporal_badge": row.get("temporal_badge", ""),
                "stale": bool_text(row.get("stale", "")),
                "source_hash_present": bool_text(bool(row.get("source_hash", ""))),
                "chunk_hash_present": bool_text(bool(row.get("chunk_hash", ""))),
                "local_bucket_rank": row.get("local_bucket_rank", ""),
                "metric_result_limit": METRIC_TOP_K,
                "replay_result_limit": REPLAY_TOP_K,
                "governance_window": GOVERNANCE_K,
                "clickback_present": result_presence(row, "clickback_present"),
                "hash_present": result_presence(row, "hash_present"),
                "adapter_present": result_presence(row, "adapter_present"),
                "receipt_present": result_presence(row, "receipt_present"),
                "result_hits_expected": result_hits_expected,
                "result_forbidden_top1": bool_text(
                    rank == 1 and row["intent"] in {"action", "evidence"} and not support_bucket
                ),
                "result_unlabelled_risky": bool_text(risky_bucket and not warning_code),
                "snippet": row.get("snippet", ""),
            }
        )
    return replay


def write_metric_dictionary() -> None:
    metrics = [
        {
            "metric": "hit_at_5",
            "level": "query aggregate",
            "definition": "A query is counted when the harness first_hit_rank over the top20 local run is <= 5.",
            "denominator": "Resolvable queries for that test_set/corpus/mode.",
            "notes": "Top10 replay independently checks rows whose first_hit_rank is within 10; ranks >10 remain query-level paired outcomes.",
        },
        {
            "metric": "hit_at_10",
            "level": "query aggregate",
            "definition": "A query is counted when the harness first_hit_rank over the top20 local run is <= 10.",
            "denominator": "Resolvable queries for that test_set/corpus/mode.",
            "notes": "Top10 replay should contain the matching hit when this metric is true.",
        },
        {
            "metric": "mrr",
            "level": "query aggregate",
            "definition": "Mean reciprocal rank over the local top20 run; query contribution is 1 / first_hit_rank, or 0 if no expected-term hit appears in top20.",
            "denominator": "Resolvable queries for that test_set/corpus/mode.",
            "notes": "This is a retrieval diagnostic, not truth confidence.",
        },
        {
            "metric": "action_leakage_rate",
            "level": "risk-query aggregate",
            "definition": "For action/evidence queries, true when top1 is not support bucket or any risky top10 result has no warning.",
            "denominator": "Queries whose intent is action or evidence.",
            "notes": "This is the strongest current governance signal.",
        },
        {
            "metric": "forbidden_top1_rate",
            "level": "risk-query aggregate",
            "definition": "For action/evidence queries, true when rank 1 is not in support buckets.",
            "denominator": "Queries whose intent is action or evidence.",
            "notes": "Support buckets are core_framework and reviewed.",
        },
        {
            "metric": "cross_bucket_violation_rate",
            "level": "risk-query aggregate",
            "definition": "For action/evidence queries, true when risky buckets appear before the first support bucket in top10, or no support appears.",
            "denominator": "Queries whose intent is action or evidence.",
            "notes": "Measures authority-like ranking collapse.",
        },
        {
            "metric": "warning_coverage_risk",
            "level": "risk-query aggregate",
            "definition": "For risky top10 results, fraction that carry a warning_code; if no risky result appears, the query receives 1.0.",
            "denominator": "Risky top10 results within each risk query, then averaged by query.",
            "notes": "Soft guardrail only; not a hard safety control.",
        },
        {
            "metric": "clickback_coverage",
            "level": "query aggregate",
            "definition": "Average top10 fraction with clickback-present behavior.",
            "denominator": "Top10 result rows per query, then averaged by query.",
            "notes": "Baseline file lexical has 0 by design in the current harness.",
        },
        {
            "metric": "hash_coverage",
            "level": "query aggregate",
            "definition": "Average top10 fraction with source_hash/chunk_hash available.",
            "denominator": "Top10 result rows per query, then averaged by query.",
            "notes": "Used for auditability, not evidence support.",
        },
        {
            "metric": "receipt_coverage",
            "level": "query aggregate",
            "definition": "Average top10 fraction produced through adapter receipt behavior.",
            "denominator": "Top10 result rows per query, then averaged by query.",
            "notes": "Receipt does not create action basis.",
        },
        {
            "metric": "stale_detection_rate",
            "level": "stale query aggregate",
            "definition": "Detected stale top10 results divided by exposed stale top10 results for stale-pressure queries, including holdout_stale.",
            "denominator": "Exposed stale results in stale-pressure queries.",
            "notes": "P0 fixes the earlier ambiguity where holdout_stale was not counted by the older summary helper.",
        },
    ]
    payload = {
        "artifact_kind": "vaks_phase_b_metric_dictionary",
        "truth_boundary": "metric_dictionary_not_truth_layer",
        "action_basis_allowed": False,
        "metric_result_limit": METRIC_TOP_K,
        "replay_result_limit": REPLAY_TOP_K,
        "governance_window": GOVERNANCE_K,
        "support_buckets": sorted(harness.SUPPORT_BUCKETS),
        "risk_buckets": sorted(harness.RISK_BUCKETS),
        "metrics": metrics,
    }
    METRIC_DICT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "---",
        "record_kind: sandbox_metric_dictionary",
        "status: candidate",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: metric_dictionary_not_truth_layer",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Metric Dictionary",
        "",
        "This file defines the current sandbox metrics. It is diagnostic only.",
        "",
        "| Metric | Level | Definition | Denominator | Notes |",
        "|---|---|---|---|---|",
    ]
    for metric in metrics:
        lines.append(
            f"| {metric['metric']} | {metric['level']} | {metric['definition']} | {metric['denominator']} | {metric['notes']} |"
        )
    lines.append("")
    METRIC_DICT_MD.write_text("\n".join(lines), encoding="utf-8")


def write_report(summary_rows: list[dict], clean_summary_rows: list[dict], replay_rows: list[dict]) -> None:
    def row_for(test_set: str, corpus: str, mode: str) -> dict:
        for row in summary_rows:
            if row["test_set"] == test_set and row["corpus"] == corpus and row["mode"] == mode:
                return row
        return {}

    lines = [
        "---",
        "record_kind: sandbox_p0_query_level_replay_report",
        "status: candidate",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: query_replay_not_mainline_decision",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B P0 Query-Level Replay Report",
        "",
        "## What This Adds",
        "",
        "```text",
        "query-level top10 replay plus top20 paired query outcomes for existing 45 queries",
        "metric dictionary with denominators",
        "clean VAKS-only lexical + authority-bucket control",
        "replay rows that can be independently recomputed",
        "```",
        "",
        "## Scope",
        "",
        "```text",
        f"replay rows: {len(replay_rows)}",
        "query sets: main 30, holdout_used 15",
        "corpora: primary, full",
        f"metric_result_limit: top{METRIC_TOP_K}",
        f"replay_result_limit: top{REPLAY_TOP_K}",
        f"governance_window: top{GOVERNANCE_K}",
        "real original Yuxi runtime: not run",
        "new blind adversarial set: not included in this P0 replay",
        "```",
        "",
        "## Clean Control Snapshot",
        "",
        "| Test Set | Corpus | Mode | hit@5 | MRR | action leakage | forbidden top1 | cross-bucket |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for test_set in ["main", "holdout_used"]:
        for corpus in ["primary", "full"]:
            for mode in ["vaks_only_lexical_bucket", "vaks_b_bucket_local", "vaks_b_adapter_skeleton", "yuxi_native_profile"]:
                row = row_for(test_set, corpus, mode)
                if row:
                    lines.append(
                        "| {test_set} | {corpus} | {mode} | {hit_at_5} | {mrr} | {action_leakage_rate} | {forbidden_top1_rate} | {cross_bucket_violation_rate} |".format(
                            **row
                        )
                    )
    lines.extend(
        [
            "",
            "## Evidence Boundary",
            "",
            "```text",
            "This report fixes auditability gaps for existing local queries.",
            "It does not answer whether original Yuxi runtime can reproduce the effect.",
        "It does not create a fresh blind holdout.",
        "It corrects the P0 stale_detection_rate denominator to include holdout_stale.",
        "It does not approve C-lite, writeback, action basis, or runtime adoption.",
            "```",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    existing_top, existing_query, _existing_summary = load_existing_rows()
    clean_top, clean_query, clean_summary = build_clean_control()
    all_top = existing_top + clean_top
    all_query = existing_query + clean_query
    all_summary = summarize_p0_metrics(all_query)
    clean_summary = [row for row in all_summary if row["mode"] == CLEAN_MODE]
    write_csv(CLEAN_TOP_RESULTS_PATH, clean_top)
    write_csv(CLEAN_QUERY_METRICS_PATH, clean_query)
    write_csv(CLEAN_SUMMARY_PATH, clean_summary)
    replay = build_replay(all_top, all_query)
    write_csv(REPLAY_PATH, replay)
    write_csv(QUERY_METRICS_PATH, all_query)
    write_csv(SUMMARY_PATH, all_summary)
    write_metric_dictionary()
    write_report(all_summary, clean_summary, replay)
    print(f"replay rows: {len(replay)}")
    print(f"query metric rows: {len(all_query)}")
    print(f"summary rows: {len(all_summary)}")


if __name__ == "__main__":
    main()
