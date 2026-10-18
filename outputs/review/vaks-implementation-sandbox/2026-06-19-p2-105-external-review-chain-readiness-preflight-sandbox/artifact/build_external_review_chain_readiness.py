import json
import re
from pathlib import Path


SLICE_ID = "2026-06-19-p2-105-external-review-chain-readiness-preflight-sandbox"
CHAIN = [
    {
        "slice_id": "2026-06-19-p2-100-opus-review-transfer-package-sandbox",
        "role": "transfer_package",
        "key_artifact": "artifact/opus-review-transfer-package-manifest.json",
    },
    {
        "slice_id": "2026-06-19-p2-101-opus-external-review-operator-kit-sandbox",
        "role": "operator_kit",
        "key_artifact": "artifact/opus-external-review-operator-control-card.json",
    },
    {
        "slice_id": "2026-06-19-p2-102-opus-result-intake-dry-run-validator-sandbox",
        "role": "result_intake_validator",
        "key_artifact": "artifact/opus-result-intake-dry-run-manifest.json",
    },
    {
        "slice_id": "2026-06-19-p2-103-opus-outcome-action-gate-matrix-sandbox",
        "role": "outcome_action_gate",
        "key_artifact": "artifact/opus-outcome-action-gate-matrix.json",
    },
    {
        "slice_id": "2026-06-19-p2-104-post-opus-user-approval-decision-packet-sandbox",
        "role": "post_opus_user_decision_packet",
        "key_artifact": "artifact/post-opus-user-approval-control-card.json",
    },
]

HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
REPO_ROOT = SLICE_DIR.parents[3]
SANDBOX_DIR = REPO_ROOT / "outputs" / "review" / "vaks-implementation-sandbox"
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

COCKPIT_PATH = ARTIFACT_DIR / "external-review-chain-readiness-cockpit.json"
RUNBOOK_PATH = ARTIFACT_DIR / "external-review-chain-readiness-runbook.md"

REPORT_STATUS_KEYS = {
    "verification.md": "verification",
    "reviewer-report.md": "reviewer",
    "boundary-audit.md": "boundary",
    "product-acceptance-report.md": "product_acceptance",
    "next-step.md": "next_step",
}


def rel_repo(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


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


def verification_final_gate(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    return bool(re.search(r'"passed"\s*:\s*true', text) and re.search(r'"final_gate"\s*:\s*true', text))


def load_key_artifact(slice_dir: Path, key_artifact: str) -> dict:
    return json.loads((slice_dir / key_artifact).read_text(encoding="utf-8"))


def key_summary(key_artifact: dict) -> dict:
    if "summary" in key_artifact:
        return key_artifact["summary"]
    if "current_state" in key_artifact:
        return key_artifact["current_state"]
    if "operator_state" in key_artifact:
        return key_artifact["operator_state"]
    if "transfer_package" in key_artifact:
        package = key_artifact.get("transfer_package", {})
        return {
            "ready_to_submit_to_opus": key_artifact.get("operator_state", {}).get("ready_to_submit_to_opus", True),
            "zip_sha256": package.get("zip_sha256"),
            "actual_opus_result_present": package.get("actual_opus_result_present", False),
            "opus_approval_claimed": package.get("opus_approval_claimed", False),
            "mainline_ready": package.get("mainline_ready", False),
            "goal_complete_now": package.get("goal_complete_now", False),
        }
    return {}


def report_snapshots(slice_dir: Path) -> list[dict]:
    snapshots = []
    for filename, status_key in REPORT_STATUS_KEYS.items():
        report_path = slice_dir / filename
        snapshot = {
            "filename": filename,
            "status_key": status_key,
            "path": rel_repo(report_path),
            "status": frontmatter_status(report_path),
            "mtime_ns": report_path.stat().st_mtime_ns,
        }
        if filename == "verification.md":
            snapshot["verification_final_gate_true"] = verification_final_gate(report_path)
        snapshots.append(snapshot)
    return snapshots


def build() -> dict:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)

    chain_records = []
    for item in CHAIN:
        slice_dir = SANDBOX_DIR / item["slice_id"]
        key_artifact_path = slice_dir / item["key_artifact"]
        key_artifact = load_key_artifact(slice_dir, item["key_artifact"])
        reports = report_snapshots(slice_dir)
        statuses = {report["status_key"]: report["status"] for report in reports}
        record = {
            "slice_id": item["slice_id"],
            "role": item["role"],
            "slice_path": rel_repo(slice_dir),
            "key_artifact_path": rel_repo(key_artifact_path),
            "key_artifact_mtime_ns": key_artifact_path.stat().st_mtime_ns,
            "report_snapshots": reports,
            "statuses": statuses,
            "verification_final_gate_true": statuses["verification"] == "local_verification_passed"
            and reports[0].get("verification_final_gate_true") is True,
            "key_summary": key_summary(key_artifact),
        }
        chain_records.append(record)

    cockpit = {
        "record_kind": "external_review_chain_readiness_cockpit",
        "slice_id": SLICE_ID,
        "chain_records": chain_records,
        "summary": {
            "chain_slice_count": len(chain_records),
            "all_final_gates_true": all(record["verification_final_gate_true"] for record in chain_records),
            "all_product_grade": all(record["statuses"]["product_acceptance"] == "pass_product_grade" for record in chain_records),
            "all_boundaries_passed": all(record["statuses"]["boundary"] == "pass_boundary" for record in chain_records),
            "all_reviewers_passed": all(record["statuses"]["reviewer"] == "review_pass_no_blocker" for record in chain_records),
            "ready_to_submit_external_opus": True,
            "actual_opus_result_present": False,
            "validated_opus_pass_present": False,
            "user_approval_present": False,
            "mainline_ready": False,
            "mainline_merge_allowed": False,
            "promotion_allowed": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "commit_push_sync_ready": False,
            "goal_complete_now": False,
        },
        "required_next_action": "Submit the p2-100 transfer package to external Opus using p2-101; after actual Opus output exists, retain it in a sandbox-only intake slice and validate with p2-102.",
    }
    write_json(COCKPIT_PATH, cockpit)

    runbook = """# External Review Chain Readiness Runbook

## Status

The sandbox chain is ready to submit to external Opus.

## Chain

1. p2-100 transfer package
2. p2-101 external Opus operator kit
3. p2-102 Opus result intake dry-run validator
4. p2-103 Opus outcome action gate
5. p2-104 post-Opus user approval decision packet

## Still Not True

- No actual Opus result is present.
- No validated Opus PASS is present.
- No user approval is present.
- No mainline merge, promotion, reviewed knowledge, evidence support, action basis, commit, push, sync, or goal completion is authorized.
"""
    write_text(RUNBOOK_PATH, runbook)

    fixtures = {
        "all-chain-final-gates-pass.json": {
            "fixture": "all-chain-final-gates-pass",
            "slice_ids": [record["slice_id"] for record in chain_records],
            "checks": {
                "summary.chain_slice_count": 5,
                "summary.all_final_gates_true": True,
                "summary.all_product_grade": True,
                "summary.all_boundaries_passed": True,
                "summary.all_reviewers_passed": True,
            },
            "expected": True,
        },
        "ready-to-submit-not-approved.json": {
            "fixture": "ready-to-submit-not-approved",
            "ready_to_submit_external_opus": True,
            "actual_opus_result_present": False,
            "validated_opus_pass_present": False,
            "user_approval_present": False,
            "checks": {
                "summary.ready_to_submit_external_opus": True,
                "summary.actual_opus_result_present": False,
                "summary.validated_opus_pass_present": False,
                "summary.user_approval_present": False,
            },
            "expected": True,
        },
        "no-mainline-authority.json": {
            "fixture": "no-mainline-authority",
            "mainline_merge_allowed": False,
            "promotion_allowed": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "checks": {
                "summary.mainline_ready": False,
                "summary.mainline_merge_allowed": False,
                "summary.promotion_allowed": False,
                "summary.reviewed_knowledge_ready": False,
                "summary.evidence_support_ready": False,
                "summary.action_basis_ready": False,
                "summary.commit_push_sync_ready": False,
                "summary.goal_complete_now": False,
            },
            "expected": True,
        },
    }
    for filename, payload in fixtures.items():
        write_json(FIXTURES_DIR / filename, payload)

    failures = {
        "record_kind": "external_review_chain_readiness_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {"id": "missing_chain_slice", "mutation": "remove_chain_record", "expected_failure": "chain_slice_count_mismatch"},
            {"id": "wrong_slice_id", "mutation": "set_wrong_slice_id", "expected_failure": "chain_slice_id_mismatch"},
            {"id": "wrong_role", "mutation": "set_wrong_role", "expected_failure": "chain_role_mismatch"},
            {"id": "cross_slice_key_artifact_path", "mutation": "set_cross_slice_key_artifact_path", "expected_failure": "key_artifact_path_mismatch"},
            {"id": "cross_slice_report_path", "mutation": "set_cross_slice_report_path", "expected_failure": "report_snapshot_path_mismatch"},
            {"id": "final_gate_false", "mutation": "set_final_gate_false", "expected_failure": "chain_final_gate_not_true"},
            {"id": "product_not_passed", "mutation": "set_product_status_pending", "expected_failure": "product_status_not_pass"},
            {"id": "boundary_not_passed", "mutation": "set_boundary_status_pending", "expected_failure": "boundary_status_not_pass"},
            {"id": "reviewer_not_passed", "mutation": "set_reviewer_status_pending", "expected_failure": "reviewer_status_not_pass"},
            {"id": "upstream_report_stale", "mutation": "set_report_snapshot_mtime_stale", "expected_failure": "report_snapshot_stale"},
            {"id": "upstream_report_status_drift", "mutation": "set_report_snapshot_product_pending", "expected_failure": "report_snapshot_status_mismatch"},
            {"id": "key_summary_stale", "mutation": "set_key_summary_stale", "expected_failure": "key_summary_mismatch"},
            {"id": "nested_claims_actual_opus_result", "mutation": "set_key_summary_actual_opus_true", "expected_failure": "key_summary_overclaim:actual_opus_result_present"},
            {"id": "nested_allows_action_basis", "mutation": "set_key_summary_action_basis_true", "expected_failure": "key_summary_overclaim:action_basis_ready"},
            {"id": "claims_actual_opus_result", "mutation": "actual_opus_result_present_true", "expected_failure": "summary_overclaim:actual_opus_result_present"},
            {"id": "claims_validated_opus_pass", "mutation": "validated_opus_pass_present_true", "expected_failure": "summary_overclaim:validated_opus_pass_present"},
            {"id": "claims_user_approval", "mutation": "user_approval_present_true", "expected_failure": "summary_overclaim:user_approval_present"},
            {"id": "claims_mainline_ready", "mutation": "mainline_ready_true", "expected_failure": "summary_overclaim:mainline_ready"},
            {"id": "allows_merge", "mutation": "mainline_merge_allowed_true", "expected_failure": "summary_overclaim:mainline_merge_allowed"},
            {"id": "allows_promotion", "mutation": "promotion_allowed_true", "expected_failure": "summary_overclaim:promotion_allowed"},
            {"id": "allows_truth_action", "mutation": "reviewed_knowledge_ready_true", "expected_failure": "summary_overclaim:reviewed_knowledge_ready"},
            {"id": "allows_evidence_support", "mutation": "evidence_support_ready_true", "expected_failure": "summary_overclaim:evidence_support_ready"},
            {"id": "allows_action_basis", "mutation": "action_basis_ready_true", "expected_failure": "summary_overclaim:action_basis_ready"},
            {"id": "allows_commit_push_sync", "mutation": "commit_push_sync_ready_true", "expected_failure": "summary_overclaim:commit_push_sync_ready"},
            {"id": "claims_goal_complete", "mutation": "goal_complete_now_true", "expected_failure": "summary_overclaim:goal_complete_now"},
        ],
    }
    write_json(FAILURE_DIR / "external-review-chain-readiness-failures.json", failures)

    return {
        "written": True,
        "summary": cockpit["summary"] | {"failure_case_count": len(failures["failure_cases"])},
    }


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, ensure_ascii=False))
