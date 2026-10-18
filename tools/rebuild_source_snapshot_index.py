#!/usr/bin/env python
"""Rebuild the deterministic Source Snapshot index for a verified Store."""

from __future__ import annotations

import argparse
import json
import os
import uuid
from pathlib import Path
from typing import Any, Callable

import store_source_capture
import validate_source_capture_bundle
import verify_source_capture_store


INDEX_SCHEMA = "urn:vaks:index:source-snapshot:v1"
INDEX_PROFILE = "source-snapshot-index/v1"
INDEX_REL = "indexes/source-snapshot-index.jsonl"
INDEX_MEDIA_TYPE = "application/vnd.vaks.source-snapshot-index.v1+jsonl"


class IndexError(RuntimeError):
    def __init__(self, code: str, message: str, *, status: str = "fail") -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status


def canonical_json_bytes(obj: dict[str, Any]) -> bytes:
    return validate_source_capture_bundle.canonical_json_bytes(obj)


def utf8_sort_key(value: str) -> bytes:
    return value.encode("utf-8")


def index_path(store_root: Path) -> Path:
    return store_root / INDEX_REL


TRUTH_INVENTORY_ROOTS = ("store.json", "captures", "blobs", ".staging")
IGNORED_TRUTH_ROOT_ENTRIES = {"indexes"}


def fsync_dir(path: Path) -> None:
    try:
        fd = os.open(str(path), os.O_RDONLY)
    except OSError:
        return
    try:
        try:
            os.fsync(fd)
        except OSError:
            pass
    finally:
        os.close(fd)


def jsonl_bytes(records: list[dict[str, Any]]) -> bytes:
    return b"".join(canonical_json_bytes(record) for record in records)


def require_string(obj: dict[str, Any], key: str, context: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        raise IndexError("INDEX_INPUT_INVALID", f"{context}.{key} must be a non-empty string")
    return value


def raw_blob_entry(verified: store_source_capture.VerifiedStoredCapture) -> dict[str, Any]:
    raw: dict[str, Any] = {
        "retention_state": verified.raw_blob_retention_state,
        "digest": verified.raw_blob_digest,
    }
    if verified.raw_blob_store_path is not None:
        raw["store_path"] = verified.raw_blob_store_path
    return raw


def index_entry(store: store_source_capture.StoreInfo, capture_dir: Path) -> dict[str, Any]:
    verified = store_source_capture.verify_stored_capture(store, capture_dir)
    envelope = store_source_capture.read_json(capture_dir / "bundle" / "capture-envelope.json")
    source = envelope.get("source")
    snapshot = envelope.get("snapshot")
    observation = envelope.get("observation")
    change = envelope.get("change")
    if not isinstance(source, dict) or not isinstance(snapshot, dict) or not isinstance(observation, dict):
        raise IndexError("INDEX_INPUT_INVALID", "capture envelope is missing source, snapshot, or observation objects")
    if not isinstance(change, dict):
        change = {}
    entry: dict[str, Any] = {
        "schema": INDEX_SCHEMA,
        "record_type": "entry",
        "source_id": require_string(source, "source_id", "source"),
        "source_kind": require_string(source, "kind", "source"),
        "snapshot_id": require_string(snapshot, "snapshot_id", "snapshot"),
        "snapshot_kind": require_string(snapshot, "kind", "snapshot"),
        "capture_id": verified.capture_id,
        "capture_store_path": verified.capture_dir,
        "observed_at": require_string(envelope, "observed_at", "capture-envelope"),
        "capture_method": require_string(observation, "capture_method", "observation"),
        "change_state": require_string(change, "state", "change"),
        "bundle_digest": verified.bundle_digest,
        "raw_blob": raw_blob_entry(verified),
    }
    resolution = envelope.get("resolution")
    revision = resolution.get("revision") if isinstance(resolution, dict) else None
    if isinstance(revision, dict):
        entry["revision"] = {
            "kind": require_string(revision, "kind", "resolution.revision"),
            "value": require_string(revision, "value", "resolution.revision"),
        }
    return entry


def build_index_records(store: store_source_capture.StoreInfo) -> list[dict[str, Any]]:
    captures_root = store.root / "captures"
    try:
        capture_dirs = [item for item in captures_root.iterdir() if item.is_dir()]
    except OSError as exc:
        raise IndexError("INDEX_STORE_IO_ERROR", f"could not read captures directory: {exc}") from exc
    entries = [index_entry(store, capture_dir) for capture_dir in capture_dirs]
    entries.sort(
        key=lambda item: (
            utf8_sort_key(item["source_id"]),
            utf8_sort_key(item["snapshot_id"]),
            utf8_sort_key(item["capture_id"]),
        )
    )
    header = {
        "schema": INDEX_SCHEMA,
        "record_type": "header",
        "profile": INDEX_PROFILE,
        "store_layout": store_source_capture.STORE_LAYOUT,
        "layout_version": store_source_capture.STORE_LAYOUT_VERSION,
        "entry_count": len(entries),
    }
    return [header, *entries]


def validate_index_record(record: dict[str, Any], line_no: int) -> None:
    try:
        record_type = validate_source_capture_bundle.require_string(record.get("record_type"), f"index line {line_no}.record_type")
    except validate_source_capture_bundle.ValidationError as exc:
        raise IndexError("INDEX_INVALID", str(exc)) from exc
    if record.get("schema") != INDEX_SCHEMA:
        raise IndexError("INDEX_INVALID", f"index line {line_no} schema mismatch")
    if record_type == "header":
        validate_source_capture_bundle.exact_keys(
            record,
            {"schema", "record_type", "profile", "store_layout", "layout_version", "entry_count"},
            {"schema", "record_type", "profile", "store_layout", "layout_version", "entry_count"},
            f"index line {line_no}",
        )
        if record.get("profile") != INDEX_PROFILE:
            raise IndexError("INDEX_INVALID", "index header profile mismatch")
        validate_source_capture_bundle.require_nonnegative_int(record.get("entry_count"), "index header entry_count")
        if record.get("store_layout") != store_source_capture.STORE_LAYOUT or record.get("layout_version") != store_source_capture.STORE_LAYOUT_VERSION:
            raise IndexError("INDEX_INVALID", "index header store layout mismatch")
        return
    if record_type != "entry":
        raise IndexError("INDEX_INVALID", f"index line {line_no} record_type is unsupported")
    validate_source_capture_bundle.exact_keys(
        record,
        {
            "schema",
            "record_type",
            "source_id",
            "source_kind",
            "snapshot_id",
            "snapshot_kind",
            "capture_id",
            "capture_store_path",
            "observed_at",
            "capture_method",
            "change_state",
            "bundle_digest",
            "raw_blob",
        },
        {
            "schema",
            "record_type",
            "source_id",
            "source_kind",
            "snapshot_id",
            "snapshot_kind",
            "capture_id",
            "capture_store_path",
            "observed_at",
            "capture_method",
            "change_state",
            "bundle_digest",
            "raw_blob",
            "revision",
        },
        f"index line {line_no}",
    )
    for key in ["source_id", "source_kind", "snapshot_id", "snapshot_kind", "capture_id", "capture_store_path", "observed_at", "capture_method", "change_state"]:
        validate_source_capture_bundle.require_string(record.get(key), f"index line {line_no}.{key}")
    validate_source_capture_bundle.require_digest(record.get("bundle_digest"), f"index line {line_no}.bundle_digest")
    raw = record.get("raw_blob")
    validate_source_capture_bundle.exact_keys(raw, {"retention_state", "digest"}, {"retention_state", "digest", "store_path"}, f"index line {line_no}.raw_blob")
    if raw.get("retention_state") not in {"retained", "not_retained"}:
        raise IndexError("INDEX_INVALID", f"index line {line_no}.raw_blob.retention_state is invalid")
    validate_source_capture_bundle.require_digest(raw.get("digest"), f"index line {line_no}.raw_blob.digest")
    if raw.get("retention_state") == "retained":
        validate_source_capture_bundle.require_string(raw.get("store_path"), f"index line {line_no}.raw_blob.store_path")
    elif "store_path" in raw:
        raise IndexError("INDEX_INVALID", f"index line {line_no}.raw_blob.store_path is only allowed for retained raw blobs")
    if "revision" in record:
        revision = record.get("revision")
        validate_source_capture_bundle.exact_keys(revision, {"kind", "value"}, {"kind", "value"}, f"index line {line_no}.revision")
        validate_source_capture_bundle.require_string(revision.get("kind"), f"index line {line_no}.revision.kind")
        validate_source_capture_bundle.require_string(revision.get("value"), f"index line {line_no}.revision.value")


def validate_index_bytes(data: bytes) -> None:
    lines = data.splitlines()
    if data and not data.endswith(b"\n"):
        raise IndexError("INDEX_INVALID", "index JSONL must end with LF")
    if not lines:
        raise IndexError("INDEX_INVALID", "index JSONL is empty")
    records: list[dict[str, Any]] = []
    for line_no, line in enumerate(lines, start=1):
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError as exc:
            raise IndexError("INDEX_INVALID", f"index line {line_no} is not valid JSON: {exc}") from exc
        if not isinstance(parsed, dict):
            raise IndexError("INDEX_INVALID", f"index line {line_no} must be a JSON object")
        validate_index_record(parsed, line_no)
        if canonical_json_bytes(parsed).rstrip(b"\n") != line:
            raise IndexError("INDEX_INVALID", f"index line {line_no} is not canonical JSON")
        records.append(parsed)
    header = records[0]
    if header.get("record_type") != "header":
        raise IndexError("INDEX_INVALID", "index first line must be header")
    entries = records[1:]
    if header.get("entry_count") != len(entries):
        raise IndexError("INDEX_INVALID", "index header entry_count does not match entries")
    sort_keys = [(entry["source_id"].encode("utf-8"), entry["snapshot_id"].encode("utf-8"), entry["capture_id"].encode("utf-8")) for entry in entries]
    if sort_keys != sorted(sort_keys):
        raise IndexError("INDEX_INVALID", "index entries are not sorted by source_id, snapshot_id, capture_id UTF-8 bytes")


def ensure_indexes_dir(store: store_source_capture.StoreInfo, *, create: bool) -> Path:
    indexes = store.root / "indexes"
    store_source_capture.ensure_no_reparse_components(indexes, "INDEX_PATH_UNSAFE", "indexes")
    kind = verify_source_capture_store.path_kind(indexes)
    if kind == "missing":
        if not create:
            raise IndexError("INDEX_MISSING", "indexes directory does not exist")
        try:
            os.mkdir(indexes, 0o700)
        except FileExistsError:
            pass
        except OSError as exc:
            raise IndexError("INDEX_WRITE_FAILED", f"could not create indexes directory: {exc}") from exc
        kind = verify_source_capture_store.path_kind(indexes)
    if kind in {"symlink", "reparse"}:
        raise IndexError("INDEX_PATH_UNSAFE", "indexes directory must not be a symlink or reparse point")
    if kind != "dir":
        raise IndexError("INDEX_PATH_UNSAFE", "indexes path must be a directory")
    return indexes


def collect_store_truth_inventory(root: Path) -> tuple[str, ...]:
    records: list[str] = []

    def visit(path: Path) -> None:
        kind = verify_source_capture_store.path_kind(path)
        records.append(f"{verify_source_capture_store.report_relative_path(root, path)}\t{verify_source_capture_store.stat_fingerprint(path, kind)}")
        if kind != "dir":
            return
        try:
            children = sorted(path.iterdir(), key=lambda item: item.name)
        except OSError:
            return
        for child in children:
            visit(child)

    seen_root_entries: set[str] = set()
    try:
        root_entries = sorted(root.iterdir(), key=lambda item: item.name)
    except OSError:
        root_entries = []
    for entry in root_entries:
        if entry.name in IGNORED_TRUTH_ROOT_ENTRIES:
            continue
        seen_root_entries.add(entry.name)
        visit(entry)
    for rel in TRUTH_INVENTORY_ROOTS:
        if rel not in seen_root_entries:
            visit(root / rel)
    return tuple(records)


def changed_during_rebuild_report() -> dict[str, Any]:
    return build_failure_report(
        "indeterminate",
        "STORE_CHANGED_DURING_INDEX_REBUILD",
        "store inventory changed during index rebuild; rerun after writes have stopped",
    )


def write_index_atomic(
    store: store_source_capture.StoreInfo,
    data: bytes,
    *,
    expected_truth_inventory: tuple[str, ...],
    before_replace_hook: Callable[[], None] | None = None,
) -> bool:
    indexes = ensure_indexes_dir(store, create=True)
    target = indexes / "source-snapshot-index.jsonl"
    target_kind = verify_source_capture_store.path_kind(target)
    if target_kind in {"symlink", "reparse", "dir", "other"}:
        raise IndexError("INDEX_PATH_UNSAFE", "index target must be a regular file or missing")
    tmp = indexes / f".source-snapshot-index.jsonl.{uuid.uuid4().hex}.tmp"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    flags |= getattr(os, "O_BINARY", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(str(tmp), flags, 0o600)
        try:
            with os.fdopen(fd, "wb") as fh:
                fh.write(data)
                fh.flush()
                os.fsync(fh.fileno())
        except Exception:
            try:
                tmp.unlink()
            except OSError:
                pass
            raise
        if before_replace_hook is not None:
            before_replace_hook()
        if collect_store_truth_inventory(store.root) != expected_truth_inventory:
            try:
                tmp.unlink()
            except OSError:
                pass
            return False
        os.replace(tmp, target)
        fsync_dir(indexes)
        return True
    except OSError as exc:
        try:
            tmp.unlink()
        except OSError:
            pass
        raise IndexError("INDEX_WRITE_FAILED", f"could not write source snapshot index: {exc}") from exc


def build_failure_report(status: str, code: str, message: str, *, findings: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {
        "status": status,
        "code": code,
        "message": message,
        "findings": findings or [],
    }


def store_verification_failed_report(report: dict[str, Any]) -> dict[str, Any]:
    status = report.get("summary", {}).get("status")
    if status == "indeterminate":
        return build_failure_report(
            "indeterminate",
            "STORE_CHANGED_DURING_INDEX_REBUILD",
            "store verification was indeterminate; index was not rebuilt",
            findings=report.get("findings", []),
        )
    return build_failure_report(
        "fail",
        "STORE_VERIFICATION_FAILED",
        "store verification failed; index was not rebuilt",
        findings=report.get("findings", []),
    )


def build_success_report(store: store_source_capture.StoreInfo, records: list[dict[str, Any]], action: str, data: bytes) -> dict[str, Any]:
    return {
        "status": "pass",
        "action": action,
        "index": {
            "media_type": INDEX_MEDIA_TYPE,
            "store_path": INDEX_REL,
            "size": len(data),
            "digest": store_source_capture.sha256_bytes(data),
            "entry_count": len(records) - 1,
        },
        "store": {
            "layout": store_source_capture.STORE_LAYOUT,
            "layout_version": store_source_capture.STORE_LAYOUT_VERSION,
            "instance_id": store.meta["store_instance_id"],
        },
    }


def rebuild_index(
    store_root: Path,
    *,
    check: bool = False,
    after_build_hook: Callable[[], None] | None = None,
    before_replace_hook: Callable[[], None] | None = None,
) -> dict[str, Any]:
    store_source_capture.ensure_no_reparse_components(store_root, "STORE_ROOT_UNSAFE", "store root")
    start_inventory = collect_store_truth_inventory(store_root)
    verification_report = verify_source_capture_store.verify_store_root(store_root)
    if verification_report["summary"]["status"] not in {"pass", "pass_with_warnings"}:
        return store_verification_failed_report(verification_report)
    store = store_source_capture.load_store(store_root)
    records = build_index_records(store)
    data = jsonl_bytes(records)
    validate_index_bytes(data)
    if after_build_hook is not None:
        after_build_hook()
    end_inventory = collect_store_truth_inventory(store.root)
    if start_inventory != end_inventory:
        return changed_during_rebuild_report()
    if check:
        indexes = ensure_indexes_dir(store, create=False)
        target = indexes / "source-snapshot-index.jsonl"
        if verify_source_capture_store.path_kind(target) != "file":
            return build_failure_report("fail", "INDEX_MISSING", "source snapshot index is missing")
        try:
            existing = target.read_bytes()
        except OSError as exc:
            raise IndexError("INDEX_READ_FAILED", f"could not read source snapshot index: {exc}") from exc
        if existing != data:
            return build_failure_report(
                "fail",
                "INDEX_CHECK_FAILED",
                "source snapshot index bytes differ from deterministic rebuild",
                findings=[
                    {
                        "severity": "error",
                        "code": "INDEX_CHECK_FAILED",
                        "message": "source snapshot index bytes differ from deterministic rebuild",
                        "details": {
                            "expected_digest": store_source_capture.sha256_bytes(data),
                            "actual_digest": store_source_capture.sha256_bytes(existing),
                        },
                    }
                ],
            )
        validate_index_bytes(existing)
        return build_success_report(store, records, "check_passed", data)
    if not write_index_atomic(
        store,
        data,
        expected_truth_inventory=start_inventory,
        before_replace_hook=before_replace_hook,
    ):
        return changed_during_rebuild_report()
    return build_success_report(store, records, "rebuilt", data)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rebuild or check the deterministic VAKS Source Snapshot index.")
    parser.add_argument("--store-root", required=True)
    parser.add_argument("--check", action="store_true", help="verify the existing index without writing")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.store_root)
    try:
        report = rebuild_index(root, check=args.check)
    except IndexError as exc:
        report = build_failure_report(exc.status, exc.code, verify_source_capture_store.sanitize_message(root, exc.message))
    except store_source_capture.StoreError as exc:
        report = build_failure_report("fail", exc.code, verify_source_capture_store.sanitize_message(root, exc.message))
    except validate_source_capture_bundle.ValidationError as exc:
        report = build_failure_report("fail", "INDEX_INVALID", str(exc))
    except (OSError, UnicodeError) as exc:
        report = build_failure_report("fail", "INDEX_IO_ERROR", verify_source_capture_store.sanitize_message(root, str(exc)))
    print(json.dumps(report, allow_nan=False, sort_keys=True))
    status = report.get("status")
    if status == "pass":
        return 0
    if status == "indeterminate":
        return 3
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
