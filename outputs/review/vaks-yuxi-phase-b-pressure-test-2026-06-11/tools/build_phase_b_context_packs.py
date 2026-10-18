import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
SUPPORT_BUCKETS = {"core_framework", "reviewed"}


RECEIPT_FILES = {
    ("main", "primary"): RESULTS_DIR / "phase_b_skeleton_main_primary_retrieval_receipts.jsonl",
    ("main", "full"): RESULTS_DIR / "phase_b_skeleton_main_full_retrieval_receipts.jsonl",
    ("holdout", "primary"): RESULTS_DIR / "phase_b_skeleton_holdout_primary_retrieval_receipts.jsonl",
    ("holdout", "full"): RESULTS_DIR / "phase_b_skeleton_holdout_full_retrieval_receipts.jsonl",
}

QUERY_FILES = {
    "main": SANDBOX_DIR / "queries_phase_b.jsonl",
    "holdout": SANDBOX_DIR / "queries_phase_b_holdout.jsonl",
}


def load_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)


def load_queries() -> dict[str, dict]:
    queries = {}
    for source_set, path in QUERY_FILES.items():
        for row in load_jsonl(path):
            queries[(source_set, row["id"])] = row
    return queries


def compact_receipt(row: dict) -> dict:
    policy = row.get("retrieval_policy") or {}
    return {
        "rank": row.get("rank"),
        "vault_path": row.get("vault_path"),
        "heading_or_anchor": row.get("heading_or_anchor"),
        "selector_or_line_range": row.get("selector_or_line_range"),
        "source_clickback": row.get("source_clickback"),
        "authority_badge": row.get("authority_badge"),
        "usage_badge": row.get("usage_badge"),
        "warning_code": row.get("warning_code"),
        "temporal_badge": row.get("temporal_badge"),
        "retrieval_reasons": row.get("retrieval_reasons") or [],
        "source_hash": row.get("source_hash"),
        "indexed_source_hash": row.get("indexed_source_hash"),
        "chunk_hash": row.get("chunk_hash"),
        "authority_bucket": policy.get("authority_bucket"),
        "receipt_action_basis_allowed": bool(policy.get("action_basis_allowed")),
        "relation_state": row.get("relation_state"),
        "review_state": row.get("review_state"),
        "snippet": row.get("snippet", "")[:240],
    }


def warning_codes_for(query: dict, receipts: list[dict]) -> list[str]:
    warnings: list[str] = [
        "context_pack_candidate_not_action_basis",
        "vaks_action_gate_required",
    ]
    if query.get("needs_boundary_warning"):
        warnings.append("query_requires_boundary_warning")
    for receipt in receipts:
        policy = receipt.get("retrieval_policy") or {}
        bucket = policy.get("authority_bucket")
        reasons = set(receipt.get("retrieval_reasons") or [])
        if bucket not in SUPPORT_BUCKETS:
            warnings.append("non_support_receipt_context_only")
        if receipt.get("warning_code"):
            warnings.extend(str(receipt["warning_code"]).split(";"))
        if receipt.get("temporal_badge") == "stale":
            warnings.append("stale_receipt_present")
        if "graph_neighbor" in reasons or receipt.get("graph_path"):
            warnings.append("graph_metadata_not_reviewed_relation")
        if policy.get("action_basis_allowed"):
            warnings.append("receipt_action_flag_suppressed_at_pack_level")
    return list(dict.fromkeys(warnings))


def gaps_for(query: dict, receipts: list[dict], primary: list[dict]) -> list[str]:
    gaps: list[str] = [
        "not_a_full_evidence_packet",
        "no_warrant_or_scope_review",
    ]
    if query.get("intent") == "action":
        gaps.append("action_basis_requires_separate_vaks_gate")
    if not primary:
        gaps.append("no_reviewed_or_core_primary_receipt")
    if any(receipt.get("temporal_badge") == "stale" for receipt in receipts):
        gaps.append("source_refresh_needed_before_action_use")
    return list(dict.fromkeys(gaps))


def build_pack(source_set: str, corpus: str, query: dict, receipts: list[dict], built_at: str) -> dict:
    receipts = sorted(receipts, key=lambda row: int(row.get("rank") or 9999))
    compact = [compact_receipt(row) for row in receipts]
    primary = [
        item
        for item in compact
        if item["authority_bucket"] in SUPPORT_BUCKETS and item["warning_code"] not in {"raw_provenance_only", "feedback_not_truth"}
    ][:5]
    neighbors = [item for item in compact if item not in primary][:5]
    warnings = warning_codes_for(query, receipts)
    gaps = gaps_for(query, receipts, primary)
    return {
        "artifact_kind": "vaks_phase_b_context_pack_candidate",
        "pack_id": f"{source_set}:{corpus}:{query['id']}",
        "source_set": source_set,
        "corpus": corpus,
        "query_id": query["id"],
        "query_group": query.get("group"),
        "query_intent": query.get("intent"),
        "pack_status": "candidate_not_action_basis",
        "pack_policy": {
            "policy_kind": "phase_b_context_pack_candidate",
            "pack_allowed": True,
            "action_basis_allowed": False,
            "review_required_before_action": True,
            "support_requires_evidence_packet": True,
        },
        "context_sections": {
            "primary": primary,
            "neighbors": neighbors,
            "warnings": warnings,
            "gaps": gaps,
            "stop_conditions": [
                "do_not_treat_pack_as_action_basis",
                "do_not_treat_retrieval_score_as_evidence_support",
                "do_not_treat_graph_metadata_as_reviewed_relation",
                "run_vaks_action_gate_before_action_use",
            ],
        },
        "coverage_summary": {
            "receipt_count": len(compact),
            "primary_count": len(primary),
            "neighbor_count": len(neighbors),
            "stale_count": sum(1 for item in compact if item.get("temporal_badge") == "stale"),
            "non_support_count": sum(1 for item in compact if item.get("authority_bucket") not in SUPPORT_BUCKETS),
            "suppressed_receipt_action_flags": sum(1 for item in compact if item.get("receipt_action_basis_allowed")),
        },
        "generated_by": "phase_b_context_pack_candidate_builder",
        "built_at": built_at,
    }


def build_all(output_path: Path) -> dict:
    queries = load_queries()
    built_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    packs = []
    for (source_set, corpus), path in RECEIPT_FILES.items():
        grouped = defaultdict(list)
        for row in load_jsonl(path):
            grouped[row["query_id"]].append(row)
        for query_id, receipts in sorted(grouped.items()):
            query = queries[(source_set, query_id)]
            packs.append(build_pack(source_set, corpus, query, receipts, built_at))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        for pack in packs:
            handle.write(json.dumps(pack, ensure_ascii=False, sort_keys=True) + "\n")
    summary = {
        "artifact_kind": "vaks_phase_b_context_pack_summary",
        "pack_count": len(packs),
        "source_sets": sorted({pack["source_set"] for pack in packs}),
        "corpora": sorted({pack["corpus"] for pack in packs}),
        "action_basis_allowed_count": sum(1 for pack in packs if pack["pack_policy"]["action_basis_allowed"]),
        "packs_with_suppressed_receipt_action_flags": sum(
            1 for pack in packs if pack["coverage_summary"]["suppressed_receipt_action_flags"]
        ),
        "output_path": str(output_path),
        "built_at": built_at,
    }
    (RESULTS_DIR / "phase_b_context_pack_candidate_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=RESULTS_DIR / "phase_b_context_pack_candidates.jsonl")
    args = parser.parse_args()
    summary = build_all(args.output)
    print(f"context pack candidates: {summary['pack_count']}")
    print(f"action_basis_allowed_count: {summary['action_basis_allowed_count']}")


if __name__ == "__main__":
    main()
