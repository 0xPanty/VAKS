from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "samples"
RESULTS = ROOT / "results"
ANNOTATIONS = SAMPLES / "annotations"
MUTATIONS = SAMPLES / "mutations"


ALLOWED_ANCHOR_STATUS = {
    "exact_verified",
    "fuzzy_recovered",
    "ambiguous",
    "broken",
    "source_changed",
}
ALLOWED_LIFECYCLE = {
    "source_annotated",
    "triaged",
    "routed",
    "repair_needed",
    "repair_candidate",
    "repaired",
    "archived",
}
ALLOWED_ROLES = {
    "question",
    "possible_support",
    "counterexample",
    "scope_limit",
    "risk_signal",
    "candidate_seed",
    "term_definition",
    "implementation_note",
    "bookmark",
}
BAD_ANCHORS = {"ambiguous", "broken", "source_changed"}
FORBIDDEN_FIELDS = {
    "truth_confidence",
    "reviewed_relation",
    "project_borrow_scope",
    "project_non_borrow_scope",
    "decision_outcome",
    "final_support_refs",
    "support_refs",
}
REQUIRED_FIELDS = {
    "record_kind",
    "annotation_id",
    "source_ref",
    "selector_type",
    "annotation_role",
    "body_note",
    "anchor_status",
    "lifecycle_state",
    "support_checked",
    "evidence_support_status",
    "retrieval_policy",
    "action_basis_allowed",
    "truth_mutation_allowed",
}
STALE_CUTOFF = date(2026, 3, 16)


def read_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing frontmatter")
    _, fm, _ = text.split("---", 2)
    loaded = yaml.safe_load(fm)
    if not isinstance(loaded, dict):
        raise ValueError(f"{path}: frontmatter is not a map")
    return loaded


def read_source_text(record: dict[str, Any]) -> str:
    source_ref = record.get("source_ref")
    if not source_ref:
        return ""
    path = ROOT / source_ref
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def sha256_text(text: str) -> str:
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def scalar_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if value == "":
        return []
    return [value]


def selector_fingerprint(record: dict[str, Any]) -> str:
    parts = [
        str(record.get("source_ref", "")),
        str(record.get("selector_type", "")),
        str(record.get("selector_exact", "")),
        str(record.get("selector_position_start", "")),
        str(record.get("selector_position_end", "")),
        str(record.get("selector_timestamp_start", "")),
        str(record.get("selector_timestamp_end", "")),
        str(record.get("selector_line_start", "")),
        str(record.get("selector_line_end", "")),
    ]
    return "|".join(parts)


def is_stale(record: dict[str, Any]) -> bool:
    if record.get("anchor_stale") is True:
        return True
    raw = record.get("anchor_checked_at")
    if not raw:
        return True
    try:
        checked = date.fromisoformat(str(raw))
    except ValueError:
        return True
    return checked < STALE_CUTOFF


def add(errors: list[str], path: Path, msg: str) -> None:
    errors.append(f"{path.relative_to(ROOT).as_posix()}: {msg}")


def validate_record(path: Path, record: dict[str, Any], *, strict_ready: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    missing = sorted(field for field in REQUIRED_FIELDS if field not in record)
    for field in missing:
        add(errors, path, f"missing required field {field}")

    if record.get("record_kind") != "source_annotation":
        add(errors, path, "record_kind must be source_annotation")

    for field in sorted(FORBIDDEN_FIELDS.intersection(record.keys())):
        add(errors, path, f"forbidden field present: {field}")

    if record.get("annotation_role") not in ALLOWED_ROLES:
        add(errors, path, f"unknown annotation_role {record.get('annotation_role')!r}")
    if record.get("anchor_status") not in ALLOWED_ANCHOR_STATUS:
        add(errors, path, f"unknown anchor_status {record.get('anchor_status')!r}")
    if record.get("lifecycle_state") not in ALLOWED_LIFECYCLE:
        add(errors, path, f"unknown lifecycle_state {record.get('lifecycle_state')!r}")

    if record.get("action_basis_allowed") is not False:
        add(errors, path, "action_basis_allowed must be false")
    if record.get("truth_mutation_allowed") is not False:
        add(errors, path, "truth_mutation_allowed must be false")

    policy = record.get("retrieval_policy") or {}
    if not isinstance(policy, dict):
        add(errors, path, "retrieval_policy must be a map")
        policy = {}
    if policy.get("action_basis_allowed") is not False:
        add(errors, path, "retrieval_policy.action_basis_allowed must be false")
    if record.get("lifecycle_state") != "archived":
        if policy.get("pack_allowed") != "review_input_only":
            add(errors, path, "active annotation pack_allowed must be review_input_only")
        if policy.get("warning_code") != "annotation_not_support":
            add(errors, path, "warning_code must be annotation_not_support")
    else:
        if policy.get("policy_kind") != "archive_only":
            add(errors, path, "archived annotation must use archive_only policy")

    if record.get("support_checked") is True and not record.get("evidence_packet_ref"):
        add(errors, path, "support_checked true requires evidence_packet_ref")
    if record.get("evidence_support_status") != "not_checked" and record.get("support_checked") is not True:
        add(errors, path, "evidence_support_status requires support_checked true")

    anchor_status = record.get("anchor_status")
    lifecycle = record.get("lifecycle_state")
    stale = is_stale(record)
    if anchor_status in BAD_ANCHORS and lifecycle not in {"repair_needed", "repair_candidate", "archived"}:
        add(errors, path, f"{anchor_status} must be in repair lifecycle or archived")
    if anchor_status in BAD_ANCHORS and record.get("review_pressure") not in {"high", "blocked", "repair"}:
        add(errors, path, f"{anchor_status} must have high/blocked/repair review pressure")
    if stale and lifecycle != "archived" and record.get("review_pressure") == "none":
        add(errors, path, "stale active anchor must have review pressure")

    selector_type = record.get("selector_type")
    if selector_type == "TextQuoteSelector":
        if not record.get("selector_exact"):
            add(errors, path, "TextQuoteSelector requires selector_exact")
        if not record.get("selector_prefix") or not record.get("selector_suffix"):
            add(errors, path, "TextQuoteSelector requires prefix and suffix")
    elif selector_type == "timestamp":
        if not record.get("selector_timestamp_start") or not record.get("selector_timestamp_end"):
            add(errors, path, "timestamp selector requires start and end")
    elif selector_type == "line_range":
        if record.get("selector_line_start") is None or record.get("selector_line_end") is None:
            add(errors, path, "line_range selector requires line start and end")
    elif selector_type == "page_rect":
        if record.get("selector_page") is None or not record.get("selector_rect"):
            add(errors, path, "page_rect selector requires page and rect")

    source_text = read_source_text(record)
    if not source_text:
        add(errors, path, "source_ref cannot be resolved")
    else:
        current_hash = sha256_text(source_text)
        source_hash = record.get("source_hash")
        exact = str(record.get("selector_exact") or "")
        count = source_text.count(exact) if exact else 0
        if anchor_status == "exact_verified" and selector_type == "TextQuoteSelector":
            if count != 1:
                add(errors, path, f"exact_verified requires one exact match, got {count}")
            if source_hash != current_hash:
                add(errors, path, "exact_verified source_hash must match current source")
        if anchor_status == "ambiguous" and count < 2:
            add(errors, path, "ambiguous anchor should have multiple exact matches")
        if anchor_status == "broken" and count != 0:
            add(errors, path, "broken anchor should not have an exact current match")
        if anchor_status == "source_changed" and source_hash == current_hash:
            add(errors, path, "source_changed requires source_hash drift")

    if lifecycle == "archived" and policy.get("pack_allowed") == "review_input_only":
        add(errors, path, "archived annotation cannot be default pack allowed")

    if strict_ready and record.get("body_note") in {None, ""}:
        add(errors, path, "body_note cannot be empty")

    return errors, warnings


def build_views(records: list[tuple[Path, dict[str, Any]]]) -> dict[str, list[str]]:
    views: dict[str, list[str]] = defaultdict(list)
    active_records = [
        record for _, record in records if record.get("lifecycle_state") != "archived"
    ]
    source_counts = Counter(str(record.get("source_ref")) for record in active_records)
    selector_counts = Counter(selector_fingerprint(record) for record in active_records)
    for path, record in records:
        ann_id = record.get("annotation_id")
        anchor = record.get("anchor_status")
        lifecycle = record.get("lifecycle_state")
        support_checked = record.get("support_checked")
        pressure = record.get("review_pressure")
        stale = is_stale(record)
        if lifecycle != "archived" and anchor not in BAD_ANCHORS and not stale:
            views["annotation_inbox"].append(ann_id)
        if lifecycle != "archived":
            views["source_drilldown"].append(ann_id)
        if scalar_list(record.get("project_overlay_refs")) and lifecycle != "archived":
            views["project_lens"].append(ann_id)
        if lifecycle != "archived" and support_checked is False and pressure != "none":
            views["routing_queue"].append(ann_id)
        if anchor in BAD_ANCHORS and lifecycle != "archived":
            views["needs_anchor_repair"].append(ann_id)
        if support_checked is True:
            views["support_checked_audit"].append(ann_id)
        if lifecycle != "archived" and stale:
            views["stale_anchor_queue"].append(ann_id)
        if lifecycle != "archived" and (
            record.get("source_digest_required") is True
            or source_counts[str(record.get("source_ref"))] > 15
            or selector_counts[selector_fingerprint(record)] > 3
        ):
            views["scale_debt"].append(ann_id)
        policy = record.get("retrieval_policy") or {}
        if (
            lifecycle != "archived"
            and not stale
            and anchor in {"exact_verified", "fuzzy_recovered"}
            and record.get("action_basis_allowed") is False
            and policy.get("warning_code") == "annotation_not_support"
        ):
            views["ai_export_ready"].append(ann_id)
        if anchor in BAD_ANCHORS or record.get("action_basis_allowed") is True or record.get("truth_mutation_allowed") is True:
            views["ai_export_blocked"].append(ann_id)
        if lifecycle == "archived":
            views["cold_archive"].append(ann_id)
    return {key: sorted(value) for key, value in sorted(views.items())}


def validate_density(records: list[tuple[Path, dict[str, Any]]]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for _, record in records:
        if record.get("lifecycle_state") != "archived":
            by_source[str(record.get("source_ref"))].append(record)
    for source_ref, items in sorted(by_source.items()):
        if len(items) > 15 and not any(item.get("source_digest_required") is True for item in items):
            errors.append(f"{source_ref}: {len(items)} active annotations but no source_digest_required route")
        elif len(items) > 15:
            warnings.append(f"{source_ref}: {len(items)} active annotations; source digest route present")
    return errors, warnings


def validate_duplicates(records: list[tuple[Path, dict[str, Any]]]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    ids = Counter(str(record.get("annotation_id")) for _, record in records)
    for ann_id, count in sorted(ids.items()):
        if count > 1:
            errors.append(f"duplicate annotation_id {ann_id}: {count}")
    fingerprints = Counter(
        selector_fingerprint(record)
        for _, record in records
        if record.get("lifecycle_state") != "archived"
    )
    for fingerprint, count in sorted(fingerprints.items()):
        if count > 3:
            warnings.append(f"selector duplicate pressure {count}x: {fingerprint[:120]}")
    return errors, warnings


def source_excerpt(record: dict[str, Any], window: int = 120) -> str:
    text = read_source_text(record)
    exact = str(record.get("selector_exact") or "")
    if not text or not exact:
        return ""
    pos = text.find(exact)
    if pos == -1:
        return ""
    start = max(0, pos - window)
    end = min(len(text), pos + len(exact) + window)
    return re.sub(r"\s+", " ", text[start:end]).strip()


def build_context_pack(records: list[tuple[Path, dict[str, Any]]], views: dict[str, list[str]]) -> dict[str, Any]:
    by_id = {record.get("annotation_id"): (path, record) for path, record in records}
    selected_ids = views.get("ai_export_ready", [])[:6]
    selected_items = []
    spans = []
    for ann_id in selected_ids:
        path, record = by_id[ann_id]
        policy = record.get("retrieval_policy") or {}
        selected_items.append(
            {
                "ref": path.relative_to(ROOT).as_posix(),
                "record_kind": "source_annotation",
                "knowledge_status": record.get("knowledge_status"),
                "pack_role": "review_input",
                "source_ref": record.get("source_ref"),
                "annotation_role": record.get("annotation_role"),
                "anchor_status": record.get("anchor_status"),
                "support_checked": record.get("support_checked"),
                "evidence_support_status": record.get("evidence_support_status"),
                "evidence_packet_ref": record.get("evidence_packet_ref") or None,
                "action_basis_allowed": False,
                "warning_code": policy.get("warning_code"),
                "selected_by": {
                    "metadata": True,
                    "lexical": True,
                    "semantic": False,
                    "graph": False,
                },
            }
        )
        spans.append(
            {
                "anchor_ref": f"{record.get('source_ref')}#{record.get('annotation_id')}",
                "source_ref": record.get("source_ref"),
                "excerpt": source_excerpt(record),
                "may_count_as_support": False,
                "support_check_required": True,
            }
        )
    return {
        "context_pack_id": "ctx-source-annotation-scale-sandbox-001",
        "query": {
            "summary": "sandbox export for annotation workbench scale test",
            "mode": "orientation",
            "active_project": "VAKS",
        },
        "authority_gate": {
            "included_buckets": ["source_annotation", "raw_source"],
            "action_basis_requested": False,
            "action_basis_allowed": False,
        },
        "selected_items": selected_items,
        "resolved_source_spans": spans,
        "coverage_overview": {
            "supported": 0,
            "weakly_supported": 0,
            "challenged": 0,
            "missing_evidence": len(selected_items),
            "out_of_scope": 0,
            "risk_flags": ["annotation_not_support"],
        },
        "coverage_map": [],
        "evidence_sufficiency": {
            "state": "insufficient",
            "checked_for": "context_pack",
            "required_next_step": "needs_review",
        },
        "action_readiness": {
            "state": "not_ready",
            "reason": "source annotations are locators, not evidence support",
        },
        "warnings": ["annotation_not_support"],
    }


def validate_context_pack(pack: dict[str, Any], *, expect_failure: bool = False) -> list[str]:
    errors: list[str] = []
    for item in pack.get("selected_items", []):
        if item.get("record_kind") == "source_annotation" and item.get("pack_role") == "support":
            errors.append("source_annotation cannot be selected as support")
        if item.get("record_kind") == "source_annotation" and item.get("action_basis_allowed") is not False:
            errors.append("source_annotation action_basis_allowed must be false in context pack")
        if item.get("record_kind") == "source_annotation" and item.get("warning_code") != "annotation_not_support":
            errors.append("source_annotation context item missing annotation_not_support warning")
    for entry in pack.get("coverage_map", []):
        for ref in scalar_list(entry.get("support_refs")):
            if "samples/annotations/" in str(ref) or "source_annotations/" in str(ref):
                errors.append("coverage_map support_refs cannot point to source_annotation")
    for span in pack.get("resolved_source_spans", []):
        if span.get("may_count_as_support") is not False:
            errors.append("resolved source spans from annotation pack may_count_as_support must be false")
        if span.get("support_check_required") is not True:
            errors.append("resolved source spans must require support check")
    if not expect_failure and "annotation_not_support" not in pack.get("warnings", []):
        errors.append("context pack missing annotation_not_support warning")
    return errors


def build_source_health_report(records: list[tuple[Path, dict[str, Any]]], views: dict[str, list[str]]) -> list[dict[str, Any]]:
    by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for _, record in records:
        by_source[str(record.get("source_ref"))].append(record)
    rows = []
    ai_ready = set(views.get("ai_export_ready", []))
    repair = set(views.get("needs_anchor_repair", []))
    stale = set(views.get("stale_anchor_queue", []))
    scale_debt = set(views.get("scale_debt", []))
    for source_ref, items in sorted(by_source.items()):
        ids = [str(item.get("annotation_id")) for item in items]
        rows.append(
            {
                "source_ref": source_ref,
                "total": len(items),
                "active": sum(1 for item in items if item.get("lifecycle_state") != "archived"),
                "ai_export_ready": sum(1 for ann_id in ids if ann_id in ai_ready),
                "needs_anchor_repair": sum(1 for ann_id in ids if ann_id in repair),
                "stale_anchor": sum(1 for ann_id in ids if ann_id in stale),
                "scale_debt": sum(1 for ann_id in ids if ann_id in scale_debt),
                "digest_required": any(item.get("source_digest_required") is True for item in items),
            }
        )
    return rows


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True), encoding="utf-8")


def write_md_report(report: dict[str, Any]) -> None:
    lines = [
        "---",
        "record_kind: sandbox_validation_report",
        "status: complete" if report["passed"] else "failed",
        "created_at: 2026-06-14",
        "---",
        "",
        "# Source Annotation Sandbox Validation Report",
        "",
        f"- Passed: {report['passed']}",
        f"- Good annotations: {report['good_annotation_count']}",
        f"- Good errors: {len(report['errors'])}",
        f"- Warnings: {len(report['warnings'])}",
        f"- Mutation annotations caught: {report['mutation_annotations_caught']} / {report['mutation_annotation_count']}",
        f"- Bad context pack caught: {report['bad_context_pack_caught']}",
        "",
        "## View Counts",
        "",
    ]
    for name, ids in report["views"].items():
        lines.append(f"- {name}: {len(ids)}")
    lines.extend(["", "## Errors", ""])
    if report["errors"]:
        lines.extend(f"- {error}" for error in report["errors"])
    else:
        lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    if report["warnings"]:
        lines.extend(f"- {warning}" for warning in report["warnings"])
    else:
        lines.append("- none")
    lines.extend(["", "## Mutation Results", ""])
    for item in report["mutation_results"]:
        status = "caught" if item["caught"] else "missed"
        lines.append(f"- {item['file']}: {status} ({item['error_count']} errors)")
    lines.append("")
    (RESULTS / "validation-report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    records = [(path, read_frontmatter(path)) for path in sorted(ANNOTATIONS.glob("*.md"))]
    errors: list[str] = []
    warnings: list[str] = []
    for path, record in records:
        record_errors, record_warnings = validate_record(path, record, strict_ready=True)
        errors.extend(record_errors)
        warnings.extend(record_warnings)

    density_errors, density_warnings = validate_density(records)
    duplicate_errors, duplicate_warnings = validate_duplicates(records)
    errors.extend(density_errors)
    errors.extend(duplicate_errors)
    warnings.extend(density_warnings)
    warnings.extend(duplicate_warnings)

    views = build_views(records)
    if set(views.get("needs_anchor_repair", [])) & set(views.get("ai_export_ready", [])):
        errors.append("bad anchors overlap with AI export ready")
    if set(views.get("cold_archive", [])) & set(views.get("ai_export_ready", [])):
        errors.append("archived annotations overlap with AI export ready")
    if set(views.get("stale_anchor_queue", [])) & set(views.get("ai_export_ready", [])):
        errors.append("stale annotations overlap with AI export ready")

    context_pack = build_context_pack(records, views)
    context_errors = validate_context_pack(context_pack)
    errors.extend(f"context_pack: {error}" for error in context_errors)
    write_json(RESULTS / "context-pack-sample.json", context_pack)
    (RESULTS / "context-pack-sample.md").write_text(
        "# Context Pack Sample\n\n"
        "This pack is orientation-only. Source annotations are review inputs, not support.\n\n"
        f"Selected items: {len(context_pack['selected_items'])}\n\n"
        "Warnings: annotation_not_support\n",
        encoding="utf-8",
    )

    source_health = build_source_health_report(records, views)
    write_json(RESULTS / "source-health-report.json", source_health)
    health_lines = [
        "---",
        "record_kind: sandbox_source_health_report",
        "status: complete",
        "created_at: 2026-06-14",
        "---",
        "",
        "# Source Health Report",
        "",
        "| Source | Total | Active | AI ready | Repair | Stale | Scale debt | Digest route |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in source_health:
        health_lines.append(
            f"| {row['source_ref']} | {row['total']} | {row['active']} | {row['ai_export_ready']} | {row['needs_anchor_repair']} | {row['stale_anchor']} | {row['scale_debt']} | {row['digest_required']} |"
        )
    (RESULTS / "source-health-report.md").write_text("\n".join(health_lines), encoding="utf-8")

    mutation_results = []
    good_ids = {str(record.get("annotation_id")) for _, record in records}
    mutation_caught = 0
    mutation_files = sorted(path for path in MUTATIONS.glob("*.md"))
    for path in mutation_files:
        mutation_record = read_frontmatter(path)
        mutation_errors, _ = validate_record(path, mutation_record, strict_ready=True)
        if str(mutation_record.get("annotation_id")) in good_ids:
            mutation_errors.append(
                f"{path.relative_to(ROOT).as_posix()}: duplicate annotation_id collides with good corpus"
            )
        caught = bool(mutation_errors)
        if caught:
            mutation_caught += 1
        mutation_results.append(
            {
                "file": path.relative_to(ROOT).as_posix(),
                "caught": caught,
                "error_count": len(mutation_errors),
                "errors": mutation_errors,
            }
        )

    bad_pack_path = MUTATIONS / "bad-context-pack.json"
    bad_pack = yaml.safe_load(bad_pack_path.read_text(encoding="utf-8"))
    bad_pack_errors = validate_context_pack(bad_pack, expect_failure=True)
    bad_context_pack_caught = bool(bad_pack_errors)

    passed = (
        not errors
        and mutation_caught == len(mutation_files)
        and bad_context_pack_caught
        and len(views.get("annotation_inbox", [])) > 0
        and len(views.get("needs_anchor_repair", [])) > 0
        and len(views.get("project_lens", [])) > 0
        and len(views.get("ai_export_ready", [])) > 0
        and len(views.get("stale_anchor_queue", [])) > 0
        and len(views.get("scale_debt", [])) > 0
    )

    report = {
        "passed": passed,
        "good_annotation_count": len(records),
        "errors": errors,
        "warnings": warnings,
        "views": views,
        "mutation_annotation_count": len(mutation_files),
        "mutation_annotations_caught": mutation_caught,
        "mutation_results": mutation_results,
        "bad_context_pack_caught": bad_context_pack_caught,
        "bad_context_pack_errors": bad_pack_errors,
    }
    write_json(RESULTS / "validation-report.json", report)
    write_json(RESULTS / "workbench-view-counts.json", views)
    write_md_report(report)
    print(json.dumps(report, indent=2, ensure_ascii=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
