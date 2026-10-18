from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path


SLICE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = SLICE_ROOT.parents[3]
SLICE_ID = SLICE_ROOT.name

CONTRACT = SLICE_ROOT / "artifact/old_file_status_normalization_transaction_package_contract.json"
PACKAGE_JSON = SLICE_ROOT / "artifact/old_file_status_normalization_transaction_package.json"
PACKAGE_MD = SLICE_ROOT / "artifact/old_file_status_normalization_transaction_package.md"
PACKAGE_HTML = SLICE_ROOT / "artifact/old_file_status_normalization_transaction_package.html"
BUILDER = SLICE_ROOT / "artifact/build_old_file_status_normalization_transaction_package.py"
VERIFIER = SLICE_ROOT / "artifact/verify_old_file_status_normalization_transaction_package.py"
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

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def add_failure(failures: list[str], condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def strict_package():
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_p2_80", STRICT_STATUS_PACKAGE)
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
    for path in [CONTRACT, PACKAGE_JSON, PACKAGE_MD, PACKAGE_HTML, BUILDER, VERIFIER]:
        add_failure(failures, path.is_file(), f"missing artifact: {path.name}")


def verify_package(contract: dict, package: dict, failures: list[str]) -> dict:
    add_failure(failures, package.get("record_kind") == "sandbox_old_file_status_normalization_transaction_package", "wrong record_kind")
    add_failure(failures, package.get("slice_id") == SLICE_ID, "wrong slice_id")

    summary = package.get("summary", {})
    for key, value in contract.get("expected_summary", {}).items():
        add_failure(failures, summary.get(key) == value, f"summary mismatch: {key}")

    gate = package.get("gate", {})
    for key, value in contract.get("expected_gate", {}).items():
        add_failure(failures, gate.get(key) == value, f"gate mismatch: {key}")

    flags = package.get("authority_flags", {})
    for key, value in contract.get("authority_flags", {}).items():
        add_failure(failures, flags.get(key) == value, f"authority flag mismatch: {key}")

    ops = package.get("transaction_operations", [])
    add_failure(failures, len(ops) == contract["expected_summary"]["transaction_operation_count"], "operation count mismatch")
    add_failure(failures, len({op.get("target_path") for op in ops}) == contract["expected_summary"]["unique_target_file_count"], "unique target count mismatch")
    add_failure(failures, len({op.get("old_slice_id") for op in ops}) == contract["expected_summary"]["target_old_slice_count"], "old slice count mismatch")
    add_failure(failures, all(SHA256_RE.match(op.get("current_target_file_sha256") or "") for op in ops), "missing or invalid sha256")
    add_failure(failures, all(op.get("prewrite_required_hash") == op.get("current_target_file_sha256") for op in ops), "prewrite hash mismatch")
    add_failure(failures, all(op.get("current_status_matches_manifest") is True for op in ops), "status drift in operation")
    add_failure(failures, all(op.get("proposed_status_already_applied") is False for op in ops), "proposed status already applied")
    add_failure(failures, all(op.get("rollback_status") == op.get("manifest_current_status") for op in ops), "rollback status mismatch")
    add_failure(failures, all(op.get("write_applied") is False for op in ops), "operation applied write")
    add_failure(failures, all(op.get("rollback_applied") is False for op in ops), "operation applied rollback")
    add_failure(failures, all(op.get("requires_exact_p2_75_approval") is True for op in ops), "operation lacks exact approval guard")
    add_failure(failures, all(op.get("requires_fresh_hash_check_before_write") is True for op in ops), "operation lacks hash guard")
    add_failure(failures, all(op.get("prewrite_hash_mismatch_blocks_execution") is True for op in ops), "hash mismatch does not block")

    preconditions = set(package.get("future_executor_preconditions", []))
    for required in [
        "future_user_message_must_exactly_match_p2_75_phrase",
        "fresh_prewrite_preflight_must_pass",
        "each_target_sha256_must_match_prewrite_required_hash",
        "boundary_audit_must_pass",
        "stop_before_write_must_be_observed",
    ]:
        add_failure(failures, required in preconditions, f"missing precondition: {required}")

    md = PACKAGE_MD.read_text(encoding="utf-8") if PACKAGE_MD.is_file() else ""
    add_failure(failures, "transaction_operation_count: `75`" in md, "Markdown missing transaction count")
    add_failure(failures, "executor_write_allowed_now: `false`" in md, "Markdown missing write block")
    add_failure(failures, "transaction_package_is_not_approval: `true`" in md, "Markdown missing approval boundary")
    add_failure(failures, "Hash match is process integrity, not evidence support" in md, "Markdown missing hash boundary")

    return {
        "transaction_operation_count": summary.get("transaction_operation_count"),
        "unique_target_file_count": summary.get("unique_target_file_count"),
        "target_old_slice_count": summary.get("target_old_slice_count"),
        "hash_record_count": summary.get("hash_record_count"),
        "current_status_mismatch_count": summary.get("current_status_mismatch_count"),
        "proposed_status_already_applied_count": summary.get("proposed_status_already_applied_count"),
        "executor_write_allowed_now": gate.get("executor_write_allowed_now"),
        "old_slice_writes_applied": summary.get("old_slice_writes_applied"),
    }


def verify_fixtures(contract: dict, package: dict, failures: list[str]) -> None:
    fixtures = [load_json(path) for path in (SLICE_ROOT / "fixtures").glob("*.json")]
    seen = {fixture.get("fixture_id") for fixture in fixtures}
    add_failure(failures, seen == set(contract.get("required_fixture_ids", [])), "fixture ids do not match contract")

    summary = package.get("summary", {})
    gate = package.get("gate", {})
    flags = package.get("authority_flags", {})
    ops = package.get("transaction_operations", [])
    merged = {}
    merged.update(summary)
    merged.update(gate)
    merged.update(flags)

    for fixture in fixtures:
        fixture_id = fixture.get("fixture_id")
        if fixture_id in {"transaction-counts-and-hashes", "no-write-authority"}:
            for key, value in fixture.get("expected", {}).items():
                if key == "all_hashes_sha256_hex":
                    add_failure(failures, all(SHA256_RE.match(op.get("current_target_file_sha256") or "") for op in ops) == value, f"{fixture_id} expected {key}")
                else:
                    add_failure(failures, merged.get(key) == value, f"{fixture_id} expected {key}")
        elif fixture_id == "rollback-status-preserved":
            expected = fixture.get("expected", {})
            add_failure(failures, all(op.get("rollback_status_equals_manifest_current_status") is True for op in ops) == expected.get("rollback_status_equals_manifest_current_status"), f"{fixture_id} rollback status")
            add_failure(failures, flags.get("rollback_applied") == expected.get("rollback_applied"), f"{fixture_id} rollback flag")
            add_failure(failures, summary.get("write_applied_count") == expected.get("write_applied_count"), f"{fixture_id} write count")
        elif fixture_id == "fresh-hash-precondition-required":
            expected = fixture.get("expected", {})
            add_failure(failures, gate.get("requires_fresh_hash_check_before_write") == expected.get("requires_fresh_hash_check_before_write"), f"{fixture_id} hash gate")
            add_failure(failures, all(op.get("prewrite_hash_mismatch_blocks_execution") is True for op in ops) == expected.get("prewrite_hash_mismatch_blocks_execution"), f"{fixture_id} hash block")
        elif fixture_id == "future-executor-must-stop-before-write":
            expected = fixture.get("expected", {})
            add_failure(failures, gate.get("requires_exact_p2_75_approval") == expected.get("requires_exact_p2_75_approval"), f"{fixture_id} exact approval")
            add_failure(failures, gate.get("requires_boundary_audit_before_write") == expected.get("requires_boundary_audit_before_write"), f"{fixture_id} boundary")
            add_failure(failures, gate.get("requires_stop_before_write") == expected.get("requires_stop_before_write"), f"{fixture_id} stop")
            add_failure(failures, gate.get("executor_write_allowed_now") is False, f"{fixture_id} immediate write allowed")


def verify_failure_cases(contract: dict, failures: list[str]) -> None:
    matrix = load_json(SLICE_ROOT / "failure-cases/old-file-status-normalization-transaction-package-failures.json")
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
    package = load_json(PACKAGE_JSON) if PACKAGE_JSON.is_file() else {}
    summary = verify_package(contract, package, failures) if package else {}
    verify_fixtures(contract, package, failures)
    verify_failure_cases(contract, failures)
    if args.final_gate:
        verify_final_gate(failures)

    result = {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "fixture_count": len(list((SLICE_ROOT / "fixtures").glob("*.json"))),
            "failure_case_count": len(load_json(SLICE_ROOT / "failure-cases/old-file-status-normalization-transaction-package-failures.json").get("failure_cases", [])),
            **summary,
            "final_gate": bool(args.final_gate),
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
