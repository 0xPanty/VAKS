from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-99-portable-opus-evidence-bundle-sandbox"
ROOT = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = ROOT / "outputs/review/vaks-implementation-sandbox"
SLICE_DIR = SANDBOX_ROOT / SLICE_ID
ARTIFACT_DIR = SLICE_DIR / "artifact"
SNAPSHOT_DIR = ARTIFACT_DIR / "evidence-snapshots"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

EVIDENCE_SOURCES = [
    (
        "p2-98-single-file-opus-review-dossier.md",
        SANDBOX_ROOT
        / "2026-06-19-p2-98-single-file-opus-review-dossier-sandbox/artifact/single-file-opus-review-dossier.md",
    ),
    (
        "p2-98-single-file-opus-review-dossier.json",
        SANDBOX_ROOT
        / "2026-06-19-p2-98-single-file-opus-review-dossier-sandbox/artifact/single-file-opus-review-dossier.json",
    ),
    (
        "p2-91-executor-apply.json",
        SANDBOX_ROOT
        / "2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox/artifact/old_file_status_normalization_executor_apply.json",
    ),
    (
        "p2-92-current-strict-audit.json",
        SANDBOX_ROOT
        / "2026-06-19-p2-92-post-apply-current-strict-closeout-audit-sandbox/artifact/post_apply_current_strict_closeout_audit.json",
    ),
    (
        "p2-94-submission-packet.json",
        SANDBOX_ROOT
        / "2026-06-19-p2-94-opus-review-submission-packet-sandbox/artifact/opus-review-submission-packet.json",
    ),
    (
        "p2-94-submission-prompt.md",
        SANDBOX_ROOT
        / "2026-06-19-p2-94-opus-review-submission-packet-sandbox/artifact/opus-review-submission-prompt.md",
    ),
    (
        "p2-96-result-intake-status.json",
        SANDBOX_ROOT
        / "2026-06-19-p2-96-opus-result-intake-skeleton-sandbox/artifact/opus-result-intake-status.json",
    ),
    (
        "p2-96-result-intake-schema.json",
        SANDBOX_ROOT
        / "2026-06-19-p2-96-opus-result-intake-skeleton-sandbox/artifact/opus-result-intake-schema.json",
    ),
    (
        "p2-97-wait-state-guard.json",
        SANDBOX_ROOT
        / "2026-06-19-p2-97-external-review-wait-state-guard-sandbox/artifact/external-review-wait-state-guard.json",
    ),
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_manifest() -> dict:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    evidence_items = []
    for snapshot_name, source_path in EVIDENCE_SOURCES:
        snapshot_path = SNAPSHOT_DIR / snapshot_name
        source_bytes = source_path.read_bytes()
        shutil.copyfile(source_path, snapshot_path)
        snapshot_bytes = snapshot_path.read_bytes()
        evidence_items.append(
            {
                "snapshot_name": snapshot_name,
                "source_path": rel(source_path),
                "snapshot_path": rel(snapshot_path),
                "source_sha256": sha256_bytes(source_bytes),
                "snapshot_sha256": sha256_bytes(snapshot_bytes),
                "hash_match": sha256_bytes(source_bytes) == sha256_bytes(snapshot_bytes),
                "size_bytes": len(snapshot_bytes),
            }
        )

    p2_98 = load_json(SANDBOX_ROOT / "2026-06-19-p2-98-single-file-opus-review-dossier-sandbox/artifact/single-file-opus-review-dossier.json")
    p2_97 = load_json(SANDBOX_ROOT / "2026-06-19-p2-97-external-review-wait-state-guard-sandbox/artifact/external-review-wait-state-guard.json")
    summary = {
        "bundle_ready": True,
        "snapshot_count": len(evidence_items),
        "hash_match_count": sum(1 for item in evidence_items if item["hash_match"]),
        "dossier_ready": p2_98["summary"]["dossier_ready"],
        "guard_state": p2_97["summary"]["guard_state"],
        "actual_opus_result_present": False,
        "opus_approval_claimed": False,
        "mainline_ready": False,
        "reviewed_knowledge_ready": False,
        "evidence_support_ready": False,
        "action_basis_ready": False,
        "goal_complete_now": False,
    }
    return {
        "record_kind": "portable_opus_evidence_bundle_manifest",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "evidence_items": evidence_items,
        "authority_flags": {
            "portable_evidence_bundle_only": True,
            "actual_opus_result_present": False,
            "opus_approval_claimed": False,
            "mainline_merge": False,
            "reviewed_knowledge": False,
            "evidence_support": False,
            "action_basis": False,
            "goal_complete_now": False,
        },
    }


def render_readme(manifest: dict) -> str:
    rows = "\n".join(
        f"| `{item['snapshot_name']}` | `{item['source_path']}` | `{item['snapshot_sha256']}` | `{item['hash_match']}` |"
        for item in manifest["evidence_items"]
    )
    return f"""# Portable Opus Evidence Bundle

## Purpose

This bundle contains snapshot copies of the dossier and key evidence files for external Opus review.

## Boundary

This bundle is not an Opus result, not Opus approval, not mainline readiness, not reviewed knowledge, not evidence support, and not action basis.

## Guard State

`{manifest["summary"]["guard_state"]}`

## Evidence Snapshots

| Snapshot | Source | SHA256 | Match |
| --- | --- | --- | --- |
{rows}

## Required Next Step

Send the dossier snapshot to Opus and retain the raw Opus response in a later sandbox-only intake slice.
"""


def write_fixtures(manifest: dict) -> None:
    s = manifest["summary"]
    write_json(
        FIXTURES_DIR / "snapshots-present-and-hash-matched.json",
        {
            "case_id": "snapshots-present-and-hash-matched",
            "snapshot_count": s["snapshot_count"],
            "hash_match_count": s["hash_match_count"],
            "passed": s["snapshot_count"] == len(EVIDENCE_SOURCES) and s["hash_match_count"] == len(EVIDENCE_SOURCES),
        },
    )
    write_json(
        FIXTURES_DIR / "dossier-and-guard-carried.json",
        {
            "case_id": "dossier-and-guard-carried",
            "dossier_ready": s["dossier_ready"],
            "guard_state": s["guard_state"],
            "passed": s["dossier_ready"] and s["guard_state"] == "STOP_WAIT_EXTERNAL_OPUS_REVIEW",
        },
    )
    write_json(
        FIXTURES_DIR / "no-opus-or-mainline-claim.json",
        {
            "case_id": "no-opus-or-mainline-claim",
            "actual_opus_result_present": s["actual_opus_result_present"],
            "opus_approval_claimed": s["opus_approval_claimed"],
            "mainline_ready": s["mainline_ready"],
            "goal_complete_now": s["goal_complete_now"],
            "passed": not any(
                [
                    s["actual_opus_result_present"],
                    s["opus_approval_claimed"],
                    s["mainline_ready"],
                    s["goal_complete_now"],
                ]
            ),
        },
    )
    write_json(
        FIXTURES_DIR / "no-truth-action-authority.json",
        {
            "case_id": "no-truth-action-authority",
            "reviewed_knowledge_ready": s["reviewed_knowledge_ready"],
            "evidence_support_ready": s["evidence_support_ready"],
            "action_basis_ready": s["action_basis_ready"],
            "passed": not any(
                [s["reviewed_knowledge_ready"], s["evidence_support_ready"], s["action_basis_ready"]]
            ),
        },
    )
    write_json(
        FIXTURES_DIR / "source-paths-preserved.json",
        {
            "case_id": "source-paths-preserved",
            "source_path_count": len({item["source_path"] for item in manifest["evidence_items"]}),
            "passed": len({item["source_path"] for item in manifest["evidence_items"]}) == len(EVIDENCE_SOURCES),
        },
    )


def write_failure_cases() -> None:
    write_json(
        FAILURE_DIR / "portable-opus-evidence-bundle-failures.json",
        {
            "record_kind": "portable_opus_evidence_bundle_failure_cases",
            "slice_id": SLICE_ID,
            "failure_cases": [
                {
                    "case_id": "P2-99-FAIL-01-missing-snapshot",
                    "must_fail_when": "Any required evidence snapshot is missing.",
                },
                {
                    "case_id": "P2-99-FAIL-02-hash-mismatch",
                    "must_fail_when": "Any snapshot hash differs from the current source artifact hash.",
                },
                {
                    "case_id": "P2-99-FAIL-03-missing-dossier",
                    "must_fail_when": "The p2-98 single-file dossier snapshot is missing.",
                },
                {
                    "case_id": "P2-99-FAIL-04-opus-approval-claimed",
                    "must_fail_when": "The bundle claims Opus approval.",
                },
                {
                    "case_id": "P2-99-FAIL-05-mainline-or-truth-authority-claimed",
                    "must_fail_when": "The bundle claims mainline readiness, reviewed knowledge, evidence support, or action basis.",
                },
                {
                    "case_id": "P2-99-FAIL-06-goal-complete-claimed",
                    "must_fail_when": "The bundle claims the overall goal is complete.",
                },
                {
                    "case_id": "P2-99-FAIL-07-source-path-lost",
                    "must_fail_when": "The manifest omits original source paths.",
                },
                {
                    "case_id": "P2-99-FAIL-08-protected-path-write",
                    "must_fail_when": "This slice writes outside its own sandbox path.",
                },
            ],
        },
    )


def write_outputs() -> dict:
    manifest = build_manifest()
    write_json(ARTIFACT_DIR / "portable-opus-evidence-bundle-manifest.json", manifest)
    write_text(ARTIFACT_DIR / "portable-opus-evidence-bundle-readme.md", render_readme(manifest))
    write_fixtures(manifest)
    write_failure_cases()
    return manifest


def main() -> None:
    manifest = write_outputs()
    print(json.dumps({"written": True, "summary": manifest["summary"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

