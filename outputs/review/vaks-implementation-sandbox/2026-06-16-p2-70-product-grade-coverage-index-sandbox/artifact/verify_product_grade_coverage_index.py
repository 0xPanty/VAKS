from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True


SLICE_ID = "2026-06-16-p2-70-product-grade-coverage-index-sandbox"
STRICT_PACKAGE_SLICE_ID = "2026-06-16-p2-67-user-decision-strict-status-package-sandbox"

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"
OUTPUT_JSON = ARTIFACT / "product_grade_coverage_index.json"

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
    "product_grade_coverage_contract.json",
    "build_product_grade_coverage_index.py",
    "verify_product_grade_coverage_index.py",
    "product_grade_coverage_index.json",
    "product_grade_coverage_index.md",
    "product_grade_coverage_index.html",
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
    path = ARTIFACT / "build_product_grade_coverage_index.py"
    spec = importlib.util.spec_from_file_location("p2_70_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load p2-70 builder")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_package():
    builder = import_builder()
    return builder.load_package()


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
    add_failure(failures, contract.get("record_kind") == "sandbox_product_grade_coverage_contract", "wrong contract record_kind")
    add_failure(failures, contract.get("slice_id") == SLICE_ID, "wrong contract slice_id")
    input_contract = contract.get("input_contract", {})
    output_contract = contract.get("output_contract", {})
    add_failure(failures, input_contract.get("status_source") == "strict_yaml_frontmatter_only", "wrong status source")
    add_failure(failures, input_contract.get("ignore_body_literals") is True, "body literals not ignored")
    add_failure(failures, input_contract.get("ignore_code_literals") is True, "code literals not ignored")
    add_failure(failures, STRICT_PACKAGE_SLICE_ID == input_contract.get("status_parser_source_slice"), "wrong status parser source")
    add_failure(failures, output_contract.get("canonical_pass_requires_product_status") == "pass_product_grade", "wrong product status rule")
    add_failure(failures, output_contract.get("canonical_pass_requires_next_step_status") == "pass_product_grade_pending_next_slice", "wrong next-step rule")
    for flag in [
        "coverage_index_is_not_mainline_readiness",
        "coverage_index_is_not_promotion_approval",
        "coverage_index_is_not_reviewed_knowledge",
        "coverage_index_is_not_action_basis",
    ]:
        add_failure(failures, output_contract.get(flag) is True, f"{flag} not true")
    for flag in ["dependency_install_required", "network_required", "mcp_required", "background_service_required"]:
        add_failure(failures, output_contract.get(flag) is False, f"{flag} not false")


def validate_payload(payload: dict, current: dict, failures: list[str], label: str) -> None:
    add_failure(failures, payload.get("record_kind") == "sandbox_product_grade_coverage_index", f"{label} wrong record_kind")
    add_failure(failures, payload.get("slice_id") == SLICE_ID, f"{label} wrong slice_id")
    add_failure(failures, payload == current, f"{label} does not match current builder output")
    parser = payload.get("parser_contract", {})
    add_failure(failures, parser.get("status_source") == "strict_yaml_frontmatter_only", f"{label} wrong parser source")
    add_failure(failures, parser.get("ignore_body_literals") is True, f"{label} body literals not ignored")
    add_failure(failures, parser.get("ignore_code_literals") is True, f"{label} code literals not ignored")
    rules = payload.get("rules", {})
    add_failure(failures, rules.get("pending_product_counts_as_pass") is False, f"{label} pending product counts as pass")
    add_failure(failures, rules.get("legacy_variants_count_as_canonical") is False, f"{label} legacy variants count as canonical")
    add_failure(failures, rules.get("next_step_required_for_canonical") is True, f"{label} next-step not required")
    add_failure(failures, rules.get("reviewer_required_for_canonical") is True, f"{label} reviewer not required")
    add_failure(failures, rules.get("boundary_required_for_canonical") is True, f"{label} boundary not required")
    flags = payload.get("authority_flags", {})
    for flag in ["mainline_ready", "promotion_ready", "reviewed_knowledge_ready", "evidence_support_ready", "action_basis_ready", "user_approval_collected"]:
        add_failure(failures, flags.get(flag) is False, f"{label} {flag} not false")
    summary = payload.get("summary", {})
    add_failure(failures, summary.get("planned_items_total") == 20, f"{label} wrong planned item total")
    add_failure(failures, summary.get("planned_items_found") == 20, f"{label} original planned items not all found")
    add_failure(failures, summary.get("literal_pass_token_count_not_counted", 0) >= 1, f"{label} no literal-hit evidence")
    add_failure(failures, summary.get("literal_hit_files_sampled", 0) >= 1, f"{label} no literal-hit sample evidence")
    planned = payload.get("planned_items", [])
    add_failure(failures, isinstance(planned, list) and len(planned) == 20, f"{label} planned list not 20")
    add_failure(failures, any(item.get("legacy_pass_variant") for item in planned), f"{label} no legacy pass variant surfaced")
    add_failure(failures, any(item.get("pending_next_step_closeout") for item in planned), f"{label} no pending next-step surfaced")


def validate_fixtures(fixtures: list[Path], failures: list[str]) -> int:
    package = load_package()
    seen = set()
    for path in fixtures:
        data = load_json(path)
        fixture_id = data.get("fixture_id") if isinstance(data, dict) else None
        seen.add(fixture_id)
        if fixture_id == "canonical-pass-statuses":
            statuses = data["reports"]
            expected = data["expected"]["canonical_strict_pass"]
            observed = all(
                package.parse_strict_frontmatter_status(text).get("status") == wanted
                for text, wanted in [
                    (statuses["verification"], "local_verification_passed"),
                    (statuses["reviewer"], "review_pass_no_blocker"),
                    (statuses["boundary"], "pass_boundary"),
                    (statuses["product"], "pass_product_grade"),
                    (statuses["next_step"], "pass_product_grade_pending_next_slice"),
                ]
            )
            add_failure(failures, observed is expected, "canonical fixture mismatch")
        elif fixture_id == "legacy-pass-variant":
            product_status = package.parse_strict_frontmatter_status(data["reports"]["product"]).get("status")
            next_status = package.parse_strict_frontmatter_status(data["reports"]["next_step"]).get("status")
            add_failure(failures, product_status == "pass_product_grade_round_2", "legacy fixture product status mismatch")
            add_failure(failures, next_status == "pending_acceptance", "legacy fixture next status mismatch")
            add_failure(failures, data["expected"]["legacy_pass_variant"] is True, "legacy fixture expected mismatch")
        elif fixture_id == "body-literal-not-status":
            status = package.parse_strict_frontmatter_status(data["document"]).get("status")
            add_failure(failures, status == data["expected"]["strict_status"], "body literal fixture strict status mismatch")
        elif fixture_id == "code-literal-not-status":
            parsed = package.parse_strict_frontmatter_status(data["document"])
            add_failure(failures, parsed.get("valid") is False, "code literal fixture should not have valid frontmatter")
            add_failure(failures, data["expected"]["strict_status"] is None, "code literal fixture expected mismatch")
        else:
            failures.append(f"unknown fixture: {fixture_id}")
    for required in ["canonical-pass-statuses", "legacy-pass-variant", "body-literal-not-status", "code-literal-not-status"]:
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
    for token in ["body_literal", "code_literal", "pending_product", "legacy_variant", "next_step", "reviewer", "boundary", "mainline"]:
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
    contract_path = ARTIFACT / "product_grade_coverage_contract.json"
    contract = load_json(contract_path) if contract_path.exists() else {}
    if isinstance(contract, dict):
        validate_contract(contract, failures)
    else:
        failures.append("contract is not object")
    payload = load_json(OUTPUT_JSON) if OUTPUT_JSON.exists() else {}
    builder = import_builder()
    current = builder.build_index()
    if isinstance(payload, dict):
        validate_payload(payload, current, failures, "payload")
    else:
        failures.append("payload is not object")
        payload = {}
    fixture_count = validate_fixtures(fixtures, failures)
    failure_case_count = validate_failure_cases(failure_files, payload, current, failures)
    if final_gate:
        validate_final_reports(failures)
    return {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "fixture_count": fixture_count,
            "failure_case_count": failure_case_count,
            "planned_items_found": payload.get("summary", {}).get("planned_items_found"),
            "planned_items_total": payload.get("summary", {}).get("planned_items_total"),
            "all_planned_items_current_strict_pass": payload.get("summary", {}).get("all_planned_items_current_strict_pass"),
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
