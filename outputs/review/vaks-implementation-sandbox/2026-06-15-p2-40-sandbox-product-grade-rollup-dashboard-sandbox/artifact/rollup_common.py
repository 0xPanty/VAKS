from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p2-40-sandbox-product-grade-rollup-dashboard-sandbox"
ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[3]
SANDBOX_ROOT = ROOT.parent

VERSION = "sandbox-product-grade-rollup-v1"
TRUTH_BOUNDARY = "sandbox_rollup_status_not_authority"
PURPOSE = "read-only product-grade sandbox status rollup for operator review"
WRITE_SCOPE = f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"

REQUIRED_REPORTS = [
    "slice-plan.md",
    "source-map.md",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]

OPERATION_FLAGS = [
    "formal_vault_read",
    "formal_vault_scan",
    "formal_vault_write",
    "formal_vault_hash",
    "formal_vault_snapshot",
    "formal_vault_state_check",
    "obsidian_sync",
    "commit",
    "push",
    "promotion",
    "dependency_install",
    "background_service",
    "mcp_write_tool",
    "hooks",
    "approval_collection",
    "user_instruction_collection",
    "user_wording_storage",
    "command_emitted",
    "execution_permission_granted",
    "execution_performed",
    "action_basis_creation",
    "reviewed_knowledge_creation",
    "evidence_support_creation",
    "mainline_merge",
    "dirty_tree_repair",
    "auto_advance",
]

ROLLUP_CONTROLS = [
    "read_only_scan",
    "sandbox_only_output",
    "product_pass_is_sandbox_only",
    "verification_status_is_file_evidence",
    "no_formal_vault_claim",
    "no_mainline_claim",
    "no_action_basis",
    "no_evidence_support",
    "no_reviewed_knowledge",
    "no_auto_advance",
]

REQUIRED_NON_CLAIMS = [
    "not formal vault approval",
    "not formal vault state",
    "not formal vault access",
    "not Obsidian sync",
    "not user approval",
    "not user instruction",
    "not execution permission",
    "not command surface",
    "not reviewed knowledge",
    "not evidence support",
    "not action basis",
    "not mainline readiness",
    "not promotion approval",
    "not dirty-tree repair",
    "not auto advance",
]


def rel(path: Path) -> str:
    return path.resolve().relative_to(WORKSPACE).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_status(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^status:\s*(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def text_contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="ignore")


def source_slice_dirs() -> list[Path]:
    dirs = []
    for path in sorted(SANDBOX_ROOT.iterdir(), key=lambda item: item.name):
        if path.is_dir() and path.name < SLICE_ID:
            dirs.append(path)
    return dirs


def scan_source_slices() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for directory in source_slice_dirs():
        reports = {name: directory / name for name in REQUIRED_REPORTS}
        product_path = reports["product-acceptance-report.md"]
        verification_path = reports["verification.md"]
        reviewer_path = reports["reviewer-report.md"]
        boundary_path = reports["boundary-audit.md"]
        next_path = reports["next-step.md"]

        product_status = parse_status(product_path)
        verification_status = parse_status(verification_path)
        reviewer_status = parse_status(reviewer_path)
        boundary_status = parse_status(boundary_path)
        next_status = parse_status(next_path)
        product_text = product_path.read_text(encoding="utf-8", errors="ignore") if product_path.exists() else ""

        missing_reports = [name for name, path in reports.items() if not path.exists()]
        rows.append(
            {
                "slice_id": directory.name,
                "path": rel(directory),
                "report_hashes": {
                    name: sha256_file(path) if path.exists() else None for name, path in reports.items()
                },
                "missing_reports": missing_reports,
                "product_status": product_status,
                "product_pass": bool(product_status and product_status.startswith("pass_product_grade") and "PASS_PRODUCT_GRADE" in product_text),
                "verification_status": verification_status,
                "verification_present": verification_path.exists(),
                "reviewer_status": reviewer_status,
                "boundary_status": boundary_status,
                "next_status": next_status,
                "revision_mentions": product_text.count("REVISE_BEFORE_NEXT") + product_text.count("reviewer_revise") + product_text.count("REVIEWER_REVISE"),
                "truth_boundary": "sandbox_only_status_evidence",
                "authority": {
                    "formal_vault_approval": False,
                    "reviewed_knowledge": False,
                    "evidence_support": False,
                    "action_basis": False,
                    "mainline_ready": False,
                    "execution_permission": False,
                },
            }
        )
    return rows


def default_rollup(view: str = "operator-rollup") -> dict[str, Any]:
    slices = scan_source_slices()
    product_pass_count = sum(1 for item in slices if item["product_pass"])
    verification_present_count = sum(1 for item in slices if item["verification_present"])
    non_pass_slices = [item["slice_id"] for item in slices if not item["product_pass"]]
    missing_verification_slices = [item["slice_id"] for item in slices if not item["verification_present"]]
    revision_slices = [item["slice_id"] for item in slices if item["revision_mentions"] > 0]
    return {
        "record_kind": "sandbox_product_grade_rollup_dashboard",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
        "view": view,
        "source_root": rel(SANDBOX_ROOT),
        "source_slice_count": len(slices),
        "product_pass_count": product_pass_count,
        "verification_present_count": verification_present_count,
        "non_pass_slices": non_pass_slices,
        "missing_verification_slices": missing_verification_slices,
        "revision_slices": revision_slices,
        "source_slices": slices,
        "blocked_operations": {name: False for name in OPERATION_FLAGS},
        "rollup_controls": {name: True for name in ROLLUP_CONTROLS},
        "required_non_claims": list(REQUIRED_NON_CLAIMS),
        "operator_summary": {
            "all_sources_product_pass": product_pass_count == len(slices) and len(slices) > 0,
            "all_sources_have_verification": verification_present_count == len(slices) and len(slices) > 0,
            "rollup_is_mainline_authority": False,
            "rollup_is_formal_vault_authority": False,
            "rollup_is_action_basis": False,
        },
    }


def validate_rollup(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "record_kind": "sandbox_product_grade_rollup_dashboard",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
        "source_root": rel(SANDBOX_ROOT),
    }
    for key, value in expected.items():
        if data.get(key) != value:
            errors.append(f"{key}_mismatch")

    current = default_rollup(data.get("view", "operator-rollup"))
    for key in [
        "source_slice_count",
        "product_pass_count",
        "verification_present_count",
        "non_pass_slices",
        "missing_verification_slices",
        "revision_slices",
        "source_slices",
    ]:
        if data.get(key) != current.get(key):
            errors.append(f"{key}_mismatch")

    if data.get("source_slice_count", 0) < 39:
        errors.append("source_slice_count_too_low")
    if data.get("product_pass_count") != data.get("source_slice_count"):
        errors.append("not_all_sources_product_pass")
    if data.get("verification_present_count") != data.get("source_slice_count"):
        errors.append("not_all_sources_have_verification")
    if data.get("non_pass_slices"):
        errors.append("non_pass_slices_present")
    if data.get("missing_verification_slices"):
        errors.append("missing_verification_slices_present")

    blocked = data.get("blocked_operations", {})
    for name in OPERATION_FLAGS:
        if blocked.get(name) is not False:
            errors.append(f"operation_not_false:{name}")

    controls = data.get("rollup_controls", {})
    for name in ROLLUP_CONTROLS:
        if controls.get(name) is not True:
            errors.append(f"rollup_control_not_true:{name}")

    non_claims = set(data.get("required_non_claims", []))
    if not set(REQUIRED_NON_CLAIMS).issubset(non_claims):
        errors.append("required_non_claims_missing")

    summary = data.get("operator_summary", {})
    if summary.get("all_sources_product_pass") is not True:
        errors.append("summary_all_sources_product_pass_not_true")
    if summary.get("all_sources_have_verification") is not True:
        errors.append("summary_all_sources_have_verification_not_true")
    for flag in ["rollup_is_mainline_authority", "rollup_is_formal_vault_authority", "rollup_is_action_basis"]:
        if summary.get(flag) is not False:
            errors.append(f"summary_flag_not_false:{flag}")

    for item in data.get("source_slices", []):
        if item.get("missing_reports"):
            errors.append(f"source_missing_reports:{item.get('slice_id')}")
        if not item.get("product_pass"):
            errors.append(f"source_product_not_pass:{item.get('slice_id')}")
        if not item.get("verification_present"):
            errors.append(f"source_verification_missing:{item.get('slice_id')}")
        authority = item.get("authority", {})
        for key, value in authority.items():
            if value is not False:
                errors.append(f"source_authority_not_false:{item.get('slice_id')}:{key}")

    return errors


def make_failure_cases(base: dict[str, Any]) -> dict[str, list[str]]:
    cases: dict[str, list[str]] = {}
    index = 1

    def add(name: str, mutate, expected: list[str]) -> None:
        nonlocal index
        sample = copy.deepcopy(base)
        mutate(sample)
        filename = f"{index:03d}-{name}.json"
        write_json(ROOT / "failure-cases" / filename, sample)
        cases[filename] = expected
        index += 1

    for key in ["record_kind", "slice_id", "version", "truth_boundary", "purpose", "write_scope", "source_root"]:
        add(f"top-level-{key}", lambda sample, key=key: sample.__setitem__(key, "wrong"), [f"{key}_mismatch"])

    add(
        "summary-source_slice_count",
        lambda sample: sample.__setitem__("source_slice_count", 0),
        [
            "source_slice_count_mismatch",
            "source_slice_count_too_low",
            "not_all_sources_product_pass",
            "not_all_sources_have_verification",
        ],
    )
    add(
        "summary-product_pass_count",
        lambda sample: sample.__setitem__("product_pass_count", 0),
        ["product_pass_count_mismatch", "not_all_sources_product_pass"],
    )
    add(
        "summary-verification_present_count",
        lambda sample: sample.__setitem__("verification_present_count", 0),
        ["verification_present_count_mismatch", "not_all_sources_have_verification"],
    )

    add("non-pass-slice-present", lambda sample: sample.__setitem__("non_pass_slices", ["fake-slice"]), ["non_pass_slices_mismatch", "non_pass_slices_present"])
    add("missing-verification-present", lambda sample: sample.__setitem__("missing_verification_slices", ["fake-slice"]), ["missing_verification_slices_mismatch", "missing_verification_slices_present"])

    for op in OPERATION_FLAGS:
        add(f"operation-{op}", lambda sample, op=op: sample["blocked_operations"].__setitem__(op, True), [f"operation_not_false:{op}"])

    for control in ROLLUP_CONTROLS:
        add(
            f"control-{control}",
            lambda sample, control=control: sample["rollup_controls"].__setitem__(control, False),
            [f"rollup_control_not_true:{control}"],
        )

    for non_claim in REQUIRED_NON_CLAIMS:
        safe_name = non_claim.replace(" ", "-").replace("/", "-")
        add(
            f"missing-non-claim-{safe_name}",
            lambda sample, non_claim=non_claim: sample["required_non_claims"].remove(non_claim),
            ["required_non_claims_missing"],
        )

    for flag in ["rollup_is_mainline_authority", "rollup_is_formal_vault_authority", "rollup_is_action_basis"]:
        add(
            f"summary-authority-{flag}",
            lambda sample, flag=flag: sample["operator_summary"].__setitem__(flag, True),
            [f"summary_flag_not_false:{flag}"],
        )

    if base["source_slices"]:
        add(
            "source-product-pass-false",
            lambda sample: sample["source_slices"][0].__setitem__("product_pass", False),
            ["source_slices_mismatch", f"source_product_not_pass:{base['source_slices'][0]['slice_id']}"],
        )
        add(
            "source-verification-missing",
            lambda sample: sample["source_slices"][0].__setitem__("verification_present", False),
            ["source_slices_mismatch", f"source_verification_missing:{base['source_slices'][0]['slice_id']}"],
        )
        add(
            "source-authority-mainline",
            lambda sample: sample["source_slices"][0]["authority"].__setitem__("mainline_ready", True),
            ["source_slices_mismatch", f"source_authority_not_false:{base['source_slices'][0]['slice_id']}:mainline_ready"],
        )
        add(
            "source-report-hash-drift",
            lambda sample: sample["source_slices"][0]["report_hashes"].__setitem__("product-acceptance-report.md", "0" * 64),
            ["source_slices_mismatch"],
        )

    return cases


def reset_generated() -> None:
    for directory in ["fixtures", "failure-cases", "prototype/sandbox-product-grade-rollup-dashboard", "rollup-packets"]:
        path = ROOT / directory
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)


def validate_failure_cases() -> dict[str, Any]:
    oracle_path = ROOT / "artifact" / "failure-case-oracle.json"
    failure_dir = ROOT / "failure-cases"
    if not oracle_path.exists():
        return {
            "count": 0,
            "actual_file_count": len(list(failure_dir.glob("*.json"))) if failure_dir.exists() else 0,
            "orphan_count": 0,
            "mismatches": [{"file": "failure-case-oracle.json", "expected": ["oracle_present"], "actual": ["missing_oracle"]}],
        }
    oracle = read_json(oracle_path).get("cases", {})
    if not oracle:
        return {
            "count": 0,
            "actual_file_count": len(list(failure_dir.glob("*.json"))) if failure_dir.exists() else 0,
            "orphan_count": 0,
            "mismatches": [{"file": "failure-case-oracle.json", "expected": ["oracle_non_empty"], "actual": ["empty_oracle"]}],
        }
    actual_files = {path.name for path in failure_dir.glob("*.json")} if failure_dir.exists() else set()
    expected_files = set(oracle)
    mismatches = []
    for extra in sorted(actual_files - expected_files):
        mismatches.append({"file": extra, "expected": ["not_present_outside_oracle"], "actual": ["orphan_failure_case_file"]})
    for name, expected in oracle.items():
        path = failure_dir / name
        if not path.exists():
            mismatches.append({"file": name, "expected": expected, "actual": ["missing_failure_case"]})
            continue
        actual = validate_rollup(read_json(path))
        if sorted(actual) != sorted(expected):
            mismatches.append({"file": name, "expected": expected, "actual": actual})
    return {
        "count": len(oracle),
        "actual_file_count": len(actual_files),
        "orphan_count": len(actual_files - expected_files),
        "mismatches": mismatches,
    }


def validate_fixtures() -> dict[str, Any]:
    details = []
    errors = []
    for path in sorted((ROOT / "fixtures").glob("*.json")):
        fixture_errors = validate_rollup(read_json(path))
        details.append({"file": path.name, "errors": fixture_errors})
        if fixture_errors:
            errors.append({"file": path.name, "errors": fixture_errors})
    if not details:
        errors.append({"file": "fixtures", "errors": ["missing_positive_fixtures"]})
    return {"count": len(details), "fixtures": details, "errors": errors}


def validate_prototype() -> dict[str, Any]:
    prototype = ROOT / "prototype" / "sandbox-product-grade-rollup-dashboard"
    issues: list[str] = []
    expected = default_rollup()
    for item in ["index.html", "app.js", "receipt.json"]:
        if not (prototype / item).exists():
            issues.append(f"missing_prototype_file:{item}")
    if (prototype / "index.html").exists():
        html_raw = (prototype / "index.html").read_text(encoding="utf-8")
        html = html_raw.lower()
        for forbidden in ["<form", "download", "contenteditable", "<a ", "h:\\obsidian"]:
            if forbidden in html:
                issues.append(f"prototype_forbidden:{forbidden}")
        if html.count("data-rollup-card=") != 4:
            issues.append("prototype_rollup_card_count_mismatch")
        if html.count("<tr data-slice-row=") != expected["source_slice_count"]:
            issues.append("prototype_slice_row_count_mismatch")
        for value in [
            str(expected["source_slice_count"]),
            str(expected["product_pass_count"]),
            str(expected["verification_present_count"]),
            str(len(expected["revision_slices"])),
        ]:
            if f">{value}<" not in html_raw:
                issues.append(f"prototype_summary_value_missing:{value}")
    if (prototype / "receipt.json").exists():
        receipt = read_json(prototype / "receipt.json")
        for flag in [
            "formal_vault_accessed",
            "sync_performed",
            "write_performed",
            "commit_performed",
            "push_performed",
            "promotion_performed",
            "mainline_ready",
            "action_basis_created",
            "reviewed_knowledge_created",
            "evidence_support_created",
            "auto_advanced",
        ]:
            if receipt.get(flag) is not False:
                issues.append(f"prototype_receipt_flag_not_false:{flag}")
        if not set(REQUIRED_NON_CLAIMS).issubset(set(receipt.get("non_claims", []))):
            issues.append("prototype_receipt_non_claims_missing")
    return {"prototype_path": str(prototype), "issues": issues}


def validate_required_reports(final_gate: bool = False) -> dict[str, Any]:
    required = {
        "slice-plan.md": "built_pending_review",
        "source-map.md": "built_pending_review",
        "verification.md": "local_verification_passed_pending_review",
    }
    if final_gate:
        required.update(
            {
                "reviewer-report.md": "reviewer_pass",
                "boundary-audit.md": "boundary_pass",
                "product-acceptance-report.md": "pass_product_grade",
                "next-step.md": "pass_product_grade_pending_user_next_slice_decision",
            }
        )
    statuses: dict[str, str | None] = {}
    issues: list[str] = []
    for name, expected in required.items():
        status = parse_status(ROOT / name)
        statuses[name] = status
        if status != expected:
            issues.append(f"bad_status:{name}:{status}:expected:{expected}")
    return {"statuses": statuses, "issues": issues}


def validate_all(final_gate: bool = False) -> dict[str, Any]:
    fixture = ROOT / "fixtures" / "valid-rollup-dashboard.json"
    config_errors = validate_rollup(read_json(fixture)) if fixture.exists() else ["missing_valid_fixture"]
    rollup_data_path = ROOT / "artifact" / "rollup-data.json"
    rollup_data_errors = (
        validate_rollup(read_json(rollup_data_path)) if rollup_data_path.exists() else ["missing_rollup_data"]
    )
    fixtures = validate_fixtures()
    failure_cases = validate_failure_cases()
    prototype = validate_prototype()
    reports = validate_required_reports(final_gate=final_gate)
    failures: list[str] = []
    failures.extend(config_errors)
    failures.extend([f"rollup_data_error:{item}" for item in rollup_data_errors])
    failures.extend([f"fixture_error:{item['file']}" for item in fixtures["errors"]])
    failures.extend([f"failure_case_mismatch:{item['file']}" for item in failure_cases["mismatches"]])
    failures.extend(prototype["issues"])
    failures.extend(reports["issues"])
    return {
        "slice_id": SLICE_ID,
        "passed": not failures,
        "failures": failures,
        "valid_config_errors": config_errors,
        "rollup_data_errors": rollup_data_errors,
        "positive_fixtures": fixtures,
        "failure_cases": failure_cases,
        "prototype": prototype,
        "required_reports": reports,
        "source_summary": {
            "source_slice_count": default_rollup()["source_slice_count"],
            "product_pass_count": default_rollup()["product_pass_count"],
            "verification_present_count": default_rollup()["verification_present_count"],
            "revision_slices": default_rollup()["revision_slices"],
        },
        "non_claims": REQUIRED_NON_CLAIMS,
    }
