from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-97-external-review-wait-state-guard-sandbox"
ROOT = Path(__file__).resolve().parents[5]
SLICE_DIR = ROOT / "outputs/review/vaks-implementation-sandbox" / SLICE_ID
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

BUILD_SCRIPT = ARTIFACT_DIR / "build_external_review_wait_state_guard.py"
GUARD_JSON = ARTIFACT_DIR / "external-review-wait-state-guard.json"
GUARD_MD = ARTIFACT_DIR / "external-review-wait-state-guard.md"
NO_MERGE_MD = ARTIFACT_DIR / "no-merge-checklist.md"
HANDOFF_MD = ARTIFACT_DIR / "wait-state-handoff.md"
FAILURES_JSON = FAILURE_DIR / "external-review-wait-state-guard-failures.json"


def load_build_module():
    spec = importlib.util.spec_from_file_location("p2_97_build", BUILD_SCRIPT)
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
        "stop-wait-guard-active.json": {
            "guard_state": "STOP_WAIT_EXTERNAL_OPUS_REVIEW",
            "external_opus_review_pending": True,
            "actual_opus_result_present": False,
            "passed": True,
        },
        "sandbox-product-grade-but-not-complete.json": {
            "sandbox_closeout_evidence_product_grade": True,
            "goal_complete_now": False,
            "passed": True,
        },
        "no-mainline-or-truth-authority.json": {
            "mainline_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "passed": True,
        },
        "no-commit-push-sync.json": {
            "commit_push_sync_ready": False,
            "may_merge_mainline": False,
            "may_claim_complete": False,
            "passed": True,
        },
        "sandbox-preparation-may-continue.json": {
            "may_continue_sandbox_preparation": True,
            "result_intake_ready": True,
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
        Path(__file__),
        GUARD_JSON,
        GUARD_MD,
        NO_MERGE_MD,
        HANDOFF_MD,
        FAILURES_JSON,
    ]
    for path in required_files:
        if not path.exists():
            failures.append(f"missing_required_file:{path.relative_to(SLICE_DIR)}")

    if not failures:
        build_module = load_build_module()
        current_guard = build_module.build_guard()
        stored_guard = load_json(GUARD_JSON)
        for key, value in current_guard["summary"].items():
            if stored_guard["summary"].get(key) != value:
                failures.append(
                    f"summary_mismatch:{key}:stored={stored_guard['summary'].get(key)}:current={value}"
                )

        expected_summary = {
            "guard_state": "STOP_WAIT_EXTERNAL_OPUS_REVIEW",
            "sandbox_closeout_evidence_product_grade": True,
            "result_intake_ready": True,
            "actual_opus_result_present": False,
            "external_opus_review_pending": True,
            "opus_approval_claimed": False,
            "mainline_ready": False,
            "promotion_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "commit_push_sync_ready": False,
            "goal_complete_now": False,
            "may_continue_sandbox_preparation": True,
            "may_merge_mainline": False,
            "may_claim_complete": False,
        }
        for key, expected in expected_summary.items():
            actual = stored_guard["summary"].get(key)
            if actual != expected:
                failures.append(f"expected_summary_failed:{key}:expected={expected}:actual={actual}")

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

        joined_text = "\n".join(
            [
                GUARD_MD.read_text(encoding="utf-8"),
                NO_MERGE_MD.read_text(encoding="utf-8"),
                HANDOFF_MD.read_text(encoding="utf-8"),
            ]
        )
        for needle in [
            "STOP_WAIT_EXTERNAL_OPUS_REVIEW",
            "Do not merge mainline",
            "do not claim complete",
            "not reviewed knowledge, evidence support, or action basis",
            "User separately approves any mainline integration",
            "p2-96 intake",
        ]:
            if needle not in joined_text:
                failures.append(f"missing_guard_text:{needle}")

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
    if GUARD_JSON.exists():
        guard = load_json(GUARD_JSON)
        failure_case_count = len(load_json(FAILURES_JSON).get("failure_cases", [])) if FAILURES_JSON.exists() else 0
        summary = {
            "fixture_count": len(list(FIXTURES_DIR.glob("*.json"))),
            "failure_case_count": failure_case_count,
            "guard_state": guard["summary"].get("guard_state"),
            "sandbox_closeout_evidence_product_grade": guard["summary"].get(
                "sandbox_closeout_evidence_product_grade"
            ),
            "actual_opus_result_present": guard["summary"].get("actual_opus_result_present"),
            "external_opus_review_pending": guard["summary"].get("external_opus_review_pending"),
            "opus_approval_claimed": guard["summary"].get("opus_approval_claimed"),
            "mainline_ready": guard["summary"].get("mainline_ready"),
            "goal_complete_now": guard["summary"].get("goal_complete_now"),
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

