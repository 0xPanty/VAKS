from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-93-opus-reviewable-closeout-packet-sandbox"
ROOT = Path(__file__).resolve().parents[5]
SLICE_DIR = ROOT / "outputs/review/vaks-implementation-sandbox" / SLICE_ID
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

BUILD_SCRIPT = ARTIFACT_DIR / "build_opus_reviewable_closeout_packet.py"
PACKET_JSON = ARTIFACT_DIR / "opus_reviewable_closeout_packet.json"
PACKET_MD = ARTIFACT_DIR / "opus_reviewable_closeout_packet.md"
PACKET_HTML = ARTIFACT_DIR / "opus_reviewable_closeout_packet.html"
CHECKLIST_MD = ARTIFACT_DIR / "opus-review-checklist.md"


def load_build_module():
    spec = importlib.util.spec_from_file_location("p2_93_build", BUILD_SCRIPT)
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


def fixture_expectations() -> dict[str, dict]:
    return {
        "p2-91-status-normalization-applied.json": {
            "p2_91_old_slice_writes_applied": 75,
            "p2_91_protected_path_writes": 0,
            "passed": True,
        },
        "p2-92-original-20-current-strict-complete.json": {
            "original_item_count": 20,
            "current_strict_complete_original_item_count": 20,
            "passed": True,
        },
        "p2-92-hash-and-body-preservation.json": {
            "current_file_hash_match_count": 75,
            "body_unchanged_count": 75,
            "non_status_frontmatter_unchanged_count": 75,
            "passed": True,
        },
        "external-review-boundary-clean.json": {
            "p2_92_old_slice_writes_applied": 0,
            "p2_92_protected_path_writes": 0,
            "external_review_packet_ready": True,
            "passed": True,
        },
        "opus-pending-not-claimed.json": {
            "opus_approval_claimed": False,
            "mainline_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "passed": True,
        },
    }


def check_no_cache_files() -> list[str]:
    failures = []
    for path in SLICE_DIR.rglob("*"):
        lowered = path.name.lower()
        if lowered == "__pycache__" or lowered.endswith(".pyc") or lowered.endswith(".tmp") or lowered.endswith(".log"):
            failures.append(f"cache_or_temp_file_present:{path.relative_to(SLICE_DIR)}")
    return failures


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
        PACKET_MD,
        PACKET_HTML,
        CHECKLIST_MD,
        FAILURE_DIR / "opus-reviewable-closeout-packet-failures.json",
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
            "original_item_count": 20,
            "status_operation_count": 75,
            "p2_80_transaction_operation_count": 75,
            "p2_91_old_slice_writes_applied": 75,
            "p2_91_protected_path_writes": 0,
            "p2_92_current_strict_status_operation_count": 75,
            "p2_92_current_file_hash_match_count": 75,
            "p2_92_body_unchanged_count": 75,
            "p2_92_non_status_frontmatter_unchanged_count": 75,
            "p2_92_current_strict_complete_original_item_count": 20,
            "p2_92_old_slice_writes_applied": 0,
            "p2_92_protected_path_writes": 0,
            "p2_92_final_gate_statuses_complete": True,
            "external_review_packet_ready": True,
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

        if len(stored_packet["original_item_ids"]) != 20:
            failures.append("original_item_ids_count_not_20")
        if len(stored_packet["opus_review_checklist"]) < 7:
            failures.append("opus_review_checklist_too_short")

        for filename, expected_values in fixture_expectations().items():
            path = FIXTURES_DIR / filename
            if not path.exists():
                failures.append(f"missing_fixture:{filename}")
                continue
            payload = load_json(path)
            for key, expected in expected_values.items():
                if payload.get(key) != expected:
                    failures.append(f"fixture_mismatch:{filename}:{key}:expected={expected}:actual={payload.get(key)}")

        failure_payload = load_json(FAILURE_DIR / "opus-reviewable-closeout-packet-failures.json")
        if len(failure_payload.get("failure_cases", [])) != 8:
            failures.append("failure_case_count_not_8")

        md_text = PACKET_MD.read_text(encoding="utf-8")
        html_text = PACKET_HTML.read_text(encoding="utf-8")
        checklist_text = CHECKLIST_MD.read_text(encoding="utf-8")
        for needle in [
            "does not claim Opus approval",
            "not claim Opus approval",
            "not mainline",
            "mainline integration",
            "reviewed knowledge",
            "action basis",
        ]:
            if needle not in md_text and needle not in html_text and needle not in checklist_text:
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
    if PACKET_JSON.exists():
        packet = load_json(PACKET_JSON)
        failure_case_count = 0
        failure_path = FAILURE_DIR / "opus-reviewable-closeout-packet-failures.json"
        if failure_path.exists():
            failure_case_count = len(load_json(failure_path).get("failure_cases", []))
        summary = {
            "fixture_count": len(list(FIXTURES_DIR.glob("*.json"))),
            "failure_case_count": failure_case_count,
            "original_item_count": packet["summary"].get("original_item_count"),
            "status_operation_count": packet["summary"].get("status_operation_count"),
            "p2_91_old_slice_writes_applied": packet["summary"].get("p2_91_old_slice_writes_applied"),
            "p2_92_current_strict_complete_original_item_count": packet["summary"].get(
                "p2_92_current_strict_complete_original_item_count"
            ),
            "external_review_packet_ready": packet["summary"].get("external_review_packet_ready"),
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

