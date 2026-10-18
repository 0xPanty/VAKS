from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


SLICE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = SLICE_ROOT.parents[3]
SLICE_ID = SLICE_ROOT.name

CONTRACT = SLICE_ROOT / "artifact/old_file_status_normalization_approval_request_contract.json"
PACKET_JSON = SLICE_ROOT / "artifact/old_file_status_normalization_approval_request.json"
PACKET_MD = SLICE_ROOT / "artifact/old_file_status_normalization_approval_request.md"
PACKET_HTML = SLICE_ROOT / "artifact/old_file_status_normalization_approval_request.html"
BUILDER = SLICE_ROOT / "artifact/build_old_file_status_normalization_approval_request.py"
VERIFIER = SLICE_ROOT / "artifact/verify_old_file_status_normalization_approval_request.py"
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
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_p2_75", STRICT_STATUS_PACKAGE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load strict status package")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def strict_status(path: Path) -> str | None:
    parsed = strict_package().parse_strict_frontmatter_status(path.read_text(encoding="utf-8"))
    return parsed.get("status") if parsed.get("valid") else None


def normalized(text: str) -> str:
    return " ".join(text.split())


def verify_files(failures: list[str]) -> None:
    for name in REQUIRED_ROOT_FILES:
        add_failure(failures, (SLICE_ROOT / name).is_file(), f"missing root file: {name}")
    for path in [CONTRACT, PACKET_JSON, PACKET_MD, PACKET_HTML, BUILDER, VERIFIER]:
        add_failure(failures, path.is_file(), f"missing artifact: {path.name}")


def verify_packet(contract: dict, packet: dict, failures: list[str]) -> dict:
    add_failure(failures, packet.get("record_kind") == "sandbox_old_file_status_normalization_approval_request", "wrong record_kind")
    add_failure(failures, packet.get("slice_id") == SLICE_ID, "wrong slice_id")
    state = packet.get("current_state", {})
    for key, value in contract.get("expected_numbers", {}).items():
        add_failure(failures, state.get(key) == value, f"number mismatch: {key}")
    flags = packet.get("authority_flags", {})
    for key, value in contract.get("authority_flags", {}).items():
        add_failure(failures, flags.get(key) == value, f"authority flag mismatch: {key}")

    request = packet.get("request", {})
    exact_phrase = contract.get("exact_approval_phrase")
    add_failure(failures, request.get("exact_approval_phrase") == exact_phrase, "exact approval phrase mismatch")
    add_failure(failures, request.get("approval_status_now") == "not_collected", "approval status now is not not_collected")
    add_failure(failures, request.get("generic_language_is_not_approval") is True, "generic language guard missing")
    add_failure(failures, set(request.get("non_approval_examples", [])) == set(contract.get("non_approval_examples", [])), "non approval examples mismatch")

    scope = packet.get("future_if_approved_scope", {})
    expected_scope = contract.get("future_if_approved_scope", {})
    for key, value in expected_scope.items():
        add_failure(failures, scope.get(key) == value, f"future scope mismatch: {key}")

    digest = packet.get("dry_run_manifest_digest", {})
    add_failure(failures, digest.get("status_change_count") == 75, "dry-run status change count not 75")
    add_failure(failures, digest.get("all_changes_unapplied") is True, "not all dry-run changes are unapplied")
    add_failure(failures, digest.get("all_changes_require_explicit_user_approval") is True, "not all changes require explicit approval")

    examples = packet.get("approval_classifier_examples", [])
    exact_examples = [example for example in examples if example.get("input_text") == exact_phrase]
    generic_examples = [example for example in examples if example.get("input_text") != exact_phrase]
    add_failure(failures, len(exact_examples) == 1 and exact_examples[0].get("would_count_as_explicit_approval_in_future") is True, "exact phrase not accepted for future")
    add_failure(failures, generic_examples and all(example.get("would_count_as_explicit_approval_in_future") is False for example in generic_examples), "generic examples accepted as approval")
    add_failure(failures, all(example.get("current_packet_collects_approval") is False for example in examples), "packet claims to collect approval")

    md = PACKET_MD.read_text(encoding="utf-8") if PACKET_MD.is_file() else ""
    add_failure(failures, exact_phrase in md, "Markdown missing exact approval phrase")
    add_failure(failures, "This request packet does not collect approval" in md, "Markdown missing no-approval boundary")
    add_failure(failures, "body content edits allowed: `false`" in md, "Markdown missing body edit block")
    add_failure(failures, "Obsidian sync allowed: `false`" in md, "Markdown missing Obsidian sync block")
    return {
        "original_items": state.get("original_items"),
        "status_changes": state.get("status_changes"),
        "old_file_current_strict_final_gate": state.get("old_file_current_strict_final_gate"),
        "sidecar_closeout_passed": state.get("sidecar_closeout_passed"),
        "old_slice_writes_applied": state.get("old_slice_writes_applied"),
    }


def verify_fixtures(contract: dict, packet: dict, failures: list[str]) -> None:
    fixtures = [load_json(path) for path in (SLICE_ROOT / "fixtures").glob("*.json")]
    seen = {fixture.get("fixture_id") for fixture in fixtures}
    add_failure(failures, seen == set(contract.get("required_fixture_ids", [])), "fixture ids do not match contract")
    flags = packet.get("authority_flags", {})
    scope = packet.get("future_if_approved_scope", {})
    exact_phrase = contract.get("exact_approval_phrase")
    examples = {example.get("input_text"): example for example in packet.get("approval_classifier_examples", [])}
    for fixture in fixtures:
        fixture_id = fixture.get("fixture_id")
        if fixture_id == "exact-approval-phrase":
            example = examples.get(fixture.get("input_text"), {})
            for key, value in fixture.get("expected", {}).items():
                add_failure(failures, example.get(key) == value, f"{fixture_id} expected {key}")
            add_failure(failures, normalized(fixture.get("input_text", "")) == normalized(exact_phrase), "exact phrase fixture drift")
        elif fixture_id == "generic-continuation-not-approval":
            add_failure(
                failures,
                all(examples.get(text, {}).get("would_count_as_explicit_approval_in_future") is False for text in fixture.get("input_texts", [])),
                "generic fixture accepted as approval",
            )
        elif fixture_id == "future-scope-status-only":
            for key, value in fixture.get("expected", {}).items():
                add_failure(failures, scope.get(key) == value, f"{fixture_id} expected {key}")
        elif fixture_id == "request-is-not-approval":
            for key, value in fixture.get("expected", {}).items():
                add_failure(failures, flags.get(key) == value, f"{fixture_id} expected {key}")


def verify_failure_cases(contract: dict, failures: list[str]) -> None:
    matrix = load_json(SLICE_ROOT / "failure-cases/old-file-status-normalization-approval-request-failures.json")
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
    packet = load_json(PACKET_JSON) if PACKET_JSON.is_file() else {}
    summary = verify_packet(contract, packet, failures) if packet else {}
    verify_fixtures(contract, packet, failures)
    verify_failure_cases(contract, failures)
    if args.final_gate:
        verify_final_gate(failures)

    result = {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "fixture_count": len(list((SLICE_ROOT / "fixtures").glob("*.json"))),
            "failure_case_count": len(load_json(SLICE_ROOT / "failure-cases/old-file-status-normalization-approval-request-failures.json").get("failure_cases", [])),
            **summary,
            "final_gate": bool(args.final_gate),
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
