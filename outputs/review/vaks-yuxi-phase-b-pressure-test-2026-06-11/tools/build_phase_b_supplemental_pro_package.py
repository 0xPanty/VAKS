import hashlib
import json
import shutil
import zipfile
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
PACKAGE_DIR = SANDBOX_DIR / "pro-review-supplemental-package"
PACKAGE_ZIP = SANDBOX_DIR / "vaks-yuxi-phase-b-p0-p1-supplemental-pro-review-package.zip"
PACKAGE_MANIFEST = PACKAGE_DIR / "PACKAGE_MANIFEST.json"


PACKAGE_FILES = [
    "PRO_SUPPLEMENTAL_REVIEW_REQUEST.md",
    "PHASE_B_SUPPLEMENTAL_COMPLETION_AUDIT.md",
    "PHASE_B_P0_P1_SUPPLEMENTAL_PRESSURE_REPORT.md",
    "PHASE_B_P0_QUERY_LEVEL_REPLAY_REPORT.md",
    "PHASE_B_P0_QUERY_LEVEL_REPLAY_CHECK.md",
    "PHASE_B_METRIC_DICTIONARY.md",
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
    "PHASE_B_P1_ADVERSARIAL_AUDIT_REPORT.md",
    "PHASE_B_P1_ADVERSARIAL_AUDIT_CHECK.md",
    "PHASE_B_P1_PROMOTION_GATE_CALIBRATION_REPORT.md",
    "PHASE_B_P1_PROMOTION_GATE_CALIBRATION_CHECK.md",
    "PHASE_B_AGENT_BLIND_AUDIT_REPORT.md",
    "PHASE_B_AGENT_BLIND_AUDIT_CHECK.md",
    "PHASE_B_ORIGINAL_YUXI_RUNTIME_FEASIBILITY.md",
    "PHASE_B_EXTERNAL_VALIDATION_NEXT_STEPS.md",
    "PHASE_B_EXTERNAL_BLIND_QUERY_SET_KIT.md",
    "PHASE_B_EXTERNAL_BLIND_QUERY_SET_KIT_CHECK.md",
    "PHASE_B_READ_ONLY_ANSWER_LOOP_PILOT_SPEC.md",
    "PHASE_B_NEXT_STEP_SPECS_CHECK.md",
    "queries_phase_b.jsonl",
    "queries_phase_b_holdout.jsonl",
    "queries_phase_b_adversarial.jsonl",
    "queries_phase_b_agent_blind.jsonl",
    "queries_phase_b_blind_relevance.jsonl",
    "queries_phase_b_external_blind_template.jsonl",
    "task_plan.md",
    "progress.md",
    "findings.md",
    "results/phase_b_p0_summary.csv",
    "results/phase_b_p0_query_level_metrics.csv",
    "results/phase_b_p0_query_level_replay.csv",
    "results/phase_b_p0_query_level_replay_check.json",
    "results/phase_b_p0_clean_vaks_only_summary.csv",
    "results/phase_b_p0_clean_vaks_only_query_metrics.csv",
    "results/phase_b_metric_dictionary.json",
    "results/phase_b_frozen_corpus_manifest.json",
    "results/phase_b_frozen_corpus_manifest.csv",
    "results/phase_b_frozen_corpus_manifest_check.json",
    "results/phase_b_top11_20_item_receipts.csv",
    "results/phase_b_top11_20_item_receipts_summary.csv",
    "results/phase_b_top11_20_item_receipts_summary.json",
    "results/phase_b_top11_20_item_receipts_check.json",
    "results/phase_b_frozen_rerun_v2_manifest.json",
    "results/phase_b_frozen_rerun_v2_corpus_manifest.csv",
    "results/phase_b_frozen_rerun_v2_query_manifest.csv",
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
    "results/phase_b_p1_adversarial_combined_summary.csv",
    "results/phase_b_p1_adversarial_audit.json",
    "results/phase_b_p1_adversarial_audit_check.json",
    "results/phase_b_p1_adversarial_clean_vaks_only_summary.csv",
    "results/phase_b_p1_adversarial_clean_vaks_only_query_metrics.csv",
    "results/phase_b_adversarial_summary.csv",
    "results/phase_b_adversarial_query_metrics.csv",
    "results/phase_b_adversarial_top_results.csv",
    "results/phase_b_p1_promotion_gate_calibration_cases.jsonl",
    "results/phase_b_p1_promotion_gate_calibration_evaluations.jsonl",
    "results/phase_b_p1_promotion_gate_calibration_summary.json",
    "results/phase_b_p1_promotion_gate_calibration_check.json",
    "results/phase_b_agent_blind_summary.csv",
    "results/phase_b_agent_blind_query_metrics.csv",
    "results/phase_b_agent_blind_top_results.csv",
    "results/phase_b_agent_blind_combined_summary.csv",
    "results/phase_b_agent_blind_audit.json",
    "results/phase_b_agent_blind_audit_check.json",
    "results/phase_b_agent_blind_clean_vaks_only_summary.csv",
    "results/phase_b_agent_blind_clean_vaks_only_query_metrics.csv",
    "tools/run_phase_b_pressure.py",
    "tools/build_phase_b_p0_query_replay.py",
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
    "tools/build_phase_b_p1_adversarial_audit.py",
    "tools/validate_phase_b_p1_adversarial_audit.py",
    "tools/build_phase_b_p1_promotion_gate_calibration.py",
    "tools/validate_phase_b_p1_promotion_gate_calibration.py",
    "tools/build_phase_b_agent_blind_audit.py",
    "tools/validate_phase_b_agent_blind_audit.py",
    "tools/validate_phase_b_next_step_specs.py",
    "tools/build_phase_b_supplemental_pro_package.py",
    "tools/validate_phase_b_supplemental_pro_package.py",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_file(rel: str) -> dict:
    src = SANDBOX_DIR / rel
    if not src.exists():
        raise FileNotFoundError(rel)
    dst = PACKAGE_DIR / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {"path": rel, "bytes": dst.stat().st_size, "sha256": sha256(dst)}


def main() -> None:
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    records = [copy_file(rel) for rel in PACKAGE_FILES]
    manifest = {
        "artifact_kind": "phase_b_p0_p1_supplemental_pro_review_package_manifest",
        "created_at": "2026-06-11",
        "truth_boundary": "package_manifest_not_decision",
        "action_basis_allowed": False,
        "file_count": len(records),
        "files": records,
    }
    PACKAGE_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    with zipfile.ZipFile(PACKAGE_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for record in records:
            archive.write(PACKAGE_DIR / record["path"], record["path"])
        archive.write(PACKAGE_MANIFEST, "PACKAGE_MANIFEST.json")
    print(f"package files: {len(records)}")
    print(f"zip bytes: {PACKAGE_ZIP.stat().st_size}")


if __name__ == "__main__":
    main()
