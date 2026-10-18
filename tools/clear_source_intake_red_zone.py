#!/usr/bin/env python
"""Clear Source Intake red-zone frontmatter fields after warning classification.

This is a mechanical migration for the current sandbox corpus:
- source-card top-level confidence -> source_integrity.capture_confidence
- source-card top-level relations -> candidate_relation_suggestions
- source-card soft authority-like triage fields -> legacy_raw_metadata
- confirmed-overlay sentinel placeholders -> project-local semantic strings

It does not promote any item to reviewed knowledge or action basis.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs/review/source-intake-control-flow-hardening-2026-06-12/results"
ISSUES = OUT_DIR / "source_intake_current_lint_issues.csv"
SOFT_SOURCE_AUTHORITY_FIELDS = {
    "cross_source_count",
    "freshness",
    "relevance",
    "source_quality",
}


def split_frontmatter(text: str) -> tuple[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    return text[4:end], text[end + 5 :]


def write_frontmatter(path: Path, raw: str, body: str) -> None:
    if not body.startswith("\n"):
        body = "\n" + body
    path.write_text("---\n" + raw.rstrip("\n") + "\n---" + body, encoding="utf-8")


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def load_yaml(raw: str) -> dict[str, Any]:
    data = yaml.safe_load(raw) or {}
    return data if isinstance(data, dict) else {}


def replace_top_level_line(lines: list[str], key: str, replacement: str) -> bool:
    prefix = f"{key}:"
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = f"{key}: {yaml_quote(replacement)}"
            return True
    return False


def move_top_level_confidence(lines: list[str]) -> bool:
    confidence_value: str | None = None
    out: list[str] = []
    for line in lines:
        if line.startswith("confidence:"):
            confidence_value = line.split(":", 1)[1].strip()
            continue
        out.append(line)
    if confidence_value is None:
        return False

    insert_idx = None
    for idx, line in enumerate(out):
        if line.startswith("evidence_level:"):
            insert_idx = idx + 1
            break
    if insert_idx is None:
        for idx, line in enumerate(out):
            if line.startswith("verification_status:"):
                insert_idx = idx + 1
                break
    if insert_idx is None:
        insert_idx = 0

    out[insert_idx:insert_idx] = [
        "source_integrity:",
        f"  capture_confidence: {confidence_value}",
    ]
    lines[:] = out
    return True


def rename_top_level_relations(lines: list[str]) -> bool:
    for idx, line in enumerate(lines):
        if line == "relations:":
            lines[idx] = "candidate_relation_suggestions:"
            return True
    return False


def move_soft_source_fields_to_legacy_raw_metadata(lines: list[str]) -> list[str]:
    moved: list[tuple[str, str]] = []
    out: list[str] = []
    for line in lines:
        if not line or line.startswith(" ") or ":" not in line:
            out.append(line)
            continue
        key, value = line.split(":", 1)
        if key in SOFT_SOURCE_AUTHORITY_FIELDS:
            moved.append((key, value.strip()))
            continue
        out.append(line)
    if not moved:
        return []

    out.append("legacy_raw_metadata:")
    for key, value in moved:
        out.append(f"  {key}: {value}")
    lines[:] = out
    return [key for key, _ in moved]


def first_ref(data: dict[str, Any]) -> str:
    for key in ["source_ref", "review_ref", "distillation_ref", "derived_view", "project_ref"]:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    derived = data.get("derived_from")
    if isinstance(derived, list):
        for value in derived:
            if isinstance(value, str) and value.strip():
                return value.strip()
    return f"project_overlay:{data.get('project_id', 'unknown')}"


def clear_overlay_placeholders(lines: list[str], data: dict[str, Any]) -> list[str]:
    project = data.get("project_id") or data.get("project_ref") or "active project"
    target = first_ref(data)
    replacements = {
        "target_ref": target,
        "project_borrow_scope": (
            f"For project {project}, borrow only the listed target_layers/target_hint "
            "and body Borrow Scope as orientation or review input, not reviewed support or action basis."
        ),
        "project_non_borrow_scope": (
            f"For project {project}, do not borrow listed non_target_layers/body non-borrow scope "
            "as reviewed truth, reviewed relation, or action basis."
        ),
        "project_reopen_trigger": (
            "Reopen if active project scope, source evidence, target layers, or review gate requirements change."
        ),
    }
    changed: list[str] = []
    for key, value in replacements.items():
        if data.get(key) in {
            "see_body_or_legacy_record",
            "see_target_layers_or_body",
            "see_non_target_layers_or_body",
            "review_if_project_scope_or_evidence_changes",
            "see_derived_from_or_body",
        }:
            if replace_top_level_line(lines, key, value):
                changed.append(key)
    return changed


def rows_by_path() -> dict[str, set[str]]:
    paths: dict[str, set[str]] = {}
    if not ISSUES.exists():
        return paths
    with ISSUES.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("severity") != "error" and row.get("check") != "source_card_authority_like_metadata":
                continue
            paths.setdefault(row["path"], set()).add(row["check"])
    return paths


def main() -> int:
    changes: list[dict[str, str]] = []
    for rel, checks in rows_by_path().items():
        path = ROOT / rel
        split = split_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
        if split is None:
            continue
        raw, body = split
        data = load_yaml(raw)
        lines = raw.splitlines()
        file_changes: list[str] = []

        if "source_card_confidence_not_namespaced" in checks and move_top_level_confidence(lines):
            file_changes.append("confidence_to_source_integrity.capture_confidence")
        if "source_card_relation_authority_metadata" in checks and rename_top_level_relations(lines):
            file_changes.append("relations_to_candidate_relation_suggestions")
        if "source_card_authority_like_metadata" in checks:
            moved_soft_fields = move_soft_source_fields_to_legacy_raw_metadata(lines)
            if moved_soft_fields:
                file_changes.append("soft_source_authority_fields_to_legacy_raw_metadata:" + ",".join(moved_soft_fields))
        if "confirmed_overlay_placeholder_value" in checks:
            file_changes.extend(f"overlay_placeholder:{field}" for field in clear_overlay_placeholders(lines, data))

        if file_changes:
            write_frontmatter(path, "\n".join(lines), body)
            changes.append({"path": rel, "changes": ";".join(file_changes)})

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUT_DIR / "source_intake_red_zone_cleanup.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["path", "changes"])
        writer.writeheader()
        writer.writerows(changes)
    summary = {
        "changed_files": len(changes),
        "truth_boundary": "mechanical frontmatter cleanup only; no reviewed truth promotion",
        "csv": str(csv_path.relative_to(ROOT)).replace("\\", "/"),
    }
    (OUT_DIR / "source_intake_red_zone_cleanup_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
