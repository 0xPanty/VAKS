import ast
import csv
import json
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"

PACKET_CSV = RESULTS_DIR / "phase_b_blind_relevance_judgment_packet.csv"
JUDGMENTS_CSV = RESULTS_DIR / "phase_b_blind_relevance_judgments.csv"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_INTERNAL_RELEVANCE_JUDGMENT_REPORT.md"

JUDGE_ID = "codex_internal_heuristic_judge_v1"


PROFILES = {
    "VAKS-BLIND-001": {
        "terms": ["authority bucket", "bucket", "rrf", "raw", "candidate", "reviewed", "overlay", "ranking"],
        "paths": ["SOURCE_INTAKE.md", "retrieval-layer-design", "FUSION_ARCHITECTURE"],
    },
    "VAKS-BLIND-002": {
        "terms": ["processing_tier", "knowledge_status", "heavy", "medium", "review", "promotion", "source intake"],
        "paths": ["SOURCE_INTAKE.md", "REFERENCE_REVIEW_PROTOCOL.md"],
    },
    "VAKS-BLIND-003": {
        "terms": ["candidate", "review queue", "promotion", "promotion_target", "review_status", "pattern"],
        "paths": ["REVIEW_QUEUE.md", "SOURCE_INTAKE.md", "wiki/patterns", "templates/library-review"],
    },
    "VAKS-BLIND-004": {
        "terms": ["source anchor", "source_range", "source span", "evidence", "url-only", "confidence cap", "support_refs"],
        "paths": ["SCHEMA.md", "SOURCE_INTAKE.md", "REFERENCE_REVIEW_PROTOCOL.md"],
    },
    "VAKS-BLIND-005": {
        "terms": ["retrieval score", "graph rank", "association score", "evidence support", "support_refs", "truth confidence"],
        "paths": ["SOURCE_INTAKE.md", "MEMORY_TIER.md", "DEV_CONTEXT.md", "graph-retrieval", "retrieval-layer-design"],
    },
    "VAKS-BLIND-006": {
        "terms": ["context pack", "action basis", "coverage", "evidence_sufficiency", "action_readiness", "answer-ready"],
        "paths": ["DEV_CONTEXT.md", "IMPLEMENTATION_BLUEPRINT.md", "context_pack", "context-pack"],
    },
    "VAKS-BLIND-007": {
        "terms": ["action basis", "evidence_sufficiency", "missing_evidence", "weak", "action_readiness", "needs_review"],
        "paths": ["DEV_CONTEXT.md", "IMPLEMENTATION_BLUEPRINT.md", "SOURCE_INTAKE.md", "evidence_sufficiency"],
    },
    "VAKS-BLIND-008": {
        "terms": ["feedback", "truth confidence", "review_due", "activation", "use ledger", "action_outcome"],
        "paths": ["FEEDBACK.md", "MEMORY_TIER.md", "REVIEW_QUEUE.md"],
    },
    "VAKS-BLIND-009": {
        "terms": ["feedback", "project_ref", "review_due", "scope", "anti-pattern", "project_non_borrow_scope"],
        "paths": ["FEEDBACK.md", "REVIEW_QUEUE.md", "project_lens", "project_overlays"],
    },
    "VAKS-BLIND-010": {
        "terms": ["candidate relation", "reviewed relation", "point_graph_fragment", "graph_path", "relation_state", "triplet"],
        "paths": ["SCHEMA.md", "graph-retrieval", "knowledge-graph-index"],
    },
    "VAKS-BLIND-011": {
        "terms": ["relation neighborhood", "candidate relation", "reviewed relation", "graph retrieval", "community report", "graph rank"],
        "paths": ["SCHEMA.md", "graph-retrieval", "knowledge-graph-index"],
    },
    "VAKS-BLIND-012": {
        "terms": ["temporal", "valid_until", "stale", "superseded", "applicability", "out_of_scope", "review_due"],
        "paths": ["SCHEMA.md", "FEEDBACK.md", "SOURCE_INTAKE.md", "Graphiti", "temporal"],
    },
    "VAKS-BLIND-013": {
        "terms": ["decision", "superseded", "replacement", "review_due", "out_of_scope", "decision outcome"],
        "paths": ["REVIEW_QUEUE.md", "wiki/decisions", "FEEDBACK.md"],
    },
    "VAKS-BLIND-014": {
        "terms": ["agent", "mcp", "read-only", "suggest-only", "reviewed-write", "write gate", "memory quarantine"],
        "paths": ["AGENTS.md", "IMPLEMENTATION_BLUEPRINT.md", "DEV_CONTEXT.md", "agent"],
    },
    "VAKS-BLIND-015": {
        "terms": ["adapter", "read-only", "retrieval receipt", "mcp", "skills", "writeback", "runtime adoption"],
        "paths": ["PHASE_B", "vaks-yuxi", "IMPLEMENTATION_BLUEPRINT.md", "SOURCE_INTAKE.md", "runtime"],
    },
    "VAKS-BLIND-016": {
        "terms": ["approval", "process evidence", "evidence support", "body_hash", "reviewed relation", "truth confidence"],
        "paths": ["REVIEW_QUEUE.md", "templates/maintenance-manifest", "SOURCE_INTAKE.md"],
    },
    "VAKS-BLIND-017": {
        "terms": ["context pack", "budget", "truncation", "warnings", "gaps", "risk", "coverage"],
        "paths": ["DEV_CONTEXT.md", "IMPLEMENTATION_BLUEPRINT.md", "context_pack", "context-pack"],
    },
    "VAKS-BLIND-018": {
        "terms": ["confidence cap", "source access quality", "abstract", "full text", "source range", "evidence granularity"],
        "paths": ["SOURCE_INTAKE.md", "REFERENCE_REVIEW_PROTOCOL.md", "SCHEMA.md"],
    },
}


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


def parse_list(value: str) -> list[str]:
    try:
        parsed = ast.literal_eval(value)
        return [str(item) for item in parsed] if isinstance(parsed, list) else []
    except Exception:
        return []


def score_row(row: dict) -> tuple[int, str]:
    profile = PROFILES[row["query_id"]]
    blob = "\n".join(
        [
            row.get("path", ""),
            row.get("heading", ""),
            row.get("bucket", ""),
            row.get("status", ""),
            row.get("warning_code", ""),
            row.get("snippet", ""),
        ]
    ).lower()
    terms = profile["terms"]
    path_terms = profile["paths"]
    matched_terms = [term for term in terms if term.lower() in blob]
    matched_paths = [term for term in path_terms if term.lower() in blob]
    criteria_terms = []
    for field in ["relevant_criteria", "borderline_criteria"]:
        for item in parse_list(row.get(field, "")):
            for token in item.replace("、", " ").replace("/", " ").split():
                if len(token) >= 4 and token.lower() in blob:
                    criteria_terms.append(token)
    criteria_terms = sorted(set(criteria_terms))[:6]

    score = len(matched_terms) + (2 * len(matched_paths)) + min(2, len(criteria_terms))
    if row.get("bucket") in {"core_framework", "reviewed"}:
        score += 1
    if row.get("bucket") in {"raw", "feedback"} and row["intent"] in {"action", "evidence"}:
        score -= 1

    if score >= 5:
        grade = 2
    elif score >= 2:
        grade = 1
    else:
        grade = 0

    basis = (
        f"internal heuristic relevance judgment; matched_terms={matched_terms[:6]}; "
        f"matched_paths={matched_paths[:4]}; criteria_terms={criteria_terms}; "
        f"bucket={row.get('bucket')}; score={score}; not external human judgment"
    )
    return grade, basis


def write_report(rows: list[dict]) -> None:
    counts = {"0": 0, "1": 0, "2": 0}
    for row in rows:
        counts[str(row["judged_relevance"])] += 1
    lines = [
        "---",
        "record_kind: sandbox_internal_relevance_judgment_report",
        "status: complete_internal_only",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: internal_judgment_not_external_human_relevance",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Internal Relevance Judgment Report",
        "",
        "## Result",
        "",
        "```text",
        f"judge_id: {JUDGE_ID}",
        f"judgment rows: {len(rows)}",
        f"grade_2_relevant: {counts['2']}",
        f"grade_1_borderline: {counts['1']}",
        f"grade_0_not_relevant: {counts['0']}",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "This fills the relevance judgment file with an internal heuristic/model-assisted judge.",
        "It is separate from expected_terms, but it is not external human judgment.",
        "It is not a weak human substitute or gold standard.",
        "It uses query-specific PROFILES, term/path matches, and VAKS bucket/status priors.",
        "It is only a sanity diagnostic for bias checks and external rejudgment planning.",
        "It does not validate original Yuxi runtime or C-lite.",
        "```",
        "",
    ]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    packet_rows = read_csv(PACKET_CSV)
    judgments = []
    for row in packet_rows:
        grade, basis = score_row(row)
        out = dict(row)
        out["judged_relevance"] = str(grade)
        out["judgment_basis"] = basis
        out["judge_id"] = JUDGE_ID
        judgments.append(out)
    write_csv(JUDGMENTS_CSV, judgments)
    write_report(judgments)
    print(f"judgment rows: {len(judgments)}")
    print(f"judge_id: {JUDGE_ID}")


if __name__ == "__main__":
    main()
