from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

SLICE_ID = "2026-06-15-p2-29-formal-vault-execution-plan-sandbox"
SOURCE_SLICE = "2026-06-15-p2-28-formal-vault-execution-preflight-dry-run-sandbox"
PREV_ROOT_REL = f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}"
ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[3]

PREV_FIXTURE_REL = f"{PREV_ROOT_REL}/fixtures/valid-execution-preflight-config.json"
PREV_RECEIPT_REL = (
    f"{PREV_ROOT_REL}/prototype/formal-vault-execution-preflight-dry-run/"
    "Receipts/formal-vault-execution-preflight-receipt.json"
)

SOURCE_FILES = [
    ("p2_28_next_step", f"{PREV_ROOT_REL}/next-step.md"),
    ("p2_28_product_acceptance", f"{PREV_ROOT_REL}/product-acceptance-report.md"),
    ("p2_28_verification", f"{PREV_ROOT_REL}/verification.md"),
    ("p2_28_reviewer_report", f"{PREV_ROOT_REL}/reviewer-report.md"),
    ("p2_28_boundary_audit", f"{PREV_ROOT_REL}/boundary-audit.md"),
    ("p2_28_source_map", f"{PREV_ROOT_REL}/source-map.md"),
    ("p2_28_preflight_fixture", PREV_FIXTURE_REL),
    ("p2_28_preflight_receipt", PREV_RECEIPT_REL),
    ("p2_28_contract", f"{PREV_ROOT_REL}/artifact/formal-vault-execution-preflight-dry-run-contract.md"),
]

PLAN_PURPOSE = (
    "Define a future formal-vault execution plan shape after P2-28 preflight, "
    "without collecting approval, inspecting the formal vault, emitting commands, or executing writes."
)

ALLOWED_SCENARIO_MODES = {
    "approved_plan_draft",
    "denial_block_record",
    "revision_block_record",
}

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
]

REQUIRED_PLAN_CONTROLS_TRUE = [
    "sandbox_only",
    "plan_only",
    "non_executable",
    "operator_must_stop_before_execution",
    "separate_future_user_confirmation_required",
    "separate_future_execution_slice_required",
    "validator_is_not_reviewer",
    "product_acceptance_is_not_formal_vault_approval",
    "preflight_pass_is_not_execution_permission",
    "target_hashes_are_source_hashes_only",
    "dirty_state_blocks_execution",
]

REQUIRED_PLAN_CONTROLS_FALSE = [
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
]

REQUIRED_STEP_IDS = [
    "source_binding_reconfirm",
    "target_manifest_reconfirm",
    "future_formal_vault_state_check",
    "future_snapshot_plan",
    "future_write_plan",
    "future_hash_after_plan",
    "future_sync_plan",
    "future_rollback_plan",
    "future_closeout_plan",
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
    "execution_plan_version",
    "truth_boundary",
    "purpose",
    "scenario_mode",
    "write_scope",
    "read_only_sources",
    "operations",
    "plan_controls",
    "source_inputs",
    "source_input_bundle_hash",
    "source_preflight_hash",
    "source_preflight_input_bundle_hash",
    "source_packet_hash",
    "source_packet_scope_hash",
    "source_target_manifest_hash",
    "source_required_preflight_hash",
    "source_receipt_preflight_hash",
    "target_manifest",
    "target_manifest_hash",
    "execution_plan_contract",
    "execution_plan_steps",
    "plan_samples",
    "non_execution_plan_receipt",
    "stop_conditions",
    "product_metrics",
    "execution_plan_hash",
}

SOURCE_INPUT_KEYS = {"id", "source_path", "source_sha256", "content_binding"}
TARGET_KEYS = {
    "id",
    "relative_target",
    "source_path",
    "source_sha256",
    "content_binding",
    "planned_action",
    "plan_status",
    "target_path_relative_only",
    "formal_vault_target_resolved",
    "formal_vault_target_exists_checked",
    "snapshot_taken",
    "hash_before_collected",
    "hash_after_collected",
    "write_enabled_now",
    "execution_enabled_now",
    "dry_run_only",
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
    "plan_is_non_executable",
    "separate_future_execution_slice_required",
    "separate_final_user_confirmation_required",
    "preflight_pass_not_execution_permission",
    "approved_reference_not_executable_here",
    "deny_blocks_plan",
    "revise_blocks_plan",
    "dirty_state_blocks_plan",
    "default_result",
    "required_preflight_hash",
    "required_target_manifest_hash",
    "required_scope_ids",
}
STEP_KEYS = {
    "step_id",
    "label",
    "status",
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
}
SAMPLE_KEYS = {
    "id",
    "source_preflight_sample",
    "decision_verdict",
    "preflight_result",
    "plan_draft_created",
    "executable_plan_created",
    "expected_plan_result",
    "next_gate",
    "actual_user_input",
    "approval_collected_now",
    "real_user_text_stored",
    "formal_vault_accessed",
    "formal_vault_state_inspected",
    "snapshot_taken",
    "rollback_executed",
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
    "current_status",
    "non_claims",
}
PRODUCT_METRIC_KEYS = {
    "required_positive_fixtures",
    "minimum_failure_cases",
    "required_plan_samples",
    "required_targets",
    "max_journey_steps",
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
    "preflight hash mismatch",
    "target manifest mismatch",
    "extra targets requested",
    "dirty-state acknowledgement missing",
]

DANGEROUS_VALUE_PATTERNS = [
    ("copy_item", re.compile(r"(?i)\bcopy-item\b")),
    ("robocopy", re.compile(r"(?i)\brobocopy\b")),
    ("xcopy", re.compile(r"(?i)\bxcopy\b")),
    ("powershell", re.compile(r"(?i)\bpowershell\b")),
    ("pwsh", re.compile(r"(?i)\bpwsh\b")),
    ("cmd_exe", re.compile(r"(?i)\bcmd\.exe\b")),
    ("start_process", re.compile(r"(?i)\bstart-process\b")),
    ("sync_now", re.compile(r"(?i)\bsync-now\b")),
    ("write_vault", re.compile(r"(?i)\bwrite-vault\b")),
    ("approve_now", re.compile(r"(?i)\bapprove-now\b")),
    ("obsidian_sync_command", re.compile(r"(?i)\bobsidian\s+sync\b")),
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
    items = []
    for item_id, rel_path in SOURCE_FILES:
        items.append(
            {
                "id": item_id,
                "source_path": rel_path,
                "source_sha256": sha256_file(rel_path),
                "content_binding": "exact_source_sha256",
            }
        )
    return items


def status_from_markdown(rel_path: str) -> str | None:
    match = re.search(r"(?m)^status:\s*([A-Za-z0-9_\-]+)\s*$", read_text(rel_path))
    return match.group(1) if match else None


def load_prev_fixture() -> dict[str, Any]:
    return read_json_rel(PREV_FIXTURE_REL)


def load_prev_receipt() -> dict[str, Any]:
    return read_json_rel(PREV_RECEIPT_REL)


def expected_source_input_bundle_hash(inputs: list[dict[str, str]]) -> str:
    return canonical_hash(inputs)


def expected_plan_hash_material(config: dict[str, Any]) -> dict[str, Any]:
    material = json.loads(canonical_json(config))
    material.pop("execution_plan_hash", None)
    return material


def expected_plan_hash(config: dict[str, Any]) -> str:
    return canonical_hash(expected_plan_hash_material(config))


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
    actual = set(value)
    errors = []
    for extra in sorted(actual - allowed):
        errors.append(f"unknown_key:{name}:{extra}")
    for missing in sorted(allowed - actual):
        errors.append(f"missing_key:{name}:{missing}")
    return errors


def scan_dangerous_values(value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if path.startswith("$.stop_conditions"):
        return errors
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key not in TOP_LEVEL_KEYS and path == "$":
                errors.append(f"unknown_top_level_key:{key}")
            errors.extend(scan_dangerous_values(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(scan_dangerous_values(child, f"{path}[{index}]"))
    elif isinstance(value, str):
        for label, pattern in DANGEROUS_VALUE_PATTERNS:
            if pattern.search(value):
                errors.append(f"dangerous_value:{path}:{label}")
    return errors


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    prev = load_prev_fixture()
    receipt = load_prev_receipt()

    if not isinstance(config, dict):
        return ["config_not_object"]

    errors.extend(check_keys("config", config, TOP_LEVEL_KEYS))
    errors.extend(scan_dangerous_values(config))

    if config.get("slice_id") != SLICE_ID:
        errors.append("slice_id_mismatch")
    if config.get("source_slice") != SOURCE_SLICE:
        errors.append("source_slice_mismatch")
    if config.get("execution_plan_version") != "p2-29-formal-vault-execution-plan-v1":
        errors.append("plan_version_mismatch")
    if config.get("truth_boundary") != "sandbox_only_non_executing_plan":
        errors.append("truth_boundary_mismatch")
    if config.get("purpose") != PLAN_PURPOSE:
        errors.append("purpose_mismatch")
    if config.get("scenario_mode") not in ALLOWED_SCENARIO_MODES:
        errors.append("scenario_mode_not_allowed")

    write_scope = config.get("write_scope")
    expected_scope = [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"]
    if write_scope != expected_scope:
        errors.append("write_scope_mismatch")

    operations = config.get("operations")
    if not isinstance(operations, dict):
        errors.append("operations_missing")
        operations = {}
    errors.extend(check_keys("operations", operations, set(FORBIDDEN_OPERATIONS)))
    for key in FORBIDDEN_OPERATIONS:
        if operations.get(key) is not False:
            errors.append(f"forbidden_operation_enabled:{key}")

    controls = config.get("plan_controls")
    if not isinstance(controls, dict):
        errors.append("plan_controls_missing")
        controls = {}
    errors.extend(check_keys("plan_controls", controls, set(REQUIRED_PLAN_CONTROLS_TRUE + REQUIRED_PLAN_CONTROLS_FALSE)))
    for key in REQUIRED_PLAN_CONTROLS_TRUE:
        if controls.get(key) is not True:
            errors.append(f"plan_control_not_true:{key}")
    for key in REQUIRED_PLAN_CONTROLS_FALSE:
        if controls.get(key) is not False:
            errors.append(f"plan_control_not_false:{key}")

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

    prev_hash_checks = {
        "source_preflight_hash": prev.get("preflight_hash"),
        "source_preflight_input_bundle_hash": prev.get("source_input_bundle_hash"),
        "source_packet_hash": prev.get("source_packet_hash"),
        "source_packet_scope_hash": prev.get("source_packet_scope_hash"),
        "source_target_manifest_hash": prev.get("target_manifest_hash"),
        "source_required_preflight_hash": prev.get("preflight_contract", {}).get("required_preflight_hash"),
        "source_receipt_preflight_hash": receipt.get("preflight_hash"),
    }
    for key, expected in prev_hash_checks.items():
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
        errors.extend(check_keys(f"target_manifest[{target.get('id', 'unknown')}]", target, TARGET_KEYS))
        target_id = target.get("id")
        expected = expected_targets.get(target_id)
        if expected is None:
            errors.append(f"target_not_in_preflight_scope:{target_id}")
            continue
        for field, expected_field in [
            ("relative_target", "relative_target"),
            ("source_path", "source_path"),
            ("source_sha256", "source_sha256"),
            ("content_binding", "content_binding"),
        ]:
            if target.get(field) != expected.get(expected_field):
                errors.append(f"target_{field}_mismatch:{target_id}")
        if not is_relative_safe(target.get("relative_target", "")):
            errors.append(f"target_relative_path_unsafe:{target_id}")
        for false_key in [
            "formal_vault_target_resolved",
            "formal_vault_target_exists_checked",
            "snapshot_taken",
            "hash_before_collected",
            "hash_after_collected",
            "write_enabled_now",
            "execution_enabled_now",
        ]:
            if target.get(false_key) is not False:
                errors.append(f"target_flag_not_false:{target_id}:{false_key}")
        if target.get("planned_action") != "future_copy_from_sandbox_source_to_relative_target":
            errors.append(f"target_planned_action_mismatch:{target_id}")
        if target.get("plan_status") != "planned_future_only_not_executable":
            errors.append(f"target_plan_status_mismatch:{target_id}")

    if config.get("target_manifest_hash") != canonical_hash(targets):
        errors.append("target_manifest_hash_mismatch")
    if config.get("target_manifest_hash") == config.get("source_target_manifest_hash"):
        errors.append("target_manifest_hash_not_recomputed_for_plan")

    contract = config.get("execution_plan_contract")
    if not isinstance(contract, dict):
        errors.append("execution_plan_contract_missing")
        contract = {}
    errors.extend(check_keys("execution_plan_contract", contract, CONTRACT_KEYS))
    expected_contract_flags = {
        "contract_kind": "formal_vault_execution_plan_sandbox",
        "current_slice_executes": False,
        "current_slice_collects_approval": False,
        "formal_vault_access_disallowed": True,
        "formal_vault_state_inspection_disallowed": True,
        "formal_vault_write_disallowed": True,
        "formal_vault_hash_disallowed": True,
        "formal_vault_snapshot_disallowed": True,
        "plan_is_non_executable": True,
        "separate_future_execution_slice_required": True,
        "separate_final_user_confirmation_required": True,
        "preflight_pass_not_execution_permission": True,
        "approved_reference_not_executable_here": True,
        "deny_blocks_plan": True,
        "revise_blocks_plan": True,
        "dirty_state_blocks_plan": True,
        "default_result": "PLAN_DRAFT_ONLY_NOT_EXECUTABLE",
    }
    for key, expected in expected_contract_flags.items():
        if contract.get(key) != expected:
            errors.append(f"contract_field_mismatch:{key}")
    if contract.get("required_preflight_hash") != prev.get("preflight_hash"):
        errors.append("contract_required_preflight_hash_mismatch")
    if contract.get("required_target_manifest_hash") != prev.get("target_manifest_hash"):
        errors.append("contract_required_target_manifest_hash_mismatch")
    if contract.get("required_scope_ids") != [item["id"] for item in prev.get("target_manifest", [])]:
        errors.append("contract_scope_ids_mismatch")

    steps = config.get("execution_plan_steps")
    if not isinstance(steps, list):
        errors.append("execution_plan_steps_missing")
        steps = []
    step_ids = [step.get("step_id") for step in steps if isinstance(step, dict)]
    if step_ids != REQUIRED_STEP_IDS:
        errors.append("execution_plan_step_ids_mismatch")
    for step in steps:
        if not isinstance(step, dict):
            errors.append("execution_plan_step_not_object")
            continue
        errors.extend(check_keys(f"execution_plan_steps[{step.get('step_id', 'unknown')}]", step, STEP_KEYS))
        step_id = step.get("step_id", "unknown")
        if step.get("status") != "planned_future_only":
            errors.append(f"step_status_mismatch:{step_id}")
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
            if step.get(false_key) is not False:
                errors.append(f"step_flag_not_false:{step_id}:{false_key}")
        for true_key in ["requires_future_user_confirmation", "requires_future_execution_slice"]:
            if step.get(true_key) is not True:
                errors.append(f"step_flag_not_true:{step_id}:{true_key}")
        for empty_key in ["command", "absolute_target_path", "copy_tool"]:
            if step.get(empty_key) not in ("", None, "none"):
                errors.append(f"step_forbidden_field_nonempty:{step_id}:{empty_key}")

    samples = config.get("plan_samples")
    if not isinstance(samples, list):
        errors.append("plan_samples_missing")
        samples = []
    expected_samples = {
        "synthetic_approved_preflight_plan": "PLAN_DRAFT_READY_FOR_FUTURE_REVIEW_NOT_EXECUTABLE",
        "synthetic_denied_preflight_plan": "BLOCKED_BY_DENIAL_NO_PLAN",
        "synthetic_revision_preflight_plan": "BLOCKED_BY_REVISION_NO_PLAN",
        "synthetic_dirty_state_plan_block": "BLOCKED_BY_DIRTY_STATE_NO_PLAN",
    }
    sample_ids = [sample.get("id") for sample in samples if isinstance(sample, dict)]
    if set(sample_ids) != set(expected_samples):
        errors.append("plan_sample_ids_mismatch")
    for sample in samples:
        if not isinstance(sample, dict):
            errors.append("plan_sample_not_object")
            continue
        errors.extend(check_keys(f"plan_samples[{sample.get('id', 'unknown')}]", sample, SAMPLE_KEYS))
        sample_id = sample.get("id", "unknown")
        if sample.get("expected_plan_result") != expected_samples.get(sample_id):
            errors.append(f"plan_sample_result_mismatch:{sample_id}")
        for false_key in [
            "actual_user_input",
            "approval_collected_now",
            "real_user_text_stored",
            "formal_vault_accessed",
            "formal_vault_state_inspected",
            "snapshot_taken",
            "rollback_executed",
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
        ]:
            if sample.get(false_key) is not False:
                errors.append(f"plan_sample_flag_not_false:{sample_id}:{false_key}")
        if sample.get("scope_ids") != [item["id"] for item in prev.get("target_manifest", [])]:
            errors.append(f"plan_sample_scope_ids_mismatch:{sample_id}")
        if sample_id == "synthetic_approved_preflight_plan":
            if sample.get("plan_draft_created") is not True:
                errors.append("approved_sample_plan_draft_not_created")
            if sample.get("executable_plan_created") is not False:
                errors.append("approved_sample_executable_plan_created")
        else:
            if sample.get("plan_draft_created") is not False:
                errors.append(f"blocked_sample_plan_draft_created:{sample_id}")

    receipt_obj = config.get("non_execution_plan_receipt")
    if not isinstance(receipt_obj, dict):
        errors.append("non_execution_plan_receipt_missing")
        receipt_obj = {}
    errors.extend(check_keys("non_execution_plan_receipt", receipt_obj, RECEIPT_KEYS))
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
    ]:
        if receipt_obj.get(false_key) is not False:
            errors.append(f"receipt_flag_not_false:{false_key}")
    if receipt_obj.get("current_status") != "formal_vault_execution_plan_draft_non_executable_pending_review":
        errors.append("receipt_status_mismatch")
    required_non_claims = {
        "not actual approval",
        "not execution readiness",
        "not formal vault approval",
        "not action basis",
        "not reviewed knowledge",
        "not evidence support",
        "not a write command",
    }
    if not required_non_claims.issubset(set(receipt_obj.get("non_claims", []))):
        errors.append("receipt_non_claims_missing")

    if config.get("execution_plan_hash") != expected_plan_hash(config):
        errors.append("execution_plan_hash_mismatch")

    metrics = config.get("product_metrics", {})
    errors.extend(check_keys("product_metrics", metrics, PRODUCT_METRIC_KEYS))
    if metrics.get("required_positive_fixtures") != 3:
        errors.append("product_metric_required_positive_fixtures_mismatch")
    if metrics.get("minimum_failure_cases", 0) < 85:
        errors.append("product_metric_failure_case_floor_too_low")
    if metrics.get("required_plan_samples") != 4:
        errors.append("product_metric_plan_samples_mismatch")
    if metrics.get("required_targets") != 5:
        errors.append("product_metric_required_targets_mismatch")
    if metrics.get("max_journey_steps") != 3:
        errors.append("product_metric_max_journey_steps_mismatch")

    stop_conditions = config.get("stop_conditions")
    if stop_conditions != REQUIRED_STOP_CONDITIONS:
        errors.append("stop_conditions_mismatch")

    return sorted(set(errors))


def frontmatter_status(path: Path) -> str | None:
    if not path.exists():
        return None
    match = re.search(r"(?m)^status:\s*([A-Za-z0-9_\-]+)\s*$", path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def required_report_statuses(final_gate: bool) -> dict[str, str]:
    return REQUIRED_REPORT_STATUSES if final_gate else PRE_FINAL_REPORT_STATUSES


def check_required_reports(final_gate: bool) -> dict[str, Any]:
    expected = required_report_statuses(final_gate)
    statuses = {}
    issues = []
    for name, expected_status in expected.items():
        actual = frontmatter_status(ROOT / name)
        statuses[name] = actual
        if actual != expected_status:
            if final_gate:
                issues.append(f"final_gate_bad_status:{name}:{actual}:expected:{expected_status}")
            elif actual is None:
                issues.append(f"missing_report:{name}")
    return {"statuses": statuses, "issues": issues}


def inspect_prototype() -> dict[str, Any]:
    prototype_path = ROOT / "prototype" / "formal-vault-execution-plan-sandbox"
    receipt_path = prototype_path / "Receipts" / "formal-vault-execution-plan-receipt.json"
    html_path = prototype_path / "execution-plan-inspector.html"
    required_files = [
        "00 Execution Plan Home.md",
        "01 Non Executable Plan Contract.md",
        "02 Target Manifest Plan.md",
        "03 Future State Snapshot Hash Plan.md",
        "04 Stop Conditions.md",
        "05 Non Execution Receipt.md",
        "06 Reviewer Packet.md",
        "execution-plan-inspector.html",
        "Receipts/formal-vault-execution-plan-receipt.json",
    ]
    issues = []
    for rel in required_files:
        if not (prototype_path / rel).exists():
            issues.append(f"missing_prototype_file:{rel}")

    receipt = {}
    if receipt_path.exists():
        receipt = read_json_path(receipt_path)
        for key in [
            "formal_vault_accessed",
            "formal_vault_state_inspected",
            "execution_performed",
            "write_performed",
            "hash_before_collected",
            "hash_after_collected",
            "sync_performed",
            "commit_performed",
            "push_performed",
            "promotion_performed",
        ]:
            if receipt.get(key) is not False:
                issues.append(f"prototype_receipt_flag_not_false:{key}")
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
            'data-plan-only="true"',
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
            "plan_only": 'data-plan-only="true"' in html,
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
        "contract_review": {"links_verified": (prototype_path / "01 Non Executable Plan Contract.md").exists(), "max_links": 2},
        "target_manifest_review": {"links_verified": (prototype_path / "02 Target Manifest Plan.md").exists(), "max_links": 2},
        "future_state_review": {"links_verified": (prototype_path / "03 Future State Snapshot Hash Plan.md").exists(), "max_links": 2},
        "receipt_to_stop_review": {"links_verified": (prototype_path / "04 Stop Conditions.md").exists(), "max_links": 2},
        "inspector_review": {"links_verified": html_path.exists(), "max_links": 2, "html_allowlist_ok": not issues},
    }
    return {
        "prototype_path": str(prototype_path),
        "issues": issues,
        "receipt": receipt,
        "html": html_summary,
        "actual_journeys": journeys,
    }


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
        actual_errors = validate_config(payload.get("config", {}))
        if expected_errors != oracle_errors:
            mismatches.append(f"case_oracle_disagreement:{file_name}")
        if actual_errors != oracle_errors:
            mismatches.append(
                f"failure_case_mismatch:{file_name}:actual={actual_errors}:expected={oracle_errors}"
            )
        if not actual_errors:
            mismatches.append(f"failure_case_did_not_fail:{file_name}")
    return {"count": len(actual_files), "mismatches": mismatches}
