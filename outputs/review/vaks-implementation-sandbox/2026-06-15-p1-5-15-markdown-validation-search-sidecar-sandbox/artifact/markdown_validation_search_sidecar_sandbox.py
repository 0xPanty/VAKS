#!/usr/bin/env python3
"""
Sandbox-only P1.5-15 markdown validation/search sidecar validator.

This prototype validates synthetic manifests for an mdvs-like Markdown
validation and local search sidecar. It proves the contract shape for
no-update validation, path-scoped frontmatter lint, derived search caches,
bucket-first search results, and strict VAKS authority boundaries.

It is read-only, uses only the Python standard library, does not scan a real
vault, does not build a real search index, and does not write Markdown files.
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

RECORD_KIND = "markdown_validation_search_sidecar_manifest"

KNOWN_BUCKETS = {
    "reviewed",
    "reviewed_support",
    "raw_anchor",
    "source_anchor",
    "stable_anchor",
    "candidate",
    "review_input",
    "project_overlay",
    "feedback",
    "runtime_artifact",
}

ALLOWED_PACK_ROLES = {"orientation", "review_input", "anchor", "support"}
SEARCH_TRACE_CHANNELS = {"semantic", "bm25", "hybrid", "frontmatter_filter", "path_scope", "temporal"}

FORBIDDEN_AUTHORITY_CLAIMS = {
    "support",
    "direct_support",
    "inferential_support",
    "reviewed_support",
    "truth",
    "truth_confidence",
    "review_pass",
    "reviewed_knowledge",
    "reviewed_relation",
    "reviewer_approval",
    "evidence_support",
    "action_basis",
    "ready_action_basis",
    "action_ready",
    "promotion",
    "promotion_ready",
    "mainline_ready",
    "mainline_readiness",
    "schema_governance",
}

CLAIM_FIELDS = {
    "claims",
    "artifact_claims",
    "validation_claims",
    "search_claims",
    "cache_claims",
    "hit_claims",
    "receipt_claims",
}

AUTHORITY_BOOL_FIELDS = {
    "check_pass_claims_review_pass",
    "claims_action_ready",
    "claims_review_pass",
    "valid_frontmatter_claims_support",
    "search_rank_claims_trust",
    "search_score_sets_confidence",
    "hit_claims_support",
    "cache_is_truth_database",
    "config_claims_schema_governance",
    "mdvs_replaces_vaks_validators",
    "source_mutation_allowed",
    "truth_mutation_allowed",
    "action_basis_allowed",
    "reviewed_knowledge_created",
    "evidence_support_created",
    "evidence_supported",
    "is_support",
    "is_truth",
    "review_passed",
    "supports_action",
    "promotion_ready",
    "mainline_ready",
    "creates_action_basis",
    "creates_reviewed_knowledge",
}

FORBIDDEN_FRONTMATTER_FIELDS = FORBIDDEN_AUTHORITY_CLAIMS.union(AUTHORITY_BOOL_FIELDS)

RUNTIME_FORBIDDEN_BOOL_FIELDS = {
    "dependency_install_requested": "MS_DEPENDENCY_INSTALL_FORBIDDEN",
    "installed_dependency": "MS_DEPENDENCY_INSTALL_FORBIDDEN",
    "real_runtime_started": "MS_REAL_RUNTIME_FORBIDDEN",
    "executes_mdvs_binary": "MS_REAL_RUNTIME_FORBIDDEN",
    "background_service": "MS_BACKGROUND_INDEXER_FORBIDDEN",
    "background_indexer_enabled": "MS_BACKGROUND_INDEXER_FORBIDDEN",
    "watch_mode_enabled": "MS_BACKGROUND_INDEXER_FORBIDDEN",
    "hooks_enabled": "MS_BACKGROUND_INDEXER_FORBIDDEN",
    "mcp_write_tool_exposed": "MS_MCP_WRITE_TOOL_FORBIDDEN",
    "write_tool_enabled": "MS_MCP_WRITE_TOOL_FORBIDDEN",
}

PROTECTED_TARGET_PREFIXES = {
    "h:/obsidian/",
    "h:\\obsidian\\",
    "wiki/claims/",
    "wiki/patterns/",
    "wiki/decisions/",
    "templates/",
    "tools/",
}

PROTECTED_TARGET_EXACTS = {
    "h:/obsidian",
    "wiki/claims",
    "wiki/patterns",
    "wiki/decisions",
    "templates",
    "tools",
}

PROTECTED_TARGET_FILES = {
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


def path_norm(value: Any) -> str:
    return str(value or "").strip().replace("\\", "/").lower()


def raw_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


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
    return str(value).strip() != ""


def add_once(issues: list[Issue], code: str, message: str, item_id: str = "") -> None:
    key = (code, item_id)
    if key not in {(issue.code, issue.item_id) for issue in issues}:
        issues.append(Issue(code, message, item_id))


def item_id(item: dict[str, Any]) -> str:
    return raw_text(item.get("id")) or raw_text(item.get("ref")) or raw_text(item.get("path")) or "<unknown>"


def sha256_like(value: Any) -> bool:
    text = raw_text(value).lower()
    return text.startswith("sha256:") and len(text.split("sha256:", 1)[1]) >= 16


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


def load_manifest(path: Path) -> dict[str, Any]:
    path = path.resolve()
    root = SANDBOX_ROOT
    data = load_json(path)
    if not has_value(data.get("extends")):
        return data

    base_path = (root / raw_text(data["extends"])).resolve()
    if root.resolve() not in base_path.parents and base_path != root.resolve():
        raise ValueError(f"extends path escapes sandbox root: {data['extends']}")

    base = load_manifest(base_path)
    patched = deep_merge(base, data.get("patch", {}))
    overlay = {key: value for key, value in data.items() if key not in {"extends", "patch"}}
    return deep_merge(patched, overlay)


def collect_claims(item: dict[str, Any]) -> set[str]:
    claims: set[str] = set()
    for field in CLAIM_FIELDS:
        claims.update(as_list(item.get(field)))
    return claims


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
        if trimmed.rstrip("/") in PROTECTED_TARGET_EXACTS:
            return True
        if trimmed in PROTECTED_TARGET_FILES or any(trimmed.endswith(f"/{name}") for name in PROTECTED_TARGET_FILES):
            return True
        if any(trimmed.startswith(prefix) or f"/{prefix}" in trimmed for prefix in PROTECTED_TARGET_PREFIXES):
            return True
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


def path_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def validate_sandbox_fixture_path(issues: list[Issue], value: Any, item: str, *, require_fixtures: bool = True) -> None:
    if not has_value(value):
        return
    if protected_target(value):
        add_once(issues, "MS_PROTECTED_PATH_TARGET", "path points at protected territory.", item)

    resolved = resolve_manifest_path(value)
    if resolved is None or not path_under(resolved, SANDBOX_ROOT):
        add_once(issues, "MS_PATH_OUTSIDE_SANDBOX", "path must stay inside this sandbox directory.", item)
        return

    if require_fixtures and not path_under(resolved, SANDBOX_ROOT / "fixtures"):
        add_once(issues, "MS_PATH_OUTSIDE_FIXTURES", "path must point to copied fixture or derived-cache fixture territory.", item)


def validate_existing_fixture_file(issues: list[Issue], value: Any, item: str) -> None:
    validate_sandbox_fixture_path(issues, value, item, require_fixtures=True)
    resolved = resolve_manifest_path(value)
    if resolved is None or not path_under(resolved, SANDBOX_ROOT):
        return
    if not resolved.is_file():
        add_once(issues, "MS_FIXTURE_PATH_MISSING", "referenced copied fixture file is missing.", item)
        return
    try:
        with resolved.open("r", encoding="utf-8") as handle:
            handle.read(1)
    except OSError:
        add_once(issues, "MS_FIXTURE_PATH_UNREADABLE", "referenced copied fixture file is not readable.", item)


def scan_authority_confusion(value: Any, issues: list[Issue], path: str = "$") -> None:
    if isinstance(value, dict):
        claims = collect_claims(value)
        if claims.intersection(FORBIDDEN_AUTHORITY_CLAIMS):
            add_once(
                issues,
                "MS_AUTHORITY_CLAIM_FORBIDDEN",
                "markdown validation/search sidecar artifacts cannot claim support, truth, review, action, promotion, or schema authority.",
                path,
            )

        for key, field_value in value.items():
            field_name = norm(key)
            if field_name in FORBIDDEN_AUTHORITY_CLAIMS and (
                as_bool(field_value) or (not isinstance(field_value, bool) and has_value(field_value))
            ):
                add_once(
                    issues,
                    "MS_AUTHORITY_CLAIM_FORBIDDEN",
                    "direct authority fields are forbidden in markdown sidecar artifacts.",
                    f"{path}.{key}",
                )
            if field_name in AUTHORITY_BOOL_FIELDS and as_bool(field_value):
                add_once(
                    issues,
                    "MS_AUTHORITY_CONFUSION",
                    "sidecar fields cannot assert support, truth mutation, action basis, promotion, or mainline readiness.",
                    f"{path}.{key}",
                )
            scan_authority_confusion(field_value, issues, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            scan_authority_confusion(item, issues, f"{path}[{index}]")


def validate_scope(scope: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(scope, dict):
        add_once(issues, "MS_MISSING_SCOPE", "scope block is required.")
        return issues

    if not as_bool(scope.get("sandbox_fixture_only")):
        add_once(issues, "MS_REAL_VAULT_SCAN_FORBIDDEN", "this sandbox must use copied fixtures only.")

    if as_bool(scope.get("real_vault_scan")) or as_bool(scope.get("reads_obsidian_vault")):
        add_once(issues, "MS_REAL_VAULT_SCAN_FORBIDDEN", "real vault scans are forbidden in this sandbox.")

    if as_bool(scope.get("writes_source_files")) or as_bool(scope.get("source_mutation_allowed")):
        add_once(issues, "MS_SOURCE_MUTATION_FORBIDDEN", "markdown validation/search sidecar must not mutate source files.")

    paths = scope.get("input_paths", [])
    if not isinstance(paths, list) or not paths:
        add_once(issues, "MS_INPUT_PATHS_MISSING", "scope.input_paths must list copied fixture paths.")
    else:
        for path in paths:
            validate_existing_fixture_file(issues, path, raw_text(path))

    return issues


def validate_runtime(runtime: Any) -> list[Issue]:
    issues: list[Issue] = []
    if runtime in ({}, None):
        return issues
    if not isinstance(runtime, dict):
        add_once(issues, "MS_RUNTIME_SHAPE_INVALID", "runtime block must be an object when present.")
        return issues

    for field, code in RUNTIME_FORBIDDEN_BOOL_FIELDS.items():
        if as_bool(runtime.get(field)):
            messages = {
                "MS_DEPENDENCY_INSTALL_FORBIDDEN": "dependency installation is forbidden for this sandbox.",
                "MS_REAL_RUNTIME_FORBIDDEN": "real mdvs/runtime execution is forbidden for this sandbox.",
                "MS_BACKGROUND_INDEXER_FORBIDDEN": "background indexers, watch mode, services, and hooks are forbidden.",
                "MS_MCP_WRITE_TOOL_FORBIDDEN": "MCP write tools are forbidden for this sandbox.",
            }
            add_once(issues, code, messages[code], field)

    return issues


def validate_validation(validation: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(validation, dict):
        add_once(issues, "MS_MISSING_VALIDATION", "validation block is required.")
        return issues

    if norm(validation.get("mode")) != "check":
        add_once(issues, "MS_VALIDATION_MODE_INVALID", "validation.mode must be check.")

    if not as_bool(validation.get("no_update")) or as_bool(validation.get("auto_update")):
        add_once(issues, "MS_NO_UPDATE_REQUIRED", "validation must run no-update and must not auto-update files.")

    if norm(validation.get("output_format")) != "json" or not as_bool(validation.get("deterministic_output")):
        add_once(issues, "MS_DETERMINISTIC_JSON_REQUIRED", "validation must emit deterministic JSON output.")

    path_scopes = validation.get("path_scopes", [])
    if not isinstance(path_scopes, list) or not path_scopes:
        add_once(issues, "MS_PATH_SCOPES_MISSING", "path-scoped field contracts are required.")
    else:
        for scope in path_scopes:
            if not isinstance(scope, dict):
                add_once(issues, "MS_PATH_SCOPES_MISSING", "path scope must be an object.")
                continue
            current_id = item_id(scope)
            if not has_value(scope.get("glob")):
                add_once(issues, "MS_PATH_SCOPES_MISSING", "path scope needs glob.", current_id)
            if not has_value(scope.get("allowed_fields")) or not has_value(scope.get("required_fields")):
                add_once(issues, "MS_PATH_SCOPES_MISSING", "path scope needs allowed_fields and required_fields.", current_id)
            if as_bool(scope.get("unknown_enum_allowed")):
                add_once(issues, "MS_ENUM_DRIFT_ALLOWED", "unknown enum values must fail closed.", current_id)
            if as_bool(scope.get("forbidden_fields_allowed")):
                add_once(issues, "MS_FORBIDDEN_FRONTMATTER_ALLOWED", "forbidden authority/proxy fields must not be allowed.", current_id)
            fields = set(as_list(scope.get("allowed_fields"))).union(as_list(scope.get("required_fields")))
            forbidden_fields = sorted(fields.intersection(FORBIDDEN_FRONTMATTER_FIELDS))
            if forbidden_fields:
                add_once(
                    issues,
                    "MS_FORBIDDEN_FRONTMATTER_ALLOWED",
                    f"path scope includes forbidden authority frontmatter fields: {forbidden_fields}.",
                    current_id,
                )

    if as_bool(validation.get("check_pass_claims_review_pass")):
        add_once(issues, "MS_CHECK_PASS_AS_REVIEW_PASS", "mdvs check pass is not review pass.")

    if as_bool(validation.get("valid_frontmatter_claims_support")):
        add_once(issues, "MS_FRONTMATTER_AS_SUPPORT", "valid frontmatter is not evidence support.")

    return issues


def validate_config(config: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(config, dict):
        add_once(issues, "MS_MISSING_CONFIG", "sidecar config block is required.")
        return issues

    if not has_value(config.get("contract_path")):
        add_once(issues, "MS_CONFIG_CONTRACT_MISSING", "visible config contract path is required.")

    if as_bool(config.get("inferred_from_vault")) and not as_bool(config.get("manual_review_required")):
        add_once(issues, "MS_INFERRED_CONFIG_REVIEW_REQUIRED", "inferred config requires manual review.")

    if as_bool(config.get("config_claims_schema_governance")) or as_bool(config.get("schema_governance")):
        add_once(issues, "MS_CONFIG_SCHEMA_GOVERNANCE_FORBIDDEN", "mdvs config cannot become VAKS schema governance.")

    if has_value(config.get("contract_path")):
        validate_existing_fixture_file(issues, config.get("contract_path"), "config_contract.contract_path")

    return issues


def validate_cache(cache: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(cache, dict):
        add_once(issues, "MS_MISSING_CACHE", "search cache block is required.")
        return issues

    if norm(cache.get("status")) != "derived_cache" or not as_bool(cache.get("rebuildable")):
        add_once(issues, "MS_CACHE_NOT_DERIVED", "search index/cache must be derived and rebuildable.")

    if as_bool(cache.get("committed")) or as_bool(cache.get("cache_is_truth_database")):
        add_once(issues, "MS_CACHE_COMMITTED_AS_TRUTH", ".mdvs/search cache cannot be committed truth database.")

    if not has_value(cache.get("cache_path")):
        add_once(issues, "MS_CACHE_MANIFEST_INCOMPLETE", "cache_path is required.")
    else:
        symbolic_cache_path = as_bool(cache.get("cache_path_symbolic")) or norm(cache.get("cache_path_kind")) == "symbolic_derived_cache"
        if symbolic_cache_path:
            cache_path = raw_text(cache.get("cache_path"))
            if not cache_path.startswith("symbolic:"):
                add_once(issues, "MS_CACHE_SYMBOLIC_PATH_INVALID", "symbolic cache_path must use the symbolic: prefix.")
            if any(marker in path_norm(cache_path) for marker in ["h:/obsidian", "wiki/claims", "wiki/patterns", "wiki/decisions", "templates/", "tools/"]):
                add_once(issues, "MS_PROTECTED_PATH_TARGET", "symbolic cache path points at protected territory.")
        else:
            validate_sandbox_fixture_path(issues, cache.get("cache_path"), "search_cache.cache_path", require_fixtures=True)

    if not has_value(cache.get("cache_manifest_path")):
        add_once(issues, "MS_CACHE_MANIFEST_INCOMPLETE", "cache_manifest_path is required for symbolic or physical cache fixtures.")
    else:
        validate_existing_fixture_file(issues, cache.get("cache_manifest_path"), "search_cache.cache_manifest_path")

    required_manifest = {"source_state_hash", "indexer_id", "indexer_version", "model_id", "rebuild_boundary"}
    missing = sorted(field for field in required_manifest if not has_value(cache.get(field)))
    if missing:
        add_once(issues, "MS_CACHE_MANIFEST_INCOMPLETE", f"cache manifest missing fields: {missing}.")

    if has_value(cache.get("source_state_hash")) and not sha256_like(cache.get("source_state_hash")):
        add_once(issues, "MS_CACHE_MANIFEST_INCOMPLETE", "source_state_hash must be sha256-like.")

    mismatch = as_bool(cache.get("stale")) or as_bool(cache.get("source_hash_mismatch")) or as_bool(cache.get("model_mismatch"))
    if mismatch and as_bool(cache.get("used_for_query")) and not as_bool(cache.get("rebuild_required")):
        add_once(issues, "MS_CACHE_MISMATCH_USED", "stale/mismatched search cache cannot be used silently.")

    return issues


def validate_search(search: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(search, dict):
        add_once(issues, "MS_MISSING_SEARCH", "search block is required.")
        return issues

    modes = set(as_list(search.get("modes")))
    if "hybrid" not in modes or not {"semantic", "bm25"}.issubset(modes):
        add_once(issues, "MS_SEARCH_MODES_INCOMPLETE", "sidecar search must declare semantic, BM25, and hybrid modes.")

    if not as_bool(search.get("bucket_filter_first")):
        add_once(issues, "MS_BUCKET_FILTER_NOT_FIRST", "search must filter authority buckets before rank fusion.")

    if as_bool(search.get("cross_bucket_fusion")):
        add_once(issues, "MS_CROSS_BUCKET_FUSION", "search sidecar cannot fuse across authority buckets.")

    included = set(as_list(search.get("included_buckets")))
    excluded = set(as_list(search.get("excluded_buckets")))
    if not included or not excluded:
        add_once(issues, "MS_BUCKETS_MISSING", "search receipt must list included and excluded buckets.")

    unknown = included.union(excluded).difference(KNOWN_BUCKETS)
    if unknown:
        add_once(issues, "MS_UNKNOWN_BUCKET", f"unknown authority buckets: {sorted(unknown)}.")

    if as_bool(search.get("rank_claims_trust")) or as_bool(search.get("score_sets_confidence")):
        add_once(issues, "MS_SEARCH_RANK_AS_TRUST", "search rank/score cannot become trust or confidence.")

    hits = search.get("hits", [])
    if not isinstance(hits, list) or not hits:
        add_once(issues, "MS_SEARCH_HITS_MISSING", "search.hits must contain labeled hit objects.")
        return issues

    for hit in hits:
        if not isinstance(hit, dict):
            add_once(issues, "MS_INVALID_SEARCH_HIT", "search hit must be an object.")
            continue
        current_id = item_id(hit)
        bucket = norm(hit.get("authority_bucket"))
        role = norm(hit.get("pack_role"))
        selected_by = set(as_list(hit.get("selected_by")))

        if bucket not in KNOWN_BUCKETS:
            add_once(issues, "MS_UNKNOWN_BUCKET", "search hit authority_bucket is unknown.", current_id)

        if not has_value(hit.get("ref")):
            add_once(issues, "MS_HIT_REF_MISSING", "search hit needs a fixture ref.", current_id)
        else:
            validate_existing_fixture_file(issues, hit.get("ref"), current_id)

        if bucket in excluded or (included and bucket not in included):
            add_once(issues, "MS_HIT_BUCKET_OUT_OF_SCOPE", "search hit bucket must be included and must not be excluded.", current_id)

        if role not in ALLOWED_PACK_ROLES:
            add_once(issues, "MS_HIT_ROLE_MISSING", "search hit pack_role is missing or unknown.", current_id)

        if not selected_by or selected_by.difference(SEARCH_TRACE_CHANNELS):
            add_once(issues, "MS_SELECTED_BY_MISSING", "search hit needs selected_by trace channels.", current_id)

        if as_bool(hit.get("rank_claims_trust")) or as_bool(hit.get("score_sets_confidence")):
            add_once(issues, "MS_SEARCH_RANK_AS_TRUST", "hit rank/score cannot become trust or confidence.", current_id)

        if as_bool(hit.get("action_basis_allowed")):
            add_once(issues, "MS_ACTION_BASIS_FORBIDDEN", "search hit cannot allow action basis.", current_id)

        if role == "support" and bucket != "reviewed_support":
            add_once(issues, "MS_SEARCH_HIT_AS_SUPPORT", "non-reviewed search hit cannot be support.", current_id)

    return issues


def validate_vaks(validators: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(validators, dict):
        add_once(issues, "MS_MISSING_VAKS_VALIDATORS", "vaks_validators block is required.")
        return issues

    if not as_bool(validators.get("run_separately")) or as_bool(validators.get("replaced_by_sidecar")):
        add_once(issues, "MS_REPLACES_VAKS_VALIDATORS", "markdown sidecar cannot replace VAKS validators.")

    return issues


def validate_boundary(boundary: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(boundary, dict):
        add_once(issues, "MS_MISSING_BOUNDARY", "boundary block is required.")
        return issues

    if as_bool(boundary.get("source_mutation_allowed")):
        add_once(issues, "MS_SOURCE_MUTATION_FORBIDDEN", "sidecar cannot mutate Markdown source.")

    if as_bool(boundary.get("truth_mutation_allowed")):
        add_once(issues, "MS_TRUTH_MUTATION_FORBIDDEN", "sidecar cannot mutate truth.")

    if as_bool(boundary.get("action_basis_allowed")):
        add_once(issues, "MS_ACTION_BASIS_FORBIDDEN", "sidecar cannot create action basis.")

    if as_bool(boundary.get("promotion_ready")) or as_bool(boundary.get("mainline_ready")):
        add_once(issues, "MS_AUTHORITY_CONFUSION", "sidecar cannot create promotion or mainline readiness.")

    return issues


def validate_manifest(manifest: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if norm(manifest.get("record_kind")) != RECORD_KIND:
        add_once(issues, "MS_INVALID_RECORD_KIND", f"record_kind must be {RECORD_KIND}.")
    if not has_value(manifest.get("scenario_id")):
        add_once(issues, "MS_MISSING_SCENARIO_ID", "scenario_id is required.")

    scan_authority_confusion(manifest, issues)
    issues.extend(validate_scope(manifest.get("scope")))
    issues.extend(validate_runtime(manifest.get("runtime", {})))
    issues.extend(validate_validation(manifest.get("validation")))
    issues.extend(validate_config(manifest.get("config_contract")))
    issues.extend(validate_cache(manifest.get("search_cache")))
    issues.extend(validate_search(manifest.get("search")))
    issues.extend(validate_vaks(manifest.get("vaks_validators")))
    issues.extend(validate_boundary(manifest.get("boundary")))
    return issues


def summarize(manifest: dict[str, Any], issues: list[Issue]) -> dict[str, Any]:
    return {
        "scenario_id": manifest.get("scenario_id", "<missing>"),
        "valid": not issues,
        "issue_codes": sorted({issue.code for issue in issues}),
        "issues": [issue.as_dict() for issue in issues],
        "non_claims": {
            "sidecar_pass_not_reviewed_knowledge": True,
            "sidecar_pass_not_evidence_support": True,
            "sidecar_pass_not_action_basis": True,
            "search_hit_not_support": True,
            "cache_not_truth_database": True,
            "config_not_schema_governance": True,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="path to a markdown validation/search manifest JSON file")
    args = parser.parse_args(argv)
    manifest = load_manifest(args.manifest)
    issues = validate_manifest(manifest)
    print(json.dumps(summarize(manifest, issues), indent=2, sort_keys=True))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
