from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


SLICE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = SLICE_ROOT.parents[3]
SLICE_ID = SLICE_ROOT.name

CONTRACT = SLICE_ROOT / "artifact/fresh_preflight_drift_recheck_contract.json"
RECHECK_JSON = SLICE_ROOT / "artifact/fresh_preflight_drift_recheck.json"
RECHECK_MD = SLICE_ROOT / "artifact/fresh_preflight_drift_recheck.md"
RECHECK_HTML = SLICE_ROOT / "artifact/fresh_preflight_drift_recheck.html"
BUILDER = SLICE_ROOT / "artifact/build_fresh_preflight_drift_recheck.py"
VERIFIER = SLICE_ROOT / "artifact/verify_fresh_preflight_drift_recheck.py"
STRICT_STATUS_PACKAGE = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-16-p2-67-user-decision-strict-status-package-sandbox/artifact/strict_status_package.py"

FINAL_STATUSES = {
    "verification.md": "local_verification_passed",
    "reviewer-report.md": "review_pass_no_blocker",
    "boundary-audit.md": "pass_boundary",
    "product-acceptance-report.md": "pass_product_grade",
    "next-step.md": "pass_product_grade_pending_next_slice",
}

REQUIRED_ROOT_FILES = [
    "slice-plan.md",
    "source-map.md",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def add_failure(failures: list[str], condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def strict_package():
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_p2_79", STRICT_STATUS_PACKAGE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load strict status package")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def strict_status(path: Path) -> str | None:
    parsed = strict_package().parse_strict_frontmatter_status(path.read_text(encoding="utf-8"))
    return parsed.get("status") if parsed.get("valid") else None


def verify_files(failures: list[str]) -> None:
    for name in REQUIRED_ROOT_FILES:
        add_failure(failures, (SLICE_ROOT / name).is_file(), f"missing root file: {name}")
    for path in [CONTRACT, RECHECK_JSON, RECHECK_MD, RECHECK_HTML, BUILDER, VERIFIER]:
        add_failure(failures, path.is_file(), f"missing artifact: {path.name}")


def verify_recheck(contract: dict, recheck: dict, failures: list[str]) -> dict:
    add_failure(failures, recheck.get("record_kind") == "sandbox_fresh_preflight_drift_recheck", "wrong record_kind")
    add_failure(failures, recheck.get("slice_id") == SLICE_ID, "wrong slice_id")

    summary = recheck.get("summary", {})
    for key, value in contract.get("expected_summary", {}).items():
        add_failure(failures, summary.get(key) == value, f"summary mismatch: {key}")

    gate = recheck.get("gate", {})
    for key, value in contract.get("expected_gate", {}).items():
        add_failure(failures, gate.get(key) == value, f"gate mismatch: {key}")

    flags = recheck.get("authority_flags", {})
    for key, value in contract.get("authority_flags", {}).items():
        add_failure(failures, flags.get(key) == value, f"authority flag mismatch: {key}")

    checked = recheck.get("checked_changes", [])
    add_failure(failures, len(checked) == contract["expected_summary"]["target_change_count"], "checked change count mismatch")
    add_failure(failures, all(item.get("write_applied") is False for item in checked), "some checked change applied a write")
    add_failure(failures, all(item.get("body_edit_planned") is False for item in checked), "body edit planned")
    add_failure(failures, all(item.get("artifact_edit_planned") is False for item in checked), "artifact edit planned")
    add_failure(failures, all(item.get("requires_exact_approval_before_write") is True for item in checked), "some checked change lacks exact approval guard")
    add_failure(failures, all(item.get("current_status_matches_manifest") is True for item in checked), "some checked change does not match manifest")
    add_failure(failures, all(item.get("proposed_status_already_applied") is False for item in checked), "some proposed status already applied")

    blocked_if = recheck.get("blocked_if", {})
    for key in [
        "missing_target_count_positive",
        "frontmatter_invalid_count_positive",
        "current_status_mismatch_count_positive",
        "proposed_status_already_applied_count_positive",
    ]:
        add_failure(failures, blocked_if.get(key) is False, f"blocked_if is positive: {key}")

    md = RECHECK_MD.read_text(encoding="utf-8") if RECHECK_MD.is_file() else ""
    add_failure(failures, "target_change_count: `75`" in md, "Markdown missing target count")
    add_failure(failures, "current_status_mismatch_count: `0`" in md, "Markdown missing mismatch count")
    add_failure(failures, "executor_write_allowed: `false`" in md, "Markdown missing write block")
    add_failure(failures, "Clean drift recheck is not approval" in md, "Markdown missing approval boundary")

    return {
        "target_change_count": summary.get("target_change_count"),
        "target_file_count": summary.get("target_file_count"),
        "target_old_slice_count": summary.get("target_old_slice_count"),
        "missing_target_count": summary.get("missing_target_count"),
        "frontmatter_invalid_count": summary.get("frontmatter_invalid_count"),
        "current_status_mismatch_count": summary.get("current_status_mismatch_count"),
        "proposed_status_already_applied_count": summary.get("proposed_status_already_applied_count"),
        "fresh_drift_recheck_passed": gate.get("fresh_drift_recheck_passed"),
        "executor_write_allowed": gate.get("executor_write_allowed"),
        "old_slice_writes_applied": summary.get("old_slice_writes_applied"),
    }


def verify_fixtures(contract: dict, recheck: dict, failures: list[str]) -> None:
    fixtures = [load_json(path) for path in (SLICE_ROOT / "fixtures").glob("*.json")]
    seen = {fixture.get("fixture_id") for fixture in fixtures}
    add_failure(failures, seen == set(contract.get("required_fixture_ids", [])), "fixture ids do not match contract")

    summary = recheck.get("summary", {})
    gate = recheck.get("gate", {})
    flags = recheck.get("authority_flags", {})
    merged = {}
    merged.update(summary)
    merged.update(gate)
    merged.update(flags)

    for fixture in fixtures:
        fixture_id = fixture.get("fixture_id")
        if fixture_id in {"all-targets-current-status-match-manifest", "approval-still-not-collected", "fresh-check-is-not-write-authority"}:
            for key, value in fixture.get("expected", {}).items():
                add_failure(failures, merged.get(key) == value, f"{fixture_id} expected {key}")
        elif fixture_id == "applied-or-drifted-targets-would-block":
            add_failure(failures, fixture.get("expected_clean_now") is True, f"{fixture_id} expected clean now")
            for key in fixture.get("expected_block_when_any_positive", []):
                add_failure(failures, summary.get(key) == 0, f"{fixture_id} positive blocker {key}")
        elif fixture_id == "generic-continuation-still-rejected":
            add_failure(failures, gate.get("generic_language_is_not_approval") is True, f"{fixture_id} generic language allowed")


def verify_failure_cases(contract: dict, failures: list[str]) -> None:
    matrix = load_json(SLICE_ROOT / "failure-cases/fresh-preflight-drift-recheck-failures.json")
    actual = {case.get("case_id") for case in matrix.get("failure_cases", [])}
    add_failure(failures, actual == set(contract.get("required_failure_case_ids", [])), "failure case ids do not match contract")


def verify_final_gate(failures: list[str]) -> None:
    for file_name, expected in FINAL_STATUSES.items():
        add_failure(failures, strict_status(SLICE_ROOT / file_name) == expected, f"{file_name} status not passed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--final-gate", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    verify_files(failures)
    contract = load_json(CONTRACT)
    recheck = load_json(RECHECK_JSON) if RECHECK_JSON.is_file() else {}
    summary = verify_recheck(contract, recheck, failures) if recheck else {}
    verify_fixtures(contract, recheck, failures)
    verify_failure_cases(contract, failures)
    if args.final_gate:
        verify_final_gate(failures)

    result = {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "fixture_count": len(list((SLICE_ROOT / "fixtures").glob("*.json"))),
            "failure_case_count": len(load_json(SLICE_ROOT / "failure-cases/fresh-preflight-drift-recheck-failures.json").get("failure_cases", [])),
            **summary,
            "final_gate": bool(args.final_gate),
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
