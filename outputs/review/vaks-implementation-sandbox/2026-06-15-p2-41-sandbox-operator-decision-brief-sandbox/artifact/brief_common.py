from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p2-41-sandbox-operator-decision-brief-sandbox"
SOURCE_SLICE_ID = "2026-06-15-p2-40-sandbox-product-grade-rollup-dashboard-sandbox"
ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[3]
SOURCE_ROOT = ROOT.parent / SOURCE_SLICE_ID
ROLLUP_DATA = SOURCE_ROOT / "artifact" / "rollup-data.json"
SOURCE_PRODUCT_REPORT = SOURCE_ROOT / "product-acceptance-report.md"

VERSION = "sandbox-operator-decision-brief-v1"
TRUTH_BOUNDARY = "sandbox_operator_decision_brief_not_authority"
PURPOSE = "human-readable operator decision brief for sandbox status and required approvals"
WRITE_SCOPE = f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"

DECISION_OPTIONS = [
    {
        "id": "continue_sandbox_hardening",
        "decision": "allowed_only_in_fresh_sandbox",
        "requires_user_approval": False,
        "requires_fresh_sandbox": True,
        "operation_authorized_now": False,
        "reason": "Existing Product PASS artifacts may inform another sandbox slice, but do not authorize mainline or formal vault work.",
    },
    {
        "id": "prepare_promotion_request_packet",
        "decision": "allowed_as_sandbox_draft_only",
        "requires_user_approval": True,
        "requires_fresh_sandbox": True,
        "operation_authorized_now": False,
        "reason": "A request packet can be drafted in sandbox, but promotion itself needs separate explicit user approval.",
    },
    {
        "id": "formal_vault_work",
        "decision": "blocked_needs_separate_user_approval",
        "requires_user_approval": True,
        "requires_fresh_sandbox": False,
        "operation_authorized_now": False,
        "reason": "Sandbox PASS is not formal vault approval or Obsidian sync permission.",
    },
    {
        "id": "mainline_merge_commit_push",
        "decision": "blocked_needs_separate_user_approval",
        "requires_user_approval": True,
        "requires_fresh_sandbox": False,
        "operation_authorized_now": False,
        "reason": "Sandbox PASS is not mainline readiness, commit approval, push approval, or promotion approval.",
    },
    {
        "id": "use_as_action_basis",
        "decision": "blocked",
        "requires_user_approval": True,
        "requires_fresh_sandbox": False,
        "operation_authorized_now": False,
        "reason": "Sandbox status is not reviewed knowledge, evidence support, or action basis.",
    },
]

BLOCKED_OPERATIONS = [
    "formal_vault_read",
    "formal_vault_scan",
    "formal_vault_write",
    "formal_vault_hash",
    "formal_vault_snapshot",
    "formal_vault_state_check",
    "obsidian_sync",
    "commit",
    "push",
    "promotion",
    "dependency_install",
    "background_service",
    "mcp_write_tool",
    "hooks",
    "approval_collection",
    "user_instruction_collection",
    "user_wording_storage",
    "command_emitted",
    "execution_permission_granted",
    "execution_performed",
    "action_basis_creation",
    "reviewed_knowledge_creation",
    "evidence_support_creation",
    "mainline_merge",
    "dirty_tree_repair",
    "auto_advance",
]

REQUIRED_NON_CLAIMS = [
    "not formal vault approval",
    "not formal vault state",
    "not formal vault access",
    "not Obsidian sync",
    "not user approval",
    "not user instruction",
    "not execution permission",
    "not command surface",
    "not reviewed knowledge",
    "not evidence support",
    "not action basis",
    "not mainline readiness",
    "not promotion approval",
    "not dirty-tree repair",
    "not auto advance",
]

BRIEF_CONTROLS = [
    "source_rollup_pass_required",
    "all_product_pass_count_visible",
    "verification_count_visible",
    "revision_history_visible",
    "fresh_sandbox_only_for_continuation",
    "separate_approval_for_formal_vault",
    "separate_approval_for_mainline",
    "no_action_basis_claim",
    "no_evidence_support_claim",
    "no_reviewed_knowledge_claim",
]


def rel(path: Path) -> str:
    return path.resolve().relative_to(WORKSPACE).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_status(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^status:\s*(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def source_snapshot() -> dict[str, Any]:
    rollup = read_json(ROLLUP_DATA)
    product_text = SOURCE_PRODUCT_REPORT.read_text(encoding="utf-8", errors="ignore")
    return {
        "source_slice_id": SOURCE_SLICE_ID,
        "rollup_data_path": rel(ROLLUP_DATA),
        "rollup_data_sha256": sha256_file(ROLLUP_DATA),
        "product_report_path": rel(SOURCE_PRODUCT_REPORT),
        "product_report_sha256": sha256_file(SOURCE_PRODUCT_REPORT),
        "source_product_status": parse_status(SOURCE_PRODUCT_REPORT),
        "source_product_pass_text": "PASS_PRODUCT_GRADE" in product_text,
        "source_slice_count": rollup.get("source_slice_count"),
        "product_pass_count": rollup.get("product_pass_count"),
        "verification_present_count": rollup.get("verification_present_count"),
        "revision_slice_count": len(rollup.get("revision_slices", [])),
        "non_pass_slices": rollup.get("non_pass_slices", []),
        "missing_verification_slices": rollup.get("missing_verification_slices", []),
        "rollup_truth_boundary": rollup.get("truth_boundary"),
        "rollup_authority_flags": {
            "mainline": rollup.get("operator_summary", {}).get("rollup_is_mainline_authority"),
            "formal_vault": rollup.get("operator_summary", {}).get("rollup_is_formal_vault_authority"),
            "action_basis": rollup.get("operator_summary", {}).get("rollup_is_action_basis"),
        },
    }


def default_brief(view: str = "operator-decision-brief") -> dict[str, Any]:
    snapshot = source_snapshot()
    return {
        "record_kind": "sandbox_operator_decision_brief",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
        "view": view,
        "source_snapshot": snapshot,
        "plain_verdict": "sandbox_product_grade_operator_ready_not_enterprise_production",
        "safe_summary": {
            "completed_sandbox_slices": snapshot["source_slice_count"],
            "product_grade_sandbox_slices": snapshot["product_pass_count"],
            "verified_sandbox_slices": snapshot["verification_present_count"],
            "revision_history_slices": snapshot["revision_slice_count"],
            "current_status": "sandbox_product_grade_rollup_available",
            "enterprise_experience_status": "operator_grade_sandbox_experience_not_full_enterprise_production",
        },
        "decision_options": copy.deepcopy(DECISION_OPTIONS),
        "required_separate_approvals": [
            "formal vault scan/write/sync",
            "mainline merge",
            "promotion",
            "commit",
            "push",
            "using sandbox output as action basis",
            "moving artifacts into templates or tools",
        ],
        "blocked_operations": {name: False for name in BLOCKED_OPERATIONS},
        "brief_controls": {name: True for name in BRIEF_CONTROLS},
        "required_non_claims": list(REQUIRED_NON_CLAIMS),
        "operator_next_step": "continue only in a fresh sandbox slice unless the user separately approves a boundary-crossing action",
    }


def validate_brief(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "record_kind": "sandbox_operator_decision_brief",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            errors.append(f"{key}_mismatch")

    current = default_brief(data.get("view", "operator-decision-brief"))
    for key in ["source_snapshot", "safe_summary", "decision_options", "required_separate_approvals"]:
        if data.get(key) != current.get(key):
            errors.append(f"{key}_mismatch")

    if data.get("plain_verdict") != "sandbox_product_grade_operator_ready_not_enterprise_production":
        errors.append("plain_verdict_mismatch")

    snapshot = data.get("source_snapshot", {})
    if snapshot.get("source_product_status") != "pass_product_grade":
        errors.append("source_product_status_not_pass")
    if snapshot.get("source_product_pass_text") is not True:
        errors.append("source_product_pass_text_missing")
    if snapshot.get("source_slice_count") != 39:
        errors.append("source_slice_count_mismatch")
    if snapshot.get("product_pass_count") != 39:
        errors.append("product_pass_count_mismatch")
    if snapshot.get("verification_present_count") != 39:
        errors.append("verification_present_count_mismatch")
    if snapshot.get("revision_slice_count") != 8:
        errors.append("revision_slice_count_mismatch")
    if snapshot.get("non_pass_slices"):
        errors.append("non_pass_slices_present")
    if snapshot.get("missing_verification_slices"):
        errors.append("missing_verification_slices_present")
    for key, value in snapshot.get("rollup_authority_flags", {}).items():
        if value is not False:
            errors.append(f"source_rollup_authority_not_false:{key}")

    for option in data.get("decision_options", []):
        if option.get("operation_authorized_now") is not False:
            errors.append(f"decision_operation_authorized:{option.get('id')}")
        if option.get("id") in {"formal_vault_work", "mainline_merge_commit_push", "use_as_action_basis"}:
            if option.get("requires_user_approval") is not True:
                errors.append(f"decision_missing_user_approval:{option.get('id')}")

    blocked = data.get("blocked_operations", {})
    for name in BLOCKED_OPERATIONS:
        if blocked.get(name) is not False:
            errors.append(f"operation_not_false:{name}")

    controls = data.get("brief_controls", {})
    for name in BRIEF_CONTROLS:
        if controls.get(name) is not True:
            errors.append(f"brief_control_not_true:{name}")

    if not set(REQUIRED_NON_CLAIMS).issubset(set(data.get("required_non_claims", []))):
        errors.append("required_non_claims_missing")

    return errors


def make_failure_cases(base: dict[str, Any]) -> dict[str, list[str]]:
    cases: dict[str, list[str]] = {}
    index = 1

    def add(name: str, mutate, expected: list[str]) -> None:
        nonlocal index
        sample = copy.deepcopy(base)
        mutate(sample)
        filename = f"{index:03d}-{name}.json"
        write_json(ROOT / "failure-cases" / filename, sample)
        cases[filename] = expected
        index += 1

    for key in ["record_kind", "slice_id", "version", "truth_boundary", "purpose", "write_scope"]:
        add(f"top-level-{key}", lambda sample, key=key: sample.__setitem__(key, "wrong"), [f"{key}_mismatch"])

    add(
        "source_snapshot-drift",
        lambda sample: sample.__setitem__("source_snapshot", {}),
        [
            "source_snapshot_mismatch",
            "source_product_status_not_pass",
            "source_product_pass_text_missing",
            "source_slice_count_mismatch",
            "product_pass_count_mismatch",
            "verification_present_count_mismatch",
            "revision_slice_count_mismatch",
        ],
    )
    for key in ["safe_summary", "decision_options", "required_separate_approvals"]:
        add(f"{key}-drift", lambda sample, key=key: sample.__setitem__(key, {}), [f"{key}_mismatch"])

    add("plain-verdict-drift", lambda sample: sample.__setitem__("plain_verdict", "enterprise_production_ready"), ["plain_verdict_mismatch"])
    add("source-product-status-not-pass", lambda sample: sample["source_snapshot"].__setitem__("source_product_status", "pending"), ["source_snapshot_mismatch", "source_product_status_not_pass"])
    add("source-product-pass-text-missing", lambda sample: sample["source_snapshot"].__setitem__("source_product_pass_text", False), ["source_snapshot_mismatch", "source_product_pass_text_missing"])
    add("source-slice-count-drift", lambda sample: sample["source_snapshot"].__setitem__("source_slice_count", 38), ["source_snapshot_mismatch", "source_slice_count_mismatch"])
    add("product-pass-count-drift", lambda sample: sample["source_snapshot"].__setitem__("product_pass_count", 38), ["source_snapshot_mismatch", "product_pass_count_mismatch"])
    add("verification-count-drift", lambda sample: sample["source_snapshot"].__setitem__("verification_present_count", 38), ["source_snapshot_mismatch", "verification_present_count_mismatch"])
    add("revision-count-drift", lambda sample: sample["source_snapshot"].__setitem__("revision_slice_count", 0), ["source_snapshot_mismatch", "revision_slice_count_mismatch"])
    add("non-pass-slices-present", lambda sample: sample["source_snapshot"].__setitem__("non_pass_slices", ["fake"]), ["source_snapshot_mismatch", "non_pass_slices_present"])
    add("missing-verification-present", lambda sample: sample["source_snapshot"].__setitem__("missing_verification_slices", ["fake"]), ["source_snapshot_mismatch", "missing_verification_slices_present"])

    for flag in ["mainline", "formal_vault", "action_basis"]:
        add(
            f"source-authority-{flag}",
            lambda sample, flag=flag: sample["source_snapshot"]["rollup_authority_flags"].__setitem__(flag, True),
            ["source_snapshot_mismatch", f"source_rollup_authority_not_false:{flag}"],
        )

    for option_id in ["continue_sandbox_hardening", "prepare_promotion_request_packet", "formal_vault_work", "mainline_merge_commit_push", "use_as_action_basis"]:
        add(
            f"decision-{option_id}-authorized-now",
            lambda sample, option_id=option_id: next(item for item in sample["decision_options"] if item["id"] == option_id).__setitem__("operation_authorized_now", True),
            ["decision_options_mismatch", f"decision_operation_authorized:{option_id}"],
        )

    for option_id in ["formal_vault_work", "mainline_merge_commit_push", "use_as_action_basis"]:
        add(
            f"decision-{option_id}-approval-false",
            lambda sample, option_id=option_id: next(item for item in sample["decision_options"] if item["id"] == option_id).__setitem__("requires_user_approval", False),
            ["decision_options_mismatch", f"decision_missing_user_approval:{option_id}"],
        )

    for op in BLOCKED_OPERATIONS:
        add(f"operation-{op}", lambda sample, op=op: sample["blocked_operations"].__setitem__(op, True), [f"operation_not_false:{op}"])

    for control in BRIEF_CONTROLS:
        add(f"control-{control}", lambda sample, control=control: sample["brief_controls"].__setitem__(control, False), [f"brief_control_not_true:{control}"])

    for non_claim in REQUIRED_NON_CLAIMS:
        safe = non_claim.replace(" ", "-")
        add(f"missing-non-claim-{safe}", lambda sample, non_claim=non_claim: sample["required_non_claims"].remove(non_claim), ["required_non_claims_missing"])

    return cases


def reset_generated() -> None:
    for directory in ["fixtures", "failure-cases", "prototype/sandbox-operator-decision-brief", "brief-packets"]:
        path = ROOT / directory
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)


def validate_failure_cases() -> dict[str, Any]:
    oracle_path = ROOT / "artifact" / "failure-case-oracle.json"
    failure_dir = ROOT / "failure-cases"
    if not oracle_path.exists():
        return {"count": 0, "actual_file_count": 0, "orphan_count": 0, "mismatches": [{"file": "failure-case-oracle.json", "expected": ["oracle_present"], "actual": ["missing_oracle"]}]}
    oracle = read_json(oracle_path).get("cases", {})
    actual_files = {path.name for path in failure_dir.glob("*.json")} if failure_dir.exists() else set()
    if not oracle:
        return {"count": 0, "actual_file_count": len(actual_files), "orphan_count": len(actual_files), "mismatches": [{"file": "failure-case-oracle.json", "expected": ["oracle_non_empty"], "actual": ["empty_oracle"]}]}
    expected_files = set(oracle)
    mismatches = []
    for extra in sorted(actual_files - expected_files):
        mismatches.append({"file": extra, "expected": ["not_present_outside_oracle"], "actual": ["orphan_failure_case_file"]})
    for name, expected in oracle.items():
        path = failure_dir / name
        if not path.exists():
            mismatches.append({"file": name, "expected": expected, "actual": ["missing_failure_case"]})
            continue
        actual = validate_brief(read_json(path))
        if sorted(actual) != sorted(expected):
            mismatches.append({"file": name, "expected": expected, "actual": actual})
    return {"count": len(oracle), "actual_file_count": len(actual_files), "orphan_count": len(actual_files - expected_files), "mismatches": mismatches}


def validate_fixtures() -> dict[str, Any]:
    details = []
    errors = []
    for path in sorted((ROOT / "fixtures").glob("*.json")):
        fixture_errors = validate_brief(read_json(path))
        details.append({"file": path.name, "errors": fixture_errors})
        if fixture_errors:
            errors.append({"file": path.name, "errors": fixture_errors})
    if not details:
        errors.append({"file": "fixtures", "errors": ["missing_positive_fixtures"]})
    return {"count": len(details), "fixtures": details, "errors": errors}


def validate_prototype() -> dict[str, Any]:
    prototype = ROOT / "prototype" / "sandbox-operator-decision-brief"
    issues: list[str] = []
    expected = default_brief()
    for item in ["index.html", "app.js", "receipt.json"]:
        if not (prototype / item).exists():
            issues.append(f"missing_prototype_file:{item}")
    if (prototype / "index.html").exists():
        html_raw = (prototype / "index.html").read_text(encoding="utf-8")
        html = html_raw.lower()
        for forbidden in ["<form", "download", "contenteditable", "<a ", "h:\\obsidian", "onclick"]:
            if forbidden in html:
                issues.append(f"prototype_forbidden:{forbidden}")
        if html.count("data-decision-option=") != len(DECISION_OPTIONS):
            issues.append("prototype_decision_option_count_mismatch")
        for value in [
            str(expected["safe_summary"]["completed_sandbox_slices"]),
            str(expected["safe_summary"]["product_grade_sandbox_slices"]),
            str(expected["safe_summary"]["verified_sandbox_slices"]),
            str(expected["safe_summary"]["revision_history_slices"]),
        ]:
            if f">{value}<" not in html_raw:
                issues.append(f"prototype_summary_value_missing:{value}")
        for phrase in ["not formal vault approval", "not action basis", "not mainline readiness"]:
            if phrase not in html:
                issues.append(f"prototype_non_claim_missing:{phrase}")
    if (prototype / "receipt.json").exists():
        receipt = read_json(prototype / "receipt.json")
        for flag in [
            "formal_vault_accessed",
            "sync_performed",
            "write_performed",
            "commit_performed",
            "push_performed",
            "promotion_performed",
            "mainline_ready",
            "action_basis_created",
            "reviewed_knowledge_created",
            "evidence_support_created",
            "auto_advanced",
        ]:
            if receipt.get(flag) is not False:
                issues.append(f"prototype_receipt_flag_not_false:{flag}")
        if not set(REQUIRED_NON_CLAIMS).issubset(set(receipt.get("non_claims", []))):
            issues.append("prototype_receipt_non_claims_missing")
    return {"prototype_path": str(prototype), "issues": issues}


def validate_required_reports(final_gate: bool = False) -> dict[str, Any]:
    required = {
        "slice-plan.md": "built_pending_review",
        "source-map.md": "built_pending_review",
        "verification.md": "local_verification_passed_pending_review",
    }
    if final_gate:
        required.update(
            {
                "reviewer-report.md": "reviewer_pass",
                "boundary-audit.md": "boundary_pass",
                "product-acceptance-report.md": "pass_product_grade",
                "next-step.md": "pass_product_grade_pending_user_next_slice_decision",
            }
        )
    statuses: dict[str, str | None] = {}
    issues: list[str] = []
    for name, expected in required.items():
        status = parse_status(ROOT / name)
        statuses[name] = status
        if status != expected:
            issues.append(f"bad_status:{name}:{status}:expected:{expected}")
    return {"statuses": statuses, "issues": issues}


def validate_all(final_gate: bool = False) -> dict[str, Any]:
    fixture = ROOT / "fixtures" / "valid-decision-brief.json"
    config_errors = validate_brief(read_json(fixture)) if fixture.exists() else ["missing_valid_fixture"]
    brief_path = ROOT / "artifact" / "decision-brief.json"
    brief_errors = validate_brief(read_json(brief_path)) if brief_path.exists() else ["missing_decision_brief"]
    fixtures = validate_fixtures()
    failures = validate_failure_cases()
    prototype = validate_prototype()
    reports = validate_required_reports(final_gate=final_gate)
    all_failures: list[str] = []
    all_failures.extend(config_errors)
    all_failures.extend([f"decision_brief_error:{item}" for item in brief_errors])
    all_failures.extend([f"fixture_error:{item['file']}" for item in fixtures["errors"]])
    all_failures.extend([f"failure_case_mismatch:{item['file']}" for item in failures["mismatches"]])
    all_failures.extend(prototype["issues"])
    all_failures.extend(reports["issues"])
    return {
        "slice_id": SLICE_ID,
        "passed": not all_failures,
        "failures": all_failures,
        "valid_config_errors": config_errors,
        "decision_brief_errors": brief_errors,
        "positive_fixtures": fixtures,
        "failure_cases": failures,
        "prototype": prototype,
        "required_reports": reports,
        "source_snapshot": source_snapshot(),
        "non_claims": REQUIRED_NON_CLAIMS,
    }
