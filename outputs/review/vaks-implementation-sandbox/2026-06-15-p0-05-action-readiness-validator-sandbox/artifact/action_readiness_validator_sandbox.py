#!/usr/bin/env python3
"""
Sandbox-only P0-05 action readiness validator.

This prototype checks one Markdown file with flat YAML-like frontmatter. It is
read-only and uses only the Python standard library. It does not approve actions,
write mainline files, promote reviewed knowledge, or replace human review.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


READY_STATE = "ready"

BAD_BASIS_CODES = {
    "candidate": "AR_CANDIDATE_BASIS_READY",
    "candidate_distillation": "AR_CANDIDATE_BASIS_READY",
    "candidate_point": "AR_CANDIDATE_BASIS_READY",
    "project_overlay": "AR_CANDIDATE_BASIS_READY",
    "feedback": "AR_FEEDBACK_BASIS_READY",
    "feedback_event": "AR_FEEDBACK_BASIS_READY",
    "retrieval_rank": "AR_RETRIEVAL_RANK_BASIS_READY",
    "retrieval_score": "AR_RETRIEVAL_RANK_BASIS_READY",
    "graph_rank": "AR_RETRIEVAL_RANK_BASIS_READY",
    "source_summary": "AR_SOURCE_SUMMARY_BASIS_READY",
    "briefing_summary": "AR_SOURCE_SUMMARY_BASIS_READY",
}

DIAGNOSTIC_BASIS = {
    "validator_pass",
    "test_pass",
    "lint_pass",
    "blind_review",
    "llm_judge",
    "operation_receipt",
}

POSITIVE_ACTION_BASIS = {
    "reviewed_support",
    "evidence_packet",
}

SIGNIFICANT_ACTION_MODES = {
    "decision",
    "implementation",
    "propose_write",
    "write",
    "delete",
    "schema_change",
    "deploy",
}

WRITE_OPERATION_MODES = {"write", "delete", "schema_change"}


@dataclass(frozen=True)
class Issue:
    code: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message}


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


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


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


def is_ready(record: dict[str, Any]) -> bool:
    return (
        norm(record.get("action_readiness")) == READY_STATE
        or as_bool(record.get("action_basis_ready_claimed"))
    )


def is_significant_action(record: dict[str, Any]) -> bool:
    action_mode = norm(record.get("action_mode"))
    operation_mode = norm(record.get("operation_mode"))
    return (
        as_bool(record.get("significant_action"))
        or action_mode in SIGNIFICANT_ACTION_MODES
        or operation_mode in SIGNIFICANT_ACTION_MODES
    )


def validate_record(record: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []

    if norm(record.get("record_kind")) != "action_readiness_check":
        add_once(
            issues,
            "AR_INVALID_RECORD_KIND",
            "record_kind must be action_readiness_check.",
        )

    if not has_value(record.get("action_id")):
        add_once(issues, "AR_MISSING_ACTION_ID", "action_id is required.")

    if not has_value(record.get("action_readiness")):
        add_once(
            issues,
            "AR_MISSING_ACTION_READINESS",
            "action_readiness is required.",
        )

    if issues:
        return issues

    if not is_ready(record):
        return issues

    evidence_sufficiency = norm(record.get("evidence_sufficiency"))
    temporal_applicability = norm(record.get("temporal_applicability"))
    evidence_support_status = norm(record.get("evidence_support_status"))
    basis_materials = set(as_list(record.get("basis_materials")))

    if evidence_sufficiency == "insufficient":
        add_once(
            issues,
            "AR_INSUFFICIENT_EVIDENCE_READY",
            "insufficient evidence_sufficiency cannot produce ready action basis.",
        )

    if evidence_sufficiency == "out_of_scope":
        add_once(
            issues,
            "AR_OUT_OF_SCOPE_READY",
            "out_of_scope evidence_sufficiency cannot produce ready action basis.",
        )

    if evidence_sufficiency == "risky" or as_bool(record.get("unresolved_risk")):
        add_once(
            issues,
            "AR_UNRESOLVED_RISK_READY",
            "unresolved or risky evidence cannot be action_readiness ready.",
        )

    if evidence_sufficiency != "sufficient":
        add_once(
            issues,
            "AR_EVIDENCE_SUFFICIENCY_NOT_SUFFICIENT",
            "ready action basis requires explicit evidence_sufficiency: sufficient.",
        )

    if evidence_support_status in {
        "unsupported",
        "unclear",
        "missing_anchor",
        "not_checked",
        "self_support_loop",
    }:
        add_once(
            issues,
            "AR_SUPPORT_NOT_SUPPORTED_READY",
            "ready action basis requires supported current evidence, not weak support.",
        )

    if temporal_applicability in {"stale", "superseded", "out_of_scope"}:
        if not (
            has_value(record.get("replacement_basis_ref"))
            or has_value(record.get("narrowed_scope_ref"))
        ):
            add_once(
                issues,
                "AR_STALE_SUPERSEDED_WITHOUT_REPLACEMENT_READY",
                "stale, superseded, or out_of_scope basis needs replacement or narrowed scope before ready.",
            )

    if as_bool(record.get("warnings_or_gaps_trimmed")) or as_bool(
        record.get("missing_evidence_trimmed")
    ):
        add_once(
            issues,
            "AR_HIDDEN_WARNING_OR_GAP_READY",
            "known warning, gap, or missing evidence was hidden by trimming.",
        )

    if is_significant_action(record) and not as_bool(record.get("intent_confirmed")):
        add_once(
            issues,
            "AR_MISSING_INTENT_CONFIRMATION",
            "significant action requires explicit intent confirmation before ready.",
        )

    if is_significant_action(record) and not as_bool(
        record.get("success_criteria_present")
    ):
        add_once(
            issues,
            "AR_MISSING_SUCCESS_CRITERIA",
            "significant action basis needs visible success criteria.",
        )

    for material in sorted(basis_materials):
        if material in BAD_BASIS_CODES:
            code = BAD_BASIS_CODES[material]
            add_once(
                issues,
                code,
                f"{material} can orient review but cannot be action basis.",
            )

    has_positive_basis = bool(basis_materials.intersection(POSITIVE_ACTION_BASIS)) or any(
        has_value(record.get(field))
        for field in ("action_basis_ref", "reviewed_support_refs", "evidence_packet_ref")
    )
    if not has_positive_basis:
        add_once(
            issues,
            "AR_MISSING_REVIEWED_ACTION_BASIS",
            "ready action basis requires reviewed support or an evidence packet reference.",
        )

    if "context_pack" in basis_materials and not (
        "reviewed_support" in basis_materials or "evidence_packet" in basis_materials
    ):
        add_once(
            issues,
            "AR_CONTEXT_PACK_ONLY_READY",
            "context pack alone is not ready action basis.",
        )

    if basis_materials.intersection(DIAGNOSTIC_BASIS):
        add_once(
            issues,
            "AR_DIAGNOSTIC_BASIS_READY",
            "diagnostic, receipt, or judge output cannot substitute for action basis.",
        )

    reviewed_write = as_bool(record.get("reviewed_write")) or norm(
        record.get("target_bucket")
    ) in {"reviewed", "reviewed_knowledge", "decision"}

    if reviewed_write and not as_bool(record.get("approved")):
        add_once(
            issues,
            "AR_REVIEWED_WRITE_MISSING_APPROVAL",
            "reviewed write needs explicit approval before ready.",
        )

    if reviewed_write and not as_bool(record.get("checked_body_hash_present")):
        add_once(
            issues,
            "AR_REVIEWED_WRITE_MISSING_CHECKED_BODY_HASH",
            "reviewed write needs checked body hash before ready.",
        )

    operation_mode = norm(record.get("operation_mode"))
    action_mode = norm(record.get("action_mode"))
    destructive = operation_mode in {"delete", "schema_change"} or action_mode in {
        "delete",
        "schema_change",
    } or as_bool(
        record.get("rollback_required")
    )
    if destructive and not as_bool(record.get("rollback_plan_present")):
        add_once(
            issues,
            "AR_DESTRUCTIVE_MISSING_ROLLBACK",
            "destructive or hard-to-rollback action needs a rollback plan.",
        )

    actor_tier = norm(record.get("actor_tier"))
    if actor_tier in {"read_only", "readonly", "suggest_only"} and (
        operation_mode in WRITE_OPERATION_MODES or action_mode in WRITE_OPERATION_MODES
    ):
        add_once(
            issues,
            "AR_READ_ONLY_ACTOR_WRITE",
            "read-only or suggest-only actor cannot perform write operations.",
        )

    if (operation_mode == "schema_change" or action_mode == "schema_change") and not as_bool(
        record.get("owner_final")
    ):
        add_once(
            issues,
            "AR_SCHEMA_CHANGE_MISSING_OWNER_FINAL",
            "schema change needs owner_final before ready.",
        )

    return issues


def validate_path(path: Path) -> tuple[dict[str, Any] | None, list[Issue]]:
    try:
        text = path.read_text(encoding="utf-8")
        record = parse_frontmatter(text)
    except OSError as exc:
        return None, [Issue("AR_READ_ERROR", str(exc))]
    except ValueError as exc:
        return None, [Issue("AR_INVALID_FRONTMATTER", str(exc))]
    return record, validate_record(record)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Validate one sandbox action readiness record."
    )
    parser.add_argument("record", help="Markdown record with flat frontmatter")
    parser.add_argument("--json", action="store_true", help="emit JSON result")
    args = parser.parse_args(argv)

    path = Path(args.record)
    record, issues = validate_path(path)
    status = "pass" if not issues else "fail"
    payload = {
        "status": status,
        "record": str(path),
        "action_id": "" if record is None else record.get("action_id", ""),
        "issues": [issue.as_dict() for issue in issues],
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif not issues:
        print(f"PASS action_readiness {path}")
    else:
        print(f"FAIL action_readiness {path}")
        for issue in issues:
            print(f"{issue.code}: {issue.message}")

    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
