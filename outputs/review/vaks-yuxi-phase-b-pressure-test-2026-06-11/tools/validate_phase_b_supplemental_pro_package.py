import json
import zipfile
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
PACKAGE_DIR = SANDBOX_DIR / "pro-review-supplemental-package"
PACKAGE_ZIP = SANDBOX_DIR / "vaks-yuxi-phase-b-p0-p1-supplemental-pro-review-package.zip"
PACKAGE_MANIFEST = PACKAGE_DIR / "PACKAGE_MANIFEST.json"
CHECK_JSON = RESULTS_DIR / "phase_b_supplemental_pro_package_check.json"
CHECK_MD = SANDBOX_DIR / "PHASE_B_SUPPLEMENTAL_PRO_PACKAGE_CHECK.md"


REQUIRED_PACKAGE_FILES = {
    "PRO_SUPPLEMENTAL_REVIEW_REQUEST.md",
    "PHASE_B_SUPPLEMENTAL_COMPLETION_AUDIT.md",
    "PHASE_B_P0_P1_SUPPLEMENTAL_PRESSURE_REPORT.md",
    "PHASE_B_P0_QUERY_LEVEL_REPLAY_CHECK.md",
    "PHASE_B_FROZEN_CORPUS_MANIFEST.md",
    "PHASE_B_FROZEN_CORPUS_MANIFEST_CHECK.md",
    "PHASE_B_TOP11_20_ITEM_RECEIPTS_REPORT.md",
    "PHASE_B_TOP11_20_ITEM_RECEIPTS_CHECK.md",
    "PHASE_B_FROZEN_RERUN_V2_REPORT.md",
    "PHASE_B_FROZEN_RERUN_V2_CHECK.md",
    "PHASE_B_BLIND_RELEVANCE_PILOT_REPORT.md",
    "PHASE_B_BLIND_RELEVANCE_CHECK.md",
    "PHASE_B_BLIND_RELEVANCE_JUDGMENT_INSTRUCTIONS.md",
    "PHASE_B_INTERNAL_RELEVANCE_JUDGMENT_REPORT.md",
    "PHASE_B_EXTERNAL_RELEVANCE_JUDGMENT_KIT.md",
    "PHASE_B_EXTERNAL_RELEVANCE_JUDGMENT_KIT_CHECK.md",
    "PHASE_B_P1_ADVERSARIAL_AUDIT_CHECK.md",
    "PHASE_B_P1_PROMOTION_GATE_CALIBRATION_CHECK.md",
    "PHASE_B_AGENT_BLIND_AUDIT_REPORT.md",
    "PHASE_B_AGENT_BLIND_AUDIT_CHECK.md",
    "PHASE_B_ORIGINAL_YUXI_RUNTIME_FEASIBILITY.md",
    "PHASE_B_EXTERNAL_VALIDATION_NEXT_STEPS.md",
    "PHASE_B_EXTERNAL_BLIND_QUERY_SET_KIT.md",
    "PHASE_B_EXTERNAL_BLIND_QUERY_SET_KIT_CHECK.md",
    "PHASE_B_READ_ONLY_ANSWER_LOOP_PILOT_SPEC.md",
    "PHASE_B_NEXT_STEP_SPECS_CHECK.md",
    "results/phase_b_p0_query_level_replay.csv",
    "results/phase_b_frozen_corpus_manifest.json",
    "results/phase_b_frozen_corpus_manifest.csv",
    "results/phase_b_frozen_corpus_manifest_check.json",
    "results/phase_b_top11_20_item_receipts.csv",
    "results/phase_b_top11_20_item_receipts_summary.json",
    "results/phase_b_top11_20_item_receipts_check.json",
    "results/phase_b_frozen_rerun_v2_manifest.json",
    "results/phase_b_frozen_rerun_v2_top20_items.csv",
    "results/phase_b_frozen_rerun_v2_top1_10_replay.csv",
    "results/phase_b_frozen_rerun_v2_top11_20_receipts.csv",
    "results/phase_b_frozen_rerun_v2_query_metrics.csv",
    "results/phase_b_frozen_rerun_v2_summary.csv",
    "results/phase_b_frozen_rerun_v2_check.json",
    "results/phase_b_blind_relevance_manifest.json",
    "results/phase_b_blind_relevance_query_manifest.csv",
    "results/phase_b_blind_relevance_top20_items.csv",
    "results/phase_b_blind_relevance_judgment_packet.csv",
    "results/phase_b_blind_relevance_judgments.csv",
    "results/phase_b_blind_relevance_judged_summary.csv",
    "results/phase_b_blind_relevance_check.json",
    "results/phase_b_blind_relevance_external_judgment_template.csv",
    "results/phase_b_blind_relevance_external_judgment_mapping.csv",
    "results/phase_b_external_relevance_judgment_kit.json",
    "results/phase_b_external_relevance_judgment_kit_check.json",
    "results/phase_b_external_blind_query_author_manifest_template.json",
    "results/phase_b_external_blind_query_set_kit.json",
    "results/phase_b_external_blind_query_set_kit_check.json",
    "results/phase_b_next_step_specs_check.json",
    "queries_phase_b_external_blind_template.jsonl",
    "results/phase_b_p1_adversarial_combined_summary.csv",
    "results/phase_b_p1_promotion_gate_calibration_summary.json",
    "results/phase_b_agent_blind_combined_summary.csv",
    "results/phase_b_agent_blind_audit.json",
    "tools/validate_phase_b_p0_query_replay.py",
    "tools/build_phase_b_frozen_corpus_manifest.py",
    "tools/validate_phase_b_frozen_corpus_manifest.py",
    "tools/build_phase_b_top11_20_receipts.py",
    "tools/validate_phase_b_top11_20_receipts.py",
    "tools/build_phase_b_frozen_rerun_v2.py",
    "tools/validate_phase_b_frozen_rerun_v2.py",
    "tools/build_phase_b_blind_relevance_pilot.py",
    "tools/validate_phase_b_blind_relevance_pilot.py",
    "tools/build_phase_b_internal_relevance_judgments.py",
    "tools/build_phase_b_external_relevance_judgment_kit.py",
    "tools/validate_phase_b_external_relevance_judgment_kit.py",
    "tools/build_phase_b_external_blind_query_set_kit.py",
    "tools/validate_phase_b_external_blind_query_set_kit.py",
    "tools/validate_phase_b_p1_adversarial_audit.py",
    "tools/validate_phase_b_p1_promotion_gate_calibration.py",
    "tools/validate_phase_b_agent_blind_audit.py",
    "tools/build_phase_b_supplemental_pro_package.py",
    "tools/validate_phase_b_supplemental_pro_package.py",
}


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_md(result: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_supplemental_pro_package_check",
        f"status: {result['supplemental_pro_package_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: package_check_not_decision",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Supplemental Pro Package Check",
        "",
        "## Result",
        "",
        "```text",
        f"status: {result['supplemental_pro_package_status']}",
        f"error count: {result['error_count']}",
        f"package file count: {result['package_file_count']}",
        f"zip bytes: {result['zip_bytes']}",
        "```",
        "",
        "## Errors",
        "",
    ]
    if result["errors"]:
        lines.extend(f"- {item['code']}: {item['detail']}" for item in result["errors"])
    else:
        lines.append("- none")
    lines.append("")
    CHECK_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    errors: list[dict] = []
    for path in [PACKAGE_DIR, PACKAGE_ZIP, PACKAGE_MANIFEST]:
        if not path.exists():
            add_error(errors, "missing_package_artifact", str(path))
        elif path.is_file() and path.stat().st_size == 0:
            add_error(errors, "empty_package_artifact", str(path))

    manifest = read_json(PACKAGE_MANIFEST) if PACKAGE_MANIFEST.exists() else {}
    manifest_files = {item.get("path") for item in manifest.get("files", [])}
    missing_manifest = sorted(REQUIRED_PACKAGE_FILES - manifest_files)
    if missing_manifest:
        add_error(errors, "manifest_missing_required_files", ",".join(missing_manifest))

    zip_names: set[str] = set()
    zip_bytes = PACKAGE_ZIP.stat().st_size if PACKAGE_ZIP.exists() else 0
    if PACKAGE_ZIP.exists():
        with zipfile.ZipFile(PACKAGE_ZIP) as archive:
            bad = archive.testzip()
            if bad:
                add_error(errors, "zip_integrity_bad_member", bad)
            zip_names = {name.rstrip("/") for name in archive.namelist() if not name.endswith("/")}
    missing_zip = sorted(REQUIRED_PACKAGE_FILES - zip_names)
    if missing_zip:
        add_error(errors, "zip_missing_required_files", ",".join(missing_zip))

    p0 = read_json(RESULTS_DIR / "phase_b_p0_query_level_replay_check.json")
    p1 = read_json(RESULTS_DIR / "phase_b_p1_adversarial_audit_check.json")
    gate = read_json(RESULTS_DIR / "phase_b_p1_promotion_gate_calibration_check.json")
    blind = read_json(RESULTS_DIR / "phase_b_agent_blind_audit_check.json")
    frozen = read_json(RESULTS_DIR / "phase_b_frozen_corpus_manifest_check.json")
    top_receipts = read_json(RESULTS_DIR / "phase_b_top11_20_item_receipts_check.json")
    frozen_v2 = read_json(RESULTS_DIR / "phase_b_frozen_rerun_v2_check.json")
    blind_relevance = read_json(RESULTS_DIR / "phase_b_blind_relevance_check.json")
    external_relevance = read_json(RESULTS_DIR / "phase_b_external_relevance_judgment_kit_check.json")
    external_blind_queries = read_json(RESULTS_DIR / "phase_b_external_blind_query_set_kit_check.json")
    next_specs = read_json(RESULTS_DIR / "phase_b_next_step_specs_check.json")
    status_checks = {
        "p0_query_replay": (p0.get("p0_query_replay_check_status"), p0.get("error_count")),
        "frozen_corpus_manifest": (frozen.get("frozen_corpus_manifest_check_status"), frozen.get("error_count")),
        "top11_20_item_receipts": (top_receipts.get("top11_20_item_receipts_check_status"), top_receipts.get("error_count")),
        "frozen_rerun_v2": (frozen_v2.get("frozen_rerun_v2_check_status"), frozen_v2.get("error_count")),
        "blind_relevance_packet": (
            blind_relevance.get("blind_relevance_check_status"),
            blind_relevance.get("error_count"),
        ),
        "external_relevance_judgment_kit": (
            external_relevance.get("external_relevance_judgment_kit_check_status"),
            external_relevance.get("error_count"),
        ),
        "external_blind_query_set_kit": (
            external_blind_queries.get("external_blind_query_set_kit_check_status"),
            external_blind_queries.get("error_count"),
        ),
        "p1_adversarial": (p1.get("p1_adversarial_check_status"), p1.get("error_count")),
        "p1_promotion_gate_calibration": (gate.get("calibration_check_status"), gate.get("error_count")),
        "agent_blind": (blind.get("agent_blind_check_status"), blind.get("error_count")),
        "next_step_specs": (next_specs.get("next_step_specs_check_status"), next_specs.get("error_count")),
    }
    for name, (status, error_count) in status_checks.items():
        allowed_pending = name == "blind_relevance_packet" and status == "pending_judgment" and int(error_count or 0) == 0
        allowed_pending = allowed_pending or (
            name == "external_relevance_judgment_kit"
            and status == "pending_external_judgment"
            and int(error_count or 0) == 0
        )
        allowed_pending = allowed_pending or (
            name == "external_blind_query_set_kit"
            and status == "pending_external_queries"
            and int(error_count or 0) == 0
        )
        if not allowed_pending and (status != "pass" or int(error_count or 0) != 0):
            add_error(errors, "required_check_not_pass", f"{name}:{status}/{error_count}")

    result = {
        "supplemental_pro_package_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "package_dir": str(PACKAGE_DIR),
        "package_zip": str(PACKAGE_ZIP),
        "package_file_count": int(manifest.get("file_count") or len(manifest_files)),
        "zip_bytes": zip_bytes,
        "required_checks": status_checks,
    }
    CHECK_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_md(result)
    print(f"supplemental pro package status: {result['supplemental_pro_package_status']}")
    print(f"error count: {result['error_count']}")
    print(f"zip bytes: {zip_bytes}")


if __name__ == "__main__":
    main()
