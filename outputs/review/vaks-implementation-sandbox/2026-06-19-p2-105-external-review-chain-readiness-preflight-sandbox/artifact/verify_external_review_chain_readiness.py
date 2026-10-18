import copy
import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-19-p2-105-external-review-chain-readiness-preflight-sandbox"
EXPECTED_CHAIN_COUNT = 5
EXPECTED_CHAIN = [
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
FALSE_SUMMARY_KEYS = [
    "actual_opus_result_present",
    "validated_opus_pass_present",
    "user_approval_present",
    "mainline_ready",
    "mainline_merge_allowed",
    "promotion_allowed",
    "reviewed_knowledge_ready",
    "evidence_support_ready",
    "action_basis_ready",
    "commit_push_sync_ready",
    "goal_complete_now",
]
FALSE_KEY_SUMMARY_KEYS = set(FALSE_SUMMARY_KEYS + [
    "opus_approval_claimed",
    "ready_for_merge_proposal",
])

HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
REPO_ROOT = SLICE_DIR.parents[3]
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

COCKPIT_PATH = ARTIFACT_DIR / "external-review-chain-readiness-cockpit.json"
RUNBOOK_PATH = ARTIFACT_DIR / "external-review-chain-readiness-runbook.md"
FAILURE_CASE_PATH = FAILURE_DIR / "external-review-chain-readiness-failures.json"

EXPECTED_FINAL_STATUSES = {
    "verification.md": "local_verification_passed",
    "reviewer-report.md": "review_pass_no_blocker",
    "boundary-audit.md": "pass_boundary",
    "product-acceptance-report.md": "pass_product_grade",
    "next-step.md": "pass_product_grade_pending_next_slice",
}

UPSTREAM_EXPECTED_STATUSES = {
    "verification": "local_verification_passed",
    "reviewer": "review_pass_no_blocker",
    "boundary": "pass_boundary",
    "product_acceptance": "pass_product_grade",
    "next_step": "pass_product_grade_pending_next_slice",
}

REPORT_STATUS_KEYS = {
    "verification.md": "verification",
    "reviewer-report.md": "reviewer",
    "boundary-audit.md": "boundary",
    "product-acceptance-report.md": "product_acceptance",
    "next-step.md": "next_step",
}


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


def verification_final_gate(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    return '"passed": true' in text and '"final_gate": true' in text


def dotted_get(payload: dict, dotted_path: str):
    current = payload
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


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


def validate_cockpit(cockpit: dict) -> list[str]:
    failures = []
    if cockpit.get("record_kind") != "external_review_chain_readiness_cockpit":
        failures.append("record_kind_mismatch")
    if cockpit.get("slice_id") != SLICE_ID:
        failures.append("slice_id_mismatch")
    records = cockpit.get("chain_records", [])
    if len(records) != EXPECTED_CHAIN_COUNT:
        failures.append("chain_slice_count_mismatch")
    for index, record in enumerate(records):
        expected_record = EXPECTED_CHAIN[index] if index < len(EXPECTED_CHAIN) else None
        expected_slice_id = expected_record.get("slice_id") if expected_record else None
        expected_role = expected_record.get("role") if expected_record else None
        expected_slice_path = f"outputs/review/vaks-implementation-sandbox/{expected_slice_id}" if expected_slice_id else None
        expected_key_path = f"{expected_slice_path}/{expected_record['key_artifact']}" if expected_record else None
        if expected_record and record.get("slice_id") != expected_slice_id:
            failures.append("chain_slice_id_mismatch")
        if expected_record and record.get("role") != expected_role:
            failures.append("chain_role_mismatch")
        if expected_record and record.get("slice_path") != expected_slice_path:
            failures.append("chain_slice_path_mismatch")
        key_path = record.get("key_artifact_path")
        if not key_path:
            failures.append("key_artifact_path_missing")
        else:
            if expected_key_path and key_path != expected_key_path:
                failures.append("key_artifact_path_mismatch")
            key_abs = REPO_ROOT / key_path
            if not key_abs.exists():
                failures.append("key_artifact_missing")
            elif record.get("key_artifact_mtime_ns") != key_abs.stat().st_mtime_ns:
                failures.append("key_artifact_stale")
            else:
                try:
                    current_key_summary = key_summary(json.loads(key_abs.read_text(encoding="utf-8")))
                    if record.get("key_summary") != current_key_summary:
                        failures.append("key_summary_mismatch")
                except Exception as exc:
                    failures.append(f"key_summary_load_failed:{exc}")
        for key, value in (record.get("key_summary") or {}).items():
            if key in FALSE_KEY_SUMMARY_KEYS and value is not False:
                failures.append(f"key_summary_overclaim:{key}")
        report_snapshots = record.get("report_snapshots", [])
        if len(report_snapshots) != len(REPORT_STATUS_KEYS):
            failures.append("report_snapshot_count_mismatch")
        snapshot_by_file = {snapshot.get("filename"): snapshot for snapshot in report_snapshots}
        for filename, status_key in REPORT_STATUS_KEYS.items():
            snapshot = snapshot_by_file.get(filename)
            if not snapshot:
                failures.append(f"report_snapshot_missing:{filename}")
                continue
            report_path = snapshot.get("path")
            if not report_path:
                failures.append(f"report_snapshot_path_missing:{filename}")
                continue
            expected_report_path = f"{expected_slice_path}/{filename}" if expected_slice_path else None
            if expected_report_path and report_path != expected_report_path:
                failures.append("report_snapshot_path_mismatch")
            report_abs = REPO_ROOT / report_path
            if not report_abs.exists():
                failures.append(f"report_snapshot_file_missing:{filename}")
                continue
            if snapshot.get("mtime_ns") != report_abs.stat().st_mtime_ns:
                failures.append("report_snapshot_stale")
            current_status = frontmatter_status(report_abs)
            if snapshot.get("status") != current_status:
                failures.append("report_snapshot_status_mismatch")
            if snapshot.get("status_key") != status_key:
                failures.append(f"report_snapshot_status_key_mismatch:{filename}")
            if record.get("statuses", {}).get(status_key) != current_status:
                failures.append("record_status_stale")
            expected = UPSTREAM_EXPECTED_STATUSES[status_key]
            if current_status != expected:
                failures.append(f"upstream_report_status_not_expected:{filename}")
            if filename == "verification.md":
                current_final_gate = verification_final_gate(report_abs)
                if snapshot.get("verification_final_gate_true") != current_final_gate:
                    failures.append("report_snapshot_final_gate_mismatch")
                if current_final_gate is not True:
                    failures.append("upstream_verification_final_gate_not_true")
        if record.get("verification_final_gate_true") is not True:
            failures.append("chain_final_gate_not_true")
        statuses = record.get("statuses", {})
        if statuses.get("product_acceptance") != "pass_product_grade":
            failures.append("product_status_not_pass")
        if statuses.get("boundary") != "pass_boundary":
            failures.append("boundary_status_not_pass")
        if statuses.get("reviewer") != "review_pass_no_blocker":
            failures.append("reviewer_status_not_pass")
    summary = cockpit.get("summary", {})
    if summary.get("all_final_gates_true") is not True:
        failures.append("summary_all_final_gates_not_true")
    if summary.get("all_product_grade") is not True:
        failures.append("summary_all_product_grade_not_true")
    if summary.get("ready_to_submit_external_opus") is not True:
        failures.append("summary_not_ready_to_submit")
    for key in FALSE_SUMMARY_KEYS:
        if summary.get(key) is not False:
            failures.append(f"summary_overclaim:{key}")
    return failures


def mutate_cockpit(cockpit: dict, mutation: str) -> dict:
    mutated = copy.deepcopy(cockpit)
    if mutation == "remove_chain_record":
        mutated["chain_records"] = mutated["chain_records"][:-1]
    elif mutation == "set_wrong_slice_id":
        mutated["chain_records"][0]["slice_id"] = "2026-06-19-p2-999-wrong-slice"
    elif mutation == "set_wrong_role":
        mutated["chain_records"][0]["role"] = "wrong_role"
    elif mutation == "set_cross_slice_key_artifact_path":
        mutated["chain_records"][0]["key_artifact_path"] = mutated["chain_records"][1]["key_artifact_path"]
        mutated["chain_records"][0]["key_artifact_mtime_ns"] = mutated["chain_records"][1]["key_artifact_mtime_ns"]
    elif mutation == "set_cross_slice_report_path":
        source_snapshot = mutated["chain_records"][1]["report_snapshots"][0]
        mutated["chain_records"][0]["report_snapshots"][0]["path"] = source_snapshot["path"]
        mutated["chain_records"][0]["report_snapshots"][0]["mtime_ns"] = source_snapshot["mtime_ns"]
        mutated["chain_records"][0]["report_snapshots"][0]["status"] = source_snapshot["status"]
    elif mutation == "set_final_gate_false":
        mutated["chain_records"][0]["verification_final_gate_true"] = False
    elif mutation == "set_product_status_pending":
        mutated["chain_records"][0]["statuses"]["product_acceptance"] = "pending_product_acceptance"
    elif mutation == "set_boundary_status_pending":
        mutated["chain_records"][0]["statuses"]["boundary"] = "pending_boundary_audit"
    elif mutation == "set_reviewer_status_pending":
        mutated["chain_records"][0]["statuses"]["reviewer"] = "pending_review"
    elif mutation == "set_report_snapshot_mtime_stale":
        mutated["chain_records"][0]["report_snapshots"][0]["mtime_ns"] = 0
    elif mutation == "set_report_snapshot_product_pending":
        for snapshot in mutated["chain_records"][0]["report_snapshots"]:
            if snapshot.get("filename") == "product-acceptance-report.md":
                snapshot["status"] = "pending_product_acceptance"
                break
    elif mutation == "set_key_summary_stale":
        mutated["chain_records"][0]["key_summary"]["mainline_ready"] = "stale"
    elif mutation == "set_key_summary_actual_opus_true":
        mutated["chain_records"][0]["key_summary"]["actual_opus_result_present"] = True
    elif mutation == "set_key_summary_action_basis_true":
        mutated["chain_records"][1]["key_summary"]["action_basis_ready"] = True
    elif mutation.endswith("_true"):
        key = mutation[:-5]
        mutated["summary"][key] = True
    return mutated


def verify(final_gate: bool = False) -> dict:
    failures = []
    cockpit = load_json(COCKPIT_PATH, failures) if COCKPIT_PATH.exists() else None
    failure_payload = load_json(FAILURE_CASE_PATH, failures) if FAILURE_CASE_PATH.exists() else None
    if not RUNBOOK_PATH.exists():
        failures.append("missing_runbook")

    if not cockpit:
        failures.append("missing_cockpit")
    else:
        failures.extend(validate_cockpit(cockpit))

    fixture_files = sorted(FIXTURES_DIR.glob("*.json"))
    if len(fixture_files) != 3:
        failures.append(f"fixture_count_mismatch:{len(fixture_files)}")
    for fixture in fixture_files:
        payload = load_json(fixture, failures)
        if payload and payload.get("expected") is not True:
            failures.append(f"fixture_not_positive:{fixture.name}")
        if payload:
            for key, expected in payload.get("checks", {}).items():
                actual = dotted_get(cockpit or {}, key)
                if actual != expected:
                    failures.append(f"fixture_check_failed:{fixture.name}:{key}:expected={expected}:actual={actual}")

    failure_case_count = 0
    expected_failure_hits = 0
    if not failure_payload:
        failures.append("missing_failure_cases")
    elif cockpit:
        cases = failure_payload.get("failure_cases", [])
        failure_case_count = len(cases)
        if failure_case_count < 25:
            failures.append(f"failure_case_count_too_low:{failure_case_count}")
        for case in cases:
            mutated = mutate_cockpit(cockpit, case.get("mutation"))
            actual = validate_cockpit(mutated)
            expected = case.get("expected_failure")
            if expected in actual:
                expected_failure_hits += 1
            else:
                failures.append(f"failure_case_not_caught:{case.get('id')}:{expected}:{actual}")

    if RUNBOOK_PATH.exists():
        text = RUNBOOK_PATH.read_text(encoding="utf-8")
        for phrase in [
            "ready to submit to external Opus",
            "No actual Opus result is present",
            "No validated Opus PASS is present",
            "No user approval is present",
            "No mainline merge",
            "reviewed knowledge",
            "evidence support",
            "action basis",
            "commit",
            "push",
            "sync",
            "goal completion",
        ]:
            if phrase not in text:
                failures.append(f"runbook_missing_phrase:{phrase}")

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
        "chain_slice_count": len(cockpit.get("chain_records", [])) if cockpit else 0,
        "fixture_count": len(fixture_files),
        "failure_case_count": failure_case_count,
        "expected_failure_hits": expected_failure_hits,
        "ready_to_submit_external_opus": bool(cockpit and cockpit.get("summary", {}).get("ready_to_submit_external_opus")),
        "actual_opus_result_present": bool(cockpit and cockpit.get("summary", {}).get("actual_opus_result_present")),
        "user_approval_present": bool(cockpit and cockpit.get("summary", {}).get("user_approval_present")),
        "mainline_ready": bool(cockpit and cockpit.get("summary", {}).get("mainline_ready")),
        "goal_complete_now": bool(cockpit and cockpit.get("summary", {}).get("goal_complete_now")),
        "final_gate": final_gate,
    }
    return {"passed": not failures, "failures": failures, "summary": summary}


if __name__ == "__main__":
    result = verify(final_gate="--final-gate" in sys.argv)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["passed"] else 1)
