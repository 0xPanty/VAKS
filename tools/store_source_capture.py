#!/usr/bin/env python
"""Store validated Source Capture Envelope bundles in a local filesystem CAS.

This is a persistence layer for Raw Capture artifacts only. It does not create
candidate, reviewed, evidence-support, or action artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

import validate_source_capture_bundle


STORE_SCHEMA = "urn:vaks:schema:source-capture-store:v1"
RECEIPT_SCHEMA = "urn:vaks:schema:capture-storage-receipt:v1"
BUNDLE_ID_SCHEMA = "urn:vaks:identity:capture-bundle:v1"
STORE_LAYOUT = "vaks-source-capture-store/v1"
STORE_LAYOUT_VERSION = "1"
DIGEST_PROFILE = "vaks-capture-bundle-id/v1"
SHA256_RE = validate_source_capture_bundle.DIGEST_RE
CAPTURE_ID_RE = validate_source_capture_bundle.CAPTURE_ID_RE
REQUIRED_BUNDLE_ARTIFACTS = {
    "capture-envelope.json": "application/vnd.vaks.source-capture.v1+json",
    "snapshot-hygiene.intoto.json": "application/vnd.in-toto+json",
    "snapshot-manifest.jsonl": "application/vnd.vaks.snapshot-manifest.v1+jsonl",
}
IMPLEMENTATION_CONTEXT_NAME = "source-capture-implementation-manifest.json"
POLICY_CONTEXT_NAME = "raw-intake-policy.json"
CHUNK_SIZE = 1024 * 1024
EXPECTED_STORED_IMPLEMENTATION_COMPONENTS = validate_source_capture_bundle.EXPECTED_IMPLEMENTATION_COMPONENTS
POLICY_COMPONENT_PATH = validate_source_capture_bundle.POLICY_COMPONENT_PATH


class StoreError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class FileDescriptor:
    name: str
    size: int
    digest: str
    media_type: str | None = None


@dataclass(frozen=True)
class StoreInfo:
    root: Path
    meta: dict[str, Any]


@dataclass(frozen=True)
class VerifiedStoredCapture:
    capture_id: str
    capture_dir: str
    bundle_digest: str
    raw_blob_retention_state: str
    raw_blob_digest: str
    raw_blob_store_path: str | None


def now_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def script_root() -> Path:
    return Path(__file__).resolve().parent.parent


def default_implementation_manifest_path() -> Path:
    return script_root() / "tools" / "source_capture_implementation_manifest.json"


def default_policy_path() -> Path:
    return script_root() / "policies" / "source-capture" / "raw-intake-default-v1.json"


def canonical_json_bytes(obj: dict[str, Any]) -> bytes:
    return validate_source_capture_bundle.canonical_json_bytes(obj)


def sha256_bytes(data: bytes) -> str:
    return validate_source_capture_bundle.sha256_bytes(data)


def digest_file(path: Path) -> str:
    return validate_source_capture_bundle.digest_file(path)


def is_reparse_or_symlink(path: Path) -> bool:
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        return False
    if stat.S_ISLNK(st.st_mode):
        return True
    attrs = getattr(st, "st_file_attributes", 0)
    return bool(attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def absolute_no_resolve(path: Path) -> Path:
    if path.is_absolute():
        return path
    return Path.cwd() / path


def ensure_no_reparse_components(path: Path, code: str, context: str) -> None:
    """Reject symlink/reparse points in every existing component of a path."""
    absolute = absolute_no_resolve(path)
    current = Path(absolute.anchor)
    parts = absolute.parts[1:] if absolute.anchor else absolute.parts
    for part in parts:
        current = current / part
        try:
            st = os.lstat(current)
        except FileNotFoundError:
            break
        if stat.S_ISLNK(st.st_mode):
            raise StoreError(code, f"{context} path component must not be a symlink: {current}")
        attrs = getattr(st, "st_file_attributes", 0)
        if attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):
            raise StoreError(code, f"{context} path component must not be a reparse point: {current}")
        if current != absolute and not stat.S_ISDIR(st.st_mode):
            raise StoreError(code, f"{context} parent component must be a directory: {current}")


def require_existing_dir(path: Path, code: str, context: str) -> None:
    ensure_no_reparse_components(path, code, context)
    if is_reparse_or_symlink(path):
        raise StoreError(code, f"{context} must not be a symlink or reparse point: {path}")
    try:
        st = os.lstat(path)
    except FileNotFoundError as exc:
        raise StoreError(code, f"{context} does not exist: {path}") from exc
    if not stat.S_ISDIR(st.st_mode):
        raise StoreError(code, f"{context} must be a directory: {path}")


def require_regular_file(path: Path, code: str, context: str) -> None:
    if is_reparse_or_symlink(path):
        raise StoreError(code, f"{context} must not be a symlink or reparse point: {path}")
    try:
        st = os.lstat(path)
    except FileNotFoundError as exc:
        raise StoreError(code, f"{context} does not exist: {path}") from exc
    if not stat.S_ISREG(st.st_mode):
        raise StoreError(code, f"{context} must be a regular file: {path}")


def ensure_no_unsafe_existing_path(path: Path, code: str, context: str) -> None:
    if path.exists() or path.is_symlink():
        if is_reparse_or_symlink(path):
            raise StoreError(code, f"{context} must not be a symlink or reparse point: {path}")


def safe_relative_posix(path: str, context: str) -> None:
    if "\\" in path or path.startswith("/") or ":" in PurePosixPath(path).parts[0]:
        raise StoreError("STORE_RECEIPT_PATH_INVALID", f"{context} must be a relative POSIX path")
    if any(part in {"", ".", ".."} for part in PurePosixPath(path).parts):
        raise StoreError("STORE_RECEIPT_PATH_INVALID", f"{context} must not contain empty, dot, or parent segments")


def write_exclusive(path: Path, data: bytes, mode: int = 0o600) -> None:
    ensure_no_unsafe_existing_path(path, "STORE_OUTPUT_EXISTS", "output path")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    flags |= getattr(os, "O_BINARY", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(str(path), flags, mode)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
    except Exception:
        try:
            path.unlink()
        except OSError:
            pass
        raise


def write_json_exclusive(path: Path, obj: dict[str, Any]) -> FileDescriptor:
    data = canonical_json_bytes(obj)
    write_exclusive(path, data)
    return FileDescriptor(name=path.name, size=len(data), digest=sha256_bytes(data))


def read_json(path: Path) -> dict[str, Any]:
    return validate_source_capture_bundle.read_json(path)


def copy_regular_file(src: Path, dst: Path, *, name: str, media_type: str | None = None) -> FileDescriptor:
    require_regular_file(src, "STORE_INPUT_UNSAFE", name)
    ensure_no_unsafe_existing_path(dst, "STORE_OUTPUT_EXISTS", name)
    h = hashlib.sha256()
    size = 0
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    flags |= getattr(os, "O_BINARY", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(str(dst), flags, 0o600)
    try:
        with src.open("rb") as source, os.fdopen(fd, "wb") as target:
            for chunk in iter(lambda: source.read(CHUNK_SIZE), b""):
                size += len(chunk)
                h.update(chunk)
                target.write(chunk)
            target.flush()
            os.fsync(target.fileno())
    except Exception:
        try:
            dst.unlink()
        except OSError:
            pass
        raise
    return FileDescriptor(name=name, size=size, digest="sha256:" + h.hexdigest(), media_type=media_type)


def hash_existing_regular_file(path: Path, code: str, context: str) -> FileDescriptor:
    require_regular_file(path, code, context)
    return FileDescriptor(name=path.name, size=path.stat().st_size, digest=digest_file(path))


def create_store(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.store_root)
    ensure_no_reparse_components(root, "STORE_ROOT_UNSAFE", "store root")
    if root.exists() or root.is_symlink():
        require_existing_dir(root, "STORE_ROOT_UNSAFE", "store root")
        if (root / "store.json").exists():
            raise StoreError("STORE_ALREADY_INITIALIZED", "store.json already exists")
        if any(root.iterdir()):
            raise StoreError("STORE_ROOT_NOT_EMPTY", "store root is non-empty but has no store.json")
    else:
        root.mkdir(parents=True)
    require_existing_dir(root, "STORE_ROOT_UNSAFE", "store root")
    meta = {
        "schema": STORE_SCHEMA,
        "layout_version": STORE_LAYOUT_VERSION,
        "store_instance_id": "urn:uuid:" + str(uuid.uuid4()),
        "created_at": now_z(),
        "content_addressing": {
            "algorithm": "sha256",
            "layout": "prefix-2/v1",
        },
    }
    write_json_exclusive(root / "store.json", meta)
    (root / "blobs" / "sha256").mkdir(parents=True, exist_ok=False)
    (root / "captures").mkdir(exist_ok=False)
    (root / ".staging").mkdir(exist_ok=False)
    return {"status": "pass", "store_root": str(root), "store_instance_id": meta["store_instance_id"]}


def load_store(root: Path) -> StoreInfo:
    ensure_no_reparse_components(root, "STORE_ROOT_UNSAFE", "store root")
    require_existing_dir(root, "STORE_ROOT_UNSAFE", "store root")
    store_json = root / "store.json"
    require_regular_file(store_json, "STORE_MISSING", "store.json")
    try:
        meta = read_json(store_json)
        validate_source_capture_bundle.exact_keys(
            meta,
            {"schema", "layout_version", "store_instance_id", "created_at", "content_addressing"},
            {"schema", "layout_version", "store_instance_id", "created_at", "content_addressing"},
            "store.json",
        )
    except validate_source_capture_bundle.ValidationError as exc:
        raise StoreError("STORE_INVALID", str(exc)) from exc
    except (OSError, UnicodeError) as exc:
        raise StoreError("STORE_IO_ERROR", f"could not read store.json: {exc}") from exc
    if meta.get("schema") != STORE_SCHEMA or meta.get("layout_version") != STORE_LAYOUT_VERSION:
        raise StoreError("STORE_UNSUPPORTED_LAYOUT", "store layout is unsupported")
    if not isinstance(meta.get("store_instance_id"), str) or not meta["store_instance_id"].startswith("urn:uuid:"):
        raise StoreError("STORE_INVALID", "store_instance_id must be a urn:uuid")
    try:
        parsed_store_uuid = uuid.UUID(meta["store_instance_id"].split("urn:uuid:", 1)[1])
    except (ValueError, IndexError) as exc:
        raise StoreError("STORE_INVALID", "store_instance_id must be a valid urn:uuid") from exc
    if meta["store_instance_id"] != "urn:uuid:" + str(parsed_store_uuid):
        raise StoreError("STORE_INVALID", "store_instance_id must be a canonical lowercase urn:uuid")
    try:
        validate_source_capture_bundle.parse_datetime(meta.get("created_at"), "store.created_at")
    except validate_source_capture_bundle.ValidationError as exc:
        raise StoreError("STORE_INVALID", str(exc)) from exc
    content = meta.get("content_addressing")
    if not isinstance(content, dict) or content.get("algorithm") != "sha256" or content.get("layout") != "prefix-2/v1":
        raise StoreError("STORE_UNSUPPORTED_LAYOUT", "store content addressing is unsupported")
    for rel in ["blobs", "blobs/sha256", "captures", ".staging"]:
        require_existing_dir(root / rel, "STORE_LAYOUT_INCOMPLETE", rel)
    return StoreInfo(root=root, meta=meta)


def capture_dir_name(capture_id: str) -> str:
    if not CAPTURE_ID_RE.match(capture_id):
        raise StoreError("CAPTURE_ID_INVALID", "capture_id must be a valid urn:uuid")
    return capture_id.split("urn:uuid:", 1)[1].lower()


def cas_path(root: Path, digest: str) -> tuple[Path, str]:
    if not SHA256_RE.match(digest):
        raise StoreError("DIGEST_INVALID", "digest must be sha256:<64 lowercase hex>")
    hex_digest = digest.split(":", 1)[1]
    rel = f"blobs/sha256/{hex_digest[:2]}/{hex_digest}"
    return root / rel, rel


def expected_raw_blob_store_path(digest: str) -> str:
    return cas_path(Path("."), digest)[1]


def expected_implementation_store_path(capture_dir: str) -> str:
    return f"captures/{capture_dir}/validation-context/{IMPLEMENTATION_CONTEXT_NAME}"


def expected_policy_store_path(capture_dir: str) -> str:
    return f"captures/{capture_dir}/validation-context/{POLICY_CONTEXT_NAME}"


def ensure_cas_prefix_dir(store: StoreInfo, digest: str) -> Path:
    target, _rel = cas_path(store.root, digest)
    base = store.root / "blobs" / "sha256"
    require_existing_dir(base, "STORE_LAYOUT_INCOMPLETE", "blobs/sha256")
    prefix_dir = target.parent
    ensure_no_reparse_components(prefix_dir, "STORE_BLOB_PATH_UNSAFE", "CAS prefix directory")
    if prefix_dir.exists() or prefix_dir.is_symlink():
        require_existing_dir(prefix_dir, "STORE_BLOB_PATH_UNSAFE", "CAS prefix directory")
        return prefix_dir
    try:
        os.mkdir(prefix_dir, 0o700)
    except FileExistsError:
        require_existing_dir(prefix_dir, "STORE_BLOB_PATH_UNSAFE", "CAS prefix directory")
    except OSError as exc:
        raise StoreError("STORE_WRITE_FAILED", f"could not create CAS prefix directory: {exc}") from exc
    require_existing_dir(prefix_dir, "STORE_BLOB_PATH_UNSAFE", "CAS prefix directory")
    return prefix_dir


def verify_existing_cas_blob(target: Path, expected_digest: str, expected_size: int) -> dict[str, Any]:
    existing = hash_existing_regular_file(target, "STORE_BLOB_FIXITY_MISMATCH", "existing CAS blob")
    if existing.digest != expected_digest or existing.size != expected_size:
        raise StoreError("STORE_BLOB_FIXITY_MISMATCH", "existing CAS blob does not match its digest path")
    return {
        "retention_state": "retained",
        "media_type": None,
        "size": expected_size,
        "digest": expected_digest,
        "store_path": expected_raw_blob_store_path(expected_digest),
    }


def load_stored_implementation_manifest(path: Path) -> dict[str, Any]:
    manifest = read_json(path)
    validate_source_capture_bundle.exact_keys(
        manifest,
        {"schema", "id", "version", "components", "runtime"},
        {"schema", "id", "version", "components", "runtime"},
        "stored implementation manifest",
    )
    if manifest.get("schema") != validate_source_capture_bundle.IMPLEMENTATION_SCHEMA:
        raise StoreError("STORE_CONTEXT_FIXITY_MISMATCH", "stored implementation manifest schema mismatch")
    if manifest.get("id") != validate_source_capture_bundle.IMPLEMENTATION_ID:
        raise StoreError("STORE_CONTEXT_FIXITY_MISMATCH", "stored implementation manifest id mismatch")
    if manifest.get("version") != validate_source_capture_bundle.IMPLEMENTATION_VERSION:
        raise StoreError("STORE_CONTEXT_FIXITY_MISMATCH", "stored implementation manifest version mismatch")
    components = manifest.get("components")
    if not isinstance(components, list):
        raise StoreError("STORE_CONTEXT_FIXITY_MISMATCH", "stored implementation manifest components must be a list")
    seen: set[str] = set()
    component_digests: dict[str, str] = {}
    for idx, component in enumerate(components):
        try:
            validate_source_capture_bundle.exact_keys(
                component,
                {"path", "digest"},
                {"path", "digest"},
                f"stored implementation manifest component[{idx}]",
            )
            rel = validate_source_capture_bundle.require_string(component.get("path"), f"stored implementation manifest component[{idx}].path")
            digest = validate_source_capture_bundle.require_digest(
                component.get("digest"),
                f"stored implementation manifest component[{idx}].digest",
            )
        except validate_source_capture_bundle.ValidationError as exc:
            raise StoreError("STORE_CONTEXT_FIXITY_MISMATCH", str(exc)) from exc
        if "\\" in rel or rel.startswith("/") or ".." in PurePosixPath(rel).parts:
            raise StoreError("STORE_CONTEXT_FIXITY_MISMATCH", f"stored implementation component path is invalid: {rel}")
        if rel in seen:
            raise StoreError("STORE_CONTEXT_FIXITY_MISMATCH", f"duplicate stored implementation component: {rel}")
        seen.add(rel)
        component_digests[rel] = digest
    if seen != EXPECTED_STORED_IMPLEMENTATION_COMPONENTS:
        missing = sorted(EXPECTED_STORED_IMPLEMENTATION_COMPONENTS - seen)
        extra = sorted(seen - EXPECTED_STORED_IMPLEMENTATION_COMPONENTS)
        raise StoreError("STORE_CONTEXT_FIXITY_MISMATCH", f"stored implementation component set mismatch; missing={missing}; extra={extra}")
    runtime = manifest.get("runtime")
    try:
        validate_source_capture_bundle.exact_keys(runtime, {"language", "minimum_version"}, {"language", "minimum_version"}, "stored implementation runtime")
    except validate_source_capture_bundle.ValidationError as exc:
        raise StoreError("STORE_CONTEXT_FIXITY_MISMATCH", str(exc)) from exc
    if runtime.get("language") != "python" or runtime.get("minimum_version") != "3.10":
        raise StoreError("STORE_CONTEXT_FIXITY_MISMATCH", "stored implementation runtime is invalid")
    return {
        "descriptor": {
            "media_type": validate_source_capture_bundle.IMPLEMENTATION_MEDIA_TYPE,
            "size": path.stat().st_size,
            "digest": digest_file(path),
        },
        "component_digests": component_digests,
    }


def validate_bundle_against_stored_context(bundle_dir: Path, implementation_manifest: Path, policy_file: Path) -> None:
    implementation = load_stored_implementation_manifest(implementation_manifest)
    try:
        policy = validate_source_capture_bundle.load_policy(policy_file)
        validate_source_capture_bundle.validate_bundle(bundle_dir, profile="base", policy_file=policy_file)
    except validate_source_capture_bundle.ValidationError as exc:
        raise StoreError("BUNDLE_VALIDATION_FAILED", str(exc)) from exc
    policy_digest = digest_file(policy_file)
    if policy_digest != implementation["component_digests"][POLICY_COMPONENT_PATH]:
        raise StoreError("STORE_CONTEXT_FIXITY_MISMATCH", "stored policy digest does not match stored implementation manifest policy component")
    envelope = read_json(bundle_dir / "capture-envelope.json")
    hygiene = read_json(bundle_dir / "snapshot-hygiene.intoto.json")
    expected_descriptor = implementation["descriptor"]
    producer_impl = envelope.get("producer", {}).get("implementation") if isinstance(envelope.get("producer"), dict) else None
    predicate = hygiene.get("predicate") if isinstance(hygiene.get("predicate"), dict) else {}
    checker = predicate.get("checker", {}) if isinstance(predicate, dict) and isinstance(predicate.get("checker"), dict) else {}
    checker_impl = checker.get("implementation") if isinstance(checker, dict) else None
    if producer_impl != expected_descriptor or checker_impl != expected_descriptor:
        raise StoreError("STORE_CONTEXT_FIXITY_MISMATCH", "stored implementation manifest does not match bundle descriptors")
    raw_policy = envelope.get("raw_handling", {}).get("policy") if isinstance(envelope.get("raw_handling"), dict) else None
    if not isinstance(raw_policy, dict) or raw_policy.get("id") != policy.get("id") or raw_policy.get("digest") != policy.get("_canonical_digest"):
        raise StoreError("STORE_CONTEXT_FIXITY_MISMATCH", "stored policy does not match raw_handling.policy")
    validate_historical_enterprise_alpha1_state(envelope, hygiene)


def validate_historical_enterprise_alpha1_state(envelope: dict[str, Any], hygiene: dict[str, Any]) -> None:
    try:
        validate_source_capture_bundle.validate_capture_semantics(envelope, profile="enterprise-alpha1")
        validate_source_capture_bundle.validate_hygiene_semantics(hygiene, profile="enterprise-alpha1")
    except validate_source_capture_bundle.ValidationError as exc:
        raise StoreError("BUNDLE_VALIDATION_FAILED", str(exc)) from exc
    snapshot = envelope.get("snapshot")
    observation = envelope.get("observation")
    source = envelope.get("source")
    raw_handling = envelope.get("raw_handling")
    predicate = hygiene.get("predicate")
    if not all(isinstance(item, dict) for item in [snapshot, observation, source, raw_handling, predicate]):
        raise StoreError("BUNDLE_VALIDATION_FAILED", "enterprise-alpha1 bundle objects are missing")
    content_type = observation.get("content_type")
    if not isinstance(content_type, dict):
        raise StoreError("BUNDLE_VALIDATION_FAILED", "enterprise-alpha1 requires observation.content_type")
    profiles = predicate.get("profiles")
    if not isinstance(profiles, list):
        raise StoreError("BUNDLE_VALIDATION_FAILED", "enterprise-alpha1 requires hygiene profiles")
    snapshot_kind = snapshot.get("kind")
    disposition = raw_handling.get("disposition")
    detection_basis = content_type.get("detection_basis")
    detected_media_type = content_type.get("detected_media_type")
    archive_intent = source.get("kind") == "archive" or observation.get("capture_method") in {"provider_archive", "archive_file"}
    if snapshot_kind == "tree":
        if detection_basis != "container_parser":
            raise StoreError("BUNDLE_VALIDATION_FAILED", "tree snapshots require observation.content_type.detection_basis=container_parser")
        if detected_media_type not in validate_source_capture_bundle.ARCHIVE_MEDIA_TYPES:
            raise StoreError("BUNDLE_VALIDATION_FAILED", "tree snapshots require an archive detected media type")
    if snapshot_kind == "blob" and disposition == "admitted" and detection_basis == "container_parser":
        raise StoreError("BUNDLE_VALIDATION_FAILED", "admitted blob snapshots must not use observation.content_type.detection_basis=container_parser")
    if detection_basis == "container_parser" and "archive-safety/v1" not in profiles:
        raise StoreError("BUNDLE_VALIDATION_FAILED", "container_parser captures must carry archive-safety/v1 hygiene profile")
    if (archive_intent or snapshot_kind == "tree") and "archive-safety/v1" not in profiles:
        raise StoreError("BUNDLE_VALIDATION_FAILED", "archive/tree captures must carry archive-safety/v1 hygiene profile")


def bundle_artifact_descriptors(bundle_dir: Path) -> list[FileDescriptor]:
    descriptors: list[FileDescriptor] = []
    names = {path.name for path in bundle_dir.iterdir()} if bundle_dir.exists() else set()
    expected = set(REQUIRED_BUNDLE_ARTIFACTS)
    if names != expected:
        missing = sorted(expected - names)
        extra = sorted(names - expected)
        raise StoreError("BUNDLE_SHAPE_INVALID", f"bundle directory must contain exactly the v1 artifacts; missing={missing}; extra={extra}")
    for name in sorted(REQUIRED_BUNDLE_ARTIFACTS):
        path = bundle_dir / name
        desc = hash_existing_regular_file(path, "BUNDLE_INPUT_UNSAFE", name)
        descriptors.append(FileDescriptor(name=name, size=desc.size, digest=desc.digest, media_type=REQUIRED_BUNDLE_ARTIFACTS[name]))
    return descriptors


def bundle_identity_payload(descriptors: list[FileDescriptor]) -> dict[str, Any]:
    return {
        "schema": BUNDLE_ID_SCHEMA,
        "artifacts": [
            {
                "name": desc.name,
                "media_type": desc.media_type,
                "size": desc.size,
                "digest": desc.digest,
            }
            for desc in sorted(descriptors, key=lambda item: item.name)
        ],
    }


def bundle_digest(descriptors: list[FileDescriptor]) -> str:
    return sha256_bytes(canonical_json_bytes(bundle_identity_payload(descriptors)))


def validate_capture_bundle(bundle_dir: Path, implementation_manifest: Path, policy_file: Path) -> dict[str, Any]:
    try:
        return validate_source_capture_bundle.validate_bundle(
            bundle_dir,
            profile="enterprise-alpha1",
            policy_file=policy_file,
            implementation_manifest=implementation_manifest,
        )
    except validate_source_capture_bundle.ValidationError as exc:
        raise StoreError("BUNDLE_VALIDATION_FAILED", str(exc)) from exc


def validate_capture_bundle_base(bundle_dir: Path) -> dict[str, Any]:
    try:
        return validate_source_capture_bundle.validate_bundle(bundle_dir, profile="base")
    except validate_source_capture_bundle.ValidationError as exc:
        raise StoreError("BUNDLE_VALIDATION_FAILED", str(exc)) from exc


def stage_inputs(
    stage: Path,
    bundle_dir: Path,
    raw_blob: Path | None,
    implementation_manifest: Path,
    policy_file: Path,
) -> tuple[Path, Path | None, Path, Path, list[FileDescriptor], FileDescriptor | None, FileDescriptor, FileDescriptor]:
    bundle_stage = stage / "bundle"
    context_stage = stage / "validation-context"
    bundle_stage.mkdir()
    context_stage.mkdir()
    bundle_artifact_descriptors(bundle_dir)
    staged_bundle_desc: list[FileDescriptor] = []
    for name in sorted(REQUIRED_BUNDLE_ARTIFACTS):
        staged_bundle_desc.append(
            copy_regular_file(
                bundle_dir / name,
                bundle_stage / name,
                name=name,
                media_type=REQUIRED_BUNDLE_ARTIFACTS[name],
            )
        )
    impl_desc = copy_regular_file(
        implementation_manifest,
        context_stage / IMPLEMENTATION_CONTEXT_NAME,
        name=IMPLEMENTATION_CONTEXT_NAME,
        media_type=validate_source_capture_bundle.IMPLEMENTATION_MEDIA_TYPE,
    )
    policy_desc = copy_regular_file(policy_file, context_stage / POLICY_CONTEXT_NAME, name=POLICY_CONTEXT_NAME, media_type="application/json")
    raw_stage: Path | None = None
    raw_desc: FileDescriptor | None = None
    if raw_blob is not None:
        raw_stage = stage / "raw-blob"
        raw_desc = copy_regular_file(raw_blob, raw_stage, name="raw-blob")
    return bundle_stage, raw_stage, context_stage / IMPLEMENTATION_CONTEXT_NAME, context_stage / POLICY_CONTEXT_NAME, staged_bundle_desc, raw_desc, impl_desc, policy_desc


def descriptor_without_media(desc: FileDescriptor) -> dict[str, Any]:
    return {"name": desc.name, "size": desc.size, "digest": desc.digest}


def build_receipt(
    store: StoreInfo,
    capture_id: str,
    bundle_desc: list[FileDescriptor],
    raw_blob_record: dict[str, Any],
    implementation_desc: FileDescriptor,
    policy_desc: FileDescriptor,
    capture_dir: str,
) -> dict[str, Any]:
    bundle_id = bundle_digest(bundle_desc)
    return {
        "schema": RECEIPT_SCHEMA,
        "capture_id": capture_id,
        "stored_at": now_z(),
        "store": {
            "instance_id": store.meta["store_instance_id"],
            "layout": STORE_LAYOUT,
        },
        "bundle": {
            "digest_profile": DIGEST_PROFILE,
            "digest": bundle_id,
            "artifacts": [descriptor_without_media(desc) for desc in sorted(bundle_desc, key=lambda item: item.name)],
        },
        "raw_blob": raw_blob_record,
        "validation_context": {
            "implementation": {
                "size": implementation_desc.size,
                "digest": implementation_desc.digest,
                "store_path": f"captures/{capture_dir}/validation-context/{IMPLEMENTATION_CONTEXT_NAME}",
            },
            "policy": {
                "size": policy_desc.size,
                "digest": policy_desc.digest,
                "store_path": f"captures/{capture_dir}/validation-context/{POLICY_CONTEXT_NAME}",
            },
        },
        "storage_state": "retained",
    }


def commit_cas_blob(store: StoreInfo, staged_raw: Path, expected_digest: str, expected_size: int) -> tuple[dict[str, Any], bool]:
    desc = hash_existing_regular_file(staged_raw, "RAW_BLOB_STAGING_UNSAFE", "staged raw blob")
    if desc.digest != expected_digest or desc.size != expected_size:
        raise StoreError("RAW_BLOB_DIGEST_MISMATCH", "raw blob size/digest does not match capture envelope")
    target, rel = cas_path(store.root, expected_digest)
    ensure_cas_prefix_dir(store, expected_digest)
    if target.exists() or target.is_symlink():
        record = verify_existing_cas_blob(target, expected_digest, expected_size)
        try:
            staged_raw.unlink()
        except OSError:
            pass
        return record, False
    try:
        os.link(staged_raw, target)
        staged_raw.unlink()
    except FileExistsError:
        record = verify_existing_cas_blob(target, expected_digest, expected_size)
        try:
            staged_raw.unlink()
        except OSError:
            pass
        return record, False
    except OSError:
        if target.exists() or target.is_symlink():
            record = verify_existing_cas_blob(target, expected_digest, expected_size)
            try:
                staged_raw.unlink()
            except OSError:
                pass
            return record, False
        try:
            # Fallback keeps no-overwrite semantics even on filesystems without hardlink support.
            copy_regular_file(staged_raw, target, name=target.name)
            staged_raw.unlink()
        except FileExistsError:
            record = verify_existing_cas_blob(target, expected_digest, expected_size)
            try:
                staged_raw.unlink()
            except OSError:
                pass
            return record, False
        except OSError as exc:
            raise StoreError("STORE_WRITE_FAILED", f"could not write CAS blob: {exc}") from exc
    existing = hash_existing_regular_file(target, "STORE_BLOB_FIXITY_MISMATCH", "stored CAS blob")
    if existing.digest != expected_digest or existing.size != expected_size:
        raise StoreError("STORE_BLOB_FIXITY_MISMATCH", "stored CAS blob does not match expected digest")
    return {"retention_state": "retained", "media_type": None, "size": expected_size, "digest": expected_digest, "store_path": rel}, True


def raw_blob_expected_record(envelope: dict[str, Any]) -> tuple[str, int, str]:
    observation = envelope.get("observation")
    if not isinstance(observation, dict) or not isinstance(observation.get("blob"), dict):
        raise StoreError("BUNDLE_SHAPE_INVALID", "capture envelope observation.blob is missing")
    blob = observation["blob"]
    digest = blob.get("digest")
    size = blob.get("size")
    media_type = blob.get("media_type")
    if not isinstance(digest, str) or not SHA256_RE.match(digest):
        raise StoreError("BUNDLE_SHAPE_INVALID", "observation.blob.digest is invalid")
    if type(size) is not int or size < 0:
        raise StoreError("BUNDLE_SHAPE_INVALID", "observation.blob.size is invalid")
    if not isinstance(media_type, str) or not media_type:
        raise StoreError("BUNDLE_SHAPE_INVALID", "observation.blob.media_type is invalid")
    return digest, size, media_type


def receipt_raw_blob_for_no_raw(expected_digest: str, expected_size: int) -> dict[str, Any]:
    return {
        "retention_state": "not_retained",
        "reason": "not_provided",
        "expected_digest": expected_digest,
        "expected_size": expected_size,
    }


def compare_idempotent(existing: dict[str, Any], new: dict[str, Any]) -> bool:
    return (
        existing.get("capture_id") == new.get("capture_id")
        and existing.get("bundle", {}).get("digest") == new.get("bundle", {}).get("digest")
        and existing.get("raw_blob") == new.get("raw_blob")
    )


def load_receipt(path: Path) -> dict[str, Any]:
    require_regular_file(path, "STORE_RECEIPT_MISSING", "capture-storage-receipt.json")
    receipt = read_json(path)
    validate_receipt_shape(receipt)
    return receipt


def validate_receipt_shape(receipt: dict[str, Any]) -> None:
    validate_source_capture_bundle.exact_keys(
        receipt,
        {"schema", "capture_id", "stored_at", "store", "bundle", "raw_blob", "validation_context", "storage_state"},
        {"schema", "capture_id", "stored_at", "store", "bundle", "raw_blob", "validation_context", "storage_state"},
        "capture-storage-receipt",
    )
    if receipt.get("schema") != RECEIPT_SCHEMA:
        raise StoreError("STORE_RECEIPT_INVALID", "receipt schema mismatch")
    if not isinstance(receipt.get("capture_id"), str) or not CAPTURE_ID_RE.match(receipt["capture_id"]):
        raise StoreError("STORE_RECEIPT_INVALID", "receipt capture_id is invalid")
    validate_source_capture_bundle.parse_datetime(receipt.get("stored_at"), "receipt.stored_at")
    if receipt.get("storage_state") != "retained":
        raise StoreError("STORE_RECEIPT_INVALID", "receipt storage_state must be retained")
    store = receipt.get("store")
    validate_source_capture_bundle.exact_keys(store, {"instance_id", "layout"}, {"instance_id", "layout"}, "receipt.store")
    if store.get("layout") != STORE_LAYOUT:
        raise StoreError("STORE_RECEIPT_INVALID", "receipt store layout is invalid")
    bundle = receipt.get("bundle")
    validate_source_capture_bundle.exact_keys(bundle, {"digest_profile", "digest", "artifacts"}, {"digest_profile", "digest", "artifacts"}, "receipt.bundle")
    if bundle.get("digest_profile") != DIGEST_PROFILE or not SHA256_RE.match(str(bundle.get("digest"))):
        raise StoreError("STORE_RECEIPT_INVALID", "receipt bundle digest is invalid")
    artifacts = bundle.get("artifacts")
    if not isinstance(artifacts, list) or [item.get("name") for item in artifacts if isinstance(item, dict)] != sorted(REQUIRED_BUNDLE_ARTIFACTS):
        raise StoreError("STORE_RECEIPT_INVALID", "receipt bundle artifacts must list the fixed v1 names")
    for item in artifacts:
        validate_source_capture_bundle.exact_keys(item, {"name", "size", "digest"}, {"name", "size", "digest"}, "receipt.bundle.artifact")
        if item.get("name") not in REQUIRED_BUNDLE_ARTIFACTS:
            raise StoreError("STORE_RECEIPT_INVALID", "receipt bundle artifact name is invalid")
        validate_source_capture_bundle.require_nonnegative_int(item.get("size"), "receipt.bundle.artifact.size")
        validate_source_capture_bundle.require_digest(item.get("digest"), "receipt.bundle.artifact.digest")
    raw_blob = receipt.get("raw_blob")
    if not isinstance(raw_blob, dict):
        raise StoreError("STORE_RECEIPT_INVALID", "receipt raw_blob must be an object")
    if raw_blob.get("retention_state") == "retained":
        validate_source_capture_bundle.exact_keys(raw_blob, {"retention_state", "media_type", "size", "digest", "store_path"}, {"retention_state", "media_type", "size", "digest", "store_path"}, "receipt.raw_blob")
        validate_source_capture_bundle.require_nonnegative_int(raw_blob.get("size"), "receipt.raw_blob.size")
        validate_source_capture_bundle.require_digest(raw_blob.get("digest"), "receipt.raw_blob.digest")
        validate_source_capture_bundle.require_string(raw_blob.get("media_type"), "receipt.raw_blob.media_type")
        safe_relative_posix(validate_source_capture_bundle.require_string(raw_blob.get("store_path"), "receipt.raw_blob.store_path"), "receipt.raw_blob.store_path")
    elif raw_blob.get("retention_state") == "not_retained":
        validate_source_capture_bundle.exact_keys(raw_blob, {"retention_state", "reason", "expected_digest", "expected_size"}, {"retention_state", "reason", "expected_digest", "expected_size"}, "receipt.raw_blob")
        if raw_blob.get("reason") != "not_provided":
            raise StoreError("STORE_RECEIPT_INVALID", "receipt raw_blob reason is invalid")
        validate_source_capture_bundle.require_digest(raw_blob.get("expected_digest"), "receipt.raw_blob.expected_digest")
        validate_source_capture_bundle.require_nonnegative_int(raw_blob.get("expected_size"), "receipt.raw_blob.expected_size")
    else:
        raise StoreError("STORE_RECEIPT_INVALID", "receipt raw_blob retention_state is invalid")
    context = receipt.get("validation_context")
    validate_source_capture_bundle.exact_keys(context, {"implementation", "policy"}, {"implementation", "policy"}, "receipt.validation_context")
    for key in ["implementation", "policy"]:
        desc = context.get(key)
        validate_source_capture_bundle.exact_keys(desc, {"size", "digest", "store_path"}, {"size", "digest", "store_path"}, f"receipt.validation_context.{key}")
        validate_source_capture_bundle.require_nonnegative_int(desc.get("size"), f"receipt.validation_context.{key}.size")
        validate_source_capture_bundle.require_digest(desc.get("digest"), f"receipt.validation_context.{key}.digest")
        safe_relative_posix(validate_source_capture_bundle.require_string(desc.get("store_path"), f"receipt.validation_context.{key}.store_path"), f"receipt.validation_context.{key}.store_path")


def verify_receipt_against_capture(
    store: StoreInfo,
    capture_dir: Path,
    receipt: dict[str, Any],
    *,
    implementation_manifest: Path | None = None,
    policy_file: Path | None = None,
    expected_dir_name: str | None = None,
    enterprise_revalidate: bool = False,
) -> None:
    capture_id = receipt["capture_id"]
    if (expected_dir_name or capture_dir.name) != capture_dir_name(capture_id):
        raise StoreError("STORE_RECEIPT_INVALID", "receipt capture_id does not match capture directory")
    if receipt["store"]["instance_id"] != store.meta["store_instance_id"]:
        raise StoreError("STORE_RECEIPT_INVALID", "receipt store instance does not match store.json")
    bundle_dir = capture_dir / "bundle"
    context_dir = capture_dir / "validation-context"
    require_existing_dir(bundle_dir, "STORE_CAPTURE_INVALID", "stored bundle directory")
    require_existing_dir(context_dir, "STORE_CAPTURE_INVALID", "stored validation-context directory")
    bundle_desc = bundle_artifact_descriptors(bundle_dir)
    if bundle_digest(bundle_desc) != receipt["bundle"]["digest"]:
        raise StoreError("STORE_BUNDLE_FIXITY_MISMATCH", "stored bundle digest does not match receipt")
    receipt_artifacts = {item["name"]: item for item in receipt["bundle"]["artifacts"]}
    for desc in bundle_desc:
        recorded = receipt_artifacts[desc.name]
        if recorded["size"] != desc.size or recorded["digest"] != desc.digest:
            raise StoreError("STORE_BUNDLE_FIXITY_MISMATCH", f"stored bundle artifact mismatch: {desc.name}")
    impl_path = context_dir / IMPLEMENTATION_CONTEXT_NAME
    policy_path = context_dir / POLICY_CONTEXT_NAME
    impl_desc = hash_existing_regular_file(impl_path, "STORE_CONTEXT_FIXITY_MISMATCH", "stored implementation manifest")
    policy_desc = hash_existing_regular_file(policy_path, "STORE_CONTEXT_FIXITY_MISMATCH", "stored policy")
    context = receipt["validation_context"]
    expected_capture_dir = expected_dir_name or capture_dir.name
    expected_impl_store_path = expected_implementation_store_path(expected_capture_dir)
    expected_policy_path = expected_policy_store_path(expected_capture_dir)
    if context["implementation"]["store_path"] != expected_impl_store_path:
        raise StoreError("STORE_RECEIPT_INVALID", "receipt implementation store_path is not canonical")
    if context["policy"]["store_path"] != expected_policy_path:
        raise StoreError("STORE_RECEIPT_INVALID", "receipt policy store_path is not canonical")
    if impl_desc.digest != context["implementation"]["digest"] or impl_desc.size != context["implementation"]["size"]:
        raise StoreError("STORE_CONTEXT_FIXITY_MISMATCH", "stored implementation manifest does not match receipt")
    if policy_desc.digest != context["policy"]["digest"] or policy_desc.size != context["policy"]["size"]:
        raise StoreError("STORE_CONTEXT_FIXITY_MISMATCH", "stored policy does not match receipt")
    validate_bundle_against_stored_context(bundle_dir, impl_path, policy_path)
    envelope = read_json(bundle_dir / "capture-envelope.json")
    hygiene = read_json(bundle_dir / "snapshot-hygiene.intoto.json")
    if enterprise_revalidate:
        if implementation_manifest is not None and policy_file is not None:
            validate_capture_bundle(bundle_dir, implementation_manifest, policy_file)
    expected_digest, expected_size, expected_media_type = raw_blob_expected_record(envelope)
    raw_blob = receipt["raw_blob"]
    if raw_blob["retention_state"] == "retained":
        if raw_blob["store_path"] != expected_raw_blob_store_path(expected_digest):
            raise StoreError("STORE_RECEIPT_INVALID", "receipt raw_blob store_path is not canonical")
        if raw_blob["digest"] != expected_digest or raw_blob["size"] != expected_size or raw_blob["media_type"] != expected_media_type:
            raise StoreError("STORE_RAW_BLOB_MISMATCH", "receipt raw_blob does not match envelope")
        blob_path = store.root / raw_blob["store_path"]
        if not blob_path.exists() and not blob_path.is_symlink():
            raise StoreError("STORE_RAW_BLOB_MISSING", "retained raw blob is missing from CAS")
        blob_desc = hash_existing_regular_file(blob_path, "STORE_RAW_BLOB_MISMATCH", "stored raw blob")
        if blob_desc.digest != raw_blob["digest"] or blob_desc.size != raw_blob["size"]:
            raise StoreError("STORE_RAW_BLOB_MISMATCH", "stored raw blob does not match receipt")
    else:
        if raw_blob["expected_digest"] != expected_digest or raw_blob["expected_size"] != expected_size:
            raise StoreError("STORE_RAW_BLOB_MISMATCH", "not-retained raw blob expectation does not match envelope")


def verify_stored_capture(store: StoreInfo, capture_dir: Path) -> VerifiedStoredCapture:
    require_existing_dir(capture_dir, "STORE_CAPTURE_MISSING", "capture directory")
    receipt = load_receipt(capture_dir / "capture-storage-receipt.json")
    verify_receipt_against_capture(
        store,
        capture_dir,
        receipt,
        enterprise_revalidate=False,
    )
    raw_blob = receipt["raw_blob"]
    if raw_blob["retention_state"] == "retained":
        raw_digest = raw_blob["digest"]
        raw_store_path = raw_blob["store_path"]
    else:
        raw_digest = raw_blob["expected_digest"]
        raw_store_path = None
    return VerifiedStoredCapture(
        capture_id=receipt["capture_id"],
        capture_dir=f"captures/{capture_dir.name}",
        bundle_digest=receipt["bundle"]["digest"],
        raw_blob_retention_state=raw_blob["retention_state"],
        raw_blob_digest=raw_digest,
        raw_blob_store_path=raw_store_path,
    )


def verify_capture(args: argparse.Namespace) -> dict[str, Any]:
    store = load_store(Path(args.store_root))
    capture_id = args.capture_id
    capture_dir = store.root / "captures" / capture_dir_name(capture_id)
    verified = verify_stored_capture(store, capture_dir)
    return {
        "status": "pass",
        "capture_id": verified.capture_id,
        "bundle_digest": verified.bundle_digest,
        "raw_blob_retention_state": verified.raw_blob_retention_state,
    }


def existing_capture_result(
    store: StoreInfo,
    capture_dir: Path,
    new_receipt: dict[str, Any],
    *,
    implementation_manifest: Path | None = None,
    policy_file: Path | None = None,
) -> dict[str, Any] | None:
    if not capture_dir.exists() and not capture_dir.is_symlink():
        return None
    require_existing_dir(capture_dir, "CAPTURE_ID_CONFLICT", "existing capture directory")
    receipt = load_receipt(capture_dir / "capture-storage-receipt.json")
    verify_receipt_against_capture(
        store,
        capture_dir,
        receipt,
        implementation_manifest=implementation_manifest,
        policy_file=policy_file,
        enterprise_revalidate=True,
    )
    if compare_idempotent(receipt, new_receipt):
        return {
            "status": "pass",
            "result": "already_retained",
            "capture_id": receipt["capture_id"],
            "bundle_digest": receipt["bundle"]["digest"],
            "receipt": f"captures/{capture_dir.name}/capture-storage-receipt.json",
        }
    raise StoreError("CAPTURE_ID_CONFLICT", "capture_id already exists with different bundle or raw retention")


def put_capture(args: argparse.Namespace) -> dict[str, Any]:
    store = load_store(Path(args.store_root))
    bundle_dir = Path(args.bundle_dir)
    implementation_manifest = Path(args.implementation_manifest)
    policy_file = Path(args.policy_file)
    raw_blob = Path(args.raw_blob) if args.raw_blob else None
    require_existing_dir(bundle_dir, "BUNDLE_INPUT_UNSAFE", "bundle directory")
    bundle_artifact_descriptors(bundle_dir)
    require_regular_file(implementation_manifest, "STORE_INPUT_UNSAFE", "implementation manifest")
    require_regular_file(policy_file, "STORE_INPUT_UNSAFE", "policy file")
    validate_capture_bundle(bundle_dir, implementation_manifest, policy_file)

    stage = store.root / ".staging" / f"put-{uuid.uuid4().hex}"
    stage.mkdir(mode=0o700)
    try:
        (
            staged_bundle,
            staged_raw,
            staged_impl,
            staged_policy,
            bundle_desc,
            raw_desc,
            implementation_desc,
            policy_desc,
        ) = stage_inputs(stage, bundle_dir, raw_blob, implementation_manifest, policy_file)
        validate_bundle_against_stored_context(staged_bundle, staged_impl, staged_policy)
        envelope = read_json(staged_bundle / "capture-envelope.json")
        capture_id = envelope.get("capture_id")
        if not isinstance(capture_id, str):
            raise StoreError("BUNDLE_SHAPE_INVALID", "capture envelope capture_id is missing")
        capture_dir = capture_dir_name(capture_id)
        expected_digest, expected_size, expected_media_type = raw_blob_expected_record(envelope)
        if staged_raw is not None:
            if raw_desc is None or raw_desc.digest != expected_digest or raw_desc.size != expected_size:
                raise StoreError("RAW_BLOB_DIGEST_MISMATCH", "raw blob size/digest does not match capture envelope")
            raw_record_preview, _created = {
                "retention_state": "retained",
                "media_type": expected_media_type,
                "size": expected_size,
                "digest": expected_digest,
                "store_path": cas_path(store.root, expected_digest)[1],
            }, False
        else:
            raw_record_preview = receipt_raw_blob_for_no_raw(expected_digest, expected_size)
        receipt_preview = build_receipt(
            store,
            capture_id,
            bundle_desc,
            raw_record_preview,
            implementation_desc,
            policy_desc,
            capture_dir,
        )
        existing = existing_capture_result(
            store,
            store.root / "captures" / capture_dir,
            receipt_preview,
            implementation_manifest=implementation_manifest,
            policy_file=policy_file,
        )
        if existing is not None:
            return existing
        raw_record = raw_record_preview
        cas_created = False
        if staged_raw is not None:
            raw_record, cas_created = commit_cas_blob(store, staged_raw, expected_digest, expected_size)
            raw_record["media_type"] = expected_media_type
        receipt = build_receipt(store, capture_id, bundle_desc, raw_record, implementation_desc, policy_desc, capture_dir)
        capture_stage = stage / "capture"
        capture_stage.mkdir()
        shutil.move(str(staged_bundle), str(capture_stage / "bundle"))
        shutil.move(str(stage / "validation-context"), str(capture_stage / "validation-context"))
        write_json_exclusive(capture_stage / "capture-storage-receipt.json", receipt)
        verify_receipt_against_capture(
            store,
            capture_stage,
            receipt,
            expected_dir_name=capture_dir,
            enterprise_revalidate=False,
        )
        final_capture = store.root / "captures" / capture_dir
        if final_capture.exists() or final_capture.is_symlink():
            existing = existing_capture_result(
                store,
                final_capture,
                receipt,
                implementation_manifest=implementation_manifest,
                policy_file=policy_file,
            )
            if existing is not None:
                return existing
        try:
            os.rename(capture_stage, final_capture)
        except OSError as exc:
            if final_capture.exists() or final_capture.is_symlink():
                existing = existing_capture_result(
                    store,
                    final_capture,
                    receipt,
                    implementation_manifest=implementation_manifest,
                    policy_file=policy_file,
                )
                if existing is not None:
                    return existing
            raise StoreError("STORE_WRITE_FAILED", f"could not commit capture directory: {exc}") from exc
        stored_receipt = load_receipt(final_capture / "capture-storage-receipt.json")
        verify_receipt_against_capture(
            store,
            final_capture,
            stored_receipt,
            implementation_manifest=implementation_manifest,
            policy_file=policy_file,
            enterprise_revalidate=True,
        )
        return {
            "status": "pass",
            "result": "stored",
            "capture_id": capture_id,
            "bundle_digest": receipt["bundle"]["digest"],
            "raw_blob_retention_state": receipt["raw_blob"]["retention_state"],
            "raw_blob_cas_created": cas_created,
            "receipt": f"captures/{capture_dir}/capture-storage-receipt.json",
        }
    finally:
        if stage.exists():
            shutil.rmtree(stage, ignore_errors=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Store validated VAKS Source Capture bundles in a local filesystem CAS.")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="Initialize a source capture store.")
    init.add_argument("--store-root", required=True)
    put = sub.add_parser("put", help="Store a validated capture bundle.")
    put.add_argument("--store-root", required=True)
    put.add_argument("--bundle-dir", required=True)
    put.add_argument("--raw-blob")
    put.add_argument("--implementation-manifest", default=str(default_implementation_manifest_path()))
    put.add_argument("--policy-file", default=str(default_policy_path()))
    verify = sub.add_parser("verify-capture", help="Verify one stored capture.")
    verify.add_argument("--store-root", required=True)
    verify.add_argument("--capture-id", required=True)
    verify.add_argument("--implementation-manifest", default=str(default_implementation_manifest_path()))
    verify.add_argument("--policy-file", default=str(default_policy_path()))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "init":
            result = create_store(args)
        elif args.command == "put":
            result = put_capture(args)
        elif args.command == "verify-capture":
            result = verify_capture(args)
        else:
            raise StoreError("CLI_ERROR", "unsupported command")
    except StoreError as exc:
        print(json.dumps({"status": "fail", "code": exc.code, "message": exc.message}, allow_nan=False, sort_keys=True))
        return 1
    except validate_source_capture_bundle.ValidationError as exc:
        print(json.dumps({"status": "fail", "code": "VALIDATION_ERROR", "message": str(exc)}, allow_nan=False, sort_keys=True))
        return 1
    print(json.dumps(result, allow_nan=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
