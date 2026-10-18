from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


SLICE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = SLICE_ROOT.parents[3]
SLICE_ID = SLICE_ROOT.name

CONTRACT_PATH = SLICE_ROOT / "artifact/original_20_current_strict_sidecar_closeout_contract.json"
LEDGER_JSON = SLICE_ROOT / "artifact/original_20_current_strict_sidecar_closeout_ledger.json"
LEDGER_MD = SLICE_ROOT / "artifact/original_20_current_strict_sidecar_closeout_ledger.md"
LEDGER_HTML = SLICE_ROOT / "artifact/original_20_current_strict_sidecar_closeout_ledger.html"
BUILDER = SLICE_ROOT / "artifact/build_original_20_current_strict_sidecar_closeout_ledger.py"
VERIFIER = SLICE_ROOT / "artifact/verify_original_20_current_strict_sidecar_closeout_ledger.py"
STRICT_STATUS_PACKAGE = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-16-p2-67-user-decision-strict-status-package-sandbox/artifact/strict_status_package.py"

REQUIRED_ROOT_FILES = [
    "slice-plan.md",
    "source-map.md",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]

FINAL_STATUSES = {
    "verification.md": "local_verification_passed",
    "reviewer-report.md": "review_pass_no_blocker",
    "boundary-audit.md": "pass_boundary",
    "product-acceptance-report.md": "pass_product_grade",
    "next-step.md": "pass_product_grade_pending_next_slice",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def add_failure(failures: list[str], condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def strict_package():
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_p2_73", STRICT_STATUS_PACKAGE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load strict status package")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def strict_status(path: Path) -> str | None:
    parsed = strict_package().parse_strict_frontmatter_status(path.read_text(encoding="utf-8"))
    return parsed.get("status") if parsed.get("valid") else None


def fixture_count() -> int:
    return len(list((SLICE_ROOT / "fixtures").glob("*.json")))


def failure_case_count() -> int:
    matrix = load_json(SLICE_ROOT / "failure-cases/original-20-sidecar-closeout-failures.json")
    return len(matrix.get("failure_cases", []))


def verify_required_files(failures: list[str]) -> None:
    for name in REQUIRED_ROOT_FILES:
        add_failure(failures, (SLICE_ROOT / name).is_file(), f"missing root file: {name}")
    for path in [CONTRACT_PATH, LEDGER_JSON, LEDGER_MD, LEDGER_HTML, BUILDER, VERIFIER]:
        add_failure(failures, path.is_file(), f"missing artifact: {path.name}")


def verify_contract_and_ledger(contract: dict, ledger: dict, failures: list[str]) -> dict:
    summary = ledger.get("summary", {})
    expected = contract.get("expected_summary", {})
    flags = ledger.get("authority_flags", {})
    contract_flags = contract.get("authority_flags", {})
    items = ledger.get("items", [])

    add_failure(failures, ledger.get("record_kind") == "sandbox_original_20_current_strict_sidecar_closeout_ledger", "wrong ledger record_kind")
    add_failure(failures, ledger.get("slice_id") == SLICE_ID, "wrong ledger slice_id")
    for key, value in expected.items():
        add_failure(failures, summary.get(key) == value, f"summary mismatch: {key}")
    for key, value in contract_flags.items():
        add_failure(failures, flags.get(key) == value, f"authority flag mismatch: {key}")

    add_failure(failures, isinstance(items, list) and len(items) == 20, "ledger item count is not 20")
    add_failure(failures, len({item.get("plan_key") for item in items}) == 20, "plan keys are not unique")
    add_failure(failures, len({item.get("old_slice_id") for item in items}) == 20, "old slice ids are not unique")

    required_final_gate_statuses = contract.get("required_final_gate_statuses", {})
    for item in items:
        label = item.get("plan_key", "unknown")
        source = item.get("source_evidence", {})
        add_failure(failures, item.get("sidecar_closeout_passed") is True, f"{label} sidecar closeout not passed")
        add_failure(failures, item.get("old_slice_current_strict_final_gate") is False, f"{label} incorrectly claims old strict final gate")
        add_failure(failures, item.get("old_slice_modified") is False, f"{label} old slice modified")
        add_failure(failures, item.get("old_slice_status_normalized") is False, f"{label} old slice status normalized")
        add_failure(failures, item.get("requires_explicit_user_approval_for_old_slice_edit") is True, f"{label} missing approval guard")
        add_failure(
            failures,
            item.get("required_final_gate_statuses_for_future_closeout") == required_final_gate_statuses,
            f"{label} required final-gate statuses drifted",
        )
        for evidence_key in [
            "verification_pass_evidence",
            "reviewer_pass_evidence",
            "boundary_pass_evidence",
            "product_acceptance_evidence",
            "core_reports_have_pass_evidence",
        ]:
            add_failure(failures, source.get(evidence_key) is True, f"{label} missing {evidence_key}")

    guard = ledger.get("decision_packet_guard", {})
    add_failure(failures, guard.get("approve_status_only_normalization_allowed_now") is False, "approval option incorrectly allowed now")
    add_failure(failures, guard.get("status_only_normalization_requires_separate_user_approval") is True, "missing separate approval requirement")
    add_failure(failures, guard.get("rerun_recloseout_without_old_slice_edits_allowed_now") is True, "recloseout-without-old-edits not allowed")

    return {
        "original_items_covered": summary.get("original_items_covered"),
        "sidecar_closeout_passed_count": summary.get("sidecar_closeout_passed_count"),
        "source_old_slice_current_strict_final_gate_count": summary.get("source_old_slice_current_strict_final_gate_count"),
        "old_slice_writes_applied": summary.get("old_slice_writes_applied"),
    }


def verify_fixtures(contract: dict, ledger: dict, failures: list[str]) -> None:
    required_ids = set(contract.get("required_fixture_ids", []))
    fixtures = [load_json(path) for path in (SLICE_ROOT / "fixtures").glob("*.json")]
    seen_ids = {fixture.get("fixture_id") for fixture in fixtures}
    add_failure(failures, seen_ids == required_ids, "fixture ids do not match contract")

    summary = ledger.get("summary", {})
    flags = ledger.get("authority_flags", {})
    artifact_state = {
        "has_machine_json": LEDGER_JSON.is_file(),
        "has_human_markdown": LEDGER_MD.is_file(),
        "has_portable_html": LEDGER_HTML.is_file(),
        "has_rebuild_script": BUILDER.is_file(),
        "has_verifier": VERIFIER.is_file(),
    }
    merged = {}
    merged.update(summary)
    merged.update(flags)
    merged.update(artifact_state)
    for fixture in fixtures:
        for key, value in fixture.get("expected", {}).items():
            add_failure(failures, merged.get(key) == value, f"fixture {fixture.get('fixture_id')} expected {key}={value}")


def verify_failure_cases(contract: dict, failures: list[str]) -> None:
    matrix = load_json(SLICE_ROOT / "failure-cases/original-20-sidecar-closeout-failures.json")
    expected = set(contract.get("required_failure_case_ids", []))
    actual = {case.get("case_id") for case in matrix.get("failure_cases", [])}
    add_failure(failures, actual == expected, "failure case ids do not match contract")


def verify_final_gate(failures: list[str]) -> None:
    for file_name, expected_status in FINAL_STATUSES.items():
        add_failure(failures, strict_status(SLICE_ROOT / file_name) == expected_status, f"{file_name} status not passed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--final-gate", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    verify_required_files(failures)
    contract = load_json(CONTRACT_PATH)
    ledger = load_json(LEDGER_JSON) if LEDGER_JSON.is_file() else {}
    summary = verify_contract_and_ledger(contract, ledger, failures) if ledger else {}
    verify_fixtures(contract, ledger, failures)
    verify_failure_cases(contract, failures)
    if args.final_gate:
        verify_final_gate(failures)

    result = {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "fixture_count": fixture_count(),
            "failure_case_count": failure_case_count(),
            **summary,
            "final_gate": bool(args.final_gate),
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
