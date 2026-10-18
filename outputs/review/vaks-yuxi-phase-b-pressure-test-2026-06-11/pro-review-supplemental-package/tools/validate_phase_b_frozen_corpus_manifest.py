import csv
import hashlib
import json
from pathlib import Path

import run_phase_b_pressure as harness


SANDBOX_DIR = harness.SANDBOX_DIR
RESULTS_DIR = harness.RESULTS_DIR

MANIFEST_JSON = RESULTS_DIR / "phase_b_frozen_corpus_manifest.json"
MANIFEST_CSV = RESULTS_DIR / "phase_b_frozen_corpus_manifest.csv"
CHECK_JSON = RESULTS_DIR / "phase_b_frozen_corpus_manifest_check.json"
CHECK_MD = SANDBOX_DIR / "PHASE_B_FROZEN_CORPUS_MANIFEST_CHECK.md"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_FROZEN_CORPUS_MANIFEST.md"


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def current_rows() -> list[dict]:
    doc_lookup: dict[tuple[str, str], harness.FileDoc] = {}
    rows: list[dict] = []
    for corpus in ["primary", "full"]:
        for doc in harness.build_file_docs(corpus):
            doc_lookup[(corpus, doc.path)] = doc
        for path in harness.iter_markdown_files(corpus):
            rel = path.relative_to(harness.ROOT).as_posix()
            doc = doc_lookup[(corpus, rel)]
            rows.append(
                {
                    "corpus": corpus,
                    "path": rel,
                    "bytes": str(path.stat().st_size),
                    "sha256": sha256_file(path),
                    "source_hash": doc.source_hash,
                    "status": doc.status,
                    "bucket": doc.bucket,
                    "record_kind": doc.record_kind,
                }
            )
    return rows


def validate_artifacts(errors: list[dict]) -> dict:
    artifacts = []
    for path in [MANIFEST_JSON, MANIFEST_CSV, REPORT_PATH]:
        exists = path.exists()
        artifacts.append(
            {"path": str(path.relative_to(SANDBOX_DIR)), "exists": exists, "bytes": path.stat().st_size if exists else 0}
        )
        if not exists:
            add_error(errors, "missing_artifact", str(path))
        elif path.stat().st_size == 0:
            add_error(errors, "empty_artifact", str(path))
    return {"artifacts": artifacts}


def validate_manifest(errors: list[dict]) -> dict:
    payload = read_json(MANIFEST_JSON)
    csv_rows = read_csv(MANIFEST_CSV)
    manifest_rows = payload.get("file_records", [])
    if len(csv_rows) != len(manifest_rows):
        add_error(errors, "csv_json_row_count_mismatch", f"{len(csv_rows)} != {len(manifest_rows)}")

    current = current_rows()
    manifest_by_key = {(row["corpus"], row["path"]): row for row in manifest_rows}
    current_by_key = {(row["corpus"], row["path"]): row for row in current}
    if set(manifest_by_key) != set(current_by_key):
        missing = sorted(set(current_by_key) - set(manifest_by_key))[:20]
        extra = sorted(set(manifest_by_key) - set(current_by_key))[:20]
        add_error(errors, "corpus_file_set_mismatch", f"missing={missing}; extra={extra}")

    mismatch_count = 0
    for key, current_row in current_by_key.items():
        manifest_row = manifest_by_key.get(key)
        if not manifest_row:
            continue
        for field in ["bytes", "sha256", "source_hash", "status", "bucket", "record_kind"]:
            if str(manifest_row.get(field, "")) != str(current_row.get(field, "")):
                mismatch_count += 1
                if mismatch_count <= 20:
                    add_error(errors, "corpus_file_record_mismatch", f"{key}:{field}")
    primary = [row for row in manifest_rows if row.get("corpus") == "primary"]
    full = [row for row in manifest_rows if row.get("corpus") == "full"]
    return {
        "manifest_rows": len(manifest_rows),
        "current_rows": len(current),
        "primary_files": len(primary),
        "full_files": len(full),
        "record_mismatch_count": mismatch_count,
    }


def write_report(result: dict) -> None:
    manifest = result.get("manifest") or {}
    lines = [
        "---",
        "record_kind: sandbox_frozen_corpus_manifest_check",
        f"status: {result['frozen_corpus_manifest_check_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: corpus_manifest_check_not_runtime_validation",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Frozen Corpus Manifest Check",
        "",
        "## Result",
        "",
        "```text",
        f"status: {result['frozen_corpus_manifest_check_status']}",
        f"error count: {result['error_count']}",
        f"manifest rows: {manifest.get('manifest_rows', 0)}",
        f"primary files: {manifest.get('primary_files', 0)}",
        f"full files: {manifest.get('full_files', 0)}",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "This verifies the local corpus hash snapshot against the current filesystem.",
        "It does not validate original Yuxi runtime or C-lite.",
        "```",
        "",
        "## Errors",
        "",
    ]
    if result["errors"]:
        lines.extend(f"- {error['code']}: {error['detail']}" for error in result["errors"])
    else:
        lines.append("- none")
    lines.append("")
    CHECK_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    errors: list[dict] = []
    artifacts = validate_artifacts(errors)
    manifest = validate_manifest(errors) if MANIFEST_JSON.exists() and MANIFEST_CSV.exists() else {}
    result = {
        "frozen_corpus_manifest_check_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "artifacts": artifacts,
        "manifest": manifest,
    }
    CHECK_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(result)
    print(f"frozen corpus manifest check status: {result['frozen_corpus_manifest_check_status']}")
    print(f"error count: {result['error_count']}")


if __name__ == "__main__":
    main()
