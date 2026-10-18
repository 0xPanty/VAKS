from __future__ import annotations

import hashlib
import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-87-old-file-status-normalization-diff-preview-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
ARTIFACT = SLICE_ROOT / "artifact" / "old_file_status_normalization_diff_preview.json"
FIXTURES_DIR = SLICE_ROOT / "fixtures"
FAILURES = SLICE_ROOT / "failure-cases" / "old-file-status-normalization-diff-preview-failures.json"
P2_80 = REPO_ROOT / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox/artifact/old_file_status_normalization_transaction_package.json"


REQUIRED_FILES = [
    "slice-plan.md",
    "source-map.md",
    "artifact/build_old_file_status_normalization_diff_preview.py",
    "artifact/verify_old_file_status_normalization_diff_preview.py",
    "artifact/old_file_status_normalization_diff_preview.json",
    "artifact/old_file_status_normalization_diff_preview.md",
    "artifact/old_file_status_normalization_diff_preview.html",
    "failure-cases/old-file-status-normalization-diff-preview-failures.json",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]

REQUIRED_FIXTURES = {
    "all-75-previews-present.json",
    "body-content-unchanged.json",
    "non-status-frontmatter-unchanged.json",
    "prewrite-hashes-match.json",
    "preview-not-write-authority.json",
}

REQUIRED_FAILURE_CASES = {
    "P2-87-FAIL-01-incomplete-preview",
    "P2-87-FAIL-02-body-drift",
    "P2-87-FAIL-03-non-status-frontmatter-drift",
    "P2-87-FAIL-04-prewrite-hash-mismatch",
    "P2-87-FAIL-05-status-not-applied-in-preview",
    "P2-87-FAIL-06-old-slice-write",
    "P2-87-FAIL-07-preview-as-approval",
    "P2-87-FAIL-08-mainline-authority",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def frontmatter_status(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    for line in lines[1:]:
        if line == "---":
            break
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return None


def check(final_gate: bool = False) -> dict:
    failures: list[str] = []
    for rel in REQUIRED_FILES:
        if not (SLICE_ROOT / rel).exists():
            failures.append(f"missing required file: {rel}")

    payload = load_json(ARTIFACT) if ARTIFACT.exists() else {}
    p2_80 = load_json(P2_80)
    operations = p2_80["transaction_operations"]
    previews = payload.get("preview_operations", [])
    preview_by_index = {item.get("operation_index"): item for item in previews}

    if len(previews) != 75:
        failures.append(f"expected 75 previews, found {len(previews)}")
    if len(preview_by_index) != 75:
        failures.append("preview operation indexes are not unique 75")

    for op in operations:
        item = preview_by_index.get(op["operation_index"])
        if not item:
            failures.append(f"missing preview operation {op['operation_index']}")
            continue
        target = REPO_ROOT / op["target_path"]
        current_sha = sha256_bytes(target.read_bytes()) if target.exists() else None
        if item.get("target_path") != op["target_path"]:
            failures.append(f"target path mismatch for operation {op['operation_index']}")
        if item.get("before_status") != op["before_status"]:
            failures.append(f"before status mismatch for operation {op['operation_index']}")
        if item.get("proposed_status") != op["proposed_status"]:
            failures.append(f"proposed status mismatch for operation {op['operation_index']}")
        if item.get("rollback_status") != op["rollback_status"]:
            failures.append(f"rollback status mismatch for operation {op['operation_index']}")
        if item.get("before_sha256") != current_sha:
            failures.append(f"current hash mismatch for operation {op['operation_index']}")
        if item.get("prewrite_required_hash") != op["prewrite_required_hash"]:
            failures.append(f"prewrite required hash mismatch for operation {op['operation_index']}")
        if item.get("before_hash_matches_prewrite_required") is not True:
            failures.append(f"prewrite hash not matched for operation {op['operation_index']}")
        if item.get("body_unchanged") is not True:
            failures.append(f"body changed for operation {op['operation_index']}")
        if item.get("non_status_frontmatter_unchanged") is not True:
            failures.append(f"non-status frontmatter changed for operation {op['operation_index']}")
        if item.get("proposed_status_applied_in_preview") is not True:
            failures.append(f"proposed status not applied in preview for operation {op['operation_index']}")
        if item.get("old_slice_write_applied") is not False:
            failures.append(f"old slice write applied for operation {op['operation_index']}")

    summary = payload.get("summary", {})
    expected_summary = {
        "preview_operation_count": 75,
        "unique_target_file_count": 75,
        "prewrite_hash_match_count": 75,
        "body_unchanged_count": 75,
        "non_status_frontmatter_unchanged_count": 75,
        "proposed_status_applied_count": 75,
        "p2_86_positive_ready_count": 1,
        "p2_86_executor_write_allowed_now": False,
        "old_slice_writes_applied": 0,
        "preview_authorizes_write": False,
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            failures.append(f"summary mismatch for {key}: expected {expected!r}, got {summary.get(key)!r}")

    fixture_names = {path.name for path in FIXTURES_DIR.glob("*.json")} if FIXTURES_DIR.exists() else set()
    missing_fixtures = REQUIRED_FIXTURES - fixture_names
    if missing_fixtures:
        failures.append(f"missing fixtures: {sorted(missing_fixtures)}")

    failure_payload = load_json(FAILURES) if FAILURES.exists() else {"failure_cases": []}
    failure_ids = {case.get("case_id") for case in failure_payload.get("failure_cases", [])}
    missing_failure_cases = REQUIRED_FAILURE_CASES - failure_ids
    if missing_failure_cases:
        failures.append(f"missing failure cases: {sorted(missing_failure_cases)}")

    authority = payload.get("authority_flags", {})
    for key in [
        "approval_collected",
        "preview_is_user_approval",
        "preview_is_write_authority",
        "executor_write_allowed",
        "old_slice_write_allowed",
        "normalization_applied",
        "mainline_ready",
        "promotion_ready",
        "reviewed_knowledge_ready",
        "evidence_support_ready",
        "action_basis_ready",
        "goal_complete_now",
    ]:
        if authority.get(key) is not False:
            failures.append(f"authority flag must remain false: {key}")
    if authority.get("old_slice_writes_applied") != 0:
        failures.append("authority old_slice_writes_applied must be 0")

    md_text = (SLICE_ROOT / "artifact" / "old_file_status_normalization_diff_preview.md").read_text(encoding="utf-8") if (SLICE_ROOT / "artifact" / "old_file_status_normalization_diff_preview.md").exists() else ""
    html_text = (SLICE_ROOT / "artifact" / "old_file_status_normalization_diff_preview.html").read_text(encoding="utf-8") if (SLICE_ROOT / "artifact" / "old_file_status_normalization_diff_preview.html").exists() else ""
    for needle in ["preview_operation_count: 75", "body_unchanged_count: 75", "old_slice_writes_applied: 0"]:
        if needle not in md_text:
            failures.append(f"markdown missing: {needle}")
    for needle in ["Status Diff Preview", "Prewrite hash match", "Preview only"]:
        if needle not in html_text:
            failures.append(f"html missing: {needle}")

    if final_gate:
        report_statuses = {
            "verification.md": "local_verification_passed",
            "reviewer-report.md": "review_pass_no_blocker",
            "boundary-audit.md": "pass_boundary",
            "product-acceptance-report.md": "pass_product_grade",
            "next-step.md": "pass_product_grade_pending_next_slice",
        }
        for rel, expected in report_statuses.items():
            actual = frontmatter_status(SLICE_ROOT / rel)
            if actual != expected:
                failures.append(f"{rel} status expected {expected!r}, got {actual!r}")

    result = {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "fixture_count": len(fixture_names),
            "failure_case_count": len(failure_ids),
            "preview_operation_count": summary.get("preview_operation_count"),
            "prewrite_hash_match_count": summary.get("prewrite_hash_match_count"),
            "body_unchanged_count": summary.get("body_unchanged_count"),
            "non_status_frontmatter_unchanged_count": summary.get("non_status_frontmatter_unchanged_count"),
            "old_slice_writes_applied": summary.get("old_slice_writes_applied"),
            "final_gate": final_gate,
        },
    }
    return result


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--final-gate", action="store_true")
    args = parser.parse_args()
    result = check(final_gate=args.final_gate)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
