#!/usr/bin/env python3
"""
Sandbox-only P1.5-16 MISA runtime memory / VAKS bridge validator.

This prototype validates synthetic bridge manifests with real copied fixtures.
It proves a narrow contract: runtime memory may remember process context, a
MISA-side adapter may read VAKS context-pack fixtures, and writeback may create
feedback/candidate/review_due signals through receipts. It must not write
reviewed VAKS knowledge, create support, create action basis, install runtime
dependencies, start hooks/services, or expose MCP write tools.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

SANDBOX_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = SANDBOX_ROOT.parents[3]

RECORD_KIND = "misa_runtime_memory_vaks_bridge_manifest"

ALLOWED_MEMORY_TYPES = {"session_observation", "preference_slot", "pending_work", "tool_result"}
ALLOWED_WRITEBACK_TYPES = {"feedback_event", "candidate_signal", "review_due"}
KNOWN_BUCKETS = {
    "reviewed",
    "reviewed_support",
    "raw_anchor",
    "stable_anchor",
    "candidate",
    "review_input",
    "feedback",
    "runtime_memory",
}
ALLOWED_PACK_ROLES = {"orientation", "review_input", "anchor", "support"}
SELECTED_BY_CHANNELS = {"context_pack", "runtime_memory", "receipt", "manual_fixture", "bucket_filter", "semantic", "lexical"}
SUPPORT_SUFFICIENCY = {"sufficient", "insufficient", "missing_anchor", "not_ready", "scope_limited", "not_checked"}

CLAIM_FIELDS = {
    "claims",
    "memory_claims",
    "context_claims",
    "writeback_claims",
    "bridge_claims",
    "action_claims",
}

FORBIDDEN_AUTHORITY_CLAIMS = {
    "truth",
    "truth_confidence",
    "review_pass",
    "reviewed_knowledge",
    "reviewed_claim",
    "reviewed_pattern",
    "reviewed_decision",
    "reviewed_relation",
    "evidence_support",
    "support",
    "action_basis",
    "ready_action_basis",
    "action_ready",
    "promotion",
    "promotion_ready",
    "mainline_ready",
    "schema_governance",
}

AUTHORITY_BOOL_FIELDS = {
    "truth_mutation_allowed",
    "truth_confidence_changed",
    "verification_status_changed",
    "reviewed_knowledge_created",
    "reviewed_claim_created",
    "reviewed_relation_created",
    "evidence_support_created",
    "support_created",
    "action_basis_allowed",
    "action_ready",
    "promotion_ready",
    "mainline_ready",
    "schema_governance",
    "memory_rank_claims_truth",
    "memory_confidence_claims_truth",
    "retention_score_claims_truth",
    "lesson_claims_reviewed",
    "selected_by_claims_authority",
    "feedback_mutates_truth",
    "review_due_invalidates_truth",
    "candidate_signal_promotes",
    "uses_runtime_memory_as_action_basis",
    "context_hit_claims_support",
    "writeback_direct_to_reviewed",
    "memory_save_direct_vaks_writeback",
    "on_memory_write_direct_vaks_writeback",
}

RUNTIME_FORBIDDEN_BOOL_FIELDS = {
    "dependency_install_requested": "MB_DEPENDENCY_INSTALL_FORBIDDEN",
    "agentmemory_install_requested": "MB_DEPENDENCY_INSTALL_FORBIDDEN",
    "real_misa_runtime_started": "MB_REAL_RUNTIME_FORBIDDEN",
    "real_agentmemory_runtime_started": "MB_REAL_RUNTIME_FORBIDDEN",
    "hooks_enabled": "MB_HOOKS_FORBIDDEN",
    "background_service": "MB_BACKGROUND_SERVICE_FORBIDDEN",
    "background_memory_sync": "MB_BACKGROUND_SERVICE_FORBIDDEN",
    "mcp_write_tool_exposed": "MB_MCP_WRITE_TOOL_FORBIDDEN",
    "broad_mcp_save_tool": "MB_BROAD_MCP_TOOL_FORBIDDEN",
    "broad_mcp_delete_tool": "MB_BROAD_MCP_TOOL_FORBIDDEN",
    "broad_mcp_export_tool": "MB_BROAD_MCP_TOOL_FORBIDDEN",
    "obsidian_sync_requested": "MB_OBSIDIAN_SYNC_FORBIDDEN",
    "obsidian_export_as_knowledge": "MB_OBSIDIAN_SYNC_FORBIDDEN",
}

PROTECTED_PREFIXES = {
    "h:/obsidian/",
    "h:\\obsidian\\",
    "wiki/claims/",
    "wiki/patterns/",
    "wiki/decisions/",
    "templates/",
    "tools/",
    "raw/",
}

PROTECTED_EXACTS = {
    "h:/obsidian",
    "wiki/claims",
    "wiki/patterns",
    "wiki/decisions",
    "templates",
    "tools",
    "raw",
}

PROTECTED_FILES = {
    "schema.md",
    "architecture_principles.md",
    "fusion_architecture_v0_2_draft.md",
    "readme.md",
}


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    item_id: str = ""

    def as_dict(self) -> dict[str, str]:
        result = {"code": self.code, "message": self.message}
        if self.item_id:
            result["item_id"] = self.item_id
        return result


def norm(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).strip().lower().replace("\\", "/").replace(" ", "_").replace("-", "_")


def raw_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def path_norm(value: Any) -> str:
    return raw_text(value).replace("\\", "/").lower()


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return norm(value) in {"true", "yes", "1"}


def as_list(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [norm(item) for item in value if norm(item)]
    return [norm(item) for item in str(value).split(",") if norm(item)]


def has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, list):
        return any(has_value(item) for item in value)
    if isinstance(value, dict):
        return bool(value)
    return raw_text(value) != ""


def add_once(issues: list[Issue], code: str, message: str, item_id: str = "") -> None:
    key = (code, item_id)
    if key not in {(issue.code, issue.item_id) for issue in issues}:
        issues.append(Issue(code, message, item_id))


def item_id(item: dict[str, Any]) -> str:
    return raw_text(item.get("id")) or raw_text(item.get("ref")) or raw_text(item.get("path")) or "<unknown>"


def deep_merge(base: Any, patch: Any) -> Any:
    if isinstance(patch, dict) and patch.get("__delete__") is True:
        return "__SANDBOX_DELETE__"
    if isinstance(base, dict) and isinstance(patch, dict):
        result = dict(base)
        for key, value in patch.items():
            merged = deep_merge(result.get(key), value)
            if merged == "__SANDBOX_DELETE__":
                result.pop(key, None)
            else:
                result[key] = merged
        return result
    return patch


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"manifest must be a JSON object: {path}")
    return data


def load_fixture_json(issues: list[Issue], value: Any, item: str) -> dict[str, Any] | None:
    resolved = validate_fixture_file(issues, value, item)
    if resolved is None:
        return None
    try:
        return load_json(resolved)
    except (OSError, json.JSONDecodeError, ValueError):
        add_once(issues, "MB_FIXTURE_JSON_INVALID", "referenced fixture must be valid JSON.", item)
        return None


def load_manifest(path: Path) -> dict[str, Any]:
    path = path.resolve()
    data = load_json(path)
    if not has_value(data.get("extends")):
        return data

    base_path = (SANDBOX_ROOT / raw_text(data["extends"])).resolve()
    if not path_under(base_path, SANDBOX_ROOT):
        raise ValueError(f"extends path escapes sandbox root: {data['extends']}")

    base = load_manifest(base_path)
    patched = deep_merge(base, data.get("patch", {}))
    overlay = {key: value for key, value in data.items() if key not in {"extends", "patch"}}
    return deep_merge(patched, overlay)


def path_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def resolve_manifest_path(value: Any) -> Path | None:
    text = raw_text(value)
    if not text:
        return None
    candidate = Path(text)
    if candidate.is_absolute():
        return candidate.resolve()
    normalized = path_norm(text).lstrip("./")
    if normalized.startswith(("fixtures/", "artifact/", "failure-cases/")):
        return (SANDBOX_ROOT / text).resolve()
    return (WORKSPACE_ROOT / text).resolve()


def protected_target(value: Any) -> bool:
    original = path_norm(value)
    if not original:
        return False
    candidates = {original.lstrip("./")}
    resolved = resolve_manifest_path(value)
    if resolved is not None:
        resolved_text = path_norm(resolved.as_posix())
        candidates.add(resolved_text)
        try:
            candidates.add(path_norm(resolved.relative_to(WORKSPACE_ROOT).as_posix()))
        except ValueError:
            pass

    for text in candidates:
        trimmed = text.lstrip("./")
        if ".codex/" in trimmed or trimmed.startswith(".codex/"):
            return True
        if trimmed.rstrip("/") in PROTECTED_EXACTS:
            return True
        if trimmed in PROTECTED_FILES or any(trimmed.endswith(f"/{name}") for name in PROTECTED_FILES):
            return True
        if any(trimmed.startswith(prefix) or f"/{prefix}" in trimmed for prefix in PROTECTED_PREFIXES):
            return True
    return False


def allowed_write_path_in_slice(value: Any) -> bool:
    resolved = resolve_manifest_path(value)
    if resolved is None:
        return False
    return path_under(resolved, SANDBOX_ROOT)


def validate_fixture_file(issues: list[Issue], value: Any, item: str) -> Path | None:
    if not has_value(value):
        add_once(issues, "MB_FIXTURE_REF_MISSING", "fixture ref is required.", item)
        return None
    if protected_target(value):
        add_once(issues, "MB_PROTECTED_PATH_TARGET", "fixture ref points at protected territory.", item)

    resolved = resolve_manifest_path(value)
    if resolved is None or not path_under(resolved, SANDBOX_ROOT):
        add_once(issues, "MB_PATH_OUTSIDE_SANDBOX", "fixture ref must stay inside this sandbox.", item)
        return None
    if not path_under(resolved, SANDBOX_ROOT / "fixtures"):
        add_once(issues, "MB_PATH_OUTSIDE_FIXTURES", "fixture ref must point inside copied fixtures.", item)
    if not resolved.is_file():
        add_once(issues, "MB_FIXTURE_PATH_MISSING", "referenced fixture file is missing.", item)
        return None
    try:
        with resolved.open("r", encoding="utf-8") as handle:
            handle.read(1)
    except OSError:
        add_once(issues, "MB_FIXTURE_PATH_UNREADABLE", "referenced fixture file is not readable.", item)
        return None
    return resolved


def validate_runtime_fixture(issues: list[Issue], entry: dict[str, Any], current_id: str) -> None:
    data = load_fixture_json(issues, entry.get("ref"), current_id)
    if data is None:
        return
    if norm(data.get("memory_type")) != norm(entry.get("memory_type")):
        add_once(issues, "MB_RUNTIME_FIXTURE_TYPE_MISMATCH", "runtime fixture memory_type must match manifest entry.", current_id)
    if norm(entry.get("memory_type")) in {"session_observation", "tool_result"} and not has_value(
        data.get("sourceObservationIds")
    ):
        add_once(issues, "MB_SOURCE_OBSERVATION_TRACE_MISSING", "runtime fixture needs sourceObservationIds.", current_id)
    if any(
        as_bool(data.get(field))
        for field in ["truth_mutation_allowed", "reviewed_knowledge_created", "action_basis_allowed", "promotion_ready"]
    ):
        add_once(issues, "MB_RUNTIME_FIXTURE_AUTHORITY_CONFUSION", "runtime fixture cannot assert VAKS authority.", current_id)


def validate_context_pack_fixture(issues: list[Issue], ref: Any, included: set[str], excluded: set[str]) -> dict[str, Any] | None:
    data = load_fixture_json(issues, ref, raw_text(ref))
    if data is None:
        return None
    if not as_bool(data.get("read_only")):
        add_once(issues, "MB_CONTEXT_FIXTURE_NOT_READ_ONLY", "context pack fixture must be read-only.", raw_text(ref))
    fixture_included = set(as_list(data.get("included_buckets")))
    fixture_excluded = set(as_list(data.get("excluded_buckets")))
    if fixture_included and not fixture_included.issubset(included):
        add_once(issues, "MB_CONTEXT_FIXTURE_BUCKET_MISMATCH", "context pack included buckets exceed manifest buckets.", raw_text(ref))
    if fixture_excluded and not excluded.issubset(fixture_excluded):
        add_once(issues, "MB_CONTEXT_FIXTURE_BUCKET_MISMATCH", "context pack excluded buckets do not preserve manifest exclusions.", raw_text(ref))
    for item in data.get("items", []):
        if not isinstance(item, dict):
            add_once(issues, "MB_CONTEXT_FIXTURE_ITEM_INVALID", "context pack fixture item must be object.", raw_text(ref))
            continue
        bucket = norm(item.get("authority_bucket"))
        role = norm(item.get("pack_role"))
        current_id = raw_text(item.get("id")) or raw_text(ref)
        if bucket in excluded or (included and bucket not in included):
            add_once(issues, "MB_CONTEXT_FIXTURE_BUCKET_MISMATCH", "context pack item bucket outside manifest scope.", current_id)
        if role == "support" and bucket not in {"reviewed_support", "raw_anchor", "stable_anchor"}:
            add_once(issues, "MB_CONTEXT_FIXTURE_SUPPORT_MISUSE", "context pack fixture misuses support role.", current_id)
        if as_bool(item.get("action_basis_allowed")):
            add_once(issues, "MB_CONTEXT_FIXTURE_ACTION_BASIS", "context pack fixture cannot allow action basis.", current_id)
    return data


def validate_writeback_fixture(issues: list[Issue], record: dict[str, Any], current_id: str) -> None:
    data = load_fixture_json(issues, record.get("ref"), current_id)
    if data is None:
        return
    if norm(data.get("record_kind")).replace("_fixture", "") != norm(record.get("record_type")):
        # The fixture names are intentionally lightweight, so this is warning-like
        # but still blocks obvious cross-type drift.
        expected_prefixes = {
            "feedback_event": "feedback_event",
            "candidate_signal": "candidate_signal",
            "review_due": "review_due",
        }
        prefix = expected_prefixes.get(norm(record.get("record_type")), "")
        if prefix and not norm(data.get("record_kind")).startswith(prefix):
            add_once(issues, "MB_WRITEBACK_FIXTURE_TYPE_MISMATCH", "writeback fixture kind must match record type.", current_id)
    if as_bool(data.get("truth_mutation_allowed")) or as_bool(data.get("feedback_mutates_truth")):
        add_once(issues, "MB_FEEDBACK_TRUTH_MUTATION", "writeback fixture cannot mutate truth.", current_id)
    if as_bool(data.get("promotion_ready")) or as_bool(data.get("candidate_signal_promotes")):
        add_once(issues, "MB_CANDIDATE_SIGNAL_PROMOTION", "writeback fixture cannot promote.", current_id)
    if as_bool(data.get("review_due_invalidates_truth")):
        add_once(issues, "MB_REVIEW_DUE_INVALIDATES_TRUTH", "review_due fixture cannot invalidate truth.", current_id)
    if as_bool(data.get("writeback_direct_to_reviewed")):
        add_once(issues, "MB_REVIEWED_WRITE_FORBIDDEN", "writeback fixture cannot target reviewed layer.", current_id)


def validate_receipt_fixture(issues: list[Issue], ref: Any) -> dict[str, Any] | None:
    data = load_fixture_json(issues, ref, "writeback.operation_receipt_ref")
    if data is None:
        return None
    if not has_value(data.get("receipt_id")):
        add_once(issues, "MB_RECEIPT_ID_MISSING", "operation receipt fixture needs receipt_id.")
    if as_bool(data.get("writes_reviewed_layer")):
        add_once(issues, "MB_RECEIPT_WRITES_REVIEWED", "operation receipt cannot write reviewed layer.")
    allowed = set(as_list(data.get("allowed_record_types")))
    if not allowed or not allowed.issubset(ALLOWED_WRITEBACK_TYPES):
        add_once(issues, "MB_RECEIPT_ALLOWED_TYPES_INVALID", "operation receipt allowed types are invalid.")
    return data


def collect_claims(item: dict[str, Any]) -> set[str]:
    claims: set[str] = set()
    for field in CLAIM_FIELDS:
        claims.update(as_list(item.get(field)))
    return claims


def scan_authority_confusion(value: Any, issues: list[Issue], path: str = "$") -> None:
    if isinstance(value, dict):
        claims = collect_claims(value)
        if claims.intersection(FORBIDDEN_AUTHORITY_CLAIMS):
            add_once(
                issues,
                "MB_AUTHORITY_CLAIM_FORBIDDEN",
                "bridge artifacts cannot claim truth, support, review, action, promotion, or schema authority.",
                path,
            )

        for key, field_value in value.items():
            field_name = norm(key)
            if field_name in FORBIDDEN_AUTHORITY_CLAIMS and (
                as_bool(field_value) or (not isinstance(field_value, bool) and has_value(field_value))
            ):
                add_once(
                    issues,
                    "MB_AUTHORITY_CLAIM_FORBIDDEN",
                    "direct authority fields are forbidden in bridge artifacts.",
                    f"{path}.{key}",
                )
            if field_name in AUTHORITY_BOOL_FIELDS and as_bool(field_value):
                add_once(
                    issues,
                    "MB_AUTHORITY_CONFUSION",
                    "runtime memory / bridge fields cannot assert truth, support, action, promotion, or reviewed authority.",
                    f"{path}.{key}",
                )
            scan_authority_confusion(field_value, issues, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            scan_authority_confusion(item, issues, f"{path}[{index}]")


def validate_scope(scope: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(scope, dict):
        add_once(issues, "MB_MISSING_SCOPE", "scope block is required.")
        return issues

    if not as_bool(scope.get("sandbox_fixture_only")):
        add_once(issues, "MB_SCOPE_NOT_SANDBOX_ONLY", "bridge sandbox must use copied fixtures only.")

    for field, code in RUNTIME_FORBIDDEN_BOOL_FIELDS.items():
        if as_bool(scope.get(field)):
            messages = {
                "MB_DEPENDENCY_INSTALL_FORBIDDEN": "dependency installation is forbidden.",
                "MB_REAL_RUNTIME_FORBIDDEN": "real MISA/agentmemory runtime execution is forbidden.",
                "MB_HOOKS_FORBIDDEN": "hooks are forbidden.",
                "MB_BACKGROUND_SERVICE_FORBIDDEN": "background services or sync are forbidden.",
                "MB_MCP_WRITE_TOOL_FORBIDDEN": "MCP write tools are forbidden.",
                "MB_BROAD_MCP_TOOL_FORBIDDEN": "broad save/delete/export MCP tools are forbidden.",
                "MB_OBSIDIAN_SYNC_FORBIDDEN": "Obsidian export/sync is forbidden.",
            }
            add_once(issues, code, messages[code], field)

    for path in scope.get("allowed_write_paths", []):
        if not allowed_write_path_in_slice(path):
            add_once(issues, "MB_WRITE_PATH_OUTSIDE_SLICE", "allowed write path must be this sandbox slice.", raw_text(path))
        if protected_target(path):
            add_once(issues, "MB_PROTECTED_PATH_TARGET", "allowed write path points at protected territory.", raw_text(path))

    return issues


def validate_runtime_memory(runtime_memory: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(runtime_memory, dict):
        add_once(issues, "MB_MISSING_RUNTIME_MEMORY", "runtime_memory block is required.")
        return issues

    if norm(runtime_memory.get("status")) != "quarantined_runtime_memory":
        add_once(issues, "MB_RUNTIME_MEMORY_NOT_QUARANTINED", "runtime memory must stay quarantined.")

    allowed = set(as_list(runtime_memory.get("allowed_memory_types")))
    if not allowed or not allowed.issubset(ALLOWED_MEMORY_TYPES):
        add_once(issues, "MB_MEMORY_TYPES_INVALID", "allowed memory types must be the runtime-only registry subset.")

    if as_bool(runtime_memory.get("writes_vaks_reviewed_layer")) or as_bool(runtime_memory.get("direct_vaks_writeback")):
        add_once(issues, "MB_RUNTIME_DIRECT_VAKS_WRITE_FORBIDDEN", "runtime memory cannot directly write VAKS.")

    entries = runtime_memory.get("entries", [])
    if not isinstance(entries, list) or not entries:
        add_once(issues, "MB_RUNTIME_ENTRIES_MISSING", "runtime memory entries are required.")
        return issues

    for entry in entries:
        if not isinstance(entry, dict):
            add_once(issues, "MB_RUNTIME_ENTRY_INVALID", "runtime memory entry must be an object.")
            continue
        current_id = item_id(entry)
        memory_type = norm(entry.get("memory_type"))
        if memory_type not in ALLOWED_MEMORY_TYPES:
            add_once(issues, "MB_MEMORY_TYPE_INVALID", "memory entry type is not allowed.", current_id)
        if allowed and memory_type not in allowed:
            add_once(issues, "MB_MEMORY_TYPE_NOT_ALLOWED_BY_MANIFEST", "memory entry type is outside manifest allowlist.", current_id)
        validate_runtime_fixture(issues, entry, current_id)
        if memory_type in {"session_observation", "tool_result"} and not has_value(entry.get("source_observation_ids")):
            add_once(issues, "MB_SOURCE_OBSERVATION_TRACE_MISSING", "runtime observation needs sourceObservationIds-style trace.", current_id)
        if as_bool(entry.get("action_basis_allowed")):
            add_once(issues, "MB_ACTION_BASIS_FORBIDDEN", "runtime memory entry cannot be action basis.", current_id)

    return issues


def validate_context_adapter(adapter: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(adapter, dict):
        add_once(issues, "MB_MISSING_CONTEXT_ADAPTER", "context_adapter block is required.")
        return issues

    if norm(adapter.get("mode")) != "read_only_context_pack_fetch":
        add_once(issues, "MB_CONTEXT_MODE_INVALID", "context adapter must be read_only_context_pack_fetch.")
    if not as_bool(adapter.get("read_only")):
        add_once(issues, "MB_CONTEXT_NOT_READ_ONLY", "context adapter must be read-only.")
    if not as_bool(adapter.get("authority_bucket_first")):
        add_once(issues, "MB_BUCKET_FILTER_NOT_FIRST", "authority bucket filter must run before context injection.")
    if as_bool(adapter.get("cross_bucket_fusion")):
        add_once(issues, "MB_CROSS_BUCKET_FUSION", "context adapter cannot fuse across authority buckets.")
    if not as_bool(adapter.get("context_injection_labeled")) or not as_bool(adapter.get("warnings_visible")):
        add_once(issues, "MB_CONTEXT_LABELS_MISSING", "context injection needs authority labels and visible warnings.")

    included = set(as_list(adapter.get("included_buckets")))
    excluded = set(as_list(adapter.get("excluded_buckets")))
    context_pack_refs = adapter.get("context_pack_refs", [])
    if not isinstance(context_pack_refs, list) or not context_pack_refs:
        add_once(issues, "MB_CONTEXT_PACK_REFS_MISSING", "context adapter must list context pack fixture refs.")
        pack_items: set[tuple[str, str]] = set()
    else:
        pack_items = set()
        for ref in context_pack_refs:
            pack = validate_context_pack_fixture(issues, ref, included, excluded)
            if isinstance(pack, dict):
                for pack_item in pack.get("items", []):
                    if isinstance(pack_item, dict):
                        pack_items.add((raw_text(pack_item.get("id")), raw_text(pack_item.get("ref"))))

    items = adapter.get("items", [])
    if not isinstance(items, list) or not items:
        add_once(issues, "MB_CONTEXT_ITEMS_MISSING", "context adapter items are required.")
        return issues

    if not included or not excluded:
        add_once(issues, "MB_CONTEXT_BUCKETS_MISSING", "included and excluded buckets are required.")

    for item in items:
        if not isinstance(item, dict):
            add_once(issues, "MB_CONTEXT_ITEM_INVALID", "context item must be an object.")
            continue
        current_id = item_id(item)
        bucket = norm(item.get("authority_bucket"))
        role = norm(item.get("pack_role"))
        selected_by = set(as_list(item.get("selected_by")))
        validate_fixture_file(issues, item.get("ref"), current_id)
        if pack_items and (raw_text(item.get("id")), raw_text(item.get("ref"))) not in pack_items:
            add_once(issues, "MB_CONTEXT_ITEM_NOT_IN_PACK", "manifest context item must exist in referenced context pack fixture.", current_id)

        if bucket not in KNOWN_BUCKETS:
            add_once(issues, "MB_UNKNOWN_BUCKET", "unknown authority bucket.", current_id)
        if bucket in excluded or (included and bucket not in included):
            add_once(issues, "MB_CONTEXT_BUCKET_OUT_OF_SCOPE", "context item bucket is not allowed for this bridge call.", current_id)
        if role not in ALLOWED_PACK_ROLES:
            add_once(issues, "MB_CONTEXT_ROLE_MISSING", "context item pack_role is missing or invalid.", current_id)
        if role == "support" and bucket not in {"reviewed_support", "raw_anchor", "stable_anchor"}:
            add_once(issues, "MB_CONTEXT_HIT_AS_SUPPORT", "candidate/runtime/feedback context cannot be support.", current_id)
        if role == "support" and not has_value(item.get("independent_anchor_ref")):
            add_once(issues, "MB_SUPPORT_ANCHOR_MISSING", "support context needs an independent anchor ref.", current_id)
        if as_bool(item.get("action_basis_allowed")):
            add_once(issues, "MB_ACTION_BASIS_FORBIDDEN", "context item cannot itself be action basis.", current_id)
        if not has_value(item.get("warning_code")):
            add_once(issues, "MB_CONTEXT_WARNING_MISSING", "context item needs warning code.", current_id)
        if not selected_by or selected_by.difference(SELECTED_BY_CHANNELS):
            add_once(issues, "MB_SELECTED_BY_MISSING", "context item needs selected_by trace.", current_id)

    return issues


def validate_writeback(writeback: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(writeback, dict):
        add_once(issues, "MB_MISSING_WRITEBACK", "writeback block is required.")
        return issues

    allowed = set(as_list(writeback.get("allowed_record_types")))
    if not allowed or not allowed.issubset(ALLOWED_WRITEBACK_TYPES):
        add_once(issues, "MB_WRITEBACK_TYPES_INVALID", "writeback is limited to feedback_event, candidate_signal, and review_due.")
    if as_bool(writeback.get("memory_save_direct_vaks_writeback")) or as_bool(writeback.get("on_memory_write_direct_vaks_writeback")):
        add_once(issues, "MB_DIRECT_MEMORY_WRITEBACK_FORBIDDEN", "memory_save/on_memory_write cannot directly write VAKS.")
    receipt = validate_receipt_fixture(issues, writeback.get("operation_receipt_ref"))
    receipt_id = raw_text(receipt.get("receipt_id")) if isinstance(receipt, dict) else ""
    receipt_allowed_types = set(as_list(receipt.get("allowed_record_types"))) if isinstance(receipt, dict) else set()

    records = writeback.get("records", [])
    if not isinstance(records, list) or not records:
        add_once(issues, "MB_WRITEBACK_RECORDS_MISSING", "writeback records are required.")
        return issues

    for record in records:
        if not isinstance(record, dict):
            add_once(issues, "MB_WRITEBACK_RECORD_INVALID", "writeback record must be an object.")
            continue
        current_id = item_id(record)
        record_type = norm(record.get("record_type"))
        if record_type not in ALLOWED_WRITEBACK_TYPES:
            add_once(issues, "MB_WRITEBACK_TYPE_FORBIDDEN", "writeback record type is not allowed.", current_id)
        if allowed and record_type not in allowed:
            add_once(issues, "MB_WRITEBACK_TYPE_NOT_ALLOWED_BY_MANIFEST", "writeback record type is outside manifest allowlist.", current_id)
        validate_writeback_fixture(issues, record, current_id)
        if not has_value(record.get("receipt_id")):
            add_once(issues, "MB_WRITEBACK_RECEIPT_MISSING", "writeback record needs a receipt id.", current_id)
        elif receipt_id and raw_text(record.get("receipt_id")) != receipt_id:
            add_once(issues, "MB_RECEIPT_ID_MISMATCH", "writeback record receipt_id must match operation receipt.", current_id)
        if receipt_allowed_types and record_type not in receipt_allowed_types:
            add_once(issues, "MB_RECEIPT_TYPE_NOT_ALLOWED", "operation receipt does not allow this record type.", current_id)
        if record_type == "feedback_event" and as_bool(record.get("feedback_mutates_truth")):
            add_once(issues, "MB_FEEDBACK_TRUTH_MUTATION", "feedback cannot mutate truth.", current_id)
        if record_type == "candidate_signal" and as_bool(record.get("candidate_signal_promotes")):
            add_once(issues, "MB_CANDIDATE_SIGNAL_PROMOTION", "candidate signal cannot promote knowledge.", current_id)
        if record_type == "review_due" and as_bool(record.get("review_due_invalidates_truth")):
            add_once(issues, "MB_REVIEW_DUE_INVALIDATES_TRUTH", "review_due is review pressure, not proof of invalidity.", current_id)
        if as_bool(record.get("writeback_direct_to_reviewed")):
            add_once(issues, "MB_REVIEWED_WRITE_FORBIDDEN", "writeback cannot target reviewed VAKS knowledge.", current_id)

    return issues


def validate_action_readiness(action: Any, expected_receipt_ref: Any = None) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(action, dict):
        add_once(issues, "MB_MISSING_ACTION_READINESS", "action_readiness block is required.")
        return issues

    if not as_bool(action.get("vaks_action_readiness_check_required")):
        add_once(issues, "MB_ACTION_READINESS_CHECK_REQUIRED", "action-facing bridge output must require VAKS action-readiness check.")
    sufficiency = norm(action.get("support_sufficiency"))
    if sufficiency not in SUPPORT_SUFFICIENCY:
        add_once(issues, "MB_SUPPORT_SUFFICIENCY_INVALID", "support_sufficiency value is invalid.")
    if sufficiency != "sufficient" and (as_bool(action.get("action_ready")) or as_bool(action.get("action_basis_allowed"))):
        add_once(issues, "MB_ACTION_READY_WITH_INSUFFICIENT_SUPPORT", "insufficient support cannot produce action readiness.")
    if as_bool(action.get("uses_runtime_memory_as_action_basis")):
        add_once(issues, "MB_RUNTIME_MEMORY_AS_ACTION_BASIS", "runtime memory cannot be action basis.")
    if as_bool(action.get("action_basis_allowed")):
        add_once(issues, "MB_ACTION_BASIS_FORBIDDEN", "bridge cannot directly allow action basis.")
    if not has_value(action.get("blocker_codes")) and sufficiency != "sufficient":
        add_once(issues, "MB_ACTION_BLOCKERS_MISSING", "blocked action-readiness state needs blocker codes.")
    validate_fixture_file(issues, action.get("context_pack_ref"), "action_readiness.context_pack_ref")
    validate_receipt_fixture(issues, action.get("operation_receipt_ref"))
    if has_value(expected_receipt_ref) and raw_text(action.get("operation_receipt_ref")) != raw_text(expected_receipt_ref):
        add_once(issues, "MB_ACTION_RECEIPT_MISMATCH", "action-readiness receipt must match writeback operation receipt.")

    return issues


def validate_use_loop_trace(trace: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(trace, dict):
        add_once(issues, "MB_MISSING_USE_LOOP_TRACE", "use_loop_trace block is required.")
        return issues

    data = load_fixture_json(issues, trace.get("trace_ref"), "use_loop_trace.trace_ref")
    if not as_bool(trace.get("read_only")):
        add_once(issues, "MB_USE_LOOP_NOT_READ_ONLY", "use-loop trace must be read-only.")
    if as_bool(trace.get("tool_writes")):
        add_once(issues, "MB_USE_LOOP_WRITES_FORBIDDEN", "use-loop trace cannot include tool writes.")
    if as_bool(trace.get("action_basis_allowed")):
        add_once(issues, "MB_USE_LOOP_ACTION_BASIS", "use-loop trace cannot create action basis.")
    if not as_bool(trace.get("authority_labels_visible")) or not as_bool(trace.get("warnings_visible")):
        add_once(issues, "MB_USE_LOOP_LABELS_MISSING", "use-loop trace needs visible authority labels and warnings.")

    if data is not None:
        if not as_bool(data.get("read_only")):
            add_once(issues, "MB_USE_LOOP_NOT_READ_ONLY", "use-loop fixture must be read-only.")
        if as_bool(data.get("tool_writes")):
            add_once(issues, "MB_USE_LOOP_WRITES_FORBIDDEN", "use-loop fixture cannot include tool writes.")
        if as_bool(data.get("action_basis_allowed")):
            add_once(issues, "MB_USE_LOOP_ACTION_BASIS", "use-loop fixture cannot create action basis.")
        if not as_bool(data.get("authority_labels_visible")) or not as_bool(data.get("warnings_visible")):
            add_once(issues, "MB_USE_LOOP_LABELS_MISSING", "use-loop fixture needs visible authority labels and warnings.")
        validate_fixture_file(issues, data.get("context_pack_ref"), "use_loop_trace.fixture.context_pack_ref")

    return issues


def validate_boundary(boundary: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(boundary, dict):
        add_once(issues, "MB_MISSING_BOUNDARY", "boundary block is required.")
        return issues

    if as_bool(boundary.get("reviewed_write_allowed")) or as_bool(boundary.get("truth_mutation_allowed")):
        add_once(issues, "MB_REVIEWED_WRITE_FORBIDDEN", "bridge cannot write reviewed/truth layers.")
    if as_bool(boundary.get("evidence_support_created")):
        add_once(issues, "MB_SUPPORT_CREATION_FORBIDDEN", "bridge cannot create evidence support.")
    if as_bool(boundary.get("action_basis_allowed")):
        add_once(issues, "MB_ACTION_BASIS_FORBIDDEN", "bridge cannot create action basis.")
    if as_bool(boundary.get("promotion_ready")) or as_bool(boundary.get("mainline_ready")):
        add_once(issues, "MB_AUTHORITY_CONFUSION", "bridge cannot create promotion or mainline readiness.")

    return issues


def validate_manifest(manifest: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if norm(manifest.get("record_kind")) != RECORD_KIND:
        add_once(issues, "MB_INVALID_RECORD_KIND", f"record_kind must be {RECORD_KIND}.")
    if not has_value(manifest.get("scenario_id")):
        add_once(issues, "MB_MISSING_SCENARIO_ID", "scenario_id is required.")

    scan_authority_confusion(manifest, issues)
    issues.extend(validate_scope(manifest.get("scope")))
    issues.extend(validate_runtime_memory(manifest.get("runtime_memory")))
    issues.extend(validate_context_adapter(manifest.get("context_adapter")))
    issues.extend(validate_writeback(manifest.get("writeback")))
    writeback = manifest.get("writeback") if isinstance(manifest.get("writeback"), dict) else {}
    issues.extend(validate_action_readiness(manifest.get("action_readiness"), writeback.get("operation_receipt_ref")))
    issues.extend(validate_use_loop_trace(manifest.get("use_loop_trace")))
    issues.extend(validate_boundary(manifest.get("boundary")))
    return issues


def summarize(manifest: dict[str, Any], issues: list[Issue]) -> dict[str, Any]:
    return {
        "scenario_id": manifest.get("scenario_id", "<missing>"),
        "valid": not issues,
        "issue_codes": sorted({issue.code for issue in issues}),
        "issues": [issue.as_dict() for issue in issues],
        "non_claims": {
            "runtime_memory_not_reviewed_knowledge": True,
            "context_pack_fetch_not_evidence_support": True,
            "writeback_signal_not_truth_mutation": True,
            "bridge_pass_not_action_basis": True,
            "bridge_pass_not_mainline_readiness": True,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="path to a MISA/VAKS bridge manifest JSON")
    args = parser.parse_args(argv)
    manifest = load_manifest(args.manifest)
    issues = validate_manifest(manifest)
    print(json.dumps(summarize(manifest, issues), indent=2, sort_keys=True))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
