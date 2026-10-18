from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True


SLICE_ID = "2026-06-19-p2-72-original-slice-normalization-decision-packet-sandbox"
SOURCE_AUDIT_SLICE_ID = "2026-06-16-p2-71-original-slice-closeout-normalization-audit-sandbox"
STRICT_PACKAGE_SLICE_ID = "2026-06-16-p2-67-user-decision-strict-status-package-sandbox"

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"
OUTPUT_JSON = ARTIFACT / "original_slice_normalization_decision_packet.json"
PACKAGE_PATH = (
    WORKSPACE
    / "outputs"
    / "review"
    / "vaks-implementation-sandbox"
    / STRICT_PACKAGE_SLICE_ID
    / "artifact"
    / "strict_status_package.py"
)

REQUIRED_ROOT = [
    "slice-plan.md",
    "source-map.md",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]

REQUIRED_ARTIFACT = [
    "original_slice_normalization_decision_contract.json",
    "build_original_slice_normalization_decision_packet.py",
    "verify_original_slice_normalization_decision_packet.py",
    "original_slice_normalization_decision_packet.json",
    "original_slice_normalization_decision_packet.md",
    "original_slice_normalization_decision_packet.html",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def add_failure(failures: list[str], condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def import_builder():
    path = ARTIFACT / "build_original_slice_normalization_decision_packet.py"
    spec = importlib.util.spec_from_file_location("p2_72_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load p2-72 builder")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_package():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_p2_72", PACKAGE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load strict status package")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def strict_status(text: str) -> str | None:
    package = load_package()
    parsed = package.parse_strict_frontmatter_status(text)
    return parsed.get("status") if parsed.get("valid") else None


def validate_files(failures: list[str]) -> tuple[list[Path], list[Path]]:
    for filename in REQUIRED_ROOT:
        add_failure(failures, (ROOT / filename).exists(), f"missing root file: {filename}")
    for filename in REQUIRED_ARTIFACT:
        add_failure(failures, (ARTIFACT / filename).exists(), f"missing artifact file: {filename}")
    fixtures = sorted(FIXTURES.glob("*.json"))
    failure_files = sorted(FAILURE_CASES.glob("*.json"))
    add_failure(failures, len(fixtures) >= 4, "expected at least 4 fixtures")
    add_failure(failures, len(failure_files) >= 1, "expected failure case file")
    return fixtures, failure_files


def validate_contract(contract: dict, failures: list[str]) -> None:
    add_failure(failures, contract.get("record_kind") == "sandbox_original_slice_normalization_decision_contract", "wrong contract record_kind")
    add_failure(failures, contract.get("slice_id") == SLICE_ID, "wrong contract slice_id")
    input_contract = contract.get("input_contract", {})
    output_contract = contract.get("output_contract", {})
    add_failure(failures, input_contract.get("source_audit_slice_id") == SOURCE_AUDIT_SLICE_ID, "wrong source audit slice")
    add_failure(failures, input_contract.get("required_original_item_count") == 20, "wrong original item count")
    add_failure(failures, input_contract.get("required_candidate_count") == 20, "wrong candidate count")
    for flag in ["decision_packet_only"]:
        add_failure(failures, output_contract.get(flag) is True, f"{flag} not true")
    for flag in [
        "normalization_applied",
        "old_slice_write_allowed",
        "user_approval_collected",
        "mainline_ready",
        "promotion_ready",
        "reviewed_knowledge_ready",
        "evidence_support_ready",
        "action_basis_ready",
        "dependency_install_required",
        "network_required",
        "mcp_required",
        "background_service_required",
    ]:
        add_failure(failures, output_contract.get(flag) is False, f"{flag} not false")


def validate_payload(payload: dict, current: dict, failures: list[str], label: str) -> None:
    add_failure(failures, payload.get("record_kind") == "sandbox_original_slice_normalization_decision_packet", f"{label} wrong record_kind")
    add_failure(failures, payload.get("slice_id") == SLICE_ID, f"{label} wrong slice_id")
    add_failure(failures, payload == current, f"{label} does not match current builder output")
    source = payload.get("source_audit", {})
    add_failure(failures, source.get("source_audit_slice_id") == SOURCE_AUDIT_SLICE_ID, f"{label} wrong source audit")
    summary = payload.get("summary", {})
    add_failure(failures, summary.get("original_items_covered") == 20, f"{label} original items not 20")
    add_failure(failures, summary.get("product_acceptance_evidence_count") == 20, f"{label} product evidence not 20")
    add_failure(failures, summary.get("core_pass_evidence_count") == 20, f"{label} core evidence not 20")
    add_failure(failures, summary.get("current_strict_final_gate_count") == 0, f"{label} strict final-gate not 0")
    add_failure(failures, summary.get("status_normalization_candidate_count") == 20, f"{label} candidates not 20")
    add_failure(failures, summary.get("dry_run_status_change_count", 0) >= 20, f"{label} dry-run changes too low")
    add_failure(failures, summary.get("old_slice_writes_applied") == 0, f"{label} old slice writes applied")
    options = {option.get("option_id"): option for option in payload.get("decision_options", [])}
    approve = options.get("approve_status_only_normalization", {})
    add_failure(failures, approve.get("allowed_now") is False, f"{label} approval option allowed now")
    add_failure(failures, approve.get("requires_separate_user_approval") is True, f"{label} approval option lacks separate approval")
    leave = options.get("leave_audit_only", {})
    rerun = options.get("rerun_recloseout_without_old_slice_edits", {})
    add_failure(failures, leave.get("allowed_now") is True, f"{label} leave option not allowed")
    add_failure(failures, rerun.get("allowed_now") is True, f"{label} rerun option not allowed")
    manifest = payload.get("dry_run_manifest", {})
    changes = manifest.get("status_changes", [])
    add_failure(failures, manifest.get("applied") is False, f"{label} manifest applied")
    add_failure(failures, manifest.get("requires_explicit_user_approval") is True, f"{label} manifest approval flag missing")
    add_failure(failures, isinstance(changes, list) and len(changes) == summary.get("dry_run_status_change_count"), f"{label} dry-run change count mismatch")
    add_failure(failures, all(change.get("applied") is False for change in changes), f"{label} contains applied dry-run change")
    add_failure(failures, all(change.get("requires_explicit_user_approval") is True for change in changes), f"{label} change lacks approval requirement")
    flags = payload.get("authority_flags", {})
    for flag in [
        "decision_packet_only",
        "dry_run_only",
    ]:
        add_failure(failures, flags.get(flag) is True, f"{label} {flag} not true")
    for flag in [
        "old_slice_write_allowed",
        "normalization_applied",
        "mainline_ready",
        "promotion_ready",
        "reviewed_knowledge_ready",
        "evidence_support_ready",
        "action_basis_ready",
        "user_approval_collected",
    ]:
        add_failure(failures, flags.get(flag) is False, f"{label} {flag} not false")


def validate_fixtures(fixtures: list[Path], payload: dict, failures: list[str]) -> int:
    options = {option.get("option_id"): option for option in payload.get("decision_options", [])}
    seen = set()
    for path in fixtures:
        data = load_json(path)
        fixture_id = data.get("fixture_id") if isinstance(data, dict) else None
        seen.add(fixture_id)
        if fixture_id in {"approve-status-only-normalization", "leave-audit-only", "rerun-recloseout-option"}:
            option = options.get(data["decision_option"], {})
            for key, expected in data["expected"].items():
                add_failure(failures, option.get(key) is expected, f"{fixture_id} {key} mismatch")
        elif fixture_id == "forbid-implicit-approval":
            approve = options.get(data["decision_option"], {})
            add_failure(failures, approve.get("allowed_now") is data["expected"]["allowed_now"], "implicit approval allowed now mismatch")
            add_failure(
                failures,
                data["expected"]["counts_as_explicit_old_slice_edit_approval"] is False,
                "implicit approval fixture expected mismatch",
            )
        else:
            failures.append(f"unknown fixture: {fixture_id}")
    for required in [
        "approve-status-only-normalization",
        "leave-audit-only",
        "rerun-recloseout-option",
        "forbid-implicit-approval",
    ]:
        add_failure(failures, required in seen, f"missing fixture {required}")
    return len(fixtures)


def apply_mutation(payload: dict, mutation: dict) -> dict:
    mutated = json.loads(json.dumps(payload, ensure_ascii=False))
    cursor = mutated
    path = mutation["set_path"]["path"]
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = mutation["set_path"]["value"]
    return mutated


def validate_failure_cases(files: list[Path], payload: dict, current: dict, failures: list[str]) -> int:
    cases: list[dict] = []
    for path in files:
        data = load_json(path)
        if isinstance(data, list):
            cases.extend(item for item in data if isinstance(item, dict))
        elif isinstance(data, dict):
            cases.append(data)
    add_failure(failures, len(cases) >= 8, "expected at least 8 failure cases")
    ids = [case.get("failure_id") for case in cases]
    add_failure(failures, len(ids) == len(set(ids)), "failure ids not unique")
    joined = "\n".join(str(case) for case in cases)
    for token in ["user_approval", "normalization_applied", "old_slice_write", "mainline", "action_basis", "item_count", "dry_run", "approval_option"]:
        add_failure(failures, token in joined, f"failure cases do not cover {token}")
    for case in cases:
        mutation = case.get("mutation")
        add_failure(failures, isinstance(mutation, dict), f"{case.get('failure_id')} missing mutation")
        if isinstance(mutation, dict):
            mutated = apply_mutation(payload, mutation)
            local_failures: list[str] = []
            validate_payload(mutated, current, local_failures, "mutated")
            add_failure(failures, bool(local_failures), f"{case.get('failure_id')} mutation was not rejected")
    return len(cases)


def final_status(path: Path) -> str | None:
    return strict_status(read_text(path))


def validate_final_reports(failures: list[str]) -> None:
    add_failure(failures, final_status(ROOT / "verification.md") == "local_verification_passed", "verification status not passed")
    add_failure(failures, final_status(ROOT / "reviewer-report.md") == "review_pass_no_blocker", "Reviewer report status not passed")
    add_failure(failures, final_status(ROOT / "boundary-audit.md") == "pass_boundary", "Boundary audit status not passed")
    add_failure(failures, final_status(ROOT / "product-acceptance-report.md") == "pass_product_grade", "Product report status not passed")
    add_failure(failures, final_status(ROOT / "next-step.md") == "pass_product_grade_pending_next_slice", "next-step status not passed")


def verify(final_gate: bool = False) -> dict:
    failures: list[str] = []
    fixtures, failure_files = validate_files(failures)
    contract = load_json(ARTIFACT / "original_slice_normalization_decision_contract.json")
    if isinstance(contract, dict):
        validate_contract(contract, failures)
    else:
        failures.append("contract is not object")
    payload = load_json(OUTPUT_JSON) if OUTPUT_JSON.exists() else {}
    builder = import_builder()
    current = builder.build_packet()
    if isinstance(payload, dict):
        validate_payload(payload, current, failures, "payload")
    else:
        failures.append("payload is not object")
        payload = {}
    fixture_count = validate_fixtures(fixtures, payload, failures)
    failure_case_count = validate_failure_cases(failure_files, payload, current, failures)
    if final_gate:
        validate_final_reports(failures)
    summary = payload.get("summary", {}) if isinstance(payload, dict) else {}
    return {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "fixture_count": fixture_count,
            "failure_case_count": failure_case_count,
            "original_items_covered": summary.get("original_items_covered"),
            "dry_run_status_change_count": summary.get("dry_run_status_change_count"),
            "old_slice_writes_applied": summary.get("old_slice_writes_applied"),
            "final_gate": final_gate,
        },
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--final-gate", action="store_true")
    args = parser.parse_args()
    result = verify(final_gate=args.final_gate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
