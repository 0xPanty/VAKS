#!/usr/bin/env python
"""Build or verify the Source Capture implementation manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


MANIFEST_SCHEMA = "urn:vaks:schema:source-capture-implementation:v1"
MANIFEST_ID = "vaks.source-capture-envelope"
MANIFEST_VERSION = "1.0-alpha.1"
COMPONENT_PATHS = [
    "policies/source-capture/raw-intake-default-v1.json",
    "schemas/snapshot-hygiene-v1.schema.json",
    "schemas/source-capture-v1.schema.json",
    "tools/inspect_source_snapshot.py",
    "tools/source_intake_enum_registry.json",
    "tools/validate_source_capture_bundle.py",
]


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def canonical_json_bytes(obj: dict[str, Any]) -> bytes:
    return (json.dumps(obj, allow_nan=False, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def build_manifest(root: Path) -> dict[str, Any]:
    components: list[dict[str, str]] = []
    for rel in sorted(COMPONENT_PATHS):
        path = root / rel
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"component is missing: {rel}")
        if path.is_symlink():
            raise RuntimeError(f"component must not be a symlink: {rel}")
        components.append({"path": rel, "digest": digest_file(path)})
    return {
        "schema": MANIFEST_SCHEMA,
        "id": MANIFEST_ID,
        "version": MANIFEST_VERSION,
        "components": components,
        "runtime": {
            "language": "python",
            "minimum_version": "3.10",
        },
    }


def write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        os.replace(temp_name, path)
    except Exception:
        try:
            Path(temp_name).unlink(missing_ok=True)
        finally:
            raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build or verify the Source Capture implementation manifest.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", default="tools/source_capture_implementation_manifest.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    output = (root / args.output).resolve()
    manifest = build_manifest(root)
    expected = canonical_json_bytes(manifest)
    if args.check:
        if not output.exists():
            print(json.dumps({"status": "fail", "error": "implementation manifest is missing"}, sort_keys=True))
            return 1
        actual = output.read_bytes()
        if actual != expected:
            print(json.dumps({"status": "fail", "error": "implementation manifest is stale"}, sort_keys=True))
            return 1
        print(json.dumps({"status": "pass", "components": len(manifest["components"])}, sort_keys=True))
        return 0
    write_atomic(output, expected)
    print(json.dumps({"status": "pass", "output": str(output), "components": len(manifest["components"])}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
