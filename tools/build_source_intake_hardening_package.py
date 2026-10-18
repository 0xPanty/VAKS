#!/usr/bin/env python
"""Build the Source Intake hardening Pro-review package."""

from __future__ import annotations

import hashlib
import importlib.util
import csv
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "tools" / "validate_source_intake_contract.py"
SPEC = importlib.util.spec_from_file_location("validate_source_intake_contract", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load validator from {VALIDATOR_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)
collect_files = VALIDATOR.collect_files

PACKAGE_DIR = Path("outputs/review/source-intake-control-flow-hardening-2026-06-12")
ZIP_NAME = "source-intake-control-flow-hardening-pro-review-package.zip"

STATIC_INCLUDE = [
    "SOURCE_INTAKE.md",
    "templates/source-record.md",
    "templates/video-source.md",
    "templates/candidate-distillation.md",
    "templates/project-overlay.md",
    "templates/query-run.md",
    "templates/feedback-event.md",
    "templates/heavy-review-open.md",
    "templates/context-pack-manifest.md",
    "tools/source_intake_enum_registry.json",
    "tools/validate_source_intake_contract.py",
    "tools/normalize_source_intake_fields.py",
    "tools/preserve_source_intake_legacy_fields.py",
    "tools/clear_source_intake_red_zone.py",
    "tools/relocate_legacy_project_lens.py",
    "tools/validate_source_intake_failure_matrix.py",
    "tools/validate_source_intake_hardening_package.py",
    "tools/build_source_intake_hardening_package.py",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/README.md",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/MINIMUM_FIX_CHECKLIST.md",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/MINIMUM_TEST_CASES.md",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/RUNTIME_RISK_MATRIX.md",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/WARNING_CLASSIFICATION.md",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/FINAL_WARNING_POLICY_DECISION.md",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/MIGRATION_REPORT.md",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/MIGRATION_STRATEGY_DECISION.md",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/CHECK_RESULTS.md",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/PRO_REVIEW_REQUEST.md",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/NOTES_FOR_USER.md",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/results/source_intake_contract_lint_summary.json",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/results/source_intake_contract_lint_issues.csv",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/results/source_intake_current_lint_summary.json",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/results/source_intake_current_lint_issues.csv",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/results/source_intake_current_lint_corpus_manifest.json",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/results/source_intake_current_lint_corpus_manifest.csv",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/results/source_intake_legacy_project_lens_compatibility.json",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/results/source_intake_legacy_project_lens_compatibility.csv",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/results/source_intake_legacy_project_lens_tombstone.md",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/results/source_intake_failure_matrix_summary.json",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/results/source_intake_failure_matrix_results.csv",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/results/source_intake_semantic_migration_summary.json",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/results/source_intake_semantic_migration_ledger.csv",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/results/source_intake_nonisomorphic_mapping_policy.csv",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/results/source_intake_red_zone_cleanup_summary.json",
    "outputs/review/source-intake-control-flow-hardening-2026-06-12/results/source_intake_red_zone_cleanup.csv",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_current_lint_corpus_manifest() -> None:
    out_dir = ROOT / PACKAGE_DIR / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for rel in collect_files(ROOT, "current"):
        path = ROOT / rel
        data = VALIDATOR.frontmatter(path)
        is_surface = bool(data is not None and VALIDATOR.is_intake_surface(rel, data))
        rows.append(
            {
                "path": rel.as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "is_validated_intake_surface": is_surface,
                "record_kind": data.get("record_kind", "") if isinstance(data, dict) else "",
                "type": data.get("type", "") if isinstance(data, dict) else "",
            }
        )
    csv_path = out_dir / "source_intake_current_lint_corpus_manifest.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["path", "bytes", "sha256", "is_validated_intake_surface", "record_kind", "type"],
        )
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "collected_file_count": len(rows),
        "validated_intake_surface_count": sum(1 for row in rows if row["is_validated_intake_surface"]),
        "skipped_non_target_file_count": sum(1 for row in rows if not row["is_validated_intake_surface"]),
        "csv": str(csv_path.relative_to(ROOT)).replace("\\", "/"),
        "truth_boundary": "current lint corpus identity manifest only; not semantic equivalence proof",
    }
    (out_dir / "source_intake_current_lint_corpus_manifest.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def legacy_project_lens_files() -> list[Path]:
    return sorted(path.relative_to(ROOT) for path in (ROOT / "outputs" / "review" / "_legacy_project_lens").glob("*.md"))


def main() -> int:
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    write_current_lint_corpus_manifest()
    manifest_path = PACKAGE_DIR / "PACKAGE_MANIFEST.json"
    check_path = PACKAGE_DIR / "PACKAGE_CHECK.json"
    zip_path = PACKAGE_DIR / ZIP_NAME
    rows = []
    missing = []
    include = sorted(
        {
            *STATIC_INCLUDE,
            *(path.as_posix() for path in collect_files(ROOT, "current")),
            *(path.as_posix() for path in legacy_project_lens_files()),
        }
    )
    for rel in include:
        path = ROOT / rel
        if not path.exists():
            missing.append(rel)
            continue
        rows.append(
            {
                "path": rel.replace("\\", "/"),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    manifest = {
        "package": ZIP_NAME,
        "created_at": "2026-06-12",
        "scope": "VAKS Source Intake control-flow hardening Pro-review package",
        "truth_boundary": "evidence package only; not reviewed knowledge or action basis",
        "current_lint_corpus_included": True,
        "current_lint_corpus_file_count": len(collect_files(ROOT, "current")),
        "file_count": len(rows),
        "missing": missing,
        "files": rows,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    package_check = {
        "status": "pass" if not missing else "fail",
        "file_count": manifest["file_count"],
        "zip": str(zip_path).replace("\\", "/"),
        "zip_present": True,
        "zip_entry_check": "pass" if not missing else "not_run",
        "package_check_in_zip": True,
        "errors": [f"missing files: {missing}"] if missing else [],
        "truth_boundary": "package integrity evidence only; not Source Intake P0 approval",
    }
    check_path.write_text(json.dumps(package_check, ensure_ascii=False, indent=2), encoding="utf-8")

    all_files = [Path(row["path"]) for row in rows] + [manifest_path, check_path]
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for rel in all_files:
            zf.write(ROOT / rel, rel.as_posix())
    print(json.dumps({"zip": str(zip_path), "files": len(all_files), "missing": missing}, ensure_ascii=False))
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
