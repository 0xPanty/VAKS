from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-98-single-file-opus-review-dossier-sandbox"
ROOT = Path(__file__).resolve().parents[5]
SLICE_DIR = ROOT / "outputs/review/vaks-implementation-sandbox" / SLICE_ID
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

BUILD_SCRIPT = ARTIFACT_DIR / "build_single_file_opus_review_dossier.py"
DOSSIER_JSON = ARTIFACT_DIR / "single-file-opus-review-dossier.json"
DOSSIER_MD = ARTIFACT_DIR / "single-file-opus-review-dossier.md"
FAILURES_JSON = FAILURE_DIR / "single-file-opus-review-dossier-failures.json"


def load_build_module():
    spec = importlib.util.spec_from_file_location("p2_98_build", BUILD_SCRIPT)
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
        "dossier-ready.json": {"dossier_ready": True, "evidence_digest_count": 5, "allowed_conclusion_token_count": 3, "passed": True},
        "p2-91-p2-92-evidence-carried.json": {
            "p2_91_old_slice_writes_applied": 75,
            "p2_92_current_strict_complete_original_item_count": 20,
            "passed": True,
        },
        "external-review-and-intake-ready.json": {
            "p2_94_submission_packet_ready": True,
            "p2_96_result_intake_ready": True,
            "p2_97_guard_state": "STOP_WAIT_EXTERNAL_OPUS_REVIEW",
            "passed": True,
        },
        "authority-boundary-false.json": {
            "actual_opus_result_present": False,
            "opus_approval_claimed": False,
            "mainline_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "goal_complete_now": False,
            "passed": True,
        },
        "allowed-tokens-exact.json": {
            "allowed_conclusion_tokens": [
                "OPUS_PASS_SANDBOX_CLOSEOUT",
                "OPUS_REVISE_SANDBOX_CLOSEOUT",
                "OPUS_BLOCKED_NEEDS_USER",
            ],
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
        DOSSIER_JSON,
        DOSSIER_MD,
        FAILURES_JSON,
    ]
    for path in required_files:
        if not path.exists():
            failures.append(f"missing_required_file:{path.relative_to(SLICE_DIR)}")

    if not failures:
        build_module = load_build_module()
        current_dossier = build_module.build_dossier()
        stored_dossier = load_json(DOSSIER_JSON)
        for key, value in current_dossier["summary"].items():
            if stored_dossier["summary"].get(key) != value:
                failures.append(
                    f"summary_mismatch:{key}:stored={stored_dossier['summary'].get(key)}:current={value}"
                )

        expected_summary = {
            "dossier_ready": True,
            "evidence_digest_count": 5,
            "allowed_conclusion_token_count": 3,
            "p2_91_old_slice_writes_applied": 75,
            "p2_91_protected_path_writes": 0,
            "p2_92_original_item_count": 20,
            "p2_92_current_strict_complete_original_item_count": 20,
            "p2_94_submission_packet_ready": True,
            "p2_96_result_intake_ready": True,
            "p2_97_guard_state": "STOP_WAIT_EXTERNAL_OPUS_REVIEW",
            "actual_opus_result_present": False,
            "opus_approval_claimed": False,
            "mainline_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "goal_complete_now": False,
        }
        for key, expected in expected_summary.items():
            actual = stored_dossier["summary"].get(key)
            if actual != expected:
                failures.append(f"expected_summary_failed:{key}:expected={expected}:actual={actual}")

        if [item["id"] for item in stored_dossier["evidence_digest"]] != ["p2-91", "p2-92", "p2-94", "p2-96", "p2-97"]:
            failures.append("evidence_digest_ids_mismatch")
        if stored_dossier["allowed_conclusion_tokens"] != [
            "OPUS_PASS_SANDBOX_CLOSEOUT",
            "OPUS_REVISE_SANDBOX_CLOSEOUT",
            "OPUS_BLOCKED_NEEDS_USER",
        ]:
            failures.append("allowed_tokens_mismatch")

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

        text = DOSSIER_MD.read_text(encoding="utf-8")
        for needle in [
            "Single-File Opus Review Dossier",
            "Do not treat any pass as mainline approval",
            "Actual Opus result is not present",
            "OPUS_PASS_SANDBOX_CLOSEOUT",
            "OPUS_REVISE_SANDBOX_CLOSEOUT",
            "OPUS_BLOCKED_NEEDS_USER",
            "later sandbox-only result intake slice",
            "Do not merge mainline",
        ]:
            if needle not in text:
                failures.append(f"missing_dossier_text:{needle}")

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
    if DOSSIER_JSON.exists():
        dossier = load_json(DOSSIER_JSON)
        failure_case_count = len(load_json(FAILURES_JSON).get("failure_cases", [])) if FAILURES_JSON.exists() else 0
        summary = {
            "fixture_count": len(list(FIXTURES_DIR.glob("*.json"))),
            "failure_case_count": failure_case_count,
            "dossier_ready": dossier["summary"].get("dossier_ready"),
            "evidence_digest_count": dossier["summary"].get("evidence_digest_count"),
            "allowed_conclusion_token_count": dossier["summary"].get("allowed_conclusion_token_count"),
            "actual_opus_result_present": dossier["summary"].get("actual_opus_result_present"),
            "opus_approval_claimed": dossier["summary"].get("opus_approval_claimed"),
            "mainline_ready": dossier["summary"].get("mainline_ready"),
            "goal_complete_now": dossier["summary"].get("goal_complete_now"),
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

