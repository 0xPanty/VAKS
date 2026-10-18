from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-94-opus-review-submission-packet-sandbox"
ROOT = Path(__file__).resolve().parents[5]
SLICE_DIR = ROOT / "outputs/review/vaks-implementation-sandbox" / SLICE_ID
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

BUILD_SCRIPT = ARTIFACT_DIR / "build_opus_review_submission_packet.py"
PACKET_JSON = ARTIFACT_DIR / "opus-review-submission-packet.json"
MANIFEST_JSON = ARTIFACT_DIR / "opus-review-evidence-manifest.json"
MANIFEST_MD = ARTIFACT_DIR / "opus-review-evidence-manifest.md"
PROMPT_MD = ARTIFACT_DIR / "opus-review-submission-prompt.md"
INTAKE_GATE_MD = ARTIFACT_DIR / "opus-result-intake-gate.md"
FAILURES_JSON = FAILURE_DIR / "opus-review-submission-packet-failures.json"


def load_build_module():
    spec = importlib.util.spec_from_file_location("p2_94_build", BUILD_SCRIPT)
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
        "submission-prompt-ready.json": {
            "evidence_item_count": 7,
            "review_question_count": 6,
            "submission_packet_ready": True,
            "passed": True,
        },
        "p2-93-evidence-ready-not-opus-approved.json": {
            "p2_93_external_review_packet_ready": True,
            "p2_93_opus_approval_claimed": False,
            "passed": True,
        },
        "p2-91-p2-92-proof-carried-forward.json": {
            "p2_91_old_slice_writes_applied": 75,
            "p2_91_protected_path_writes": 0,
            "p2_92_status_operation_count": 75,
            "p2_92_current_strict_complete_original_item_count": 20,
            "passed": True,
        },
        "allowed-opus-conclusions.json": {
            "allowed_external_conclusions": [
                "OPUS_PASS_SANDBOX_CLOSEOUT",
                "OPUS_REVISE_SANDBOX_CLOSEOUT",
                "OPUS_BLOCKED_NEEDS_USER",
            ],
            "passed": True,
        },
        "authority-boundaries-false.json": {
            "opus_review_performed": False,
            "opus_approval_claimed": False,
            "mainline_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "goal_complete_now": False,
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
        PACKET_JSON,
        MANIFEST_JSON,
        MANIFEST_MD,
        PROMPT_MD,
        INTAKE_GATE_MD,
        FAILURES_JSON,
    ]
    for path in required_files:
        if not path.exists():
            failures.append(f"missing_required_file:{path.relative_to(SLICE_DIR)}")

    if not failures:
        build_module = load_build_module()
        current_packet = build_module.build_packet()
        stored_packet = load_json(PACKET_JSON)
        for key, value in current_packet["summary"].items():
            if stored_packet["summary"].get(key) != value:
                failures.append(
                    f"summary_mismatch:{key}:stored={stored_packet['summary'].get(key)}:current={value}"
                )

        expected_summary = {
            "evidence_item_count": 7,
            "review_question_count": 6,
            "required_conclusion_token_count": 3,
            "p2_93_external_review_packet_ready": True,
            "p2_93_opus_approval_claimed": False,
            "p2_91_old_slice_writes_applied": 75,
            "p2_91_protected_path_writes": 0,
            "p2_92_status_operation_count": 75,
            "p2_92_current_strict_complete_original_item_count": 20,
            "submission_packet_ready": True,
            "opus_review_performed": False,
            "opus_approval_claimed": False,
            "mainline_ready": False,
            "promotion_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "goal_complete_now": False,
        }
        for key, expected in expected_summary.items():
            actual = stored_packet["summary"].get(key)
            if actual != expected:
                failures.append(f"expected_summary_failed:{key}:expected={expected}:actual={actual}")

        manifest = load_json(MANIFEST_JSON)
        if len(manifest.get("evidence_items", [])) != 7:
            failures.append("manifest_evidence_item_count_not_7")
        if len(manifest.get("review_questions", [])) != 6:
            failures.append("manifest_review_question_count_not_6")
        missing_evidence_paths = [
            item["path"] for item in manifest.get("evidence_items", []) if not (ROOT / item["path"]).exists()
        ]
        if missing_evidence_paths:
            failures.append(f"manifest_missing_evidence_paths:{','.join(missing_evidence_paths)}")

        prompt_text = PROMPT_MD.read_text(encoding="utf-8")
        gate_text = INTAKE_GATE_MD.read_text(encoding="utf-8")
        for token in [
            "OPUS_PASS_SANDBOX_CLOSEOUT",
            "OPUS_REVISE_SANDBOX_CLOSEOUT",
            "OPUS_BLOCKED_NEEDS_USER",
        ]:
            if token not in prompt_text or token not in gate_text:
                failures.append(f"missing_opus_token:{token}")
        for needle in [
            "Do not assume sandbox closeout means mainline merge",
            "Do not translate Opus pass into mainline merge",
            "Do not translate Opus pass into reviewed knowledge",
            "not claim Opus approval",
            "action basis",
        ]:
            if needle not in prompt_text and needle not in gate_text:
                failures.append(f"missing_boundary_text:{needle}")

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
    if PACKET_JSON.exists():
        packet = load_json(PACKET_JSON)
        failure_case_count = len(load_json(FAILURES_JSON).get("failure_cases", [])) if FAILURES_JSON.exists() else 0
        summary = {
            "fixture_count": len(list(FIXTURES_DIR.glob("*.json"))),
            "failure_case_count": failure_case_count,
            "evidence_item_count": packet["summary"].get("evidence_item_count"),
            "review_question_count": packet["summary"].get("review_question_count"),
            "submission_packet_ready": packet["summary"].get("submission_packet_ready"),
            "opus_review_performed": packet["summary"].get("opus_review_performed"),
            "opus_approval_claimed": packet["summary"].get("opus_approval_claimed"),
            "mainline_ready": packet["summary"].get("mainline_ready"),
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

