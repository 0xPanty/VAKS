from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p2-43-sandbox-promotion-request-dry-run-sandbox"
SOURCE_SLICE_ID = "2026-06-15-p2-42-sandbox-executive-readiness-brief-sandbox"
ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[3]
SOURCE_ROOT = ROOT.parent / SOURCE_SLICE_ID
SOURCE_READINESS = SOURCE_ROOT / "artifact" / "executive-readiness-brief.json"
SOURCE_PRODUCT_REPORT = SOURCE_ROOT / "product-acceptance-report.md"

VERSION = "sandbox-promotion-request-dry-run-v1"
TRUTH_BOUNDARY = "sandbox_promotion_request_dry_run_not_approval"
PURPOSE = "sandbox-only dry-run packet for future promotion requests and approval requirements"
WRITE_SCOPE = f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"

REQUEST_ITEMS = [
    {
        "id": "mainline_merge_request",
        "label": "Mainline merge request",
        "request_intent": "Ask whether sandbox artifacts may be considered for mainline integration.",
        "requires_explicit_user_approval": True,
    },
    {
        "id": "formal_vault_write_or_sync_request",
        "label": "Formal vault write or sync request",
        "request_intent": "Ask whether any artifact may be written or synced to the formal Obsidian vault.",
        "requires_explicit_user_approval": True,
    },
    {
        "id": "template_or_tool_movement_request",
        "label": "Template or tool movement request",
        "request_intent": "Ask whether sandbox patterns may move into templates or tools.",
        "requires_explicit_user_approval": True,
    },
    {
        "id": "commit_push_request",
        "label": "Commit and push request",
        "request_intent": "Ask whether a reviewed change set may be committed or pushed.",
        "requires_explicit_user_approval": True,
    },
    {
        "id": "action_basis_request",
        "label": "Action-basis use request",
        "request_intent": "Ask whether any output may become action basis after separate evidence/review gates.",
        "requires_explicit_user_approval": True,
    },
]

PRECONDITIONS = [
    {
        "id": "explicit_user_approval_captured_separately",
        "label": "Separate explicit user approval",
        "satisfied_now": False,
        "reason": "This dry-run does not collect approval or user wording.",
    },
    {
        "id": "target_paths_named_and_scoped",
        "label": "Target paths named and scoped",
        "satisfied_now": False,
        "reason": "No actual mainline, formal-vault, template, or tool target path is selected.",
    },
    {
        "id": "promotion_diff_reviewed",
        "label": "Promotion diff reviewed",
        "satisfied_now": False,
        "reason": "No promotion diff exists in this dry-run.",
    },
    {
        "id": "formal_vault_write_plan_approved",
        "label": "Formal vault write plan approved",
        "satisfied_now": False,
        "reason": "Formal vault work remains forbidden without separate approval.",
    },
    {
        "id": "mainline_owner_review_passed",
        "label": "Mainline owner review passed",
        "satisfied_now": False,
        "reason": "Sandbox Product PASS is not mainline owner review.",
    },
    {
        "id": "post_approval_final_gate_defined",
        "label": "Post-approval final gate defined",
        "satisfied_now": False,
        "reason": "This dry-run only lists required gates; it does not run a promotion gate.",
    },
]

OPERATION_FLAGS = [
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
    "not approval",
    "not promotion",
    "not mainline merge",
    "not formal vault approval",
    "not formal vault access",
    "not Obsidian sync",
    "not commit",
    "not push",
    "not user instruction",
    "not user wording capture",
    "not action basis",
    "not reviewed knowledge",
    "not evidence support",
    "not enterprise production ready",
    "not auto advance",
]

ALLOWED_PACKET_VIEWS = [
    "promotion-request-dry-run",
    "approval-requirements-view",
    "boundary-stop-view",
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
    readiness = read_json(SOURCE_READINESS)
    product_text = SOURCE_PRODUCT_REPORT.read_text(encoding="utf-8", errors="ignore")
    return {
        "source_slice_id": SOURCE_SLICE_ID,
        "readiness_path": rel(SOURCE_READINESS),
        "readiness_sha256": sha256_file(SOURCE_READINESS),
        "product_report_path": rel(SOURCE_PRODUCT_REPORT),
        "product_report_sha256": sha256_file(SOURCE_PRODUCT_REPORT),
        "source_product_status": parse_status(SOURCE_PRODUCT_REPORT),
        "source_product_pass_text": "PASS_PRODUCT_GRADE" in product_text,
        "executive_verdict": readiness.get("executive_verdict"),
        "completed_sandbox_slices": readiness.get("scorecard", {}).get("completed_sandbox_slices"),
        "product_grade_sandbox_slices": readiness.get("scorecard", {}).get("product_grade_sandbox_slices"),
        "verified_sandbox_slices": readiness.get("scorecard", {}).get("verified_sandbox_slices"),
        "enterprise_production_ready": readiness.get("readiness_flags", {}).get("enterprise_production_ready"),
        "mainline_ready": readiness.get("readiness_flags", {}).get("mainline_ready"),
        "formal_vault_ready": readiness.get("readiness_flags", {}).get("formal_vault_ready"),
        "action_basis_ready": readiness.get("readiness_flags", {}).get("action_basis_ready"),
    }


def default_packet(view: str = "promotion-request-dry-run") -> dict[str, Any]:
    return {
        "record_kind": "sandbox_promotion_request_dry_run_packet",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
        "view": view,
        "source_snapshot": source_snapshot(),
        "request_status": "draft_request_only_not_submitted",
        "promotion_permitted_now": False,
        "approval_collected_now": False,
        "user_instruction_collected_now": False,
        "target_paths_selected": False,
        "request_items": [
            {
                **item,
                "authorized_now": False,
                "performed_now": False,
            }
            for item in REQUEST_ITEMS
        ],
        "preconditions": copy.deepcopy(PRECONDITIONS),
        "operation_performed_flags": {name: False for name in OPERATION_FLAGS},
        "required_non_claims": list(REQUIRED_NON_CLAIMS),
        "operator_summary": {
            "can_submit_request_now": False,
            "can_promote_now": False,
            "can_write_formal_vault_now": False,
            "can_commit_or_push_now": False,
            "can_move_templates_or_tools_now": False,
            "safe_next_action": "ask user for separate explicit approval before any boundary-crossing path",
        },
    }


def validate_packet(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    view = data.get("view")
    if view not in ALLOWED_PACKET_VIEWS:
        errors.append("view_mismatch")
    expected = {
        "record_kind": "sandbox_promotion_request_dry_run_packet",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            errors.append(f"{key}_mismatch")

    current = default_packet(view if view in ALLOWED_PACKET_VIEWS else "promotion-request-dry-run")
    for key in ["source_snapshot", "request_items", "preconditions", "operator_summary"]:
        if data.get(key) != current.get(key):
            errors.append(f"{key}_mismatch")

    for key in ["promotion_permitted_now", "approval_collected_now", "user_instruction_collected_now", "target_paths_selected"]:
        if data.get(key) is not False:
            errors.append(f"{key}_not_false")
    if data.get("request_status") != "draft_request_only_not_submitted":
        errors.append("request_status_mismatch")

    source = data.get("source_snapshot", {})
    if not isinstance(source, dict):
        errors.append("source_snapshot_bad_type")
        source = {}
    if source.get("source_product_status") != "pass_product_grade":
        errors.append("source_product_status_not_pass")
    if source.get("source_product_pass_text") is not True:
        errors.append("source_product_pass_text_missing")
    for flag in ["enterprise_production_ready", "mainline_ready", "formal_vault_ready", "action_basis_ready"]:
        if source.get(flag) is not False:
            errors.append(f"source_readiness_flag_not_false:{flag}")

    request_items = data.get("request_items", [])
    if not isinstance(request_items, list):
        errors.append("request_items_bad_type")
        request_items = []
    for item in request_items:
        if not isinstance(item, dict):
            errors.append("request_item_bad_type")
            continue
        if item.get("requires_explicit_user_approval") is not True:
            errors.append(f"request_missing_approval:{item.get('id')}")
        if item.get("authorized_now") is not False:
            errors.append(f"request_authorized_now:{item.get('id')}")
        if item.get("performed_now") is not False:
            errors.append(f"request_performed_now:{item.get('id')}")
        if not item.get("label") or not item.get("request_intent"):
            errors.append(f"request_human_text_missing:{item.get('id')}")

    preconditions = data.get("preconditions", [])
    if not isinstance(preconditions, list):
        errors.append("preconditions_bad_type")
        preconditions = []
    for item in preconditions:
        if not isinstance(item, dict):
            errors.append("precondition_bad_type")
            continue
        if item.get("satisfied_now") is not False:
            errors.append(f"precondition_satisfied_now:{item.get('id')}")
        if not item.get("label") or not item.get("reason"):
            errors.append(f"precondition_human_text_missing:{item.get('id')}")

    performed = data.get("operation_performed_flags", {})
    if not isinstance(performed, dict):
        errors.append("operation_performed_flags_bad_type")
        performed = {}
    if set(performed) != set(OPERATION_FLAGS):
        errors.append("operation_performed_flags_mismatch")
    for name, value in performed.items():
        if value is not False:
            errors.append(f"operation_performed_not_false:{name}")

    required_non_claims = data.get("required_non_claims", [])
    if not isinstance(required_non_claims, list):
        errors.append("required_non_claims_bad_type")
        required_non_claims = []
    if required_non_claims != REQUIRED_NON_CLAIMS:
        errors.append("required_non_claims_mismatch")

    summary = data.get("operator_summary", {})
    if not isinstance(summary, dict):
        errors.append("operator_summary_bad_type")
        summary = {}
    for key in ["can_submit_request_now", "can_promote_now", "can_write_formal_vault_now", "can_commit_or_push_now", "can_move_templates_or_tools_now"]:
        if summary.get(key) is not False:
            errors.append(f"operator_summary_flag_not_false:{key}")

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
    add("top-level-view", lambda sample: sample.__setitem__("view", "unexpected-mainline-view"), ["view_mismatch"])

    add("request_items-drift", lambda sample: sample.__setitem__("request_items", {}), ["request_items_mismatch", "request_items_bad_type"])
    add("preconditions-drift", lambda sample: sample.__setitem__("preconditions", {}), ["preconditions_mismatch", "preconditions_bad_type"])
    add(
        "source_snapshot-drift",
        lambda sample: sample.__setitem__("source_snapshot", {}),
        [
            "source_snapshot_mismatch",
            "source_product_status_not_pass",
            "source_product_pass_text_missing",
            "source_readiness_flag_not_false:enterprise_production_ready",
            "source_readiness_flag_not_false:mainline_ready",
            "source_readiness_flag_not_false:formal_vault_ready",
            "source_readiness_flag_not_false:action_basis_ready",
        ],
    )
    add(
        "operator_summary-drift",
        lambda sample: sample.__setitem__("operator_summary", {}),
        [
            "operator_summary_mismatch",
            "operator_summary_flag_not_false:can_submit_request_now",
            "operator_summary_flag_not_false:can_promote_now",
            "operator_summary_flag_not_false:can_write_formal_vault_now",
            "operator_summary_flag_not_false:can_commit_or_push_now",
            "operator_summary_flag_not_false:can_move_templates_or_tools_now",
        ],
    )
    add(
        "source_snapshot-bad-type",
        lambda sample: sample.__setitem__("source_snapshot", "bad-type"),
        [
            "source_snapshot_mismatch",
            "source_snapshot_bad_type",
            "source_product_status_not_pass",
            "source_product_pass_text_missing",
            "source_readiness_flag_not_false:enterprise_production_ready",
            "source_readiness_flag_not_false:mainline_ready",
            "source_readiness_flag_not_false:formal_vault_ready",
            "source_readiness_flag_not_false:action_basis_ready",
        ],
    )
    add("request_items-bad-type", lambda sample: sample.__setitem__("request_items", "bad-type"), ["request_items_mismatch", "request_items_bad_type"])
    add("request_item-bad-type", lambda sample: sample["request_items"].__setitem__(0, "bad-item"), ["request_items_mismatch", "request_item_bad_type"])
    add("preconditions-bad-type", lambda sample: sample.__setitem__("preconditions", "bad-type"), ["preconditions_mismatch", "preconditions_bad_type"])
    add("precondition-bad-type", lambda sample: sample["preconditions"].__setitem__(0, "bad-item"), ["preconditions_mismatch", "precondition_bad_type"])
    add(
        "operation-performed-flags-bad-type",
        lambda sample: sample.__setitem__("operation_performed_flags", "bad-type"),
        ["operation_performed_flags_bad_type", "operation_performed_flags_mismatch"],
    )
    add(
        "required-non-claims-bad-type",
        lambda sample: sample.__setitem__("required_non_claims", "bad-type"),
        ["required_non_claims_bad_type", "required_non_claims_mismatch"],
    )
    add(
        "required-non-claims-extra",
        lambda sample: sample["required_non_claims"].append("not silently expanded"),
        ["required_non_claims_mismatch"],
    )
    add(
        "operator-summary-bad-type",
        lambda sample: sample.__setitem__("operator_summary", "bad-type"),
        [
            "operator_summary_mismatch",
            "operator_summary_bad_type",
            "operator_summary_flag_not_false:can_submit_request_now",
            "operator_summary_flag_not_false:can_promote_now",
            "operator_summary_flag_not_false:can_write_formal_vault_now",
            "operator_summary_flag_not_false:can_commit_or_push_now",
            "operator_summary_flag_not_false:can_move_templates_or_tools_now",
        ],
    )

    for key in ["promotion_permitted_now", "approval_collected_now", "user_instruction_collected_now", "target_paths_selected"]:
        add(f"{key}-true", lambda sample, key=key: sample.__setitem__(key, True), [f"{key}_not_false"])
    add("request-status-submitted", lambda sample: sample.__setitem__("request_status", "submitted"), ["request_status_mismatch"])

    for flag in ["enterprise_production_ready", "mainline_ready", "formal_vault_ready", "action_basis_ready"]:
        add(
            f"source-{flag}-true",
            lambda sample, flag=flag: sample["source_snapshot"].__setitem__(flag, True),
            ["source_snapshot_mismatch", f"source_readiness_flag_not_false:{flag}"],
        )

    for item in REQUEST_ITEMS:
        rid = item["id"]
        add(
            f"request-{rid}-approval-false",
            lambda sample, rid=rid: next(row for row in sample["request_items"] if row["id"] == rid).__setitem__("requires_explicit_user_approval", False),
            ["request_items_mismatch", f"request_missing_approval:{rid}"],
        )
        add(
            f"request-{rid}-authorized",
            lambda sample, rid=rid: next(row for row in sample["request_items"] if row["id"] == rid).__setitem__("authorized_now", True),
            ["request_items_mismatch", f"request_authorized_now:{rid}"],
        )
        add(
            f"request-{rid}-performed",
            lambda sample, rid=rid: next(row for row in sample["request_items"] if row["id"] == rid).__setitem__("performed_now", True),
            ["request_items_mismatch", f"request_performed_now:{rid}"],
        )
        add(
            f"request-{rid}-missing-human-text",
            lambda sample, rid=rid: next(row for row in sample["request_items"] if row["id"] == rid).__setitem__("label", ""),
            ["request_items_mismatch", f"request_human_text_missing:{rid}"],
        )

    for item in PRECONDITIONS:
        pid = item["id"]
        add(
            f"precondition-{pid}-satisfied",
            lambda sample, pid=pid: next(row for row in sample["preconditions"] if row["id"] == pid).__setitem__("satisfied_now", True),
            ["preconditions_mismatch", f"precondition_satisfied_now:{pid}"],
        )

    for op in OPERATION_FLAGS:
        add(f"operation-performed-{op}", lambda sample, op=op: sample["operation_performed_flags"].__setitem__(op, True), [f"operation_performed_not_false:{op}"])

    for non_claim in REQUIRED_NON_CLAIMS:
        add(f"missing-non-claim-{non_claim.replace(' ', '-')}", lambda sample, non_claim=non_claim: sample["required_non_claims"].remove(non_claim), ["required_non_claims_mismatch"])

    for key in ["can_submit_request_now", "can_promote_now", "can_write_formal_vault_now", "can_commit_or_push_now", "can_move_templates_or_tools_now"]:
        add(
            f"summary-{key}-true",
            lambda sample, key=key: sample["operator_summary"].__setitem__(key, True),
            ["operator_summary_mismatch", f"operator_summary_flag_not_false:{key}"],
        )

    return cases


def reset_generated() -> None:
    for directory in ["fixtures", "failure-cases", "prototype/sandbox-promotion-request-dry-run", "request-packets"]:
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
        actual = validate_packet(read_json(path))
        if sorted(actual) != sorted(expected):
            mismatches.append({"file": name, "expected": expected, "actual": actual})
    return {"count": len(oracle), "actual_file_count": len(actual_files), "orphan_count": len(actual_files - expected_files), "mismatches": mismatches}


def validate_fixtures() -> dict[str, Any]:
    details = []
    errors = []
    for path in sorted((ROOT / "fixtures").glob("*.json")):
        fixture_errors = validate_packet(read_json(path))
        details.append({"file": path.name, "errors": fixture_errors})
        if fixture_errors:
            errors.append({"file": path.name, "errors": fixture_errors})
    if not details:
        errors.append({"file": "fixtures", "errors": ["missing_positive_fixtures"]})
    return {"count": len(details), "fixtures": details, "errors": errors}


def validate_readout() -> dict[str, Any]:
    path = ROOT / "request-packets" / "promotion-request-dry-run.md"
    issues: list[str] = []
    if not path.exists():
        return {"path": str(path), "issues": ["missing_readout"]}
    text = path.read_text(encoding="utf-8")
    for item in REQUEST_ITEMS:
        if item["label"] not in text or item["request_intent"] not in text:
            issues.append(f"readout_request_detail_missing:{item['id']}")
    for item in PRECONDITIONS:
        if item["label"] not in text or item["reason"] not in text:
            issues.append(f"readout_precondition_detail_missing:{item['id']}")
    for phrase in ["not approval", "not promotion", "not mainline merge", "not formal vault approval", "not action basis"]:
        if phrase not in text:
            issues.append(f"readout_non_claim_missing:{phrase}")
    return {"path": str(path), "issues": issues}


def validate_prototype() -> dict[str, Any]:
    prototype = ROOT / "prototype" / "sandbox-promotion-request-dry-run"
    issues: list[str] = []
    for item in ["index.html", "app.js", "receipt.json"]:
        if not (prototype / item).exists():
            issues.append(f"missing_prototype_file:{item}")
    if (prototype / "index.html").exists():
        html_raw = (prototype / "index.html").read_text(encoding="utf-8")
        html = html_raw.lower()
        for forbidden in ["<form", "download", "contenteditable", "<a ", "h:\\obsidian", "onclick"]:
            if forbidden in html:
                issues.append(f"prototype_forbidden:{forbidden}")
        if html.count("data-request-item=") != len(REQUEST_ITEMS):
            issues.append("prototype_request_count_mismatch")
        if html.count("data-precondition=") != len(PRECONDITIONS):
            issues.append("prototype_precondition_count_mismatch")
        for item in REQUEST_ITEMS:
            if item["label"] not in html_raw or item["request_intent"] not in html_raw:
                issues.append(f"prototype_request_detail_missing:{item['id']}")
        for item in PRECONDITIONS:
            if item["label"] not in html_raw or item["reason"] not in html_raw:
                issues.append(f"prototype_precondition_detail_missing:{item['id']}")
        for phrase in ["not approval", "not promotion", "not mainline merge", "not formal vault approval", "not action basis"]:
            if phrase not in html:
                issues.append(f"prototype_non_claim_missing:{phrase}")
    if (prototype / "receipt.json").exists():
        receipt = read_json(prototype / "receipt.json")
        for flag in [
            "promotion_performed",
            "approval_collected",
            "formal_vault_accessed",
            "sync_performed",
            "commit_performed",
            "push_performed",
            "mainline_merged",
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
    fixture = ROOT / "fixtures" / "valid-promotion-request-dry-run.json"
    config_errors = validate_packet(read_json(fixture)) if fixture.exists() else ["missing_valid_fixture"]
    packet_path = ROOT / "artifact" / "promotion-request-dry-run.json"
    packet_errors = validate_packet(read_json(packet_path)) if packet_path.exists() else ["missing_promotion_request_packet"]
    fixtures = validate_fixtures()
    failure_cases = validate_failure_cases()
    prototype = validate_prototype()
    readout = validate_readout()
    reports = validate_required_reports(final_gate=final_gate)
    failures: list[str] = []
    failures.extend(config_errors)
    failures.extend([f"promotion_request_error:{item}" for item in packet_errors])
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
        "promotion_request_errors": packet_errors,
        "positive_fixtures": fixtures,
        "failure_cases": failure_cases,
        "prototype": prototype,
        "readout": readout,
        "required_reports": reports,
        "source_snapshot": source_snapshot(),
        "non_claims": REQUIRED_NON_CLAIMS,
    }
