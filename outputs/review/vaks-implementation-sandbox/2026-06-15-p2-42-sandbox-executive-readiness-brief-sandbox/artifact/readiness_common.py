from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p2-42-sandbox-executive-readiness-brief-sandbox"
SOURCE_SLICE_ID = "2026-06-15-p2-41-sandbox-operator-decision-brief-sandbox"
ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[3]
SOURCE_ROOT = ROOT.parent / SOURCE_SLICE_ID
SOURCE_BRIEF = SOURCE_ROOT / "artifact" / "decision-brief.json"
SOURCE_PRODUCT_REPORT = SOURCE_ROOT / "product-acceptance-report.md"

VERSION = "sandbox-executive-readiness-brief-v1"
TRUTH_BOUNDARY = "sandbox_executive_readiness_brief_not_authority"
PURPOSE = "compact executive and operator readiness brief for sandbox product-grade status"
WRITE_SCOPE = f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"

LANDED_CAPABILITIES = [
    "receipt_and_hash_boundary",
    "validator_failure_matrix",
    "read_only_query_and_retrieval",
    "formal_vault_preflight_dry_run",
    "operator_status_and_workflow_surfaces",
    "follow_up_agent_blind_run_regression",
    "rollup_and_decision_brief_surfaces",
]

CAPABILITY_DETAILS = {
    "receipt_and_hash_boundary": {
        "label": "Receipts and hash boundaries",
        "summary": "Retrieval and operation outputs now carry inspectable receipts and source/hash boundaries.",
    },
    "validator_failure_matrix": {
        "label": "Validator failure matrix",
        "summary": "Validators are paired with negative cases so green checks cannot hide known boundary failures.",
    },
    "read_only_query_and_retrieval": {
        "label": "Read-only query and retrieval pilots",
        "summary": "Query and retrieval pilots remain inspect-only and cannot create truth, evidence, or action authority.",
    },
    "formal_vault_preflight_dry_run": {
        "label": "Formal-vault preflight dry runs",
        "summary": "Formal-vault work is represented as dry-run packets and gates, not as actual vault access.",
    },
    "operator_status_and_workflow_surfaces": {
        "label": "Operator status and workflow surfaces",
        "summary": "Operators can inspect status, next steps, approval requirements, and stop conditions.",
    },
    "follow_up_agent_blind_run_regression": {
        "label": "Follow-up-agent blind-run regression",
        "summary": "Independent agents are tested against prompts to catch authority confusion before continuation.",
    },
    "rollup_and_decision_brief_surfaces": {
        "label": "Rollup and decision brief surfaces",
        "summary": "Completed sandbox slices are summarized into readable rollups and decision briefs.",
    },
}

IMPROVEMENTS = [
    "retrieval_no_longer_counts_as_support",
    "sandbox_pass_no_longer_counts_as_mainline",
    "validator_pass_no_longer_counts_as_approval",
    "agent_decision_no_longer_counts_as_action_basis",
    "operator_can_see_pass_verification_revision_status",
    "boundary_crossing_now_requires_explicit_separate_approval",
]

IMPROVEMENT_DETAILS = {
    "retrieval_no_longer_counts_as_support": {
        "label": "Retrieval no longer counts as support",
        "summary": "Finding a source is separated from proving that it supports a point.",
    },
    "sandbox_pass_no_longer_counts_as_mainline": {
        "label": "Sandbox pass no longer counts as mainline",
        "summary": "Product-grade sandbox artifacts remain outside main architecture until separately approved.",
    },
    "validator_pass_no_longer_counts_as_approval": {
        "label": "Validator pass no longer counts as approval",
        "summary": "Automated validation is evidence for review, not reviewer or product acceptance.",
    },
    "agent_decision_no_longer_counts_as_action_basis": {
        "label": "Agent decision no longer counts as action basis",
        "summary": "Agent judgments are constrained to sandbox observations unless a separate authority exists.",
    },
    "operator_can_see_pass_verification_revision_status": {
        "label": "Operator can see pass, verification, and revision status",
        "summary": "The rollup exposes Product PASS counts, verification coverage, and revision history.",
    },
    "boundary_crossing_now_requires_explicit_separate_approval": {
        "label": "Boundary crossing requires explicit separate approval",
        "summary": "Formal vault, promotion, merge, commit, push, sync, and action-basis use remain blocked.",
    },
}

NON_PRODUCTION_GAPS = [
    "not_promoted_to_mainline",
    "not_written_to_formal_vault",
    "not_synced_to_obsidian",
    "not_deployed_or_multi_user_operationalized",
    "not_enterprise_permissioned_or_monitored",
    "not_reviewed_knowledge_or_action_basis",
]

APPROVAL_REQUIREMENTS = [
    "formal vault scan/write/sync",
    "mainline merge",
    "promotion",
    "commit",
    "push",
    "using sandbox output as action basis",
    "moving artifacts into templates or tools",
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
    "not enterprise production ready",
    "not formal vault approval",
    "not formal vault state",
    "not formal vault access",
    "not Obsidian sync",
    "not user approval",
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
    match = re.search(r"^status:\s*(.+?)\s*$", path.read_text(encoding="utf-8", errors="ignore"), re.MULTILINE)
    return match.group(1).strip() if match else None


def source_snapshot() -> dict[str, Any]:
    brief = read_json(SOURCE_BRIEF)
    product_text = SOURCE_PRODUCT_REPORT.read_text(encoding="utf-8", errors="ignore")
    summary = brief.get("safe_summary", {})
    return {
        "source_slice_id": SOURCE_SLICE_ID,
        "decision_brief_path": rel(SOURCE_BRIEF),
        "decision_brief_sha256": sha256_file(SOURCE_BRIEF),
        "product_report_path": rel(SOURCE_PRODUCT_REPORT),
        "product_report_sha256": sha256_file(SOURCE_PRODUCT_REPORT),
        "source_product_status": parse_status(SOURCE_PRODUCT_REPORT),
        "source_product_pass_text": "PASS_PRODUCT_GRADE" in product_text,
        "plain_verdict": brief.get("plain_verdict"),
        "completed_sandbox_slices": summary.get("completed_sandbox_slices"),
        "product_grade_sandbox_slices": summary.get("product_grade_sandbox_slices"),
        "verified_sandbox_slices": summary.get("verified_sandbox_slices"),
        "revision_history_slices": summary.get("revision_history_slices"),
        "enterprise_experience_status": summary.get("enterprise_experience_status"),
        "operator_next_step": brief.get("operator_next_step"),
    }


def default_readiness(view: str = "executive-readiness") -> dict[str, Any]:
    source = source_snapshot()
    return {
        "record_kind": "sandbox_executive_readiness_brief",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
        "view": view,
        "source_snapshot": source,
        "executive_verdict": "SANDBOX_PRODUCT_GRADE_OPERATOR_READY_NOT_ENTERPRISE_PRODUCTION",
        "scorecard": {
            "completed_sandbox_slices": source["completed_sandbox_slices"],
            "product_grade_sandbox_slices": source["product_grade_sandbox_slices"],
            "verified_sandbox_slices": source["verified_sandbox_slices"],
            "revision_history_slices": source["revision_history_slices"],
            "operator_experience_grade": "sandbox_product_grade",
            "enterprise_production_grade": "not_ready",
        },
        "landed_capabilities": [
            {
                "id": item,
                "label": CAPABILITY_DETAILS[item]["label"],
                "summary": CAPABILITY_DETAILS[item]["summary"],
                "status": "sandbox_product_grade",
                "authority": "sandbox_only",
            }
            for item in LANDED_CAPABILITIES
        ],
        "positive_improvements": [
            {
                "id": item,
                "label": IMPROVEMENT_DETAILS[item]["label"],
                "summary": IMPROVEMENT_DETAILS[item]["summary"],
                "direction": "positive",
                "authority": "sandbox_evidence_only",
            }
            for item in IMPROVEMENTS
        ],
        "non_production_gaps": [
            {"id": item, "status": "not_satisfied_for_production"} for item in NON_PRODUCTION_GAPS
        ],
        "approval_requirements": [
            {"id": item, "required_before_action": True, "authorized_now": False}
            for item in APPROVAL_REQUIREMENTS
        ],
        "readiness_flags": {
            "sandbox_operator_ready": True,
            "enterprise_production_ready": False,
            "mainline_ready": False,
            "formal_vault_ready": False,
            "action_basis_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
        },
        "operation_performed_flags": {name: False for name in BLOCKED_OPERATIONS},
        "required_non_claims": list(REQUIRED_NON_CLAIMS),
        "next_decision": "continue sandbox hardening or request separate approval for any boundary-crossing action",
    }


def validate_readiness(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "record_kind": "sandbox_executive_readiness_brief",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            errors.append(f"{key}_mismatch")

    current = default_readiness(data.get("view", "executive-readiness"))
    for key in [
        "source_snapshot",
        "scorecard",
        "landed_capabilities",
        "positive_improvements",
        "non_production_gaps",
        "approval_requirements",
    ]:
        if data.get(key) != current.get(key):
            errors.append(f"{key}_mismatch")

    if data.get("executive_verdict") != "SANDBOX_PRODUCT_GRADE_OPERATOR_READY_NOT_ENTERPRISE_PRODUCTION":
        errors.append("executive_verdict_mismatch")

    source = data.get("source_snapshot", {})
    if source.get("source_product_status") != "pass_product_grade":
        errors.append("source_product_status_not_pass")
    if source.get("source_product_pass_text") is not True:
        errors.append("source_product_pass_text_missing")
    if source.get("completed_sandbox_slices") != 39:
        errors.append("completed_sandbox_slices_mismatch")
    if source.get("product_grade_sandbox_slices") != 39:
        errors.append("product_grade_sandbox_slices_mismatch")
    if source.get("verified_sandbox_slices") != 39:
        errors.append("verified_sandbox_slices_mismatch")
    if source.get("revision_history_slices") != 8:
        errors.append("revision_history_slices_mismatch")
    if source.get("enterprise_experience_status") != "operator_grade_sandbox_experience_not_full_enterprise_production":
        errors.append("enterprise_experience_status_mismatch")

    flags = data.get("readiness_flags", {})
    if flags.get("sandbox_operator_ready") is not True:
        errors.append("sandbox_operator_ready_not_true")
    for flag in [
        "enterprise_production_ready",
        "mainline_ready",
        "formal_vault_ready",
        "action_basis_ready",
        "reviewed_knowledge_ready",
        "evidence_support_ready",
    ]:
        if flags.get(flag) is not False:
            errors.append(f"readiness_flag_not_false:{flag}")

    for item in data.get("approval_requirements", []):
        if item.get("required_before_action") is not True:
            errors.append(f"approval_not_required:{item.get('id')}")
        if item.get("authorized_now") is not False:
            errors.append(f"approval_authorized_now:{item.get('id')}")

    performed = data.get("operation_performed_flags", {})
    if set(performed) != set(BLOCKED_OPERATIONS):
        errors.append("operation_performed_flags_mismatch")
    for name, value in performed.items():
        if value is not False:
            errors.append(f"operation_performed_not_false:{name}")

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

    add("executive-verdict-production-claim", lambda sample: sample.__setitem__("executive_verdict", "ENTERPRISE_PRODUCTION_READY"), ["executive_verdict_mismatch"])

    add(
        "source_snapshot-drift",
        lambda sample: sample.__setitem__("source_snapshot", {}),
        [
            "source_snapshot_mismatch",
            "source_product_status_not_pass",
            "source_product_pass_text_missing",
            "completed_sandbox_slices_mismatch",
            "product_grade_sandbox_slices_mismatch",
            "verified_sandbox_slices_mismatch",
            "revision_history_slices_mismatch",
            "enterprise_experience_status_mismatch",
        ],
    )
    for key in ["scorecard", "landed_capabilities", "positive_improvements", "non_production_gaps", "approval_requirements"]:
        add(f"{key}-drift", lambda sample, key=key: sample.__setitem__(key, {}), [f"{key}_mismatch"])

    add("source-product-status-not-pass", lambda sample: sample["source_snapshot"].__setitem__("source_product_status", "pending"), ["source_snapshot_mismatch", "source_product_status_not_pass"])
    add("source-product-pass-text-missing", lambda sample: sample["source_snapshot"].__setitem__("source_product_pass_text", False), ["source_snapshot_mismatch", "source_product_pass_text_missing"])
    add("completed-count-drift", lambda sample: sample["source_snapshot"].__setitem__("completed_sandbox_slices", 38), ["source_snapshot_mismatch", "completed_sandbox_slices_mismatch"])
    add("product-count-drift", lambda sample: sample["source_snapshot"].__setitem__("product_grade_sandbox_slices", 38), ["source_snapshot_mismatch", "product_grade_sandbox_slices_mismatch"])
    add("verified-count-drift", lambda sample: sample["source_snapshot"].__setitem__("verified_sandbox_slices", 38), ["source_snapshot_mismatch", "verified_sandbox_slices_mismatch"])
    add("revision-count-drift", lambda sample: sample["source_snapshot"].__setitem__("revision_history_slices", 0), ["source_snapshot_mismatch", "revision_history_slices_mismatch"])
    add("enterprise-status-claim", lambda sample: sample["source_snapshot"].__setitem__("enterprise_experience_status", "enterprise_ready"), ["source_snapshot_mismatch", "enterprise_experience_status_mismatch"])

    add("sandbox-operator-ready-false", lambda sample: sample["readiness_flags"].__setitem__("sandbox_operator_ready", False), ["sandbox_operator_ready_not_true"])
    for flag in ["enterprise_production_ready", "mainline_ready", "formal_vault_ready", "action_basis_ready", "reviewed_knowledge_ready", "evidence_support_ready"]:
        add(f"readiness-{flag}-true", lambda sample, flag=flag: sample["readiness_flags"].__setitem__(flag, True), [f"readiness_flag_not_false:{flag}"])

    for requirement in APPROVAL_REQUIREMENTS:
        add(
            f"approval-{requirement}-not-required".replace("/", "-").replace(" ", "-"),
            lambda sample, requirement=requirement: next(item for item in sample["approval_requirements"] if item["id"] == requirement).__setitem__("required_before_action", False),
            ["approval_requirements_mismatch", f"approval_not_required:{requirement}"],
        )
        add(
            f"approval-{requirement}-authorized".replace("/", "-").replace(" ", "-"),
            lambda sample, requirement=requirement: next(item for item in sample["approval_requirements"] if item["id"] == requirement).__setitem__("authorized_now", True),
            ["approval_requirements_mismatch", f"approval_authorized_now:{requirement}"],
        )

    for operation in BLOCKED_OPERATIONS:
        add(
            f"operation-performed-{operation}",
            lambda sample, operation=operation: sample["operation_performed_flags"].__setitem__(operation, True),
            [f"operation_performed_not_false:{operation}"],
        )

    for non_claim in REQUIRED_NON_CLAIMS:
        add(f"missing-non-claim-{non_claim.replace(' ', '-')}", lambda sample, non_claim=non_claim: sample["required_non_claims"].remove(non_claim), ["required_non_claims_missing"])

    return cases


def reset_generated() -> None:
    for directory in ["fixtures", "failure-cases", "prototype/sandbox-executive-readiness-brief", "readiness-packets"]:
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
        actual = validate_readiness(read_json(path))
        if sorted(actual) != sorted(expected):
            mismatches.append({"file": name, "expected": expected, "actual": actual})
    return {"count": len(oracle), "actual_file_count": len(actual_files), "orphan_count": len(actual_files - expected_files), "mismatches": mismatches}


def validate_fixtures() -> dict[str, Any]:
    details = []
    errors = []
    for path in sorted((ROOT / "fixtures").glob("*.json")):
        fixture_errors = validate_readiness(read_json(path))
        details.append({"file": path.name, "errors": fixture_errors})
        if fixture_errors:
            errors.append({"file": path.name, "errors": fixture_errors})
    if not details:
        errors.append({"file": "fixtures", "errors": ["missing_positive_fixtures"]})
    return {"count": len(details), "fixtures": details, "errors": errors}


def validate_prototype() -> dict[str, Any]:
    prototype = ROOT / "prototype" / "sandbox-executive-readiness-brief"
    issues: list[str] = []
    expected = default_readiness()
    for item in ["index.html", "app.js", "receipt.json"]:
        if not (prototype / item).exists():
            issues.append(f"missing_prototype_file:{item}")
    if (prototype / "index.html").exists():
        html_raw = (prototype / "index.html").read_text(encoding="utf-8")
        html = html_raw.lower()
        for forbidden in ["<form", "download", "contenteditable", "<a ", "h:\\obsidian", "onclick"]:
            if forbidden in html:
                issues.append(f"prototype_forbidden:{forbidden}")
        for value in ["39", "8", "not enterprise production", "not formal vault approval", "not action basis", "not mainline readiness"]:
            if value not in html:
                issues.append(f"prototype_required_text_missing:{value}")
        for item in LANDED_CAPABILITIES:
            if f'data-capability="{item}"' not in html_raw:
                issues.append(f"prototype_capability_missing:{item}")
            if CAPABILITY_DETAILS[item]["label"] not in html_raw:
                issues.append(f"prototype_capability_label_missing:{item}")
        for item in IMPROVEMENTS:
            if f'data-improvement="{item}"' not in html_raw:
                issues.append(f"prototype_improvement_missing:{item}")
            if IMPROVEMENT_DETAILS[item]["label"] not in html_raw:
                issues.append(f"prototype_improvement_label_missing:{item}")
        if html.count("data-capability=") != len(LANDED_CAPABILITIES):
            issues.append("prototype_capability_count_mismatch")
        if html.count("data-improvement=") != len(IMPROVEMENTS):
            issues.append("prototype_improvement_count_mismatch")
        if html.count("data-gap=") != len(NON_PRODUCTION_GAPS):
            issues.append("prototype_gap_count_mismatch")
        if html.count("data-approval=") != len(APPROVAL_REQUIREMENTS):
            issues.append("prototype_approval_count_mismatch")
        if str(len(expected["landed_capabilities"])) not in html_raw:
            issues.append("prototype_landed_capability_count_missing")
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
            "enterprise_production_ready",
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


def validate_readout() -> dict[str, Any]:
    path = ROOT / "readiness-packets" / "executive-readiness-readout.md"
    issues: list[str] = []
    if not path.exists():
        return {"path": str(path), "issues": ["missing_readout"]}
    text = path.read_text(encoding="utf-8")
    for heading in ["Landed capabilities", "Positive improvements", "Non-production gap count"]:
        if heading not in text:
            issues.append(f"readout_heading_missing:{heading}")
    for item in LANDED_CAPABILITIES:
        if CAPABILITY_DETAILS[item]["label"] not in text or CAPABILITY_DETAILS[item]["summary"] not in text:
            issues.append(f"readout_capability_detail_missing:{item}")
    for item in IMPROVEMENTS:
        if IMPROVEMENT_DETAILS[item]["label"] not in text or IMPROVEMENT_DETAILS[item]["summary"] not in text:
            issues.append(f"readout_improvement_detail_missing:{item}")
    for phrase in ["not enterprise production ready", "not formal vault approval", "not action basis", "not mainline readiness"]:
        if phrase not in text:
            issues.append(f"readout_non_claim_missing:{phrase}")
    return {"path": str(path), "issues": issues}


def parse_report_status(path: Path) -> str | None:
    return parse_status(path)


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
        status = parse_report_status(ROOT / name)
        statuses[name] = status
        if status != expected:
            issues.append(f"bad_status:{name}:{status}:expected:{expected}")
    return {"statuses": statuses, "issues": issues}


def validate_all(final_gate: bool = False) -> dict[str, Any]:
    fixture = ROOT / "fixtures" / "valid-executive-readiness.json"
    config_errors = validate_readiness(read_json(fixture)) if fixture.exists() else ["missing_valid_fixture"]
    readiness_path = ROOT / "artifact" / "executive-readiness-brief.json"
    readiness_errors = validate_readiness(read_json(readiness_path)) if readiness_path.exists() else ["missing_executive_readiness_brief"]
    fixtures = validate_fixtures()
    failure_cases = validate_failure_cases()
    prototype = validate_prototype()
    readout = validate_readout()
    reports = validate_required_reports(final_gate=final_gate)
    failures: list[str] = []
    failures.extend(config_errors)
    failures.extend([f"executive_readiness_error:{item}" for item in readiness_errors])
    failures.extend([f"fixture_error:{item['file']}" for item in fixtures["errors"]])
    failures.extend([f"failure_case_mismatch:{item['file']}" for item in failure_cases["mismatches"]])
    failures.extend(prototype["issues"])
    failures.extend(readout["issues"])
    failures.extend(reports["issues"])
    return {
        "slice_id": SLICE_ID,
        "passed": not failures,
        "failures": failures,
        "valid_config_errors": config_errors,
        "executive_readiness_errors": readiness_errors,
        "positive_fixtures": fixtures,
        "failure_cases": failure_cases,
        "prototype": prototype,
        "readout": readout,
        "required_reports": reports,
        "source_snapshot": source_snapshot(),
        "non_claims": REQUIRED_NON_CLAIMS,
    }
