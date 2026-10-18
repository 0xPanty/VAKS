from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-95-goal-state-external-review-waiting-ledger-sandbox"
ROOT = Path(__file__).resolve().parents[5]
SLICE_DIR = ROOT / "outputs/review/vaks-implementation-sandbox" / SLICE_ID
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

BUILD_SCRIPT = ARTIFACT_DIR / "build_goal_state_external_review_waiting_ledger.py"
LEDGER_JSON = ARTIFACT_DIR / "goal-state-external-review-waiting-ledger.json"
LEDGER_MD = ARTIFACT_DIR / "goal-state-external-review-waiting-ledger.md"
GATE_MATRIX_MD = ARTIFACT_DIR / "remaining-gate-matrix.md"
WAITING_LEDGER_MD = ARTIFACT_DIR / "external-review-waiting-ledger.md"
FAILURES_JSON = FAILURE_DIR / "goal-state-external-review-waiting-ledger-failures.json"


def load_build_module():
    spec = importlib.util.spec_from_file_location("p2_95_build", BUILD_SCRIPT)
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
        "product-grade-sandbox-closeout-evidence.json": {
            "tracked_closeout_slice_count": 4,
            "tracked_closeout_final_gate_complete_count": 4,
            "tracked_closeout_product_grade_count": 4,
            "sandbox_closeout_evidence_product_grade": True,
            "passed": True,
        },
        "external-opus-review-pending.json": {
            "external_opus_review_pending": True,
            "p2_94_opus_review_performed": False,
            "opus_approval_claimed": False,
            "passed": True,
        },
        "mainline-and-truth-boundaries-false.json": {
            "mainline_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "commit_push_sync_ready": False,
            "goal_complete_now": False,
            "passed": True,
        },
        "p2-91-p2-92-proof-intact.json": {
            "p2_91_old_slice_writes_applied": 75,
            "p2_91_protected_path_writes": 0,
            "p2_92_original_item_count": 20,
            "p2_92_current_strict_complete_original_item_count": 20,
            "passed": True,
        },
        "remaining-gates-present.json": {
            "remaining_gate_count": 3,
            "remaining_gate_ids": ["external_opus_review", "opus_result_intake", "user_mainline_approval"],
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
        LEDGER_JSON,
        LEDGER_MD,
        GATE_MATRIX_MD,
        WAITING_LEDGER_MD,
        FAILURES_JSON,
    ]
    for path in required_files:
        if not path.exists():
            failures.append(f"missing_required_file:{path.relative_to(SLICE_DIR)}")

    if not failures:
        build_module = load_build_module()
        current_ledger = build_module.build_ledger()
        stored_ledger = load_json(LEDGER_JSON)
        for key, value in current_ledger["summary"].items():
            if stored_ledger["summary"].get(key) != value:
                failures.append(
                    f"summary_mismatch:{key}:stored={stored_ledger['summary'].get(key)}:current={value}"
                )

        expected_summary = {
            "tracked_closeout_slice_count": 4,
            "tracked_closeout_final_gate_complete_count": 4,
            "tracked_closeout_product_grade_count": 4,
            "p2_91_old_slice_writes_applied": 75,
            "p2_91_protected_path_writes": 0,
            "p2_92_original_item_count": 20,
            "p2_92_current_strict_complete_original_item_count": 20,
            "p2_93_external_review_packet_ready": True,
            "p2_94_submission_packet_ready": True,
            "p2_94_opus_review_performed": False,
            "external_opus_review_pending": True,
            "opus_approval_claimed": False,
            "sandbox_closeout_evidence_product_grade": True,
            "mainline_ready": False,
            "promotion_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "commit_push_sync_ready": False,
            "goal_complete_now": False,
        }
        for key, expected in expected_summary.items():
            actual = stored_ledger["summary"].get(key)
            if actual != expected:
                failures.append(f"expected_summary_failed:{key}:expected={expected}:actual={actual}")

        if len(stored_ledger.get("slice_states", [])) != 4:
            failures.append("slice_states_count_not_4")
        if len(stored_ledger.get("remaining_gates", [])) != 3:
            failures.append("remaining_gates_count_not_3")

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
                LEDGER_MD.read_text(encoding="utf-8"),
                GATE_MATRIX_MD.read_text(encoding="utf-8"),
                WAITING_LEDGER_MD.read_text(encoding="utf-8"),
            ]
        )
        for needle in [
            "overall goal is not complete",
            "actual Opus review is still pending",
            "not Opus approval",
            "not mainline readiness",
            "No sandbox or Opus pass may become mainline merge",
            "external_opus_review",
            "user_mainline_approval",
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
    if LEDGER_JSON.exists():
        ledger = load_json(LEDGER_JSON)
        failure_case_count = len(load_json(FAILURES_JSON).get("failure_cases", [])) if FAILURES_JSON.exists() else 0
        summary = {
            "fixture_count": len(list(FIXTURES_DIR.glob("*.json"))),
            "failure_case_count": failure_case_count,
            "tracked_closeout_slice_count": ledger["summary"].get("tracked_closeout_slice_count"),
            "tracked_closeout_product_grade_count": ledger["summary"].get("tracked_closeout_product_grade_count"),
            "sandbox_closeout_evidence_product_grade": ledger["summary"].get(
                "sandbox_closeout_evidence_product_grade"
            ),
            "external_opus_review_pending": ledger["summary"].get("external_opus_review_pending"),
            "opus_approval_claimed": ledger["summary"].get("opus_approval_claimed"),
            "mainline_ready": ledger["summary"].get("mainline_ready"),
            "goal_complete_now": ledger["summary"].get("goal_complete_now"),
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

