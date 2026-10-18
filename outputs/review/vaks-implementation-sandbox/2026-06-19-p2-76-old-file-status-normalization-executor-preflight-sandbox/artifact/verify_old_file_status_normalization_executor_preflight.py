from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


SLICE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = SLICE_ROOT.parents[3]
SLICE_ID = SLICE_ROOT.name

CONTRACT = SLICE_ROOT / "artifact/old_file_status_normalization_executor_preflight_contract.json"
PREFLIGHT_JSON = SLICE_ROOT / "artifact/old_file_status_normalization_executor_preflight.json"
PREFLIGHT_MD = SLICE_ROOT / "artifact/old_file_status_normalization_executor_preflight.md"
PREFLIGHT_HTML = SLICE_ROOT / "artifact/old_file_status_normalization_executor_preflight.html"
BUILDER = SLICE_ROOT / "artifact/build_old_file_status_normalization_executor_preflight.py"
VERIFIER = SLICE_ROOT / "artifact/verify_old_file_status_normalization_executor_preflight.py"
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
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_p2_76", STRICT_STATUS_PACKAGE)
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
    for path in [CONTRACT, PREFLIGHT_JSON, PREFLIGHT_MD, PREFLIGHT_HTML, BUILDER, VERIFIER]:
        add_failure(failures, path.is_file(), f"missing artifact: {path.name}")


def verify_preflight(contract: dict, preflight: dict, failures: list[str]) -> dict:
    add_failure(failures, preflight.get("record_kind") == "sandbox_old_file_status_normalization_executor_preflight", "wrong record_kind")
    add_failure(failures, preflight.get("slice_id") == SLICE_ID, "wrong slice_id")
    summary = preflight.get("summary", {})
    for key, value in contract.get("expected_numbers", {}).items():
        add_failure(failures, summary.get(key) == value, f"summary mismatch: {key}")
    flags = preflight.get("authority_flags", {})
    for key, value in contract.get("authority_flags", {}).items():
        add_failure(failures, flags.get(key) == value, f"authority flag mismatch: {key}")
    gate = preflight.get("approval_gate", {})
    write_gate = contract.get("write_gate", {})
    add_failure(failures, gate.get("approval_present") is False, "approval is present")
    add_failure(failures, gate.get("executor_write_allowed") is False, "executor write allowed")
    add_failure(failures, gate.get("p2_75_packet_is_not_approval") == write_gate.get("p2_75_packet_is_not_approval"), "p2-75 approval boundary mismatch")
    add_failure(failures, gate.get("generic_language_is_not_approval") == write_gate.get("generic_language_is_not_approval"), "generic language boundary mismatch")

    allowed = preflight.get("allowed_future_edit", {})
    for key, value in contract.get("allowed_future_edit", {}).items():
        add_failure(failures, allowed.get(key) == value, f"allowed future edit mismatch: {key}")

    changes = preflight.get("preflight_changes", [])
    rollback = preflight.get("rollback_manifest", [])
    add_failure(failures, len(changes) == 75, "preflight change count not 75")
    add_failure(failures, len(rollback) == 75, "rollback count not 75")
    add_failure(failures, len({item.get("target_path") for item in changes}) == 75, "target paths are not unique")
    add_failure(failures, len({item.get("old_slice_id") for item in changes}) == 20, "old slice count not 20")
    for item in changes:
        label = item.get("change_index", "unknown")
        add_failure(failures, item.get("field") == "frontmatter.status", f"{label} field not frontmatter.status")
        add_failure(failures, item.get("change_kind") == "status_only_frontmatter_normalization", f"{label} wrong change kind")
        add_failure(failures, item.get("target_exists") is True, f"{label} target missing")
        add_failure(failures, item.get("frontmatter_valid") is True, f"{label} frontmatter invalid")
        add_failure(failures, item.get("current_status_matches_manifest") is True, f"{label} current status mismatch")
        add_failure(failures, item.get("rollback_status") == item.get("manifest_current_status"), f"{label} rollback status mismatch")
        add_failure(failures, item.get("body_edit_planned") is False, f"{label} body edit planned")
        add_failure(failures, item.get("artifact_edit_planned") is False, f"{label} artifact edit planned")
        add_failure(failures, item.get("write_applied") is False, f"{label} write applied")
        add_failure(failures, item.get("rollback_applied") is False, f"{label} rollback applied")

    md = PREFLIGHT_MD.read_text(encoding="utf-8") if PREFLIGHT_MD.is_file() else ""
    add_failure(failures, "approval present: `false`" in md, "Markdown missing approval false")
    add_failure(failures, "executor write allowed: `false`" in md, "Markdown missing executor write false")
    add_failure(failures, "No old slice writes are applied" in md, "Markdown missing old write boundary")
    return {
        "target_change_count": summary.get("target_change_count"),
        "target_file_count": summary.get("target_file_count"),
        "target_old_slice_count": summary.get("target_old_slice_count"),
        "missing_target_count": summary.get("missing_target_count"),
        "current_status_mismatch_count": summary.get("current_status_mismatch_count"),
        "rollback_entry_count": summary.get("rollback_entry_count"),
        "old_slice_writes_applied": summary.get("old_slice_writes_applied"),
    }


def verify_fixtures(contract: dict, preflight: dict, failures: list[str]) -> None:
    fixtures = [load_json(path) for path in (SLICE_ROOT / "fixtures").glob("*.json")]
    seen = {fixture.get("fixture_id") for fixture in fixtures}
    add_failure(failures, seen == set(contract.get("required_fixture_ids", [])), "fixture ids do not match contract")
    summary = preflight.get("summary", {})
    flags = preflight.get("authority_flags", {})
    gate = preflight.get("approval_gate", {})
    merged = {}
    merged.update(summary)
    merged.update(flags)
    merged.update(gate)
    merged.update(contract.get("write_gate", {}))
    for fixture in fixtures:
        for key, value in fixture.get("expected", {}).items():
            add_failure(failures, merged.get(key) == value, f"{fixture.get('fixture_id')} expected {key}")


def verify_failure_cases(contract: dict, failures: list[str]) -> None:
    matrix = load_json(SLICE_ROOT / "failure-cases/old-file-status-normalization-executor-preflight-failures.json")
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
    preflight = load_json(PREFLIGHT_JSON) if PREFLIGHT_JSON.is_file() else {}
    summary = verify_preflight(contract, preflight, failures) if preflight else {}
    verify_fixtures(contract, preflight, failures)
    verify_failure_cases(contract, failures)
    if args.final_gate:
        verify_final_gate(failures)

    result = {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "fixture_count": len(list((SLICE_ROOT / "fixtures").glob("*.json"))),
            "failure_case_count": len(load_json(SLICE_ROOT / "failure-cases/old-file-status-normalization-executor-preflight-failures.json").get("failure_cases", [])),
            **summary,
            "final_gate": bool(args.final_gate),
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
