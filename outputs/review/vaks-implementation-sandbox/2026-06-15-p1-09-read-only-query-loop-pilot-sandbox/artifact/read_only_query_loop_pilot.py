#!/usr/bin/env python3
"""
Sandbox-only P1-09 read-only query loop pilot.

This prototype consumes compact scenario fixtures and proves that a read-only
query loop can emit retrieval/operation receipts while refusing to turn
retrieval, candidates, stale decisions, feedback, or proposals into action
authority. It uses the P1-08 sandbox receipt validator and the Python standard
library only.
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

ROOT = Path(__file__).resolve().parents[1]
P1_08_VALIDATOR = (
    ROOT.parent
    / "2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox"
    / "artifact"
    / "receipt_validator_pilot.py"
)

STORY_KINDS = {
    "ordinary_orientation",
    "action_adjacent",
    "candidate_temptation",
    "stale_decision",
    "feedback_correction",
    "agent_propose_write",
}

ACTION_ADJACENT_GATES = {
    "context_pack_present",
    "support_check_present",
    "action_readiness_check_present",
}

FORBIDDEN_SIDE_EFFECT_FIELDS = {
    "runtime_write_attempted",
    "filesystem_write_performed",
    "mainline_write_claimed",
    "promotion_attempted",
    "obsidian_sync_attempted",
    "commit_attempted",
    "push_attempted",
    "hook_installed",
    "background_service_started",
    "mcp_write_tool_used",
}


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


def load_receipt_validator():
    if not P1_08_VALIDATOR.exists():
        raise FileNotFoundError(f"P1-08 receipt validator not found: {P1_08_VALIDATOR}")
    spec = importlib.util.spec_from_file_location("p1_08_receipt_validator", P1_08_VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load P1-08 validator from {P1_08_VALIDATOR}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["p1_08_receipt_validator"] = module
    spec.loader.exec_module(module)
    return module


def build_retrieval_receipt(scenario: dict[str, Any]) -> dict[str, Any]:
    included_buckets = as_list(scenario.get("included_buckets")) or ["reviewed"]
    selected_buckets = as_list(scenario.get("selected_authority_buckets")) or included_buckets
    selected_roles = as_list(scenario.get("selected_pack_roles")) or ["orientation"]

    return {
        "record_kind": "retrieval_receipt",
        "receipt_id": f"rr-{scenario.get('scenario_id', 'unknown')}",
        "query_id": scenario.get("scenario_id", "unknown"),
        "query_mode": scenario.get("query_mode", "orientation"),
        "requested_authority_bucket": scenario.get(
            "requested_authority_bucket", "mixed_for_orientation"
        ),
        "included_buckets": included_buckets,
        "rrf_scope": scenario.get("rrf_scope", "same_authority_bucket_only"),
        "cross_bucket_rrf_used": scenario.get("cross_bucket_rrf_used", False),
        "cross_bucket_rank_used": scenario.get("cross_bucket_rank_used", False),
        "selected_item_authority_buckets": selected_buckets,
        "selected_item_pack_roles": selected_roles,
        "selected_item_action_basis_allowed": scenario.get(
            "selected_action_basis_allowed", False
        ),
        "selected_by_claims_support": scenario.get("selected_by_claims_support", False),
        "retrieval_rank_claims_support": scenario.get(
            "retrieval_rank_claims_support", False
        ),
        "scores_are_support": scenario.get("scores_are_support", False),
        "graph_rank_claims_trust": scenario.get("graph_rank_claims_trust", False),
        "legacy_raw_metadata_used": scenario.get("legacy_raw_metadata_used", False),
        "support_result": scenario.get("support_result", "not_ready"),
        "support_evidence_role": scenario.get(
            "support_evidence_role", "background_context"
        ),
        "support_anchor_kind": scenario.get("support_anchor_kind", ""),
        "independent_anchor_ref": scenario.get("independent_anchor_ref", ""),
        "support_claimed": scenario.get("support_claimed", False),
        "receipt_claims": as_list(scenario.get("retrieval_receipt_claims")),
        "selected_by_is_not_support": scenario.get("selected_by_is_not_support", True),
        "same_bucket_rrf_only": scenario.get("same_bucket_rrf_only", True),
        "cross_bucket_rank_not_authority": scenario.get(
            "cross_bucket_rank_not_authority", True
        ),
        "legacy_raw_metadata_excluded": scenario.get("legacy_raw_metadata_excluded", True),
        "candidate_overlay_feedback_not_support": scenario.get(
            "candidate_overlay_feedback_not_support", True
        ),
        "url_only_not_direct_support": scenario.get("url_only_not_direct_support", True),
        "graph_rank_not_trust": scenario.get("graph_rank_not_trust", True),
        "receipt_not_review_approval": scenario.get(
            "retrieval_receipt_not_review_approval", True
        ),
        "receipt_not_action_basis": scenario.get(
            "retrieval_receipt_not_action_basis", True
        ),
        "receipt_not_reviewed_knowledge": scenario.get(
            "retrieval_receipt_not_reviewed_knowledge", True
        ),
    }


def operation_receipt_required(scenario: dict[str, Any]) -> bool:
    story_kind = norm(scenario.get("story_kind"))
    return story_kind == "agent_propose_write" or as_bool(
        scenario.get("operation_receipt_required")
    )


def build_operation_receipt(scenario: dict[str, Any]) -> dict[str, Any] | None:
    if not operation_receipt_required(scenario) and not as_bool(
        scenario.get("operation_receipt_present")
    ):
        return None
    if not as_bool(scenario.get("operation_receipt_present")):
        return None

    return {
        "record_kind": "operation_receipt",
        "operation_id": f"op-{scenario.get('scenario_id', 'unknown')}",
        "actor_tier": scenario.get("actor_tier", "suggest_only"),
        "operation_mode": scenario.get("operation_mode", "propose_write"),
        "actual_write_performed": scenario.get("operation_actual_write_performed", False),
        "target_scope": scenario.get("target_scope", "sandbox"),
        "user_intent_confirmed": scenario.get("user_intent_confirmed", True),
        "basis_materials": as_list(scenario.get("operation_basis_materials"))
        or ["reviewed_support"],
        "approval_present": scenario.get("approval_present", False),
        "checked_body_hash": scenario.get("checked_body_hash", ""),
        "checked_body_hash_match": scenario.get("checked_body_hash_match", True),
        "owner_final_present": scenario.get("owner_final_present", False),
        "rollback_required": scenario.get("rollback_required", False),
        "rollback_plan_present": scenario.get("rollback_plan_present", False),
        "operation_claims": as_list(scenario.get("operation_claims")),
        "receipt_not_truth": scenario.get("receipt_not_truth", True),
        "receipt_not_review_approval": scenario.get(
            "operation_receipt_not_review_approval", True
        ),
        "receipt_not_reviewed_knowledge": scenario.get(
            "operation_receipt_not_reviewed_knowledge", True
        ),
        "receipt_not_action_basis": scenario.get(
            "operation_receipt_not_action_basis", True
        ),
        "validator_pass_not_reviewer_approval": scenario.get(
            "validator_pass_not_reviewer_approval", True
        ),
        "sandbox_not_mainline": scenario.get("sandbox_not_mainline", True),
    }


def validate_story_rules(scenario: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    story_kind = norm(scenario.get("story_kind"))

    if story_kind not in STORY_KINDS:
        add_once(
            issues,
            "QL_UNKNOWN_STORY_KIND",
            "story_kind must be one of the six P1 pilot stories.",
        )
        return issues

    for field in sorted(FORBIDDEN_SIDE_EFFECT_FIELDS):
        if as_bool(scenario.get(field)):
            add_once(
                issues,
                "QL_FORBIDDEN_SIDE_EFFECT",
                f"read-only query loop cannot perform or claim side effect: {field}.",
            )

    if as_bool(scenario.get("action_basis_ready_claimed")):
        add_once(
            issues,
            "QL_READ_ONLY_ACTION_BASIS_CLAIM",
            "read-only query loop cannot claim ready action basis.",
        )

    if operation_receipt_required(scenario) and not as_bool(
        scenario.get("operation_receipt_present")
    ):
        add_once(
            issues,
            "QL_OPERATION_RECEIPT_REQUIRED",
            "operation-receipt-required scenarios must emit an operation receipt.",
        )

    if story_kind == "ordinary_orientation":
        if as_bool(scenario.get("full_audit_required")):
            add_once(
                issues,
                "QL_ORDINARY_QUERY_OVERSTRICT",
                "ordinary orientation queries must not require full audit.",
            )

    if story_kind == "action_adjacent":
        missing = sorted(
            field for field in ACTION_ADJACENT_GATES if not as_bool(scenario.get(field))
        )
        if missing:
            add_once(
                issues,
                "QL_ACTION_ADJACENT_MISSING_GATE",
                f"action-adjacent query is missing required gate(s): {missing}.",
            )

    if story_kind == "candidate_temptation":
        if as_bool(scenario.get("candidate_used_as_support")) or as_bool(
            scenario.get("candidate_used_as_action_basis")
        ):
            add_once(
                issues,
                "QL_CANDIDATE_USED_AS_SUPPORT",
                "candidate material cannot support action-facing answers or action basis.",
            )
        if not as_bool(scenario.get("candidate_boundary_warning_present")):
            add_once(
                issues,
                "QL_CANDIDATE_WARNING_MISSING",
                "candidate temptation scenario must expose a candidate boundary warning.",
            )

    if story_kind == "stale_decision":
        if as_bool(scenario.get("stale_decision_used_for_ready_action")):
            add_once(
                issues,
                "QL_STALE_DECISION_READY_ACTION",
                "stale decisions may explain history but cannot produce ready action.",
            )
        if not as_bool(scenario.get("stale_warning_present")):
            add_once(
                issues,
                "QL_STALE_WARNING_MISSING",
                "stale decision scenario must expose a stale/superseded warning.",
            )

    if story_kind == "feedback_correction":
        if (
            as_bool(scenario.get("truth_mutation_attempted"))
            or as_bool(scenario.get("feedback_changes_truth_confidence"))
            or as_bool(scenario.get("reviewed_note_modified"))
        ):
            add_once(
                issues,
                "QL_FEEDBACK_MUTATES_TRUTH",
                "feedback correction can create review pressure but cannot mutate truth.",
            )
        if not as_bool(scenario.get("review_due_envelope_emitted")):
            add_once(
                issues,
                "QL_FEEDBACK_REVIEW_DUE_MISSING",
                "explicit correction should emit a review_due envelope.",
            )

    if story_kind == "agent_propose_write":
        if as_bool(scenario.get("reviewed_write_performed")) or as_bool(
            scenario.get("operation_actual_write_performed")
        ):
            add_once(
                issues,
                "QL_AGENT_PROPOSE_WRITE_PERFORMED_WRITE",
                "agent propose-write story must remain proposal-only.",
            )

    return issues


def outcome_for(story_kind: str) -> str:
    return {
        "ordinary_orientation": "orientation_answer",
        "action_adjacent": "action_gated_answer",
        "candidate_temptation": "candidate_blocked_as_support",
        "stale_decision": "historical_only_ready_action_blocked",
        "feedback_correction": "review_due_envelope_truth_unchanged",
        "agent_propose_write": "proposal_only_with_operation_receipt",
    }.get(story_kind, "blocked")


def run_scenario(scenario: dict[str, Any], receipt_validator=None) -> dict[str, Any]:
    if receipt_validator is None:
        receipt_validator = load_receipt_validator()

    issues = validate_story_rules(scenario)
    retrieval_receipt = build_retrieval_receipt(scenario)
    retrieval_issues = receipt_validator.validate_record(retrieval_receipt)
    if retrieval_issues:
        add_once(
            issues,
            "QL_RETRIEVAL_RECEIPT_INVALID",
            "generated retrieval receipt failed P1-08 validation.",
        )

    operation_receipt = build_operation_receipt(scenario)
    operation_issues = []
    if operation_receipt is not None:
        operation_issues = receipt_validator.validate_record(operation_receipt)
        if operation_issues:
            add_once(
                issues,
                "QL_OPERATION_RECEIPT_INVALID",
                "generated operation receipt failed P1-08 validation.",
            )

    issue_codes = {issue.code for issue in issues}
    issue_codes.update(issue.code for issue in retrieval_issues)
    issue_codes.update(issue.code for issue in operation_issues)
    valid = not issue_codes
    story_kind = norm(scenario.get("story_kind"))

    return {
        "scenario_id": scenario.get("scenario_id", ""),
        "story_kind": story_kind,
        "valid": valid,
        "outcome": outcome_for(story_kind) if valid else "blocked",
        "issue_codes": sorted(issue_codes),
        "issues": [issue.as_dict() for issue in issues],
        "retrieval_receipt": {
            "present": True,
            "valid": not retrieval_issues,
            "issue_codes": sorted({issue.code for issue in retrieval_issues}),
            "record": retrieval_receipt,
        },
        "operation_receipt": {
            "present": operation_receipt is not None,
            "valid": not operation_issues,
            "issue_codes": sorted({issue.code for issue in operation_issues}),
            "record": operation_receipt,
        },
        "query_loop_non_claims": {
            "read_only_loop_not_reviewer_approval": True,
            "retrieval_found_not_evidence_support": True,
            "candidate_not_action_basis": True,
            "feedback_not_truth_mutation": True,
            "operation_receipt_not_approval": True,
            "validator_pass_not_product_acceptance": True,
            "sandbox_not_mainline": True,
        },
    }


def load_scenario(path: Path) -> dict[str, Any]:
    record = parse_frontmatter(path.read_text(encoding="utf-8"))
    if norm(record.get("record_kind")) != "read_only_query_scenario":
        raise ValueError("record_kind must be read_only_query_scenario")
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run one read-only query scenario.")
    parser.add_argument("path", type=Path, help="Scenario Markdown file")
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
        scenario = load_scenario(args.path)
        result = run_scenario(scenario)
    except Exception as exc:  # pragma: no cover - CLI boundary
        result = {
            "path": str(args.path),
            "valid": False,
            "outcome": "blocked",
            "issue_codes": ["QL_PARSE_OR_RUNTIME_ERROR"],
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
