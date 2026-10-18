#!/usr/bin/env python
"""Validate the Source Intake hardening Pro-review package manifest and zip."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(".").resolve()
PACKAGE_DIR = Path("outputs/review/source-intake-control-flow-hardening-2026-06-12")
MANIFEST = PACKAGE_DIR / "PACKAGE_MANIFEST.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    zip_path = PACKAGE_DIR / manifest["package"]
    zip_present = zip_path.exists()
    if manifest.get("missing"):
        errors.append(f"manifest has missing files: {manifest['missing']}")
    for row in manifest["files"]:
        path = ROOT / row["path"]
        if not path.exists():
            errors.append(f"missing manifest file: {row['path']}")
            continue
        if path.stat().st_size != row["bytes"]:
            errors.append(f"size mismatch: {row['path']}")
        if sha256(path) != row["sha256"]:
            errors.append(f"sha256 mismatch: {row['path']}")
    zip_entry_check = "skipped_no_zip"
    package_check_in_zip = False
    if zip_present:
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = set(zf.namelist())
        expected = {row["path"] for row in manifest["files"]}
        expected.add(str(MANIFEST).replace("\\", "/"))
        expected.add(str(PACKAGE_DIR / "PACKAGE_CHECK.json").replace("\\", "/"))
        missing_in_zip = sorted(expected - names)
        if missing_in_zip:
            errors.append(f"zip missing entries: {missing_in_zip}")
            zip_entry_check = "fail"
        else:
            zip_entry_check = "pass"
        package_check_in_zip = str(PACKAGE_DIR / "PACKAGE_CHECK.json").replace("\\", "/") in names
    summary = {
        "status": "pass" if not errors else "fail",
        "file_count": manifest["file_count"],
        "zip": str(zip_path).replace("\\", "/"),
        "zip_present": zip_present,
        "zip_entry_check": zip_entry_check,
        "package_check_in_zip": package_check_in_zip,
        "errors": errors,
        "truth_boundary": "package integrity evidence only; not Source Intake P0 approval",
    }
    out_path = PACKAGE_DIR / "PACKAGE_CHECK.json"
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
