from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p2-36-formal-vault-read-only-product-workflow-prototype-sandbox"
ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[3]

SOURCE_SLICES = [
    "2026-06-15-p2-33-formal-vault-execution-request-screening-sandbox",
    "2026-06-15-p2-34-formal-vault-operator-status-surface-sandbox",
    "2026-06-15-p2-35-formal-vault-status-surface-handoff-packet-sandbox",
]

WORKFLOW_VERSION = "p2-36-formal-vault-read-only-product-workflow-prototype-v1"
TRUTH_BOUNDARY = "sandbox_read_only_product_workflow_not_authority"
PURPOSE = (
    "Show a read-only operator workflow from request screening to status surface "
    "to safe handoff/prebrief without collecting approval, commands, user wording, "
    "formal-vault access, or action-basis authority."
)

WORKFLOW_MODES = [
    "screen_status_handoff_walkthrough",
    "stop_before_formal_vault_workflow",
    "fresh_sandbox_prebrief_workflow",
]

SOURCE_INPUTS = [
    {
        "id": "p2_33_product_acceptance",
        "slice_id": SOURCE_SLICES[0],
        "role": "request_screening_pass",
        "path": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICES[0]}/product-acceptance-report.md",
    },
    {
        "id": "p2_33_verification",
        "slice_id": SOURCE_SLICES[0],
        "role": "request_screening_verification",
        "path": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICES[0]}/verification.md",
    },
    {
        "id": "p2_33_contract",
        "slice_id": SOURCE_SLICES[0],
        "role": "request_screening_contract",
        "path": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICES[0]}/artifact/formal-vault-execution-request-screening-contract.md",
    },
    {
        "id": "p2_34_product_acceptance",
        "slice_id": SOURCE_SLICES[1],
        "role": "status_surface_pass",
        "path": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICES[1]}/product-acceptance-report.md",
    },
    {
        "id": "p2_34_verification",
        "slice_id": SOURCE_SLICES[1],
        "role": "status_surface_verification",
        "path": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICES[1]}/verification.md",
    },
    {
        "id": "p2_34_contract",
        "slice_id": SOURCE_SLICES[1],
        "role": "status_surface_contract",
        "path": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICES[1]}/artifact/formal-vault-operator-status-surface-contract.md",
    },
    {
        "id": "p2_35_product_acceptance",
        "slice_id": SOURCE_SLICES[2],
        "role": "handoff_packet_pass",
        "path": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICES[2]}/product-acceptance-report.md",
    },
    {
        "id": "p2_35_verification",
        "slice_id": SOURCE_SLICES[2],
        "role": "handoff_packet_verification",
        "path": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICES[2]}/verification.md",
    },
    {
        "id": "p2_35_contract",
        "slice_id": SOURCE_SLICES[2],
        "role": "handoff_packet_contract",
        "path": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICES[2]}/artifact/formal-vault-status-surface-handoff-packet-contract.md",
    },
    {
        "id": "p2_35_next_step",
        "slice_id": SOURCE_SLICES[2],
        "role": "handoff_next_step",
        "path": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICES[2]}/next-step.md",
    },
]

SOURCE_STATUSES = [
    {
        "slice_id": SOURCE_SLICES[0],
        "file": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICES[0]}/product-acceptance-report.md",
        "expected_status": "pass_product_grade",
    },
    {
        "slice_id": SOURCE_SLICES[1],
        "file": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICES[1]}/product-acceptance-report.md",
        "expected_status": "pass_product_grade",
    },
    {
        "slice_id": SOURCE_SLICES[2],
        "file": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICES[2]}/product-acceptance-report.md",
        "expected_status": "pass_product_grade",
    },
    {
        "slice_id": SOURCE_SLICES[2],
        "file": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICES[2]}/next-step.md",
        "expected_status": "pass_product_grade_pending_user_next_slice_decision",
    },
]

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
    "workflow_auto_advance",
]

CONTROL_EXPECTED = {
    "sandbox_only": True,
    "read_only_workflow_only": True,
    "non_executable": True,
    "source_bound": True,
    "fresh_sandbox_required_for_next_work": True,
    "no_formal_vault_access": True,
    "no_approval_collection": True,
    "no_user_instruction": True,
    "no_user_wording": True,
    "no_commands": True,
    "no_absolute_vault_paths": True,
    "no_mainline_claim": True,
    "no_action_basis": True,
    "no_evidence_support": True,
    "no_reviewed_knowledge": True,
    "no_dirty_tree_repair": True,
    "no_auto_advance": True,
    "operator_must_stop_before_execution": True,
    "workflow_is_not_authority": True,
}

STEP_IDS = ["request_screening", "operator_status_surface", "handoff_prebrief"]
CHECK_IDS = [
    "source_slices_passed",
    "request_screening_visible",
    "status_surface_visible",
    "handoff_packet_visible",
    "no_approval_capture",
    "no_command_surface",
    "no_formal_vault_path",
    "no_action_basis_claim",
    "fresh_sandbox_next_step_only",
    "stop_before_execution",
]

NON_CLAIMS = {
    "not actual approval",
    "not user instruction",
    "not user wording storage",
    "not command surface",
    "not execution permission",
    "not formal vault access",
    "not formal vault approval",
    "not formal vault state",
    "not reviewed knowledge",
    "not evidence support",
    "not action basis",
    "not mainline readiness",
    "not merge approval",
    "not dirty tree repair",
    "not auto advance",
}

TOP_LEVEL_KEYS = {
    "slice_id",
    "workflow_version",
    "truth_boundary",
    "purpose",
    "workflow_mode",
    "write_scope",
    "read_only_sources",
    "source_inputs",
    "source_statuses",
    "source_surface_binding",
    "operations",
    "workflow_controls",
    "workflow_steps",
    "workflow_payload",
    "workflow_checks",
    "workflow_receipt",
}

PROTOTYPE_REQUIRED_FILES = [
    "00 Workflow Home.md",
    "01 Request Screening Step.md",
    "02 Status Surface Step.md",
    "03 Handoff Prebrief Step.md",
    "04 Stop Conditions.md",
    "05 Reviewer Packet.md",
    "workflow-prototype-inspector.html",
    "Receipts/workflow-prototype-receipt.json",
]
PROTOTYPE_MARKDOWN_FILES = PROTOTYPE_REQUIRED_FILES[:6]

DANGEROUS_PATTERNS = {
    "python_command": re.compile(r"\bpython\s+tools/", re.IGNORECASE),
    "sync_flag": re.compile(r"--sync\b", re.IGNORECASE),
    "run_now": re.compile(r"\brun\s+now\b", re.IGNORECASE),
    "approval_collected_marker": re.compile(r"approval\s+collected\s*:\s*yes", re.IGNORECASE),
    "mainline_ready_marker": re.compile(r"mainline\s+ready\s*:\s*yes", re.IGNORECASE),
    "execution_granted_marker": re.compile(r"execution\s+permission\s*:\s*granted", re.IGNORECASE),
    "absolute_obsidian_path": re.compile(r"H:[/\\]Obsidian", re.IGNORECASE),
    "action_basis_ready_marker": re.compile(r"action\s+basis\s*:\s*ready", re.IGNORECASE),
}

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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json_path(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_path(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_hash(data: Any) -> str:
    return hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()


def frontmatter_status(path: Path) -> str | None:
    if not path.exists():
        return None
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:20]:
        if line.strip() == "---":
            return None
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return None


def expected_source_inputs() -> list[dict[str, Any]]:
    result = []
    for item in SOURCE_INPUTS:
        path = REPO_ROOT / item["path"]
        result.append(
            {
                **item,
                "exists": path.exists(),
                "sha256": sha256_file(path) if path.exists() else None,
            }
        )
    return result


def expected_source_statuses() -> list[dict[str, Any]]:
    result = []
    for item in SOURCE_STATUSES:
        path = REPO_ROOT / item["file"]
        result.append({**item, "actual_status": frontmatter_status(path)})
    return result


def expected_source_binding() -> dict[str, Any]:
    return {
        "binding_kind": "read_only_product_workflow_source_binding",
        "source_slice_count": 3,
        "source_input_count": len(SOURCE_INPUTS),
        "required_status_count": len(SOURCE_STATUSES),
        "p2_33_product_status": "pass_product_grade",
        "p2_34_product_status": "pass_product_grade",
        "p2_35_product_status": "pass_product_grade",
        "p2_35_next_status": "pass_product_grade_pending_user_next_slice_decision",
        "formal_vault_accessed": False,
        "approval_collected_now": False,
        "user_instruction_collected": False,
        "user_wording_stored": False,
        "execution_permission_granted": False,
        "execution_performed": False,
        "write_performed": False,
        "sync_performed": False,
        "commit_performed": False,
        "push_performed": False,
        "promotion_performed": False,
        "mainline_ready": False,
        "workflow_used_as_action_basis": False,
        "dirty_tree_fixed": False,
        "auto_advanced": False,
    }


def expected_steps(mode: str) -> list[dict[str, Any]]:
    focus_by_mode = {
        "screen_status_handoff_walkthrough": "full_read_only_walkthrough",
        "stop_before_formal_vault_workflow": "stop_and_boundary_visibility",
        "fresh_sandbox_prebrief_workflow": "fresh_sandbox_prebrief_only",
    }
    return [
        {
            "step_id": "request_screening",
            "source_slice": SOURCE_SLICES[0],
            "visible_input": "formal-vault request screening result",
            "operator_value": "Shows whether a request is reviewable, denied, or missing confirmation.",
            "allowed_interaction": "read_only_inspection",
            "blocked_interactions": ["approval_collection", "command_entry", "formal_vault_access"],
            "focus": focus_by_mode.get(mode),
        },
        {
            "step_id": "operator_status_surface",
            "source_slice": SOURCE_SLICES[1],
            "visible_input": "formal-vault safety chain status",
            "operator_value": "Shows pass state, stop lines, and non-authority boundaries in one surface.",
            "allowed_interaction": "read_only_inspection",
            "blocked_interactions": ["mainline_claim", "action_basis_claim", "dirty_tree_repair"],
            "focus": focus_by_mode.get(mode),
        },
        {
            "step_id": "handoff_prebrief",
            "source_slice": SOURCE_SLICES[2],
            "visible_input": "safe handoff packet",
            "operator_value": "Shows how to recover, prebrief, or park without treating the handoff as approval.",
            "allowed_interaction": "read_only_prebrief",
            "blocked_interactions": ["auto_advance", "execution_permission", "user_wording_storage"],
            "focus": focus_by_mode.get(mode),
        },
    ]


def expected_payload(mode: str) -> dict[str, Any]:
    visible_next_action = {
        "screen_status_handoff_walkthrough": "inspect_chain_then_stop_before_any_execution",
        "stop_before_formal_vault_workflow": "park_or_ask_user_if_formal_vault_action_is_needed",
        "fresh_sandbox_prebrief_workflow": "start_next_slice_only_in_a_fresh_sandbox_path",
    }.get(mode)
    return {
        "payload_kind": "read_only_operator_workflow_payload",
        "mode": mode,
        "visible_next_action": visible_next_action,
        "operator_can_copy_commands": False,
        "operator_can_collect_approval": False,
        "operator_can_store_user_wording": False,
        "operator_can_access_formal_vault": False,
        "operator_can_create_action_basis": False,
        "operator_can_mark_mainline_ready": False,
        "operator_can_fix_dirty_tree": False,
        "operator_can_auto_advance": False,
        "next_work_must_use_fresh_sandbox": True,
        "non_claims": sorted(NON_CLAIMS),
    }


def expected_checks() -> list[dict[str, Any]]:
    return [
        {
            "check_id": check_id,
            "result_required": "pass",
            "authority": "diagnostic_only_not_action_authority",
        }
        for check_id in CHECK_IDS
    ]


def workflow_hash_without_hash(config: dict[str, Any]) -> str:
    clone = copy.deepcopy(config)
    if isinstance(clone.get("workflow_receipt"), dict):
        clone["workflow_receipt"].pop("workflow_hash", None)
    return canonical_hash(clone)


def base_config(mode: str) -> dict[str, Any]:
    config = {
        "slice_id": SLICE_ID,
        "workflow_version": WORKFLOW_VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "workflow_mode": mode,
        "write_scope": [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"],
        "read_only_sources": [f"outputs/review/vaks-implementation-sandbox/{sid}/" for sid in SOURCE_SLICES],
        "source_inputs": expected_source_inputs(),
        "source_statuses": expected_source_statuses(),
        "source_surface_binding": expected_source_binding(),
        "operations": {key: False for key in OPERATION_KEYS},
        "workflow_controls": dict(CONTROL_EXPECTED),
        "workflow_steps": expected_steps(mode),
        "workflow_payload": expected_payload(mode),
        "workflow_checks": expected_checks(),
        "workflow_receipt": {
            "record_kind": "sandbox_read_only_product_workflow_receipt",
            "slice_id": SLICE_ID,
            "source_slice_count": 3,
            "step_count": len(STEP_IDS),
            "check_count": len(CHECK_IDS),
            "formal_vault_accessed": False,
            "approval_collected_now": False,
            "user_instruction_collected": False,
            "user_wording_stored": False,
            "execution_permission_granted": False,
            "execution_performed": False,
            "write_performed": False,
            "sync_performed": False,
            "commit_performed": False,
            "push_performed": False,
            "promotion_performed": False,
            "mainline_ready": False,
            "workflow_used_as_action_basis": False,
            "dirty_tree_fixed": False,
            "auto_advanced": False,
            "workflow_hash": "",
            "non_claims": sorted(NON_CLAIMS),
        },
    }
    config["workflow_receipt"]["workflow_hash"] = workflow_hash_without_hash(config)
    return config


def check_keys(label: str, value: dict[str, Any], expected: set[str]) -> list[str]:
    actual = set(value)
    errors = []
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        errors.append(f"{label}_missing_keys:{','.join(missing)}")
    if extra:
        errors.append(f"{label}_extra_keys:{','.join(extra)}")
    return errors


def scan_dangerous_values(value: Any, prefix: str = "value") -> list[str]:
    errors = []
    if isinstance(value, str):
        for name, pattern in DANGEROUS_PATTERNS.items():
            if pattern.search(value):
                errors.append(f"dangerous_text:{prefix}:{name}")
    elif isinstance(value, dict):
        for key, nested in value.items():
            errors.extend(scan_dangerous_values(nested, f"{prefix}.{key}"))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(scan_dangerous_values(nested, f"{prefix}[{index}]"))
    return errors


def current_valid_config() -> dict[str, Any] | None:
    path = ROOT / "fixtures" / "valid-screen-status-handoff-workflow-config.json"
    if not path.exists():
        return None
    return read_json_path(path)


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(config, dict):
        return ["config_not_object"]
    errors.extend(check_keys("config", config, TOP_LEVEL_KEYS))
    errors.extend(scan_dangerous_values(config))

    mode = config.get("workflow_mode")
    if config.get("slice_id") != SLICE_ID:
        errors.append("slice_id_mismatch")
    if config.get("workflow_version") != WORKFLOW_VERSION:
        errors.append("workflow_version_mismatch")
    if config.get("truth_boundary") != TRUTH_BOUNDARY:
        errors.append("truth_boundary_mismatch")
    if config.get("purpose") != PURPOSE:
        errors.append("purpose_mismatch")
    if mode not in WORKFLOW_MODES:
        errors.append("workflow_mode_not_allowed")
    if config.get("write_scope") != [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"]:
        errors.append("write_scope_mismatch")
    if config.get("read_only_sources") != [f"outputs/review/vaks-implementation-sandbox/{sid}/" for sid in SOURCE_SLICES]:
        errors.append("read_only_sources_mismatch")

    if config.get("source_inputs") != expected_source_inputs():
        errors.append("source_inputs_mismatch")
    if config.get("source_statuses") != expected_source_statuses():
        errors.append("source_statuses_mismatch")

    binding = config.get("source_surface_binding")
    if binding != expected_source_binding():
        errors.append("source_surface_binding_mismatch")
    if isinstance(binding, dict):
        for false_key in [
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
            "workflow_used_as_action_basis",
            "dirty_tree_fixed",
            "auto_advanced",
        ]:
            if binding.get(false_key) is not False:
                errors.append(f"source_binding_flag_not_false:{false_key}")
    else:
        errors.append("source_surface_binding_not_object")

    operations = config.get("operations")
    if not isinstance(operations, dict):
        errors.append("operations_missing")
        operations = {}
    errors.extend(check_keys("operations", operations, set(OPERATION_KEYS)))
    for key in OPERATION_KEYS:
        if operations.get(key) is not False:
            errors.append(f"operation_not_false:{key}")

    controls = config.get("workflow_controls")
    if not isinstance(controls, dict):
        errors.append("workflow_controls_missing")
        controls = {}
    errors.extend(check_keys("workflow_controls", controls, set(CONTROL_EXPECTED)))
    for key, expected in CONTROL_EXPECTED.items():
        if controls.get(key) is not expected:
            errors.append(f"workflow_control_mismatch:{key}")

    if config.get("workflow_steps") != expected_steps(mode):
        errors.append("workflow_steps_mismatch")
    if isinstance(config.get("workflow_steps"), list):
        ids = [step.get("step_id") for step in config["workflow_steps"] if isinstance(step, dict)]
        if ids != STEP_IDS:
            errors.append("workflow_step_ids_mismatch")
    else:
        errors.append("workflow_steps_not_list")

    payload = config.get("workflow_payload")
    expected_payload_value = expected_payload(mode) if mode in WORKFLOW_MODES else {}
    if payload != expected_payload_value:
        errors.append("workflow_payload_mismatch")
    if isinstance(payload, dict):
        for false_key in [
            "operator_can_copy_commands",
            "operator_can_collect_approval",
            "operator_can_store_user_wording",
            "operator_can_access_formal_vault",
            "operator_can_create_action_basis",
            "operator_can_mark_mainline_ready",
            "operator_can_fix_dirty_tree",
            "operator_can_auto_advance",
        ]:
            if payload.get(false_key) is not False:
                errors.append(f"workflow_payload_flag_not_false:{false_key}")
        if payload.get("next_work_must_use_fresh_sandbox") is not True:
            errors.append("workflow_payload_fresh_sandbox_not_true")
        if not NON_CLAIMS.issubset(set(payload.get("non_claims", []))):
            errors.append("workflow_payload_non_claims_missing")
    else:
        errors.append("workflow_payload_not_object")

    if config.get("workflow_checks") != expected_checks():
        errors.append("workflow_checks_mismatch")

    receipt = config.get("workflow_receipt")
    if not isinstance(receipt, dict):
        errors.append("workflow_receipt_missing")
    else:
        if receipt.get("workflow_hash") != workflow_hash_without_hash(config):
            errors.append("workflow_receipt_hash_mismatch")
        if receipt.get("source_slice_count") != 3:
            errors.append("workflow_receipt_source_slice_count_mismatch")
        if receipt.get("step_count") != len(STEP_IDS):
            errors.append("workflow_receipt_step_count_mismatch")
        if receipt.get("check_count") != len(CHECK_IDS):
            errors.append("workflow_receipt_check_count_mismatch")
        for false_key in [
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
            "workflow_used_as_action_basis",
            "dirty_tree_fixed",
            "auto_advanced",
        ]:
            if receipt.get(false_key) is not False:
                errors.append(f"workflow_receipt_flag_not_false:{false_key}")
        if not NON_CLAIMS.issubset(set(receipt.get("non_claims", []))):
            errors.append("workflow_receipt_non_claims_missing")

    return sorted(set(errors))


def validate_prototype_markdown_text(rel: str, text: str) -> list[str]:
    errors = []
    required = [
        SLICE_ID,
        SOURCE_SLICES[0],
        SOURCE_SLICES[1],
        SOURCE_SLICES[2],
        "READ_ONLY_PRODUCT_WORKFLOW",
        "STOP_BEFORE_FORMAL_VAULT_EXECUTION",
        "FRESH_SANDBOX_ONLY_NEXT_STEP",
    ]
    for marker in required:
        if marker not in text:
            errors.append(f"prototype_markdown_missing_marker:{rel}:{marker}")
    errors.extend(f"prototype_text_dangerous:{rel}:{err.rsplit(':', 1)[-1]}" for err in scan_dangerous_values(text, rel))
    return errors


def validate_prototype_html_text(rel: str, html: str) -> list[str]:
    errors = []
    for attr in [
        'data-sandbox-only="true"',
        'data-read-only-workflow="true"',
        'data-non-executable="true"',
        'data-no-formal-vault-access="true"',
        'data-no-write="true"',
        'data-no-sync="true"',
        'data-no-authority="true"',
        'data-no-approval="true"',
        'data-no-user-wording="true"',
        'data-no-command="true"',
    ]:
        if attr not in html:
            errors.append(f"html_missing_attr:{attr}")
    for marker in [SLICE_ID, *SOURCE_SLICES, "READ_ONLY_PRODUCT_WORKFLOW"]:
        if marker not in html:
            errors.append(f"html_missing_marker:{marker}")
    lower = html.lower()
    if lower.count("<form"):
        errors.append("html_contains_form")
    if lower.count("download="):
        errors.append("html_contains_download")
    if lower.count("contenteditable"):
        errors.append("html_contains_contenteditable")
    if lower.count("<a "):
        errors.append("html_contains_anchor")
    cards = re.findall(r'data-step="([^"]+)"', html)
    if cards != STEP_IDS:
        errors.append(f"html_step_cards_mismatch:{cards}:expected:{STEP_IDS}")
    errors.extend(f"prototype_text_dangerous:{rel}:{err.rsplit(':', 1)[-1]}" for err in scan_dangerous_values(html, rel))
    return sorted(set(errors))


def validate_prototype_receipt(receipt: dict[str, Any]) -> list[str]:
    errors = []
    if receipt.get("record_kind") != "sandbox_read_only_product_workflow_prototype_receipt":
        errors.append("prototype_receipt_kind_mismatch")
    if receipt.get("slice_id") != SLICE_ID:
        errors.append("prototype_receipt_slice_id_mismatch")
    if receipt.get("step_count") != len(STEP_IDS):
        errors.append("prototype_receipt_step_count_mismatch")
    if receipt.get("check_count") != len(CHECK_IDS):
        errors.append("prototype_receipt_check_count_mismatch")
    for false_key in [
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
        "workflow_used_as_action_basis",
        "dirty_tree_fixed",
        "auto_advanced",
    ]:
        if receipt.get(false_key) is not False:
            errors.append(f"prototype_receipt_flag_not_false:{false_key}")
    if not NON_CLAIMS.issubset(set(receipt.get("non_claims", []))):
        errors.append("prototype_receipt_non_claims_missing")
    return sorted(set(errors))


def inspect_prototype() -> dict[str, Any]:
    prototype_path = ROOT / "prototype" / "formal-vault-read-only-product-workflow"
    receipt_path = prototype_path / "Receipts" / "workflow-prototype-receipt.json"
    html_path = prototype_path / "workflow-prototype-inspector.html"
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
        issues.extend(validate_prototype_html_text("workflow-prototype-inspector.html", html))
        lower = html.lower()
        html_summary = {
            "sandbox_only": 'data-sandbox-only="true"' in html,
            "read_only_workflow": 'data-read-only-workflow="true"' in html,
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
            "steps": re.findall(r'data-step="([^"]+)"', html),
        }
    else:
        issues.append("missing_workflow_html")
    return {"prototype_path": str(prototype_path), "issues": sorted(set(issues)), "receipt": receipt, "html": html_summary}


def validate_prototype_tamper(tamper: dict[str, Any]) -> list[str]:
    if tamper.get("kind") == "markdown_replace":
        return validate_prototype_markdown_text(tamper.get("file", "unknown.md"), tamper.get("content", ""))
    if tamper.get("kind") == "html_replace":
        return validate_prototype_html_text(tamper.get("file", "workflow-prototype-inspector.html"), tamper.get("content", ""))
    receipt_path = ROOT / "prototype" / "formal-vault-read-only-product-workflow" / "Receipts" / "workflow-prototype-receipt.json"
    base_receipt = read_json_path(receipt_path) if receipt_path.exists() else {}
    if tamper.get("kind") == "receipt_update":
        receipt = copy.deepcopy(base_receipt)
        receipt.update(tamper.get("updates", {}))
        return validate_prototype_receipt(receipt)
    return ["unknown_prototype_tamper_kind"]


def load_failure_oracle() -> dict[str, Any]:
    return read_json_path(ROOT / "artifact" / "failure-case-oracle.json")


def validate_failure_cases() -> dict[str, Any]:
    oracle = load_failure_oracle()
    expected_cases = oracle.get("cases", {})
    actual_files = sorted(path.name for path in (ROOT / "failure-cases").glob("*.json"))
    mismatches = []
    if sorted(expected_cases) != actual_files:
        mismatches.append("failure_case_file_set_mismatch")
    for filename in actual_files:
        payload = read_json_path(ROOT / "failure-cases" / filename)
        candidate = payload.get("candidate")
        expected_errors = payload.get("expected_errors", [])
        actual_errors = validate_config(candidate)
        if not set(expected_errors).issubset(set(actual_errors)):
            mismatches.append(f"failure_case_mismatch:{filename}:actual={actual_errors}:expected_subset={expected_errors}")
    return {"count": len(actual_files), "mismatches": mismatches}


def _rehash_for_probe(config: dict[str, Any]) -> None:
    if isinstance(config.get("workflow_receipt"), dict):
        config["workflow_receipt"]["workflow_hash"] = workflow_hash_without_hash(config)


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
    add_probe("manual-control-approval", ["workflow_controls", "no_approval_collection"], False, ["workflow_control_mismatch:no_approval_collection"])
    add_probe("manual-payload-action-basis", ["workflow_payload", "operator_can_create_action_basis"], True, ["workflow_payload_flag_not_false:operator_can_create_action_basis", "workflow_payload_mismatch"])
    add_probe("manual-binding-mainline", ["source_surface_binding", "mainline_ready"], True, ["source_binding_flag_not_false:mainline_ready", "source_surface_binding_mismatch"])
    add_probe("manual-receipt-permission", ["workflow_receipt", "execution_permission_granted"], True, ["workflow_receipt_flag_not_false:execution_permission_granted"])

    prototype_probes = [
        ("manual-prototype-missing-markers", {"kind": "markdown_replace", "file": "00 Workflow Home.md", "content": "# Workflow\n\nGeneric."}, [f"prototype_markdown_missing_marker:00 Workflow Home.md:{SLICE_ID}"]),
        ("manual-prototype-command", {"kind": "html_replace", "file": "workflow-prototype-inspector.html", "content": "<html><body>python tools/promote.py --sync</body></html>"}, ["prototype_text_dangerous:workflow-prototype-inspector.html:python_command"]),
        ("manual-prototype-run-now", {"kind": "html_replace", "file": "workflow-prototype-inspector.html", "content": "<html><body><button>Run now</button></body></html>"}, ["prototype_text_dangerous:workflow-prototype-inspector.html:run_now"]),
        ("manual-prototype-approval", {"kind": "markdown_replace", "file": "04 Stop Conditions.md", "content": "approval collected: yes"}, ["prototype_text_dangerous:04 Stop Conditions.md:approval_collected_marker"]),
        ("manual-prototype-mainline", {"kind": "markdown_replace", "file": "04 Stop Conditions.md", "content": "mainline ready: yes"}, ["prototype_text_dangerous:04 Stop Conditions.md:mainline_ready_marker"]),
        ("manual-prototype-receipt-action-basis", {"kind": "receipt_update", "updates": {"workflow_used_as_action_basis": True}}, ["prototype_receipt_flag_not_false:workflow_used_as_action_basis"]),
        ("manual-prototype-receipt-count", {"kind": "receipt_update", "updates": {"step_count": 99}}, ["prototype_receipt_step_count_mismatch"]),
    ]
    for name, tamper, expected in prototype_probes:
        probes.append({"name": name, "expected_errors": expected, "actual_errors": validate_prototype_tamper(tamper)})

    mismatches = []
    for probe in probes:
        if not set(probe["expected_errors"]).issubset(set(probe["actual_errors"])):
            mismatches.append(f"manual_probe_mismatch:{probe['name']}:actual={probe['actual_errors']}:expected_subset={probe['expected_errors']}")
    return {"count": len(probes), "mismatches": mismatches, "probes": probes}


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


def validate_all(final_gate: bool = False) -> dict[str, Any]:
    fixture_results = []
    for path in sorted((ROOT / "fixtures").glob("*.json")):
        fixture_results.append({"file": path.name, "errors": validate_config(read_json_path(path))})
    failure_results = validate_failure_cases()
    manual_results = run_manual_negative_probes()
    prototype = inspect_prototype()
    reports = check_required_reports(final_gate=final_gate)
    failures = []
    for result in fixture_results:
        if result["errors"]:
            failures.append(f"fixture_failed:{result['file']}:{result['errors']}")
    if failure_results["mismatches"]:
        failures.extend(failure_results["mismatches"])
    if manual_results["mismatches"]:
        failures.extend(manual_results["mismatches"])
    if prototype["issues"]:
        failures.extend(prototype["issues"])
    if reports["issues"]:
        failures.extend(reports["issues"])
    return {
        "slice_id": SLICE_ID,
        "passed": not failures,
        "failures": failures,
        "positive_fixtures": fixture_results,
        "failure_cases": failure_results,
        "manual_negative_probes": manual_results,
        "prototype": prototype,
        "required_reports": reports,
        "non_claims": [
            "sandbox read-only workflow only",
            "not actual approval",
            "not user instruction",
            "not run permission",
            "not reviewed knowledge",
            "not evidence support",
            "not action basis",
            "not mainline readiness",
            "not formal vault approval",
        ],
    }
