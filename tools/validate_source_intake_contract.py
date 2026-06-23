#!/usr/bin/env python
"""Validate VAKS Source Intake enum and boundary contract.

The validator has two intended uses:
- contract mode: main SOURCE_INTAKE.md + templates must pass.
- current mode: audit current vault/source-intake surfaces and report drift.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

import yaml
from yaml.nodes import MappingNode, ScalarNode, SequenceNode


CONTRACT_FILES = [
    "SOURCE_INTAKE.md",
    "templates/source-record.md",
    "templates/source-annotation.md",
    "templates/video-source.md",
    "templates/candidate-distillation.md",
    "templates/project-overlay.md",
    "templates/query-run.md",
    "templates/feedback-event.md",
    "templates/heavy-review-open.md",
    "templates/context-pack-manifest.md",
]

CURRENT_GLOBS = [
    "SOURCE_INTAKE.md",
    "templates/*.md",
    "raw/**/*.md",
    "outputs/qa/**/*.md",
    "outputs/feedback/**/*.md",
    "outputs/review/*candidate-distillation.md",
    "outputs/review/*refresh.md",
    "outputs/review/*query-run*.md",
    "outputs/review/*context-pack*.md",
    "outputs/review/*feedback*.md",
    "outputs/review/*overlay*.md",
    "outputs/review/source_annotations/**/*.md",
    "outputs/review/project_lens_overlays/*.md",
    "outputs/review/project_overlays/**/*.md",
]

SOURCE_INTAKE_RECORD_KINDS = {
    "source_card",
    "source_annotation",
    "candidate_distillation",
    "project_overlay",
    "overlay_suggestion",
    "feedback_event",
    "heavy_review_open",
    "context_pack_manifest",
    "query_run_trace",
}

TYPE_RECORD_KIND_ALIASES = {
    "source": "source_card",
    "source_record": "source_card",
    "video_source_card": "source_card",
    "source_snapshot_index": "source_card",
    "source_annotation": "source_annotation",
    "candidate_distillation": "candidate_distillation",
    "candidate_distillation_refresh": "candidate_distillation",
    "project_lens_overlay": "project_overlay",
    "project_overlay": "project_overlay",
    "feedback_event": "feedback_event",
    "heavy_review_open": "heavy_review_open",
    "context_pack_manifest": "context_pack_manifest",
    "query_run_trace": "query_run_trace",
}

FORBIDDEN_INTAKE_FIELDS = {
    "truth_score",
    "truth_confidence",
    "confidence_delta",
    "adopted",
    "rejected",
    "must_use",
    "universal_ban",
    "decision_outcome",
    "review_verdict",
    "accepted",
}

UNIVERSAL_BAN_TERMS = [
    "never",
    "always",
    "wrong",
    "universal_ban",
    "under no circumstances",
    "categorically avoid",
    "任何情况下",
    "永远",
    "绝不",
    "一律",
    "完全错误",
]

PROXY_SUPPORT_TERMS = [
    "diagram",
    "source_count",
    "tool_count",
    "project_count",
    "vendor says",
    "benchmark passed",
    "retrieval_score",
    "retrieval score",
    "graph_rank",
    "graph rank",
    "dashboard_hit",
    "dashboard hit",
    "semantic score",
    "lexical rank",
    "vector score",
]

LEGACY_RAW_METADATA_TERMS = [
    "legacy_raw_metadata",
    "legacy raw metadata",
]

MIGRATION_PLACEHOLDER_VALUES = {
    "see_body_or_legacy_record",
    "see_target_layers_or_body",
    "see_non_target_layers_or_body",
    "review_if_project_scope_or_evidence_changes",
    "see_derived_from_or_body",
}

RAW_SOURCE_SAVE_REASON_MARKERS = [
    "## capture reason",
    "## why captured",
    "## why saved",
    "## why this source matters",
    "## 为什么收录",
    "## 为什么保存",
    "## 收录原因",
    "## 捕获原因",
    "## 采集原因",
]

SOURCE_CARD_AUTHORITY_LIKE_FIELDS = {
    "confidence",
    "cross_source_count",
    "relations",
    "source_quality",
    "freshness",
    "relevance",
}

CONFIRMED_OVERLAY_PLACEHOLDER_FIELDS = {
    "target_ref",
    "project_borrow_scope",
    "project_non_borrow_scope",
    "project_reopen_trigger",
}

SOURCE_CARD_HARD_AUTHORITY_FIELDS = {
    "confidence",
    "relations",
}


def extract_frontmatter_text(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    return text[4:end]


def load_registry(root: Path) -> dict[str, Any]:
    path = root / "tools" / "source_intake_enum_registry.json"
    return json.loads(path.read_text(encoding="utf-8"))


def frontmatter(path: Path) -> dict[str, Any] | None:
    raw = extract_frontmatter_text(path)
    if raw is None:
        return None
    data = yaml.safe_load(raw) or {}
    return data if isinstance(data, dict) else {}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def body_text(markdown_text: str) -> str:
    if markdown_text.startswith("---\n"):
        end = markdown_text.find("\n---", 4)
        if end != -1:
            return markdown_text[end + 4 :]
    return markdown_text


def has_raw_source_save_reason(markdown_text: str) -> bool:
    body = body_text(markdown_text)
    lower = body.lower()
    return any(marker in lower or marker in body for marker in RAW_SOURCE_SAVE_REASON_MARKERS)


def line_for_key(path: Path, key: str) -> int:
    try:
        for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            if line.lstrip().startswith(f"{key}:"):
                return i
    except Exception:
        pass
    return 0


def normalize(v: Any) -> Any:
    if isinstance(v, str):
        return v.strip()
    return v


def is_template_placeholder(v: Any) -> bool:
    return isinstance(v, str) and "|" in v


def is_blank(v: Any) -> bool:
    if v is None:
        return True
    if isinstance(v, str):
        return v.strip() == ""
    if isinstance(v, (list, dict)):
        return len(v) == 0
    return False


def is_template_path(path: Path) -> bool:
    return str(path).replace("\\", "/").startswith("templates/")


def add_issue(
    issues: list[dict[str, Any]],
    path: Path,
    severity: str,
    check: str,
    field: str,
    value: Any,
    message: str,
    *,
    line: int | None = None,
    semantic_class: str | None = None,
    recommended_action: str | None = None,
) -> None:
    if semantic_class is None:
        semantic_class = "hard_error_canonical_p0" if severity == "error" else "high_risk_manual_review"
    if recommended_action is None:
        recommended_action = "fix before canonical P0" if severity == "error" else "manual review before canonical P0"
    issues.append(
        {
            "severity": severity,
            "check": check,
            "path": str(path).replace("\\", "/"),
            "line": line if line is not None else line_for_key(path, field.split(".")[-1]),
            "field": field,
            "value": "" if value is None else str(value),
            "message": message,
            "semantic_class": semantic_class,
            "recommended_action": recommended_action,
        }
    )


def duplicate_yaml_keys(raw: str) -> list[tuple[str, int]]:
    try:
        root = yaml.compose(raw)
    except yaml.YAMLError:
        return []
    duplicates: list[tuple[str, int]] = []

    def walk(node: Any, prefix: str = "") -> None:
        if isinstance(node, MappingNode):
            seen: set[str] = set()
            for key_node, value_node in node.value:
                if isinstance(key_node, ScalarNode):
                    key = str(key_node.value)
                else:
                    key = str(key_node)
                field = f"{prefix}.{key}" if prefix else key
                if key in seen:
                    duplicates.append((field, key_node.start_mark.line + 1))
                seen.add(key)
                walk(value_node, field)
            return
        if isinstance(node, SequenceNode):
            for idx, child in enumerate(node.value):
                walk(child, f"{prefix}[{idx}]" if prefix else f"[{idx}]")

    if root is not None:
        walk(root)
    return duplicates


def check_duplicate_yaml_keys(issues: list[dict[str, Any]], path: Path, raw: str) -> None:
    for field, line in duplicate_yaml_keys(raw):
        add_issue(
            issues,
            path,
            "error",
            "duplicate_yaml_key",
            field,
            field,
            "Duplicate YAML keys are not allowed; last-wins parsing can hide boundary fields.",
            line=line,
        )


def get_policy(data: dict[str, Any]) -> dict[str, Any]:
    policy = data.get("retrieval_policy")
    return policy if isinstance(policy, dict) else {}


def is_intake_surface(path: Path, data: dict[str, Any]) -> bool:
    p = str(path).replace("\\", "/")
    if data.get("record_kind") == "runtime_test_artifact":
        return False
    if p == "SOURCE_INTAKE.md":
        return True
    if p.startswith("templates/"):
        return p in CONTRACT_FILES
    record_kind = data.get("record_kind")
    if record_kind in SOURCE_INTAKE_RECORD_KINDS:
        return True
    if data.get("type") in TYPE_RECORD_KIND_ALIASES:
        return True
    if p.startswith("raw/"):
        return True
    if p.startswith("outputs/review/project_lens_overlays/"):
        return True
    if p.startswith("outputs/review/project_overlays/"):
        return True
    if (
        p.endswith("candidate-distillation.md")
        or p.endswith("refresh.md")
        or "query-run" in p
        or "context-pack" in p
        or p.endswith("feedback-event.md")
        or p.endswith("source-annotation.md")
        or p.endswith("-overlay.md")
        or p.startswith("outputs/review/source_annotations/")
    ):
        return True
    return False


def inferred_record_kind(path: Path, data: dict[str, Any]) -> str | None:
    p = str(path).replace("\\", "/")
    if p == "SOURCE_INTAKE.md":
        return None
    if data.get("record_kind") == "overlay_suggestion":
        return "overlay_suggestion"
    if data.get("record_type") == "query-run":
        return "query_run_trace"
    source_type = data.get("type")
    if source_type in TYPE_RECORD_KIND_ALIASES:
        return TYPE_RECORD_KIND_ALIASES[source_type]
    if p.startswith("raw/"):
        return "source_card"
    if p.startswith("outputs/review/source_annotations/") or p.endswith("source-annotation.md"):
        return "source_annotation"
    if p.endswith("candidate-distillation.md") or p.endswith("refresh.md"):
        return "candidate_distillation"
    if "query-run" in p:
        return "query_run_trace"
    if "context-pack" in p:
        return "context_pack_manifest"
    if p.endswith("feedback-event.md") or p.endswith("-feedback.md"):
        return "feedback_event"
    if p.startswith("outputs/review/project_lens_overlays/"):
        return "project_overlay"
    if p.startswith("outputs/review/project_overlays/") or p.endswith("-overlay.md"):
        return "project_overlay"
    return None


def check_enum(
    issues: list[dict[str, Any]],
    registry: dict[str, Any],
    path: Path,
    field: str,
    value: Any,
) -> None:
    if value is None or is_template_placeholder(value):
        return
    allowed = registry["enums"][field]
    if normalize(value) not in allowed:
        add_issue(
            issues,
            path,
            "error",
            "enum_registry",
            field,
            value,
            f"Unknown enum value for {field}; fail closed.",
        )


def check_enum_as(
    issues: list[dict[str, Any]],
    registry: dict[str, Any],
    path: Path,
    enum_field: str,
    issue_field: str,
    value: Any,
) -> None:
    if value is None or is_template_placeholder(value):
        return
    allowed = registry["enums"][enum_field]
    if normalize(value) not in allowed:
        add_issue(
            issues,
            path,
            "error",
            "enum_registry",
            issue_field,
            value,
            f"Unknown enum value for {enum_field}; fail closed.",
        )


def require_field(
    issues: list[dict[str, Any]],
    path: Path,
    data: dict[str, Any],
    field: str,
    *,
    require_value: bool,
) -> None:
    if field not in data:
        add_issue(
            issues,
            path,
            "error",
            "missing_required_field",
            field,
            None,
            f"Missing required field: {field}.",
        )
        return
    if require_value and is_blank(data.get(field)):
        add_issue(
            issues,
            path,
            "error",
            "blank_required_field",
            field,
            data.get(field),
            f"Required field is blank: {field}.",
        )


def require_one_of(
    issues: list[dict[str, Any]],
    path: Path,
    data: dict[str, Any],
    fields: list[str],
    *,
    require_value: bool,
) -> None:
    if any(field in data and (not require_value or not is_blank(data.get(field))) for field in fields):
        return
    add_issue(
        issues,
        path,
        "error",
        "missing_required_field",
        " | ".join(fields),
        None,
        f"One of these fields is required: {', '.join(fields)}.",
    )


def require_list(
    issues: list[dict[str, Any]],
    path: Path,
    data: dict[str, Any],
    field: str,
    *,
    require_value: bool,
) -> None:
    if field not in data:
        add_issue(issues, path, "error", "missing_required_field", field, None, f"Missing required field: {field}.")
        return
    if require_value and is_blank(data.get(field)):
        add_issue(issues, path, "error", "blank_required_field", field, data.get(field), f"Required field is blank: {field}.")
        return
    if data.get(field) is not None and not isinstance(data.get(field), list):
        add_issue(issues, path, "error", "field_shape", field, data.get(field), f"{field} must be a list.")


def require_mapping(
    issues: list[dict[str, Any]],
    path: Path,
    data: dict[str, Any],
    field: str,
    *,
    require_value: bool,
) -> None:
    if field not in data:
        add_issue(issues, path, "error", "missing_required_field", field, None, f"Missing required field: {field}.")
        return
    if require_value and is_blank(data.get(field)):
        add_issue(issues, path, "error", "blank_required_field", field, data.get(field), f"Required field is blank: {field}.")
        return
    if data.get(field) is not None and not isinstance(data.get(field), dict):
        add_issue(issues, path, "error", "field_shape", field, data.get(field), f"{field} must be a mapping.")


def body_has_candidate_points(text: str) -> bool:
    lower = text.lower()
    return (
        "candidate_points:" in lower
        or "## candidate points" in lower
        or "candidate point" in lower
        or "## 候选" in text
        or "候选点" in text
    )


def check_project_local_wording(
    issues: list[dict[str, Any]],
    path: Path,
    value: Any,
) -> None:
    if not isinstance(value, str):
        return
    lower = value.lower()
    if any(term in lower or term in value for term in UNIVERSAL_BAN_TERMS):
        add_issue(
            issues,
            path,
            "error",
            "universal_ban_wording",
            "project_non_borrow_scope",
            value,
            "Project non-borrow scope must use project-local wording, not universal ban language.",
        )


def check_placeholder_values(
    issues: list[dict[str, Any]],
    path: Path,
    value: Any,
    prefix: str = "",
    root: dict[str, Any] | None = None,
    document_text: str = "",
) -> None:
    if root is None and isinstance(value, dict):
        root = value
    if isinstance(value, dict):
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            check_placeholder_values(issues, path, child, child_prefix, root, document_text)
        return
    if isinstance(value, list):
        for idx, child in enumerate(value):
            check_placeholder_values(issues, path, child, f"{prefix}[{idx}]", root, document_text)
        return
    if isinstance(value, str) and value in MIGRATION_PLACEHOLDER_VALUES:
        is_confirmed_overlay_placeholder = (
            isinstance(root, dict)
            and root.get("record_kind") == "project_overlay"
            and root.get("overlay_state") == "confirmed"
            and prefix in CONFIRMED_OVERLAY_PLACEHOLDER_FIELDS
        )
        is_raw_source_why_saved_placeholder = (
            isinstance(root, dict)
            and root.get("record_kind") == "source_card"
            and root.get("knowledge_status") == "raw"
            and prefix == "why_saved"
        )
        raw_source_has_body_reason = is_raw_source_why_saved_placeholder and has_raw_source_save_reason(document_text)
        check_name = "migration_placeholder_value"
        message = "Migration placeholder satisfies field presence only; semantic adequacy still needs review."
        semantic_class = "high_risk_manual_review"
        recommended_action = "manual semantic review before canonical P0"
        if is_confirmed_overlay_placeholder:
            check_name = "confirmed_overlay_placeholder_value"
            message = "Confirmed Project Overlay placeholder does not satisfy semantic adequacy."
            semantic_class = "hard_error_canonical_p0"
            recommended_action = "replace confirmed-overlay target/borrow/non-borrow/reopen placeholder with project-local semantic content or exclude from canonical overlay scope"
        elif is_raw_source_why_saved_placeholder and raw_source_has_body_reason:
            semantic_class = "migration_debt_defer_ok"
            recommended_action = "keep as migration debt only while raw/orientation and body contains a real capture/save reason; require drilldown before pack/support"
        elif is_raw_source_why_saved_placeholder:
            check_name = "source_why_saved_placeholder_without_body_reason"
            message = "Raw source why_saved placeholder is only defer-ok when the body contains a real capture/save reason."
            semantic_class = "high_risk_manual_review"
            recommended_action = "fill why_saved or add a real Why Captured/为什么收录 body section before treating this as accepted migration debt"
        add_issue(
            issues,
            path,
            "error" if is_confirmed_overlay_placeholder else "warning",
            check_name,
            prefix,
            value,
            message,
            semantic_class=semantic_class,
            recommended_action=recommended_action,
        )


def check_source_card_authority_like_metadata(
    issues: list[dict[str, Any]],
    path: Path,
    data: dict[str, Any],
) -> None:
    for field in sorted(SOURCE_CARD_AUTHORITY_LIKE_FIELDS):
        if field in data:
            is_hard = field in SOURCE_CARD_HARD_AUTHORITY_FIELDS
            check = "source_card_authority_like_metadata"
            message = "Source cards are provenance records; legacy confidence/count/relation metadata is diagnostic only and must not be read as support or reviewed relation."
            if field == "relations":
                check = "source_card_relation_authority_metadata"
                message = "Source cards must not carry top-level relations; relation-like metadata can be misread as reviewed relation or evidence support."
            elif field == "confidence":
                check = "source_card_confidence_not_namespaced"
                message = "Source-card top-level confidence is not allowed unless moved into a non-authority capture/extraction namespace."
            add_issue(
                issues,
                path,
                "error" if is_hard else "warning",
                check,
                field,
                data.get(field),
                message,
                semantic_class="hard_error_canonical_p0" if is_hard else "high_risk_manual_review",
                recommended_action=(
                    "delete or move into a non-authority namespace before canonical P0"
                    if is_hard
                    else "move to legacy_raw_metadata/non-authority namespace or remove if this source enters frequent retrieval/context-pack use"
                ),
            )


VSRC_RE = re.compile(r"^vsrc:1:([A-Za-z0-9_.-]+):[^\s\x00-\x1f\x7f]+$")
NO_CONTROL_RE = re.compile(r"^[^\x00-\x1f\x7f]+$")
CAPTURE_ENVELOPE_REF_RE = re.compile(r"^(?![A-Za-z]:)(?!/)(?!.*\s)(?!.*\\)(?!.*(?:^|/)\.\.(?:/|$)).*/capture-envelope\.json$")
IDENTITY_PROFILE_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]*/v[0-9]+$")

SOURCE_IDENTITY_KEYS = {
    "schema_version",
    "source_id",
    "kind",
    "canonical_locator",
    "identity_profile",
    "aliases",
}

SOURCE_IDENTITY_ID_KINDS = {
    "repo",
    "doi",
    "arxiv",
    "openalex",
    "video",
    "opaque",
    "content",
}


def vsrc_kind(source_id: Any) -> str | None:
    if not isinstance(source_id, str):
        return None
    match = VSRC_RE.match(source_id)
    return match.group(1) if match else None


def has_control_char(value: str) -> bool:
    return NO_CONTROL_RE.match(value) is None


def check_source_capture_identity(
    issues: list[dict[str, Any]],
    path: Path,
    data: dict[str, Any],
    *,
    require_value: bool,
) -> None:
    top_source_id = data.get("source_id")
    source_identity = data.get("source_identity")
    if "source_integrity" in data:
        add_issue(
            issues,
            path,
            "warning",
            "legacy_source_integrity_compatibility",
            "source_integrity",
            data.get("source_integrity"),
            "source_integrity is legacy ingest hygiene; new structured capture should use Source Capture Envelope v1 artifacts.",
            semantic_class="migration_debt_defer_ok",
            recommended_action="leave legacy records as-is; use source_identity/latest_observed_capture_ref and capture-envelope artifacts when naturally touched",
        )
    if source_identity is None:
        add_issue(
            issues,
            path,
            "warning",
            "source_identity_missing",
            "source_identity",
            None,
            "Source Card lacks Source Capture Envelope v1 source_identity; legacy records remain readable but new structured captures should include it.",
            semantic_class="migration_debt_defer_ok",
            recommended_action="do not bulk migrate; add source_identity on new or naturally touched source records",
        )
        return
    if not isinstance(source_identity, dict):
        add_issue(
            issues,
            path,
            "error",
            "source_identity_shape",
            "source_identity",
            source_identity,
            "source_identity must be a mapping when present.",
        )
        return
    extra_keys = sorted(set(source_identity) - SOURCE_IDENTITY_KEYS)
    for key in extra_keys:
        add_issue(
            issues,
            path,
            "error",
            "source_identity_extra_field",
            f"source_identity.{key}",
            source_identity.get(key),
            "source_identity v1 is a lightweight identity mapping; extra fields must live in Capture Envelope artifacts or legacy/latest hint namespaces.",
        )
    for key in sorted(SOURCE_IDENTITY_KEYS):
        if key not in source_identity:
            add_issue(
                issues,
                path,
                "error",
                "source_identity_missing_field",
                f"source_identity.{key}",
                None,
                "source_identity v1 requires schema_version, source_id, kind, canonical_locator, identity_profile, and aliases when the mapping is present.",
            )
    schema_version = source_identity.get("schema_version")
    nested_source_id = source_identity.get("source_id")
    identity_kind = source_identity.get("kind")
    canonical_locator = source_identity.get("canonical_locator")
    identity_profile = source_identity.get("identity_profile")
    aliases = source_identity.get("aliases")
    if schema_version != 1:
        add_issue(
            issues,
            path,
            "error",
            "source_identity_schema_version",
            "source_identity.schema_version",
            schema_version,
            "source_identity.schema_version must be 1 for Source Capture Envelope v1.",
        )
    if not is_blank(nested_source_id):
        if not isinstance(nested_source_id, str) or not VSRC_RE.match(nested_source_id):
            add_issue(
                issues,
                path,
                "error",
                "source_identity_id_format",
                "source_identity.source_id",
                nested_source_id,
                "source_identity.source_id must use the vsrc:1 stable source-id format.",
            )
        else:
            id_kind = vsrc_kind(nested_source_id)
            if id_kind not in SOURCE_IDENTITY_ID_KINDS:
                add_issue(
                    issues,
                    path,
                    "error",
                    "source_identity_id_kind",
                    "source_identity.source_id",
                    nested_source_id,
                    "source_identity.source_id uses an unsupported vsrc:1 kind for v1 Source Cards.",
                )
            if not is_blank(identity_kind) and identity_kind != id_kind:
                add_issue(
                    issues,
                    path,
                    "error",
                    "source_identity_kind_mismatch",
                    "source_identity.kind",
                    identity_kind,
                    "source_identity.kind must match the vsrc:1 kind embedded in source_identity.source_id.",
                )
        if isinstance(top_source_id, str) and top_source_id.startswith("vsrc:1:") and top_source_id != nested_source_id:
            add_issue(
                issues,
                path,
                "error",
                "source_identity_top_level_mismatch",
                "source_id",
                top_source_id,
                "Top-level source_id mirrors source_identity.source_id when it uses vsrc:1.",
            )
    elif require_value and not is_template_path(path):
        add_issue(
            issues,
            path,
            "error",
            "source_identity_id_blank",
            "source_identity.source_id",
            nested_source_id,
            "source_identity exists but does not carry a stable source_id.",
        )
    if not is_blank(identity_kind):
        if not isinstance(identity_kind, str) or identity_kind not in SOURCE_IDENTITY_ID_KINDS:
            add_issue(
                issues,
                path,
                "error",
                "source_identity_kind",
                "source_identity.kind",
                identity_kind,
                "source_identity.kind must be one of the v1 source identity kinds.",
            )
    elif require_value and not is_template_path(path):
        add_issue(
            issues,
            path,
            "error",
            "source_identity_kind_blank",
            "source_identity.kind",
            identity_kind,
            "source_identity exists but does not carry a source kind.",
        )
    for field, value in [
        ("canonical_locator", canonical_locator),
        ("identity_profile", identity_profile),
    ]:
        if is_blank(value):
            if require_value and not is_template_path(path):
                add_issue(
                    issues,
                    path,
                    "error",
                    f"source_identity_{field}_blank",
                    f"source_identity.{field}",
                    value,
                    f"source_identity.{field} is required when source_identity is present.",
                )
            continue
        if not isinstance(value, str) or has_control_char(value):
            add_issue(
                issues,
                path,
                "error",
                f"source_identity_{field}_format",
                f"source_identity.{field}",
                value,
                f"source_identity.{field} must be a plain string without control characters.",
            )
    if not is_blank(identity_profile) and isinstance(identity_profile, str) and not IDENTITY_PROFILE_RE.match(identity_profile):
        add_issue(
            issues,
            path,
            "error",
            "source_identity_profile_format",
            "source_identity.identity_profile",
            identity_profile,
            "source_identity.identity_profile must be a versioned profile such as repo-provider-native/v1.",
        )
    if not isinstance(aliases, list):
        add_issue(
            issues,
            path,
            "error",
            "source_identity_aliases_shape",
            "source_identity.aliases",
            aliases,
            "source_identity.aliases must be a list of typed alias objects.",
        )
    else:
        for idx, alias in enumerate(aliases):
            if not alias and not require_value:
                continue
            if not isinstance(alias, dict) or set(alias) != {"kind", "value"}:
                add_issue(
                    issues,
                    path,
                    "error",
                    "source_identity_alias_shape",
                    f"source_identity.aliases[{idx}]",
                    alias,
                    "Each source_identity alias must be a mapping with only string kind and value fields.",
                )
                continue
            if not isinstance(alias.get("kind"), str) or is_blank(alias.get("kind")) or has_control_char(alias.get("kind")):
                add_issue(
                    issues,
                    path,
                    "error",
                    "source_identity_alias_kind",
                    f"source_identity.aliases[{idx}].kind",
                    alias.get("kind"),
                    "Each source_identity alias kind must be a non-blank string without control characters.",
                )
            if not isinstance(alias.get("value"), str) or is_blank(alias.get("value")) or has_control_char(alias.get("value")):
                add_issue(
                    issues,
                    path,
                    "error",
                    "source_identity_alias_value",
                    f"source_identity.aliases[{idx}].value",
                    alias.get("value"),
                    "Each source_identity alias value must be a non-blank string without control characters.",
                )
    latest_ref = data.get("latest_observed_capture_ref")
    if not is_blank(latest_ref):
        if not isinstance(latest_ref, str) or has_control_char(latest_ref) or not CAPTURE_ENVELOPE_REF_RE.match(latest_ref):
            add_issue(
                issues,
                path,
                "error",
                "latest_observed_capture_ref_format",
                "latest_observed_capture_ref",
                latest_ref,
                "latest_observed_capture_ref must be a relative pointer ending in capture-envelope.json.",
            )


def check_legacy_project_lens_overlay(
    issues: list[dict[str, Any]],
    path: Path,
    data: dict[str, Any],
) -> None:
    p = str(path).replace("\\", "/")
    if p.startswith("outputs/review/project_lens_overlays/") or data.get("type") == "project_lens_overlay":
        add_issue(
            issues,
            path,
            "warning",
            "legacy_project_lens_overlay_compatibility",
            "type",
            data.get("type") or p,
            "Legacy project_lens_overlay is included for compatibility; it is not proof of canonical Project Overlay P0 compliance.",
            semantic_class="high_risk_manual_review",
            recommended_action="migrate to canonical project_overlay with real target/scope fields, or explicitly exclude from canonical P0 scope",
        )


def check_support_item(
    issues: list[dict[str, Any]],
    path: Path,
    item: dict[str, Any],
    prefix: str,
    registry: dict[str, Any],
    *,
    require_value: bool,
) -> None:
    for field in ["ref", "record_kind", "knowledge_status", "pack_role", "warning_code", "action_basis_allowed", "selected_by"]:
        if field not in item:
            add_issue(
                issues,
                path,
                "error",
                "missing_required_field",
                f"{prefix}.{field}",
                None,
                f"{prefix}.{field} is required for receipt/pack item boundary checks.",
            )
        elif require_value and is_blank(item.get(field)):
            add_issue(
                issues,
                path,
                "error",
                "blank_required_field",
                f"{prefix}.{field}",
                item.get(field),
                f"Required item field is blank: {prefix}.{field}.",
            )
    for field in ["record_kind", "knowledge_status", "pack_role", "warning_code"]:
        if field in item:
            enum_field = field if field != "warning_code" else "retrieval_policy.warning_code"
            check_enum_as(issues, registry, path, enum_field, f"{prefix}.{field}", item.get(field))
    if "selected_by" in item and item.get("selected_by") is not None and not isinstance(item.get("selected_by"), dict):
        add_issue(
            issues,
            path,
            "error",
            "field_shape",
            f"{prefix}.selected_by",
            item.get("selected_by"),
            "selected_by must be a mapping.",
        )
    selected_by = item.get("selected_by") if isinstance(item.get("selected_by"), dict) else {}
    if selected_by.get("legacy_raw_metadata") is True:
        add_issue(
            issues,
            path,
            "error",
            "legacy_raw_metadata_used_for_selection",
            f"{prefix}.selected_by.legacy_raw_metadata",
            selected_by.get("legacy_raw_metadata"),
            "legacy_raw_metadata is historical audit debt and must be ignored by retrieval, graph, and support compilers.",
        )
    pack_role = item.get("pack_role")
    status = item.get("knowledge_status")
    record_kind = item.get("record_kind")
    anchor = item.get("independent_anchor_ref")
    if pack_role == "support":
        if status == "candidate" or record_kind in {"source_annotation", "candidate_distillation", "project_overlay", "feedback_event", "heavy_review_open", "graph_neighbor"}:
            add_issue(
                issues,
                path,
                "error",
                "non_support_record_marked_support",
                f"{prefix}.pack_role",
                pack_role,
                "Source annotations, candidates, overlays, feedback, heavy-review-open, and graph-neighbor items cannot be final support.",
            )
        if is_blank(anchor):
            add_issue(
                issues,
                path,
                "error",
                "support_missing_independent_anchor",
                f"{prefix}.independent_anchor_ref",
                anchor,
                "Support items require independent raw/stable anchors.",
            )
        if selected_by and is_blank(anchor):
            add_issue(
                issues,
                path,
                "error",
                "diagnostic_signal_as_support",
                f"{prefix}.selected_by",
                selected_by,
                "Lexical, semantic, graph, metadata, rank, and dashboard signals are diagnostics, not support.",
            )


def check_support_checks(
    issues: list[dict[str, Any]],
    path: Path,
    checks: Any,
    registry: dict[str, Any],
) -> None:
    if not isinstance(checks, list):
        return
    for idx, check in enumerate(checks):
        if not isinstance(check, dict):
            continue
        result = check.get("result")
        if result is not None and not is_template_placeholder(result):
            check_enum(issues, registry, path, "support_result", result)
        for field in ["claim_ref", "independent_anchor_ref"]:
            value = check.get(field)
            if isinstance(value, str) and any(term in value.lower() for term in LEGACY_RAW_METADATA_TERMS):
                add_issue(
                    issues,
                    path,
                    "error",
                    "legacy_raw_metadata_used_as_support_anchor",
                    f"support_checks[{idx}].{field}",
                    value,
                    "legacy_raw_metadata cannot be a support claim or independent anchor.",
                )
        if result == "supported" and is_blank(check.get("independent_anchor_ref")):
            add_issue(
                issues,
                path,
                "error",
                "supported_without_independent_anchor",
                f"support_checks[{idx}].independent_anchor_ref",
                check.get("independent_anchor_ref"),
                "A supported result requires an independent anchor.",
            )


def validate_file(root: Path, rel_path: Path, registry: dict[str, Any], issues: list[dict[str, Any]]) -> bool:
    abs_path = root / rel_path
    text = read_text(abs_path)
    raw_frontmatter = extract_frontmatter_text(abs_path)
    data = frontmatter(abs_path)
    if data is None:
        return False
    if not is_intake_surface(rel_path, data):
        return False
    if raw_frontmatter is not None:
        check_duplicate_yaml_keys(issues, rel_path, raw_frontmatter)
    require_value = not is_template_path(rel_path)
    if require_value:
        check_placeholder_values(issues, rel_path, data, document_text=text)
        check_legacy_project_lens_overlay(issues, rel_path, data)

    expected_record_kind = inferred_record_kind(rel_path, data)
    if expected_record_kind and data.get("record_kind") != expected_record_kind:
        add_issue(
            issues,
            rel_path,
            "error",
            "canonical_serialization",
            "record_kind",
            data.get("record_kind"),
            f"Source Intake surface must serialize canonical record_kind: {expected_record_kind}.",
        )
    if "record_type" in data:
        add_issue(
            issues,
            rel_path,
            "error",
            "canonical_serialization",
            "record_type",
            data.get("record_type"),
            "Use record_kind, not record_type, for Source Intake machine kind.",
        )

    for field in ["record_kind", "processing_tier", "knowledge_status", "overlay_state", "review_pressure", "promotion_gate", "query_mode", "event_kind", "anchor_status", "evidence_support_status"]:
        if field in data:
            check_enum(issues, registry, rel_path, field, data.get(field))

    if "processing_mode" in data or "processing_level" in data:
        add_issue(
            issues,
            rel_path,
            "error",
            "duplicate_processing_fields",
            "processing_mode/processing_level",
            data.get("processing_mode") or data.get("processing_level"),
            "Use processing_tier as the only machine field for processing effort.",
        )

    policy = get_policy(data)
    if "retrieval_policy" in data and not isinstance(data.get("retrieval_policy"), dict):
        add_issue(
            issues,
            rel_path,
            "error",
            "retrieval_policy_shape",
            "retrieval_policy",
            data.get("retrieval_policy"),
            "retrieval_policy must be a mapping with policy_kind, pack_allowed, action_basis_allowed, warning_code.",
        )
    for key in ["policy_kind", "pack_allowed", "action_basis_allowed", "warning_code"]:
        if key in policy:
            check_enum(issues, registry, rel_path, f"retrieval_policy.{key}", policy.get(key))

    record_kind = data.get("record_kind")
    knowledge_status = data.get("knowledge_status")
    intake_authority_status = record_kind in {
        "source_card",
        "source_annotation",
        "candidate_distillation",
        "project_overlay",
        "overlay_suggestion",
        "feedback_event",
        "heavy_review_open",
        "context_pack_manifest",
    } or knowledge_status in {"raw", "candidate"}

    if intake_authority_status:
        for field in FORBIDDEN_INTAKE_FIELDS:
            if field in data:
                add_issue(
                    issues,
                    rel_path,
                    "error",
                    "forbidden_intake_field",
                    field,
                    data.get(field),
                    "Forbidden authority-like field on source/candidate/overlay/feedback intake surface.",
                )

    if knowledge_status in {"raw", "candidate"} or record_kind in {"source_annotation", "project_overlay", "overlay_suggestion", "feedback_event", "heavy_review_open", "context_pack_manifest"}:
        for field, value in [
            ("action_basis_allowed", data.get("action_basis_allowed")),
            ("truth_mutation_allowed", data.get("truth_mutation_allowed")),
            ("retrieval_policy.action_basis_allowed", policy.get("action_basis_allowed")),
        ]:
            if value is True or str(value).lower() == "true":
                add_issue(
                    issues,
                    rel_path,
                    "error",
                    "authority_bypass",
                    field,
                    value,
                    "Raw/candidate/overlay/feedback surfaces cannot allow action basis or truth mutation.",
                )

    if record_kind == "overlay_suggestion":
        add_issue(
            issues,
            rel_path,
            "error",
            "suggested_overlay_persisted",
            "record_kind",
            record_kind,
            "Overlay suggestions are trace/inbox artifacts and must not persist as standalone Source Intake records.",
        )

    if record_kind == "source_card":
        if require_value:
            check_source_card_authority_like_metadata(issues, rel_path, data)
        check_source_capture_identity(issues, rel_path, data, require_value=require_value)
        for field in ["source_id", "captured_at", "title", "why_saved"]:
            require_field(issues, rel_path, data, field, require_value=require_value)
        require_one_of(issues, rel_path, data, ["source_url", "raw_location"], require_value=require_value)
        if knowledge_status != "raw":
            add_issue(
                issues,
                rel_path,
                "error",
                "source_card_status",
                "knowledge_status",
                knowledge_status,
                "Source cards are provenance records and must use knowledge_status: raw.",
            )

    if record_kind == "source_annotation":
        for field in ["annotation_id", "source_ref", "selector_type", "anchor_status", "annotation_role", "support_checked", "evidence_support_status"]:
            require_field(issues, rel_path, data, field, require_value=require_value)
        require_one_of(
            issues,
            rel_path,
            data,
            ["selector_exact", "selector_position", "selector_timestamp_start", "selector_page", "selector_rect"],
            require_value=require_value,
        )
        if knowledge_status != "candidate":
            add_issue(
                issues,
                rel_path,
                "error",
                "source_annotation_status",
                "knowledge_status",
                knowledge_status,
                "Source annotations are candidate/review-input locators and must use knowledge_status: candidate.",
            )
        if data.get("processing_tier") not in {"light", "medium"}:
            add_issue(
                issues,
                rel_path,
                "error",
                "source_annotation_processing_tier",
                "processing_tier",
                data.get("processing_tier"),
                "Source annotations are lightweight locator records and must use processing_tier: light or medium.",
            )
        if data.get("support_checked") is True and is_blank(data.get("evidence_packet_ref")):
            add_issue(
                issues,
                rel_path,
                "error",
                "source_annotation_support_without_packet",
                "evidence_packet_ref",
                data.get("evidence_packet_ref"),
                "A checked annotation must point to the Evidence Packet that performed evidence_support.",
            )

    if record_kind == "project_overlay":
        for field in ["project_id", "target_ref", "project_borrow_scope", "project_non_borrow_scope", "project_reopen_trigger"]:
            require_field(issues, rel_path, data, field, require_value=require_value)
        check_project_local_wording(issues, rel_path, data.get("project_non_borrow_scope"))
        state = data.get("overlay_state")
        if state == "suggested":
            add_issue(
                issues,
                rel_path,
                "error",
                "suggested_overlay_persisted",
                "overlay_state",
                state,
                "Suggested overlays must stay in trace/inbox and not persist as project_overlay records.",
            )
        if state == "confirmed" and data.get("retrieval_scope") != "active_project_only":
            add_issue(
                issues,
                rel_path,
                "error",
                "overlay_scope",
                "retrieval_scope",
                data.get("retrieval_scope"),
                "Confirmed overlays must be active-project-only by default.",
            )
        if state == "confirmed" and data.get("default_retrieval") is not False:
            add_issue(
                issues,
                rel_path,
                "error",
                "confirmed_overlay_default_retrieval",
                "default_retrieval",
                data.get("default_retrieval"),
                "Confirmed overlays are active-project-only and must not enter default retrieval globally.",
            )
        if state == "archived":
            if data.get("default_retrieval") is not False:
                add_issue(
                    issues,
                    rel_path,
                    "error",
                    "archived_overlay_default_retrieval",
                    "default_retrieval",
                    data.get("default_retrieval"),
                    "Archived overlays must be excluded from default retrieval.",
                )
            if policy.get("pack_allowed") != "none":
                add_issue(
                    issues,
                    rel_path,
                    "error",
                    "archived_overlay_pack_allowed",
                    "retrieval_policy.pack_allowed",
                    policy.get("pack_allowed"),
                    "Archived overlays must not enter context packs by default.",
                )

    if record_kind == "candidate_distillation":
        require_one_of(issues, rel_path, data, ["source_ref", "derived_from"], require_value=require_value)
        require_field(issues, rel_path, data, "provisional", require_value=False)
        if data.get("provisional") is not True and str(data.get("provisional")).lower() != "true":
            add_issue(
                issues,
                rel_path,
                "error",
                "candidate_not_provisional",
                "provisional",
                data.get("provisional"),
                "Candidate distillation must explicitly serialize provisional: true.",
            )
        if not body_has_candidate_points(text):
            add_issue(
                issues,
                rel_path,
                "error",
                "missing_candidate_points",
                "candidate_points",
                None,
                "Candidate distillation must include candidate points in frontmatter or body.",
            )
        for field in ["project_borrow_scope", "project_non_borrow_scope"]:
            if field in data:
                add_issue(
                    issues,
                    rel_path,
                    "error",
                    "candidate_project_decision",
                    field,
                    data.get(field),
                    "Candidate distillation must not carry project borrow/non-borrow decisions.",
                )

    if record_kind == "heavy_review_open":
        for field in ["claim", "warrant", "scope", "gaps", "residual_risk", "review_status"]:
            require_field(issues, rel_path, data, field, require_value=require_value)
        require_one_of(issues, rel_path, data, ["source_anchor_refs", "evidence_anchor_refs"], require_value=require_value)
        review_status = data.get("review_status")
        if review_status in {"accepted", "review_passed"}:
            if data.get("forbidden_support_proxies_checked") is not True:
                add_issue(
                    issues,
                    rel_path,
                    "error",
                    "forbidden_proxy_check_missing",
                    "forbidden_support_proxies_checked",
                    data.get("forbidden_support_proxies_checked"),
                    "Accepted/passed heavy review must explicitly pass forbidden proxy check.",
                )
        warrant = data.get("warrant")
        if isinstance(warrant, str):
            lower = warrant.lower()
            if any(term in lower for term in PROXY_SUPPORT_TERMS):
                add_issue(
                    issues,
                    rel_path,
                    "error",
                    "proxy_support_in_warrant",
                    "warrant",
                    warrant,
                    "Warrant cannot use diagram, score, rank, vendor claim, benchmark, or count as support.",
                )

    if record_kind == "feedback_event":
        for field in ["event_kind", "target_ref", "event_time", "review_pressure_effect"]:
            require_field(issues, rel_path, data, field, require_value=require_value)
        require_one_of(issues, rel_path, data, ["project_ref", "observed_in_context"], require_value=require_value)
        if data.get("event_kind") is not None:
            check_enum(issues, registry, rel_path, "event_kind", data.get("event_kind"))

    if record_kind == "query_run_trace":
        for field in ["query_id", "query_time", "question_summary", "verbatim_input", "query_mode", "requested_authority_bucket"]:
            require_field(issues, rel_path, data, field, require_value=require_value)
        for field in ["active_project", "human_confirmation_required"]:
            require_field(issues, rel_path, data, field, require_value=False)
        require_list(issues, rel_path, data, "included_buckets", require_value=False)
        require_list(issues, rel_path, data, "excluded_buckets", require_value=False)
        require_mapping(issues, rel_path, data, "retrieval_filters", require_value=False)
        require_list(issues, rel_path, data, "selected_items", require_value=False)
        require_list(issues, rel_path, data, "support_checks", require_value=False)
        if data.get("query_mode") is not None:
            check_enum(issues, registry, rel_path, "query_mode", data.get("query_mode"))
        selected_items = data.get("selected_items")
        if isinstance(selected_items, list):
            for idx, item in enumerate(selected_items):
                if isinstance(item, dict):
                    check_support_item(issues, rel_path, item, f"selected_items[{idx}]", registry, require_value=require_value)
        check_support_checks(issues, rel_path, data.get("support_checks"), registry)

    if record_kind == "context_pack_manifest":
        for field in ["query_run_ref", "active_project", "query_mode", "requested_authority_bucket"]:
            require_field(issues, rel_path, data, field, require_value=require_value)
        require_list(issues, rel_path, data, "included_buckets", require_value=False)
        require_list(issues, rel_path, data, "excluded_buckets", require_value=False)
        require_list(issues, rel_path, data, "items", require_value=False)
        require_list(issues, rel_path, data, "support_checks", require_value=False)
        if data.get("query_mode") is not None:
            check_enum(issues, registry, rel_path, "query_mode", data.get("query_mode"))
        items = data.get("items")
        if isinstance(items, list):
            for idx, item in enumerate(items):
                if isinstance(item, dict):
                    check_support_item(issues, rel_path, item, f"items[{idx}]", registry, require_value=require_value)
        check_support_checks(issues, rel_path, data.get("support_checks"), registry)
    return True


def collect_files(root: Path, scope: str) -> list[Path]:
    if scope == "contract":
        return [Path(p) for p in CONTRACT_FILES if (root / p).exists()]
    paths: set[Path] = set()
    for pattern in CURRENT_GLOBS:
        paths.update(p.relative_to(root) for p in root.glob(pattern) if p.is_file())
    return sorted(paths)


def write_outputs(root: Path, out_dir: Path, scope: str, files: list[Path], issues: list[dict[str, Any]], validated_count: int) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    errors = [i for i in issues if i["severity"] == "error"]
    warnings = [i for i in issues if i["severity"] == "warning"]
    warning_breakdown: dict[str, int] = {}
    warning_breakdown_by_semantic_class: dict[str, int] = {}
    issue_breakdown_by_semantic_class: dict[str, int] = {}
    for warning in warnings:
        check = str(warning.get("check", "unknown"))
        warning_breakdown[check] = warning_breakdown.get(check, 0) + 1
        semantic_class = str(warning.get("semantic_class", "unknown"))
        warning_breakdown_by_semantic_class[semantic_class] = warning_breakdown_by_semantic_class.get(semantic_class, 0) + 1
    for issue in issues:
        semantic_class = str(issue.get("semantic_class", "unknown"))
        issue_breakdown_by_semantic_class[semantic_class] = issue_breakdown_by_semantic_class.get(semantic_class, 0) + 1
    if errors:
        status = "fail"
        structural_status = "fail"
        semantic_status = "blocked_by_structural_errors"
    elif warnings:
        status = "structural_pass_semantic_debt"
        structural_status = "pass"
        semantic_status = "debt_pending"
    else:
        status = "pass"
        structural_status = "pass"
        semantic_status = "clear"
    retrieval_visible_project_lens_count = len(
        list((root / "outputs" / "review" / "project_lens_overlays").glob("*.md"))
    )
    archived_legacy_project_lens_count = len(list((root / "outputs" / "review" / "_legacy_project_lens").glob("*.md")))
    summary = {
        "scope": scope,
        "files_scanned": len(files),
        "files_validated": validated_count,
        "files_skipped": len(files) - validated_count,
        "canonical_validated_surfaces_excluding_legacy_lens": (
            validated_count - retrieval_visible_project_lens_count if scope == "current" else None
        ),
        "legacy_project_lens_compatibility_included_in_current_scope": scope == "current",
        "legacy_project_lens_compatibility_count": retrieval_visible_project_lens_count if scope == "current" else None,
        "legacy_project_lens_archive_excluded_count": archived_legacy_project_lens_count if scope == "current" else None,
        "issue_count": len(issues),
        "warning_count": len(warnings),
        "error_count": len(errors),
        "status": status,
        "structural_status": structural_status,
        "semantic_status": semantic_status,
        "warning_breakdown_by_check": warning_breakdown,
        "warning_breakdown_by_semantic_class": warning_breakdown_by_semantic_class,
        "issue_breakdown_by_semantic_class": issue_breakdown_by_semantic_class,
        "canonical_p0_status": "not_passed" if warnings or errors else "candidate_structural_clear",
        "truth_boundary": "Structural lint can pass while semantic migration debt remains; retrieval-visible legacy project_lens overlays are included as compatibility surfaces but do not count as canonical P0 compliance.",
    }
    (out_dir / f"source_intake_{scope}_lint_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    with (out_dir / f"source_intake_{scope}_lint_issues.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "severity",
            "check",
            "semantic_class",
            "recommended_action",
            "path",
            "line",
            "field",
            "value",
            "message",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(issues)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", choices=["contract", "current"], default="contract")
    parser.add_argument("--root", default=".")
    parser.add_argument("--out-dir", default="outputs/review/source-intake-control-flow-hardening-2026-06-12/results")
    parser.add_argument("--no-fail", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    registry = load_registry(root)
    files = collect_files(root, args.scope)
    issues: list[dict[str, Any]] = []
    validated_count = 0
    for rel in files:
        if validate_file(root, rel, registry, issues):
            validated_count += 1
    write_outputs(root, root / args.out_dir, args.scope, files, issues, validated_count)
    errors = [i for i in issues if i["severity"] == "error"]
    warnings = [i for i in issues if i["severity"] == "warning"]
    print(
        json.dumps(
            {
                "scope": args.scope,
                "files_scanned": len(files),
                "files_validated": validated_count,
                "warnings": len(warnings),
                "errors": len(errors),
            },
            ensure_ascii=False,
        )
    )
    return 0 if args.no_fail or not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
