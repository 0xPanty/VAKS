#!/usr/bin/env python3
"""
Sandbox-only P1.5-12 robust RAG retrieval runner.

This prototype validates synthetic robust-retrieval manifests. It proves that
hybrid, vector, graph, local/global/DRIFT, and rerank traces can improve recall
while preserving VAKS authority boundaries.

It is read-only, uses only the Python standard library, and does not scan the
real vault.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

SLICE_ROOT = Path(__file__).resolve().parents[1]
SANDBOX_ROOT = SLICE_ROOT.parent
P1_10_RUNTIME_CHECK = (
    SANDBOX_ROOT
    / "2026-06-15-p1-10-runtime-artifact-exclusion-test-sandbox"
    / "artifact"
    / "runtime_artifact_exclusion_test.py"
)
P1_11_ANCHOR_CHECK = (
    SANDBOX_ROOT
    / "2026-06-15-p1-11-semantic-anchor-support-check-sandbox"
    / "artifact"
    / "semantic_anchor_support_check.py"
)

RECORD_KIND = "robust_rag_retrieval_manifest"

QUERY_MODES = {
    "orientation",
    "source_inspection",
    "review",
    "action",
}

ROUTE_MODES = {
    "local_entity",
    "global_theme",
    "drift_explore",
    "basic_vector",
    "hybrid_bucketed",
}

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

SUPPORT_BUCKETS = {"reviewed_support", "raw_anchor", "source_anchor", "stable_anchor"}
CANDIDATE_BUCKETS = {"candidate", "review_input", "project_overlay"}
FEEDBACK_BUCKETS = {"feedback"}
RUNTIME_BUCKETS = {"runtime_artifact"}

SUPPORT_ROLES = {"support", "anchor", "direct_support", "inferential_support"}
ACTION_ROLES = {"action_basis", "ready_action_basis"}
ORIENTATION_ROLES = {"orientation", "review_input", "none", ""}
SUMMARY_KINDS = {"community_report", "raptor_summary", "tree_summary", "theme_briefing"}
GRAPH_RELATION_KINDS = {"llm_extracted_relation", "auto_extracted_relation", "graph_relation"}

SCORE_AUTHORITY_FIELDS = {
    "score_sets_confidence",
    "rerank_score_sets_confidence",
    "vector_score_sets_confidence",
    "graph_rank_sets_confidence",
    "rank_claims_trust",
    "score_claims_support",
    "semantic_score_claims_support",
    "semantic_similarity_claims_support",
    "selected_by_claims_support",
    "vector_score_claims_support",
    "rerank_score_claims_support",
    "retrieval_rank_as_trust",
    "graph_rank_claims_support",
    "graph_relation_claims_support",
    "graph_score_claims_support",
    "association_score_claims_support",
    "graph_rank_as_trust",
}

REQUIRED_FORBIDDEN_SUPPORT_TYPES = {
    "retrieval_score",
    "graph_rank",
    "community_report_summary",
    "llm_extracted_relation",
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


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


RUNTIME_MODULE = load_module("p1_10_runtime_artifact_check_for_robust_rag", P1_10_RUNTIME_CHECK)
ANCHOR_MODULE = load_module("p1_11_semantic_anchor_check_for_robust_rag", P1_11_ANCHOR_CHECK)


def item_id(item: dict[str, Any]) -> str:
    return raw_text(item.get("id")) or raw_text(item.get("ref")) or "<unknown>"


def item_kind(item: dict[str, Any]) -> str:
    return norm(item.get("record_kind")) or norm(item.get("artifact_kind"))


def item_bucket(item: dict[str, Any]) -> str:
    return norm(item.get("authority_bucket"))


def item_path(item: dict[str, Any]) -> str:
    return raw_text(item.get("path")) or raw_text(item.get("ref"))


def pack_role(item: dict[str, Any]) -> str:
    return norm(item.get("pack_role"))


def selected_by(item: dict[str, Any]) -> dict[str, Any]:
    selected = item.get("selected_by")
    return selected if isinstance(selected, dict) else {}


def selected_by_channels(item: dict[str, Any]) -> list[str]:
    selected = selected_by(item)
    return sorted([norm(key) for key, value in selected.items() if as_bool(value)])


def is_runtime_item(item: dict[str, Any]) -> bool:
    if RUNTIME_MODULE is None:
        return as_bool(item.get("runtime_artifact")) or item_bucket(item) in RUNTIME_BUCKETS
    runtime_item = {
        "id": item_id(item),
        "path": item_path(item),
        "artifact_kind": raw_text(item.get("artifact_kind")) or raw_text(item.get("record_kind")),
        "runtime_artifact": item.get("runtime_artifact", False),
    }
    return bool(RUNTIME_MODULE.is_runtime_artifact(runtime_item))


def claims_support(item: dict[str, Any]) -> bool:
    role = pack_role(item)
    return (
        as_bool(item.get("support_claimed"))
        or role in SUPPORT_ROLES
        or norm(item.get("evidence_role")) in SUPPORT_ROLES
    )


def claims_action_basis(item: dict[str, Any]) -> bool:
    return (
        as_bool(item.get("action_basis_allowed"))
        or as_bool(item.get("claims_action_basis"))
        or pack_role(item) in ACTION_ROLES
        or norm(item.get("evidence_role")) in ACTION_ROLES
    )


def item_claims(item: dict[str, Any]) -> set[str]:
    claims = set(as_list(item.get("artifact_claims")))
    claims.update(as_list(item.get("item_claims")))
    claims.update(as_list(item.get("retrieval_claims")))
    return claims


def validate_query(query: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(query, dict):
        add_once(issues, "RR_MISSING_QUERY", "query object is required.")
        return issues

    mode = norm(query.get("query_mode"))
    if mode not in QUERY_MODES:
        add_once(issues, "RR_UNKNOWN_QUERY_MODE", "query_mode must be a known VAKS query mode.")

    if as_bool(query.get("action_sensitive")) and (
        not has_value(query.get("verbatim_input")) or not as_bool(query.get("verbatim_preserved"))
    ):
        add_once(
            issues,
            "RR_VERBATIM_INPUT_REQUIRED",
            "action-sensitive query construction must preserve verbatim input.",
        )

    if not has_value(query.get("question_summary")):
        add_once(issues, "RR_MISSING_QUESTION_SUMMARY", "question_summary is required.")

    return issues


def validate_route(route: dict[str, Any], query: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(route, dict):
        add_once(issues, "RR_MISSING_ROUTE_SELECTION", "route_selection object is required.")
        return issues

    selected = norm(route.get("selected"))
    if selected not in ROUTE_MODES:
        add_once(issues, "RR_UNKNOWN_ROUTE_MODE", "route selected value is unknown.")

    included = set(as_list(route.get("authority_buckets_included")))
    excluded = set(as_list(route.get("authority_buckets_excluded")))
    if not included or not excluded:
        add_once(
            issues,
            "RR_ROUTE_BUCKETS_MISSING",
            "route selection must record included and excluded authority buckets.",
        )

    unknown_buckets = (included.union(excluded)).difference(KNOWN_BUCKETS)
    if unknown_buckets:
        add_once(
            issues,
            "RR_UNKNOWN_AUTHORITY_BUCKET",
            f"unknown authority buckets: {sorted(unknown_buckets)}",
        )

    forbidden = set(as_list(route.get("forbidden_support_types")))
    if not REQUIRED_FORBIDDEN_SUPPORT_TYPES.issubset(forbidden):
        add_once(
            issues,
            "RR_FORBIDDEN_SUPPORT_TYPES_MISSING",
            "route receipt must list score, graph, community, and extracted-relation support forbiddance.",
        )

    if selected == "drift_explore":
        lineage = route.get("query_lineage")
        if not isinstance(lineage, list) or len(lineage) < 2:
            add_once(
                issues,
                "RR_DRIFT_LINEAGE_MISSING",
                "DRIFT route must preserve original query and follow-up lineage.",
            )
        if not has_value(query.get("verbatim_input")):
            add_once(
                issues,
                "RR_DRIFT_LINEAGE_MISSING",
                "DRIFT route needs original user intent or verbatim input.",
            )

    return issues


def validate_config(config: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(config, dict):
        add_once(issues, "RR_MISSING_RETRIEVAL_CONFIG", "retrieval_config object is required.")
        return issues

    if not as_bool(config.get("bucket_filter_first")):
        add_once(
            issues,
            "RR_BUCKET_FILTER_NOT_FIRST",
            "VAKS authority buckets must be applied before ranking or fusion.",
        )
    if not as_bool(config.get("rrf_within_bucket_only")):
        add_once(
            issues,
            "RR_RRF_NOT_BUCKET_LOCAL",
            "RRF and rerank fusion must stay inside an allowed authority bucket.",
        )
    if not as_bool(config.get("exclude_runtime_artifacts")):
        add_once(
            issues,
            "RR_RUNTIME_FILTER_DISABLED",
            "robust retrieval must exclude runtime artifacts.",
        )
    return issues


def validate_fusion_groups(groups: Any) -> list[Issue]:
    issues: list[Issue] = []
    if groups is None:
        return issues
    if not isinstance(groups, list):
        add_once(issues, "RR_INVALID_FUSION_GROUPS", "fusion_groups must be a list.")
        return issues
    for index, group in enumerate(groups):
        if not isinstance(group, dict):
            add_once(issues, "RR_INVALID_FUSION_GROUPS", "fusion group must be an object.", f"group-{index}")
            continue
        buckets = set(as_list(group.get("authority_buckets")))
        if len(buckets) > 1:
            add_once(
                issues,
                "RR_CROSS_BUCKET_FUSION",
                "RRF/rerank fusion cannot merge across authority buckets.",
                raw_text(group.get("id")) or f"group-{index}",
            )
    return issues


def validate_anchor(item: dict[str, Any]) -> tuple[list[Issue], list[str]]:
    if ANCHOR_MODULE is None:
        return [], []
    anchor = item.get("semantic_anchor")
    if not isinstance(anchor, dict):
        return [], []
    manifest = {
        "record_kind": "semantic_anchor_support_manifest",
        "scenario_id": f"anchor-for-{item_id(item)}",
        "anchors": [anchor],
    }
    anchor_issues = ANCHOR_MODULE.validate_manifest(manifest)
    anchor_codes = sorted({issue.code for issue in anchor_issues})
    issues: list[Issue] = []
    if anchor_issues:
        add_once(
            issues,
            "RR_SEMANTIC_ANCHOR_BOUNDARY_FAILED",
            f"semantic anchor boundary failed with {anchor_codes}",
            item_id(item),
        )
    return issues, anchor_codes


def validate_item(item: dict[str, Any], included: set[str], excluded: set[str]) -> tuple[list[Issue], list[str]]:
    issues: list[Issue] = []
    anchor_codes: list[str] = []
    current_id = item_id(item)
    bucket = item_bucket(item)
    kind = item_kind(item)
    role = pack_role(item)
    selected = as_bool(item.get("selected"))
    excluded_item = as_bool(item.get("excluded"))
    runtime = is_runtime_item(item)
    claims = item_claims(item)
    reviewed_relation_claimed = (
        "reviewed_relation" in claims
        or as_bool(item.get("reviewed_relation_created"))
        or as_bool(item.get("claims_reviewed_relation"))
    )

    if not has_value(item.get("id")):
        add_once(issues, "RR_MISSING_ITEM_ID", "item id is required.", current_id)

    if bucket not in KNOWN_BUCKETS:
        add_once(issues, "RR_UNKNOWN_AUTHORITY_BUCKET", "item authority_bucket is unknown.", current_id)

    if selected and bucket in excluded:
        add_once(
            issues,
            "RR_SELECTED_EXCLUDED_BUCKET",
            "selected item comes from an excluded authority bucket.",
            current_id,
        )
    if selected and bucket not in included:
        add_once(
            issues,
            "RR_SELECTED_BUCKET_NOT_INCLUDED",
            "selected item bucket is not listed as included by the route.",
            current_id,
        )

    if runtime and selected:
        add_once(
            issues,
            "RR_RUNTIME_ARTIFACT_SELECTED",
            "runtime artifacts cannot be selected by robust retrieval.",
            current_id,
        )
    if runtime and not excluded_item:
        add_once(
            issues,
            "RR_RUNTIME_ARTIFACT_NOT_EXCLUDED",
            "runtime artifacts must be explicitly excluded.",
            current_id,
        )

    if any(as_bool(item.get(field)) for field in SCORE_AUTHORITY_FIELDS):
        add_once(
            issues,
            "RR_SCORE_SET_CONFIDENCE",
            "vector, rerank, graph, or retrieval scores cannot set support, confidence, or trust.",
            current_id,
        )

    if (
        as_bool(item.get("graph_path_claims_reviewed_relation"))
        or (kind in GRAPH_RELATION_KINDS and reviewed_relation_claimed)
        or (as_bool(selected_by(item).get("graph")) and reviewed_relation_claimed)
    ):
        add_once(
            issues,
            "RR_GRAPH_PATH_REVIEWED_RELATION",
            "graph paths and LLM-extracted relations cannot create reviewed relations.",
            current_id,
        )

    if kind in SUMMARY_KINDS and (claims_support(item) or claims_action_basis(item)):
        add_once(
            issues,
            "RR_SUMMARY_AS_ACTION_SUPPORT",
            "community, RAPTOR, or tree summaries cannot become support or action basis without drilldown.",
            current_id,
        )

    if kind == "community_report" and as_bool(item.get("satisfies_evidence_sufficiency")):
        add_once(
            issues,
            "RR_COMMUNITY_REPORT_SUFFICIENCY",
            "community reports cannot satisfy evidence sufficiency without raw/reviewed drilldown.",
            current_id,
        )

    if bucket in CANDIDATE_BUCKETS and (claims_support(item) or claims_action_basis(item)):
        add_once(
            issues,
            "RR_CANDIDATE_AS_SUPPORT",
            "candidate, review_input, and project overlay items cannot be support or action basis.",
            current_id,
        )

    if bucket in FEEDBACK_BUCKETS and claims_support(item):
        add_once(
            issues,
            "RR_FEEDBACK_AS_SUPPORT",
            "feedback can affect activation and review pressure, not evidence support.",
            current_id,
        )

    if claims_action_basis(item):
        add_once(
            issues,
            "RR_RETRIEVAL_ITEM_ACTION_BASIS",
            "robust retrieval items cannot themselves create action basis.",
            current_id,
        )

    if role in SUPPORT_ROLES and bucket not in SUPPORT_BUCKETS:
        add_once(
            issues,
            "RR_SUPPORT_BUCKET_INVALID",
            "support role requires raw/source/stable/reviewed-support bucket.",
            current_id,
        )

    if selected and not selected_by_channels(item):
        add_once(
            issues,
            "RR_SELECTED_BY_MISSING",
            "selected items must expose retrieval selected_by trace.",
            current_id,
        )

    anchor_issues, anchor_codes = validate_anchor(item)
    issues.extend(anchor_issues)

    return issues, anchor_codes


def validate_answer(answer: dict[str, Any], query: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(answer, dict):
        return issues

    action_mode = norm(query.get("query_mode")) == "action"
    has_citations = as_bool(answer.get("has_citations"))
    support_checked = as_bool(answer.get("support_checks_passed"))
    sufficiency_checked = as_bool(answer.get("sufficiency_checked"))

    if as_bool(answer.get("eval_pass_claims_reviewer_approval")) or as_bool(
        answer.get("reviewer_approval_from_eval")
    ):
        add_once(
            issues,
            "RR_EVAL_PASS_AS_REVIEWER_APPROVAL",
            "eval diagnostics cannot become reviewer approval.",
        )

    if as_bool(answer.get("auto_promote_candidates")) or as_bool(
        answer.get("active_retrieval_auto_promotes_candidate")
    ):
        add_once(
            issues,
            "RR_ACTIVE_RETRIEVAL_AUTO_PROMOTION",
            "active retrieval cannot auto-promote candidates.",
        )

    if as_bool(answer.get("claims_action_basis")):
        add_once(
            issues,
            "RR_GENERATED_ANSWER_ACTION_BASIS",
            "generated answers from robust retrieval cannot claim action basis.",
        )

    if action_mode and has_citations and (not support_checked or not sufficiency_checked):
        add_once(
            issues,
            "RR_CITATION_WITHOUT_SUPPORT_CHECK",
            "citations in action mode still need support and sufficiency checks.",
        )

    return issues


def validate_plugin(plugin: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(plugin, dict) or not plugin:
        return issues
    mode = norm(plugin.get("mode"))
    if mode and mode not in {"read_only", "suggest_only", "read_only_suggest_only"}:
        add_once(
            issues,
            "RR_PLUGIN_NOT_READ_ONLY",
            "optional robust retrieval plugins must remain read-only or suggest-only.",
        )
    if as_bool(plugin.get("write_tools_enabled")) or as_bool(plugin.get("auto_update_enabled")):
        add_once(
            issues,
            "RR_PLUGIN_NOT_READ_ONLY",
            "plugins cannot expose writes or automatic index/truth updates in this sandbox.",
        )
    return issues


def validate_cache(cache: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(cache, dict) or not cache:
        return issues
    mismatch = as_bool(cache.get("model_mismatch")) or as_bool(cache.get("source_hash_mismatch"))
    stale = as_bool(cache.get("stale"))
    if (mismatch or stale) and as_bool(cache.get("used_without_rebuild")):
        add_once(
            issues,
            "RR_STALE_DERIVED_CACHE_USED",
            "stale or mismatched derived retrieval cache cannot be used silently.",
        )
    return issues


def validate_manifest(manifest: dict[str, Any]) -> tuple[list[Issue], dict[str, list[str]]]:
    issues: list[Issue] = []
    anchor_codes_by_item: dict[str, list[str]] = {}

    if norm(manifest.get("record_kind")) != RECORD_KIND:
        add_once(issues, "RR_INVALID_RECORD_KIND", f"record_kind must be {RECORD_KIND}.")

    if not has_value(manifest.get("scenario_id")):
        add_once(issues, "RR_MISSING_SCENARIO_ID", "scenario_id is required.")

    query = manifest.get("query")
    route = manifest.get("route_selection")
    config = manifest.get("retrieval_config")

    query_obj = query if isinstance(query, dict) else {}
    route_obj = route if isinstance(route, dict) else {}
    config_obj = config if isinstance(config, dict) else {}

    issues.extend(validate_query(query_obj))
    issues.extend(validate_route(route_obj, query_obj))
    issues.extend(validate_config(config_obj))
    issues.extend(validate_fusion_groups(manifest.get("fusion_groups")))
    issues.extend(validate_answer(manifest.get("generated_answer", {}), query_obj))
    issues.extend(validate_plugin(manifest.get("optional_plugin", {})))
    issues.extend(validate_cache(manifest.get("derived_cache_manifest", {})))

    included = set(as_list(route_obj.get("authority_buckets_included")))
    excluded = set(as_list(route_obj.get("authority_buckets_excluded")))

    items = manifest.get("retrieved_items")
    if not isinstance(items, list) or not items:
        add_once(issues, "RR_MISSING_RETRIEVED_ITEMS", "retrieved_items must be a non-empty list.")
        return issues, anchor_codes_by_item

    seen_ids: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            add_once(issues, "RR_INVALID_RETRIEVED_ITEM", "each retrieved item must be an object.")
            continue
        current_id = item_id(item)
        if current_id in seen_ids:
            add_once(issues, "RR_DUPLICATE_ITEM_ID", "retrieved item ids must be unique.", current_id)
        seen_ids.add(current_id)
        item_issues, anchor_codes = validate_item(item, included, excluded)
        issues.extend(item_issues)
        if anchor_codes:
            anchor_codes_by_item[current_id] = anchor_codes

    return issues, anchor_codes_by_item


def summarize(manifest: dict[str, Any], issues: list[Issue], anchor_codes_by_item: dict[str, list[str]]) -> dict[str, Any]:
    items = manifest.get("retrieved_items", [])
    if not isinstance(items, list):
        items = []
    selected_ids = [
        item_id(item)
        for item in items
        if isinstance(item, dict) and as_bool(item.get("selected"))
    ]
    runtime_ids = [
        item_id(item)
        for item in items
        if isinstance(item, dict) and is_runtime_item(item)
    ]
    issue_codes = sorted({issue.code for issue in issues})
    issues_by_item: dict[str, list[str]] = {}
    for issue in issues:
        if issue.item_id:
            issues_by_item.setdefault(issue.item_id, []).append(issue.code)

    item_results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        current_id = item_id(item)
        item_results.append(
            {
                "id": current_id,
                "authority_bucket": item_bucket(item),
                "record_kind": item_kind(item),
                "pack_role": pack_role(item),
                "selected": as_bool(item.get("selected")),
                "selected_by": selected_by_channels(item),
                "runtime_artifact": is_runtime_item(item),
                "anchor_issue_codes": anchor_codes_by_item.get(current_id, []),
                "issue_codes": sorted(set(issues_by_item.get(current_id, []))),
            }
        )

    return {
        "scenario_id": manifest.get("scenario_id", ""),
        "valid": not issues,
        "issue_codes": issue_codes,
        "issues": [issue.as_dict() for issue in issues],
        "route_selected": norm(manifest.get("route_selection", {}).get("selected"))
        if isinstance(manifest.get("route_selection"), dict)
        else "",
        "selected_item_ids": selected_ids,
        "runtime_item_ids": runtime_ids,
        "item_results": item_results,
        "robust_rag_non_claims": {
            "retrieval_rank_not_support": True,
            "semantic_or_graph_route_not_confidence": True,
            "community_report_not_truth": True,
            "generated_answer_not_action_basis": True,
            "eval_pass_not_reviewer_approval": True,
            "sandbox_not_mainline": True,
        },
    }


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate robust RAG retrieval sandbox manifest.")
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
        issues, anchor_codes_by_item = validate_manifest(manifest)
        result = summarize(manifest, issues, anchor_codes_by_item)
    except Exception as exc:  # pragma: no cover - CLI boundary
        result = {
            "path": str(args.path),
            "valid": False,
            "issue_codes": ["RR_PARSE_OR_RUNTIME_ERROR"],
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
