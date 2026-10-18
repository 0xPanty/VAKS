from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p2-34-formal-vault-operator-status-surface-sandbox"
ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[3]

STATUS_SURFACE_PURPOSE = (
    "Create a sandbox-only operator status surface for the P2-30 through P2-33 "
    "formal-vault safety chain without collecting approval, storing user wording, "
    "emitting commands, touching the formal vault, granting execution permission, "
    "or declaring mainline readiness."
)

SOURCE_SLICES = [
    {
        "stage_id": "p2_30_dry_run_ledger",
        "slice_id": "2026-06-15-p2-30-formal-vault-execution-dry-run-ledger-sandbox",
        "label": "Dry-run ledger",
        "result_key": "ledger_hash",
        "receipt_path": "prototype/formal-vault-execution-dry-run-ledger/Receipts/formal-vault-execution-dry-run-ledger-receipt.json",
        "contract_path": "artifact/formal-vault-execution-dry-run-ledger-contract.md",
    },
    {
        "stage_id": "p2_31_readiness_gate",
        "slice_id": "2026-06-15-p2-31-formal-vault-execution-readiness-gate-sandbox",
        "label": "Readiness gate",
        "result_key": "readiness_gate_hash",
        "receipt_path": "prototype/formal-vault-execution-readiness-gate/Receipts/formal-vault-execution-readiness-gate-receipt.json",
        "contract_path": "artifact/formal-vault-execution-readiness-gate-contract.md",
    },
    {
        "stage_id": "p2_32_request_packet",
        "slice_id": "2026-06-15-p2-32-formal-vault-execution-request-packet-sandbox",
        "label": "Request packet",
        "result_key": "request_packet_hash",
        "receipt_path": "prototype/formal-vault-execution-request-packet/Receipts/formal-vault-execution-request-packet-receipt.json",
        "contract_path": "artifact/formal-vault-execution-request-packet-contract.md",
    },
    {
        "stage_id": "p2_33_request_screening",
        "slice_id": "2026-06-15-p2-33-formal-vault-execution-request-screening-sandbox",
        "label": "Request screening",
        "result_key": "request_screening_hash",
        "receipt_path": "prototype/formal-vault-execution-request-screening/Receipts/formal-vault-execution-request-screening-receipt.json",
        "contract_path": "artifact/formal-vault-execution-request-screening-contract.md",
    },
]

REPORT_STATUS_EXPECTED = {
    "slice-plan.md": "built_pending_review",
    "source-map.md": "built_pending_review",
    "verification.md": "local_verification_passed_pending_review",
    "reviewer-report.md": "reviewer_pass",
    "boundary-audit.md": "boundary_pass",
    "product-acceptance-report.md": "pass_product_grade",
    "next-step.md": "pass_product_grade_pending_user_next_slice_decision",
}

STATUS_MODES = {
    "chain_overview_surface": "STATUS_SURFACE_CHAIN_OVERVIEW_NOT_EXECUTABLE",
    "latest_screening_focus_surface": "STATUS_SURFACE_SCREENING_FOCUS_NOT_SUBMITTED",
    "boundary_stop_focus_surface": "STATUS_SURFACE_BOUNDARY_FOCUS_STOP_BEFORE_EXECUTION",
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
    "execution_performed",
    "packet_submission",
    "screening_submission",
    "action_basis_creation",
    "reviewed_knowledge_creation",
    "evidence_support_creation",
    "mainline_merge",
    "template_write",
    "tools_write",
    "wiki_truth_write",
    "command_emitted",
    "absolute_vault_path_resolved",
    "dirty_state_resolution",
]

STATUS_CONTROL_EXPECTED = {
    "sandbox_only": True,
    "read_only_status_surface": True,
    "source_hash_bound": True,
    "existing_sandbox_only": True,
    "non_executable": True,
    "no_formal_vault_access": True,
    "no_approval_collection": True,
    "no_user_instruction": True,
    "no_user_wording": True,
    "no_commands": True,
    "no_absolute_vault_paths": True,
    "no_truth_mutation": True,
    "no_mainline_claim": True,
    "no_merge_claim": True,
    "no_replay_claim": True,
    "status_is_not_authority": True,
    "badges_are_not_approval": True,
    "dirty_state_is_process_risk_not_truth": True,
    "product_acceptance_is_not_formal_vault_approval": True,
    "operator_must_stop_before_execution": True,
    "execution_allowed_now": False,
    "formal_vault_write_allowed_now": False,
    "action_basis_ready": False,
    "reviewed_knowledge_created": False,
    "evidence_support_created": False,
    "mainline_ready": False,
    "user_approval_collected": False,
    "dirty_tree_fixed": False,
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
    "not a replay surface",
    "not dirty tree repair",
}

TOP_LEVEL_KEYS = {
    "slice_id",
    "status_surface_version",
    "truth_boundary",
    "purpose",
    "surface_mode",
    "write_scope",
    "read_only_sources",
    "operations",
    "status_controls",
    "source_inputs",
    "source_statuses",
    "operator_chain",
    "status_badges",
    "stop_lines",
    "surface_receipt",
    "product_metrics",
    "status_surface_hash",
}
SOURCE_INPUT_KEYS = {"id", "source_path", "source_sha256", "content_binding"}
SOURCE_STATUS_KEYS = {"slice_id", "file", "expected_status", "actual_status"}
CHAIN_KEYS = {
    "stage_id",
    "slice_id",
    "label",
    "product_status",
    "reviewer_status",
    "boundary_status",
    "verification_status",
    "next_status",
    "receipt_kind",
    "result_label",
    "result_hash",
    "receipt_sha256",
    "formal_vault_accessed",
    "approval_collected_now",
    "user_wording_stored",
    "execution_permission_granted",
    "execution_performed",
    "write_performed",
    "sync_performed",
    "promotion_performed",
    "used_as_action_basis",
    "submitted",
    "non_claims",
}
BADGE_KEYS = {"badge_id", "label", "status", "meaning", "non_authority"}
STOP_LINE_KEYS = {"stop_id", "label", "must_stop", "reason", "non_claim"}
RECEIPT_KEYS = {
    "record_kind",
    "slice_id",
    "surface_result",
    "source_slice_count",
    "source_input_count",
    "badge_count",
    "stop_line_count",
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
    "status_surface_hash",
    "non_claims",
}
METRIC_KEYS = {
    "required_positive_fixtures",
    "minimum_failure_cases",
    "source_slice_count",
    "source_input_count",
    "manual_negative_probes",
    "max_visible_stages",
}

PROTOTYPE_REQUIRED_FILES = [
    "00 Operator Status Home.md",
    "01 Evidence Chain.md",
    "02 Status Badges.md",
    "03 Stop Lines.md",
    "04 Reviewer Packet.md",
    "operator-status-surface.html",
    "Receipts/operator-status-surface-receipt.json",
]
PROTOTYPE_MARKDOWN_FILES = [
    "00 Operator Status Home.md",
    "01 Evidence Chain.md",
    "02 Status Badges.md",
    "03 Stop Lines.md",
    "04 Reviewer Packet.md",
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
    ("execute_now", re.compile(r"(?i)\bexecute-now\b")),
    ("ready_to_execute", re.compile(r"(?i)\bready to execute\b")),
    ("approved_for_execution", re.compile(r"(?i)\bapproved for execution\b")),
    ("execution_permission_marker", re.compile(r"(?i)\bexecution permission\s*[:=]\s*(yes|true|granted|allowed|ready)\b")),
    ("formal_vault_approval_marker", re.compile(r"(?i)\bformal vault approval\s*[:=]\s*(yes|true|granted|allowed|ready)\b")),
    ("action_basis_marker", re.compile(r"(?i)\baction basis\s*[:=]\s*(yes|true|granted|allowed|ready)\b")),
    ("mainline_ready_marker", re.compile(r"(?i)\bmainline ready\s*[:=]\s*(yes|true|ready)\b")),
    ("merge_approved_marker", re.compile(r"(?i)\bmerge approved\s*[:=]\s*(yes|true)\b")),
    ("approval_collected_marker", re.compile(r"(?i)\bapproval collected\s*[:=]\s*(yes|true)\b")),
    ("user_instruction_marker", re.compile(r"(?i)\buser instruction\s*[:=]\s*(yes|true|approved)\b")),
    ("actual_user_wording_marker", re.compile(r"(?i)\bactual user wording\s*[:=]")),
    ("absolute_formal_vault_path", re.compile(r"(?i)\b[A-Z]:[\\/][^\\n\\r]*Obsidian[\\/]")),
]

PROTOTYPE_SEMANTIC_DENY_PATTERNS = [
    ("authorizes_execution", re.compile(r"(?i)\bauthori[sz](?:es|ed|ation)?\b[^.\n]{0,80}\bexecution\b|\bexecution\b[^.\n]{0,80}\bauthori[sz](?:es|ed|ation)?\b")),
    ("may_execute", re.compile(r"(?i)\bmay execute\b")),
    ("submit_packet", re.compile(r"(?i)\bsubmit packet\b")),
    ("submit_screening", re.compile(r"(?i)\bsubmit screening\b")),
    ("start_execution", re.compile(r"(?i)\bstart execution\b")),
    ("run_now", re.compile(r"(?i)\brun now\b")),
    ("approval_obtained", re.compile(r"(?i)\bapproval obtained\b")),
    ("status_as_authority", re.compile(r"(?i)\bstatus badge\b[^.\n]{0,80}\bauthority\b")),
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
    'data-status-only="true"',
    'data-non-executable="true"',
    'data-no-formal-vault-access="true"',
    'data-no-write="true"',
    'data-no-sync="true"',
    'data-no-authority="true"',
    'data-no-approval="true"',
    'data-no-user-wording="true"',
    'data-no-command="true"',
]


def expected_stage_markers() -> list[dict[str, str]]:
    return [{"stage_id": spec["stage_id"], "slice_id": spec["slice_id"], "label": spec["label"]} for spec in SOURCE_SLICES]


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


def validate_prototype_markdown_text(rel_path: str, text: str) -> list[str]:
    errors = scan_prototype_text(rel_path, text)
    if rel_path == "00 Operator Status Home.md":
        for marker in expected_stage_markers():
            if marker["slice_id"] not in text:
                errors.append(f"prototype_markdown_missing_stage_slice:{marker['stage_id']}")
            if marker["label"] not in text:
                errors.append(f"prototype_markdown_missing_stage_label:{marker['stage_id']}")
    return errors


def validate_prototype_stage_html(html: str) -> list[str]:
    errors = []
    stage_cards = re.findall(r"<article\b[^>]*data-kind=\"stage\"[^>]*>", html)
    if len(stage_cards) != len(SOURCE_SLICES):
        errors.append(f"html_stage_card_count_mismatch:{len(stage_cards)}:expected:{len(SOURCE_SLICES)}")
    for marker in expected_stage_markers():
        if marker["slice_id"] not in html:
            errors.append(f"html_missing_stage_slice:{marker['stage_id']}")
        if marker["label"] not in html:
            errors.append(f"html_missing_stage_label:{marker['stage_id']}")
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
    errors.extend(validate_prototype_stage_html(html))
    return errors


def read_only_sources() -> list[str]:
    sources = []
    for spec in SOURCE_SLICES:
        base = f"outputs/review/vaks-implementation-sandbox/{spec['slice_id']}"
        for file_name in REPORT_STATUS_EXPECTED:
            sources.append(f"{base}/{file_name}")
        sources.append(f"{base}/{spec['contract_path']}")
        sources.append(f"{base}/{spec['receipt_path']}")
    return sources


def expected_source_inputs() -> list[dict[str, str]]:
    items = []
    for index, rel_path in enumerate(read_only_sources()):
        items.append(
            {
                "id": f"source_{index:02d}",
                "source_path": rel_path,
                "source_sha256": file_sha256(repo_path(rel_path)),
                "content_binding": "exact_source_sha256",
            }
        )
    return items


def expected_source_statuses() -> list[dict[str, str | None]]:
    statuses = []
    for spec in SOURCE_SLICES:
        base = repo_path(f"outputs/review/vaks-implementation-sandbox/{spec['slice_id']}")
        for file_name, expected in REPORT_STATUS_EXPECTED.items():
            statuses.append(
                {
                    "slice_id": spec["slice_id"],
                    "file": file_name,
                    "expected_status": expected,
                    "actual_status": frontmatter_status(base / file_name),
                }
            )
    return statuses


def receipt_for(spec: dict[str, str]) -> dict[str, Any]:
    return read_json_path(repo_path(f"outputs/review/vaks-implementation-sandbox/{spec['slice_id']}/{spec['receipt_path']}"))


def result_label(receipt: dict[str, Any]) -> str:
    for key in ["gate_result", "packet_result", "screening_result", "ledger_hash"]:
        if receipt.get(key):
            return str(receipt[key])
    return "RECORDED_NON_EXECUTING_STAGE"


def bool_receipt_flag(receipt: dict[str, Any], *names: str) -> bool:
    return any(receipt.get(name) is True for name in names)


def expected_operator_chain() -> list[dict[str, Any]]:
    chain = []
    for spec in SOURCE_SLICES:
        base = repo_path(f"outputs/review/vaks-implementation-sandbox/{spec['slice_id']}")
        receipt = receipt_for(spec)
        chain.append(
            {
                "stage_id": spec["stage_id"],
                "slice_id": spec["slice_id"],
                "label": spec["label"],
                "product_status": frontmatter_status(base / "product-acceptance-report.md"),
                "reviewer_status": frontmatter_status(base / "reviewer-report.md"),
                "boundary_status": frontmatter_status(base / "boundary-audit.md"),
                "verification_status": frontmatter_status(base / "verification.md"),
                "next_status": frontmatter_status(base / "next-step.md"),
                "receipt_kind": receipt.get("record_kind"),
                "result_label": result_label(receipt),
                "result_hash": receipt.get(spec["result_key"], ""),
                "receipt_sha256": file_sha256(base / spec["receipt_path"]),
                "formal_vault_accessed": bool_receipt_flag(receipt, "formal_vault_accessed"),
                "approval_collected_now": bool_receipt_flag(receipt, "approval_collected_now"),
                "user_wording_stored": bool_receipt_flag(receipt, "real_user_text_stored", "actual_user_wording_stored"),
                "execution_permission_granted": bool_receipt_flag(receipt, "execution_permission_granted"),
                "execution_performed": bool_receipt_flag(receipt, "execution_performed"),
                "write_performed": bool_receipt_flag(receipt, "write_performed"),
                "sync_performed": bool_receipt_flag(receipt, "sync_performed"),
                "promotion_performed": bool_receipt_flag(receipt, "promotion_performed"),
                "used_as_action_basis": bool_receipt_flag(
                    receipt,
                    "ledger_used_as_action_basis",
                    "gate_used_as_action_basis",
                    "packet_used_as_action_basis",
                    "screening_used_as_action_basis",
                ),
                "submitted": bool_receipt_flag(receipt, "packet_submitted", "packet_submitted_to_gate", "screening_submitted"),
                "non_claims": sorted(set(receipt.get("non_claims", []))),
            }
        )
    return chain


def expected_badges(mode: str) -> list[dict[str, str | bool]]:
    return [
        {
            "badge_id": "sandbox_product_grade",
            "label": "Sandbox product-grade chain",
            "status": STATUS_MODES[mode],
            "meaning": "All displayed stages passed sandbox Product Acceptance.",
            "non_authority": True,
        },
        {
            "badge_id": "formal_vault_stop",
            "label": "Formal vault untouched",
            "status": "STOP_BEFORE_FORMAL_VAULT",
            "meaning": "No displayed receipt records formal-vault access or write.",
            "non_authority": True,
        },
        {
            "badge_id": "approval_stop",
            "label": "No approval collected",
            "status": "NO_ACTUAL_APPROVAL",
            "meaning": "The surface does not collect approval or user wording.",
            "non_authority": True,
        },
        {
            "badge_id": "mainline_stop",
            "label": "Not mainline-ready",
            "status": "SANDBOX_ONLY_NOT_MAINLINE",
            "meaning": "The surface is navigation/status only.",
            "non_authority": True,
        },
    ]


def expected_stop_lines() -> list[dict[str, Any]]:
    return [
        {
            "stop_id": "stop_before_execution",
            "label": "Stop before execution",
            "must_stop": True,
            "reason": "No slice grants current execution permission.",
            "non_claim": "status_surface_is_not_execution_permission",
        },
        {
            "stop_id": "stop_before_approval_collection",
            "label": "Stop before approval collection",
            "must_stop": True,
            "reason": "This surface displays status and cannot collect user intent.",
            "non_claim": "status_surface_is_not_user_instruction",
        },
        {
            "stop_id": "stop_before_formal_vault",
            "label": "Stop before formal vault",
            "must_stop": True,
            "reason": "This surface never reads, writes, hashes, snapshots, or syncs the formal vault.",
            "non_claim": "status_surface_is_not_formal_vault_state",
        },
        {
            "stop_id": "stop_before_mainline",
            "label": "Stop before mainline",
            "must_stop": True,
            "reason": "Sandbox Product Acceptance is not merge approval.",
            "non_claim": "status_surface_is_not_mainline_readiness",
        },
    ]


def expected_surface_hash(config: dict[str, Any]) -> str:
    clone = copy.deepcopy(config)
    clone.pop("status_surface_hash", None)
    if isinstance(clone.get("surface_receipt"), dict):
        clone["surface_receipt"].pop("status_surface_hash", None)
    return canonical_hash(clone)


def current_valid_config() -> dict[str, Any] | None:
    path = ROOT / "fixtures" / "valid-chain-overview-status-surface-config.json"
    if not path.exists():
        return None
    return read_json_path(path)


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(config, dict):
        return ["config_not_object"]
    errors.extend(check_keys("config", config, TOP_LEVEL_KEYS))
    errors.extend(scan_dangerous_values(config))
    mode = config.get("surface_mode")
    if config.get("slice_id") != SLICE_ID:
        errors.append("slice_id_mismatch")
    if config.get("status_surface_version") != "p2-34-formal-vault-operator-status-surface-v1":
        errors.append("status_surface_version_mismatch")
    if config.get("truth_boundary") != "sandbox_only_operator_status_not_authority":
        errors.append("truth_boundary_mismatch")
    if config.get("purpose") != STATUS_SURFACE_PURPOSE:
        errors.append("purpose_mismatch")
    if mode not in STATUS_MODES:
        errors.append("surface_mode_not_allowed")
    if config.get("write_scope") != [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"]:
        errors.append("write_scope_mismatch")
    if config.get("read_only_sources") != read_only_sources():
        errors.append("read_only_sources_mismatch")

    operations = config.get("operations")
    if not isinstance(operations, dict):
        errors.append("operations_missing")
        operations = {}
    errors.extend(check_keys("operations", operations, set(OPERATION_KEYS)))
    for key in OPERATION_KEYS:
        if operations.get(key) is not False:
            errors.append(f"operation_not_false:{key}")

    controls = config.get("status_controls")
    if not isinstance(controls, dict):
        errors.append("status_controls_missing")
        controls = {}
    errors.extend(check_keys("status_controls", controls, set(STATUS_CONTROL_EXPECTED)))
    for key, expected in STATUS_CONTROL_EXPECTED.items():
        if controls.get(key) is not expected:
            errors.append(f"status_control_mismatch:{key}")

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
            errors.extend(check_keys(f"source_statuses[{item.get('slice_id', 'unknown')}:{item.get('file', 'unknown')}]", item, SOURCE_STATUS_KEYS))
            if item.get("expected_status") != item.get("actual_status"):
                errors.append(f"source_status_not_met:{item.get('slice_id')}:{item.get('file')}")
    else:
        errors.append("source_statuses_not_list")

    chain = config.get("operator_chain")
    if chain != expected_operator_chain():
        errors.append("operator_chain_mismatch")
    if isinstance(chain, list):
        if len(chain) != len(SOURCE_SLICES):
            errors.append("operator_chain_length_mismatch")
        for item in chain:
            errors.extend(check_keys(f"operator_chain[{item.get('stage_id', 'unknown')}]", item, CHAIN_KEYS))
            for status_key, expected in [
                ("product_status", "pass_product_grade"),
                ("reviewer_status", "reviewer_pass"),
                ("boundary_status", "boundary_pass"),
                ("verification_status", "local_verification_passed_pending_review"),
                ("next_status", "pass_product_grade_pending_user_next_slice_decision"),
            ]:
                if item.get(status_key) != expected:
                    errors.append(f"operator_chain_status_bad:{item.get('stage_id')}:{status_key}")
            for false_key in [
                "formal_vault_accessed",
                "approval_collected_now",
                "user_wording_stored",
                "execution_permission_granted",
                "execution_performed",
                "write_performed",
                "sync_performed",
                "promotion_performed",
                "used_as_action_basis",
                "submitted",
            ]:
                if item.get(false_key) is not False:
                    errors.append(f"operator_chain_flag_not_false:{item.get('stage_id')}:{false_key}")
            if not {"not action basis", "not reviewed knowledge", "not evidence support"}.issubset(set(item.get("non_claims", []))):
                errors.append(f"operator_chain_non_claims_missing:{item.get('stage_id')}")
    else:
        errors.append("operator_chain_not_list")

    badges = config.get("status_badges")
    expected_badge_rows = expected_badges(mode) if mode in STATUS_MODES else []
    if badges != expected_badge_rows:
        errors.append("status_badges_mismatch")
    if isinstance(badges, list):
        for item in badges:
            errors.extend(check_keys(f"status_badges[{item.get('badge_id', 'unknown')}]", item, BADGE_KEYS))
            if item.get("non_authority") is not True:
                errors.append(f"status_badge_authority_confusion:{item.get('badge_id')}")
    else:
        errors.append("status_badges_not_list")

    stop_lines = config.get("stop_lines")
    if stop_lines != expected_stop_lines():
        errors.append("stop_lines_mismatch")
    if isinstance(stop_lines, list):
        for item in stop_lines:
            errors.extend(check_keys(f"stop_lines[{item.get('stop_id', 'unknown')}]", item, STOP_LINE_KEYS))
            if item.get("must_stop") is not True:
                errors.append(f"stop_line_not_must_stop:{item.get('stop_id')}")
    else:
        errors.append("stop_lines_not_list")

    receipt = config.get("surface_receipt")
    if not isinstance(receipt, dict):
        errors.append("surface_receipt_missing")
        receipt = {}
    errors.extend(check_keys("surface_receipt", receipt, RECEIPT_KEYS))
    if receipt.get("record_kind") != "sandbox_formal_vault_operator_status_surface_receipt":
        errors.append("receipt_record_kind_mismatch")
    if receipt.get("slice_id") != SLICE_ID:
        errors.append("receipt_slice_id_mismatch")
    if receipt.get("surface_result") != STATUS_MODES.get(mode):
        errors.append("receipt_surface_result_mismatch")
    if receipt.get("source_slice_count") != len(SOURCE_SLICES):
        errors.append("receipt_source_slice_count_mismatch")
    if receipt.get("source_input_count") != len(read_only_sources()):
        errors.append("receipt_source_input_count_mismatch")
    if receipt.get("badge_count") != len(expected_badges(mode)) if mode in STATUS_MODES else True:
        errors.append("receipt_badge_count_mismatch")
    if receipt.get("stop_line_count") != len(expected_stop_lines()):
        errors.append("receipt_stop_line_count_mismatch")
    if receipt.get("status_surface_hash") != expected_surface_hash(config):
        errors.append("receipt_status_surface_hash_mismatch")
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
        "status_used_as_action_basis",
        "dirty_tree_fixed",
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
    if metrics.get("source_slice_count") != len(SOURCE_SLICES):
        errors.append("metric_source_slice_count_mismatch")
    if metrics.get("source_input_count") != len(read_only_sources()):
        errors.append("metric_source_input_count_mismatch")
    if metrics.get("manual_negative_probes") != 12:
        errors.append("metric_manual_negative_probes_mismatch")
    if metrics.get("max_visible_stages") != 4:
        errors.append("metric_max_visible_stages_mismatch")

    if config.get("status_surface_hash") != expected_surface_hash(config):
        errors.append("status_surface_hash_mismatch")
    return sorted(set(errors))


def validate_prototype_receipt(receipt: Any, config: dict[str, Any] | None = None) -> list[str]:
    errors = []
    if not isinstance(receipt, dict):
        return ["prototype_receipt_not_object"]
    errors.extend(check_keys("prototype_receipt", receipt, RECEIPT_KEYS))
    errors.extend(scan_dangerous_values(receipt, "$.prototype_receipt"))
    expected_config = config or current_valid_config()
    expected_hash = expected_config.get("status_surface_hash") if expected_config else None
    expected_result = expected_config.get("surface_receipt", {}).get("surface_result") if expected_config else None
    if receipt.get("record_kind") != "sandbox_formal_vault_operator_status_surface_receipt":
        errors.append("prototype_receipt_record_kind_mismatch")
    if receipt.get("slice_id") != SLICE_ID:
        errors.append("prototype_receipt_slice_id_mismatch")
    if expected_result and receipt.get("surface_result") != expected_result:
        errors.append("prototype_receipt_surface_result_mismatch")
    if receipt.get("source_slice_count") != len(SOURCE_SLICES):
        errors.append("prototype_receipt_source_slice_count_mismatch")
    if receipt.get("source_input_count") != len(read_only_sources()):
        errors.append("prototype_receipt_source_input_count_mismatch")
    if receipt.get("badge_count") != len(expected_badges("chain_overview_surface")):
        errors.append("prototype_receipt_badge_count_mismatch")
    if receipt.get("stop_line_count") != len(expected_stop_lines()):
        errors.append("prototype_receipt_stop_line_count_mismatch")
    if expected_hash and receipt.get("status_surface_hash") != expected_hash:
        errors.append("prototype_receipt_status_surface_hash_mismatch")
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
        "status_used_as_action_basis",
        "dirty_tree_fixed",
    ]:
        if receipt.get(false_key) is not False:
            errors.append(f"prototype_receipt_flag_not_false:{false_key}")
    if not NON_CLAIMS.issubset(set(receipt.get("non_claims", []))):
        errors.append("prototype_receipt_non_claims_missing")
    return sorted(set(errors))


def inspect_prototype() -> dict[str, Any]:
    prototype_path = ROOT / "prototype" / "formal-vault-operator-status-surface"
    receipt_path = prototype_path / "Receipts" / "operator-status-surface-receipt.json"
    html_path = prototype_path / "operator-status-surface.html"
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
        issues.extend(validate_prototype_html_text("operator-status-surface.html", html))
        lower = html.lower()
        buttons = re.findall(r"<button[^>]*data-filter=\"([^\"]+)\"[^>]*>([^<]+)</button>", html)
        html_summary = {
            "sandbox_only": 'data-sandbox-only="true"' in html,
            "status_only": 'data-status-only="true"' in html,
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
            "button_texts": [button[1].strip() for button in buttons],
        }
    else:
        issues.append("missing_status_surface_html")
    return {"prototype_path": str(prototype_path), "issues": sorted(set(issues)), "receipt": receipt, "html": html_summary}


def validate_prototype_tamper(tamper: dict[str, Any]) -> list[str]:
    if tamper.get("kind") == "markdown_replace":
        return validate_prototype_markdown_text(tamper.get("file", "unknown.md"), tamper.get("content", ""))
    if tamper.get("kind") == "html_replace":
        return validate_prototype_html_text(tamper.get("file", "operator-status-surface.html"), tamper.get("content", ""))
    receipt_path = ROOT / "prototype" / "formal-vault-operator-status-surface" / "Receipts" / "operator-status-surface-receipt.json"
    if receipt_path.exists():
        base_receipt = read_json_path(receipt_path)
    else:
        config = current_valid_config()
        base_receipt = copy.deepcopy(config.get("surface_receipt", {})) if config else {}
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
    config["status_surface_hash"] = ""
    if isinstance(config.get("surface_receipt"), dict):
        config["surface_receipt"]["status_surface_hash"] = ""
    surface_hash = expected_surface_hash(config)
    config["status_surface_hash"] = surface_hash
    if isinstance(config.get("surface_receipt"), dict):
        config["surface_receipt"]["status_surface_hash"] = surface_hash
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

    add_probe("manual-operation-formal-vault-read", ["operations", "formal_vault_read"], True, ["operation_not_false:formal_vault_read"])
    add_probe("manual-control-mainline-ready", ["status_controls", "mainline_ready"], True, ["status_control_mismatch:mainline_ready"])
    add_probe("manual-chain-execution-permission", ["operator_chain", 1, "execution_permission_granted"], True, ["operator_chain_flag_not_false:p2_31_readiness_gate:execution_permission_granted", "operator_chain_mismatch"])
    add_probe("manual-badge-authority", ["status_badges", 0, "non_authority"], False, ["status_badge_authority_confusion:sandbox_product_grade", "status_badges_mismatch"])
    add_probe("manual-receipt-action-basis", ["surface_receipt", "status_used_as_action_basis"], True, ["receipt_flag_not_false:status_used_as_action_basis"])

    prototype_probes = [
        ("manual-prototype-execution-permission", {"kind": "markdown_replace", "file": "03 Stop Lines.md", "content": "execution permission: granted"}, ["prototype_text_dangerous:03 Stop Lines.md:execution_permission_marker"]),
        ("manual-prototype-formal-vault-approval", {"kind": "markdown_replace", "file": "02 Status Badges.md", "content": "formal vault approval: yes"}, ["prototype_text_dangerous:02 Status Badges.md:formal_vault_approval_marker"]),
        ("manual-prototype-action-basis", {"kind": "markdown_replace", "file": "01 Evidence Chain.md", "content": "action basis: yes"}, ["prototype_text_dangerous:01 Evidence Chain.md:action_basis_marker"]),
        ("manual-prototype-command", {"kind": "html_replace", "file": "operator-status-surface.html", "content": "<html><body>python tools/promote.py --sync</body></html>"}, ["prototype_text_dangerous:operator-status-surface.html:python_command"]),
        ("manual-prototype-start-execution", {"kind": "html_replace", "file": "operator-status-surface.html", "content": "<html><body><button>Start execution</button></body></html>"}, ["prototype_text_authority_confusion:operator-status-surface.html:start_execution"]),
        ("manual-prototype-actual-user-wording", {"kind": "markdown_replace", "file": "04 Reviewer Packet.md", "content": "actual user wording: approve now"}, ["prototype_text_dangerous:04 Reviewer Packet.md:actual_user_wording_marker"]),
        ("manual-prototype-receipt-permission", {"kind": "receipt_update", "updates": {"execution_permission_granted": True}}, ["prototype_receipt_flag_not_false:execution_permission_granted"]),
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
