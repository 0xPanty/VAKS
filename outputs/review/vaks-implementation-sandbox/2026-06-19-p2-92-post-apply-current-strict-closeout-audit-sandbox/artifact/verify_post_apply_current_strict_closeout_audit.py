from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-92-post-apply-current-strict-closeout-audit-sandbox"
ROOT = Path(__file__).resolve().parents[5]
SLICE_DIR = ROOT / "outputs/review/vaks-implementation-sandbox" / SLICE_ID
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

REPORT_JSON = ARTIFACT_DIR / "post_apply_current_strict_closeout_audit.json"
REPORT_MD = ARTIFACT_DIR / "post_apply_current_strict_closeout_audit.md"
REPORT_HTML = ARTIFACT_DIR / "post_apply_current_strict_closeout_audit.html"
BUILD_SCRIPT = ARTIFACT_DIR / "build_post_apply_current_strict_closeout_audit.py"


def load_build_module():
    spec = importlib.util.spec_from_file_location("p2_92_build", BUILD_SCRIPT)
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
        "all-75-current-strict-statuses-present.json": {
            "status_operation_count": 75,
            "current_strict_status_operation_count": 75,
            "passed": True,
        },
        "all-20-original-items-current-strict-complete.json": {
            "original_item_count": 20,
            "current_strict_complete_original_item_count": 20,
            "passed": True,
        },
        "body-and-non-status-frontmatter-preserved.json": {
            "body_unchanged_count": 75,
            "non_status_frontmatter_unchanged_count": 75,
            "passed": True,
        },
        "protected-paths-not-written.json": {
            "p2_91_protected_path_writes": 0,
            "p2_92_protected_path_writes": 0,
            "passed": True,
        },
        "sandbox-not-mainline-or-truth-authority.json": {
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
        REPORT_JSON,
        REPORT_MD,
        REPORT_HTML,
        FAILURE_DIR / "post-apply-current-strict-closeout-failures.json",
    ]
    for path in required_files:
        if not path.exists():
            failures.append(f"missing_required_file:{path.relative_to(SLICE_DIR)}")

    if not failures:
        build_module = load_build_module()
        current_report = build_module.build_report()
        stored_report = load_json(REPORT_JSON)
        for key, value in current_report["summary"].items():
            if stored_report["summary"].get(key) != value:
                failures.append(
                    f"summary_mismatch:{key}:stored={stored_report['summary'].get(key)}:current={value}"
                )
        current_by_target = {
            item["target_path"]: item for item in current_report["operation_results"]
        }
        stored_by_target = {
            item["target_path"]: item for item in stored_report["operation_results"]
        }
        if set(current_by_target) != set(stored_by_target):
            failures.append("operation_target_set_mismatch")
        else:
            for target_path, current_item in current_by_target.items():
                stored_item = stored_by_target[target_path]
                for field in [
                    "current_status",
                    "current_file_sha256",
                    "current_body_sha256",
                    "current_non_status_frontmatter_sha256",
                    "current_strict_status_operation_complete",
                ]:
                    if current_item[field] != stored_item[field]:
                        failures.append(f"operation_mismatch:{target_path}:{field}")

        summary = stored_report["summary"]
        expected_summary = {
            "original_item_count": 20,
            "status_operation_count": 75,
            "missing_p2_91_target_count": 0,
            "current_strict_status_operation_count": 75,
            "current_file_hash_match_count": 75,
            "body_unchanged_count": 75,
            "non_status_frontmatter_unchanged_count": 75,
            "current_strict_complete_original_item_count": 20,
            "p2_91_old_slice_writes_applied": 75,
            "p2_91_protected_path_writes": 0,
            "p2_92_old_slice_writes_applied": 0,
            "p2_92_protected_path_writes": 0,
            "sandbox_original_20_current_strict_closeout_complete": True,
            "ready_for_opus_review_packet": True,
            "mainline_ready": False,
            "promotion_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "goal_complete_now": False,
        }
        for key, expected in expected_summary.items():
            if summary.get(key) != expected:
                failures.append(f"expected_summary_failed:{key}:expected={expected}:actual={summary.get(key)}")

        if len(stored_report["original_item_results"]) != 20:
            failures.append("original_item_results_count_not_20")
        incomplete_groups = [
            item["old_slice_id"] for item in stored_report["original_item_results"] if not item["current_strict_complete"]
        ]
        if incomplete_groups:
            failures.append(f"incomplete_original_item_groups:{','.join(incomplete_groups)}")
        incomplete_ops = [
            item["target_path"]
            for item in stored_report["operation_results"]
            if not item["current_strict_status_operation_complete"]
        ]
        if incomplete_ops:
            failures.append(f"incomplete_operations:{','.join(incomplete_ops[:5])}")

        fixtures = fixture_expectations()
        for filename, expected_values in fixtures.items():
            path = FIXTURES_DIR / filename
            if not path.exists():
                failures.append(f"missing_fixture:{filename}")
                continue
            payload = load_json(path)
            for key, expected in expected_values.items():
                if payload.get(key) != expected:
                    failures.append(f"fixture_mismatch:{filename}:{key}:expected={expected}:actual={payload.get(key)}")

        failure_payload = load_json(FAILURE_DIR / "post-apply-current-strict-closeout-failures.json")
        if len(failure_payload.get("failure_cases", [])) != 8:
            failures.append("failure_case_count_not_8")

        md_text = REPORT_MD.read_text(encoding="utf-8")
        html_text = REPORT_HTML.read_text(encoding="utf-8")
        for needle in [
            "sandbox closeout audit only",
            "not a mainline merge",
            "not a mainline merge, promotion, reviewed knowledge, evidence support, action basis, or Opus approval",
        ]:
            if needle not in md_text and needle not in html_text:
                failures.append(f"missing_authority_text:{needle}")

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
    if REPORT_JSON.exists():
        stored = load_json(REPORT_JSON)
        summary = {
            "fixture_count": len(list(FIXTURES_DIR.glob("*.json"))),
            "failure_case_count": len(load_json(FAILURE_DIR / "post-apply-current-strict-closeout-failures.json").get("failure_cases", []))
            if (FAILURE_DIR / "post-apply-current-strict-closeout-failures.json").exists()
            else 0,
            "original_item_count": stored["summary"].get("original_item_count"),
            "status_operation_count": stored["summary"].get("status_operation_count"),
            "current_strict_status_operation_count": stored["summary"].get("current_strict_status_operation_count"),
            "current_file_hash_match_count": stored["summary"].get("current_file_hash_match_count"),
            "body_unchanged_count": stored["summary"].get("body_unchanged_count"),
            "non_status_frontmatter_unchanged_count": stored["summary"].get("non_status_frontmatter_unchanged_count"),
            "current_strict_complete_original_item_count": stored["summary"].get(
                "current_strict_complete_original_item_count"
            ),
            "p2_92_old_slice_writes_applied": stored["summary"].get("p2_92_old_slice_writes_applied"),
            "p2_92_protected_path_writes": stored["summary"].get("p2_92_protected_path_writes"),
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

