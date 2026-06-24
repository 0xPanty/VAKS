#!/usr/bin/env python
"""Validate a Source Capture Envelope v1 artifact bundle.

This validates an existing bundle directory containing:
- capture-envelope.json
- snapshot-manifest.jsonl
- snapshot-hygiene.intoto.json

It is intentionally fail-closed and uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any


SEVERITY_ORDER = {"none": 0, "info": 1, "warning": 2, "hazard": 3, "error": 4}
CAPTURE_ID_RE = re.compile(r"^urn:uuid:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$")
SOURCE_ID_RE = re.compile(r"^vsrc:1:[A-Za-z0-9_.-]+:[^\s\x00-\x1f\x7f]+$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
ALGORITHM_DIGEST_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]*:[0-9a-f]{40,128}$")
REVISION_KINDS = {
    "git_commit",
    "git_tag",
    "git_ref",
    "version",
    "arxiv_version",
    "timestamp",
    "content_hash",
    "provider_revision",
    "doi_version",
    "web_capture_time",
}
HYGIENE_PREDICATES = {
    "urn:vaks:predicate:repo-snapshot-hygiene:v1",
    "urn:vaks:predicate:source-snapshot-hygiene:v1",
}
HYGIENE_PROFILES = {"archive-safety/v1", "repo-portability/v1", "repo-completeness/v1", "source-fixity/v1"}
SOURCE_KINDS = {"repo", "file", "archive", "pdf", "video", "web", "unknown"}
CAPTURE_METHODS = {"provider_archive", "git_clone", "api", "upload", "local_file", "archive_file"}
OBSERVATION_STATES = {"captured", "partial", "failed"}
CHANGE_STATES = {"first_seen", "same_snapshot", "new_snapshot", "unknown"}
RAW_DISPOSITIONS = {"admitted", "quarantined", "rejected", "not_evaluated"}
IMPLEMENTATION_MEDIA_TYPE = "application/vnd.vaks.source-capture-implementation.v1+json"
IMPLEMENTATION_SCHEMA = "urn:vaks:schema:source-capture-implementation:v1"
IMPLEMENTATION_ID = "vaks.source-capture-envelope"
IMPLEMENTATION_VERSION = "1.0-alpha.1"
CONTENT_TYPE_PROFILE = "vaks-media-type-detection/v1"
CONTENT_TYPE_BASIS = {"container_parser", "magic_signature", "locator_hint", "fallback"}
CONTENT_TYPE_HINT_MATCH = {"matched", "mismatch", "no_hint", "not_comparable"}
ARCHIVE_MEDIA_TYPES = {"application/zip", "application/x-tar", "application/gzip", "application/x-bzip2", "application/x-xz"}
VALIDATOR_PROFILES = {"base", "enterprise-alpha1"}
MAX_MANIFEST_BYTES = 64 * 1024 * 1024
MAX_HYGIENE_BYTES = 16 * 1024 * 1024
MAX_MANIFEST_ENTRIES = 100_000
MAX_STRING_LENGTH = 16_384
MAX_ARCHIVE_PATH_STRING_LENGTH = MAX_STRING_LENGTH
PINNED_MAX_FINDINGS_PER_CODE = 100
POLICY_COMPONENT_PATH = "policies/source-capture/raw-intake-default-v1.json"
EXPECTED_IMPLEMENTATION_COMPONENTS = {
    POLICY_COMPONENT_PATH,
    "schemas/snapshot-hygiene-v1.schema.json",
    "schemas/source-capture-v1.schema.json",
    "tools/inspect_source_snapshot.py",
    "tools/source_intake_enum_registry.json",
    "tools/validate_source_capture_bundle.py",
}
ENTERPRISE_PARAMETER_KEYS = {"max_input_blob_size"}
REQUIRED_PARAMETER_KEYS = {
    "limits_profile",
    "max_entries",
    "max_total_size",
    "max_entry_size",
    "max_compression_ratio",
    "max_path_depth",
    "max_path_length",
    "max_symlink_target_size",
    "max_findings_per_code",
    "max_finding_paths",
    "max_finding_detail_items",
}


class ValidationError(Exception):
    pass


def reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def loads_strict_json(text: str, context: str) -> Any:
    try:
        return json.loads(
            text,
            object_pairs_hook=reject_duplicate_json_keys,
            parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"non-standard JSON constant: {value}")),
        )
    except Exception as exc:
        raise ValidationError(f"invalid JSON: {context}: {exc}") from exc


def exact_keys(obj: Any, required: set[str], allowed: set[str], context: str) -> None:
    if not isinstance(obj, dict):
        raise ValidationError(f"{context} must be an object")
    missing = sorted(required - set(obj))
    if missing:
        raise ValidationError(f"{context} missing required keys: {', '.join(missing)}")
    extra = sorted(set(obj) - allowed)
    if extra:
        raise ValidationError(f"{context} has unsupported keys: {', '.join(extra)}")


def require_string(value: Any, context: str, *, non_blank: bool = True, pattern: re.Pattern[str] | None = None) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"{context} must be a string")
    if len(value) > MAX_STRING_LENGTH:
        raise ValidationError(f"{context} exceeds validator string length limit")
    if non_blank and not value.strip():
        raise ValidationError(f"{context} must be non-blank")
    if any(ord(char) < 0x20 or ord(char) == 0x7F for char in value):
        raise ValidationError(f"{context} must not contain control characters")
    if pattern is not None and not pattern.match(value):
        raise ValidationError(f"{context} has invalid format")
    return value


def require_digest(value: Any, context: str) -> str:
    return require_string(value, context, pattern=DIGEST_RE)


def require_nonnegative_int(value: Any, context: str) -> int:
    if type(value) is not int or value < 0:
        raise ValidationError(f"{context} must be a non-negative integer")
    return value


def require_positive_int(value: Any, context: str) -> int:
    if type(value) is not int or value < 1:
        raise ValidationError(f"{context} must be a positive integer")
    return value


def parse_datetime(value: Any, context: str) -> None:
    text = require_string(value, context)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValidationError(f"{context} must be ISO 8601 date-time") from exc
    if parsed.tzinfo is None:
        raise ValidationError(f"{context} must include timezone")


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def canonical_json_bytes(obj: dict[str, Any]) -> bytes:
    return (json.dumps(obj, allow_nan=False, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def script_root() -> Path:
    return Path(__file__).resolve().parent.parent


def default_implementation_manifest_path() -> Path:
    return script_root() / "tools" / "source_capture_implementation_manifest.json"


def load_implementation_manifest(manifest_path: Path) -> dict[str, Any]:
    root = script_root()
    manifest = read_json(manifest_path)
    exact_keys(manifest, {"schema", "id", "version", "components", "runtime"}, {"schema", "id", "version", "components", "runtime"}, "implementation manifest")
    if manifest.get("schema") != IMPLEMENTATION_SCHEMA or manifest.get("id") != IMPLEMENTATION_ID:
        raise ValidationError("implementation manifest identity mismatch")
    if manifest.get("version") != IMPLEMENTATION_VERSION:
        raise ValidationError("implementation manifest version mismatch")
    components = manifest.get("components")
    if not isinstance(components, list) or not components:
        raise ValidationError("implementation manifest components must be a non-empty list")
    seen_paths: set[str] = set()
    component_digests: dict[str, str] = {}
    for idx, component in enumerate(components):
        exact_keys(component, {"path", "digest"}, {"path", "digest"}, f"implementation manifest component[{idx}]")
        rel = require_string(component.get("path"), f"implementation manifest component[{idx}].path")
        expected_digest = require_digest(component.get("digest"), f"implementation manifest component[{idx}].digest")
        if "\\" in rel or rel.startswith("/") or ".." in Path(rel).parts:
            raise ValidationError(f"implementation manifest component path is invalid: {rel}")
        if rel in seen_paths:
            raise ValidationError(f"duplicate implementation manifest component: {rel}")
        seen_paths.add(rel)
        component_path = (root / rel).resolve()
        try:
            component_path.relative_to(root)
        except ValueError as exc:
            raise ValidationError(f"implementation manifest component escapes root: {rel}") from exc
        if not component_path.is_file() or component_path.is_symlink():
            raise ValidationError(f"implementation manifest component is missing or unsafe: {rel}")
        actual_digest = digest_file(component_path)
        if actual_digest != expected_digest:
            raise ValidationError(f"implementation manifest component digest mismatch: {rel}")
        component_digests[rel] = expected_digest
    if seen_paths != EXPECTED_IMPLEMENTATION_COMPONENTS:
        missing = sorted(EXPECTED_IMPLEMENTATION_COMPONENTS - seen_paths)
        extra = sorted(seen_paths - EXPECTED_IMPLEMENTATION_COMPONENTS)
        raise ValidationError(f"implementation manifest component set mismatch; missing={missing}; extra={extra}")
    runtime = manifest.get("runtime")
    exact_keys(runtime, {"language", "minimum_version"}, {"language", "minimum_version"}, "implementation manifest runtime")
    if runtime.get("language") != "python" or runtime.get("minimum_version") != "3.10":
        raise ValidationError("implementation manifest runtime is invalid")
    return {
        "root": root,
        "path": manifest_path,
        "descriptor": {
            "media_type": IMPLEMENTATION_MEDIA_TYPE,
            "size": manifest_path.stat().st_size,
            "digest": digest_file(manifest_path),
        },
        "component_digests": component_digests,
    }


def read_json(path: Path) -> dict[str, Any]:
    if path.name == "snapshot-hygiene.intoto.json" and path.stat().st_size > MAX_HYGIENE_BYTES:
        raise ValidationError("snapshot hygiene exceeds validator size limit")
    data = loads_strict_json(path.read_text(encoding="utf-8"), str(path))
    if not isinstance(data, dict):
        raise ValidationError(f"JSON root must be an object: {path}")
    return data


def require_file(bundle: Path, name: str) -> Path:
    path = bundle / name
    if not path.exists() or not path.is_file() or path.is_symlink():
        raise ValidationError(f"missing or unsafe bundle file: {name}")
    return path


def descriptor_matches(path: Path, descriptor: dict[str, Any], field: str) -> None:
    data = path.read_bytes()
    expected_size = descriptor.get("size")
    expected_digest = descriptor.get("digest")
    if expected_size != len(data):
        raise ValidationError(f"{field}.size mismatch: expected {expected_size}, got {len(data)}")
    actual_digest = sha256_bytes(data)
    if expected_digest != actual_digest:
        raise ValidationError(f"{field}.digest mismatch: expected {expected_digest}, got {actual_digest}")


def parse_manifest(path: Path) -> tuple[list[dict[str, Any]], bytes]:
    data = path.read_bytes()
    if len(data) > MAX_MANIFEST_BYTES:
        raise ValidationError("snapshot manifest exceeds validator size limit")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError("snapshot manifest is not UTF-8") from exc
    if not text.endswith("\n"):
        raise ValidationError("snapshot manifest must end with LF")
    if "\r" in text:
        raise ValidationError("snapshot manifest must use LF, not CRLF")
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        row = loads_strict_json(line, f"manifest line {line_no}")
        if not isinstance(row, dict):
            raise ValidationError(f"manifest line {line_no} must be an object")
        try:
            canonical = json.dumps(row, allow_nan=False, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        except ValueError as exc:
            raise ValidationError(f"manifest line {line_no} contains non-standard JSON numeric values") from exc
        if canonical != line:
            raise ValidationError(f"manifest line {line_no} is not canonical sorted-key JSON")
        rows.append(row)
        if len(rows) > MAX_MANIFEST_ENTRIES + 1:
            raise ValidationError("snapshot manifest exceeds validator entry limit")
    if not rows:
        raise ValidationError("snapshot manifest is empty")
    return rows, data


def is_absolute_path(path: str) -> bool:
    return path.startswith(("/", "\\")) or bool(re.match(r"^[A-Za-z]:", path))


def path_segments(path: str) -> list[str]:
    return re.split(r"[\\/]", path)


def validate_manifest_path(path: str, context: str) -> None:
    require_string(path, context)
    if "\\" in path:
        raise ValidationError(f"{context} uses backslash; v1 manifest paths must use forward slash")
    if is_absolute_path(path):
        raise ValidationError(f"{context} is absolute")
    if "//" in path:
        raise ValidationError(f"{context} contains empty path segment")
    segments = path_segments(path)
    if any(segment in {"", ".", ".."} for segment in segments):
        raise ValidationError(f"{context} contains empty, dot, or traversal segment")


def has_path_traversal(path: str) -> bool:
    return any(segment == ".." for segment in path_segments(path) if segment)


def parent_paths(path: str) -> list[str]:
    parts = path.split("/")
    return ["/".join(parts[:idx]) for idx in range(1, len(parts)) if "/".join(parts[:idx])]


def validate_manifest_tree_model(entries: list[dict[str, Any]]) -> None:
    terminal_paths = {str(entry["path"]) for entry in entries}
    if len(terminal_paths) != len(entries):
        raise ValidationError("manifest contains duplicate paths")
    for entry in entries:
        entry_path = str(entry["path"])
        for parent in parent_paths(entry_path):
            if parent in terminal_paths:
                raise ValidationError(f"manifest path has file/symlink ancestor conflict: {parent} -> {entry_path}")


def validate_manifest_rows(rows: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]]]:
    header = rows[0]
    exact_keys(header, {"schema", "profile", "state"}, {"schema", "profile", "state", "reason_codes"}, "manifest header")
    if header.get("schema") != "urn:vaks:schema:snapshot-manifest:v1":
        raise ValidationError("manifest header schema mismatch")
    if header.get("profile") != "vaks-archive-tree/v1":
        raise ValidationError("manifest header profile mismatch")
    state = header.get("state")
    if state not in {"complete", "blob", "unavailable"}:
        raise ValidationError(f"manifest header state is invalid: {state}")
    if state == "unavailable":
        reason_codes = header.get("reason_codes")
        if not isinstance(reason_codes, list) or not reason_codes:
            raise ValidationError("unavailable manifest must carry non-empty reason_codes")
        for idx, code in enumerate(reason_codes):
            require_string(code, f"manifest header reason_codes[{idx}]")
    elif "reason_codes" in header:
        raise ValidationError("reason_codes are only allowed on unavailable manifests")
    entries = rows[1:]
    if state in {"blob", "unavailable"} and entries:
        raise ValidationError(f"{state} manifest must not carry tree entries")
    paths: list[str] = []
    for idx, entry in enumerate(entries, start=2):
        if not isinstance(entry, dict):
            raise ValidationError(f"manifest line {idx} must be an object")
        entry_type = entry.get("type")
        path = entry.get("path")
        validate_manifest_path(path, f"manifest line {idx} path")
        paths.append(path)
        if entry_type == "file":
            exact_keys(entry, {"digest", "mode", "path", "size", "type"}, {"digest", "mode", "path", "size", "type"}, f"manifest line {idx}")
            digest = entry.get("digest")
            require_digest(digest, f"manifest line {idx} digest")
            if digest == "sha256:" + ("0" * 64):
                raise ValidationError(f"manifest line {idx} uses forbidden zero digest fallback")
            require_nonnegative_int(entry.get("size"), f"manifest line {idx} size")
            if entry.get("mode") not in {"100644", "100755"}:
                raise ValidationError(f"manifest line {idx} has invalid file mode")
        elif entry_type == "symlink":
            exact_keys(entry, {"mode", "path", "target", "type"}, {"mode", "path", "target", "type"}, f"manifest line {idx}")
            if entry.get("mode") != "120000":
                raise ValidationError(f"manifest line {idx} has invalid symlink mode")
            target = require_string(entry.get("target"), f"manifest line {idx} symlink target")
            if "\\" in target or is_absolute_path(target) or has_path_traversal(target):
                raise ValidationError(f"manifest line {idx} symlink target escapes or is platform-ambiguous")
        else:
            raise ValidationError(f"manifest line {idx} has invalid entry type")
    if paths != sorted(paths):
        raise ValidationError("manifest entries are not sorted by path")
    validate_manifest_tree_model(entries)
    return str(state), entries


def computed_max_severity(findings: list[dict[str, Any]]) -> str:
    if not findings:
        return "none"
    return max((str(item.get("severity")) for item in findings), key=lambda value: SEVERITY_ORDER.get(value, -1))


def path_depth(path: str) -> int:
    return len([part for part in path.split("/") if part])


def finding_counts_by_code(findings: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in findings:
        code = item.get("code")
        if not isinstance(code, str) or code == "HYGIENE_FINDINGS_TRUNCATED":
            continue
        counts[code] = counts.get(code, 0) + 1
    return counts


def truncation_counts_by_code(findings: list[dict[str, Any]]) -> dict[str, int]:
    markers = [item for item in findings if item.get("code") == "HYGIENE_FINDINGS_TRUNCATED"]
    if len(markers) > 1:
        raise ValidationError("HYGIENE_FINDINGS_TRUNCATED must appear at most once")
    if not markers:
        return {}
    marker = markers[0]
    if marker.get("severity") != "warning":
        raise ValidationError("HYGIENE_FINDINGS_TRUNCATED must use warning severity")
    details = marker.get("details")
    if not isinstance(details, dict):
        raise ValidationError("HYGIENE_FINDINGS_TRUNCATED must carry details")
    truncated = details.get("truncated_by_code")
    if not isinstance(truncated, dict) or not truncated:
        raise ValidationError("HYGIENE_FINDINGS_TRUNCATED must carry non-empty details.truncated_by_code")
    result: dict[str, int] = {}
    for code, value in truncated.items():
        require_string(code, "HYGIENE_FINDINGS_TRUNCATED details.truncated_by_code key")
        if type(value) is not int or value < 1:
            raise ValidationError(f"HYGIENE_FINDINGS_TRUNCATED count for {code} must be a positive integer")
        result[code] = value
    return result


def validate_truncation_marker(
    findings: list[dict[str, Any]],
    truncation_counts: dict[str, int],
    *,
    max_findings_per_code: int,
) -> None:
    explicit_counts = finding_counts_by_code(findings)
    for code in truncation_counts:
        if explicit_counts.get(code, 0) != max_findings_per_code:
            raise ValidationError(
                f"HYGIENE_FINDINGS_TRUNCATED for {code} requires exactly max_findings_per_code explicit findings"
            )


def validate_manifest_limits(
    entries: list[dict[str, Any]],
    parameters: dict[str, Any],
    findings: list[dict[str, Any]],
    *,
    manifest_state: str,
    truncation_counts: dict[str, int] | None = None,
) -> None:
    max_entries = require_positive_int(parameters.get("max_entries"), "hygiene parameters.max_entries")
    max_total_size = require_positive_int(parameters.get("max_total_size"), "hygiene parameters.max_total_size")
    max_entry_size = require_positive_int(parameters.get("max_entry_size"), "hygiene parameters.max_entry_size")
    max_path_depth = require_positive_int(parameters.get("max_path_depth"), "hygiene parameters.max_path_depth")
    max_path_length = require_positive_int(parameters.get("max_path_length"), "hygiene parameters.max_path_length")
    max_symlink_target_size = require_positive_int(
        parameters.get("max_symlink_target_size"),
        "hygiene parameters.max_symlink_target_size",
    )
    max_findings_per_code = require_positive_int(
        parameters.get("max_findings_per_code"),
        "hygiene parameters.max_findings_per_code",
    )
    truncation_counts = truncation_counts or {}
    validate_truncation_marker(findings, truncation_counts, max_findings_per_code=max_findings_per_code)
    if len(entries) > max_entries:
        raise ValidationError("manifest entry count exceeds recorded hygiene limit")
    total_size = 0
    path_too_long_warning_paths: list[str] = []
    for idx, item in enumerate(findings):
        if item.get("code") != "PATH_TOO_LONG":
            continue
        if item.get("severity") != "warning":
            raise ValidationError("PATH_TOO_LONG must use warning severity")
        paths = item.get("paths")
        if not isinstance(paths, list) or len(paths) != 1 or not isinstance(paths[0], str):
            raise ValidationError(f"PATH_TOO_LONG finding[{idx}] must bind exactly one manifest path")
        path_too_long_warning_paths.append(paths[0])
    if len(path_too_long_warning_paths) != len(set(path_too_long_warning_paths)):
        raise ValidationError("PATH_TOO_LONG findings must bind distinct manifest paths")
    actual_too_long_paths: list[str] = []
    for idx, entry in enumerate(entries, start=2):
        path = str(entry.get("path"))
        if path_depth(path) > max_path_depth:
            raise ValidationError(f"manifest line {idx} path depth exceeds recorded hygiene limit")
        if len(path) > max_path_length:
            actual_too_long_paths.append(path)
        if entry.get("type") == "file":
            size = require_nonnegative_int(entry.get("size"), f"manifest line {idx} size")
            if size > max_entry_size:
                raise ValidationError(f"manifest line {idx} file size exceeds recorded hygiene limit")
            total_size += size
        elif entry.get("type") == "symlink":
            target = require_string(entry.get("target"), f"manifest line {idx} symlink target")
            target_size = len(target.encode("utf-8"))
            if target_size > max_symlink_target_size:
                raise ValidationError(f"manifest line {idx} symlink target exceeds recorded hygiene limit")
            if target_size > max_entry_size:
                raise ValidationError(f"manifest line {idx} symlink target exceeds recorded entry-size limit")
            total_size += target_size
    if total_size > max_total_size:
        raise ValidationError("manifest total logical file size exceeds recorded hygiene limit")
    if manifest_state == "complete":
        expected_paths = sorted(actual_too_long_paths)
        expected_explicit_paths = expected_paths[:max_findings_per_code]
        expected_truncated_count = max(0, len(expected_paths) - max_findings_per_code)
        if sorted(path_too_long_warning_paths) != expected_explicit_paths:
            raise ValidationError("PATH_TOO_LONG findings must exactly match the deterministic over-limit manifest path prefix")
        observed_truncated_count = truncation_counts.get("PATH_TOO_LONG", 0)
        if observed_truncated_count != expected_truncated_count:
            raise ValidationError("PATH_TOO_LONG truncation count does not match deterministic manifest replay")
    elif path_too_long_warning_paths and "PATH_TOO_LONG" in truncation_counts:
        # Unavailable/blob manifests have no tree entries to replay, but the report-size
        # marker still proves the scanner retained the deterministic explicit prefix.
        if len(path_too_long_warning_paths) != max_findings_per_code:
            raise ValidationError("PATH_TOO_LONG truncation marker requires max_findings_per_code explicit findings")


def validate_capture_semantics(envelope: dict[str, Any], *, profile: str) -> None:
    exact_keys(
        envelope,
        {"schema", "capture_id", "observed_at", "producer", "source", "observation", "snapshot", "change", "inspection_refs", "fidelity", "raw_handling"},
        {"schema", "capture_id", "observed_at", "producer", "source", "resolution", "observation", "snapshot", "change", "inspection_refs", "fidelity", "raw_handling"},
        "capture envelope",
    )
    if envelope.get("schema") != "urn:vaks:schema:source-capture:v1":
        raise ValidationError("capture envelope schema mismatch")
    capture_id = envelope.get("capture_id")
    if not isinstance(capture_id, str) or not CAPTURE_ID_RE.match(capture_id):
        raise ValidationError("capture_id must be a valid urn:uuid")
    parse_datetime(envelope.get("observed_at"), "observed_at")
    strict = profile == "enterprise-alpha1"
    producer = envelope.get("producer")
    producer_required = {"id", "version", "implementation"} if strict else {"id", "version"}
    exact_keys(producer, producer_required, {"id", "version", "implementation"}, "producer")
    require_string(producer.get("id"), "producer.id")
    require_string(producer.get("version"), "producer.version")
    if "implementation" in producer:
        validate_descriptor(producer.get("implementation"), "producer.implementation")
        if producer["implementation"]["media_type"] != IMPLEMENTATION_MEDIA_TYPE:
            raise ValidationError("producer.implementation.media_type is invalid")

    source = envelope.get("source")
    exact_keys(source, {"source_id", "kind", "requested_locator"}, {"source_id", "kind", "requested_locator", "resolved_locator"}, "source")
    source_id = source.get("source_id")
    if not isinstance(source_id, str) or not SOURCE_ID_RE.match(source_id):
        raise ValidationError("source.source_id must be a stable vsrc:1 ID without whitespace or control characters")
    if source.get("kind") not in SOURCE_KINDS:
        raise ValidationError("source.kind is invalid")
    require_string(source.get("requested_locator"), "source.requested_locator")
    if "resolved_locator" in source:
        require_string(source.get("resolved_locator"), "source.resolved_locator")

    resolution = envelope.get("resolution")
    if "resolution" in envelope and not isinstance(resolution, dict):
        raise ValidationError("resolution must be an object when present")
    if resolution is not None:
        exact_keys(resolution, set(), {"selector", "revision"}, "resolution")
    if isinstance(resolution, dict) and "selector" in resolution:
        selector = resolution.get("selector")
        exact_keys(selector, {"kind", "value"}, {"kind", "value"}, "resolution.selector")
        require_string(selector.get("kind"), "resolution.selector.kind")
        if not isinstance(selector.get("value"), str):
            raise ValidationError("resolution.selector.value must be a string")
    if isinstance(resolution, dict) and "revision" in resolution:
        revision = resolution.get("revision")
        exact_keys(revision, {"kind", "value"}, {"kind", "value"}, "resolution.revision")
        if revision.get("kind") not in REVISION_KINDS:
            raise ValidationError("resolution.revision.kind is not a v1 enum value")
        require_string(revision.get("value"), "resolution.revision.value")

    observation = envelope.get("observation")
    observation_required = {"state", "capture_method", "blob", "content_type"} if strict else {"state", "capture_method", "blob"}
    exact_keys(observation, observation_required, {"state", "capture_method", "blob", "content_type"}, "observation")
    if observation.get("state") not in OBSERVATION_STATES:
        raise ValidationError("observation.state is invalid")
    if observation.get("capture_method") not in CAPTURE_METHODS:
        raise ValidationError("observation.capture_method is invalid")
    validate_descriptor(observation.get("blob"), "observation.blob")
    if "content_type" in observation:
        validate_content_type(observation.get("content_type"), observation["blob"].get("media_type"), strict=strict)

    snapshot = envelope.get("snapshot")
    exact_keys(snapshot, {"snapshot_id", "kind"}, {"snapshot_id", "kind", "manifest"}, "snapshot")
    snapshot_kind = snapshot.get("kind")
    if snapshot_kind not in {"tree", "blob"}:
        raise ValidationError("snapshot.kind is invalid")
    snapshot_id = require_string(snapshot.get("snapshot_id"), "snapshot.snapshot_id")
    if snapshot_kind == "tree":
        if not snapshot_id.startswith("vsnap:1:tree:"):
            raise ValidationError("tree snapshot_id must use vsnap:1:tree")
        validate_descriptor(snapshot.get("manifest"), "snapshot.manifest")
    elif snapshot_kind == "blob":
        if not snapshot_id.startswith("vsnap:1:blob:"):
            raise ValidationError("blob snapshot_id must use vsnap:1:blob")
        if "manifest" in snapshot:
            raise ValidationError("blob snapshot must not carry snapshot.manifest")

    change = envelope.get("change")
    exact_keys(change, {"state", "compared_to_capture_id"}, {"state", "compared_to_capture_id"}, "change")
    change_state = change.get("state")
    if change_state not in CHANGE_STATES:
        raise ValidationError("change.state is invalid")
    previous = change.get("compared_to_capture_id")
    if change_state == "first_seen" and previous is not None:
        raise ValidationError("change.first_seen must not carry compared_to_capture_id")
    if change_state in {"same_snapshot", "new_snapshot"}:
        if not isinstance(previous, str) or not CAPTURE_ID_RE.match(previous):
            raise ValidationError("change.same_snapshot/new_snapshot require a valid compared_to_capture_id")
    if change_state == "unknown" and previous is not None:
        raise ValidationError("change.unknown must not carry compared_to_capture_id")

    fidelity = envelope.get("fidelity")
    exact_keys(fidelity, {"state"}, {"state", "profile", "compared_to"}, "fidelity")
    fidelity_state = fidelity.get("state")
    if fidelity_state in {"matched", "mismatch", "partial"}:
        require_string(fidelity.get("profile"), "fidelity.profile")
        compared_to = fidelity.get("compared_to")
        exact_keys(compared_to, {"kind", "digest"}, {"kind", "digest", "media_type", "size"}, "fidelity.compared_to")
        require_string(compared_to.get("kind"), "fidelity.compared_to.kind")
        require_string(compared_to.get("digest"), "fidelity.compared_to.digest", pattern=ALGORITHM_DIGEST_RE)
        if "media_type" in compared_to:
            require_string(compared_to.get("media_type"), "fidelity.compared_to.media_type")
        if "size" in compared_to:
            require_nonnegative_int(compared_to.get("size"), "fidelity.compared_to.size")
    elif fidelity_state == "not_checked":
        if "profile" in fidelity or "compared_to" in fidelity:
            raise ValidationError("fidelity.not_checked must not carry profile or compared_to")
    else:
        raise ValidationError("fidelity.state is invalid")

    inspection_refs = envelope.get("inspection_refs")
    if not isinstance(inspection_refs, list) or not inspection_refs:
        raise ValidationError("inspection_refs must be a non-empty list")
    for idx, inspection_ref in enumerate(inspection_refs):
        exact_keys(
            inspection_ref,
            {"media_type", "size", "digest", "predicate_type"},
            {"media_type", "size", "digest", "predicate_type"},
            f"inspection_refs[{idx}]",
        )
        if inspection_ref.get("media_type") != "application/vnd.in-toto+json":
            raise ValidationError(f"inspection_refs[{idx}].media_type is invalid")
        require_nonnegative_int(inspection_ref.get("size"), f"inspection_refs[{idx}].size")
        require_digest(inspection_ref.get("digest"), f"inspection_refs[{idx}].digest")
        if inspection_ref.get("predicate_type") not in HYGIENE_PREDICATES:
            raise ValidationError(f"inspection_refs[{idx}].predicate_type is invalid")

    raw = envelope.get("raw_handling")
    exact_keys(raw, {"disposition", "policy", "reason_codes"}, {"disposition", "policy", "reason_codes"}, "raw_handling")
    if raw.get("disposition") not in RAW_DISPOSITIONS:
        raise ValidationError("raw_handling.disposition is invalid")
    policy = raw.get("policy")
    policy_required = {"id", "digest"} if strict else {"id"}
    exact_keys(policy, policy_required, {"id", "digest"}, "raw_handling.policy")
    require_string(policy.get("id"), "raw_handling.policy.id")
    if "digest" in policy:
        require_digest(policy.get("digest"), "raw_handling.policy.digest")
    reason_codes = raw.get("reason_codes")
    if not isinstance(reason_codes, list):
        raise ValidationError("raw_handling.reason_codes must be a list")
    for idx, code in enumerate(reason_codes):
        require_string(code, f"raw_handling.reason_codes[{idx}]")


def validate_descriptor(descriptor: Any, context: str) -> None:
    exact_keys(descriptor, {"media_type", "size", "digest"}, {"media_type", "size", "digest"}, context)
    require_string(descriptor.get("media_type"), f"{context}.media_type")
    require_nonnegative_int(descriptor.get("size"), f"{context}.size")
    require_digest(descriptor.get("digest"), f"{context}.digest")


def validate_content_type(content_type: Any, blob_media_type: Any, *, strict: bool) -> None:
    exact_keys(
        content_type,
        {"profile", "detected_media_type", "detection_basis", "hint_match"},
        {"profile", "detected_media_type", "detection_basis", "locator_hint_media_type", "hint_match"},
        "observation.content_type",
    )
    if content_type.get("profile") != CONTENT_TYPE_PROFILE:
        raise ValidationError("observation.content_type.profile is invalid")
    detected = require_string(content_type.get("detected_media_type"), "observation.content_type.detected_media_type")
    if detected != blob_media_type:
        raise ValidationError("observation.blob.media_type must match observation.content_type.detected_media_type")
    detection_basis = content_type.get("detection_basis")
    if detection_basis not in CONTENT_TYPE_BASIS:
        raise ValidationError("observation.content_type.detection_basis is invalid")
    hint_match = content_type.get("hint_match")
    if hint_match not in CONTENT_TYPE_HINT_MATCH:
        raise ValidationError("observation.content_type.hint_match is invalid")
    if strict and detection_basis == "locator_hint":
        raise ValidationError("observation.content_type.detection_basis=locator_hint is not supported by enterprise-alpha1")
    if strict and hint_match == "not_comparable":
        raise ValidationError("observation.content_type.hint_match=not_comparable is not supported by enterprise-alpha1")
    if strict:
        if detection_basis == "container_parser" and detected not in ARCHIVE_MEDIA_TYPES:
            raise ValidationError("observation.content_type.detection_basis=container_parser requires an archive media type")
        if detection_basis == "magic_signature" and detected != "application/pdf":
            raise ValidationError("observation.content_type.detection_basis=magic_signature requires application/pdf")
        if detection_basis == "fallback" and detected != "application/octet-stream":
            raise ValidationError("observation.content_type.detection_basis=fallback requires application/octet-stream")
    locator_hint = content_type.get("locator_hint_media_type")
    if "locator_hint_media_type" in content_type:
        locator_hint = require_string(content_type.get("locator_hint_media_type"), "observation.content_type.locator_hint_media_type")
    if hint_match == "matched":
        if locator_hint is None or locator_hint != detected:
            raise ValidationError("observation.content_type.hint_match=matched requires locator_hint_media_type equal to detected_media_type")
    elif hint_match == "mismatch":
        if locator_hint is None or locator_hint == detected:
            raise ValidationError("observation.content_type.hint_match=mismatch requires a differing locator_hint_media_type")
    elif hint_match == "no_hint":
        if locator_hint is not None:
            raise ValidationError("observation.content_type.hint_match=no_hint must not carry locator_hint_media_type")
    elif hint_match == "not_comparable":
        if locator_hint is None:
            raise ValidationError("observation.content_type.hint_match=not_comparable requires locator_hint_media_type")


def validate_hygiene_semantics(hygiene: dict[str, Any], *, profile: str) -> None:
    exact_keys(hygiene, {"_type", "subject", "predicateType", "predicate"}, {"_type", "subject", "predicateType", "predicate"}, "hygiene statement")
    if hygiene.get("_type") != "https://in-toto.io/Statement/v1":
        raise ValidationError("hygiene _type is invalid")
    if hygiene.get("predicateType") not in HYGIENE_PREDICATES:
        raise ValidationError("hygiene predicateType is not a supported v1 predicate")
    subjects = hygiene.get("subject")
    if not isinstance(subjects, list) or len(subjects) != 1:
        raise ValidationError("hygiene subject must contain exactly one subject in v1")
    subject = subjects[0]
    exact_keys(subject, {"name", "digest"}, {"name", "digest"}, "hygiene subject[0]")
    if subject.get("name") not in {"snapshot-manifest", "capture-blob"}:
        raise ValidationError("hygiene subject[0].name is invalid")
    digest_obj = subject.get("digest")
    exact_keys(digest_obj, {"sha256"}, {"sha256"}, "hygiene subject[0].digest")
    require_string(digest_obj.get("sha256"), "hygiene subject[0].digest.sha256", pattern=re.compile(r"^[0-9a-f]{64}$"))
    predicate = hygiene.get("predicate")
    strict = profile == "enterprise-alpha1"
    exact_keys(predicate, {"checker", "execution_state", "profiles", "parameters", "summary", "findings"}, {"checker", "execution_state", "profiles", "parameters", "summary", "findings"}, "hygiene predicate")
    checker = predicate.get("checker")
    checker_required = {"id", "version", "implementation"} if strict else {"id", "version"}
    exact_keys(checker, checker_required, {"id", "version", "implementation"}, "hygiene predicate.checker")
    require_string(checker.get("id"), "hygiene predicate.checker.id")
    require_string(checker.get("version"), "hygiene predicate.checker.version")
    if "implementation" in checker:
        validate_descriptor(checker.get("implementation"), "hygiene predicate.checker.implementation")
        if checker["implementation"]["media_type"] != IMPLEMENTATION_MEDIA_TYPE:
            raise ValidationError("hygiene predicate.checker.implementation.media_type is invalid")
    execution_state = predicate.get("execution_state")
    profiles = predicate.get("profiles")
    parameters = predicate.get("parameters")
    findings = predicate.get("findings")
    parameter_keys = REQUIRED_PARAMETER_KEYS | (ENTERPRISE_PARAMETER_KEYS if strict else set())
    if not isinstance(parameters, dict) or set(parameters) - (REQUIRED_PARAMETER_KEYS | ENTERPRISE_PARAMETER_KEYS) or not REQUIRED_PARAMETER_KEYS.issubset(parameters):
        raise ValidationError("hygiene predicate.parameters must record the effective v1 limit parameters")
    if strict and set(parameters) != parameter_keys:
        raise ValidationError("enterprise-alpha1 hygiene parameters must include max_input_blob_size")
    if parameters.get("limits_profile") != "vaks-default-archive-limits/v1":
        raise ValidationError("hygiene parameters.limits_profile is invalid")
    for key in REQUIRED_PARAMETER_KEYS - {"limits_profile", "max_compression_ratio"}:
        require_positive_int(parameters.get(key), f"hygiene parameters.{key}")
    if strict and parameters.get("max_findings_per_code") != PINNED_MAX_FINDINGS_PER_CODE:
        raise ValidationError("enterprise-alpha1 requires hygiene parameters.max_findings_per_code = 100")
    if "max_input_blob_size" in parameters:
        require_positive_int(parameters.get("max_input_blob_size"), "hygiene parameters.max_input_blob_size")
    if (
        type(parameters.get("max_compression_ratio")) not in {int, float}
        or not math.isfinite(parameters["max_compression_ratio"])
        or parameters["max_compression_ratio"] <= 0
    ):
        raise ValidationError("hygiene parameters.max_compression_ratio must be positive")
    if not isinstance(profiles, list) or len(profiles) != len(set(profiles)) or any(profile not in HYGIENE_PROFILES for profile in profiles):
        raise ValidationError("hygiene profiles must use allowed v1 profile IDs")
    if not isinstance(findings, list):
        raise ValidationError("hygiene findings must be a list")
    for idx, finding in enumerate(findings):
        exact_keys(finding, {"code", "severity", "profile", "message"}, {"code", "severity", "profile", "message", "paths", "details"}, f"hygiene finding[{idx}]")
        require_string(finding.get("code"), f"hygiene finding[{idx}].code")
        if finding.get("severity") not in {"info", "warning", "hazard", "error"}:
            raise ValidationError("hygiene finding severity must use an allowed v1 enum")
        if finding.get("profile") not in HYGIENE_PROFILES:
            raise ValidationError("hygiene finding profile must use an allowed v1 profile ID")
        require_string(finding.get("message"), f"hygiene finding[{idx}].message")
        if "paths" in finding:
            if not isinstance(finding["paths"], list):
                raise ValidationError(f"hygiene finding[{idx}].paths must be a list")
            for path_idx, path in enumerate(finding["paths"]):
                require_string(path, f"hygiene finding[{idx}].paths[{path_idx}]", non_blank=False)
        if "details" in finding and not isinstance(finding["details"], dict):
            raise ValidationError(f"hygiene finding[{idx}].details must be an object")
    summary = predicate.get("summary")
    exact_keys(summary, {"finding_count", "max_severity"}, {"finding_count", "max_severity"}, "hygiene summary")
    require_nonnegative_int(summary.get("finding_count"), "hygiene summary.finding_count")
    if summary.get("max_severity") not in SEVERITY_ORDER:
        raise ValidationError("hygiene summary.max_severity is invalid")
    if execution_state == "not_run":
        if profiles or findings:
            raise ValidationError("hygiene not_run must not carry profiles or findings")
    elif execution_state in {"complete", "partial", "failed"}:
        if not profiles:
            raise ValidationError("hygiene complete/partial/failed must carry at least one profile")
        if execution_state in {"partial", "failed"} and not findings:
            raise ValidationError("hygiene partial/failed must carry findings")
    else:
        raise ValidationError("hygiene execution_state is invalid")


def load_policy(policy_file: Path | None) -> dict[str, Any] | None:
    if policy_file is None:
        return None
    policy = read_json(policy_file)
    exact_keys(policy, {"schema", "id", "version", "unsafe_finding", "decision"}, {"schema", "id", "version", "unsafe_finding", "decision"}, "policy")
    if policy.get("schema") != "urn:vaks:policy:raw-intake:v1":
        raise ValidationError("policy schema mismatch")
    require_string(policy.get("id"), "policy.id")
    require_string(policy.get("version"), "policy.version")
    unsafe = policy.get("unsafe_finding")
    exact_keys(unsafe, {"severities", "codes"}, {"severities", "codes"}, "policy.unsafe_finding")
    severities = unsafe.get("severities")
    codes = unsafe.get("codes")
    if not isinstance(severities, list) or not severities or any(item not in {"info", "warning", "hazard", "error"} for item in severities):
        raise ValidationError("policy unsafe severities are invalid")
    if not isinstance(codes, list) or not codes or any(not isinstance(item, str) or not item.strip() for item in codes):
        raise ValidationError("policy unsafe codes are invalid")
    if len(codes) != len(set(codes)) or len(severities) != len(set(severities)):
        raise ValidationError("policy unsafe codes/severities must be unique")
    if not {"hazard", "error"}.issubset(set(severities)):
        raise ValidationError("policy unsafe severities must include hazard and error")
    decision = policy.get("decision")
    exact_keys(decision, {"unsafe", "complete_without_unsafe"}, {"unsafe", "complete_without_unsafe"}, "policy.decision")
    if decision.get("unsafe") != "quarantined" or decision.get("complete_without_unsafe") != "admitted":
        raise ValidationError("policy decision is not supported by alpha.1")
    policy["_canonical_digest"] = sha256_bytes(canonical_json_bytes(policy_without_internal_keys(policy)))
    return policy


def policy_without_internal_keys(policy: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in policy.items() if not key.startswith("_")}


def validate_bundle(
    bundle: Path,
    *,
    profile: str = "base",
    policy_file: Path | None = None,
    implementation_manifest: Path | None = None,
) -> dict[str, Any]:
    if profile not in VALIDATOR_PROFILES:
        raise ValidationError(f"unsupported validator profile: {profile}")
    strict = profile == "enterprise-alpha1"
    implementation = load_implementation_manifest(implementation_manifest or default_implementation_manifest_path()) if strict else None
    policy = load_policy(policy_file)
    envelope_path = require_file(bundle, "capture-envelope.json")
    manifest_path = require_file(bundle, "snapshot-manifest.jsonl")
    hygiene_path = require_file(bundle, "snapshot-hygiene.intoto.json")

    envelope = read_json(envelope_path)
    hygiene = read_json(hygiene_path)
    validate_capture_semantics(envelope, profile=profile)
    validate_hygiene_semantics(hygiene, profile=profile)
    manifest_rows, manifest_bytes = parse_manifest(manifest_path)
    manifest_state, manifest_entries = validate_manifest_rows(manifest_rows)

    snapshot = envelope.get("snapshot")
    if not isinstance(snapshot, dict):
        raise ValidationError("capture envelope snapshot must be an object")
    observation = envelope.get("observation")
    if not isinstance(observation, dict) or not isinstance(observation.get("blob"), dict):
        raise ValidationError("capture envelope observation.blob must be an object")
    snapshot_kind = snapshot.get("kind")
    source = envelope.get("source") if isinstance(envelope.get("source"), dict) else {}
    observation_state = observation.get("state")
    capture_method = observation.get("capture_method")
    archive_intent = source.get("kind") == "archive" or capture_method in {"provider_archive", "archive_file"}
    raw_handling = envelope.get("raw_handling") if isinstance(envelope.get("raw_handling"), dict) else {}
    disposition = raw_handling.get("disposition")
    reason_codes_list = raw_handling.get("reason_codes", []) if isinstance(raw_handling.get("reason_codes"), list) else []
    reason_codes = set(reason_codes_list)
    raw_policy = raw_handling.get("policy") if isinstance(raw_handling.get("policy"), dict) else {}
    if profile == "enterprise-alpha1":
        if policy is None:
            raise ValidationError("enterprise-alpha1 validation requires --policy-file")
        if raw_policy.get("id") != policy.get("id"):
            raise ValidationError("raw_handling.policy.id does not match policy file")
        if raw_policy.get("digest") != policy.get("_canonical_digest"):
            raise ValidationError("raw_handling.policy.digest does not match policy file")
    predicate = hygiene.get("predicate")
    if not isinstance(predicate, dict):
        raise ValidationError("hygiene predicate must be an object")
    hygiene_state = predicate.get("execution_state")
    hygiene_parameters = predicate.get("parameters")
    if not isinstance(hygiene_parameters, dict):
        raise ValidationError("hygiene parameters are missing")
    if "max_input_blob_size" in hygiene_parameters:
        blob_size = observation["blob"].get("size")
        if type(blob_size) is not int or blob_size > hygiene_parameters["max_input_blob_size"]:
            raise ValidationError("observation.blob.size exceeds recorded max_input_blob_size")
    if profile == "enterprise-alpha1":
        producer_impl = envelope.get("producer", {}).get("implementation") if isinstance(envelope.get("producer"), dict) else None
        checker_impl = predicate.get("checker", {}).get("implementation") if isinstance(predicate.get("checker"), dict) else None
        if producer_impl != checker_impl:
            raise ValidationError("producer/checker implementation descriptors must match")
        if producer_impl != implementation["descriptor"]:
            raise ValidationError("producer/checker implementation descriptor does not match implementation manifest")
        try:
            policy_rel = str(Path(policy_file).resolve().relative_to(implementation["root"])).replace("\\", "/")
        except ValueError as exc:
            raise ValidationError("enterprise policy file must be under the implementation root") from exc
        if policy_rel != POLICY_COMPONENT_PATH:
            raise ValidationError("enterprise policy file must be the implementation-pinned policy component")
        if digest_file(Path(policy_file)) != implementation["component_digests"][POLICY_COMPONENT_PATH]:
            raise ValidationError("enterprise policy file digest does not match implementation manifest policy component")
    predicate = hygiene.get("predicate")
    findings_for_limits = predicate.get("findings") if isinstance(predicate, dict) and isinstance(predicate.get("findings"), list) else []
    truncation_counts = truncation_counts_by_code(findings_for_limits)
    validate_manifest_limits(
        manifest_entries,
        hygiene_parameters,
        findings_for_limits,
        manifest_state=manifest_state,
        truncation_counts=truncation_counts,
    )
    manifest_digest = sha256_bytes(manifest_bytes)
    if snapshot_kind == "tree":
        if manifest_state != "complete":
            raise ValidationError("tree snapshot requires manifest.state = complete")
        if disposition != "admitted":
            raise ValidationError("tree snapshot requires raw_handling.disposition = admitted")
        if observation.get("state") != "captured":
            raise ValidationError("tree snapshot requires observation.state = captured")
        if hygiene_state != "complete":
            raise ValidationError("tree snapshot requires hygiene.execution_state = complete")
        manifest_descriptor = snapshot.get("manifest")
        if not isinstance(manifest_descriptor, dict):
            raise ValidationError("tree snapshot requires snapshot.manifest descriptor")
        descriptor_matches(manifest_path, manifest_descriptor, "snapshot.manifest")
        expected_snapshot_id = "vsnap:1:tree:" + manifest_digest
        if snapshot.get("snapshot_id") != expected_snapshot_id:
            raise ValidationError(f"snapshot_id mismatch: expected {expected_snapshot_id}")
        expected_subject = manifest_digest
        expected_subject_name = "snapshot-manifest"
    elif snapshot_kind == "blob":
        if disposition in {"admitted", "not_evaluated"} and manifest_state != "blob":
            raise ValidationError("admitted/not_evaluated blob snapshot requires manifest.state = blob")
        if disposition in {"quarantined", "rejected"} and manifest_state != "unavailable":
            raise ValidationError("quarantined/rejected blob snapshot requires manifest.state = unavailable")
        if archive_intent and disposition in {"admitted", "not_evaluated"}:
            raise ValidationError("archive-intent captures must not produce admitted/not_evaluated blob snapshots")
        if disposition == "admitted":
            if observation_state != "captured":
                raise ValidationError("admitted blob snapshot requires observation.state = captured")
            if hygiene_state != "complete":
                raise ValidationError("admitted blob snapshot requires hygiene.execution_state = complete")
        if disposition == "not_evaluated" and hygiene_state != "not_run":
            raise ValidationError("not_evaluated blob snapshot requires hygiene.execution_state = not_run")
        if disposition in {"quarantined", "rejected"}:
            if hygiene_state not in {"partial", "failed"}:
                raise ValidationError("quarantined/rejected blob snapshot requires partial or failed hygiene")
            if observation_state not in {"partial", "failed"}:
                raise ValidationError("quarantined/rejected blob snapshot requires partial or failed observation")
        if manifest_state == "unavailable":
            manifest_reasons = set(manifest_rows[0].get("reason_codes", []))
            if manifest_reasons != reason_codes:
                raise ValidationError("unavailable manifest reason_codes must match raw_handling.reason_codes")
        blob_digest = observation["blob"].get("digest")
        expected_snapshot_id = "vsnap:1:blob:" + blob_digest
        if snapshot.get("snapshot_id") != expected_snapshot_id:
            raise ValidationError(f"blob snapshot_id mismatch: expected {expected_snapshot_id}")
        expected_subject = blob_digest
        expected_subject_name = "capture-blob"
    else:
        raise ValidationError(f"unsupported snapshot.kind: {snapshot_kind}")

    inspection_refs = envelope.get("inspection_refs")
    if not isinstance(inspection_refs, list) or len(inspection_refs) != 1:
        raise ValidationError("capture envelope must include exactly one hygiene inspection_ref in v1")
    inspection_ref = inspection_refs[0]
    if not isinstance(inspection_ref, dict):
        raise ValidationError("inspection_ref must be an object")
    descriptor_matches(hygiene_path, inspection_ref, "inspection_refs[0]")
    if inspection_ref.get("predicate_type") != hygiene.get("predicateType"):
        raise ValidationError("inspection_ref predicate_type must match hygiene predicateType")
    expected_predicate = (
        "urn:vaks:predicate:repo-snapshot-hygiene:v1"
        if source.get("kind") == "repo"
        else "urn:vaks:predicate:source-snapshot-hygiene:v1"
    )
    if hygiene.get("predicateType") != expected_predicate:
        raise ValidationError("hygiene predicateType must match envelope source.kind")

    subjects = hygiene.get("subject")
    if not isinstance(subjects, list) or not subjects:
        raise ValidationError("hygiene subject is missing")
    if subjects[0].get("name") != expected_subject_name:
        raise ValidationError("hygiene subject name does not match snapshot kind")
    subject_digest = subjects[0].get("digest", {}).get("sha256")
    if "sha256:" + str(subject_digest) != expected_subject:
        raise ValidationError("hygiene subject digest does not bind to the expected snapshot/blob digest")

    findings = predicate.get("findings")
    if not isinstance(findings, list):
        raise ValidationError("hygiene findings must be a list")
    summary = predicate.get("summary")
    if not isinstance(summary, dict):
        raise ValidationError("hygiene summary must be an object")
    if summary.get("finding_count") != len(findings):
        raise ValidationError("hygiene finding_count does not match findings length")
    if summary.get("max_severity") != computed_max_severity(findings):
        raise ValidationError("hygiene max_severity does not match findings")

    finding_codes = {item.get("code") for item in findings}
    finding_pairs = {(item.get("code"), item.get("severity")) for item in findings}
    content_type = observation.get("content_type") if isinstance(observation.get("content_type"), dict) else {}
    detected_media_type = content_type.get("detected_media_type")
    if source.get("kind") == "pdf" and detected_media_type != "application/pdf":
        if ("SOURCE_KIND_FORMAT_MISMATCH", "hazard") not in finding_pairs:
            raise ValidationError("source.kind=pdf with non-PDF detected media type requires SOURCE_KIND_FORMAT_MISMATCH hazard finding")
    if content_type.get("hint_match") == "mismatch":
        if ("MEDIA_TYPE_HINT_MISMATCH", "warning") not in finding_pairs:
            raise ValidationError("media-type hint mismatch requires MEDIA_TYPE_HINT_MISMATCH warning finding")

    if policy is not None:
        unsafe_codes = set(policy["unsafe_finding"]["codes"])
        unsafe_severities = set(policy["unsafe_finding"]["severities"])
        policy_unsafe_codes = sorted(
            {
                item.get("code")
                for item in findings
                if item.get("code") in unsafe_codes or item.get("severity") in unsafe_severities
            }
            | {code for code in truncation_counts if code in unsafe_codes}
        )
        hazard_codes = set(policy_unsafe_codes)
        expected_disposition = policy["decision"]["unsafe"] if policy_unsafe_codes else policy["decision"]["complete_without_unsafe"]
        if disposition != expected_disposition:
            raise ValidationError("raw_handling.disposition does not match policy replay")
        if sorted(reason_codes_list) != policy_unsafe_codes:
            raise ValidationError("raw_handling.reason_codes must exactly match policy-unsafe finding codes")
    else:
        hazard_codes = {item.get("code") for item in findings if item.get("severity") in {"hazard", "error"}}
    if disposition in {"admitted", "not_evaluated"} and reason_codes:
        raise ValidationError("admitted/not_evaluated raw handling must not carry reason_codes")
    if hazard_codes:
        if disposition != "quarantined":
            raise ValidationError("hazard/error findings require raw_handling.disposition = quarantined")
        if not hazard_codes.issubset(reason_codes):
            raise ValidationError("hazard/error findings must be included in raw_handling.reason_codes")

    profiles = predicate.get("profiles")
    detection_basis = content_type.get("detection_basis")
    if strict:
        if snapshot_kind == "tree":
            if detection_basis != "container_parser":
                raise ValidationError("tree snapshots require observation.content_type.detection_basis=container_parser")
            if detected_media_type not in ARCHIVE_MEDIA_TYPES:
                raise ValidationError("tree snapshots require an archive detected media type")
        if snapshot_kind == "blob" and disposition == "admitted" and detection_basis == "container_parser":
            raise ValidationError("admitted blob snapshots must not use observation.content_type.detection_basis=container_parser")
        if detection_basis == "container_parser" and "archive-safety/v1" not in profiles:
            raise ValidationError("container_parser captures must carry archive-safety/v1 hygiene profile")
    if (archive_intent or snapshot_kind == "tree") and "archive-safety/v1" not in profiles:
        raise ValidationError("archive/tree captures must carry archive-safety/v1 hygiene profile")

    return {
        "status": "pass",
        "bundle": str(bundle),
        "snapshot_id": snapshot.get("snapshot_id"),
        "finding_count": len(findings),
        "max_severity": summary.get("max_severity"),
        "raw_disposition": disposition,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a Source Capture Envelope v1 bundle.")
    parser.add_argument("bundle_dir")
    parser.add_argument("--profile", default="base", choices=sorted(VALIDATOR_PROFILES))
    parser.add_argument("--policy-file")
    parser.add_argument("--implementation-manifest", default=str(default_implementation_manifest_path()))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = validate_bundle(
            Path(args.bundle_dir),
            profile=args.profile,
            policy_file=Path(args.policy_file) if args.policy_file else None,
            implementation_manifest=Path(args.implementation_manifest) if args.implementation_manifest else None,
        )
    except ValidationError as exc:
        print(json.dumps({"status": "fail", "error": str(exc)}, allow_nan=False, sort_keys=True))
        return 1
    print(json.dumps(result, allow_nan=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
