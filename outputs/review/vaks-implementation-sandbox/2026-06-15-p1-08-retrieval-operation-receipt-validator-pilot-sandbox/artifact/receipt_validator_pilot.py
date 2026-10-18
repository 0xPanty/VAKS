#!/usr/bin/env python3
"""
Sandbox-only P1-08 retrieval/operation receipt validator pilot.

This prototype validates compact Markdown receipts with flat YAML-like
frontmatter. It is read-only, uses only the Python standard library, and does
not create reviewer approval, evidence support, reviewed knowledge, action
basis, or mainline readiness.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RETRIEVAL_FORBIDDEN_SUPPORT_BUCKETS = {
    "candidate",
    "candidate_distillation",
    "candidate_point",
    "project_overlay",
    "source_annotation",
    "feedback",
    "feedback_event",
}

RETRIEVAL_AUTHORITY_BUCKETS = {
    "reviewed",
    "raw_anchor",
    "candidate",
    "candidate_distillation",
    "candidate_point",
    "project_overlay",
    "source_annotation",
    "feedback",
    "feedback_event",
}

RETRIEVAL_REQUEST_BUCKETS = RETRIEVAL_AUTHORITY_BUCKETS.union(
    {"mixed_for_orientation"}
)

RETRIEVAL_PACK_ROLES = {
    "orientation",
    "review_input",
    "support",
    "anchor",
    "counterexample",
    "background_context",
}

OPERATION_ACTOR_TIERS = {
    "read_only",
    "suggest_only",
    "candidate_write",
    "reviewed_write",
    "owner_final",
}

OPERATION_MODES = {
    "read",
    "suggest",
    "propose_write",
    "write",
    "delete",
    "schema_change",
}

OPERATION_TARGET_SCOPES = {
    "candidate",
    "sandbox",
    "reviewed",
    "mainline",
    "formal",
    "schema",
    "protected",
}

BAD_OPERATION_BASIS_MATERIALS = {
    "candidate",
    "candidate_distillation",
    "candidate_point",
    "project_overlay",
    "source_annotation",
    "feedback",
    "feedback_event",
    "retrieval_receipt",
    "retrieval_rank",
    "retrieval_score",
    "graph_rank",
    "source_summary",
    "briefing_summary",
    "context_pack",
}

AUTHORITY_CLAIMS = {
    "truth",
    "truth_confidence",
    "reviewed_truth",
    "reviewed_knowledge",
    "reviewed_relation",
    "review_approval",
    "reviewer_approval",
    "evidence_support",
    "direct_support",
    "action_basis",
    "action_readiness",
    "mainline_ready",
    "promotion_ready",
    "owner_approval",
}

RETRIEVAL_BOUNDARY_FLAGS = {
    "selected_by_is_not_support",
    "same_bucket_rrf_only",
    "cross_bucket_rank_not_authority",
    "legacy_raw_metadata_excluded",
    "candidate_overlay_feedback_not_support",
    "url_only_not_direct_support",
    "graph_rank_not_trust",
    "receipt_not_review_approval",
    "receipt_not_action_basis",
    "receipt_not_reviewed_knowledge",
}

OPERATION_BOUNDARY_FLAGS = {
    "receipt_not_truth",
    "receipt_not_review_approval",
    "receipt_not_reviewed_knowledge",
    "receipt_not_action_basis",
    "validator_pass_not_reviewer_approval",
    "sandbox_not_mainline",
}

WRITE_MODES = {"write", "delete", "schema_change"}
SIGNIFICANT_OPERATION_MODES = {"propose_write", "write", "delete", "schema_change"}


@dataclass(frozen=True)
class Issue:
    code: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message}


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value == "":
        return ""
    lower = value.lower()
    if lower in {"true", "yes"}:
        return True
    if lower in {"false", "no"}:
        return False
    if lower in {"null", "none"}:
        return ""
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [strip_quotes(part.strip()) for part in inner.split(",")]
    return strip_quotes(value)


def parse_frontmatter(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter fence")

    closing_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = index
            break

    if closing_index is None:
        raise ValueError("missing closing frontmatter fence")

    record: dict[str, Any] = {}
    for line in lines[1:closing_index]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, raw_value = line.split(":", 1)
        record[key.strip()] = parse_scalar(raw_value)
    return record


def norm(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")


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


def add_once(issues: list[Issue], code: str, message: str) -> None:
    if code not in {issue.code for issue in issues}:
        issues.append(Issue(code, message))


def add_missing(issues: list[Issue], field: str) -> None:
    add_once(
        issues,
        "RV_OV_MISSING_REQUIRED_FIELD",
        f"missing required field: {field}.",
    )


def receipt_claims_authority(record: dict[str, Any]) -> bool:
    explicit_claims = set(as_list(record.get("receipt_claims"))).union(
        set(as_list(record.get("operation_claims")))
    )
    if explicit_claims.intersection(AUTHORITY_CLAIMS):
        return True

    for claim in AUTHORITY_CLAIMS:
        if as_bool(record.get(f"claims_{claim}")):
            return True
        if as_bool(record.get(f"receipt_claims_{claim}")):
            return True
        if as_bool(record.get(f"operation_claims_{claim}")):
            return True
    return False


def validate_boundary_flags(
    record: dict[str, Any],
    expected_flags: set[str],
    issue_code: str,
    issues: list[Issue],
) -> None:
    for flag in sorted(expected_flags):
        if flag in record and not as_bool(record.get(flag)):
            add_once(
                issues,
                issue_code,
                f"boundary flag must remain true: {flag}.",
            )


def validate_retrieval(record: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []

    if not has_value(record.get("receipt_id")) and not has_value(record.get("query_id")):
        add_missing(issues, "receipt_id or query_id")
    for field in (
        "query_mode",
        "requested_authority_bucket",
        "included_buckets",
        "rrf_scope",
        "selected_item_authority_buckets",
        "selected_item_pack_roles",
    ):
        if not has_value(record.get(field)):
            add_missing(issues, field)

    if issues:
        return issues

    requested_bucket = norm(record.get("requested_authority_bucket"))
    if requested_bucket not in RETRIEVAL_REQUEST_BUCKETS:
        add_once(
            issues,
            "RV_UNKNOWN_AUTHORITY_BUCKET",
            "requested_authority_bucket must be a known receipt bucket.",
        )

    included_buckets = set(as_list(record.get("included_buckets")))
    selected_buckets = set(as_list(record.get("selected_item_authority_buckets")))
    unknown_buckets = sorted(
        included_buckets.union(selected_buckets).difference(RETRIEVAL_AUTHORITY_BUCKETS)
    )
    if unknown_buckets:
        add_once(
            issues,
            "RV_UNKNOWN_AUTHORITY_BUCKET",
            f"unknown authority bucket(s): {unknown_buckets}.",
        )

    roles = set(as_list(record.get("selected_item_pack_roles")))
    unknown_roles = sorted(roles.difference(RETRIEVAL_PACK_ROLES))
    if unknown_roles:
        add_once(
            issues,
            "RV_UNKNOWN_PACK_ROLE",
            f"unknown selected item pack role(s): {unknown_roles}.",
        )

    rrf_scope = norm(record.get("rrf_scope"))
    if rrf_scope != "same_authority_bucket_only":
        add_once(
            issues,
            "RV_CROSS_BUCKET_RRF",
            "rrf_scope must stay same_authority_bucket_only.",
        )

    if as_bool(record.get("cross_bucket_rrf_used")) or as_bool(
        record.get("cross_bucket_rank_used")
    ):
        add_once(
            issues,
            "RV_CROSS_BUCKET_RRF",
            "cross-bucket fusion/ranking cannot create authority.",
        )

    if as_bool(record.get("selected_by_claims_support")) or as_bool(
        record.get("retrieval_rank_claims_support")
    ) or as_bool(record.get("scores_are_support")):
        add_once(
            issues,
            "RV_SELECTED_BY_AS_SUPPORT",
            "selected_by or retrieval scores cannot be evidence support.",
        )

    if as_bool(record.get("graph_rank_claims_trust")):
        add_once(
            issues,
            "RV_GRAPH_RANK_AS_TRUST",
            "graph rank cannot create trust, support, or confidence.",
        )

    buckets = selected_buckets
    if (
        buckets.intersection(RETRIEVAL_FORBIDDEN_SUPPORT_BUCKETS)
        and ("support" in roles or as_bool(record.get("selected_item_action_basis_allowed")))
    ):
        add_once(
            issues,
            "RV_CANDIDATE_OVERLAY_FEEDBACK_AS_SUPPORT",
            "candidate, overlay, source annotation, or feedback items cannot be support or action basis.",
        )

    if as_bool(record.get("legacy_raw_metadata_used")):
        add_once(
            issues,
            "RV_LEGACY_RAW_METADATA_USED",
            "legacy raw metadata must stay excluded from support receipts.",
        )

    evidence_role = norm(record.get("support_evidence_role"))
    support_result = norm(record.get("support_result"))
    support_claimed = (
        as_bool(record.get("support_claimed"))
        or support_result == "supported"
        or evidence_role in {"direct_support", "inferential_support"}
    )
    anchor_kind = norm(record.get("support_anchor_kind"))

    weak_anchor_kind = anchor_kind in {
        "url_only",
        "metadata_only",
        "summary_only",
        "briefing_summary",
    }
    if (evidence_role == "direct_support" or support_claimed) and weak_anchor_kind:
        add_once(
            issues,
            "RV_URL_ONLY_DIRECT_SUPPORT",
            "url-only, metadata-only, or summary-only material cannot be claimed support.",
        )

    if support_claimed and not has_value(record.get("independent_anchor_ref")):
        add_once(
            issues,
            "RV_MISSING_INDEPENDENT_SUPPORT_ANCHOR",
            "claimed support requires an independent anchor reference.",
        )

    if receipt_claims_authority(record):
        add_once(
            issues,
            "RV_RECEIPT_CLAIMS_AUTHORITY",
            "retrieval receipts cannot claim truth, review approval, support, action basis, or mainline readiness.",
        )

    validate_boundary_flags(
        record,
        RETRIEVAL_BOUNDARY_FLAGS,
        "RV_SUPPORT_BOUNDARY_FLAG_FALSE",
        issues,
    )
    return issues


def is_significant_operation(record: dict[str, Any]) -> bool:
    mode = norm(record.get("operation_mode"))
    return (
        mode in SIGNIFICANT_OPERATION_MODES
        or as_bool(record.get("actual_write_performed"))
        or as_bool(record.get("intent_confirmation_required"))
    )


def validate_operation(record: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []

    if not has_value(record.get("operation_id")) and not has_value(
        record.get("receipt_id")
    ):
        add_missing(issues, "operation_id or receipt_id")
    for field in ("actor_tier", "operation_mode", "actual_write_performed"):
        if field not in record:
            add_missing(issues, field)

    if issues:
        return issues

    actor_tier = norm(record.get("actor_tier"))
    mode = norm(record.get("operation_mode"))
    target_scope = norm(record.get("target_scope"))
    actual_write = as_bool(record.get("actual_write_performed"))

    if actor_tier not in OPERATION_ACTOR_TIERS:
        add_once(
            issues,
            "OV_UNKNOWN_ACTOR_TIER",
            "actor_tier must be one of the known operation receipt tiers.",
        )

    if mode not in OPERATION_MODES:
        add_once(
            issues,
            "OV_UNKNOWN_OPERATION_MODE",
            "operation_mode must be one of the known operation modes.",
        )

    if target_scope and target_scope not in OPERATION_TARGET_SCOPES:
        add_once(
            issues,
            "OV_UNKNOWN_TARGET_SCOPE",
            "target_scope must be one of the known target scopes.",
        )

    if actor_tier == "read_only" and (mode != "read" or actual_write):
        add_once(
            issues,
            "OV_ACTOR_TIER_CANNOT_WRITE",
            "read_only actors cannot suggest action writes or perform writes.",
        )

    if actor_tier == "suggest_only" and (
        mode not in {"read", "suggest", "propose_write"} or actual_write
    ):
        add_once(
            issues,
            "OV_ACTOR_TIER_CANNOT_WRITE",
            "suggest_only actors can propose but cannot perform writes.",
        )

    if actor_tier == "candidate_write" and mode in WRITE_MODES and target_scope not in {
        "candidate",
        "sandbox",
    }:
        add_once(
            issues,
            "OV_CANDIDATE_WRITE_OUT_OF_SCOPE",
            "candidate_write actors can write only candidate or sandbox scopes.",
        )

    if mode == "schema_change" and (
        actor_tier != "owner_final" or not as_bool(record.get("owner_final_present"))
    ):
        add_once(
            issues,
            "OV_SCHEMA_CHANGE_MISSING_OWNER_FINAL",
            "schema_change requires owner_final actor and owner-final approval.",
        )

    if mode == "delete" and (
        actor_tier != "owner_final" or not as_bool(record.get("owner_final_present"))
    ):
        add_once(
            issues,
            "OV_DESTRUCTIVE_OPERATION_REQUIRES_OWNER_FINAL",
            "delete requires owner_final actor and owner-final approval.",
        )

    formal_write = mode in WRITE_MODES and target_scope in {
        "reviewed",
        "mainline",
        "formal",
        "schema",
        "protected",
    }
    reviewed_write = mode == "write" and (
        actor_tier == "reviewed_write" or target_scope == "reviewed"
    )
    approval_required_write = reviewed_write or formal_write or (
        actual_write and target_scope in {"mainline", "formal", "schema", "protected"}
    )
    if approval_required_write and (
        not as_bool(record.get("approval_present"))
        or not has_value(record.get("checked_body_hash"))
    ):
        add_once(
            issues,
            "OV_REVIEWED_WRITE_MISSING_APPROVAL_OR_HASH",
            "reviewed, formal, schema, protected, or mainline writes require approval and checked_body_hash.",
        )

    if "checked_body_hash_match" in record and not as_bool(
        record.get("checked_body_hash_match")
    ):
        add_once(
            issues,
            "OV_CHECKED_BODY_HASH_MISMATCH",
            "checked_body_hash mismatch invalidates approval for the changed body.",
        )

    rollback_required = (
        as_bool(record.get("rollback_required"))
        or mode in {"delete", "schema_change"}
        or (mode == "write" and target_scope in {"reviewed", "mainline"})
    )
    if rollback_required and not as_bool(record.get("rollback_plan_present")):
        add_once(
            issues,
            "OV_ROLLBACK_REQUIRED",
            "delete, schema_change, reviewed/mainline write, or explicitly rollback-required operation needs a rollback plan.",
        )

    if is_significant_operation(record) and not as_bool(
        record.get("user_intent_confirmed")
    ):
        add_once(
            issues,
            "OV_MISSING_INTENT_CONFIRMATION",
            "significant operations require user intent confirmation.",
        )

    basis_materials = set(as_list(record.get("basis_materials")))
    action_basis_sensitive = (
        mode in SIGNIFICANT_OPERATION_MODES
        or actual_write
        or as_bool(record.get("action_basis_ready_claimed"))
    )
    if action_basis_sensitive and basis_materials.intersection(
        BAD_OPERATION_BASIS_MATERIALS
    ):
        add_once(
            issues,
            "OV_INVALID_ACTION_BASIS",
            "candidate, feedback, retrieval, summary, context-pack, or rank material cannot be action basis.",
        )

    if receipt_claims_authority(record):
        add_once(
            issues,
            "OV_RECEIPT_CLAIMS_AUTHORITY",
            "operation receipts cannot claim truth, review approval, reviewed knowledge, action basis, or mainline readiness.",
        )

    validate_boundary_flags(
        record,
        OPERATION_BOUNDARY_FLAGS,
        "OV_OPERATION_BOUNDARY_FLAG_FALSE",
        issues,
    )
    return issues


def validate_record(record: dict[str, Any]) -> list[Issue]:
    record_kind = norm(record.get("record_kind"))
    if record_kind == "retrieval_receipt":
        return validate_retrieval(record)
    if record_kind == "operation_receipt":
        return validate_operation(record)
    return [
        Issue(
            "RV_OV_INVALID_RECORD_KIND",
            "record_kind must be retrieval_receipt or operation_receipt.",
        )
    ]


def validate_path(path: Path) -> tuple[dict[str, Any], list[Issue]]:
    record = parse_frontmatter(path.read_text(encoding="utf-8"))
    return record, validate_record(record)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Sandbox-only retrieval/operation receipt validator pilot."
    )
    parser.add_argument("path", type=Path, help="Markdown receipt to validate")
    parser.add_argument(
        "--expect",
        choices=("valid", "invalid"),
        help="Optional expectation for CI-style checks.",
    )
    parser.add_argument(
        "--expect-code",
        action="append",
        default=[],
        help="Expected issue code; may be repeated.",
    )
    args = parser.parse_args(argv)

    try:
        record, issues = validate_path(args.path)
    except Exception as exc:  # pragma: no cover - CLI boundary
        result = {
            "path": str(args.path),
            "valid": False,
            "parse_error": str(exc),
            "issues": [{"code": "RV_OV_PARSE_ERROR", "message": str(exc)}],
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1

    issue_codes = {issue.code for issue in issues}
    valid = not issues
    result = {
        "path": str(args.path),
        "record_kind": record.get("record_kind"),
        "valid": valid,
        "issue_codes": sorted(issue_codes),
        "issues": [issue.as_dict() for issue in issues],
        "authority_non_claims": {
            "validator_pass_not_reviewer_approval": True,
            "receipt_not_evidence_support": True,
            "receipt_not_reviewed_knowledge": True,
            "receipt_not_action_basis": True,
            "sandbox_not_mainline": True,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))

    failed = False
    if args.expect == "valid" and not valid:
        failed = True
    if args.expect == "invalid" and valid:
        failed = True
    for code in args.expect_code:
        if code not in issue_codes:
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
