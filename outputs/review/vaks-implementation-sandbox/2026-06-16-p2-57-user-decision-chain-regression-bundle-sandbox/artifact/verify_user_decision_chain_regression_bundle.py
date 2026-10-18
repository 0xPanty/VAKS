from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-57-user-decision-chain-regression-bundle-sandbox"
ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
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
]

MUST_NOT_REQUIRED = {
    "execute_option",
    "merge_mainline",
    "promote",
    "sync_obsidian",
    "commit",
    "push",
    "write_reviewed_knowledge",
    "create_evidence_support",
    "create_action_basis",
    "start_future_slice_by_inference",
}

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
    "build_user_decision_chain_regression_bundle.py",
    "run_user_decision_chain_regression_bundle.py",
    "verify_user_decision_chain_regression_bundle.py",
    "user_decision_chain_regression_contract.json",
    "user_decision_chain_regression_readout.md",
    "user_decision_chain_regression_prototype.html",
]

DANGEROUS_READOUT_PHRASES = [
    "ready for mainline",
    "mainline approved",
    "promotion approved",
    "execution approved",
    "Obsidian sync approved",
    "reviewed knowledge created",
    "evidence support created",
    "action basis created",
    "可以合并",
    "已合并",
    "可以同步",
    "已同步",
    "执行授权",
    "pip install",
    "npm install",
    "pnpm add",
    "yarn add",
    "background service",
    "Start-Process",
    "Register-ScheduledTask",
    "MCP write",
    "hook installed",
    "git commit",
    "git push",
]

FORBIDDEN_STATIC_COMMAND_PHRASES = [
    "pip install",
    "npm install",
    "pnpm add",
    "yarn add",
    "Start-Process",
    "Register-ScheduledTask",
    "New-Service",
    "schtasks",
    "git commit",
    "git push",
    "mcp write",
    "hook installed",
    "shell=True",
]


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def add_failure(failures: list[str], condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def frontmatter_status(path: Path) -> str:
    for line in read_text(path).splitlines():
        if line.lower().startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def import_runner():
    path = ARTIFACT / "run_user_decision_chain_regression_bundle.py"
    spec = importlib.util.spec_from_file_location("p2_57_runner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load p2-57 runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_files(failures: list[str]) -> tuple[list[Path], list[Path]]:
    for filename in REQUIRED_ROOT:
        add_failure(failures, (ROOT / filename).exists(), f"missing root file: {filename}")
    for filename in REQUIRED_ARTIFACT:
        add_failure(failures, (ARTIFACT / filename).exists(), f"missing artifact file: {filename}")
    fixture_files = sorted(FIXTURES.glob("*.json"))
    failure_files = sorted(FAILURE_CASES.glob("*.json"))
    add_failure(failures, len(fixture_files) >= 8, "expected at least 8 fixtures")
    add_failure(failures, len(failure_files) >= 1, "expected failure cases")
    return fixture_files, failure_files


def validate_static_boundary_surface(failures: list[str]) -> None:
    scanned_paths = [
        ARTIFACT / "run_user_decision_chain_regression_bundle.py",
        ARTIFACT / "build_user_decision_chain_regression_bundle.py",
    ]
    for path in scanned_paths:
        text = read_text(path)
        lower_text = text.lower()
        for phrase in FORBIDDEN_STATIC_COMMAND_PHRASES:
            add_failure(
                failures,
                phrase.lower() not in lower_text,
                f"forbidden static command phrase in {path.name}: {phrase}",
            )
    build_path = ARTIFACT / "build_user_decision_chain_regression_bundle.py"
    write_lines = [
        line.strip()
        for line in read_text(build_path).splitlines()
        if ".write_text(" in line
    ]
    add_failure(
        failures,
        write_lines == [
            'READOUT.write_text(result["readout_markdown"] + "\\n", encoding="utf-8")',
            "PROTOTYPE.write_text(render_html(result), encoding=\"utf-8\")",
        ],
        f"builder write surface drifted: {write_lines}",
    )
    runner_text = read_text(ARTIFACT / "run_user_decision_chain_regression_bundle.py")
    add_failure(failures, "P2_56_VERIFIER" in runner_text, "runner no longer calls explicit p2-56 verifier")
    add_failure(failures, '"--final-gate"' in runner_text, "runner no longer requires p2-56 --final-gate")


def validate_contract(contract: dict, failures: list[str]) -> None:
    add_failure(failures, contract.get("record_kind") == "sandbox_user_decision_chain_regression_contract", "wrong record_kind")
    add_failure(failures, contract.get("slice_id") == SLICE_ID, "wrong slice_id")
    add_failure(failures, contract.get("source_slice_ids") == SOURCE_SLICE_IDS, "wrong source_slice_ids")
    add_failure(
        failures,
        contract.get("truth_boundary") == "chain_regression_bundle_not_user_decision_or_execution_authority",
        "wrong truth boundary",
    )
    source_gate = contract.get("source_final_gate_command", "")
    add_failure(failures, SOURCE_SLICE_IDS[-1] in source_gate and "--final-gate" in source_gate, "source gate incomplete")
    output = contract.get("output_contract", {})
    for flag in [
        "automatic_execution",
        "decision_collected",
        "ready_to_execute",
        "mainline_ready",
        "promotion_ready",
        "action_basis_ready",
    ]:
        add_failure(failures, output.get(flag) is False, f"contract {flag} not false")
    add_failure(failures, MUST_NOT_REQUIRED <= set(output.get("must_not", [])), "contract must_not incomplete")
    usage = contract.get("ordinary_agent_usage", {})
    add_failure(failures, "Builder-only" in usage.get("rebuild", ""), "rebuild not Builder-only")
    add_failure(failures, "--final-gate" in usage.get("final_gate", ""), "final gate usage missing")
    non_claims = "\n".join(str(item) for item in contract.get("required_non_claims", []))
    for phrase in [
        "not a user decision",
        "not execution authority",
        "not mainline approval",
        "not promotion approval",
        "not Obsidian sync approval",
        "not reviewed knowledge",
        "not evidence support",
        "not action basis",
    ]:
        add_failure(failures, phrase in non_claims, f"missing non-claim phrase: {phrase}")


def recompute_chain_passed(result: dict) -> bool:
    reports = result.get("source_reports", [])
    source_all_pass = (
        isinstance(reports, list)
        and len(reports) == len(SOURCE_SLICE_IDS)
        and all(
            isinstance(report, dict)
            and report.get("root_exists") is True
            and report.get("product_pass") is True
            and report.get("reviewer_pass") is True
            and report.get("boundary_pass") is True
            and report.get("verification_present") is True
            and report.get("next_step_present") is True
            for report in reports
        )
    )
    demo_summary = result.get("demo_summary", {})
    demo_rows = result.get("demo_rows", [])
    demo_safe = (
        isinstance(demo_summary, dict)
        and demo_summary.get("scenario_count") == len(demo_rows)
        and demo_summary.get("scenario_count", 0) >= 9
        and demo_summary.get("demo_safe") is True
        and demo_summary.get("automatic_execution") is False
        and demo_summary.get("decision_collected") is False
        and demo_summary.get("ready_to_execute") is False
        and all(
            isinstance(row, dict)
            and row.get("automatic_execution") is False
            and row.get("decision_collected") is False
            and row.get("ready_to_execute") is False
            and MUST_NOT_REQUIRED <= set(row.get("must_not", []))
            for row in demo_rows
        )
    )
    top_flags_false = all(
        result.get(flag) is False
        for flag in [
            "automatic_execution",
            "decision_collected",
            "ready_to_execute",
            "mainline_ready",
            "promotion_ready",
            "action_basis_ready",
        ]
    )
    return (
        source_all_pass
        and result.get("p2_56_final_gate_passed") is True
        and demo_safe
        and top_flags_false
        and MUST_NOT_REQUIRED <= set(result.get("must_not", []))
        and not has_dangerous_readout(result)
    )


def has_dangerous_readout(result: dict) -> bool:
    readout = str(result.get("readout_markdown", ""))
    return any(phrase in readout for phrase in DANGEROUS_READOUT_PHRASES)


def validate_bundle_result(result: dict, failures: list[str], label: str) -> None:
    add_failure(failures, result.get("record_kind") == "sandbox_user_decision_chain_regression_result", f"{label} wrong record_kind")
    add_failure(failures, result.get("slice_id") == SLICE_ID, f"{label} wrong slice_id")
    add_failure(failures, result.get("source_slice_ids") == SOURCE_SLICE_IDS, f"{label} wrong source_slice_ids")
    add_failure(
        failures,
        result.get("truth_boundary") == "chain_regression_bundle_not_user_decision_or_execution_authority",
        f"{label} wrong truth boundary",
    )
    for flag in [
        "automatic_execution",
        "decision_collected",
        "ready_to_execute",
        "mainline_ready",
        "promotion_ready",
        "action_basis_ready",
    ]:
        add_failure(failures, result.get(flag) is False, f"{label} {flag} not false")
    add_failure(failures, MUST_NOT_REQUIRED <= set(result.get("must_not", [])), f"{label} must_not incomplete")
    reports = result.get("source_reports", [])
    add_failure(failures, isinstance(reports, list), f"{label} source_reports not list")
    if isinstance(reports, list):
        by_id = {report.get("slice_id"): report for report in reports if isinstance(report, dict)}
        for slice_id in SOURCE_SLICE_IDS:
            report = by_id.get(slice_id)
            add_failure(failures, isinstance(report, dict), f"{label} missing source report {slice_id}")
            if isinstance(report, dict):
                for key in ["root_exists", "product_pass", "reviewer_pass", "boundary_pass", "verification_present", "next_step_present"]:
                    add_failure(failures, report.get(key) is True, f"{label} {slice_id} {key} not true")
    counts = result.get("source_pass_counts", {})
    for key in ["source_count", "product_pass", "reviewer_pass", "boundary_pass", "verification_present"]:
        add_failure(failures, counts.get(key) == len(SOURCE_SLICE_IDS), f"{label} count {key} mismatch")
    add_failure(failures, result.get("p2_56_final_gate_passed") is True, f"{label} p2-56 final gate not true")
    add_failure(failures, not has_dangerous_readout(result), f"{label} dangerous readout overclaim")
    recomputed = recompute_chain_passed(result)
    add_failure(failures, recomputed, f"{label} recomputed chain failed")
    add_failure(failures, result.get("chain_passed") is recomputed, f"{label} stored chain_passed disagrees with recomputed chain")


def validate_fixtures(fixture_files: list[Path], result: dict, failures: list[str]) -> int:
    by_id = {report.get("slice_id"): report for report in result.get("source_reports", []) if isinstance(report, dict)}
    seen_source_ids = set()
    seen_chain = False
    seen_demo = False
    for path in fixture_files:
        fixture = load_json(path)
        if not isinstance(fixture, dict):
            failures.append(f"{path.name} is not object")
            continue
        kind = fixture.get("fixture_kind")
        if kind == "source_slice_expected":
            slice_id = fixture.get("slice_id")
            seen_source_ids.add(str(slice_id))
            report = by_id.get(slice_id)
            add_failure(failures, isinstance(report, dict), f"{path.name} source missing from result")
            if isinstance(report, dict):
                for key in ["product_pass", "reviewer_pass", "boundary_pass", "verification_present", "next_step_present"]:
                    add_failure(failures, report.get(key) is fixture.get(key), f"{path.name} {key} mismatch")
        elif kind == "chain_summary_expected":
            seen_chain = True
            add_failure(failures, result.get("chain_passed") is fixture.get("chain_passed"), f"{path.name} chain mismatch")
            add_failure(
                failures,
                result.get("source_pass_counts", {}).get("source_count") == fixture.get("source_count"),
                f"{path.name} source count mismatch",
            )
        elif kind == "demo_guard_expected":
            seen_demo = True
            demo_summary = result.get("demo_summary", {})
            add_failure(failures, demo_summary.get("scenario_count") == fixture.get("scenario_count"), f"{path.name} scenario count mismatch")
            add_failure(failures, demo_summary.get("demo_safe") is fixture.get("demo_safe"), f"{path.name} demo_safe mismatch")
            add_failure(failures, MUST_NOT_REQUIRED <= set(result.get("must_not", [])), f"{path.name} must_not incomplete")
        else:
            failures.append(f"{path.name} unknown fixture_kind {kind}")
    for slice_id in SOURCE_SLICE_IDS:
        add_failure(failures, slice_id in seen_source_ids, f"missing source fixture for {slice_id}")
    add_failure(failures, seen_chain, "missing chain summary fixture")
    add_failure(failures, seen_demo, "missing demo guard fixture")
    return len(fixture_files)


def set_source_field(result: dict, slice_id: str, key: str, value: object) -> None:
    for report in result.get("source_reports", []):
        if isinstance(report, dict) and report.get("slice_id") == slice_id:
            report[key] = value


def set_demo_row_field(result: dict, scenario_id: str, key: str, value: object) -> None:
    for row in result.get("demo_rows", []):
        if isinstance(row, dict) and row.get("scenario_id") == scenario_id:
            row[key] = value


def apply_mutation(result: dict, mutation: dict) -> dict:
    mutated = json.loads(json.dumps(result, ensure_ascii=False))
    if "set_top" in mutation:
        for key, value in mutation["set_top"].items():
            mutated[key] = value
    if "set_source" in mutation:
        source = mutation["set_source"]
        set_source_field(mutated, source["slice_id"], source["key"], source["value"])
    if "drop_source_slice_id" in mutation:
        drop_id = mutation["drop_source_slice_id"]
        mutated["source_reports"] = [item for item in mutated.get("source_reports", []) if item.get("slice_id") != drop_id]
    if "set_count" in mutation:
        count = mutation["set_count"]
        mutated.setdefault("source_pass_counts", {})[count["key"]] = count["value"]
    if "set_demo_summary" in mutation:
        for key, value in mutation["set_demo_summary"].items():
            mutated.setdefault("demo_summary", {})[key] = value
    if "set_demo_row" in mutation:
        row = mutation["set_demo_row"]
        set_demo_row_field(mutated, row["scenario_id"], row["key"], row["value"])
    if "remove_top_must_not" in mutation:
        target = mutation["remove_top_must_not"]
        mutated["must_not"] = [item for item in mutated.get("must_not", []) if item != target]
    if "remove_row_must_not" in mutation:
        row = mutation["remove_row_must_not"]
        for demo_row in mutated.get("demo_rows", []):
            if demo_row.get("scenario_id") == row["scenario_id"]:
                demo_row["must_not"] = [item for item in demo_row.get("must_not", []) if item != row["value"]]
    if "append_readout" in mutation:
        mutated["readout_markdown"] = str(mutated.get("readout_markdown", "")) + "\n" + mutation["append_readout"]
    return mutated


def validate_failure_cases(failure_files: list[Path], result: dict, failures: list[str]) -> int:
    all_cases: list[dict] = []
    for path in failure_files:
        payload = load_json(path)
        if isinstance(payload, list):
            all_cases.extend(item for item in payload if isinstance(item, dict))
        elif isinstance(payload, dict):
            all_cases.append(payload)
    add_failure(failures, len(all_cases) >= 20, "expected at least 20 failure cases")
    ids = [item.get("failure_id") for item in all_cases]
    add_failure(failures, len(ids) == len(set(ids)), "failure ids not unique")
    joined = "\n".join(str(item) for item in all_cases)
    for token in [
        "product",
        "reviewer",
        "boundary",
        "verification",
        "final_gate",
        "automatic_execution",
        "mainline",
        "promotion",
        "action_basis",
        "must_not",
        "readout",
        "scenario",
        "source",
        "chain",
        "dependency",
        "service",
        "hook",
        "mcp_write",
        "git",
    ]:
        add_failure(failures, token in joined, f"failure cases do not cover {token}")
    for item in all_cases:
        mutation = item.get("mutation")
        add_failure(failures, isinstance(mutation, dict) and bool(mutation), f"{item.get('failure_id')} lacks executable mutation")
        if isinstance(mutation, dict) and mutation:
            mutated = apply_mutation(result, mutation)
            local_failures: list[str] = []
            validate_bundle_result(mutated, local_failures, "mutated")
            add_failure(failures, bool(local_failures), f"{item.get('failure_id')} mutation was not rejected")
        add_failure(failures, MUST_NOT_REQUIRED <= set(item.get("must_not", [])), f"{item.get('failure_id')} must_not incomplete")
    return len(all_cases)


def validate_final_reports(failures: list[str]) -> None:
    add_failure(failures, frontmatter_status(ROOT / "verification.md") == "local_verification_passed", "verification status not passed")
    add_failure(failures, "REVIEW_PASS_NO_BLOCKER" in read_text(ROOT / "reviewer-report.md"), "Reviewer report lacks REVIEW_PASS_NO_BLOCKER")
    add_failure(failures, "PASS_BOUNDARY" in read_text(ROOT / "boundary-audit.md"), "Boundary audit lacks PASS_BOUNDARY")
    add_failure(failures, "PASS_PRODUCT_GRADE" in read_text(ROOT / "product-acceptance-report.md"), "Product report lacks PASS_PRODUCT_GRADE")
    add_failure(failures, frontmatter_status(ROOT / "next-step.md") == "pass_product_grade_pending_next_slice", "next-step status not passed")


def verify(final_gate: bool = False) -> dict:
    failures: list[str] = []
    fixture_files, failure_files = validate_files(failures)
    validate_static_boundary_surface(failures)
    contract_path = ARTIFACT / "user_decision_chain_regression_contract.json"
    contract = load_json(contract_path) if contract_path.exists() else {}
    if isinstance(contract, dict):
        validate_contract(contract, failures)
    else:
        failures.append("contract is not object")
        contract = {}
    runner = import_runner()
    result = runner.run_bundle()
    validate_bundle_result(result, failures, "bundle")
    fixture_count = validate_fixtures(fixture_files, result, failures)
    failure_case_count = validate_failure_cases(failure_files, result, failures)
    if final_gate:
        validate_final_reports(failures)
    return {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "source_slice_count": len(SOURCE_SLICE_IDS),
            "fixture_count": fixture_count,
            "failure_case_count": failure_case_count,
            "p2_56_final_gate_passed": result.get("p2_56_final_gate_passed"),
            "chain_passed": result.get("chain_passed"),
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
