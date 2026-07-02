#!/usr/bin/env python
"""Verify a VAKS Source Capture Store without repairing or rewriting it."""

from __future__ import annotations

import argparse
import json
import os
import stat
from pathlib import Path
from typing import Any, Callable

import store_source_capture
import validate_source_capture_bundle


REPORT_SCHEMA = "urn:vaks:schema:source-capture-store-verification-report:v1"
REPORT_PROFILE = "source-capture-store-verification/v1"
STORE_VERSION = "1"
CAPTURE_DIR_ENTRIES = {"bundle", "validation-context", "capture-storage-receipt.json"}
VALIDATION_CONTEXT_ENTRIES = {
    store_source_capture.IMPLEMENTATION_CONTEXT_NAME,
    store_source_capture.POLICY_CONTEXT_NAME,
}
STORE_ROOT_ENTRIES = {"store.json", "blobs", "captures", ".staging", "indexes"}
STORE_BLOBS_ENTRIES = {"sha256"}
HEX = set("0123456789abcdef")
PATH_SAFE_BYTES = set(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-")


def canonical_json_bytes(obj: dict[str, Any]) -> bytes:
    return validate_source_capture_bundle.canonical_json_bytes(obj)


def encode_path_component(component: str) -> str:
    encoded = component.encode("utf-8", errors="surrogateescape")
    parts: list[str] = []
    for byte in encoded:
        if byte in PATH_SAFE_BYTES:
            parts.append(chr(byte))
        else:
            parts.append(f"%{byte:02X}")
    return "".join(parts)


def report_relative_path(root: Path, path: Path) -> str:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return "outside-store/" + encode_path_component(str(path))
    if rel == Path("."):
        return "."
    return "/".join(encode_path_component(part) for part in rel.parts)


def sanitize_message(root: Path, message: str) -> str:
    sanitized = message
    candidates = {str(root)}
    try:
        candidates.add(str(root.resolve()))
    except OSError:
        pass
    for candidate in sorted(candidates, key=len, reverse=True):
        if candidate:
            sanitized = sanitized.replace(candidate, "<store-root>")
    return sanitized


def store_error_finding(store: store_source_capture.StoreInfo, severity: str, exc: store_source_capture.StoreError, path: Path | None = None) -> dict[str, Any]:
    return finding(
        severity,
        exc.code,
        sanitize_message(store.root, exc.message),
        path=report_relative_path(store.root, path) if path is not None else None,
    )


def exception_finding(store: store_source_capture.StoreInfo, severity: str, code: str, exc: BaseException, path: Path | None = None) -> dict[str, Any]:
    return finding(
        severity,
        code,
        sanitize_message(store.root, str(exc)),
        path=report_relative_path(store.root, path) if path is not None else None,
    )


def finding(severity: str, code: str, message: str, *, path: str | None = None, details: dict[str, Any] | None = None) -> dict[str, Any]:
    item: dict[str, Any] = {
        "severity": severity,
        "code": code,
        "message": message,
    }
    if path is not None:
        item["path"] = path
    if details:
        item["details"] = details
    return item


def path_kind(path: Path) -> str:
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        return "missing"
    if stat.S_ISLNK(st.st_mode):
        return "symlink"
    attrs = getattr(st, "st_file_attributes", 0)
    if attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):
        return "reparse"
    if stat.S_ISDIR(st.st_mode):
        return "dir"
    if stat.S_ISREG(st.st_mode):
        return "file"
    return "other"


def stat_fingerprint(path: Path, kind: str) -> str:
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        return "missing"
    attrs = getattr(st, "st_file_attributes", 0)
    identity = f"{getattr(st, 'st_dev', 0)}:{getattr(st, 'st_ino', 0)}"
    digest = ""
    if kind == "file":
        try:
            digest = ":" + store_source_capture.digest_file(path)
        except (OSError, UnicodeError) as exc:
            digest = f":digest-error:{type(exc).__name__}"
        except validate_source_capture_bundle.ValidationError as exc:
            digest = f":digest-error:{type(exc).__name__}"
    return f"{kind}:{identity}:{st.st_size}:{st.st_mtime_ns}:{attrs}{digest}"


def collect_inventory(root: Path) -> tuple[str, ...]:
    records: list[str] = []

    def visit(path: Path) -> None:
        kind = path_kind(path)
        records.append(f"{report_relative_path(root, path)}\t{stat_fingerprint(path, kind)}")
        if kind != "dir":
            return
        try:
            children = sorted(path.iterdir(), key=lambda item: item.name)
        except OSError:
            return
        for child in children:
            visit(child)

    visit(root)
    return tuple(records)


def store_layout_findings(store: store_source_capture.StoreInfo) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    try:
        root_entries = sorted(store.root.iterdir(), key=lambda item: item.name)
    except OSError as exc:
        return [finding("error", "STORE_IO_ERROR", sanitize_message(store.root, f"could not read store root: {exc}"))]
    for entry in root_entries:
        rel = report_relative_path(store.root, entry)
        if entry.name not in STORE_ROOT_ENTRIES:
            findings.append(finding("error", "STORE_LAYOUT_INVALID", "store root contains unsupported entry", path=rel))
            continue
        kind = path_kind(entry)
        if entry.name == "store.json":
            if kind != "file":
                findings.append(finding("error", "STORE_LAYOUT_INVALID", "store.json must be a regular file", path=rel))
        else:
            if kind in {"symlink", "reparse"}:
                findings.append(finding("error", "STORE_LAYOUT_INVALID", "store root directory entry must not be a symlink or reparse point", path=rel))
            elif kind != "dir":
                findings.append(finding("error", "STORE_LAYOUT_INVALID", "store root entry must be a directory", path=rel))
    blobs = store.root / "blobs"
    try:
        blob_entries = sorted(blobs.iterdir(), key=lambda item: item.name)
    except OSError as exc:
        findings.append(finding("error", "STORE_IO_ERROR", sanitize_message(store.root, f"could not read blobs directory: {exc}"), path="blobs"))
        return findings
    for entry in blob_entries:
        rel = report_relative_path(store.root, entry)
        if entry.name not in STORE_BLOBS_ENTRIES:
            findings.append(finding("error", "STORE_LAYOUT_INVALID", "blobs directory contains unsupported content-addressing algorithm", path=rel))
    return findings


def staging_findings(store: store_source_capture.StoreInfo) -> list[dict[str, Any]]:
    stage = store.root / ".staging"
    try:
        entries = sorted(stage.iterdir(), key=lambda item: item.name)
    except OSError as exc:
        return [
            finding(
                "indeterminate",
                "STORE_STAGING_UNREADABLE",
                sanitize_message(store.root, f"could not read .staging: {exc}"),
                path=".staging",
            )
        ]
    if not entries:
        return []
    findings: list[dict[str, Any]] = []
    for entry in entries:
        findings.append(
            finding(
                "indeterminate",
                "STORE_STAGING_NOT_EMPTY",
                "store staging directory is not empty; verification cannot distinguish active writes from crash residue",
                path=report_relative_path(store.root, entry),
            )
        )
    return findings


def validate_capture_dir_shape(store: store_source_capture.StoreInfo, capture_dir: Path) -> None:
    if path_kind(capture_dir) in {"symlink", "reparse"}:
        raise store_source_capture.StoreError("STORE_CAPTURE_PATH_UNSAFE", "capture directory must not be a symlink or reparse point")
    if path_kind(capture_dir) != "dir":
        raise store_source_capture.StoreError("STORE_CAPTURE_INVALID", "capture entry must be a directory")
    try:
        parsed = store_source_capture.capture_dir_name("urn:uuid:" + capture_dir.name)
    except store_source_capture.StoreError as exc:
        raise store_source_capture.StoreError("STORE_CAPTURE_INVALID", "capture directory name must be a canonical UUID") from exc
    if parsed != capture_dir.name:
        raise store_source_capture.StoreError("STORE_CAPTURE_INVALID", "capture directory name must be canonical lowercase UUID")
    names = {entry.name for entry in capture_dir.iterdir()}
    extra = sorted(names - CAPTURE_DIR_ENTRIES)
    if extra:
        raise store_source_capture.StoreError("STORE_CAPTURE_SHAPE_INVALID", f"capture directory has unsupported entries: {extra}")
    context_dir = capture_dir / "validation-context"
    if context_dir.exists() or context_dir.is_symlink():
        if path_kind(context_dir) != "dir":
            raise store_source_capture.StoreError("STORE_CAPTURE_SHAPE_INVALID", "validation-context must be a directory")
        context_names = {entry.name for entry in context_dir.iterdir()}
        if context_names != VALIDATION_CONTEXT_ENTRIES:
            missing = sorted(VALIDATION_CONTEXT_ENTRIES - context_names)
            extra_context = sorted(context_names - VALIDATION_CONTEXT_ENTRIES)
            raise store_source_capture.StoreError(
                "STORE_CAPTURE_SHAPE_INVALID",
                f"validation-context entries mismatch; missing={missing}; extra={extra_context}",
            )


def verify_captures(store: store_source_capture.StoreInfo) -> tuple[list[dict[str, Any]], set[str], list[dict[str, Any]]]:
    captures: list[dict[str, Any]] = []
    retained_paths: set[str] = set()
    findings: list[dict[str, Any]] = []
    captures_dir = store.root / "captures"
    try:
        entries = sorted(captures_dir.iterdir(), key=lambda item: item.name)
    except OSError as exc:
        return [], set(), [exception_finding(store, "error", "STORE_IO_ERROR", exc, captures_dir)]
    for entry in entries:
        rel = report_relative_path(store.root, entry)
        try:
            validate_capture_dir_shape(store, entry)
            verified = store_source_capture.verify_stored_capture(store, entry)
            if verified.raw_blob_store_path is not None:
                retained_paths.add(verified.raw_blob_store_path)
            captures.append(
                {
                    "capture_id": verified.capture_id,
                    "store_path": verified.capture_dir,
                    "status": "pass",
                    "bundle_digest": verified.bundle_digest,
                    "raw_blob_retention_state": verified.raw_blob_retention_state,
                    "raw_blob_digest": verified.raw_blob_digest,
                    **({"raw_blob_store_path": verified.raw_blob_store_path} if verified.raw_blob_store_path is not None else {}),
                }
            )
        except store_source_capture.StoreError as exc:
            findings.append(store_error_finding(store, "error", exc, entry))
            captures.append({"store_path": rel, "status": "fail", "code": exc.code})
        except validate_source_capture_bundle.ValidationError as exc:
            findings.append(exception_finding(store, "error", "STORE_RECEIPT_INVALID", exc, entry))
            captures.append({"store_path": rel, "status": "fail", "code": "STORE_RECEIPT_INVALID"})
        except (OSError, UnicodeError) as exc:
            findings.append(exception_finding(store, "error", "STORE_IO_ERROR", exc, entry))
            captures.append({"store_path": rel, "status": "fail", "code": "STORE_IO_ERROR"})
    return captures, retained_paths, findings


def expected_cas_rel(prefix: str, digest_hex: str) -> str:
    return f"blobs/sha256/{prefix}/{digest_hex}"


def verify_cas(store: store_source_capture.StoreInfo, retained_paths: set[str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    cas_root = store.root / "blobs" / "sha256"
    try:
        prefix_dirs = sorted(cas_root.iterdir(), key=lambda item: item.name)
    except OSError as exc:
        return [finding("error", "STORE_IO_ERROR", sanitize_message(store.root, f"could not read CAS root: {exc}"), path="blobs/sha256")]
    for prefix_dir in prefix_dirs:
        prefix_rel = report_relative_path(store.root, prefix_dir)
        kind = path_kind(prefix_dir)
        if kind in {"symlink", "reparse"}:
            findings.append(finding("error", "STORE_BLOB_PATH_UNSAFE", "CAS prefix must not be a symlink or reparse point", path=prefix_rel))
            continue
        if kind != "dir":
            findings.append(finding("error", "STORE_CAS_PATH_INVALID", "CAS prefix entry must be a directory", path=prefix_rel))
            continue
        if len(prefix_dir.name) != 2 or any(char not in HEX for char in prefix_dir.name):
            findings.append(finding("error", "STORE_CAS_PATH_INVALID", "CAS prefix directory must be two lowercase hex characters", path=prefix_rel))
            continue
        try:
            blobs = sorted(prefix_dir.iterdir(), key=lambda item: item.name)
        except OSError as exc:
            findings.append(finding("error", "STORE_IO_ERROR", sanitize_message(store.root, f"could not read CAS prefix: {exc}"), path=prefix_rel))
            continue
        for blob in blobs:
            blob_rel = report_relative_path(store.root, blob)
            blob_kind = path_kind(blob)
            if blob_kind in {"symlink", "reparse"}:
                findings.append(finding("error", "STORE_BLOB_PATH_UNSAFE", "CAS blob must not be a symlink or reparse point", path=blob_rel))
                continue
            if blob_kind != "file":
                findings.append(finding("error", "STORE_CAS_PATH_INVALID", "CAS blob entry must be a regular file", path=blob_rel))
                continue
            if len(blob.name) != 64 or any(char not in HEX for char in blob.name) or blob.name[:2] != prefix_dir.name:
                findings.append(finding("error", "STORE_CAS_PATH_INVALID", "CAS blob filename must match prefix-2 SHA256 layout", path=blob_rel))
                continue
            expected_digest = "sha256:" + blob.name
            try:
                desc = store_source_capture.hash_existing_regular_file(blob, "STORE_BLOB_FIXITY_MISMATCH", "CAS blob")
            except store_source_capture.StoreError as exc:
                findings.append(store_error_finding(store, "error", exc, blob))
                continue
            except OSError as exc:
                findings.append(exception_finding(store, "error", "STORE_IO_ERROR", exc, blob))
                continue
            if desc.digest != expected_digest:
                findings.append(
                    finding(
                        "error",
                        "STORE_BLOB_FIXITY_MISMATCH",
                        "CAS blob content digest does not match its path",
                        path=blob_rel,
                        details={"expected_digest": expected_digest, "actual_digest": desc.digest},
                    )
                )
                continue
            expected_rel = expected_cas_rel(prefix_dir.name, blob.name)
            if expected_rel not in retained_paths:
                findings.append(
                    finding(
                        "warning",
                        "STORE_ORPHAN_CAS_BLOB",
                        "CAS blob is valid but is not referenced by any retained capture receipt",
                        path=blob_rel,
                        details={"digest": expected_digest, "size": desc.size},
                    )
                )
    return findings


def report_status(findings: list[dict[str, Any]]) -> str:
    if any(item["severity"] == "indeterminate" for item in findings):
        return "indeterminate"
    if any(item["severity"] == "error" for item in findings):
        return "fail"
    if any(item["severity"] == "warning" for item in findings):
        return "pass_with_warnings"
    return "pass"


def build_report(
    store: store_source_capture.StoreInfo,
    captures: list[dict[str, Any]],
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    status = report_status(findings)
    return {
        "schema": REPORT_SCHEMA,
        "profile": REPORT_PROFILE,
        "store": {
            "layout": store_source_capture.STORE_LAYOUT,
            "layout_version": STORE_VERSION,
            "instance_id": store.meta["store_instance_id"],
        },
        "assurance_scope": {
            "retention_and_fixity": True,
            "source_authenticity": False,
            "evidentiary_support": False,
            "review_status": False,
            "action_authorization": False,
            "repair_performed": False,
        },
        "summary": {
            "status": status,
            "captures_total": len(captures),
            "captures_verified": sum(1 for item in captures if item.get("status") == "pass"),
            "warnings_count": sum(1 for item in findings if item["severity"] == "warning"),
            "errors_count": sum(1 for item in findings if item["severity"] == "error"),
            "indeterminate_count": sum(1 for item in findings if item["severity"] == "indeterminate"),
        },
        "captures": captures,
        "findings": findings,
    }


def verify_store_root(store_root: Path, *, after_scan_hook: Callable[[], None] | None = None) -> dict[str, Any]:
    store_source_capture.ensure_no_reparse_components(store_root, "STORE_ROOT_UNSAFE", "store root")
    start_inventory = collect_inventory(store_root)
    store = store_source_capture.load_store(store_root)
    findings = store_layout_findings(store)
    findings.extend(staging_findings(store))
    captures, retained_paths, capture_findings = verify_captures(store)
    findings.extend(capture_findings)
    findings.extend(verify_cas(store, retained_paths))
    if after_scan_hook is not None:
        after_scan_hook()
    end_inventory = collect_inventory(store.root)
    if start_inventory != end_inventory:
        findings.append(
            finding(
                "indeterminate",
                "STORE_CHANGED_DURING_SCAN",
                "store inventory changed during verification; rerun after writes have stopped",
            )
        )
    return build_report(store, captures, findings)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify a VAKS Source Capture Store without modifying it.")
    parser.add_argument("--store-root", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = verify_store_root(Path(args.store_root))
    except store_source_capture.StoreError as exc:
        root = Path(args.store_root)
        print(json.dumps({"status": "fail", "code": exc.code, "message": sanitize_message(root, exc.message)}, allow_nan=False, sort_keys=True))
        return 1
    except validate_source_capture_bundle.ValidationError as exc:
        print(json.dumps({"status": "fail", "code": "STORE_INVALID", "message": str(exc)}, allow_nan=False, sort_keys=True))
        return 1
    except (OSError, UnicodeError) as exc:
        root = Path(args.store_root)
        print(json.dumps({"status": "fail", "code": "STORE_IO_ERROR", "message": sanitize_message(root, str(exc))}, allow_nan=False, sort_keys=True))
        return 1
    print(json.dumps(report, allow_nan=False, sort_keys=True))
    status = report["summary"]["status"]
    if status in {"pass", "pass_with_warnings"}:
        return 0
    if status == "indeterminate":
        return 3
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
