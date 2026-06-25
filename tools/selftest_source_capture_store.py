#!/usr/bin/env python
"""Self-test Source Capture Store v1 PR-B1 behavior."""

from __future__ import annotations

import json
import os
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
sys.path.insert(0, str(ROOT / "tools"))
import store_source_capture  # noqa: E402
import validate_source_capture_bundle  # noqa: E402


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


def capture_dir(store: Path, capture_id: str) -> Path:
    return store / "captures" / capture_id.split("urn:uuid:", 1)[1].lower()


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
