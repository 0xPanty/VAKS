from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


SLICE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = SLICE_ROOT.parents[3]
SLICE_ID = SLICE_ROOT.name
COPY_ROOT = SLICE_ROOT / "fixtures/target-copies"

CONTRACT = SLICE_ROOT / "artifact/sandbox_copy_executor_rehearsal_contract.json"
REHEARSAL_JSON = SLICE_ROOT / "artifact/sandbox_copy_executor_rehearsal.json"
REHEARSAL_MD = SLICE_ROOT / "artifact/sandbox_copy_executor_rehearsal.md"
REHEARSAL_HTML = SLICE_ROOT / "artifact/sandbox_copy_executor_rehearsal.html"
BUILDER = SLICE_ROOT / "artifact/build_sandbox_copy_executor_rehearsal.py"
VERIFIER = SLICE_ROOT / "artifact/verify_sandbox_copy_executor_rehearsal.py"
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def add_failure(failures: list[str], condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def strict_package():
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_p2_82", STRICT_STATUS_PACKAGE)
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
    for path in [CONTRACT, REHEARSAL_JSON, REHEARSAL_MD, REHEARSAL_HTML, BUILDER, VERIFIER]:
        add_failure(failures, path.is_file(), f"missing artifact: {path.name}")


def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def verify_rehearsal(contract: dict, rehearsal: dict, failures: list[str]) -> dict:
    add_failure(failures, rehearsal.get("record_kind") == "sandbox_copy_executor_rehearsal", "wrong record_kind")
    add_failure(failures, rehearsal.get("slice_id") == SLICE_ID, "wrong slice_id")

    summary = rehearsal.get("summary", {})
    for key, value in contract.get("expected_summary", {}).items():
        add_failure(failures, summary.get(key) == value, f"summary mismatch: {key}")

    gate = rehearsal.get("gate", {})
    for key, value in contract.get("expected_gate", {}).items():
        add_failure(failures, gate.get(key) == value, f"gate mismatch: {key}")

    flags = rehearsal.get("authority_flags", {})
    for key, value in contract.get("authority_flags", {}).items():
        add_failure(failures, flags.get(key) == value, f"authority flag mismatch: {key}")

    results = rehearsal.get("rehearsal_results", [])
    add_failure(failures, len(results) == contract["expected_summary"]["fixture_copy_count"], "rehearsal result count mismatch")
    add_failure(failures, len({item.get("sandbox_copy_path") for item in results}) == contract["expected_summary"]["fixture_copy_count"], "fixture copy path count mismatch")
    add_failure(failures, len({item.get("old_slice_id") for item in results}) == 20, "old slice count mismatch")
    for item in results:
        copy_path = SLICE_ROOT / item.get("sandbox_copy_path", "")
        add_failure(failures, is_within(copy_path, COPY_ROOT), f"copy path outside copy root: {item.get('sandbox_copy_path')}")
        add_failure(failures, copy_path.is_file(), f"missing copy: {item.get('sandbox_copy_path')}")
        if copy_path.is_file():
            final_bytes = copy_path.read_bytes()
            add_failure(failures, sha256_bytes(final_bytes) == item.get("final_copy_sha256"), f"final copy sha mismatch: {item.get('sandbox_copy_path')}")
            add_failure(failures, sha256_bytes(final_bytes) == item.get("original_sha256"), f"final copy not restored: {item.get('sandbox_copy_path')}")
            add_failure(failures, len(final_bytes) == item.get("original_byte_length"), f"final byte length mismatch: {item.get('sandbox_copy_path')}")
        add_failure(failures, item.get("copy_path_within_slice") is True, "copy path flag false")
        add_failure(failures, item.get("original_hash_matches_p2_80") is True, "original hash drift")
        add_failure(failures, item.get("copy_before_sha_matches_original") is True, "copy before hash mismatch")
        add_failure(failures, item.get("copy_before_byte_length") == item.get("original_byte_length"), "copy before byte length mismatch")
        add_failure(failures, item.get("after_status_matches_proposed") is True, "after status mismatch")
        add_failure(failures, item.get("body_unchanged_after_apply") is True, "body changed")
        add_failure(failures, item.get("body_bytes_unchanged_after_apply") is True, "body bytes changed")
        add_failure(failures, item.get("non_status_frontmatter_unchanged") is True, "non-status frontmatter changed")
        add_failure(failures, item.get("final_copy_status_matches_rollback") is True, "final status rollback mismatch")
        add_failure(failures, item.get("final_copy_sha_matches_original") is True, "final copy sha not original")
        add_failure(failures, item.get("final_copy_byte_sha_matches_original") is True, "final copy byte sha not original")
        add_failure(failures, item.get("final_copy_byte_length") == item.get("original_byte_length"), "final byte length not original")
        add_failure(failures, item.get("old_slice_write_applied") is False, "old slice write applied")
        add_failure(failures, item.get("write_target_family") == "sandbox_fixture_copy", "wrong write target family")

    md = REHEARSAL_MD.read_text(encoding="utf-8") if REHEARSAL_MD.is_file() else ""
    add_failure(failures, "fixture_copy_count: `75`" in md, "Markdown missing fixture count")
    add_failure(failures, "body_bytes_unchanged_after_apply_count: `75`" in md, "Markdown missing body byte count")
    add_failure(failures, "final_copy_sha_match_count: `75`" in md, "Markdown missing rollback hash count")
    add_failure(failures, "final_copy_byte_sha_match_count: `75`" in md, "Markdown missing byte rollback hash count")
    add_failure(failures, "executor_write_allowed_now: `false`" in md, "Markdown missing write block")
    add_failure(failures, "Fixture writes are confined to this sandbox" in md, "Markdown missing sandbox write boundary")

    return {
        "fixture_copy_count": summary.get("fixture_copy_count"),
        "fixture_apply_write_count": summary.get("fixture_apply_write_count"),
        "fixture_rollback_write_count": summary.get("fixture_rollback_write_count"),
        "copy_before_byte_sha_match_count": summary.get("copy_before_byte_sha_match_count"),
        "after_status_match_count": summary.get("after_status_match_count"),
        "body_unchanged_after_apply_count": summary.get("body_unchanged_after_apply_count"),
        "body_bytes_unchanged_after_apply_count": summary.get("body_bytes_unchanged_after_apply_count"),
        "final_copy_sha_match_count": summary.get("final_copy_sha_match_count"),
        "final_copy_byte_sha_match_count": summary.get("final_copy_byte_sha_match_count"),
        "rehearsal_failure_count": summary.get("rehearsal_failure_count"),
        "executor_write_allowed_now": gate.get("executor_write_allowed_now"),
        "old_slice_writes_applied": summary.get("old_slice_writes_applied"),
    }


def verify_fixtures(contract: dict, rehearsal: dict, failures: list[str]) -> None:
    fixtures = [load_json(path) for path in (SLICE_ROOT / "fixtures").glob("*.json")]
    seen = {fixture.get("fixture_id") for fixture in fixtures}
    add_failure(failures, seen == set(contract.get("required_fixture_ids", [])), "fixture ids do not match contract")
    summary = rehearsal.get("summary", {})
    gate = rehearsal.get("gate", {})
    flags = rehearsal.get("authority_flags", {})
    merged = {}
    merged.update(summary)
    merged.update(gate)
    merged.update(flags)
    for fixture in fixtures:
        fixture_id = fixture.get("fixture_id")
        for key, value in fixture.get("expected", {}).items():
            add_failure(failures, merged.get(key) == value, f"{fixture_id} expected {key}")


def verify_failure_cases(contract: dict, failures: list[str]) -> None:
    matrix = load_json(SLICE_ROOT / "failure-cases/sandbox-copy-executor-rehearsal-failures.json")
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
    rehearsal = load_json(REHEARSAL_JSON) if REHEARSAL_JSON.is_file() else {}
    summary = verify_rehearsal(contract, rehearsal, failures) if rehearsal else {}
    verify_fixtures(contract, rehearsal, failures)
    verify_failure_cases(contract, failures)
    if args.final_gate:
        verify_final_gate(failures)

    result = {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "fixture_count": len(list((SLICE_ROOT / "fixtures").glob("*.json"))),
            "failure_case_count": len(load_json(SLICE_ROOT / "failure-cases/sandbox-copy-executor-rehearsal-failures.json").get("failure_cases", [])),
            **summary,
            "final_gate": bool(args.final_gate),
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
