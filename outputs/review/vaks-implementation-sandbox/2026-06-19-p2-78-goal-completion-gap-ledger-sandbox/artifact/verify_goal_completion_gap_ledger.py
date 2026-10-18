from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


SLICE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = SLICE_ROOT.parents[3]
SLICE_ID = SLICE_ROOT.name

CONTRACT = SLICE_ROOT / "artifact/goal_completion_gap_ledger_contract.json"
LEDGER_JSON = SLICE_ROOT / "artifact/goal_completion_gap_ledger.json"
LEDGER_MD = SLICE_ROOT / "artifact/goal_completion_gap_ledger.md"
LEDGER_HTML = SLICE_ROOT / "artifact/goal_completion_gap_ledger.html"
BUILDER = SLICE_ROOT / "artifact/build_goal_completion_gap_ledger.py"
VERIFIER = SLICE_ROOT / "artifact/verify_goal_completion_gap_ledger.py"
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
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_p2_78", STRICT_STATUS_PACKAGE)
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
    for path in [CONTRACT, LEDGER_JSON, LEDGER_MD, LEDGER_HTML, BUILDER, VERIFIER]:
        add_failure(failures, path.is_file(), f"missing artifact: {path.name}")
    add_failure(failures, (SLICE_ROOT / "fixtures").is_dir(), "missing fixtures dir")
    add_failure(failures, (SLICE_ROOT / "failure-cases").is_dir(), "missing failure-cases dir")


def verify_ledger(contract: dict, ledger: dict, failures: list[str]) -> dict:
    add_failure(failures, ledger.get("record_kind") == "sandbox_goal_completion_gap_ledger", "wrong record_kind")
    add_failure(failures, ledger.get("slice_id") == SLICE_ID, "wrong slice_id")

    summary = ledger.get("summary", {})
    for key, value in contract.get("expected_summary", {}).items():
        add_failure(failures, summary.get(key) == value, f"summary mismatch: {key}")

    verdict = ledger.get("goal_verdict", {})
    for key, value in contract.get("expected_goal_verdict", {}).items():
        add_failure(failures, verdict.get(key) == value, f"goal verdict mismatch: {key}")

    blockers = ledger.get("blocking_gates", {})
    for key, value in contract.get("expected_blockers", {}).items():
        add_failure(failures, blockers.get(key) == value, f"blocker mismatch: {key}")

    flags = ledger.get("authority_flags", {})
    for key, value in contract.get("authority_flags", {}).items():
        add_failure(failures, flags.get(key) == value, f"authority flag mismatch: {key}")

    forbidden_claims = set(ledger.get("forbidden_claims", []))
    for claim in [
        "all_original_20_current_strict_final_gate_complete",
        "p2_75_request_packet_is_approval",
        "p2_76_clean_preflight_is_approval",
        "p2_77_readiness_gate_executed_normalization",
        "product_acceptance_is_user_approval_for_old_file_write",
    ]:
        add_failure(failures, claim in forbidden_claims, f"missing forbidden claim: {claim}")

    ladder = {item.get("state"): item for item in ledger.get("completion_ladder", [])}
    add_failure(failures, ladder.get("old_slice_current_strict_final_gate", {}).get("verdict") == "not_complete", "old strict final gate not marked incomplete")
    add_failure(failures, ladder.get("old_file_status_normalization_executor", {}).get("verdict") == "blocked", "executor not marked blocked")

    md = LEDGER_MD.read_text(encoding="utf-8") if LEDGER_MD.is_file() else ""
    add_failure(failures, "goal_complete_now: `false`" in md, "Markdown missing false completion verdict")
    add_failure(failures, "old_slice_current_strict_final_gate_count: `0`" in md, "Markdown missing zero old strict count")
    add_failure(failures, "pending_status_change_count: `75`" in md, "Markdown missing pending status change count")
    add_failure(failures, "executor_write_allowed: `false`" in md, "Markdown missing executor write block")

    return {
        "goal_complete_now": verdict.get("goal_complete_now"),
        "completion_state": verdict.get("completion_state"),
        "legacy_product_acceptance_evidence_count": summary.get("legacy_product_acceptance_evidence_count"),
        "sidecar_closeout_passed_count": summary.get("sidecar_closeout_passed_count"),
        "old_slice_current_strict_final_gate_count": summary.get("old_slice_current_strict_final_gate_count"),
        "pending_status_change_count": summary.get("pending_status_change_count"),
        "executor_write_allowed": blockers.get("executor_write_allowed"),
        "old_slice_writes_applied": summary.get("old_slice_writes_applied"),
    }


def verify_fixtures(contract: dict, ledger: dict, failures: list[str]) -> None:
    fixtures = [load_json(path) for path in (SLICE_ROOT / "fixtures").glob("*.json")]
    seen = {fixture.get("fixture_id") for fixture in fixtures}
    add_failure(failures, seen == set(contract.get("required_fixture_ids", [])), "fixture ids do not match contract")

    summary = ledger.get("summary", {})
    verdict = ledger.get("goal_verdict", {})
    blockers = ledger.get("blocking_gates", {})
    flags = ledger.get("authority_flags", {})
    safe_next = set(ledger.get("safe_next_work", []))
    forbidden_next = set(ledger.get("forbidden_next_work_without_exact_approval", []))

    merged = {}
    merged.update(summary)
    merged.update(verdict)
    merged.update(blockers)
    merged.update(flags)

    for fixture in fixtures:
        fixture_id = fixture.get("fixture_id")
        if fixture_id in {"current-state-not-complete", "exact-approval-required-before-old-normalization"}:
            for key, value in fixture.get("expected", {}).items():
                add_failure(failures, merged.get(key) == value, f"{fixture_id} expected {key}")
        elif fixture_id == "strict-complete-claim-rejected":
            add_failure(failures, fixture.get("expected", {}).get("claim_allowed") is False, f"{fixture_id} fixture should reject claim")
            add_failure(failures, verdict.get("claim_all_original_20_current_strict_complete_allowed") is False, f"{fixture_id} ledger allows strict complete claim")
        elif fixture_id == "safe-next-work-without-old-writes":
            for item in fixture.get("expected_allowed_next_work", []):
                add_failure(failures, item in safe_next, f"{fixture_id} missing allowed next work {item}")
            for item in fixture.get("expected_forbidden_next_work", []):
                add_failure(failures, item in forbidden_next, f"{fixture_id} missing forbidden next work {item}")
        elif fixture_id == "dirty-tree-baseline-is-not-completion-evidence":
            expected = fixture.get("expected", {})
            add_failure(failures, expected.get("dirty_tree_can_prove_completion") is False, f"{fixture_id} dirty tree fixture is unsafe")
            add_failure(failures, ledger.get("goal_verdict", {}).get("goal_complete_now") is False, f"{fixture_id} ledger claims completion")


def verify_failure_cases(contract: dict, failures: list[str]) -> None:
    matrix = load_json(SLICE_ROOT / "failure-cases/goal-completion-gap-ledger-failures.json")
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
    ledger = load_json(LEDGER_JSON) if LEDGER_JSON.is_file() else {}
    summary = verify_ledger(contract, ledger, failures) if ledger else {}
    verify_fixtures(contract, ledger, failures)
    verify_failure_cases(contract, failures)
    if args.final_gate:
        verify_final_gate(failures)

    result = {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "fixture_count": len(list((SLICE_ROOT / "fixtures").glob("*.json"))),
            "failure_case_count": len(load_json(SLICE_ROOT / "failure-cases/goal-completion-gap-ledger-failures.json").get("failure_cases", [])),
            **summary,
            "final_gate": bool(args.final_gate),
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
