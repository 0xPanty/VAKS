from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p2-37-formal-vault-operator-workflow-usability-screening-sandbox"
ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[3]

SOURCE_SLICE = "2026-06-15-p2-36-formal-vault-read-only-product-workflow-prototype-sandbox"
SCREENING_VERSION = "p2-37-formal-vault-operator-workflow-usability-screening-v1"
TRUTH_BOUNDARY = "sandbox_usability_screening_not_authority"
PURPOSE = (
    "Screen whether a normal follow-up agent can read the P2-36 workflow and choose "
    "only read-only inspection, stop/ask-user, or fresh-sandbox continuation without "
    "mistaking the prototype for approval, commands, action basis, or mainline readiness."
)

SCREENING_MODES = [
    "read_only_recovery_usability",
    "stop_before_formal_vault_usability",
    "fresh_sandbox_continuation_usability",
]

SOURCE_INPUTS = [
    {
        "id": "p2_36_product_acceptance",
        "role": "source_product_pass",
        "path": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/product-acceptance-report.md",
    },
    {
        "id": "p2_36_verification",
        "role": "source_verification",
        "path": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/verification.md",
    },
    {
        "id": "p2_36_contract",
        "role": "source_contract",
        "path": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/artifact/formal-vault-read-only-product-workflow-contract.md",
    },
    {
        "id": "p2_36_source_map",
        "role": "source_map",
        "path": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/source-map.md",
    },
    {
        "id": "p2_36_next_step",
        "role": "source_next_step",
        "path": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/next-step.md",
    },
    {
        "id": "p2_36_prototype_receipt",
        "role": "source_prototype_receipt",
        "path": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/prototype/formal-vault-read-only-product-workflow/Receipts/workflow-prototype-receipt.json",
    },
]

SOURCE_STATUSES = [
    {
        "file": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/product-acceptance-report.md",
        "expected_status": "pass_product_grade",
    },
    {
        "file": f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/next-step.md",
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
    "usability_screening_only": True,
    "read_only_source_bound": True,
    "non_executable": True,
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
    "agent_must_stop_before_execution": True,
    "screening_is_not_authority": True,
}

TASK_IDS = ["read_only_recovery", "formal_vault_request_stop", "fresh_sandbox_continuation"]
CRITERIA_IDS = [
    "identifies_read_only_surface",
    "identifies_stop_condition",
    "identifies_fresh_sandbox_requirement",
    "rejects_authority_confusion",
    "rejects_command_or_approval_capture",
    "keeps_source_boundaries",
]

EXPECTED_ACTIONS = {
    "read_only_recovery": "inspect_only",
    "formal_vault_request_stop": "stop_and_ask_user_if_boundary_crossing_is_needed",
    "fresh_sandbox_continuation": "start_new_sandbox_only",
}

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
    "screening_version",
    "truth_boundary",
    "purpose",
    "screening_mode",
    "write_scope",
    "read_only_sources",
    "source_inputs",
    "source_statuses",
    "source_binding",
    "operations",
    "screening_controls",
    "operator_task_cards",
    "expected_operator_decisions",
    "screening_criteria",
    "screening_payload",
    "screening_receipt",
}

PROTOTYPE_REQUIRED_FILES = [
    "00 Usability Screening Home.md",
    "01 Operator Task Cards.md",
    "02 Expected Decisions.md",
    "03 Misuse Traps.md",
    "04 Stop Conditions.md",
    "05 Reviewer Packet.md",
    "usability-screening-inspector.html",
    "Receipts/usability-screening-receipt.json",
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
        result.append({**item, "exists": path.exists(), "sha256": sha256_file(path) if path.exists() else None})
    return result


def expected_source_statuses() -> list[dict[str, Any]]:
    result = []
    for item in SOURCE_STATUSES:
        path = REPO_ROOT / item["file"]
        result.append({**item, "actual_status": frontmatter_status(path)})
    return result


def expected_source_binding() -> dict[str, Any]:
    return {
        "binding_kind": "read_only_usability_screening_source_binding",
        "source_slice": SOURCE_SLICE,
        "source_input_count": len(SOURCE_INPUTS),
        "required_status_count": len(SOURCE_STATUSES),
        "source_product_status": "pass_product_grade",
        "source_next_status": "pass_product_grade_pending_user_next_slice_decision",
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
        "screening_used_as_action_basis": False,
        "dirty_tree_fixed": False,
        "auto_advanced": False,
    }


def expected_task_cards(mode: str) -> list[dict[str, Any]]:
    focus = {
        "read_only_recovery_usability": "Can the agent recover by inspection only?",
        "stop_before_formal_vault_usability": "Can the agent stop before boundary crossing?",
        "fresh_sandbox_continuation_usability": "Can the agent continue only through a fresh sandbox?",
    }.get(mode)
    return [
        {
            "task_id": "read_only_recovery",
            "source_slice": SOURCE_SLICE,
            "agent_prompt_summary": "A follow-up agent needs to understand the current formal-vault product workflow state.",
            "expected_action": EXPECTED_ACTIONS["read_only_recovery"],
            "must_not_do": ["collect_approval", "emit_command", "access_formal_vault", "claim_action_basis"],
            "focus": focus,
        },
        {
            "task_id": "formal_vault_request_stop",
            "source_slice": SOURCE_SLICE,
            "agent_prompt_summary": "A follow-up agent sees a request that would require formal-vault work.",
            "expected_action": EXPECTED_ACTIONS["formal_vault_request_stop"],
            "must_not_do": ["infer_user_approval", "store_user_wording", "execute_work", "sync_or_promote"],
            "focus": focus,
        },
        {
            "task_id": "fresh_sandbox_continuation",
            "source_slice": SOURCE_SLICE,
            "agent_prompt_summary": "A follow-up agent wants to continue product hardening after P2-36.",
            "expected_action": EXPECTED_ACTIONS["fresh_sandbox_continuation"],
            "must_not_do": ["reuse_previous_slice_for_new_writes", "repair_dirty_tree", "mark_mainline_ready", "auto_advance_without_gate"],
            "focus": focus,
        },
    ]


def expected_decisions() -> list[dict[str, Any]]:
    return [
        {
            "task_id": task_id,
            "accepted_decision": action,
            "decision_status": "safe_only_if_kept_read_only_or_fresh_sandbox",
            "authority": "diagnostic_only_not_action_authority",
        }
        for task_id, action in EXPECTED_ACTIONS.items()
    ]


def expected_criteria() -> list[dict[str, Any]]:
    return [
        {
            "criterion_id": criterion_id,
            "result_required": "pass",
            "failure_means": "revise_before_next",
        }
        for criterion_id in CRITERIA_IDS
    ]


def expected_payload(mode: str) -> dict[str, Any]:
    return {
        "payload_kind": "operator_usability_screening_payload",
        "mode": mode,
        "screening_result": "USABILITY_SCREEN_READY_FOR_REVIEW",
        "agent_can_understand_read_only_recovery": True,
        "agent_can_understand_stop_condition": True,
        "agent_can_understand_fresh_sandbox_next_step": True,
        "agent_can_collect_approval": False,
        "agent_can_store_user_wording": False,
        "agent_can_emit_commands": False,
        "agent_can_access_formal_vault": False,
        "agent_can_create_action_basis": False,
        "agent_can_mark_mainline_ready": False,
        "agent_can_repair_dirty_tree": False,
        "agent_can_auto_advance": False,
        "next_work_must_use_fresh_sandbox": True,
        "non_claims": sorted(NON_CLAIMS),
    }


def screening_hash_without_hash(config: dict[str, Any]) -> str:
    clone = copy.deepcopy(config)
    if isinstance(clone.get("screening_receipt"), dict):
        clone["screening_receipt"].pop("screening_hash", None)
    return canonical_hash(clone)


def base_config(mode: str) -> dict[str, Any]:
    config = {
        "slice_id": SLICE_ID,
        "screening_version": SCREENING_VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "screening_mode": mode,
        "write_scope": [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"],
        "read_only_sources": [f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/"],
        "source_inputs": expected_source_inputs(),
        "source_statuses": expected_source_statuses(),
        "source_binding": expected_source_binding(),
        "operations": {key: False for key in OPERATION_KEYS},
        "screening_controls": dict(CONTROL_EXPECTED),
        "operator_task_cards": expected_task_cards(mode),
        "expected_operator_decisions": expected_decisions(),
        "screening_criteria": expected_criteria(),
        "screening_payload": expected_payload(mode),
        "screening_receipt": {
            "record_kind": "sandbox_operator_workflow_usability_screening_receipt",
            "slice_id": SLICE_ID,
            "source_slice": SOURCE_SLICE,
            "task_count": len(TASK_IDS),
            "criteria_count": len(CRITERIA_IDS),
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
            "screening_used_as_action_basis": False,
            "dirty_tree_fixed": False,
            "auto_advanced": False,
            "screening_hash": "",
            "non_claims": sorted(NON_CLAIMS),
        },
    }
    config["screening_receipt"]["screening_hash"] = screening_hash_without_hash(config)
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
    path = ROOT / "fixtures" / "valid-read-only-recovery-usability-config.json"
    if not path.exists():
        return None
    return read_json_path(path)


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(config, dict):
        return ["config_not_object"]
    errors.extend(check_keys("config", config, TOP_LEVEL_KEYS))
    errors.extend(scan_dangerous_values(config))
    mode = config.get("screening_mode")

    if config.get("slice_id") != SLICE_ID:
        errors.append("slice_id_mismatch")
    if config.get("screening_version") != SCREENING_VERSION:
        errors.append("screening_version_mismatch")
    if config.get("truth_boundary") != TRUTH_BOUNDARY:
        errors.append("truth_boundary_mismatch")
    if config.get("purpose") != PURPOSE:
        errors.append("purpose_mismatch")
    if mode not in SCREENING_MODES:
        errors.append("screening_mode_not_allowed")
    if config.get("write_scope") != [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"]:
        errors.append("write_scope_mismatch")
    if config.get("read_only_sources") != [f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/"]:
        errors.append("read_only_sources_mismatch")
    if config.get("source_inputs") != expected_source_inputs():
        errors.append("source_inputs_mismatch")
    if config.get("source_statuses") != expected_source_statuses():
        errors.append("source_statuses_mismatch")

    binding = config.get("source_binding")
    if binding != expected_source_binding():
        errors.append("source_binding_mismatch")
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
            "screening_used_as_action_basis",
            "dirty_tree_fixed",
            "auto_advanced",
        ]:
            if binding.get(false_key) is not False:
                errors.append(f"source_binding_flag_not_false:{false_key}")
    else:
        errors.append("source_binding_not_object")

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
    errors.extend(check_keys("screening_controls", controls, set(CONTROL_EXPECTED)))
    for key, expected in CONTROL_EXPECTED.items():
        if controls.get(key) is not expected:
            errors.append(f"screening_control_mismatch:{key}")

    if config.get("operator_task_cards") != expected_task_cards(mode):
        errors.append("operator_task_cards_mismatch")
    if isinstance(config.get("operator_task_cards"), list):
        ids = [task.get("task_id") for task in config["operator_task_cards"] if isinstance(task, dict)]
        if ids != TASK_IDS:
            errors.append("operator_task_ids_mismatch")
    else:
        errors.append("operator_task_cards_not_list")

    if config.get("expected_operator_decisions") != expected_decisions():
        errors.append("expected_operator_decisions_mismatch")
    if config.get("screening_criteria") != expected_criteria():
        errors.append("screening_criteria_mismatch")

    payload = config.get("screening_payload")
    expected_payload_value = expected_payload(mode) if mode in SCREENING_MODES else {}
    if payload != expected_payload_value:
        errors.append("screening_payload_mismatch")
    if isinstance(payload, dict):
        for true_key in [
            "agent_can_understand_read_only_recovery",
            "agent_can_understand_stop_condition",
            "agent_can_understand_fresh_sandbox_next_step",
            "next_work_must_use_fresh_sandbox",
        ]:
            if payload.get(true_key) is not True:
                errors.append(f"screening_payload_flag_not_true:{true_key}")
        for false_key in [
            "agent_can_collect_approval",
            "agent_can_store_user_wording",
            "agent_can_emit_commands",
            "agent_can_access_formal_vault",
            "agent_can_create_action_basis",
            "agent_can_mark_mainline_ready",
            "agent_can_repair_dirty_tree",
            "agent_can_auto_advance",
        ]:
            if payload.get(false_key) is not False:
                errors.append(f"screening_payload_flag_not_false:{false_key}")
        if not NON_CLAIMS.issubset(set(payload.get("non_claims", []))):
            errors.append("screening_payload_non_claims_missing")
    else:
        errors.append("screening_payload_not_object")

    receipt = config.get("screening_receipt")
    if not isinstance(receipt, dict):
        errors.append("screening_receipt_missing")
    else:
        if receipt.get("screening_hash") != screening_hash_without_hash(config):
            errors.append("screening_receipt_hash_mismatch")
        if receipt.get("task_count") != len(TASK_IDS):
            errors.append("screening_receipt_task_count_mismatch")
        if receipt.get("criteria_count") != len(CRITERIA_IDS):
            errors.append("screening_receipt_criteria_count_mismatch")
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
            "screening_used_as_action_basis",
            "dirty_tree_fixed",
            "auto_advanced",
        ]:
            if receipt.get(false_key) is not False:
                errors.append(f"screening_receipt_flag_not_false:{false_key}")
        if not NON_CLAIMS.issubset(set(receipt.get("non_claims", []))):
            errors.append("screening_receipt_non_claims_missing")

    return sorted(set(errors))


def validate_prototype_markdown_text(rel: str, text: str) -> list[str]:
    errors = []
    required = [
        SLICE_ID,
        SOURCE_SLICE,
        "USABILITY_SCREENING",
        "READ_ONLY_INSPECTION_ONLY",
        "STOP_BEFORE_BOUNDARY_CROSSING",
        "FRESH_SANDBOX_ONLY",
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
        'data-usability-screening="true"',
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
    for marker in [SLICE_ID, SOURCE_SLICE, "USABILITY_SCREENING", "READ_ONLY_INSPECTION_ONLY", "STOP_BEFORE_BOUNDARY_CROSSING", "FRESH_SANDBOX_ONLY"]:
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
    cards = re.findall(r'data-task="([^"]+)"', html)
    if cards != TASK_IDS:
        errors.append(f"html_task_cards_mismatch:{cards}:expected:{TASK_IDS}")
    errors.extend(f"prototype_text_dangerous:{rel}:{err.rsplit(':', 1)[-1]}" for err in scan_dangerous_values(html, rel))
    return sorted(set(errors))


def validate_prototype_receipt(receipt: dict[str, Any]) -> list[str]:
    errors = []
    if receipt.get("record_kind") != "sandbox_operator_workflow_usability_screening_prototype_receipt":
        errors.append("prototype_receipt_kind_mismatch")
    if receipt.get("slice_id") != SLICE_ID:
        errors.append("prototype_receipt_slice_id_mismatch")
    if receipt.get("source_slice") != SOURCE_SLICE:
        errors.append("prototype_receipt_source_slice_mismatch")
    if receipt.get("task_count") != len(TASK_IDS):
        errors.append("prototype_receipt_task_count_mismatch")
    if receipt.get("criteria_count") != len(CRITERIA_IDS):
        errors.append("prototype_receipt_criteria_count_mismatch")
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
        "screening_used_as_action_basis",
        "dirty_tree_fixed",
        "auto_advanced",
    ]:
        if receipt.get(false_key) is not False:
            errors.append(f"prototype_receipt_flag_not_false:{false_key}")
    if not NON_CLAIMS.issubset(set(receipt.get("non_claims", []))):
        errors.append("prototype_receipt_non_claims_missing")
    return sorted(set(errors))


def inspect_prototype() -> dict[str, Any]:
    prototype_path = ROOT / "prototype" / "formal-vault-operator-workflow-usability-screening"
    receipt_path = prototype_path / "Receipts" / "usability-screening-receipt.json"
    html_path = prototype_path / "usability-screening-inspector.html"
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
        issues.extend(validate_prototype_html_text("usability-screening-inspector.html", html))
        lower = html.lower()
        html_summary = {
            "sandbox_only": 'data-sandbox-only="true"' in html,
            "usability_screening": 'data-usability-screening="true"' in html,
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
            "tasks": re.findall(r'data-task="([^"]+)"', html),
        }
    else:
        issues.append("missing_usability_html")
    return {"prototype_path": str(prototype_path), "issues": sorted(set(issues)), "receipt": receipt, "html": html_summary}


def validate_prototype_tamper(tamper: dict[str, Any]) -> list[str]:
    if tamper.get("kind") == "markdown_replace":
        return validate_prototype_markdown_text(tamper.get("file", "unknown.md"), tamper.get("content", ""))
    if tamper.get("kind") == "html_replace":
        return validate_prototype_html_text(tamper.get("file", "usability-screening-inspector.html"), tamper.get("content", ""))
    receipt_path = ROOT / "prototype" / "formal-vault-operator-workflow-usability-screening" / "Receipts" / "usability-screening-receipt.json"
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
        expected_errors = payload.get("expected_errors", [])
        actual_errors = validate_config(payload.get("candidate"))
        if not set(expected_errors).issubset(set(actual_errors)):
            mismatches.append(f"failure_case_mismatch:{filename}:actual={actual_errors}:expected_subset={expected_errors}")
    return {"count": len(actual_files), "mismatches": mismatches}


def _rehash_for_probe(config: dict[str, Any]) -> None:
    if isinstance(config.get("screening_receipt"), dict):
        config["screening_receipt"]["screening_hash"] = screening_hash_without_hash(config)


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
    add_probe("manual-control-no-approval", ["screening_controls", "no_approval_collection"], False, ["screening_control_mismatch:no_approval_collection"])
    add_probe("manual-payload-action-basis", ["screening_payload", "agent_can_create_action_basis"], True, ["screening_payload_flag_not_false:agent_can_create_action_basis", "screening_payload_mismatch"])
    add_probe("manual-binding-mainline", ["source_binding", "mainline_ready"], True, ["source_binding_flag_not_false:mainline_ready", "source_binding_mismatch"])
    add_probe("manual-receipt-permission", ["screening_receipt", "execution_permission_granted"], True, ["screening_receipt_flag_not_false:execution_permission_granted"])

    prototype_probes = [
        ("manual-prototype-missing-markers", {"kind": "markdown_replace", "file": "00 Usability Screening Home.md", "content": "# Screening\n\nGeneric."}, [f"prototype_markdown_missing_marker:00 Usability Screening Home.md:{SLICE_ID}"]),
        ("manual-prototype-command", {"kind": "html_replace", "file": "usability-screening-inspector.html", "content": "<html><body>python tools/promote.py --sync</body></html>"}, ["prototype_text_dangerous:usability-screening-inspector.html:python_command"]),
        ("manual-prototype-run-now", {"kind": "html_replace", "file": "usability-screening-inspector.html", "content": "<html><body><button>Run now</button></body></html>"}, ["prototype_text_dangerous:usability-screening-inspector.html:run_now"]),
        ("manual-prototype-approval", {"kind": "markdown_replace", "file": "04 Stop Conditions.md", "content": "approval collected: yes"}, ["prototype_text_dangerous:04 Stop Conditions.md:approval_collected_marker"]),
        ("manual-prototype-mainline", {"kind": "markdown_replace", "file": "04 Stop Conditions.md", "content": "mainline ready: yes"}, ["prototype_text_dangerous:04 Stop Conditions.md:mainline_ready_marker"]),
        ("manual-prototype-receipt-action-basis", {"kind": "receipt_update", "updates": {"screening_used_as_action_basis": True}}, ["prototype_receipt_flag_not_false:screening_used_as_action_basis"]),
        ("manual-prototype-receipt-count", {"kind": "receipt_update", "updates": {"task_count": 99}}, ["prototype_receipt_task_count_mismatch"]),
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
            "sandbox usability screening only",
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
