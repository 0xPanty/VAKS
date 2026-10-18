#!/usr/bin/env python3
"""
Sandbox-only P1.5-13 local Obsidian graph retrieval / read-only MCP validator.

This prototype validates synthetic manifests for an Obsidian-like graph
retrieval sidecar. It proves the contract shape for candidate structural
triples, derived cache lifecycle, hybrid graph retrieval receipts, and a
read-only MCP query surface.

It is read-only, uses only the Python standard library, and does not access a
real Obsidian vault or start an MCP server.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

RECORD_KIND = "local_obsidian_graph_readonly_mcp_manifest"

KNOWN_BUCKETS = {
    "reviewed",
    "reviewed_support",
    "raw_anchor",
    "source_anchor",
    "stable_anchor",
    "candidate",
    "review_input",
    "project_overlay",
    "feedback",
    "runtime_artifact",
}

REQUIRED_HYBRID_CHANNELS = {"vector", "bm25", "temporal", "synonym"}
READ_ONLY_OPERATIONS = {"query", "list", "read", "read_context", "inspect"}
WRITE_OPERATIONS = {"write", "save", "delete", "sync", "promote", "update", "append", "export"}
FORBIDDEN_AUTHORITY_CLAIMS = {
    "support",
    "direct_support",
    "inferential_support",
    "reviewed_support",
    "truth",
    "truth_confidence",
    "reviewed_knowledge",
    "reviewed_relation",
    "reviewer_approval",
    "evidence_support",
    "action_basis",
    "ready_action_basis",
    "action_ready",
    "promotion_ready",
    "mainline_ready",
}
RANK_SUPPORT_FIELDS = {
    "graph_rank_claims_support",
    "retrieval_score_claims_support",
    "vector_score_claims_support",
    "bm25_score_claims_support",
    "temporal_rank_claims_support",
    "synonym_rank_claims_support",
    "rank_claims_trust",
    "score_sets_confidence",
    "graph_rank_sets_confidence",
    "retrieval_score_sets_confidence",
    "association_score_claims_support",
}


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    item_id: str = ""

    def as_dict(self) -> dict[str, str]:
        result = {"code": self.code, "message": self.message}
        if self.item_id:
            result["item_id"] = self.item_id
        return result


def norm(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).strip().lower().replace("\\", "/").replace(" ", "_").replace("-", "_")


def raw_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return norm(value) in {"true", "yes", "1"}


def as_list(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [norm(item) for item in value if norm(item)]
    return [norm(item) for item in str(value).split(",") if norm(item)]


def has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, list):
        return any(has_value(item) for item in value)
    if isinstance(value, dict):
        return bool(value)
    return str(value).strip() != ""


def add_once(issues: list[Issue], code: str, message: str, item_id: str = "") -> None:
    key = (code, item_id)
    if key not in {(issue.code, issue.item_id) for issue in issues}:
        issues.append(Issue(code, message, item_id))


def item_id(item: dict[str, Any]) -> str:
    return raw_text(item.get("id")) or raw_text(item.get("ref")) or "<unknown>"


def item_claims(item: dict[str, Any]) -> set[str]:
    claims = set(as_list(item.get("claims")))
    claims.update(as_list(item.get("artifact_claims")))
    claims.update(as_list(item.get("tool_claims")))
    claims.update(as_list(item.get("receipt_claims")))
    return claims


def has_forbidden_authority_claim(item: dict[str, Any]) -> bool:
    return bool(item_claims(item).intersection(FORBIDDEN_AUTHORITY_CLAIMS))


def rank_or_score_claims_authority(item: dict[str, Any]) -> bool:
    if any(as_bool(item.get(field)) for field in RANK_SUPPORT_FIELDS):
        return True

    authority_words = {"support", "confidence", "trust", "truth", "action", "basis", "reviewed"}
    for field, value in item.items():
        field_name = norm(field)
        if not as_bool(value):
            continue
        if ("rank" in field_name or "score" in field_name) and any(word in field_name for word in authority_words):
            return True
    return False


def sha256_like(value: Any) -> bool:
    text = raw_text(value).lower()
    return text.startswith("sha256:") and len(text.split("sha256:", 1)[1]) >= 16


def md5_like(value: Any) -> bool:
    text = raw_text(value).lower()
    return text.startswith("md5:") or norm(value.get("hash_algorithm") if isinstance(value, dict) else "") == "md5"


def validate_vault_access(access: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(access, dict):
        add_once(issues, "OG_MISSING_VAULT_ACCESS", "vault_access object is required.")
        return issues

    if not as_bool(access.get("sandbox_fixture_only")) or as_bool(access.get("uses_real_vault")):
        add_once(
            issues,
            "OG_REAL_VAULT_ACCESS_REQUESTED",
            "this sandbox must use fixtures only and must not access a real Obsidian vault.",
        )

    if not as_bool(access.get("read_only")):
        add_once(issues, "OG_VAULT_NOT_READ_ONLY", "vault access must be read-only.")

    if (
        as_bool(access.get("write_attempted"))
        or as_bool(access.get("sync_attempted"))
        or as_bool(access.get("delete_attempted"))
        or as_bool(access.get("bulk_export_attempted"))
    ):
        add_once(
            issues,
            "OG_VAULT_WRITE_OR_SYNC_REQUESTED",
            "vault writes, sync, delete, and bulk export are forbidden.",
        )

    vault_path = raw_text(access.get("vault_path")).lower().replace("\\", "/")
    if vault_path.startswith("h:/obsidian"):
        add_once(
            issues,
            "OG_REAL_VAULT_ACCESS_REQUESTED",
            "formal Obsidian vault paths are not used by this sandbox, even when marked fixture-only.",
        )

    return issues


def validate_mcp_contract(contract: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(contract, dict):
        add_once(issues, "OG_MISSING_MCP_CONTRACT", "mcp_contract object is required.")
        return issues

    if as_bool(contract.get("server_started")):
        add_once(issues, "OG_MCP_SERVER_STARTED", "this sandbox must not start a real MCP server.")

    if as_bool(contract.get("background_service")) or as_bool(contract.get("hooks_enabled")):
        add_once(
            issues,
            "OG_MCP_BACKGROUND_OR_HOOK_ENABLED",
            "background services and hooks are forbidden.",
        )

    tools = contract.get("tools")
    if not isinstance(tools, list) or not tools:
        add_once(issues, "OG_MCP_QUERY_TOOL_MISSING", "MCP contract must list a read-only query tool.")
        return issues

    has_query_tool = False
    for tool in tools:
        if not isinstance(tool, dict):
            add_once(issues, "OG_INVALID_MCP_TOOL", "MCP tool entry must be an object.")
            continue
        current_id = raw_text(tool.get("name")) or "<unknown_tool>"
        operations = set(as_list(tool.get("operations")))
        mode = norm(tool.get("mode"))

        if norm(tool.get("name")) in {"query_graph", "query_vault_graph"}:
            has_query_tool = True

        if mode not in {"read_only", "suggest_only", "read_only_suggest_only"}:
            add_once(issues, "OG_MCP_WRITE_TOOL_EXPOSED", "MCP tool mode must be read-only.", current_id)

        if operations.intersection(WRITE_OPERATIONS) or as_bool(tool.get("write_enabled")):
            add_once(
                issues,
                "OG_MCP_WRITE_TOOL_EXPOSED",
                "MCP contract cannot expose write/save/delete/sync/promote operations.",
                current_id,
            )

        if operations and not operations.issubset(READ_ONLY_OPERATIONS.union(WRITE_OPERATIONS)):
            add_once(
                issues,
                "OG_MCP_UNKNOWN_OPERATION",
                "MCP operations must be explicit read/query/list/inspect or rejected write operations.",
                current_id,
            )

    if not has_query_tool:
        add_once(issues, "OG_MCP_QUERY_TOOL_MISSING", "query_graph read-only tool is required.")

    return issues


def validate_triples(triples: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(triples, list) or not triples:
        add_once(issues, "OG_TRIPLES_MISSING", "structural_triples must be a non-empty list.")
        return issues

    seen_ids: set[str] = set()
    for triple in triples:
        if not isinstance(triple, dict):
            add_once(issues, "OG_INVALID_TRIPLE", "structural triple must be an object.")
            continue
        current_id = item_id(triple)
        if current_id in seen_ids:
            add_once(issues, "OG_DUPLICATE_TRIPLE_ID", "structural triple ids must be unique.", current_id)
        seen_ids.add(current_id)

        if not has_value(triple.get("source_ref")) or not has_value(triple.get("from")) or not has_value(triple.get("to")):
            add_once(issues, "OG_TRIPLE_MISSING_SOURCE", "triple needs source_ref, from, and to.", current_id)

        if not sha256_like(triple.get("source_hash")):
            add_once(issues, "OG_TRIPLE_MISSING_SOURCE_HASH", "triple needs sha256 source_hash.", current_id)

        if norm(triple.get("graph_status")) != "candidate_graph_fragment":
            add_once(
                issues,
                "OG_TRIPLE_STATUS_NOT_CANDIDATE",
                "wikilink/frontmatter triples must stay candidate graph fragments.",
                current_id,
            )

        if (
            has_forbidden_authority_claim(triple)
            or as_bool(triple.get("claims_reviewed_relation"))
            or as_bool(triple.get("reviewed_relation_created"))
            or norm(triple.get("graph_status")) == "reviewed_relation"
        ):
            add_once(
                issues,
                "OG_TRIPLE_CLAIMS_REVIEWED_RELATION",
                "auto structural triples cannot create reviewed relations or authority claims.",
                current_id,
            )

        if as_bool(triple.get("auto_promote")) or as_bool(triple.get("promotion_ready")):
            add_once(issues, "OG_TRIPLE_AUTO_PROMOTION", "structural triples cannot auto-promote.", current_id)

        if md5_like(triple.get("source_hash")) or norm(triple.get("hash_algorithm")) == "md5":
            add_once(
                issues,
                "OG_WEAK_HASH_AS_PROVENANCE",
                "MD5 content-change hashes cannot be VAKS provenance hashes.",
                current_id,
            )

    return issues


def validate_cache(cache: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(cache, dict):
        add_once(issues, "OG_MISSING_CACHE_MANIFEST", "derived_cache_manifest object is required.")
        return issues

    required_fields = {
        "cache_id",
        "source_state_hash",
        "indexer_id",
        "indexer_version",
        "model_id",
        "model_fingerprint",
        "rebuild_boundary",
    }
    missing = sorted(field for field in required_fields if not has_value(cache.get(field)))
    if missing:
        add_once(
            issues,
            "OG_CACHE_MANIFEST_INCOMPLETE",
            f"derived cache manifest missing fields: {missing}",
        )

    if as_bool(cache.get("source_of_record")) or as_bool(cache.get("graph_index_is_truth")):
        add_once(
            issues,
            "OG_GRAPH_INDEX_AS_SOURCE_OF_RECORD",
            "derived graph indexes are not the VAKS source of record.",
        )

    if has_forbidden_authority_claim(cache):
        add_once(
            issues,
            "OG_CACHE_CLAIMS_AUTHORITY",
            "derived cache manifests cannot claim support, truth, approval, action basis, or mainline readiness.",
        )

    if not sha256_like(cache.get("source_state_hash")):
        add_once(issues, "OG_CACHE_MANIFEST_INCOMPLETE", "source_state_hash must be sha256-like.")

    if norm(cache.get("hash_algorithm")) == "md5":
        add_once(
            issues,
            "OG_WEAK_HASH_AS_PROVENANCE",
            "MD5 may be cache-internal only, not VAKS provenance.",
        )

    mismatch = (
        as_bool(cache.get("stale"))
        or as_bool(cache.get("model_mismatch"))
        or as_bool(cache.get("source_hash_mismatch"))
    )
    if mismatch and as_bool(cache.get("used_for_query")) and not as_bool(cache.get("rebuild_required")):
        add_once(
            issues,
            "OG_CACHE_MISMATCH_USED",
            "stale or mismatched derived cache cannot be used silently.",
        )

    if norm(cache.get("model_locality")) in {"cloud_default", "unknown"} and not as_bool(cache.get("locality_reviewed")):
        add_once(
            issues,
            "OG_MODEL_LOCALITY_UNREVIEWED",
            "default cloud/unknown model configuration needs locality review.",
        )

    return issues


def validate_receipt(receipt: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(receipt, dict):
        add_once(issues, "OG_MISSING_RETRIEVAL_RECEIPT", "retrieval_receipt object is required.")
        return issues

    included = set(as_list(receipt.get("included_buckets")))
    excluded = set(as_list(receipt.get("excluded_buckets")))
    if not included or not excluded:
        add_once(
            issues,
            "OG_RECEIPT_BUCKETS_MISSING",
            "retrieval receipt must list included and excluded authority buckets.",
        )
    unknown = included.union(excluded).difference(KNOWN_BUCKETS)
    if unknown:
        add_once(issues, "OG_UNKNOWN_AUTHORITY_BUCKET", f"unknown authority buckets: {sorted(unknown)}")

    if not as_bool(receipt.get("bucket_filter_first")):
        add_once(issues, "OG_BUCKET_FILTER_NOT_FIRST", "authority buckets must be filtered before graph/rank fusion.")

    channels = set(as_list(receipt.get("selected_by_channels")))
    if norm(receipt.get("route")) == "hybrid_graph" and not REQUIRED_HYBRID_CHANNELS.issubset(channels):
        add_once(
            issues,
            "OG_HYBRID_SELECTED_BY_MISSING",
            "hybrid graph retrieval must emit vector/BM25/temporal/synonym selected_by channels.",
        )

    if as_bool(receipt.get("cross_bucket_fusion")):
        add_once(issues, "OG_CROSS_BUCKET_FUSION", "graph retrieval cannot fuse across authority buckets.")

    if has_forbidden_authority_claim(receipt):
        add_once(
            issues,
            "OG_RECEIPT_CLAIMS_AUTHORITY",
            "retrieval receipts cannot claim support, truth, approval, action basis, or mainline readiness.",
        )

    if rank_or_score_claims_authority(receipt):
        add_once(
            issues,
            "OG_RANK_AS_SUPPORT_OR_CONFIDENCE",
            "graph rank and retrieval score cannot become support or confidence.",
        )

    return issues


def validate_context_items(items: Any) -> list[Issue]:
    issues: list[Issue] = []
    if items is None:
        return issues
    if not isinstance(items, list):
        add_once(issues, "OG_INVALID_CONTEXT_ITEM", "retrieved_context must be a list.")
        return issues

    for item in items:
        if not isinstance(item, dict):
            add_once(issues, "OG_INVALID_CONTEXT_ITEM", "context item must be an object.")
            continue
        current_id = item_id(item)
        bucket = norm(item.get("authority_bucket"))
        role = norm(item.get("pack_role"))

        if bucket not in KNOWN_BUCKETS:
            add_once(issues, "OG_UNKNOWN_AUTHORITY_BUCKET", "context item bucket is unknown.", current_id)

        if rank_or_score_claims_authority(item):
            add_once(
                issues,
                "OG_RANK_AS_SUPPORT_OR_CONFIDENCE",
                "retrieval, graph, or association ranks cannot set support/confidence.",
                current_id,
            )

        if (
            bucket in {"candidate", "review_input", "project_overlay"}
            and role in {"support", "action_basis", "ready_action_basis"}
        ):
            add_once(
                issues,
                "OG_CANDIDATE_CONTEXT_AS_SUPPORT",
                "candidate graph/context items cannot be support or action basis.",
                current_id,
            )

        if has_forbidden_authority_claim(item):
            add_once(
                issues,
                "OG_CONTEXT_CLAIMS_AUTHORITY",
                "retrieved context cannot claim support, truth, approval, promotion, or action basis.",
                current_id,
            )

        if as_bool(item.get("action_basis_allowed")):
            add_once(issues, "OG_CITED_ANSWER_ACTION_BASIS", "retrieved context cannot allow action basis.", current_id)

    return issues


def validate_answer(answer: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(answer, dict):
        return issues

    if as_bool(answer.get("prompt_anti_hallucination_claims_review_approval")):
        add_once(
            issues,
            "OG_PROMPT_AS_REVIEW_APPROVAL",
            "anti-hallucination prompt discipline is not review approval.",
        )

    if has_forbidden_authority_claim(answer):
        add_once(
            issues,
            "OG_ANSWER_CLAIMS_AUTHORITY",
            "generated answers cannot claim support, truth, approval, action basis, or mainline readiness.",
        )

    if as_bool(answer.get("claims_action_basis")) or (
        as_bool(answer.get("has_file_citations")) and as_bool(answer.get("citations_claim_support"))
    ):
        add_once(
            issues,
            "OG_CITED_ANSWER_ACTION_BASIS",
            "file citations cannot create support or action basis without gates.",
        )

    return issues


def validate_manifest(manifest: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []

    if norm(manifest.get("record_kind")) != RECORD_KIND:
        add_once(issues, "OG_INVALID_RECORD_KIND", f"record_kind must be {RECORD_KIND}.")

    if not has_value(manifest.get("scenario_id")):
        add_once(issues, "OG_MISSING_SCENARIO_ID", "scenario_id is required.")

    issues.extend(validate_vault_access(manifest.get("vault_access", {})))
    issues.extend(validate_mcp_contract(manifest.get("mcp_contract", {})))
    issues.extend(validate_triples(manifest.get("structural_triples")))
    issues.extend(validate_cache(manifest.get("derived_cache_manifest", {})))
    issues.extend(validate_receipt(manifest.get("retrieval_receipt", {})))
    issues.extend(validate_context_items(manifest.get("retrieved_context", [])))
    issues.extend(validate_answer(manifest.get("generated_answer", {})))

    return issues


def summarize(manifest: dict[str, Any], issues: list[Issue]) -> dict[str, Any]:
    issue_codes = sorted({issue.code for issue in issues})
    triples = manifest.get("structural_triples", [])
    context = manifest.get("retrieved_context", [])
    if not isinstance(triples, list):
        triples = []
    if not isinstance(context, list):
        context = []
    return {
        "scenario_id": manifest.get("scenario_id", ""),
        "valid": not issues,
        "issue_codes": issue_codes,
        "issues": [issue.as_dict() for issue in issues],
        "triple_ids": [item_id(item) for item in triples if isinstance(item, dict)],
        "context_item_ids": [item_id(item) for item in context if isinstance(item, dict)],
        "mcp_tool_names": [
            raw_text(tool.get("name"))
            for tool in manifest.get("mcp_contract", {}).get("tools", [])
            if isinstance(tool, dict)
        ]
        if isinstance(manifest.get("mcp_contract"), dict)
        else [],
        "local_obsidian_graph_non_claims": {
            "structural_triple_not_reviewed_relation": True,
            "derived_cache_not_source_of_record": True,
            "mcp_query_not_write_authority": True,
            "graph_rank_not_support_or_confidence": True,
            "file_citation_not_action_basis": True,
            "sandbox_not_mainline": True,
        },
    }


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate local Obsidian graph read-only MCP sandbox manifest.")
    parser.add_argument("path", type=Path, help="JSON manifest to validate")
    parser.add_argument("--expect", choices=("valid", "invalid"), help="Optional expectation")
    parser.add_argument(
        "--expect-code",
        action="append",
        default=[],
        help="Expected issue code; may be repeated.",
    )
    args = parser.parse_args(argv)

    try:
        manifest = load_manifest(args.path)
        issues = validate_manifest(manifest)
        result = summarize(manifest, issues)
    except Exception as exc:  # pragma: no cover - CLI boundary
        result = {
            "path": str(args.path),
            "valid": False,
            "issue_codes": ["OG_PARSE_OR_RUNTIME_ERROR"],
            "parse_error": str(exc),
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))

    failed = False
    if args.expect == "valid" and not result["valid"]:
        failed = True
    if args.expect == "invalid" and result["valid"]:
        failed = True
    issue_codes = set(result["issue_codes"])
    for code in args.expect_code:
        if code.upper() not in issue_codes:
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
