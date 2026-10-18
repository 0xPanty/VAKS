from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


SLICE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = SLICE_ROOT.parents[3]
SLICE_ID = SLICE_ROOT.name

CONTRACT = SLICE_ROOT / "artifact/old_file_status_normalization_executor_readiness_gate_contract.json"
GATE_JSON = SLICE_ROOT / "artifact/old_file_status_normalization_executor_readiness_gate.json"
GATE_MD = SLICE_ROOT / "artifact/old_file_status_normalization_executor_readiness_gate.md"
GATE_HTML = SLICE_ROOT / "artifact/old_file_status_normalization_executor_readiness_gate.html"
BUILDER = SLICE_ROOT / "artifact/build_old_file_status_normalization_executor_readiness_gate.py"
VERIFIER = SLICE_ROOT / "artifact/verify_old_file_status_normalization_executor_readiness_gate.py"
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
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_p2_77", STRICT_STATUS_PACKAGE)
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
    for path in [CONTRACT, GATE_JSON, GATE_MD, GATE_HTML, BUILDER, VERIFIER]:
        add_failure(failures, path.is_file(), f"missing artifact: {path.name}")


def verify_gate(contract: dict, gate: dict, failures: list[str]) -> dict:
    add_failure(failures, gate.get("record_kind") == "sandbox_old_file_status_normalization_executor_readiness_gate", "wrong record_kind")
    add_failure(failures, gate.get("slice_id") == SLICE_ID, "wrong slice_id")
    decision = gate.get("current_decision", {})
    for key, value in contract.get("expected_current_decision", {}).items():
        add_failure(failures, decision.get(key) == value, f"decision mismatch: {key}")
    numbers = gate.get("preflight_summary", {})
    for key, value in contract.get("expected_numbers", {}).items():
        add_failure(failures, numbers.get(key) == value, f"number mismatch: {key}")
    flags = gate.get("authority_flags", {})
    for key, value in contract.get("authority_flags", {}).items():
        add_failure(failures, flags.get(key) == value, f"authority flag mismatch: {key}")

    future = gate.get("future_exact_approval_scenario", {})
    expected_future = contract.get("future_if_exact_approval_present", {})
    for key, value in expected_future.items():
        actual_key = "readiness" if key == "readiness" else key
        add_failure(failures, future.get(actual_key) == value, f"future scenario mismatch: {key}")
    add_failure(failures, future.get("executor_write_allowed_immediately") is False, "future scenario allows immediate write")

    drift = gate.get("future_exact_approval_preflight_drift_scenario", {})
    expected_drift = contract.get("future_if_exact_approval_but_preflight_drift", {})
    for key, value in expected_drift.items():
        add_failure(failures, drift.get(key) == value, f"preflight drift scenario mismatch: {key}")
    representative_drift = drift.get("representative_drift", {})
    add_failure(failures, representative_drift.get("missing_target_count", 0) > 0, "preflight drift fixture has no missing target")
    add_failure(failures, representative_drift.get("current_status_mismatch_count", 0) > 0, "preflight drift fixture has no status mismatch")

    generic = gate.get("generic_language_scenarios", [])
    add_failure(failures, generic and all(item.get("approval_phrase_matched") is False for item in generic), "generic language matched approval")
    add_failure(failures, all(item.get("readiness") == "blocked_no_exact_approval" for item in generic), "generic language not blocked")

    md = GATE_MD.read_text(encoding="utf-8") if GATE_MD.is_file() else ""
    add_failure(failures, "readiness: `blocked_no_exact_approval`" in md, "Markdown missing blocked readiness")
    add_failure(failures, "readiness: `blocked_preflight_drift`" in md, "Markdown missing preflight drift block")
    add_failure(failures, "executor write allowed: `false`" in md, "Markdown missing write block")
    add_failure(failures, "Current goal continuation is not approval" in md, "Markdown missing continuation boundary")
    return {
        "readiness": decision.get("readiness"),
        "approval_phrase_matched": decision.get("approval_phrase_matched"),
        "preflight_clean": decision.get("preflight_clean"),
        "executor_write_allowed": decision.get("executor_write_allowed"),
        "target_change_count": numbers.get("target_change_count"),
        "old_slice_writes_applied": decision.get("old_slice_writes_applied"),
    }


def verify_fixtures(contract: dict, gate: dict, failures: list[str]) -> None:
    fixtures = [load_json(path) for path in (SLICE_ROOT / "fixtures").glob("*.json")]
    seen = {fixture.get("fixture_id") for fixture in fixtures}
    add_failure(failures, seen == set(contract.get("required_fixture_ids", [])), "fixture ids do not match contract")
    decision = gate.get("current_decision", {})
    flags = gate.get("authority_flags", {})
    future = gate.get("future_exact_approval_scenario", {})
    drift = gate.get("future_exact_approval_preflight_drift_scenario", {})
    generic = gate.get("generic_language_scenarios", [])
    merged = {}
    merged.update(decision)
    merged.update(flags)
    for fixture in fixtures:
        fixture_id = fixture.get("fixture_id")
        if fixture_id == "current-continuation-blocked":
            for key, value in fixture.get("expected", {}).items():
                add_failure(failures, decision.get(key) == value, f"{fixture_id} expected {key}")
        elif fixture_id == "exact-approval-future-scenario":
            expected = fixture.get("expected", {})
            add_failure(failures, future.get("approval_phrase_matched") == expected.get("approval_phrase_matched"), f"{fixture_id} approval")
            add_failure(failures, future.get("readiness") == expected.get("future_readiness"), f"{fixture_id} readiness")
            add_failure(failures, future.get("still_requires_fresh_preflight") == expected.get("still_requires_fresh_preflight"), f"{fixture_id} fresh preflight")
            add_failure(failures, future.get("still_requires_stop_before_write") == expected.get("still_requires_stop_before_write"), f"{fixture_id} stop before write")
        elif fixture_id == "generic-language-rejected":
            add_failure(failures, all(item.get("readiness") == "blocked_no_exact_approval" for item in generic), f"{fixture_id} generic not rejected")
        elif fixture_id == "clean-preflight-still-not-approval":
            for key, value in fixture.get("expected", {}).items():
                add_failure(failures, merged.get(key) == value, f"{fixture_id} expected {key}")
        elif fixture_id == "exact-approval-preflight-drift-blocked":
            for key, value in fixture.get("expected", {}).items():
                add_failure(failures, drift.get(key) == value, f"{fixture_id} expected {key}")


def verify_failure_cases(contract: dict, failures: list[str]) -> None:
    matrix = load_json(SLICE_ROOT / "failure-cases/old-file-status-normalization-executor-readiness-gate-failures.json")
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
    gate = load_json(GATE_JSON) if GATE_JSON.is_file() else {}
    summary = verify_gate(contract, gate, failures) if gate else {}
    verify_fixtures(contract, gate, failures)
    verify_failure_cases(contract, failures)
    if args.final_gate:
        verify_final_gate(failures)

    result = {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "fixture_count": len(list((SLICE_ROOT / "fixtures").glob("*.json"))),
            "failure_case_count": len(load_json(SLICE_ROOT / "failure-cases/old-file-status-normalization-executor-readiness-gate-failures.json").get("failure_cases", [])),
            **summary,
            "final_gate": bool(args.final_gate),
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
