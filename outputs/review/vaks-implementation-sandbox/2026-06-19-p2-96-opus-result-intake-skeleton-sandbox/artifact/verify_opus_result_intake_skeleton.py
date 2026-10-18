from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


SLICE_ID = "2026-06-19-p2-96-opus-result-intake-skeleton-sandbox"
ROOT = Path(__file__).resolve().parents[5]
SLICE_DIR = ROOT / "outputs/review/vaks-implementation-sandbox" / SLICE_ID
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

BUILD_SCRIPT = ARTIFACT_DIR / "build_opus_result_intake_skeleton.py"
VALIDATOR = ARTIFACT_DIR / "validate_opus_result_intake.py"
STATUS_JSON = ARTIFACT_DIR / "opus-result-intake-status.json"
STATUS_MD = ARTIFACT_DIR / "opus-result-intake-status.md"
SCHEMA_JSON = ARTIFACT_DIR / "opus-result-intake-schema.json"
PLACEHOLDER = ARTIFACT_DIR / "raw-opus-result-placeholder.md"
FAILURES_JSON = FAILURE_DIR / "opus-result-intake-skeleton-failures.json"
SAMPLE_VALID_RECORD = FIXTURES_DIR / "sample-valid-opus-result-record.json"
SAMPLE_INVALID_RECORD = FAILURE_DIR / "sample-invalid-opus-result-record.json"


def load_build_module():
    spec = importlib.util.spec_from_file_location("p2_96_build", BUILD_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load build module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def split_newline(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    return line, ""


def read_status(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return ""
    for line in lines[1:]:
        if line.strip() == "---":
            break
        content, _newline = split_newline(line)
        if content.startswith("status:"):
            return content.split(":", 1)[1].strip()
    return ""


def check_no_cache_files() -> list[str]:
    failures = []
    for path in SLICE_DIR.rglob("*"):
        lowered = path.name.lower()
        if lowered == "__pycache__" or lowered.endswith(".pyc") or lowered.endswith(".tmp") or lowered.endswith(".log"):
            failures.append(f"cache_or_temp_file_present:{path.relative_to(SLICE_DIR)}")
    return failures


def fixture_expectations() -> dict[str, dict]:
    return {
        "pending-result-not-approval.json": {
            "actual_opus_result_present": False,
            "opus_review_performed": False,
            "opus_approval_claimed": False,
            "passed": True,
        },
        "allowed-conclusion-tokens.json": {
            "allowed_conclusion_tokens": [
                "OPUS_PASS_SANDBOX_CLOSEOUT",
                "OPUS_REVISE_SANDBOX_CLOSEOUT",
                "OPUS_BLOCKED_NEEDS_USER",
            ],
            "passed": True,
        },
        "intake-ready-with-opus-pending.json": {
            "result_intake_ready": True,
            "p2_95_external_opus_review_pending": True,
            "passed": True,
        },
        "authority-boundaries-false.json": {
            "mainline_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "commit_push_sync_ready": False,
            "goal_complete_now": False,
            "passed": True,
        },
        "future-result-record-contract.json": {
            "required_keys": ["blockers", "boundary_verdict", "raw_conclusion_token", "raw_response_path", "reviewed_evidence"],
            "passed": True,
        },
    }


def verify(final_gate: bool) -> dict:
    failures: list[str] = []
    required_files = [
        SLICE_DIR / "slice-plan.md",
        SLICE_DIR / "source-map.md",
        SLICE_DIR / "verification.md",
        SLICE_DIR / "reviewer-report.md",
        SLICE_DIR / "boundary-audit.md",
        SLICE_DIR / "product-acceptance-report.md",
        SLICE_DIR / "next-step.md",
        BUILD_SCRIPT,
        VALIDATOR,
        Path(__file__),
        STATUS_JSON,
        STATUS_MD,
        SCHEMA_JSON,
        PLACEHOLDER,
        FAILURES_JSON,
        SAMPLE_VALID_RECORD,
        SAMPLE_INVALID_RECORD,
    ]
    for path in required_files:
        if not path.exists():
            failures.append(f"missing_required_file:{path.relative_to(SLICE_DIR)}")

    if not failures:
        build_module = load_build_module()
        current_status = build_module.build_status()
        stored_status = load_json(STATUS_JSON)
        for key, value in current_status["summary"].items():
            if stored_status["summary"].get(key) != value:
                failures.append(
                    f"summary_mismatch:{key}:stored={stored_status['summary'].get(key)}:current={value}"
                )

        expected_summary = {
            "allowed_conclusion_token_count": 3,
            "raw_result_placeholder_present": True,
            "actual_opus_result_present": False,
            "opus_review_performed": False,
            "opus_approval_claimed": False,
            "result_intake_ready": True,
            "p2_95_external_opus_review_pending": True,
            "p2_95_goal_complete_now": False,
            "mainline_ready": False,
            "promotion_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "commit_push_sync_ready": False,
            "goal_complete_now": False,
        }
        for key, expected in expected_summary.items():
            actual = stored_status["summary"].get(key)
            if actual != expected:
                failures.append(f"expected_summary_failed:{key}:expected={expected}:actual={actual}")

        schema = load_json(SCHEMA_JSON)
        if schema.get("allowed_conclusion_tokens") != [
            "OPUS_PASS_SANDBOX_CLOSEOUT",
            "OPUS_REVISE_SANDBOX_CLOSEOUT",
            "OPUS_BLOCKED_NEEDS_USER",
        ]:
            failures.append("schema_allowed_tokens_mismatch")
        if len(schema.get("required_fields_when_result_exists", [])) != 4:
            failures.append("schema_required_fields_count_not_4")

        for filename, expected_values in fixture_expectations().items():
            path = FIXTURES_DIR / filename
            if not path.exists():
                failures.append(f"missing_fixture:{filename}")
                continue
            payload = load_json(path)
            for key, expected in expected_values.items():
                if payload.get(key) != expected:
                    failures.append(f"fixture_mismatch:{filename}:{key}:expected={expected}:actual={payload.get(key)}")

        failure_payload = load_json(FAILURES_JSON)
        if len(failure_payload.get("failure_cases", [])) != 8:
            failures.append("failure_case_count_not_8")

        valid_run = subprocess.run(
            [sys.executable, "-B", str(VALIDATOR), "--record", str(SAMPLE_VALID_RECORD)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if valid_run.returncode != 0:
            failures.append(f"sample_valid_record_failed:{valid_run.stdout.strip()}:{valid_run.stderr.strip()}")

        invalid_run = subprocess.run(
            [sys.executable, "-B", str(VALIDATOR), "--record", str(SAMPLE_INVALID_RECORD)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if invalid_run.returncode == 0:
            failures.append("sample_invalid_record_unexpectedly_passed")
        else:
            try:
                invalid_payload = json.loads(invalid_run.stdout)
                if not any(item.startswith("invalid_conclusion_token") for item in invalid_payload.get("failures", [])):
                    failures.append("sample_invalid_record_missing_token_failure")
                if not any(item.startswith("forbidden_authority_true") for item in invalid_payload.get("failures", [])):
                    failures.append("sample_invalid_record_missing_authority_failure")
            except json.JSONDecodeError:
                failures.append(f"sample_invalid_record_invalid_json:{invalid_run.stdout.strip()}")

        joined_text = "\n".join([STATUS_MD.read_text(encoding="utf-8"), PLACEHOLDER.read_text(encoding="utf-8")])
        for needle in [
            "no actual Opus result exists",
            "not Opus approval",
            "not mainline approval",
            "not mainline approval, reviewed knowledge, evidence support, action basis",
            "OPUS_PASS_SANDBOX_CLOSEOUT",
            "OPUS_REVISE_SANDBOX_CLOSEOUT",
            "OPUS_BLOCKED_NEEDS_USER",
        ]:
            if needle not in joined_text:
                failures.append(f"missing_boundary_text:{needle}")

    failures.extend(check_no_cache_files())

    if final_gate:
        expected_statuses = {
            "verification.md": "local_verification_passed",
            "reviewer-report.md": "review_pass_no_blocker",
            "boundary-audit.md": "pass_boundary",
            "product-acceptance-report.md": "pass_product_grade",
            "next-step.md": "pass_product_grade_pending_next_slice",
        }
        for filename, expected in expected_statuses.items():
            actual = read_status(SLICE_DIR / filename)
            if actual != expected:
                failures.append(f"final_gate_status:{filename}:expected={expected}:actual={actual}")

    summary = {}
    if STATUS_JSON.exists():
        status = load_json(STATUS_JSON)
        failure_case_count = len(load_json(FAILURES_JSON).get("failure_cases", [])) if FAILURES_JSON.exists() else 0
        summary = {
            "fixture_count": len(list(FIXTURES_DIR.glob("*.json"))),
            "failure_case_count": failure_case_count,
            "validator_sample_valid_present": SAMPLE_VALID_RECORD.exists(),
            "validator_sample_invalid_present": SAMPLE_INVALID_RECORD.exists(),
            "allowed_conclusion_token_count": status["summary"].get("allowed_conclusion_token_count"),
            "result_intake_ready": status["summary"].get("result_intake_ready"),
            "actual_opus_result_present": status["summary"].get("actual_opus_result_present"),
            "opus_approval_claimed": status["summary"].get("opus_approval_claimed"),
            "mainline_ready": status["summary"].get("mainline_ready"),
            "goal_complete_now": status["summary"].get("goal_complete_now"),
            "final_gate": final_gate,
        }

    return {"passed": not failures, "failures": failures, "summary": summary}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--final-gate", action="store_true")
    args = parser.parse_args()
    result = verify(final_gate=args.final_gate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
