from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p2-33-formal-vault-execution-request-screening-sandbox"
SOURCE_SLICE = "2026-06-15-p2-32-formal-vault-execution-request-packet-sandbox"
ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[3]

SCREENING_PURPOSE = (
    "Screen synthetic P2-32 request packets against P2-31 readiness-gate projection "
    "expectations without submitting packets, collecting approval, storing actual user "
    "wording, resolving formal-vault paths, emitting commands, or granting permission."
)

READ_ONLY_SOURCES = [
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/next-step.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/product-acceptance-report.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/verification.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/reviewer-report.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/boundary-audit.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/source-map.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/fixtures/valid-reviewable-request-packet-config.json",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/fixtures/valid-missing-confirmation-request-packet-config.json",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/fixtures/valid-denied-request-packet-config.json",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/prototype/formal-vault-execution-request-packet/Receipts/formal-vault-execution-request-packet-receipt.json",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/artifact/formal-vault-execution-request-packet-contract.md",
]

SOURCE_IDS = [
    "p2_32_next_step",
    "p2_32_product_acceptance",
    "p2_32_verification",
    "p2_32_reviewer_report",
    "p2_32_boundary_audit",
    "p2_32_source_map",
    "p2_32_reviewable_packet_config",
    "p2_32_missing_confirmation_packet_config",
    "p2_32_denied_packet_config",
    "p2_32_request_packet_receipt",
    "p2_32_request_packet_contract",
]

REQUIRED_SOURCE_STATUSES = {
    "next-step.md": "pass_product_grade_pending_user_next_slice_decision",
    "product-acceptance-report.md": "pass_product_grade",
    "verification.md": "local_verification_passed_pending_review",
    "reviewer-report.md": "reviewer_pass",
    "boundary-audit.md": "boundary_pass",
    "source-map.md": "built_pending_review",
}

SCREENING_MODES = {
    "synthetic_reviewable_request_screening": "SCREENED_REVIEWABLE_NOT_SUBMITTED",
    "synthetic_missing_confirmation_screening": "SCREENED_BLOCKED_MISSING_CONFIRMATION_NOT_SUBMITTED",
    "synthetic_denied_request_screening": "SCREENED_BLOCKED_BY_DENIAL_NOT_SUBMITTED",
}

MODE_TO_PACKET_FIXTURE = {
    "synthetic_reviewable_request_screening": "valid-reviewable-request-packet-config.json",
    "synthetic_missing_confirmation_screening": "valid-missing-confirmation-request-packet-config.json",
    "synthetic_denied_request_screening": "valid-denied-request-packet-config.json",
}

MODE_TO_PACKET_MODE = {
    "synthetic_reviewable_request_screening": "synthetic_reviewable_request_packet",
    "synthetic_missing_confirmation_screening": "synthetic_missing_confirmation_packet",
    "synthetic_denied_request_screening": "synthetic_denied_request_packet",
}

MODE_TO_PACKET_RESULT = {
    "synthetic_reviewable_request_screening": "REQUEST_PACKET_REVIEWABLE_NOT_APPROVAL",
    "synthetic_missing_confirmation_screening": "REQUEST_PACKET_BLOCKED_MISSING_FUTURE_CONFIRMATION",
    "synthetic_denied_request_screening": "REQUEST_PACKET_BLOCKED_BY_DENIAL",
}

MODE_TO_GATE_RESULT = {
    "synthetic_reviewable_request_screening": "READINESS_PACKET_REVIEWABLE_NOT_EXECUTABLE",
    "synthetic_missing_confirmation_screening": "BLOCKED_MISSING_FUTURE_CONFIRMATION_LEDGER_ONLY",
    "synthetic_denied_request_screening": "BLOCKED_BY_DENIAL_LEDGER_ONLY",
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
    "actual_approval_collection",
    "actual_user_approval",
    "actual_user_decision_collection",
    "user_approval_inference",
    "actual_user_wording_storage",
    "actual_user_wording_capture",
    "packet_submission",
    "screening_submission",
    "gate_submission",
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
    "screening_promoted_to_execution_permission",
    "screening_used_as_action_basis",
]

SCREENING_CONTROL_EXPECTED = {
    "sandbox_only": True,
    "screening_only": True,
    "read_only_projection": True,
    "synthetic_packet_only": True,
    "non_executable": True,
    "no_submission": True,
    "no_actual_approval": True,
    "no_actual_user_wording": True,
    "no_formal_vault_paths": True,
    "no_commands": True,
    "operator_must_stop_before_execution": True,
    "separate_future_user_confirmation_required": True,
    "separate_future_execution_slice_required": True,
    "separate_future_formal_vault_state_check_required": True,
    "product_acceptance_is_not_formal_vault_approval": True,
    "screening_is_not_execution_permission": True,
    "screening_is_not_action_basis": True,
    "screening_is_not_user_instruction": True,
    "screening_is_not_reviewed_knowledge": True,
    "screening_is_not_evidence_support": True,
    "execution_allowed_now": False,
    "formal_vault_access_allowed_now": False,
    "formal_vault_write_allowed_now": False,
    "formal_vault_hash_allowed_now": False,
    "formal_vault_snapshot_allowed_now": False,
    "user_confirmation_collected_now": False,
    "actual_user_wording_stored": False,
    "contains_commands": False,
    "absolute_vault_paths_present": False,
    "sync_commit_push_promotion_allowed": False,
    "screening_can_be_replayed": False,
    "screening_result_can_be_used_as_action_basis": False,
}

SCREENING_CHECK_IDS = [
    "p2_32_product_pass_present",
    "p2_32_packet_hash_bound",
    "source_hashes_current",
    "packet_identity_synthetic",
    "projection_matches_p2_31",
    "packet_not_submitted",
    "no_actual_approval",
    "no_actual_user_wording",
    "no_commands_or_paths",
    "no_current_execution_permission",
]

SCREENING_CHECK_STATUS = {
    "synthetic_reviewable_request_screening": {
        "p2_32_product_pass_present": "PASS",
        "p2_32_packet_hash_bound": "PASS",
        "source_hashes_current": "PASS",
        "packet_identity_synthetic": "PASS",
        "projection_matches_p2_31": "PASS",
        "packet_not_submitted": "PASS",
        "no_actual_approval": "PASS",
        "no_actual_user_wording": "PASS",
        "no_commands_or_paths": "PASS",
        "no_current_execution_permission": "PASS",
    },
    "synthetic_missing_confirmation_screening": {
        "p2_32_product_pass_present": "PASS",
        "p2_32_packet_hash_bound": "PASS",
        "source_hashes_current": "PASS",
        "packet_identity_synthetic": "PASS",
        "projection_matches_p2_31": "PASS",
        "packet_not_submitted": "PASS",
        "no_actual_approval": "PASS",
        "no_actual_user_wording": "PASS",
        "no_commands_or_paths": "PASS",
        "no_current_execution_permission": "BLOCKED_MISSING_FUTURE_CONFIRMATION",
    },
    "synthetic_denied_request_screening": {
        "p2_32_product_pass_present": "PASS",
        "p2_32_packet_hash_bound": "PASS",
        "source_hashes_current": "PASS",
        "packet_identity_synthetic": "PASS",
        "projection_matches_p2_31": "PASS",
        "packet_not_submitted": "PASS",
        "no_actual_approval": "PASS",
        "no_actual_user_wording": "PASS",
        "no_commands_or_paths": "PASS",
        "no_current_execution_permission": "BLOCKED_BY_DENIAL",
    },
}

NON_CLAIMS = {
    "not actual approval",
    "not user instruction",
    "not actual user wording",
    "not packet submission",
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
    "request_screening_version",
    "truth_boundary",
    "purpose",
    "screening_mode",
    "write_scope",
    "read_only_sources",
    "operations",
    "screening_controls",
    "source_inputs",
    "source_statuses",
    "p2_32_binding",
    "screening_input_packet",
    "screening_projection",
    "screening_checks",
    "screening_receipt",
    "product_metrics",
    "request_screening_hash",
}

SOURCE_INPUT_KEYS = {"id", "source_path", "source_sha256", "content_binding"}
SOURCE_STATUS_KEYS = {"file", "expected_status", "actual_status"}
P2_32_BINDING_KEYS = {
    "source_slice",
    "product_acceptance_status",
    "reviewer_status",
    "boundary_status",
    "request_packet_version",
    "request_packet_hash",
    "packet_receipt_kind",
    "packet_receipt_hash",
    "packet_field_count",
    "packet_source_count",
    "packet_result",
    "packet_submitted_to_gate",
    "execution_permission_granted",
    "packet_used_as_action_basis",
    "formal_vault_accessed",
    "approval_collected_now",
    "real_user_text_stored",
    "write_performed",
    "sync_performed",
    "promotion_performed",
}
SCREENING_INPUT_KEYS = {
    "source_fixture",
    "source_packet_hash",
    "packet_id",
    "packet_mode",
    "packet_result",
    "synthetic_only",
    "actual_approval_collected",
    "actual_user_wording_stored",
    "commands_supplied",
    "absolute_paths_present",
    "requested_execution_now",
    "requested_action_basis",
    "packet_submitted",
    "non_claims",
}
PROJECTION_KEYS = {
    "target_gate_slice",
    "target_request_mode",
    "projected_request_id",
    "projected_gate_result",
    "screening_result",
    "projection_matches_packet",
    "projection_is_not_submission",
    "projection_collects_no_approval",
    "projection_contains_no_commands",
    "projection_contains_no_formal_vault_paths",
}
CHECK_KEYS = {"check_id", "sequence", "status", "screened_now", "collected_now", "non_claim"}
RECEIPT_KEYS = {
    "record_kind",
    "slice_id",
    "source_slice",
    "screening_result",
    "packet_submitted",
    "formal_vault_accessed",
    "formal_vault_state_inspected",
    "approval_collected_now",
    "actual_user_input_used",
    "actual_user_wording_stored",
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
    "screening_replayed",
    "screening_used_as_action_basis",
    "check_count",
    "source_count",
    "request_screening_hash",
    "non_claims",
}
METRIC_KEYS = {
    "required_positive_fixtures",
    "minimum_failure_cases",
    "required_screening_checks",
    "required_source_inputs",
    "manual_negative_probes",
    "max_journey_steps",
}

PROTOTYPE_REQUIRED_FILES = [
    "00 Screening Home.md",
    "01 Screening Contract.md",
    "02 Screening Checks.md",
    "03 Non Submission Receipt.md",
    "04 Stop Conditions.md",
    "05 Reviewer Packet.md",
    "request-screening-inspector.html",
    "Receipts/formal-vault-execution-request-screening-receipt.json",
]
PROTOTYPE_MARKDOWN_FILES = [
    "00 Screening Home.md",
    "01 Screening Contract.md",
    "02 Screening Checks.md",
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
    ("actual_user_wording_marker", re.compile(r"(?i)\bactual user wording\s*[:=]")),
    ("absolute_formal_vault_path", re.compile(r"(?i)\b[A-Z]:[\\/][^\\n\\r]*Obsidian[\\/]")),
]

PROTOTYPE_SEMANTIC_DENY_PATTERNS = [
    ("execution_permission_yes", re.compile(r"(?i)\bexecution permission\s*[:=]\s*(yes|true|granted|allowed|ready)\b")),
    ("formal_vault_approval_yes", re.compile(r"(?i)\bformal vault approval\s*[:=]\s*(yes|true|granted|allowed|ready)\b")),
    ("action_basis_yes", re.compile(r"(?i)\baction basis\s*[:=]\s*(yes|true|granted|allowed|ready)\b")),
    ("approval_collected_yes", re.compile(r"(?i)\bapproval collected\s*[:=]\s*(yes|true)\b")),
    ("packet_submitted_yes", re.compile(r"(?i)\bpacket submitted\s*[:=]\s*(yes|true)\b")),
    ("screening_submitted_yes", re.compile(r"(?i)\bscreening submitted\s*[:=]\s*(yes|true)\b")),
    ("authorizes_execution", re.compile(r"(?i)\bauthori[sz](?:es|ed|ation)?\b[^.\n]{0,80}\bexecution\b|\bexecution\b[^.\n]{0,80}\bauthori[sz](?:es|ed|ation)?\b")),
    ("may_execute", re.compile(r"(?i)\bmay execute\b")),
    ("submit_packet", re.compile(r"(?i)\bsubmit packet\b")),
    ("submit_screening", re.compile(r"(?i)\bsubmit screening\b")),
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
    'data-screening-only="true"',
    'data-non-executable="true"',
    'data-no-formal-vault-access="true"',
    'data-no-write="true"',
    'data-no-sync="true"',
    'data-no-authority="true"',
    'data-no-permission="true"',
    'data-no-actual-user-wording="true"',
    'data-no-submission="true"',
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
        items.append({"id": source_id, "source_path": rel_path, "source_sha256": file_sha256(repo_path(rel_path)), "content_binding": "exact_source_sha256"})
    return items


def expected_source_statuses() -> list[dict[str, str | None]]:
    statuses = []
    base = repo_path(f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}")
    for file_name, expected in REQUIRED_SOURCE_STATUSES.items():
        statuses.append({"file": file_name, "expected_status": expected, "actual_status": frontmatter_status(base / file_name)})
    return statuses


def load_prev_config(file_name: str = "valid-reviewable-request-packet-config.json") -> dict[str, Any]:
    return read_json_path(repo_path(f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/fixtures/{file_name}"))


def load_prev_receipt() -> dict[str, Any]:
    return read_json_path(
        repo_path(
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/prototype/"
            "formal-vault-execution-request-packet/Receipts/formal-vault-execution-request-packet-receipt.json"
        )
    )


def expected_p2_32_binding() -> dict[str, Any]:
    prev_config = load_prev_config()
    prev_receipt = load_prev_receipt()
    base = repo_path(f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}")
    return {
        "source_slice": SOURCE_SLICE,
        "product_acceptance_status": frontmatter_status(base / "product-acceptance-report.md"),
        "reviewer_status": frontmatter_status(base / "reviewer-report.md"),
        "boundary_status": frontmatter_status(base / "boundary-audit.md"),
        "request_packet_version": prev_config.get("request_packet_version"),
        "request_packet_hash": prev_config.get("request_packet_hash"),
        "packet_receipt_kind": prev_receipt.get("record_kind"),
        "packet_receipt_hash": prev_receipt.get("request_packet_hash"),
        "packet_field_count": prev_receipt.get("field_count"),
        "packet_source_count": prev_receipt.get("source_count"),
        "packet_result": prev_receipt.get("packet_result"),
        "packet_submitted_to_gate": prev_receipt.get("packet_submitted_to_gate"),
        "execution_permission_granted": prev_receipt.get("execution_permission_granted"),
        "packet_used_as_action_basis": prev_receipt.get("packet_used_as_action_basis"),
        "formal_vault_accessed": prev_receipt.get("formal_vault_accessed"),
        "approval_collected_now": prev_receipt.get("approval_collected_now"),
        "real_user_text_stored": prev_receipt.get("real_user_text_stored"),
        "write_performed": prev_receipt.get("write_performed"),
        "sync_performed": prev_receipt.get("sync_performed"),
        "promotion_performed": prev_receipt.get("promotion_performed"),
    }


def expected_screening_hash(config: dict[str, Any]) -> str:
    clone = copy.deepcopy(config)
    clone.pop("request_screening_hash", None)
    if isinstance(clone.get("screening_receipt"), dict):
        clone["screening_receipt"].pop("request_screening_hash", None)
    return canonical_hash(clone)


def current_valid_config() -> dict[str, Any] | None:
    path = ROOT / "fixtures" / "valid-reviewable-request-screening-config.json"
    if not path.exists():
        return None
    return read_json_path(path)


def expected_screening_input(mode: str) -> dict[str, Any]:
    fixture = MODE_TO_PACKET_FIXTURE[mode]
    packet_config = load_prev_config(fixture)
    packet = packet_config["request_packet"]
    return {
        "source_fixture": fixture,
        "source_packet_hash": packet_config["request_packet_hash"],
        "packet_id": packet["packet_id"],
        "packet_mode": packet["packet_mode"],
        "packet_result": packet["packet_result"],
        "synthetic_only": packet["synthetic_only"],
        "actual_approval_collected": packet["actual_user_confirmation_collected"],
        "actual_user_wording_stored": packet["actual_user_text_stored"],
        "commands_supplied": packet["actual_commands_supplied"],
        "absolute_paths_present": bool(packet["absolute_target_path"]),
        "requested_execution_now": packet["requested_execution_now"],
        "requested_action_basis": packet["requested_action_basis"],
        "packet_submitted": False,
        "non_claims": sorted(NON_CLAIMS),
    }


def expected_projection(mode: str) -> dict[str, Any]:
    packet_config = load_prev_config(MODE_TO_PACKET_FIXTURE[mode])
    projection = packet_config["readiness_gate_projection"]
    return {
        "target_gate_slice": projection["target_gate_slice"],
        "target_request_mode": projection["target_request_mode"],
        "projected_request_id": projection["projected_request_id"],
        "projected_gate_result": projection["projected_gate_result"],
        "screening_result": SCREENING_MODES[mode],
        "projection_matches_packet": True,
        "projection_is_not_submission": True,
        "projection_collects_no_approval": True,
        "projection_contains_no_commands": True,
        "projection_contains_no_formal_vault_paths": True,
    }


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(config, dict):
        return ["config_not_object"]
    errors.extend(check_keys("config", config, TOP_LEVEL_KEYS))
    errors.extend(scan_dangerous_values(config))

    mode = config.get("screening_mode")
    if config.get("slice_id") != SLICE_ID:
        errors.append("slice_id_mismatch")
    if config.get("source_slice") != SOURCE_SLICE:
        errors.append("source_slice_mismatch")
    if config.get("request_screening_version") != "p2-33-formal-vault-execution-request-screening-v1":
        errors.append("request_screening_version_mismatch")
    if config.get("truth_boundary") != "sandbox_only_request_screening_not_submission":
        errors.append("truth_boundary_mismatch")
    if config.get("purpose") != SCREENING_PURPOSE:
        errors.append("purpose_mismatch")
    if mode not in SCREENING_MODES:
        errors.append("screening_mode_not_allowed")
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

    controls = config.get("screening_controls")
    if not isinstance(controls, dict):
        errors.append("screening_controls_missing")
        controls = {}
    errors.extend(check_keys("screening_controls", controls, set(SCREENING_CONTROL_EXPECTED)))
    for key, expected in SCREENING_CONTROL_EXPECTED.items():
        if controls.get(key) is not expected:
            errors.append(f"screening_control_mismatch:{key}")

    if config.get("source_inputs") != expected_source_inputs():
        errors.append("source_inputs_mismatch")
    if isinstance(config.get("source_inputs"), list):
        for item in config["source_inputs"]:
            errors.extend(check_keys(f"source_inputs[{item.get('id', 'unknown')}]", item, SOURCE_INPUT_KEYS))
    else:
        errors.append("source_inputs_not_list")

    if config.get("source_statuses") != expected_source_statuses():
        errors.append("source_statuses_mismatch")
    if isinstance(config.get("source_statuses"), list):
        for item in config["source_statuses"]:
            errors.extend(check_keys(f"source_statuses[{item.get('file', 'unknown')}]", item, SOURCE_STATUS_KEYS))
            if item.get("expected_status") != item.get("actual_status"):
                errors.append(f"source_status_not_met:{item.get('file')}")
    else:
        errors.append("source_statuses_not_list")

    binding = config.get("p2_32_binding")
    expected_binding = expected_p2_32_binding()
    if binding != expected_binding:
        errors.append("p2_32_binding_mismatch")
    if isinstance(binding, dict):
        errors.extend(check_keys("p2_32_binding", binding, P2_32_BINDING_KEYS))
        for false_key in [
            "packet_submitted_to_gate",
            "execution_permission_granted",
            "packet_used_as_action_basis",
            "formal_vault_accessed",
            "approval_collected_now",
            "real_user_text_stored",
            "write_performed",
            "sync_performed",
            "promotion_performed",
        ]:
            if binding.get(false_key) is not False:
                errors.append(f"p2_32_binding_flag_not_false:{false_key}")
        if binding.get("product_acceptance_status") != "pass_product_grade":
            errors.append("p2_32_product_acceptance_not_pass")
        if binding.get("reviewer_status") != "reviewer_pass":
            errors.append("p2_32_reviewer_not_pass")
        if binding.get("boundary_status") != "boundary_pass":
            errors.append("p2_32_boundary_not_pass")
        if binding.get("request_packet_hash") != binding.get("packet_receipt_hash"):
            errors.append("p2_32_packet_hash_receipt_mismatch")
    else:
        errors.append("p2_32_binding_not_object")

    screening_input = config.get("screening_input_packet")
    expected_input = expected_screening_input(mode) if mode in SCREENING_MODES else {}
    if screening_input != expected_input:
        errors.append("screening_input_packet_mismatch")
    if isinstance(screening_input, dict):
        errors.extend(check_keys("screening_input_packet", screening_input, SCREENING_INPUT_KEYS))
        if screening_input.get("packet_mode") != MODE_TO_PACKET_MODE.get(mode):
            errors.append("screening_input_packet_mode_mismatch")
        if screening_input.get("packet_result") != MODE_TO_PACKET_RESULT.get(mode):
            errors.append("screening_input_packet_result_mismatch")
        for false_key in [
            "actual_approval_collected",
            "actual_user_wording_stored",
            "commands_supplied",
            "absolute_paths_present",
            "requested_execution_now",
            "requested_action_basis",
            "packet_submitted",
        ]:
            if screening_input.get(false_key) is not False:
                errors.append(f"screening_input_flag_not_false:{false_key}")
        if screening_input.get("synthetic_only") is not True:
            errors.append("screening_input_not_synthetic")
        if not NON_CLAIMS.issubset(set(screening_input.get("non_claims", []))):
            errors.append("screening_input_non_claims_missing")
    else:
        errors.append("screening_input_packet_not_object")

    projection = config.get("screening_projection")
    expected_proj = expected_projection(mode) if mode in SCREENING_MODES else {}
    if projection != expected_proj:
        errors.append("screening_projection_mismatch")
    if isinstance(projection, dict):
        errors.extend(check_keys("screening_projection", projection, PROJECTION_KEYS))
        if projection.get("screening_result") != SCREENING_MODES.get(mode):
            errors.append("projection_screening_result_mismatch")
        if projection.get("projected_gate_result") != MODE_TO_GATE_RESULT.get(mode):
            errors.append("projection_gate_result_mismatch")
        for true_key in [
            "projection_matches_packet",
            "projection_is_not_submission",
            "projection_collects_no_approval",
            "projection_contains_no_commands",
            "projection_contains_no_formal_vault_paths",
        ]:
            if projection.get(true_key) is not True:
                errors.append(f"projection_flag_not_true:{true_key}")
    else:
        errors.append("screening_projection_not_object")

    checks = config.get("screening_checks")
    expected_status = SCREENING_CHECK_STATUS.get(mode, {})
    if not isinstance(checks, list):
        errors.append("screening_checks_missing")
        checks = []
    check_ids = [item.get("check_id") for item in checks if isinstance(item, dict)]
    if check_ids != SCREENING_CHECK_IDS:
        errors.append("screening_check_ids_mismatch")
    for index, check in enumerate(checks, start=1):
        if not isinstance(check, dict):
            errors.append("screening_check_not_object")
            continue
        check_id = check.get("check_id", "unknown")
        errors.extend(check_keys(f"screening_checks[{check_id}]", check, CHECK_KEYS))
        if check.get("sequence") != index:
            errors.append(f"screening_check_sequence_mismatch:{check_id}")
        if check.get("status") != expected_status.get(check_id):
            errors.append(f"screening_check_status_mismatch:{check_id}")
        if check.get("screened_now") is not True:
            errors.append(f"screening_check_screened_now_not_true:{check_id}")
        if check.get("collected_now") is not False:
            errors.append(f"screening_check_collected_now_not_false:{check_id}")
        if check.get("non_claim") != "screening_check_is_not_permission":
            errors.append(f"screening_check_non_claim_mismatch:{check_id}")

    receipt = config.get("screening_receipt")
    if not isinstance(receipt, dict):
        errors.append("screening_receipt_missing")
        receipt = {}
    errors.extend(check_keys("screening_receipt", receipt, RECEIPT_KEYS))
    if receipt.get("record_kind") != "sandbox_formal_vault_execution_request_screening_receipt":
        errors.append("receipt_record_kind_mismatch")
    if receipt.get("slice_id") != SLICE_ID:
        errors.append("receipt_slice_id_mismatch")
    if receipt.get("source_slice") != SOURCE_SLICE:
        errors.append("receipt_source_slice_mismatch")
    if receipt.get("screening_result") != SCREENING_MODES.get(mode):
        errors.append("receipt_screening_result_mismatch")
    if receipt.get("check_count") != len(SCREENING_CHECK_IDS):
        errors.append("receipt_check_count_mismatch")
    if receipt.get("source_count") != len(READ_ONLY_SOURCES):
        errors.append("receipt_source_count_mismatch")
    if receipt.get("request_screening_hash") != expected_screening_hash(config):
        errors.append("receipt_request_screening_hash_mismatch")
    for false_key in [
        "packet_submitted",
        "formal_vault_accessed",
        "formal_vault_state_inspected",
        "approval_collected_now",
        "actual_user_input_used",
        "actual_user_wording_stored",
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
        "screening_replayed",
        "screening_used_as_action_basis",
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
    if metrics.get("required_screening_checks") != len(SCREENING_CHECK_IDS):
        errors.append("metric_screening_checks_mismatch")
    if metrics.get("required_source_inputs") != len(READ_ONLY_SOURCES):
        errors.append("metric_source_inputs_mismatch")
    if metrics.get("manual_negative_probes") != 12:
        errors.append("metric_manual_negative_probes_mismatch")
    if metrics.get("max_journey_steps") != 3:
        errors.append("metric_max_journey_steps_mismatch")

    if config.get("request_screening_hash") != expected_screening_hash(config):
        errors.append("request_screening_hash_mismatch")
    return sorted(set(errors))


def validate_prototype_receipt(receipt: Any, config: dict[str, Any] | None = None) -> list[str]:
    errors = []
    if not isinstance(receipt, dict):
        return ["prototype_receipt_not_object"]
    errors.extend(check_keys("prototype_receipt", receipt, RECEIPT_KEYS))
    errors.extend(scan_dangerous_values(receipt, "$.prototype_receipt"))
    expected_config = config or current_valid_config()
    expected_hash = expected_config.get("request_screening_hash") if expected_config else None
    expected_result = expected_config.get("screening_projection", {}).get("screening_result") if expected_config else None
    if receipt.get("record_kind") != "sandbox_formal_vault_execution_request_screening_receipt":
        errors.append("prototype_receipt_record_kind_mismatch")
    if receipt.get("slice_id") != SLICE_ID:
        errors.append("prototype_receipt_slice_id_mismatch")
    if receipt.get("source_slice") != SOURCE_SLICE:
        errors.append("prototype_receipt_source_slice_mismatch")
    if expected_result and receipt.get("screening_result") != expected_result:
        errors.append("prototype_receipt_screening_result_mismatch")
    if receipt.get("check_count") != len(SCREENING_CHECK_IDS):
        errors.append("prototype_receipt_check_count_mismatch")
    if receipt.get("source_count") != len(READ_ONLY_SOURCES):
        errors.append("prototype_receipt_source_count_mismatch")
    if expected_hash and receipt.get("request_screening_hash") != expected_hash:
        errors.append("prototype_receipt_screening_hash_mismatch")
    for false_key in [
        "packet_submitted",
        "formal_vault_accessed",
        "formal_vault_state_inspected",
        "approval_collected_now",
        "actual_user_input_used",
        "actual_user_wording_stored",
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
        "screening_replayed",
        "screening_used_as_action_basis",
    ]:
        if receipt.get(false_key) is not False:
            errors.append(f"prototype_receipt_flag_not_false:{false_key}")
    if not NON_CLAIMS.issubset(set(receipt.get("non_claims", []))):
        errors.append("prototype_receipt_non_claims_missing")
    return sorted(set(errors))


def inspect_prototype() -> dict[str, Any]:
    prototype_path = ROOT / "prototype" / "formal-vault-execution-request-screening"
    receipt_path = prototype_path / "Receipts" / "formal-vault-execution-request-screening-receipt.json"
    html_path = prototype_path / "request-screening-inspector.html"
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
        issues.extend(validate_prototype_html_text("request-screening-inspector.html", html))
        lower = html.lower()
        buttons = re.findall(r"<button[^>]*data-filter=\"([^\"]+)\"[^>]*>([^<]+)</button>", html)
        html_summary = {
            "sandbox_only": 'data-sandbox-only="true"' in html,
            "screening_only": 'data-screening-only="true"' in html,
            "non_executable": 'data-non-executable="true"' in html,
            "no_formal_vault_access": 'data-no-formal-vault-access="true"' in html,
            "no_write": 'data-no-write="true"' in html,
            "no_sync": 'data-no-sync="true"' in html,
            "no_authority": 'data-no-authority="true"' in html,
            "no_permission": 'data-no-permission="true"' in html,
            "no_actual_user_wording": 'data-no-actual-user-wording="true"' in html,
            "no_submission": 'data-no-submission="true"' in html,
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
        "contract_file": (prototype_path / "01 Screening Contract.md").exists(),
        "checks_file": (prototype_path / "02 Screening Checks.md").exists(),
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
        return validate_prototype_html_text(tamper.get("file", "request-screening-inspector.html"), tamper.get("content", ""))
    receipt_path = ROOT / "prototype" / "formal-vault-execution-request-screening" / "Receipts" / "formal-vault-execution-request-screening-receipt.json"
    if receipt_path.exists():
        base_receipt = read_json_path(receipt_path)
    else:
        config = current_valid_config()
        base_receipt = copy.deepcopy(config.get("screening_receipt", {})) if config else {}
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
    config["request_screening_hash"] = ""
    if isinstance(config.get("screening_receipt"), dict):
        config["screening_receipt"]["request_screening_hash"] = ""
    screening_hash = expected_screening_hash(config)
    config["request_screening_hash"] = screening_hash
    if isinstance(config.get("screening_receipt"), dict):
        config["screening_receipt"]["request_screening_hash"] = screening_hash
    return config


def run_manual_negative_probes() -> dict[str, Any]:
    config = current_valid_config()
    if not config:
        return {"count": 0, "mismatches": ["missing_current_valid_config"], "probes": []}
    probes: list[dict[str, Any]] = []

    def add_probe(name: str, path: list[str], value: Any, expected: list[str]) -> None:
        candidate = copy.deepcopy(config)
        cursor: Any = candidate
        for part in path[:-1]:
            cursor = cursor[part]
        cursor[path[-1]] = value
        _rehash_for_probe(candidate)
        probes.append({"name": name, "expected_errors": expected, "actual_errors": validate_config(candidate)})

    add_probe("manual-screening-input-command", ["screening_input_packet", "packet_id"], "python tools/promote.py --sync", ["screening_input_packet_mismatch", "dangerous_value:$.screening_input_packet.packet_id:python_command", "dangerous_value:$.screening_input_packet.packet_id:promote_py", "dangerous_value:$.screening_input_packet.packet_id:sync_flag"])
    add_probe("manual-projection-submit-false", ["screening_projection", "projection_is_not_submission"], False, ["projection_flag_not_true:projection_is_not_submission", "screening_projection_mismatch"])
    add_probe("manual-projection-command", ["screening_projection", "projected_request_id"], "python tools/promote.py --sync", ["screening_projection_mismatch", "dangerous_value:$.screening_projection.projected_request_id:python_command", "dangerous_value:$.screening_projection.projected_request_id:promote_py", "dangerous_value:$.screening_projection.projected_request_id:sync_flag"])
    add_probe("manual-receipt-submitted", ["screening_receipt", "packet_submitted"], True, ["receipt_flag_not_false:packet_submitted"])
    add_probe("manual-receipt-permission", ["screening_receipt", "execution_permission_granted"], True, ["receipt_flag_not_false:execution_permission_granted"])

    prototype_probes = [
        ("manual-prototype-screening-submitted-yes", {"kind": "markdown_replace", "file": "03 Non Submission Receipt.md", "content": "screening submitted: yes"}, ["prototype_text_authority_confusion:03 Non Submission Receipt.md:screening_submitted_yes"]),
        ("manual-prototype-submit-screening", {"kind": "html_replace", "file": "request-screening-inspector.html", "content": "<html><body><button>Submit screening to gate</button></body></html>"}, ["prototype_text_authority_confusion:request-screening-inspector.html:submit_screening"]),
        ("manual-prototype-authorizes-execution", {"kind": "markdown_replace", "file": "01 Screening Contract.md", "content": "This screening authorizes the future execution slice."}, ["prototype_text_authority_confusion:01 Screening Contract.md:authorizes_execution"]),
        ("manual-prototype-actual-user-wording", {"kind": "markdown_replace", "file": "02 Screening Checks.md", "content": "actual user wording: approve execution now"}, ["prototype_text_dangerous:02 Screening Checks.md:actual_user_wording_marker"]),
        ("manual-prototype-approval-obtained", {"kind": "markdown_replace", "file": "03 Non Submission Receipt.md", "content": "Approval obtained from the user."}, ["prototype_text_authority_confusion:03 Non Submission Receipt.md:approval_obtained"]),
        ("manual-prototype-may-execute", {"kind": "markdown_replace", "file": "04 Stop Conditions.md", "content": "The operator may execute the formal vault operation."}, ["prototype_text_authority_confusion:04 Stop Conditions.md:may_execute"]),
        ("manual-prototype-html-missing-attrs", {"kind": "html_replace", "file": "request-screening-inspector.html", "content": "<html><body>Screening inspector</body></html>"}, ["html_missing_attr:data-sandbox-only=\"true\""]),
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

