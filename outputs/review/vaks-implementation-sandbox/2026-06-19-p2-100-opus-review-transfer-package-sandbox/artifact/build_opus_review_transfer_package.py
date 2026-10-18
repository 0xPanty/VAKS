import hashlib
import json
import zipfile
from pathlib import Path


SLICE_ID = "2026-06-19-p2-100-opus-review-transfer-package-sandbox"
SOURCE_SLICE_ID = "2026-06-19-p2-99-portable-opus-evidence-bundle-sandbox"
FIXED_ZIP_DATE = (1980, 1, 1, 0, 0, 0)

HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
REPO_ROOT = SLICE_DIR.parents[3]
SOURCE_SLICE_DIR = (
    REPO_ROOT
    / "outputs"
    / "review"
    / "vaks-implementation-sandbox"
    / SOURCE_SLICE_ID
)
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

ZIP_PATH = ARTIFACT_DIR / "opus-review-transfer-package.zip"
ZIP_SHA_PATH = ARTIFACT_DIR / "opus-review-transfer-package-sha256.txt"
EXTERNAL_MANIFEST_PATH = ARTIFACT_DIR / "opus-review-transfer-package-manifest.json"
TRANSFER_README_PATH = ARTIFACT_DIR / "opus-review-transfer-package-readme.md"
CONTENT_MANIFEST_PATH = ARTIFACT_DIR / "transfer-package-contents-manifest.json"


def rel_repo(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


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


def source_files() -> list[Path]:
    blocked_parts = {"__pycache__"}
    blocked_suffixes = {".pyc", ".pyo", ".tmp", ".temp"}
    files = []
    for path in SOURCE_SLICE_DIR.rglob("*"):
        if not path.is_file():
            continue
        if any(part in blocked_parts for part in path.parts):
            continue
        if path.suffix.lower() in blocked_suffixes:
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(SOURCE_SLICE_DIR).as_posix())


def add_zip_file(zf: zipfile.ZipFile, archive_path: str, data: bytes) -> None:
    info = zipfile.ZipInfo(archive_path, FIXED_ZIP_DATE)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    zf.writestr(info, data)


def build() -> dict:
    if not SOURCE_SLICE_DIR.exists():
        raise FileNotFoundError(f"missing source slice: {SOURCE_SLICE_DIR}")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)

    source_manifest_path = SOURCE_SLICE_DIR / "artifact" / "portable-opus-evidence-bundle-manifest.json"
    source_manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))

    transfer_readme = """# Opus Review Transfer Package

## Purpose

This ZIP packages the p2-99 portable Opus evidence bundle for external Opus review.

## How To Use

1. Send `opus-review-transfer-package.zip` to the external Opus review surface.
2. Provide the SHA256 from `opus-review-transfer-package-sha256.txt`.
3. Ask Opus to inspect the included p2-99 bundle, especially the p2-98 dossier snapshot and the p2-91/p2-92/p2-94/p2-96/p2-97 evidence snapshots.
4. Retain the raw Opus response in a later sandbox-only intake slice.

## Boundary

This package is not an Opus result, not Opus approval, not mainline readiness, not reviewed knowledge, not evidence support, not action basis, and not goal completion.
"""
    write_text(TRANSFER_README_PATH, transfer_readme)

    content_items = []

    readme_bytes = TRANSFER_README_PATH.read_bytes()
    content_items.append(
        {
            "archive_path": "TRANSFER-README.md",
            "source_path": rel_repo(TRANSFER_README_PATH),
            "source_sha256": sha256_bytes(readme_bytes),
            "archive_sha256": sha256_bytes(readme_bytes),
            "size_bytes": len(readme_bytes),
            "kind": "transfer_instructions",
        }
    )

    for source in source_files():
        data = source.read_bytes()
        archive_path = (
            "p2-99-portable-opus-evidence-bundle/"
            + source.relative_to(SOURCE_SLICE_DIR).as_posix()
        )
        digest = sha256_bytes(data)
        content_items.append(
            {
                "archive_path": archive_path,
                "source_path": rel_repo(source),
                "source_sha256": digest,
                "archive_sha256": digest,
                "size_bytes": len(data),
                "kind": "p2_99_source_file",
            }
        )

    stable_created_at = source_manifest.get("created_at", "2026-06-19T00:00:00+00:00")

    content_manifest = {
        "record_kind": "opus_review_transfer_package_contents_manifest",
        "slice_id": SLICE_ID,
        "source_slice_id": SOURCE_SLICE_ID,
        "created_at": stable_created_at,
        "summary": {
            "content_count": len(content_items),
            "p2_99_file_count": sum(1 for item in content_items if item["kind"] == "p2_99_source_file"),
            "transfer_readme_included": True,
            "source_bundle_ready": bool(source_manifest["summary"].get("bundle_ready")),
            "source_snapshot_count": source_manifest["summary"].get("snapshot_count"),
            "source_hash_match_count": source_manifest["summary"].get("hash_match_count"),
        },
        "content_items": content_items,
    }
    write_json(CONTENT_MANIFEST_PATH, content_manifest)

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w") as zf:
        add_zip_file(zf, "TRANSFER-README.md", readme_bytes)
        add_zip_file(
            zf,
            "transfer-package-contents-manifest.json",
            CONTENT_MANIFEST_PATH.read_bytes(),
        )
        for item in sorted(content_items, key=lambda record: record["archive_path"]):
            if item["archive_path"] == "TRANSFER-README.md":
                continue
            source_path = REPO_ROOT / item["source_path"]
            add_zip_file(zf, item["archive_path"], source_path.read_bytes())

    zip_sha256 = sha256_file(ZIP_PATH)
    write_text(ZIP_SHA_PATH, f"{zip_sha256}  {ZIP_PATH.name}\n")

    authority_flags = {
        "transfer_package_only": True,
        "actual_opus_result_present": False,
        "opus_approval_claimed": False,
        "mainline_ready": False,
        "reviewed_knowledge_ready": False,
        "evidence_support_ready": False,
        "action_basis_ready": False,
        "goal_complete_now": False,
    }
    p2_99_statuses = {
        name: frontmatter_status(SOURCE_SLICE_DIR / name)
        for name in [
            "verification.md",
            "reviewer-report.md",
            "boundary-audit.md",
            "product-acceptance-report.md",
            "next-step.md",
        ]
    }
    external_manifest = {
        "record_kind": "opus_review_transfer_package_manifest",
        "slice_id": SLICE_ID,
        "source_slice_id": SOURCE_SLICE_ID,
        "created_at": stable_created_at,
        "summary": {
            "transfer_ready": True,
            "zip_path": rel_repo(ZIP_PATH),
            "zip_sha256": zip_sha256,
            "zip_size_bytes": ZIP_PATH.stat().st_size,
            "content_manifest_path": rel_repo(CONTENT_MANIFEST_PATH),
            "content_manifest_sha256": sha256_file(CONTENT_MANIFEST_PATH),
            "content_count": len(content_items),
            "p2_99_file_count": p2_99_statuses and content_manifest["summary"]["p2_99_file_count"],
            "source_bundle_ready": source_manifest["summary"].get("bundle_ready"),
            "source_snapshot_count": source_manifest["summary"].get("snapshot_count"),
            "source_hash_match_count": source_manifest["summary"].get("hash_match_count"),
            "actual_opus_result_present": False,
            "opus_approval_claimed": False,
            "mainline_ready": False,
            "goal_complete_now": False,
        },
        "source_slice_statuses": p2_99_statuses,
        "authority_flags": authority_flags,
        "required_external_next_step": "Send the ZIP to Opus, retain the raw Opus response in a later sandbox-only intake slice, then validate that result separately.",
    }
    write_json(EXTERNAL_MANIFEST_PATH, external_manifest)

    fixtures = {
        "zip-present-and-hash-matched.json": {
            "fixture": "zip-present-and-hash-matched",
            "zip_path": rel_repo(ZIP_PATH),
            "zip_sha256": zip_sha256,
            "expected": True,
        },
        "contains-required-review-dossier.json": {
            "fixture": "contains-required-review-dossier",
            "required_archive_path": "p2-99-portable-opus-evidence-bundle/artifact/evidence-snapshots/p2-98-single-file-opus-review-dossier.md",
            "expected": True,
        },
        "contains-p2-99-acceptance-evidence.json": {
            "fixture": "contains-p2-99-acceptance-evidence",
            "required_archive_paths": [
                "p2-99-portable-opus-evidence-bundle/verification.md",
                "p2-99-portable-opus-evidence-bundle/reviewer-report.md",
                "p2-99-portable-opus-evidence-bundle/boundary-audit.md",
                "p2-99-portable-opus-evidence-bundle/product-acceptance-report.md",
                "p2-99-portable-opus-evidence-bundle/next-step.md",
            ],
            "expected": True,
        },
        "no-authority-overclaim.json": {
            "fixture": "no-authority-overclaim",
            "authority_flags": authority_flags,
            "expected": True,
        },
        "source-bundle-preserved.json": {
            "fixture": "source-bundle-preserved",
            "source_slice_id": SOURCE_SLICE_ID,
            "p2_99_file_count": content_manifest["summary"]["p2_99_file_count"],
            "expected": True,
        },
    }
    for filename, payload in fixtures.items():
        write_json(FIXTURES_DIR / filename, payload)

    failure_cases = {
        "record_kind": "opus_review_transfer_package_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {
                "id": "missing_zip",
                "expectation": "Verifier fails if the ZIP is missing.",
            },
            {
                "id": "zip_hash_mismatch",
                "expectation": "Verifier fails if the ZIP SHA256 does not match the manifest and sha256 file.",
            },
            {
                "id": "missing_content_manifest",
                "expectation": "Verifier fails if the ZIP omits transfer-package-contents-manifest.json.",
            },
            {
                "id": "missing_dossier_snapshot",
                "expectation": "Verifier fails if the p2-98 dossier snapshot is absent from the ZIP.",
            },
            {
                "id": "archive_source_hash_mismatch",
                "expectation": "Verifier fails if any archived file hash diverges from its source hash.",
            },
            {
                "id": "opus_approval_overclaim",
                "expectation": "Verifier fails if the package claims Opus approval.",
            },
            {
                "id": "mainline_ready_overclaim",
                "expectation": "Verifier fails if the package claims mainline readiness.",
            },
            {
                "id": "truth_or_action_authority_overclaim",
                "expectation": "Verifier fails if the package claims reviewed knowledge, evidence support, or action basis.",
            },
            {
                "id": "goal_complete_overclaim",
                "expectation": "Verifier fails if the package claims the full goal is complete.",
            },
            {
                "id": "runtime_cache_in_archive",
                "expectation": "Verifier fails if __pycache__, .pyc, or temporary files appear in the package.",
            },
        ],
    }
    write_json(FAILURE_DIR / "opus-review-transfer-package-failures.json", failure_cases)

    return {
        "written": True,
        "summary": external_manifest["summary"] | {
            "fixture_count": len(fixtures),
            "failure_case_count": len(failure_cases["failure_cases"]),
        },
    }


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, ensure_ascii=False))
