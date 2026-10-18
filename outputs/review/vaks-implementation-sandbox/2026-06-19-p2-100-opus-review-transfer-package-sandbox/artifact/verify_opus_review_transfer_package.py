import hashlib
import json
import sys
import zipfile
from pathlib import Path


SLICE_ID = "2026-06-19-p2-100-opus-review-transfer-package-sandbox"
SOURCE_SLICE_ID = "2026-06-19-p2-99-portable-opus-evidence-bundle-sandbox"

HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
REPO_ROOT = SLICE_DIR.parents[3]
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

ZIP_PATH = ARTIFACT_DIR / "opus-review-transfer-package.zip"
ZIP_SHA_PATH = ARTIFACT_DIR / "opus-review-transfer-package-sha256.txt"
EXTERNAL_MANIFEST_PATH = ARTIFACT_DIR / "opus-review-transfer-package-manifest.json"
TRANSFER_README_PATH = ARTIFACT_DIR / "opus-review-transfer-package-readme.md"
CONTENT_MANIFEST_PATH = ARTIFACT_DIR / "transfer-package-contents-manifest.json"

REQUIRED_ARCHIVE_PATHS = {
    "TRANSFER-README.md",
    "transfer-package-contents-manifest.json",
    "p2-99-portable-opus-evidence-bundle/artifact/portable-opus-evidence-bundle-manifest.json",
    "p2-99-portable-opus-evidence-bundle/artifact/portable-opus-evidence-bundle-readme.md",
    "p2-99-portable-opus-evidence-bundle/artifact/evidence-snapshots/p2-98-single-file-opus-review-dossier.md",
    "p2-99-portable-opus-evidence-bundle/verification.md",
    "p2-99-portable-opus-evidence-bundle/reviewer-report.md",
    "p2-99-portable-opus-evidence-bundle/boundary-audit.md",
    "p2-99-portable-opus-evidence-bundle/product-acceptance-report.md",
    "p2-99-portable-opus-evidence-bundle/next-step.md",
}

EXPECTED_FINAL_STATUSES = {
    "verification.md": "local_verification_passed",
    "reviewer-report.md": "review_pass_no_blocker",
    "boundary-audit.md": "pass_boundary",
    "product-acceptance-report.md": "pass_product_grade",
    "next-step.md": "pass_product_grade_pending_next_slice",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(path: Path, failures: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"json_load_failed:{path.name}:{exc}")
        return None


def frontmatter_status(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return "missing_frontmatter"
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def verify(final_gate: bool = False) -> dict:
    failures: list[str] = []
    for path in [
        ZIP_PATH,
        ZIP_SHA_PATH,
        EXTERNAL_MANIFEST_PATH,
        TRANSFER_README_PATH,
        CONTENT_MANIFEST_PATH,
        FAILURE_DIR / "opus-review-transfer-package-failures.json",
    ]:
        if not path.exists():
            failures.append(f"missing_required_file:{path.relative_to(SLICE_DIR).as_posix()}")

    manifest = load_json(EXTERNAL_MANIFEST_PATH, failures) if EXTERNAL_MANIFEST_PATH.exists() else None
    content_manifest = load_json(CONTENT_MANIFEST_PATH, failures) if CONTENT_MANIFEST_PATH.exists() else None

    zip_sha = None
    zip_names: set[str] = set()
    zip_bytes_by_name: dict[str, bytes] = {}
    if ZIP_PATH.exists():
        zip_sha = sha256_file(ZIP_PATH)
        try:
            with zipfile.ZipFile(ZIP_PATH, "r") as zf:
                zip_names = set(zf.namelist())
                for name in sorted(zip_names):
                    zip_bytes_by_name[name] = zf.read(name)
        except Exception as exc:
            failures.append(f"zip_read_failed:{exc}")

    if manifest:
        summary = manifest.get("summary", {})
        if manifest.get("record_kind") != "opus_review_transfer_package_manifest":
            failures.append("manifest_record_kind_mismatch")
        if manifest.get("slice_id") != SLICE_ID:
            failures.append("manifest_slice_id_mismatch")
        if manifest.get("source_slice_id") != SOURCE_SLICE_ID:
            failures.append("manifest_source_slice_id_mismatch")
        if summary.get("transfer_ready") is not True:
            failures.append("transfer_ready_not_true")
        if zip_sha and summary.get("zip_sha256") != zip_sha:
            failures.append("zip_sha_mismatch_manifest")
        if summary.get("actual_opus_result_present") is not False:
            failures.append("actual_opus_result_overclaim")
        if summary.get("opus_approval_claimed") is not False:
            failures.append("opus_approval_overclaim")
        if summary.get("mainline_ready") is not False:
            failures.append("mainline_ready_overclaim")
        if summary.get("goal_complete_now") is not False:
            failures.append("goal_complete_overclaim")
        flags = manifest.get("authority_flags", {})
        for key in [
            "actual_opus_result_present",
            "opus_approval_claimed",
            "mainline_ready",
            "reviewed_knowledge_ready",
            "evidence_support_ready",
            "action_basis_ready",
            "goal_complete_now",
        ]:
            if flags.get(key) is not False:
                failures.append(f"authority_flag_overclaim:{key}")

    if ZIP_SHA_PATH.exists() and zip_sha:
        sha_text = ZIP_SHA_PATH.read_text(encoding="utf-8").strip()
        if zip_sha not in sha_text or ZIP_PATH.name not in sha_text:
            failures.append("zip_sha_file_mismatch")

    if zip_names:
        for required in REQUIRED_ARCHIVE_PATHS:
            if required not in zip_names:
                failures.append(f"missing_archive_path:{required}")
        for name in zip_names:
            lower = name.lower()
            if "__pycache__" in name or lower.endswith((".pyc", ".pyo", ".tmp", ".temp")):
                failures.append(f"runtime_cache_or_temp_in_archive:{name}")
        if "transfer-package-contents-manifest.json" in zip_bytes_by_name:
            if sha256_bytes(zip_bytes_by_name["transfer-package-contents-manifest.json"]) != sha256_file(CONTENT_MANIFEST_PATH):
                failures.append("content_manifest_archive_hash_mismatch")

    if content_manifest:
        if content_manifest.get("record_kind") != "opus_review_transfer_package_contents_manifest":
            failures.append("content_manifest_record_kind_mismatch")
        if content_manifest.get("slice_id") != SLICE_ID:
            failures.append("content_manifest_slice_id_mismatch")
        items = content_manifest.get("content_items", [])
        if not items:
            failures.append("content_manifest_empty")
        for item in items:
            archive_path = item.get("archive_path")
            source_path = item.get("source_path")
            if not archive_path or not source_path:
                failures.append("content_item_missing_path")
                continue
            source_abs = REPO_ROOT / source_path
            if not source_abs.exists():
                failures.append(f"content_source_missing:{source_path}")
                continue
            source_sha = sha256_file(source_abs)
            if source_sha != item.get("source_sha256"):
                failures.append(f"content_source_hash_mismatch:{source_path}")
            if archive_path not in zip_bytes_by_name:
                failures.append(f"content_archive_missing:{archive_path}")
                continue
            archive_sha = sha256_bytes(zip_bytes_by_name[archive_path])
            if archive_sha != item.get("archive_sha256"):
                failures.append(f"content_archive_hash_mismatch:{archive_path}")
            if archive_sha != source_sha:
                failures.append(f"archive_source_hash_mismatch:{archive_path}")

    fixture_files = sorted(FIXTURES_DIR.glob("*.json"))
    if len(fixture_files) != 5:
        failures.append(f"fixture_count_mismatch:{len(fixture_files)}")
    for fixture_file in fixture_files:
        fixture = load_json(fixture_file, failures)
        if fixture and fixture.get("expected") is not True:
            failures.append(f"fixture_not_positive:{fixture_file.name}")

    failure_payload = (
        load_json(FAILURE_DIR / "opus-review-transfer-package-failures.json", failures)
        if (FAILURE_DIR / "opus-review-transfer-package-failures.json").exists()
        else None
    )
    failure_case_count = 0
    if failure_payload:
        failure_case_count = len(failure_payload.get("failure_cases", []))
        if failure_case_count < 10:
            failures.append(f"failure_case_count_too_low:{failure_case_count}")

    if TRANSFER_README_PATH.exists():
        readme = TRANSFER_README_PATH.read_text(encoding="utf-8")
        for phrase in [
            "not an Opus result",
            "not Opus approval",
            "not mainline readiness",
            "not reviewed knowledge",
            "not evidence support",
            "not action basis",
            "not goal completion",
        ]:
            if phrase not in readme:
                failures.append(f"missing_readme_boundary:{phrase}")

    if final_gate:
        for filename, expected in EXPECTED_FINAL_STATUSES.items():
            report_path = SLICE_DIR / filename
            if not report_path.exists():
                failures.append(f"final_gate_missing_report:{filename}")
                continue
            actual = frontmatter_status(report_path)
            if actual != expected:
                failures.append(f"final_gate_status:{filename}:expected={expected}:actual={actual}")

    summary = {
        "fixture_count": len(fixture_files),
        "failure_case_count": failure_case_count,
        "content_count": len(content_manifest.get("content_items", [])) if content_manifest else 0,
        "zip_present": ZIP_PATH.exists(),
        "zip_sha256": zip_sha,
        "transfer_ready": bool(manifest and manifest.get("summary", {}).get("transfer_ready") is True),
        "actual_opus_result_present": bool(manifest and manifest.get("summary", {}).get("actual_opus_result_present")),
        "opus_approval_claimed": bool(manifest and manifest.get("summary", {}).get("opus_approval_claimed")),
        "mainline_ready": bool(manifest and manifest.get("summary", {}).get("mainline_ready")),
        "goal_complete_now": bool(manifest and manifest.get("summary", {}).get("goal_complete_now")),
        "final_gate": final_gate,
    }
    return {"passed": not failures, "failures": failures, "summary": summary}


if __name__ == "__main__":
    result = verify(final_gate="--final-gate" in sys.argv)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["passed"] else 1)
