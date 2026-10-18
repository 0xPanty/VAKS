#!/usr/bin/env python3
"""
Sandbox-only P2-17 VAKS use-surface optimization validator.

This prototype validates copied product-surface blueprints. It proves that
entry/status/navigation/receipt/hash/dirty-state surfaces can improve operator
flow without creating reviewed knowledge, evidence support, action basis,
promotion, mainline readiness, or real UI/runtime authority.
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
SLICE_PATH = "outputs/review/vaks-implementation-sandbox/2026-06-15-p2-17-use-surface-optimization-pass"

RECORD_KIND = "vaks_use_surface_blueprint"

REQUIRED_ENTRIES = {
    "add_source": ("source_card", "provenance_only"),
    "process_this": ("candidate_distillation", "candidate_only"),
    "ask_vault": ("query_run_trace", "orientation_unless_action_mode"),
    "check_vault": ("maintenance_manifest", "diagnostic_only"),
    "make_context_pack": ("context_pack_manifest", "not_action_basis_by_itself"),
    "review_candidates": ("evidence_packet_or_review_candidate", "review_input_only"),
    "record_feedback": ("feedback_event", "activation_review_pressure_only"),
    "prepare_action": ("context_support_readiness_bundle", "blocked_until_action_readiness"),
}

REQUIRED_QUESTIONS = {
    "where_put_this",
    "what_state_is_it_in",
    "orientation_review_or_action",
    "what_blocks_promotion_or_action",
    "source_hash_receipt_integrity",
    "authority_not_mutated",
}

REQUIRED_STATUS_FLAGS = {
    "blocked",
    "stale",
    "missing_anchor",
    "hash_mismatch",
    "action_not_ready",
    "dirty_state",
}

REQUIRED_BADGES = {
    "raw",
    "candidate",
    "review_input",
    "reviewed",
    "context_pack",
    "action_readiness",
    "feedback",
}

AUTHORITY_BOOL_FIELDS = {
    "can_approve",
    "can_write_reviewed",
    "can_promote",
    "creates_action_basis",
    "creates_evidence_support",
    "mutates_truth",
    "mainline_ready",
    "reviewed_write_enabled",
    "selected_by_is_support",
    "raw_topk_is_trust",
    "badge_can_promote",
    "dirty_state_judges_knowledge",
    "hash_match_is_evidence_support",
    "context_pack_is_action_basis",
    "sync_mutates_truth",
    "query_hit_is_support",
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
    "SCHEMA.md",
    "ARCHITECTURE_PRINCIPLES.md",
    "FUSION_ARCHITECTURE_V0_2_DRAFT.md",
    "README.md",
}

FORBIDDEN_SCOPE_FIELDS = {
    "server_started",
    "real_ui_started",
    "real_runtime_started",
    "ui_deployed",
    "background_service",
    "background_service_started",
    "watcher_started",
    "automation_started",
    "hook_enabled",
    "hooks_enabled",
    "dependency_install",
    "mcp_write_tool",
    "obsidian_sync",
    "commit_or_push",
}


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    item: str = ""


def raw_text(value: Any) -> str:
    return "" if value is None else str(value)


def norm(value: Any) -> str:
    return raw_text(value).strip().lower()


def path_norm(value: Any) -> str:
    return raw_text(value).replace("\\", "/").strip()


def as_bool(value: Any) -> bool:
    return value is True or norm(value) in {"true", "yes", "1", "allowed", "enabled", "ready"}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def add_once(issues: list[Issue], code: str, message: str, item: str = "") -> None:
    candidate = Issue(code, message, item)
    if candidate not in issues:
        issues.append(candidate)


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
    if normalized.startswith(("fixtures/", "prototype/", "artifact/", "failure-cases/")):
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
        trimmed_lower = trimmed.lower()
        protected_files_lower = {name.lower() for name in PROTECTED_FILES}
        if ".codex/" in trimmed_lower or trimmed_lower.startswith(".codex/"):
            return True
        if trimmed_lower.rstrip("/") in PROTECTED_EXACTS:
            return True
        if trimmed_lower in protected_files_lower or any(trimmed_lower.endswith(f"/{name}") for name in protected_files_lower):
            return True
        if any(
            trimmed_lower.startswith(prefix.lower()) or f"/{prefix.lower()}" in trimmed_lower
            for prefix in PROTECTED_PREFIXES
        ):
            return True
    return False


def allowed_write_path_in_slice(value: Any) -> bool:
    resolved = resolve_manifest_path(value)
    if resolved is None:
        return False
    return path_under(resolved, SANDBOX_ROOT)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def deep_merge(base: Any, patch: Any) -> Any:
    if isinstance(patch, dict) and patch.get("__delete__") is True:
        return None
    if isinstance(base, dict) and isinstance(patch, dict):
        result = dict(base)
        for key, value in patch.items():
            if isinstance(value, dict) and value.get("__delete__") is True:
                result.pop(key, None)
            else:
                result[key] = deep_merge(result.get(key), value)
        return result
    return patch


def load_manifest(path: Path) -> dict[str, Any]:
    data = load_json(path)
    if not data.get("extends"):
        return data
    base_path = (SANDBOX_ROOT / raw_text(data["extends"])).resolve()
    if not path_under(base_path, SANDBOX_ROOT):
        raise ValueError(f"extends path escapes sandbox root: {data['extends']}")
    base = load_manifest(base_path)
    patched = deep_merge(base, data.get("patch", {}))
    overlay = {key: value for key, value in data.items() if key not in {"extends", "patch"}}
    return deep_merge(patched, overlay)


def scan_authority_confusion(value: Any, issues: list[Issue], path: str = "$") -> None:
    if isinstance(value, dict):
        for key, field_value in value.items():
            if key in AUTHORITY_BOOL_FIELDS and as_bool(field_value):
                add_once(
                    issues,
                    "US_AUTHORITY_CONFUSION",
                    "use-surface fields cannot assert truth, support, action, promotion, reviewed authority, or mainline readiness.",
                    f"{path}.{key}",
                )
            scan_authority_confusion(field_value, issues, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            scan_authority_confusion(item, issues, f"{path}[{index}]")


def validate_scope(scope: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(scope, dict):
        add_once(issues, "US_MISSING_SCOPE", "scope block is required.")
        return issues
    if not as_bool(scope.get("sandbox_only")):
        add_once(issues, "US_NOT_SANDBOX_ONLY", "use surface pass must stay sandbox-only.")
    for path in scope.get("allowed_write_paths", []):
        if not allowed_write_path_in_slice(path):
            add_once(issues, "US_WRITE_PATH_OUTSIDE_SLICE", "allowed write path must resolve under this sandbox slice.", raw_text(path))
        if protected_target(path):
            add_once(issues, "US_PROTECTED_PATH_TARGET", "allowed write path points at protected territory.", raw_text(path))
    for field in sorted(FORBIDDEN_SCOPE_FIELDS):
        if as_bool(scope.get(field)):
            add_once(issues, "US_RUNTIME_OR_SYNC_FORBIDDEN", "UI/runtime, install, hooks, background services, automation, sync, commit, and push are forbidden.", field)
    return issues


def entry_by_id(entries: Any) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for entry in as_list(entries):
        if isinstance(entry, dict):
            result[raw_text(entry.get("id"))] = entry
    return result


def validate_entries(entries: Any) -> list[Issue]:
    issues: list[Issue] = []
    indexed = entry_by_id(entries)
    if not indexed:
        add_once(issues, "US_ENTRIES_MISSING", "entry surface map is required.")
        return issues

    for entry_id, (backend, boundary) in REQUIRED_ENTRIES.items():
        entry = indexed.get(entry_id)
        if entry is None:
            add_once(issues, "US_REQUIRED_ENTRY_MISSING", "required product entry is missing.", entry_id)
            continue
        if norm(entry.get("backend_artifact")) != backend:
            add_once(issues, "US_ENTRY_BACKEND_MISMATCH", "entry backend artifact does not match contract.", entry_id)
        if norm(entry.get("boundary_label")) != boundary:
            add_once(issues, "US_ENTRY_BOUNDARY_MISSING", "entry boundary label is missing or wrong.", entry_id)
        if as_bool(entry.get("can_approve")):
            add_once(issues, "US_ENTRY_APPROVES_FORBIDDEN", "entry surface cannot approve reviewed knowledge.", entry_id)
        if as_bool(entry.get("can_write_reviewed")) or as_bool(entry.get("reviewed_write_enabled")):
            add_once(issues, "US_ENTRY_REVIEWED_WRITE_FORBIDDEN", "entry surface cannot write reviewed layers.", entry_id)
        if as_bool(entry.get("can_promote")):
            add_once(issues, "US_ENTRY_PROMOTION_FORBIDDEN", "entry surface cannot promote.", entry_id)
        if as_bool(entry.get("creates_action_basis")):
            add_once(issues, "US_ENTRY_ACTION_BASIS_FORBIDDEN", "entry surface cannot create action basis.", entry_id)
        if entry_id in {"ask_vault", "make_context_pack", "prepare_action"} and not as_bool(entry.get("receipt_required")):
            add_once(issues, "US_ENTRY_RECEIPT_MISSING", "entry needs a receipt or trace.", entry_id)
    return issues


def validate_user_questions(questions: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(questions, dict):
        add_once(issues, "US_QUESTIONS_MISSING", "user acceptance questions are required.")
        return issues
    for question_id in REQUIRED_QUESTIONS:
        answer = questions.get(question_id)
        if not isinstance(answer, dict):
            add_once(issues, "US_QUESTION_MISSING", "required user question is missing.", question_id)
            continue
        if not answer.get("surface_ref"):
            add_once(issues, "US_QUESTION_SURFACE_MISSING", "user question needs a surface reference.", question_id)
        if as_bool(answer.get("creates_authority")):
            add_once(issues, "US_QUESTION_CREATES_AUTHORITY", "answering a user question cannot create authority.", question_id)
    return issues


def validate_status_surfaces(status_surfaces: Any) -> list[Issue]:
    issues: list[Issue] = []
    surfaces = as_list(status_surfaces)
    if not surfaces:
        add_once(issues, "US_STATUS_SURFACE_MISSING", "short status surface is required.")
        return issues
    shown: set[str] = set()
    for surface in surfaces:
        if not isinstance(surface, dict):
            continue
        shown.update(raw_text(item) for item in as_list(surface.get("shows")))
        if as_bool(surface.get("can_approve")):
            add_once(issues, "US_STATUS_CAN_APPROVE", "status surface cannot approve.", raw_text(surface.get("id")))
        if as_bool(surface.get("mutates_truth")):
            add_once(issues, "US_STATUS_MUTATES_TRUTH", "status surface cannot mutate truth.", raw_text(surface.get("id")))
        if as_bool(surface.get("can_promote")):
            add_once(issues, "US_STATUS_PROMOTES_FORBIDDEN", "status surface cannot promote.", raw_text(surface.get("id")))
    missing = REQUIRED_STATUS_FLAGS - shown
    if missing:
        add_once(issues, "US_STATUS_FLAGS_MISSING", "status surface misses required operator states.", ",".join(sorted(missing)))
    return issues


def validate_search_surface(search: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(search, dict):
        add_once(issues, "US_SEARCH_SURFACE_MISSING", "search surface is required.")
        return issues
    if not as_bool(search.get("receipt_backed")):
        add_once(issues, "US_RECEIPT_BACKED_SEARCH_REQUIRED", "search must be receipt-backed.")
    if as_bool(search.get("selected_by_is_support")) or as_bool(search.get("query_hit_is_support")):
        add_once(issues, "US_SELECTED_BY_AS_SUPPORT", "selected_by/query hit is trace metadata, not support.")
    if as_bool(search.get("raw_topk_is_trust")):
        add_once(issues, "US_RAW_TOPK_TRUST", "raw top-k result cannot be trust.")
    required = set(raw_text(item) for item in as_list(search.get("action_mode_requires")))
    for gate in {"context_pack", "support_check", "action_readiness_check"}:
        if gate not in required:
            add_once(issues, "US_ACTION_MODE_GATE_MISSING", "action mode needs context, support, and readiness gates.", gate)
    if as_bool(search.get("context_pack_is_action_basis")):
        add_once(issues, "US_CONTEXT_PACK_AS_ACTION_BASIS", "context pack is not action basis by itself.")
    return issues


def validate_badges(badges: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(badges, dict):
        add_once(issues, "US_BADGES_MISSING", "layer badges are required.")
        return issues
    if not as_bool(badges.get("display_only")):
        add_once(issues, "US_BADGE_DISPLAY_ONLY_REQUIRED", "badges must be display-only.")
    if as_bool(badges.get("badge_can_promote")):
        add_once(issues, "US_BADGE_PROMOTES", "badge cannot promote.")
    layers = set(raw_text(layer) for layer in as_list(badges.get("layers")))
    missing = REQUIRED_BADGES - layers
    if missing:
        add_once(issues, "US_BADGES_MISSING_REQUIRED_LAYER", "badges miss required layers.", ",".join(sorted(missing)))
    return issues


def validate_guardrails(guardrails: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(guardrails, dict):
        add_once(issues, "US_GUARDRAILS_MISSING", "guardrails are required.")
        return issues
    if not as_bool(guardrails.get("dirty_state_visible")) or not as_bool(guardrails.get("dirty_state_blocks_risky_actions")):
        add_once(issues, "US_DIRTY_GUARDRAIL_MISSING", "dirty state must be visible and block risky actions.")
    if as_bool(guardrails.get("dirty_state_judges_knowledge")):
        add_once(issues, "US_DIRTY_STATE_AS_KNOWLEDGE", "dirty state is operator safety, not knowledge quality.")
    if as_bool(guardrails.get("hash_match_is_evidence_support")):
        add_once(issues, "US_HASH_AS_SUPPORT", "hash match is process integrity, not evidence support.")
    if as_bool(guardrails.get("sync_enabled")) and not as_bool(guardrails.get("sync_requires_operation_receipt")):
        add_once(issues, "US_SYNC_WITHOUT_OPERATION_RECEIPT", "sync needs operation receipt in this product surface.")
    if as_bool(guardrails.get("sync_mutates_truth")):
        add_once(issues, "US_SYNC_MUTATES_TRUTH", "sync cannot mutate truth.")
    if as_bool(guardrails.get("mainline_ready")):
        add_once(issues, "US_MAINLINE_READY_FORBIDDEN", "use surface sandbox cannot mark mainline readiness.")
    return issues


def validate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    issues: list[Issue] = []
    if manifest.get("record_kind") != RECORD_KIND:
        add_once(issues, "US_RECORD_KIND_INVALID", "record_kind must be vaks_use_surface_blueprint.")
    issues.extend(validate_scope(manifest.get("scope")))
    issues.extend(validate_entries(manifest.get("entries")))
    issues.extend(validate_user_questions(manifest.get("user_questions")))
    issues.extend(validate_status_surfaces(manifest.get("status_surfaces")))
    issues.extend(validate_search_surface(manifest.get("search_surface")))
    issues.extend(validate_badges(manifest.get("layer_badges")))
    issues.extend(validate_guardrails(manifest.get("guardrails")))
    scan_authority_confusion(manifest, issues)
    return {
        "valid": not issues,
        "issues": [issue.__dict__ for issue in issues],
        "non_claims": {
            "surface_pass_not_reviewed_knowledge": True,
            "surface_pass_not_evidence_support": True,
            "surface_pass_not_action_basis": True,
            "surface_pass_not_mainline_readiness": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a sandbox VAKS use-surface blueprint.")
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    manifest_path = args.manifest.resolve()
    if not path_under(manifest_path, SANDBOX_ROOT):
        raise SystemExit("manifest must be inside this sandbox")
    result = validate_manifest(load_manifest(manifest_path))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
