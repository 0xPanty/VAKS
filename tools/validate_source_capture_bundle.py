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
MAX_MANIFEST_BYTES = 64 * 1024 * 1024
MAX_HYGIENE_BYTES = 16 * 1024 * 1024
MAX_MANIFEST_ENTRIES = 100_000
MAX_STRING_LENGTH = 16_384
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


def validate_manifest_limits(entries: list[dict[str, Any]], parameters: dict[str, Any]) -> None:
    max_entries = require_positive_int(parameters.get("max_entries"), "hygiene parameters.max_entries")
    max_total_size = require_positive_int(parameters.get("max_total_size"), "hygiene parameters.max_total_size")
    max_entry_size = require_positive_int(parameters.get("max_entry_size"), "hygiene parameters.max_entry_size")
    max_path_depth = require_positive_int(parameters.get("max_path_depth"), "hygiene parameters.max_path_depth")
    max_path_length = require_positive_int(parameters.get("max_path_length"), "hygiene parameters.max_path_length")
    max_symlink_target_size = require_positive_int(
        parameters.get("max_symlink_target_size"),
        "hygiene parameters.max_symlink_target_size",
    )
    if len(entries) > max_entries:
        raise ValidationError("manifest entry count exceeds recorded hygiene limit")
    total_size = 0
    for idx, entry in enumerate(entries, start=2):
        path = str(entry.get("path"))
        if path_depth(path) > max_path_depth:
            raise ValidationError(f"manifest line {idx} path depth exceeds recorded hygiene limit")
        if len(path) > max_path_length:
            raise ValidationError(f"manifest line {idx} path length exceeds recorded hygiene limit")
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


def validate_capture_semantics(envelope: dict[str, Any]) -> None:
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
    producer = envelope.get("producer")
    exact_keys(producer, {"id", "version"}, {"id", "version"}, "producer")
    require_string(producer.get("id"), "producer.id")
    require_string(producer.get("version"), "producer.version")

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
    exact_keys(observation, {"state", "capture_method", "blob"}, {"state", "capture_method", "blob"}, "observation")
    if observation.get("state") not in OBSERVATION_STATES:
        raise ValidationError("observation.state is invalid")
    if observation.get("capture_method") not in CAPTURE_METHODS:
        raise ValidationError("observation.capture_method is invalid")
    validate_descriptor(observation.get("blob"), "observation.blob")

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
    exact_keys(policy, {"id"}, {"id", "digest"}, "raw_handling.policy")
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


def validate_hygiene_semantics(hygiene: dict[str, Any]) -> None:
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
    exact_keys(predicate, {"checker", "execution_state", "profiles", "parameters", "summary", "findings"}, {"checker", "execution_state", "profiles", "parameters", "summary", "findings"}, "hygiene predicate")
    checker = predicate.get("checker")
    exact_keys(checker, {"id", "version"}, {"id", "version"}, "hygiene predicate.checker")
    require_string(checker.get("id"), "hygiene predicate.checker.id")
    require_string(checker.get("version"), "hygiene predicate.checker.version")
    execution_state = predicate.get("execution_state")
    profiles = predicate.get("profiles")
    parameters = predicate.get("parameters")
    findings = predicate.get("findings")
    if not isinstance(parameters, dict) or set(parameters) != REQUIRED_PARAMETER_KEYS:
        raise ValidationError("hygiene predicate.parameters must record the effective v1 limit parameters")
    if parameters.get("limits_profile") != "vaks-default-archive-limits/v1":
        raise ValidationError("hygiene parameters.limits_profile is invalid")
    for key in REQUIRED_PARAMETER_KEYS - {"limits_profile", "max_compression_ratio"}:
        require_positive_int(parameters.get(key), f"hygiene parameters.{key}")
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


def validate_bundle(bundle: Path) -> dict[str, Any]:
    envelope_path = require_file(bundle, "capture-envelope.json")
    manifest_path = require_file(bundle, "snapshot-manifest.jsonl")
    hygiene_path = require_file(bundle, "snapshot-hygiene.intoto.json")

    envelope = read_json(envelope_path)
    hygiene = read_json(hygiene_path)
    validate_capture_semantics(envelope)
    validate_hygiene_semantics(hygiene)
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
    reason_codes = set(raw_handling.get("reason_codes", [])) if isinstance(raw_handling.get("reason_codes"), list) else set()
    predicate = hygiene.get("predicate")
    if not isinstance(predicate, dict):
        raise ValidationError("hygiene predicate must be an object")
    hygiene_state = predicate.get("execution_state")
    hygiene_parameters = predicate.get("parameters")
    if not isinstance(hygiene_parameters, dict):
        raise ValidationError("hygiene parameters are missing")
    validate_manifest_limits(manifest_entries, hygiene_parameters)
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

    hazard_codes = {item.get("code") for item in findings if item.get("severity") in {"hazard", "error"}}
    if disposition in {"admitted", "not_evaluated"} and reason_codes:
        raise ValidationError("admitted/not_evaluated raw handling must not carry reason_codes")
    if hazard_codes:
        if disposition != "quarantined":
            raise ValidationError("hazard/error findings require raw_handling.disposition = quarantined")
        if not hazard_codes.issubset(reason_codes):
            raise ValidationError("hazard/error findings must be included in raw_handling.reason_codes")

    profiles = predicate.get("profiles")
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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = validate_bundle(Path(args.bundle_dir))
    except ValidationError as exc:
        print(json.dumps({"status": "fail", "error": str(exc)}, allow_nan=False, sort_keys=True))
        return 1
    print(json.dumps(result, allow_nan=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
