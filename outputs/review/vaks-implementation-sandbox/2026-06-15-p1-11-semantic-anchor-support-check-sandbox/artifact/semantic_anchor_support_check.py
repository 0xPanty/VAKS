#!/usr/bin/env python3
"""
Sandbox-only P1-11 semantic anchor support check.

This prototype validates JSON manifests that describe retrieval or graph
anchors proposed as evidence support. It allows semantic/vector/graph hits as
orientation, but blocks them from becoming support unless they resolve to a
stable raw or reviewed-support anchor.

It is read-only and uses only the Python standard library.
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

RECORD_KIND = "semantic_anchor_support_manifest"

STABLE_SUPPORT_ANCHOR_KINDS = {
    "raw_excerpt",
    "raw_snapshot_path",
    "code_line_range",
    "transcript_segment",
    "section_fragment",
    "quote_selector",
    "table_or_code_anchor",
    "hash_anchor",
    "stored_artifact_path",
    "stable_url_with_capture_date",
    "reviewed_support_ref",
}

SEMANTIC_ORIENTATION_ANCHOR_KINDS = {
    "semantic_vector_hit",
    "embedding_neighborhood",
    "reranker_score",
    "graph_neighbor",
    "graph_relation",
    "association_neighbor",
    "community_summary",
    "retrieval_result",
}

FORBIDDEN_SUPPORT_ANCHOR_KINDS = SEMANTIC_ORIENTATION_ANCHOR_KINDS.union(
    {
        "llm_summary",
        "briefing_summary",
        "source_summary",
        "candidate_distillation",
        "project_overlay",
        "feedback_event",
        "url_only",
        "metadata_only",
        "runtime_artifact",
        "generated_receipt",
        "cache_entry",
        "suite_output",
    }
)

ALLOWED_ANCHOR_KINDS = STABLE_SUPPORT_ANCHOR_KINDS.union(FORBIDDEN_SUPPORT_ANCHOR_KINDS)

SUPPORT_ROLES = {"direct_support", "inferential_support"}
SUPPORT_PACK_ROLES = {"support", "evidence_support"}
ACTION_ROLES = {"action_basis", "ready_action_basis"}

SUPPORT_AUTHORITY_BUCKETS = {
    "raw_anchor",
    "source_anchor",
    "stable_anchor",
    "reviewed_support",
}

CANDIDATE_BUCKETS = {"candidate", "review_input", "project_overlay", "candidate_overlay"}
FEEDBACK_BUCKETS = {"feedback", "feedback_event"}
SUMMARY_KINDS = {"llm_summary", "briefing_summary", "source_summary", "community_summary"}
CANDIDATE_KINDS = {"candidate_distillation", "project_overlay"}
FEEDBACK_KINDS = {"feedback_event"}
URL_ONLY_KINDS = {"url_only", "metadata_only"}
RUNTIME_ANCHOR_KINDS = {"runtime_artifact", "generated_receipt", "cache_entry", "suite_output"}

SEMANTIC_SCORE_FIELDS = {
    "semantic_score_claims_support",
    "semantic_similarity_claims_support",
    "selected_by_claims_support",
    "score_counted_as_support",
    "rank_counted_as_support",
    "retrieval_rank_as_trust",
}

GRAPH_SCORE_FIELDS = {
    "graph_rank_claims_support",
    "graph_relation_claims_support",
    "graph_score_claims_support",
    "association_score_claims_support",
    "graph_rank_as_trust",
}

REVIEWED_AUTHORITY_CLAIMS = {
    "truth",
    "truth_confidence",
    "reviewed_knowledge",
    "reviewed_relation",
    "reviewer_approval",
    "promotion_ready",
    "mainline_ready",
}

ACTION_AUTHORITY_CLAIMS = {
    "action_basis",
    "ready_action_basis",
    "action_ready",
}


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    anchor_id: str = ""

    def as_dict(self) -> dict[str, str]:
        result = {"code": self.code, "message": self.message}
        if self.anchor_id:
            result["anchor_id"] = self.anchor_id
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
    return str(value).strip() != ""


def add_once(issues: list[Issue], code: str, message: str, anchor_id: str = "") -> None:
    key = (code, anchor_id)
    if key not in {(issue.code, issue.anchor_id) for issue in issues}:
        issues.append(Issue(code, message, anchor_id))


def load_runtime_module():
    spec = importlib.util.spec_from_file_location("p1_10_runtime_artifact_check", P1_10_RUNTIME_CHECK)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules["p1_10_runtime_artifact_check"] = module
    spec.loader.exec_module(module)
    return module


RUNTIME_MODULE = load_runtime_module()


def anchor_id(anchor: dict[str, Any]) -> str:
    return raw_text(anchor.get("id")) or raw_text(anchor.get("source_ref")) or "<unknown>"


def anchor_kind(anchor: dict[str, Any]) -> str:
    return norm(anchor.get("anchor_kind"))


def support_role(anchor: dict[str, Any]) -> str:
    return norm(anchor.get("support_role")) or norm(anchor.get("evidence_role"))


def claims_score_support(anchor: dict[str, Any], field_names: set[str]) -> bool:
    return any(as_bool(anchor.get(field)) for field in field_names)


def claims_support(anchor: dict[str, Any]) -> bool:
    role = support_role(anchor)
    pack_role = norm(anchor.get("pack_role"))
    return (
        as_bool(anchor.get("support_claimed"))
        or role in SUPPORT_ROLES
        or role == "evidence_support"
        or pack_role in SUPPORT_PACK_ROLES
        or claims_score_support(anchor, SEMANTIC_SCORE_FIELDS)
        or claims_score_support(anchor, GRAPH_SCORE_FIELDS)
    )


def has_selector(anchor: dict[str, Any]) -> bool:
    selector_fields = {
        "selector",
        "line_range",
        "segment_id",
        "timestamp",
        "timestamp_range",
        "section",
        "fragment",
        "quote_selector",
        "hash",
        "snapshot_hash",
        "commit_sha",
    }
    return any(has_value(anchor.get(field)) for field in selector_fields)


def is_url(value: str) -> bool:
    lowered = value.lower()
    return lowered.startswith("http://") or lowered.startswith("https://")


def is_url_only_support(anchor: dict[str, Any]) -> bool:
    kind = anchor_kind(anchor)
    source_ref = raw_text(anchor.get("source_ref"))
    if kind in URL_ONLY_KINDS:
        return True
    if not is_url(source_ref):
        return False
    return not (
        has_value(anchor.get("captured_date"))
        and (
            has_value(anchor.get("selector"))
            or has_value(anchor.get("fragment"))
            or has_value(anchor.get("hash"))
            or has_value(anchor.get("snapshot_hash"))
        )
    )


def stable_anchor_available(anchor: dict[str, Any]) -> bool:
    kind = anchor_kind(anchor)
    if kind not in STABLE_SUPPORT_ANCHOR_KINDS:
        return False
    if not has_value(anchor.get("source_ref")):
        return False
    if kind == "stable_url_with_capture_date":
        return not is_url_only_support(anchor)
    return has_selector(anchor)


def runtime_item_for_anchor(anchor: dict[str, Any]) -> dict[str, Any]:
    path = (
        raw_text(anchor.get("anchor_path"))
        or raw_text(anchor.get("source_ref"))
        or raw_text(anchor.get("path"))
    )
    return {
        "id": anchor_id(anchor),
        "path": path,
        "artifact_kind": raw_text(anchor.get("artifact_kind")) or raw_text(anchor.get("anchor_kind")),
        "runtime_artifact": anchor.get("runtime_artifact", False),
    }


def is_runtime_anchor(anchor: dict[str, Any]) -> bool:
    if anchor_kind(anchor) in RUNTIME_ANCHOR_KINDS:
        return True
    if as_bool(anchor.get("runtime_artifact")):
        return True
    if RUNTIME_MODULE is None:
        return False
    return bool(RUNTIME_MODULE.is_runtime_artifact(runtime_item_for_anchor(anchor)))


def authority_claims(anchor: dict[str, Any]) -> set[str]:
    claims = set(as_list(anchor.get("anchor_claims")))
    claims.update(as_list(anchor.get("artifact_claims")))
    claims.update(as_list(anchor.get("receipt_claims")))
    return claims


def validate_anchor(anchor: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    current_id = anchor_id(anchor)
    kind = anchor_kind(anchor)
    role = support_role(anchor)
    bucket = norm(anchor.get("authority_bucket"))
    source_ref = raw_text(anchor.get("source_ref"))
    source_ref_kind = norm(anchor.get("source_ref_kind"))
    target_ref = raw_text(anchor.get("target_ref"))
    support_claim = claims_support(anchor)
    runtime_anchor = is_runtime_anchor(anchor)
    claims = authority_claims(anchor)

    if not has_value(anchor.get("id")):
        add_once(issues, "SA_MISSING_ANCHOR_ID", "anchor id is required.", current_id)

    if kind not in ALLOWED_ANCHOR_KINDS:
        add_once(
            issues,
            "SA_UNKNOWN_ANCHOR_KIND",
            "anchor_kind must be registered as stable support or orientation-only.",
            current_id,
        )

    if runtime_anchor:
        add_once(
            issues,
            "SA_RUNTIME_ARTIFACT_ANCHOR",
            "runtime artifacts cannot be semantic support anchors.",
            current_id,
        )

    if claims_score_support(anchor, SEMANTIC_SCORE_FIELDS):
        add_once(
            issues,
            "SA_SEMANTIC_SCORE_AS_SUPPORT",
            "semantic scores, ranks, and selected_by markers cannot claim support.",
            current_id,
        )

    if claims_score_support(anchor, GRAPH_SCORE_FIELDS):
        add_once(
            issues,
            "SA_GRAPH_RANK_AS_SUPPORT",
            "graph rank, graph relation, or association score cannot claim support.",
            current_id,
        )

    if claims.intersection(REVIEWED_AUTHORITY_CLAIMS) or as_bool(anchor.get("claims_reviewed_knowledge")):
        add_once(
            issues,
            "SA_ANCHOR_CLAIMS_REVIEWED_KNOWLEDGE",
            "anchor checks cannot claim truth, reviewer approval, promotion, or reviewed knowledge.",
            current_id,
        )

    if (
        claims.intersection(ACTION_AUTHORITY_CLAIMS)
        or as_bool(anchor.get("claims_action_basis"))
        or as_bool(anchor.get("action_basis_allowed"))
        or norm(anchor.get("pack_role")) in ACTION_ROLES
    ):
        add_once(
            issues,
            "SA_ANCHOR_CLAIMS_ACTION_BASIS",
            "semantic anchor checks cannot create action basis.",
            current_id,
        )

    if support_claim:
        if role not in SUPPORT_ROLES:
            add_once(
                issues,
                "SA_SUPPORT_ROLE_INVALID",
                "support claims require support_role direct_support or inferential_support.",
                current_id,
            )

        if role == "inferential_support" and not has_value(anchor.get("reviewer_note")):
            add_once(
                issues,
                "SA_INFERENTIAL_SUPPORT_MISSING_REVIEWER_NOTE",
                "inferential support requires a reviewer_note.",
                current_id,
            )

        if not has_value(source_ref):
            add_once(issues, "SA_MISSING_SOURCE_REF", "support anchors require source_ref.", current_id)

        if not has_selector(anchor):
            add_once(
                issues,
                "SA_MISSING_SELECTOR",
                "support anchors require a selector, range, segment, timestamp, hash, or commit.",
                current_id,
            )

        if is_url_only_support(anchor):
            add_once(
                issues,
                "SA_URL_ONLY_SUPPORT",
                "URL-only or metadata-only provenance cannot be final support.",
                current_id,
            )

        if kind in CANDIDATE_KINDS or bucket in CANDIDATE_BUCKETS:
            add_once(
                issues,
                "SA_CANDIDATE_AS_SUPPORT",
                "candidate distillations and project overlays can route review but cannot be support.",
                current_id,
            )

        if kind in FEEDBACK_KINDS or bucket in FEEDBACK_BUCKETS:
            add_once(
                issues,
                "SA_FEEDBACK_AS_SUPPORT",
                "feedback can create review pressure but cannot be evidence support.",
                current_id,
            )

        if kind in SUMMARY_KINDS:
            add_once(
                issues,
                "SA_SUMMARY_AS_SUPPORT",
                "summaries and community reports cannot replace inspected source anchors.",
                current_id,
            )

        if runtime_anchor:
            add_once(
                issues,
                "SA_RUNTIME_ARTIFACT_AS_SUPPORT",
                "runtime artifact anchors cannot be used as support.",
                current_id,
            )

        if bucket not in SUPPORT_AUTHORITY_BUCKETS:
            add_once(
                issues,
                "SA_AUTHORITY_BUCKET_INVALID_FOR_SUPPORT",
                "support anchors require raw/source/stable/reviewed-support authority bucket.",
                current_id,
            )

        if target_ref and norm(target_ref) == norm(source_ref):
            add_once(
                issues,
                "SA_SELF_SUPPORT_LOOP",
                "a target claim or note cannot cite itself as support.",
                current_id,
            )

        if source_ref_kind in {"claim_note", "candidate_note", "source_summary"}:
            add_once(
                issues,
                "SA_SELF_SUPPORT_LOOP",
                "claim, candidate, or summary notes are not independent source anchors.",
                current_id,
            )

        if kind in FORBIDDEN_SUPPORT_ANCHOR_KINDS or not stable_anchor_available(anchor):
            add_once(
                issues,
                "SA_SUPPORT_REQUIRES_STABLE_ANCHOR",
                "support requires a stable raw or reviewed-support anchor, not semantic orientation alone.",
                current_id,
            )

    return issues


def validate_manifest(manifest: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []

    if norm(manifest.get("record_kind")) != RECORD_KIND:
        add_once(
            issues,
            "SA_INVALID_RECORD_KIND",
            f"record_kind must be {RECORD_KIND}.",
        )

    if not has_value(manifest.get("scenario_id")):
        add_once(issues, "SA_MISSING_SCENARIO_ID", "scenario_id is required.")

    anchors = manifest.get("anchors")
    if not isinstance(anchors, list) or not anchors:
        add_once(issues, "SA_MISSING_ANCHORS", "anchors must be a non-empty list.")
        return issues

    seen_ids: set[str] = set()
    for anchor in anchors:
        if not isinstance(anchor, dict):
            add_once(issues, "SA_INVALID_ANCHOR", "each anchor must be an object.")
            continue
        current_id = anchor_id(anchor)
        if current_id in seen_ids:
            add_once(issues, "SA_DUPLICATE_ANCHOR_ID", "anchor ids must be unique.", current_id)
        seen_ids.add(current_id)
        issues.extend(validate_anchor(anchor))

    return issues


def summarize(manifest: dict[str, Any], issues: list[Issue]) -> dict[str, Any]:
    anchors = manifest.get("anchors", [])
    if not isinstance(anchors, list):
        anchors = []
    issue_codes = sorted({issue.code for issue in issues})
    issues_by_anchor: dict[str, list[str]] = {}
    for issue in issues:
        if issue.anchor_id:
            issues_by_anchor.setdefault(issue.anchor_id, []).append(issue.code)

    anchor_results = []
    for anchor in anchors:
        if not isinstance(anchor, dict):
            continue
        current_id = anchor_id(anchor)
        anchor_results.append(
            {
                "id": current_id,
                "anchor_kind": anchor_kind(anchor),
                "claims_support": claims_support(anchor),
                "stable_anchor_available": stable_anchor_available(anchor),
                "runtime_anchor": is_runtime_anchor(anchor),
                "issue_codes": sorted(set(issues_by_anchor.get(current_id, []))),
            }
        )

    return {
        "scenario_id": manifest.get("scenario_id", ""),
        "valid": not issues,
        "issue_codes": issue_codes,
        "issues": [issue.as_dict() for issue in issues],
        "anchor_results": anchor_results,
        "semantic_anchor_non_claims": {
            "semantic_hit_not_evidence_support": True,
            "graph_rank_not_evidence_support": True,
            "anchor_check_pass_not_reviewed_knowledge": True,
            "anchor_check_pass_not_reviewer_approval": True,
            "anchor_check_pass_not_action_basis": True,
            "sandbox_not_mainline": True,
        },
    }


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate semantic anchors proposed as support in a sandbox manifest."
    )
    parser.add_argument("path", type=Path, help="JSON manifest to validate")
    parser.add_argument(
        "--expect",
        choices=("valid", "invalid"),
        help="Optional expectation for checks.",
    )
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
            "issue_codes": ["SA_PARSE_OR_RUNTIME_ERROR"],
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
