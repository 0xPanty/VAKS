#!/usr/bin/env python
"""Normalize legacy Source Intake machine fields.

This is a mechanical migration for enum drift discovered by
validate_source_intake_contract.py. It only changes frontmatter machine fields;
it does not change prose conclusions, source summaries, review text, or
candidate claims.
"""

from __future__ import annotations

import argparse
from pathlib import Path


CURRENT_GLOBS = [
    "SOURCE_INTAKE.md",
    "templates/*.md",
    "raw/**/*.md",
    "outputs/qa/**/*.md",
    "outputs/feedback/**/*.md",
    "outputs/review/*candidate-distillation.md",
    "outputs/review/*refresh.md",
    "outputs/review/*query-run*.md",
    "outputs/review/*context-pack*.md",
    "outputs/review/*feedback*.md",
    "outputs/review/*overlay*.md",
    "outputs/review/project_overlays/**/*.md",
]

REPLACEMENTS = {
    "record_type: query-run": "record_kind: query_run_trace",
    "type: source_record": "type: source_record",
    "type: candidate_distillation": "type: candidate_distillation",
    "type: candidate_distillation_refresh": "type: candidate_distillation_refresh",
    "type: project_lens_overlay": "type: project_lens_overlay",
    "record_kind: source_record": "record_kind: source_card",
    "record_kind: video_source_card": "record_kind: source_card",
    "record_kind: source_snapshot_index": "record_kind: source_card",
    "record_kind: project_lens_overlay": "record_kind: project_overlay",
    "overlay_state: candidate_only": "overlay_state: none",
    "overlay_state: candidate": "overlay_state: none",
    "overlay_state: project_sidecar_created": "overlay_state: none",
    "review_pressure: local_benchmark_required": "review_pressure: review_due",
    "review_pressure: local_pilot_required": "review_pressure: review_due",
    "  policy_kind: candidate_only": "  policy_kind: orientation_only",
    "  policy_kind: source_with_candidate_comprehension": "  policy_kind: source_identity_only",
    "  pack_allowed: context_with_warning": "  pack_allowed: activation_only",
    "  warning_code: candidate_not_reviewed": "  warning_code: candidate_not_action_basis",
    "  warning_code: raw_snapshot_only": "  warning_code: raw_is_provenance_only",
    "promotion_gate: evidence_aware_review_required": "promotion_gate: v0_2_13_required",
    "promotion_gate: evidence_aware_review_and_local_benchmark_required": "promotion_gate: v0_2_13_required",
    "promotion_gate: evidence_aware_review_and_sandbox_required": "promotion_gate: v0_2_13_required",
    "promotion_gate: retrieval_layer_comparison_and_sandbox_required": "promotion_gate: v0_2_13_required",
}

TYPE_TO_RECORD_KIND = {
    "source": "source_card",
    "source_record": "source_card",
    "source_annotation": "source_annotation",
    "candidate_distillation": "candidate_distillation",
    "candidate_distillation_refresh": "candidate_distillation",
    "project_lens_overlay": "project_overlay",
}

LEGACY_PRESERVING_REPLACEMENTS = {
    "record_kind: source_record": ("legacy_record_kind", "source_record", "pure_rename"),
    "record_kind: video_source_card": ("legacy_record_kind", "video_source_card", "pure_rename"),
    "record_kind: source_snapshot_index": ("legacy_record_kind", "source_snapshot_index", "semantic_compression"),
    "record_kind: project_lens_overlay": ("legacy_record_kind", "project_lens_overlay", "pure_rename"),
    "overlay_state: candidate_only": ("legacy_overlay_state", "candidate_only", "semantic_compression"),
    "overlay_state: candidate": ("legacy_overlay_state", "candidate", "semantic_compression"),
    "overlay_state: project_sidecar_created": ("legacy_overlay_state", "project_sidecar_created", "semantic_compression"),
    "review_pressure: local_benchmark_required": ("legacy_review_pressure", "local_benchmark_required", "semantic_compression"),
    "review_pressure: local_pilot_required": ("legacy_review_pressure", "local_pilot_required", "semantic_compression"),
    "  policy_kind: candidate_only": ("legacy_retrieval_policy_kind", "candidate_only", "semantic_compression"),
    "  policy_kind: source_with_candidate_comprehension": (
        "legacy_retrieval_policy_kind",
        "source_with_candidate_comprehension",
        "semantic_compression",
    ),
    "  pack_allowed: context_with_warning": ("legacy_retrieval_pack_allowed", "context_with_warning", "semantic_compression"),
    "  warning_code: candidate_not_reviewed": ("legacy_retrieval_warning_code", "candidate_not_reviewed", "semantic_shift"),
    "  warning_code: raw_snapshot_only": ("legacy_retrieval_warning_code", "raw_snapshot_only", "pure_rename"),
    "promotion_gate: evidence_aware_review_required": (
        "legacy_promotion_gate",
        "evidence_aware_review_required",
        "semantic_compression",
    ),
    "promotion_gate: evidence_aware_review_and_local_benchmark_required": (
        "legacy_promotion_gate",
        "evidence_aware_review_and_local_benchmark_required",
        "semantic_compression",
    ),
    "promotion_gate: evidence_aware_review_and_sandbox_required": (
        "legacy_promotion_gate",
        "evidence_aware_review_and_sandbox_required",
        "semantic_compression",
    ),
    "promotion_gate: retrieval_layer_comparison_and_sandbox_required": (
        "legacy_promotion_gate",
        "retrieval_layer_comparison_and_sandbox_required",
        "semantic_compression",
    ),
}


def split_frontmatter(text: str) -> tuple[list[str], list[str]] | None:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return lines[: idx + 1], lines[idx + 1 :]
    return None


def value_for(lines: list[str], key: str) -> str | None:
    prefix = f"{key}:"
    for raw in lines:
        line = raw.rstrip("\r\n")
        if line.startswith(prefix):
            value = line[len(prefix) :].strip()
            return value if value else None
    return None


def type_value(lines: list[str]) -> str | None:
    return value_for(lines, "type")


def has_key(lines: list[str], key: str) -> bool:
    prefix = f"{key}:"
    return any(raw.rstrip("\r\n").startswith(prefix) for raw in lines)


def insert_before_end(lines: list[str], additions: list[str]) -> list[str]:
    if not additions:
        return lines
    for idx in range(len(lines) - 1, 0, -1):
        if lines[idx].strip() == "---":
            newline = "\n" if lines[idx].endswith("\n") else ""
            return lines[:idx] + [line + newline for line in additions] + lines[idx:]
    return lines + [line + "\n" for line in additions]


def append_unique(additions: list[str], line: str) -> None:
    if line not in additions:
        additions.append(line)


def is_template_path(path: Path) -> bool:
    return "templates" in path.parts


def normalize_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    parts = split_frontmatter(text)
    if parts is None:
        return False
    fm, body = parts
    changed = False
    new_fm: list[str] = []
    legacy_additions: list[str] = []
    has_type_source = any(line.strip() == "type: source" for line in fm)
    has_record_kind = any(line.startswith("record_kind:") for line in (raw.rstrip("\r\n") for raw in fm))
    inferred_from_type = TYPE_TO_RECORD_KIND.get(type_value(fm) or "")
    inserted_record_kind = False
    for raw_line in fm:
        line = raw_line.rstrip("\r\n")
        newline = raw_line[len(line) :]
        if (has_type_source or inferred_from_type) and not has_record_kind and not inserted_record_kind and line.startswith("type:"):
            new_fm.append(raw_line)
            new_fm.append(f"record_kind: {inferred_from_type or 'source_card'}" + newline)
            inserted_record_kind = True
            changed = True
            continue
        if line.startswith("processing_mode:") or line.startswith("processing_level:"):
            changed = True
            continue
        replacement = REPLACEMENTS.get(line)
        if replacement is not None:
            legacy = LEGACY_PRESERVING_REPLACEMENTS.get(line)
            if legacy is not None:
                legacy_key, legacy_value, migration_kind = legacy
                if not has_key(fm, legacy_key):
                    append_unique(legacy_additions, f"{legacy_key}: {legacy_value}")
                if migration_kind == "semantic_compression" and not has_key(fm, "migration_note"):
                    append_unique(legacy_additions, "migration_note: legacy_enum_semantics_preserved_for_review")
            new_fm.append(replacement + newline)
            changed = True
        else:
            new_fm.append(raw_line)
    joined = "".join(new_fm)
    additions: list[str] = []
    is_source_card = "record_kind: source_card" in joined
    is_candidate = "record_kind: candidate_distillation" in joined
    is_overlay = "record_kind: project_overlay" in joined
    if is_source_card:
        repaired: list[str] = []
        for raw_line in new_fm:
            line = raw_line.rstrip("\r\n")
            newline = raw_line[len(line) :]
            if line.startswith("knowledge_status:") and line != "knowledge_status: raw":
                repaired.append("knowledge_status: raw" + newline)
                changed = True
            else:
                repaired.append(raw_line)
        new_fm = repaired
        if not has_key(new_fm, "knowledge_status"):
            additions.append("knowledge_status: raw")
        if not has_key(new_fm, "processing_tier"):
            additions.append("processing_tier: light")
        if not has_key(new_fm, "source_id"):
            sid = value_for(new_fm, "repo") or value_for(new_fm, "source_url") or value_for(new_fm, "url") or f"legacy:{path.stem}"
            additions.append(f"source_id: {sid}")
        if not has_key(new_fm, "source_url"):
            url = value_for(new_fm, "url")
            if url:
                additions.append(f"source_url: {url}")
        if (
            value_for(new_fm, "source_url") is None
            and value_for(new_fm, "raw_location") is None
            and not is_template_path(path)
        ):
            additions.append(f"raw_location: {path.as_posix()}")
        if not has_key(new_fm, "captured_at"):
            captured = value_for(new_fm, "retrieved") or value_for(new_fm, "captured") or "legacy_unknown"
            additions.append(f"captured_at: {captured}")
        if not has_key(new_fm, "title"):
            title = value_for(new_fm, "repo") or path.stem
            additions.append(f"title: {title}")
        if not has_key(new_fm, "why_saved"):
            additions.append("why_saved: see_body_or_legacy_record")
        if not has_key(new_fm, "retrieval_policy"):
            additions.extend(
                [
                    "retrieval_policy:",
                    "  policy_kind: source_identity_only",
                    "  pack_allowed: drilldown_required",
                    "  action_basis_allowed: false",
                    "  warning_code: raw_is_provenance_only",
                ]
            )
        if not has_key(new_fm, "promotion_gate"):
            additions.append("promotion_gate: none")
        if not has_key(new_fm, "action_basis_allowed"):
            additions.append("action_basis_allowed: false")
        if not has_key(new_fm, "truth_mutation_allowed"):
            additions.append("truth_mutation_allowed: false")
    if is_candidate:
        if not has_key(new_fm, "provisional"):
            additions.append("provisional: true")
    if is_overlay:
        if not has_key(new_fm, "overlay_state"):
            additions.append("overlay_state: confirmed")
        if not has_key(new_fm, "review_pressure"):
            additions.append("review_pressure: none")
        if not has_key(new_fm, "project_id"):
            project_id = value_for(new_fm, "project_ref") or "verified-action-knowledge-system"
            additions.append(f"project_id: {project_id}")
        if not has_key(new_fm, "target_ref"):
            target_ref = value_for(new_fm, "source_ref") or "see_derived_from_or_body"
            additions.append(f"target_ref: {target_ref}")
        if not has_key(new_fm, "project_borrow_scope"):
            additions.append("project_borrow_scope: see_target_layers_or_body")
        if not has_key(new_fm, "project_non_borrow_scope"):
            additions.append("project_non_borrow_scope: see_non_target_layers_or_body")
        if not has_key(new_fm, "project_reopen_trigger"):
            additions.append("project_reopen_trigger: review_if_project_scope_or_evidence_changes")
    if legacy_additions:
        additions = legacy_additions + additions
    if additions:
        new_fm = insert_before_end(new_fm, additions)
        changed = True
    if changed:
        path.write_text("".join(new_fm + body), encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    changed: list[str] = []
    seen: set[Path] = set()
    for pattern in CURRENT_GLOBS:
        for path in root.glob(pattern):
            if path.is_file() and path not in seen:
                seen.add(path)
                if normalize_file(path):
                    changed.append(str(path.relative_to(root)).replace("\\", "/"))
    print(f"normalized_files={len(changed)}")
    for rel in changed:
        print(rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
