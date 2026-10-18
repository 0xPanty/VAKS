from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p2-35-formal-vault-status-surface-handoff-packet-sandbox"
SOURCE_SLICE = "2026-06-15-p2-34-formal-vault-operator-status-surface-sandbox"
ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[3]

PURPOSE = (
    "Create a sandbox-only handoff packet for later agents to reuse the P2-34 "
    "operator status surface without treating status as approval, execution "
    "permission, action basis, reviewed knowledge, evidence support, mainline "
    "readiness, formal-vault authority, or dirty-tree repair."
)

READ_ONLY_SOURCES = [
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/slice-plan.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/source-map.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/verification.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/reviewer-report.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/boundary-audit.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/product-acceptance-report.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/next-step.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/artifact/formal-vault-operator-status-surface-contract.md",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/prototype/formal-vault-operator-status-surface/Receipts/operator-status-surface-receipt.json",
    f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/fixtures/valid-chain-overview-status-surface-config.json",
]

SOURCE_STATUS_EXPECTED = {
    "slice-plan.md": "built_pending_review",
    "source-map.md": "built_pending_review",
    "verification.md": "local_verification_passed_pending_review",
    "reviewer-report.md": "reviewer_pass",
    "boundary-audit.md": "boundary_pass",
    "product-acceptance-report.md": "pass_product_grade",
    "next-step.md": "pass_product_grade_pending_user_next_slice_decision",
}

HANDOFF_MODES = {
    "next_agent_read_only_handoff": "HANDOFF_PACKET_READY_FOR_READ_ONLY_NEXT_AGENT",
    "product_workflow_prebrief_handoff": "HANDOFF_PACKET_READY_FOR_SANDBOX_WORKFLOW_PROTOTYPE",
    "pause_or_park_handoff": "HANDOFF_PACKET_READY_FOR_STOP_OR_PARK_RECORD",
}

MODE_NEXT_TYPE = {
    "next_agent_read_only_handoff": "read_only_recovery_or_inspection",
    "product_workflow_prebrief_handoff": "fresh_sandbox_product_workflow_prototype",
    "pause_or_park_handoff": "fresh_sandbox_stop_or_park_record",
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
    "approval_collection",
    "user_instruction_collection",
    "user_wording_storage",
    "command_emitted",
    "absolute_vault_path_resolved",
    "execution_permission_granted",
    "execution_performed",
    "action_basis_creation",
    "reviewed_knowledge_creation",
    "evidence_support_creation",
    "mainline_merge",
    "dirty_tree_repair",
    "handoff_auto_advance",
]

CONTROL_EXPECTED = {
    "sandbox_only": True,
    "handoff_only": True,
    "read_only_source_bound": True,
    "fresh_sandbox_required_for_next_work": True,
    "non_executable": True,
    "no_formal_vault_access": True,
    "no_approval_collection": True,
    "no_user_instruction": True,
    "no_user_wording": True,
    "no_commands": True,
    "no_absolute_vault_paths": True,
    "no_truth_mutation": True,
    "no_mainline_claim": True,
    "status_surface_is_not_authority": True,
    "handoff_packet_is_not_authority": True,
    "product_acceptance_is_not_formal_vault_approval": True,
    "operator_must_stop_before_execution": True,
    "execution_allowed_now": False,
    "formal_vault_access_allowed_now": False,
    "approval_collected_now": False,
    "action_basis_ready": False,
    "reviewed_knowledge_created": False,
    "evidence_support_created": False,
    "mainline_ready": False,
    "dirty_tree_fixed": False,
    "auto_advance_allowed": False,
}

NON_CLAIMS = {
    "not formal vault approval",
    "not user instruction",
    "not execution permission",
    "not execution readiness",
    "not action basis",
    "not reviewed knowledge",
    "not evidence support",
    "not mainline readiness",
    "not merge approval",
    "not formal vault state",
    "not approval collection",
    "not user wording storage",
    "not a command surface",
    "not dirty tree repair",
    "not auto advance",
}

TOP_LEVEL_KEYS = {
    "slice_id",
    "source_slice",
    "handoff_packet_version",
    "truth_boundary",
    "purpose",
    "handoff_mode",
    "write_scope",
    "read_only_sources",
    "operations",
    "handoff_controls",
    "source_inputs",
    "source_statuses",
    "source_surface_binding",
    "handoff_payload",
    "handoff_checks",
    "handoff_receipt",
    "product_metrics",
    "handoff_packet_hash",
}
SOURCE_INPUT_KEYS = {"id", "source_path", "source_sha256", "content_binding"}
SOURCE_STATUS_KEYS = {"file", "expected_status", "actual_status"}
BINDING_KEYS = {
    "source_slice",
    "product_status",
    "reviewer_status",
    "boundary_status",
    "verification_status",
    "next_status",
    "surface_result",
    "source_slice_count",
    "source_input_count",
    "badge_count",
    "stop_line_count",
    "status_surface_hash",
    "formal_vault_accessed",
    "approval_collected_now",
    "user_instruction_collected",
    "user_wording_stored",
    "execution_permission_granted",
    "execution_performed",
    "write_performed",
    "sync_performed",
    "commit_performed",
    "push_performed",
    "promotion_performed",
    "mainline_ready",
    "status_used_as_action_basis",
    "dirty_tree_fixed",
}
PAYLOAD_KEYS = {
    "packet_id",
    "handoff_mode",
    "handoff_result",
    "source_surface_hash",
    "source_surface_result",
    "source_surface_stage_count",
    "next_work_type",
    "next_work_must_use_fresh_sandbox",
    "allowed_next_write_scope_pattern",
    "forbidden_next_actions",
    "required_next_checks",
    "operator_stop_summary",
    "actual_approval_collected",
    "actual_user_wording_stored",
    "commands_supplied",
    "formal_vault_paths_present",
    "execution_permission_granted",
    "handoff_used_as_action_basis",
    "mainline_ready",
    "dirty_tree_fixed",
    "non_claims",
}
CHECK_KEYS = {"check_id", "sequence", "status", "checked_now", "collected_now", "non_claim"}
RECEIPT_KEYS = {
    "record_kind",
    "slice_id",
    "source_slice",
    "handoff_result",
    "source_input_count",
    "check_count",
    "formal_vault_accessed",
    "approval_collected_now",
    "user_instruction_collected",
    "user_wording_stored",
    "execution_permission_granted",
    "execution_performed",
    "write_performed",
    "sync_performed",
    "commit_performed",
    "push_performed",
    "promotion_performed",
    "mainline_ready",
    "handoff_used_as_action_basis",
    "dirty_tree_fixed",
    "auto_advanced",
    "handoff_packet_hash",
    "non_claims",
}
METRIC_KEYS = {
    "required_positive_fixtures",
    "minimum_failure_cases",
    "required_source_inputs",
    "required_handoff_checks",
    "manual_negative_probes",
    "max_handoff_steps",
}

CHECK_IDS = [
    "p2_34_product_pass_present",
    "p2_34_surface_hash_bound",
    "p2_34_status_chain_visible",
    "handoff_requires_fresh_sandbox",
    "handoff_no_formal_vault",
    "handoff_no_approval_collection",
    "handoff_no_user_wording",
    "handoff_no_commands_or_paths",
    "handoff_not_action_basis",
    "handoff_not_mainline_ready",
]

PROTOTYPE_REQUIRED_FILES = [
    "00 Handoff Home.md",
    "01 Source Surface Binding.md",
    "02 Allowed Continuations.md",
    "03 Stop Conditions.md",
    "04 Reviewer Packet.md",
    "handoff-packet-inspector.html",
    "Receipts/handoff-packet-receipt.json",
]
PROTOTYPE_MARKDOWN_FILES = [
    "00 Handoff Home.md",
    "01 Source Surface Binding.md",
    "02 Allowed Continuations.md",
    "03 Stop Conditions.md",
    "04 Reviewer Packet.md",
]

DANGEROUS_VALUE_PATTERNS = [
    ("copy_item", re.compile(r"(?i)\bcopy-item\b")),
    ("robocopy", re.compile(r"(?i)\brobocopy\b")),
    ("powershell", re.compile(r"(?i)\bpowershell\b")),
    ("python_command", re.compile(r"(?i)\bpython(?:\.exe)?\b")),
    ("promote_py", re.compile(r"(?i)\bpromote\.py\b")),
    ("sync_flag", re.compile(r"(?i)--sync\b")),
    ("write_vault", re.compile(r"(?i)\bwrite-vault\b")),
    ("approve_now", re.compile(r"(?i)\bapprove-now\b")),
    ("execute_now", re.compile(r"(?i)\bexecute-now\b")),
    ("ready_to_execute", re.compile(r"(?i)\bready to execute\b")),
    ("approved_for_execution", re.compile(r"(?i)\bapproved for execution\b")),
    ("execution_permission_marker", re.compile(r"(?i)\bexecution permission\s*[:=]\s*(yes|true|granted|allowed|ready)\b")),
    ("formal_vault_approval_marker", re.compile(r"(?i)\bformal vault approval\s*[:=]\s*(yes|true|granted|allowed|ready)\b")),
    ("action_basis_marker", re.compile(r"(?i)\baction basis\s*[:=]\s*(yes|true|granted|allowed|ready)\b")),
    ("mainline_ready_marker", re.compile(r"(?i)\bmainline ready\s*[:=]\s*(yes|true|ready)\b")),
    ("merge_approved_marker", re.compile(r"(?i)\bmerge approved\s*[:=]\s*(yes|true)\b")),
    ("approval_collected_marker", re.compile(r"(?i)\bapproval collected\s*[:=]\s*(yes|true)\b")),
    ("actual_user_wording_marker", re.compile(r"(?i)\bactual user wording\s*[:=]")),
    ("absolute_formal_vault_path", re.compile(r"(?i)\b[A-Z]:[\\/][^\\n\\r]*Obsidian[\\/]")),
]

PROTOTYPE_SEMANTIC_DENY_PATTERNS = [
    ("authorizes_execution", re.compile(r"(?i)\bauthori[sz](?:es|ed|ation)?\b[^.\n]{0,80}\bexecution\b|\bexecution\b[^.\n]{0,80}\bauthori[sz](?:es|ed|ation)?\b")),
    ("may_execute", re.compile(r"(?i)\bmay execute\b")),
    ("start_execution", re.compile(r"(?i)\bstart execution\b")),
    ("run_now", re.compile(r"(?i)\brun now\b")),
    ("approval_obtained", re.compile(r"(?i)\bapproval obtained\b")),
    ("handoff_as_authority", re.compile(r"(?i)\bhandoff packet\b[^.\n]{0,80}\bauthority\b")),
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
    'data-handoff-only="true"',
    'data-non-executable="true"',
    'data-no-formal-vault-access="true"',
    'data-no-write="true"',
    'data-no-sync="true"',
    'data-no-authority="true"',
    'data-no-approval="true"',
    'data-no-user-wording="true"',
    'data-no-command="true"',
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


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


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


def validate_prototype_markdown_text(rel_path: str, text: str) -> list[str]:
    errors = scan_prototype_text(rel_path, text)
    if rel_path == "00 Handoff Home.md":
        for marker in [SOURCE_SLICE, "HANDOFF_PACKET_READY_FOR_READ_ONLY_NEXT_AGENT", "HANDOFF_PACKET_READY_FOR_SANDBOX_WORKFLOW_PROTOTYPE", "HANDOFF_PACKET_READY_FOR_STOP_OR_PARK_RECORD"]:
            if marker not in text:
                errors.append(f"prototype_markdown_missing_marker:{marker}")
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
    cards = re.findall(r"<article\b[^>]*data-kind=\"handoff\"[^>]*>", html)
    if len(cards) != len(HANDOFF_MODES):
        errors.append(f"html_handoff_card_count_mismatch:{len(cards)}:expected:{len(HANDOFF_MODES)}")
    for result in HANDOFF_MODES.values():
        if result not in html:
            errors.append(f"html_missing_handoff_result:{result}")
    if SOURCE_SLICE not in html:
        errors.append("html_missing_source_slice")
    return errors


def expected_source_inputs() -> list[dict[str, str]]:
    return [
        {"id": f"source_{index:02d}", "source_path": rel_path, "source_sha256": file_sha256(repo_path(rel_path)), "content_binding": "exact_source_sha256"}
        for index, rel_path in enumerate(READ_ONLY_SOURCES)
    ]


def expected_source_statuses() -> list[dict[str, str | None]]:
    base = repo_path(f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}")
    return [{"file": file_name, "expected_status": expected, "actual_status": frontmatter_status(base / file_name)} for file_name, expected in SOURCE_STATUS_EXPECTED.items()]


def source_receipt() -> dict[str, Any]:
    return read_json_path(repo_path(f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/prototype/formal-vault-operator-status-surface/Receipts/operator-status-surface-receipt.json"))


def expected_source_binding() -> dict[str, Any]:
    base = repo_path(f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}")
    receipt = source_receipt()
    return {
        "source_slice": SOURCE_SLICE,
        "product_status": frontmatter_status(base / "product-acceptance-report.md"),
        "reviewer_status": frontmatter_status(base / "reviewer-report.md"),
        "boundary_status": frontmatter_status(base / "boundary-audit.md"),
        "verification_status": frontmatter_status(base / "verification.md"),
        "next_status": frontmatter_status(base / "next-step.md"),
        "surface_result": receipt.get("surface_result"),
        "source_slice_count": receipt.get("source_slice_count"),
        "source_input_count": receipt.get("source_input_count"),
        "badge_count": receipt.get("badge_count"),
        "stop_line_count": receipt.get("stop_line_count"),
        "status_surface_hash": receipt.get("status_surface_hash"),
        "formal_vault_accessed": receipt.get("formal_vault_accessed"),
        "approval_collected_now": receipt.get("approval_collected_now"),
        "user_instruction_collected": receipt.get("user_instruction_collected"),
        "user_wording_stored": receipt.get("user_wording_stored"),
        "execution_permission_granted": receipt.get("execution_permission_granted"),
        "execution_performed": receipt.get("execution_performed"),
        "write_performed": receipt.get("write_performed"),
        "sync_performed": receipt.get("sync_performed"),
        "commit_performed": receipt.get("commit_performed"),
        "push_performed": receipt.get("push_performed"),
        "promotion_performed": receipt.get("promotion_performed"),
        "mainline_ready": receipt.get("mainline_ready"),
        "status_used_as_action_basis": receipt.get("status_used_as_action_basis"),
        "dirty_tree_fixed": receipt.get("dirty_tree_fixed"),
    }


def expected_payload(mode: str) -> dict[str, Any]:
    binding = expected_source_binding()
    return {
        "packet_id": f"{SLICE_ID}:{mode}",
        "handoff_mode": mode,
        "handoff_result": HANDOFF_MODES[mode],
        "source_surface_hash": binding["status_surface_hash"],
        "source_surface_result": binding["surface_result"],
        "source_surface_stage_count": binding["source_slice_count"],
        "next_work_type": MODE_NEXT_TYPE[mode],
        "next_work_must_use_fresh_sandbox": True,
        "allowed_next_write_scope_pattern": "outputs/review/vaks-implementation-sandbox/<date>-<slice-id>/",
        "forbidden_next_actions": sorted(OPERATION_KEYS),
        "required_next_checks": CHECK_IDS,
        "operator_stop_summary": "Stop before approval, commands, action basis, mainline, or formal vault access.",
        "actual_approval_collected": False,
        "actual_user_wording_stored": False,
        "commands_supplied": False,
        "formal_vault_paths_present": False,
        "execution_permission_granted": False,
        "handoff_used_as_action_basis": False,
        "mainline_ready": False,
        "dirty_tree_fixed": False,
        "non_claims": sorted(NON_CLAIMS),
    }


def expected_checks() -> list[dict[str, Any]]:
    return [{"check_id": check_id, "sequence": index, "status": "PASS", "checked_now": True, "collected_now": False, "non_claim": "handoff_check_is_not_authority"} for index, check_id in enumerate(CHECK_IDS, start=1)]


def expected_hash(config: dict[str, Any]) -> str:
    clone = copy.deepcopy(config)
    clone.pop("handoff_packet_hash", None)
    if isinstance(clone.get("handoff_receipt"), dict):
        clone["handoff_receipt"].pop("handoff_packet_hash", None)
    return canonical_hash(clone)


def current_valid_config() -> dict[str, Any] | None:
    path = ROOT / "fixtures" / "valid-next-agent-read-only-handoff-config.json"
    if not path.exists():
        return None
    return read_json_path(path)


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(config, dict):
        return ["config_not_object"]
    errors.extend(check_keys("config", config, TOP_LEVEL_KEYS))
    errors.extend(scan_dangerous_values(config))
    mode = config.get("handoff_mode")
    if config.get("slice_id") != SLICE_ID:
        errors.append("slice_id_mismatch")
    if config.get("source_slice") != SOURCE_SLICE:
        errors.append("source_slice_mismatch")
    if config.get("handoff_packet_version") != "p2-35-formal-vault-status-surface-handoff-packet-v1":
        errors.append("handoff_packet_version_mismatch")
    if config.get("truth_boundary") != "sandbox_only_handoff_packet_not_authority":
        errors.append("truth_boundary_mismatch")
    if config.get("purpose") != PURPOSE:
        errors.append("purpose_mismatch")
    if mode not in HANDOFF_MODES:
        errors.append("handoff_mode_not_allowed")
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

    controls = config.get("handoff_controls")
    if not isinstance(controls, dict):
        errors.append("handoff_controls_missing")
        controls = {}
    errors.extend(check_keys("handoff_controls", controls, set(CONTROL_EXPECTED)))
    for key, expected in CONTROL_EXPECTED.items():
        if controls.get(key) is not expected:
            errors.append(f"handoff_control_mismatch:{key}")

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

    binding = config.get("source_surface_binding")
    if binding != expected_source_binding():
        errors.append("source_surface_binding_mismatch")
    if isinstance(binding, dict):
        errors.extend(check_keys("source_surface_binding", binding, BINDING_KEYS))
        for status_key, expected in [("product_status", "pass_product_grade"), ("reviewer_status", "reviewer_pass"), ("boundary_status", "boundary_pass"), ("verification_status", "local_verification_passed_pending_review"), ("next_status", "pass_product_grade_pending_user_next_slice_decision")]:
            if binding.get(status_key) != expected:
                errors.append(f"source_binding_bad_status:{status_key}")
        for false_key in ["formal_vault_accessed", "approval_collected_now", "user_instruction_collected", "user_wording_stored", "execution_permission_granted", "execution_performed", "write_performed", "sync_performed", "commit_performed", "push_performed", "promotion_performed", "mainline_ready", "status_used_as_action_basis", "dirty_tree_fixed"]:
            if binding.get(false_key) is not False:
                errors.append(f"source_binding_flag_not_false:{false_key}")
    else:
        errors.append("source_surface_binding_not_object")

    payload = config.get("handoff_payload")
    expected = expected_payload(mode) if mode in HANDOFF_MODES else {}
    if payload != expected:
        errors.append("handoff_payload_mismatch")
    if isinstance(payload, dict):
        errors.extend(check_keys("handoff_payload", payload, PAYLOAD_KEYS))
        for false_key in ["actual_approval_collected", "actual_user_wording_stored", "commands_supplied", "formal_vault_paths_present", "execution_permission_granted", "handoff_used_as_action_basis", "mainline_ready", "dirty_tree_fixed"]:
            if payload.get(false_key) is not False:
                errors.append(f"handoff_payload_flag_not_false:{false_key}")
        if payload.get("next_work_must_use_fresh_sandbox") is not True:
            errors.append("handoff_payload_fresh_sandbox_not_true")
        if not NON_CLAIMS.issubset(set(payload.get("non_claims", []))):
            errors.append("handoff_payload_non_claims_missing")
    else:
        errors.append("handoff_payload_not_object")

    checks = config.get("handoff_checks")
    if checks != expected_checks():
        errors.append("handoff_checks_mismatch")
    if isinstance(checks, list):
        ids = [item.get("check_id") for item in checks if isinstance(item, dict)]
        if ids != CHECK_IDS:
            errors.append("handoff_check_ids_mismatch")
        for index, item in enumerate(checks, start=1):
            if not isinstance(item, dict):
                errors.append("handoff_check_not_object")
                continue
            errors.extend(check_keys(f"handoff_checks[{item.get('check_id', 'unknown')}]", item, CHECK_KEYS))
            if item.get("sequence") != index:
                errors.append(f"handoff_check_sequence_mismatch:{item.get('check_id')}")
            if item.get("status") != "PASS":
                errors.append(f"handoff_check_status_mismatch:{item.get('check_id')}")
            if item.get("checked_now") is not True:
                errors.append(f"handoff_check_checked_now_not_true:{item.get('check_id')}")
            if item.get("collected_now") is not False:
                errors.append(f"handoff_check_collected_now_not_false:{item.get('check_id')}")
    else:
        errors.append("handoff_checks_not_list")

    receipt = config.get("handoff_receipt")
    if not isinstance(receipt, dict):
        errors.append("handoff_receipt_missing")
        receipt = {}
    errors.extend(check_keys("handoff_receipt", receipt, RECEIPT_KEYS))
    if receipt.get("record_kind") != "sandbox_formal_vault_status_surface_handoff_packet_receipt":
        errors.append("receipt_record_kind_mismatch")
    if receipt.get("slice_id") != SLICE_ID:
        errors.append("receipt_slice_id_mismatch")
    if receipt.get("source_slice") != SOURCE_SLICE:
        errors.append("receipt_source_slice_mismatch")
    if receipt.get("handoff_result") != HANDOFF_MODES.get(mode):
        errors.append("receipt_handoff_result_mismatch")
    if receipt.get("source_input_count") != len(READ_ONLY_SOURCES):
        errors.append("receipt_source_input_count_mismatch")
    if receipt.get("check_count") != len(CHECK_IDS):
        errors.append("receipt_check_count_mismatch")
    if receipt.get("handoff_packet_hash") != expected_hash(config):
        errors.append("receipt_handoff_packet_hash_mismatch")
    for false_key in ["formal_vault_accessed", "approval_collected_now", "user_instruction_collected", "user_wording_stored", "execution_permission_granted", "execution_performed", "write_performed", "sync_performed", "commit_performed", "push_performed", "promotion_performed", "mainline_ready", "handoff_used_as_action_basis", "dirty_tree_fixed", "auto_advanced"]:
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
    if metrics.get("required_source_inputs") != len(READ_ONLY_SOURCES):
        errors.append("metric_source_inputs_mismatch")
    if metrics.get("required_handoff_checks") != len(CHECK_IDS):
        errors.append("metric_handoff_checks_mismatch")
    if metrics.get("manual_negative_probes") != 12:
        errors.append("metric_manual_negative_probes_mismatch")
    if metrics.get("max_handoff_steps") != 3:
        errors.append("metric_max_handoff_steps_mismatch")

    if config.get("handoff_packet_hash") != expected_hash(config):
        errors.append("handoff_packet_hash_mismatch")
    return sorted(set(errors))


def validate_prototype_receipt(receipt: Any, config: dict[str, Any] | None = None) -> list[str]:
    errors = []
    if not isinstance(receipt, dict):
        return ["prototype_receipt_not_object"]
    errors.extend(check_keys("prototype_receipt", receipt, RECEIPT_KEYS))
    errors.extend(scan_dangerous_values(receipt, "$.prototype_receipt"))
    expected_config = config or current_valid_config()
    expected_hash_value = expected_config.get("handoff_packet_hash") if expected_config else None
    expected_result = expected_config.get("handoff_receipt", {}).get("handoff_result") if expected_config else None
    if receipt.get("record_kind") != "sandbox_formal_vault_status_surface_handoff_packet_receipt":
        errors.append("prototype_receipt_record_kind_mismatch")
    if receipt.get("slice_id") != SLICE_ID:
        errors.append("prototype_receipt_slice_id_mismatch")
    if receipt.get("source_slice") != SOURCE_SLICE:
        errors.append("prototype_receipt_source_slice_mismatch")
    if expected_result and receipt.get("handoff_result") != expected_result:
        errors.append("prototype_receipt_handoff_result_mismatch")
    if receipt.get("source_input_count") != len(READ_ONLY_SOURCES):
        errors.append("prototype_receipt_source_input_count_mismatch")
    if receipt.get("check_count") != len(CHECK_IDS):
        errors.append("prototype_receipt_check_count_mismatch")
    if expected_hash_value and receipt.get("handoff_packet_hash") != expected_hash_value:
        errors.append("prototype_receipt_handoff_packet_hash_mismatch")
    for false_key in ["formal_vault_accessed", "approval_collected_now", "user_instruction_collected", "user_wording_stored", "execution_permission_granted", "execution_performed", "write_performed", "sync_performed", "commit_performed", "push_performed", "promotion_performed", "mainline_ready", "handoff_used_as_action_basis", "dirty_tree_fixed", "auto_advanced"]:
        if receipt.get(false_key) is not False:
            errors.append(f"prototype_receipt_flag_not_false:{false_key}")
    if not NON_CLAIMS.issubset(set(receipt.get("non_claims", []))):
        errors.append("prototype_receipt_non_claims_missing")
    return sorted(set(errors))


def inspect_prototype() -> dict[str, Any]:
    prototype_path = ROOT / "prototype" / "formal-vault-status-surface-handoff-packet"
    receipt_path = prototype_path / "Receipts" / "handoff-packet-receipt.json"
    html_path = prototype_path / "handoff-packet-inspector.html"
    issues = []
    for rel in PROTOTYPE_REQUIRED_FILES:
        if not (prototype_path / rel).exists():
            issues.append(f"missing_prototype_file:{rel}")
    for rel in PROTOTYPE_MARKDOWN_FILES:
        path = prototype_path / rel
        if path.exists():
            issues.extend(validate_prototype_markdown_text(rel, path.read_text(encoding="utf-8")))
    receipt = {}
    if receipt_path.exists():
        receipt = read_json_path(receipt_path)
        issues.extend(validate_prototype_receipt(receipt))
    else:
        issues.append("missing_prototype_receipt")
    html_summary = {}
    if html_path.exists():
        html = html_path.read_text(encoding="utf-8")
        issues.extend(validate_prototype_html_text("handoff-packet-inspector.html", html))
        lower = html.lower()
        buttons = re.findall(r"<button[^>]*data-filter=\"([^\"]+)\"[^>]*>([^<]+)</button>", html)
        html_summary = {
            "sandbox_only": 'data-sandbox-only="true"' in html,
            "handoff_only": 'data-handoff-only="true"' in html,
            "non_executable": 'data-non-executable="true"' in html,
            "no_formal_vault_access": 'data-no-formal-vault-access="true"' in html,
            "no_write": 'data-no-write="true"' in html,
            "no_sync": 'data-no-sync="true"' in html,
            "no_authority": 'data-no-authority="true"' in html,
            "no_approval": 'data-no-approval="true"' in html,
            "no_user_wording": 'data-no-user-wording="true"' in html,
            "no_command": 'data-no-command="true"' in html,
            "forms": lower.count("<form"),
            "downloads": lower.count("download="),
            "contenteditable": lower.count("contenteditable"),
            "anchors": lower.count("<a "),
            "buttons": [button[0] for button in buttons],
        }
    else:
        issues.append("missing_handoff_html")
    return {"prototype_path": str(prototype_path), "issues": sorted(set(issues)), "receipt": receipt, "html": html_summary}


def validate_prototype_tamper(tamper: dict[str, Any]) -> list[str]:
    if tamper.get("kind") == "markdown_replace":
        return validate_prototype_markdown_text(tamper.get("file", "unknown.md"), tamper.get("content", ""))
    if tamper.get("kind") == "html_replace":
        return validate_prototype_html_text(tamper.get("file", "handoff-packet-inspector.html"), tamper.get("content", ""))
    receipt_path = ROOT / "prototype" / "formal-vault-status-surface-handoff-packet" / "Receipts" / "handoff-packet-receipt.json"
    if receipt_path.exists():
        base_receipt = read_json_path(receipt_path)
    else:
        config = current_valid_config()
        base_receipt = copy.deepcopy(config.get("handoff_receipt", {})) if config else {}
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
    actual_files = sorted(path.name for path in (ROOT / "failure-cases").glob("*.json"))
    mismatches = []
    if set(actual_files) != set(expected_cases):
        for missing in sorted(set(expected_cases) - set(actual_files)):
            mismatches.append(f"missing_failure_case_file:{missing}")
        for extra in sorted(set(actual_files) - set(expected_cases)):
            mismatches.append(f"extra_failure_case_file:{extra}")
    for file_name in actual_files:
        payload = read_json_path(ROOT / "failure-cases" / file_name)
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
    config["handoff_packet_hash"] = ""
    if isinstance(config.get("handoff_receipt"), dict):
        config["handoff_receipt"]["handoff_packet_hash"] = ""
    packet_hash = expected_hash(config)
    config["handoff_packet_hash"] = packet_hash
    if isinstance(config.get("handoff_receipt"), dict):
        config["handoff_receipt"]["handoff_packet_hash"] = packet_hash
    return config


def run_manual_negative_probes() -> dict[str, Any]:
    config = current_valid_config()
    if not config:
        return {"count": 0, "mismatches": ["missing_current_valid_config"], "probes": []}
    probes: list[dict[str, Any]] = []

    def add_probe(name: str, path: list[Any], value: Any, expected: list[str]) -> None:
        candidate = copy.deepcopy(config)
        cursor: Any = candidate
        for part in path[:-1]:
            cursor = cursor[part]
        cursor[path[-1]] = value
        _rehash_for_probe(candidate)
        probes.append({"name": name, "expected_errors": expected, "actual_errors": validate_config(candidate)})

    add_probe("manual-operation-command", ["operations", "command_emitted"], True, ["operation_not_false:command_emitted"])
    add_probe("manual-control-auto-advance", ["handoff_controls", "auto_advance_allowed"], True, ["handoff_control_mismatch:auto_advance_allowed"])
    add_probe("manual-payload-action-basis", ["handoff_payload", "handoff_used_as_action_basis"], True, ["handoff_payload_flag_not_false:handoff_used_as_action_basis", "handoff_payload_mismatch"])
    add_probe("manual-binding-mainline", ["source_surface_binding", "mainline_ready"], True, ["source_binding_flag_not_false:mainline_ready", "source_surface_binding_mismatch"])
    add_probe("manual-receipt-permission", ["handoff_receipt", "execution_permission_granted"], True, ["receipt_flag_not_false:execution_permission_granted"])

    prototype_probes = [
        ("manual-prototype-missing-home-markers", {"kind": "markdown_replace", "file": "00 Handoff Home.md", "content": "# Handoff\n\nGeneric."}, ["prototype_markdown_missing_marker:" + SOURCE_SLICE]),
        ("manual-prototype-command", {"kind": "html_replace", "file": "handoff-packet-inspector.html", "content": "<html><body>python tools/promote.py --sync</body></html>"}, ["prototype_text_dangerous:handoff-packet-inspector.html:python_command"]),
        ("manual-prototype-run-now", {"kind": "html_replace", "file": "handoff-packet-inspector.html", "content": "<html><body><button>Run now</button></body></html>"}, ["prototype_text_authority_confusion:handoff-packet-inspector.html:run_now"]),
        ("manual-prototype-approval", {"kind": "markdown_replace", "file": "03 Stop Conditions.md", "content": "approval collected: yes"}, ["prototype_text_dangerous:03 Stop Conditions.md:approval_collected_marker"]),
        ("manual-prototype-mainline", {"kind": "markdown_replace", "file": "02 Allowed Continuations.md", "content": "mainline ready: yes"}, ["prototype_text_dangerous:02 Allowed Continuations.md:mainline_ready_marker"]),
        ("manual-prototype-receipt-action-basis", {"kind": "receipt_update", "updates": {"handoff_used_as_action_basis": True}}, ["prototype_receipt_flag_not_false:handoff_used_as_action_basis"]),
        ("manual-prototype-receipt-count", {"kind": "receipt_update", "updates": {"check_count": 99}}, ["prototype_receipt_check_count_mismatch"]),
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


def check_required_reports(final_gate: bool) -> dict[str, Any]:
    statuses = {}
    issues = []
    expected_statuses = REQUIRED_REPORT_STATUSES if final_gate else PRE_FINAL_REPORT_STATUSES
    for name, expected in expected_statuses.items():
        actual = frontmatter_status(ROOT / name)
        statuses[name] = actual
        if actual != expected:
            if final_gate:
                issues.append(f"final_gate_bad_status:{name}:{actual}:expected:{expected}")
            elif actual is None:
                issues.append(f"missing_report:{name}")
    return {"statuses": statuses, "issues": issues}
