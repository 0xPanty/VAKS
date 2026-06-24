#!/usr/bin/env python
"""Inspect a source blob/archive without extracting it.

Produces the three Source Capture Envelope v1 artifacts:
- capture-envelope.json
- snapshot-manifest.jsonl
- snapshot-hygiene.intoto.json

The tool is intentionally read-only with respect to source cards and semantic
layers. It does not access the network, does not follow symlinks, and does not
write candidate/reviewed/action artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import stat
import struct
import tarfile
import tempfile
import unicodedata
import uuid
import zipfile
import zlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import validate_source_capture_bundle


SCHEMA_CAPTURE = "urn:vaks:schema:source-capture:v1"
SCHEMA_MANIFEST = "urn:vaks:schema:snapshot-manifest:v1"
HYGIENE_TYPE = "https://in-toto.io/Statement/v1"
REPO_HYGIENE_PREDICATE = "urn:vaks:predicate:repo-snapshot-hygiene:v1"
SOURCE_HYGIENE_PREDICATE = "urn:vaks:predicate:source-snapshot-hygiene:v1"
INSPECTOR_ID = "vaks.snapshot-inspector"
INSPECTOR_VERSION = "1.0-alpha.1"
IMPLEMENTATION_MEDIA_TYPE = "application/vnd.vaks.source-capture-implementation.v1+json"
IMPLEMENTATION_SCHEMA = "urn:vaks:schema:source-capture-implementation:v1"
IMPLEMENTATION_ID = "vaks.source-capture-envelope"
IMPLEMENTATION_VERSION = "1.0-alpha.1"
POLICY_SCHEMA = "urn:vaks:policy:raw-intake:v1"
POLICY_VERSION = "1.0-alpha.1"
MEDIA_TYPE_DETECTION_PROFILE = "vaks-media-type-detection/v1"
MANIFEST_PROFILE = "vaks-archive-tree/v1"
LIMITS_PROFILE = "vaks-default-archive-limits/v1"
REPO_HYGIENE_PROFILES = [
    "archive-safety/v1",
    "repo-portability/v1",
    "repo-completeness/v1",
]
SOURCE_FIXITY_PROFILE = "source-fixity/v1"
FINDING_SEVERITY_ORDER = {"info": 1, "warning": 2, "hazard": 3, "error": 4}
MAX_FINDINGS_PER_CODE = 100
MAX_FINDING_PATHS = 20
MAX_FINDING_DETAIL_ITEMS = 20
MAX_ARCHIVE_PATH_STRING_LENGTH = 16_384
UNIX_ZIP_CREATE_SYSTEMS = {3, 19}
ZIP_UNICODE_PATH_EXTRA_ID = 0x7075
ZIP_DECOMPRESS_OUTPUT_CHUNK_LIMIT = 1024 * 1024

WINDOWS_RESERVED = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}
WINDOWS_INVALID_RE = re.compile(r'[<>:"\\|?*\x00-\x1f]')
ARCHIVE_SUFFIXES = {
    ".zip",
    ".tar",
    ".tar.gz",
    ".tgz",
    ".tar.bz2",
    ".tbz",
    ".tbz2",
    ".tar.xz",
    ".txz",
    ".gz",
    ".bz2",
    ".xz",
}
SUPPORTED_ZIP_COMPRESSION = {
    zipfile.ZIP_STORED,
    zipfile.ZIP_DEFLATED,
}
REVISION_KINDS = [
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
]
CAPTURE_ID_RE = re.compile(r"^urn:uuid:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$")
SOURCE_ID_RE = re.compile(r"^vsrc:1:[A-Za-z0-9_.-]+:[^\s\x00-\x1f\x7f]+$")
EXPECTED_IMPLEMENTATION_COMPONENTS = {
    "policies/source-capture/raw-intake-default-v1.json",
    "schemas/snapshot-hygiene-v1.schema.json",
    "schemas/source-capture-v1.schema.json",
    "tools/inspect_source_snapshot.py",
    "tools/source_intake_enum_registry.json",
    "tools/validate_source_capture_bundle.py",
}


@dataclass(frozen=True)
class Limits:
    max_input_blob_size: int = 2 * 1024 * 1024 * 1024
    max_entries: int = 50_000
    max_total_size: int = 512 * 1024 * 1024
    max_entry_size: int = 128 * 1024 * 1024
    max_compression_ratio: float = 100.0
    max_path_depth: int = 100
    max_path_length: int = 260
    max_symlink_target_size: int = 4096


def limits_parameters(limits: Limits) -> dict[str, object]:
    return {
        "limits_profile": LIMITS_PROFILE,
        "max_input_blob_size": limits.max_input_blob_size,
        "max_entries": limits.max_entries,
        "max_total_size": limits.max_total_size,
        "max_entry_size": limits.max_entry_size,
        "max_compression_ratio": limits.max_compression_ratio,
        "max_path_depth": limits.max_path_depth,
        "max_path_length": limits.max_path_length,
        "max_symlink_target_size": limits.max_symlink_target_size,
        "max_findings_per_code": MAX_FINDINGS_PER_CODE,
        "max_finding_paths": MAX_FINDING_PATHS,
        "max_finding_detail_items": MAX_FINDING_DETAIL_ITEMS,
    }


class InputBlobLimitExceeded(Exception):
    def __init__(self, limit: int, observed_at_least: int) -> None:
        super().__init__(f"input blob exceeds limit {limit} bytes")
        self.limit = limit
        self.observed_at_least = observed_at_least


class ImplementationPinningError(Exception):
    def __init__(self, code: str, message: str, *, component: str | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.component = component


@dataclass(frozen=True)
class Descriptor:
    media_type: str
    size: int
    digest: str

    def to_json(self) -> dict[str, object]:
        return {
            "media_type": self.media_type,
            "size": self.size,
            "digest": self.digest,
        }


@dataclass(frozen=True)
class ImplementationInfo:
    root: Path
    manifest_path: Path
    descriptor: Descriptor
    component_digests: dict[str, str]


@dataclass(frozen=True)
class RawIntakePolicy:
    path: Path
    id: str
    digest: str
    unsafe_codes: set[str]
    unsafe_severities: set[str]
    unsafe_disposition: str
    complete_disposition: str


@dataclass(frozen=True)
class ContentTypeDetection:
    detected_media_type: str
    detection_basis: str
    locator_hint_media_type: str | None
    hint_match: str

    def to_json(self) -> dict[str, object]:
        item: dict[str, object] = {
            "profile": MEDIA_TYPE_DETECTION_PROFILE,
            "detected_media_type": self.detected_media_type,
            "detection_basis": self.detection_basis,
            "hint_match": self.hint_match,
        }
        if self.locator_hint_media_type is not None:
            item["locator_hint_media_type"] = self.locator_hint_media_type
        return item


@dataclass
class Finding:
    code: str
    severity: str
    profile: str
    message: str
    paths: list[str] = field(default_factory=list)
    details: dict[str, object] = field(default_factory=dict)

    def to_json(self) -> dict[str, object]:
        item: dict[str, object] = {
            "code": self.code,
            "severity": self.severity,
            "profile": self.profile,
            "message": self.message,
        }
        if self.paths:
            item["paths"] = self.paths
        if self.details:
            item["details"] = self.details
        return item


@dataclass
class Entry:
    raw_path: str
    manifest_path: str
    type: str
    size: int = 0
    mode: str = "100644"
    digest: str | None = None
    target: str | None = None
    preview: bytes = b""
    zip_info: zipfile.ZipInfo | None = None
    zip_header: "ZipLocalHeader | None" = None
    tar_member: tarfile.TarInfo | None = None


@dataclass(frozen=True)
class ZipLocalHeader:
    flags: int
    method: int
    crc: int
    compressed_size: int
    file_size: int
    raw_name: bytes
    extra: bytes
    data_start: int


@dataclass
class InspectionResult:
    blob_digest: str
    blob_size: int
    media_type: str
    content_type: ContentTypeDetection
    snapshot_kind: str
    snapshot_id: str
    manifest_bytes: bytes
    manifest_digest: str
    findings: list[Finding]
    disposition: str
    reason_codes: list[str]
    execution_state: str
    entry_count: int
    total_logical_size: int


@dataclass
class MaterializedInput:
    temp_dir: tempfile.TemporaryDirectory[str]
    path: Path
    blob_digest: str
    blob_size: int

    def cleanup(self) -> None:
        self.temp_dir.cleanup()


def sha256_file(path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            size += len(chunk)
            h.update(chunk)
    return f"sha256:{h.hexdigest()}", size


def materialize_input_copy(path: Path, max_input_blob_size: int) -> MaterializedInput:
    """Copy the source to a private immutable-by-convention blob for inspection."""
    st = path.stat(follow_symlinks=False)
    if st.st_size > max_input_blob_size:
        raise InputBlobLimitExceeded(limit=max_input_blob_size, observed_at_least=st.st_size)
    temp_dir = tempfile.TemporaryDirectory(prefix="vaks-source-capture-")
    temp_root = Path(temp_dir.name)
    try:
        try:
            os.chmod(temp_root, 0o700)
        except OSError:
            pass
        target = temp_root / path.name
        h = hashlib.sha256()
        size = 0
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        fd = os.open(target, flags, 0o600)
        try:
            with path.open("rb") as src, os.fdopen(fd, "wb") as dst:
                for chunk in iter(lambda: src.read(1024 * 1024), b""):
                    size += len(chunk)
                    if size > max_input_blob_size:
                        raise InputBlobLimitExceeded(limit=max_input_blob_size, observed_at_least=size)
                    h.update(chunk)
                    dst.write(chunk)
        except Exception:
            try:
                target.unlink(missing_ok=True)
            finally:
                raise
        return MaterializedInput(temp_dir=temp_dir, path=target, blob_digest=f"sha256:{h.hexdigest()}", blob_size=size)
    except Exception:
        temp_dir.cleanup()
        raise


def file_preview(path: Path, limit: int = 512) -> bytes:
    with path.open("rb") as fh:
        return fh.read(limit)


def digest_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def digest_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8", "surrogatepass")).hexdigest()


def json_line(obj: dict[str, object]) -> str:
    return json.dumps(obj, allow_nan=False, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def json_bytes(obj: dict[str, object]) -> bytes:
    return (json.dumps(obj, allow_nan=False, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def canonical_json_bytes(obj: dict[str, Any]) -> bytes:
    return (json.dumps(obj, allow_nan=False, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def load_strict_json(path: Path) -> Any:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_json_keys,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"non-standard JSON constant: {value}")),
    )


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def script_root() -> Path:
    return Path(__file__).resolve().parent.parent


def locator_media_type_hint(path: Path) -> str | None:
    name = path.name.lower()
    suffix = path.suffix.lower()
    if name.endswith(".zip"):
        return "application/zip"
    if name.endswith(".tar"):
        return "application/x-tar"
    if name.endswith((".tar.gz", ".tgz")):
        return "application/gzip"
    if name.endswith((".tar.bz2", ".tbz", ".tbz2")):
        return "application/x-bzip2"
    if name.endswith((".tar.xz", ".txz")):
        return "application/x-xz"
    if suffix == ".gz":
        return "application/gzip"
    if suffix == ".bz2":
        return "application/x-bzip2"
    if suffix == ".xz":
        return "application/x-xz"
    if suffix == ".pdf":
        return "application/pdf"
    return None


def media_type_for(path: Path) -> str:
    return locator_media_type_hint(path) or "application/octet-stream"


def archive_kind(path: Path) -> str:
    if zipfile.is_zipfile(path):
        return "zip"
    if tarfile.is_tarfile(path):
        return "tar"
    return "file"


def tar_media_type(path: Path) -> str:
    preview = file_preview(path, 8)
    if preview.startswith(b"\x1f\x8b"):
        return "application/gzip"
    if preview.startswith(b"BZh"):
        return "application/x-bzip2"
    if preview.startswith(b"\xfd7zXZ\x00"):
        return "application/x-xz"
    return "application/x-tar"


def detect_media_type(path: Path, inspection_kind: str, locator_hint: str | None) -> ContentTypeDetection:
    if inspection_kind == "zip":
        detected = "application/zip"
        basis = "container_parser"
    elif inspection_kind == "tar":
        detected = tar_media_type(path)
        basis = "container_parser"
    else:
        preview = file_preview(path, 8)
        if preview.startswith(b"%PDF-"):
            detected = "application/pdf"
            basis = "magic_signature"
        else:
            detected = "application/octet-stream"
            basis = "fallback"
    if locator_hint is None:
        hint_match = "no_hint"
    elif locator_hint == detected:
        hint_match = "matched"
    else:
        hint_match = "mismatch"
    return ContentTypeDetection(
        detected_media_type=detected,
        detection_basis=basis,
        locator_hint_media_type=locator_hint,
        hint_match=hint_match,
    )


def check_content_type_findings(
    detection: ContentTypeDetection,
    source_kind: str,
    findings: list[Finding],
    identity_path: Path,
) -> None:
    if detection.hint_match == "mismatch":
        add_finding(
            findings,
            "MEDIA_TYPE_HINT_MISMATCH",
            "warning",
            SOURCE_FIXITY_PROFILE,
            "Locator media-type hint differs from the scanner-selected content interpretation.",
            [identity_path.name],
            {
                "locator_hint_media_type": detection.locator_hint_media_type,
                "detected_media_type": detection.detected_media_type,
                "detection_profile": MEDIA_TYPE_DETECTION_PROFILE,
            },
        )
    if source_kind == "pdf" and detection.detected_media_type != "application/pdf":
        add_finding(
            findings,
            "SOURCE_KIND_FORMAT_MISMATCH",
            "hazard",
            SOURCE_FIXITY_PROFILE,
            "Declared source kind does not match the scanner-selected content interpretation.",
            [identity_path.name],
            {
                "source_kind": source_kind,
                "detected_media_type": detection.detected_media_type,
            },
        )


def default_implementation_manifest_path() -> Path:
    return script_root() / "tools" / "source_capture_implementation_manifest.json"


def default_policy_path() -> Path:
    return script_root() / "policies" / "source-capture" / "raw-intake-default-v1.json"


def validate_descriptor_shape(descriptor: Any, context: str) -> Descriptor:
    if not isinstance(descriptor, dict):
        raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", f"{context} must be an object")
    if set(descriptor) != {"media_type", "size", "digest"}:
        raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", f"{context} has invalid keys")
    media_type = descriptor.get("media_type")
    size = descriptor.get("size")
    digest = descriptor.get("digest")
    if not isinstance(media_type, str) or not media_type.strip():
        raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", f"{context}.media_type is invalid")
    if type(size) is not int or size < 0:
        raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", f"{context}.size is invalid")
    if not isinstance(digest, str) or not re.match(r"^sha256:[0-9a-f]{64}$", digest):
        raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", f"{context}.digest is invalid")
    return Descriptor(media_type=media_type, size=size, digest=digest)


def load_implementation_info(manifest_path: Path) -> ImplementationInfo:
    root = script_root()
    manifest_path = manifest_path.resolve()
    try:
        manifest = load_strict_json(manifest_path)
    except Exception as exc:
        raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", str(exc)) from exc
    if not isinstance(manifest, dict):
        raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", "implementation manifest root must be an object")
    required = {"schema", "id", "version", "components", "runtime"}
    if set(manifest) != required:
        raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", "implementation manifest has invalid keys")
    if manifest.get("schema") != IMPLEMENTATION_SCHEMA or manifest.get("id") != IMPLEMENTATION_ID:
        raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", "implementation manifest identity mismatch")
    if manifest.get("version") != IMPLEMENTATION_VERSION:
        raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", "implementation manifest version mismatch")
    components = manifest.get("components")
    if not isinstance(components, list) or not components:
        raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", "implementation manifest components must be a non-empty list")
    seen_paths: set[str] = set()
    component_digests: dict[str, str] = {}
    for idx, component in enumerate(components):
        if not isinstance(component, dict) or set(component) != {"path", "digest"}:
            raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", f"component {idx} has invalid shape")
        rel = component.get("path")
        expected_digest = component.get("digest")
        if not isinstance(rel, str) or not rel.strip() or "\\" in rel or rel.startswith("/") or ".." in Path(rel).parts:
            raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", f"component {idx} has invalid path")
        if rel in seen_paths:
            raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", f"duplicate component: {rel}", component=rel)
        seen_paths.add(rel)
        if not isinstance(expected_digest, str) or not re.match(r"^sha256:[0-9a-f]{64}$", expected_digest):
            raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", f"component {rel} digest is invalid", component=rel)
        component_path = (root / rel).resolve()
        try:
            component_path.relative_to(root)
        except ValueError as exc:
            raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", f"component escapes root: {rel}", component=rel) from exc
        if component_path.is_symlink() or not component_path.is_file():
            raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", f"component missing or unsafe: {rel}", component=rel)
        actual_digest = digest_file(component_path)
        if actual_digest != expected_digest:
            raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", f"component digest mismatch: {rel}", component=rel)
        component_digests[rel] = expected_digest
    if seen_paths != EXPECTED_IMPLEMENTATION_COMPONENTS:
        missing = sorted(EXPECTED_IMPLEMENTATION_COMPONENTS - seen_paths)
        extra = sorted(seen_paths - EXPECTED_IMPLEMENTATION_COMPONENTS)
        raise ImplementationPinningError(
            "CAPTURE_IMPLEMENTATION_PIN_MISMATCH",
            f"implementation manifest component set mismatch; missing={missing}; extra={extra}",
        )
    runtime = manifest.get("runtime")
    if not isinstance(runtime, dict) or set(runtime) != {"language", "minimum_version"}:
        raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", "implementation manifest runtime is invalid")
    if runtime.get("language") != "python" or runtime.get("minimum_version") != "3.10":
        raise ImplementationPinningError("CAPTURE_IMPLEMENTATION_PIN_MISMATCH", "implementation manifest runtime is invalid")
    descriptor = Descriptor(
        media_type=IMPLEMENTATION_MEDIA_TYPE,
        size=manifest_path.stat().st_size,
        digest=digest_file(manifest_path),
    )
    return ImplementationInfo(root=root, manifest_path=manifest_path, descriptor=descriptor, component_digests=component_digests)


def load_raw_intake_policy(path: Path, expected_id: str) -> RawIntakePolicy:
    try:
        policy = load_strict_json(path)
    except Exception as exc:
        raise ImplementationPinningError("CAPTURE_POLICY_PIN_MISMATCH", str(exc)) from exc
    if not isinstance(policy, dict):
        raise ImplementationPinningError("CAPTURE_POLICY_PIN_MISMATCH", "policy root must be an object")
    if set(policy) != {"schema", "id", "version", "unsafe_finding", "decision"}:
        raise ImplementationPinningError("CAPTURE_POLICY_PIN_MISMATCH", "policy has invalid keys")
    if policy.get("schema") != POLICY_SCHEMA:
        raise ImplementationPinningError("CAPTURE_POLICY_PIN_MISMATCH", "policy schema mismatch")
    policy_id = policy.get("id")
    if policy_id != expected_id:
        raise ImplementationPinningError("CAPTURE_POLICY_PIN_MISMATCH", "policy ID does not match CLI policy ID")
    if policy.get("version") != POLICY_VERSION:
        raise ImplementationPinningError("CAPTURE_POLICY_PIN_MISMATCH", "policy version mismatch")
    unsafe = policy.get("unsafe_finding")
    decision = policy.get("decision")
    if not isinstance(unsafe, dict) or set(unsafe) != {"codes", "severities"}:
        raise ImplementationPinningError("CAPTURE_POLICY_PIN_MISMATCH", "policy unsafe_finding has invalid shape")
    if not isinstance(decision, dict) or set(decision) != {"unsafe", "complete_without_unsafe"}:
        raise ImplementationPinningError("CAPTURE_POLICY_PIN_MISMATCH", "policy decision has invalid shape")
    severities = unsafe.get("severities")
    codes = unsafe.get("codes")
    if (
        not isinstance(severities, list)
        or not severities
        or any(not isinstance(item, str) or item not in {"hazard", "error", "warning", "info"} for item in severities)
    ):
        raise ImplementationPinningError("CAPTURE_POLICY_PIN_MISMATCH", "policy severities are invalid")
    if not isinstance(codes, list) or not codes or any(not isinstance(item, str) or not item.strip() for item in codes):
        raise ImplementationPinningError("CAPTURE_POLICY_PIN_MISMATCH", "policy codes are invalid")
    if len(codes) != len(set(codes)) or len(severities) != len(set(severities)):
        raise ImplementationPinningError("CAPTURE_POLICY_PIN_MISMATCH", "policy codes/severities must be unique")
    if not {"hazard", "error"}.issubset(set(severities)):
        raise ImplementationPinningError("CAPTURE_POLICY_PIN_MISMATCH", "policy unsafe severities must include hazard and error")
    unsafe_disposition = decision.get("unsafe")
    complete_disposition = decision.get("complete_without_unsafe")
    if unsafe_disposition != "quarantined" or complete_disposition != "admitted":
        raise ImplementationPinningError("CAPTURE_POLICY_PIN_MISMATCH", "policy decision values are not supported by alpha.1")
    canonical_digest = digest_bytes(canonical_json_bytes(policy))
    return RawIntakePolicy(
        path=path,
        id=policy_id,
        digest=canonical_digest,
        unsafe_codes=set(codes),
        unsafe_severities=set(severities),
        unsafe_disposition=unsafe_disposition,
        complete_disposition=complete_disposition,
    )


def suffix_suggests_archive(path: Path) -> bool:
    name = path.name.lower()
    return any(name.endswith(suffix) for suffix in ARCHIVE_SUFFIXES)


def capture_method_suggests_archive(capture_method: str) -> bool:
    return capture_method in {"provider_archive", "archive_file"}


def source_or_method_requires_archive(source_kind: str, capture_method: str) -> bool:
    return source_kind == "archive" or capture_method_suggests_archive(capture_method)


def default_locator_for(path: Path) -> str:
    if not path.is_absolute():
        return path.as_posix()
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.name


def add_parse_failed(
    findings: list[Finding],
    path: Path,
    message: str,
    exc: BaseException | None = None,
) -> None:
    details: dict[str, object] = {}
    if exc is not None:
        details = {"exception_type": type(exc).__name__, "exception": str(exc)}
    add_finding(
        findings,
        "ARCHIVE_PARSE_FAILED",
        "hazard",
        "archive-safety/v1",
        message,
        [path.name],
        details,
    )


def path_parts(path: str) -> list[str]:
    return [p for p in re.split(r"[\\/]+", path) if p]


def raw_path_segments(path: str) -> list[str]:
    return re.split(r"[\\/]", path)


def is_absolute_path(path: str) -> bool:
    return path.startswith(("/", "\\")) or bool(re.match(r"^[A-Za-z]:", path))


def has_path_traversal(path: str) -> bool:
    return any(part == ".." for part in path_parts(path))


def normalized_for_collision(path: str, form: str) -> str:
    return unicodedata.normalize(form, path)


def windows_equivalence_key(path: str) -> str:
    parts = [part.rstrip(" .").casefold() for part in path_parts(path)]
    return "/".join(parts)


def canonical_archive_path(raw_path: str, findings: list[Finding]) -> str:
    if len(raw_path) > MAX_ARCHIVE_PATH_STRING_LENGTH:
        add_path_length_limit_finding(raw_path, findings)
        return raw_path.replace("\\", "/")
    if any(ord(char) < 0x20 or ord(char) == 0x7F for char in raw_path):
        add_finding(
            findings,
            "ARCHIVE_PATH_CONTROL_CHARACTER",
            "hazard",
            "archive-safety/v1",
            "Archive path contains a control character.",
            [raw_path],
        )
    if any(0xDC80 <= ord(char) <= 0xDCFF for char in raw_path):
        add_finding(
            findings,
            "ARCHIVE_PATH_INVALID_UTF8",
            "hazard",
            "archive-safety/v1",
            "Archive path contains undecodable bytes represented as surrogate escapes.",
            [raw_path],
        )
    if "\\" in raw_path:
        add_finding(
            findings,
            "ARCHIVE_BACKSLASH_PATH",
            "hazard",
            "archive-safety/v1",
            "Archive path uses backslash; v1 requires forward-slash archive paths.",
            [raw_path],
        )
    if "//" in raw_path:
        add_finding(
            findings,
            "ARCHIVE_EMPTY_PATH_SEGMENT",
            "hazard",
            "archive-safety/v1",
            "Archive path contains repeated slashes or an empty segment.",
            [raw_path],
        )
    segments = raw_path_segments(raw_path)
    if any(segment in {"", "."} for segment in segments):
        add_finding(
            findings,
            "ARCHIVE_DOT_OR_EMPTY_SEGMENT",
            "hazard",
            "archive-safety/v1",
            "Archive path contains an empty or dot segment.",
            [raw_path],
        )
    return raw_path.replace("\\", "/")


def zip_path_for_validation(path: str) -> str:
    if path.endswith("/") and not path.endswith("//"):
        return path[:-1]
    return path


def add_path_length_limit_finding(path: str, findings: list[Finding]) -> None:
    add_finding(
        findings,
        "ARCHIVE_PATH_LENGTH_LIMIT_EXCEEDED",
        "hazard",
        "archive-safety/v1",
        "Archive path exceeds the implementation hard string limit.",
        [],
        {
            "path_digest": digest_text(path),
            "path_preview": path[:128],
            "path_length": len(path),
            "max_archive_path_string_length": MAX_ARCHIVE_PATH_STRING_LENGTH,
        },
    )


def add_finding(
    findings: list[Finding],
    code: str,
    severity: str,
    profile: str,
    message: str,
    paths: Iterable[str] = (),
    details: dict[str, object] | None = None,
) -> None:
    findings.append(
        Finding(
            code=code,
            severity=severity,
            profile=profile,
            message=message,
            paths=list(paths)[:20],
            details=details or {},
        )
    )


def stable_json_value(value: object) -> object:
    if isinstance(value, str):
        return "".join(
            f"\\u{ord(char):04x}"
            if ord(char) < 0x20 or ord(char) == 0x7F or 0xD800 <= ord(char) <= 0xDFFF
            else char
            for char in value
        )
    if isinstance(value, dict):
        return {
            str(key): stable_json_value(child)
            for key, child in sorted(value.items(), key=lambda item: str(item[0]))[:MAX_FINDING_DETAIL_ITEMS]
        }
    if isinstance(value, list):
        cleaned = [stable_json_value(item) for item in value]
        if all(isinstance(item, str) for item in cleaned):
            cleaned = sorted(set(cleaned))
        return cleaned[:MAX_FINDING_DETAIL_ITEMS]
    if isinstance(value, tuple):
        return stable_json_value(list(value))
    if isinstance(value, float):
        if value == float("inf"):
            return "inf"
        if value == float("-inf"):
            return "-inf"
        if value != value:
            return "nan"
        return float(f"{value:.12g}")
    return value


def canonical_finding(finding: Finding) -> Finding:
    paths = sorted(set(str(stable_json_value(path)) for path in finding.paths))[:MAX_FINDING_PATHS]
    details = stable_json_value(finding.details)
    if not isinstance(details, dict):
        details = {"value": details}
    return Finding(
        code=str(stable_json_value(finding.code)),
        severity=str(stable_json_value(finding.severity)),
        profile=str(stable_json_value(finding.profile)),
        message=str(stable_json_value(finding.message)),
        paths=paths,
        details=details,
    )


def prepared_findings(findings: list[Finding]) -> list[Finding]:
    canonical = [canonical_finding(finding) for finding in findings]
    deduped: dict[str, Finding] = {}
    for finding in canonical:
        key = json.dumps(finding.to_json(), allow_nan=False, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        deduped[key] = finding
    sorted_findings = sorted(
        deduped.values(),
        key=lambda finding: (
            finding.profile,
            FINDING_SEVERITY_ORDER.get(finding.severity, 99),
            finding.code,
            tuple(finding.paths),
            json.dumps(finding.details, allow_nan=False, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        ),
    )
    counts: dict[str, int] = {}
    limited: list[Finding] = []
    truncated: dict[str, int] = {}
    for finding in sorted_findings:
        count = counts.get(finding.code, 0)
        if count >= MAX_FINDINGS_PER_CODE:
            truncated[finding.code] = truncated.get(finding.code, 0) + 1
            continue
        counts[finding.code] = count + 1
        limited.append(finding)
    if truncated:
        limited.append(
            Finding(
                code="HYGIENE_FINDINGS_TRUNCATED",
                severity="warning",
                profile="source-fixity/v1",
                message="Hygiene findings were truncated by deterministic report-size limits.",
                details={"truncated_by_code": dict(sorted(truncated.items()))},
            )
        )
    return sorted(
        limited,
        key=lambda finding: (
            finding.profile,
            FINDING_SEVERITY_ORDER.get(finding.severity, 99),
            finding.code,
            tuple(finding.paths),
            json.dumps(finding.details, allow_nan=False, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        ),
    )


def first_common_archive_root(paths: list[str]) -> str | None:
    useful = [p for p in paths if p and not p.endswith("/")]
    if not useful:
        return None
    split = [p.split("/") for p in useful]
    if any(len(parts) < 2 for parts in split):
        return None
    root = split[0][0]
    if root and all(parts[0] == root for parts in split):
        return root
    return None


def strip_root(path: str, root: str | None) -> str:
    if not root:
        return path
    prefix = root + "/"
    if path == root:
        return ""
    if path.startswith(prefix):
        return path[len(prefix):]
    return path


def add_path_too_long_warning(path: str, findings: list[Finding], limits: Limits) -> None:
    if len(path) > limits.max_path_length:
        add_finding(
            findings,
            "PATH_TOO_LONG",
            "warning",
            "repo-portability/v1",
            "Path exceeds the configured portability length.",
            [path],
            {"max_path_length": limits.max_path_length},
        )


def check_path_hygiene(
    path: str,
    findings: list[Finding],
    limits: Limits,
    *,
    check_portability_length: bool = True,
) -> None:
    if len(path) > MAX_ARCHIVE_PATH_STRING_LENGTH:
        add_path_length_limit_finding(path, findings)
        return
    if is_absolute_path(path):
        add_finding(
            findings,
            "ARCHIVE_ABSOLUTE_PATH",
            "hazard",
            "archive-safety/v1",
            "Archive entry uses an absolute path.",
            [path],
        )
    if has_path_traversal(path):
        add_finding(
            findings,
            "ARCHIVE_PATH_TRAVERSAL",
            "hazard",
            "archive-safety/v1",
            "Archive entry contains a path traversal component.",
            [path],
        )
    parts = path_parts(path)
    if len(parts) > limits.max_path_depth:
        add_finding(
            findings,
            "ARCHIVE_PATH_DEPTH_EXCEEDED",
            "hazard",
            "archive-safety/v1",
            "Archive entry exceeds the configured path-depth limit.",
            [path],
            {"max_path_depth": limits.max_path_depth},
        )
    if check_portability_length:
        add_path_too_long_warning(path, findings, limits)
    for part in parts:
        base = part.split(".", 1)[0].upper()
        if base in WINDOWS_RESERVED:
            add_finding(
                findings,
                "PATH_WINDOWS_RESERVED_NAME",
                "warning",
                "repo-portability/v1",
                "Path contains a Windows reserved name.",
                [path],
            )
        if WINDOWS_INVALID_RE.search(part):
            add_finding(
                findings,
                "PATH_WINDOWS_INVALID_CHARACTER",
                "warning",
                "repo-portability/v1",
                "Path contains a Windows-invalid character.",
                [path],
            )
        if part.endswith((" ", ".")):
            add_finding(
                findings,
                "PATH_WINDOWS_TRAILING_DOT_OR_SPACE",
                "warning",
                "repo-portability/v1",
                "Path component has trailing dot or space.",
                [path],
            )


def parent_paths(path: str) -> list[str]:
    parts = path.split("/")
    parents: list[str] = []
    for idx in range(1, len(parts)):
        parent = "/".join(parts[:idx])
        if parent:
            parents.append(parent)
    return parents


def check_tree_model(entries: list[Entry], explicit_dirs: set[str], findings: list[Finding]) -> None:
    paths = [entry.manifest_path for entry in entries if entry.manifest_path]
    for dupe in duplicate_paths(paths):
        add_finding(
            findings,
            "ARCHIVE_DUPLICATE_ENTRY",
            "hazard",
            "archive-safety/v1",
            "Archive entries collide after root stripping.",
            [dupe],
        )
    typed: dict[str, str] = {}
    for directory in explicit_dirs:
        if directory:
            typed[directory] = "dir"
    for entry in entries:
        if not entry.manifest_path:
            continue
        previous = typed.get(entry.manifest_path)
        if previous and previous != entry.type:
            add_finding(
                findings,
                "ARCHIVE_TYPE_COLLISION",
                "hazard",
                "archive-safety/v1",
                "Archive path has conflicting file/directory/symlink types.",
                [entry.manifest_path],
                {"existing_type": previous, "new_type": entry.type},
            )
        typed[entry.manifest_path] = entry.type
    terminal_paths = {entry.manifest_path for entry in entries if entry.manifest_path}
    for entry in entries:
        for parent in parent_paths(entry.manifest_path):
            if parent in terminal_paths:
                add_finding(
                    findings,
                    "ARCHIVE_ANCESTOR_PREFIX_CONFLICT",
                    "hazard",
                    "archive-safety/v1",
                    "Archive contains a file/symlink path that is also an ancestor directory.",
                    [parent, entry.manifest_path],
                )
    for directory in explicit_dirs:
        if not directory:
            continue
        for parent in parent_paths(directory):
            if parent in terminal_paths:
                add_finding(
                    findings,
                    "ARCHIVE_ANCESTOR_PREFIX_CONFLICT",
                    "hazard",
                    "archive-safety/v1",
                    "Archive contains an explicit directory whose ancestor is a file or symlink.",
                    [parent, directory],
                )


def check_collision_groups(paths: list[str], findings: list[Finding]) -> None:
    def groups_by(key_func):
        groups: dict[str, list[str]] = {}
        for p in paths:
            groups.setdefault(key_func(p), []).append(p)
        return [sorted(set(v)) for v in groups.values() if len(set(v)) > 1]

    for code, key_func, message in [
        ("PATH_CASE_COLLISION", lambda p: p.casefold(), "Paths collide after case folding."),
        ("PATH_UNICODE_NFC_COLLISION", lambda p: normalized_for_collision(p, "NFC"), "Paths collide after Unicode NFC normalization."),
        ("PATH_UNICODE_NFD_COLLISION", lambda p: normalized_for_collision(p, "NFD"), "Paths collide after Unicode NFD normalization."),
        ("PATH_WINDOWS_EQUIVALENCE_COLLISION", windows_equivalence_key, "Paths collide under Windows path equivalence."),
    ]:
        for group in groups_by(key_func):
            add_finding(
                findings,
                code,
                "warning",
                "repo-portability/v1",
                message,
                group,
                {"group": group},
            )


def duplicate_paths(paths: list[str]) -> list[str]:
    seen: set[str] = set()
    dupes: set[str] = set()
    for path in paths:
        if path in seen:
            dupes.add(path)
        seen.add(path)
    return sorted(dupes)


def unsafe_findings(findings: list[Finding], policy: RawIntakePolicy) -> list[Finding]:
    return [f for f in findings if f.code in policy.unsafe_codes or f.severity in policy.unsafe_severities]


def file_digest_from_zip(
    path: Path,
    info: zipfile.ZipInfo,
    local_header: ZipLocalHeader | None,
    entry_path: str,
    findings: list[Finding],
    limits: Limits,
    *,
    capture_limit: int = 512,
    remaining_total_budget: int | None = None,
) -> tuple[str, bytes]:
    h = hashlib.sha256()
    captured = bytearray()
    if local_header is None:
        add_finding(
            findings,
            "ARCHIVE_ZIP_HEADER_CONFLICT",
            "hazard",
            "archive-safety/v1",
            "ZIP local header is unavailable for exact payload validation.",
            [entry_path],
        )
        return "sha256:" + h.hexdigest(), b""

    actual_crc = 0
    actual_size = 0
    size_hazard_reported = False
    integrity_hazard = False
    ratio_budget = int(info.compress_size * limits.max_compression_ratio)
    if info.compress_size == 0:
        ratio_budget = 0 if info.file_size == 0 else limits.max_entry_size
    output_budget = min(
        limits.max_entry_size,
        limits.max_total_size if remaining_total_budget is None else max(remaining_total_budget, 0),
        max(ratio_budget, 0),
    )

    def add_stream_hazard(message: str, details: dict[str, object] | None = None) -> None:
        nonlocal integrity_hazard
        integrity_hazard = True
        add_finding(
            findings,
            "ARCHIVE_ZIP_STREAM_INTEGRITY_FAILED",
            "hazard",
            "archive-safety/v1",
            message,
            [entry_path],
            details,
        )

    def consume(output: bytes) -> bool:
        nonlocal actual_crc, actual_size, size_hazard_reported
        if not output:
            return True
        h.update(output)
        actual_crc = zlib.crc32(output, actual_crc) & 0xFFFFFFFF
        if len(captured) < capture_limit:
            captured.extend(output[: capture_limit - len(captured)])
        actual_size += len(output)
        if actual_size > output_budget and not size_hazard_reported:
            size_hazard_reported = True
            add_finding(
                findings,
                "ARCHIVE_ENTRY_SIZE_LIMIT_EXCEEDED",
                "hazard",
                "archive-safety/v1",
                "Actual decompressed ZIP entry exceeds the configured exact-validation output budget.",
                [entry_path],
                {
                    "actual_size": actual_size,
                    "entry_budget": limits.max_entry_size,
                    "remaining_total_budget": remaining_total_budget,
                    "ratio_budget": ratio_budget,
                },
            )
            return False
        return True

    def remaining_output_budget() -> int:
        return output_budget - actual_size

    def read_compressed_chunks(fh) -> Iterable[bytes]:
        remaining = info.compress_size
        while remaining > 0:
            chunk = fh.read(min(1024 * 1024, remaining))
            if not chunk:
                add_finding(
                    findings,
                    "ARCHIVE_ZIP_STREAM_INTEGRITY_FAILED",
                    "hazard",
                    "archive-safety/v1",
                    "ZIP compressed payload ended before the declared compressed size.",
                    [entry_path],
                    {"remaining": remaining},
                )
                return
            remaining -= len(chunk)
            yield chunk

    try:
        with path.open("rb") as fh:
            fh.seek(local_header.data_start)
            if info.compress_type == zipfile.ZIP_STORED:
                if info.compress_size != info.file_size:
                    add_finding(
                        findings,
                        "ARCHIVE_ZIP_STREAM_INTEGRITY_FAILED",
                        "hazard",
                        "archive-safety/v1",
                        "ZIP STORED entry has different compressed and uncompressed sizes.",
                        [entry_path],
                        {"compressed_size": info.compress_size, "file_size": info.file_size},
                    )
                for chunk in read_compressed_chunks(fh):
                    if not consume(chunk):
                        break
            elif info.compress_type == zipfile.ZIP_DEFLATED:
                decompressor = zlib.decompressobj(-zlib.MAX_WBITS)
                stopped = False
                for chunk in read_compressed_chunks(fh):
                    pending = chunk
                    try:
                        while pending:
                            budget = remaining_output_budget()
                            if budget < 0:
                                stopped = True
                                break
                            output = decompressor.decompress(
                                pending,
                                max_length=min(budget + 1, ZIP_DECOMPRESS_OUTPUT_CHUNK_LIMIT),
                            )
                            pending = decompressor.unconsumed_tail
                            if not consume(output):
                                stopped = True
                                break
                            if decompressor.unused_data:
                                add_stream_hazard(
                                    "ZIP DEFLATE stream ended before all declared compressed bytes were consumed.",
                                    {"unused_bytes": len(decompressor.unused_data)},
                                )
                                stopped = True
                                break
                            if not output and not pending:
                                break
                    except zlib.error as exc:
                        add_stream_hazard(
                            "ZIP DEFLATE stream could not be decompressed exactly.",
                            {"exception": str(exc)},
                        )
                        stopped = True
                        break
                    if stopped:
                        break
                    if decompressor.unused_data:
                        add_stream_hazard(
                            "ZIP DEFLATE stream ended before all declared compressed bytes were consumed.",
                            {"unused_bytes": len(decompressor.unused_data)},
                        )
                        stopped = True
                        break
                if not stopped:
                    while True:
                        budget = remaining_output_budget()
                        if budget < 0:
                            stopped = True
                            break
                        try:
                            output = decompressor.flush(min(budget + 1, ZIP_DECOMPRESS_OUTPUT_CHUNK_LIMIT))
                        except zlib.error as exc:
                            add_stream_hazard(
                                "ZIP DEFLATE stream failed during final flush.",
                                {"exception": str(exc)},
                            )
                            stopped = True
                            break
                        if not output:
                            break
                        if not consume(output):
                            stopped = True
                            break
                if not stopped and not decompressor.eof:
                    add_stream_hazard("ZIP DEFLATE stream did not reach an end-of-stream marker.")
                if decompressor.unconsumed_tail:
                    add_stream_hazard(
                        "ZIP DEFLATE stream left unconsumed compressed tail data.",
                        {"unconsumed_tail": len(decompressor.unconsumed_tail)},
                    )
            else:
                add_finding(
                    findings,
                    "ARCHIVE_UNSUPPORTED_COMPRESSION",
                    "hazard",
                    "archive-safety/v1",
                    "ZIP compression method is not supported by exact-stream validation.",
                    [entry_path],
                    {"compress_type": info.compress_type},
                )
    except OSError as exc:
        add_stream_hazard(
            "ZIP compressed payload could not be read for exact validation.",
            {"exception": str(exc)},
        )

    if integrity_hazard or size_hazard_reported:
        return "sha256:" + h.hexdigest(), bytes(captured)

    if actual_size != info.file_size:
        add_stream_hazard(
            "ZIP actual decompressed size does not match the central directory size.",
            {"actual_size": actual_size, "declared_size": info.file_size},
        )
    if actual_crc != info.CRC:
        add_stream_hazard(
            "ZIP actual decompressed CRC does not match the central directory CRC.",
            {"actual_crc32": f"{actual_crc:08x}", "declared_crc32": f"{info.CRC:08x}"},
        )
    return "sha256:" + h.hexdigest(), bytes(captured)


def file_digest_from_tar(tf: tarfile.TarFile, member: tarfile.TarInfo) -> tuple[str, bytes]:
    h = hashlib.sha256()
    preview = bytearray()
    fh = tf.extractfile(member)
    if fh is None:
        return "sha256:" + hashlib.sha256(b"").hexdigest(), b""
    with fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            if len(preview) < 512:
                preview.extend(chunk[: 512 - len(preview)])
            h.update(chunk)
    return "sha256:" + h.hexdigest(), bytes(preview)


def entry_logical_size(entry: Entry) -> int:
    if entry.type == "symlink" and entry.target is not None:
        return len(entry.target.encode("utf-8"))
    return entry.size


def check_entry_logical_size(entry: Entry, findings: list[Finding], limits: Limits) -> None:
    size = entry_logical_size(entry)
    if size > limits.max_entry_size:
        add_finding(
            findings,
            "ARCHIVE_ENTRY_SIZE_LIMIT_EXCEEDED",
            "hazard",
            "archive-safety/v1",
            "Archive entry exceeds the configured entry size limit.",
            [entry.raw_path],
            {"size": size, "max_entry_size": limits.max_entry_size},
        )


def check_total_logical_size(entries: list[Entry], findings: list[Finding], limits: Limits) -> int:
    total = sum(entry_logical_size(entry) for entry in entries)
    if total > limits.max_total_size and not any(f.code == "ARCHIVE_TOTAL_SIZE_LIMIT_EXCEEDED" for f in findings):
        add_finding(
            findings,
            "ARCHIVE_TOTAL_SIZE_LIMIT_EXCEEDED",
            "hazard",
            "archive-safety/v1",
            "Archive exceeds the configured total logical size limit.",
            details={"total_size": total, "max_total_size": limits.max_total_size},
        )
    return total


def zip_mode(info: zipfile.ZipInfo) -> int:
    return (info.external_attr >> 16) & 0o777777


def zip_unix_mode(info: zipfile.ZipInfo) -> int | None:
    if info.create_system not in UNIX_ZIP_CREATE_SYSTEMS:
        return None
    mode = zip_mode(info)
    return mode if mode else None


def manifest_mode(mode: int, entry_type: str) -> str:
    if entry_type == "symlink":
        return "120000"
    if mode & 0o111:
        return "100755"
    return "100644"


def is_zip_symlink(info: zipfile.ZipInfo) -> bool:
    mode = zip_unix_mode(info)
    return bool(mode is not None and stat.S_ISLNK(mode))


def zip_entry_type(info: zipfile.ZipInfo, findings: list[Finding]) -> str | None:
    mode = zip_unix_mode(info)
    raw_mode = zip_mode(info)
    file_type = (mode or 0) & 0o170000
    dir_marker = info.filename.endswith("/")
    dos_attr = info.external_attr & 0xFF
    evidence: list[tuple[str, str]] = []
    if dir_marker:
        evidence.append(("filename_marker", "dir"))
    if dos_attr & 0x08:
        add_finding(
            findings,
            "ARCHIVE_SPECIAL_FILE",
            "hazard",
            "archive-safety/v1",
            "ZIP entry is a DOS volume-label entry, not file content.",
            [info.filename],
            {"dos_attr": dos_attr, "create_system": info.create_system},
        )
        return None
    if dos_attr & 0x10:
        evidence.append(("dos_attr", "dir"))
    mode_type: str | None
    if mode is None or file_type == 0:
        mode_type = None
    elif stat.S_ISDIR(mode):
        mode_type = "dir"
    elif stat.S_ISREG(mode):
        mode_type = "file"
    elif stat.S_ISLNK(mode):
        mode_type = "symlink"
    else:
        add_finding(
            findings,
            "ARCHIVE_SPECIAL_FILE",
            "hazard",
            "archive-safety/v1",
            "Archive ZIP entry is not a regular file, directory, or symlink.",
            [info.filename],
            {"mode": f"{raw_mode:06o}", "create_system": info.create_system},
        )
        return None
    if mode_type is not None:
        evidence.append(("unix_mode", mode_type))
    evidence_types = {entry_type for source, entry_type in evidence}
    if len(evidence_types) > 1:
        add_finding(
            findings,
            "ARCHIVE_TYPE_COLLISION",
            "hazard",
            "archive-safety/v1",
            "ZIP entry carries conflicting filename, DOS, or Unix type evidence.",
            [info.filename],
            {
                "create_system": info.create_system,
                "dos_attr": dos_attr,
                "evidence": [f"{source}:{entry_type}" for source, entry_type in evidence],
                "mode": f"{raw_mode:06o}",
                "size": info.file_size,
            },
        )
        return None
    evidenced_type = next(iter(evidence_types), None)
    if evidenced_type == "dir" and not dir_marker:
        add_finding(
            findings,
            "ARCHIVE_TYPE_COLLISION",
            "hazard",
            "archive-safety/v1",
            "ZIP directory type evidence is missing the directory filename marker.",
            [info.filename],
            {"create_system": info.create_system, "dos_attr": dos_attr, "mode": f"{raw_mode:06o}", "size": info.file_size},
        )
        return None
    if dir_marker:
        if info.file_size != 0:
            add_finding(
                findings,
                "ARCHIVE_TYPE_COLLISION",
                "hazard",
                "archive-safety/v1",
                "ZIP directory entry carries a non-zero payload.",
                [info.filename],
                {"size": info.file_size},
            )
            return None
        return "dir"
    if mode_type is None:
        return "file"
    if mode_type in {"file", "symlink"}:
        return mode_type
    add_finding(
        findings,
        "ARCHIVE_SPECIAL_FILE",
        "hazard",
        "archive-safety/v1",
        "Archive ZIP entry is not a regular file, directory, or symlink.",
        [info.filename],
        {"mode": f"{raw_mode:06o}", "create_system": info.create_system},
    )
    return None


def decode_symlink_target(raw: bytes, entry_path: str, findings: list[Finding], limits: Limits) -> str:
    if len(raw) > limits.max_symlink_target_size:
        add_finding(
            findings,
            "ARCHIVE_SYMLINK_TARGET_LIMIT_EXCEEDED",
            "hazard",
            "archive-safety/v1",
            "Symlink target exceeds the configured target-size limit.",
            [entry_path],
            {"size": len(raw), "max_symlink_target_size": limits.max_symlink_target_size},
        )
        return ""
    if len(raw) == 0:
        add_finding(
            findings,
            "ARCHIVE_SYMLINK_TARGET_EMPTY",
            "hazard",
            "archive-safety/v1",
            "Symlink target is empty.",
            [entry_path],
        )
        return ""
    try:
        target = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        add_finding(
            findings,
            "ARCHIVE_SYMLINK_TARGET_INVALID_UTF8",
            "hazard",
            "archive-safety/v1",
            "Symlink target is not strict UTF-8.",
            [entry_path],
        )
        return ""
    if "\\" in target:
        add_finding(
            findings,
            "ARCHIVE_SYMLINK_TARGET_BACKSLASH",
            "hazard",
            "archive-safety/v1",
            "Symlink target uses backslash; v1 requires forward-slash targets.",
            [entry_path, target],
        )
    if any(ord(char) < 0x20 or ord(char) == 0x7F for char in target):
        add_finding(
            findings,
            "ARCHIVE_SYMLINK_TARGET_CONTROL_CHARACTER",
            "hazard",
            "archive-safety/v1",
            "Symlink target contains a control character.",
            [entry_path, target],
        )
    return target


def decode_zip_name(raw: bytes, utf8_flag: bool, findings: list[Finding], context: str) -> str | None:
    encoding = "utf-8" if utf8_flag else "cp437"
    try:
        return raw.decode(encoding, errors="strict")
    except UnicodeDecodeError:
        add_finding(
            findings,
            "ARCHIVE_PATH_INVALID_UTF8",
            "hazard",
            "archive-safety/v1",
            "ZIP path representation cannot be decoded deterministically.",
            [context],
            {"encoding": encoding},
        )
        return None


def read_local_zip_header(path: Path, info: zipfile.ZipInfo, findings: list[Finding]) -> ZipLocalHeader | None:
    try:
        with path.open("rb") as fh:
            fh.seek(info.header_offset)
            header = fh.read(30)
            if len(header) != 30:
                raise zipfile.BadZipFile("truncated local file header")
            (
                signature,
                _version_needed,
                flags,
                method,
                _mtime,
                _mdate,
                crc,
                compressed_size,
                file_size,
                name_len,
                extra_len,
            ) = struct.unpack("<IHHHHHIIIHH", header)
            if signature != 0x04034B50:
                raise zipfile.BadZipFile("local file header signature mismatch")
            name = fh.read(name_len)
            extra = fh.read(extra_len)
            if len(name) != name_len or len(extra) != extra_len:
                raise zipfile.BadZipFile("truncated local file header name or extra field")
            data_start = info.header_offset + 30 + name_len + extra_len
            resolved_file_size, resolved_compressed_size = resolve_local_zip_sizes(file_size, compressed_size, extra, findings, info.filename)
            return ZipLocalHeader(
                flags=flags,
                method=method,
                crc=crc,
                compressed_size=resolved_compressed_size,
                file_size=resolved_file_size,
                raw_name=name,
                extra=extra,
                data_start=data_start,
            )
    except Exception as exc:
        add_parse_failed(findings, path, "ZIP local header path metadata could not be inspected.", exc)
        return None


def iter_zip_extra_fields(extra: bytes, findings: list[Finding], context: str) -> Iterable[tuple[int, bytes]]:
    offset = 0
    while offset < len(extra):
        if offset + 4 > len(extra):
            add_finding(
                findings,
                "ARCHIVE_PATH_REPRESENTATION_CONFLICT",
                "hazard",
                "archive-safety/v1",
                "ZIP extra field metadata is truncated.",
                [context],
            )
            return
        field_id, size = struct.unpack("<HH", extra[offset : offset + 4])
        offset += 4
        if offset + size > len(extra):
            add_finding(
                findings,
                "ARCHIVE_PATH_REPRESENTATION_CONFLICT",
                "hazard",
                "archive-safety/v1",
                "ZIP extra field metadata length exceeds available bytes.",
                [context],
                {"field_id": f"0x{field_id:04x}", "size": size},
            )
            return
        yield field_id, extra[offset : offset + size]
        offset += size


def resolve_local_zip_sizes(
    file_size: int,
    compressed_size: int,
    extra: bytes,
    findings: list[Finding],
    context: str,
) -> tuple[int, int]:
    needs_file_size = file_size == 0xFFFFFFFF
    needs_compressed_size = compressed_size == 0xFFFFFFFF
    if not needs_file_size and not needs_compressed_size:
        return file_size, compressed_size
    zip64_data: bytes | None = None
    for field_id, data in iter_zip_extra_fields(extra, findings, f"{context} local ZIP64 extra"):
        if field_id == 0x0001:
            zip64_data = data
            break
    if zip64_data is None:
        add_finding(
            findings,
            "ARCHIVE_ZIP_HEADER_CONFLICT",
            "hazard",
            "archive-safety/v1",
            "ZIP local header uses ZIP64 size placeholders without a ZIP64 extra field.",
            [context],
        )
        return file_size, compressed_size
    offset = 0
    try:
        if needs_file_size:
            file_size = struct.unpack("<Q", zip64_data[offset : offset + 8])[0]
            offset += 8
        if needs_compressed_size:
            compressed_size = struct.unpack("<Q", zip64_data[offset : offset + 8])[0]
    except struct.error:
        add_finding(
            findings,
            "ARCHIVE_ZIP_HEADER_CONFLICT",
            "hazard",
            "archive-safety/v1",
            "ZIP local header ZIP64 size field is truncated.",
            [context],
        )
    return file_size, compressed_size


def unicode_path_extra_names(
    extra: bytes,
    raw_name: bytes | None,
    findings: list[Finding],
    context: str,
) -> list[str]:
    names: list[str] = []
    for field_id, data in iter_zip_extra_fields(extra, findings, context):
        if field_id != ZIP_UNICODE_PATH_EXTRA_ID:
            continue
        if len(data) < 5:
            add_finding(
                findings,
                "ARCHIVE_PATH_REPRESENTATION_CONFLICT",
                "hazard",
                "archive-safety/v1",
                "ZIP Unicode path extra field is too short.",
                [context],
            )
            continue
        version = data[0]
        if version != 1:
            add_finding(
                findings,
                "ARCHIVE_PATH_REPRESENTATION_CONFLICT",
                "hazard",
                "archive-safety/v1",
                "ZIP Unicode path extra field uses an unsupported version.",
                [context],
                {"version": version},
            )
            continue
        expected_crc = struct.unpack("<I", data[1:5])[0]
        if raw_name is not None:
            actual_crc = zlib.crc32(raw_name) & 0xFFFFFFFF
            if expected_crc != actual_crc:
                add_finding(
                    findings,
                    "ARCHIVE_PATH_REPRESENTATION_CONFLICT",
                    "hazard",
                    "archive-safety/v1",
                    "ZIP Unicode path extra field CRC does not bind to the raw path bytes.",
                    [context],
                    {"actual_crc32": f"{actual_crc:08x}", "expected_crc32": f"{expected_crc:08x}"},
                )
        try:
            names.append(data[5:].decode("utf-8", errors="strict"))
        except UnicodeDecodeError:
            add_finding(
                findings,
                "ARCHIVE_PATH_INVALID_UTF8",
                "hazard",
                "archive-safety/v1",
                "ZIP Unicode path extra field is not strict UTF-8.",
                [context],
            )
    return names


def validate_zip_path_representation(path_text: str, label: str, findings: list[Finding], limits: Limits) -> str:
    validation_path = zip_path_for_validation(path_text)
    canonical = canonical_archive_path(validation_path, findings)
    check_path_hygiene(canonical, findings, limits, check_portability_length=False)
    return canonical


def validate_zip_path_representations(
    info: zipfile.ZipInfo,
    local_header: ZipLocalHeader | None,
    findings: list[Finding],
    limits: Limits,
) -> str:
    utf8_flag = bool(info.flag_bits & 0x800)
    representations: list[tuple[str, str]] = [
        ("filename", info.filename),
        ("orig_filename", info.orig_filename),
    ]
    if local_header is not None:
        local_name = decode_zip_name(local_header.raw_name, utf8_flag, findings, "zip local header path")
        if local_name is not None:
            representations.append(("local_header", local_name))
    local_raw_name = local_header.raw_name if local_header is not None else None
    for idx, unicode_name in enumerate(unicode_path_extra_names(info.extra, local_raw_name, findings, "zip central unicode path extra")):
        representations.append((f"central_unicode_extra[{idx}]", unicode_name))
    if local_header is not None:
        for idx, unicode_name in enumerate(unicode_path_extra_names(local_header.extra, local_raw_name, findings, "zip local unicode path extra")):
            representations.append((f"local_unicode_extra[{idx}]", unicode_name))

    canonical_by_label: dict[str, str] = {}
    marker_by_label: dict[str, bool] = {}
    for label, text in representations:
        canonical_by_label[label] = validate_zip_path_representation(text, label, findings, limits)
        marker_by_label[label] = text.endswith("/")
    markers = set(marker_by_label.values())
    if len(markers) > 1:
        add_finding(
            findings,
            "ARCHIVE_TYPE_COLLISION",
            "hazard",
            "archive-safety/v1",
            "ZIP path representations disagree about directory marker status.",
            [info.filename],
            {"markers": marker_by_label},
        )
    canonical_values = set(canonical_by_label.values())
    if len(canonical_values) > 1:
        add_finding(
            findings,
            "ARCHIVE_PATH_REPRESENTATION_CONFLICT",
            "hazard",
            "archive-safety/v1",
            "ZIP path representations disagree after v1 canonicalization.",
            [info.filename],
            {"representations": canonical_by_label},
        )
    return canonical_by_label["filename"]


def zip_data_boundaries(infos: list[zipfile.ZipInfo], start_dir: int) -> dict[int, int]:
    ordered = sorted(infos, key=lambda item: item.header_offset)
    boundaries: dict[int, int] = {}
    for idx, info in enumerate(ordered):
        next_boundary = ordered[idx + 1].header_offset if idx + 1 < len(ordered) else start_dir
        boundaries[id(info)] = next_boundary
    return boundaries


def validate_zip_header_consistency(
    info: zipfile.ZipInfo,
    local_header: ZipLocalHeader | None,
    data_boundary: int,
    entry_path: str,
    findings: list[Finding],
) -> None:
    if local_header is None:
        return
    if local_header.flags != info.flag_bits:
        add_finding(
            findings,
            "ARCHIVE_ZIP_HEADER_CONFLICT",
            "hazard",
            "archive-safety/v1",
            "ZIP local-header flags do not match central-directory flags.",
            [entry_path],
            {"central_flags": info.flag_bits, "local_flags": local_header.flags},
        )
    if (local_header.flags | info.flag_bits) & 0x08:
        add_finding(
            findings,
            "ARCHIVE_ZIP_DATA_DESCRIPTOR_UNSUPPORTED",
            "hazard",
            "archive-safety/v1",
            "ZIP data-descriptor entries are not admitted by v1 exact-stream validation.",
            [entry_path],
            {"central_flags": info.flag_bits, "local_flags": local_header.flags},
        )
    if local_header.method != info.compress_type:
        add_finding(
            findings,
            "ARCHIVE_ZIP_HEADER_CONFLICT",
            "hazard",
            "archive-safety/v1",
            "ZIP local-header compression method does not match central-directory method.",
            [entry_path],
            {"central_method": info.compress_type, "local_method": local_header.method},
        )
    if local_header.crc != info.CRC:
        add_finding(
            findings,
            "ARCHIVE_ZIP_HEADER_CONFLICT",
            "hazard",
            "archive-safety/v1",
            "ZIP local-header CRC does not match central-directory CRC.",
            [entry_path],
            {"central_crc32": f"{info.CRC:08x}", "local_crc32": f"{local_header.crc:08x}"},
        )
    if local_header.compressed_size != info.compress_size:
        add_finding(
            findings,
            "ARCHIVE_ZIP_HEADER_CONFLICT",
            "hazard",
            "archive-safety/v1",
            "ZIP local-header compressed size does not match central-directory size.",
            [entry_path],
            {"central_compressed_size": info.compress_size, "local_compressed_size": local_header.compressed_size},
        )
    if local_header.file_size != info.file_size:
        add_finding(
            findings,
            "ARCHIVE_ZIP_HEADER_CONFLICT",
            "hazard",
            "archive-safety/v1",
            "ZIP local-header uncompressed size does not match central-directory size.",
            [entry_path],
            {"central_file_size": info.file_size, "local_file_size": local_header.file_size},
        )
    declared_data_end = local_header.data_start + info.compress_size
    if declared_data_end != data_boundary:
        add_finding(
            findings,
            "ARCHIVE_ZIP_STREAM_INTEGRITY_FAILED",
            "hazard",
            "archive-safety/v1",
            "ZIP declared compressed payload does not end exactly at the next local header or central directory.",
            [entry_path],
            {"declared_data_end": declared_data_end, "next_boundary": data_boundary},
        )
    if info.compress_type == zipfile.ZIP_STORED and info.compress_size != info.file_size:
        add_finding(
            findings,
            "ARCHIVE_ZIP_STREAM_INTEGRITY_FAILED",
            "hazard",
            "archive-safety/v1",
            "ZIP STORED entry must have identical compressed and uncompressed sizes.",
            [entry_path],
            {"compressed_size": info.compress_size, "file_size": info.file_size},
        )


def should_strip_wrapper_root(source_kind: str, capture_method: str) -> bool:
    return source_kind == "repo" and capture_method == "provider_archive"


def read_zip_entries(
    path: Path,
    limits: Limits,
    findings: list[Finding],
    *,
    source_kind: str,
    capture_method: str,
    policy: RawIntakePolicy,
) -> tuple[list[Entry], int]:
    entries: list[Entry] = []
    explicit_dirs: set[str] = set()
    total_size = 0
    with zipfile.ZipFile(path) as zf:
        infos = zf.infolist()
        if len(infos) > limits.max_entries:
            add_finding(
                findings,
                "ARCHIVE_ENTRY_LIMIT_EXCEEDED",
                "hazard",
                "archive-safety/v1",
                "Archive exceeds the configured entry count limit.",
                details={"entry_count": len(infos), "max_entries": limits.max_entries},
            )
        boundaries = zip_data_boundaries(infos, zf.start_dir)
        typed_infos: list[tuple[zipfile.ZipInfo, ZipLocalHeader | None, str, str | None]] = []
        for info in infos:
            local_header = read_local_zip_header(path, info, findings)
            entry_type = zip_entry_type(info, findings)
            raw_name = validate_zip_path_representations(info, local_header, findings, limits)
            validate_zip_header_consistency(info, local_header, boundaries.get(id(info), zf.start_dir), raw_name, findings)
            if len(raw_name) > MAX_ARCHIVE_PATH_STRING_LENGTH:
                continue
            typed_infos.append((info, local_header, raw_name, entry_type))
        raw_names = [raw_path for info, local_header, raw_path, entry_type in typed_infos if entry_type not in {"dir", None}]
        for dupe in duplicate_paths(raw_names):
            add_finding(
                findings,
                "ARCHIVE_DUPLICATE_ENTRY",
                "hazard",
                "archive-safety/v1",
                "Archive contains an exact duplicate entry path.",
                [dupe],
            )
        root = first_common_archive_root(raw_names) if should_strip_wrapper_root(source_kind, capture_method) else None
        payload_items: list[tuple[zipfile.ZipInfo, ZipLocalHeader | None, str, str]] = []
        for info, local_header, raw_path, entry_type in typed_infos:
            if entry_type is None:
                continue
            if info.flag_bits & 0x1:
                add_finding(
                    findings,
                    "ARCHIVE_ENCRYPTED_ENTRY",
                    "hazard",
                    "archive-safety/v1",
                    "Archive entry is encrypted and cannot be inspected deterministically.",
                    [raw_path],
                )
            if info.compress_type not in SUPPORTED_ZIP_COMPRESSION:
                add_finding(
                    findings,
                    "ARCHIVE_UNSUPPORTED_COMPRESSION",
                    "hazard",
                    "archive-safety/v1",
                    "Archive entry uses an unsupported ZIP compression method.",
                    [raw_path],
                    {"compress_type": info.compress_type},
                )
            payload_items.append((info, local_header, raw_path, entry_type))
            manifest_path = strip_root(raw_path, root)
            if entry_type == "dir":
                manifest_dir = strip_root(zip_path_for_validation(raw_path), root)
                explicit_dirs.add(manifest_dir)
                continue
            add_path_too_long_warning(manifest_path, findings, limits)
            total_size += info.file_size
            if info.file_size > limits.max_entry_size:
                add_finding(
                    findings,
                    "ARCHIVE_ENTRY_SIZE_LIMIT_EXCEEDED",
                    "hazard",
                    "archive-safety/v1",
                    "Archive entry exceeds the configured entry size limit.",
                    [raw_path],
                    {"size": info.file_size, "max_entry_size": limits.max_entry_size},
                )
            if info.compress_size == 0 and info.file_size > 0:
                ratio = float("inf")
            elif info.compress_size == 0:
                ratio = 0.0
            else:
                ratio = info.file_size / max(info.compress_size, 1)
            if ratio > limits.max_compression_ratio:
                add_finding(
                    findings,
                    "ARCHIVE_COMPRESSION_RATIO_EXCEEDED",
                    "hazard",
                    "archive-safety/v1",
                    "Archive entry exceeds the configured compression-ratio limit.",
                    [raw_path],
                    {"ratio": ratio, "max_compression_ratio": limits.max_compression_ratio},
                )
            entries.append(
                Entry(
                    raw_path=raw_path,
                    manifest_path=manifest_path,
                    type=entry_type,
                    size=info.file_size,
                    mode=manifest_mode(zip_unix_mode(info) or 0, entry_type),
                    zip_info=info,
                    zip_header=local_header,
                )
            )
        if total_size > limits.max_total_size:
            add_finding(
                findings,
                "ARCHIVE_TOTAL_SIZE_LIMIT_EXCEEDED",
                "hazard",
                "archive-safety/v1",
                "Archive exceeds the configured total logical size limit.",
                details={"total_size": total_size, "max_total_size": limits.max_total_size},
            )
        check_tree_model(entries, explicit_dirs, findings)
        check_collision_groups([e.manifest_path for e in entries if e.manifest_path], findings)
        if not unsafe_findings(findings, policy):
            actual_total_size = 0
            for info, local_header, raw_path, entry_type in payload_items:
                if unsafe_findings(findings, policy):
                    break
                if entry_type == "dir":
                    _digest, output = file_digest_from_zip(
                        path,
                        info,
                        local_header,
                        raw_path,
                        findings,
                        limits,
                        capture_limit=1,
                        remaining_total_budget=limits.max_total_size - actual_total_size,
                    )
                    if output:
                        add_finding(
                            findings,
                            "ARCHIVE_ZIP_STREAM_INTEGRITY_FAILED",
                            "hazard",
                            "archive-safety/v1",
                            "ZIP directory entry produced decompressed payload bytes.",
                            [raw_path],
                            {"preview_size": len(output)},
                        )
                    continue
                matching_entry = next((entry for entry in entries if entry.zip_info is info), None)
                if matching_entry is None:
                    continue
                matching_entry.digest, payload_preview = file_digest_from_zip(
                    path,
                    info,
                    local_header,
                    raw_path,
                    findings,
                    limits,
                    capture_limit=limits.max_symlink_target_size + 1 if entry_type == "symlink" else 512,
                    remaining_total_budget=limits.max_total_size - actual_total_size,
                )
                if unsafe_findings(findings, policy):
                    break
                if entry_type == "symlink":
                    target = decode_symlink_target(payload_preview, raw_path, findings, limits)
                    matching_entry.target = target
                    check_entry_logical_size(matching_entry, findings, limits)
                    actual_total_size += entry_logical_size(matching_entry)
                    if is_absolute_path(target) or has_path_traversal(target):
                        add_finding(
                            findings,
                            "ARCHIVE_SYMLINK_ESCAPE",
                            "hazard",
                            "archive-safety/v1",
                            "Symlink target is absolute or escapes by traversal.",
                            [raw_path, target],
                        )
                else:
                    matching_entry.preview = payload_preview
                    actual_total_size += matching_entry.size
                    if source_kind == "repo" and is_lfs_pointer(matching_entry):
                        add_finding(
                            findings,
                            "REPO_LFS_POINTER_PRESENT",
                            "info",
                            "repo-completeness/v1",
                            "File appears to be a Git LFS pointer.",
                            [matching_entry.manifest_path],
                        )
            total_size = check_total_logical_size(entries, findings, limits)
    return entries, total_size


def read_tar_entries(
    path: Path,
    limits: Limits,
    findings: list[Finding],
    *,
    source_kind: str,
    capture_method: str,
    blob_size: int,
    policy: RawIntakePolicy,
) -> tuple[list[Entry], int]:
    entries: list[Entry] = []
    explicit_dirs: set[str] = set()
    total_size = 0
    with tarfile.open(path) as tf:
        named_members: list[tuple[tarfile.TarInfo, str]] = []
        member_count = 0
        while True:
            member = tf.next()
            if member is None:
                break
            member_count += 1
            if member_count > limits.max_entries:
                add_finding(
                    findings,
                    "ARCHIVE_ENTRY_LIMIT_EXCEEDED",
                    "hazard",
                    "archive-safety/v1",
                    "Archive exceeds the configured entry count limit.",
                    details={"entry_count": member_count, "max_entries": limits.max_entries},
                )
                break
            if member.size > 0:
                total_size += member.size
                if total_size > limits.max_total_size:
                    add_finding(
                        findings,
                        "ARCHIVE_TOTAL_SIZE_LIMIT_EXCEEDED",
                        "hazard",
                        "archive-safety/v1",
                        "Archive exceeds the configured total logical size limit.",
                        details={"total_size": total_size, "max_total_size": limits.max_total_size},
                    )
                    break
            raw_path = canonical_archive_path(member.name, findings)
            if len(raw_path) > MAX_ARCHIVE_PATH_STRING_LENGTH:
                continue
            named_members.append((member, raw_path))
        raw_names = [raw_path for member, raw_path in named_members if not member.isdir()]
        for dupe in duplicate_paths(raw_names):
            add_finding(
                findings,
                "ARCHIVE_DUPLICATE_ENTRY",
                "hazard",
                "archive-safety/v1",
                "Archive contains an exact duplicate entry path.",
                [dupe],
            )
        root = first_common_archive_root(raw_names) if should_strip_wrapper_root(source_kind, capture_method) else None
        total_size = 0
        for member, raw_path in named_members:
            check_path_hygiene(raw_path, findings, limits, check_portability_length=False)
            manifest_path = strip_root(raw_path, root)
            if member.isdir():
                if member.size != 0:
                    add_finding(
                        findings,
                        "ARCHIVE_TYPE_COLLISION",
                        "hazard",
                        "archive-safety/v1",
                        "TAR directory member carries a non-zero payload size.",
                        [raw_path],
                        {"size": member.size},
                    )
                explicit_dirs.add(strip_root(raw_path.rstrip("/"), root))
                continue
            total_size += max(member.size, 0)
            if member.size > limits.max_entry_size:
                add_finding(
                    findings,
                    "ARCHIVE_ENTRY_SIZE_LIMIT_EXCEEDED",
                    "hazard",
                    "archive-safety/v1",
                    "Archive entry exceeds the configured entry size limit.",
                    [raw_path],
                    {"size": member.size, "max_entry_size": limits.max_entry_size},
                )
            if member.isfile():
                entry_type = "file"
            elif member.issym():
                entry_type = "symlink"
                if member.size != 0:
                    add_finding(
                        findings,
                        "ARCHIVE_TYPE_COLLISION",
                        "hazard",
                        "archive-safety/v1",
                        "TAR symlink member carries a non-zero payload size.",
                        [raw_path],
                        {"size": member.size},
                    )
            else:
                add_finding(
                    findings,
                    "ARCHIVE_SPECIAL_FILE",
                    "hazard",
                    "archive-safety/v1",
                    "Archive member is not a regular file, directory, or symlink.",
                    [raw_path],
                    {"tar_type": str(member.type)},
                )
                continue
            add_path_too_long_warning(manifest_path, findings, limits)
            entries.append(
                Entry(
                    raw_path=raw_path,
                    manifest_path=manifest_path,
                    type=entry_type,
                    size=member.size,
                    mode=manifest_mode(member.mode, entry_type),
                    tar_member=member,
                )
            )
        if total_size > limits.max_total_size and not any(f.code == "ARCHIVE_TOTAL_SIZE_LIMIT_EXCEEDED" for f in findings):
            add_finding(
                findings,
                "ARCHIVE_TOTAL_SIZE_LIMIT_EXCEEDED",
                "hazard",
                "archive-safety/v1",
                "Archive exceeds the configured total logical size limit.",
                details={"total_size": total_size, "max_total_size": limits.max_total_size},
            )
        if blob_size == 0 and total_size > 0:
            ratio = float("inf")
        elif blob_size == 0:
            ratio = 0.0
        else:
            ratio = total_size / max(blob_size, 1)
        if ratio > limits.max_compression_ratio:
            add_finding(
                findings,
                "ARCHIVE_COMPRESSION_RATIO_EXCEEDED",
                "hazard",
                "archive-safety/v1",
                "TAR archive total logical size exceeds the configured compression-ratio limit.",
                details={"ratio": ratio, "max_compression_ratio": limits.max_compression_ratio},
            )
        check_tree_model(entries, explicit_dirs, findings)
        check_collision_groups([e.manifest_path for e in entries if e.manifest_path], findings)
        if not unsafe_findings(findings, policy):
            for entry in entries:
                if entry.tar_member is None:
                    continue
                if entry.type == "symlink":
                    target_bytes = entry.tar_member.linkname.encode("utf-8", errors="surrogateescape")
                    entry.target = decode_symlink_target(target_bytes, entry.raw_path, findings, limits)
                    check_entry_logical_size(entry, findings, limits)
                    if is_absolute_path(entry.target) or has_path_traversal(entry.target):
                        add_finding(
                            findings,
                            "ARCHIVE_SYMLINK_ESCAPE",
                            "hazard",
                            "archive-safety/v1",
                            "Symlink target is absolute or escapes by traversal.",
                            [entry.raw_path, entry.target],
                        )
                else:
                    entry.digest, entry.preview = file_digest_from_tar(tf, entry.tar_member)
                    if source_kind == "repo" and is_lfs_pointer(entry):
                        add_finding(
                            findings,
                            "REPO_LFS_POINTER_PRESENT",
                            "info",
                            "repo-completeness/v1",
                            "File appears to be a Git LFS pointer.",
                            [entry.manifest_path],
                        )
            total_size = check_total_logical_size(entries, findings, limits)
    return entries, total_size


def is_lfs_pointer(entry: Entry) -> bool:
    return entry.preview.startswith(b"version https://git-lfs.github.com/spec/v1\n")


def manifest_entry(entry: Entry) -> dict[str, object]:
    if entry.type == "symlink":
        if entry.target is None:
            raise ValueError(f"symlink target missing for {entry.manifest_path}")
        return {
            "mode": entry.mode,
            "path": entry.manifest_path,
            "target": entry.target,
            "type": "symlink",
        }
    if entry.digest is None:
        raise ValueError(f"file digest missing for {entry.manifest_path}")
    return {
        "digest": entry.digest,
        "mode": entry.mode,
        "path": entry.manifest_path,
        "size": entry.size,
        "type": "file",
    }


def build_manifest(entries: list[Entry], *, state: str = "complete", reason_codes: list[str] | None = None) -> bytes:
    header: dict[str, object] = {
        "profile": MANIFEST_PROFILE,
        "schema": SCHEMA_MANIFEST,
        "state": state,
    }
    if reason_codes:
        header["reason_codes"] = reason_codes
    lines = [json_line(header)]
    if state == "complete":
        for entry in sorted((e for e in entries if e.manifest_path), key=lambda e: e.manifest_path):
            lines.append(json_line(manifest_entry(entry)))
    return ("\n".join(lines) + "\n").encode("utf-8")


def max_severity(findings: list[Finding]) -> str:
    rank = {"none": 0, "info": 1, "warning": 2, "hazard": 3, "error": 4}
    if not findings:
        return "none"
    return max((f.severity for f in findings), key=lambda s: rank.get(s, 0))


def hygiene_predicate_for(source_kind: str) -> str:
    if source_kind == "repo":
        return REPO_HYGIENE_PREDICATE
    return SOURCE_HYGIENE_PREDICATE


def hygiene_profiles_for(
    source_kind: str,
    findings: list[Finding],
    *,
    snapshot_kind: str,
    capture_method: str,
    content_detection_basis: str | None,
) -> list[str]:
    profiles: list[str] = []
    if source_kind == "repo":
        profiles.extend(REPO_HYGIENE_PROFILES)
    elif (
        content_detection_basis == "container_parser"
        or source_kind == "archive"
        or capture_method_suggests_archive(capture_method)
        or snapshot_kind == "tree"
    ):
        profiles.append("archive-safety/v1")
    elif any(f.profile == "archive-safety/v1" for f in findings):
        profiles.append("archive-safety/v1")
    else:
        profiles.append(SOURCE_FIXITY_PROFILE)
    for finding in findings:
        if finding.profile not in profiles:
            profiles.append(finding.profile)
    return sorted(profiles)


def build_hygiene(
    subject_name: str,
    subject_digest: str,
    findings: list[Finding],
    execution_state: str,
    *,
    source_kind: str,
    snapshot_kind: str,
    capture_method: str,
    content_detection_basis: str | None,
    limits: Limits,
    implementation: ImplementationInfo,
) -> tuple[bytes, str]:
    output_findings = prepared_findings(findings)
    predicate_type = hygiene_predicate_for(source_kind)
    digest = subject_digest.split(":", 1)[1] if ":" in subject_digest else subject_digest
    obj = {
        "_type": HYGIENE_TYPE,
        "subject": [
            {
                "name": subject_name,
                "digest": {"sha256": digest},
            }
        ],
        "predicateType": predicate_type,
        "predicate": {
            "checker": {
                "id": INSPECTOR_ID,
                "version": INSPECTOR_VERSION,
                "implementation": implementation.descriptor.to_json(),
            },
            "execution_state": execution_state,
            "profiles": hygiene_profiles_for(
                source_kind,
                output_findings,
                snapshot_kind=snapshot_kind,
                capture_method=capture_method,
                content_detection_basis=content_detection_basis,
            ),
            "parameters": limits_parameters(limits),
            "summary": {
                "finding_count": len(output_findings),
                "max_severity": max_severity(output_findings),
            },
            "findings": [f.to_json() for f in output_findings],
        },
    }
    return json_bytes(obj), predicate_type


def inspect_path(
    path: Path,
    limits: Limits,
    *,
    input_profile: str = "auto",
    capture_method: str = "archive_file",
    source_kind: str = "unknown",
    blob_digest: str | None = None,
    blob_size: int | None = None,
    display_path: Path | None = None,
    policy: RawIntakePolicy,
) -> InspectionResult:
    if blob_digest is None or blob_size is None:
        blob_digest, blob_size = sha256_file(path)
    kind = archive_kind(path)
    findings: list[Finding] = []
    identity_path = display_path or path
    required_archive = source_or_method_requires_archive(source_kind, capture_method)
    expected_archive = input_profile == "archive" or required_archive or (
        input_profile == "auto"
        and suffix_suggests_archive(display_path or path)
        and source_kind != "pdf"
    )
    if input_profile == "blob" and not required_archive:
        kind = "file"
    locator_hint = locator_media_type_hint(identity_path)
    content_type = detect_media_type(path, kind, locator_hint)
    check_content_type_findings(content_type, source_kind, findings, identity_path)
    media_type = content_type.detected_media_type
    entries: list[Entry] = []
    total_size = blob_size
    if kind == "file" and expected_archive:
        add_parse_failed(findings, identity_path, "Input was expected to be an archive but could not be parsed as ZIP or TAR.")
    if kind == "zip":
        try:
            entries, total_size = read_zip_entries(
                path,
                limits,
                findings,
                source_kind=source_kind,
                capture_method=capture_method,
                policy=policy,
            )
        except (zipfile.BadZipFile, RuntimeError, NotImplementedError, OSError) as exc:
            add_parse_failed(findings, identity_path, "ZIP archive parsing failed.", exc)
            kind = "file"
    elif kind == "tar":
        try:
            entries, total_size = read_tar_entries(
                path,
                limits,
                findings,
                source_kind=source_kind,
                capture_method=capture_method,
                blob_size=blob_size,
                policy=policy,
            )
        except (tarfile.TarError, RuntimeError, OSError) as exc:
            add_parse_failed(findings, identity_path, "TAR archive parsing failed.", exc)
            kind = "file"
    if kind == "file" and not expected_archive:
        entry = Entry(
            raw_path=identity_path.name,
            manifest_path=identity_path.name,
            type="file",
            size=blob_size,
            mode="100644",
            digest=blob_digest,
            preview=file_preview(path),
        )
        entries = [entry]
        check_path_hygiene(identity_path.name, findings, limits)
        if source_kind == "repo" and is_lfs_pointer(entry):
            add_finding(
                findings,
                "REPO_LFS_POINTER_PRESENT",
                "info",
                "repo-completeness/v1",
                "File appears to be a Git LFS pointer.",
                [entry.manifest_path],
            )

    if source_kind == "repo" and any(e.manifest_path == ".gitmodules" or e.manifest_path.endswith("/.gitmodules") for e in entries):
        add_finding(
            findings,
            "REPO_SUBMODULE_PRESENT",
            "info",
            "repo-completeness/v1",
            "Snapshot contains a .gitmodules file; submodule content completeness is not proven.",
        )

    final_blob_digest, final_blob_size = sha256_file(path)
    if final_blob_digest != blob_digest or final_blob_size != blob_size:
        add_finding(
            findings,
            "CAPTURE_INPUT_CHANGED_DURING_SCAN",
            "hazard",
            SOURCE_FIXITY_PROFILE,
            "Input file changed while it was being scanned; the tree interpretation is not reliable.",
            [path.name],
            {
                "initial_digest": blob_digest,
                "final_digest": final_blob_digest,
                "initial_size": blob_size,
                "final_size": final_blob_size,
            },
        )
        blob_digest = final_blob_digest
        blob_size = final_blob_size

    unsafe = unsafe_findings(findings, policy)
    if kind == "file" and not unsafe_findings(findings, policy) and not expected_archive:
        snapshot_kind = "blob"
        snapshot_id = "vsnap:1:blob:" + blob_digest
        manifest_bytes = build_manifest(entries, state="blob")
        disposition = policy.complete_disposition
        reason_codes: list[str] = []
        execution_state = "complete"
    elif unsafe:
        reason_codes = sorted({f.code for f in unsafe})
        manifest_bytes = build_manifest([], state="unavailable", reason_codes=reason_codes)
        snapshot_kind = "blob"
        snapshot_id = "vsnap:1:blob:" + blob_digest
        disposition = policy.unsafe_disposition
        execution_state = "failed" if any(f.code == "ARCHIVE_PARSE_FAILED" for f in unsafe) else "partial"
    else:
        manifest_bytes = build_manifest(entries)
        manifest_digest = digest_bytes(manifest_bytes)
        snapshot_kind = "tree"
        snapshot_id = "vsnap:1:tree:" + manifest_digest
        disposition = policy.complete_disposition
        reason_codes = []
        execution_state = "complete"

    manifest_digest = digest_bytes(manifest_bytes)
    return InspectionResult(
        blob_digest=blob_digest,
        blob_size=blob_size,
        media_type=media_type,
        content_type=content_type,
        snapshot_kind=snapshot_kind,
        snapshot_id=snapshot_id,
        manifest_bytes=manifest_bytes,
        manifest_digest=manifest_digest,
        findings=findings,
        disposition=disposition,
        reason_codes=reason_codes,
        execution_state=execution_state,
        entry_count=len(entries),
        total_logical_size=total_size,
    )


def default_source_id(path: Path, blob_digest: str) -> str:
    return "vsrc:1:content:" + blob_digest


def failed_result_from_exception(
    path: Path,
    exc: BaseException,
    *,
    blob_digest: str,
    blob_size: int,
    display_path: Path | None = None,
) -> InspectionResult:
    identity_path = display_path or path
    try:
        inspection_kind = archive_kind(path)
    except Exception:
        inspection_kind = "file"
    content_type = detect_media_type(path, inspection_kind, locator_media_type_hint(identity_path))
    finding = Finding(
        code="SCANNER_UNHANDLED_EXCEPTION",
        severity="hazard",
        profile=SOURCE_FIXITY_PROFILE,
        message="Scanner failed before it could complete structured inspection.",
        paths=[identity_path.name],
        details={
            "exception_type": type(exc).__name__,
            "exception": str(exc),
        },
    )
    reason_codes = ["SCANNER_UNHANDLED_EXCEPTION"]
    manifest_bytes = build_manifest([], state="unavailable", reason_codes=reason_codes)
    return InspectionResult(
        blob_digest=blob_digest,
        blob_size=blob_size,
        media_type=content_type.detected_media_type,
        content_type=content_type,
        snapshot_kind="blob",
        snapshot_id="vsnap:1:blob:" + blob_digest,
        manifest_bytes=manifest_bytes,
        manifest_digest=digest_bytes(manifest_bytes),
        findings=[finding],
        disposition="quarantined",
        reason_codes=reason_codes,
        execution_state="failed",
        entry_count=0,
        total_logical_size=0,
    )


def build_capture_envelope(
    args: argparse.Namespace,
    result: InspectionResult,
    hygiene_digest: str,
    hygiene_size: int,
    hygiene_predicate_type: str,
    *,
    implementation: ImplementationInfo,
    policy: RawIntakePolicy,
) -> dict[str, object]:
    capture_id = args.capture_id or f"urn:uuid:{uuid.uuid4()}"
    source_id = args.source_id or default_source_id(Path(args.input), result.blob_digest)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    source_path = Path(args.input)
    requested_locator = args.requested_locator or default_locator_for(source_path)
    resolution: dict[str, object] = {
        "selector": {
            "kind": args.selector_kind,
            "value": args.selector_value,
        }
    }
    if args.revision_kind and args.revision_value:
        resolution["revision"] = {
            "kind": args.revision_kind,
            "value": args.revision_value,
        }
    snapshot: dict[str, object] = {
        "snapshot_id": result.snapshot_id,
        "kind": result.snapshot_kind,
    }
    if result.snapshot_kind in {"tree", "partial_tree"}:
        snapshot["manifest"] = {
            "media_type": "application/vnd.vaks.snapshot-manifest.v1+jsonl",
            "size": len(result.manifest_bytes),
            "digest": result.manifest_digest,
        }
    source_obj: dict[str, object] = {
        "source_id": source_id,
        "kind": args.source_kind,
        "requested_locator": requested_locator,
    }
    if args.resolved_locator:
        source_obj["resolved_locator"] = args.resolved_locator
    return {
        "schema": SCHEMA_CAPTURE,
        "capture_id": capture_id,
        "observed_at": args.observed_at or now,
        "producer": {
            "id": INSPECTOR_ID,
            "version": INSPECTOR_VERSION,
            "implementation": implementation.descriptor.to_json(),
        },
        "source": source_obj,
        "resolution": resolution,
        "observation": {
            "state": "captured" if result.execution_state == "complete" else "partial",
            "capture_method": args.capture_method,
            "blob": {
                "media_type": result.media_type,
                "size": result.blob_size,
                "digest": result.blob_digest,
            },
            "content_type": result.content_type.to_json(),
        },
        "snapshot": snapshot,
        "change": {
            "state": args.change_state,
            "compared_to_capture_id": args.compared_to_capture_id,
        },
        "inspection_refs": [
            {
                "media_type": "application/vnd.in-toto+json",
                "size": hygiene_size,
                "digest": hygiene_digest,
                "predicate_type": hygiene_predicate_type,
            }
        ],
        "fidelity": {
            "state": "not_checked",
        },
        "raw_handling": {
            "disposition": result.disposition,
            "policy": {
                "id": policy.id,
                "digest": policy.digest,
            },
            "reason_codes": result.reason_codes,
        },
    }


def absolute_without_symlink_resolution(path: Path) -> Path:
    if path.is_absolute():
        return Path(os.path.abspath(os.fspath(path)))
    return Path(os.path.abspath(os.fspath(Path.cwd() / path)))


def assert_no_symlink_components(path: Path) -> None:
    full = absolute_without_symlink_resolution(path)
    parts = full.parts
    if not parts:
        return
    current = Path(parts[0])
    for part in parts[1:]:
        current = current / part
        if current.is_symlink():
            raise FileExistsError(f"refusing symlink in output path component: {current}")


def assert_safe_output_dir(out_dir: Path, input_path: Path) -> None:
    assert_no_symlink_components(out_dir)
    resolved_input = input_path.resolve()
    if out_dir.exists():
        if out_dir.is_symlink():
            raise FileExistsError(f"refusing to use symlink output directory: {out_dir}")
        if not out_dir.is_dir():
            raise FileExistsError(f"output path exists and is not a directory: {out_dir}")
        if any(out_dir.iterdir()):
            raise FileExistsError(f"output directory must be empty: {out_dir}")
    else:
        out_dir.mkdir(parents=True)
    for name in ["capture-envelope.json", "snapshot-manifest.jsonl", "snapshot-hygiene.intoto.json"]:
        target = out_dir / name
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"refusing to overwrite existing output target: {target}")
        try:
            if target.resolve() == resolved_input:
                raise FileExistsError(f"output target resolves to input source: {target}")
        except FileNotFoundError:
            pass


def write_exclusive(path: Path, data: bytes) -> None:
    assert_no_symlink_components(path.parent)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags, 0o600)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
    except Exception:
        try:
            path.unlink(missing_ok=True)
        finally:
            raise


def write_outputs(
    out_dir: Path,
    input_path: Path,
    envelope: dict[str, object],
    manifest: bytes,
    hygiene: bytes,
    *,
    policy_file: Path,
    implementation_manifest: Path,
) -> None:
    assert_safe_output_dir(out_dir, input_path)
    parent = out_dir.parent if out_dir.parent != Path("") else Path(".")
    parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{out_dir.name}.staging-", dir=parent))
    try:
        write_exclusive(staging / "capture-envelope.json", json_bytes(envelope))
        write_exclusive(staging / "snapshot-manifest.jsonl", manifest)
        write_exclusive(staging / "snapshot-hygiene.intoto.json", hygiene)
        validate_source_capture_bundle.validate_bundle(
            staging,
            profile="enterprise-alpha1",
            policy_file=policy_file,
            implementation_manifest=implementation_manifest,
        )
        if out_dir.exists():
            if any(out_dir.iterdir()):
                raise FileExistsError(f"output directory became non-empty before commit: {out_dir}")
            out_dir.rmdir()
        staging.rename(out_dir)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect a source snapshot without extracting it.")
    parser.add_argument("input", help="Source blob/archive path to inspect.")
    parser.add_argument("--out", required=True, help="Explicit output directory for capture artifacts.")
    parser.add_argument("--source-id", help="Stable vsrc:1 source ID. Defaults to content-addressed fallback.")
    parser.add_argument("--source-kind", default="archive", choices=["repo", "file", "archive", "pdf", "video", "web", "unknown"])
    parser.add_argument("--requested-locator")
    parser.add_argument("--resolved-locator")
    parser.add_argument("--selector-kind", default="path")
    parser.add_argument("--selector-value", default="")
    parser.add_argument("--revision-kind", choices=REVISION_KINDS)
    parser.add_argument("--revision-value")
    parser.add_argument("--input-profile", default="auto", choices=["auto", "blob", "archive"])
    parser.add_argument("--capture-method", default="local_file", choices=["provider_archive", "git_clone", "api", "upload", "local_file", "archive_file"])
    parser.add_argument("--capture-id")
    parser.add_argument("--observed-at")
    parser.add_argument("--change-state", default="unknown", choices=["first_seen", "same_snapshot", "new_snapshot", "unknown"])
    parser.add_argument("--compared-to-capture-id")
    parser.add_argument("--allow-content-source-fallback", action="store_true")
    parser.add_argument("--policy-id", default="vaks-raw-intake-default")
    parser.add_argument("--policy-file", default=str(default_policy_path()))
    parser.add_argument("--implementation-manifest", default=str(default_implementation_manifest_path()))
    parser.add_argument("--max-input-blob-size", type=int, default=Limits.max_input_blob_size)
    parser.add_argument("--max-entries", type=int, default=Limits.max_entries)
    parser.add_argument("--max-total-size", type=int, default=Limits.max_total_size)
    parser.add_argument("--max-entry-size", type=int, default=Limits.max_entry_size)
    parser.add_argument("--max-compression-ratio", type=float, default=Limits.max_compression_ratio)
    parser.add_argument("--max-path-depth", type=int, default=Limits.max_path_depth)
    parser.add_argument("--max-path-length", type=int, default=Limits.max_path_length)
    parser.add_argument("--max-symlink-target-size", type=int, default=Limits.max_symlink_target_size)
    return parser


def parse_observed_at(value: str) -> datetime:
    text = value
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError("timestamp has no timezone")
    return parsed


def validate_args(parser: argparse.ArgumentParser, args: argparse.Namespace, input_path: Path) -> Limits:
    if input_path.is_symlink():
        parser.error(f"input symlink is not accepted for immutable capture: {input_path}")
    if args.capture_id and not CAPTURE_ID_RE.match(args.capture_id):
        parser.error("--capture-id must be a valid urn:uuid")
    if args.source_id and not SOURCE_ID_RE.match(args.source_id):
        parser.error("--source-id must be a valid vsrc:1 ID without whitespace/control characters")
    if args.input_profile == "blob" and source_or_method_requires_archive(args.source_kind, args.capture_method):
        parser.error("--input-profile blob cannot override archive intent from source kind or capture method")
    if bool(args.revision_kind) != bool(args.revision_value):
        parser.error("--revision-kind and --revision-value must be provided together")
    if args.revision_value is not None and not str(args.revision_value).strip():
        parser.error("--revision-value must be non-blank")
    if args.observed_at:
        try:
            parse_observed_at(args.observed_at)
        except ValueError as exc:
            parser.error(f"--observed-at must be an ISO 8601 timestamp with timezone: {exc}")
    if args.change_state == "first_seen" and args.compared_to_capture_id is not None:
        parser.error("--change-state first_seen must not carry --compared-to-capture-id")
    if args.change_state in {"same_snapshot", "new_snapshot"}:
        if not args.compared_to_capture_id or not CAPTURE_ID_RE.match(args.compared_to_capture_id):
            parser.error("--change-state same_snapshot/new_snapshot require a valid --compared-to-capture-id")
    if args.change_state == "unknown" and args.compared_to_capture_id is not None:
        parser.error("--change-state unknown must not carry --compared-to-capture-id")
    for name in ["requested_locator", "resolved_locator", "selector_kind", "policy_id", "policy_file", "implementation_manifest"]:
        value = getattr(args, name)
        if value is not None and not str(value).strip():
            parser.error(f"--{name.replace('_', '-')} must be non-blank when provided")
    int_limits = {
        "max_input_blob_size": args.max_input_blob_size,
        "max_entries": args.max_entries,
        "max_total_size": args.max_total_size,
        "max_entry_size": args.max_entry_size,
        "max_path_depth": args.max_path_depth,
        "max_path_length": args.max_path_length,
        "max_symlink_target_size": args.max_symlink_target_size,
    }
    for name, value in int_limits.items():
        if not isinstance(value, int) or value < 1:
            parser.error(f"--{name.replace('_', '-')} must be a positive integer")
    if (
        not isinstance(args.max_compression_ratio, (int, float))
        or not math.isfinite(args.max_compression_ratio)
        or args.max_compression_ratio <= 0
    ):
        parser.error("--max-compression-ratio must be a finite positive number")
    return Limits(
        max_input_blob_size=args.max_input_blob_size,
        max_entries=args.max_entries,
        max_total_size=args.max_total_size,
        max_entry_size=args.max_entry_size,
        max_compression_ratio=args.max_compression_ratio,
        max_path_depth=args.max_path_depth,
        max_path_length=args.max_path_length,
        max_symlink_target_size=args.max_symlink_target_size,
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    input_path = Path(args.input)
    if not input_path.exists() or not input_path.is_file():
        parser.error(f"input is not a file: {input_path}")
    if (
        not args.source_id
        and args.source_kind in {"repo", "web", "video"}
        and not args.allow_content_source_fallback
    ):
        parser.error(
            "--source-id is required for repo/web/video sources; use --allow-content-source-fallback only for isolated content-addressed captures"
        )
    limits = validate_args(parser, args, input_path)
    try:
        implementation = load_implementation_info(Path(args.implementation_manifest))
        policy = load_raw_intake_policy(Path(args.policy_file), args.policy_id)
        try:
            policy_rel = str(Path(args.policy_file).resolve().relative_to(implementation.root)).replace("\\", "/")
        except ValueError as exc:
            raise ImplementationPinningError(
                "CAPTURE_POLICY_PIN_MISMATCH",
                "runtime policy file is outside the implementation root",
                component=str(args.policy_file),
            ) from exc
        expected_policy_digest = implementation.component_digests.get(policy_rel)
        if expected_policy_digest is None:
            raise ImplementationPinningError(
                "CAPTURE_POLICY_PIN_MISMATCH",
                "runtime policy file is not pinned by the implementation manifest",
                component=policy_rel,
            )
        if expected_policy_digest != digest_file(policy.path):
            raise ImplementationPinningError(
                "CAPTURE_POLICY_PIN_MISMATCH",
                "runtime policy file digest does not match implementation manifest",
                component=policy_rel,
            )
    except ImplementationPinningError as exc:
        payload: dict[str, object] = {
            "status": "fail",
            "code": exc.code,
            "error": str(exc),
            "bundle_created": False,
        }
        if exc.component:
            payload["component"] = exc.component
        print(json.dumps(payload, allow_nan=False, ensure_ascii=False, sort_keys=True))
        return 4
    try:
        materialized = materialize_input_copy(input_path, limits.max_input_blob_size)
    except InputBlobLimitExceeded as exc:
        print(
            json.dumps(
                {
                    "status": "fail",
                    "code": "CAPTURE_INPUT_BLOB_LIMIT_EXCEEDED",
                    "limit": exc.limit,
                    "observed_at_least": exc.observed_at_least,
                    "bundle_created": False,
                },
                allow_nan=False,
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 3
    except Exception as exc:
        print(
            json.dumps(
                {
                    "status": "fail",
                    "code": "CAPTURE_INPUT_COPY_FAILED",
                    "error": "input could not be copied and hashed; no capture bundle was created",
                    "exception_type": type(exc).__name__,
                    "exception": str(exc),
                    "bundle_created": False,
                },
                allow_nan=False,
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 3
    try:
        try:
            result = inspect_path(
                materialized.path,
                limits,
                input_profile=args.input_profile,
                capture_method=args.capture_method,
                source_kind=args.source_kind,
                blob_digest=materialized.blob_digest,
                blob_size=materialized.blob_size,
                display_path=input_path,
                policy=policy,
            )
        except Exception as exc:
            result = failed_result_from_exception(
                materialized.path,
                exc,
                blob_digest=materialized.blob_digest,
                blob_size=materialized.blob_size,
                display_path=input_path,
            )
        subject_name = "snapshot-manifest" if result.snapshot_kind == "tree" else "capture-blob"
        subject_digest = result.manifest_digest if result.snapshot_kind == "tree" else result.blob_digest
        hygiene, hygiene_predicate_type = build_hygiene(
            subject_name,
            subject_digest,
            result.findings,
            result.execution_state,
            source_kind=args.source_kind,
            snapshot_kind=result.snapshot_kind,
            capture_method=args.capture_method,
            content_detection_basis=result.content_type.detection_basis,
            limits=limits,
            implementation=implementation,
        )
        hygiene_digest = digest_bytes(hygiene)
        envelope = build_capture_envelope(
            args,
            result,
            hygiene_digest,
            len(hygiene),
            hygiene_predicate_type,
            implementation=implementation,
            policy=policy,
        )
        write_outputs(
            Path(args.out),
            input_path,
            envelope,
            result.manifest_bytes,
            hygiene,
            policy_file=policy.path,
            implementation_manifest=implementation.manifest_path,
        )
        output_findings = prepared_findings(result.findings)
        summary = {
            "capture_envelope": str(Path(args.out) / "capture-envelope.json"),
            "snapshot_manifest": str(Path(args.out) / "snapshot-manifest.jsonl"),
            "snapshot_hygiene": str(Path(args.out) / "snapshot-hygiene.intoto.json"),
            "snapshot_id": result.snapshot_id,
            "raw_disposition": result.disposition,
            "finding_count": len(output_findings),
            "max_severity": max_severity(output_findings),
        }
        print(json.dumps(summary, allow_nan=False, ensure_ascii=False, sort_keys=True))
        return 0
    finally:
        materialized.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
