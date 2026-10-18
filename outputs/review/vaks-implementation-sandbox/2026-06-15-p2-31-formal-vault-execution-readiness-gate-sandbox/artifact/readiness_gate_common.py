from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p2-31-formal-vault-execution-readiness-gate-sandbox"
SOURCE_SLICE = "2026-06-15-p2-30-formal-vault-execution-dry-run-ledger-sandbox"
ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[3]

GATE_PURPOSE = (
    "Check whether a future formal-vault execution request has a complete reviewable "
    "readiness packet without collecting approval, inspecting the formal vault, "
    "emitting commands, or granting execution permission."
)

READ_ONLY_SOURCES = [
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/next-step.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/product-acceptance-report.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/verification.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/reviewer-report.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/boundary-audit.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/source-map.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/fixtures/valid-dry-run-ledger-config.json",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/prototype/formal-vault-execution-dry-run-ledger/Receipts/formal-vault-execution-dry-run-ledger-receipt.json",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/artifact/formal-vault-execution-dry-run-ledger-contract.md",
]

SOURCE_IDS = [
    "p2_30_next_step",
    "p2_30_product_acceptance",
    "p2_30_verification",
    "p2_30_reviewer_report",
    "p2_30_boundary_audit",
    "p2_30_source_map",
    "p2_30_valid_dry_run_ledger_config",
    "p2_30_dry_run_ledger_receipt",
    "p2_30_dry_run_ledger_contract",
]

REQUIRED_SOURCE_STATUSES = {
    "next-step.md": "pass_product_grade_pending_user_next_slice_decision",
    "product-acceptance-report.md": "pass_product_grade",
    "verification.md": "local_verification_passed_pending_review",
    "reviewer-report.md": "reviewer_pass",
    "boundary-audit.md": "boundary_pass",
    "source-map.md": "built_pending_review",
}

OPERATION_KEYS = [
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
    "real_base_files",
    "production_ui",
    "local_storage_write",
    "network_post",
    "actual_approval_collection",
    "actual_user_approval",
    "actual_user_decision_collection",
    "user_approval_inference",
    "real_user_text_storage",
    "real_user_text_capture",
    "write_gate_opening",
    "execution_performed",
    "snapshot_taken",
    "rollback_executed",
    "hash_before_collected",
    "hash_after_collected",
    "action_basis_creation",
    "reviewed_knowledge_creation",
    "external_notification",
    "shell_command_emitted",
    "copy_command_emitted",
    "absolute_vault_path_resolved",
    "readiness_gate_promoted_to_execution_permission",
    "readiness_gate_used_as_action_basis",
]

GATE_CONTROL_EXPECTED = {
    "sandbox_only": True,
    "read_only_gate": True,
    "dry_run_input_only": True,
    "non_executable": True,
    "operator_must_stop_before_execution": True,
    "separate_future_user_confirmation_required": True,
    "separate_future_execution_slice_required": True,
    "separate_future_formal_vault_state_check_required": True,
    "validator_is_not_reviewer": True,
    "product_acceptance_is_not_formal_vault_approval": True,
    "readiness_pass_is_not_execution_permission": True,
    "readiness_gate_is_not_action_basis": True,
    "readiness_gate_is_not_reviewed_knowledge": True,
    "readiness_gate_is_not_evidence_support": True,
    "dirty_state_blocks_execution": True,
    "execution_allowed_now": False,
    "formal_vault_access_allowed_now": False,
    "formal_vault_state_check_allowed_now": False,
    "formal_vault_write_allowed_now": False,
    "formal_vault_hash_allowed_now": False,
    "formal_vault_snapshot_allowed_now": False,
    "user_confirmation_collected_now": False,
    "actual_user_text_stored": False,
    "contains_commands": False,
    "command_export_enabled": False,
    "copy_paste_command_enabled": False,
    "absolute_vault_paths_present": False,
    "sync_commit_push_promotion_allowed": False,
    "gate_can_be_replayed": False,
    "gate_result_can_be_used_as_action_basis": False,
}

REQUEST_MODES = {
    "synthetic_reviewable_packet": "READINESS_PACKET_REVIEWABLE_NOT_EXECUTABLE",
    "synthetic_missing_future_confirmation": "BLOCKED_MISSING_FUTURE_CONFIRMATION_LEDGER_ONLY",
    "synthetic_denied_request": "BLOCKED_BY_DENIAL_LEDGER_ONLY",
}

CHECK_IDS = [
    "p2_30_product_pass_present",
    "p2_30_ledger_hash_bound",
    "source_hashes_current",
    "no_current_execution_permission",
    "future_user_confirmation",
    "future_formal_vault_state_check",
    "future_snapshot_and_rollback_plan",
    "commands_absent",
    "dirty_tree_policy",
    "final_human_go_no_go",
]

CHECK_STATUS_BY_MODE = {
    "synthetic_reviewable_packet": {
        "p2_30_product_pass_present": "PASS",
        "p2_30_ledger_hash_bound": "PASS",
        "source_hashes_current": "PASS",
        "no_current_execution_permission": "PASS",
        "future_user_confirmation": "SYNTHETIC_REFERENCE_ONLY_NOT_COLLECTED_NOW",
        "future_formal_vault_state_check": "MUST_BE_COLLECTED_IN_SEPARATE_EXECUTION_SLICE",
        "future_snapshot_and_rollback_plan": "REFERENCE_PRESENT_NOT_EXECUTED",
        "commands_absent": "PASS",
        "dirty_tree_policy": "PRE_EXISTING_BASELINE_NOT_EXECUTION_READY",
        "final_human_go_no_go": "NOT_COLLECTED_CURRENT_SLICE",
    },
    "synthetic_missing_future_confirmation": {
        "p2_30_product_pass_present": "PASS",
        "p2_30_ledger_hash_bound": "PASS",
        "source_hashes_current": "PASS",
        "no_current_execution_permission": "PASS",
        "future_user_confirmation": "MISSING",
        "future_formal_vault_state_check": "MUST_BE_COLLECTED_IN_SEPARATE_EXECUTION_SLICE",
        "future_snapshot_and_rollback_plan": "REFERENCE_PRESENT_NOT_EXECUTED",
        "commands_absent": "PASS",
        "dirty_tree_policy": "PRE_EXISTING_BASELINE_NOT_EXECUTION_READY",
        "final_human_go_no_go": "NOT_COLLECTED_CURRENT_SLICE",
    },
    "synthetic_denied_request": {
        "p2_30_product_pass_present": "PASS",
        "p2_30_ledger_hash_bound": "PASS",
        "source_hashes_current": "PASS",
        "no_current_execution_permission": "PASS",
        "future_user_confirmation": "DENIED",
        "future_formal_vault_state_check": "MUST_BE_COLLECTED_IN_SEPARATE_EXECUTION_SLICE",
        "future_snapshot_and_rollback_plan": "REFERENCE_PRESENT_NOT_EXECUTED",
        "commands_absent": "PASS",
        "dirty_tree_policy": "PRE_EXISTING_BASELINE_NOT_EXECUTION_READY",
        "final_human_go_no_go": "DENIED",
    },
}

NON_CLAIMS = {
    "not actual approval",
    "not execution readiness",
    "not execution permission",
    "not formal vault approval",
    "not formal vault state",
    "not action basis",
    "not reviewed knowledge",
    "not evidence support",
    "not an execution log",
    "not replayable",
}

TOP_LEVEL_KEYS = {
    "slice_id",
    "source_slice",
    "readiness_gate_version",
    "truth_boundary",
    "purpose",
    "gate_mode",
    "write_scope",
    "read_only_sources",
    "operations",
    "gate_controls",
    "source_inputs",
    "source_statuses",
    "p2_30_binding",
    "request_envelope",
    "readiness_checks",
    "readiness_receipt",
    "product_metrics",
    "readiness_gate_hash",
}

SOURCE_INPUT_KEYS = {"id", "source_path", "source_sha256", "content_binding"}
SOURCE_STATUS_KEYS = {"file", "expected_status", "actual_status"}
P2_30_BINDING_KEYS = {
    "source_slice",
    "product_acceptance_status",
    "reviewer_status",
    "boundary_status",
    "ledger_version",
    "ledger_hash",
    "ledger_receipt_kind",
    "ledger_receipt_hash",
    "ledger_entry_count",
    "ledger_target_count",
    "ledger_non_executable",
    "ledger_used_as_action_basis",
    "formal_vault_accessed",
    "write_performed",
    "sync_performed",
    "promotion_performed",
}
REQUEST_KEYS = {
    "request_kind",
    "request_mode",
    "request_id",
    "synthetic_only",
    "actual_user_confirmation_collected",
    "actual_user_text_stored",
    "actual_formal_vault_state_checked",
    "actual_commands_supplied",
    "requested_action_basis",
    "requested_execution_now",
    "future_execution_slice_required",
    "future_user_confirmation_required",
    "future_formal_vault_state_check_required",
    "operator_decision",
    "gate_result",
    "command",
    "absolute_target_path",
    "real_user_text",
    "non_claim",
}
CHECK_KEYS = {"check_id", "sequence", "status", "required_before_execution", "current_slice_collects", "non_claim"}
RECEIPT_KEYS = {
    "record_kind",
    "slice_id",
    "source_slice",
    "gate_result",
    "formal_vault_accessed",
    "formal_vault_state_inspected",
    "approval_collected_now",
    "actual_user_input_used",
    "real_user_text_stored",
    "execution_permission_granted",
    "execution_performed",
    "write_performed",
    "snapshot_taken",
    "hash_before_collected",
    "hash_after_collected",
    "sync_performed",
    "commit_performed",
    "push_performed",
    "promotion_performed",
    "gate_replayed",
    "gate_used_as_action_basis",
    "check_count",
    "source_count",
    "readiness_gate_hash",
    "non_claims",
}
METRIC_KEYS = {
    "required_positive_fixtures",
    "minimum_failure_cases",
    "required_readiness_checks",
    "required_source_inputs",
    "max_journey_steps",
}

PROTOTYPE_REQUIRED_FILES = [
    "00 Readiness Gate Home.md",
    "01 Gate Contract.md",
    "02 Readiness Checks.md",
    "03 Non Permission Receipt.md",
    "04 Stop Conditions.md",
    "05 Reviewer Packet.md",
    "readiness-gate-inspector.html",
    "Receipts/formal-vault-execution-readiness-gate-receipt.json",
]
PROTOTYPE_MARKDOWN_FILES = [
    "00 Readiness Gate Home.md",
    "01 Gate Contract.md",
    "02 Readiness Checks.md",
    "03 Non Permission Receipt.md",
    "04 Stop Conditions.md",
    "05 Reviewer Packet.md",
]

DANGEROUS_VALUE_PATTERNS = [
    ("copy_item", re.compile(r"(?i)\bcopy-item\b")),
    ("robocopy", re.compile(r"(?i)\brobocopy\b")),
    ("xcopy", re.compile(r"(?i)\bxcopy\b")),
    ("powershell", re.compile(r"(?i)\bpowershell\b")),
    ("pwsh", re.compile(r"(?i)\bpwsh\b")),
    ("cmd_exe", re.compile(r"(?i)\bcmd\.exe\b")),
    ("python_command", re.compile(r"(?i)\bpython(?:\.exe)?\b")),
    ("promote_py", re.compile(r"(?i)\bpromote\.py\b")),
    ("sync_flag", re.compile(r"(?i)--sync\b")),
    ("start_process", re.compile(r"(?i)\bstart-process\b")),
    ("write_vault", re.compile(r"(?i)\bwrite-vault\b")),
    ("approve_now", re.compile(r"(?i)\bapprove-now\b")),
    ("approve_execution_now", re.compile(r"(?i)\bapprove execution now\b")),
    ("execute_now", re.compile(r"(?i)\bexecute-now\b")),
    ("execute_now_phrase", re.compile(r"(?i)\bexecute now\b")),
    ("ready_to_execute", re.compile(r"(?i)\bready to execute\b")),
    ("approved_for_execution", re.compile(r"(?i)\bapproved for execution\b")),
    ("execution_permission_granted", re.compile(r"(?i)\bexecution permission granted\b")),
    ("absolute_formal_vault_path", re.compile(r"(?i)\b[A-Z]:[\\/][^\\n\\r]*Obsidian[\\/]")),
]

PROTOTYPE_SEMANTIC_DENY_PATTERNS = [
    ("execution_permission", re.compile(r"(?i)\bexecution permission granted\b")),
    ("execution_permission_yes", re.compile(r"(?i)\bexecution permission\s*[:=]\s*(yes|true|granted|allowed|ready)\b")),
    ("formal_vault_approval", re.compile(r"(?i)\bformal vault approval granted\b")),
    ("formal_vault_approval_yes", re.compile(r"(?i)\bformal vault approval\s*[:=]\s*(yes|true|granted|allowed|ready)\b")),
    ("action_basis", re.compile(r"(?i)\bis action basis\b")),
    ("action_basis_yes", re.compile(r"(?i)\baction basis\s*[:=]\s*(yes|true|granted|allowed|ready)\b")),
    ("replayable", re.compile(r"(?i)\breplayable command\b|\breplayable gate\b")),
]


def repo_path(rel_path: str) -> Path:
    return REPO_ROOT / rel_path.replace("/", "\\")


def read_text_rel(rel_path: str) -> str:
    return repo_path(rel_path).read_text(encoding="utf-8")


def read_json_path(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.replace("\r\n", "\n"), encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frontmatter_status(path: Path) -> str | None:
    if not path.exists():
        return None
    match = re.search(r"(?m)^status:\s*([A-Za-z0-9_\-]+)\s*$", path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def check_keys(label: str, obj: Any, allowed: set[str]) -> list[str]:
    if not isinstance(obj, dict):
        return [f"{label}_not_object"]
    errors = []
    actual = set(obj)
    for key in sorted(allowed - actual):
        errors.append(f"missing_key:{label}:{key}")
    for key in sorted(actual - allowed):
        errors.append(f"unknown_key:{label}:{key}")
    return errors


def scan_dangerous_values(value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            errors.extend(scan_dangerous_values(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(scan_dangerous_values(child, f"{path}[{index}]"))
    elif isinstance(value, str):
        for label, pattern in DANGEROUS_VALUE_PATTERNS:
            if pattern.search(value):
                errors.append(f"dangerous_value:{path}:{label}")
    return errors


def scan_prototype_text(rel_path: str, text: str) -> list[str]:
    errors = []
    for label, pattern in DANGEROUS_VALUE_PATTERNS:
        if pattern.search(text):
            errors.append(f"prototype_text_dangerous:{rel_path}:{label}")
    for label, pattern in PROTOTYPE_SEMANTIC_DENY_PATTERNS:
        if pattern.search(text):
            errors.append(f"prototype_text_authority_confusion:{rel_path}:{label}")
    return errors


def expected_source_inputs() -> list[dict[str, str]]:
    items = []
    for source_id, rel_path in zip(SOURCE_IDS, READ_ONLY_SOURCES):
        path = repo_path(rel_path)
        items.append(
            {
                "id": source_id,
                "source_path": rel_path,
                "source_sha256": file_sha256(path),
                "content_binding": "exact_source_sha256",
            }
        )
    return items


def expected_source_statuses() -> list[dict[str, str | None]]:
    statuses = []
    base = repo_path(f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}")
    for file_name, expected in REQUIRED_SOURCE_STATUSES.items():
        statuses.append(
            {
                "file": file_name,
                "expected_status": expected,
                "actual_status": frontmatter_status(base / file_name),
            }
        )
    return statuses


def load_prev_config() -> dict[str, Any]:
    return read_json_path(repo_path(f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/fixtures/valid-dry-run-ledger-config.json"))


def load_prev_receipt() -> dict[str, Any]:
    return read_json_path(
        repo_path(
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/prototype/"
            "formal-vault-execution-dry-run-ledger/Receipts/formal-vault-execution-dry-run-ledger-receipt.json"
        )
    )


def expected_p2_30_binding() -> dict[str, Any]:
    prev_config = load_prev_config()
    prev_receipt = load_prev_receipt()
    base = repo_path(f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}")
    return {
        "source_slice": SOURCE_SLICE,
        "product_acceptance_status": frontmatter_status(base / "product-acceptance-report.md"),
        "reviewer_status": frontmatter_status(base / "reviewer-report.md"),
        "boundary_status": frontmatter_status(base / "boundary-audit.md"),
        "ledger_version": prev_config.get("dry_run_ledger_version"),
        "ledger_hash": prev_config.get("dry_run_ledger_hash"),
        "ledger_receipt_kind": prev_receipt.get("record_kind"),
        "ledger_receipt_hash": prev_receipt.get("ledger_hash"),
        "ledger_entry_count": prev_receipt.get("entry_count"),
        "ledger_target_count": prev_receipt.get("target_count"),
        "ledger_non_executable": prev_config.get("ledger_controls", {}).get("non_executable"),
        "ledger_used_as_action_basis": prev_receipt.get("ledger_used_as_action_basis"),
        "formal_vault_accessed": prev_receipt.get("formal_vault_accessed"),
        "write_performed": prev_receipt.get("write_performed"),
        "sync_performed": prev_receipt.get("sync_performed"),
        "promotion_performed": prev_receipt.get("promotion_performed"),
    }


def expected_gate_hash(config: dict[str, Any]) -> str:
    clone = copy.deepcopy(config)
    clone.pop("readiness_gate_hash", None)
    if isinstance(clone.get("readiness_receipt"), dict):
        clone["readiness_receipt"].pop("readiness_gate_hash", None)
    return canonical_hash(clone)


def current_valid_config() -> dict[str, Any] | None:
    path = ROOT / "fixtures" / "valid-reviewable-readiness-gate-config.json"
    if not path.exists():
        return None
    return read_json_path(path)


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(config, dict):
        return ["config_not_object"]
    errors.extend(check_keys("config", config, TOP_LEVEL_KEYS))
    errors.extend(scan_dangerous_values(config))

    if config.get("slice_id") != SLICE_ID:
        errors.append("slice_id_mismatch")
    if config.get("source_slice") != SOURCE_SLICE:
        errors.append("source_slice_mismatch")
    if config.get("readiness_gate_version") != "p2-31-formal-vault-execution-readiness-gate-v1":
        errors.append("readiness_gate_version_mismatch")
    if config.get("truth_boundary") != "sandbox_only_readiness_gate_not_execution_permission":
        errors.append("truth_boundary_mismatch")
    if config.get("purpose") != GATE_PURPOSE:
        errors.append("purpose_mismatch")
    if config.get("gate_mode") != "future_execution_readiness_gate_review_only":
        errors.append("gate_mode_mismatch")
    if config.get("write_scope") != [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"]:
        errors.append("write_scope_mismatch")
    if config.get("read_only_sources") != READ_ONLY_SOURCES:
        errors.append("read_only_sources_mismatch")

    operations = config.get("operations")
    if not isinstance(operations, dict):
        errors.append("operations_missing")
        operations = {}
    errors.extend(check_keys("operations", operations, set(OPERATION_KEYS)))
    for key in OPERATION_KEYS:
        if operations.get(key) is not False:
            errors.append(f"operation_not_false:{key}")

    controls = config.get("gate_controls")
    if not isinstance(controls, dict):
        errors.append("gate_controls_missing")
        controls = {}
    errors.extend(check_keys("gate_controls", controls, set(GATE_CONTROL_EXPECTED)))
    for key, expected in GATE_CONTROL_EXPECTED.items():
        if controls.get(key) is not expected:
            errors.append(f"gate_control_mismatch:{key}")

    expected_inputs = expected_source_inputs()
    source_inputs = config.get("source_inputs")
    if source_inputs != expected_inputs:
        errors.append("source_inputs_mismatch")
    if isinstance(source_inputs, list):
        for item in source_inputs:
            errors.extend(check_keys(f"source_inputs[{item.get('id', 'unknown')}]", item, SOURCE_INPUT_KEYS))
    else:
        errors.append("source_inputs_not_list")

    expected_statuses = expected_source_statuses()
    source_statuses = config.get("source_statuses")
    if source_statuses != expected_statuses:
        errors.append("source_statuses_mismatch")
    if isinstance(source_statuses, list):
        for item in source_statuses:
            errors.extend(check_keys(f"source_statuses[{item.get('file', 'unknown')}]", item, SOURCE_STATUS_KEYS))
            if item.get("expected_status") != item.get("actual_status"):
                errors.append(f"source_status_not_met:{item.get('file')}")
    else:
        errors.append("source_statuses_not_list")

    binding = config.get("p2_30_binding")
    expected_binding = expected_p2_30_binding()
    if binding != expected_binding:
        errors.append("p2_30_binding_mismatch")
    if isinstance(binding, dict):
        errors.extend(check_keys("p2_30_binding", binding, P2_30_BINDING_KEYS))
        for false_key in ["ledger_used_as_action_basis", "formal_vault_accessed", "write_performed", "sync_performed", "promotion_performed"]:
            if binding.get(false_key) is not False:
                errors.append(f"p2_30_binding_flag_not_false:{false_key}")
        if binding.get("product_acceptance_status") != "pass_product_grade":
            errors.append("p2_30_product_acceptance_not_pass")
        if binding.get("reviewer_status") != "reviewer_pass":
            errors.append("p2_30_reviewer_not_pass")
        if binding.get("boundary_status") != "boundary_pass":
            errors.append("p2_30_boundary_not_pass")
        if binding.get("ledger_hash") != binding.get("ledger_receipt_hash"):
            errors.append("p2_30_ledger_hash_receipt_mismatch")
    else:
        errors.append("p2_30_binding_not_object")

    request = config.get("request_envelope")
    if not isinstance(request, dict):
        errors.append("request_envelope_missing")
        request = {}
    errors.extend(check_keys("request_envelope", request, REQUEST_KEYS))
    mode = request.get("request_mode")
    expected_result = REQUEST_MODES.get(mode)
    if request.get("request_kind") != "synthetic_future_formal_vault_execution_request":
        errors.append("request_kind_mismatch")
    if mode not in REQUEST_MODES:
        errors.append("request_mode_not_allowed")
    if request.get("request_id") != f"{SLICE_ID}:{mode}":
        errors.append("request_id_mismatch")
    if request.get("gate_result") != expected_result:
        errors.append("request_gate_result_mismatch")
    for false_key in [
        "actual_user_confirmation_collected",
        "actual_user_text_stored",
        "actual_formal_vault_state_checked",
        "actual_commands_supplied",
        "requested_action_basis",
        "requested_execution_now",
    ]:
        if request.get(false_key) is not False:
            errors.append(f"request_flag_not_false:{false_key}")
    for true_key in ["synthetic_only", "future_execution_slice_required", "future_user_confirmation_required", "future_formal_vault_state_check_required"]:
        if request.get(true_key) is not True:
            errors.append(f"request_flag_not_true:{true_key}")
    for empty_key in ["command", "absolute_target_path", "real_user_text"]:
        if request.get(empty_key) not in ("", None):
            errors.append(f"request_forbidden_field_nonempty:{empty_key}")
    if request.get("non_claim") != "readiness_gate_request_is_synthetic_only":
        errors.append("request_non_claim_mismatch")
    if mode == "synthetic_denied_request" and request.get("operator_decision") != "deny":
        errors.append("request_denial_decision_mismatch")
    if mode == "synthetic_missing_future_confirmation" and request.get("operator_decision") != "missing_confirmation":
        errors.append("request_missing_confirmation_decision_mismatch")
    if mode == "synthetic_reviewable_packet" and request.get("operator_decision") != "review_packet_only":
        errors.append("request_review_packet_decision_mismatch")

    checks = config.get("readiness_checks")
    expected_status = CHECK_STATUS_BY_MODE.get(mode, {})
    if not isinstance(checks, list):
        errors.append("readiness_checks_missing")
        checks = []
    check_ids = [item.get("check_id") for item in checks if isinstance(item, dict)]
    if check_ids != CHECK_IDS:
        errors.append("readiness_check_ids_mismatch")
    for index, check in enumerate(checks, start=1):
        if not isinstance(check, dict):
            errors.append("readiness_check_not_object")
            continue
        check_id = check.get("check_id", "unknown")
        errors.extend(check_keys(f"readiness_checks[{check_id}]", check, CHECK_KEYS))
        if check.get("sequence") != index:
            errors.append(f"readiness_check_sequence_mismatch:{check_id}")
        if check.get("status") != expected_status.get(check_id):
            errors.append(f"readiness_check_status_mismatch:{check_id}")
        if check.get("required_before_execution") is not True:
            errors.append(f"readiness_check_required_before_execution_not_true:{check_id}")
        if check.get("current_slice_collects") is not False:
            errors.append(f"readiness_check_current_slice_collects_not_false:{check_id}")
        if check.get("non_claim") != "check_is_readiness_input_not_permission":
            errors.append(f"readiness_check_non_claim_mismatch:{check_id}")

    receipt = config.get("readiness_receipt")
    if not isinstance(receipt, dict):
        errors.append("readiness_receipt_missing")
        receipt = {}
    errors.extend(check_keys("readiness_receipt", receipt, RECEIPT_KEYS))
    if receipt.get("record_kind") != "sandbox_formal_vault_execution_readiness_gate_receipt":
        errors.append("receipt_record_kind_mismatch")
    if receipt.get("slice_id") != SLICE_ID:
        errors.append("receipt_slice_id_mismatch")
    if receipt.get("source_slice") != SOURCE_SLICE:
        errors.append("receipt_source_slice_mismatch")
    if receipt.get("gate_result") != expected_result:
        errors.append("receipt_gate_result_mismatch")
    if receipt.get("check_count") != len(CHECK_IDS):
        errors.append("receipt_check_count_mismatch")
    if receipt.get("source_count") != len(READ_ONLY_SOURCES):
        errors.append("receipt_source_count_mismatch")
    if receipt.get("readiness_gate_hash") != expected_gate_hash(config):
        errors.append("receipt_readiness_gate_hash_mismatch")
    for false_key in [
        "formal_vault_accessed",
        "formal_vault_state_inspected",
        "approval_collected_now",
        "actual_user_input_used",
        "real_user_text_stored",
        "execution_permission_granted",
        "execution_performed",
        "write_performed",
        "snapshot_taken",
        "hash_before_collected",
        "hash_after_collected",
        "sync_performed",
        "commit_performed",
        "push_performed",
        "promotion_performed",
        "gate_replayed",
        "gate_used_as_action_basis",
    ]:
        if receipt.get(false_key) is not False:
            errors.append(f"receipt_flag_not_false:{false_key}")
    if not NON_CLAIMS.issubset(set(receipt.get("non_claims", []))):
        errors.append("receipt_non_claims_missing")

    metrics = config.get("product_metrics")
    if not isinstance(metrics, dict):
        errors.append("product_metrics_missing")
        metrics = {}
    errors.extend(check_keys("product_metrics", metrics, METRIC_KEYS))
    if metrics.get("required_positive_fixtures") != 3:
        errors.append("metric_positive_fixtures_mismatch")
    if metrics.get("minimum_failure_cases", 0) < 100:
        errors.append("metric_failure_case_floor_too_low")
    if metrics.get("required_readiness_checks") != len(CHECK_IDS):
        errors.append("metric_readiness_checks_mismatch")
    if metrics.get("required_source_inputs") != len(READ_ONLY_SOURCES):
        errors.append("metric_source_inputs_mismatch")
    if metrics.get("max_journey_steps") != 3:
        errors.append("metric_max_journey_steps_mismatch")

    if config.get("readiness_gate_hash") != expected_gate_hash(config):
        errors.append("readiness_gate_hash_mismatch")
    return sorted(set(errors))


def validate_prototype_receipt(receipt: Any, config: dict[str, Any] | None = None) -> list[str]:
    errors = []
    if not isinstance(receipt, dict):
        return ["prototype_receipt_not_object"]
    errors.extend(check_keys("prototype_receipt", receipt, RECEIPT_KEYS))
    errors.extend(scan_dangerous_values(receipt, "$.prototype_receipt"))
    expected_config = config or current_valid_config()
    expected_hash = expected_config.get("readiness_gate_hash") if expected_config else None
    expected_result = expected_config.get("request_envelope", {}).get("gate_result") if expected_config else None
    if receipt.get("record_kind") != "sandbox_formal_vault_execution_readiness_gate_receipt":
        errors.append("prototype_receipt_record_kind_mismatch")
    if receipt.get("slice_id") != SLICE_ID:
        errors.append("prototype_receipt_slice_id_mismatch")
    if receipt.get("source_slice") != SOURCE_SLICE:
        errors.append("prototype_receipt_source_slice_mismatch")
    if expected_result and receipt.get("gate_result") != expected_result:
        errors.append("prototype_receipt_gate_result_mismatch")
    if receipt.get("check_count") != len(CHECK_IDS):
        errors.append("prototype_receipt_check_count_mismatch")
    if receipt.get("source_count") != len(READ_ONLY_SOURCES):
        errors.append("prototype_receipt_source_count_mismatch")
    if expected_hash and receipt.get("readiness_gate_hash") != expected_hash:
        errors.append("prototype_receipt_gate_hash_mismatch")
    for false_key in [
        "formal_vault_accessed",
        "formal_vault_state_inspected",
        "approval_collected_now",
        "actual_user_input_used",
        "real_user_text_stored",
        "execution_permission_granted",
        "execution_performed",
        "write_performed",
        "snapshot_taken",
        "hash_before_collected",
        "hash_after_collected",
        "sync_performed",
        "commit_performed",
        "push_performed",
        "promotion_performed",
        "gate_replayed",
        "gate_used_as_action_basis",
    ]:
        if receipt.get(false_key) is not False:
            errors.append(f"prototype_receipt_flag_not_false:{false_key}")
    if not NON_CLAIMS.issubset(set(receipt.get("non_claims", []))):
        errors.append("prototype_receipt_non_claims_missing")
    return sorted(set(errors))


def inspect_prototype() -> dict[str, Any]:
    prototype_path = ROOT / "prototype" / "formal-vault-execution-readiness-gate"
    receipt_path = prototype_path / "Receipts" / "formal-vault-execution-readiness-gate-receipt.json"
    html_path = prototype_path / "readiness-gate-inspector.html"
    issues = []
    for rel in PROTOTYPE_REQUIRED_FILES:
        if not (prototype_path / rel).exists():
            issues.append(f"missing_prototype_file:{rel}")
    for rel in PROTOTYPE_MARKDOWN_FILES:
        path = prototype_path / rel
        if path.exists():
            issues.extend(scan_prototype_text(rel, path.read_text(encoding="utf-8")))
    receipt = {}
    if receipt_path.exists():
        receipt = read_json_path(receipt_path)
        issues.extend(validate_prototype_receipt(receipt))
    else:
        issues.append("missing_prototype_receipt")
    html_summary = {}
    if html_path.exists():
        html = html_path.read_text(encoding="utf-8")
        issues.extend(scan_prototype_text("readiness-gate-inspector.html", html))
        lower = html.lower()
        forbidden_bits = [
            "<form",
            "download=",
            "contenteditable",
            "localstorage",
            "sessionstorage",
            "fetch(",
            "xmlhttprequest",
            "navigator.sendbeacon",
            "window.open",
            "powershell",
            "robocopy",
            "copy-item",
            "write-vault",
            "sync-now",
            "approve-now",
            "execute-now",
        ]
        for bit in forbidden_bits:
            if bit in lower:
                issues.append(f"html_forbidden_token:{bit}")
        required_attrs = [
            'data-sandbox-only="true"',
            'data-readiness-only="true"',
            'data-non-executable="true"',
            'data-no-formal-vault-access="true"',
            'data-no-write="true"',
            'data-no-sync="true"',
            'data-no-authority="true"',
            'data-no-permission="true"',
        ]
        for attr in required_attrs:
            if attr not in html:
                issues.append(f"html_missing_attr:{attr}")
        buttons = re.findall(r"<button[^>]*data-filter=\"([^\"]+)\"[^>]*>([^<]+)</button>", html)
        html_summary = {
            "sandbox_only": 'data-sandbox-only="true"' in html,
            "readiness_only": 'data-readiness-only="true"' in html,
            "non_executable": 'data-non-executable="true"' in html,
            "no_formal_vault_access": 'data-no-formal-vault-access="true"' in html,
            "no_write": 'data-no-write="true"' in html,
            "no_sync": 'data-no-sync="true"' in html,
            "no_authority": 'data-no-authority="true"' in html,
            "no_permission": 'data-no-permission="true"' in html,
            "forms": lower.count("<form"),
            "downloads": lower.count("download="),
            "contenteditable": lower.count("contenteditable"),
            "anchors": lower.count("<a "),
            "buttons": [button[0] for button in buttons],
            "button_texts": [button[1].strip() for button in buttons],
        }
    else:
        issues.append("missing_inspector_html")
    journeys = {
        "contract_review": {"links_verified": (prototype_path / "01 Gate Contract.md").exists(), "max_links": 2},
        "check_review": {"links_verified": (prototype_path / "02 Readiness Checks.md").exists(), "max_links": 2},
        "receipt_review": {"links_verified": (prototype_path / "03 Non Permission Receipt.md").exists(), "max_links": 2},
        "stop_review": {"links_verified": (prototype_path / "04 Stop Conditions.md").exists(), "max_links": 2},
        "inspector_review": {"links_verified": html_path.exists(), "max_links": 2, "html_allowlist_ok": not issues},
    }
    return {"prototype_path": str(prototype_path), "issues": sorted(set(issues)), "receipt": receipt, "html": html_summary, "actual_journeys": journeys}


def validate_prototype_tamper(tamper: dict[str, Any]) -> list[str]:
    if tamper.get("kind") == "markdown_replace":
        return scan_prototype_text(tamper.get("file", "unknown.md"), tamper.get("content", ""))
    receipt_path = ROOT / "prototype" / "formal-vault-execution-readiness-gate" / "Receipts" / "formal-vault-execution-readiness-gate-receipt.json"
    if receipt_path.exists():
        base_receipt = read_json_path(receipt_path)
    else:
        config = current_valid_config()
        base_receipt = copy.deepcopy(config.get("readiness_receipt", {})) if config else {}
    if tamper.get("kind") == "receipt_update":
        receipt = copy.deepcopy(base_receipt)
        receipt.update(tamper.get("updates", {}))
        return validate_prototype_receipt(receipt)
    if tamper.get("kind") == "receipt_replace_non_claims":
        receipt = copy.deepcopy(base_receipt)
        receipt["non_claims"] = tamper.get("non_claims", [])
        return validate_prototype_receipt(receipt)
    return ["unknown_prototype_tamper_kind"]


def load_failure_oracle() -> dict[str, Any]:
    return read_json_path(ROOT / "artifact" / "failure-case-oracle.json")


def validate_failure_cases() -> dict[str, Any]:
    oracle = load_failure_oracle()
    expected_cases = oracle.get("cases", {})
    failure_dir = ROOT / "failure-cases"
    actual_files = sorted(path.name for path in failure_dir.glob("*.json"))
    mismatches = []
    if set(actual_files) != set(expected_cases):
        for missing in sorted(set(expected_cases) - set(actual_files)):
            mismatches.append(f"missing_failure_case_file:{missing}")
        for extra in sorted(set(actual_files) - set(expected_cases)):
            mismatches.append(f"extra_failure_case_file:{extra}")
    for file_name in actual_files:
        payload = read_json_path(failure_dir / file_name)
        expected_errors = sorted(payload.get("expected_errors", []))
        oracle_errors = sorted(expected_cases.get(file_name, []))
        if "config" in payload:
            actual_errors = sorted(validate_config(payload.get("config", {})))
        elif "prototype_tamper" in payload:
            actual_errors = sorted(validate_prototype_tamper(payload.get("prototype_tamper", {})))
        else:
            actual_errors = ["failure_case_missing_payload"]
        if expected_errors != oracle_errors:
            mismatches.append(f"case_oracle_disagreement:{file_name}")
        if actual_errors != oracle_errors:
            mismatches.append(f"failure_case_mismatch:{file_name}:actual={actual_errors}:expected={oracle_errors}")
        if not actual_errors:
            mismatches.append(f"failure_case_did_not_fail:{file_name}")
    return {"count": len(actual_files), "mismatches": mismatches}


def _rehash_for_probe(config: dict[str, Any]) -> dict[str, Any]:
    config["readiness_gate_hash"] = ""
    if isinstance(config.get("readiness_receipt"), dict):
        config["readiness_receipt"]["readiness_gate_hash"] = ""
    gate_hash = expected_gate_hash(config)
    config["readiness_gate_hash"] = gate_hash
    if isinstance(config.get("readiness_receipt"), dict):
        config["readiness_receipt"]["readiness_gate_hash"] = gate_hash
    return config


def run_manual_negative_probes() -> dict[str, Any]:
    config = current_valid_config()
    if not config:
        return {"count": 0, "mismatches": ["missing_current_valid_config"], "probes": []}

    probes: list[dict[str, Any]] = []

    def add_config_probe(name: str, request_id: str, expected: list[str]) -> None:
        candidate = copy.deepcopy(config)
        candidate["request_envelope"]["request_id"] = request_id
        _rehash_for_probe(candidate)
        actual = validate_config(candidate)
        probes.append({"name": name, "expected_errors": expected, "actual_errors": actual})

    add_config_probe(
        "manual-request-id-real-user-text",
        "user said approve execution",
        ["request_id_mismatch"],
    )
    add_config_probe(
        "manual-request-id-command",
        "python tools/promote.py --sync",
        [
            "request_id_mismatch",
            "dangerous_value:$.request_envelope.request_id:python_command",
            "dangerous_value:$.request_envelope.request_id:promote_py",
            "dangerous_value:$.request_envelope.request_id:sync_flag",
        ],
    )
    add_config_probe(
        "manual-request-id-approval-now",
        "I approve execution now",
        [
            "request_id_mismatch",
            "dangerous_value:$.request_envelope.request_id:approve_execution_now",
        ],
    )
    add_config_probe(
        "manual-request-id-execute-now",
        "execute now",
        [
            "request_id_mismatch",
            "dangerous_value:$.request_envelope.request_id:execute_now_phrase",
        ],
    )

    prototype_probes = [
        (
            "manual-prototype-execution-permission-yes",
            {"kind": "markdown_replace", "file": "02 Readiness Checks.md", "content": "execution permission: yes"},
            ["prototype_text_authority_confusion:02 Readiness Checks.md:execution_permission_yes"],
        ),
        (
            "manual-prototype-formal-vault-approval-yes",
            {"kind": "markdown_replace", "file": "03 Non Permission Receipt.md", "content": "formal vault approval: yes"},
            ["prototype_text_authority_confusion:03 Non Permission Receipt.md:formal_vault_approval_yes"],
        ),
        (
            "manual-prototype-action-basis-yes",
            {"kind": "markdown_replace", "file": "05 Reviewer Packet.md", "content": "action basis: yes"},
            ["prototype_text_authority_confusion:05 Reviewer Packet.md:action_basis_yes"],
        ),
    ]
    for name, tamper, expected in prototype_probes:
        probes.append({"name": name, "expected_errors": expected, "actual_errors": validate_prototype_tamper(tamper)})

    mismatches = []
    for probe in probes:
        actual = set(probe["actual_errors"])
        expected = set(probe["expected_errors"])
        if not expected.issubset(actual):
            mismatches.append(f"manual_probe_mismatch:{probe['name']}:actual={probe['actual_errors']}:expected_subset={probe['expected_errors']}")
    return {"count": len(probes), "mismatches": mismatches, "probes": probes}


REQUIRED_REPORT_STATUSES = {
    "slice-plan.md": "built_pending_review",
    "source-map.md": "built_pending_review",
    "verification.md": "local_verification_passed_pending_review",
    "reviewer-report.md": "reviewer_pass",
    "boundary-audit.md": "boundary_pass",
    "product-acceptance-report.md": "pass_product_grade",
    "next-step.md": "pass_product_grade_pending_user_next_slice_decision",
}
PRE_FINAL_REPORT_STATUSES = {
    "slice-plan.md": "built_pending_review",
    "source-map.md": "built_pending_review",
    "verification.md": "local_verification_passed_pending_review",
}


def required_report_statuses(final_gate: bool) -> dict[str, str]:
    return REQUIRED_REPORT_STATUSES if final_gate else PRE_FINAL_REPORT_STATUSES


def check_required_reports(final_gate: bool) -> dict[str, Any]:
    statuses = {}
    issues = []
    for name, expected in required_report_statuses(final_gate).items():
        actual = frontmatter_status(ROOT / name)
        statuses[name] = actual
        if actual != expected:
            if final_gate:
                issues.append(f"final_gate_bad_status:{name}:{actual}:expected:{expected}")
            elif actual is None:
                issues.append(f"missing_report:{name}")
    return {"statuses": statuses, "issues": issues}
