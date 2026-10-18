#!/usr/bin/env python
"""Recover legacy Source Intake enum semantics from git HEAD.

This script is a one-time safety net for the 2026-06-12 Source Intake
normalization pass. It compares tracked Markdown frontmatter in HEAD with the
current working tree, writes legacy_* fields for non-isomorphic enum mappings,
and emits an auditable old -> new ledger.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs" / "review" / "source-intake-control-flow-hardening-2026-06-12" / "results"
LEDGER = OUT_DIR / "source_intake_semantic_migration_ledger.csv"
SUMMARY = OUT_DIR / "source_intake_semantic_migration_summary.json"
MAPPING_POLICY = OUT_DIR / "source_intake_nonisomorphic_mapping_policy.csv"

MAPPINGS = [
    ("record_kind", "source_record", "source_card", "legacy_record_kind", "pure_rename"),
    ("record_kind", "video_source_card", "source_card", "legacy_record_kind", "pure_rename"),
    ("record_kind", "source_snapshot_index", "source_card", "legacy_record_kind", "semantic_compression"),
    ("record_kind", "project_lens_overlay", "project_overlay", "legacy_record_kind", "pure_rename"),
    ("overlay_state", "candidate_only", "none", "legacy_overlay_state", "semantic_compression"),
    ("overlay_state", "candidate", "none", "legacy_overlay_state", "semantic_compression"),
    ("overlay_state", "project_sidecar_created", "none", "legacy_overlay_state", "semantic_compression"),
    ("review_pressure", "local_benchmark_required", "review_due", "legacy_review_pressure", "semantic_compression"),
    ("review_pressure", "local_pilot_required", "review_due", "legacy_review_pressure", "semantic_compression"),
    ("retrieval_policy.policy_kind", "candidate_only", "orientation_only", "legacy_retrieval_policy_kind", "semantic_compression"),
    (
        "retrieval_policy.policy_kind",
        "source_with_candidate_comprehension",
        "source_identity_only",
        "legacy_retrieval_policy_kind",
        "semantic_compression",
    ),
    ("retrieval_policy.pack_allowed", "context_with_warning", "activation_only", "legacy_retrieval_pack_allowed", "semantic_compression"),
    ("retrieval_policy.warning_code", "candidate_not_reviewed", "candidate_not_action_basis", "legacy_retrieval_warning_code", "semantic_shift"),
    ("retrieval_policy.warning_code", "raw_snapshot_only", "raw_is_provenance_only", "legacy_retrieval_warning_code", "pure_rename"),
    ("promotion_gate", "evidence_aware_review_required", "v0_2_13_required", "legacy_promotion_gate", "semantic_compression"),
    (
        "promotion_gate",
        "evidence_aware_review_and_local_benchmark_required",
        "v0_2_13_required",
        "legacy_promotion_gate",
        "semantic_compression",
    ),
    (
        "promotion_gate",
        "evidence_aware_review_and_sandbox_required",
        "v0_2_13_required",
        "legacy_promotion_gate",
        "semantic_compression",
    ),
    (
        "promotion_gate",
        "retrieval_layer_comparison_and_sandbox_required",
        "v0_2_13_required",
        "legacy_promotion_gate",
        "semantic_compression",
    ),
]


def run_git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8", errors="replace")


def tracked_markdown_changed_files() -> list[Path]:
    out = run_git(["diff", "--name-only", "--", "*.md"])
    return sorted(Path(line.strip()) for line in out.splitlines() if line.strip())


def git_head_text(rel: Path) -> str | None:
    try:
        return run_git(["show", f"HEAD:{rel.as_posix()}"])
    except subprocess.CalledProcessError:
        return None


def split_frontmatter(text: str) -> tuple[list[str], str] | None:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            fm_text = "".join(lines[1:idx])
            return lines[: idx + 1], fm_text
    return None


def parse_frontmatter(text: str) -> dict[str, Any] | None:
    parts = split_frontmatter(text)
    if parts is None:
        return None
    _, fm_text = parts
    data = yaml.safe_load(fm_text) or {}
    return data if isinstance(data, dict) else {}


def field_value(data: dict[str, Any], field_path: str) -> Any:
    value: Any = data
    for part in field_path.split("."):
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value


def value_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def has_key(frontmatter_lines: list[str], key: str) -> bool:
    prefix = f"{key}:"
    return any(line.rstrip("\r\n").startswith(prefix) for line in frontmatter_lines)


def insert_before_end(frontmatter_lines: list[str], additions: list[str]) -> list[str]:
    if not additions:
        return frontmatter_lines
    for idx in range(len(frontmatter_lines) - 1, 0, -1):
        if frontmatter_lines[idx].strip() == "---":
            newline = "\n" if frontmatter_lines[idx].endswith("\n") else ""
            return frontmatter_lines[:idx] + [line + newline for line in additions] + frontmatter_lines[idx:]
    return frontmatter_lines


def append_unique(additions: list[str], line: str) -> None:
    if line not in additions:
        additions.append(line)


def update_file(rel: Path, rows: list[dict[str, str]], write: bool) -> int:
    current_path = ROOT / rel
    current_text = current_path.read_text(encoding="utf-8", errors="replace")
    old_text = git_head_text(rel)
    if old_text is None:
        return 0
    old_data = parse_frontmatter(old_text)
    current_data = parse_frontmatter(current_text)
    parts = split_frontmatter(current_text)
    if old_data is None or current_data is None or parts is None:
        return 0
    fm_lines, _ = parts
    additions: list[str] = []
    insertions = 0
    for field, old_value, new_value, legacy_field, migration_kind in MAPPINGS:
        if value_text(field_value(old_data, field)) != old_value:
            continue
        current_value = value_text(field_value(current_data, field))
        status = "mapped" if current_value == new_value else "current_value_differs"
        legacy_present = has_key(fm_lines, legacy_field)
        inserted = False
        if current_value == new_value and not legacy_present:
            append_unique(additions, f"{legacy_field}: {old_value}")
            if migration_kind == "semantic_compression" and not has_key(fm_lines, "migration_note"):
                append_unique(additions, "migration_note: legacy_enum_semantics_preserved_for_review")
            inserted = True
            insertions += 1
        rows.append(
            {
                "path": rel.as_posix(),
                "field": field,
                "old_value": old_value,
                "new_value": new_value,
                "current_value": current_value,
                "legacy_field": legacy_field,
                "migration_kind": migration_kind,
                "legacy_present_before": str(legacy_present).lower(),
                "legacy_inserted": str(inserted).lower(),
                "status": status,
                "source": "git_head_vs_worktree",
            }
        )
    if additions and write:
        body = current_text.splitlines(keepends=True)[len(fm_lines) :]
        current_path.write_text("".join(insert_before_end(fm_lines, additions) + body), encoding="utf-8")
    return insertions


def write_mapping_policy() -> None:
    fieldnames = ["field", "old_value", "new_value", "legacy_field", "migration_kind", "risk_note"]
    semantic_note = "not fully equivalent; preserve legacy value or review before relying on canonical value"
    pure_note = "mostly naming drift; legacy retained for audit when recovered"
    with MAPPING_POLICY.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for field, old_value, new_value, legacy_field, migration_kind in MAPPINGS:
            writer.writerow(
                {
                    "field": field,
                    "old_value": old_value,
                    "new_value": new_value,
                    "legacy_field": legacy_field,
                    "migration_kind": migration_kind,
                    "risk_note": pure_note if migration_kind == "pure_rename" else semantic_note,
                }
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rows: list[dict[str, str]] = []
    insertions = 0
    for rel in tracked_markdown_changed_files():
        insertions += update_file(rel, rows, write=not args.dry_run)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_mapping_policy()
    fieldnames = [
        "path",
        "field",
        "old_value",
        "new_value",
        "current_value",
        "legacy_field",
        "migration_kind",
        "legacy_present_before",
        "legacy_inserted",
        "status",
        "source",
    ]
    with LEDGER.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "status": "dry_run" if args.dry_run else "updated",
        "changed_tracked_markdown_files": len(tracked_markdown_changed_files()),
        "ledger_rows": len(rows),
        "legacy_insertions": insertions,
        "ledger": str(LEDGER.relative_to(ROOT)).replace("\\", "/"),
        "mapping_policy": str(MAPPING_POLICY.relative_to(ROOT)).replace("\\", "/"),
        "recoverability_note": (
            "Per-file old values can only be recovered where a tracked HEAD version exists. "
            "For already-normalized untracked/generated files, this package records the mapping policy "
            "but does not pretend to reconstruct lost old values."
        ),
        "truth_boundary": "migration audit only; legacy fields preserve old machine semantics for review, not authority",
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
