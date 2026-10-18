from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True


SLICE_ID = "2026-06-16-p2-71-original-slice-closeout-normalization-audit-sandbox"
SOURCE_INDEX_SLICE_ID = "2026-06-16-p2-70-product-grade-coverage-index-sandbox"
STRICT_PACKAGE_SLICE_ID = "2026-06-16-p2-67-user-decision-strict-status-package-sandbox"

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"
OUTPUT_JSON = ARTIFACT / "original_slice_closeout_normalization_audit.json"
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
    "original_slice_closeout_normalization_contract.json",
    "build_original_slice_closeout_normalization_audit.py",
    "verify_original_slice_closeout_normalization_audit.py",
    "original_slice_closeout_normalization_audit.json",
    "original_slice_closeout_normalization_audit.md",
    "original_slice_closeout_normalization_audit.html",
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
    path = ARTIFACT / "build_original_slice_closeout_normalization_audit.py"
    spec = importlib.util.spec_from_file_location("p2_71_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load p2-71 builder")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_package():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_p2_71", PACKAGE_PATH)
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
    add_failure(failures, contract.get("record_kind") == "sandbox_original_slice_closeout_normalization_contract", "wrong contract record_kind")
    add_failure(failures, contract.get("slice_id") == SLICE_ID, "wrong contract slice_id")
    input_contract = contract.get("input_contract", {})
    output_contract = contract.get("output_contract", {})
    add_failure(failures, input_contract.get("source_index_slice_id") == SOURCE_INDEX_SLICE_ID, "wrong source index slice")
    add_failure(failures, input_contract.get("original_plan_item_count") == 20, "wrong original plan item count")
    add_failure(failures, input_contract.get("old_slice_reads_only") is True, "old slices not read-only")
    for flag in ["normalization_applied", "old_slice_edit_allowed"]:
        add_failure(failures, output_contract.get(flag) is False, f"{flag} not false")
    for flag in [
        "user_approval_required_for_old_slice_edits",
        "audit_is_not_mainline_readiness",
        "audit_is_not_promotion_approval",
        "audit_is_not_reviewed_knowledge",
        "audit_is_not_evidence_support",
        "audit_is_not_action_basis",
    ]:
        add_failure(failures, output_contract.get(flag) is True, f"{flag} not true")
    for flag in ["dependency_install_required", "network_required", "mcp_required", "background_service_required"]:
        add_failure(failures, output_contract.get(flag) is False, f"{flag} not false")


def validate_payload(payload: dict, current: dict, failures: list[str], label: str) -> None:
    add_failure(failures, payload.get("record_kind") == "sandbox_original_slice_closeout_normalization_audit", f"{label} wrong record_kind")
    add_failure(failures, payload.get("slice_id") == SLICE_ID, f"{label} wrong slice_id")
    add_failure(failures, payload == current, f"{label} does not match current builder output")
    source = payload.get("source_index", {})
    add_failure(failures, source.get("source_index_slice_id") == SOURCE_INDEX_SLICE_ID, f"{label} wrong source index")
    rules = payload.get("rules", {})
    for flag in [
        "product_evidence_counts_as_current_strict_gate",
        "legacy_product_status_counts_as_current_strict_gate",
        "pending_next_step_counts_as_current_strict_gate",
    ]:
        add_failure(failures, rules.get(flag) is False, f"{label} {flag} not false")
    add_failure(failures, rules.get("old_slice_edit_requires_separate_user_approval") is True, f"{label} old-slice approval rule not true")
    flags = payload.get("authority_flags", {})
    for flag in [
        "old_slice_edit_allowed",
        "normalization_applied",
        "mainline_ready",
        "promotion_ready",
        "reviewed_knowledge_ready",
        "evidence_support_ready",
        "action_basis_ready",
        "user_approval_collected",
    ]:
        add_failure(failures, flags.get(flag) is False, f"{label} authority {flag} not false")
    summary = payload.get("summary", {})
    add_failure(failures, summary.get("total_original_items") == 20, f"{label} total original items not 20")
    add_failure(failures, summary.get("product_acceptance_evidence_count") == 20, f"{label} product evidence count not 20")
    add_failure(failures, summary.get("core_reports_have_pass_evidence_count") == 20, f"{label} core pass evidence count not 20")
    add_failure(failures, summary.get("core_reports_current_canonical_count") == 0, f"{label} core canonical count not 0")
    add_failure(failures, summary.get("current_strict_final_gate_count") == 0, f"{label} strict gate count not 0")
    add_failure(failures, summary.get("status_normalization_candidate_count") == 20, f"{label} normalization candidate count not 20")
    add_failure(failures, summary.get("requires_re_review_or_reacceptance_count") == 0, f"{label} re-review count not 0")
    add_failure(failures, summary.get("audit_only_no_old_slice_writes") is True, f"{label} audit-only flag not true")
    items = payload.get("items", [])
    add_failure(failures, isinstance(items, list) and len(items) == 20, f"{label} items not 20")
    for index, item in enumerate(items):
        add_failure(failures, item.get("current_strict_final_gate") is False, f"{label} item {index} unexpectedly strict pass")
        add_failure(failures, item.get("product_acceptance_evidence") is True, f"{label} item {index} lacks product evidence")
        add_failure(
            failures,
            item.get("recommendation") == "user_approved_status_normalization_candidate",
            f"{label} item {index} wrong recommendation",
        )
        add_failure(failures, item.get("old_slice_edit_allowed") is False, f"{label} item {index} old edit allowed")
        add_failure(failures, item.get("normalization_applied") is False, f"{label} item {index} normalization applied")


def validate_fixtures(fixtures: list[Path], failures: list[str]) -> int:
    builder = import_builder()
    seen = set()
    for path in fixtures:
        data = load_json(path)
        fixture_id = data.get("fixture_id") if isinstance(data, dict) else None
        seen.add(fixture_id)
        if fixture_id in {
            "current-strict-pass-no-action",
            "legacy-status-normalization-candidate",
            "missing-product-acceptance-rereview",
        }:
            observed = builder.classify_statuses(data["statuses"])
            for key, expected in data["expected"].items():
                if key == "recommendation":
                    add_failure(failures, observed.get("recommendation") == expected, f"{fixture_id} recommendation mismatch")
                else:
                    add_failure(failures, observed.get(key) is expected, f"{fixture_id} {key} mismatch")
        elif fixture_id == "old-slice-edit-forbidden":
            action = data["candidate_action"]
            allowed = action.get("old_slice_edit_allowed") is True and action.get("user_approval_present") is True
            add_failure(failures, allowed is data["expected"]["allowed"], "old-slice edit fixture mismatch")
        else:
            failures.append(f"unknown fixture: {fixture_id}")
    for required in [
        "current-strict-pass-no-action",
        "legacy-status-normalization-candidate",
        "missing-product-acceptance-rereview",
        "old-slice-edit-forbidden",
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
    for token in ["all_strict_pass", "product_evidence", "old_slice_edit", "normalization_applied", "mainline", "user_approval", "source_index", "no_action"]:
        add_failure(failures, token in joined, f"failure cases do not cover {token}")
    builder = import_builder()
    local_fail_statuses = {
        "verification": "not_pass",
        "reviewer": "not_pass",
        "boundary": "not_pass",
        "product": "pass_product_grade",
        "next_step": "pending_product_acceptance",
    }
    local_fail_classification = builder.classify_statuses(local_fail_statuses)
    add_failure(
        failures,
        local_fail_classification.get("core_reports_have_pass_evidence") is False,
        "legacy pass detector accepts not_pass status",
    )
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
    contract = load_json(ARTIFACT / "original_slice_closeout_normalization_contract.json")
    if isinstance(contract, dict):
        validate_contract(contract, failures)
    else:
        failures.append("contract is not object")
    payload = load_json(OUTPUT_JSON) if OUTPUT_JSON.exists() else {}
    builder = import_builder()
    current = builder.build_audit()
    if isinstance(payload, dict):
        validate_payload(payload, current, failures, "payload")
    else:
        failures.append("payload is not object")
        payload = {}
    fixture_count = validate_fixtures(fixtures, failures)
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
            "total_original_items": summary.get("total_original_items"),
            "product_acceptance_evidence_count": summary.get("product_acceptance_evidence_count"),
            "current_strict_final_gate_count": summary.get("current_strict_final_gate_count"),
            "status_normalization_candidate_count": summary.get("status_normalization_candidate_count"),
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
