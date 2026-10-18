from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p2-32-formal-vault-execution-request-packet-sandbox"
SOURCE_SLICE = "2026-06-15-p2-31-formal-vault-execution-readiness-gate-sandbox"
ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[3]

PACKET_PURPOSE = (
    "Define a synthetic future formal-vault execution request packet that can be "
    "screened by the P2-31 readiness gate without collecting real approval, "
    "storing real user text, resolving formal-vault paths, or emitting commands."
)

READ_ONLY_SOURCES = [
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/next-step.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/product-acceptance-report.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/verification.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/reviewer-report.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/boundary-audit.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/source-map.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/fixtures/valid-reviewable-readiness-gate-config.json",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/prototype/formal-vault-execution-readiness-gate/Receipts/formal-vault-execution-readiness-gate-receipt.json",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/artifact/formal-vault-execution-readiness-gate-contract.md",
]

SOURCE_IDS = [
    "p2_31_next_step",
    "p2_31_product_acceptance",
    "p2_31_verification",
    "p2_31_reviewer_report",
    "p2_31_boundary_audit",
    "p2_31_source_map",
    "p2_31_valid_readiness_gate_config",
    "p2_31_readiness_gate_receipt",
    "p2_31_readiness_gate_contract",
]

REQUIRED_SOURCE_STATUSES = {
    "next-step.md": "pass_product_grade_pending_user_next_slice_decision",
    "product-acceptance-report.md": "pass_product_grade",
    "verification.md": "local_verification_passed_pending_review",
    "reviewer-report.md": "reviewer_pass",
    "boundary-audit.md": "boundary_pass",
    "source-map.md": "built_pending_review",
}

PACKET_MODES = {
    "synthetic_reviewable_request_packet": "REQUEST_PACKET_REVIEWABLE_NOT_APPROVAL",
    "synthetic_missing_confirmation_packet": "REQUEST_PACKET_BLOCKED_MISSING_FUTURE_CONFIRMATION",
    "synthetic_denied_request_packet": "REQUEST_PACKET_BLOCKED_BY_DENIAL",
}

TARGET_GATE_REQUEST_MODES = {
    "synthetic_reviewable_request_packet": "synthetic_reviewable_packet",
    "synthetic_missing_confirmation_packet": "synthetic_missing_future_confirmation",
    "synthetic_denied_request_packet": "synthetic_denied_request",
}

TARGET_GATE_RESULTS = {
    "synthetic_reviewable_request_packet": "READINESS_PACKET_REVIEWABLE_NOT_EXECUTABLE",
    "synthetic_missing_confirmation_packet": "BLOCKED_MISSING_FUTURE_CONFIRMATION_LEDGER_ONLY",
    "synthetic_denied_request_packet": "BLOCKED_BY_DENIAL_LEDGER_ONLY",
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
    "request_packet_promoted_to_execution_permission",
    "request_packet_used_as_action_basis",
]

PACKET_CONTROL_EXPECTED = {
    "sandbox_only": True,
    "synthetic_packet_only": True,
    "readiness_gate_screenable": True,
    "non_executable": True,
    "no_real_user_text": True,
    "no_actual_approval": True,
    "no_formal_vault_paths": True,
    "no_commands": True,
    "operator_must_stop_before_execution": True,
    "separate_future_user_confirmation_required": True,
    "separate_future_execution_slice_required": True,
    "separate_future_formal_vault_state_check_required": True,
    "product_acceptance_is_not_formal_vault_approval": True,
    "request_packet_is_not_execution_permission": True,
    "request_packet_is_not_action_basis": True,
    "request_packet_is_not_reviewed_knowledge": True,
    "request_packet_is_not_evidence_support": True,
    "execution_allowed_now": False,
    "formal_vault_access_allowed_now": False,
    "formal_vault_write_allowed_now": False,
    "formal_vault_hash_allowed_now": False,
    "formal_vault_snapshot_allowed_now": False,
    "user_confirmation_collected_now": False,
    "actual_user_text_stored": False,
    "contains_commands": False,
    "absolute_vault_paths_present": False,
    "sync_commit_push_promotion_allowed": False,
    "packet_can_be_replayed": False,
    "packet_result_can_be_used_as_action_basis": False,
}

PACKET_FIELD_IDS = [
    "packet_id",
    "packet_mode",
    "synthetic_confirmation_reference",
    "operator_decision_reference",
    "scope_reference",
    "target_manifest_reference",
    "readiness_gate_projection",
    "non_claims",
]

NON_CLAIMS = {
    "not actual approval",
    "not user instruction",
    "not real user text",
    "not execution permission",
    "not execution readiness",
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
    "request_packet_version",
    "truth_boundary",
    "purpose",
    "packet_mode",
    "write_scope",
    "read_only_sources",
    "operations",
    "packet_controls",
    "source_inputs",
    "source_statuses",
    "p2_31_binding",
    "packet_schema",
    "request_packet",
    "readiness_gate_projection",
    "packet_receipt",
    "product_metrics",
    "request_packet_hash",
}

SOURCE_INPUT_KEYS = {"id", "source_path", "source_sha256", "content_binding"}
SOURCE_STATUS_KEYS = {"file", "expected_status", "actual_status"}
P2_31_BINDING_KEYS = {
    "source_slice",
    "product_acceptance_status",
    "reviewer_status",
    "boundary_status",
    "readiness_gate_version",
    "readiness_gate_hash",
    "readiness_receipt_kind",
    "readiness_receipt_hash",
    "readiness_check_count",
    "readiness_source_count",
    "gate_result",
    "execution_permission_granted",
    "gate_used_as_action_basis",
    "formal_vault_accessed",
    "write_performed",
    "sync_performed",
    "promotion_performed",
}
SCHEMA_FIELD_KEYS = {"field_id", "required", "synthetic_only", "forbidden_real_content", "non_claim"}
REQUEST_PACKET_KEYS = {
    "packet_id",
    "packet_kind",
    "packet_mode",
    "packet_result",
    "synthetic_only",
    "actual_user_confirmation_collected",
    "actual_user_text_stored",
    "actual_user_text",
    "actual_formal_vault_state_checked",
    "actual_commands_supplied",
    "requested_execution_now",
    "requested_action_basis",
    "operator_decision_reference",
    "synthetic_confirmation_reference",
    "scope_reference",
    "target_manifest_reference",
    "command",
    "absolute_target_path",
    "approval_text",
    "non_claims",
}
PROJECTION_KEYS = {
    "target_gate_slice",
    "target_gate_version",
    "target_request_mode",
    "projected_request_id",
    "projected_gate_result",
    "screenable_by_p2_31",
    "projection_is_not_submission",
    "projection_collects_no_approval",
    "projection_contains_no_commands",
    "projection_contains_no_formal_vault_paths",
}
RECEIPT_KEYS = {
    "record_kind",
    "slice_id",
    "source_slice",
    "packet_result",
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
    "packet_submitted_to_gate",
    "packet_replayed",
    "packet_used_as_action_basis",
    "field_count",
    "source_count",
    "request_packet_hash",
    "non_claims",
}
METRIC_KEYS = {
    "required_positive_fixtures",
    "minimum_failure_cases",
    "required_packet_fields",
    "required_source_inputs",
    "manual_negative_probes",
    "max_journey_steps",
}

PROTOTYPE_REQUIRED_FILES = [
    "00 Request Packet Home.md",
    "01 Packet Contract.md",
    "02 Packet Fields.md",
    "03 Non Submission Receipt.md",
    "04 Stop Conditions.md",
    "05 Reviewer Packet.md",
    "request-packet-inspector.html",
    "Receipts/formal-vault-execution-request-packet-receipt.json",
]
PROTOTYPE_MARKDOWN_FILES = [
    "00 Request Packet Home.md",
    "01 Packet Contract.md",
    "02 Packet Fields.md",
    "03 Non Submission Receipt.md",
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
    ("real_user_text_marker", re.compile(r"(?i)\breal user text\s*[:=]")),
    ("absolute_formal_vault_path", re.compile(r"(?i)\b[A-Z]:[\\/][^\\n\\r]*Obsidian[\\/]")),
]

PROTOTYPE_SEMANTIC_DENY_PATTERNS = [
    ("execution_permission_yes", re.compile(r"(?i)\bexecution permission\s*[:=]\s*(yes|true|granted|allowed|ready)\b")),
    ("formal_vault_approval_yes", re.compile(r"(?i)\bformal vault approval\s*[:=]\s*(yes|true|granted|allowed|ready)\b")),
    ("action_basis_yes", re.compile(r"(?i)\baction basis\s*[:=]\s*(yes|true|granted|allowed|ready)\b")),
    ("approval_collected_yes", re.compile(r"(?i)\bapproval collected\s*[:=]\s*(yes|true)\b")),
    ("packet_submitted_yes", re.compile(r"(?i)\bpacket submitted\s*[:=]\s*(yes|true)\b")),
    ("authorizes_execution", re.compile(r"(?i)\bauthori[sz](?:es|ed|ation)?\b[^.\n]{0,80}\bexecution\b|\bexecution\b[^.\n]{0,80}\bauthori[sz](?:es|ed|ation)?\b")),
    ("may_execute", re.compile(r"(?i)\bmay execute\b")),
    ("submit_packet", re.compile(r"(?i)\bsubmit packet\b")),
    ("permission_collected", re.compile(r"(?i)\bpermission collected\b")),
    ("approval_obtained", re.compile(r"(?i)\bapproval obtained\b")),
]

HTML_FORBIDDEN_BITS = [
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

HTML_REQUIRED_ATTRS = [
    'data-sandbox-only="true"',
    'data-request-packet-only="true"',
    'data-non-executable="true"',
    'data-no-formal-vault-access="true"',
    'data-no-write="true"',
    'data-no-sync="true"',
    'data-no-authority="true"',
    'data-no-permission="true"',
    'data-no-real-user-text="true"',
]


def repo_path(rel_path: str) -> Path:
    return REPO_ROOT / rel_path.replace("/", "\\")


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


def validate_prototype_html_text(rel_path: str, html: str) -> list[str]:
    errors = scan_prototype_text(rel_path, html)
    lower = html.lower()
    for bit in HTML_FORBIDDEN_BITS:
        if bit in lower:
            errors.append(f"html_forbidden_token:{bit}")
    for attr in HTML_REQUIRED_ATTRS:
        if attr not in html:
            errors.append(f"html_missing_attr:{attr}")
    return errors


def expected_source_inputs() -> list[dict[str, str]]:
    items = []
    for source_id, rel_path in zip(SOURCE_IDS, READ_ONLY_SOURCES):
        path = repo_path(rel_path)
        items.append({"id": source_id, "source_path": rel_path, "source_sha256": file_sha256(path), "content_binding": "exact_source_sha256"})
    return items


def expected_source_statuses() -> list[dict[str, str | None]]:
    statuses = []
    base = repo_path(f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}")
    for file_name, expected in REQUIRED_SOURCE_STATUSES.items():
        statuses.append({"file": file_name, "expected_status": expected, "actual_status": frontmatter_status(base / file_name)})
    return statuses


def load_prev_config() -> dict[str, Any]:
    return read_json_path(repo_path(f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/fixtures/valid-reviewable-readiness-gate-config.json"))


def load_prev_receipt() -> dict[str, Any]:
    return read_json_path(
        repo_path(
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/prototype/"
            "formal-vault-execution-readiness-gate/Receipts/formal-vault-execution-readiness-gate-receipt.json"
        )
    )


def expected_p2_31_binding() -> dict[str, Any]:
    prev_config = load_prev_config()
    prev_receipt = load_prev_receipt()
    base = repo_path(f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}")
    return {
        "source_slice": SOURCE_SLICE,
        "product_acceptance_status": frontmatter_status(base / "product-acceptance-report.md"),
        "reviewer_status": frontmatter_status(base / "reviewer-report.md"),
        "boundary_status": frontmatter_status(base / "boundary-audit.md"),
        "readiness_gate_version": prev_config.get("readiness_gate_version"),
        "readiness_gate_hash": prev_config.get("readiness_gate_hash"),
        "readiness_receipt_kind": prev_receipt.get("record_kind"),
        "readiness_receipt_hash": prev_receipt.get("readiness_gate_hash"),
        "readiness_check_count": prev_receipt.get("check_count"),
        "readiness_source_count": prev_receipt.get("source_count"),
        "gate_result": prev_receipt.get("gate_result"),
        "execution_permission_granted": prev_receipt.get("execution_permission_granted"),
        "gate_used_as_action_basis": prev_receipt.get("gate_used_as_action_basis"),
        "formal_vault_accessed": prev_receipt.get("formal_vault_accessed"),
        "write_performed": prev_receipt.get("write_performed"),
        "sync_performed": prev_receipt.get("sync_performed"),
        "promotion_performed": prev_receipt.get("promotion_performed"),
    }


def expected_packet_hash(config: dict[str, Any]) -> str:
    clone = copy.deepcopy(config)
    clone.pop("request_packet_hash", None)
    if isinstance(clone.get("packet_receipt"), dict):
        clone["packet_receipt"].pop("request_packet_hash", None)
    return canonical_hash(clone)


def current_valid_config() -> dict[str, Any] | None:
    path = ROOT / "fixtures" / "valid-reviewable-request-packet-config.json"
    if not path.exists():
        return None
    return read_json_path(path)


def expected_packet_id(mode: str) -> str:
    return f"{SLICE_ID}:{mode}"


def expected_projection_id(mode: str) -> str:
    target_mode = TARGET_GATE_REQUEST_MODES.get(mode)
    return f"{SOURCE_SLICE}:{target_mode}"


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
    if config.get("request_packet_version") != "p2-32-formal-vault-execution-request-packet-v1":
        errors.append("request_packet_version_mismatch")
    if config.get("truth_boundary") != "sandbox_only_request_packet_not_execution_permission":
        errors.append("truth_boundary_mismatch")
    if config.get("purpose") != PACKET_PURPOSE:
        errors.append("purpose_mismatch")
    mode = config.get("packet_mode")
    if mode not in PACKET_MODES:
        errors.append("packet_mode_not_allowed")
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

    controls = config.get("packet_controls")
    if not isinstance(controls, dict):
        errors.append("packet_controls_missing")
        controls = {}
    errors.extend(check_keys("packet_controls", controls, set(PACKET_CONTROL_EXPECTED)))
    for key, expected in PACKET_CONTROL_EXPECTED.items():
        if controls.get(key) is not expected:
            errors.append(f"packet_control_mismatch:{key}")

    expected_inputs = expected_source_inputs()
    if config.get("source_inputs") != expected_inputs:
        errors.append("source_inputs_mismatch")
    if isinstance(config.get("source_inputs"), list):
        for item in config["source_inputs"]:
            errors.extend(check_keys(f"source_inputs[{item.get('id', 'unknown')}]", item, SOURCE_INPUT_KEYS))
    else:
        errors.append("source_inputs_not_list")

    expected_statuses = expected_source_statuses()
    if config.get("source_statuses") != expected_statuses:
        errors.append("source_statuses_mismatch")
    if isinstance(config.get("source_statuses"), list):
        for item in config["source_statuses"]:
            errors.extend(check_keys(f"source_statuses[{item.get('file', 'unknown')}]", item, SOURCE_STATUS_KEYS))
            if item.get("expected_status") != item.get("actual_status"):
                errors.append(f"source_status_not_met:{item.get('file')}")
    else:
        errors.append("source_statuses_not_list")

    binding = config.get("p2_31_binding")
    expected_binding = expected_p2_31_binding()
    if binding != expected_binding:
        errors.append("p2_31_binding_mismatch")
    if isinstance(binding, dict):
        errors.extend(check_keys("p2_31_binding", binding, P2_31_BINDING_KEYS))
        for false_key in ["execution_permission_granted", "gate_used_as_action_basis", "formal_vault_accessed", "write_performed", "sync_performed", "promotion_performed"]:
            if binding.get(false_key) is not False:
                errors.append(f"p2_31_binding_flag_not_false:{false_key}")
        if binding.get("product_acceptance_status") != "pass_product_grade":
            errors.append("p2_31_product_acceptance_not_pass")
        if binding.get("reviewer_status") != "reviewer_pass":
            errors.append("p2_31_reviewer_not_pass")
        if binding.get("boundary_status") != "boundary_pass":
            errors.append("p2_31_boundary_not_pass")
        if binding.get("readiness_gate_hash") != binding.get("readiness_receipt_hash"):
            errors.append("p2_31_gate_hash_receipt_mismatch")
    else:
        errors.append("p2_31_binding_not_object")

    schema = config.get("packet_schema")
    if not isinstance(schema, list):
        errors.append("packet_schema_not_list")
        schema = []
    field_ids = [item.get("field_id") for item in schema if isinstance(item, dict)]
    if field_ids != PACKET_FIELD_IDS:
        errors.append("packet_schema_field_ids_mismatch")
    for item in schema:
        if not isinstance(item, dict):
            errors.append("packet_schema_item_not_object")
            continue
        field_id = item.get("field_id", "unknown")
        errors.extend(check_keys(f"packet_schema[{field_id}]", item, SCHEMA_FIELD_KEYS))
        if item.get("required") is not True or item.get("synthetic_only") is not True or item.get("forbidden_real_content") is not True:
            errors.append(f"packet_schema_flag_mismatch:{field_id}")
        if item.get("non_claim") != "schema_field_is_contract_not_user_input":
            errors.append(f"packet_schema_non_claim_mismatch:{field_id}")

    packet = config.get("request_packet")
    if not isinstance(packet, dict):
        errors.append("request_packet_missing")
        packet = {}
    errors.extend(check_keys("request_packet", packet, REQUEST_PACKET_KEYS))
    expected_result = PACKET_MODES.get(mode)
    if packet.get("packet_id") != expected_packet_id(mode):
        errors.append("packet_id_mismatch")
    if packet.get("packet_kind") != "synthetic_future_formal_vault_execution_request_packet":
        errors.append("packet_kind_mismatch")
    if packet.get("packet_mode") != mode:
        errors.append("packet_mode_mismatch")
    if packet.get("packet_result") != expected_result:
        errors.append("packet_result_mismatch")
    for true_key in ["synthetic_only"]:
        if packet.get(true_key) is not True:
            errors.append(f"packet_flag_not_true:{true_key}")
    for false_key in [
        "actual_user_confirmation_collected",
        "actual_user_text_stored",
        "actual_formal_vault_state_checked",
        "actual_commands_supplied",
        "requested_execution_now",
        "requested_action_basis",
    ]:
        if packet.get(false_key) is not False:
            errors.append(f"packet_flag_not_false:{false_key}")
    for empty_key in ["actual_user_text", "command", "absolute_target_path", "approval_text"]:
        if packet.get(empty_key) not in ("", None):
            errors.append(f"packet_forbidden_field_nonempty:{empty_key}")
    if not NON_CLAIMS.issubset(set(packet.get("non_claims", []))):
        errors.append("packet_non_claims_missing")
    expected_decision = {
        "synthetic_reviewable_request_packet": "review_packet_only",
        "synthetic_missing_confirmation_packet": "missing_confirmation",
        "synthetic_denied_request_packet": "deny",
    }.get(mode)
    if packet.get("operator_decision_reference") != expected_decision:
        errors.append("packet_operator_decision_reference_mismatch")
    if packet.get("synthetic_confirmation_reference") != f"synthetic_confirmation_reference:{mode}":
        errors.append("packet_synthetic_confirmation_reference_mismatch")
    if packet.get("scope_reference") != "p2_30_target_manifest_reference_only":
        errors.append("packet_scope_reference_mismatch")
    if packet.get("target_manifest_reference") != "p2_30_target_manifest_reference_only":
        errors.append("packet_target_manifest_reference_mismatch")

    projection = config.get("readiness_gate_projection")
    if not isinstance(projection, dict):
        errors.append("readiness_gate_projection_missing")
        projection = {}
    errors.extend(check_keys("readiness_gate_projection", projection, PROJECTION_KEYS))
    if projection.get("target_gate_slice") != SOURCE_SLICE:
        errors.append("projection_target_gate_slice_mismatch")
    expected_gate_version = binding.get("readiness_gate_version") if isinstance(binding, dict) else None
    if projection.get("target_gate_version") != expected_gate_version:
        errors.append("projection_target_gate_version_mismatch")
    if projection.get("target_request_mode") != TARGET_GATE_REQUEST_MODES.get(mode):
        errors.append("projection_target_request_mode_mismatch")
    if projection.get("projected_request_id") != expected_projection_id(mode):
        errors.append("projection_request_id_mismatch")
    if projection.get("projected_gate_result") != TARGET_GATE_RESULTS.get(mode):
        errors.append("projection_gate_result_mismatch")
    for true_key in ["screenable_by_p2_31", "projection_is_not_submission", "projection_collects_no_approval", "projection_contains_no_commands", "projection_contains_no_formal_vault_paths"]:
        if projection.get(true_key) is not True:
            errors.append(f"projection_flag_not_true:{true_key}")

    receipt = config.get("packet_receipt")
    if not isinstance(receipt, dict):
        errors.append("packet_receipt_missing")
        receipt = {}
    errors.extend(check_keys("packet_receipt", receipt, RECEIPT_KEYS))
    if receipt.get("record_kind") != "sandbox_formal_vault_execution_request_packet_receipt":
        errors.append("receipt_record_kind_mismatch")
    if receipt.get("slice_id") != SLICE_ID:
        errors.append("receipt_slice_id_mismatch")
    if receipt.get("source_slice") != SOURCE_SLICE:
        errors.append("receipt_source_slice_mismatch")
    if receipt.get("packet_result") != expected_result:
        errors.append("receipt_packet_result_mismatch")
    if receipt.get("field_count") != len(PACKET_FIELD_IDS):
        errors.append("receipt_field_count_mismatch")
    if receipt.get("source_count") != len(READ_ONLY_SOURCES):
        errors.append("receipt_source_count_mismatch")
    if receipt.get("request_packet_hash") != expected_packet_hash(config):
        errors.append("receipt_request_packet_hash_mismatch")
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
        "packet_submitted_to_gate",
        "packet_replayed",
        "packet_used_as_action_basis",
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
    if metrics.get("required_packet_fields") != len(PACKET_FIELD_IDS):
        errors.append("metric_packet_fields_mismatch")
    if metrics.get("required_source_inputs") != len(READ_ONLY_SOURCES):
        errors.append("metric_source_inputs_mismatch")
    if metrics.get("manual_negative_probes") != 12:
        errors.append("metric_manual_negative_probes_mismatch")
    if metrics.get("max_journey_steps") != 3:
        errors.append("metric_max_journey_steps_mismatch")

    if config.get("request_packet_hash") != expected_packet_hash(config):
        errors.append("request_packet_hash_mismatch")
    return sorted(set(errors))


def validate_prototype_receipt(receipt: Any, config: dict[str, Any] | None = None) -> list[str]:
    errors = []
    if not isinstance(receipt, dict):
        return ["prototype_receipt_not_object"]
    errors.extend(check_keys("prototype_receipt", receipt, RECEIPT_KEYS))
    errors.extend(scan_dangerous_values(receipt, "$.prototype_receipt"))
    expected_config = config or current_valid_config()
    expected_hash = expected_config.get("request_packet_hash") if expected_config else None
    expected_result = expected_config.get("request_packet", {}).get("packet_result") if expected_config else None
    if receipt.get("record_kind") != "sandbox_formal_vault_execution_request_packet_receipt":
        errors.append("prototype_receipt_record_kind_mismatch")
    if receipt.get("slice_id") != SLICE_ID:
        errors.append("prototype_receipt_slice_id_mismatch")
    if receipt.get("source_slice") != SOURCE_SLICE:
        errors.append("prototype_receipt_source_slice_mismatch")
    if expected_result and receipt.get("packet_result") != expected_result:
        errors.append("prototype_receipt_packet_result_mismatch")
    if receipt.get("field_count") != len(PACKET_FIELD_IDS):
        errors.append("prototype_receipt_field_count_mismatch")
    if receipt.get("source_count") != len(READ_ONLY_SOURCES):
        errors.append("prototype_receipt_source_count_mismatch")
    if expected_hash and receipt.get("request_packet_hash") != expected_hash:
        errors.append("prototype_receipt_packet_hash_mismatch")
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
        "packet_submitted_to_gate",
        "packet_replayed",
        "packet_used_as_action_basis",
    ]:
        if receipt.get(false_key) is not False:
            errors.append(f"prototype_receipt_flag_not_false:{false_key}")
    if not NON_CLAIMS.issubset(set(receipt.get("non_claims", []))):
        errors.append("prototype_receipt_non_claims_missing")
    return sorted(set(errors))


def inspect_prototype() -> dict[str, Any]:
    prototype_path = ROOT / "prototype" / "formal-vault-execution-request-packet"
    receipt_path = prototype_path / "Receipts" / "formal-vault-execution-request-packet-receipt.json"
    html_path = prototype_path / "request-packet-inspector.html"
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
        issues.extend(validate_prototype_html_text("request-packet-inspector.html", html))
        lower = html.lower()
        buttons = re.findall(r"<button[^>]*data-filter=\"([^\"]+)\"[^>]*>([^<]+)</button>", html)
        html_summary = {
            "sandbox_only": 'data-sandbox-only="true"' in html,
            "request_packet_only": 'data-request-packet-only="true"' in html,
            "non_executable": 'data-non-executable="true"' in html,
            "no_formal_vault_access": 'data-no-formal-vault-access="true"' in html,
            "no_write": 'data-no-write="true"' in html,
            "no_sync": 'data-no-sync="true"' in html,
            "no_authority": 'data-no-authority="true"' in html,
            "no_permission": 'data-no-permission="true"' in html,
            "no_real_user_text": 'data-no-real-user-text="true"' in html,
            "forms": lower.count("<form"),
            "downloads": lower.count("download="),
            "contenteditable": lower.count("contenteditable"),
            "anchors": lower.count("<a "),
            "buttons": [button[0] for button in buttons],
            "button_texts": [button[1].strip() for button in buttons],
        }
    else:
        issues.append("missing_inspector_html")
    file_presence = {
        "contract_file": (prototype_path / "01 Packet Contract.md").exists(),
        "field_file": (prototype_path / "02 Packet Fields.md").exists(),
        "receipt_file": (prototype_path / "03 Non Submission Receipt.md").exists(),
        "stop_file": (prototype_path / "04 Stop Conditions.md").exists(),
        "inspector_file": html_path.exists(),
        "html_allowlist_ok": not issues,
    }
    return {"prototype_path": str(prototype_path), "issues": sorted(set(issues)), "receipt": receipt, "html": html_summary, "prototype_file_presence": file_presence}


def validate_prototype_tamper(tamper: dict[str, Any]) -> list[str]:
    if tamper.get("kind") == "markdown_replace":
        return scan_prototype_text(tamper.get("file", "unknown.md"), tamper.get("content", ""))
    if tamper.get("kind") == "html_replace":
        return validate_prototype_html_text(tamper.get("file", "request-packet-inspector.html"), tamper.get("content", ""))
    receipt_path = ROOT / "prototype" / "formal-vault-execution-request-packet" / "Receipts" / "formal-vault-execution-request-packet-receipt.json"
    if receipt_path.exists():
        base_receipt = read_json_path(receipt_path)
    else:
        config = current_valid_config()
        base_receipt = copy.deepcopy(config.get("packet_receipt", {})) if config else {}
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
    config["request_packet_hash"] = ""
    if isinstance(config.get("packet_receipt"), dict):
        config["packet_receipt"]["request_packet_hash"] = ""
    packet_hash = expected_packet_hash(config)
    config["request_packet_hash"] = packet_hash
    if isinstance(config.get("packet_receipt"), dict):
        config["packet_receipt"]["request_packet_hash"] = packet_hash
    return config


def run_manual_negative_probes() -> dict[str, Any]:
    config = current_valid_config()
    if not config:
        return {"count": 0, "mismatches": ["missing_current_valid_config"], "probes": []}
    probes: list[dict[str, Any]] = []

    def add_packet_probe(name: str, path: list[str], value: Any, expected: list[str]) -> None:
        candidate = copy.deepcopy(config)
        cursor: Any = candidate
        for part in path[:-1]:
            cursor = cursor[part]
        cursor[path[-1]] = value
        _rehash_for_probe(candidate)
        probes.append({"name": name, "expected_errors": expected, "actual_errors": validate_config(candidate)})

    add_packet_probe("manual-packet-id-real-user-text", ["request_packet", "packet_id"], "user said approve execution", ["packet_id_mismatch"])
    add_packet_probe(
        "manual-packet-id-command",
        ["request_packet", "packet_id"],
        "python tools/promote.py --sync",
        [
            "packet_id_mismatch",
            "dangerous_value:$.request_packet.packet_id:python_command",
            "dangerous_value:$.request_packet.packet_id:promote_py",
            "dangerous_value:$.request_packet.packet_id:sync_flag",
        ],
    )
    add_packet_probe(
        "manual-approval-text-approval-now",
        ["request_packet", "approval_text"],
        "I approve execution now",
        [
            "packet_forbidden_field_nonempty:approval_text",
            "dangerous_value:$.request_packet.approval_text:approve_execution_now",
        ],
    )
    add_packet_probe(
        "manual-projection-submission",
        ["readiness_gate_projection", "projection_is_not_submission"],
        False,
        ["projection_flag_not_true:projection_is_not_submission"],
    )
    add_packet_probe(
        "manual-projection-request-id-command",
        ["readiness_gate_projection", "projected_request_id"],
        "python tools/promote.py --sync",
        [
            "projection_request_id_mismatch",
            "dangerous_value:$.readiness_gate_projection.projected_request_id:python_command",
            "dangerous_value:$.readiness_gate_projection.projected_request_id:promote_py",
            "dangerous_value:$.readiness_gate_projection.projected_request_id:sync_flag",
        ],
    )

    prototype_probes = [
        ("manual-prototype-approval-collected-yes", {"kind": "markdown_replace", "file": "03 Non Submission Receipt.md", "content": "approval collected: yes"}, ["prototype_text_authority_confusion:03 Non Submission Receipt.md:approval_collected_yes"]),
        ("manual-prototype-packet-submitted-yes", {"kind": "markdown_replace", "file": "05 Reviewer Packet.md", "content": "packet submitted: yes"}, ["prototype_text_authority_confusion:05 Reviewer Packet.md:packet_submitted_yes"]),
        ("manual-prototype-real-user-text", {"kind": "markdown_replace", "file": "02 Packet Fields.md", "content": "real user text: approve execution now"}, ["prototype_text_dangerous:02 Packet Fields.md:real_user_text_marker"]),
        ("manual-prototype-authorizes-execution", {"kind": "markdown_replace", "file": "01 Packet Contract.md", "content": "This packet authorizes the future execution slice."}, ["prototype_text_authority_confusion:01 Packet Contract.md:authorizes_execution"]),
        ("manual-prototype-may-execute", {"kind": "markdown_replace", "file": "04 Stop Conditions.md", "content": "The operator may execute the formal vault operation."}, ["prototype_text_authority_confusion:04 Stop Conditions.md:may_execute"]),
        ("manual-prototype-permission-collected", {"kind": "markdown_replace", "file": "03 Non Submission Receipt.md", "content": "Permission collected from the user."}, ["prototype_text_authority_confusion:03 Non Submission Receipt.md:permission_collected"]),
        ("manual-prototype-approval-obtained", {"kind": "markdown_replace", "file": "03 Non Submission Receipt.md", "content": "Approval obtained from the user."}, ["prototype_text_authority_confusion:03 Non Submission Receipt.md:approval_obtained"]),
    ]
    for name, tamper, expected in prototype_probes:
        probes.append({"name": name, "expected_errors": expected, "actual_errors": validate_prototype_tamper(tamper)})

    mismatches = []
    for probe in probes:
        if not set(probe["expected_errors"]).issubset(set(probe["actual_errors"])):
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
