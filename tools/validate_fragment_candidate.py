#!/usr/bin/env python
"""Validate VAKS fragment_candidate Markdown records."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from yaml.nodes import MappingNode, ScalarNode, SequenceNode


SCHEMA = "urn:vaks:schema:fragment-candidate:v1"
UUID_RE = re.compile(r"^urn:uuid:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

FRAGMENT_KINDS = {
    "idea",
    "claim_like",
    "quote_like",
    "question",
    "pattern_hint",
    "risk_hint",
    "task_hint",
    "term",
}
LANGUAGES = {"zh", "en", "unknown"}
QUOTE_EXACTNESS = {"not_applicable", "unverified"}
PROVENANCE_STATUS = {"self_authored", "memory_trace", "source_hint_only", "source_unknown"}
HINT_CONFIDENCE = {"none", "low", "medium"}
SOURCE_RECOVERY_STATUS = {"not_attempted", "needed", "failed", "found"}
FRAGMENT_STATES = {"inbox", "source_recovery_needed", "parked", "merged", "discarded"}
MERGE_KINDS = {"source_card", "source_annotation", "candidate_distillation"}

FORBIDDEN_KEYS = {
    "action",
    "source_id",
    "source_snapshot_id",
    "source_snapshot_ref",
    "capture_id",
    "annotation_id",
    "annotation_target",
    "authority",
    "citation",
    "claim_support",
    "evidence",
    "source_anchor",
    "source_anchor_ref",
    "source",
    "source_ref",
    "source_refs",
    "source_anchor_refs",
    "source_card_ref",
    "source_capture_ref",
    "source_locator",
    "source_url",
    "capture_ref",
    "annotation_ref",
    "evidence_ref",
    "evidence_packet_ref",
    "evidence_support_ref",
    "evidence_items",
    "itemReviewed",
    "review",
    "review_ref",
    "review_status",
    "reviewed_knowledge_ref",
    "support",
    "target",
    "truth_confidence",
    "action_ref",
    "action_basis_ref",
    "action_readiness",
    "evidence_support_status",
    "action_basis_allowed",
    "evidence_support_allowed",
    "reviewed_knowledge_allowed",
    "pack_content_allowed",
    "action_basis_status",
    "reviewed_knowledge_status",
    "recovered_source_ref",
    "merged_into",
}
ALLOWED_FORBIDDEN_KEY_PATHS = {
    "state.merged_into",
    "state.merged_into.ref",
    "provenance.source_recovery.recovered_source_ref",
    "retrieval_policy.action_basis_allowed",
    "usage_policy.pack_content_allowed",
    "usage_policy.action_basis_allowed",
    "usage_policy.evidence_support_allowed",
    "usage_policy.reviewed_knowledge_allowed",
}

FRAGMENT_FIELDS = {"kind", "language", "content_digest", "quote_exactness", "literal_quote_allowed"}
PROVENANCE_FIELDS = {"status", "source_hint", "source_recovery"}
SOURCE_HINT_FIELDS = {
    "hint_text",
    "possible_title",
    "possible_author",
    "possible_url",
    "possible_platform",
    "possible_timeframe",
    "hint_confidence",
}
SOURCE_RECOVERY_FIELDS = {"status", "recovered_source_ref", "attempts"}
SOURCE_RECOVERY_ATTEMPT_FIELDS = {"method", "query", "outcome", "result_ref"}
RETRIEVAL_POLICY_FIELDS = {"policy_kind", "pack_allowed", "action_basis_allowed", "warning_code"}
USAGE_POLICY_FIELDS = {
    "pack_content_allowed",
    "pack_pointer_allowed",
    "action_basis_allowed",
    "evidence_support_allowed",
    "reviewed_knowledge_allowed",
}
STATE_FIELDS = {"fragment_state", "merged_into", "discarded_reason"}
MERGED_INTO_FIELDS = {"kind", "ref"}


def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def extract_frontmatter_and_body(path: Path) -> tuple[str, str]:
    text = normalize_lf(path.read_text(encoding="utf-8"))
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("unterminated YAML frontmatter")
    body_start = end + len("\n---")
    if body_start < len(text) and text[body_start] == "\n":
        body_start += 1
    return text[4:end], text[body_start:]


def reject_duplicate_yaml_keys(raw: str) -> list[str]:
    try:
        root = yaml.compose(raw)
    except yaml.YAMLError as exc:
        return [f"invalid YAML: {exc}"]
    duplicates: list[str] = []

    def walk(node: Any, prefix: str = "") -> None:
        if isinstance(node, MappingNode):
            seen: set[str] = set()
            for key_node, value_node in node.value:
                key = str(key_node.value) if isinstance(key_node, ScalarNode) else str(key_node)
                field = f"{prefix}.{key}" if prefix else key
                if key in seen:
                    duplicates.append(field)
                seen.add(key)
                walk(value_node, field)
            return
        if isinstance(node, SequenceNode):
            for idx, child in enumerate(node.value):
                walk(child, f"{prefix}[{idx}]" if prefix else f"[{idx}]")

    if root is not None:
        walk(root)
    return [f"duplicate YAML key: {field}" for field in duplicates]


def parse_frontmatter(raw: str) -> dict[str, Any]:
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def is_blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def issue(path: Path, code: str, field: str, message: str) -> dict[str, str]:
    return {
        "severity": "error",
        "code": code,
        "path": str(path).replace("\\", "/"),
        "field": field,
        "message": message,
    }


def require_mapping(issues: list[dict[str, str]], path: Path, parent: dict[str, Any], field: str) -> dict[str, Any]:
    value = parent.get(field)
    if not isinstance(value, dict):
        issues.append(issue(path, "FIELD_SHAPE_INVALID", field, f"{field} must be a mapping"))
        return {}
    return value


def require_exact_fields(issues: list[dict[str, str]], path: Path, value: dict[str, Any], allowed: set[str], field: str) -> None:
    extra = sorted(set(value) - allowed)
    if extra:
        issues.append(issue(path, "EXTRA_FIELD", field, f"{field} has unsupported fields: {', '.join(extra)}"))


def require_enum(issues: list[dict[str, str]], path: Path, value: Any, allowed: set[str], field: str) -> None:
    if value not in allowed:
        issues.append(issue(path, "ENUM_INVALID", field, f"{field} must be one of: {', '.join(sorted(allowed))}"))


def walk_keys(obj: Any, prefix: str = "") -> list[tuple[str, Any]]:
    result: list[tuple[str, Any]] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            field = f"{prefix}.{key}" if prefix else str(key)
            result.append((field, value))
            result.extend(walk_keys(value, field))
    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            result.extend(walk_keys(value, f"{prefix}[{idx}]"))
    return result


def has_nonempty_hint(source_hint: dict[str, Any]) -> bool:
    for key in ["hint_text", "possible_title", "possible_author", "possible_url", "possible_platform", "possible_timeframe"]:
        if not is_blank(source_hint.get(key)):
            return True
    return False


def validate_data(path: Path, data: dict[str, Any], body: str) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []

    expected_top_level = {
        "schema",
        "record_kind",
        "fragment_id",
        "created_at",
        "created_by",
        "knowledge_status",
        "candidate_class",
        "processing_tier",
        "fragment",
        "provenance",
        "retrieval_policy",
        "usage_policy",
        "state",
        "tags",
    }
    extra = sorted(set(data) - expected_top_level)
    if extra:
        issues.append(issue(path, "EXTRA_FIELD", ",".join(extra), "fragment_candidate frontmatter has unsupported top-level fields"))

    scalar_expectations = {
        "schema": SCHEMA,
        "record_kind": "fragment_candidate",
        "knowledge_status": "candidate",
        "candidate_class": "fragment_only",
        "processing_tier": "light",
    }
    for field, expected in scalar_expectations.items():
        if data.get(field) != expected:
            issues.append(issue(path, "FIELD_VALUE_INVALID", field, f"{field} must be {expected}"))

    if not isinstance(data.get("fragment_id"), str) or not UUID_RE.match(data["fragment_id"]):
        issues.append(issue(path, "FRAGMENT_ID_INVALID", "fragment_id", "fragment_id must be a valid urn:uuid"))
    if is_blank(data.get("created_by")):
        issues.append(issue(path, "CREATED_BY_REQUIRED", "created_by", "created_by is required"))
    try:
        created_at = str(data.get("created_at", "")).replace("Z", "+00:00")
        datetime.fromisoformat(created_at)
    except ValueError:
        issues.append(issue(path, "CREATED_AT_INVALID", "created_at", "created_at must be ISO 8601 datetime"))

    fragment = require_mapping(issues, path, data, "fragment")
    provenance = require_mapping(issues, path, data, "provenance")
    retrieval_policy = require_mapping(issues, path, data, "retrieval_policy")
    usage_policy = require_mapping(issues, path, data, "usage_policy")
    state = require_mapping(issues, path, data, "state")
    require_exact_fields(issues, path, fragment, FRAGMENT_FIELDS, "fragment")
    require_exact_fields(issues, path, provenance, PROVENANCE_FIELDS, "provenance")
    require_exact_fields(issues, path, retrieval_policy, RETRIEVAL_POLICY_FIELDS, "retrieval_policy")
    require_exact_fields(issues, path, usage_policy, USAGE_POLICY_FIELDS, "usage_policy")
    require_exact_fields(issues, path, state, STATE_FIELDS, "state")

    require_enum(issues, path, fragment.get("kind"), FRAGMENT_KINDS, "fragment.kind")
    require_enum(issues, path, fragment.get("language"), LANGUAGES, "fragment.language")
    require_enum(issues, path, fragment.get("quote_exactness"), QUOTE_EXACTNESS, "fragment.quote_exactness")
    if fragment.get("literal_quote_allowed") is not False:
        issues.append(issue(path, "LITERAL_QUOTE_NOT_ALLOWED", "fragment.literal_quote_allowed", "literal_quote_allowed must be false"))
    expected_digest = sha256_text(body)
    if fragment.get("content_digest") != expected_digest:
        issues.append(issue(path, "CONTENT_DIGEST_MISMATCH", "fragment.content_digest", f"content_digest must equal {expected_digest}"))

    require_enum(issues, path, provenance.get("status"), PROVENANCE_STATUS, "provenance.status")
    source_hint = require_mapping(issues, path, provenance, "source_hint")
    source_recovery = require_mapping(issues, path, provenance, "source_recovery")
    require_exact_fields(issues, path, source_hint, SOURCE_HINT_FIELDS, "provenance.source_hint")
    require_exact_fields(issues, path, source_recovery, SOURCE_RECOVERY_FIELDS, "provenance.source_recovery")
    require_enum(issues, path, source_hint.get("hint_confidence"), HINT_CONFIDENCE, "provenance.source_hint.hint_confidence")
    require_enum(issues, path, source_recovery.get("status"), SOURCE_RECOVERY_STATUS, "provenance.source_recovery.status")
    attempts = source_recovery.get("attempts")
    if not isinstance(attempts, list):
        issues.append(issue(path, "SOURCE_RECOVERY_ATTEMPTS_INVALID", "provenance.source_recovery.attempts", "attempts must be a list"))
    else:
        for idx, attempt in enumerate(attempts):
            field = f"provenance.source_recovery.attempts[{idx}]"
            if not isinstance(attempt, dict):
                issues.append(issue(path, "SOURCE_RECOVERY_ATTEMPT_INVALID", field, "attempts items must be objects"))
            else:
                require_exact_fields(issues, path, attempt, SOURCE_RECOVERY_ATTEMPT_FIELDS, field)
    if provenance.get("status") in {"memory_trace", "source_hint_only"} and not has_nonempty_hint(source_hint):
        issues.append(issue(path, "SOURCE_HINT_REQUIRED", "provenance.source_hint", "memory_trace/source_hint_only fragments need at least one non-empty hint"))
    if provenance.get("status") == "source_unknown" and has_nonempty_hint(source_hint):
        issues.append(issue(path, "SOURCE_UNKNOWN_HAS_HINT", "provenance.source_hint", "source_unknown fragments must not carry source hints"))
    if source_recovery.get("status") == "found":
        recovered_ref = source_recovery.get("recovered_source_ref")
        if not isinstance(recovered_ref, str) or recovered_ref.strip() == "":
            issues.append(issue(path, "RECOVERED_SOURCE_REF_TYPE_INVALID", "provenance.source_recovery.recovered_source_ref", "found source recovery needs non-empty string recovered_source_ref"))
    if source_recovery.get("status") != "found" and source_recovery.get("recovered_source_ref") is not None:
        issues.append(issue(path, "RECOVERED_SOURCE_REF_NOT_ALLOWED", "provenance.source_recovery.recovered_source_ref", "recovered_source_ref is allowed only when source_recovery.status is found"))
    if provenance.get("status") == "source_unknown" and source_recovery.get("status") == "found":
        issues.append(issue(path, "SOURCE_UNKNOWN_FOUND_CONFLICT", "provenance.source_recovery.status", "source_unknown fragments cannot also declare found source recovery"))

    expected_retrieval = {
        "policy_kind": "orientation_only",
        "pack_allowed": "activation_only",
        "action_basis_allowed": False,
        "warning_code": "missing_source_provenance",
    }
    for field, expected in expected_retrieval.items():
        if retrieval_policy.get(field) != expected:
            issues.append(issue(path, "RETRIEVAL_POLICY_INVALID", f"retrieval_policy.{field}", f"retrieval_policy.{field} must be {expected}"))
    expected_usage = {
        "pack_content_allowed": False,
        "pack_pointer_allowed": True,
        "action_basis_allowed": False,
        "evidence_support_allowed": False,
        "reviewed_knowledge_allowed": False,
    }
    for field, expected in expected_usage.items():
        if usage_policy.get(field) is not expected:
            issues.append(issue(path, "USAGE_POLICY_INVALID", f"usage_policy.{field}", f"usage_policy.{field} must be {str(expected).lower()}"))

    require_enum(issues, path, state.get("fragment_state"), FRAGMENT_STATES, "state.fragment_state")
    merged_into = state.get("merged_into")
    if state.get("fragment_state") != "merged" and merged_into is not None:
        issues.append(issue(path, "MERGED_TARGET_NOT_ALLOWED", "state.merged_into", "merged_into is allowed only when fragment_state is merged"))
    if state.get("fragment_state") == "merged":
        if not isinstance(merged_into, dict):
            issues.append(issue(path, "MERGED_TARGET_REQUIRED", "state.merged_into", "merged fragments need merged_into"))
        else:
            require_exact_fields(issues, path, merged_into, MERGED_INTO_FIELDS, "state.merged_into")
            require_enum(issues, path, merged_into.get("kind"), MERGE_KINDS, "state.merged_into.kind")
            if not isinstance(merged_into.get("ref"), str) or merged_into.get("ref", "").strip() == "":
                issues.append(issue(path, "MERGED_TARGET_REF_TYPE_INVALID", "state.merged_into.ref", "merged fragments need non-empty string merged_into.ref"))
            if source_recovery.get("status") != "found" and merged_into.get("kind") != "candidate_distillation":
                issues.append(issue(path, "MERGED_SOURCE_RECOVERY_REQUIRED", "provenance.source_recovery.status", "merged source/source-annotation targets require source_recovery.status: found"))
    if source_recovery.get("status") == "found" and state.get("fragment_state") != "merged":
        issues.append(issue(path, "RECOVERED_SOURCE_FOUND_NOT_MERGED", "state.fragment_state", "found source recovery must be represented by fragment_state: merged"))

    if fragment.get("kind") == "quote_like" and source_recovery.get("status") != "found":
        if fragment.get("quote_exactness") != "unverified" or fragment.get("literal_quote_allowed") is not False:
            issues.append(issue(path, "QUOTE_LIKE_UNVERIFIED", "fragment.quote_exactness", "quote_like fragments without recovered source must be unverified and not literal"))

    tags = data.get("tags")
    if not isinstance(tags, list) or "fragment" not in tags:
        issues.append(issue(path, "FRAGMENT_TAG_REQUIRED", "tags", "tags must include fragment"))

    for key_path, _value in walk_keys(data):
        key = key_path.split(".")[-1]
        if key in FORBIDDEN_KEYS and key_path not in ALLOWED_FORBIDDEN_KEY_PATHS:
            issues.append(issue(path, "FORBIDDEN_SOURCE_OR_EVIDENCE_FIELD", key_path, f"{key_path} is not allowed on fragment_candidate"))

    return issues


def validate_file(path: Path) -> list[dict[str, str]]:
    try:
        raw, body = extract_frontmatter_and_body(path)
    except Exception as exc:
        return [issue(path, "FRONTMATTER_INVALID", "frontmatter", str(exc))]
    duplicate_issues = [issue(path, "DUPLICATE_YAML_KEY", "frontmatter", msg) for msg in reject_duplicate_yaml_keys(raw)]
    try:
        data = parse_frontmatter(raw)
    except Exception as exc:
        return duplicate_issues + [issue(path, "FRONTMATTER_INVALID", "frontmatter", str(exc))]
    return duplicate_issues + validate_data(path, data, body)


def collect_targets(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(p for p in path.rglob("*.md") if p.is_file() and p.name.lower() != "readme.md"))
        elif path.is_file():
            files.append(path)
    return sorted(dict.fromkeys(files))


def validate_paths(paths: list[Path]) -> dict[str, Any]:
    files = collect_targets(paths)
    issues: list[dict[str, str]] = []
    for path in files:
        issues.extend(validate_file(path))
    return {
        "schema": "urn:vaks:report:fragment-candidate-validation:v1",
        "files_scanned": len(files),
        "issue_count": len(issues),
        "status": "pass" if not issues else "fail",
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="fragment_candidate Markdown files or directories")
    parser.add_argument("--no-fail", action="store_true", help="emit report but always return zero")
    args = parser.parse_args()

    report = validate_paths([Path(p) for p in args.paths])
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if args.no_fail or report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
