from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-60-user-decision-index-freeze-checksum-sandbox"
ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"
MANIFEST_PATH = ARTIFACT / "user_decision_index_freeze_checksum_manifest.json"

SOURCE_SLICE_IDS = [
    "2026-06-16-p2-51-user-decision-request-packet-sandbox",
    "2026-06-16-p2-52-user-decision-no-auto-advance-guard-sandbox",
    "2026-06-16-p2-53-user-response-classifier-dry-run-sandbox",
    "2026-06-16-p2-54-safe-user-response-renderer-dry-run-sandbox",
    "2026-06-16-p2-55-user-decision-e2e-dry-run-simulator-sandbox",
    "2026-06-16-p2-56-user-decision-demo-transcript-smoke-runner-sandbox",
    "2026-06-16-p2-57-user-decision-chain-regression-bundle-sandbox",
    "2026-06-16-p2-58-user-decision-static-boundary-scan-regression-sandbox",
    "2026-06-16-p2-59-user-decision-operator-handoff-index-sandbox",
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
    "build_user_decision_index_freeze_checksum.py",
    "verify_user_decision_index_freeze_checksum.py",
    "user_decision_index_freeze_checksum_contract.json",
    "user_decision_index_freeze_checksum_manifest.json",
    "user_decision_index_freeze_checksum_readout.md",
    "user_decision_index_freeze_checksum_prototype.html",
]

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


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def add_failure(failures: list[str], condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def import_builder():
    path = ARTIFACT / "build_user_decision_index_freeze_checksum.py"
    spec = importlib.util.spec_from_file_location("p2_60_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load p2-60 builder")
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
    add_failure(failures, len(fixtures) >= 3, "expected at least 3 fixtures")
    add_failure(failures, len(failure_cases) >= 1, "expected failure cases")
    return fixtures, failure_cases


def validate_contract(contract: dict, failures: list[str]) -> None:
    add_failure(failures, contract.get("record_kind") == "sandbox_user_decision_index_freeze_checksum_contract", "wrong contract record_kind")
    add_failure(failures, contract.get("slice_id") == SLICE_ID, "wrong contract slice_id")
    add_failure(failures, contract.get("source_slice_ids") == SOURCE_SLICE_IDS, "wrong contract source_slice_ids")
    add_failure(failures, contract.get("hash_algorithm") == "sha256_bytes", "wrong hash_algorithm")
    add_failure(failures, contract.get("truth_boundary") == "checksum_freeze_not_user_decision_or_execution_authority", "wrong truth boundary")
    add_failure(
        failures,
        contract.get("latest_source_status_method") == "read_existing_reports_no_script_execution",
        "latest source status method must be report-read only",
    )
    status_paths = contract.get("latest_source_status_paths", [])
    add_failure(failures, isinstance(status_paths, list) and len(status_paths) >= 5, "latest source status paths incomplete")
    add_failure(
        failures,
        all(SOURCE_SLICE_IDS[-1] in str(path) for path in status_paths),
        "latest source status paths must point to p2-59 reports",
    )
    add_failure(failures, "latest_source_final_gate_command" not in contract, "contract must not execute latest source command")
    add_failure(failures, MUST_NOT_REQUIRED <= set(contract.get("output_contract", {}).get("must_not", [])), "contract must_not incomplete")


def dangerous_readout() -> bool:
    text = read_text(ARTIFACT / "user_decision_index_freeze_checksum_readout.md") + "\n" + read_text(
        ARTIFACT / "user_decision_index_freeze_checksum_prototype.html"
    )
    return any(phrase in text for phrase in DANGEROUS_PHRASES)


def validate_manifest(manifest: dict, current: dict, failures: list[str], label: str) -> None:
    add_failure(failures, manifest.get("record_kind") == "sandbox_user_decision_index_freeze_checksum_manifest", f"{label} wrong record_kind")
    add_failure(failures, manifest.get("slice_id") == SLICE_ID, f"{label} wrong slice_id")
    add_failure(failures, manifest.get("source_slice_ids") == SOURCE_SLICE_IDS, f"{label} wrong source_slice_ids")
    add_failure(failures, manifest.get("truth_boundary") == "checksum_freeze_not_user_decision_or_execution_authority", f"{label} wrong truth boundary")
    add_failure(failures, manifest.get("hash_algorithm") == "sha256_bytes", f"{label} wrong hash algorithm")
    add_failure(failures, manifest.get("latest_source_final_gate_passed") is True, f"{label} latest source gate not passed")
    add_failure(
        failures,
        manifest.get("latest_source_status_method") == "read_existing_reports_no_script_execution",
        f"{label} latest source status method must be report-read only",
    )
    add_failure(failures, "latest_source_final_gate_command" not in manifest, f"{label} must not include executable latest source command")
    recorded = manifest.get("latest_source_recorded_status", {})
    if isinstance(recorded, dict):
        add_failure(failures, recorded.get("status_method") == "read_existing_reports_no_script_execution", f"{label} recorded status method wrong")
        add_failure(failures, recorded.get("verification_status") == "local_verification_passed", f"{label} source verification not passed")
        add_failure(failures, recorded.get("reviewer_passed") is True, f"{label} source reviewer not passed")
        add_failure(failures, recorded.get("boundary_passed") is True, f"{label} source boundary not passed")
        add_failure(failures, recorded.get("product_acceptance_passed") is True, f"{label} source product not passed")
        add_failure(
            failures,
            recorded.get("next_step_status") == "pass_product_grade_pending_next_slice",
            f"{label} source next-step not passed",
        )
    else:
        failures.append(f"{label} recorded status missing")
    add_failure(failures, manifest.get("freeze_ready") is True, f"{label} freeze_ready not true")
    add_failure(failures, manifest.get("missing_count") == 0, f"{label} missing_count not zero")
    add_failure(failures, MUST_NOT_REQUIRED <= set(manifest.get("must_not", [])), f"{label} must_not incomplete")
    for flag in ["automatic_execution", "mainline_ready", "promotion_ready", "action_basis_ready"]:
        add_failure(failures, manifest.get(flag) is False, f"{label} {flag} not false")
    entries = manifest.get("entries", [])
    current_entries = current.get("entries", [])
    add_failure(failures, isinstance(entries, list) and len(entries) > 0, f"{label} entries missing")
    add_failure(failures, manifest.get("entry_count") == len(entries), f"{label} entry_count mismatch")
    add_failure(failures, len(entries) == len(current_entries), f"{label} current entry count mismatch")
    by_path = {entry.get("path"): entry for entry in entries if isinstance(entry, dict)}
    current_by_path = {entry.get("path"): entry for entry in current_entries if isinstance(entry, dict)}
    add_failure(failures, len(by_path) == len(entries), f"{label} duplicate manifest paths")
    for path, entry in by_path.items():
        current_entry = current_by_path.get(path)
        add_failure(failures, isinstance(current_entry, dict), f"{label} path missing from current manifest: {path}")
        if isinstance(current_entry, dict):
            for key in ["sha256", "bytes", "source_slice_id"]:
                add_failure(failures, entry.get(key) == current_entry.get(key), f"{label} {path} {key} drift")
        add_failure(
            failures,
            any(str(path).startswith(f"outputs/review/vaks-implementation-sandbox/{slice_id}/") for slice_id in SOURCE_SLICE_IDS),
            f"{label} path outside source slices: {path}",
        )
    for slice_id in SOURCE_SLICE_IDS:
        add_failure(failures, any(entry.get("source_slice_id") == slice_id for entry in entries), f"{label} no entries for {slice_id}")
    add_failure(failures, not dangerous_readout(), f"{label} dangerous authority phrase in readout/prototype")


def validate_fixtures(fixtures: list[Path], manifest: dict, failures: list[str]) -> int:
    seen = set()
    for path in fixtures:
        fixture = load_json(path)
        if not isinstance(fixture, dict):
            failures.append(f"{path.name} is not object")
            continue
        seen.add(str(fixture.get("fixture_id")))
        if fixture.get("fixture_id") == "source-count":
            add_failure(failures, len(manifest.get("source_slice_ids", [])) == fixture.get("source_count"), "source-count mismatch")
        elif fixture.get("fixture_id") == "freeze-ready":
            add_failure(failures, manifest.get("freeze_ready") is fixture.get("freeze_ready"), "freeze-ready mismatch")
            add_failure(failures, manifest.get("latest_source_final_gate_passed") is fixture.get("latest_source_final_gate_passed"), "latest gate mismatch")
        elif fixture.get("fixture_id") == "must-not":
            add_failure(failures, MUST_NOT_REQUIRED <= set(manifest.get("must_not", [])), "must-not fixture mismatch")
        else:
            failures.append(f"unknown fixture {path.name}")
    for required in ["source-count", "freeze-ready", "must-not"]:
        add_failure(failures, required in seen, f"missing fixture {required}")
    return len(fixtures)


def apply_mutation(manifest: dict, mutation: dict) -> dict:
    mutated = json.loads(json.dumps(manifest, ensure_ascii=False))
    if "set_top" in mutation:
        for key, value in mutation["set_top"].items():
            mutated[key] = value
    if "set_first_entry" in mutation and mutated.get("entries"):
        for key, value in mutation["set_first_entry"].items():
            mutated["entries"][0][key] = value
    if "drop_first_entry" in mutation and mutated.get("entries"):
        mutated["entries"] = mutated["entries"][1:]
    if "duplicate_first_entry" in mutation and mutated.get("entries"):
        mutated["entries"].append(json.loads(json.dumps(mutated["entries"][0])))
    if "remove_source_slice" in mutation:
        target = mutation["remove_source_slice"]
        mutated["source_slice_ids"] = [item for item in mutated.get("source_slice_ids", []) if item != target]
    if "remove_must_not" in mutation:
        value = mutation["remove_must_not"]
        mutated["must_not"] = [item for item in mutated.get("must_not", []) if item != value]
    return mutated


def validate_failure_cases(files: list[Path], manifest: dict, current: dict, failures: list[str]) -> int:
    cases: list[dict] = []
    for path in files:
        payload = load_json(path)
        if isinstance(payload, list):
            cases.extend(item for item in payload if isinstance(item, dict))
        elif isinstance(payload, dict):
            cases.append(payload)
    add_failure(failures, len(cases) >= 13, "expected at least 13 failure cases")
    ids = [case.get("failure_id") for case in cases]
    add_failure(failures, len(ids) == len(set(ids)), "failure ids not unique")
    joined = "\n".join(str(case) for case in cases)
    for token in ["hash", "bytes", "entry", "source", "gate", "freeze", "must_not", "mainline", "promotion", "action_basis", "outside", "duplicate"]:
        add_failure(failures, token in joined, f"failure cases do not cover {token}")
    for case in cases:
        mutation = case.get("mutation")
        add_failure(failures, isinstance(mutation, dict) and bool(mutation), f"{case.get('failure_id')} lacks mutation")
        if isinstance(mutation, dict):
            mutated = apply_mutation(manifest, mutation)
            local_failures: list[str] = []
            validate_manifest(mutated, current, local_failures, "mutated")
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
    contract = load_json(ARTIFACT / "user_decision_index_freeze_checksum_contract.json") if (ARTIFACT / "user_decision_index_freeze_checksum_contract.json").exists() else {}
    if isinstance(contract, dict):
        validate_contract(contract, failures)
    else:
        failures.append("contract is not object")
    manifest = load_json(MANIFEST_PATH) if MANIFEST_PATH.exists() else {}
    builder = import_builder()
    current = builder.build_manifest()
    if isinstance(manifest, dict):
        validate_manifest(manifest, current, failures, "manifest")
    else:
        failures.append("manifest is not object")
        manifest = {}
    fixture_count = validate_fixtures(fixtures, manifest, failures)
    failure_case_count = validate_failure_cases(failure_files, manifest, current, failures)
    if final_gate:
        validate_final_reports(failures)
    return {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "source_slice_count": len(SOURCE_SLICE_IDS),
            "entry_count": manifest.get("entry_count"),
            "fixture_count": fixture_count,
            "failure_case_count": failure_case_count,
            "latest_source_final_gate_passed": manifest.get("latest_source_final_gate_passed"),
            "freeze_ready": manifest.get("freeze_ready"),
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
