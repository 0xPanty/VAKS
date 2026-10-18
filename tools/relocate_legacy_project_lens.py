#!/usr/bin/env python
"""Move legacy Project Lens overlays out of canonical Source Intake scope."""

from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "outputs" / "review" / "project_lens_overlays"
TARGET_DIR = ROOT / "outputs" / "review" / "_legacy_project_lens"
OUT_DIR = ROOT / "outputs" / "review" / "source-intake-control-flow-hardening-2026-06-12" / "results"
TOMBSTONE = OUT_DIR / "source_intake_legacy_project_lens_tombstone.md"


LEGACY_FIELDS = {
    "legacy_overlay_compatibility": True,
    "canonical_p0_included": False,
    "canonical_current_lint_scope": False,
    "legacy_storage": "outputs/review/_legacy_project_lens",
    "default_retrieval": False,
}


def ensure_inside_workspace(path: Path) -> None:
    root = ROOT.resolve()
    resolved = path.resolve()
    if root != resolved and root not in resolved.parents:
        raise RuntimeError(f"Refusing path outside workspace: {resolved}")


def split_frontmatter(text: str) -> tuple[dict, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    raw = text[4:end]
    body = text[end + 4 :]
    data = yaml.safe_load(raw) or {}
    return (data if isinstance(data, dict) else {}, body)


def dump_frontmatter(data: dict, body: str) -> str:
    raw = yaml.safe_dump(data, sort_keys=False, allow_unicode=True).strip()
    return f"---\n{raw}\n---{body}"


def mark_legacy(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    parsed = split_frontmatter(text)
    changed = False
    data: dict = {}
    if parsed is not None:
        data, body = parsed
        for key, value in LEGACY_FIELDS.items():
            if data.get(key) != value:
                data[key] = value
                changed = True
        if "truth_boundary" not in data:
            data["truth_boundary"] = "legacy project lens compatibility artifact only; not canonical overlay; not reviewed knowledge; not action basis"
            changed = True
        if changed:
            path.write_text(dump_frontmatter(data, body), encoding="utf-8")
    else:
        body = text

    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "type": data.get("type", "") if data else "",
        "record_kind": data.get("record_kind", "") if data else "",
        "legacy_overlay_compatibility": str(data.get("legacy_overlay_compatibility", "")) if data else "",
        "canonical_p0_included": str(data.get("canonical_p0_included", "")) if data else "",
        "canonical_current_lint_scope": str(data.get("canonical_current_lint_scope", "")) if data else "",
    }


def main() -> int:
    ensure_inside_workspace(SOURCE_DIR)
    ensure_inside_workspace(TARGET_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    moved: list[dict] = []
    if SOURCE_DIR.exists():
        for source in sorted(SOURCE_DIR.glob("*.md")):
            ensure_inside_workspace(source)
            target = TARGET_DIR / source.name
            ensure_inside_workspace(target)
            if target.exists():
                source.unlink()
                action = "removed_duplicate_source_after_existing_target"
            else:
                shutil.move(str(source), str(target))
                action = "moved"
            row = mark_legacy(target)
            row["source_path"] = source.relative_to(ROOT).as_posix()
            row["action"] = action
            moved.append(row)

    for target in sorted(TARGET_DIR.glob("*.md")):
        rows.append(mark_legacy(target))

    csv_path = OUT_DIR / "source_intake_legacy_project_lens_compatibility.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "path",
            "bytes",
            "type",
            "record_kind",
            "legacy_overlay_compatibility",
            "canonical_p0_included",
            "canonical_current_lint_scope",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    tombstone_lines = [
        "---",
        "type: source_intake_legacy_project_lens_tombstone",
        "status: archived_excluded",
        "created_at: 2026-06-12",
        "truth_boundary: tombstone only; not canonical overlay; not reviewed knowledge; not action basis",
        "---",
        "",
        "# Legacy Project Lens Tombstone",
        "",
        "These files were moved out of canonical Source Intake scope.",
        "",
        "```text",
        f"legacy_dir: {TARGET_DIR.relative_to(ROOT).as_posix()}",
        "canonical_current_lint_scope: false",
        "canonical_p0_included: false",
        "default_retrieval: false",
        "downstream_consumption_allowed: false",
        "```",
        "",
        "| Old path | Archived path | Reason |",
        "|---|---|---|",
    ]
    moved_by_target = {row["path"]: row.get("source_path", "") for row in moved}
    for row in rows:
        archived = row["path"]
        old = moved_by_target.get(archived, f"outputs/review/project_lens_overlays/{Path(archived).name}")
        tombstone_lines.append(
            f"| `{old}` | `{archived}` | excluded from canonical P0; retained only for audit/sandbox compatibility |"
        )
    TOMBSTONE.write_text("\n".join(tombstone_lines) + "\n", encoding="utf-8")

    summary = {
        "status": "compatibility_report",
        "legacy_file_count": len(rows),
        "moved_this_run": moved,
        "legacy_dir": TARGET_DIR.relative_to(ROOT).as_posix(),
        "canonical_current_lint_scope": False,
        "canonical_p0_included": False,
        "default_retrieval": False,
        "recommended_action": "migrate selected active-value files manually as gold examples, or keep excluded as audit/sandbox reference",
        "csv": csv_path.relative_to(ROOT).as_posix(),
        "tombstone": TOMBSTONE.relative_to(ROOT).as_posix(),
        "downstream_consumption_allowed": False,
        "truth_boundary": "legacy compatibility report only; not canonical overlay validation",
    }
    (OUT_DIR / "source_intake_legacy_project_lens_compatibility.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
