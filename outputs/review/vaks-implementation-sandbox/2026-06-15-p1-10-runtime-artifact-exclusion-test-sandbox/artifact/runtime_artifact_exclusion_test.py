#!/usr/bin/env python3
"""
Sandbox-only P1-10 runtime artifact exclusion test.

This prototype validates a JSON manifest of retrieval-visible items. It proves
that runtime artifacts such as caches, bytecode, logs, temporary receipts,
generated receipts, suite outputs, and derived indexes are excluded from
retrieval selection, evidence support, reviewed authority, and action basis.

It is read-only and uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RUNTIME_ARTIFACT_KINDS = {
    "python_cache",
    "bytecode_cache",
    "test_output",
    "suite_output",
    "verifier_output",
    "execution_log",
    "temporary_receipt",
    "generated_receipt",
    "scratch_file",
    "lockfile",
    "runtime_cache",
    "derived_index",
    "temporary_download",
    "transient_state",
    "benchmark_output",
}

DURABLE_NON_RUNTIME_KINDS = {
    "source_record",
    "raw_anchor",
    "reviewed_note",
    "reviewed_summary",
    "decision_record",
    "candidate_note",
    "project_overlay",
    "feedback_record",
    "sandbox_contract",
    "sandbox_verification_doc",
    "fixture",
    "failure_case",
    "source_map",
    "next_step_doc",
}

ALLOWED_ARTIFACT_KINDS = RUNTIME_ARTIFACT_KINDS.union(DURABLE_NON_RUNTIME_KINDS)

RUNTIME_PATH_MARKERS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    "node_modules/.cache",
    "tmp/",
    "temp/",
    "scratch/",
    "run-output",
    "suite-output",
    "verification-output",
    "generated-receipts",
    "runtime-cache",
    "derived-index",
}

RUNTIME_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".log",
    ".tmp",
    ".temp",
    ".lock",
    ".sqlite",
    ".db",
}

SUPPORT_ROLES = {
    "support",
    "direct_support",
    "inferential_support",
    "evidence_support",
    "anchor",
}
ACTION_ROLES = {"action_basis", "ready_action_basis"}
AUTHORITY_BUCKETS_FORBIDDEN_TO_RUNTIME = {
    "reviewed",
    "reviewed_knowledge",
    "raw",
    "raw_anchor",
    "support",
    "evidence_support",
    "action",
    "action_basis",
}
AUTHORITY_CLAIMS = {
    "truth",
    "truth_confidence",
    "reviewed_knowledge",
    "reviewed_relation",
    "reviewer_approval",
    "evidence_support",
    "direct_support",
    "action_basis",
    "mainline_ready",
    "promotion_ready",
}

REQUIRED_RUNTIME_EXCLUSION_REASON = "runtime_artifact_excluded"


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
    return str(value).strip() != ""


def add_once(issues: list[Issue], code: str, message: str, item_id: str = "") -> None:
    key = (code, item_id)
    if key not in {(issue.code, issue.item_id) for issue in issues}:
        issues.append(Issue(code, message, item_id))


def path_looks_runtime(path: str) -> bool:
    normalized = path.replace("\\", "/").lower()
    canonical = normalized.replace("_", "-").replace(" ", "-")
    if any(marker in normalized for marker in RUNTIME_PATH_MARKERS):
        return True
    if any(
        marker.replace("_", "-").replace(" ", "-") in canonical
        for marker in RUNTIME_PATH_MARKERS
    ):
        return True
    return any(normalized.endswith(suffix) for suffix in RUNTIME_SUFFIXES)


def item_id(item: dict[str, Any]) -> str:
    return raw_text(item.get("id")) or raw_text(item.get("path")) or "<unknown>"


def artifact_kind(item: dict[str, Any]) -> str:
    return norm(item.get("artifact_kind"))


def is_runtime_artifact(item: dict[str, Any]) -> bool:
    kind = artifact_kind(item)
    path = raw_text(item.get("path"))
    return as_bool(item.get("runtime_artifact")) or kind in RUNTIME_ARTIFACT_KINDS or path_looks_runtime(path)


def validate_item(item: dict[str, Any], exclude_runtime: bool) -> list[Issue]:
    issues: list[Issue] = []
    current_id = item_id(item)
    kind = artifact_kind(item)
    runtime = is_runtime_artifact(item)

    if not has_value(item.get("id")):
        add_once(issues, "RA_MISSING_ITEM_ID", "item id is required.", current_id)

    if not has_value(item.get("path")):
        add_once(issues, "RA_MISSING_ITEM_PATH", "item path is required.", current_id)

    if kind not in ALLOWED_ARTIFACT_KINDS:
        add_once(
            issues,
            "RA_UNKNOWN_ARTIFACT_KIND",
            "artifact_kind must be a known durable or runtime kind.",
            current_id,
        )

    if runtime and item.get("runtime_artifact") is False:
        add_once(
            issues,
            "RA_RUNTIME_ARTIFACT_MISLABELED",
            "path or kind indicates runtime artifact but runtime_artifact is false.",
            current_id,
        )

    seen_by_retrieval = as_bool(item.get("seen_by_retrieval"))
    selected = as_bool(item.get("selected"))
    excluded = as_bool(item.get("excluded"))
    excluded_reason = norm(item.get("excluded_reason"))
    pack_role = norm(item.get("pack_role"))
    evidence_role = norm(item.get("evidence_role"))
    authority_bucket = norm(item.get("authority_bucket"))
    action_basis_allowed = as_bool(item.get("action_basis_allowed")) or as_bool(
        item.get("used_as_action_basis")
    )

    if runtime and not exclude_runtime:
        add_once(
            issues,
            "RA_RUNTIME_FILTER_DISABLED",
            "runtime artifacts require exclude_runtime_artifacts=true.",
            current_id,
        )

    if runtime and seen_by_retrieval and not excluded:
        add_once(
            issues,
            "RA_RUNTIME_ARTIFACT_NOT_EXCLUDED",
            "retrieval-visible runtime artifact must be excluded.",
            current_id,
        )

    if runtime and excluded and excluded_reason != REQUIRED_RUNTIME_EXCLUSION_REASON:
        add_once(
            issues,
            "RA_RUNTIME_ARTIFACT_BAD_EXCLUSION_REASON",
            "runtime artifact exclusion must use runtime_artifact_excluded reason.",
            current_id,
        )

    if runtime and selected:
        add_once(
            issues,
            "RA_RUNTIME_ARTIFACT_SELECTED",
            "runtime artifact cannot be selected for query context.",
            current_id,
        )

    if runtime and (
        pack_role in SUPPORT_ROLES
        or evidence_role in SUPPORT_ROLES
        or as_bool(item.get("support_claimed"))
    ):
        add_once(
            issues,
            "RA_RUNTIME_ARTIFACT_AS_SUPPORT",
            "runtime artifact cannot be evidence support or support anchor.",
            current_id,
        )

    if runtime and (
        action_basis_allowed or pack_role in ACTION_ROLES or evidence_role in ACTION_ROLES
    ):
        add_once(
            issues,
            "RA_RUNTIME_ARTIFACT_ACTION_BASIS",
            "runtime artifact cannot be action basis.",
            current_id,
        )

    if runtime and authority_bucket in AUTHORITY_BUCKETS_FORBIDDEN_TO_RUNTIME:
        add_once(
            issues,
            "RA_RUNTIME_ARTIFACT_AUTHORITY_BUCKET",
            "runtime artifact cannot carry reviewed/raw/support/action authority bucket.",
            current_id,
        )

    claims = set(as_list(item.get("artifact_claims"))).union(set(as_list(item.get("receipt_claims"))))
    if runtime and claims.intersection(AUTHORITY_CLAIMS):
        add_once(
            issues,
            "RA_RUNTIME_ARTIFACT_CLAIMS_AUTHORITY",
            "runtime artifact cannot claim truth, support, approval, action basis, or mainline readiness.",
            current_id,
        )

    return issues


def validate_manifest(manifest: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []

    if norm(manifest.get("record_kind")) != "runtime_artifact_exclusion_manifest":
        add_once(
            issues,
            "RA_INVALID_RECORD_KIND",
            "record_kind must be runtime_artifact_exclusion_manifest.",
        )

    if not has_value(manifest.get("scenario_id")):
        add_once(issues, "RA_MISSING_SCENARIO_ID", "scenario_id is required.")

    if "exclude_runtime_artifacts" not in manifest:
        add_once(
            issues,
            "RA_MISSING_RUNTIME_FILTER",
            "exclude_runtime_artifacts is required.",
        )

    exclude_runtime = as_bool(manifest.get("exclude_runtime_artifacts"))
    if not exclude_runtime:
        add_once(
            issues,
            "RA_RUNTIME_FILTER_DISABLED",
            "exclude_runtime_artifacts must be true.",
        )

    items = manifest.get("items")
    if not isinstance(items, list) or not items:
        add_once(issues, "RA_MISSING_ITEMS", "items must be a non-empty list.")
        return issues

    seen_ids: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            add_once(issues, "RA_INVALID_ITEM", "each item must be an object.")
            continue
        current_id = item_id(item)
        if current_id in seen_ids:
            add_once(issues, "RA_DUPLICATE_ITEM_ID", "item ids must be unique.", current_id)
        seen_ids.add(current_id)
        issues.extend(validate_item(item, exclude_runtime))

    return issues


def summarize(manifest: dict[str, Any], issues: list[Issue]) -> dict[str, Any]:
    items = manifest.get("items", [])
    if not isinstance(items, list):
        items = []
    runtime_ids = [item_id(item) for item in items if isinstance(item, dict) and is_runtime_artifact(item)]
    selected_ids = [
        item_id(item)
        for item in items
        if isinstance(item, dict) and as_bool(item.get("selected"))
    ]
    excluded_runtime_ids = [
        item_id(item)
        for item in items
        if isinstance(item, dict)
        and is_runtime_artifact(item)
        and as_bool(item.get("excluded"))
        and norm(item.get("excluded_reason")) == REQUIRED_RUNTIME_EXCLUSION_REASON
    ]
    issue_codes = sorted({issue.code for issue in issues})
    return {
        "scenario_id": manifest.get("scenario_id", ""),
        "valid": not issues,
        "issue_codes": issue_codes,
        "issues": [issue.as_dict() for issue in issues],
        "runtime_artifact_ids": runtime_ids,
        "selected_item_ids": selected_ids,
        "excluded_runtime_artifact_ids": excluded_runtime_ids,
        "runtime_artifact_non_claims": {
            "runtime_artifacts_not_evidence_support": True,
            "runtime_artifacts_not_reviewed_knowledge": True,
            "runtime_artifacts_not_action_basis": True,
            "runtime_filter_pass_not_reviewer_approval": True,
            "sandbox_not_mainline": True,
        },
    }


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate runtime artifact exclusion in a sandbox manifest."
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
            "issue_codes": ["RA_PARSE_OR_RUNTIME_ERROR"],
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
