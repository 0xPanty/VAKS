#!/usr/bin/env python3
"""Sandbox-only P2-18 Bases cockpit prototype validator."""

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
RECORD_KIND = "vaks_bases_cockpit_prototype"

REQUIRED_BASES = {
    "review-candidates.base": {
        "purpose": "review_queue_visibility",
        "boundary": "cannot_approve",
        "columns": {"review_status", "review_object_state", "body_hash", "promotion_target", "missing_evidence", "risk_flags"},
    },
    "context-packs.base": {
        "purpose": "context_action_visibility",
        "boundary": "cannot_infer_ready",
        "columns": {"query_mode", "evidence_sufficiency.state", "action_readiness.state", "warnings", "gaps"},
    },
    "feedback-events.base": {
        "purpose": "feedback_pressure_visibility",
        "boundary": "cannot_mutate_truth",
        "columns": {"event_kind", "target_ref", "project_ref", "review_pressure_effect", "query_run_ref"},
    },
    "operator-cockpit.base": {
        "purpose": "total_operator_cockpit",
        "boundary": "cannot_replace_validators",
        "columns": {"blocked", "stale", "missing_anchor", "hash_mismatch", "action_not_ready"},
    },
}

REQUIRED_OPERATOR_STATES = {"blocked", "stale", "missing_anchor", "hash_mismatch", "action_not_ready", "dirty_state"}
REQUIRED_SOURCE_ARTIFACT_LINKS = {
    "review_candidate",
    "context_pack_manifest",
    "feedback_event",
    "maintenance_manifest",
}

FORBIDDEN_SCOPE_FIELDS = {
    "real_base_file_created",
    "obsidian_base_written",
    "obsidian_sync",
    "obsidian_export",
    "server_started",
    "real_ui_started",
    "dependency_install",
    "mcp_write_tool",
    "background_service",
    "watcher_started",
    "automation_started",
    "hook_enabled",
    "hooks_enabled",
    "commit_or_push",
}

AUTHORITY_BOOL_FIELDS = {
    "can_approve",
    "can_write_reviewed",
    "can_promote",
    "creates_action_basis",
    "creates_evidence_support",
    "mutates_truth",
    "infers_action_ready",
    "replaces_validators",
    "hash_match_is_support",
    "dirty_state_judges_knowledge",
    "activity_count_changes_confidence",
    "navigation_creates_authority",
    "base_row_is_reviewed",
    "filter_result_is_evidence",
    "mainline_ready",
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
        candidates.add(path_norm(resolved.as_posix()))
        try:
            candidates.add(path_norm(resolved.relative_to(WORKSPACE_ROOT).as_posix()))
        except ValueError:
            pass
    protected_files_lower = {name.lower() for name in PROTECTED_FILES}
    for text in candidates:
        trimmed = text.lstrip("./")
        lowered = trimmed.lower()
        if ".codex/" in lowered or lowered.startswith(".codex/"):
            return True
        if lowered.rstrip("/") in PROTECTED_EXACTS:
            return True
        if lowered in protected_files_lower or any(lowered.endswith(f"/{name}") for name in protected_files_lower):
            return True
        if any(lowered.startswith(prefix.lower()) or f"/{prefix.lower()}" in lowered for prefix in PROTECTED_PREFIXES):
            return True
    return False


def allowed_write_path_in_slice(value: Any) -> bool:
    resolved = resolve_manifest_path(value)
    return bool(resolved and path_under(resolved, SANDBOX_ROOT))


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
                add_once(issues, "BC_AUTHORITY_CONFUSION", "cockpit fields cannot assert truth, support, approval, action, promotion, or mainline authority.", f"{path}.{key}")
            scan_authority_confusion(field_value, issues, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            scan_authority_confusion(item, issues, f"{path}[{index}]")


def validate_scope(scope: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(scope, dict):
        add_once(issues, "BC_MISSING_SCOPE", "scope block is required.")
        return issues
    if not as_bool(scope.get("sandbox_only")):
        add_once(issues, "BC_NOT_SANDBOX_ONLY", "cockpit prototype must stay sandbox-only.")
    for path in scope.get("allowed_write_paths", []):
        if not allowed_write_path_in_slice(path):
            add_once(issues, "BC_WRITE_PATH_OUTSIDE_SLICE", "allowed write path must resolve under this sandbox slice.", raw_text(path))
        if protected_target(path):
            add_once(issues, "BC_PROTECTED_PATH_TARGET", "allowed write path points at protected territory.", raw_text(path))
    for field in sorted(FORBIDDEN_SCOPE_FIELDS):
        if as_bool(scope.get(field)):
            add_once(issues, "BC_RUNTIME_OR_SYNC_FORBIDDEN", "real Bases, runtime, install, hooks, automation, sync, commit, and push are forbidden.", field)
    return issues


def bases_by_name(bases: Any) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for base in as_list(bases):
        if isinstance(base, dict):
            result[raw_text(base.get("name"))] = base
    return result


def validate_bases(bases: Any) -> list[Issue]:
    issues: list[Issue] = []
    indexed = bases_by_name(bases)
    if not indexed:
        add_once(issues, "BC_BASES_MISSING", "bases list is required.")
        return issues
    for name, spec in REQUIRED_BASES.items():
        base = indexed.get(name)
        if base is None:
            add_once(issues, "BC_REQUIRED_BASE_MISSING", "required cockpit base is missing.", name)
            continue
        if norm(base.get("purpose")) != spec["purpose"]:
            add_once(issues, "BC_BASE_PURPOSE_MISMATCH", "base purpose does not match contract.", name)
        if norm(base.get("boundary")) != spec["boundary"]:
            add_once(issues, "BC_BASE_BOUNDARY_MISMATCH", "base boundary does not match contract.", name)
        columns = {raw_text(column) for column in as_list(base.get("columns"))}
        missing = spec["columns"] - columns
        if missing:
            add_once(issues, "BC_BASE_KEY_COLUMNS_MISSING", "base is missing required columns.", f"{name}:{','.join(sorted(missing))}")
        if not as_bool(base.get("display_only")):
            add_once(issues, "BC_BASE_NOT_DISPLAY_ONLY", "cockpit bases must be display-only.", name)
        if as_bool(base.get("can_approve")):
            add_once(issues, "BC_BASE_APPROVES_FORBIDDEN", "cockpit base cannot approve.", name)
        if as_bool(base.get("can_write_reviewed")):
            add_once(issues, "BC_REVIEWED_WRITE_FORBIDDEN", "cockpit base cannot write reviewed layers.", name)
        if as_bool(base.get("can_promote")):
            add_once(issues, "BC_PROMOTION_FORBIDDEN", "cockpit base cannot promote.", name)
        if as_bool(base.get("creates_action_basis")):
            add_once(issues, "BC_ACTION_BASIS_FORBIDDEN", "cockpit base cannot create action basis.", name)
        if as_bool(base.get("infers_action_ready")):
            add_once(issues, "BC_READY_INFERENCE_FORBIDDEN", "cockpit base cannot infer action readiness.", name)
        if as_bool(base.get("mutates_truth")):
            add_once(issues, "BC_TRUTH_MUTATION_FORBIDDEN", "cockpit base cannot mutate truth.", name)
        if as_bool(base.get("replaces_validators")):
            add_once(issues, "BC_REPLACES_VALIDATORS_FORBIDDEN", "cockpit base cannot replace validators.", name)
    return issues


def validate_navigation(navigation: Any) -> list[Issue]:
    issues: list[Issue] = []
    links = as_list(navigation)
    if not links:
        add_once(issues, "BC_NAVIGATION_MISSING", "cockpit navigation links are required.")
        return issues
    targets = {raw_text(link.get("to")) for link in links if isinstance(link, dict)}
    missing = set(REQUIRED_BASES) - targets
    if missing:
        add_once(issues, "BC_NAVIGATION_TARGET_MISSING", "navigation must link required bases.", ",".join(sorted(missing)))
    artifact_targets = {raw_text(link.get("artifact_ref")) for link in links if isinstance(link, dict) and raw_text(link.get("artifact_ref"))}
    missing_artifacts = REQUIRED_SOURCE_ARTIFACT_LINKS - artifact_targets
    if missing_artifacts:
        add_once(issues, "BC_SOURCE_ARTIFACT_LINKS_MISSING", "navigation must link required source artifacts.", ",".join(sorted(missing_artifacts)))
    for link in links:
        if not isinstance(link, dict):
            continue
        if as_bool(link.get("navigation_creates_authority")):
            add_once(issues, "BC_NAVIGATION_AUTHORITY_FORBIDDEN", "navigation cannot create authority.", raw_text(link.get("id")))
        if as_bool(link.get("opens_reviewed_write")):
            add_once(issues, "BC_NAVIGATION_REVIEWED_WRITE_FORBIDDEN", "navigation cannot open reviewed-write paths.", raw_text(link.get("id")))
    return issues


def validate_operator_states(states: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(states, dict):
        add_once(issues, "BC_OPERATOR_STATES_MISSING", "operator states are required.")
        return issues
    shown = {raw_text(item) for item in as_list(states.get("shows"))}
    missing = REQUIRED_OPERATOR_STATES - shown
    if missing:
        add_once(issues, "BC_OPERATOR_STATES_INCOMPLETE", "operator cockpit misses required states.", ",".join(sorted(missing)))
    if as_bool(states.get("dirty_state_judges_knowledge")):
        add_once(issues, "BC_DIRTY_STATE_AS_KNOWLEDGE", "dirty state is operator safety, not knowledge quality.")
    if as_bool(states.get("hash_match_is_support")):
        add_once(issues, "BC_HASH_AS_SUPPORT", "hash match is process integrity, not evidence support.")
    if as_bool(states.get("activity_count_changes_confidence")):
        add_once(issues, "BC_ACTIVITY_AS_CONFIDENCE", "activity count is not truth confidence.")
    if as_bool(states.get("mainline_ready")):
        add_once(issues, "BC_MAINLINE_READY_FORBIDDEN", "cockpit prototype cannot mark mainline readiness.")
    return issues


def validate_non_claims(non_claims: Any) -> list[Issue]:
    issues: list[Issue] = []
    required = {"not_reviewed_knowledge", "not_evidence_support", "not_action_basis", "not_reviewer_approval", "not_mainline_readiness", "not_real_bases"}
    provided = {raw_text(item) for item in as_list(non_claims)}
    missing = required - provided
    if missing:
        add_once(issues, "BC_NON_CLAIMS_MISSING", "required non-claims are missing.", ",".join(sorted(missing)))
    return issues


def validate_prototype_metadata(manifest: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if not (manifest.get("prototype_kind") or manifest.get("prototype_boundary")):
        return issues
    if norm(manifest.get("prototype_kind")) != "copied_json_bases_cockpit_only":
        add_once(issues, "BC_PROTOTYPE_KIND_INVALID", "prototype_kind must identify copied JSON cockpit only.")
    if norm(manifest.get("prototype_boundary")) != "not_real_obsidian_bases":
        add_once(issues, "BC_PROTOTYPE_BOUNDARY_INVALID", "prototype boundary must say this is not real Obsidian Bases.")
    return issues


def validate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    issues: list[Issue] = []
    if manifest.get("record_kind") != RECORD_KIND:
        add_once(issues, "BC_RECORD_KIND_INVALID", "record_kind must be vaks_bases_cockpit_prototype.")
    issues.extend(validate_scope(manifest.get("scope")))
    issues.extend(validate_bases(manifest.get("bases")))
    issues.extend(validate_navigation(manifest.get("navigation")))
    issues.extend(validate_operator_states(manifest.get("operator_states")))
    issues.extend(validate_non_claims(manifest.get("non_claims")))
    issues.extend(validate_prototype_metadata(manifest))
    scan_authority_confusion(manifest, issues)
    return {
        "valid": not issues,
        "issues": [issue.__dict__ for issue in issues],
        "non_claims": {
            "cockpit_pass_not_real_bases": True,
            "cockpit_pass_not_reviewed_knowledge": True,
            "cockpit_pass_not_evidence_support": True,
            "cockpit_pass_not_action_basis": True,
            "cockpit_pass_not_mainline_readiness": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a sandbox VAKS Bases cockpit prototype.")
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
