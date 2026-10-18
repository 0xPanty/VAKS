from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


SLICE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = SLICE_ROOT.parents[3]
SLICE_ID = SLICE_ROOT.name

CONTRACT = SLICE_ROOT / "artifact/original_20_operator_status_surface_contract.json"
SURFACE_JSON = SLICE_ROOT / "artifact/original_20_operator_status_surface.json"
SURFACE_MD = SLICE_ROOT / "artifact/original_20_operator_status_surface.md"
SURFACE_HTML = SLICE_ROOT / "artifact/original_20_operator_status_surface.html"
BUILDER = SLICE_ROOT / "artifact/build_original_20_operator_status_surface.py"
VERIFIER = SLICE_ROOT / "artifact/verify_original_20_operator_status_surface.py"
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
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_p2_74", STRICT_STATUS_PACKAGE)
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
    for path in [CONTRACT, SURFACE_JSON, SURFACE_MD, SURFACE_HTML, BUILDER, VERIFIER]:
        add_failure(failures, path.is_file(), f"missing artifact: {path.name}")


def verify_surface(contract: dict, surface: dict, failures: list[str]) -> dict:
    add_failure(failures, surface.get("record_kind") == "sandbox_original_20_operator_status_surface", "wrong record_kind")
    add_failure(failures, surface.get("slice_id") == SLICE_ID, "wrong slice_id")
    numbers = surface.get("numbers", {})
    for key, value in contract.get("expected_numbers", {}).items():
        add_failure(failures, numbers.get(key) == value, f"number mismatch: {key}")
    flags = surface.get("authority_flags", {})
    for key, value in contract.get("authority_flags", {}).items():
        add_failure(failures, flags.get(key) == value, f"authority flag mismatch: {key}")

    cards = surface.get("status_cards", [])
    card_ids = {card.get("card_id") for card in cards}
    add_failure(failures, card_ids == set(contract.get("required_status_cards", [])), "status cards do not match contract")
    options = surface.get("decision_options", [])
    option_ids = {option.get("option_id") for option in options}
    add_failure(failures, option_ids == set(contract.get("required_decision_options", [])), "decision options do not match contract")

    option_map = {option["option_id"]: option for option in options}
    add_failure(failures, option_map["continue_with_sidecar_recloseout"]["allowed_now"] is True, "sidecar continuation not allowed")
    add_failure(failures, option_map["continue_with_sidecar_recloseout"]["edits_old_files"] is False, "sidecar continuation edits old files")
    add_failure(failures, option_map["request_explicit_old_file_status_normalization_approval"]["allowed_now"] is False, "old-file edit request incorrectly allowed now")
    add_failure(failures, option_map["request_explicit_old_file_status_normalization_approval"]["edits_old_files"] is True, "old-file edit option not marked as editing old files")
    add_failure(failures, option_map["do_not_claim_all_old_files_strict_complete"]["allowed_now"] is True, "do-not-claim option not allowed")
    add_failure(failures, option_map["do_not_merge_mainline"]["allowed_now"] is True, "do-not-merge option not allowed")

    md = SURFACE_MD.read_text(encoding="utf-8") if SURFACE_MD.is_file() else ""
    add_failure(failures, "old-file current strict final-gate: `0`" in md, "Markdown missing old-file strict count")
    add_failure(failures, "product-grade sidecar closeout: `20`" in md, "Markdown missing sidecar count")
    add_failure(failures, "Do not say all old files are current strict complete" in md, "Markdown missing forbidden old-file claim")
    return {
        "original_items": numbers.get("original_items"),
        "sidecar_closeout_passed": numbers.get("sidecar_closeout_passed"),
        "old_file_current_strict_final_gate": numbers.get("old_file_current_strict_final_gate"),
        "old_slice_writes_applied": numbers.get("old_slice_writes_applied"),
    }


def verify_fixtures(contract: dict, surface: dict, failures: list[str]) -> None:
    fixture_dir = SLICE_ROOT / "fixtures"
    fixtures = [load_json(path) for path in fixture_dir.glob("*.json")]
    seen = {fixture.get("fixture_id") for fixture in fixtures}
    add_failure(failures, seen == set(contract.get("required_fixture_ids", [])), "fixture ids do not match contract")
    cards = {card.get("card_id") for card in surface.get("status_cards", [])}
    options = {option.get("option_id"): option for option in surface.get("decision_options", [])}
    flags = surface.get("authority_flags", {})
    artifact_state = {
        "has_json": SURFACE_JSON.is_file(),
        "has_markdown": SURFACE_MD.is_file(),
        "has_html": SURFACE_HTML.is_file(),
        "markdown_mentions_old_file_count": "old-file current strict final-gate: `0`" in SURFACE_MD.read_text(encoding="utf-8"),
        "markdown_mentions_sidecar_count": "product-grade sidecar closeout: `20`" in SURFACE_MD.read_text(encoding="utf-8"),
    }
    for fixture in fixtures:
        if "expected_cards" in fixture:
            add_failure(failures, set(fixture["expected_cards"]) == cards, f"{fixture['fixture_id']} card mismatch")
        if "expected" in fixture:
            merged = {}
            merged.update(flags)
            merged.update(artifact_state)
            for key, value in fixture["expected"].items():
                add_failure(failures, merged.get(key) == value, f"{fixture['fixture_id']} expected {key}")
        if "expected_decision_allowed_now" in fixture:
            for option_id, allowed in fixture["expected_decision_allowed_now"].items():
                add_failure(failures, options.get(option_id, {}).get("allowed_now") == allowed, f"{fixture['fixture_id']} option {option_id}")


def verify_failure_cases(contract: dict, failures: list[str]) -> None:
    matrix = load_json(SLICE_ROOT / "failure-cases/original-20-operator-status-surface-failures.json")
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
    surface = load_json(SURFACE_JSON) if SURFACE_JSON.is_file() else {}
    summary = verify_surface(contract, surface, failures) if surface else {}
    verify_fixtures(contract, surface, failures)
    verify_failure_cases(contract, failures)
    if args.final_gate:
        verify_final_gate(failures)

    result = {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "fixture_count": len(list((SLICE_ROOT / "fixtures").glob("*.json"))),
            "failure_case_count": len(load_json(SLICE_ROOT / "failure-cases/original-20-operator-status-surface-failures.json").get("failure_cases", [])),
            **summary,
            "final_gate": bool(args.final_gate),
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
