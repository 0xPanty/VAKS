#!/usr/bin/env python
"""Self-test VAKS Source Capture Envelope v1 inspector invariants."""

from __future__ import annotations

import json
import io
import os
import stat
import struct
import tempfile
import tarfile
import warnings
import zipfile
import zlib
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Any

import inspect_source_snapshot
import validate_source_capture_bundle


def write_zip(path: Path, entries: list[tuple[str, bytes]], *, reverse: bool = False, year: int = 2026) -> None:
    ordered = list(reversed(entries)) if reverse else entries
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, data in ordered:
            info = zipfile.ZipInfo(name)
            info.date_time = (year, 1, 1, 0, 0, 0)
            zf.writestr(info, data)


def write_tar(path: Path, entries: list[tuple[str, bytes]]) -> None:
    with tarfile.open(path, "w") as tf:
        for name, data in entries:
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mode = 0o644
            tf.addfile(info, io.BytesIO(data))


def write_zip_infos(path: Path, entries: list[tuple[zipfile.ZipInfo, bytes]]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as zf:
        for info, data in entries:
            zf.writestr(info, data)


def long_manifest_paths(count: int) -> list[tuple[str, bytes]]:
    return [(f"{idx:04d}-{'a' * 261}", b"a") for idx in range(count)]


def write_zip_with_compression(path: Path, entries: list[tuple[str, bytes]], compression: int) -> None:
    with zipfile.ZipFile(path, "w", compression=compression) as zf:
        for name, data in entries:
            info = zipfile.ZipInfo(name)
            info.date_time = (2026, 1, 1, 0, 0, 0)
            zf.writestr(info, data, compress_type=compression)


def zip_info(name: str, mode: int = 0o100644) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name)
    info.date_time = (2026, 1, 1, 0, 0, 0)
    info.create_system = 3
    info.external_attr = mode << 16
    return info


def unicode_path_extra(raw_name: bytes, unicode_name: str) -> bytes:
    payload = bytes([1]) + struct.pack("<I", zlib.crc32(raw_name) & 0xFFFFFFFF) + unicode_name.encode("utf-8")
    return struct.pack("<HH", 0x7075, len(payload)) + payload


def write_raw_zip(
    path: Path,
    entries: list[tuple[bytes, bytes]],
    *,
    flag_bits: int = 0,
    create_system: int = 3,
    external_attr: int = 0,
    extra: bytes = b"",
) -> None:
    local_parts: list[bytes] = []
    central_parts: list[bytes] = []
    offset = 0
    version_made_by = (create_system << 8) | 20
    for name, data in entries:
        crc = zlib.crc32(data) & 0xFFFFFFFF
        local = struct.pack(
            "<IHHHHHIIIHH",
            0x04034B50,
            20,
            flag_bits,
            0,
            0,
            0,
            crc,
            len(data),
            len(data),
            len(name),
            len(extra),
        ) + name + extra + data
        central = struct.pack(
            "<IHHHHHHIIIHHHHHII",
            0x02014B50,
            version_made_by,
            20,
            flag_bits,
            0,
            0,
            0,
            crc,
            len(data),
            len(data),
            len(name),
            len(extra),
            0,
            0,
            0,
            external_attr,
            offset,
        ) + name + extra
        local_parts.append(local)
        central_parts.append(central)
        offset += len(local)
    central_dir = b"".join(central_parts)
    eocd = struct.pack("<IHHHHIIH", 0x06054B50, 0, 0, len(entries), len(entries), len(central_dir), offset, 0)
    path.write_bytes(b"".join(local_parts) + central_dir + eocd)


def raw_deflate(data: bytes) -> bytes:
    compressor = zlib.compressobj(level=6, wbits=-15)
    return compressor.compress(data) + compressor.flush()


def write_malformed_zip_single(
    path: Path,
    *,
    name: bytes = b"repo/a.txt",
    payload: bytes = b"safe",
    central_payload_size: int | None = None,
    central_file_size: int | None = None,
    local_payload_size: int | None = None,
    local_file_size: int | None = None,
    central_crc: int | None = None,
    local_crc: int | None = None,
    central_method: int = 0,
    local_method: int | None = None,
    central_flags: int = 0,
    local_flags: int | None = None,
    create_system: int = 3,
) -> None:
    local_method = central_method if local_method is None else local_method
    local_flags = central_flags if local_flags is None else local_flags
    central_payload_size = len(payload) if central_payload_size is None else central_payload_size
    local_payload_size = central_payload_size if local_payload_size is None else local_payload_size
    central_file_size = len(payload) if central_file_size is None else central_file_size
    local_file_size = central_file_size if local_file_size is None else local_file_size
    central_crc = zlib.crc32(payload) & 0xFFFFFFFF if central_crc is None else central_crc
    local_crc = central_crc if local_crc is None else local_crc
    local = struct.pack(
        "<IHHHHHIIIHH",
        0x04034B50,
        20,
        local_flags,
        local_method,
        0,
        0,
        local_crc,
        local_payload_size,
        local_file_size,
        len(name),
        0,
    ) + name + payload
    version_made_by = (create_system << 8) | 20
    central = struct.pack(
        "<IHHHHHHIIIHHHHHII",
        0x02014B50,
        version_made_by,
        20,
        central_flags,
        central_method,
        0,
        0,
        central_crc,
        central_payload_size,
        central_file_size,
        len(name),
        0,
        0,
        0,
        0,
        0,
        0,
    ) + name
    eocd = struct.pack("<IHHHHIIH", 0x06054B50, 0, 0, 1, 1, len(central), len(local), 0)
    path.write_bytes(local + central + eocd)


def run_inspector(input_path: Path, out_dir: Path, *extra: str) -> dict[str, Any]:
    capture_id = "urn:uuid:00000000-0000-4000-8000-000000000001"
    args = [
        str(input_path),
        "--out",
        str(out_dir),
        "--capture-id",
        capture_id,
        "--observed-at",
        "2026-06-23T00:00:00Z",
        "--source-id",
        "vsrc:1:repo:github.com/example/repo",
        "--source-kind",
        "repo",
        "--capture-method",
        "provider_archive",
        *extra,
    ]
    with redirect_stdout(io.StringIO()):
        rc = inspect_source_snapshot.main(args)
    assert rc == 0
    return {
        "out_dir": out_dir,
        "envelope": json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8")),
        "manifest_lines": (out_dir / "snapshot-manifest.jsonl").read_text(encoding="utf-8").splitlines(),
        "hygiene": json.loads((out_dir / "snapshot-hygiene.intoto.json").read_text(encoding="utf-8")),
        "bundle_validation": validate_source_capture_bundle.validate_bundle(out_dir),
    }


def finding_codes(result: dict[str, Any]) -> set[str]:
    return {item["code"] for item in result["hygiene"]["predicate"]["findings"]}


def write_json(path: Path, obj: dict[str, Any]) -> bytes:
    data = (json.dumps(obj, allow_nan=False, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    path.write_bytes(data)
    return data


def rebind_hygiene_ref(out_dir: Path, envelope: dict[str, Any], hygiene: dict[str, Any]) -> None:
    hygiene_bytes = write_json(out_dir / "snapshot-hygiene.intoto.json", hygiene)
    envelope["inspection_refs"][0]["size"] = len(hygiene_bytes)
    envelope["inspection_refs"][0]["digest"] = inspect_source_snapshot.digest_bytes(hygiene_bytes)
    write_json(out_dir / "capture-envelope.json", envelope)


def rewrite_hygiene_findings(out_dir: Path, findings: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    hygiene = json.loads((out_dir / "snapshot-hygiene.intoto.json").read_text(encoding="utf-8"))
    hygiene["predicate"]["findings"] = findings
    hygiene["predicate"]["summary"] = {
        "finding_count": len(findings),
        "max_severity": validate_source_capture_bundle.computed_max_severity(findings),
    }
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    return envelope, hygiene


def assert_enterprise_validator_rejects(out_dir: Path, expected: str) -> None:
    try:
        validate_source_capture_bundle.validate_bundle(
            out_dir,
            profile="enterprise-alpha1",
            policy_file=inspect_source_snapshot.default_policy_path(),
        )
    except validate_source_capture_bundle.ValidationError as exc:
        assert expected in str(exc), str(exc)
    else:
        raise AssertionError(f"enterprise-alpha1 must reject bundle: {expected}")


def write_manifest_rows(out_dir: Path, rows: list[dict[str, Any]]) -> bytes:
    data = ("\n".join(inspect_source_snapshot.json_line(row) for row in rows) + "\n").encode("utf-8")
    (out_dir / "snapshot-manifest.jsonl").write_bytes(data)
    return data


def rebind_tree_manifest(out_dir: Path, rows: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest_bytes = write_manifest_rows(out_dir, rows)
    manifest_digest = inspect_source_snapshot.digest_bytes(manifest_bytes)
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    hygiene = json.loads((out_dir / "snapshot-hygiene.intoto.json").read_text(encoding="utf-8"))
    envelope["snapshot"]["kind"] = "tree"
    envelope["snapshot"]["snapshot_id"] = "vsnap:1:tree:" + manifest_digest
    envelope["snapshot"]["manifest"] = {
        "media_type": "application/vnd.vaks.snapshot-manifest.v1+jsonl",
        "size": len(manifest_bytes),
        "digest": manifest_digest,
    }
    hygiene["subject"][0]["name"] = "snapshot-manifest"
    hygiene["subject"][0]["digest"]["sha256"] = manifest_digest.split(":", 1)[1]
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    return envelope, hygiene


def test_clean_archive(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/README.md", b"hello\n"), ("repo/src/app.py", b"print('x')\n")])
    result = run_inspector(archive, tmp / "out-clean")
    envelope = result["envelope"]
    assert envelope["raw_handling"]["disposition"] == "admitted"
    assert envelope["snapshot"]["kind"] == "tree"
    assert envelope["fidelity"]["state"] == "not_checked"
    assert envelope["change"]["state"] == "unknown"
    assert envelope["change"]["compared_to_capture_id"] is None
    assert envelope["source"]["requested_locator"] == "clean.zip"
    assert "resolved_locator" not in envelope["source"]
    assert result["hygiene"]["predicate"]["summary"]["finding_count"] == 0


def test_repo_requires_explicit_source_id(tmp: Path) -> None:
    archive = tmp / "repo.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    args = [str(archive), "--out", str(tmp / "out"), "--source-kind", "repo"]
    try:
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            inspect_source_snapshot.main(args)
    except SystemExit as exc:
        assert exc.code == 2
        return
    raise AssertionError("repo/web/video captures should require explicit source_id unless fallback is allowed")


def expect_bundle_validation_error(out_dir: Path) -> None:
    try:
        validate_source_capture_bundle.validate_bundle(out_dir)
    except validate_source_capture_bundle.ValidationError:
        return
    raise AssertionError("bundle validator should fail closed")


def test_bundle_rejects_same_snapshot_without_previous(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-change")
    out_dir = result["out_dir"]
    envelope_path = out_dir / "capture-envelope.json"
    envelope = result["envelope"]
    envelope["change"]["state"] = "same_snapshot"
    envelope["change"]["compared_to_capture_id"] = None
    envelope_path.write_text(json.dumps(envelope, allow_nan=False, sort_keys=True), encoding="utf-8")
    expect_bundle_validation_error(out_dir)


def test_bundle_rejects_fake_fidelity_match(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-fidelity")
    out_dir = result["out_dir"]
    envelope_path = out_dir / "capture-envelope.json"
    envelope = result["envelope"]
    envelope["fidelity"] = {"state": "matched"}
    envelope_path.write_text(json.dumps(envelope, allow_nan=False, sort_keys=True), encoding="utf-8")
    expect_bundle_validation_error(out_dir)


def test_bundle_rejects_bad_revision_kind(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-revision", "--revision-kind", "git_commit", "--revision-value", "abc")
    out_dir = result["out_dir"]
    envelope_path = out_dir / "capture-envelope.json"
    envelope = result["envelope"]
    envelope["resolution"]["revision"]["kind"] = "whatever"
    envelope_path.write_text(json.dumps(envelope, allow_nan=False, sort_keys=True), encoding="utf-8")
    expect_bundle_validation_error(out_dir)


def test_bundle_rejects_multiple_hygiene_subjects(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-hygiene-subject")
    out_dir = result["out_dir"]
    hygiene_path = out_dir / "snapshot-hygiene.intoto.json"
    hygiene = result["hygiene"]
    hygiene["subject"].append(hygiene["subject"][0])
    hygiene_path.write_text(json.dumps(hygiene, allow_nan=False, sort_keys=True), encoding="utf-8")
    expect_bundle_validation_error(out_dir)


def test_same_tree_different_zip_metadata(tmp: Path) -> None:
    entries = [("repo/a.txt", b"a"), ("repo/b.txt", b"b")]
    first = tmp / "first.zip"
    second = tmp / "second.zip"
    write_zip(first, entries, reverse=False, year=2026)
    write_zip(second, entries, reverse=True, year=2027)
    r1 = run_inspector(first, tmp / "out-first")
    r2 = run_inspector(second, tmp / "out-second")
    assert r1["envelope"]["snapshot"]["snapshot_id"] == r2["envelope"]["snapshot"]["snapshot_id"]
    assert r1["envelope"]["observation"]["blob"]["digest"] != r2["envelope"]["observation"]["blob"]["digest"]


def test_same_tree_different_zip_compression(tmp: Path) -> None:
    entries = [("repo/a.txt", b"a" * 1024), ("repo/b.txt", b"b" * 1024)]
    first = tmp / "stored.zip"
    second = tmp / "deflated.zip"
    write_zip_with_compression(first, entries, zipfile.ZIP_STORED)
    write_zip_with_compression(second, entries, zipfile.ZIP_DEFLATED)
    r1 = run_inspector(first, tmp / "out-stored")
    r2 = run_inspector(second, tmp / "out-deflated")
    assert r1["envelope"]["snapshot"]["snapshot_id"] == r2["envelope"]["snapshot"]["snapshot_id"]
    assert r1["envelope"]["observation"]["blob"]["digest"] != r2["envelope"]["observation"]["blob"]["digest"]


def test_hygiene_deterministic_across_entry_order(tmp: Path) -> None:
    entries = [("repo/TAG.SQL", b"upper"), ("repo/TAG.sql", b"lower"), ("repo/CON/readme.md", b"reserved")]
    first = tmp / "findings-first.zip"
    second = tmp / "findings-second.zip"
    write_zip(first, entries, reverse=False, year=2026)
    write_zip(second, entries, reverse=True, year=2027)
    r1 = run_inspector(first, tmp / "out-hygiene-first")
    r2 = run_inspector(second, tmp / "out-hygiene-second")
    h1 = (r1["out_dir"] / "snapshot-hygiene.intoto.json").read_bytes()
    h2 = (r2["out_dir"] / "snapshot-hygiene.intoto.json").read_bytes()
    assert r1["envelope"]["snapshot"]["snapshot_id"] == r2["envelope"]["snapshot"]["snapshot_id"]
    assert h1 == h2


def test_case_collision_preserved(tmp: Path) -> None:
    archive = tmp / "case.zip"
    write_zip(archive, [("repo/TAG.SQL", b"upper"), ("repo/TAG.sql", b"lower")])
    result = run_inspector(archive, tmp / "out-case")
    assert result["envelope"]["raw_handling"]["disposition"] == "admitted"
    assert "PATH_CASE_COLLISION" in finding_codes(result)
    manifest = "\n".join(result["manifest_lines"])
    assert '"path":"TAG.SQL"' in manifest
    assert '"path":"TAG.sql"' in manifest


def test_duplicate_entry_quarantined(tmp: Path) -> None:
    archive = tmp / "dupe.zip"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        write_zip(archive, [("repo/dup.txt", b"one"), ("repo/dup.txt", b"two")])
    result = run_inspector(archive, tmp / "out-dupe")
    assert "ARCHIVE_DUPLICATE_ENTRY" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"
    assert result["envelope"]["snapshot"]["kind"] == "blob"
    assert '"state":"unavailable"' in result["manifest_lines"][0]


def test_entry_size_limit_uses_entry_code(tmp: Path) -> None:
    archive = tmp / "entry-limit.zip"
    write_zip(archive, [("repo/big.txt", b"abc")])
    result = run_inspector(archive, tmp / "out-entry-limit", "--max-entry-size", "1")
    codes = finding_codes(result)
    assert "ARCHIVE_ENTRY_SIZE_LIMIT_EXCEEDED" in codes
    assert "ARCHIVE_TOTAL_SIZE_LIMIT_EXCEEDED" not in codes
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_path_traversal_quarantined(tmp: Path) -> None:
    archive = tmp / "traversal.zip"
    write_zip(archive, [("../evil.txt", b"bad")])
    result = run_inspector(archive, tmp / "out-traversal")
    assert "ARCHIVE_PATH_TRAVERSAL" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_portability_and_completeness_findings(tmp: Path) -> None:
    archive = tmp / "portability.zip"
    lfs = b"version https://git-lfs.github.com/spec/v1\noid sha256:" + (b"1" * 64) + b"\nsize 1\n"
    write_zip(
        archive,
        [
            ("repo/CON/readme.md", b"reserved"),
            ("repo/name./file.txt", b"trailing"),
            ("repo/.gitmodules", b"[submodule]\n"),
            ("repo/asset.bin", lfs),
        ],
    )
    result = run_inspector(archive, tmp / "out-portability")
    codes = finding_codes(result)
    assert "PATH_WINDOWS_RESERVED_NAME" in codes
    assert "PATH_WINDOWS_TRAILING_DOT_OR_SPACE" in codes
    assert "REPO_SUBMODULE_PRESENT" in codes
    assert "REPO_LFS_POINTER_PRESENT" in codes
    assert result["envelope"]["raw_handling"]["disposition"] == "admitted"


def test_clean_tar_archive(tmp: Path) -> None:
    archive = tmp / "clean.tar"
    write_tar(archive, [("repo/README.md", b"hello\n"), ("repo/docs/a.md", b"a\n")])
    result = run_inspector(archive, tmp / "out-tar")
    assert result["envelope"]["raw_handling"]["disposition"] == "admitted"
    assert result["envelope"]["snapshot"]["kind"] == "tree"
    assert result["hygiene"]["predicate"]["summary"]["finding_count"] == 0


def test_single_file_blob_snapshot(tmp: Path) -> None:
    source = tmp / "asset.bin"
    source.write_bytes(b"version https://git-lfs.github.com/spec/v1\noid sha256:" + (b"2" * 64) + b"\nsize 2\n")
    result = run_inspector(source, tmp / "out-file", "--source-kind", "file", "--capture-method", "local_file")
    assert result["envelope"]["raw_handling"]["disposition"] == "admitted"
    assert result["envelope"]["snapshot"]["kind"] == "blob"
    assert result["hygiene"]["predicateType"] == "urn:vaks:predicate:source-snapshot-hygiene:v1"
    assert result["hygiene"]["predicate"]["profiles"] == ["source-fixity/v1"]
    assert "REPO_LFS_POINTER_PRESENT" not in finding_codes(result)


def test_symlink_target_limit_quarantined(tmp: Path) -> None:
    archive = tmp / "symlink-long.zip"
    info = zip_info("repo/link", stat.S_IFLNK | 0o777)
    write_zip_infos(archive, [(info, b"a" * 5000)])
    result = run_inspector(archive, tmp / "out-symlink")
    assert "ARCHIVE_SYMLINK_TARGET_LIMIT_EXCEEDED" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"
    assert result["envelope"]["snapshot"]["kind"] == "blob"


def test_symlink_invalid_utf8_quarantined(tmp: Path) -> None:
    archive = tmp / "symlink-invalid-utf8.zip"
    info = zip_info("repo/link", stat.S_IFLNK | 0o777)
    write_zip_infos(archive, [(info, b"\xff")])
    result = run_inspector(archive, tmp / "out-symlink-invalid")
    assert "ARCHIVE_SYMLINK_TARGET_INVALID_UTF8" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_symlink_escape_quarantined(tmp: Path) -> None:
    archive = tmp / "symlink-escape.zip"
    info = zip_info("repo/link", stat.S_IFLNK | 0o777)
    write_zip_infos(archive, [(info, b"../evil")])
    result = run_inspector(archive, tmp / "out-symlink-escape")
    assert "ARCHIVE_SYMLINK_ESCAPE" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_zip_special_file_quarantined(tmp: Path) -> None:
    archive = tmp / "special.zip"
    info = zip_info("repo/fifo", stat.S_IFIFO | 0o644)
    write_zip_infos(archive, [(info, b"")])
    result = run_inspector(archive, tmp / "out-special")
    assert "ARCHIVE_SPECIAL_FILE" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_tar_hardlink_quarantined(tmp: Path) -> None:
    archive = tmp / "hardlink.tar"
    with tarfile.open(archive, "w") as tf:
        info = tarfile.TarInfo("repo/base.txt")
        data = b"base"
        info.size = len(data)
        tf.addfile(info, io.BytesIO(data))
        link = tarfile.TarInfo("repo/link.txt")
        link.type = tarfile.LNKTYPE
        link.linkname = "repo/base.txt"
        tf.addfile(link)
    result = run_inspector(archive, tmp / "out-hardlink")
    assert "ARCHIVE_SPECIAL_FILE" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_backslash_traversal_quarantined(tmp: Path) -> None:
    findings: list[inspect_source_snapshot.Finding] = []
    inspect_source_snapshot.canonical_archive_path(r"repo\..\evil.txt", findings)
    inspect_source_snapshot.check_path_hygiene(r"repo\..\evil.txt", findings, inspect_source_snapshot.Limits())
    codes = {finding.code for finding in findings}
    assert "ARCHIVE_BACKSLASH_PATH" in codes
    assert "ARCHIVE_PATH_TRAVERSAL" in codes


def test_corrupt_archive_quarantined(tmp: Path) -> None:
    archive = tmp / "corrupt.zip"
    archive.write_bytes(b"not a real zip")
    result = run_inspector(archive, tmp / "out-corrupt", "--input-profile", "archive")
    assert "ARCHIVE_PARSE_FAILED" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"
    assert result["envelope"]["snapshot"]["kind"] == "blob"


def test_dot_segment_quarantined(tmp: Path) -> None:
    archive = tmp / "dot.zip"
    write_zip(archive, [("repo/a.txt", b"one"), ("repo/./a.txt", b"two")])
    result = run_inspector(archive, tmp / "out-dot")
    assert "ARCHIVE_DOT_OR_EMPTY_SEGMENT" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_ancestor_prefix_conflict_quarantined(tmp: Path) -> None:
    archive = tmp / "ancestor.zip"
    write_zip(archive, [("repo/a", b"file"), ("repo/a/b", b"child")])
    result = run_inspector(archive, tmp / "out-ancestor")
    assert "ARCHIVE_ANCESTOR_PREFIX_CONFLICT" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_non_executable_mode_does_not_change_snapshot(tmp: Path) -> None:
    first = tmp / "mode-0644.zip"
    second = tmp / "mode-0600.zip"
    write_zip_infos(first, [(zip_info("repo/a.txt", stat.S_IFREG | 0o644), b"same")])
    write_zip_infos(second, [(zip_info("repo/a.txt", stat.S_IFREG | 0o600), b"same")])
    r1 = run_inspector(first, tmp / "out-0644")
    r2 = run_inspector(second, tmp / "out-0600")
    assert r1["envelope"]["snapshot"]["snapshot_id"] == r2["envelope"]["snapshot"]["snapshot_id"]


def test_existing_output_dir_refused(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    out_dir = tmp / "out-existing"
    out_dir.mkdir()
    (out_dir / "capture-envelope.json").write_text("existing", encoding="utf-8")
    try:
        run_inspector(archive, out_dir)
    except FileExistsError:
        return
    raise AssertionError("inspector should refuse non-empty output directory")


def test_media_type_for_compound_suffixes(tmp: Path) -> None:
    assert inspect_source_snapshot.media_type_for(tmp / "archive.tar.gz") == "application/gzip"
    assert inspect_source_snapshot.media_type_for(tmp / "plain.gz") == "application/gzip"
    assert inspect_source_snapshot.media_type_for(tmp / "archive.tar") == "application/x-tar"
    assert inspect_source_snapshot.media_type_for(tmp / "doc.pdf") == "application/pdf"


def test_unhandled_inspection_exception_structured_failed(tmp: Path) -> None:
    archive = tmp / "boom.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    original = inspect_source_snapshot.read_zip_entries

    def boom(*args: Any, **kwargs: Any) -> tuple[list[Any], int]:
        raise AssertionError("forced failure")

    inspect_source_snapshot.read_zip_entries = boom  # type: ignore[assignment]
    try:
        result = run_inspector(archive, tmp / "out-boom")
    finally:
        inspect_source_snapshot.read_zip_entries = original  # type: ignore[assignment]
    assert "SCANNER_UNHANDLED_EXCEPTION" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"
    assert result["hygiene"]["predicate"]["execution_state"] == "failed"


def test_input_change_during_scan_quarantined(tmp: Path) -> None:
    archive = tmp / "changing.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    original = inspect_source_snapshot.read_zip_entries

    def changing(path: Path, *args: Any, **kwargs: Any) -> tuple[list[Any], int]:
        entries, total = original(path, *args, **kwargs)
        path.write_bytes(path.read_bytes() + b"changed")
        return entries, total

    inspect_source_snapshot.read_zip_entries = changing  # type: ignore[assignment]
    try:
        result = run_inspector(archive, tmp / "out-changing")
    finally:
        inspect_source_snapshot.read_zip_entries = original  # type: ignore[assignment]
    assert "CAPTURE_INPUT_CHANGED_DURING_SCAN" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_original_input_aba_does_not_affect_temp_snapshot(tmp: Path) -> None:
    archive = tmp / "aba.zip"
    write_zip(archive, [("repo/A.txt", b"a")])
    replacement = tmp / "replacement.zip"
    write_zip(replacement, [("repo/B.txt", b"b")])
    replacement_bytes = replacement.read_bytes()
    original = inspect_source_snapshot.inspect_path

    def replace_original(path: Path, *args: Any, **kwargs: Any) -> inspect_source_snapshot.InspectionResult:
        display_path = kwargs.get("display_path")
        if isinstance(display_path, Path):
            display_path.write_bytes(replacement_bytes)
        return original(path, *args, **kwargs)

    inspect_source_snapshot.inspect_path = replace_original  # type: ignore[assignment]
    try:
        result = run_inspector(archive, tmp / "out-aba")
    finally:
        inspect_source_snapshot.inspect_path = original  # type: ignore[assignment]
    manifest = "\n".join(result["manifest_lines"])
    assert '"path":"A.txt"' in manifest
    assert '"path":"B.txt"' not in manifest
    assert result["envelope"]["raw_handling"]["disposition"] == "admitted"


def test_zip_directory_marker_symlink_collision_quarantined(tmp: Path) -> None:
    archive = tmp / "zip-type-confusion.zip"
    info = zip_info("repo/link/", stat.S_IFLNK | 0o777)
    write_zip_infos(archive, [(info, b"../evil")])
    result = run_inspector(archive, tmp / "out-zip-type-confusion")
    assert "ARCHIVE_TYPE_COLLISION" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_output_parent_symlink_refused(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    real_parent = tmp / "real-parent"
    real_parent.mkdir()
    link_parent = tmp / "link-parent"
    try:
        os.symlink(real_parent, link_parent, target_is_directory=True)
    except (OSError, NotImplementedError):
        return
    try:
        run_inspector(archive, link_parent / "child")
    except FileExistsError:
        return
    raise AssertionError("inspector should refuse symlink output path components")


def test_cli_rejects_invalid_change_and_limits(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    bad_cases = [
        ["--change-state", "same_snapshot"],
        ["--revision-kind", "git_commit"],
        ["--max-compression-ratio", "nan"],
        ["--max-compression-ratio", "inf"],
        ["--max-compression-ratio", "0"],
        ["--max-entry-size", "0"],
    ]
    for idx, extra in enumerate(bad_cases):
        args = [
            str(archive),
            "--out",
            str(tmp / f"out-bad-cli-{idx}"),
            "--source-id",
            "vsrc:1:repo:github.com/example/repo",
            "--source-kind",
            "repo",
            *extra,
        ]
        try:
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                inspect_source_snapshot.main(args)
        except SystemExit as exc:
            assert exc.code == 2
            continue
        raise AssertionError(f"invalid CLI arguments should fail fast: {extra}")


def test_input_copy_failure_creates_no_bundle(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    out_dir = tmp / "out-copy-fail"
    original = inspect_source_snapshot.materialize_input_copy

    def fail_copy(path: Path, max_input_blob_size: int) -> inspect_source_snapshot.MaterializedInput:
        raise PermissionError("forced unreadable source")

    inspect_source_snapshot.materialize_input_copy = fail_copy  # type: ignore[assignment]
    try:
        with redirect_stdout(io.StringIO()):
            rc = inspect_source_snapshot.main(
                [
                    str(archive),
                    "--out",
                    str(out_dir),
                    "--source-id",
                    "vsrc:1:repo:github.com/example/repo",
                    "--source-kind",
                    "repo",
                ]
            )
    finally:
        inspect_source_snapshot.materialize_input_copy = original  # type: ignore[assignment]
    assert rc == 3
    assert not out_dir.exists()


def test_empty_zip_is_valid_empty_tree(tmp: Path) -> None:
    archive = tmp / "empty.zip"
    with zipfile.ZipFile(archive, "w"):
        pass
    result = run_inspector(archive, tmp / "out-empty")
    assert result["envelope"]["snapshot"]["kind"] == "tree"
    assert result["envelope"]["raw_handling"]["disposition"] == "admitted"
    assert result["manifest_lines"] == [
        '{"profile":"vaks-archive-tree/v1","schema":"urn:vaks:schema:snapshot-manifest:v1","state":"complete"}'
    ]


def test_bundle_rejects_dangerous_rebound_manifest_path(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-dangerous-manifest")
    out_dir = result["out_dir"]
    rows = [
        {"profile": "vaks-archive-tree/v1", "schema": "urn:vaks:schema:snapshot-manifest:v1", "state": "complete"},
        {"digest": "sha256:" + "1" * 64, "mode": "100644", "path": "../evil.txt", "size": 1, "type": "file"},
    ]
    rebind_tree_manifest(out_dir, rows)
    expect_bundle_validation_error(out_dir)


def test_bundle_rejects_unavailable_tree_admitted(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-unavailable-tree")
    out_dir = result["out_dir"]
    rows = [
        {
            "profile": "vaks-archive-tree/v1",
            "reason_codes": ["ARCHIVE_PARSE_FAILED"],
            "schema": "urn:vaks:schema:snapshot-manifest:v1",
            "state": "unavailable",
        }
    ]
    envelope, hygiene = rebind_tree_manifest(out_dir, rows)
    envelope["raw_handling"]["disposition"] = "admitted"
    envelope["raw_handling"]["reason_codes"] = ["ARCHIVE_PARSE_FAILED"]
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    expect_bundle_validation_error(out_dir)


def test_bundle_rejects_blob_with_complete_tree_manifest(tmp: Path) -> None:
    source = tmp / "asset.bin"
    source.write_bytes(b"blob")
    result = run_inspector(source, tmp / "out-blob-tree-manifest", "--source-kind", "file", "--capture-method", "local_file")
    out_dir = result["out_dir"]
    rows = [
        {"profile": "vaks-archive-tree/v1", "schema": "urn:vaks:schema:snapshot-manifest:v1", "state": "complete"},
        {"digest": "sha256:" + "2" * 64, "mode": "100644", "path": "a.txt", "size": 1, "type": "file"},
    ]
    write_manifest_rows(out_dir, rows)
    expect_bundle_validation_error(out_dir)


def test_bundle_rejects_missing_producer_and_bad_severity(tmp: Path) -> None:
    archive = tmp / "case.zip"
    write_zip(archive, [("repo/TAG.SQL", b"upper"), ("repo/TAG.sql", b"lower")])
    result = run_inspector(archive, tmp / "out-schema-strict")
    out_dir = result["out_dir"]
    envelope = result["envelope"]
    del envelope["producer"]
    write_json(out_dir / "capture-envelope.json", envelope)
    expect_bundle_validation_error(out_dir)

    result = run_inspector(archive, tmp / "out-bad-severity")
    out_dir = result["out_dir"]
    envelope = result["envelope"]
    hygiene = result["hygiene"]
    hygiene["predicate"]["findings"][0]["severity"] = "critical"
    hygiene["predicate"]["summary"]["max_severity"] = "critical"
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    expect_bundle_validation_error(out_dir)


def test_symlink_empty_backslash_control_quarantined(tmp: Path) -> None:
    cases = [
        ("empty", b"", "ARCHIVE_SYMLINK_TARGET_EMPTY"),
        ("backslash", b"foo\\bar", "ARCHIVE_SYMLINK_TARGET_BACKSLASH"),
        ("control", b"foo\x01bar", "ARCHIVE_SYMLINK_TARGET_CONTROL_CHARACTER"),
    ]
    for name, target, code in cases:
        archive = tmp / f"symlink-{name}.zip"
        info = zip_info("repo/link", stat.S_IFLNK | 0o777)
        write_zip_infos(archive, [(info, target)])
        result = run_inspector(archive, tmp / f"out-symlink-{name}")
        assert code in finding_codes(result)
        assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"
        assert result["bundle_validation"]["status"] == "pass"


def test_path_control_character_quarantined(tmp: Path) -> None:
    archive = tmp / "path-control.zip"
    write_zip(archive, [("repo/bad\x01name.txt", b"bad")])
    result = run_inspector(archive, tmp / "out-path-control")
    assert "ARCHIVE_PATH_CONTROL_CHARACTER" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"
    assert result["bundle_validation"]["status"] == "pass"


def test_damaged_tbz_txz_archive_intent_quarantined(tmp: Path) -> None:
    for suffix in [".tbz", ".tbz2", ".txz"]:
        archive = tmp / f"bad{suffix}"
        archive.write_bytes(b"not a parseable archive")
        result = run_inspector(archive, tmp / f"out-bad-{suffix[1:]}", "--source-kind", "archive")
        assert "ARCHIVE_PARSE_FAILED" in finding_codes(result)
        assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_bundle_rejects_remaining_state_matrix_bypasses(tmp: Path) -> None:
    source = tmp / "asset.bin"
    source.write_bytes(b"blob")
    result = run_inspector(source, tmp / "out-blob-noteval", "--source-kind", "file", "--capture-method", "local_file")
    out_dir = result["out_dir"]
    rows = [
        {"profile": "vaks-archive-tree/v1", "schema": "urn:vaks:schema:snapshot-manifest:v1", "state": "complete"},
        {"digest": "sha256:" + "3" * 64, "mode": "100644", "path": "a.txt", "size": 1, "type": "file"},
    ]
    write_manifest_rows(out_dir, rows)
    envelope = result["envelope"]
    envelope["raw_handling"]["disposition"] = "not_evaluated"
    write_json(out_dir / "capture-envelope.json", envelope)
    expect_bundle_validation_error(out_dir)

    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-tree-failed-observation")
    out_dir = result["out_dir"]
    envelope = result["envelope"]
    envelope["observation"]["state"] = "failed"
    write_json(out_dir / "capture-envelope.json", envelope)
    expect_bundle_validation_error(out_dir)

    result = run_inspector(archive, tmp / "out-tree-partial-hygiene")
    out_dir = result["out_dir"]
    envelope = result["envelope"]
    hygiene = result["hygiene"]
    hygiene["predicate"]["execution_state"] = "partial"
    hygiene["predicate"]["findings"] = [
        {
            "code": "SYNTHETIC_WARNING",
            "message": "Synthetic warning for state-matrix regression.",
            "profile": "archive-safety/v1",
            "severity": "warning",
        }
    ]
    hygiene["predicate"]["summary"] = {"finding_count": 1, "max_severity": "warning"}
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    expect_bundle_validation_error(out_dir)

    result = run_inspector(archive, tmp / "out-tree-wrong-subject")
    out_dir = result["out_dir"]
    envelope = result["envelope"]
    hygiene = result["hygiene"]
    hygiene["subject"][0]["name"] = "capture-blob"
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    expect_bundle_validation_error(out_dir)


def test_bundle_rejects_manifest_limit_bypasses(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-limit-depth")
    out_dir = result["out_dir"]
    deep_path = "/".join(f"d{i}" for i in range(101)) + "/a.txt"
    rows = [
        {"profile": "vaks-archive-tree/v1", "schema": "urn:vaks:schema:snapshot-manifest:v1", "state": "complete"},
        {"digest": "sha256:" + "4" * 64, "mode": "100644", "path": deep_path, "size": 1, "type": "file"},
    ]
    rebind_tree_manifest(out_dir, rows)
    expect_bundle_validation_error(out_dir)

    result = run_inspector(archive, tmp / "out-limit-symlink")
    out_dir = result["out_dir"]
    rows = [
        {"profile": "vaks-archive-tree/v1", "schema": "urn:vaks:schema:snapshot-manifest:v1", "state": "complete"},
        {"mode": "120000", "path": "link", "target": "a" * 4097, "type": "symlink"},
    ]
    rebind_tree_manifest(out_dir, rows)
    expect_bundle_validation_error(out_dir)


def test_tar_directory_payload_quarantined(tmp: Path) -> None:
    archive = tmp / "dir-payload.tar"
    with tarfile.open(archive, "w") as tf:
        directory = tarfile.TarInfo("repo/dir")
        directory.type = tarfile.DIRTYPE
        directory.size = 4
        tf.addfile(directory, io.BytesIO(b"evil"))
        info = tarfile.TarInfo("repo/a.txt")
        data = b"a"
        info.size = len(data)
        tf.addfile(info, io.BytesIO(data))
    result = run_inspector(archive, tmp / "out-dir-payload")
    assert "ARCHIVE_TYPE_COLLISION" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_bundle_rejects_type_schema_and_profile_bypasses(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-resolution-null")
    out_dir = result["out_dir"]
    envelope = result["envelope"]
    envelope["resolution"] = None
    write_json(out_dir / "capture-envelope.json", envelope)
    expect_bundle_validation_error(out_dir)

    result = run_inspector(archive, tmp / "out-bool-size")
    out_dir = result["out_dir"]
    envelope = result["envelope"]
    envelope["observation"]["blob"]["size"] = True
    write_json(out_dir / "capture-envelope.json", envelope)
    expect_bundle_validation_error(out_dir)

    result = run_inspector(archive, tmp / "out-bool-finding-count")
    out_dir = result["out_dir"]
    envelope = result["envelope"]
    hygiene = result["hygiene"]
    hygiene["predicate"]["summary"]["finding_count"] = False
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    expect_bundle_validation_error(out_dir)

    result = run_inspector(archive, tmp / "out-admitted-reason")
    out_dir = result["out_dir"]
    envelope = result["envelope"]
    envelope["raw_handling"]["reason_codes"] = ["SYNTHETIC_REASON"]
    write_json(out_dir / "capture-envelope.json", envelope)
    expect_bundle_validation_error(out_dir)

    result = run_inspector(archive, tmp / "out-archive-profile", "--source-kind", "archive")
    out_dir = result["out_dir"]
    envelope = result["envelope"]
    hygiene = result["hygiene"]
    hygiene["predicate"]["profiles"] = ["source-fixity/v1"]
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    expect_bundle_validation_error(out_dir)

    result = run_inspector(archive, tmp / "out-archive-method-profile", "--source-kind", "file", "--capture-method", "archive_file")
    assert "archive-safety/v1" in result["hygiene"]["predicate"]["profiles"]
    out_dir = result["out_dir"]
    envelope = result["envelope"]
    hygiene = result["hygiene"]
    hygiene["predicate"]["profiles"] = ["source-fixity/v1"]
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    expect_bundle_validation_error(out_dir)


def test_zip_repeated_trailing_separator_quarantined(tmp: Path) -> None:
    archive = tmp / "repeated-separator.zip"
    info = zip_info("repo/foo//", stat.S_IFDIR | 0o755)
    write_zip_infos(archive, [(info, b"")])
    result = run_inspector(archive, tmp / "out-repeated-separator")
    assert "ARCHIVE_EMPTY_PATH_SEGMENT" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_input_profile_blob_cannot_override_archive_intent(tmp: Path) -> None:
    archive = tmp / "bad.zip"
    archive.write_bytes(b"not a real zip")
    args = [
        str(archive),
        "--out",
        str(tmp / "out-blob-override"),
        "--source-id",
        "vsrc:1:archive:test",
        "--source-kind",
        "archive",
        "--capture-method",
        "archive_file",
        "--input-profile",
        "blob",
    ]
    try:
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            inspect_source_snapshot.main(args)
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("archive intent must not be downgraded by --input-profile blob")

    source = tmp / "asset.bin"
    source.write_bytes(b"blob")
    result = run_inspector(source, tmp / "out-archive-intent-blob", "--source-kind", "file", "--capture-method", "local_file")
    out_dir = result["out_dir"]
    envelope = result["envelope"]
    envelope["source"]["kind"] = "archive"
    envelope["observation"]["capture_method"] = "archive_file"
    write_json(out_dir / "capture-envelope.json", envelope)
    expect_bundle_validation_error(out_dir)


def test_input_profile_blob_can_force_local_file_blob(tmp: Path) -> None:
    archive = tmp / "force-blob.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(
        archive,
        tmp / "out-force-blob",
        "--source-kind",
        "file",
        "--capture-method",
        "local_file",
        "--input-profile",
        "blob",
        "--source-id",
        "vsrc:1:content:sha256:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
    )
    envelope = result["envelope"]
    content_type = envelope["observation"]["content_type"]
    assert envelope["snapshot"]["kind"] == "blob"
    assert envelope["raw_handling"]["disposition"] == "admitted"
    assert envelope["observation"]["blob"]["media_type"] == "application/octet-stream"
    assert content_type["detected_media_type"] == "application/octet-stream"
    assert content_type["detection_basis"] == "fallback"
    assert content_type["locator_hint_media_type"] == "application/zip"
    assert content_type["hint_match"] == "mismatch"
    assert "MEDIA_TYPE_HINT_MISMATCH" in finding_codes(result)
    validate_source_capture_bundle.validate_bundle(
        result["out_dir"],
        profile="enterprise-alpha1",
        policy_file=inspect_source_snapshot.default_policy_path(),
    )


def test_path_too_long_is_portability_warning_not_hard_failure(tmp: Path) -> None:
    archive = tmp / "long-path.zip"
    long_name = "a" * 261
    write_zip(archive, [(f"repo/{long_name}", b"a")])
    result = run_inspector(archive, tmp / "out-long-path")
    envelope = result["envelope"]
    assert envelope["snapshot"]["kind"] == "tree"
    assert envelope["raw_handling"]["disposition"] == "admitted"
    assert "PATH_TOO_LONG" in finding_codes(result)
    assert ("PATH_TOO_LONG", "warning") in {
        (item["code"], item["severity"]) for item in result["hygiene"]["predicate"]["findings"]
    }
    validate_source_capture_bundle.validate_bundle(
        result["out_dir"],
        profile="enterprise-alpha1",
        policy_file=inspect_source_snapshot.default_policy_path(),
    )


def test_bundle_rejects_unbound_path_too_long_warning(tmp: Path) -> None:
    archive = tmp / "long-path-unbound-warning.zip"
    long_name = "a" * 261
    write_zip(archive, [(f"repo/{long_name}", b"a")])
    result = run_inspector(archive, tmp / "out-long-path-unbound-warning")
    out_dir = result["out_dir"]
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    hygiene = json.loads((out_dir / "snapshot-hygiene.intoto.json").read_text(encoding="utf-8"))
    for finding in hygiene["predicate"]["findings"]:
        if finding["code"] == "PATH_TOO_LONG":
            finding["paths"] = ["short.txt"]
            break
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    try:
        validate_source_capture_bundle.validate_bundle(
            out_dir,
            profile="enterprise-alpha1",
            policy_file=inspect_source_snapshot.default_policy_path(),
        )
    except validate_source_capture_bundle.ValidationError as exc:
        assert "PATH_TOO_LONG" in str(exc) or "path length" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must bind PATH_TOO_LONG warnings to the over-limit manifest path")


def test_archive_path_hard_limit_is_structured_quarantine(tmp: Path) -> None:
    exact_limit_archive = tmp / "exact-limit-path.zip"
    exact_limit_path = "a" * inspect_source_snapshot.MAX_ARCHIVE_PATH_STRING_LENGTH
    write_zip(exact_limit_archive, [(exact_limit_path, b"a")])
    exact_result = run_inspector(exact_limit_archive, tmp / "out-exact-limit-path")
    assert exact_result["envelope"]["snapshot"]["kind"] == "tree"
    assert exact_result["envelope"]["raw_handling"]["disposition"] == "admitted"
    assert "PATH_TOO_LONG" in finding_codes(exact_result)
    validate_source_capture_bundle.validate_bundle(
        exact_result["out_dir"],
        profile="enterprise-alpha1",
        policy_file=inspect_source_snapshot.default_policy_path(),
    )

    over_limit_archive = tmp / "over-limit-path.zip"
    over_limit_path = "a" * (inspect_source_snapshot.MAX_ARCHIVE_PATH_STRING_LENGTH + 1)
    write_zip(over_limit_archive, [(over_limit_path, b"a")])
    over_result = run_inspector(over_limit_archive, tmp / "out-over-limit-path")
    assert over_result["envelope"]["snapshot"]["kind"] == "blob"
    assert over_result["envelope"]["raw_handling"]["disposition"] == "quarantined"
    assert "ARCHIVE_PATH_LENGTH_LIMIT_EXCEEDED" in finding_codes(over_result)
    path_limit_findings = [
        item
        for item in over_result["hygiene"]["predicate"]["findings"]
        if item["code"] == "ARCHIVE_PATH_LENGTH_LIMIT_EXCEEDED"
    ]
    assert path_limit_findings
    assert not path_limit_findings[0].get("paths")
    assert path_limit_findings[0]["details"]["path_length"] == len(over_limit_path)
    validate_source_capture_bundle.validate_bundle(
        over_result["out_dir"],
        profile="enterprise-alpha1",
        policy_file=inspect_source_snapshot.default_policy_path(),
    )

    near_zip_limit_archive = tmp / "near-zip-limit-path.zip"
    near_zip_limit_path = "a" * 65_000
    write_zip(near_zip_limit_archive, [(near_zip_limit_path, b"a")])
    near_result = run_inspector(near_zip_limit_archive, tmp / "out-near-zip-limit-path")
    assert near_result["envelope"]["snapshot"]["kind"] == "blob"
    assert near_result["envelope"]["raw_handling"]["disposition"] == "quarantined"
    assert "ARCHIVE_PATH_LENGTH_LIMIT_EXCEEDED" in finding_codes(near_result)
    validate_source_capture_bundle.validate_bundle(
        near_result["out_dir"],
        profile="enterprise-alpha1",
        policy_file=inspect_source_snapshot.default_policy_path(),
    )


def test_path_too_long_uses_root_stripped_manifest_path(tmp: Path) -> None:
    archive = tmp / "root-stripped-long-path.zip"
    final_path = "a" * 259
    write_zip(archive, [(f"r/{final_path}", b"a")])
    result = run_inspector(archive, tmp / "out-root-stripped-long-path")
    assert result["envelope"]["snapshot"]["kind"] == "tree"
    assert result["envelope"]["raw_handling"]["disposition"] == "admitted"
    assert "PATH_TOO_LONG" not in finding_codes(result)
    manifest_entries = [json.loads(line) for line in result["manifest_lines"][1:]]
    assert manifest_entries == [
        {
            "digest": "sha256:ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
            "mode": "100644",
            "path": final_path,
            "size": 1,
            "type": "file",
        }
    ]
    validate_source_capture_bundle.validate_bundle(
        result["out_dir"],
        profile="enterprise-alpha1",
        policy_file=inspect_source_snapshot.default_policy_path(),
    )


def test_quarantined_long_path_does_not_require_complete_manifest_binding(tmp: Path) -> None:
    archive = tmp / "pdf-long-path.zip"
    long_name = "a" * 261
    write_zip(archive, [(long_name, b"a")])
    result = run_inspector(
        archive,
        tmp / "out-pdf-long-path",
        "--source-kind",
        "pdf",
        "--capture-method",
        "upload",
        "--source-id",
        "vsrc:1:opaque:pdf-long-path-demo",
    )
    assert result["envelope"]["snapshot"]["kind"] == "blob"
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"
    assert "PATH_TOO_LONG" in finding_codes(result)
    assert "SOURCE_KIND_FORMAT_MISMATCH" in finding_codes(result)
    assert json.loads(result["manifest_lines"][0])["state"] == "unavailable"
    validate_source_capture_bundle.validate_bundle(
        result["out_dir"],
        profile="enterprise-alpha1",
        policy_file=inspect_source_snapshot.default_policy_path(),
    )


def assert_path_too_long_truncation_case(result: dict[str, Any], expected_truncated: int) -> None:
    assert result["envelope"]["snapshot"]["kind"] == "tree"
    assert result["envelope"]["raw_handling"]["disposition"] == "admitted"
    findings = result["hygiene"]["predicate"]["findings"]
    explicit = [item for item in findings if item["code"] == "PATH_TOO_LONG"]
    assert len(explicit) == 100
    markers = [item for item in findings if item["code"] == "HYGIENE_FINDINGS_TRUNCATED"]
    if expected_truncated:
        assert len(markers) == 1
        assert markers[0]["severity"] == "warning"
        assert markers[0]["details"]["truncated_by_code"]["PATH_TOO_LONG"] == expected_truncated
    else:
        assert not markers
    validate_source_capture_bundle.validate_bundle(
        result["out_dir"],
        profile="enterprise-alpha1",
        policy_file=inspect_source_snapshot.default_policy_path(),
    )


def test_path_too_long_truncation_marker_replays_zip(tmp: Path) -> None:
    zip_100 = tmp / "long-paths-100.zip"
    write_zip(zip_100, long_manifest_paths(100))
    assert_path_too_long_truncation_case(run_inspector(zip_100, tmp / "out-long-paths-100-zip"), 0)

    zip_101 = tmp / "long-paths-101.zip"
    write_zip(zip_101, long_manifest_paths(101))
    assert_path_too_long_truncation_case(run_inspector(zip_101, tmp / "out-long-paths-101-zip"), 1)

    zip_1000 = tmp / "long-paths-1000.zip"
    write_zip(zip_1000, long_manifest_paths(1000))
    assert_path_too_long_truncation_case(run_inspector(zip_1000, tmp / "out-long-paths-1000-zip"), 900)


def test_path_too_long_truncation_marker_replays_tar(tmp: Path) -> None:
    tar_101 = tmp / "long-paths-101.tar"
    write_tar(tar_101, long_manifest_paths(101))
    assert_path_too_long_truncation_case(run_inspector(tar_101, tmp / "out-long-paths-101-tar"), 1)

    tar_1000 = tmp / "long-paths-1000.tar"
    write_tar(tar_1000, long_manifest_paths(1000))
    assert_path_too_long_truncation_case(run_inspector(tar_1000, tmp / "out-long-paths-1000-tar"), 900)


def test_truncation_marker_cannot_hide_unsafe_code(tmp: Path) -> None:
    blob = tmp / "clean.txt"
    blob.write_bytes(b"clean")
    result = run_inspector(
        blob,
        tmp / "out-truncated-unsafe",
        "--source-kind",
        "file",
        "--capture-method",
        "local_file",
        "--source-id",
        "vsrc:1:content:sha256:3333333333333333333333333333333333333333333333333333333333333333",
    )
    marker = {
        "code": "HYGIENE_FINDINGS_TRUNCATED",
        "severity": "warning",
        "profile": "source-fixity/v1",
        "message": "Hygiene findings were truncated by deterministic report-size limits.",
        "details": {"truncated_by_code": {"ARCHIVE_PATH_TRAVERSAL": 1}},
    }
    rewrite_hygiene_findings(result["out_dir"], result["hygiene"]["predicate"]["findings"] + [marker])
    assert_enterprise_validator_rejects(result["out_dir"], "HYGIENE_FINDINGS_TRUNCATED")


def test_path_too_long_truncation_requires_explicit_prefix(tmp: Path) -> None:
    archive = tmp / "long-paths-101-missing-explicit.zip"
    write_zip(archive, long_manifest_paths(101))
    result = run_inspector(archive, tmp / "out-long-paths-101-missing-explicit")
    marker = {
        "code": "HYGIENE_FINDINGS_TRUNCATED",
        "severity": "warning",
        "profile": "source-fixity/v1",
        "message": "Hygiene findings were truncated by deterministic report-size limits.",
        "details": {"truncated_by_code": {"PATH_TOO_LONG": 101}},
    }
    findings = [item for item in result["hygiene"]["predicate"]["findings"] if item["code"] != "PATH_TOO_LONG"]
    findings = [item for item in findings if item["code"] != "HYGIENE_FINDINGS_TRUNCATED"] + [marker]
    rewrite_hygiene_findings(result["out_dir"], findings)
    assert_enterprise_validator_rejects(result["out_dir"], "HYGIENE_FINDINGS_TRUNCATED")


def test_truncation_rejects_tampered_max_findings_per_code(tmp: Path) -> None:
    archive = tmp / "long-paths-101-tampered-cap.zip"
    write_zip(archive, long_manifest_paths(101))
    result = run_inspector(archive, tmp / "out-long-paths-101-tampered-cap")
    out_dir = result["out_dir"]
    hygiene = result["hygiene"]
    explicit = [item for item in hygiene["predicate"]["findings"] if item["code"] == "PATH_TOO_LONG"]
    marker = {
        "code": "HYGIENE_FINDINGS_TRUNCATED",
        "severity": "warning",
        "profile": "source-fixity/v1",
        "message": "Hygiene findings were truncated by deterministic report-size limits.",
        "details": {"truncated_by_code": {"PATH_TOO_LONG": 100}},
    }
    hygiene["predicate"]["parameters"]["max_findings_per_code"] = 1
    hygiene["predicate"]["findings"] = [explicit[0], marker]
    hygiene["predicate"]["summary"] = {
        "finding_count": len(hygiene["predicate"]["findings"]),
        "max_severity": validate_source_capture_bundle.computed_max_severity(hygiene["predicate"]["findings"]),
    }
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    assert_enterprise_validator_rejects(out_dir, "max_findings_per_code")


def test_path_too_long_binding_is_exact_not_suffix(tmp: Path) -> None:
    long_path = "a" * 261
    archive = tmp / "long-path-suffix.zip"
    write_zip(archive, [(long_path, b"a"), (f"x/{long_path}", b"b")])
    result = run_inspector(archive, tmp / "out-long-path-suffix")
    findings = [
        item
        for item in result["hygiene"]["predicate"]["findings"]
        if item["code"] != "PATH_TOO_LONG" or item.get("paths") == [f"x/{long_path}"]
    ]
    rewrite_hygiene_findings(result["out_dir"], findings)
    assert_enterprise_validator_rejects(result["out_dir"], "PATH_TOO_LONG")


def test_truncation_marker_must_be_unique(tmp: Path) -> None:
    archive = tmp / "long-paths-101-duplicate-marker.zip"
    write_zip(archive, long_manifest_paths(101))
    result = run_inspector(archive, tmp / "out-long-paths-101-duplicate-marker")
    marker = next(item for item in result["hygiene"]["predicate"]["findings"] if item["code"] == "HYGIENE_FINDINGS_TRUNCATED")
    rewrite_hygiene_findings(result["out_dir"], result["hygiene"]["predicate"]["findings"] + [dict(marker)])
    assert_enterprise_validator_rejects(result["out_dir"], "at most once")


def test_explicit_directory_prefix_conflict_quarantined(tmp: Path) -> None:
    archive = tmp / "explicit-dir-conflict.zip"
    file_info = zip_info("repo/a", stat.S_IFREG | 0o644)
    dir_info = zip_info("repo/a/b/", stat.S_IFDIR | 0o755)
    write_zip_infos(archive, [(file_info, b"file"), (dir_info, b"")])
    result = run_inspector(archive, tmp / "out-explicit-dir-conflict-zip")
    assert "ARCHIVE_ANCESTOR_PREFIX_CONFLICT" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"

    tar_path = tmp / "explicit-dir-conflict.tar"
    with tarfile.open(tar_path, "w") as tf:
        info = tarfile.TarInfo("repo/a")
        data = b"file"
        info.size = len(data)
        tf.addfile(info, io.BytesIO(data))
        directory = tarfile.TarInfo("repo/a/b")
        directory.type = tarfile.DIRTYPE
        directory.size = 0
        tf.addfile(directory)
    result = run_inspector(tar_path, tmp / "out-explicit-dir-conflict-tar")
    assert "ARCHIVE_ANCESTOR_PREFIX_CONFLICT" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_bundle_rejects_blob_admitted_with_failed_or_partial_state(tmp: Path) -> None:
    source = tmp / "asset.bin"
    source.write_bytes(b"blob")
    result = run_inspector(source, tmp / "out-blob-bad-state", "--source-kind", "file", "--capture-method", "local_file")
    out_dir = result["out_dir"]
    envelope = result["envelope"]
    hygiene = result["hygiene"]
    envelope["observation"]["state"] = "failed"
    hygiene["predicate"]["execution_state"] = "partial"
    hygiene["predicate"]["findings"] = [
        {
            "code": "SYNTHETIC_WARNING",
            "message": "Synthetic warning for blob state-matrix regression.",
            "profile": "source-fixity/v1",
            "severity": "warning",
        }
    ]
    hygiene["predicate"]["summary"] = {"finding_count": 1, "max_severity": "warning"}
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    expect_bundle_validation_error(out_dir)


def test_bundle_rejects_symlink_entry_and_total_size_limit_bypasses(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-symlink-total-limit")
    out_dir = result["out_dir"]
    rows = [
        {"profile": "vaks-archive-tree/v1", "schema": "urn:vaks:schema:snapshot-manifest:v1", "state": "complete"},
        {"mode": "120000", "path": "a", "target": "x", "type": "symlink"},
        {"mode": "120000", "path": "b", "target": "y", "type": "symlink"},
    ]
    envelope, hygiene = rebind_tree_manifest(out_dir, rows)
    hygiene["predicate"]["parameters"]["max_total_size"] = 1
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    expect_bundle_validation_error(out_dir)

    result = run_inspector(archive, tmp / "out-symlink-entry-limit")
    out_dir = result["out_dir"]
    rows = [
        {"profile": "vaks-archive-tree/v1", "schema": "urn:vaks:schema:snapshot-manifest:v1", "state": "complete"},
        {"mode": "120000", "path": "a", "target": "xy", "type": "symlink"},
    ]
    envelope, hygiene = rebind_tree_manifest(out_dir, rows)
    hygiene["predicate"]["parameters"]["max_entry_size"] = 1
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    expect_bundle_validation_error(out_dir)


def test_tar_symlink_payload_quarantined(tmp: Path) -> None:
    archive = tmp / "symlink-payload.tar"
    with tarfile.open(archive, "w") as tf:
        link = tarfile.TarInfo("repo/link")
        link.type = tarfile.SYMTYPE
        link.linkname = "safe"
        link.size = 4
        tf.addfile(link, io.BytesIO(b"AAAA"))
    result = run_inspector(archive, tmp / "out-symlink-payload")
    assert "ARCHIVE_TYPE_COLLISION" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_zip_multi_path_representations_quarantined(tmp: Path) -> None:
    nul_x = tmp / "nul-x.zip"
    nul_y = tmp / "nul-y.zip"
    write_raw_zip(nul_x, [(b"repo/a\x00X", b"same")])
    write_raw_zip(nul_y, [(b"repo/a\x00Y", b"same")])
    r1 = run_inspector(nul_x, tmp / "out-nul-x")
    r2 = run_inspector(nul_y, tmp / "out-nul-y")
    assert r1["envelope"]["raw_handling"]["disposition"] == "quarantined"
    assert r2["envelope"]["raw_handling"]["disposition"] == "quarantined"
    assert "ARCHIVE_PATH_CONTROL_CHARACTER" in finding_codes(r1)
    assert "ARCHIVE_PATH_CONTROL_CHARACTER" in finding_codes(r2)

    unicode_traversal = tmp / "unicode-traversal.zip"
    raw_safe = b"repo/safe.txt"
    write_raw_zip(unicode_traversal, [(raw_safe, b"data")], extra=unicode_path_extra(raw_safe, "../evil.txt"))
    result = run_inspector(unicode_traversal, tmp / "out-unicode-traversal")
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"
    assert {"ARCHIVE_PATH_TRAVERSAL", "ARCHIVE_PATH_REPRESENTATION_CONFLICT"} & finding_codes(result)

    raw_backslash = tmp / "raw-backslash.zip"
    raw_name = b"repo\\safe.txt"
    write_raw_zip(raw_backslash, [(raw_name, b"data")], extra=unicode_path_extra(raw_name, "repo/safe.txt"))
    result = run_inspector(raw_backslash, tmp / "out-raw-backslash")
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"
    assert {"ARCHIVE_BACKSLASH_PATH", "ARCHIVE_PATH_REPRESENTATION_CONFLICT"} & finding_codes(result)


def test_zip_dos_type_evidence_reconciled(tmp: Path) -> None:
    dos_dir = tmp / "dos-dir.zip"
    write_raw_zip(dos_dir, [(b"repo/a", b"")], create_system=0, external_attr=0x10)
    result = run_inspector(dos_dir, tmp / "out-dos-dir")
    assert "ARCHIVE_TYPE_COLLISION" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"

    volume = tmp / "dos-volume.zip"
    write_raw_zip(volume, [(b"repo/VOLUME", b"")], create_system=0, external_attr=0x08)
    result = run_inspector(volume, tmp / "out-dos-volume")
    assert "ARCHIVE_SPECIAL_FILE" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"

    pseudo_symlink = tmp / "dos-pseudo-symlink.zip"
    write_raw_zip(
        pseudo_symlink,
        [(b"repo/link", b"../not-a-target")],
        create_system=0,
        external_attr=(stat.S_IFLNK | 0o777) << 16,
    )
    result = run_inspector(pseudo_symlink, tmp / "out-dos-pseudo-symlink")
    assert result["envelope"]["raw_handling"]["disposition"] == "admitted"
    assert '"path":"link","size":15,"type":"file"' in "\n".join(result["manifest_lines"])


def test_bundle_rejects_duplicate_json_keys(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-duplicate-disposition")
    out_dir = result["out_dir"]
    envelope_path = out_dir / "capture-envelope.json"
    text = envelope_path.read_text(encoding="utf-8")
    text = text.replace('"disposition": "admitted"', '"disposition": "admitted",\n    "disposition": "quarantined"', 1)
    envelope_path.write_text(text, encoding="utf-8")
    expect_bundle_validation_error(out_dir)

    result = run_inspector(archive, tmp / "out-duplicate-execution")
    out_dir = result["out_dir"]
    hygiene_path = out_dir / "snapshot-hygiene.intoto.json"
    hygiene_text = hygiene_path.read_text(encoding="utf-8")
    hygiene_text = hygiene_text.replace('"execution_state": "complete"', '"execution_state": "complete",\n    "execution_state": "partial"', 1)
    hygiene_path.write_text(hygiene_text, encoding="utf-8")
    envelope = result["envelope"]
    hygiene_bytes = hygiene_text.encode("utf-8")
    envelope["inspection_refs"][0]["size"] = len(hygiene_bytes)
    envelope["inspection_refs"][0]["digest"] = inspect_source_snapshot.digest_bytes(hygiene_bytes)
    write_json(out_dir / "capture-envelope.json", envelope)
    expect_bundle_validation_error(out_dir)

    case_archive = tmp / "case.zip"
    write_zip(case_archive, [("repo/TAG.SQL", b"upper"), ("repo/TAG.sql", b"lower")])
    result = run_inspector(case_archive, tmp / "out-duplicate-severity")
    out_dir = result["out_dir"]
    hygiene_path = out_dir / "snapshot-hygiene.intoto.json"
    hygiene_text = hygiene_path.read_text(encoding="utf-8")
    hygiene_text = hygiene_text.replace('"severity": "warning"', '"severity": "warning",\n        "severity": "critical"', 1)
    hygiene_path.write_text(hygiene_text, encoding="utf-8")
    envelope = result["envelope"]
    hygiene_bytes = hygiene_text.encode("utf-8")
    envelope["inspection_refs"][0]["size"] = len(hygiene_bytes)
    envelope["inspection_refs"][0]["digest"] = inspect_source_snapshot.digest_bytes(hygiene_bytes)
    write_json(out_dir / "capture-envelope.json", envelope)
    expect_bundle_validation_error(out_dir)


def test_zip_hidden_decompressed_suffix_quarantined(tmp: Path) -> None:
    archive = tmp / "hidden-deflate-suffix.zip"
    full_output = b"safeEVIL"
    compressed = raw_deflate(full_output)
    safe_crc = zlib.crc32(b"safe") & 0xFFFFFFFF
    write_malformed_zip_single(
        archive,
        payload=compressed,
        central_payload_size=len(compressed),
        local_payload_size=len(compressed),
        central_file_size=4,
        local_file_size=4,
        central_crc=safe_crc,
        local_crc=safe_crc,
        central_method=zipfile.ZIP_DEFLATED,
    )
    result = run_inspector(archive, tmp / "out-hidden-deflate")
    assert "ARCHIVE_ZIP_STREAM_INTEGRITY_FAILED" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_zip_stored_size_mismatch_quarantined(tmp: Path) -> None:
    archive = tmp / "stored-size-mismatch.zip"
    safe_crc = zlib.crc32(b"safe") & 0xFFFFFFFF
    write_malformed_zip_single(
        archive,
        payload=b"safeEVIL",
        central_payload_size=8,
        local_payload_size=8,
        central_file_size=4,
        local_file_size=4,
        central_crc=safe_crc,
        local_crc=safe_crc,
        central_method=zipfile.ZIP_STORED,
    )
    result = run_inspector(archive, tmp / "out-stored-size-mismatch")
    assert "ARCHIVE_ZIP_STREAM_INTEGRITY_FAILED" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_zip_local_central_header_mismatches_quarantined(tmp: Path) -> None:
    method_mismatch = tmp / "method-mismatch.zip"
    write_malformed_zip_single(
        method_mismatch,
        payload=b"safe",
        central_method=zipfile.ZIP_STORED,
        local_method=zipfile.ZIP_DEFLATED,
    )
    result = run_inspector(method_mismatch, tmp / "out-method-mismatch")
    assert "ARCHIVE_ZIP_HEADER_CONFLICT" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"

    for label, local_flag in [("encryption", 0x1), ("utf8", 0x800), ("data-descriptor", 0x8)]:
        archive = tmp / f"flag-{label}.zip"
        write_malformed_zip_single(
            archive,
            payload=b"safe",
            central_flags=0,
            local_flags=local_flag,
        )
        result = run_inspector(archive, tmp / f"out-flag-{label}")
        assert "ARCHIVE_ZIP_HEADER_CONFLICT" in finding_codes(result)
        if local_flag == 0x8:
            assert "ARCHIVE_ZIP_DATA_DESCRIPTOR_UNSUPPORTED" in finding_codes(result)
        assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"

    crc_mismatch = tmp / "crc-mismatch.zip"
    write_malformed_zip_single(
        crc_mismatch,
        payload=b"safe",
        central_crc=zlib.crc32(b"safe") & 0xFFFFFFFF,
        local_crc=zlib.crc32(b"evil") & 0xFFFFFFFF,
    )
    result = run_inspector(crc_mismatch, tmp / "out-crc-mismatch")
    assert "ARCHIVE_ZIP_HEADER_CONFLICT" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"

    size_mismatch = tmp / "size-mismatch.zip"
    write_malformed_zip_single(
        size_mismatch,
        payload=b"safe",
        central_payload_size=4,
        local_payload_size=5,
        central_file_size=4,
        local_file_size=5,
    )
    result = run_inspector(size_mismatch, tmp / "out-size-mismatch")
    assert "ARCHIVE_ZIP_HEADER_CONFLICT" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_zip_directory_payload_exact_validation_quarantined(tmp: Path) -> None:
    archive = tmp / "directory-hidden-payload.zip"
    payload = raw_deflate(b"EVIL")
    write_malformed_zip_single(
        archive,
        name=b"repo/dir/",
        payload=payload,
        central_payload_size=len(payload),
        local_payload_size=len(payload),
        central_file_size=0,
        local_file_size=0,
        central_crc=0,
        local_crc=0,
        central_method=zipfile.ZIP_DEFLATED,
    )
    result = run_inspector(archive, tmp / "out-directory-hidden-payload")
    codes = finding_codes(result)
    assert "ARCHIVE_ENTRY_SIZE_LIMIT_EXCEEDED" in codes or "ARCHIVE_ZIP_STREAM_INTEGRITY_FAILED" in codes
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_zip_directory_encryption_and_unsupported_methods_quarantined(tmp: Path) -> None:
    encrypted = tmp / "encrypted-directory.zip"
    write_malformed_zip_single(
        encrypted,
        name=b"repo/secret/",
        payload=b"",
        central_flags=0x1,
    )
    result = run_inspector(encrypted, tmp / "out-encrypted-directory")
    assert "ARCHIVE_ENCRYPTED_ENTRY" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"

    for label, method in [("bzip2", zipfile.ZIP_BZIP2), ("lzma", zipfile.ZIP_LZMA)]:
        archive = tmp / f"{label}-directory.zip"
        write_malformed_zip_single(
            archive,
            name=b"repo/dir/",
            payload=b"",
            central_method=method,
        )
        result = run_inspector(archive, tmp / f"out-{label}-directory")
        assert "ARCHIVE_UNSUPPORTED_COMPRESSION" in finding_codes(result)
        assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_zip_legal_empty_directories_admitted(tmp: Path) -> None:
    stored = tmp / "stored-empty-directory.zip"
    write_malformed_zip_single(stored, name=b"repo/empty/", payload=b"")
    result = run_inspector(stored, tmp / "out-stored-empty-directory")
    assert finding_codes(result) == set()
    assert result["envelope"]["raw_handling"]["disposition"] == "admitted"

    deflated = tmp / "deflated-empty-directory.zip"
    payload = raw_deflate(b"")
    write_malformed_zip_single(
        deflated,
        name=b"repo/empty/",
        payload=payload,
        central_payload_size=len(payload),
        local_payload_size=len(payload),
        central_file_size=0,
        local_file_size=0,
        central_crc=0,
        local_crc=0,
        central_method=zipfile.ZIP_DEFLATED,
    )
    result = run_inspector(deflated, tmp / "out-deflated-empty-directory")
    assert finding_codes(result) == set()
    assert result["envelope"]["raw_handling"]["disposition"] == "admitted"


def test_zip_deflate_budget_limits_actual_output(tmp: Path) -> None:
    archive = tmp / "deflate-budget.zip"
    full_output = b"A" * 2048
    payload = raw_deflate(full_output)
    write_malformed_zip_single(
        archive,
        payload=payload,
        central_payload_size=len(payload),
        local_payload_size=len(payload),
        central_file_size=1,
        local_file_size=1,
        central_crc=zlib.crc32(b"A") & 0xFFFFFFFF,
        local_crc=zlib.crc32(b"A") & 0xFFFFFFFF,
        central_method=zipfile.ZIP_DEFLATED,
    )
    result = run_inspector(archive, tmp / "out-deflate-budget", "--max-entry-size", "1024")
    assert "ARCHIVE_ENTRY_SIZE_LIMIT_EXCEEDED" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "quarantined"
    findings = result["hygiene"]["predicate"]["findings"]
    size_finding = next(item for item in findings if item["code"] == "ARCHIVE_ENTRY_SIZE_LIMIT_EXCEEDED")
    assert size_finding["details"]["actual_size"] == 1025


def test_input_blob_size_limit_creates_no_bundle(tmp: Path) -> None:
    source = tmp / "blob.bin"
    source.write_bytes(b"ab")
    out_dir = tmp / "out-limit"
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        rc = inspect_source_snapshot.main(
            [
                str(source),
                "--out",
                str(out_dir),
                "--source-id",
                "vsrc:1:content:sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "--source-kind",
                "file",
                "--capture-method",
                "local_file",
                "--max-input-blob-size",
                "1",
            ]
        )
    payload = json.loads(stdout.getvalue())
    assert rc == 3
    assert payload["code"] == "CAPTURE_INPUT_BLOB_LIMIT_EXCEEDED"
    assert payload["bundle_created"] is False
    assert not out_dir.exists()

    result = run_inspector(
        source,
        tmp / "out-limit-exact",
        "--source-kind",
        "file",
        "--capture-method",
        "local_file",
        "--max-input-blob-size",
        "2",
    )
    assert result["envelope"]["raw_handling"]["disposition"] == "admitted"
    assert result["hygiene"]["predicate"]["parameters"]["max_input_blob_size"] == 2


def test_media_type_detection_hint_mismatch_and_source_kind_conflict(tmp: Path) -> None:
    disguised = tmp / "report.pdf"
    write_zip(disguised, [("repo/a.txt", b"a")])
    result = run_inspector(disguised, tmp / "out-disguised")
    observation = result["envelope"]["observation"]
    assert observation["blob"]["media_type"] == "application/zip"
    assert observation["content_type"]["detected_media_type"] == "application/zip"
    assert observation["content_type"]["locator_hint_media_type"] == "application/pdf"
    assert observation["content_type"]["hint_match"] == "mismatch"
    assert "MEDIA_TYPE_HINT_MISMATCH" in finding_codes(result)
    assert result["envelope"]["raw_handling"]["disposition"] == "admitted"

    conflict = run_inspector(
        disguised,
        tmp / "out-source-kind-conflict",
        "--source-kind",
        "pdf",
        "--capture-method",
        "upload",
        "--source-id",
        "vsrc:1:opaque:pdf-demo",
    )
    assert "SOURCE_KIND_FORMAT_MISMATCH" in finding_codes(conflict)
    assert conflict["envelope"]["raw_handling"]["disposition"] == "quarantined"


def test_tar_and_unknown_blob_media_type_detection(tmp: Path) -> None:
    tar_path = tmp / "payload.bin"
    write_tar(tar_path, [("repo/a.txt", b"a")])
    tar_result = run_inspector(
        tar_path,
        tmp / "out-tar-media",
        "--source-kind",
        "archive",
        "--capture-method",
        "archive_file",
        "--source-id",
        "vsrc:1:opaque:tar-demo",
    )
    assert tar_result["envelope"]["observation"]["blob"]["media_type"] == "application/x-tar"

    blob = tmp / "unknown"
    blob.write_bytes(b"not a typed document")
    blob_result = run_inspector(
        blob,
        tmp / "out-unknown-blob",
        "--source-kind",
        "file",
        "--capture-method",
        "local_file",
        "--source-id",
        "vsrc:1:content:sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    )
    assert blob_result["envelope"]["observation"]["blob"]["media_type"] == "application/octet-stream"
    assert blob_result["envelope"]["observation"]["content_type"]["detection_basis"] == "fallback"


def test_implementation_manifest_mismatch_fails_before_bundle(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    bad_manifest = tmp / "bad-implementation.json"
    manifest = json.loads(inspect_source_snapshot.default_implementation_manifest_path().read_text(encoding="utf-8"))
    manifest["components"][0]["digest"] = "sha256:" + "0" * 64
    bad_manifest.write_text(json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    out_dir = tmp / "out-bad-implementation"
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        rc = inspect_source_snapshot.main(
            [
                str(archive),
                "--out",
                str(out_dir),
                "--source-id",
                "vsrc:1:repo:github.com/example/repo",
                "--source-kind",
                "repo",
                "--implementation-manifest",
                str(bad_manifest),
            ]
        )
    payload = json.loads(stdout.getvalue())
    assert rc == 4
    assert payload["code"] == "CAPTURE_IMPLEMENTATION_PIN_MISMATCH"
    assert payload["bundle_created"] is False
    assert not out_dir.exists()


def test_implementation_manifest_must_pin_required_component_set(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    schema_digest = inspect_source_snapshot.digest_file(Path("SCHEMA.md"))
    bad_manifest = tmp / "minimal-implementation.json"
    bad_manifest.write_text(
        json.dumps(
            {
                "schema": "urn:vaks:schema:source-capture-implementation:v1",
                "id": "vaks.source-capture-envelope",
                "version": "1.0-alpha.1",
                "components": [{"path": "SCHEMA.md", "digest": schema_digest}],
                "runtime": {"language": "python", "minimum_version": "3.10"},
            },
            allow_nan=False,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n",
        encoding="utf-8",
    )
    out_dir = tmp / "out-minimal-implementation"
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        rc = inspect_source_snapshot.main(
            [
                str(archive),
                "--out",
                str(out_dir),
                "--source-id",
                "vsrc:1:repo:github.com/example/repo",
                "--source-kind",
                "repo",
                "--implementation-manifest",
                str(bad_manifest),
            ]
        )
    payload = json.loads(stdout.getvalue())
    assert rc == 4
    assert payload["code"] == "CAPTURE_IMPLEMENTATION_PIN_MISMATCH"
    assert not out_dir.exists()


def test_runtime_policy_must_match_pinned_implementation_policy(tmp: Path) -> None:
    archive = tmp / "report.pdf"
    write_zip(archive, [("repo/a.txt", b"a")])
    default_policy = json.loads(inspect_source_snapshot.default_policy_path().read_text(encoding="utf-8"))
    default_policy["unsafe_finding"]["codes"].remove("SOURCE_KIND_FORMAT_MISMATCH")
    custom_policy = tmp / "custom-policy.json"
    custom_policy.write_text(
        json.dumps(default_policy, allow_nan=False, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    out_dir = tmp / "out-custom-policy"
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        rc = inspect_source_snapshot.main(
            [
                str(archive),
                "--out",
                str(out_dir),
                "--source-id",
                "vsrc:1:opaque:pdf-demo",
                "--source-kind",
                "pdf",
                "--capture-method",
                "upload",
                "--policy-file",
                str(custom_policy),
            ]
        )
    payload = json.loads(stdout.getvalue())
    assert rc == 4
    assert payload["code"] == "CAPTURE_POLICY_PIN_MISMATCH"
    assert not out_dir.exists()


def test_enterprise_validator_requires_policy_and_implementation_binding(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-enterprise")
    out_dir = result["out_dir"]
    policy_file = inspect_source_snapshot.default_policy_path()
    validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=policy_file)

    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    del envelope["raw_handling"]["policy"]["digest"]
    write_json(out_dir / "capture-envelope.json", envelope)
    try:
        validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=policy_file)
    except validate_source_capture_bundle.ValidationError as exc:
        assert "policy" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must require policy digest")

    result = run_inspector(archive, tmp / "out-implementation-binding")
    out_dir = result["out_dir"]
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    hygiene = json.loads((out_dir / "snapshot-hygiene.intoto.json").read_text(encoding="utf-8"))
    hygiene["predicate"]["checker"]["implementation"]["digest"] = "sha256:" + "1" * 64
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    try:
        validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=policy_file)
    except validate_source_capture_bundle.ValidationError as exc:
        assert "implementation" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must bind producer/checker implementation descriptors")


def test_enterprise_validator_binds_implementation_descriptor_to_manifest(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-fake-implementation-descriptor")
    out_dir = result["out_dir"]
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    hygiene = json.loads((out_dir / "snapshot-hygiene.intoto.json").read_text(encoding="utf-8"))
    fake_descriptor = {
        "media_type": "application/vnd.vaks.source-capture-implementation.v1+json",
        "size": 1,
        "digest": "sha256:" + "0" * 64,
    }
    envelope["producer"]["implementation"] = fake_descriptor
    hygiene["predicate"]["checker"]["implementation"] = fake_descriptor
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    try:
        validate_source_capture_bundle.validate_bundle(
            out_dir,
            profile="enterprise-alpha1",
            policy_file=inspect_source_snapshot.default_policy_path(),
        )
    except validate_source_capture_bundle.ValidationError as exc:
        assert "implementation descriptor" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must bind implementation descriptors to the pinned manifest")


def test_enterprise_validator_rejects_unpinned_policy_file(tmp: Path) -> None:
    blob = tmp / "clean.txt"
    blob.write_bytes(b"clean")
    result = run_inspector(
        blob,
        tmp / "out-unpinned-policy",
        "--source-kind",
        "file",
        "--capture-method",
        "local_file",
        "--source-id",
        "vsrc:1:content:sha256:" + "3" * 64,
    )
    out_dir = result["out_dir"]
    custom_policy = json.loads(inspect_source_snapshot.default_policy_path().read_text(encoding="utf-8"))
    custom_policy["unsafe_finding"]["codes"] = ["SOME_OTHER_CODE"]
    custom_policy_path = tmp / "custom-policy.json"
    custom_policy_path.write_text(
        json.dumps(custom_policy, allow_nan=False, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    hygiene = json.loads((out_dir / "snapshot-hygiene.intoto.json").read_text(encoding="utf-8"))
    envelope["raw_handling"]["policy"]["digest"] = validate_source_capture_bundle.sha256_bytes(
        validate_source_capture_bundle.canonical_json_bytes(custom_policy)
    )
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    try:
        validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=custom_policy_path)
    except validate_source_capture_bundle.ValidationError as exc:
        assert "policy file" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must reject policy files not pinned by the implementation manifest")


def test_policy_must_include_hazard_and_error_unsafe_severities(tmp: Path) -> None:
    weak_policy = json.loads(inspect_source_snapshot.default_policy_path().read_text(encoding="utf-8"))
    weak_policy["unsafe_finding"]["severities"] = ["error"]
    weak_policy_path = tmp / "weak-policy.json"
    weak_policy_path.write_text(
        json.dumps(weak_policy, allow_nan=False, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    try:
        validate_source_capture_bundle.load_policy(weak_policy_path)
    except validate_source_capture_bundle.ValidationError as exc:
        assert "hazard and error" in str(exc)
    else:
        raise AssertionError("validator policy loader must reject policies that omit hazard or error")

    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    out_dir = tmp / "out-weak-policy"
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        rc = inspect_source_snapshot.main(
            [
                str(archive),
                "--out",
                str(out_dir),
                "--source-id",
                "vsrc:1:repo:github.com/example/repo",
                "--source-kind",
                "repo",
                "--policy-file",
                str(weak_policy_path),
            ]
        )
    payload = json.loads(stdout.getvalue())
    assert rc == 4
    assert payload["code"] == "CAPTURE_POLICY_PIN_MISMATCH"
    assert not out_dir.exists()


def test_enterprise_validator_replays_policy_decision_and_reason_codes(tmp: Path) -> None:
    blob = tmp / "clean.txt"
    blob.write_bytes(b"clean")
    result = run_inspector(
        blob,
        tmp / "out-clean-blob",
        "--source-kind",
        "file",
        "--capture-method",
        "local_file",
        "--source-id",
        "vsrc:1:content:sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
    )
    out_dir = result["out_dir"]
    policy_file = inspect_source_snapshot.default_policy_path()
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    hygiene = json.loads((out_dir / "snapshot-hygiene.intoto.json").read_text(encoding="utf-8"))
    envelope["observation"]["state"] = "partial"
    envelope["raw_handling"]["disposition"] = "quarantined"
    envelope["raw_handling"]["reason_codes"] = ["FAKE_REASON"]
    write_manifest_rows(
        out_dir,
        [
            {
                "profile": "vaks-archive-tree/v1",
                "schema": "urn:vaks:schema:snapshot-manifest:v1",
                "state": "unavailable",
                "reason_codes": ["FAKE_REASON"],
            }
        ],
    )
    hygiene["predicate"]["execution_state"] = "partial"
    hygiene["predicate"]["findings"] = [
        {
            "code": "MEDIA_TYPE_HINT_MISMATCH",
            "severity": "warning",
            "profile": "source-fixity/v1",
            "message": "warning only",
        }
    ]
    hygiene["predicate"]["summary"] = {"finding_count": 1, "max_severity": "warning"}
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    try:
        validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=policy_file)
    except validate_source_capture_bundle.ValidationError as exc:
        assert "policy replay" in str(exc) or "reason_codes" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must reject quarantine without policy-unsafe findings")

    pdf_zip = tmp / "report.pdf"
    write_zip(pdf_zip, [("repo/a.txt", b"a")])
    conflict = run_inspector(
        pdf_zip,
        tmp / "out-pdf-zip",
        "--source-kind",
        "pdf",
        "--capture-method",
        "upload",
        "--source-id",
        "vsrc:1:opaque:pdf-demo",
    )
    out_dir = conflict["out_dir"]
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    envelope["raw_handling"]["reason_codes"].append("FAKE_EXTRA")
    rows = [json.loads(line) for line in (out_dir / "snapshot-manifest.jsonl").read_text(encoding="utf-8").splitlines()]
    rows[0]["reason_codes"] = envelope["raw_handling"]["reason_codes"]
    write_manifest_rows(out_dir, rows)
    hygiene = json.loads((out_dir / "snapshot-hygiene.intoto.json").read_text(encoding="utf-8"))
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    try:
        validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=policy_file)
    except validate_source_capture_bundle.ValidationError as exc:
        assert "reason_codes" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must reject extra reason_codes")


def test_enterprise_validator_rejects_unknown_hazard_admitted(tmp: Path) -> None:
    blob = tmp / "clean.txt"
    blob.write_bytes(b"clean")
    result = run_inspector(
        blob,
        tmp / "out-unknown-hazard",
        "--source-kind",
        "file",
        "--capture-method",
        "local_file",
        "--source-id",
        "vsrc:1:content:sha256:1111111111111111111111111111111111111111111111111111111111111111",
    )
    out_dir = result["out_dir"]
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    hygiene = json.loads((out_dir / "snapshot-hygiene.intoto.json").read_text(encoding="utf-8"))
    hygiene["predicate"]["findings"].append(
        {
            "code": "UNREGISTERED_SECURITY_HAZARD",
            "severity": "hazard",
            "profile": "source-fixity/v1",
            "message": "synthetic hazard",
        }
    )
    hygiene["predicate"]["summary"] = {
        "finding_count": len(hygiene["predicate"]["findings"]),
        "max_severity": validate_source_capture_bundle.computed_max_severity(hygiene["predicate"]["findings"]),
    }
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    try:
        validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=inspect_source_snapshot.default_policy_path())
    except validate_source_capture_bundle.ValidationError as exc:
        assert "policy replay" in str(exc) or "reason_codes" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must reject admitted bundles with unknown hazard/error findings")


def test_enterprise_validator_rejects_policy_code_downgraded_to_warning_admitted(tmp: Path) -> None:
    blob = tmp / "clean.txt"
    blob.write_bytes(b"clean")
    result = run_inspector(
        blob,
        tmp / "out-policy-code-warning",
        "--source-kind",
        "file",
        "--capture-method",
        "local_file",
        "--source-id",
        "vsrc:1:content:sha256:2222222222222222222222222222222222222222222222222222222222222222",
    )
    out_dir = result["out_dir"]
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    hygiene = json.loads((out_dir / "snapshot-hygiene.intoto.json").read_text(encoding="utf-8"))
    if "archive-safety/v1" not in hygiene["predicate"]["profiles"]:
        hygiene["predicate"]["profiles"].append("archive-safety/v1")
        hygiene["predicate"]["profiles"].sort()
    hygiene["predicate"]["findings"].append(
        {
            "code": "ARCHIVE_ZIP_STREAM_INTEGRITY_FAILED",
            "severity": "warning",
            "profile": "archive-safety/v1",
            "message": "synthetic downgraded unsafe code",
        }
    )
    hygiene["predicate"]["summary"] = {
        "finding_count": len(hygiene["predicate"]["findings"]),
        "max_severity": validate_source_capture_bundle.computed_max_severity(hygiene["predicate"]["findings"]),
    }
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    try:
        validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=inspect_source_snapshot.default_policy_path())
    except validate_source_capture_bundle.ValidationError as exc:
        assert "policy replay" in str(exc) or "reason_codes" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must reject admitted bundles with policy-listed unsafe codes even if severity is warning")


def test_enterprise_validator_requires_source_kind_media_type_finding(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(
        archive,
        tmp / "out-rebound-pdf",
        "--source-kind",
        "archive",
        "--capture-method",
        "archive_file",
        "--source-id",
        "vsrc:1:opaque:archive-demo",
    )
    out_dir = result["out_dir"]
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    envelope["source"]["kind"] = "pdf"
    hygiene = json.loads((out_dir / "snapshot-hygiene.intoto.json").read_text(encoding="utf-8"))
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    try:
        validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=inspect_source_snapshot.default_policy_path())
    except validate_source_capture_bundle.ValidationError as exc:
        assert "SOURCE_KIND_FORMAT_MISMATCH" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must reject pdf source kind with non-PDF detected media type")


def test_enterprise_validator_rejects_contradictory_hint_match(tmp: Path) -> None:
    disguised = tmp / "report.pdf"
    write_zip(disguised, [("repo/a.txt", b"a")])
    result = run_inspector(disguised, tmp / "out-hint-match")
    out_dir = result["out_dir"]
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    content_type = envelope["observation"]["content_type"]
    assert content_type["detected_media_type"] == "application/zip"
    assert content_type["locator_hint_media_type"] == "application/pdf"
    content_type["hint_match"] = "matched"
    write_json(out_dir / "capture-envelope.json", envelope)
    try:
        validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=inspect_source_snapshot.default_policy_path())
    except validate_source_capture_bundle.ValidationError as exc:
        assert "hint_match=matched" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must reject contradictory hint_match")


def test_enterprise_validator_rejects_not_comparable_hint_match(tmp: Path) -> None:
    disguised = tmp / "report.pdf"
    write_zip(disguised, [("repo/a.txt", b"a")])
    result = run_inspector(disguised, tmp / "out-not-comparable")
    out_dir = result["out_dir"]
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    hygiene = json.loads((out_dir / "snapshot-hygiene.intoto.json").read_text(encoding="utf-8"))
    content_type = envelope["observation"]["content_type"]
    assert content_type["detected_media_type"] == "application/zip"
    assert content_type["locator_hint_media_type"] == "application/pdf"
    content_type["hint_match"] = "not_comparable"
    hygiene["predicate"]["findings"] = [
        item for item in hygiene["predicate"]["findings"] if item.get("code") != "MEDIA_TYPE_HINT_MISMATCH"
    ]
    hygiene["predicate"]["summary"] = {
        "finding_count": len(hygiene["predicate"]["findings"]),
        "max_severity": validate_source_capture_bundle.computed_max_severity(hygiene["predicate"]["findings"]),
    }
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    try:
        validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=inspect_source_snapshot.default_policy_path())
    except validate_source_capture_bundle.ValidationError as exc:
        assert "not_comparable" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must reject currently unreachable not_comparable hint_match")


def test_enterprise_validator_rejects_not_comparable_even_when_hint_matches(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-not-comparable-matched")
    out_dir = result["out_dir"]
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    content_type = envelope["observation"]["content_type"]
    content_type["locator_hint_media_type"] = content_type["detected_media_type"]
    content_type["hint_match"] = "not_comparable"
    write_json(out_dir / "capture-envelope.json", envelope)
    try:
        validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=inspect_source_snapshot.default_policy_path())
    except validate_source_capture_bundle.ValidationError as exc:
        assert "not_comparable" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must reject not_comparable even when hint equals detected media type")


def test_enterprise_validator_rejects_locator_hint_basis(tmp: Path) -> None:
    blob = tmp / "unknown.bin"
    blob.write_bytes(b"plain")
    result = run_inspector(
        blob,
        tmp / "out-locator-hint-basis",
        "--source-kind",
        "file",
        "--capture-method",
        "local_file",
        "--source-id",
        "vsrc:1:content:sha256:dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
    )
    out_dir = result["out_dir"]
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    content_type = envelope["observation"]["content_type"]
    assert content_type["hint_match"] == "no_hint"
    content_type["detection_basis"] = "locator_hint"
    write_json(out_dir / "capture-envelope.json", envelope)
    try:
        validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=inspect_source_snapshot.default_policy_path())
    except validate_source_capture_bundle.ValidationError as exc:
        assert "detection_basis=locator_hint" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must reject currently unreachable locator_hint detection basis")


def test_enterprise_validator_rejects_tree_pdf_magic_content_type(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-tree-pdf-magic")
    out_dir = result["out_dir"]
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    blob = envelope["observation"]["blob"]
    content_type = envelope["observation"]["content_type"]
    blob["media_type"] = "application/pdf"
    content_type["detected_media_type"] = "application/pdf"
    content_type["detection_basis"] = "magic_signature"
    content_type["locator_hint_media_type"] = "application/pdf"
    content_type["hint_match"] = "matched"
    write_json(out_dir / "capture-envelope.json", envelope)
    try:
        validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=inspect_source_snapshot.default_policy_path())
    except validate_source_capture_bundle.ValidationError as exc:
        assert "tree snapshots require" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must reject tree snapshots with PDF magic-signature content type")


def test_enterprise_validator_rejects_tree_fallback_content_type(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-tree-fallback")
    out_dir = result["out_dir"]
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    blob = envelope["observation"]["blob"]
    content_type = envelope["observation"]["content_type"]
    blob["media_type"] = "application/octet-stream"
    content_type["detected_media_type"] = "application/octet-stream"
    content_type["detection_basis"] = "fallback"
    content_type.pop("locator_hint_media_type", None)
    content_type["hint_match"] = "no_hint"
    write_json(out_dir / "capture-envelope.json", envelope)
    try:
        validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=inspect_source_snapshot.default_policy_path())
    except validate_source_capture_bundle.ValidationError as exc:
        assert "tree snapshots require" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must reject tree snapshots with fallback content type")


def test_enterprise_validator_rejects_zip_with_fallback_basis(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-zip-fallback")
    out_dir = result["out_dir"]
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    content_type = envelope["observation"]["content_type"]
    assert content_type["detected_media_type"] == "application/zip"
    content_type["detection_basis"] = "fallback"
    write_json(out_dir / "capture-envelope.json", envelope)
    try:
        validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=inspect_source_snapshot.default_policy_path())
    except validate_source_capture_bundle.ValidationError as exc:
        assert "fallback requires application/octet-stream" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must reject application/zip with fallback detection basis")


def test_enterprise_validator_rejects_admitted_blob_container_parser(tmp: Path) -> None:
    blob_path = tmp / "plain.bin"
    blob_path.write_bytes(b"plain")
    result = run_inspector(
        blob_path,
        tmp / "out-blob-container-parser",
        "--source-kind",
        "file",
        "--capture-method",
        "local_file",
        "--source-id",
        "vsrc:1:content:sha256:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
    )
    out_dir = result["out_dir"]
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    blob = envelope["observation"]["blob"]
    content_type = envelope["observation"]["content_type"]
    blob["media_type"] = "application/zip"
    content_type["detected_media_type"] = "application/zip"
    content_type["detection_basis"] = "container_parser"
    content_type.pop("locator_hint_media_type", None)
    content_type["hint_match"] = "no_hint"
    write_json(out_dir / "capture-envelope.json", envelope)
    try:
        validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=inspect_source_snapshot.default_policy_path())
    except validate_source_capture_bundle.ValidationError as exc:
        assert "admitted blob snapshots" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must reject admitted blob snapshots with container_parser content type")


def test_enterprise_validator_rejects_container_parser_without_archive_safety(tmp: Path) -> None:
    archive = tmp / "clean.zip"
    write_zip(archive, [("repo/a.txt", b"a")])
    result = run_inspector(archive, tmp / "out-container-no-archive-safety")
    out_dir = result["out_dir"]
    envelope = json.loads((out_dir / "capture-envelope.json").read_text(encoding="utf-8"))
    hygiene = json.loads((out_dir / "snapshot-hygiene.intoto.json").read_text(encoding="utf-8"))
    assert envelope["observation"]["content_type"]["detection_basis"] == "container_parser"
    hygiene["predicate"]["profiles"] = ["source-fixity/v1"]
    rebind_hygiene_ref(out_dir, envelope, hygiene)
    try:
        validate_source_capture_bundle.validate_bundle(out_dir, profile="enterprise-alpha1", policy_file=inspect_source_snapshot.default_policy_path())
    except validate_source_capture_bundle.ValidationError as exc:
        assert "archive-safety/v1" in str(exc)
    else:
        raise AssertionError("enterprise-alpha1 must reject container_parser captures without archive-safety/v1")


def main() -> int:
    tests = [
        test_clean_archive,
        test_repo_requires_explicit_source_id,
        test_bundle_rejects_same_snapshot_without_previous,
        test_bundle_rejects_fake_fidelity_match,
        test_bundle_rejects_bad_revision_kind,
        test_bundle_rejects_multiple_hygiene_subjects,
        test_same_tree_different_zip_metadata,
        test_same_tree_different_zip_compression,
        test_hygiene_deterministic_across_entry_order,
        test_case_collision_preserved,
        test_duplicate_entry_quarantined,
        test_entry_size_limit_uses_entry_code,
        test_path_traversal_quarantined,
        test_portability_and_completeness_findings,
        test_clean_tar_archive,
        test_single_file_blob_snapshot,
        test_symlink_target_limit_quarantined,
        test_symlink_invalid_utf8_quarantined,
        test_symlink_escape_quarantined,
        test_zip_special_file_quarantined,
        test_tar_hardlink_quarantined,
        test_backslash_traversal_quarantined,
        test_corrupt_archive_quarantined,
        test_dot_segment_quarantined,
        test_ancestor_prefix_conflict_quarantined,
        test_non_executable_mode_does_not_change_snapshot,
        test_existing_output_dir_refused,
        test_media_type_for_compound_suffixes,
        test_unhandled_inspection_exception_structured_failed,
        test_input_change_during_scan_quarantined,
        test_original_input_aba_does_not_affect_temp_snapshot,
        test_zip_directory_marker_symlink_collision_quarantined,
        test_output_parent_symlink_refused,
        test_cli_rejects_invalid_change_and_limits,
        test_input_copy_failure_creates_no_bundle,
        test_empty_zip_is_valid_empty_tree,
        test_bundle_rejects_dangerous_rebound_manifest_path,
        test_bundle_rejects_unavailable_tree_admitted,
        test_bundle_rejects_blob_with_complete_tree_manifest,
        test_bundle_rejects_missing_producer_and_bad_severity,
        test_symlink_empty_backslash_control_quarantined,
        test_path_control_character_quarantined,
        test_damaged_tbz_txz_archive_intent_quarantined,
        test_bundle_rejects_remaining_state_matrix_bypasses,
        test_bundle_rejects_manifest_limit_bypasses,
        test_tar_directory_payload_quarantined,
        test_bundle_rejects_type_schema_and_profile_bypasses,
        test_zip_repeated_trailing_separator_quarantined,
        test_input_profile_blob_cannot_override_archive_intent,
        test_input_profile_blob_can_force_local_file_blob,
        test_path_too_long_is_portability_warning_not_hard_failure,
        test_bundle_rejects_unbound_path_too_long_warning,
        test_archive_path_hard_limit_is_structured_quarantine,
        test_path_too_long_uses_root_stripped_manifest_path,
        test_quarantined_long_path_does_not_require_complete_manifest_binding,
        test_path_too_long_truncation_marker_replays_zip,
        test_path_too_long_truncation_marker_replays_tar,
        test_truncation_marker_cannot_hide_unsafe_code,
        test_path_too_long_truncation_requires_explicit_prefix,
        test_truncation_rejects_tampered_max_findings_per_code,
        test_path_too_long_binding_is_exact_not_suffix,
        test_truncation_marker_must_be_unique,
        test_explicit_directory_prefix_conflict_quarantined,
        test_bundle_rejects_blob_admitted_with_failed_or_partial_state,
        test_bundle_rejects_symlink_entry_and_total_size_limit_bypasses,
        test_tar_symlink_payload_quarantined,
        test_zip_multi_path_representations_quarantined,
        test_zip_dos_type_evidence_reconciled,
        test_bundle_rejects_duplicate_json_keys,
        test_zip_hidden_decompressed_suffix_quarantined,
        test_zip_stored_size_mismatch_quarantined,
        test_zip_local_central_header_mismatches_quarantined,
        test_zip_directory_payload_exact_validation_quarantined,
        test_zip_directory_encryption_and_unsupported_methods_quarantined,
        test_zip_legal_empty_directories_admitted,
        test_zip_deflate_budget_limits_actual_output,
        test_input_blob_size_limit_creates_no_bundle,
        test_media_type_detection_hint_mismatch_and_source_kind_conflict,
        test_tar_and_unknown_blob_media_type_detection,
        test_implementation_manifest_mismatch_fails_before_bundle,
        test_implementation_manifest_must_pin_required_component_set,
        test_runtime_policy_must_match_pinned_implementation_policy,
        test_enterprise_validator_requires_policy_and_implementation_binding,
        test_enterprise_validator_binds_implementation_descriptor_to_manifest,
        test_enterprise_validator_rejects_unpinned_policy_file,
        test_policy_must_include_hazard_and_error_unsafe_severities,
        test_enterprise_validator_replays_policy_decision_and_reason_codes,
        test_enterprise_validator_rejects_unknown_hazard_admitted,
        test_enterprise_validator_rejects_policy_code_downgraded_to_warning_admitted,
        test_enterprise_validator_requires_source_kind_media_type_finding,
        test_enterprise_validator_rejects_contradictory_hint_match,
        test_enterprise_validator_rejects_not_comparable_hint_match,
        test_enterprise_validator_rejects_not_comparable_even_when_hint_matches,
        test_enterprise_validator_rejects_locator_hint_basis,
        test_enterprise_validator_rejects_tree_pdf_magic_content_type,
        test_enterprise_validator_rejects_tree_fallback_content_type,
        test_enterprise_validator_rejects_zip_with_fallback_basis,
        test_enterprise_validator_rejects_admitted_blob_container_parser,
        test_enterprise_validator_rejects_container_parser_without_archive_safety,
    ]
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        for test in tests:
            case_dir = root / test.__name__
            case_dir.mkdir(parents=True, exist_ok=True)
            test(case_dir)
        print(json.dumps({"passed": len(tests), "tests": [test.__name__ for test in tests]}, allow_nan=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
