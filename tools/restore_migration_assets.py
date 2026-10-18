#!/usr/bin/env python3
"""Restore hash-pinned migration assets from the project's private GitHub release.

Default: verify local copies only. --download requires an authenticated gh CLI.
Does not extract archives, execute assets, or overwrite differing local files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "docs/migration/2026-10-19-release-assets.json"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def destination(relative: str) -> Path:
    rel = PurePosixPath(relative)
    if rel.is_absolute() or not rel.parts or any(p in ("..", ".") for p in rel.parts) or "\\" in relative or ":" in relative:
        raise ValueError(f"Unsafe manifest path: {relative}")
    target = ROOT.joinpath(*rel.parts)
    if not target.resolve().is_relative_to(ROOT):
        raise ValueError(f"Path escapes checkout: {relative}")
    if any(p.is_symlink() for p in (target, *target.parents) if p != ROOT and p.is_relative_to(ROOT)):
        raise ValueError(f"Symlink destination refused: {relative}")
    return target


def matches(path: Path, item: dict) -> bool:
    return path.is_file() and path.stat().st_size == item["bytes"] and digest(path) == item["sha256"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if args.download and not shutil.which("gh"):
        parser.error("Install GitHub CLI and run gh auth login first.")
    # Preflight every destination before any download or write.
    targets = [(item, destination(item["path"])) for item in manifest["assets"]]
    for item, target in targets:
        if target.exists() and not matches(target, item):
            parser.error(f"Existing file differs; refusing overwrite: {item['path']}")
        if Path(item["asset_name"]).name != item["asset_name"] or "/" in item["asset_name"] or "\\" in item["asset_name"]:
            parser.error("Invalid release asset name")
    missing = 0
    for item, target in targets:
        if not target.exists() and args.download:
            with tempfile.TemporaryDirectory(prefix="vaks-release-") as scratch:
                subprocess.run([
                    "gh", "release", "download", manifest["tag"],
                    "--repo", manifest["repository"], "--pattern", item["asset_name"],
                    "--dir", scratch,
                ], check=True)
                downloaded = Path(scratch) / item["asset_name"]
                if not matches(downloaded, item):
                    raise ValueError(f"Downloaded hash/size mismatch: {item['asset_name']}")
                target.parent.mkdir(parents=True, exist_ok=True)
                # Exclusive creation also prevents an unexpected concurrent overwrite.
                with downloaded.open("rb") as src, target.open("xb") as dst:
                    shutil.copyfileobj(src, dst)
        if matches(target, item):
            print(f"OK {item['path']}")
        else:
            missing += 1
            print(f"MISSING {item['path']}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
