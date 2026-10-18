from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-59-user-decision-operator-handoff-index-sandbox"
ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"

SOURCE_SLICE_IDS = [
    "2026-06-16-p2-51-user-decision-request-packet-sandbox",
    "2026-06-16-p2-52-user-decision-no-auto-advance-guard-sandbox",
    "2026-06-16-p2-53-user-response-classifier-dry-run-sandbox",
    "2026-06-16-p2-54-safe-user-response-renderer-dry-run-sandbox",
    "2026-06-16-p2-55-user-decision-e2e-dry-run-simulator-sandbox",
    "2026-06-16-p2-56-user-decision-demo-transcript-smoke-runner-sandbox",
    "2026-06-16-p2-57-user-decision-chain-regression-bundle-sandbox",
    "2026-06-16-p2-58-user-decision-static-boundary-scan-regression-sandbox",
]

MUST_NOT_REQUIRED = {
    "execute_option",
    "merge_mainline",
    "promote",
    "sync_obsidian",
    "commit",
    "push",
    "install_dependencies",
    "start_background_service",
    "install_hooks",
    "use_mcp_write_tool",
    "write_reviewed_knowledge",
    "create_evidence_support",
    "create_action_basis",
    "start_future_slice_by_inference",
}

DANGEROUS_PHRASES = [
    "mainline approved",
    "promotion approved",
    "execution approved",
    "sync approved",
    "reviewed knowledge created",
    "evidence support created",
    "action basis created",
    "可以合并",
    "已合并",
    "执行授权",
]

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
    "run_user_decision_operator_handoff_index.py",
    "build_user_decision_operator_handoff_index.py",
    "verify_user_decision_operator_handoff_index.py",
    "user_decision_operator_handoff_index_contract.json",
    "user_decision_operator_handoff_index_readout.md",
    "user_decision_operator_handoff_index_prototype.html",
]


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def add_failure(failures: list[str], condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def import_runner():
    path = ARTIFACT / "run_user_decision_operator_handoff_index.py"
    spec = importlib.util.spec_from_file_location("p2_59_runner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load p2-59 runner")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def frontmatter_status(path: Path) -> str:
    for line in read_text(path).splitlines():
        if line.lower().startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def validate_files(failures: list[str]) -> tuple[list[Path], list[Path]]:
    for filename in REQUIRED_ROOT:
        add_failure(failures, (ROOT / filename).exists(), f"missing root file: {filename}")
    for filename in REQUIRED_ARTIFACT:
        add_failure(failures, (ARTIFACT / filename).exists(), f"missing artifact file: {filename}")
    fixtures = sorted(FIXTURES.glob("*.json"))
    failure_cases = sorted(FAILURE_CASES.glob("*.json"))
    add_failure(failures, len(fixtures) >= 9, "expected at least 9 fixtures")
    add_failure(failures, len(failure_cases) >= 1, "expected failure cases")
    return fixtures, failure_cases


def validate_contract(contract: dict, failures: list[str]) -> None:
    add_failure(failures, contract.get("record_kind") == "sandbox_user_decision_operator_handoff_index_contract", "wrong record_kind")
    add_failure(failures, contract.get("slice_id") == SLICE_ID, "wrong slice_id")
    source_ids = [item.get("slice_id") for item in contract.get("source_slices", [])]
    add_failure(failures, source_ids == SOURCE_SLICE_IDS, "wrong source_slices")
    add_failure(failures, contract.get("expected_entry_count") == len(SOURCE_SLICE_IDS), "wrong expected_entry_count")
    add_failure(
        failures,
        contract.get("truth_boundary") == "operator_handoff_index_not_user_decision_or_execution_authority",
        "wrong truth boundary",
    )
    latest = contract.get("latest_source_final_gate_command", "")
    add_failure(failures, SOURCE_SLICE_IDS[-1] in latest and "--final-gate" in latest, "latest source gate incomplete")
    output = contract.get("output_contract", {})
    for flag in ["automatic_execution", "mainline_ready", "promotion_ready", "action_basis_ready"]:
        add_failure(failures, output.get(flag) is False, f"contract {flag} not false")
    add_failure(failures, MUST_NOT_REQUIRED <= set(output.get("must_not", [])), "contract must_not incomplete")
    non_claims = "\n".join(contract.get("required_non_claims", []))
    for phrase in ["not a user decision", "not execution authority", "not mainline approval", "not action basis"]:
        add_failure(failures, phrase in non_claims, f"missing non-claim {phrase}")


def dangerous_markdown(index: dict) -> bool:
    markdown = str(index.get("handoff_markdown", ""))
    return any(phrase in markdown for phrase in DANGEROUS_PHRASES)


def recompute_source_chain_ready(index: dict) -> bool:
    entries = index.get("entries", [])
    return (
        isinstance(entries, list)
        and len(entries) == len(SOURCE_SLICE_IDS)
        and index.get("source_slice_ids") == SOURCE_SLICE_IDS
        and index.get("latest_source_final_gate_passed") is True
        and all(
            isinstance(entry, dict)
            and entry.get("slice_id") in SOURCE_SLICE_IDS
            and entry.get("root_exists") is True
            and entry.get("product_pass") is True
            and entry.get("reviewer_pass") is True
            and entry.get("boundary_pass") is True
            and entry.get("verification_present") is True
            and entry.get("final_gate_declared") is True
            and entry.get("allowed_use") == "operator_orientation_and_gate_routing_only"
            and MUST_NOT_REQUIRED <= set(entry.get("must_not", []))
            for entry in entries
        )
        and all(index.get(flag) is False for flag in ["automatic_execution", "mainline_ready", "promotion_ready", "action_basis_ready"])
        and index.get("operator_next_action") == "read_index_and_run_latest_gate_only_until_p2_59_product_pass"
        and MUST_NOT_REQUIRED <= set(index.get("must_not", []))
        and not dangerous_markdown(index)
    )


def recompute_handoff_ready(index: dict) -> bool:
    self_gate = index.get("self_report_gate", {})
    return recompute_source_chain_ready(index) and self_gate.get("overall_pass") is True


def validate_index(index: dict, failures: list[str], label: str) -> None:
    add_failure(failures, index.get("record_kind") == "sandbox_user_decision_operator_handoff_index", f"{label} wrong record_kind")
    add_failure(failures, index.get("slice_id") == SLICE_ID, f"{label} wrong slice_id")
    add_failure(failures, index.get("truth_boundary") == "operator_handoff_index_not_user_decision_or_execution_authority", f"{label} wrong truth boundary")
    add_failure(failures, index.get("entry_count") == len(SOURCE_SLICE_IDS), f"{label} entry_count mismatch")
    add_failure(failures, not dangerous_markdown(index), f"{label} dangerous authority phrase in markdown")
    recomputed_source = recompute_source_chain_ready(index)
    add_failure(failures, recomputed_source, f"{label} recomputed source_chain_ready false")
    add_failure(failures, index.get("source_chain_ready") is recomputed_source, f"{label} stored source_chain_ready disagrees with recomputed")
    recomputed = recompute_handoff_ready(index)
    add_failure(failures, index.get("handoff_ready") is recomputed, f"{label} stored handoff_ready disagrees with recomputed")


def validate_fixtures(fixtures: list[Path], index: dict, failures: list[str]) -> int:
    by_id = {entry.get("slice_id"): entry for entry in index.get("entries", []) if isinstance(entry, dict)}
    seen_sources = set()
    seen_summary = False
    for path in fixtures:
        fixture = load_json(path)
        if not isinstance(fixture, dict):
            failures.append(f"{path.name} is not object")
            continue
        if fixture.get("fixture_kind") == "source_entry_expected":
            slice_id = fixture.get("slice_id")
            seen_sources.add(str(slice_id))
            entry = by_id.get(slice_id)
            add_failure(failures, isinstance(entry, dict), f"{path.name} source missing")
            if isinstance(entry, dict):
                for key in ["product_pass", "reviewer_pass", "boundary_pass", "final_gate_declared"]:
                    add_failure(failures, entry.get(key) is fixture.get(key), f"{path.name} {key} mismatch")
                add_failure(failures, entry.get("operator_use") == fixture.get("operator_use"), f"{path.name} operator_use mismatch")
        elif fixture.get("fixture_kind") == "handoff_summary_expected":
            seen_summary = True
            add_failure(failures, index.get("entry_count") == fixture.get("entry_count"), f"{path.name} entry count mismatch")
            add_failure(failures, index.get("source_chain_ready") is fixture.get("source_chain_ready"), f"{path.name} source_chain_ready mismatch")
            add_failure(failures, index.get("handoff_ready") is index.get("self_report_gate", {}).get("overall_pass"), f"{path.name} handoff/self gate mismatch")
        else:
            failures.append(f"{path.name} unknown fixture_kind {fixture.get('fixture_kind')}")
    for slice_id in SOURCE_SLICE_IDS:
        add_failure(failures, slice_id in seen_sources, f"missing fixture for {slice_id}")
    add_failure(failures, seen_summary, "missing summary fixture")
    return len(fixtures)


def set_entry(index: dict, slice_id: str, key: str, value: object) -> None:
    for entry in index.get("entries", []):
        if isinstance(entry, dict) and entry.get("slice_id") == slice_id:
            entry[key] = value


def apply_mutation(index: dict, mutation: dict) -> dict:
    mutated = json.loads(json.dumps(index, ensure_ascii=False))
    if "set_top" in mutation:
        for key, value in mutation["set_top"].items():
            mutated[key] = value
    if "set_entry" in mutation:
        item = mutation["set_entry"]
        set_entry(mutated, item["slice_id"], item["key"], item["value"])
    if "drop_entry" in mutation:
        mutated["entries"] = [entry for entry in mutated.get("entries", []) if entry.get("slice_id") != mutation["drop_entry"]]
    if "remove_top_must_not" in mutation:
        value = mutation["remove_top_must_not"]
        mutated["must_not"] = [item for item in mutated.get("must_not", []) if item != value]
    if "remove_entry_must_not" in mutation:
        item = mutation["remove_entry_must_not"]
        for entry in mutated.get("entries", []):
            if entry.get("slice_id") == item["slice_id"]:
                entry["must_not"] = [value for value in entry.get("must_not", []) if value != item["value"]]
    if "append_markdown" in mutation:
        mutated["handoff_markdown"] = str(mutated.get("handoff_markdown", "")) + "\n" + mutation["append_markdown"]
    return mutated


def validate_failure_cases(files: list[Path], index: dict, failures: list[str]) -> int:
    cases: list[dict] = []
    for path in files:
        payload = load_json(path)
        if isinstance(payload, list):
            cases.extend(item for item in payload if isinstance(item, dict))
        elif isinstance(payload, dict):
            cases.append(payload)
    add_failure(failures, len(cases) >= 16, "expected at least 16 failure cases")
    ids = [case.get("failure_id") for case in cases]
    add_failure(failures, len(ids) == len(set(ids)), "failure ids not unique")
    joined = "\n".join(str(case) for case in cases)
    for token in ["product", "reviewer", "boundary", "gate", "entry", "must_not", "mainline", "promotion", "sync", "dependency", "service", "hook", "mcp", "action_basis"]:
        add_failure(failures, token in joined, f"failure cases do not cover {token}")
    for case in cases:
        mutation = case.get("mutation")
        add_failure(failures, isinstance(mutation, dict) and bool(mutation), f"{case.get('failure_id')} lacks mutation")
        if isinstance(mutation, dict):
            mutated = apply_mutation(index, mutation)
            local_failures: list[str] = []
            validate_index(mutated, local_failures, "mutated")
            add_failure(failures, bool(local_failures), f"{case.get('failure_id')} mutation was not rejected")
        add_failure(failures, MUST_NOT_REQUIRED <= set(case.get("must_not", [])), f"{case.get('failure_id')} must_not incomplete")
    return len(cases)


def validate_final_reports(failures: list[str]) -> None:
    add_failure(failures, frontmatter_status(ROOT / "verification.md") == "local_verification_passed", "verification status not passed")
    add_failure(failures, "REVIEW_PASS_NO_BLOCKER" in read_text(ROOT / "reviewer-report.md"), "Reviewer report lacks REVIEW_PASS_NO_BLOCKER")
    add_failure(failures, "PASS_BOUNDARY" in read_text(ROOT / "boundary-audit.md"), "Boundary audit lacks PASS_BOUNDARY")
    add_failure(failures, "PASS_PRODUCT_GRADE" in read_text(ROOT / "product-acceptance-report.md"), "Product report lacks PASS_PRODUCT_GRADE")
    add_failure(failures, frontmatter_status(ROOT / "next-step.md") == "pass_product_grade_pending_next_slice", "next-step status not passed")


def verify(final_gate: bool = False) -> dict:
    failures: list[str] = []
    fixtures, failure_files = validate_files(failures)
    contract_path = ARTIFACT / "user_decision_operator_handoff_index_contract.json"
    contract = load_json(contract_path) if contract_path.exists() else {}
    if isinstance(contract, dict):
        validate_contract(contract, failures)
    else:
        failures.append("contract is not object")
    runner = import_runner()
    index = runner.run_index()
    validate_index(index, failures, "index")
    fixture_count = validate_fixtures(fixtures, index, failures)
    failure_case_count = validate_failure_cases(failure_files, index, failures)
    if final_gate:
        validate_final_reports(failures)
    return {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "entry_count": index.get("entry_count"),
            "fixture_count": fixture_count,
            "failure_case_count": failure_case_count,
            "latest_source_final_gate_passed": index.get("latest_source_final_gate_passed"),
            "handoff_ready": index.get("handoff_ready"),
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
