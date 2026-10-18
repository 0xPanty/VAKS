from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


SLICE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = SLICE_ROOT.parents[3]
SLICE_ID = SLICE_ROOT.name

CONTRACT = SLICE_ROOT / "artifact/old_file_status_normalization_transaction_simulation_contract.json"
SIM_JSON = SLICE_ROOT / "artifact/old_file_status_normalization_transaction_simulation.json"
SIM_MD = SLICE_ROOT / "artifact/old_file_status_normalization_transaction_simulation.md"
SIM_HTML = SLICE_ROOT / "artifact/old_file_status_normalization_transaction_simulation.html"
BUILDER = SLICE_ROOT / "artifact/build_old_file_status_normalization_transaction_simulation.py"
VERIFIER = SLICE_ROOT / "artifact/verify_old_file_status_normalization_transaction_simulation.py"
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
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_p2_81", STRICT_STATUS_PACKAGE)
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
    for path in [CONTRACT, SIM_JSON, SIM_MD, SIM_HTML, BUILDER, VERIFIER]:
        add_failure(failures, path.is_file(), f"missing artifact: {path.name}")


def verify_simulation(contract: dict, simulation: dict, failures: list[str]) -> dict:
    add_failure(failures, simulation.get("record_kind") == "sandbox_old_file_status_normalization_transaction_simulation", "wrong record_kind")
    add_failure(failures, simulation.get("slice_id") == SLICE_ID, "wrong slice_id")

    summary = simulation.get("summary", {})
    for key, value in contract.get("expected_summary", {}).items():
        add_failure(failures, summary.get(key) == value, f"summary mismatch: {key}")

    gate = simulation.get("gate", {})
    for key, value in contract.get("expected_gate", {}).items():
        add_failure(failures, gate.get(key) == value, f"gate mismatch: {key}")

    flags = simulation.get("authority_flags", {})
    for key, value in contract.get("authority_flags", {}).items():
        add_failure(failures, flags.get(key) == value, f"authority flag mismatch: {key}")

    results = simulation.get("simulation_results", [])
    add_failure(failures, len(results) == contract["expected_summary"]["simulated_operation_count"], "simulation result count mismatch")
    add_failure(failures, len({item.get("target_path") for item in results}) == contract["expected_summary"]["unique_target_file_count"], "unique target count mismatch")
    add_failure(failures, len({item.get("old_slice_id") for item in results}) == contract["expected_summary"]["target_old_slice_count"], "old slice count mismatch")
    add_failure(failures, all(item.get("before_hash_matches_p2_80") is True for item in results), "target hash drifted before simulation")
    add_failure(failures, all(item.get("before_status") == item.get("p2_80_before_status") for item in results), "before status mismatch")
    add_failure(failures, all(item.get("after_status_matches_proposed") is True for item in results), "after status not proposed")
    add_failure(failures, all(item.get("rollback_status_matches_rollback_status") is True for item in results), "rollback status mismatch")
    add_failure(failures, all(item.get("body_unchanged") is True for item in results), "body changed")
    add_failure(failures, all(item.get("non_status_frontmatter_unchanged") is True for item in results), "non-status frontmatter changed")
    add_failure(failures, all(item.get("rollback_sha_matches_original") is True for item in results), "rollback sha mismatch")
    add_failure(failures, all(item.get("status_only_change") is True for item in results), "non-status change detected")
    add_failure(failures, all(item.get("write_applied") is False for item in results), "simulation applied write")
    add_failure(failures, all(item.get("old_slice_write_applied") is False for item in results), "simulation applied old slice write")

    md = SIM_MD.read_text(encoding="utf-8") if SIM_MD.is_file() else ""
    add_failure(failures, "simulated_operation_count: `75`" in md, "Markdown missing operation count")
    add_failure(failures, "body_unchanged_count: `75`" in md, "Markdown missing body unchanged count")
    add_failure(failures, "rollback_sha_match_count: `75`" in md, "Markdown missing rollback sha count")
    add_failure(failures, "executor_write_allowed_now: `false`" in md, "Markdown missing write block")
    add_failure(failures, "Simulation success is not approval" in md, "Markdown missing approval boundary")

    return {
        "simulated_operation_count": summary.get("simulated_operation_count"),
        "after_status_match_count": summary.get("after_status_match_count"),
        "rollback_status_match_count": summary.get("rollback_status_match_count"),
        "body_unchanged_count": summary.get("body_unchanged_count"),
        "rollback_sha_match_count": summary.get("rollback_sha_match_count"),
        "status_only_change_count": summary.get("status_only_change_count"),
        "simulation_failure_count": summary.get("simulation_failure_count"),
        "executor_write_allowed_now": gate.get("executor_write_allowed_now"),
        "old_slice_writes_applied": summary.get("old_slice_writes_applied"),
    }


def verify_fixtures(contract: dict, simulation: dict, failures: list[str]) -> None:
    fixtures = [load_json(path) for path in (SLICE_ROOT / "fixtures").glob("*.json")]
    seen = {fixture.get("fixture_id") for fixture in fixtures}
    add_failure(failures, seen == set(contract.get("required_fixture_ids", [])), "fixture ids do not match contract")

    summary = simulation.get("summary", {})
    gate = simulation.get("gate", {})
    flags = simulation.get("authority_flags", {})
    merged = {}
    merged.update(summary)
    merged.update(gate)
    merged.update(flags)

    for fixture in fixtures:
        fixture_id = fixture.get("fixture_id")
        if fixture_id in {"all-operations-simulate-status-only", "body-content-preserved", "simulation-not-approval"}:
            for key, value in fixture.get("expected", {}).items():
                if key == "body_change_count":
                    add_failure(failures, (summary.get("simulated_operation_count", 0) - summary.get("body_unchanged_count", 0)) == value, f"{fixture_id} expected {key}")
                else:
                    add_failure(failures, merged.get(key) == value, f"{fixture_id} expected {key}")
        elif fixture_id == "rollback-restores-original":
            for key, value in fixture.get("expected", {}).items():
                add_failure(failures, merged.get(key) == value, f"{fixture_id} expected {key}")
        elif fixture_id == "future-real-write-still-gated":
            expected = fixture.get("expected", {})
            add_failure(failures, gate.get("requires_exact_p2_75_approval_before_real_write") == expected.get("requires_exact_p2_75_approval_before_real_write"), f"{fixture_id} exact approval")
            add_failure(failures, gate.get("requires_fresh_hash_check_before_real_write") == expected.get("requires_fresh_hash_check_before_real_write"), f"{fixture_id} hash")
            add_failure(failures, gate.get("requires_stop_before_write") == expected.get("requires_stop_before_write"), f"{fixture_id} stop")
            add_failure(failures, gate.get("executor_write_allowed_now") is False, f"{fixture_id} immediate write allowed")


def verify_failure_cases(contract: dict, failures: list[str]) -> None:
    matrix = load_json(SLICE_ROOT / "failure-cases/old-file-status-normalization-transaction-simulation-failures.json")
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
    simulation = load_json(SIM_JSON) if SIM_JSON.is_file() else {}
    summary = verify_simulation(contract, simulation, failures) if simulation else {}
    verify_fixtures(contract, simulation, failures)
    verify_failure_cases(contract, failures)
    if args.final_gate:
        verify_final_gate(failures)

    result = {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "fixture_count": len(list((SLICE_ROOT / "fixtures").glob("*.json"))),
            "failure_case_count": len(load_json(SLICE_ROOT / "failure-cases/old-file-status-normalization-transaction-simulation-failures.json").get("failure_cases", [])),
            **summary,
            "final_gate": bool(args.final_gate),
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
