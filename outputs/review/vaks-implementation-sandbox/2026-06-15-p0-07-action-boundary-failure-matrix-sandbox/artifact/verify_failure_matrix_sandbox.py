#!/usr/bin/env python3
"""
Sandbox-only P0-07 action-boundary failure matrix verifier.

This verifier checks JSON matrix shape and P0-07 minimum coverage. It does not
run the earlier validators, approve mainline promotion, create reviewed
knowledge, or grant action basis.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p0-07-action-boundary-failure-matrix-sandbox"

REQUIRED_CASES = {
    "AB-01": "body_hash mismatch still approved",
    "AB-02": "checked_body_hash mismatch writeback",
    "AB-03": "candidate item marked support",
    "AB-04": "URL-only citation marked direct_support",
    "AB-05": "graph_rank marked trust",
    "AB-06": "feedback modifies truth_confidence",
    "AB-07": "stale point produces ready action basis",
    "AB-08": "budget trimming hides missing evidence",
    "AB-09": "read-only actor writes file",
    "AB-10": "schema change without owner_final",
    "AB-11": "destructive operation without rollback",
    "AB-12": "retrieval receipt crosses authority buckets",
}

REQUIRED_CASE_FIELDS = {
    "case_id",
    "title",
    "failure_mode",
    "boundary_class",
    "source_refs",
    "blocked_by",
    "detection",
    "expected_outcome",
    "fixture_refs",
    "validator_or_check_refs",
    "authority_non_claims",
}

FALSE_AUTHORITY_FLAGS = {
    "mainline_ready",
    "reviewer_approval_created",
    "reviewed_knowledge_created",
    "evidence_support_created",
    "action_basis_created",
    "promotion_authorized",
}

BLOCKING_OUTCOMES = {"blocked", "not_ready", "requires_review", "reject"}


@dataclass(frozen=True)
class Issue:
    code: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message}


def has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, list):
        return any(has_value(item) for item in value)
    if isinstance(value, dict):
        return any(has_value(item) for item in value.values())
    return str(value).strip() != ""


def add_once(issues: list[Issue], code: str, message: str) -> None:
    if code not in {issue.code for issue in issues}:
        issues.append(Issue(code, message))


def validate_authority_flags(
    value: Any, issues: list[Issue], context: str
) -> None:
    if not isinstance(value, dict):
        add_once(
            issues,
            "MATRIX_MISSING_AUTHORITY_NON_CLAIM",
            f"{context} authority_non_claims must be an object.",
        )
        return

    for flag in FALSE_AUTHORITY_FLAGS:
        if flag not in value:
            add_once(
                issues,
                "MATRIX_MISSING_AUTHORITY_NON_CLAIM",
                f"{context} missing authority_non_claims.{flag}.",
            )
        elif value[flag] is not False:
            add_once(
                issues,
                "MATRIX_FORBIDDEN_AUTHORITY_CLAIM",
                f"{context} authority_non_claims.{flag} must be false.",
            )


def validate_case(case: Any, issues: list[Issue]) -> None:
    if not isinstance(case, dict):
        add_once(issues, "MATRIX_INVALID_CASE", "case entry must be an object.")
        return

    case_id = str(case.get("case_id", "")).strip()
    context = case_id or "case"

    for field in REQUIRED_CASE_FIELDS:
        if field not in case or not has_value(case.get(field)):
            add_once(
                issues,
                "MATRIX_CASE_MISSING_FIELD",
                f"{context} missing required field {field}.",
            )

    for list_field in ("source_refs", "blocked_by", "fixture_refs", "validator_or_check_refs"):
        if not isinstance(case.get(list_field), list) or not case.get(list_field):
            add_once(
                issues,
                "MATRIX_CASE_MISSING_FIELD",
                f"{context} field {list_field} must be a non-empty list.",
            )

    for guard in case.get("blocked_by", []):
        if not isinstance(guard, dict) or not has_value(guard.get("slice_id")) or not has_value(
            guard.get("guard")
        ):
            add_once(
                issues,
                "MATRIX_CASE_MISSING_GUARD",
                f"{context} blocked_by entries need slice_id and guard.",
            )

    outcome = case.get("expected_outcome")
    if not isinstance(outcome, dict) or str(outcome.get("status", "")).strip() not in BLOCKING_OUTCOMES:
        add_once(
            issues,
            "MATRIX_CASE_NOT_BLOCKING",
            f"{context} expected_outcome.status must be blocking.",
        )

    validate_authority_flags(case.get("authority_non_claims"), issues, context)


def validate_matrix(data: Any) -> list[Issue]:
    issues: list[Issue] = []

    if not isinstance(data, dict):
        return [Issue("MATRIX_INVALID_JSON_SHAPE", "top-level JSON must be an object.")]

    if data.get("record_kind") != "action_boundary_failure_matrix":
        add_once(
            issues,
            "MATRIX_INVALID_RECORD_KIND",
            "record_kind must be action_boundary_failure_matrix.",
        )

    if data.get("slice_id") != SLICE_ID:
        add_once(issues, "MATRIX_INVALID_SLICE_ID", f"slice_id must be {SLICE_ID}.")

    validate_authority_flags(data.get("authority_non_claims"), issues, "matrix")

    cases = data.get("cases")
    if not isinstance(cases, list):
        add_once(issues, "MATRIX_CASES_NOT_LIST", "cases must be a list.")
        return issues

    seen: set[str] = set()
    case_ids: set[str] = set()
    for case in cases:
        case_id = str(case.get("case_id", "")).strip() if isinstance(case, dict) else ""
        if case_id in seen:
            add_once(issues, "MATRIX_DUPLICATE_CASE_ID", f"duplicate case_id {case_id}.")
        if case_id:
            seen.add(case_id)
            case_ids.add(case_id)
            if case_id.startswith("AB-") and case_id not in REQUIRED_CASES:
                add_once(issues, "MATRIX_UNKNOWN_CASE_ID", f"unknown required-scope case {case_id}.")
        validate_case(case, issues)

    missing = sorted(set(REQUIRED_CASES) - case_ids)
    if missing:
        add_once(
            issues,
            "MATRIX_MISSING_REQUIRED_CASE",
            "missing required cases: " + ", ".join(missing),
        )

    return issues


def load_json(path: Path) -> tuple[Any | None, list[Issue]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except OSError as exc:
        return None, [Issue("MATRIX_READ_ERROR", str(exc))]
    except json.JSONDecodeError as exc:
        return None, [Issue("MATRIX_JSON_PARSE_ERROR", str(exc))]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Validate one sandbox action-boundary failure matrix JSON file."
    )
    parser.add_argument("matrix", help="Matrix JSON file")
    parser.add_argument("--json", action="store_true", help="emit JSON result")
    args = parser.parse_args(argv)

    path = Path(args.matrix)
    data, issues = load_json(path)
    if data is not None:
        issues.extend(validate_matrix(data))

    status = "pass" if not issues else "fail"
    payload = {
        "status": status,
        "matrix": str(path),
        "issues": [issue.as_dict() for issue in issues],
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif not issues:
        print(f"PASS action_boundary_failure_matrix {path}")
    else:
        print(f"FAIL action_boundary_failure_matrix {path}")
        for issue in issues:
            print(f"{issue.code}: {issue.message}")

    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

