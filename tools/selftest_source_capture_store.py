#!/usr/bin/env python
"""Self-test Source Capture Store v1 PR-B1 behavior."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
INSPECTOR = ROOT / "tools" / "inspect_source_snapshot.py"
STORE_TOOL = ROOT / "tools" / "store_source_capture.py"
VERIFY_STORE_TOOL = ROOT / "tools" / "verify_source_capture_store.py"
sys.path.insert(0, str(ROOT / "tools"))
import store_source_capture  # noqa: E402
import validate_source_capture_bundle  # noqa: E402
import verify_source_capture_store  # noqa: E402

REPORT_PATH_RE = re.compile(r"^(?!/)(?!.*(^|/)\.\.?(/|$))(?:[A-Za-z0-9._-]|%[0-9A-F]{2}|/)+$")


def run_json(args: list[str], *, expect: int = 0) -> dict[str, Any]:
    result = subprocess.run(args, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != expect:
        raise AssertionError(
            f"command returned {result.returncode}, expected {expect}\n"
            f"args={args}\nstdout={result.stdout}\nstderr={result.stderr}"
        )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"command did not emit JSON\nargs={args}\nstdout={result.stdout}\nstderr={result.stderr}") from exc


def write_zip(path: Path, entries: list[tuple[str, bytes]]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, data in entries:
            info = zipfile.ZipInfo(name)
            info.date_time = (2026, 1, 1, 0, 0, 0)
            zf.writestr(info, data)


def write_canonical_json(path: Path, obj: dict[str, Any]) -> None:
    path.write_bytes(validate_source_capture_bundle.canonical_json_bytes(obj))


def file_descriptor(path: Path) -> dict[str, Any]:
    return {
        "name": path.name,
        "size": path.stat().st_size,
        "digest": validate_source_capture_bundle.digest_file(path),
    }


def rewrite_receipt_bundle(capture: Path) -> None:
    receipt_path = capture / "capture-storage-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    bundle_dir = capture / "bundle"
    descriptors = store_source_capture.bundle_artifact_descriptors(bundle_dir)
    receipt["bundle"]["artifacts"] = [
        store_source_capture.descriptor_without_media(desc)
        for desc in sorted(descriptors, key=lambda item: item.name)
    ]
    receipt["bundle"]["digest"] = store_source_capture.bundle_digest(descriptors)
    write_canonical_json(receipt_path, receipt)


def add_hygiene_finding(capture: Path, finding: dict[str, Any]) -> None:
    bundle_dir = capture / "bundle"
    hygiene_path = bundle_dir / "snapshot-hygiene.intoto.json"
    envelope_path = bundle_dir / "capture-envelope.json"
    hygiene = json.loads(hygiene_path.read_text(encoding="utf-8"))
    findings = hygiene["predicate"]["findings"]
    findings.append(finding)
    hygiene["predicate"]["summary"]["finding_count"] = len(findings)
    order = validate_source_capture_bundle.SEVERITY_ORDER
    max_severity = "none"
    for item in findings:
        if order[item["severity"]] > order[max_severity]:
            max_severity = item["severity"]
    hygiene["predicate"]["summary"]["max_severity"] = max_severity
    write_canonical_json(hygiene_path, hygiene)
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    envelope["inspection_refs"][0]["size"] = hygiene_path.stat().st_size
    envelope["inspection_refs"][0]["digest"] = validate_source_capture_bundle.digest_file(hygiene_path)
    write_canonical_json(envelope_path, envelope)
    rewrite_receipt_bundle(capture)


def rewrite_envelope(capture: Path, envelope: dict[str, Any]) -> None:
    envelope_path = capture / "bundle" / "capture-envelope.json"
    write_canonical_json(envelope_path, envelope)
    rewrite_receipt_bundle(capture)


def rewrite_hygiene_and_ref(capture: Path, hygiene: dict[str, Any]) -> None:
    bundle_dir = capture / "bundle"
    hygiene_path = bundle_dir / "snapshot-hygiene.intoto.json"
    envelope_path = bundle_dir / "capture-envelope.json"
    write_canonical_json(hygiene_path, hygiene)
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    envelope["inspection_refs"][0]["size"] = hygiene_path.stat().st_size
    envelope["inspection_refs"][0]["digest"] = validate_source_capture_bundle.digest_file(hygiene_path)
    write_canonical_json(envelope_path, envelope)
    rewrite_receipt_bundle(capture)


def update_receipt_context_descriptor(capture: Path, key: str) -> None:
    receipt_path = capture / "capture-storage-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    context_file = capture / "validation-context" / (
        store_source_capture.IMPLEMENTATION_CONTEXT_NAME if key == "implementation" else store_source_capture.POLICY_CONTEXT_NAME
    )
    receipt["validation_context"][key]["size"] = context_file.stat().st_size
    receipt["validation_context"][key]["digest"] = validate_source_capture_bundle.digest_file(context_file)
    write_canonical_json(receipt_path, receipt)


def try_symlink_dir(target: Path, link: Path) -> bool:
    try:
        os.symlink(target, link, target_is_directory=True)
        return True
    except (OSError, NotImplementedError):
        return False


def make_bundle(tmp: Path, name: str, entries: list[tuple[str, bytes]], *extra: str) -> tuple[Path, Path, dict[str, Any]]:
    source = tmp / f"{name}.zip"
    out_dir = tmp / f"{name}-bundle"
    write_zip(source, entries)
    cmd = [
        sys.executable,
        str(INSPECTOR),
        str(source),
        "--out",
        str(out_dir),
        "--source-kind",
        "archive",
        "--capture-method",
        "archive_file",
        *extra,
    ]
    result = run_json(cmd)
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    return source, out_dir, envelope


def store_init(store: Path, *, expect: int = 0) -> dict[str, Any]:
    return run_json([sys.executable, str(STORE_TOOL), "init", "--store-root", str(store)], expect=expect)


def store_put(store: Path, bundle: Path, raw_blob: Path | None = None, *, expect: int = 0) -> dict[str, Any]:
    cmd = [
        sys.executable,
        str(STORE_TOOL),
        "put",
        "--store-root",
        str(store),
        "--bundle-dir",
        str(bundle),
    ]
    if raw_blob is not None:
        cmd.extend(["--raw-blob", str(raw_blob)])
    return run_json(cmd, expect=expect)


def store_verify_capture(store: Path, capture_id: str, *, expect: int = 0) -> dict[str, Any]:
    return run_json(
        [
            sys.executable,
            str(STORE_TOOL),
            "verify-capture",
            "--store-root",
            str(store),
            "--capture-id",
            capture_id,
        ],
        expect=expect,
    )


def store_verify_all(store: Path, *, expect: int = 0) -> dict[str, Any]:
    payload = run_json(
        [
            sys.executable,
            str(VERIFY_STORE_TOOL),
            "--store-root",
            str(store),
        ],
        expect=expect,
    )
    if payload.get("schema") == verify_source_capture_store.REPORT_SCHEMA:
        assert_report_schema(payload)
    return payload


def capture_dir(store: Path, capture_id: str) -> Path:
    return store / "captures" / capture_id.split("urn:uuid:", 1)[1].lower()


def finding_codes(report: dict[str, Any]) -> set[str]:
    return {item["code"] for item in report.get("findings", [])}


def assert_path_is_report_safe(path: str) -> None:
    assert REPORT_PATH_RE.match(path), path
    assert "\\" not in path
    assert "\n" not in path
    assert "\r" not in path


def assert_report_paths_relative(report: dict[str, Any]) -> None:
    for finding in report.get("findings", []):
        path = finding.get("path")
        if path is not None:
            assert not Path(path).is_absolute()
            assert_path_is_report_safe(path)
    for capture in report.get("captures", []):
        path = capture.get("store_path")
        if path is not None:
            assert not Path(path).is_absolute()
            assert_path_is_report_safe(path)
        raw_path = capture.get("raw_blob_store_path")
        if raw_path is not None:
            assert_path_is_report_safe(raw_path)


def assert_report_schema(report: dict[str, Any]) -> None:
    assert set(report) == {"schema", "profile", "store", "assurance_scope", "summary", "captures", "findings"}
    assert report["schema"] == verify_source_capture_store.REPORT_SCHEMA
    assert report["profile"] == verify_source_capture_store.REPORT_PROFILE
    assert set(report["store"]) == {"layout", "layout_version", "instance_id"}
    assert report["store"]["layout"] == store_source_capture.STORE_LAYOUT
    assert report["store"]["layout_version"] == "1"
    assert store_source_capture.CAPTURE_ID_RE.match(report["store"]["instance_id"])
    assert report["assurance_scope"] == {
        "retention_and_fixity": True,
        "source_authenticity": False,
        "evidentiary_support": False,
        "review_status": False,
        "action_authorization": False,
        "repair_performed": False,
    }
    assert report["summary"]["status"] in {"pass", "pass_with_warnings", "fail", "indeterminate"}
    assert_report_paths_relative(report)


def corrupt_same_size_and_restore_mtime(path: Path) -> None:
    st = path.stat()
    data = bytearray(path.read_bytes())
    assert data
    data[0] ^= 1
    path.write_bytes(bytes(data))
    os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns))


def test_init_rejects_nonempty_without_store_json(tmp: Path) -> None:
    store = tmp / "store"
    store.mkdir()
    (store / "stray.txt").write_text("stray", encoding="utf-8")
    result = store_init(store, expect=1)
    assert result["status"] == "fail"
    assert result["code"] == "STORE_ROOT_NOT_EMPTY"


def test_put_retains_raw_blob_and_is_idempotent(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "clean", [("repo/a.txt", b"a")])
    first = store_put(store, bundle, source)
    assert first["status"] == "pass"
    assert first["result"] == "stored"
    assert first["raw_blob_retention_state"] == "retained"
    receipt_path = store / first["receipt"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["capture_id"] == envelope["capture_id"]
    assert receipt["raw_blob"]["retention_state"] == "retained"
    assert (store / receipt["raw_blob"]["store_path"]).is_file()
    assert (capture_dir(store, envelope["capture_id"]) / "bundle" / "capture-envelope.json").is_file()
    assert (capture_dir(store, envelope["capture_id"]) / "validation-context" / "raw-intake-policy.json").is_file()
    verify = store_verify_capture(store, envelope["capture_id"])
    assert verify["status"] == "pass"
    duplicate = store_put(store, bundle, source)
    assert duplicate["status"] == "pass"
    assert duplicate["result"] == "already_retained"
    report = store_verify_all(store)
    assert report["summary"]["status"] == "pass"
    assert report["assurance_scope"]["retention_and_fixity"] is True
    assert report["assurance_scope"]["source_authenticity"] is False
    assert_report_paths_relative(report)


def test_put_without_raw_blob_records_not_retained(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    _source, bundle, envelope = make_bundle(tmp, "no-raw", [("repo/a.txt", b"a")])
    result = store_put(store, bundle)
    assert result["status"] == "pass"
    receipt = json.loads((capture_dir(store, envelope["capture_id"]) / "capture-storage-receipt.json").read_text(encoding="utf-8"))
    assert receipt["raw_blob"]["retention_state"] == "not_retained"
    assert receipt["raw_blob"]["expected_digest"] == envelope["observation"]["blob"]["digest"]
    assert store_verify_capture(store, envelope["capture_id"])["status"] == "pass"
    report = store_verify_all(store)
    assert report["summary"]["status"] == "pass"
    assert report["captures"][0]["raw_blob_retention_state"] == "not_retained"


def test_verify_store_empty_store_passes(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    report = store_verify_all(store)
    assert report["summary"]["status"] == "pass"
    assert report["summary"]["captures_total"] == 0


def test_verify_store_missing_referenced_blob_is_error(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "missing-blob", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    receipt = json.loads((capture_dir(store, envelope["capture_id"]) / "capture-storage-receipt.json").read_text(encoding="utf-8"))
    (store / receipt["raw_blob"]["store_path"]).unlink()
    report = store_verify_all(store, expect=1)
    assert report["summary"]["status"] == "fail"
    assert "STORE_RAW_BLOB_MISSING" in finding_codes(report)


def test_verify_store_rejects_corrupt_referenced_cas_blob(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "corrupt-referenced", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    receipt = json.loads((capture_dir(store, envelope["capture_id"]) / "capture-storage-receipt.json").read_text(encoding="utf-8"))
    (store / receipt["raw_blob"]["store_path"]).write_bytes(b"corrupt")
    report = store_verify_all(store, expect=1)
    assert report["summary"]["status"] == "fail"
    assert "STORE_RAW_BLOB_MISMATCH" in finding_codes(report)


def test_verify_store_output_argument_does_not_touch_store_or_symlink(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "output-arg", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    envelope_path = capture_dir(store, envelope["capture_id"]) / "bundle" / "capture-envelope.json"
    before = envelope_path.read_bytes()
    proc = subprocess.run(
        [
            sys.executable,
            str(VERIFY_STORE_TOOL),
            "--store-root",
            str(store),
            "--output",
            str(envelope_path),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.returncode != 0
    assert envelope_path.read_bytes() == before

    outside = tmp / "outside-report.json"
    outside.write_text("keep", encoding="utf-8")
    link = tmp / "report-link.json"
    try:
        os.symlink(outside, link)
    except (OSError, NotImplementedError):
        return
    proc = subprocess.run(
        [
            sys.executable,
            str(VERIFY_STORE_TOOL),
            "--store-root",
            str(store),
            "--output",
            str(link),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.returncode != 0
    assert outside.read_text(encoding="utf-8") == "keep"


def test_verify_store_detects_cas_content_changed_during_scan(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "cas-change-during-scan", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    receipt = json.loads((capture_dir(store, envelope["capture_id"]) / "capture-storage-receipt.json").read_text(encoding="utf-8"))
    blob_path = store / receipt["raw_blob"]["store_path"]

    def mutate_blob() -> None:
        data = bytearray(blob_path.read_bytes())
        data[0] ^= 1
        blob_path.write_bytes(bytes(data))
        os.utime(blob_path, None)

    report = verify_source_capture_store.verify_store_root(store, after_scan_hook=mutate_blob)
    assert report["summary"]["status"] == "indeterminate"
    assert "STORE_CHANGED_DURING_SCAN" in finding_codes(report)


def test_verify_store_detects_same_size_cas_change_with_mtime_restored(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "cas-change-mtime-restored", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    receipt = json.loads((capture_dir(store, envelope["capture_id"]) / "capture-storage-receipt.json").read_text(encoding="utf-8"))
    blob_path = store / receipt["raw_blob"]["store_path"]

    report = verify_source_capture_store.verify_store_root(
        store,
        after_scan_hook=lambda: corrupt_same_size_and_restore_mtime(blob_path),
    )
    assert_report_schema(report)
    assert report["summary"]["status"] == "indeterminate"
    assert "STORE_CHANGED_DURING_SCAN" in finding_codes(report)


def test_verify_store_detects_capture_content_changed_during_scan(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "capture-change-during-scan", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    envelope_path = capture_dir(store, envelope["capture_id"]) / "bundle" / "capture-envelope.json"

    def mutate_capture() -> None:
        envelope_path.write_text(envelope_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        os.utime(envelope_path, None)

    report = verify_source_capture_store.verify_store_root(store, after_scan_hook=mutate_capture)
    assert report["summary"]["status"] == "indeterminate"
    assert "STORE_CHANGED_DURING_SCAN" in finding_codes(report)


def test_verify_store_detects_same_size_capture_change_with_mtime_restored(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "capture-change-mtime-restored", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    envelope_path = capture_dir(store, envelope["capture_id"]) / "bundle" / "capture-envelope.json"

    report = verify_source_capture_store.verify_store_root(
        store,
        after_scan_hook=lambda: corrupt_same_size_and_restore_mtime(envelope_path),
    )
    assert_report_schema(report)
    assert report["summary"]["status"] == "indeterminate"
    assert "STORE_CHANGED_DURING_SCAN" in finding_codes(report)


def test_verify_store_detects_store_json_changed_during_scan(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    store_json = store / "store.json"

    def mutate_store_json() -> None:
        store_json.write_text(store_json.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        os.utime(store_json, None)

    report = verify_source_capture_store.verify_store_root(store, after_scan_hook=mutate_store_json)
    assert report["summary"]["status"] == "indeterminate"
    assert "STORE_CHANGED_DURING_SCAN" in finding_codes(report)


def test_verify_store_detects_store_json_change_with_mtime_restored(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    store_json = store / "store.json"
    report = verify_source_capture_store.verify_store_root(
        store,
        after_scan_hook=lambda: corrupt_same_size_and_restore_mtime(store_json),
    )
    assert_report_schema(report)
    assert report["summary"]["status"] == "indeterminate"
    assert "STORE_CHANGED_DURING_SCAN" in finding_codes(report)


def test_verify_store_detects_store_json_changed_during_load_store_window(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    store_json = store / "store.json"
    original_load_store = store_source_capture.load_store

    def patched_load_store(root: Path) -> store_source_capture.StoreInfo:
        loaded = original_load_store(root)
        meta = json.loads(store_json.read_text(encoding="utf-8"))
        meta["store_instance_id"] = "urn:uuid:11111111-1111-4111-8111-111111111111"
        write_canonical_json(store_json, meta)
        return loaded

    store_source_capture.load_store = patched_load_store
    try:
        report = verify_source_capture_store.verify_store_root(store)
    finally:
        store_source_capture.load_store = original_load_store

    assert_report_schema(report)
    assert report["summary"]["status"] == "indeterminate"
    assert "STORE_CHANGED_DURING_SCAN" in finding_codes(report)


def test_verify_store_detects_unknown_root_entry_added_during_scan(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    report = verify_source_capture_store.verify_store_root(
        store,
        after_scan_hook=lambda: (store / "stray.txt").write_text("stray", encoding="utf-8"),
    )
    assert_report_schema(report)
    assert report["summary"]["status"] == "indeterminate"
    assert "STORE_CHANGED_DURING_SCAN" in finding_codes(report)


def test_verify_store_detects_unsupported_algorithm_added_during_scan(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    report = verify_source_capture_store.verify_store_root(
        store,
        after_scan_hook=lambda: (store / "blobs" / "sha512").mkdir(),
    )
    assert_report_schema(report)
    assert report["summary"]["status"] == "indeterminate"
    assert "STORE_CHANGED_DURING_SCAN" in finding_codes(report)


def test_verify_store_reports_valid_orphan_cas_blob_as_warning(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    data = b"orphan"
    digest = validate_source_capture_bundle.sha256_bytes(data)
    target = store / store_source_capture.expected_raw_blob_store_path(digest)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    report = store_verify_all(store)
    assert report["summary"]["status"] == "pass_with_warnings"
    assert "STORE_ORPHAN_CAS_BLOB" in finding_codes(report)
    assert_report_paths_relative(report)


def test_verify_store_rejects_corrupt_orphan_cas_blob(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    digest = validate_source_capture_bundle.sha256_bytes(b"expected")
    target = store / store_source_capture.expected_raw_blob_store_path(digest)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"actual")
    report = store_verify_all(store, expect=1)
    assert report["summary"]["status"] == "fail"
    assert "STORE_BLOB_FIXITY_MISMATCH" in finding_codes(report)


def test_verify_store_rejects_capture_symlink(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    outside = tmp / "outside-capture"
    outside.mkdir()
    link = store / "captures" / "00000000-0000-4000-8000-000000000000"
    if not try_symlink_dir(outside, link):
        return
    report = store_verify_all(store, expect=1)
    assert report["summary"]["status"] == "fail"
    assert "STORE_CAPTURE_PATH_UNSAFE" in finding_codes(report)


def test_verify_store_rejects_cas_symlink(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    data = b"target"
    digest = validate_source_capture_bundle.sha256_bytes(data)
    target = store / store_source_capture.expected_raw_blob_store_path(digest)
    target.parent.mkdir(parents=True, exist_ok=True)
    outside = tmp / "outside-blob"
    outside.write_bytes(data)
    try:
        os.symlink(outside, target)
    except (OSError, NotImplementedError):
        return
    report = store_verify_all(store, expect=1)
    assert report["summary"]["status"] == "fail"
    assert "STORE_BLOB_PATH_UNSAFE" in finding_codes(report)


def test_verify_store_rejects_extra_capture_file(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "extra-capture-file", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    (capture_dir(store, envelope["capture_id"]) / "extra.txt").write_text("extra", encoding="utf-8")
    report = store_verify_all(store, expect=1)
    assert report["summary"]["status"] == "fail"
    assert "STORE_CAPTURE_SHAPE_INVALID" in finding_codes(report)


def test_verify_store_rejects_extra_validation_context_file(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "extra-context-file", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    (capture_dir(store, envelope["capture_id"]) / "validation-context" / "evil.json").write_text("{}", encoding="utf-8")
    report = store_verify_all(store, expect=1)
    assert report["summary"]["status"] == "fail"
    assert "STORE_CAPTURE_SHAPE_INVALID" in finding_codes(report)


def test_verify_store_rejects_extra_validation_context_directory(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "extra-context-dir", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    (capture_dir(store, envelope["capture_id"]) / "validation-context" / "extra").mkdir()
    report = store_verify_all(store, expect=1)
    assert report["summary"]["status"] == "fail"
    assert "STORE_CAPTURE_SHAPE_INVALID" in finding_codes(report)


def test_verify_store_rejects_unknown_store_root_entry(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    (store / "stray.txt").write_text("stray", encoding="utf-8")
    report = store_verify_all(store, expect=1)
    assert report["summary"]["status"] == "fail"
    assert "STORE_LAYOUT_INVALID" in finding_codes(report)


def test_verify_store_reports_malformed_store_json(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    (store / "store.json").write_text("{bad", encoding="utf-8")
    result = store_verify_all(store, expect=1)
    assert result["status"] == "fail"
    assert result["code"] == "STORE_INVALID"


def test_verify_store_reports_duplicate_key_store_json(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    (store / "store.json").write_text('{"schema":"a","schema":"b"}', encoding="utf-8")
    result = store_verify_all(store, expect=1)
    assert result["status"] == "fail"
    assert result["code"] == "STORE_INVALID"


def test_verify_store_reports_missing_store_json_field(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    meta = json.loads((store / "store.json").read_text(encoding="utf-8"))
    del meta["content_addressing"]
    write_canonical_json(store / "store.json", meta)
    result = store_verify_all(store, expect=1)
    assert result["status"] == "fail"
    assert result["code"] == "STORE_INVALID"


def test_verify_store_reports_capture_directory_io_shape_error(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    shutil.rmtree(store / "captures")
    (store / "captures").write_text("not a directory", encoding="utf-8")
    result = store_verify_all(store, expect=1)
    assert result["status"] == "fail"
    assert result["code"] == "STORE_LAYOUT_INCOMPLETE"


def test_verify_store_rejects_missing_receipt(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "missing-receipt", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    (capture_dir(store, envelope["capture_id"]) / "capture-storage-receipt.json").unlink()
    report = store_verify_all(store, expect=1)
    assert report["summary"]["status"] == "fail"
    assert "STORE_RECEIPT_MISSING" in finding_codes(report)


def test_verify_store_reports_malformed_receipt(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "malformed-receipt", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    (capture_dir(store, envelope["capture_id"]) / "capture-storage-receipt.json").write_text("{bad", encoding="utf-8")
    report = store_verify_all(store, expect=1)
    assert report["summary"]["status"] == "fail"
    assert "STORE_RECEIPT_INVALID" in finding_codes(report)


def test_verify_store_reports_duplicate_key_receipt(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "duplicate-key-receipt", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    (capture_dir(store, envelope["capture_id"]) / "capture-storage-receipt.json").write_text('{"schema":"a","schema":"b"}', encoding="utf-8")
    report = store_verify_all(store, expect=1)
    assert report["summary"]["status"] == "fail"
    assert "STORE_RECEIPT_INVALID" in finding_codes(report)


def test_verify_store_report_schema_accepts_unicode_invalid_entry(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    (store / "captures" / "é").mkdir()
    report = store_verify_all(store, expect=1)
    assert report["summary"]["status"] == "fail"
    assert report["findings"][0]["path"] == "captures/%C3%A9"
    assert_path_is_report_safe(report["findings"][0]["path"])


def test_verify_store_report_schema_accepts_backslash_and_control_encoding(tmp: Path) -> None:
    encoded = verify_source_capture_store.encode_path_component("a\\b\né")
    assert encoded == "a%5Cb%0A%C3%A9"
    dummy = {
        "schema": verify_source_capture_store.REPORT_SCHEMA,
        "profile": verify_source_capture_store.REPORT_PROFILE,
        "store": {
            "layout": store_source_capture.STORE_LAYOUT,
            "layout_version": "1",
            "instance_id": "urn:uuid:00000000-0000-4000-8000-000000000000",
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
            "status": "fail",
            "captures_total": 0,
            "captures_verified": 0,
            "warnings_count": 0,
            "errors_count": 1,
            "indeterminate_count": 0,
        },
        "captures": [],
        "findings": [{"severity": "error", "code": "X", "message": "x", "path": encoded}],
    }
    assert_report_schema(dummy)


def test_verify_store_report_contains_no_absolute_store_path(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "no-absolute-path", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    (capture_dir(store, envelope["capture_id"]) / "capture-storage-receipt.json").unlink()
    report = store_verify_all(store, expect=1)
    assert str(store) not in json.dumps(report, ensure_ascii=False)
    assert_report_schema(report)


def test_verify_store_continues_after_one_invalid_capture(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "invalid-one", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    source2, bundle2, envelope2 = make_bundle(tmp, "valid-two", [("repo/b.txt", b"b")])
    assert store_put(store, bundle2, source2)["status"] == "pass"
    (capture_dir(store, envelope["capture_id"]) / "capture-storage-receipt.json").write_text("{bad", encoding="utf-8")
    report = store_verify_all(store, expect=1)
    assert report["summary"]["status"] == "fail"
    assert any(item.get("capture_id") == envelope2["capture_id"] and item.get("status") == "pass" for item in report["captures"])
    assert any(item.get("store_path") == f"captures/{envelope['capture_id'].split('urn:uuid:', 1)[1]}" and item.get("status") == "fail" for item in report["captures"])


def test_verify_store_nonempty_staging_is_indeterminate(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    (store / ".staging" / "leftover").mkdir()
    report = store_verify_all(store, expect=3)
    assert report["summary"]["status"] == "indeterminate"
    assert "STORE_STAGING_NOT_EMPTY" in finding_codes(report)


def test_verify_store_detects_capture_added_during_scan(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"

    def add_capture() -> None:
        (store / "captures" / "00000000-0000-4000-8000-000000000000").mkdir()

    report = verify_source_capture_store.verify_store_root(store, after_scan_hook=add_capture)
    assert report["summary"]["status"] == "indeterminate"
    assert "STORE_CHANGED_DURING_SCAN" in finding_codes(report)


def test_raw_blob_mismatch_does_not_create_capture(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    _source, bundle, envelope = make_bundle(tmp, "mismatch", [("repo/a.txt", b"a")])
    wrong = tmp / "wrong.zip"
    wrong.write_bytes(b"wrong")
    result = store_put(store, bundle, wrong, expect=1)
    assert result["code"] == "RAW_BLOB_DIGEST_MISMATCH"
    assert not capture_dir(store, envelope["capture_id"]).exists()


def test_capture_id_conflict_is_not_overwritten(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "first", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    source2, bundle2, _envelope2 = make_bundle(
        tmp,
        "second",
        [("repo/b.txt", b"b")],
        "--capture-id",
        envelope["capture_id"],
    )
    result = store_put(store, bundle2, source2, expect=1)
    assert result["code"] == "CAPTURE_ID_CONFLICT"
    stored = json.loads((capture_dir(store, envelope["capture_id"]) / "bundle" / "capture-envelope.json").read_text(encoding="utf-8"))
    assert stored["snapshot"]["snapshot_id"] == envelope["snapshot"]["snapshot_id"]


def test_existing_corrupt_cas_blob_is_rejected(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "cas-corrupt", [("repo/a.txt", b"a")])
    expected = envelope["observation"]["blob"]["digest"].split(":", 1)[1]
    target = store / "blobs" / "sha256" / expected[:2] / expected
    target.parent.mkdir(parents=True)
    target.write_bytes(b"corrupt")
    result = store_put(store, bundle, source, expect=1)
    assert result["code"] == "STORE_BLOB_FIXITY_MISMATCH"
    assert target.read_bytes() == b"corrupt"


def test_verify_capture_detects_tampering(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "tamper", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    stored_manifest = capture_dir(store, envelope["capture_id"]) / "bundle" / "snapshot-manifest.jsonl"
    stored_manifest.write_text(stored_manifest.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    result = store_verify_capture(store, envelope["capture_id"], expect=1)
    assert result["code"] == "STORE_BUNDLE_FIXITY_MISMATCH"


def test_store_root_parent_symlink_is_rejected(tmp: Path) -> None:
    real = tmp / "realparent"
    real.mkdir()
    link = tmp / "linkparent"
    if not try_symlink_dir(real, link):
        return
    result = store_init(link / "store", expect=1)
    assert result["code"] == "STORE_ROOT_UNSAFE"


def test_cas_prefix_symlink_is_rejected(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "cas-prefix-link", [("repo/a.txt", b"a")])
    digest_hex = envelope["observation"]["blob"]["digest"].split(":", 1)[1]
    outside = tmp / "outside"
    outside.mkdir()
    prefix = store / "blobs" / "sha256" / digest_hex[:2]
    if not try_symlink_dir(outside, prefix):
        return
    result = store_put(store, bundle, source, expect=1)
    assert result["code"] == "STORE_BLOB_PATH_UNSAFE"
    assert not (outside / digest_hex).exists()


def test_verify_capture_rejects_policy_not_pinned_by_implementation(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "weak-policy", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    capture = capture_dir(store, envelope["capture_id"])
    policy_path = capture / "validation-context" / "raw-intake-policy.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    policy["unsafe_finding"]["codes"] = ["SOME_OTHER_CODE"]
    write_canonical_json(policy_path, policy)
    update_receipt_context_descriptor(capture, "policy")
    result = store_verify_capture(store, envelope["capture_id"], expect=1)
    assert result["code"] == "STORE_CONTEXT_FIXITY_MISMATCH"


def test_verify_capture_replays_policy_listed_warning(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "policy-warning", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    capture = capture_dir(store, envelope["capture_id"])
    add_hygiene_finding(
        capture,
        {
            "code": "ARCHIVE_PATH_TRAVERSAL",
            "severity": "warning",
            "profile": "archive-safety/v1",
            "message": "synthetic policy-listed warning",
        },
    )
    result = store_verify_capture(store, envelope["capture_id"], expect=1)
    assert result["code"] == "BUNDLE_VALIDATION_FAILED"


def test_verify_capture_rejects_fake_validation_context_paths(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "fake-context-path", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    capture = capture_dir(store, envelope["capture_id"])
    receipt_path = capture / "capture-storage-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["validation_context"]["implementation"]["store_path"] = "captures/fake/validation-context/not-real.json"
    receipt["validation_context"]["policy"]["store_path"] = "captures/fake/validation-context/not-real.json"
    write_canonical_json(receipt_path, receipt)
    result = store_verify_capture(store, envelope["capture_id"], expect=1)
    assert result["code"] == "STORE_RECEIPT_INVALID"


def test_verify_capture_rejects_noncanonical_raw_store_path(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "fake-raw-path", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    capture = capture_dir(store, envelope["capture_id"])
    receipt_path = capture / "capture-storage-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["raw_blob"]["store_path"] = "store.json"
    write_canonical_json(receipt_path, receipt)
    result = store_verify_capture(store, envelope["capture_id"], expect=1)
    assert result["code"] == "STORE_RECEIPT_INVALID"


def test_verify_capture_rejects_tree_pdf_magic_tamper(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "tree-pdf-magic", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    capture = capture_dir(store, envelope["capture_id"])
    stored_envelope = json.loads((capture / "bundle" / "capture-envelope.json").read_text(encoding="utf-8"))
    stored_envelope["observation"]["blob"]["media_type"] = "application/pdf"
    stored_envelope["observation"]["content_type"] = {
        "profile": "vaks-media-type-detection/v1",
        "detected_media_type": "application/pdf",
        "detection_basis": "magic_signature",
        "locator_hint_media_type": "application/pdf",
        "hint_match": "matched",
    }
    receipt_path = capture / "capture-storage-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["raw_blob"]["media_type"] = "application/pdf"
    write_canonical_json(receipt_path, receipt)
    rewrite_envelope(capture, stored_envelope)
    result = store_verify_capture(store, envelope["capture_id"], expect=1)
    assert result["code"] == "BUNDLE_VALIDATION_FAILED"


def test_verify_capture_rejects_tampered_max_findings_per_code(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "tamper-max-findings", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    capture = capture_dir(store, envelope["capture_id"])
    hygiene = json.loads((capture / "bundle" / "snapshot-hygiene.intoto.json").read_text(encoding="utf-8"))
    hygiene["predicate"]["parameters"]["max_findings_per_code"] = 1
    rewrite_hygiene_and_ref(capture, hygiene)
    result = store_verify_capture(store, envelope["capture_id"], expect=1)
    assert result["code"] == "BUNDLE_VALIDATION_FAILED"


def test_verify_capture_rejects_not_comparable_hint_match(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "tamper-not-comparable", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    capture = capture_dir(store, envelope["capture_id"])
    stored_envelope = json.loads((capture / "bundle" / "capture-envelope.json").read_text(encoding="utf-8"))
    stored_envelope["observation"]["content_type"]["hint_match"] = "not_comparable"
    rewrite_envelope(capture, stored_envelope)
    result = store_verify_capture(store, envelope["capture_id"], expect=1)
    assert result["code"] == "BUNDLE_VALIDATION_FAILED"


def test_verify_capture_rejects_locator_hint_basis(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "tamper-locator-hint", [("repo/a.txt", b"a")])
    assert store_put(store, bundle, source)["status"] == "pass"
    capture = capture_dir(store, envelope["capture_id"])
    stored_envelope = json.loads((capture / "bundle" / "capture-envelope.json").read_text(encoding="utf-8"))
    stored_envelope["observation"]["content_type"]["detection_basis"] = "locator_hint"
    rewrite_envelope(capture, stored_envelope)
    result = store_verify_capture(store, envelope["capture_id"], expect=1)
    assert result["code"] == "BUNDLE_VALIDATION_FAILED"


def test_concurrent_same_put_is_idempotent(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, _envelope = make_bundle(tmp, "concurrent-same", [("repo/a.txt", b"a")])
    cmd = [
        sys.executable,
        str(STORE_TOOL),
        "put",
        "--store-root",
        str(store),
        "--bundle-dir",
        str(bundle),
        "--raw-blob",
        str(source),
    ]
    procs = [subprocess.Popen(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
    results = []
    for proc in procs:
        stdout, stderr = proc.communicate(timeout=30)
        if proc.returncode != 0:
            raise AssertionError(f"concurrent put failed\nstdout={stdout}\nstderr={stderr}")
        results.append(json.loads(stdout))
    assert sorted(item["result"] for item in results) == ["already_retained", "stored"]


def test_concurrent_conflicting_put_reports_conflict(tmp: Path) -> None:
    store = tmp / "store"
    assert store_init(store)["status"] == "pass"
    source, bundle, envelope = make_bundle(tmp, "concurrent-first", [("repo/a.txt", b"a")])
    source2, bundle2, _envelope2 = make_bundle(
        tmp,
        "concurrent-second",
        [("repo/b.txt", b"b")],
        "--capture-id",
        envelope["capture_id"],
    )
    commands = [
        [
            sys.executable,
            str(STORE_TOOL),
            "put",
            "--store-root",
            str(store),
            "--bundle-dir",
            str(bundle),
            "--raw-blob",
            str(source),
        ],
        [
            sys.executable,
            str(STORE_TOOL),
            "put",
            "--store-root",
            str(store),
            "--bundle-dir",
            str(bundle2),
            "--raw-blob",
            str(source2),
        ],
    ]
    procs = [subprocess.Popen(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for cmd in commands]
    results = []
    for proc in procs:
        stdout, stderr = proc.communicate(timeout=30)
        if proc.returncode not in {0, 1}:
            raise AssertionError(f"unexpected concurrent conflict return {proc.returncode}\nstdout={stdout}\nstderr={stderr}")
        results.append((proc.returncode, json.loads(stdout)))
    assert any(code == 0 and payload.get("result") == "stored" for code, payload in results)
    assert any(code == 1 and payload.get("code") == "CAPTURE_ID_CONFLICT" for code, payload in results)


def main() -> int:
    tests = [
        test_init_rejects_nonempty_without_store_json,
        test_put_retains_raw_blob_and_is_idempotent,
        test_put_without_raw_blob_records_not_retained,
        test_verify_store_empty_store_passes,
        test_verify_store_missing_referenced_blob_is_error,
        test_verify_store_rejects_corrupt_referenced_cas_blob,
        test_verify_store_output_argument_does_not_touch_store_or_symlink,
        test_verify_store_detects_cas_content_changed_during_scan,
        test_verify_store_detects_same_size_cas_change_with_mtime_restored,
        test_verify_store_detects_capture_content_changed_during_scan,
        test_verify_store_detects_same_size_capture_change_with_mtime_restored,
        test_verify_store_detects_store_json_changed_during_scan,
        test_verify_store_detects_store_json_change_with_mtime_restored,
        test_verify_store_detects_store_json_changed_during_load_store_window,
        test_verify_store_detects_unknown_root_entry_added_during_scan,
        test_verify_store_detects_unsupported_algorithm_added_during_scan,
        test_verify_store_reports_valid_orphan_cas_blob_as_warning,
        test_verify_store_rejects_corrupt_orphan_cas_blob,
        test_verify_store_rejects_capture_symlink,
        test_verify_store_rejects_cas_symlink,
        test_verify_store_rejects_extra_capture_file,
        test_verify_store_rejects_extra_validation_context_file,
        test_verify_store_rejects_extra_validation_context_directory,
        test_verify_store_rejects_unknown_store_root_entry,
        test_verify_store_reports_malformed_store_json,
        test_verify_store_reports_duplicate_key_store_json,
        test_verify_store_reports_missing_store_json_field,
        test_verify_store_reports_capture_directory_io_shape_error,
        test_verify_store_rejects_missing_receipt,
        test_verify_store_reports_malformed_receipt,
        test_verify_store_reports_duplicate_key_receipt,
        test_verify_store_report_schema_accepts_unicode_invalid_entry,
        test_verify_store_report_schema_accepts_backslash_and_control_encoding,
        test_verify_store_report_contains_no_absolute_store_path,
        test_verify_store_continues_after_one_invalid_capture,
        test_verify_store_nonempty_staging_is_indeterminate,
        test_verify_store_detects_capture_added_during_scan,
        test_raw_blob_mismatch_does_not_create_capture,
        test_capture_id_conflict_is_not_overwritten,
        test_existing_corrupt_cas_blob_is_rejected,
        test_verify_capture_detects_tampering,
        test_store_root_parent_symlink_is_rejected,
        test_cas_prefix_symlink_is_rejected,
        test_verify_capture_rejects_policy_not_pinned_by_implementation,
        test_verify_capture_replays_policy_listed_warning,
        test_verify_capture_rejects_fake_validation_context_paths,
        test_verify_capture_rejects_noncanonical_raw_store_path,
        test_verify_capture_rejects_tree_pdf_magic_tamper,
        test_verify_capture_rejects_tampered_max_findings_per_code,
        test_verify_capture_rejects_not_comparable_hint_match,
        test_verify_capture_rejects_locator_hint_basis,
        test_concurrent_same_put_is_idempotent,
        test_concurrent_conflicting_put_reports_conflict,
    ]
    with tempfile.TemporaryDirectory(prefix="vaks-source-capture-store-test-") as tmp_raw:
        tmp = Path(tmp_raw)
        for test in tests:
            case_dir = tmp / test.__name__
            if case_dir.exists():
                shutil.rmtree(case_dir)
            case_dir.mkdir()
            test(case_dir)
    print(json.dumps({"passed": len(tests), "tests": [test.__name__ for test in tests]}, allow_nan=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
