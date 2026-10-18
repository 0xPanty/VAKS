import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import run_phase_b_pressure as harness


SANDBOX_DIR = harness.SANDBOX_DIR
RESULTS_DIR = harness.RESULTS_DIR

MANIFEST_JSON = RESULTS_DIR / "phase_b_frozen_corpus_manifest.json"
MANIFEST_CSV = RESULTS_DIR / "phase_b_frozen_corpus_manifest.csv"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_FROZEN_CORPUS_MANIFEST.md"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_file_rows() -> list[dict]:
    rows: list[dict] = []
    doc_lookup: dict[tuple[str, str], harness.FileDoc] = {}
    for corpus in ["primary", "full"]:
        for doc in harness.build_file_docs(corpus):
            doc_lookup[(corpus, doc.path)] = doc
        for path in harness.iter_markdown_files(corpus):
            rel = path.relative_to(harness.ROOT).as_posix()
            doc = doc_lookup[(corpus, rel)]
            stat = path.stat()
            rows.append(
                {
                    "corpus": corpus,
                    "path": rel,
                    "bytes": stat.st_size,
                    "sha256": sha256_file(path),
                    "source_hash": doc.source_hash,
                    "status": doc.status,
                    "bucket": doc.bucket,
                    "record_kind": doc.record_kind,
                    "mtime_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc)
                    .replace(microsecond=0)
                    .isoformat(),
                }
            )
    return rows


def build_payload(rows: list[dict]) -> dict:
    primary = [row for row in rows if row["corpus"] == "primary"]
    full = [row for row in rows if row["corpus"] == "full"]
    overlap = sorted({row["path"] for row in primary} & {row["path"] for row in full})
    return {
        "artifact_kind": "phase_b_frozen_corpus_manifest",
        "truth_boundary": "corpus_manifest_is_reproducibility_evidence_not_truth",
        "action_basis_allowed": False,
        "built_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "corpora": {
            "primary": {"file_count": len(primary), "bytes": sum(int(row["bytes"]) for row in primary)},
            "full": {"file_count": len(full), "bytes": sum(int(row["bytes"]) for row in full)},
            "primary_full_overlap_paths": len(overlap),
        },
        "selection_rules": {
            "core_files": sorted(harness.CORE_FILES),
            "primary_dirs": harness.PRIMARY_DIRS,
            "always_exclude_prefixes": sorted(harness.ALWAYS_EXCLUDE_PREFIXES),
            "markdown_only": True,
        },
        "file_records": rows,
        "hard_stops": [
            "manifest_freezes_test_corpus_only",
            "manifest_does_not_validate_original_yuxi_runtime",
            "manifest_does_not_approve_c_lite",
            "manifest_does_not_create_reviewed_knowledge",
        ],
    }


def write_report(payload: dict) -> None:
    corpora = payload["corpora"]
    lines = [
        "---",
        "record_kind: sandbox_frozen_corpus_manifest",
        "status: candidate",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: corpus_manifest_is_reproducibility_evidence_not_truth",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Frozen Corpus Manifest",
        "",
        "## What This Adds",
        "",
        "```text",
        "file-level frozen corpus manifest",
        "sha256 hash snapshot for every markdown file used by primary/full corpora",
        "corpus selection rules captured from the local harness",
        "```",
        "",
        "## Corpus Counts",
        "",
        "```text",
        f"primary files: {corpora['primary']['file_count']}",
        f"primary bytes: {corpora['primary']['bytes']}",
        f"full files: {corpora['full']['file_count']}",
        f"full bytes: {corpora['full']['bytes']}",
        f"primary/full overlap paths: {corpora['primary_full_overlap_paths']}",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "This makes the local corpus auditable and rerunnable.",
        "It does not validate original Yuxi runtime.",
        "It does not approve C-lite, writeback, action basis, or core-doc strong conclusions.",
        "```",
        "",
        "## Artifacts",
        "",
        "```text",
        "results/phase_b_frozen_corpus_manifest.json",
        "results/phase_b_frozen_corpus_manifest.csv",
        "```",
        "",
    ]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = build_file_rows()
    payload = build_payload(rows)
    MANIFEST_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(MANIFEST_CSV, rows)
    write_report(payload)
    print(f"frozen corpus files: {len(rows)}")
    print(f"primary files: {payload['corpora']['primary']['file_count']}")
    print(f"full files: {payload['corpora']['full']['file_count']}")


if __name__ == "__main__":
    main()
