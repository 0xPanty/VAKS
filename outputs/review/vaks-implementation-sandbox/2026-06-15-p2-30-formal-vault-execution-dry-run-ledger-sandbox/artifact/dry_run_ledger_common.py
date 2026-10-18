from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

SLICE_ID = "2026-06-15-p2-30-formal-vault-execution-dry-run-ledger-sandbox"
SOURCE_SLICE = "2026-06-15-p2-29-formal-vault-execution-plan-sandbox"
PREV_ROOT_REL = f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}"
ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[3]

PREV_FIXTURE_REL = f"{PREV_ROOT_REL}/fixtures/valid-execution-plan-config.json"
PREV_RECEIPT_REL = (
    f"{PREV_ROOT_REL}/prototype/formal-vault-execution-plan-sandbox/"
    "Receipts/formal-vault-execution-plan-receipt.json"
)

LEDGER_PURPOSE = (
    "Record a dry-run ledger for a future formal-vault execution plan without "
    "performing formal vault access, state inspection, hash collection, writes, sync, or commands."
)

ALLOWED_LEDGER_MODES = {
    "approved_plan_dry_run_ledger",
    "denial_block_ledger",
    "revision_block_ledger",
}

SOURCE_FILES = [
    ("p2_29_next_step", f"{PREV_ROOT_REL}/next-step.md"),
    ("p2_29_product_acceptance", f"{PREV_ROOT_REL}/product-acceptance-report.md"),
    ("p2_29_verification", f"{PREV_ROOT_REL}/verification.md"),
    ("p2_29_reviewer_report", f"{PREV_ROOT_REL}/reviewer-report.md"),
    ("p2_29_boundary_audit", f"{PREV_ROOT_REL}/boundary-audit.md"),
    ("p2_29_source_map", f"{PREV_ROOT_REL}/source-map.md"),
    ("p2_29_plan_fixture", PREV_FIXTURE_REL),
    ("p2_29_plan_receipt", PREV_RECEIPT_REL),
    ("p2_29_contract", f"{PREV_ROOT_REL}/artifact/formal-vault-execution-plan-contract.md"),
]

FORBIDDEN_OPERATIONS = [
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
    "ledger_promoted_to_execution_log",
    "ledger_used_as_action_basis",
]

REQUIRED_LEDGER_CONTROLS_TRUE = [
    "sandbox_only",
    "dry_run_only",
    "ledger_only",
    "non_executable",
    "operator_must_stop_before_execution",
    "separate_future_user_confirmation_required",
    "separate_future_execution_slice_required",
    "validator_is_not_reviewer",
    "product_acceptance_is_not_formal_vault_approval",
    "plan_pass_is_not_execution_permission",
    "dry_run_ledger_is_not_execution_log",
    "dirty_state_blocks_execution",
]

REQUIRED_LEDGER_CONTROLS_FALSE = [
    "execution_allowed_now",
    "formal_vault_access_allowed_now",
    "formal_vault_state_check_allowed_now",
    "formal_vault_write_allowed_now",
    "formal_vault_hash_allowed_now",
    "formal_vault_snapshot_allowed_now",
    "user_confirmation_collected_now",
    "actual_user_text_stored",
    "contains_commands",
    "command_export_enabled",
    "copy_paste_command_enabled",
    "absolute_vault_paths_present",
    "sync_commit_push_promotion_allowed",
    "ledger_can_be_replayed",
    "ledger_is_action_basis",
]

REQUIRED_ENTRY_RESULTS = {
    "source_binding_reconfirm": "DRY_RUN_RECORDED_NOT_PERFORMED",
    "target_manifest_reconfirm": "DRY_RUN_RECORDED_NOT_PERFORMED",
    "future_formal_vault_state_check": "BLOCKED_FUTURE_ONLY_NOT_PERFORMED",
    "future_snapshot_plan": "BLOCKED_FUTURE_ONLY_NOT_PERFORMED",
    "future_write_plan": "BLOCKED_FUTURE_ONLY_NOT_PERFORMED",
    "future_hash_after_plan": "BLOCKED_FUTURE_ONLY_NOT_PERFORMED",
    "future_sync_plan": "BLOCKED_FUTURE_ONLY_NOT_PERFORMED",
    "future_rollback_plan": "BLOCKED_FUTURE_ONLY_NOT_PERFORMED",
    "future_closeout_plan": "DRY_RUN_RECORDED_NOT_PERFORMED",
}

REQUIRED_ENTRY_QUESTIONS = {
    "source_binding_reconfirm": "Would a future execution re-check P2-29 source hashes?",
    "target_manifest_reconfirm": "Would a future execution re-check target manifest exactness?",
    "future_formal_vault_state_check": "Would a future execution inspect formal vault state?",
    "future_snapshot_plan": "Would a future execution snapshot targets before writing?",
    "future_write_plan": "Would a future execution write only approved targets?",
    "future_hash_after_plan": "Would a future execution compare after hashes?",
    "future_sync_plan": "Would a future execution consider sync only after write review?",
    "future_rollback_plan": "Would a future execution have rollback evidence?",
    "future_closeout_plan": "Would a future execution close out with evidence and non-claims?",
}

REQUIRED_SAMPLE_BINDINGS = {
    "synthetic_approved_plan_ledger": ("approved_plan_draft", "approved_plan_dry_run_ledger", True),
    "synthetic_denied_plan_ledger": ("denial_block_record", "denial_block_ledger", True),
    "synthetic_revision_plan_ledger": ("revision_block_record", "revision_block_ledger", True),
}

REQUIRED_STOP_CONDITIONS = [
    "actual user approval collection requested",
    "formal vault read or scan requested",
    "formal vault write requested",
    "formal vault state inspection requested",
    "formal vault hash or snapshot requested",
    "absolute vault path requested",
    "copy/write/sync command requested",
    "Obsidian sync requested",
    "commit or push requested",
    "promotion requested",
    "execution requested",
    "ledger replay requested",
    "ledger treated as action basis",
    "plan hash mismatch",
    "ledger entry sequence mismatch",
    "dirty-state acknowledgement missing",
]

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
    "reviewer-report.md": "pending",
    "boundary-audit.md": "pending",
    "product-acceptance-report.md": "pending",
    "next-step.md": "pending",
}

TOP_LEVEL_KEYS = {
    "slice_id",
    "source_slice",
    "dry_run_ledger_version",
    "truth_boundary",
    "purpose",
    "ledger_mode",
    "write_scope",
    "read_only_sources",
    "operations",
    "ledger_controls",
    "source_inputs",
    "source_input_bundle_hash",
    "source_plan_hash",
    "source_plan_input_bundle_hash",
    "source_target_manifest_hash",
    "source_plan_receipt_hash",
    "source_ledger_plan_contract_hash",
    "target_manifest",
    "target_manifest_hash",
    "dry_run_ledger_contract",
    "ledger_entries",
    "ledger_samples",
    "non_execution_ledger_receipt",
    "stop_conditions",
    "product_metrics",
    "dry_run_ledger_hash",
}

SOURCE_INPUT_KEYS = {"id", "source_path", "source_sha256", "content_binding"}
TARGET_KEYS = {
    "id",
    "relative_target",
    "source_path",
    "source_sha256",
    "content_binding",
    "source_plan_status",
    "ledger_target_status",
    "formal_vault_target_resolved",
    "formal_vault_target_exists_checked",
    "hash_before_collected",
    "hash_after_collected",
    "write_enabled_now",
    "execution_enabled_now",
}
CONTRACT_KEYS = {
    "contract_kind",
    "current_slice_executes",
    "current_slice_collects_approval",
    "formal_vault_access_disallowed",
    "formal_vault_state_inspection_disallowed",
    "formal_vault_write_disallowed",
    "formal_vault_hash_disallowed",
    "formal_vault_snapshot_disallowed",
    "ledger_is_non_executable",
    "ledger_is_not_execution_log",
    "ledger_is_not_action_basis",
    "separate_future_execution_slice_required",
    "separate_final_user_confirmation_required",
    "plan_pass_not_execution_permission",
    "default_result",
    "required_plan_hash",
    "required_plan_contract_hash",
    "required_scope_ids",
    "required_entry_ids",
}
ENTRY_KEYS = {
    "entry_id",
    "source_step_id",
    "sequence",
    "review_question",
    "dry_run_result",
    "perform_now",
    "writes_now",
    "formal_vault_access_now",
    "formal_vault_state_check_now",
    "hash_now",
    "snapshot_now",
    "sync_now",
    "commit_now",
    "push_now",
    "promotion_now",
    "requires_future_user_confirmation",
    "requires_future_execution_slice",
    "command",
    "absolute_target_path",
    "copy_tool",
    "evidence_recorded",
    "non_claim",
}
SAMPLE_KEYS = {
    "id",
    "source_plan_scenario",
    "ledger_mode",
    "ledger_created",
    "ledger_replayable",
    "ledger_is_execution_log",
    "expected_ledger_result",
    "actual_user_input",
    "approval_collected_now",
    "real_user_text_stored",
    "formal_vault_accessed",
    "formal_vault_state_inspected",
    "snapshot_taken",
    "hash_before_collected",
    "hash_after_collected",
    "execution_performed",
    "formal_vault_write_allowed_now",
    "action_basis_created",
    "reviewed_knowledge_created",
    "sync_allowed",
    "commit_allowed",
    "push_allowed",
    "promotion_allowed",
    "entry_count",
    "scope_ids",
    "synthetic_only",
}
RECEIPT_KEYS = {
    "approval_collected_now",
    "actual_user_input_used",
    "real_user_text_stored",
    "formal_vault_accessed",
    "formal_vault_state_inspected",
    "execution_performed",
    "snapshot_taken",
    "hash_before_collected",
    "hash_after_collected",
    "write_performed",
    "sync_performed",
    "commit_performed",
    "push_performed",
    "promotion_performed",
    "ledger_replayed",
    "ledger_used_as_action_basis",
    "current_status",
    "non_claims",
}
PRODUCT_METRIC_KEYS = {
    "required_positive_fixtures",
    "minimum_failure_cases",
    "required_ledger_samples",
    "required_targets",
    "required_entries",
    "max_journey_steps",
}

PROTOTYPE_REQUIRED_FILES = [
    "00 Dry Run Ledger Home.md",
    "01 Ledger Contract.md",
    "02 Ledger Entries.md",
    "03 Non Execution Receipt.md",
    "04 Stop Conditions.md",
    "05 Reviewer Packet.md",
    "dry-run-ledger-inspector.html",
    "Receipts/formal-vault-execution-dry-run-ledger-receipt.json",
]

PROTOTYPE_MARKDOWN_FILES = [
    "00 Dry Run Ledger Home.md",
    "01 Ledger Contract.md",
    "02 Ledger Entries.md",
    "03 Non Execution Receipt.md",
    "04 Stop Conditions.md",
    "05 Reviewer Packet.md",
]

PROTOTYPE_RECEIPT_KEYS = {
    "record_kind",
    "slice_id",
    "source_slice",
    "generated_at_utc",
    "formal_vault_accessed",
    "formal_vault_state_inspected",
    "approval_collected_now",
    "actual_user_input_used",
    "real_user_text_stored",
    "execution_performed",
    "write_performed",
    "snapshot_taken",
    "hash_before_collected",
    "hash_after_collected",
    "sync_performed",
    "commit_performed",
    "push_performed",
    "promotion_performed",
    "ledger_replayed",
    "ledger_used_as_action_basis",
    "entry_count",
    "target_count",
    "ledger_hash",
    "non_claims",
}

REQUIRED_PROTOTYPE_NON_CLAIMS = {
    "not actual approval",
    "not execution readiness",
    "not formal vault approval",
    "not action basis",
    "not reviewed knowledge",
    "not evidence support",
    "not an execution log",
    "not replayable",
}

PROTOTYPE_SEMANTIC_DENY_PATTERNS = [
    ("ready_to_execute", re.compile(r"(?i)\bready to execute\b")),
    ("approved_to_execute", re.compile(r"(?i)\bapproved to execute\b")),
    ("formal_vault_approval_granted", re.compile(r"(?i)\bformal vault approval granted\b")),
    ("is_action_basis", re.compile(r"(?i)\bis action basis\b")),
    ("is_execution_log", re.compile(r"(?i)\bis an execution log\b|\bis execution log\b")),
    ("replayable_command", re.compile(r"(?i)\breplayable command\b")),
]

DANGEROUS_VALUE_PATTERNS = [
    ("copy_item", re.compile(r"(?i)\bcopy-item\b")),
    ("robocopy", re.compile(r"(?i)\brobocopy\b")),
    ("xcopy", re.compile(r"(?i)\bxcopy\b")),
    ("powershell", re.compile(r"(?i)\bpowershell\b")),
    ("pwsh", re.compile(r"(?i)\bpwsh\b")),
    ("cmd_exe", re.compile(r"(?i)\bcmd\.exe\b")),
    ("start_process", re.compile(r"(?i)\bstart-process\b")),
    ("write_vault", re.compile(r"(?i)\bwrite-vault\b")),
    ("approve_now", re.compile(r"(?i)\bapprove-now\b")),
    ("absolute_formal_vault_path", re.compile(r"(?i)\b[A-Z]:[\\/][^\\n\\r]*Obsidian[\\/]")),
]


def repo_path(rel_path: str) -> Path:
    return REPO_ROOT / rel_path.replace("/", "\\")


def read_text(rel_path: str) -> str:
    return repo_path(rel_path).read_text(encoding="utf-8")


def read_json_path(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_json_rel(rel_path: str) -> Any:
    return read_json_path(repo_path(rel_path))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.replace("\r\n", "\n"), encoding="utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(rel_path: str) -> str:
    return hashlib.sha256(repo_path(rel_path).read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_hash(value: Any) -> str:
    return sha256_text(canonical_json(value))


def source_inputs() -> list[dict[str, str]]:
    return [
        {
            "id": item_id,
            "source_path": rel_path,
            "source_sha256": sha256_file(rel_path),
            "content_binding": "exact_source_sha256",
        }
        for item_id, rel_path in SOURCE_FILES
    ]


def status_from_markdown(rel_path: str) -> str | None:
    match = re.search(r"(?m)^status:\s*([A-Za-z0-9_\-]+)\s*$", read_text(rel_path))
    return match.group(1) if match else None


def load_prev_fixture() -> dict[str, Any]:
    return read_json_rel(PREV_FIXTURE_REL)


def load_prev_receipt() -> dict[str, Any]:
    return read_json_rel(PREV_RECEIPT_REL)


def expected_source_input_bundle_hash(inputs: list[dict[str, str]]) -> str:
    return canonical_hash(inputs)


def expected_ledger_hash_material(config: dict[str, Any]) -> dict[str, Any]:
    material = json.loads(canonical_json(config))
    material.pop("dry_run_ledger_hash", None)
    return material


def expected_ledger_hash(config: dict[str, Any]) -> str:
    return canonical_hash(expected_ledger_hash_material(config))


def is_relative_safe(path_value: str) -> bool:
    if not isinstance(path_value, str) or not path_value:
        return False
    if "\\" in path_value:
        return False
    if re.match(r"^[A-Za-z]:", path_value):
        return False
    pure = PurePosixPath(path_value)
    if pure.is_absolute():
        return False
    return ".." not in pure.parts


def check_keys(name: str, value: Any, allowed: set[str]) -> list[str]:
    if not isinstance(value, dict):
        return []
    errors = []
    actual = set(value)
    for extra in sorted(actual - allowed):
        errors.append(f"unknown_key:{name}:{extra}")
    for missing in sorted(allowed - actual):
        errors.append(f"missing_key:{name}:{missing}")
    return errors


def scan_dangerous_values(value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if path == "$" and key not in TOP_LEVEL_KEYS:
                errors.append(f"unknown_top_level_key:{key}")
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


def current_valid_config() -> dict[str, Any] | None:
    fixture_path = ROOT / "fixtures" / "valid-dry-run-ledger-config.json"
    if not fixture_path.exists():
        return None
    return read_json_path(fixture_path)


def validate_prototype_receipt(receipt: Any, config: dict[str, Any] | None = None) -> list[str]:
    errors = []
    if not isinstance(receipt, dict):
        return ["prototype_receipt_not_object"]
    errors.extend(check_keys("prototype_receipt", receipt, PROTOTYPE_RECEIPT_KEYS))
    errors.extend(scan_dangerous_values(receipt, "$.prototype_receipt"))
    if receipt.get("record_kind") != "sandbox_formal_vault_execution_dry_run_ledger_receipt":
        errors.append("prototype_receipt_record_kind_mismatch")
    if receipt.get("slice_id") != SLICE_ID:
        errors.append("prototype_receipt_slice_id_mismatch")
    if receipt.get("source_slice") != SOURCE_SLICE:
        errors.append("prototype_receipt_source_slice_mismatch")
    expected_config = config or current_valid_config()
    expected_entry_count = len(REQUIRED_ENTRY_RESULTS)
    expected_target_count = 5
    expected_hash = expected_config.get("dry_run_ledger_hash") if expected_config else None
    if receipt.get("entry_count") != expected_entry_count:
        errors.append("prototype_receipt_entry_count_mismatch")
    if receipt.get("target_count") != expected_target_count:
        errors.append("prototype_receipt_target_count_mismatch")
    if expected_hash and receipt.get("ledger_hash") != expected_hash:
        errors.append("prototype_receipt_ledger_hash_mismatch")
    for false_key in [
        "formal_vault_accessed",
        "formal_vault_state_inspected",
        "approval_collected_now",
        "actual_user_input_used",
        "real_user_text_stored",
        "execution_performed",
        "write_performed",
        "snapshot_taken",
        "hash_before_collected",
        "hash_after_collected",
        "sync_performed",
        "commit_performed",
        "push_performed",
        "promotion_performed",
        "ledger_replayed",
        "ledger_used_as_action_basis",
    ]:
        if receipt.get(false_key) is not False:
            errors.append(f"prototype_receipt_flag_not_false:{false_key}")
    if not REQUIRED_PROTOTYPE_NON_CLAIMS.issubset(set(receipt.get("non_claims", []))):
        errors.append("prototype_receipt_non_claims_missing")
    return sorted(set(errors))


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(config, dict):
        return ["config_not_object"]
    prev = load_prev_fixture()
    receipt = load_prev_receipt()

    errors.extend(check_keys("config", config, TOP_LEVEL_KEYS))
    errors.extend(scan_dangerous_values(config))

    if config.get("slice_id") != SLICE_ID:
        errors.append("slice_id_mismatch")
    if config.get("source_slice") != SOURCE_SLICE:
        errors.append("source_slice_mismatch")
    if config.get("dry_run_ledger_version") != "p2-30-formal-vault-execution-dry-run-ledger-v1":
        errors.append("ledger_version_mismatch")
    if config.get("truth_boundary") != "sandbox_only_non_executing_ledger":
        errors.append("truth_boundary_mismatch")
    if config.get("purpose") != LEDGER_PURPOSE:
        errors.append("purpose_mismatch")
    if config.get("ledger_mode") not in ALLOWED_LEDGER_MODES:
        errors.append("ledger_mode_not_allowed")

    expected_scope = [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"]
    if config.get("write_scope") != expected_scope:
        errors.append("write_scope_mismatch")

    operations = config.get("operations")
    if not isinstance(operations, dict):
        errors.append("operations_missing")
        operations = {}
    errors.extend(check_keys("operations", operations, set(FORBIDDEN_OPERATIONS)))
    for key in FORBIDDEN_OPERATIONS:
        if operations.get(key) is not False:
            errors.append(f"forbidden_operation_enabled:{key}")

    controls = config.get("ledger_controls")
    if not isinstance(controls, dict):
        errors.append("ledger_controls_missing")
        controls = {}
    errors.extend(check_keys("ledger_controls", controls, set(REQUIRED_LEDGER_CONTROLS_TRUE + REQUIRED_LEDGER_CONTROLS_FALSE)))
    for key in REQUIRED_LEDGER_CONTROLS_TRUE:
        if controls.get(key) is not True:
            errors.append(f"ledger_control_not_true:{key}")
    for key in REQUIRED_LEDGER_CONTROLS_FALSE:
        if controls.get(key) is not False:
            errors.append(f"ledger_control_not_false:{key}")

    if status_from_markdown(f"{PREV_ROOT_REL}/product-acceptance-report.md") != "pass_product_grade":
        errors.append("source_product_not_pass")
    if status_from_markdown(f"{PREV_ROOT_REL}/next-step.md") != "pass_product_grade_pending_user_next_slice_decision":
        errors.append("source_next_step_not_pass")

    expected_inputs = source_inputs()
    actual_inputs = config.get("source_inputs")
    if actual_inputs != expected_inputs:
        errors.append("source_inputs_mismatch")
    expected_read_only_sources = [item["source_path"] for item in expected_inputs]
    if config.get("read_only_sources") != expected_read_only_sources:
        errors.append("read_only_sources_mismatch")
    if isinstance(actual_inputs, list):
        for index, item in enumerate(actual_inputs):
            errors.extend(check_keys(f"source_inputs[{index}]", item, SOURCE_INPUT_KEYS))
    if config.get("source_input_bundle_hash") != expected_source_input_bundle_hash(expected_inputs):
        errors.append("source_input_bundle_hash_mismatch")

    expected_source_claims = {
        "source_plan_hash": prev.get("execution_plan_hash"),
        "source_plan_input_bundle_hash": prev.get("source_input_bundle_hash"),
        "source_target_manifest_hash": prev.get("target_manifest_hash"),
        "source_plan_receipt_hash": receipt.get("plan_hash"),
        "source_ledger_plan_contract_hash": sha256_file(f"{PREV_ROOT_REL}/artifact/formal-vault-execution-plan-contract.md"),
    }
    for key, expected in expected_source_claims.items():
        if config.get(key) != expected:
            errors.append(f"source_hash_claim_mismatch:{key}")
    if receipt.get("formal_vault_accessed") is not False:
        errors.append("source_receipt_formal_vault_accessed")
    if receipt.get("execution_performed") is not False:
        errors.append("source_receipt_execution_performed")

    expected_targets = {item["id"]: item for item in prev.get("target_manifest", [])}
    targets = config.get("target_manifest")
    if not isinstance(targets, list):
        errors.append("target_manifest_missing")
        targets = []
    actual_ids = [item.get("id") for item in targets if isinstance(item, dict)]
    if set(actual_ids) != set(expected_targets):
        errors.append("target_scope_ids_mismatch")
    if len(actual_ids) != len(set(actual_ids)):
        errors.append("target_scope_duplicate_ids")
    for target in targets:
        if not isinstance(target, dict):
            errors.append("target_item_not_object")
            continue
        target_id = target.get("id")
        errors.extend(check_keys(f"target_manifest[{target_id}]", target, TARGET_KEYS))
        expected = expected_targets.get(target_id)
        if expected is None:
            errors.append(f"target_not_in_plan_scope:{target_id}")
            continue
        for field in ["relative_target", "source_path", "source_sha256", "content_binding"]:
            if target.get(field) != expected.get(field):
                errors.append(f"target_{field}_mismatch:{target_id}")
        if target.get("source_plan_status") != expected.get("plan_status"):
            errors.append(f"target_source_plan_status_mismatch:{target_id}")
        if target.get("ledger_target_status") != "dry_run_recorded_not_performed":
            errors.append(f"target_ledger_status_mismatch:{target_id}")
        if not is_relative_safe(target.get("relative_target", "")):
            errors.append(f"target_relative_path_unsafe:{target_id}")
        for false_key in [
            "formal_vault_target_resolved",
            "formal_vault_target_exists_checked",
            "hash_before_collected",
            "hash_after_collected",
            "write_enabled_now",
            "execution_enabled_now",
        ]:
            if target.get(false_key) is not False:
                errors.append(f"target_flag_not_false:{target_id}:{false_key}")
    if config.get("target_manifest_hash") != canonical_hash(targets):
        errors.append("target_manifest_hash_mismatch")

    contract = config.get("dry_run_ledger_contract")
    if not isinstance(contract, dict):
        errors.append("dry_run_ledger_contract_missing")
        contract = {}
    errors.extend(check_keys("dry_run_ledger_contract", contract, CONTRACT_KEYS))
    expected_contract = {
        "contract_kind": "formal_vault_execution_dry_run_ledger_sandbox",
        "current_slice_executes": False,
        "current_slice_collects_approval": False,
        "formal_vault_access_disallowed": True,
        "formal_vault_state_inspection_disallowed": True,
        "formal_vault_write_disallowed": True,
        "formal_vault_hash_disallowed": True,
        "formal_vault_snapshot_disallowed": True,
        "ledger_is_non_executable": True,
        "ledger_is_not_execution_log": True,
        "ledger_is_not_action_basis": True,
        "separate_future_execution_slice_required": True,
        "separate_final_user_confirmation_required": True,
        "plan_pass_not_execution_permission": True,
        "default_result": "LEDGER_DRY_RUN_ONLY_NOT_EXECUTABLE",
    }
    for key, expected in expected_contract.items():
        if contract.get(key) != expected:
            errors.append(f"contract_field_mismatch:{key}")
    if contract.get("required_plan_hash") != prev.get("execution_plan_hash"):
        errors.append("contract_required_plan_hash_mismatch")
    if contract.get("required_plan_contract_hash") != config.get("source_ledger_plan_contract_hash"):
        errors.append("contract_required_plan_contract_hash_mismatch")
    if contract.get("required_scope_ids") != [item["id"] for item in prev.get("target_manifest", [])]:
        errors.append("contract_scope_ids_mismatch")
    if contract.get("required_entry_ids") != list(REQUIRED_ENTRY_RESULTS):
        errors.append("contract_entry_ids_mismatch")

    entries = config.get("ledger_entries")
    if not isinstance(entries, list):
        errors.append("ledger_entries_missing")
        entries = []
    entry_ids = [entry.get("entry_id") for entry in entries if isinstance(entry, dict)]
    if entry_ids != list(REQUIRED_ENTRY_RESULTS):
        errors.append("ledger_entry_ids_mismatch")
    sequences = [entry.get("sequence") for entry in entries if isinstance(entry, dict)]
    if sequences != list(range(1, len(REQUIRED_ENTRY_RESULTS) + 1)):
        errors.append("ledger_entry_sequence_mismatch")
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("ledger_entry_not_object")
            continue
        entry_id = entry.get("entry_id", "unknown")
        errors.extend(check_keys(f"ledger_entries[{entry_id}]", entry, ENTRY_KEYS))
        if entry.get("source_step_id") != entry_id:
            errors.append(f"ledger_entry_source_step_mismatch:{entry_id}")
        if entry.get("dry_run_result") != REQUIRED_ENTRY_RESULTS.get(entry_id):
            errors.append(f"ledger_entry_result_mismatch:{entry_id}")
        if entry.get("review_question") != REQUIRED_ENTRY_QUESTIONS.get(entry_id):
            errors.append(f"ledger_entry_review_question_mismatch:{entry_id}")
        for false_key in [
            "perform_now",
            "writes_now",
            "formal_vault_access_now",
            "formal_vault_state_check_now",
            "hash_now",
            "snapshot_now",
            "sync_now",
            "commit_now",
            "push_now",
            "promotion_now",
        ]:
            if entry.get(false_key) is not False:
                errors.append(f"ledger_entry_flag_not_false:{entry_id}:{false_key}")
        for true_key in ["requires_future_user_confirmation", "requires_future_execution_slice", "evidence_recorded"]:
            if entry.get(true_key) is not True:
                errors.append(f"ledger_entry_flag_not_true:{entry_id}:{true_key}")
        for empty_key in ["command", "absolute_target_path", "copy_tool"]:
            if entry.get(empty_key) not in ("", None, "none"):
                errors.append(f"ledger_entry_forbidden_field_nonempty:{entry_id}:{empty_key}")
        if entry.get("non_claim") != "dry_run_ledger_entry_not_execution":
            errors.append(f"ledger_entry_non_claim_mismatch:{entry_id}")

    samples = config.get("ledger_samples")
    if not isinstance(samples, list):
        errors.append("ledger_samples_missing")
        samples = []
    expected_samples = {
        "synthetic_approved_plan_ledger": "LEDGER_DRY_RUN_RECORDED_NOT_EXECUTABLE",
        "synthetic_denied_plan_ledger": "BLOCKED_BY_DENIAL_LEDGER_ONLY",
        "synthetic_revision_plan_ledger": "BLOCKED_BY_REVISION_LEDGER_ONLY",
    }
    sample_ids = [sample.get("id") for sample in samples if isinstance(sample, dict)]
    if set(sample_ids) != set(expected_samples):
        errors.append("ledger_sample_ids_mismatch")
    for sample in samples:
        if not isinstance(sample, dict):
            errors.append("ledger_sample_not_object")
            continue
        sample_id = sample.get("id", "unknown")
        errors.extend(check_keys(f"ledger_samples[{sample_id}]", sample, SAMPLE_KEYS))
        if sample.get("expected_ledger_result") != expected_samples.get(sample_id):
            errors.append(f"ledger_sample_result_mismatch:{sample_id}")
        expected_binding = REQUIRED_SAMPLE_BINDINGS.get(sample_id)
        if expected_binding:
            expected_scenario, expected_mode, expected_created = expected_binding
            if sample.get("source_plan_scenario") != expected_scenario:
                errors.append(f"ledger_sample_source_scenario_mismatch:{sample_id}")
            if sample.get("ledger_mode") != expected_mode:
                errors.append(f"ledger_sample_mode_mismatch:{sample_id}")
            if sample.get("ledger_created") is not expected_created:
                errors.append(f"ledger_sample_created_mismatch:{sample_id}")
        if sample.get("entry_count") != len(REQUIRED_ENTRY_RESULTS):
            errors.append(f"ledger_sample_entry_count_mismatch:{sample_id}")
        if sample.get("scope_ids") != [item["id"] for item in prev.get("target_manifest", [])]:
            errors.append(f"ledger_sample_scope_ids_mismatch:{sample_id}")
        for false_key in [
            "actual_user_input",
            "approval_collected_now",
            "real_user_text_stored",
            "formal_vault_accessed",
            "formal_vault_state_inspected",
            "snapshot_taken",
            "hash_before_collected",
            "hash_after_collected",
            "execution_performed",
            "formal_vault_write_allowed_now",
            "action_basis_created",
            "reviewed_knowledge_created",
            "sync_allowed",
            "commit_allowed",
            "push_allowed",
            "promotion_allowed",
            "ledger_replayable",
            "ledger_is_execution_log",
        ]:
            if sample.get(false_key) is not False:
                errors.append(f"ledger_sample_flag_not_false:{sample_id}:{false_key}")
        if sample.get("synthetic_only") is not True:
            errors.append(f"ledger_sample_not_synthetic:{sample_id}")

    receipt_obj = config.get("non_execution_ledger_receipt")
    if not isinstance(receipt_obj, dict):
        errors.append("non_execution_ledger_receipt_missing")
        receipt_obj = {}
    errors.extend(check_keys("non_execution_ledger_receipt", receipt_obj, RECEIPT_KEYS))
    for false_key in [
        "approval_collected_now",
        "actual_user_input_used",
        "real_user_text_stored",
        "formal_vault_accessed",
        "formal_vault_state_inspected",
        "execution_performed",
        "snapshot_taken",
        "hash_before_collected",
        "hash_after_collected",
        "write_performed",
        "sync_performed",
        "commit_performed",
        "push_performed",
        "promotion_performed",
        "ledger_replayed",
        "ledger_used_as_action_basis",
    ]:
        if receipt_obj.get(false_key) is not False:
            errors.append(f"receipt_flag_not_false:{false_key}")
    if receipt_obj.get("current_status") != "formal_vault_execution_dry_run_ledger_non_executable_pending_review":
        errors.append("receipt_status_mismatch")
    required_non_claims = {
        "not actual approval",
        "not execution readiness",
        "not formal vault approval",
        "not action basis",
        "not reviewed knowledge",
        "not evidence support",
        "not an execution log",
        "not replayable",
    }
    if not required_non_claims.issubset(set(receipt_obj.get("non_claims", []))):
        errors.append("receipt_non_claims_missing")

    if config.get("stop_conditions") != REQUIRED_STOP_CONDITIONS:
        errors.append("stop_conditions_mismatch")

    metrics = config.get("product_metrics")
    if not isinstance(metrics, dict):
        errors.append("product_metrics_missing")
        metrics = {}
    errors.extend(check_keys("product_metrics", metrics, PRODUCT_METRIC_KEYS))
    if metrics.get("required_positive_fixtures") != 3:
        errors.append("product_metric_required_positive_fixtures_mismatch")
    if metrics.get("minimum_failure_cases", 0) < 100:
        errors.append("product_metric_failure_case_floor_too_low")
    if metrics.get("required_ledger_samples") != 3:
        errors.append("product_metric_ledger_samples_mismatch")
    if metrics.get("required_targets") != 5:
        errors.append("product_metric_required_targets_mismatch")
    if metrics.get("required_entries") != len(REQUIRED_ENTRY_RESULTS):
        errors.append("product_metric_required_entries_mismatch")
    if metrics.get("max_journey_steps") != 3:
        errors.append("product_metric_max_journey_steps_mismatch")

    if config.get("dry_run_ledger_hash") != expected_ledger_hash(config):
        errors.append("dry_run_ledger_hash_mismatch")

    return sorted(set(errors))


def frontmatter_status(path: Path) -> str | None:
    if not path.exists():
        return None
    match = re.search(r"(?m)^status:\s*([A-Za-z0-9_\-]+)\s*$", path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


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


def inspect_prototype() -> dict[str, Any]:
    prototype_path = ROOT / "prototype" / "formal-vault-execution-dry-run-ledger"
    receipt_path = prototype_path / "Receipts" / "formal-vault-execution-dry-run-ledger-receipt.json"
    html_path = prototype_path / "dry-run-ledger-inspector.html"
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
        ]
        for bit in forbidden_bits:
            if bit in lower:
                issues.append(f"html_forbidden_token:{bit}")
        required_attrs = [
            'data-sandbox-only="true"',
            'data-ledger-only="true"',
            'data-dry-run-only="true"',
            'data-non-executable="true"',
            'data-no-formal-vault-access="true"',
            'data-no-write="true"',
            'data-no-sync="true"',
            'data-no-authority="true"',
        ]
        for attr in required_attrs:
            if attr not in html:
                issues.append(f"html_missing_attr:{attr}")
        buttons = re.findall(r"<button[^>]*data-filter=\"([^\"]+)\"[^>]*>([^<]+)</button>", html)
        html_summary = {
            "sandbox_only": 'data-sandbox-only="true"' in html,
            "ledger_only": 'data-ledger-only="true"' in html,
            "dry_run_only": 'data-dry-run-only="true"' in html,
            "non_executable": 'data-non-executable="true"' in html,
            "no_formal_vault_access": 'data-no-formal-vault-access="true"' in html,
            "no_write": 'data-no-write="true"' in html,
            "no_sync": 'data-no-sync="true"' in html,
            "no_authority": 'data-no-authority="true"' in html,
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
        "contract_review": {"links_verified": (prototype_path / "01 Ledger Contract.md").exists(), "max_links": 2},
        "entry_review": {"links_verified": (prototype_path / "02 Ledger Entries.md").exists(), "max_links": 2},
        "receipt_review": {"links_verified": (prototype_path / "03 Non Execution Receipt.md").exists(), "max_links": 2},
        "stop_review": {"links_verified": (prototype_path / "04 Stop Conditions.md").exists(), "max_links": 2},
        "inspector_review": {"links_verified": html_path.exists(), "max_links": 2, "html_allowlist_ok": not issues},
    }
    return {
        "prototype_path": str(prototype_path),
        "issues": issues,
        "receipt": receipt,
        "html": html_summary,
        "actual_journeys": journeys,
    }


def validate_prototype_tamper(tamper: dict[str, Any]) -> list[str]:
    if tamper.get("kind") == "markdown_replace":
        return scan_prototype_text(tamper.get("file", "unknown.md"), tamper.get("content", ""))
    if tamper.get("kind") == "receipt_update":
        receipt_path = (
            ROOT
            / "prototype"
            / "formal-vault-execution-dry-run-ledger"
            / "Receipts"
            / "formal-vault-execution-dry-run-ledger-receipt.json"
        )
        receipt = read_json_path(receipt_path)
        receipt.update(tamper.get("updates", {}))
        return validate_prototype_receipt(receipt)
    if tamper.get("kind") == "receipt_replace_non_claims":
        receipt_path = (
            ROOT
            / "prototype"
            / "formal-vault-execution-dry-run-ledger"
            / "Receipts"
            / "formal-vault-execution-dry-run-ledger-receipt.json"
        )
        receipt = read_json_path(receipt_path)
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
