from __future__ import annotations

import argparse
import hashlib
import html.parser
import importlib.util
import json
import re
import sys
from pathlib import Path


SLICE_ID = "2026-06-15-p2-28-formal-vault-execution-preflight-dry-run-sandbox"
SOURCE_SLICE_ID = "2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox"
PACKET_SLICE_ID = "2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox"

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
]

REQUIRED_BOUNDARY_PHRASES = [
    "sandbox only",
    "execution preflight dry-run only",
    "not actual approval",
    "approval not collected",
    "real user text not stored",
    "formal vault not accessed",
    "formal vault state not inspected",
    "execution not performed",
    "snapshot not taken",
    "hashes not collected from formal vault",
    "dry-run only",
    "not reviewed knowledge",
    "not evidence support",
    "not action basis",
    "does not approve",
    "does not execute",
    "no formal vault write",
    "no formal vault read",
    "no sync",
    "no commit",
    "no push",
    "no promotion",
    "requires separate user approval",
    "requires separate execution slice",
]

REQUIRED_CHECKS = {
    "source_product_passed",
    "intake_gate_hash_match",
    "packet_hash_match",
    "source_bundle_hash_match",
    "scope_hash_match",
    "target_scope_exact",
    "targets_relative_only",
    "no_extra_targets",
    "formal_vault_not_accessed",
    "formal_vault_state_not_inspected",
    "snapshot_plan_present_not_executed",
    "rollback_plan_present_not_executed",
    "hash_plan_present_not_executed",
    "no_sync_commit_push_promotion",
    "real_user_text_not_stored",
    "separate_execution_slice_required",
}

AUTHORITY_CONFUSING_PATTERNS = [
    "ready to write formal vault",
    "execution readiness approved",
    "formal vault approval granted",
    "action basis approved",
    "approval collected now",
    "actual approval collected",
    "reviewed truth",
    "merge approved",
    "sync approved",
    "promotion approved",
]


class PreflightHTMLParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.sandbox_only = False
        self.preflight_only = False
        self.dry_run_only = False
        self.no_approval = False
        self.no_real_user_text_storage = False
        self.no_formal_vault_access = False
        self.no_execution = False
        self.no_write = False
        self.no_sync = False
        self.no_authority = False
        self.roles: set[str] = set()
        self.cards: list[dict[str, str]] = []
        self.buttons: list[str] = []
        self.button_texts: list[str] = []
        self.inputs: list[dict[str, str]] = []
        self.anchors: list[dict[str, str]] = []
        self.forms = 0
        self.downloads = 0
        self.contenteditable = 0
        self._current_button: str | None = None
        self._in_script = False
        self.script_text = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k: v or "" for k, v in attrs}
        if tag == "html":
            self.sandbox_only = attr.get("data-sandbox-only") == "true"
            self.preflight_only = attr.get("data-execution-preflight-only") == "true"
            self.dry_run_only = attr.get("data-dry-run-only") == "true"
            self.no_approval = attr.get("data-no-approval") == "true"
            self.no_real_user_text_storage = attr.get("data-no-real-user-text-storage") == "true"
            self.no_formal_vault_access = attr.get("data-no-formal-vault-access") == "true"
            self.no_execution = attr.get("data-no-execution") == "true"
            self.no_write = attr.get("data-no-write") == "true"
            self.no_sync = attr.get("data-no-sync") == "true"
            self.no_authority = attr.get("data-no-authority") == "true"
        if "data-role" in attr:
            self.roles.add(attr["data-role"])
        if tag == "article" and "card" in attr.get("class", "").split():
            self.cards.append({"kind": attr.get("data-kind", ""), "search": attr.get("data-search", "")})
        if tag == "button":
            self.buttons.append(attr.get("data-filter", ""))
            self._current_button = ""
        if tag == "input":
            self.inputs.append({"id": attr.get("id", ""), "type": attr.get("type", ""), "name": attr.get("name", "")})
        if tag == "form":
            self.forms += 1
        if tag == "a":
            self.anchors.append({"href": attr.get("href", ""), "download": attr.get("download", "")})
            if "download" in attr:
                self.downloads += 1
        if attr.get("contenteditable", "").lower() == "true":
            self.contenteditable += 1
        if tag == "script" and attr.get("id") == "preflight-data":
            self._in_script = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self._in_script = False
        if tag == "button" and self._current_button is not None:
            self.button_texts.append(self._current_button.strip())
            self._current_button = None

    def handle_data(self, data: str) -> None:
        if self._in_script:
            self.script_text += data
        if self._current_button is not None:
            self._current_button += data


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def sandbox_root() -> Path:
    return root().parent


def workspace_root() -> Path:
    return sandbox_root().parents[2]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_json(data: object) -> str:
    raw = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_builder() -> object:
    path = root() / "artifact" / "execution_preflight_builder.py"
    spec = importlib.util.spec_from_file_location("execution_preflight_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load builder: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def frontmatter_status(text: str) -> str:
    if not text.startswith("---\n"):
        return "missing_frontmatter"
    end = text.find("\n---", 4)
    if end == -1:
        return "missing_frontmatter_end"
    for line in text[4:end].splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def source_intake_config() -> dict:
    return load_json(sandbox_root() / SOURCE_SLICE_ID / "fixtures" / "valid-user-decision-intake-gate-config.json")


def source_packet_config() -> dict:
    return load_json(sandbox_root() / PACKET_SLICE_ID / "fixtures" / "valid-approval-packet-config.json")


def is_bad_target(value: str) -> bool:
    normalized = value.replace("\\", "/")
    return (
        re.match(r"^[A-Za-z]:/", normalized) is not None
        or normalized.startswith("/")
        or ".." in normalized.split("/")
        or normalized.startswith("wiki/")
        or normalized.startswith("templates/")
        or normalized.startswith("tools/")
        or "Obsidian" in value
    )


def validate_source_path(source_path: str, fid: str, errors: list[str]) -> None:
    if not source_path:
        errors.append(f"source_input_path_missing:{fid}")
        return
    normalized = source_path.replace("\\", "/")
    allowed_prefixes = [
        f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/",
        f"outputs/review/vaks-implementation-sandbox/{PACKET_SLICE_ID}/",
    ]
    if is_bad_target(normalized) or not any(normalized.startswith(prefix) for prefix in allowed_prefixes):
        errors.append(f"source_input_path_invalid:{fid}")
        return
    source_abs = (workspace_root() / normalized).resolve()
    try:
        source_abs.relative_to(workspace_root())
    except ValueError:
        errors.append(f"source_input_path_invalid:{fid}")
        return
    if not source_abs.exists():
        errors.append(f"source_input_missing:{fid}")


def material(cfg: dict) -> dict:
    contract = dict(cfg.get("preflight_contract", {}))
    contract.pop("required_preflight_hash", None)
    samples = []
    for sample in cfg.get("preflight_samples", []):
        item = dict(sample)
        item.pop("required_preflight_hash", None)
        hashes = dict(item.get("hash_claims", {}))
        hashes.pop("preflight_hash", None)
        item["hash_claims"] = hashes
        samples.append(item)
    receipt = dict(cfg.get("non_execution_receipt", {}))
    receipt.pop("preflight_hash", None)
    return {
        "preflight_version": cfg.get("preflight_version"),
        "source_slice": cfg.get("source_slice"),
        "source_input_bundle_hash": cfg.get("source_input_bundle_hash"),
        "source_intake_gate_hash": cfg.get("source_intake_gate_hash"),
        "source_packet_hash": cfg.get("source_packet_hash"),
        "source_packet_source_bundle_hash": cfg.get("source_packet_source_bundle_hash"),
        "source_packet_scope_hash": cfg.get("source_packet_scope_hash"),
        "target_manifest_hash": cfg.get("target_manifest_hash"),
        "preflight_contract": contract,
        "preflight_samples": samples,
        "non_execution_receipt": receipt,
        "stop_conditions": cfg.get("stop_conditions", []),
    }


def required_sample_ids(cfg: dict) -> set[str]:
    focus = cfg.get("fixture_focus")
    if focus == "deny":
        return {"synthetic_denied_reference_preflight"}
    if focus == "revise":
        return {"synthetic_revision_reference_preflight"}
    return {
        "synthetic_approved_reference_preflight",
        "synthetic_denied_reference_preflight",
        "synthetic_revision_reference_preflight",
        "synthetic_dirty_state_preflight_block",
    }


def validate_config(cfg: dict) -> list[str]:
    errors: list[str] = []
    intake = source_intake_config()
    packet = source_packet_config()
    if cfg.get("slice_id") != SLICE_ID:
        errors.append("wrong_slice_id")
    if cfg.get("source_slice") != SOURCE_SLICE_ID:
        errors.append("wrong_source_slice")
    if cfg.get("packet_slice") != PACKET_SLICE_ID:
        errors.append("wrong_packet_slice")

    expected_scope = f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"
    if cfg.get("write_scope") != [expected_scope]:
        errors.append("invalid_write_scope")
    for scope in cfg.get("write_scope", []):
        normalized = scope.replace("\\", "/")
        if not normalized.startswith(expected_scope):
            errors.append("invalid_write_scope")
        if any(bad in normalized for bad in ["wiki/claims", "wiki/patterns", "wiki/decisions", "templates/", "tools/", "H:/Obsidian"]):
            errors.append("invalid_write_scope")

    ops = cfg.get("operations", {})
    if ops.get("default_read_only") is not True:
        errors.append("default_not_read_only")
    if ops.get("rebuild_requires_explicit_flag") is not True:
        errors.append("rebuild_not_explicit")
    for op in FORBIDDEN_OPERATIONS:
        if ops.get(op) is not False:
            errors.append(f"forbidden_operation:{op}")

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        if phrase not in cfg.get("boundary_phrases", []):
            errors.append(f"missing_boundary_phrase:{phrase}")

    for item in cfg.get("source_inputs", []):
        fid = item.get("id", "unknown")
        source_path = item.get("source_path", "")
        validate_source_path(source_path, fid, errors)
        if source_path and f"source_input_path_invalid:{fid}" not in errors and f"source_input_missing:{fid}" not in errors:
            actual = sha256(workspace_root() / source_path.replace("\\", "/"))
            if item.get("source_sha256") != actual:
                errors.append(f"source_input_hash_mismatch:{fid}")
        if item.get("content_binding") != "exact_source_sha256":
            errors.append(f"source_input_content_binding_missing:{fid}")
    if cfg.get("source_input_bundle_hash") != sha256_json(cfg.get("source_inputs", [])):
        errors.append("source_input_bundle_hash_mismatch")
    if cfg.get("source_intake_gate_hash") != intake.get("intake_gate_hash"):
        errors.append("source_intake_gate_hash_mismatch")
    if cfg.get("source_packet_hash") != packet.get("packet_hash"):
        errors.append("source_packet_hash_mismatch")
    if cfg.get("source_packet_source_bundle_hash") != packet.get("source_bundle_hash"):
        errors.append("source_packet_source_bundle_hash_mismatch")
    if cfg.get("source_packet_scope_hash") != packet.get("approval_scope", {}).get("scope_hash"):
        errors.append("source_packet_scope_hash_mismatch")

    targets = cfg.get("target_manifest", [])
    if cfg.get("target_manifest_hash") != sha256_json(targets):
        errors.append("target_manifest_hash_mismatch")
    packet_items = {item["id"]: item for item in packet.get("approval_scope", {}).get("items", [])}
    packet_scope_ids = set(packet_items)
    target_ids = {item.get("id") for item in targets}
    if target_ids != packet_scope_ids:
        errors.append("target_manifest_scope_mismatch")
    if len(targets) > len(packet_scope_ids):
        errors.append("too_many_targets")
    for item in targets:
        tid = item.get("id", "unknown")
        expected_target = packet_items.get(tid)
        if is_bad_target(item.get("relative_target", "")) or item.get("target_path_relative_only") is not True:
            errors.append(f"target_path_not_relative:{tid}")
        if expected_target is None:
            errors.append(f"target_not_in_packet_scope:{tid}")
        else:
            if item.get("relative_target") != expected_target.get("relative_target"):
                errors.append(f"target_relative_target_mismatch:{tid}")
            if item.get("source_path") != expected_target.get("p2_24_source_path"):
                errors.append(f"target_source_path_mismatch:{tid}")
            if item.get("source_sha256") != expected_target.get("p2_24_source_sha256"):
                errors.append(f"target_source_hash_mismatch:{tid}")
        if not item.get("source_sha256"):
            errors.append(f"target_source_hash_missing:{tid}")
        if item.get("content_binding") != "exact_source_sha256":
            errors.append(f"target_content_binding_missing:{tid}")
        if item.get("formal_vault_target_resolved") is not False:
            errors.append(f"target_formal_vault_resolved:{tid}")
        if item.get("formal_vault_target_exists_checked") is not False:
            errors.append(f"target_formal_vault_state_checked:{tid}")
        if item.get("snapshot_taken") is not False:
            errors.append(f"target_snapshot_taken:{tid}")
        if item.get("hash_before_collected") is not False:
            errors.append(f"target_hash_before_collected:{tid}")
        if item.get("hash_after_collected") is not False:
            errors.append(f"target_hash_after_collected:{tid}")
        if item.get("write_enabled_now") is not False:
            errors.append(f"target_write_enabled_now:{tid}")
        if item.get("dry_run_only") is not True:
            errors.append(f"target_not_dry_run:{tid}")

    if cfg.get("preflight_hash_material") != material(cfg):
        errors.append("preflight_hash_material_mismatch")
    expected_preflight_hash = sha256_json(material(cfg))
    if not cfg.get("preflight_hash"):
        errors.append("preflight_hash_missing")
    elif cfg.get("preflight_hash") != expected_preflight_hash:
        errors.append("preflight_hash_mismatch")

    contract = cfg.get("preflight_contract", {})
    if contract.get("current_slice_executes") is not False:
        errors.append("contract_allows_execution")
    if contract.get("current_slice_collects_approval") is not False:
        errors.append("contract_allows_approval_collection")
    if contract.get("formal_vault_access_disallowed") is not True:
        errors.append("contract_allows_formal_vault_access")
    if contract.get("formal_vault_state_inspection_disallowed") is not True:
        errors.append("contract_allows_formal_vault_state_inspection")
    if contract.get("separate_future_execution_slice_required") is not True:
        errors.append("contract_missing_separate_execution_slice")
    if contract.get("separate_final_user_confirmation_required") is not True:
        errors.append("contract_missing_final_user_confirmation")
    if contract.get("approved_reference_not_executable_here") is not True:
        errors.append("contract_allows_approved_reference_execution")
    if contract.get("deny_blocks_execution") is not True:
        errors.append("contract_deny_does_not_block")
    if contract.get("revise_blocks_execution") is not True:
        errors.append("contract_revise_does_not_block")
    if contract.get("dirty_state_blocks_execution") is not True:
        errors.append("contract_dirty_state_does_not_block")
    if contract.get("required_source_intake_gate_hash") != cfg.get("source_intake_gate_hash"):
        errors.append("contract_intake_gate_hash_mismatch")
    if contract.get("required_packet_hash") != cfg.get("source_packet_hash"):
        errors.append("contract_packet_hash_mismatch")
    if contract.get("required_source_bundle_hash") != cfg.get("source_packet_source_bundle_hash"):
        errors.append("contract_source_bundle_hash_mismatch")
    if contract.get("required_scope_hash") != cfg.get("source_packet_scope_hash"):
        errors.append("contract_scope_hash_mismatch")
    if contract.get("required_preflight_hash") != cfg.get("preflight_hash"):
        errors.append("contract_preflight_hash_mismatch")
    missing_checks = REQUIRED_CHECKS - set(contract.get("required_preflight_checks", []))
    for check in sorted(missing_checks):
        errors.append(f"contract_missing_required_preflight_check:{check}")

    samples = cfg.get("preflight_samples", [])
    ids = {item.get("id") for item in samples}
    for required in required_sample_ids(cfg):
        if required not in ids:
            errors.append(f"missing_preflight_sample:{required}")
    if len(samples) < cfg.get("product_metrics", {}).get("required_preflight_samples", 1):
        errors.append("too_few_preflight_samples")
    required_exclusions = set(contract.get("required_exclusions", []))
    required_scope_ids = set(contract.get("required_scope_ids", []))
    for sample in samples:
        sid = sample.get("id", "unknown")
        verdict = sample.get("decision_verdict")
        if sample.get("synthetic_only") is not True:
            errors.append(f"sample_not_synthetic:{sid}")
        if sample.get("actual_user_input") is not False:
            errors.append(f"sample_uses_actual_user_input:{sid}")
        if sample.get("approval_collected_now") is not False:
            errors.append(f"sample_collects_approval_now:{sid}")
        if sample.get("real_user_text_stored") is not False:
            errors.append(f"sample_stores_real_user_text:{sid}")
        if sample.get("captured_user_text"):
            errors.append(f"sample_captures_user_text:{sid}")
        if sample.get("decision_reference_present") is not True:
            errors.append(f"sample_missing_decision_reference:{sid}")
        if sample.get("formal_vault_accessed") is not False:
            errors.append(f"sample_accesses_formal_vault:{sid}")
        if sample.get("formal_vault_state_inspected") is not False:
            errors.append(f"sample_inspects_formal_vault_state:{sid}")
        if sample.get("snapshot_taken") is not False:
            errors.append(f"sample_snapshot_taken:{sid}")
        if sample.get("rollback_executed") is not False:
            errors.append(f"sample_rollback_executed:{sid}")
        if sample.get("hash_before_collected") is not False:
            errors.append(f"sample_hash_before_collected:{sid}")
        if sample.get("hash_after_collected") is not False:
            errors.append(f"sample_hash_after_collected:{sid}")
        if sample.get("execution_performed") is not False:
            if verdict == "DENIED_BY_USER":
                errors.append(f"denied_sample_executes:{sid}")
            elif verdict == "NEEDS_REVISION":
                errors.append(f"revise_sample_executes:{sid}")
            else:
                errors.append(f"sample_execution_performed:{sid}")
        if sample.get("formal_vault_write_allowed_now") is not False:
            errors.append(f"sample_allows_formal_vault_write_now:{sid}")
        if sample.get("action_basis_created") is not False:
            errors.append(f"sample_creates_action_basis:{sid}")
        if sample.get("reviewed_knowledge_created") is not False:
            errors.append(f"sample_creates_reviewed_knowledge:{sid}")
        for field, code in [
            ("sync_allowed", "sample_allows_sync"),
            ("commit_allowed", "sample_allows_commit"),
            ("push_allowed", "sample_allows_push"),
            ("promotion_allowed", "sample_allows_promotion"),
        ]:
            if sample.get(field) is not False:
                errors.append(f"{code}:{sid}")
        if sample.get("extra_targets_requested") is not False:
            errors.append(f"sample_extra_targets_requested:{sid}")
        if set(sample.get("scope_ids", [])) != required_scope_ids:
            errors.append(f"sample_scope_ids_mismatch:{sid}")
        hashes = sample.get("hash_claims", {})
        if hashes.get("intake_gate_hash") != cfg.get("source_intake_gate_hash"):
            errors.append(f"sample_intake_gate_hash_mismatch:{sid}")
        if hashes.get("packet_hash") != cfg.get("source_packet_hash"):
            errors.append(f"sample_packet_hash_mismatch:{sid}")
        if hashes.get("source_bundle_hash") != cfg.get("source_packet_source_bundle_hash"):
            errors.append(f"sample_source_bundle_hash_mismatch:{sid}")
        if hashes.get("scope_hash") != cfg.get("source_packet_scope_hash"):
            errors.append(f"sample_scope_hash_mismatch:{sid}")
        if hashes.get("preflight_hash") != cfg.get("preflight_hash"):
            errors.append(f"sample_preflight_hash_mismatch:{sid}")
        if sample.get("required_preflight_hash") != cfg.get("preflight_hash"):
            errors.append(f"sample_required_preflight_hash_mismatch:{sid}")
        for check in contract.get("required_preflight_checks", []):
            if sample.get("preflight_checks", {}).get(check) is not True:
                errors.append(f"sample_preflight_check_failed:{sid}:{check}")
        if verdict == "APPROVED_BY_USER":
            if sample.get("dirty_state_ack") is not True and "dirty_state" not in sid:
                errors.append(f"approved_missing_dirty_state_ack:{sid}")
            if sample.get("expected_preflight_result") == "READY_TO_WRITE":
                errors.append(f"approved_sample_result_actionable:{sid}")
            allowed_results = {
                "PREFLIGHT_DRY_RUN_COMPLETE_NOT_EXECUTABLE",
                "BLOCKED_BY_DIRTY_STATE_ACK_MISSING_NOT_EXECUTED",
            }
            if sample.get("expected_preflight_result") not in allowed_results:
                errors.append(f"approved_sample_result_bad:{sid}")
            if "dirty_state" in sid and sample.get("expected_preflight_result") != "BLOCKED_BY_DIRTY_STATE_ACK_MISSING_NOT_EXECUTED":
                errors.append(f"dirty_sample_result_bad:{sid}")
        if verdict == "DENIED_BY_USER" and sample.get("expected_preflight_result") != "BLOCKED_BY_DENIAL_NOT_EXECUTED":
            errors.append(f"denied_sample_result_bad:{sid}")
        if verdict == "NEEDS_REVISION" and sample.get("expected_preflight_result") != "BLOCKED_PENDING_PACKET_REVISION_NOT_EXECUTED":
            errors.append(f"revise_sample_result_bad:{sid}")

    receipt = cfg.get("non_execution_receipt", {})
    if receipt.get("approval_collected_now") is not False:
        errors.append("non_execution_receipt_claims_approval")
    if receipt.get("actual_user_input_used") is not False:
        errors.append("non_execution_receipt_uses_actual_user_input")
    if receipt.get("real_user_text_stored") is not False:
        errors.append("non_execution_receipt_real_user_text_stored")
    if receipt.get("formal_vault_accessed") is not False:
        errors.append("non_execution_receipt_formal_vault_accessed")
    if receipt.get("formal_vault_state_inspected") is not False:
        errors.append("non_execution_receipt_formal_vault_state_inspected")
    if receipt.get("execution_performed") is not False:
        errors.append("non_execution_receipt_claims_execution")
    if receipt.get("snapshot_taken") is not False:
        errors.append("non_execution_receipt_snapshot_taken")
    if receipt.get("hash_before_collected") is not False:
        errors.append("non_execution_receipt_hash_before_collected")
    if receipt.get("hash_after_collected") is not False:
        errors.append("non_execution_receipt_hash_after_collected")
    if receipt.get("preflight_hash") and cfg.get("preflight_hash") and receipt.get("preflight_hash") != cfg.get("preflight_hash"):
        errors.append("non_execution_receipt_preflight_hash_mismatch")

    stop_text = "\n".join(cfg.get("stop_conditions", [])).lower()
    for required in [
        "actual user approval",
        "actual user decision",
        "real user text storage",
        "formal vault read",
        "formal vault write",
        "formal vault state inspection",
        "formal vault hash",
        "obsidian sync",
        "commit",
        "push",
        "promotion",
        "execution requested",
        "decision inferred",
        "intake gate hash mismatch",
        "packet hash mismatch",
        "source bundle hash mismatch",
        "scope hash mismatch",
        "preflight hash mismatch",
        "target manifest mismatch",
        "extra targets",
        "dirty-state",
    ]:
        if required not in stop_text:
            errors.append(f"missing_stop_condition:{required}")
    authority_text = json.dumps(
        {
            "purpose": cfg.get("purpose", ""),
            "stop_conditions": cfg.get("stop_conditions", []),
            "non_claims": receipt.get("non_claims", []),
            "sample_results": [s.get("expected_preflight_result", "") for s in samples],
        },
        ensure_ascii=False,
    ).lower()
    if any(pattern in authority_text for pattern in AUTHORITY_CONFUSING_PATTERNS):
        errors.append("authority_confusing_text")

    controls = cfg.get("inspector_controls", {})
    actual_inputs = {(item.get("id", ""), item.get("type", "")) for item in controls.get("inputs", [])}
    if actual_inputs != {("q", "search")}:
        errors.append("inspector_inputs_not_allowlisted")
    actual_buttons = {item.get("filter", "") for item in controls.get("buttons", [])}
    if actual_buttons != {"all", "checklist", "targets", "blocks", "receipt", "stops"}:
        errors.append("inspector_buttons_not_allowlisted")
    for button in controls.get("buttons", []):
        label = button.get("label", "").strip().lower()
        if label in {"approve", "save", "sync", "commit", "push", "write", "promote", "execute", "submit", "run"}:
            errors.append(f"inspector_control_not_allowed:button:{label}")
    if cfg.get("product_metrics", {}).get("minimum_failure_cases", 0) < 75:
        errors.append("minimum_failure_cases_too_low")
    return sorted(set(errors))


def check_failure_cases() -> dict:
    oracle = load_json(root() / "artifact" / "failure-case-oracle.json")
    mismatches = []
    expected_files = {entry["file"] for entry in oracle}
    actual_files = {path.name for path in (root() / "failure-cases").glob("*.json")}
    for name in sorted(expected_files - actual_files):
        mismatches.append({"file": name, "missing": True})
    for name in sorted(actual_files - expected_files):
        mismatches.append({"file": name, "extra": True})
    for entry in oracle:
        path = root() / "failure-cases" / entry["file"]
        if not path.exists():
            continue
        errors = validate_config(load_json(path))
        missing = [code for code in entry["expected_failures"] if code not in errors]
        extra = [code for code in errors if code not in entry["expected_failures"]]
        if missing or extra:
            mismatches.append({"file": entry["file"], "missing_expected": missing, "extra": extra, "actual": errors})
    return {"count": len(oracle), "mismatches": mismatches}


def resolve_markdown_link(page: Path, target: str) -> Path | None:
    if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
        return None
    clean = target.split("#", 1)[0].replace("%20", " ")
    if not clean:
        return None
    return (page.parent / clean).resolve()


def page_links(page: Path) -> set[str]:
    text = page.read_text(encoding="utf-8")
    links = set(re.findall(r"\[\[([^\]]+)\]\]", text))
    links.update(match.group(1) for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text))
    if "execution-preflight-inspector.html" in text:
        links.add("execution-preflight-inspector.html")
    return links


def check_wikilinks(proto: Path) -> list[str]:
    issues = []
    pages = {path.stem for path in proto.glob("*.md")}
    for page in proto.glob("*.md"):
        for link in re.findall(r"\[\[([^\]]+)\]\]", page.read_text(encoding="utf-8")):
            target = link.split("|", 1)[0].split("#", 1)[0]
            if target not in pages:
                issues.append(f"broken_wikilink:{page.name}:{target}")
    return issues


def check_markdown_links(proto: Path) -> list[str]:
    issues = []
    for page in proto.rglob("*.md"):
        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", page.read_text(encoding="utf-8")):
            target = match.group(1)
            resolved = resolve_markdown_link(page, target)
            if resolved is None:
                continue
            if not resolved.exists():
                issues.append(f"broken_markdown_link:{page.name}:{target}")
    return issues


def check_html(path: Path) -> dict:
    issues = []
    if not path.exists():
        return {"issues": ["html_missing"], "summary": {}}
    text = path.read_text(encoding="utf-8")
    parser = PreflightHTMLParser()
    parser.feed(text)
    summary = {
        "sandbox_only": parser.sandbox_only,
        "preflight_only": parser.preflight_only,
        "dry_run_only": parser.dry_run_only,
        "no_approval": parser.no_approval,
        "no_real_user_text_storage": parser.no_real_user_text_storage,
        "no_formal_vault_access": parser.no_formal_vault_access,
        "no_execution": parser.no_execution,
        "no_write": parser.no_write,
        "no_sync": parser.no_sync,
        "no_authority": parser.no_authority,
        "cards": len(parser.cards),
        "roles": sorted(parser.roles),
        "forms": parser.forms,
        "buttons": parser.buttons,
        "button_texts": parser.button_texts,
        "inputs": parser.inputs,
        "anchors": len(parser.anchors),
        "downloads": parser.downloads,
        "contenteditable": parser.contenteditable,
    }
    if not parser.sandbox_only:
        issues.append("html_missing_sandbox_marker")
    if not parser.preflight_only:
        issues.append("html_missing_preflight_marker")
    if not parser.dry_run_only:
        issues.append("html_missing_dry_run_marker")
    if not parser.no_approval:
        issues.append("html_missing_no_approval_marker")
    if not parser.no_real_user_text_storage:
        issues.append("html_missing_no_real_user_text_storage_marker")
    if not parser.no_formal_vault_access:
        issues.append("html_missing_no_formal_vault_access_marker")
    if not parser.no_execution:
        issues.append("html_missing_no_execution_marker")
    if not parser.no_write:
        issues.append("html_missing_no_write_marker")
    if not parser.no_sync:
        issues.append("html_missing_no_sync_marker")
    if not parser.no_authority:
        issues.append("html_missing_no_authority_marker")
    for role in ["preflight-filter", "preflight-cards", "boundary-rail"]:
        if role not in parser.roles:
            issues.append(f"html_missing_role:{role}")
    if parser.forms:
        issues.append("html_form_present")
    if parser.downloads:
        issues.append("html_download_link_present")
    if parser.contenteditable:
        issues.append("html_contenteditable_present")
    if parser.inputs != [{"id": "q", "type": "search", "name": ""}]:
        issues.append("html_inputs_not_allowlisted")
    if parser.buttons != ["all", "checklist", "targets", "blocks", "receipt", "stops"]:
        issues.append("html_buttons_not_allowlisted")
    for text_value in parser.button_texts:
        if text_value.strip().lower() in {"approve", "save", "sync", "commit", "push", "write", "promote", "execute", "submit", "run"}:
            issues.append(f"html_write_or_execute_button_present:{text_value.strip().lower()}")
    if re.search(r"\b(fetch|XMLHttpRequest|sendBeacon|localStorage|sessionStorage)\b", text):
        issues.append("html_network_or_storage_api_present")
    if re.search(r"\b(approve|save|sync|write|commit|push|promote|execute|submit|run)\s*\(", text, flags=re.IGNORECASE):
        issues.append("html_write_or_execute_function_present")
    for anchor in parser.anchors:
        href = anchor.get("href", "").lower()
        if href.startswith(("http://", "https://", "mailto:", "javascript:")) or anchor.get("download"):
            issues.append("html_forbidden_anchor")
    try:
        data = json.loads(parser.script_text)
        if len(data.get("preflight_samples", [])) < 4:
            issues.append("html_embedded_samples_missing")
        if data.get("non_execution_receipt", {}).get("execution_performed") is not False:
            issues.append("html_embedded_receipt_claims_execution")
    except Exception as exc:
        issues.append(f"html_embedded_data_invalid:{exc}")
    lower = text.lower()
    for phrase in [
        "execution preflight dry-run only",
        "formal vault not accessed",
        "formal vault state not inspected",
        "execution not performed",
        "hashes not collected from formal vault",
        "does not execute",
        "no formal vault write",
        "not action basis",
    ]:
        if phrase not in lower:
            issues.append(f"html_missing_boundary_phrase:{phrase}")
    return {"issues": sorted(set(issues)), "summary": summary}


def check_actual_journeys(proto: Path, html_ok: bool) -> dict:
    issues = []
    results = {}
    pages = {
        "home": proto / "00 Execution Preflight Home.md",
        "checklist": proto / "01 Preflight Checklist.md",
        "targets": proto / "02 Dry Run Target Manifest.md",
        "approved": proto / "03 Approved Reference Dry Run.md",
        "receipt": proto / "05 Non Execution Receipt.md",
        "stops": proto / "06 Stop Conditions.md",
    }
    for key, path in pages.items():
        if not path.exists():
            issues.append(f"journey_missing_page:{key}")
    if issues:
        return {"results": results, "issues": issues}
    home_links = page_links(pages["home"])
    checklist_text = " ".join(pages["checklist"].read_text(encoding="utf-8").lower().split())
    target_text = " ".join(pages["targets"].read_text(encoding="utf-8").lower().split())
    approved_text = " ".join(pages["approved"].read_text(encoding="utf-8").lower().split())
    receipt_links = page_links(pages["receipt"])
    if "01 Preflight Checklist" not in home_links or "not execution readiness" not in checklist_text:
        issues.append("journey_path_missing:checklist_review")
    else:
        results["checklist_review"] = {"links_verified": True, "max_links": 2}
    if "02 Dry Run Target Manifest" not in home_links or "formal vault target state is not inspected" not in target_text:
        issues.append("journey_path_missing:target_review")
    else:
        results["target_review"] = {"links_verified": True, "max_links": 2}
    if "03 Approved Reference Dry Run" not in home_links or "not executable in this slice" not in approved_text:
        issues.append("journey_path_missing:approved_non_executable_review")
    else:
        results["approved_non_executable_review"] = {"links_verified": True, "max_links": 2}
    if "06 Stop Conditions" not in receipt_links:
        issues.append("journey_path_missing:receipt_to_stops")
    else:
        results["receipt_to_stops"] = {"links_verified": True, "max_links": 2}
    if "execution-preflight-inspector.html" not in home_links or not html_ok:
        issues.append("journey_path_missing:inspector_review")
    else:
        results["inspector_review"] = {"links_verified": True, "max_links": 2, "html_allowlist_ok": html_ok}
    return {"results": results, "issues": issues}


def check_prototype(cfg: dict) -> dict:
    proto = root() / "prototype" / "formal-vault-execution-preflight-dry-run"
    issues = []
    required = [
        "00 Execution Preflight Home.md",
        "01 Preflight Checklist.md",
        "02 Dry Run Target Manifest.md",
        "03 Approved Reference Dry Run.md",
        "04 Deny Or Revise Blocks.md",
        "05 Non Execution Receipt.md",
        "06 Stop Conditions.md",
        "07 Reviewer Packet.md",
        "execution-preflight-inspector.html",
        "Receipts/formal-vault-execution-preflight-receipt.json",
    ]
    for file in required:
        if not (proto / file).exists():
            issues.append(f"missing_prototype_file:{file}")
    for path in proto.rglob("*"):
        rel = path.relative_to(proto).as_posix()
        if path.suffix == ".base":
            issues.append(f"real_base_file_present:{rel}")
        if path.name == ".obsidian":
            issues.append("obsidian_config_present")
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            issues.append(f"python_cache_present:{rel}")
    if proto.exists():
        issues.extend(check_wikilinks(proto))
        issues.extend(check_markdown_links(proto))
    text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in proto.rglob("*")
        if path.is_file() and path.suffix in {".md", ".html", ".json"}
    )
    lower = text.lower()
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        if phrase.lower() not in lower:
            issues.append(f"prototype_missing_boundary_phrase:{phrase}")
    for pattern in AUTHORITY_CONFUSING_PATTERNS:
        if pattern in lower:
            issues.append(f"prototype_authority_confusing_text:{pattern}")

    receipt_summary = {}
    receipt_path = proto / "Receipts" / "formal-vault-execution-preflight-receipt.json"
    if receipt_path.exists():
        receipt = load_json(receipt_path)
        receipt_summary = {
            "slice_id": receipt.get("slice_id"),
            "source_slice": receipt.get("source_slice"),
            "formal_vault_accessed": receipt.get("formal_vault_accessed"),
            "formal_vault_state_inspected": receipt.get("formal_vault_state_inspected"),
            "execution_performed": receipt.get("execution_performed"),
            "hash_before_collected": receipt.get("hash_before_collected"),
            "target_count": receipt.get("target_count"),
            "sample_count": receipt.get("sample_count"),
        }
        if receipt.get("slice_id") != SLICE_ID:
            issues.append("receipt_wrong_slice_id")
        if receipt.get("source_slice") != SOURCE_SLICE_ID:
            issues.append("receipt_wrong_source_slice")
        for field, code in [
            ("formal_vault_accessed", "receipt_formal_vault_accessed"),
            ("formal_vault_state_inspected", "receipt_formal_vault_state_inspected"),
            ("approval_collected_now", "receipt_approval_collected_now"),
            ("actual_user_input_used", "receipt_actual_user_input_used"),
            ("real_user_text_stored", "receipt_real_user_text_stored"),
            ("execution_performed", "receipt_execution_performed"),
            ("snapshot_taken", "receipt_snapshot_taken"),
            ("hash_before_collected", "receipt_hash_before_collected"),
            ("hash_after_collected", "receipt_hash_after_collected"),
        ]:
            if receipt.get(field) is not False:
                issues.append(code)
        if receipt.get("target_count") != len(cfg.get("target_manifest", [])):
            issues.append("receipt_target_count_mismatch")
        if receipt.get("sample_count") != len(cfg.get("preflight_samples", [])):
            issues.append("receipt_sample_count_mismatch")
        if receipt.get("preflight_hash") != cfg.get("preflight_hash"):
            issues.append("receipt_preflight_hash_mismatch")
        forbidden = receipt.get("forbidden_operations", {})
        for op in FORBIDDEN_OPERATIONS:
            if op not in forbidden:
                issues.append(f"receipt_missing_forbidden_operation:{op}")
            elif forbidden.get(op) is not False:
                issues.append(f"receipt_forbidden_operation_true:{op}")
        for key, value in receipt.get("source_hashes", {}).items():
            if value == "missing":
                issues.append(f"receipt_missing_source_hash:{key}")

    html = check_html(proto / "execution-preflight-inspector.html")
    issues.extend(html["issues"])
    journeys = check_actual_journeys(proto, html_ok=not html["issues"])
    issues.extend(journeys["issues"])
    return {
        "prototype_path": str(proto),
        "issues": sorted(set(issues)),
        "receipt": receipt_summary,
        "html": html["summary"],
        "actual_journeys": journeys["results"],
    }


def check_source_status() -> dict:
    src = sandbox_root() / SOURCE_SLICE_ID
    product = src / "product-acceptance-report.md"
    next_step = src / "next-step.md"
    verification = src / "verification.md"
    issues = []
    product_status = frontmatter_status(product.read_text(encoding="utf-8")) if product.exists() else "missing"
    next_status = frontmatter_status(next_step.read_text(encoding="utf-8")) if next_step.exists() else "missing"
    verification_text = verification.read_text(encoding="utf-8") if verification.exists() else ""
    if product_status != "pass_product_grade":
        issues.append(f"source_product_not_pass:{product_status}")
    if next_status != "pass_product_grade_pending_user_next_slice_decision":
        issues.append(f"source_next_step_unexpected:{next_status}")
    if "passed: true" not in verification_text or "failure_cases: 70" not in verification_text:
        issues.append("source_final_gate_evidence_missing")
    return {"product_status": product_status, "next_status": next_status, "issues": issues}


def check_required_reports(final_gate: bool = False) -> dict:
    statuses = {}
    issues = []
    for name in [
        "slice-plan.md",
        "source-map.md",
        "verification.md",
        "reviewer-report.md",
        "boundary-audit.md",
        "product-acceptance-report.md",
        "next-step.md",
    ]:
        path = root() / name
        if not path.exists():
            issues.append(f"missing_required_report:{name}")
            continue
        statuses[name] = frontmatter_status(path.read_text(encoding="utf-8"))
    if final_gate:
        required = {
            "reviewer-report.md": "reviewer_pass",
            "boundary-audit.md": "boundary_pass",
            "product-acceptance-report.md": "pass_product_grade",
        }
        for name, expected in required.items():
            actual = statuses.get(name, "missing_status").lower()
            if actual != expected:
                issues.append(f"final_gate_bad_status:{name}:{actual}:expected:{expected}")
        actual_next = statuses.get("next-step.md", "missing_status").lower()
        if actual_next != "pass_product_grade_pending_user_next_slice_decision":
            issues.append(f"final_gate_bad_status:next-step.md:{actual_next}:expected:pass_product_grade_pending_user_next_slice_decision")
    return {"statuses": statuses, "issues": issues}


def run(rebuild: bool = False, final_gate: bool = False) -> dict:
    if rebuild:
        builder = load_builder()
        builder.build()
    fixtures = [
        root() / "fixtures" / "valid-execution-preflight-config.json",
        root() / "fixtures" / "valid-deny-execution-preflight-config.json",
        root() / "fixtures" / "valid-revise-execution-preflight-config.json",
    ]
    fixture_results = []
    for fixture in fixtures:
        fixture_results.append({"file": fixture.name, "errors": validate_config(load_json(fixture))})
    main_cfg = load_json(fixtures[0])
    failure_results = check_failure_cases()
    prototype_results = check_prototype(main_cfg)
    source_results = check_source_status()
    report_results = check_required_reports(final_gate=final_gate)
    failures = []
    if any(result["errors"] for result in fixture_results):
        failures.append("positive_fixture_errors")
    if failure_results["mismatches"]:
        failures.append("failure_case_mismatches")
    if failure_results["count"] < main_cfg.get("product_metrics", {}).get("minimum_failure_cases", 75):
        failures.append("too_few_failure_cases")
    if prototype_results["issues"]:
        failures.append("prototype_issues")
    if source_results["issues"]:
        failures.append("source_status_issues")
    if report_results["issues"]:
        failures.append("required_report_issues")
    return {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE_ID,
        "rebuild": rebuild,
        "final_gate": final_gate,
        "passed": not failures,
        "failures": failures,
        "positive_fixtures": fixture_results,
        "failure_cases": failure_results,
        "prototype": prototype_results,
        "source_status": source_results,
        "required_reports": report_results,
        "non_claims": [
            "sandbox verification only",
            "not actual approval",
            "not execution readiness",
            "not reviewed knowledge",
            "not evidence support",
            "not action basis",
            "not mainline approval",
            "not formal vault approval",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--final-gate", action="store_true")
    args = parser.parse_args()
    result = run(rebuild=args.rebuild, final_gate=args.final_gate)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
